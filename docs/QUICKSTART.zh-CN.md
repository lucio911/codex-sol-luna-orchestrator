# 快速上手：Sol–Luna Orchestrator

[返回中文首页](../README.zh-CN.md) · [English Quick Start](QUICKSTART.md) · [更多英文提示词](../examples/prompts.md)

**3 分钟理解：Sol 负责规划和最终审查，Codex 中名为 `luna_executor` 的子代理负责限定范围的实现。** 所有下列提示词都应粘贴到 **Codex 对话框**，而不是 PowerShell / 终端。

## 1. 安装一次

要求：支持 Skills 与子代理的 Codex，以及 Python 3.11+（仅安装和检查脚本需要）。从本仓库目录运行：

~~~powershell
git clone https://github.com/lucio911/codex-sol-luna-orchestrator.git
cd codex-sol-luna-orchestrator
py -3 scripts\install.py --scope user --dry-run
py -3 scripts\install.py --scope user --configure-defaults --primary-model gpt-6.1-sol --primary-effort max --executor-effort high
py -3 scripts\doctor.py --scope user
~~~

若已安装但希望更新子代理配置，安装命令可追加 `--force`，**旧代理会先被备份**。重新启动 Codex。只对单个项目安装时，使用 `--scope project --project-root "项目路径"`；两种范围详见[中文 README](../README.zh-CN.md)。

### 最简调用

~~~text
$sol-luna-orchestrator mode=auto
检查当前项目，修复失败的测试。由 Sol 规划和验收，
将明确、可独立执行的代码修改交给 luna_executor。
请列出修改文件、实际运行的测试和仍未解决的问题。
~~~

这里的 `mode=auto` 是 Skill 的**工作流约定**，不是 Codex 原生 CLI 参数。真正的模型及推理强度由 Codex 配置确定，不能靠提示词直接切换。

## 2. 复制一个适合你的任务案例

### 案例 A：修复 Python Bug（auto）

适合：报错追踪、修复单元测试、局部代码调整。

~~~text
$sol-luna-orchestrator mode=auto

我的 Python 项目中有测试失败。先由 Sol 定位问题、给出最小修复计划和验收标准，
再委派 luna_executor 修改必要文件并运行相关测试，最后由 Sol 独立审查实际 diff。
限制：不得改动无关文件，不得删除已有测试。
请汇报：根因、修改文件、测试命令及其真实结果。
~~~

### 案例 B：开发新功能（quality）

适合：跨文件实现、API 开发、需要回归测试的新需求。

~~~text
$sol-luna-orchestrator mode=quality

为当前项目添加 CSV 数据导入功能：支持 UTF-8、表头校验和错误行提示。
Sol 先检查项目结构，设计输入输出接口和可验证的验收标准；
将实现与测试委派给 luna_executor，Sol 检查边界条件、兼容性和测试证据。
不修改无关接口；若出现缺陷，给出最多两轮针对性修复意见。
~~~

### 案例 C：复杂重构（quality）

适合：跨模块重构，重视现有功能不被破坏。

~~~text
$sol-luna-orchestrator mode=quality

重构当前项目的数据处理模块，目标是减少重复代码并提高可测试性。
先调查调用链和现有测试，再将任务拆成不相互冲突的工作包，逐步交给 luna_executor。
保持公开 API 和输入输出行为不变。每个阶段运行相关测试；
最后由 Sol 审查变更范围、兼容性、潜在回归风险，报告证据。
~~~

### 案例 D：科研数值计算（research）

适合：岩土工程、有限元、数据拟合、Python 科学计算。

~~~text
$sol-luna-orchestrator mode=research

检查当前竖向循环荷载下的桩基数值计算程序。
Sol 先核对控制方程、参数定义、边界条件、单位体系及计算流程，
制定可复现的修正计划；由 luna_executor 完成限定范围内的代码修正和测试。
Sol 最后检查 Pa/kPa/MPa、m/mm 单位转换，数值稳定性、收敛性与结果追溯。
不得编造实验数据或声称运行了本机没有的专有软件。
~~~

### 案例 E：科研论文配套绘图（research）

适合：从真实数据生成图、确保论文结果可复现。

~~~text
$sol-luna-orchestrator mode=research

基于当前目录中的原始 CSV 数据，编写绘制应力–应变曲线和刚度退化曲线的 Python 脚本。
Sol 先确定图例、单位、统计处理与可复现标准；Luna 负责代码和测试。
最后由 Sol 检查是否使用了真实数据、是否正确标注坐标轴、
是否保存矢量图，并列出完整的重现命令。
不要凭空生成测量点或统计显著性结论。
~~~

### 案例 F：只审查、不改文件（quality）

适合：正式提交代码前的安全与质量审查。

~~~text
$sol-luna-orchestrator mode=quality

请只读审查当前分支相对于 main 的改动，不要修改任何文件。
由 Sol 检查需求覆盖、正确性、边界条件、测试与安全风险。
按严重程度列出具体文件、问题和修复建议；不存在证据时说明尚未验证。
本次不必委派执行代理。
~~~

### 案例 G：小任务优先省开销（economy）

适合：简单重命名、局部文本调整。

~~~text
$sol-luna-orchestrator mode=economy

将当前项目 README 中过时的安装命令改成最新命令，
检查链接是否有效。若任务足够简单，直接完成，不必启动子代理；
只汇报具体变更和实际检查结果。
~~~

## 3. 怎么确定 Luna 真的在执行？

安装检查：

~~~powershell
py -3 scripts\doctor.py --scope user --json
~~~

这只能说明 Skill / TOML 文件存在，**不能证明 Luna 被真实调用**。请在 Codex 对话中粘贴：

~~~text
$sol-luna-orchestrator mode=auto
先确认当前运行时是否具有子代理调用能力且已注册 luna_executor。
如果可以，请委派 luna_executor 只读检查当前项目的目录结构，
展示实际子代理调用与返回结果，再由主代理概括。
如果不能调用，请说明具体限制；不要用文本假装已经切换模型。
~~~

如果客户端不显示真实模型 ID，则只能确认**子代理实际运行**，不能仅凭提示词证明它使用了特定模型。

## 4. 常见问题

- **Codex 不识别 `$sol-luna-orchestrator`：** 先检查安装范围和 Skill 路径，再重启 Codex。确保在对话框而非终端输入。
- **没有 `luna_executor`：** 检查 `~/.codex/agents/luna_executor.toml` 或项目级对应路径；确认客户端支持自定义子代理。
- **访问不到 GPT-6 Luna 或 max：** 改成你的客户端实际支持的模型和推理强度；Skill 本身不会赋予模型权限。
- **修改后仍使用旧设置：** 重新启动会话。已经运行的主代理通常不会被提示词中途更换推理强度。
- **想要每次默认使用：** 可将[AGENTS.md 模板](../examples/AGENTS.example.md)中内容按需合并到自己项目或用户级的 Codex 指令中，但这只是偏好指令，不能保证每次都启动子代理。

**安全提醒：** 不要将私有数据、密钥或用户配置上传到 Issue。生产环境/重要科研成果应保留人工审查。