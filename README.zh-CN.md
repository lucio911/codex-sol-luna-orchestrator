# Sol–Luna Orchestrator（Codex 双模型协作 Skill）

[English README](README.md) · [示例提示词](examples/prompts.md) · [更新日志](CHANGELOG.md)

一个面向 Codex 的开源多代理编排 Skill：**Sol 主代理负责规划和独立审查，Luna 子代理负责限定范围内的实现和测试**。核心利用 Codex 原生的 Skills 与自定义子代理 TOML 配置，不依赖额外 MCP 服务或第三方 Python 包。

> **当前版本：v0.1.1 预览版。** 本地文件安装、配置合并与静态校验经过自动化测试；真实 Sol→Luna 子代理模型调用，仍需在你有权限的 Codex 环境中进行联机验证。Skill 本身不会切换模型。

## 工作流程

1. Sol 检查项目，识别任务范围和依赖关系。
2. 简单任务直接完成；复杂任务分解为可验收的工作包。
3. 调用真正注册的 `luna_executor` 子代理执行；限制允许修改的文件、输出和测试。
4. Sol 检查真实的代码差异、测试证据、异常和边界条件。
5. 审查不通过时，最多默认反馈两轮修改；无法解决的事项如实说明。
6. 最后汇报完成情况、修改文件、实际测试结果与仍然存在的风险。

模式包括 `auto`（自动）、`economy`（节约执行开销）、`quality`（加强检查）、`research`（科学计算与工程数值模型）。`mode=research` 等只是给 Skill 的自然语言约定，**不是 Codex 原生命令参数**。

## 前提

- Codex 版本支持 Skill 发现及原生子代理功能。
- 当前 Codex 客户端/工作区有权限调用配置的模型。
- 可选工具安装需要 Python 3.11 或更新版本，且无第三方依赖。

推荐默认执行模型：`gpt-6-luna`；主模型推荐 `gpt-6.1-sol`。如果你的环境只有 `gpt-6-sol`，可以自行改用可用的 ID。模型名称正确不等于实际获得了访问权限。

## Windows 安装（PowerShell）

下载本仓库 ZIP 并解压，或从正式 GitHub 仓库 `git clone`。在项目根目录执行：

```powershell
py -3 scripts\validate.py
py -3 scripts\install.py --scope user --dry-run
py -3 scripts\install.py --scope user --configure-defaults --primary-model gpt-6.1-sol
py -3 scripts\doctor.py --scope user
```

说明：第三条命令是**明确授权**安装脚本修改当前用户的 Codex 配置。脚本会将 Skill 安装到 `~/.agents/skills/sol-luna-orchestrator`，将执行代理安装到 `~/.codex/agents/luna_executor.toml`，并将必要设置合并至 `~/.codex/config.toml`，保留其他配置、写入前备份。如果不想修改配置，使用：

```powershell
py -3 scripts\install.py --scope user
```

如果只给某一个项目使用：

```powershell
py -3 scripts\install.py --scope project --project-root "C:\path\to\your-project" --configure-defaults --primary-model gpt-6.1-sol
```

发生文件冲突时，安装默认拒绝覆盖；如确定需要替换，指定 `--force`，旧文件会先备份。先使用 `--dry-run` 预览。

安装后重新启动 Codex，在 **Codex 对话框中**（不是 PowerShell）输入：

```text
$sol-luna-orchestrator mode=research
分析当前 Python 数值模型，检查量纲一致性、参数设置及数值收敛性。
由 Sol 制定方案，调用 luna_executor 执行限定范围内的修改和测试，
Sol 最终检查实际代码变更及结果。不要编造试验数据和测试结果。
```

如果你的 Codex 支持显式查看子代理工具调用或轨迹，请确认真的启动了 `luna_executor`，并核对其模型信息。`doctor.py` 只检查磁盘配置，**不具备线上模型识别能力**。

## 选择 high / max 推理强度

Sol 主代理与 Luna 执行代理可以分别设定 `low`、`medium`、`high`、`xhigh` 或 `max`。一般代码开发建议 `high / high`；复杂科研、数值建模与算法审查建议 **Sol = max，Luna = high**。

推荐方案（Windows PowerShell）：

```powershell
py -3 scripts\install.py --scope user --configure-defaults --primary-model gpt-6.1-sol --primary-effort max --executor-effort high --force
```

如果两者都要使用 `max`：

```powershell
py -3 scripts\install.py --scope user --configure-defaults --primary-model gpt-6.1-sol --primary-effort max --executor-effort max --force
```

也可仅执行 `--configure-defaults --primary-effort high` 将 Sol 切回 high，不改变模型名称。切换现有 Luna 设置需要 `--force`，脚本会自动备份旧代理文件；完成后请重启 Codex。

注意 `mode=research`、`mode=quality` 是 Skill 工作流模式，**不等于**实际模型的推理强度设置，无法在已经运行的主代理内部通过提示词动态切换到 max。

## 核心文件

| 文件 | 作用 |
|---|---|
| `.agents/skills/sol-luna-orchestrator/SKILL.md` | 任务分级、委派、审查和修复闭环 |
| `.agents/skills/sol-luna-orchestrator/references/` | 任务合同、模式、检查清单和科研审查 |
| `codex/agents/luna_executor.toml` | 指定 Luna 执行代理（默认安装） |
| `codex/agents/sol_reviewer.toml` | 可选独立 Sol 审查代理（默认不安装） |
| `scripts/install.py` | Windows/macOS/Linux 通用安装器 |
| `scripts/doctor.py` | 查看 Skill / 模型配置状态（静态） |
| `scripts/validate.py` | 离线验证元数据与 TOML |
| `tests/test_install.py` | 安装器和配置操作的单元测试 |

## 科研应用扩展

`research` 模式会加强单位检查（如 Pa/kPa/MPa、m/mm）、本构关系和假设说明、模型参数约束、数值收敛/敏感性、数据来源可追溯性、绘图重现性。对于 ABAQUS 等本地不可用软件，不得谎称完成了实际求解，应明确列出未能执行的检查。

## 如何测试

```powershell
py -3 scripts\validate.py
py -3 -m unittest discover -s tests -v
```

项目在 GitHub Actions 中使用 Python 3.11、3.12、3.13 自动运行离线测试，不会在 CI 中调用付费模型。

## 限制和安全

- 本项目没有通过 prompt 假装一个模型是另一个模型。模型路由必须由 Codex 运行时实现。
- 不保证一定节省 token；要通过相同测试任务比较成本、延迟、错误率。
- 用户既有的沙箱、审批要求、项目指令和隐私要求始终优先。
- 不自动开放执行权限，不使用个人 API Key，不收集账户信息。

参考文档：[Codex Skills](https://learn.chatgpt.com/docs/build-skills) · [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)。

## 开源协议

MIT，欢迎通过 Issue / Pull Request 反馈与贡献。