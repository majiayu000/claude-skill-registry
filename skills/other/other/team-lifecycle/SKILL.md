---
name: team-lifecycle
description: Unified team skill for full lifecycle - spec/impl/test. All roles invoke this skill with --role arg for role-specific execution.
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), TodoWrite(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Lifecycle

Unified team skill covering specification, implementation, testing, and review. All team members invoke this skill with `--role=xxx` to route to role-specific execution.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  Skill(skill="team-lifecycle", args="--role=xxx") │
└───────────────────┬─────────────────────────────┘
                    │ Role Router
    ┌───────┬───────┼───────┬───────┬───────┬───────┬───────┐
    ↓       ↓       ↓       ↓       ↓       ↓       ↓       ↓
┌─────────┐┌───────┐┌──────┐┌──────────┐┌───────┐┌────────┐┌──────┐┌────────┐
│coordinator││analyst││writer││discussant││planner││executor││tester││reviewer│
│ roles/   ││roles/ ││roles/││ roles/   ││roles/ ││ roles/ ││roles/││ roles/ │
└─────────┘└───────┘└──────┘└──────────┘└───────┘└────────┘└──────┘└────────┘
```

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, analyst, writer, discussant, planner, executor, tester, reviewer")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "lifecycle"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator": { file: "roles/coordinator.md", prefix: null },
  "analyst":     { file: "roles/analyst.md",     prefix: "RESEARCH" },
  "writer":      { file: "roles/writer.md",      prefix: "DRAFT" },
  "discussant":  { file: "roles/discussant.md",  prefix: "DISCUSS" },
  "planner":     { file: "roles/planner.md",     prefix: "PLAN" },
  "executor":    { file: "roles/executor.md",    prefix: "IMPL" },
  "tester":      { file: "roles/tester.md",      prefix: "TEST" },
  "reviewer":    { file: "roles/reviewer.md",    prefix: ["REVIEW", "QUALITY"] }
}

if (!VALID_ROLES[role]) {
  throw new Error(`Unknown role: ${role}. Available: ${Object.keys(VALID_ROLES).join(', ')}`)
}

// Read and execute role-specific logic
Read(VALID_ROLES[role].file)
// → Execute the 5-phase process defined in that file
```

### Available Roles

| Role | Task Prefix | Responsibility | Role File |
|------|-------------|----------------|-----------|
| `coordinator` | N/A | Pipeline orchestration, requirement clarification, task dispatch | [roles/coordinator.md](roles/coordinator.md) |
| `analyst` | RESEARCH-* | Seed analysis, codebase exploration, context gathering | [roles/analyst.md](roles/analyst.md) |
| `writer` | DRAFT-* | Product Brief / PRD / Architecture / Epics generation | [roles/writer.md](roles/writer.md) |
| `discussant` | DISCUSS-* | Multi-perspective critique, consensus building | [roles/discussant.md](roles/discussant.md) |
| `planner` | PLAN-* | Multi-angle exploration, structured planning | [roles/planner.md](roles/planner.md) |
| `executor` | IMPL-* | Code implementation following plans | [roles/executor.md](roles/executor.md) |
| `tester` | TEST-* | Adaptive test-fix cycles, quality gates | [roles/tester.md](roles/tester.md) |
| `reviewer` | `REVIEW-*` + `QUALITY-*` | Code review + Spec quality validation (auto-switch by prefix) | [roles/reviewer.md](roles/reviewer.md) |

## Shared Infrastructure

### Message Bus (All Roles)

Every SendMessage **before**, must call `mcp__ccw-tools__team_msg` to log:

```javascript
mcp__ccw-tools__team_msg({
  operation: "log",
  team: teamName,
  from: role,
  to: "coordinator",
  type: "<type>",
  summary: "<summary>",
  ref: "<file_path>"
})
```

**Message types by role**:

| Role | Types |
|------|-------|
| coordinator | `plan_approved`, `plan_revision`, `task_unblocked`, `fix_required`, `error`, `shutdown` |
| analyst | `research_ready`, `research_progress`, `error` |
| writer | `draft_ready`, `draft_revision`, `impl_progress`, `error` |
| discussant | `discussion_ready`, `discussion_blocked`, `impl_progress`, `error` |
| planner | `plan_ready`, `plan_revision`, `impl_progress`, `error` |
| executor | `impl_complete`, `impl_progress`, `error` |
| tester | `test_result`, `impl_progress`, `fix_required`, `error` |
| reviewer | `review_result`, `quality_result`, `fix_required`, `error` |

### CLI Fallback

When `mcp__ccw-tools__team_msg` MCP is unavailable:

```javascript
Bash(`ccw team log --team "${teamName}" --from "${role}" --to "coordinator" --type "<type>" --summary "<summary>" --json`)
Bash(`ccw team list --team "${teamName}" --last 10 --json`)
Bash(`ccw team status --team "${teamName}" --json`)
```

### Task Lifecycle (All Worker Roles)

```javascript
// Standard task lifecycle every worker role follows
// Phase 1: Discovery
const tasks = TaskList()
const prefixes = Array.isArray(VALID_ROLES[role].prefix) ? VALID_ROLES[role].prefix : [VALID_ROLES[role].prefix]
const myTasks = tasks.filter(t =>
  prefixes.some(p => t.subject.startsWith(`${p}-`)) &&
  t.owner === role &&
  t.status === 'pending' &&
  t.blockedBy.length === 0
)
if (myTasks.length === 0) return // idle
const task = TaskGet({ taskId: myTasks[0].id })
TaskUpdate({ taskId: task.id, status: 'in_progress' })

// Phase 1.5: Resume Artifact Check (防止重复产出)
// 当 session 从暂停恢复时，coordinator 已将 in_progress 任务重置为 pending。
// Worker 在开始工作前，必须检查该任务的输出产物是否已存在。
// 如果产物已存在且内容完整：
//   → 直接跳到 Phase 5 报告完成（避免覆盖上次成果）
// 如果产物存在但不完整（如文件为空或缺少关键 section）：
//   → 正常执行 Phase 2-4（基于已有产物继续，而非从头开始）
// 如果产物不存在：
//   → 正常执行 Phase 2-4
//
// 每个 role 检查自己的输出路径:
//   analyst  → sessionFolder/spec/discovery-context.json
//   writer   → sessionFolder/spec/{product-brief.md | requirements/ | architecture/ | epics/}
//   discussant → sessionFolder/discussions/discuss-NNN-*.md
//   planner  → sessionFolder/plan/plan.json
//   executor → git diff (已提交的代码变更)
//   tester   → test pass rate
//   reviewer → sessionFolder/spec/readiness-report.md (quality) 或 review findings (code)

// Phase 2-4: Role-specific (see roles/{role}.md)

// Phase 5: Report + Loop
mcp__ccw-tools__team_msg({ operation: "log", team: teamName, from: role, to: "coordinator", type: "...", summary: "..." })
SendMessage({ type: "message", recipient: "coordinator", content: "...", summary: "..." })
TaskUpdate({ taskId: task.id, status: 'completed' })
// Check for next task → back to Phase 1
```

## Three-Mode Pipeline

```
Spec-only:
  RESEARCH-001 → DISCUSS-001 → DRAFT-001 → DISCUSS-002
  → DRAFT-002 → DISCUSS-003 → DRAFT-003 → DISCUSS-004
  → DRAFT-004 → DISCUSS-005 → QUALITY-001 → DISCUSS-006

Impl-only:
  PLAN-001 → IMPL-001 → TEST-001 + REVIEW-001

Full-lifecycle:
  [Spec pipeline] → PLAN-001(blockedBy: DISCUSS-006) → IMPL-001 → TEST-001 + REVIEW-001
```

## Unified Session Directory

All session artifacts are stored under a single session folder:

```
.workflow/.team/TLS-{slug}-{YYYY-MM-DD}/
├── team-session.json           # Session state (status, progress, completed_tasks)
├── spec/                       # Spec artifacts (analyst, writer, reviewer output)
│   ├── spec-config.json
│   ├── discovery-context.json
│   ├── product-brief.md
│   ├── requirements/           # _index.md + REQ-*.md + NFR-*.md
│   ├── architecture/           # _index.md + ADR-*.md
│   ├── epics/                  # _index.md + EPIC-*.md
│   ├── readiness-report.md
│   └── spec-summary.md
├── discussions/                # Discussion records (discussant output)
│   └── discuss-001..006.md
└── plan/                       # Plan artifacts (planner output)
    ├── exploration-{angle}.json
    ├── explorations-manifest.json
    ├── plan.json
    └── .task/
        └── TASK-*.json
```

Messages remain at `.workflow/.team-msg/{team-name}/` (unchanged).

## Session Resume

Coordinator supports `--resume` / `--continue` flags to resume interrupted sessions:

1. Scans `.workflow/.team/TLS-*/team-session.json` for `status: "active"` or `"paused"`
2. Multiple matches → `AskUserQuestion` for user selection
3. **Audit TaskList** — 获取当前所有任务的真实状态
4. **Reconcile** — 双向同步 session.completed_tasks ↔ TaskList 状态:
   - session 已完成但 TaskList 未标记 → 修正 TaskList 为 completed
   - TaskList 已完成但 session 未记录 → 补录到 session
   - in_progress 状态（暂停中断）→ 重置为 pending
5. Determines remaining pipeline from reconciled state
6. Rebuilds team (`TeamCreate` + worker spawns for needed roles only)
7. Creates missing tasks with correct `blockedBy` dependency chain (uses `TASK_METADATA` lookup)
8. Verifies dependency chain integrity for existing tasks
9. Updates session file with reconciled state + current_phase
10. **Kick** — 向首个可执行任务的 worker 发送 `task_unblocked` 消息，打破 resume 死锁
11. Jumps to Phase 4 coordination loop

## Coordinator Spawn Template

When coordinator creates teammates:

```javascript
TeamCreate({ team_name: teamName })

// Analyst (spec-only / full)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "analyst",
  prompt: `你是 team "${teamName}" 的 ANALYST。
当你收到 RESEARCH-* 任务时，调用 Skill(skill="team-lifecycle", args="--role=analyst") 执行。
当前需求: ${taskDescription}
约束: ${constraints}
Session: ${sessionFolder}

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 RESEARCH-* 任务
2. Skill(skill="team-lifecycle", args="--role=analyst") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Writer (spec-only / full)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "writer",
  prompt: `你是 team "${teamName}" 的 WRITER。
当你收到 DRAFT-* 任务时，调用 Skill(skill="team-lifecycle", args="--role=writer") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 DRAFT-* 任务
2. Skill(skill="team-lifecycle", args="--role=writer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Discussant (spec-only / full)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "discussant",
  prompt: `你是 team "${teamName}" 的 DISCUSSANT。
当你收到 DISCUSS-* 任务时，调用 Skill(skill="team-lifecycle", args="--role=discussant") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}
讨论深度: ${discussionDepth}

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 DISCUSS-* 任务
2. Skill(skill="team-lifecycle", args="--role=discussant") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Planner (impl-only / full)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "planner",
  prompt: `你是 team "${teamName}" 的 PLANNER。
当你收到 PLAN-* 任务时，调用 Skill(skill="team-lifecycle", args="--role=planner") 执行。
当前需求: ${taskDescription}
约束: ${constraints}
Session: ${sessionFolder}

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 PLAN-* 任务
2. Skill(skill="team-lifecycle", args="--role=planner") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Executor (impl-only / full)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "executor",
  prompt: `你是 team "${teamName}" 的 EXECUTOR。
