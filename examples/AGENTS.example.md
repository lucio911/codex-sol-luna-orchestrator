# Optional AGENTS.md template: Sol–Luna Orchestrator

> Copy only the rules that fit your workspace into the **existing** project-root `AGENTS.md` or user-level `~/.codex/AGENTS.md`. Do not overwrite unrelated instructions. This file is an example and is **not installed automatically**.

## Preferred multi-agent workflow

For nontrivial coding tasks, prefer the installed `sol-luna-orchestrator` skill if Codex discovers it. The primary agent performs planning, acceptance criteria and independent review. When a real `luna_executor` subagent is registered and a spawn tool is available, delegate bounded implementation or tests to it. Require evidence of changes, test output and final review.

Prefer these prompt-mode conventions:

- `auto` for ordinary development.
- `economy` for small tasks with minimal delegation overhead.
- `quality` for higher-risk code and significant refactoring.
- `research` for numerical modeling, experiments and scientific plotting.

Skip delegation for trivial or read-only requests. Never fabricate tool calls, model selection, successful tests, numerical results or cost savings.

### Work-package discipline

State task objective, files in scope, constraints, verifiable acceptance criteria and expected return. Do not allow concurrent agents to edit the same files. Respect user approvals, existing project instructions, sandbox permissions and confidentiality.

### Failure behavior

If the named subagent is absent, unavailable, lacks model access or the runtime cannot spawn agents, report the limitation. Do not fake a multi-agent workflow. For a nontrivial task, ask before replacing explicit delegated execution with direct execution.

### Scientific computing checks

For research tasks, verify units, model assumptions, equations, boundary conditions, convergence and reproducibility. Distinguish observed data from fitted results and predictions; never invent measurements or solver output.

### Delivery checklist

At completion report the changed files, tests actually run (with results), review findings, known limitations and whether live delegation was confirmed.

## How to use

You can still invoke the skill explicitly in Codex chat for important tasks:

~~~text
$sol-luna-orchestrator mode=research
Audit my model code and fix genuine defects. Sol plans and reviews;
delegate bounded implementation to luna_executor only if a real named
subagent is available. Report actual verification evidence.
~~~

Important: A preference in `AGENTS.md` **cannot force Codex to expose an unsupported subagent or switch the main model**. It also does not change the effort level configured in TOML.