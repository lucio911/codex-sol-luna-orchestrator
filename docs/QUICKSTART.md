# Quick Start: Sol–Luna Orchestrator

[README](../README.md) · [中文快速入门](QUICKSTART.zh-CN.md) · [More prompts](../examples/prompts.md)

**Sol plans and reviews; a real Codex subagent called \`luna_executor\` performs bounded implementation.** Paste the prompts below into **Codex chat**, not into your shell.

## 1. Install once

Prerequisites: Codex with Skills and subagents support. Python 3.11+ is needed only for installer and diagnostic scripts.

~~~bash
git clone https://github.com/lucio911/codex-sol-luna-orchestrator.git
cd codex-sol-luna-orchestrator
python scripts/install.py --scope user --dry-run
python scripts/install.py --scope user --configure-defaults --primary-model gpt-6.1-sol --primary-effort max --executor-effort high
python scripts/doctor.py --scope user
~~~

Restart Codex. Existing conflicting agent files are not overwritten unless you pass \`--force\`; the installer backs them up. For per-repository setup use \`--scope project --project-root /path/to/project\`.

## 2. First prompt

~~~text
$sol-luna-orchestrator mode=auto
Inspect the current repository and fix failing tests.
Have the primary Sol agent plan and review; delegate bounded implementation
to luna_executor if the runtime supports the named agent.
Return changed paths, actual test commands/results, and unresolved issues.
~~~

\`mode=auto\` is a **skill prompt convention**, not a Codex CLI parameter. Model routing and reasoning effort come from the installed Codex runtime/configuration, not from words in a prompt.

## 3. Copyable scenarios

### A. Fix a bug — auto

~~~text
$sol-luna-orchestrator mode=auto
Find the root cause of failing unit tests in this Python repository.
Sol should set a minimal fix plan and acceptance checks;
luna_executor should implement the fix and run affected tests;
Sol should independently inspect the final diff.
Do not touch unrelated files. Report actual commands and outcomes.
~~~

### B. Add a feature — quality

~~~text
$sol-luna-orchestrator mode=quality
Implement CSV import with UTF-8 support, header validation and useful errors.
Sol should inspect existing contracts and define acceptance criteria.
Delegate implementation plus tests to luna_executor.
Sol should check regressions, edge cases and compatibility before acceptance.
~~~

### C. Refactor safely — quality

~~~text
$sol-luna-orchestrator mode=quality
Refactor the data-processing module to remove duplication without changing
public interfaces or output semantics. Plan bounded work packages and
delegate non-overlapping edits to luna_executor, with tests after each step.
Sol must review the diff and report evidence of preserved behavior.
~~~

### D. Scientific Python / geotechnical modeling — research

~~~text
$sol-luna-orchestrator mode=research
Audit the vertical cyclic-loading pile model in the current repository.
Sol: verify equations, units, boundary conditions and acceptance criteria.
Luna: implement scoped corrections and tests.
Sol: review Pa/kPa/MPa and m/mm conversions, numerical convergence and
reproducibility. Do not fabricate measurements, simulations or test results.
~~~

### E. Reproducible scientific figures — research

~~~text
$sol-luna-orchestrator mode=research
Use the existing CSV files to generate reproducible stress–strain and
stiffness-degradation plots. Sol defines plotting and unit requirements,
Luna writes and tests scripts, and Sol validates the actual source data,
axis labels, export formats and rerun instructions. Do not invent data points.
~~~

### F. Review only — quality

~~~text
$sol-luna-orchestrator mode=quality
Review this branch relative to main without editing files.
Identify correctness, regression, test and security issues with file paths
and verifiable evidence. Do not spawn an executor for this read-only task.
~~~

### G. Small task — economy

~~~text
$sol-luna-orchestrator mode=economy
Update the outdated installation command in README and verify the link.
If the change is trivial, do it directly rather than spawning an agent.
Return only concrete edits and checks performed.
~~~

## 4. Verify real delegation

~~~bash
python scripts/doctor.py --scope user --json
~~~

The doctor checks **on-disk configuration only**. It cannot prove the runtime actually selected Luna. For a live check, ask Codex:

~~~text
$sol-luna-orchestrator mode=auto
Verify that the named luna_executor subagent is available.
If possible, actually delegate a read-only repository tree inspection and
show the subagent tool result. If unavailable, describe the blocking reason.
Do not impersonate another agent or invent runtime-model evidence.
~~~

If the client does not expose the model identity, you can verify that a named subagent ran, **not** which model the provider used internally.

## 5. Troubleshooting

- **Skill not found:** confirm installation scope, restart Codex, and invoke in chat rather than the terminal.
- **Agent unavailable:** inspect the installed \`luna_executor.toml\` and check for native subagent support.
- **Model/effort rejected:** select IDs/efforts actually accessible in your Codex client.
- **Preferences on every project:** optionally adapt [AGENTS.md example](../examples/AGENTS.example.md) to your own instructions. It cannot force actual model routing.
- **No tests could run:** the executor should state why; do not label static inspection as passed tests.

Do not paste secrets or proprietary data into public issues.