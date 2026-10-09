# Example prompts (paste into Codex, not your terminal)

## Daily coding

`$sol-luna-orchestrator mode=auto. Inspect this Python package, fix the failing unit tests. Use the luna_executor subagent for bounded implementation and review the actual diff before concluding.`

## Quality review

`$sol-luna-orchestrator mode=quality. Plan a safe refactor of the data parser, delegate implementation to luna_executor, inspect the tests, then return findings and corrected output.`

## Research and geotechnics

`$sol-luna-orchestrator mode=research. Audit the cyclic-loading numerical model for physical units, parameter constraints and reproducibility. Let luna_executor implement bounded fixes. Review numerical consistency and compare tests against trusted fixtures. Never invent experimental values.`

## Simple task

`$sol-luna-orchestrator mode=economy. Rename one variable in one function. Skip delegation if the change is genuinely trivial.`

## Routing check

`$sol-luna-orchestrator. If the Codex runtime exposes a subagent spawn tool and luna_executor exists, spawn it to perform a read-only exploration task and report the actual tool result. Explain what evidence is and is not available for the selected model. Do not claim successful delegation otherwise.`
