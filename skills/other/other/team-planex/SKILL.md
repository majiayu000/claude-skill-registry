---
name: team-planex
description: Unified team skill for plan-and-execute pipeline. 2-member team (planner + executor) with wave pipeline for concurrent planning and execution. All roles invoke this skill with --role arg. Triggers on "team planex".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team PlanEx

2 成员边规划边执行团队。通过 Wave Pipeline（波次流水线）实现 planner 和 executor 并行工作：planner 完成一个 wave 的 queue 后立即创建 EXEC-* 任务，同时进入下一 wave 规划。所有成员通过 `--role=xxx` 路由。

## Architecture Overview

```
┌──────────────────────────────────────────────┐
│  Skill(skill="team-planex", args="--role=xxx") │
└────────────────┬─────────────────────────────┘
                 │ Role Router
         ┌───────┴───────┐
         ↓               ↓
    ┌─────────┐    ┌──────────┐
    │ planner │    │ executor │
    │ PLAN-*  │    │ EXEC-*   │
    └─────────┘    └──────────┘
```

**设计原则**: 只有 2 个角色，没有独立 coordinator。SKILL.md 入口承担轻量编排（创建团队、派发初始任务链），然后 planner 担任 lead 角色持续推进。

## Role Router

### Input Parsing

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  // No --role: orchestration mode (lightweight coordinator)
  // → See "Orchestration Mode" section below
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "planex"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "planner":  { file: "roles/planner.md",  prefix: "PLAN" },
  "executor": { file: "roles/executor.md", prefix: "EXEC" }
}

if (!VALID_ROLES[role]) {
  throw new Error(`Unknown role: ${role}. Available: ${Object.keys(VALID_ROLES).join(', ')}`)
}

// Read and execute role-specific logic
Read(VALID_ROLES[role].file)
// → Execute the 5-phase process defined in that file
```

### Available Roles

| Role | Task Prefix | Responsibility | Reuses Agent | Role File |
|------|-------------|----------------|--------------|-----------|
| `planner` | PLAN-* | 需求拆解 → issue 创建 → 方案设计 → 队列编排 → EXEC 任务派发 | issue-plan-agent, issue-queue-agent | [roles/planner.md](roles/planner.md) |
| `executor` | EXEC-* | 加载 solution → 代码实现 → 测试 → 提交 | code-developer | [roles/executor.md](roles/executor.md) |

## Input Types

支持 3 种输入方式（通过 args 传入 planner）：

| 输入类型 | 格式 | 示例 |
|----------|------|------|
| Issue IDs | 直接传入 ID | `--role=planner ISS-20260215-001 ISS-20260215-002` |
| 需求文本 | `--text '...'` | `--role=planner --text '实现用户认证模块'` |
| Plan 文件 | `--plan path` | `--role=planner --plan plan/2026-02-15-auth.md` |

## Shared Infrastructure

### Role Isolation Rules

#### Output Tagging（强制）

```javascript
SendMessage({ content: `## [${role}] ...`, summary: `[${role}] ...` })
mcp__ccw-tools__team_msg({ summary: `[${role}] ...` })
```

#### Planner 边界

| 允许 | 禁止 |
|------|------|
| 需求拆解 (issue 创建) | ❌ 直接编写/修改代码 |
| 方案设计 (issue-plan-agent) | ❌ 调用 code-developer |
| 队列编排 (issue-queue-agent) | ❌ 运行测试 |
| 创建 EXEC-* 任务 | ❌ git commit |
| 监控进度 (消息总线) | |

#### Executor 边界

| 允许 | 禁止 |
|------|------|
| 处理 EXEC-* 前缀的任务 | ❌ 创建 issue |
| 调用 code-developer 实现 | ❌ 修改 solution/queue |
| 运行测试验证 | ❌ 为 planner 创建 PLAN-* 任务 |
| git commit 提交 | ❌ 直接与用户交互 (AskUserQuestion) |
| SendMessage 给 planner | |

### Team Configuration

```javascript
const TEAM_CONFIG = {
  name: "planex",
  sessionDir: ".workflow/.team/PEX-{slug}-{date}/",
  msgDir: ".workflow/.team-msg/planex/",
  issueDataDir: ".workflow/issues/"
}
```

### Message Bus

```javascript
mcp__ccw-tools__team_msg({
  operation: "log",
  team: teamName,
  from: role,
  to: role === "planner" ? "executor" : "planner",
  type: "<type>",
  summary: `[${role}] <summary>`,
  ref: "<file_path>"
})
```

**Message types by role**:

| Role | Types |
|------|-------|
| planner | `wave_ready`, `queue_ready`, `all_planned`, `error` |
| executor | `impl_complete`, `impl_failed`, `wave_done`, `error` |

### CLI Fallback

```javascript
Bash(`ccw team log --team "${teamName}" --from "${role}" --to "${role === 'planner' ? 'executor' : 'planner'}" --type "<type>" --summary "<summary>" --json`)
```

### Task Lifecycle (Both Roles)

```javascript
const tasks = TaskList()
const myTasks = tasks.filter(t =>
  t.subject.startsWith(`${VALID_ROLES[role].prefix}-`) &&
  t.owner === role &&
  t.status === 'pending' &&
  t.blockedBy.length === 0
)
if (myTasks.length === 0) return // idle
const task = TaskGet({ taskId: myTasks[0].id })
TaskUpdate({ taskId: task.id, status: 'in_progress' })
// Phase 2-4: Role-specific (see roles/{role}.md)
// Phase 5: Report + Loop
```

## Wave Pipeline

```
Wave 1:  planner 创建 issues + 规划 solutions + 形成 queue
                ↓ (queue ready → 创建 EXEC-* 任务)
