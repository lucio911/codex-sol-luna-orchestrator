# Workflow modes

Modes are prompt conventions recognized by the skill's instructions, not CLI arguments or special commands.

| Mode | Delegation | Review | Recommended use |
|---|---|---|---|
| `auto` (default) | Only when worthwhile | Focused correctness review | Everyday development |
| `economy` | Prefer bounded Luna implementation; minimize redundant exploration | Focused diff and relevant tests | Clear repetitive changes |
| `quality` | Plan, execute, independent review, up to two repair rounds | Deeper regression/edge-case assessment | Important code or production changes |
| `research` | Plan assumptions and reproducibility, then implement | Units, equations, numerical evidence and traceability | Geotechnical models and scientific Python |

All modes must respect approvals, isolation, and the no-fabrication rules in `SKILL.md`. Avoid spawning another agent merely to confirm formatting.
