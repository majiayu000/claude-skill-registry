---
name: ccw
description: Stateless workflow orchestrator. Auto-selects optimal workflow based on task intent. Triggers "ccw", "workflow".
allowed-tools: Task(*), SlashCommand(*), AskUserQuestion(*), Read(*), Bash(*), Grep(*), TodoWrite(*)
---

# CCW - Claude Code Workflow Orchestrator

无状态工作流协调器，根据任务意图自动选择最优工作流。

## Workflow System Overview

CCW 提供两个工作流系统：**Main Workflow** 和 **Issue Workflow**，协同覆盖完整的软件开发生命周期。

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Main Workflow                                  │
│                                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │   Level 1   │ → │   Level 2   │ → │   Level 3   │ → │   Level 4   │     │
│  │   Rapid     │   │ Lightweight │   │  Standard   │   │ Brainstorm  │     │
│  │             │   │             │   │             │   │             │     │
│  │ lite-lite-  │   │ lite-plan   │   │    plan     │   │ brainstorm  │     │
│  │    lite     │   │ lite-fix    │   │  tdd-plan   │   │  :auto-     │     │
│  │             │   │ multi-cli-  │   │ test-fix-   │   │  parallel   │     │
│  │             │   │    plan     │   │    gen      │   │     ↓       │     │
│  │             │   │             │   │             │   │   plan      │     │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │
│                                                                             │
│  Complexity: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▶  │
│              Low                                                    High    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ After development
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Issue Workflow                                 │
│                                                                             │
│     ┌──────────────┐         ┌──────────────┐         ┌──────────────┐     │
│     │  Accumulate  │    →    │    Plan      │    →    │   Execute    │     │
│     │  Discover &  │         │    Batch     │         │   Parallel   │     │
│     │   Collect    │         │   Planning   │         │  Execution   │     │
│     └──────────────┘         └──────────────┘         └──────────────┘     │
│                                                                             │
│     Supplementary role: Maintain main branch stability, worktree isolation  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  CCW Orchestrator (CLI-Enhanced + Requirement Analysis)         │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1    │ Input Analysis (rule-based, fast path)            │
│  Phase 1.5  │ CLI Classification (semantic, smart path)         │
│  Phase 1.75 │ Requirement Clarification (clarity < 2)           │
│  Phase 2    │ Level Selection (intent → level → workflow)       │
│  Phase 2.5  │ CLI Action Planning (high complexity)             │
│  Phase 3    │ User Confirmation (optional)                      │
│  Phase 4    │ TODO Tracking Setup                               │
│  Phase 5    │ Execution Loop                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Level Quick Reference

| Level | Name | Workflows | Artifacts | Execution |
|-------|------|-----------|-----------|-----------|
| **1** | Rapid | `lite-lite-lite` | None | Direct execute |
| **2** | Lightweight | `lite-plan`, `lite-fix`, `multi-cli-plan` | Memory/Lightweight files | → `lite-execute` |
| **3** | Standard | `plan`, `tdd-plan`, `test-fix-gen` | Session persistence | → `execute` / `test-cycle-execute` |
| **4** | Brainstorm | `brainstorm:auto-parallel` → `plan` | Multi-role analysis + Session | → `execute` |
| **-** | Issue | `discover` → `plan` → `queue` → `execute` | Issue records | Worktree isolation (optional) |

## Workflow Selection Decision Tree

```
Start
  │
  ├─ Is it post-development maintenance?
  │     ├─ Yes → Issue Workflow
  │     └─ No ↓
  │
  ├─ Are requirements clear?
  │     ├─ Uncertain → Level 4 (brainstorm:auto-parallel)
  │     └─ Clear ↓
  │
  ├─ Need persistent Session?
  │     ├─ Yes → Level 3 (plan / tdd-plan / test-fix-gen)
  │     └─ No ↓
  │
  ├─ Need multi-perspective / solution comparison?
  │     ├─ Yes → Level 2 (multi-cli-plan)
  │     └─ No ↓
  │
  ├─ Is it a bug fix?
  │     ├─ Yes → Level 2 (lite-fix)
  │     └─ No ↓
  │
  ├─ Need planning?
  │     ├─ Yes → Level 2 (lite-plan)
  │     └─ No → Level 1 (lite-lite-lite)
```

## Intent Classification

### Priority Order (with Level Mapping)

