---
name: team-iterdev
description: Unified team skill for iterative development team. All roles invoke this skill with --role arg for role-specific execution. Triggers on "team iterdev".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team IterDev

持续迭代开发团队技能。通过 Generator-Critic 循环（developer↔reviewer，最多3轮）、任务账本（task-ledger.json）实时进度追踪、共享记忆（Sprint间学习）和动态管道选择，实现增量交付开发。所有团队成员通过 `--role=xxx` 路由。

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│  Skill(skill="team-iterdev", args="--role=xxx")   │
└───────────────────┬──────────────────────────────┘
                    │ Role Router
    ┌───────────┬───┼───────────┬───────────┐
    ↓           ↓   ↓           ↓           ↓
┌──────────┐┌─────────┐┌─────────┐┌──────┐┌────────┐
│coordinator││architect││developer││tester││reviewer│
│ roles/   ││ roles/  ││ roles/  ││roles/││ roles/ │
└──────────┘└─────────┘└─────────┘└──────┘└────────┘
```

## Role Router

### Input Parsing

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, architect, developer, tester, reviewer")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "iterdev"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator": { file: "roles/coordinator.md", prefix: null },
  "architect":   { file: "roles/architect.md",   prefix: "DESIGN" },
  "developer":   { file: "roles/developer.md",   prefix: "DEV" },
  "tester":      { file: "roles/tester.md",      prefix: "VERIFY" },
  "reviewer":    { file: "roles/reviewer.md",    prefix: "REVIEW" }
}

if (!VALID_ROLES[role]) {
  throw new Error(`Unknown role: ${role}. Available: ${Object.keys(VALID_ROLES).join(', ')}`)
}

Read(VALID_ROLES[role].file)
```

### Available Roles

| Role | Task Prefix | Responsibility | Role File |
|------|-------------|----------------|-----------|
| `coordinator` | N/A | Sprint规划、积压管理、任务账本维护 | [roles/coordinator.md](roles/coordinator.md) |
| `architect` | DESIGN-* | 技术设计、任务分解、架构决策 | [roles/architect.md](roles/architect.md) |
| `developer` | DEV-* | 代码实现、增量交付 | [roles/developer.md](roles/developer.md) |
| `tester` | VERIFY-* | 测试执行、修复循环、回归检测 | [roles/tester.md](roles/tester.md) |
| `reviewer` | REVIEW-* | 代码审查、质量评分、改进建议 | [roles/reviewer.md](roles/reviewer.md) |

## Shared Infrastructure

### Role Isolation Rules

#### Output Tagging（强制）

```javascript
SendMessage({ content: `## [${role}] ...`, summary: `[${role}] ...` })
mcp__ccw-tools__team_msg({ summary: `[${role}] ...` })
```

#### Coordinator 隔离

| 允许 | 禁止 |
|------|------|
| Sprint 规划 (AskUserQuestion) | ❌ 直接编写代码 |
| 创建任务链 (TaskCreate) | ❌ 直接执行测试/审查 |
| 维护任务账本 (task-ledger.json) | ❌ 调用 code-developer 等实现类 subagent |
| 监控进度 | ❌ 绕过 worker 自行完成 |

#### Worker 隔离

| 允许 | 禁止 |
|------|------|
| 处理自己前缀的任务 | ❌ 处理其他角色前缀的任务 |
| 读写 shared-memory.json (自己的字段) | ❌ 为其他角色创建任务 |
| SendMessage 给 coordinator | ❌ 直接与其他 worker 通信 |

### Team Configuration

```javascript
const TEAM_CONFIG = {
  name: "iterdev",
  sessionDir: ".workflow/.team/IDS-{slug}-{date}/",
  msgDir: ".workflow/.team-msg/iterdev/",
  sharedMemory: "shared-memory.json",
  taskLedger: "task-ledger.json"
}
```

### Task Ledger (创新模式 — 任务账本)

实时追踪所有 Sprint 任务进度：

```javascript
// task-ledger.json structure
{
  "sprint_id": "sprint-1",
  "sprint_goal": "...",
  "tasks": [
    {
      "id": "DEV-001",
      "title": "...",
      "owner": "developer",
      "status": "completed",         // pending | in_progress | completed | blocked
      "started_at": "...",
      "completed_at": "...",
      "gc_rounds": 0,                // Generator-Critic iterations
      "review_score": null,           // reviewer 评分
      "test_pass_rate": null          // tester 通过率
    }
  ],
  "metrics": {
    "total": 5,
    "completed": 3,
    "in_progress": 1,
    "blocked": 0,
    "velocity": 3                     // tasks completed this sprint
  }
}

