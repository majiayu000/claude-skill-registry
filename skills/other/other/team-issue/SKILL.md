---
name: team-issue
description: Unified team skill for issue resolution. All roles invoke this skill with --role arg for role-specific execution. Triggers on "team issue".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Issue Resolution

Unified team skill for issue processing pipeline. All team members invoke this skill with `--role=xxx` for role-specific execution.

**Scope**: Issue 处理流程（plan → queue → execute）。Issue 创建/发现由 `issue-discover` 独立处理，CRUD 管理由 `issue-manage` 独立处理。

## Architecture Overview

```
┌───────────────────────────────────────────┐
│  Skill(skill="team-issue")                │
│  args="--role=xxx [issue-ids] [--mode=M]" │
└───────────────┬───────────────────────────┘
                │ Role Router
    ┌───────────┼───────────┬───────────┬───────────┬───────────┐
    ↓           ↓           ↓           ↓           ↓           ↓
┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│coordinator││explorer  ││planner   ││reviewer  ││integrator││implementer│
│ 编排调度  ││EXPLORE-* ││SOLVE-*   ││AUDIT-*   ││MARSHAL-* ││BUILD-*   │
└──────────┘└──────────┘└──────────┘└──────────┘└──────────┘└──────────┘
```

## Command Architecture

```
roles/
├── coordinator.md      # Pipeline 编排（Phase 1/5 inline, Phase 2-4 core logic）
├── explorer.md         # 上下文分析（ACE + cli-explore-agent）
├── planner.md          # 方案设计（wraps issue-plan-agent）
├── reviewer.md         # 方案审查（技术可行性 + 风险评估）
├── integrator.md       # 队列编排（wraps issue-queue-agent）
└── implementer.md      # 代码实现（wraps code-developer）
```

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  // No --role: this is a coordinator entry point
  // Extract issue IDs and mode from args directly
  // → Read roles/coordinator.md and execute
  Read("roles/coordinator.md")
  return
}

const role = roleMatch[1]
const teamName = "issue"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator": { file: "roles/coordinator.md", prefix: null },
  "explorer":    { file: "roles/explorer.md", prefix: "EXPLORE" },
  "planner":     { file: "roles/planner.md", prefix: "SOLVE" },
  "reviewer":    { file: "roles/reviewer.md", prefix: "AUDIT" },
  "integrator":  { file: "roles/integrator.md", prefix: "MARSHAL" },
  "implementer": { file: "roles/implementer.md", prefix: "BUILD" }
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
| `coordinator` | N/A | Pipeline 编排、模式选择、任务分派 | - | [roles/coordinator.md](roles/coordinator.md) |
| `explorer` | EXPLORE-* | 上下文分析、影响面评估 | cli-explore-agent | [roles/explorer.md](roles/explorer.md) |
| `planner` | SOLVE-* | 方案设计、任务分解 | issue-plan-agent | [roles/planner.md](roles/planner.md) |
| `reviewer` | AUDIT-* | 方案审查、风险评估 | - (新角色) | [roles/reviewer.md](roles/reviewer.md) |
| `integrator` | MARSHAL-* | 冲突检测、队列编排 | issue-queue-agent | [roles/integrator.md](roles/integrator.md) |
| `implementer` | BUILD-* | 代码实现、结果提交 | code-developer | [roles/implementer.md](roles/implementer.md) |

## Shared Infrastructure

### Role Isolation Rules

**核心原则**: 每个角色仅能执行自己职责范围内的工作。

#### Output Tagging（强制）

所有角色的输出必须带 `[role_name]` 标识前缀：

```javascript
// SendMessage — content 和 summary 都必须带标识
SendMessage({
  content: `## [${role}] ...`,
  summary: `[${role}] ...`
})

// team_msg — summary 必须带标识
mcp__ccw-tools__team_msg({
  summary: `[${role}] ...`
})
```

#### Coordinator 隔离

| 允许 | 禁止 |
|------|------|
| 需求澄清 (AskUserQuestion) | ❌ 直接编写/修改代码 |
| 创建任务链 (TaskCreate) | ❌ 调用 issue-plan-agent 等实现类 agent |
| 分发任务给 worker | ❌ 直接执行分析/审查 |
| 监控进度 (消息总线) | ❌ 绕过 worker 自行完成任务 |
| 汇报结果给用户 | ❌ 修改源代码或产物文件 |

#### Worker 隔离

| 允许 | 禁止 |
|------|------|
| 处理自己前缀的任务 | ❌ 处理其他角色前缀的任务 |
| SendMessage 给 coordinator | ❌ 直接与其他 worker 通信 |
| 使用 Toolbox 中声明的工具 | ❌ 为其他角色创建任务 (TaskCreate) |
| 委派给复用的 agent | ❌ 修改不属于本职责的资源 |

### Team Configuration

```javascript
const TEAM_CONFIG = {
  name: "issue",
  sessionDir: ".workflow/.team-plan/issue/",
  msgDir: ".workflow/.team-msg/issue/",
  issueDataDir: ".workflow/issues/"
}
```

### Message Bus (All Roles)

Every SendMessage **before**, must call `mcp__ccw-tools__team_msg` to log:

```javascript
mcp__ccw-tools__team_msg({
  operation: "log",
  team: "issue",
  from: role,          // current role name
  to: "coordinator",
  type: "<type>",
  summary: "[role] <summary>",
  ref: "<file_path>"   // optional
})
```

**Message types by role**:

| Role | Types |
|------|-------|
| coordinator | `task_assigned`, `pipeline_update`, `escalation`, `shutdown`, `error` |
| explorer | `context_ready`, `impact_assessed`, `error` |
| planner | `solution_ready`, `multi_solution`, `error` |
| reviewer | `approved`, `rejected`, `concerns`, `error` |
| integrator | `queue_ready`, `conflict_found`, `error` |
| implementer | `impl_complete`, `impl_failed`, `error` |

### CLI 回退

当 `mcp__ccw-tools__team_msg` MCP 不可用时：

```javascript
Bash(`ccw team log --team "issue" --from "${role}" --to "coordinator" --type "<type>" --summary "<摘要>" --json`)
```

### Task Lifecycle (All Roles)

```javascript
// Standard task lifecycle every role follows
// Phase 1: Discovery
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

