---
name: agent-teams-playbook
version: "4.5"
description: |
  Agent Teams orchestration playbook for Claude Code. This skill should be used when the user asks to "create agent teams", "use agent swarm", "setup multi-agent collaboration", "orchestrate agents", "coordinate parallel agents", "organize team collaboration", "build agent teams", "implement swarm orchestration", "setup multi-agent system", "coordinate agent collaboration", or needs guidance on adaptive team formation, quality gates, skill discovery, task distribution, team coordination strategies, or Agent Teams best practices. 或者当用户说"多agent"、"agent协作"、"agent编排"、"并行agent"、"分工协作"、"拉团队"、"拉个团队"、"多代理协作"、"swarm编排"、"agent团队"时也应使用此技能。Note: "swarm/蜂群" is a generic industry term; Claude Code's official concept is "Agent Teams".
---

# Agent Teams 编排手册

作为 Agent Teams 协调器，你的职责包括：明确每个角色的职责边界、把控执行过程、对最终产品质量负责。

> **核心理解（铁律）**：Agent Teams 是"并行处理 + 结果汇总"模式，不是扩大单个 agent 的上下文窗口。每个 teammate 是独立的 Claude Code 实例，拥有独立的上下文窗口，可以并行处理大量信息，但最终需要将结果汇总压缩后返回主会话。

## 适用 vs 不适用

| 适用 | 不适用 |
|------|--------|
| 跨文件重构、多维度审查 | 单文件小修改 |
| 大规模代码生成、并行处理 | 简单问答、线性顺序任务 |
| 需要多角色协作的复杂任务 | 单agent可完成的任务 |

**边界处理**：用户输入模糊时，先引导明确任务再决策；任务太简单时，主动建议使用单agent而非组建团队。

## 用户可见性铁律

1. 每个阶段启动前输出计划，完成后输出结果
2. 子agent在后台执行，但进度必须汇报给用户
3. 任务拆分计划必须经用户确认后再执行
4. 失败时立即通知：`❌ [角色名] 失败: [原因]`，提供重试/跳过/终止选项
5. 全部完成后输出汇总报告（见阶段5格式）

## 场景决策树

**执行顺序**：先执行阶段0和阶段1（强制），再根据任务复杂度选择场景（影响阶段2-5）。

| 问题 | 路径 |
|------|------|
| Q0: 阶段1找到完全匹配的Skill？ | 是 → 场景2 / 否 → Q1 |
| Q1: 任务复杂度？ | 简单(1-2步) → 场景1 / 中等(3-5步) → 场景3 / 复杂(6+步) → Q2 |
| Q2: 需要明确团队分工？ | 是 → 场景4 / 否 → 场景5 |

- 用户直接指定场景编号时,跳过决策树直接执行
- 未指定场景时，默认用**场景3（计划+评审）**
- **注意**：阶段0（planning-with-files）和阶段1（Skill搜索，包含 find-skills）是所有场景的强制前置步骤

## 5大编排场景

| # | 场景 | 适用条件 | 核心策略 |
|---|------|---------|---------|
| 1 | 提示增强 | 简单任务，1-2步 | 优化单agent提示词，不拆分不组队 |
| 2 | Skill直接复用 | 任务可由单个Skill完全解决 | 执行规划和Skill搜索后，直接调用匹配的Skill，无需组建Agent Teams |
| 3 | 计划+评审 | 中等/复杂任务（**默认**） | 出计划 → 用户确认 → 并行执行 → Review验收 |
| 4 | Lead-Member | 需要明确团队分工 | Leader协调分配，Member并行执行，通过TaskList协同 |
| 5 | 复合编排 | 复杂任务，无固定模式 | 动态组合上述场景，按阶段切换策略 |


**模型分工**（所有场景通用）：通过Task工具的`model`参数按任务复杂度分配——`opus`处理复杂推理，`haiku`处理简单任务，`sonnet`处理常规任务。

## 协作模式

| 模式 | 通信方式 | 适用场景 | 启动方式 |
|------|---------|---------|---------|
| Subagent | 子agent → 主协调器单向汇报 | 并行独立任务 | `Task`工具 |
| Agent Team | 成员间可双向通信(SendMessage) | 需要协作的复杂任务 | `TeamCreate` + `Task(team_name)` |

选择原则：任务间无依赖用Subagent（简单高效），任务间需要协调用Agent Team（功能更强但成本更高）。

## 6阶段工作流（含强制规划和Skill搜索）

**重要说明**：阶段0和阶段1是**所有场景的强制前置步骤**，场景选择（1-5）只影响阶段2-5的执行方式。

### 阶段0：规划准备（Planning Setup）**【硬性标准 - 所有场景必经】**

**使用 Skill 工具调用 planning-with-files**：
```
Skill(skill="planning-with-files")
```

这将在项目目录创建三个核心文件：
- `task_plan.md` - 任务计划和阶段追踪
- `findings.md` - 研究发现和知识积累
- `progress.md` - 执行日志和进度记录

**关键规则**（规划文件创建后遵循）：
- 每个阶段开始前读取task_plan.md，完成后更新状态
- 每2次搜索/浏览操作后立即保存发现到findings.md
- 所有错误必须记录到task_plan.md的"Errors Encountered"表格
- 3次失败后升级给用户

> **铁律**：没有task_plan.md就不能开始执行。这是Manus工作流的核心，确保上下文持久化。

### 阶段1：任务分析 + Skill发现（Discovery）**【硬性标准 - 所有场景必经】**

先质疑再执行：
- 需求不合理时主动挑战假设，建议更好的方案
- 区分"现在必须做"和"以后再说"，排除非核心范围
- 任务太大时建议更聪明的起点