| Priority | Intent | Patterns | Level | Flow |
|----------|--------|----------|-------|------|
| 1 | bugfix/hotfix | `urgent,production,critical` + bug | L2 | `bugfix.hotfix` |
| 1 | bugfix | `fix,bug,error,crash,fail` | L2 | `bugfix.standard` |
| 2 | issue batch | `issues,batch` + `fix,resolve` | Issue | `issue` |
| 3 | exploration | `不确定,explore,研究,what if` | L4 | `full` |
| 3 | multi-perspective | `多视角,权衡,比较方案,cross-verify` | L2 | `multi-cli-plan` |
| 4 | quick-task | `快速,简单,small,quick` + feature | L1 | `lite-lite-lite` |
| 5 | ui design | `ui,design,component,style` | L3/L4 | `ui` |
| 6 | tdd | `tdd,test-driven,先写测试` | L3 | `tdd` |
| 7 | test-fix | `测试失败,test fail,fix test` | L3 | `test-fix-gen` |
| 8 | review | `review,审查,code review` | L3 | `review-fix` |
| 9 | documentation | `文档,docs,readme` | L2 | `docs` |
| 99 | feature | complexity-based | L2/L3 | `rapid`/`coupled` |

### Quick Selection Guide

| Scenario | Recommended Workflow | Level |
|----------|---------------------|-------|
| Quick fixes, config adjustments | `lite-lite-lite` | 1 |
| Clear single-module features | `lite-plan → lite-execute` | 2 |
| Bug diagnosis and fix | `lite-fix` | 2 |
| Production emergencies | `lite-fix --hotfix` | 2 |
| Technology selection, solution comparison | `multi-cli-plan → lite-execute` | 2 |
| Multi-module changes, refactoring | `plan → verify → execute` | 3 |
| Test-driven development | `tdd-plan → execute → tdd-verify` | 3 |
| Test failure fixes | `test-fix-gen → test-cycle-execute` | 3 |
| New features, architecture design | `brainstorm:auto-parallel → plan → execute` | 4 |
| Post-development issue fixes | Issue Workflow | - |

### Complexity Assessment

```javascript
function assessComplexity(text) {
  let score = 0
  if (/refactor|重构|migrate|迁移|architect|架构|system|系统/.test(text)) score += 2
  if (/multiple|多个|across|跨|all|所有|entire|整个/.test(text)) score += 2
  if (/integrate|集成|api|database|数据库/.test(text)) score += 1
  if (/security|安全|performance|性能|scale|扩展/.test(text)) score += 1
  return score >= 4 ? 'high' : score >= 2 ? 'medium' : 'low'
}
```

| Complexity | Flow |
|------------|------|
| high | `coupled` (plan → verify → execute) |
| medium/low | `rapid` (lite-plan → lite-execute) |

### Dimension Extraction (WHAT/WHERE/WHY/HOW)

从用户输入提取四个维度，用于需求澄清和工作流选择：

| 维度 | 提取内容 | 示例模式 |
|------|----------|----------|
| **WHAT** | action + target | `创建/修复/重构/优化/分析` + 目标对象 |
| **WHERE** | scope + paths | `file/module/system` + 文件路径 |
| **WHY** | goal + motivation | `为了.../因为.../目的是...` |
| **HOW** | constraints + preferences | `必须.../不要.../应该...` |

**Clarity Score** (0-3):
- +0.5: 有明确 action
- +0.5: 有具体 target
- +0.5: 有文件路径
- +0.5: scope 不是 unknown
- +0.5: 有明确 goal
- +0.5: 有约束条件
- -0.5: 包含不确定词 (`不知道/maybe/怎么`)

### Requirement Clarification

当 `clarity_score < 2` 时触发需求澄清：

```javascript
if (dimensions.clarity_score < 2) {
  const questions = generateClarificationQuestions(dimensions)
  // 生成问题：目标是什么? 范围是什么? 有什么约束?
  AskUserQuestion({ questions })
}
```

**澄清问题类型**:
- 目标不明确 → "你想要对什么进行操作?"
- 范围不明确 → "操作的范围是什么?"
- 目的不明确 → "这个操作的主要目标是什么?"
- 复杂操作 → "有什么特殊要求或限制?"

## TODO Tracking Protocol

### CRITICAL: Append-Only Rule

CCW 创建的 Todo **必须附加到现有列表**，不能覆盖用户的其他 Todo。

### Implementation

```javascript
// 1. 使用 CCW 前缀隔离工作流 todo
const prefix = `CCW:${flowName}`

// 2. 创建新 todo 时使用前缀格式
TodoWrite({
  todos: [
    ...existingNonCCWTodos,  // 保留用户的 todo
    { content: `${prefix}: [1/N] /command:step1`, status: "in_progress", activeForm: "..." },
    { content: `${prefix}: [2/N] /command:step2`, status: "pending", activeForm: "..." }
  ]
})

// 3. 更新状态时只修改匹配前缀的 todo
```

### Todo Format

```
CCW:{flow}: [{N}/{Total}] /command:name
```

### Visual Example

```
✓ CCW:rapid: [1/2] /workflow:lite-plan
→ CCW:rapid: [2/2] /workflow:lite-execute
  用户自己的 todo（保留不动）
```

### Status Management