// Coordinator updates ledger at each task transition
function updateLedger(sessionFolder, taskId, updates) {
  const ledger = JSON.parse(Read(`${sessionFolder}/task-ledger.json`))
  const task = ledger.tasks.find(t => t.id === taskId)
  if (task) Object.assign(task, updates)
  // Recalculate metrics
  ledger.metrics.completed = ledger.tasks.filter(t => t.status === 'completed').length
  ledger.metrics.in_progress = ledger.tasks.filter(t => t.status === 'in_progress').length
  Write(`${sessionFolder}/task-ledger.json`, JSON.stringify(ledger, null, 2))
}
```

### Shared Memory (Sprint间学习)

```javascript
// shared-memory.json — accumulated across sprints
{
  "sprint_history": [
    {
      "sprint_id": "sprint-1",
      "what_worked": ["..."],
      "what_failed": ["..."],
      "patterns_learned": ["..."]
    }
  ],
  "architecture_decisions": [],
  "implementation_context": [],
  "review_feedback_trends": []
}
```

### Message Bus

```javascript
mcp__ccw-tools__team_msg({
  operation: "log", team: teamName, from: role, to: "coordinator",
  type: "<type>", summary: `[${role}] <summary>`, ref: "<file_path>"
})
```

| Role | Types |
|------|-------|
| coordinator | `sprint_started`, `gc_loop_trigger`, `sprint_complete`, `task_unblocked`, `error`, `shutdown` |
| architect | `design_ready`, `design_revision`, `error` |
| developer | `dev_complete`, `dev_progress`, `error` |
| tester | `verify_passed`, `verify_failed`, `fix_required`, `error` |
| reviewer | `review_passed`, `review_revision`, `review_critical`, `error` |

### CLI Fallback

```javascript
Bash(`ccw team log --team "${teamName}" --from "${role}" --to "coordinator" --type "<type>" --summary "<summary>" --json`)
```

### Task Lifecycle (All Worker Roles)

```javascript
const tasks = TaskList()
const myTasks = tasks.filter(t =>
  t.subject.startsWith(`${VALID_ROLES[role].prefix}-`) &&
  t.owner === role && t.status === 'pending' && t.blockedBy.length === 0
)
if (myTasks.length === 0) return
const task = TaskGet({ taskId: myTasks[0].id })
TaskUpdate({ taskId: task.id, status: 'in_progress' })
// Phase 2-4: Role-specific
// Phase 5: Report + Loop
```

## Three-Pipeline Architecture

```
Patch (简单修复):
  DEV-001 → VERIFY-001

Sprint (标准特性):
  DESIGN-001 → DEV-001 → [VERIFY-001 + REVIEW-001](parallel)

Multi-Sprint (大型特性):
  Sprint 1: DESIGN-001 → DEV-001 → DEV-002(incremental) → VERIFY-001 → DEV-fix → REVIEW-001
  Sprint 2: DESIGN-002(refined) → DEV-003 → VERIFY-002 → REVIEW-002
  ...
```

### Generator-Critic Loop

developer ↔ reviewer 循环，最多3轮：

```
DEV → REVIEW → (if review.critical_count > 0 || review.score < 7)
              → DEV-fix → REVIEW-2 → (if still issues) → DEV-fix-2 → REVIEW-3
              → (max 3 rounds, then accept with warning)
```

### Multi-Sprint Dynamic Downgrade

```javascript
// If Sprint N is progressing well, downgrade Sprint N+1 complexity
if (sprintMetrics.velocity >= expectedVelocity && sprintMetrics.review_avg >= 8) {
  // Next sprint: skip detailed design, use simplified pipeline
  nextPipeline = 'sprint' // downgrade from multi-sprint
}
```

## Unified Session Directory

```
.workflow/.team/IDS-{slug}-{YYYY-MM-DD}/
├── team-session.json
├── shared-memory.json          # Sprint间学习: what_worked / what_failed / patterns_learned
├── task-ledger.json            # 实时任务进度账本
├── design/                     # Architect output
│   ├── design-001.md
│   └── task-breakdown.json
├── code/                       # Developer tracking
│   └── dev-log.md
├── verify/                     # Tester output
│   └── verify-001.json
└── review/                     # Reviewer output
    └── review-001.md
```

## Coordinator Spawn Template

```javascript
TeamCreate({ team_name: teamName })

// Architect
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "architect",
  prompt: `你是 team "${teamName}" 的 ARCHITECT。
当你收到 DESIGN-* 任务时，调用 Skill(skill="team-iterdev", args="--role=architect") 执行。
当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 DESIGN-* 前缀的任务
- 所有输出必须带 [architect] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 DESIGN-* 任务
2. Skill(skill="team-iterdev", args="--role=architect") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Developer
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "developer",
  prompt: `你是 team "${teamName}" 的 DEVELOPER。
当你收到 DEV-* 任务时，调用 Skill(skill="team-iterdev", args="--role=developer") 执行。
当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 DEV-* 前缀的任务
- 所有输出必须带 [developer] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 DEV-* 任务
2. Skill(skill="team-iterdev", args="--role=developer") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Tester
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "tester",
  prompt: `你是 team "${teamName}" 的 TESTER。
当你收到 VERIFY-* 任务时，调用 Skill(skill="team-iterdev", args="--role=tester") 执行。
当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 VERIFY-* 前缀的任务
- 所有输出必须带 [tester] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 VERIFY-* 任务
2. Skill(skill="team-iterdev", args="--role=tester") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Reviewer
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "reviewer",
  prompt: `你是 team "${teamName}" 的 REVIEWER。
当你收到 REVIEW-* 任务时，调用 Skill(skill="team-iterdev", args="--role=reviewer") 执行。
当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 REVIEW-* 前缀的任务
- 所有输出必须带 [reviewer] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 REVIEW-* 任务
2. Skill(skill="team-iterdev", args="--role=reviewer") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Error with usage hint |
| Role file not found | Error with expected path |
| GC loop exceeds 3 rounds | Accept with warning, record in shared memory |
| Sprint velocity drops below 50% | Coordinator alerts user, suggests scope reduction |
| Task ledger corrupted | Rebuild from TaskList state |