Wave 1 执行:  executor 开始实现  ←→  planner 继续规划 Wave 2
                                         ↓
Wave 2 执行:  executor 实现 Wave 2  ←→  planner 规划 Wave 3
                ...
Final:   planner 发送 all_planned → executor 完成剩余 EXEC-* → 结束
```

**波次规则**:
- planner 每完成一个 wave 的 queue 后，立即创建 EXEC-* 任务供 executor 消费
- planner 不等待 executor 完成当前 wave，直接进入下一 wave
- executor 持续轮询并消费可用的 EXEC-* 任务
- 当 planner 发送 `all_planned` 消息后，executor 完成所有剩余任务即可结束

## Execution Method Selection

在编排模式或直接调用 executor 前，**必须先确定执行方式**。支持 3 种执行后端：

| Executor | 后端 | 适用场景 |
|----------|------|----------|
| `agent` | code-developer subagent | 简单任务、同步执行 |
| `codex` | `ccw cli --tool codex --mode write` | 复杂任务、后台执行 |
| `gemini` | `ccw cli --tool gemini --mode write` | 分析类任务、后台执行 |

### 选择逻辑

```javascript
// ★ 统一 auto mode 检测：-y/--yes 从 $ARGUMENTS 或 ccw 传播
const autoYes = /\b(-y|--yes)\b/.test(args)
const explicitExec = args.match(/--exec[=\s]+(agent|codex|gemini|auto)/i)?.[1]

let executionConfig

if (explicitExec) {
  // 显式指定
  executionConfig = {
    executionMethod: explicitExec.charAt(0).toUpperCase() + explicitExec.slice(1),
    codeReviewTool: "Skip"
  }
} else if (autoYes) {
  // Auto 模式：默认 Agent + Skip review
  executionConfig = { executionMethod: "Auto", codeReviewTool: "Skip" }
} else {
  // 交互选择
  executionConfig = AskUserQuestion({
    questions: [
      {
        question: "选择执行方式:",
        header: "Execution",
        multiSelect: false,
        options: [
          { label: "Agent", description: "code-developer agent（同步，适合简单任务）" },
          { label: "Codex", description: "Codex CLI（后台，适合复杂任务）" },
          { label: "Gemini", description: "Gemini CLI（后台，适合分析类任务）" },
          { label: "Auto", description: "根据任务复杂度自动选择" }
        ]
      },
      {
        question: "执行后是否进行代码审查?",
        header: "Code Review",
        multiSelect: false,
        options: [
          { label: "Skip", description: "不审查" },
          { label: "Gemini Review", description: "Gemini CLI 审查" },
          { label: "Codex Review", description: "Git-aware review（--uncommitted）" },
          { label: "Agent Review", description: "当前 agent 审查" }
        ]
      }
    ]
  })
}