- 开始工作流：创建所有步骤 todo，第一步 `in_progress`
- 完成步骤：当前步骤 `completed`，下一步 `in_progress`
- 工作流结束：所有 CCW todo 标记 `completed`

## Execution Flow

```javascript
// 1. Check explicit command
if (input.startsWith('/workflow:') || input.startsWith('/issue:')) {
  SlashCommand(input)
  return
}

// 2. Classify intent
const intent = classifyIntent(input)  // See command.json intent_rules

// 3. Select flow
const flow = selectFlow(intent)  // See command.json flows

// 4. Create todos with CCW prefix
createWorkflowTodos(flow)

// 5. Dispatch first command
SlashCommand(flow.steps[0].command, args: input)
```

## CLI Tool Integration

CCW 在特定条件下自动注入 CLI 调用：

| Condition | CLI Inject |
|-----------|------------|
| 大量代码上下文 (≥50k chars) | `gemini --mode analysis` |
| 高复杂度任务 | `gemini --mode analysis` |
| Bug 诊断 | `gemini --mode analysis` |
| 多任务执行 (≥3 tasks) | `codex --mode write` |

### CLI Enhancement Phases

**Phase 1.5: CLI-Assisted Classification**

当规则匹配不明确时，使用 CLI 辅助分类：

| 触发条件 | 说明 |
|----------|------|
| matchCount < 2 | 多个意图模式匹配 |
| complexity = high | 高复杂度任务 |
| input > 100 chars | 长输入需要语义理解 |

**Phase 2.5: CLI-Assisted Action Planning**

高复杂度任务的工作流优化：

| 触发条件 | 说明 |
|----------|------|
| complexity = high | 高复杂度任务 |
| steps >= 3 | 多步骤工作流 |
| input > 200 chars | 复杂需求描述 |

CLI 可返回建议：`use_default` | `modify` (调整步骤) | `upgrade` (升级工作流)

## Continuation Commands

工作流执行中的用户控制命令：

| 命令 | 作用 |
|------|------|
| `continue` | 继续执行下一步 |
| `skip` | 跳过当前步骤 |
| `abort` | 终止工作流 |
| `/workflow:*` | 切换到指定命令 |
| 自然语言 | 重新分析意图 |

## Workflow Flow Details

### Issue Workflow (Main Workflow 补充机制)

Issue Workflow 是 Main Workflow 的**补充机制**，专注于开发后的持续维护。

#### 设计理念

| 方面 | Main Workflow | Issue Workflow |
|------|---------------|----------------|
| **用途** | 主要开发周期 | 开发后维护 |
| **时机** | 功能开发阶段 | 主工作流完成后 |
| **范围** | 完整功能实现 | 针对性修复/增强 |
| **并行性** | 依赖分析 → Agent 并行 | Worktree 隔离 (可选) |
| **分支模型** | 当前分支工作 | 可使用隔离的 worktree |

#### 为什么 Main Workflow 不自动使用 Worktree？

**依赖分析已解决并行性问题**：
1. 规划阶段 (`/workflow:plan`) 执行依赖分析
2. 自动识别任务依赖和关键路径
3. 划分为**并行组**（独立任务）和**串行链**（依赖任务）
4. Agent 并行执行独立任务，无需文件系统隔离

#### 两阶段生命周期

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Phase 1: Accumulation (积累阶段)                  │
│                                                                     │
│   Triggers: 任务完成后的 review、代码审查发现、测试失败              │
│                                                                     │
│   ┌────────────┐     ┌────────────┐     ┌────────────┐             │
│   │ discover   │     │ discover-  │     │    new     │             │
│   │ Auto-find  │     │ by-prompt  │     │  Manual    │             │
│   └────────────┘     └────────────┘     └────────────┘             │
│                                                                     │
│   持续积累 issues 到待处理队列                                       │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               │ 积累足够后
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Phase 2: Batch Resolution (批量解决阶段)            │
│                                                                     │
│   ┌────────────┐     ┌────────────┐     ┌────────────┐             │
│   │   plan     │ ──→ │   queue    │ ──→ │  execute   │             │
│   │ --all-     │     │ Optimize   │     │  Parallel  │             │
│   │  pending   │     │  order     │     │ execution  │             │
│   └────────────┘     └────────────┘     └────────────┘             │
│                                                                     │
│   支持 worktree 隔离，保持主分支稳定                                 │
└─────────────────────────────────────────────────────────────────────┘
```

#### 与 Main Workflow 的协作

```
开发迭代循环
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   ┌─────────┐                              ┌─────────┐             │
│   │ Feature │ ──→ Main Workflow ──→ Done ──→│ Review  │             │
│   │ Request │     (Level 1-4)              └────┬────┘             │
│   └─────────┘                                   │                  │
│        ▲                                        │ 发现 Issues       │
│        │                                        ▼                  │
│        │                                  ┌─────────┐              │
│   继续 │                                  │  Issue  │              │
│   新功能│                                  │ Workflow│              │
│        │                                  └────┬────┘              │
│        │         ┌──────────────────────────────┘                   │
│        │         │ 修复完成                                          │
│        │         ▼                                                 │
│   ┌────┴────┐◀──────                                               │
│   │  Main   │    Merge                                             │
│   │ Branch  │    back                                              │
│   └─────────┘                                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 命令列表

