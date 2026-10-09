#!/usr/bin/env python3
"""Offline package validation without external dependencies."""
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/sol-luna-orchestrator/SKILL.md"


def validate() -> list[str]:
    errors = []
    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md lacks YAML frontmatter")
    else:
        parts = text.split("---\n", 2)
        if len(parts) < 3:
            errors.append("SKILL.md frontmatter not closed")
        else:
            for key in ("name", "description"):
                if not re.search(rf"(?m)^{key}:\s*\S+", parts[1]):
                    errors.append(f"Missing frontmatter {key}")
            if not re.search(r"(?m)^name:\s*sol-luna-orchestrator\s*$", parts[1]):
                errors.append("Unexpected skill name")
    for md in ROOT.glob(".agents/skills/sol-luna-orchestrator/references/*.md"):
        if not md.read_text(encoding="utf-8").startswith("# "):
            errors.append(f"Missing heading in {md.name}")
    for path in (ROOT / "codex/agents/luna_executor.toml", ROOT / "codex/agents/sol_reviewer.toml", ROOT / "codex/config.example.toml"):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            if "agents" in path.parts and not {"name", "model", "developer_instructions"} <= data.keys():
                errors.append(f"Incomplete agent: {path}")
        except (ValueError, OSError) as exc:
            errors.append(f"Invalid TOML in {path.name}: {exc}")
    if not (ROOT / "LICENSE").is_file():
        errors.append("Missing license")
    return errors


if __name__ == "__main__":
    issues = validate()
    for issue in issues:
        print("ERROR:", issue)
    if issues:
        sys.exit(1)
    print("Package validation passed: SKILL.md, references, agent TOML, sample config, LICENSE.")