// Auto 解析：根据 solution task_count 决定
function resolveExecutor(taskCount) {
  if (executionConfig.executionMethod === 'Auto') {
    return taskCount <= 3 ? 'agent' : 'codex'
  }
  return executionConfig.executionMethod.toLowerCase()
}
```

### 通过 args 指定

```bash
# 显式指定
Skill(skill="team-planex", args="--exec=codex ISS-xxx")
Skill(skill="team-planex", args="--exec=agent --text '简单功能'")

# Auto 模式（跳过交互，-y 或 --yes）
Skill(skill="team-planex", args="-y --text '添加日志'")
```

## Orchestration Mode

当不带 `--role` 调用时，SKILL.md 进入轻量编排模式：

```javascript
// 1. 创建团队
TeamCreate({ team_name: teamName })

// 2. 解析输入参数
const issueIds = args.match(/ISS-\d{8}-\d{6}/g) || []
const textMatch = args.match(/--text\s+['"]([^'"]+)['"]/)
const planMatch = args.match(/--plan\s+(\S+)/)

let plannerInput = args  // 透传给 planner

// 3. 执行方式选择（见上方 Execution Method Selection）
// executionConfig 已确定: { executionMethod, codeReviewTool }

// 4. 创建初始 PLAN-* 任务
TaskCreate({
  subject: "PLAN-001: 初始规划",
  description: `规划任务。输入: ${plannerInput}`,
  activeForm: "规划中",
  owner: "planner"
})

// 5. Spawn planner agent
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "planner",
  prompt: `你是 team "${teamName}" 的 PLANNER。
当你收到 PLAN-* 任务时，调用 Skill(skill="team-planex", args="--role=planner") 执行。
当前输入: ${plannerInput}

## 执行配置
executor 的执行方式已确定: ${executionConfig.executionMethod}
创建 EXEC-* 任务时，在 description 中包含:
  execution_method: ${executionConfig.executionMethod}
  code_review: ${executionConfig.codeReviewTool}

## 角色准则（强制）
- 你只能处理 PLAN-* 前缀的任务
- 所有输出必须带 [planner] 标识前缀
- 完成每个 wave 后立即创建 EXEC-* 任务供 executor 消费
- EXEC-* 任务 description 中必须包含 execution_method 字段

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 PLAN-* 任务
2. Skill(skill="team-planex", args="--role=planner") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// 6. Spawn executor agent
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "executor",
  prompt: `你是 team "${teamName}" 的 EXECUTOR。
当你收到 EXEC-* 任务时，调用 Skill(skill="team-planex", args="--role=executor") 执行。

## 执行配置
默认执行方式: ${executionConfig.executionMethod}
代码审查: ${executionConfig.codeReviewTool}
（每个 EXEC-* 任务 description 中可能包含 execution_method 覆盖）

## 角色准则（强制）
- 你只能处理 EXEC-* 前缀的任务
- 所有输出必须带 [executor] 标识前缀
- 根据 execution_method 选择执行后端（Agent/Codex/Gemini）
- 每个 solution 完成后通知 planner

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 EXEC-* 任务（等待 planner 创建）
2. Skill(skill="team-planex", args="--role=executor") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Enter orchestration mode |
| Role file not found | Error with expected path (roles/{name}.md) |
| Planner wave failure | Retry once, then report error and halt pipeline |
| Executor impl failure | Report to planner, continue with next EXEC-* task |
| No EXEC-* tasks yet | Executor idles, polls for new tasks |
| Pipeline stall | Planner monitors — if executor blocked > 2 tasks, escalate to user |
