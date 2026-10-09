---
name: sol-luna-orchestrator
description: Plan, delegate, review, and verify multi-step Codex coding and scientific computing tasks. Use when a task benefits from a reasoning-focused primary agent (Sol) and a separately configured execution subagent (Luna), including debugging, multi-file changes, numerical modeling, and iterative review. Skip delegation for trivial tasks.
---

# Sol–Luna Orchestrator

## Purpose

Orchestrate work in Codex using a reasoning-focused **primary agent** for planning and final review and a **real Codex subagent** named `luna_executor` for bounded implementation. This skill is an instruction workflow: **it cannot switch models on its own**. A model is selected only by Codex's actual subagent configuration/runtime. Never impersonate a subagent, invent delegation results, or claim a model was used without evidence.

Read `references/modes.md` for optional modes and `references/task-contract.md` for the delegation contract. For research or numerical-computing tasks also read `references/research-review.md`.

## Operational rules

1. **Respect hierarchy and safety.** Follow existing user instructions, `AGENTS.md`, file ownership, sandbox permissions, and approval requirements. Never bypass them to make the workflow succeed.
2. **Preflight.** Inspect repository state, relevant files, and existing tests. Determine whether tools for actual subagent spawning are available and `luna_executor` is registered. Do not assume a configuration file proves a live spawn.
3. **Classify before delegating.** `SIMPLE` means a small, low-risk change handled directly. `STANDARD` means a well-bounded task suitable for Luna. `COMPLEX` means dependencies/ambiguous implementation requiring a written plan before delegation. `CRITICAL` means high-impact or irreversible changes; require explicit user approval where appropriate and stricter review. Default mode: `auto`.
4. **Plan for acceptance.** The primary agent states the goal, constraints, affected modules, steps, and observable acceptance criteria. For nontrivial work, keep a short plan and update its status after each phase.
5. **Delegate bounded execution.** Spawn `luna_executor` through an actual Codex subagent tool, if available. Give it a specific objective, files in scope, constraints, tests to run, and expected output. Use the contract in `references/task-contract.md`. Do not grant extra privileges. If Luna cannot be spawned, report the limitation and ask before changing the agreed division of labor; for trivial tasks, direct execution is acceptable.
6. **Coordinate safe parallelism.** Only independent, nonoverlapping file changes may run in parallel; otherwise serialize. Maximum concurrency is controlled by Codex configuration, not this skill. Do not delegate a task recursively unless explicitly authorized.
7. **Review independently.** After Luna reports, inspect the actual diff and run or inspect relevant validation. Check requirement coverage, correctness, test evidence, edge cases, and unexpected changes. Agent self-assessment is not evidence. Use `references/review-checklist.md`.
8. **Close the correction loop.** If review finds defects, send actionable findings back to Luna. By default allow no more than two correction rounds; if unresolved, report remaining issues transparently. Do not silently broaden scope.
9. **Finish with evidence.** Report outcome, affected files, tests actually run and results, reviewer findings, unresolved limitations, and whether genuine delegation was confirmed. If runtime does not reveal the model selected, say that model routing was configured but not independently verified.

## Mode selection

Interpret a user request such as `mode=auto`, `mode=economy`, `mode=quality`, or `mode=research` as a **natural-language convention**, not a built-in Codex command or guaranteed parser. If absent, use `auto`. Modes adjust planning/review depth, never security policy or actual model selection. See `references/modes.md`.

## No fabricated guarantees

- Do not claim that Luna executed work unless a real subagent was spawned.
- Do not claim test success unless the test output is available.
- Do not claim token or latency savings without measurements.
- Do not assume access to a particular model merely because its ID appears in a TOML file.
- Do not change the primary Codex model or global defaults without the user's explicit request.
