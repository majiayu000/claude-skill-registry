---
name: unified-taskflow
description: |
  【强制】复杂任务管理系统。
  AI 必须在遇到以下情况时**先读取此 SKILL.md**，再执行任何操作：
  - 多文件变更、规划设计、新功能开发
  - 用户说"帮我想想/重构/升级/实现"
  禁止使用内置 agentic_mode 的 artifact 目录处理复杂任务，必须使用项目根目录下的 .taskflow/ 目录。
---

# Unified Taskflow v4.1

> 更新：2026-02-13

> [!CAUTION]
> **核心规则**
> 1. 遇到复杂任务时，**必须先读取本文档**，禁止直接使用内置 task_boundary
> 2. 任务管理使用项目根目录下的 `.taskflow/` 目录，**不使用**内置 artifact 目录
> 3. 禁止跨阶段推理 — 执行时不能跳回规划，规划时不能偷跑代码
> 4. 如不确定是否触发，默认触发并询问用户

> **规则优先级**（冲突时按此顺序裁决）：
> **Safety > Correctness > Efficiency > Completeness**

## 触发判断

**触发**：多文件变更、规划设计、"帮我想想/重构/升级/实现"
**不触发**：简单问答、单行修改、明确直接指令

## 按需加载

- 进入 Phase 0 → 读取 [phase0-clarification.md](references/phase0-clarification.md)
- 需要交互决策 → 读取 [interaction-design.md](references/interaction-design.md)
- 治理规则细节 → 读取 [governance.md](references/governance.md)
- Re-grounding 细节 → 读取 [regrounding-protocol.md](references/regrounding-protocol.md)

## 工作流

### Phase 0: 理解快照（Understanding Snapshot）

**目的**：确保 Agent 正确理解用户需求，生成防幻觉锚点。

1. **禁止**立即创建文档或代码
2. Agent 输出**理解快照**：
   - 用户意图（一句话）
   - 识别到的歧义点
   - Agent 的假设（显式列出，用户逐条确认）
3. 用户确认或修正
4. **完备性门禁**（详见 phase0-clarification.md）
5. 写入 `anchor.md`（北极星文件，含版本号）

> 问题框架（参考，不强制全部使用）：边界 / 约束 / 优先级 / 风险
> 详见 [phase0-clarification.md](references/phase0-clarification.md)

### 执行（Elastic Execution）

弹性深度 — 根据任务复杂度自然展开，无固定档位：

- **简单任务**：anchor.md → 直接执行 → 更新 checkpoint.md
- **中等任务**：anchor.md → 拟定计划（口头或 checkpoint 中记录）→ 执行 → 更新 checkpoint.md
- **复杂任务**：anchor.md → 生成 design.md → 执行 → 持续更新 checkpoint.md

执行期间遵守：
- **统一 Checkpoint 协议**：事件驱动的 checkpoint 更新 + 内置 re-grounding 核对（见下方）
- **3-Strike Protocol**：同一问题 3 次失败后升级给用户

### 完成（Completion）

1. 最终 Re-grounding — 逐项核对 anchor.md 的所有 Done-when 条目
2. 向用户报告完成状态
3. 归档任务（移入 archive/）

## 运行机制

### 统一 Checkpoint 协议（合并原 2-Action Rule + Re-grounding）

将进度记录和对齐验证合并为单一机制，减少协议数量，提高遵从率。

**触发事件**（事件驱动，替代模糊的步骤计数）：

| 事件 | 说明 |
|------|------|
| 文件创建/修改 | 每 2 次文件操作触发一次（Debug 窗口放宽为 4 次） |
| 子任务完成 | 每完成一个逻辑子任务 |
| 用户新指令 | 用户补充信息或修改要求 |
| 不确定性 | 遇到模糊决策或多种可行方案 |
| 意图漂移 | 用户当前指令与 anchor.md Intent 语义不一致时 |

**每次 Checkpoint 更新包含**：
1. 做了什么 + 发现了什么
2. **Re-grounding 逐项核对**（对 anchor.md 的 Critical Constraints 和 Done-when 逐条检查状态）
3. 刷新 checkpoint.md 顶部的 **Anchor Mirror**（复制 Intent + Critical Constraints）
4. 下一步计划

**滚动压缩**：checkpoint.md 保留最近 3 条完整记录，旧记录压缩为一行摘要移入「历史摘要」区。

> 详见 [regrounding-protocol.md](references/regrounding-protocol.md)

### 3-Strike Protocol

同一问题连续失败 3 次：
1. Strike 1 — 记录问题和尝试方案
2. Strike 2 — 换一个方向，记录
3. Strike 3 — **停止尝试**，升级给用户，提供已排除方案列表

### RIPER-Core 思维规则

1. 根因解优先 — 禁止用配置/降级掩盖问题
2. 显式因果链 — Why → Condition → Limitation
3. 无魔法数字 — 常数必须来自输入/约束
4. 明确变量 — 信息不足立即暂停询问

## 反模式清单（Anti-Patterns）

> 禁止性指令的遵从率通常高于义务性指令。以下是**不要做**的事：

| 反模式 | 说明 | 正确做法 |
|--------|------|----------|
| 自由文本对齐 | 用"我觉得还在正轨"代替逐项核对 | 必须对 Critical Constraints 和 Done-when 逐条输出状态 |
| Anchor 静默修改 | 未告知用户就修改 anchor.md | 任何 anchor 修改必须用户确认，并更新 Version 和 Change Log |
| Checkpoint 堆积 | 无限追加 checkpoint 不压缩 | 超过 3 条完整记录时，压缩旧记录为摘要 |
| 跳过 Phase 0 | 直接开始执行不做理解快照 | 复杂任务必须先输出理解快照，用户确认后写入 anchor.md |
| 硬约束降级 | 把 Critical Constraint 当 Soft Preference 处理 | Critical Constraint 违反 = 立即暂停请示 |
| 假设隐含 | 不列出假设就开始执行 | 所有假设写入 anchor.md 的 Assumptions 表，用户逐条确认 |
| 忽略意图漂移 | 用户隐式改变方向时不确认就跟着走 | 检测到用户指令与 anchor.md Intent 不一致时，主动确认是否修改 Intent |

## 工作目录

```text
.taskflow/
├── index.json
├── active/[task-name]/
│   ├── anchor.md          # 北极星文件（必须，含版本号）
│   ├── checkpoint.md      # 校验点记录（必须，含 Anchor Mirror）
│   └── design.md          # 技术设计（按需）
└── archive/               # 已归档任务
```

## 交互原则

- 选择题优先，3-4 个选项
- 每个选择点有推荐选项
- 可选参考：[interaction-design.md](references/interaction-design.md)

## 引用文件

| 文件 | 用途 |
|------|------|
| [phase0-clarification.md](references/phase0-clarification.md) | Phase 0 理解快照 + 完备性门禁 |
| [regrounding-protocol.md](references/regrounding-protocol.md) | Re-grounding 逐项核对规则 |
| [governance.md](references/governance.md) | 目录隔离、生命周期、治理规范 |
| [interaction-design.md](references/interaction-design.md) | 交互设计原则（可选参考） |
| [anchor.md 模板](assets/templates/anchor.md) | Grounding Anchor 模板（分层 + 版本号） |
| [checkpoint.md 模板](assets/templates/checkpoint.md) | 校验点记录模板（Anchor Mirror + 滚动压缩） |
| [design.md 模板](assets/templates/design.md) | 技术设计模板（按需） |