输出任务总览：

| 字段 | 内容 |
|------|------|
| 任务目标 | [一句话描述] |
| 预期结果 | [具体交付物] |
| 验收标准 | [可量化的通过条件] |
| 范围界定 | [must-have vs add-later] |
| 预计Agent数 | [N个，建议≤5] |
| 选定场景 | [场景编号+名称] |
| 协作模式 | [Subagent/Agent Team] |

**Skill完整回退链**（强制执行，不可跳过）：

对每个子任务执行以下3步fallback chain：

1. **本地Skill扫描**：
   - 读取system-reminder中的"available skills"列表
   - 提取每个skill的名称和触发词/描述
   - 将子任务关键词与skill触发词比对
   - 匹配成功 → 标注`[Skill: skill-name]`，进入阶段2直接调用

2. **外部Skill搜索**（本地无匹配时）：
   - 使用 Skill 工具调用 find-skills：
   ```
   Skill(skill="find-skills", args="子任务关键词")
   ```
   - 搜索到 → 向用户推荐：`npx skills add <owner/repo@skill-name> -g -y`
   - 用户确认安装 → 标注新skill，进入阶段2调用
   - 用户拒绝 → 继续第3步

3. **通用Subagent回退**（外部也无匹配时）：
   - 该角色改用`Task`工具生成通用subagent
   - 在团队蓝图中标注`[Type: general-purpose]`

> **铁律**：这3步必须全部执行完才能进入阶段2。不允许跳过find-skills搜索。

### 阶段2：团队组建

输出团队蓝图：

| 编号 | 角色 | 职责 | 模型 | subagent_type | Skill/Type |
|------|------|------|------|---------------|------------|
| 1 | [角色名] | [具体职责] | [opus/sonnet/haiku] | [agent类型] | [Skill: name] 或 [Type: general-purpose] |

> **说明**：最后一列标注该角色使用的Skill名称（阶段1已匹配）或通用类型（fallback）。

### 阶段3：并行执行

- **Skill任务**：用`Skill`工具调用本地已安装的skill → `Skill(skill="skill-name", args="任务描述")`
- **通用任务**：用`Task`工具生成subagent，独立任务并行启动，有依赖的按序执行
- 混合编排时skill和subagent可并行运行
- 每个agent/skill完成后汇报：`✅ [角色名] 完成: [一句话结果]`
- 遇到问题时给用户选项，而不是自己默默选一个

**Agent → Skill 委派**（子agent调用skill的3种模式）：

`general-purpose`类型的subagent拥有所有工具权限，包括`Skill`工具。

| 模式 | 流程 | 适用场景 |
|------|------|---------|
| 协调器直调 | 协调器 → `Skill(skill="name")` → 结果 | 单步Skill任务，无需并行 |
| 委派式调用 | 协调器 → `Task(prompt="请使用 /skill-name 完成 X")` → subagent → `Skill` → 汇报 | 并行多个Skill，或Skill耗时较长 |
| 团队成员调用 | `TeamCreate` → 分配任务 → member → `Skill` → `SendMessage`汇报 | 需要成员间协调的复杂任务 |

委派式调用关键点：Task prompt中写明要调用的Skill名称和参数，subagent会自动识别并调用。

### 阶段4：质量把关 & 产品打磨

**验收检查**：对照阶段1的验收标准逐项检查。

**产品打磨**（不仅功能完整，更要用户体验优秀）：
- 边界处理：异常输入、空值、极端情况是否覆盖
- 专业度：命名规范、代码风格、错误提示是否友好
- 完整性：文档、配置说明、使用示例是否齐全

全部通过 → 进入阶段5。不通过 → 打回修改，最多2轮，仍不通过则通知用户人工介入。

### 阶段5：结果交付 & 部署移交

输出执行报告：

| 项目 | 内容 |
|------|------|
| 总任务数 | X个，成功Y个，失败Z个 |
| 各Agent结果 | [角色]: [状态] - [关键产出] |
| 汇总结论 | [综合所有结果的最终结论] |
| 后续建议 | [当前未覆盖但值得做的改进方向] |

**部署移交**（按需提供）：
- 运行方式：启动命令、环境要求、配置说明
- 验证步骤：用户可自行验证的操作清单
- 已知限制：当前版本的边界和约束

## 执行底线

**【硬性标准】**：
0. **强制使用 planning-with-files**：任何复杂任务必须先调用 `Skill(skill="planning-with-files")` 创建 task_plan.md、findings.md、progress.md
1. **强制执行Skill完整回退链**：本地扫描 → `Skill(skill="find-skills", args="...")` 搜索 → 通用subagent，不允许跳过任何步骤

**【其他原则】**：
2. 先目标，后组织结构——任务不清晰时先澄清，再决定是否组建团队
3. 队伍规模由任务复杂度决定，并行Agent建议不超过5个
4. 关键里程碑必须有质量闸门和回滚点
5. 不默认任何外部工具可用，执行前先验证（含find-skills）
6. 浏览器多窗口默认互相独立，不共享上下文
7. 成本只是约束，不是固定承诺——不做不切实际的成本预估
8. 危险操作、大规模变更必须先获得用户确认

## 故障处理

| 故障类型 | 处理策略 |
|---------|---------|
| Agent执行失败 | 通知用户，提供重试/跳过/终止选项 |
| Skill不可用 | 按回退链降级：本地Skill → find-skills → 通用subagent |
| 模型超时 | 调整任务复杂度或拆分为更小的子任务 |
| 质量不达标 | 打回修改最多2轮，仍不通过则人工介入 |
| 上下文溢出 | 拆分为更小的子任务，分批执行 |
