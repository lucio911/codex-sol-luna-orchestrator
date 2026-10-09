#!/usr/bin/env python3
"""Inspect on-disk Codex skill/subagent setup (not a live model-routing test)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tomllib

from install import get_destinations


def diagnose(scope: str, project_root: Path | None = None, home: Path | None = None) -> dict:
    skill, agent, config = get_destinations(scope, project_root, home)
    result = {"skill_path": str(skill), "agent_path": str(agent), "config_path": str(config),
              "skill_exists": (skill / "SKILL.md").is_file(),
              "agent_exists": agent.is_file(), "config_exists": config.is_file(),
              "agent_model": None, "primary_model": None,
              "multi_agent_enabled": None, "warnings": []}
    if result["agent_exists"]:
        try:
            agent_data = tomllib.loads(agent.read_text(encoding="utf-8"))
            result["agent_model"] = agent_data.get("model")
            if agent_data.get("name") != "luna_executor":
                result["warnings"].append("Agent name is not luna_executor")
        except (ValueError, OSError) as exc:
            result["warnings"].append(f"Invalid agent TOML: {exc}")
    if result["config_exists"]:
        try:
            cfg = tomllib.loads(config.read_text(encoding="utf-8"))
            result["primary_model"] = cfg.get("model")
            result["multi_agent_enabled"] = cfg.get("agents", {}).get("enabled", True)
        except (ValueError, OSError) as exc:
            result["warnings"].append(f"Invalid config TOML: {exc}")
    if not result["skill_exists"]:
        result["warnings"].append("Skill not found")
    if not result["agent_exists"]:
        result["warnings"].append("Named subagent file not found")
    if result["multi_agent_enabled"] is False:
        result["warnings"].append("Multi-agent tools explicitly disabled")
    result["live_routing_verified"] = False  # static inspection can never establish this
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    status = diagnose(args.scope, args.project_root)
    if args.json:
        print(json.dumps(status, indent=2, ensure_ascii=False))
    else:
        for key, value in status.items():
            print(f"{key}: {value}")
        print("For a live check, open Codex and explicitly spawn luna_executor using your installed skill.")
    return 0 if status["skill_exists"] and status["agent_exists"] and not status["warnings"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
