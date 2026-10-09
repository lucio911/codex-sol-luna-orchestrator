# Independent review checklist

Review the actual repository diff and relevant runtime evidence, not only the executor's summary.

- **Requirements:** Does behavior match the user goal and every acceptance criterion?
- **Scope:** Are there changes to unrelated paths, dependencies, configuration or generated files?
- **Correctness:** Are invariants, error handling, edge cases, and failure modes addressed?
- **Safety:** Were approvals, secrets, file permissions, and external actions handled appropriately?
- **Tests:** Which exact tests ran, which failed, and which could not run? Is coverage adequate for changed behavior?
- **Regressions:** Are API compatibility, input/output contracts, and existing behavior preserved?
- **Evidence:** Can another person reproduce the result? Are claimed measurements actually recorded?

Classify each finding as blocker / important / suggestion. Send only actionable blockers and important defects back for correction. Re-review the resulting diff rather than accepting a declaration that the issue was fixed.
