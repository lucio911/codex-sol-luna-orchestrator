# Ready-to-use prompts

**Paste into Codex chat**, not into your terminal. This document contains short prompts for everyday use. For step-by-step installation, detailed examples and troubleshooting, see [English Quick Start](../docs/QUICKSTART.md) or [中文快速入门](../docs/QUICKSTART.zh-CN.md).

## 1. Everyday code fix · auto

~~~text
$sol-luna-orchestrator mode=auto
Find and fix failing tests in the current repository.
Sol plans with explicit acceptance criteria; luna_executor implements scoped
changes and runs relevant tests; Sol reviews the actual diff and test output.
Summarize the root cause, changed paths and evidence. Skip the subagent if trivial.
~~~

## 2. New feature · quality

~~~text
$sol-luna-orchestrator mode=quality
Implement a CSV import feature with valid UTF-8, header validation and
readable errors for malformed rows. Preserve existing APIs.
Sol plans and reviews; delegate implementation/tests to luna_executor if
available. Iterate on concrete defects, not vague self-assessments.
~~~

## 3. Multi-file refactor · quality

~~~text
$sol-luna-orchestrator mode=quality
Refactor duplicated logic in the data-processing layer.
First inspect callers and existing regression coverage, then plan independent
work packages. luna_executor handles bounded edits and tests.
Sol must verify that the external behavior remains unchanged.
~~~

## 4. Scientific numerical code · research

~~~text
$sol-luna-orchestrator mode=research
Review the vertical cyclic-loading pile-foundation model in this repository.
Sol checks governing equations, parameter meanings, boundary conditions,
and unit conversions. Delegate bounded fixes and tests to luna_executor.
Sol reviews convergence, reproducibility and actual evidence.
Never fabricate simulations or experimental measurements.
~~~

## 5. Publication-grade figures · research

~~~text
$sol-luna-orchestrator mode=research
Create reproducible Python figures from the CSV files already in this folder.
Plot stress–strain and stiffness degradation, label physical units, and save
editable/vector outputs. Sol defines acceptance criteria and validates the
actual source data; Luna implements and tests. Do not invent missing data.
~~~

## 6. Read-only code audit · quality

~~~text
$sol-luna-orchestrator mode=quality
Review the current Git diff for security, regressions, test gaps and unclear
assumptions. Do not modify any file. Do not delegate an unnecessary execution
task. Cite file paths and provide actionable severity-ranked findings.
~~~

## 7. Tiny task · economy

~~~text
$sol-luna-orchestrator mode=economy
Update the old command in README to the latest documented installation command.
Check only the relevant files. If trivial, execute directly rather than
spawning luna_executor. Report what you actually changed and validated.
~~~

## 8. Verify named subagent · routing check

~~~text
$sol-luna-orchestrator mode=auto
Confirm that a real luna_executor subagent is registered and available.
If supported, actually delegate a read-only task to list relevant source
directories, and report the observed invocation/result. If not supported,
state the limitation without impersonating Luna or claiming a model was used.
~~~

## 9. Optional default behavior

See [AGENTS.md template](AGENTS.example.md) for a reusable preference that you can merge into your existing user or project instructions.

**Limitations:** Prompt modes are conventions, not native CLI flags. The actual model and effort must be configured separately. A skill does not grant model access or guarantee multi-agent execution.