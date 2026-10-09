# Sol–Luna Orchestrator for Codex

[中文说明](README.zh-CN.md) · [Changelog](CHANGELOG.md) · [Examples](examples/prompts.md)

A **dependency-free, open-source Codex Skill** that coordinates a reasoning-focused primary model for **planning and final review** with a fast, separately configured **Luna implementation subagent**. Built on Codex's *native* skills and custom-subagent mechanisms—not a prompt pretending to change models.

> **Status: v0.1.0 preview.** On-disk installation and configuration are unit tested. Live Sol→Luna model routing must still be verified in your own authorized Codex runtime. Model access varies by product, workspace and account.

## What it does

1. **Classify:** Skip unnecessary delegation for trivial requests.
2. **Plan:** Primary agent inspects the repo, defines constraints and observable acceptance criteria.
3. **Execute:** Codex spawns the named `luna_executor` subagent with a bounded work package.
4. **Review:** Primary agent inspects actual changes and independently evaluates tests and risks.
5. **Repair:** Up to two correction rounds by default, then report honest status.
6. **Deliver:** Summarize changed files, evidence, limitations and delegation status.

```
          Sol (primary agent: plan + acceptance)
                          |
                 bounded work package
                          v
         Luna (`luna_executor`: implement + test)
                          |
                   real diff + evidence
                          v
                   Sol final review
                    |           |
                 accepted    defects
                    |           |
                 deliver   send back to Luna
```

Available modes: `auto` (default), `economy`, `quality`, and `research` (additional scientific-computing checks). These are **prompt conventions**, not built-in CLI options.

## Requirements

- A Codex installation with native Skill discovery and subagent support.
- Permission to use the configured models in your Codex client/workspace.
- Python **3.11+** for the optional installer, validator, diagnostic tool and tests. Codex itself does not need Python to read the skill.
- No Python third-party packages, API keys, or MCP server are required by this project.

Defaults: primary model `gpt-6.1-sol` (only if explicitly requested during install); named executor `gpt-6-luna`. Substitute model IDs according to actual availability. The installer **never silently changes your main model or existing config**.

## Quick start

```bash
git clone https://github.com/lucio911/codex-sol-luna-orchestrator.git
cd codex-sol-luna-orchestrator
python scripts/validate.py
python scripts/install.py --scope user --dry-run
python scripts/install.py --scope user --configure-defaults --primary-model gpt-6.1-sol
python scripts/doctor.py --scope user
```

For a downloaded ZIP, enter its extracted directory. Restart Codex after installing the skill and agent.

The `--configure-defaults` switch opt-in merges `agents.enabled = true`, an agent concurrency cap, and—if provided—your primary model into the existing `~/.codex/config.toml`. It preserves unrelated TOML settings and creates a timestamped backup. Without the switch, only the skill folder and named executor agent are installed.

In **Codex chat** (not your terminal), invoke:

```text
$sol-luna-orchestrator mode=quality. Inspect the tests, plan a safe fix,
delegate bounded implementation to luna_executor, then review the actual diff.
```

For another model, change `--executor-model` (or edit the installed `luna_executor.toml`). Do not assume the model ID is available just because the file parses.

## Installation scopes

| Scope | Skill installed to | Agent installed to | Optional Codex config |
|---|---|---|---|
| `--scope user` (default) | `~/.agents/skills/sol-luna-orchestrator/` | `~/.codex/agents/luna_executor.toml` | `~/.codex/config.toml` |
| `--scope project --project-root /path/to/repo` | `<repo>/.agents/skills/sol-luna-orchestrator/` | `<repo>/.codex/agents/luna_executor.toml` | `<repo>/.codex/config.toml` |

Windows PowerShell example:

```powershell
py -3 scripts\install.py --scope user --dry-run
py -3 scripts\install.py --scope user --configure-defaults --primary-model gpt-6.1-sol
py -3 scripts\doctor.py --scope user --json
```

Project-local example (run from this repository):

```bash
python scripts/install.py --scope project --project-root /path/to/your/target-repo
```

**Collision policy:** Existing different skill or agent files are left untouched unless you explicitly supply `--force`; conflicting items are backed up before replacement. Existing configs are only edited with `--configure-defaults` and backed up. Run `--dry-run` first.

## Files

```text
.agents/skills/sol-luna-orchestrator/
  SKILL.md
  references/{modes,task-contract,review-checklist,research-review}.md
codex/
  agents/luna_executor.toml
  agents/sol_reviewer.toml         # optional; not installed by default
  config.example.toml            # documented example, not copied over existing config
scripts/{install,doctor,validate}.py
tests/test_install.py
.github/workflows/validate.yml
```

The optional `sol_reviewer.toml` can be installed manually in `.codex/agents/` if you want a separately spawned Sol reviewer. By default the **primary Sol agent** conducts final review, saving unnecessary subagent cycles.

## Design and correctness boundaries

- A Skill supplies **instructions** and can be discovered by Codex. It does not directly invoke a model API or force automatic delegation.
- The `luna_executor` TOML defines a **real named subagent**. Codex must have available spawning tools and permission to use the chosen model.
- `doctor.py` checks **files and TOML only**, not actual runtime model routing. Verify with an explicit Codex spawn and inspect available trace/tool evidence.
- No guaranteed cost reduction, benchmark result or test success is asserted without evidence.
- The default installation does not modify security, approval, sandbox, project-wide defaults or arbitrary repository files.
- No model may impersonate another. Missing capabilities are reported, not hidden.

## Validation

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/install.py --scope project --project-root /tmp/test-repo --dry-run
```

The offline suite covers frontmatter, TOML syntax, clean installation, idempotency, collision prevention, backups, config preservation, model ID validation and static diagnostics. **It cannot perform a genuine Codex model delegation test inside GitHub Actions.**

## References

- [Codex Skill discovery and file locations](https://learn.chatgpt.com/docs/build-skills)
- [Codex subagents and custom TOML files](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [OpenAI model catalog](https://developers.openai.com/api/docs/models)

## License

MIT — see [LICENSE](LICENSE). Contributions and issues are welcome.