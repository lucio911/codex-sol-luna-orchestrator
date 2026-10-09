#!/usr/bin/env python3
"""Install the Codex skill and named Luna subagent safely (Python 3.11+)."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / ".agents" / "skills" / "sol-luna-orchestrator"
AGENT_SOURCE = ROOT / "codex" / "agents" / "luna_executor.toml"
MODEL_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
EFFORT_CHOICES = ("low", "medium", "high", "xhigh", "max")


def get_destinations(scope: str, project_root: Path | None = None, home: Path | None = None):
    if scope == "user":
        root = (home or Path.home()).expanduser().resolve()
    else:
        root = (project_root or Path.cwd()).expanduser().resolve()
    return (
        root / ".agents" / "skills" / "sol-luna-orchestrator",
        root / ".codex" / "agents" / "luna_executor.toml",
        root / ".codex" / "config.toml",
    )


def validate_model_id(model: str) -> str:
    if not MODEL_PATTERN.fullmatch(model):
        raise ValueError(f"Invalid model identifier: {model!r}")
    return model


def backup_path(path: Path) -> Path:
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = path.with_name(path.name + ".bak-" + timestamp)
    candidate = base
    index = 1
    while candidate.exists():
        candidate = path.with_name(base.name + f"-{index}")
        index += 1
    return candidate


def replace_file_atomic(path: Path, contents: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmpname = tempfile.mkstemp(prefix=".sol-luna-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(contents)
        os.replace(tmpname, path)
    finally:
        if os.path.exists(tmpname):
            os.unlink(tmpname)


def same_tree(src: Path, dst: Path) -> bool:
    if not dst.is_dir():
        return False
    src_files = {p.relative_to(src) for p in src.rglob("*") if p.is_file()}
    dst_files = {p.relative_to(dst) for p in dst.rglob("*") if p.is_file()}
    return src_files == dst_files and all((src / p).read_bytes() == (dst / p).read_bytes() for p in src_files)


def modify_toml(text: str, values: dict[str, str], section: str | None) -> str:
    """Update only top-level / an existing named table, preserving unrelated text.

    Requires valid TOML both before and after. Do not attempt to resolve dotted
    keys or change arrays of tables; targets here are unambiguous bare keys.
    """
    if text.strip():
        tomllib.loads(text)
    lines = text.splitlines(keepends=True)
    headers = [(i, m.group(1).strip()) for i, ln in enumerate(lines)
               if (m := re.match(r"^\s*\[([^\[\]]+)\]\s*(?:#.*)?$", ln))]
    if section is None:
        start, end = 0, headers[0][0] if headers else len(lines)
    else:
        matches = [i for i, (_, name) in enumerate(headers) if name == section]
        if len(matches) > 1:
            raise ValueError(f"Duplicate table [{section}]")
        if not matches:
            if text and not text.endswith("\n"):
                text += "\n"
            return modify_toml(text + f"\n[{section}]\n", values, section)
        idx = matches[0]
        start = headers[idx][0] + 1
        end = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
    found = set()
    for i in range(start, end):
        for key, value in values.items():
            if re.match(rf"^\s*{re.escape(key)}\s*=", lines[i]):
                if key in found:
                    raise ValueError(f"Duplicate key: {key}")
                indent = re.match(r"^(\s*)", lines[i]).group(1)
                lines[i] = f"{indent}{key} = {value}\n"
                found.add(key)
    to_add = [f"{key} = {value}\n" for key, value in values.items() if key not in found]
    if to_add and end > 0 and lines[end - 1] and not lines[end - 1].endswith("\n"):
        lines[end - 1] += "\n"
    lines[end:end] = to_add
    result = "".join(lines)
    tomllib.loads(result)
    return result


def desired_config(existing: str, *, planner_model: str | None = None,
                   planner_effort: str | None = None) -> str:
    result = existing
    if planner_model:
        model = validate_model_id(planner_model)
        result = modify_toml(result, {"model": f'"{model}"'}, None)
    if planner_model or planner_effort:
        effort = planner_effort or "high"
        if effort not in EFFORT_CHOICES:
            raise ValueError(f"Unsupported primary reasoning effort: {effort}")
        result = modify_toml(result, {"model_reasoning_effort": f'"{effort}"'}, None)
    result = modify_toml(result, {"enabled": "true", "max_concurrent_threads_per_session": "2"}, "agents")
    return result

def install(*, scope: str, project_root: Path | None = None, home: Path | None = None,
            executor_model: str = "gpt-6-luna", executor_effort: str = "high",
            planner_model: str | None = None, planner_effort: str | None = None,
            configure_defaults: bool = False, force: bool = False, dry_run: bool = False) -> list[str]:
    validate_model_id(executor_model)
    if planner_model:
        validate_model_id(planner_model)
    if executor_effort not in EFFORT_CHOICES or (planner_effort is not None and planner_effort not in EFFORT_CHOICES):
        raise ValueError("Reasoning effort must be one of " + ", ".join(EFFORT_CHOICES))
    skill_dst, agent_dst, cfg_dst = get_destinations(scope, project_root, home)
    agent_src = AGENT_SOURCE.read_text(encoding="utf-8")
    agent_text = re.sub(r'(?m)^model\s*=\s*"[^"]+"\s*$', f'model = "{executor_model}"', agent_src, count=1)
    agent_text = re.sub(
        r'(?m)^model_reasoning_effort\s*=\s*"[^"]+"\s*$',
        f'model_reasoning_effort = "{executor_effort}"',
        agent_text, count=1,
    )
    tomllib.loads(agent_text)
    changes = []
    # Preflight all collisions before making any changes.
    skill_same = same_tree(SKILL_SOURCE, skill_dst)
    if skill_dst.exists() and not skill_same and not force:
        raise FileExistsError(f"Skill already exists with different contents: {skill_dst}. Use --force to back up and replace it.")
    agent_same = agent_dst.is_file() and agent_dst.read_text(encoding="utf-8") == agent_text
    if agent_dst.exists() and not agent_same and not force:
        raise FileExistsError(f"Agent already exists with different contents: {agent_dst}. Use --force to back up and replace it.")
    if configure_defaults:
        old_cfg = cfg_dst.read_text(encoding="utf-8") if cfg_dst.exists() else ""
        new_cfg = desired_config(old_cfg, planner_model=planner_model, planner_effort=planner_effort)
    else:
        old_cfg, new_cfg = "", ""
        if planner_model or planner_effort:
            raise ValueError("--primary-model/--primary-effort requires --configure-defaults")

    if not skill_same:
        changes.append(f"Install skill -> {skill_dst}")
        if not dry_run:
            if skill_dst.exists():
                destination = backup_path(skill_dst)
                skill_dst.rename(destination)
                changes.append(f"Backup prior skill -> {destination}")
            skill_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(SKILL_SOURCE, skill_dst)
    if not agent_same:
        changes.append(f"Install agent ({executor_model}, effort={executor_effort}) -> {agent_dst}")
        if not dry_run:
            if agent_dst.exists():
                destination = backup_path(agent_dst)
                agent_dst.rename(destination)
                changes.append(f"Backup prior agent -> {destination}")
            replace_file_atomic(agent_dst, agent_text)
    if configure_defaults and old_cfg != new_cfg:
        changes.append(f"Update Codex configuration -> {cfg_dst}")
        if not dry_run:
            if cfg_dst.exists():
                destination = backup_path(cfg_dst)
                shutil.copy2(cfg_dst, destination)
                changes.append(f"Backup prior config -> {destination}")
            replace_file_atomic(cfg_dst, new_cfg)
    if not changes:
        changes.append("Already installed; no changes needed.")
    return changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-root", type=Path, default=None, help="Project root for --scope project; default: current directory")
    parser.add_argument("--executor-model", default="gpt-6-luna", help="Model ID for luna_executor (default: gpt-6-luna)")
    parser.add_argument("--executor-effort", choices=EFFORT_CHOICES, default="high", help="Luna reasoning effort")
    parser.add_argument("--configure-defaults", action="store_true", help="Opt in to safely merging multi-agent settings into config.toml")
    parser.add_argument("--primary-model", default=None, help="Set primary Sol model; requires --configure-defaults")
    parser.add_argument("--primary-effort", choices=EFFORT_CHOICES, default=None, help="Primary reasoning effort; requires --configure-defaults")
    parser.add_argument("--force", action="store_true", help="Back up and replace conflicting skill/agent files")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing files")
    args = parser.parse_args(argv)
    try:
        messages = install(scope=args.scope, project_root=args.project_root, executor_model=args.executor_model,
                           planner_model=args.primary_model, planner_effort=args.primary_effort,
                           executor_effort=args.executor_effort, configure_defaults=args.configure_defaults,
                           force=args.force, dry_run=args.dry_run)
        for message in messages:
            print(("[dry-run] " if args.dry_run else "") + message)
        if not args.configure_defaults:
            print("Tip: use --configure-defaults --primary-model gpt-6.1-sol to opt into primary-model/config edits.")
        print("Note: file installation does not prove live model routing; verify by spawning the named subagent in Codex.")
        return 0
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