当你收到 IMPL-* 任务时，调用 Skill(skill="team-lifecycle", args="--role=executor") 执行。
当前需求: ${taskDescription}
约束: ${constraints}

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 IMPL-* 任务
2. Skill(skill="team-lifecycle", args="--role=executor") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Tester (impl-only / full)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "tester",
  prompt: `你是 team "${teamName}" 的 TESTER。
当你收到 TEST-* 任务时，调用 Skill(skill="team-lifecycle", args="--role=tester") 执行。
当前需求: ${taskDescription}
约束: ${constraints}

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 TEST-* 任务
2. Skill(skill="team-lifecycle", args="--role=tester") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Reviewer (all modes)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "reviewer",
  prompt: `你是 team "${teamName}" 的 REVIEWER。
当你收到 REVIEW-* 或 QUALITY-* 任务时，调用 Skill(skill="team-lifecycle", args="--role=reviewer") 执行。
- REVIEW-* → 代码审查逻辑
- QUALITY-* → 规格质量检查逻辑
当前需求: ${taskDescription}

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 REVIEW-* 或 QUALITY-* 任务
2. Skill(skill="team-lifecycle", args="--role=reviewer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})
```

## Shared Spec Resources

Writer 和 Reviewer 角色在 spec 模式下使用本 skill 内置的标准和模板（从 spec-generator 复制，独立维护）：

| Resource | Path | Usage |
|----------|------|-------|
| Document Standards | `specs/document-standards.md` | YAML frontmatter、命名规范、内容结构 |
| Quality Gates | `specs/quality-gates.md` | Per-phase 质量门禁、评分标尺 |
| Product Brief Template | `templates/product-brief.md` | DRAFT-001 文档生成 |
| Requirements Template | `templates/requirements-prd.md` | DRAFT-002 文档生成 |
| Architecture Template | `templates/architecture-doc.md` | DRAFT-003 文档生成 |
| Epics Template | `templates/epics-template.md` | DRAFT-004 文档生成 |

> Writer 在执行每个 DRAFT-* 任务前 **必须先 Read** 对应的 template 文件和 document-standards.md。
> 从 `roles/` 子目录引用时路径为 `../specs/` 和 `../templates/`。

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Error with usage hint |
| Role file not found | Error with expected path |
| Task prefix conflict | Log warning, proceed |