**积累阶段：**
```bash
/issue:discover            # 多视角自动发现
/issue:discover-by-prompt  # 基于提示发现
/issue:new                 # 手动创建
```

**批量解决阶段：**
```bash
/issue:plan --all-pending  # 批量规划所有待处理
/issue:queue               # 生成优化执行队列
/issue:execute             # 并行执行
```

### lite-lite-lite vs multi-cli-plan

| 维度 | lite-lite-lite | multi-cli-plan |
|------|---------------|----------------|
| **产物** | 无文件 | IMPL_PLAN.md + plan.json + synthesis.json |
| **状态** | 无状态 | 持久化 session |
| **CLI选择** | 自动分析任务类型选择 | 配置驱动 |
| **迭代** | 通过 AskUser | 多轮收敛 |
| **执行** | 直接执行 | 通过 lite-execute |
| **适用** | 快速修复、简单功能 | 复杂多步骤实现 |

**选择指南**：
- 任务清晰、改动范围小 → `lite-lite-lite`
- 需要多视角分析、复杂架构 → `multi-cli-plan`

### multi-cli-plan vs lite-plan

| 维度 | multi-cli-plan | lite-plan |
|------|---------------|-----------|
| **上下文** | ACE 语义搜索 | 手动文件模式 |
| **分析** | 多 CLI 交叉验证 | 单次规划 |
| **迭代** | 多轮直到收敛 | 单轮 |
| **置信度** | 高 (共识驱动) | 中 (单一视角) |
| **适用** | 需要多视角的复杂任务 | 直接明确的实现 |

**选择指南**：
- 需求明确、路径清晰 → `lite-plan`
- 需要权衡、多方案比较 → `multi-cli-plan`

## Artifact Flow Protocol

工作流产出的自动流转机制，支持不同格式产出间的意图提取和完成度判断。

### 产出格式

| 命令 | 产出位置 | 格式 | 关键字段 |
|------|----------|------|----------|
| `/workflow:lite-plan` | memory://plan | structured_plan | tasks, files, dependencies |
| `/workflow:plan` | .workflow/{session}/IMPL_PLAN.md | markdown_plan | phases, tasks, risks |
| `/workflow:execute` | execution_log.json | execution_report | completed_tasks, errors |
| `/workflow:test-cycle-execute` | test_results.json | test_report | pass_rate, failures, coverage |
| `/workflow:review-session-cycle` | review_report.md | review_report | findings, severity_counts |

### 意图提取 (Intent Extraction)

流转到下一步时，自动提取关键信息：

```
plan → execute:
  提取: tasks (未完成), priority_order, files_to_modify, context_summary

execute → test:
  提取: modified_files, test_scope (推断), pending_verification

test → fix:
  条件: pass_rate < 0.95
  提取: failures, error_messages, affected_files, suggested_fixes

review → fix:
  条件: critical > 0 OR high > 3
  提取: findings (critical/high), fix_priority, affected_files
```

### 完成度判断

**Test 完成度路由**:
```
pass_rate >= 0.95 AND coverage >= 0.80  → complete
pass_rate >= 0.95 AND coverage < 0.80   → add_more_tests
pass_rate >= 0.80                        → fix_failures_then_continue
pass_rate < 0.80                         → major_fix_required
```

**Review 完成度路由**:
```
critical == 0 AND high <= 3  → complete_or_optional_fix
critical > 0                  → mandatory_fix
high > 3                      → recommended_fix
```

### 流转决策模式

**plan_execute_test**:
```
plan → execute → test
         ↓ (if test fail)
    extract_failures → fix → test (max 3 iterations)
         ↓ (if still fail)
    manual_intervention
```

**iterative_improvement**:
```
execute → test → fix → test → ...
    loop until: pass_rate >= 0.95 OR iterations >= 3
```

### 使用示例

```javascript
// 执行完成后，根据产出决定下一步
const result = await execute(plan)

// 提取意图流转到测试
const testContext = extractIntent('execute_to_test', result)
// testContext = { modified_files, test_scope, pending_verification }

// 测试完成后，根据完成度决定路由
const testResult = await test(testContext)
const nextStep = evaluateCompletion('test', testResult)
// nextStep = 'fix_failures_then_continue' if pass_rate = 0.85
```

## Reference

- [command.json](command.json) - 命令元数据、Flow 定义、意图规则、Artifact Flow