// Phase 5: Report + Loop — 所有输出必须带 [role] 标识
mcp__ccw-tools__team_msg({ operation: "log", team: "issue", from: role, to: "coordinator", type: "...", summary: `[${role}] ...` })
SendMessage({ type: "message", recipient: "coordinator", content: `## [${role}] ...`, summary: `[${role}] ...` })
TaskUpdate({ taskId: task.id, status: 'completed' })
// Check for next task → back to Phase 1
```

## Pipeline Modes

```
Quick Mode (1-2 simple issues):
  EXPLORE-001 → SOLVE-001 → MARSHAL-001 → BUILD-001

Full Mode (complex issues, with review):
  EXPLORE-001 → SOLVE-001 → AUDIT-001 ─┬─(approved)→ MARSHAL-001 → BUILD-001..N(parallel)
                                         └─(rejected)→ SOLVE-fix → AUDIT-002(re-review, max 2x)

Batch Mode (5-100 issues):
  EXPLORE-001..N(batch≤5) → SOLVE-001..N(batch≤3) → AUDIT-001(batch) → MARSHAL-001 → BUILD-001..M(DAG parallel)
```

### Mode Auto-Detection

```javascript
function detectMode(issueIds, userMode) {
  if (userMode) return userMode  // 用户显式指定

  const count = issueIds.length
  if (count <= 2) {
    // Check complexity via issue priority
    const issues = issueIds.map(id => JSON.parse(Bash(`ccw issue status ${id} --json`)))
    const hasHighPriority = issues.some(i => i.priority >= 4)
    return hasHighPriority ? 'full' : 'quick'
  }
  return 'batch'
}
```

## Coordinator Spawn Template

```javascript
TeamCreate({ team_name: "issue" })

// Explorer
Task({
  subagent_type: "general-purpose",
  team_name: "issue",
  name: "explorer",
  prompt: `你是 team "issue" 的 EXPLORER。

当你收到 EXPLORE-* 任务时，调用 Skill(skill="team-issue", args="--role=explorer") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 EXPLORE-* 前缀的任务，不得执行其他角色的工作
- 所有输出（SendMessage、team_msg）必须带 [explorer] 标识前缀
- 仅与 coordinator 通信，不得直接联系其他 worker
- 不得使用 TaskCreate 为其他角色创建任务

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 EXPLORE-* 任务
2. Skill(skill="team-issue", args="--role=explorer") 执行
3. team_msg log + SendMessage 结果给 coordinator（带 [explorer] 标识）
4. TaskUpdate completed → 检查下一个任务`
})

// Planner
Task({
  subagent_type: "general-purpose",
  team_name: "issue",
  name: "planner",
  prompt: `你是 team "issue" 的 PLANNER。

当你收到 SOLVE-* 任务时，调用 Skill(skill="team-issue", args="--role=planner") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 SOLVE-* 前缀的任务
- 所有输出必须带 [planner] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 SOLVE-* 任务
2. Skill(skill="team-issue", args="--role=planner") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Reviewer
Task({
  subagent_type: "general-purpose",
  team_name: "issue",
  name: "reviewer",
  prompt: `你是 team "issue" 的 REVIEWER。

当你收到 AUDIT-* 任务时，调用 Skill(skill="team-issue", args="--role=reviewer") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 AUDIT-* 前缀的任务
- 所有输出必须带 [reviewer] 标识前缀
- 仅与 coordinator 通信
- 你是质量门控角色，审查方案但不修改代码

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 AUDIT-* 任务
2. Skill(skill="team-issue", args="--role=reviewer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Integrator
Task({
  subagent_type: "general-purpose",
  team_name: "issue",
  name: "integrator",
  prompt: `你是 team "issue" 的 INTEGRATOR。

当你收到 MARSHAL-* 任务时，调用 Skill(skill="team-issue", args="--role=integrator") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 MARSHAL-* 前缀的任务
- 所有输出必须带 [integrator] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 MARSHAL-* 任务
2. Skill(skill="team-issue", args="--role=integrator") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Implementer
Task({
  subagent_type: "general-purpose",
  team_name: "issue",
  name: "implementer",
  prompt: `你是 team "issue" 的 IMPLEMENTER。

当你收到 BUILD-* 任务时，调用 Skill(skill="team-issue", args="--role=implementer") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 BUILD-* 前缀的任务
- 所有输出必须带 [implementer] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 BUILD-* 任务
2. Skill(skill="team-issue", args="--role=implementer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Default to coordinator role |
| Role file not found | Error with expected path (roles/{name}.md) |
| Task prefix conflict | Log warning, proceed |
