# Publishing to GitHub

The repository is ready for the owner to publish. The ChatGPT GitHub connector can write to **existing** repositories but may not have permission/capability to create new ones. Do not claim publication until the remote repository is actually reachable.

## Option A: GitHub website (no GitHub CLI required)

1. Sign in to GitHub and visit <https://github.com/new>.
2. Owner: `lucio911`. Repository name: `codex-sol-luna-orchestrator`.
3. Description: `Codex Skill: Sol plans and reviews; Luna implements and tests via native subagents.`
4. Visibility: **Public** (for open source).
5. **Do not** initialize with README, .gitignore or license; these are already present locally.
6. Create the repository. Push from a downloaded source folder using commands below. Alternatively, return the created repository URL to the assistant with GitHub access, which can upload the files to this existing repository.

```bash
cd codex-sol-luna-orchestrator
git init -b main
git add .
git commit -m "feat: initial Sol-Luna Codex orchestration skill"
git remote add origin https://github.com/lucio911/codex-sol-luna-orchestrator.git
git push -u origin main
```

Git credential authentication must be configured for your own account. Never paste a personal access token into chat.

## Option B: GitHub CLI (if installed and authenticated)

```bash
gh auth login
cd codex-sol-luna-orchestrator
git init -b main
git add .
git commit -m "feat: initial Sol-Luna Codex orchestration skill"
gh repo create lucio911/codex-sol-luna-orchestrator --public --source . --remote origin --push
```

If the repository already exists, do not run `gh repo create` again; use `git remote add origin` and `git push` instead.

## After publishing

1. Confirm `README.md`, `SKILL.md`, and `codex/agents/luna_executor.toml` appear on GitHub.
2. Check the GitHub Actions `Validate skill` workflow. It should run on pushes and pull requests.
3. In a permitted Codex workspace, perform an explicit named-subagent spawn using the `examples/prompts.md` routing prompt.
4. Add GitHub topics: `codex`, `codex-skills`, `multi-agent`, `orchestration`, `research`.
5. Create a `v0.1.0` tag/release **only after** live routing has been tested; the current offline status is preview.

Security: inspect source before installing, and keep confidential project data or credentials out of the public repository.