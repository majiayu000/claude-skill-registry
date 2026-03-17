---
name: team-lifecycle-v2
description: Unified team skill for full lifecycle - spec/impl/test. All roles invoke this skill with --role arg for role-specific execution. Triggers on "team lifecycle".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), TodoWrite(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Lifecycle

Unified team skill covering specification, implementation, testing, and review. All team members invoke this skill with `--role=xxx` to route to role-specific execution.

## Architecture Overview

```
┌───────────────────────────────────────────────────┐
│  Skill(skill="team-lifecycle-v2")                      │
│  args="任务描述" 或 args="--role=xxx"               │
└───────────────────┬───────────────────────────────┘
                    │ Role Router
                    │
         ┌──── --role present? ────┐
         │ NO                      │ YES
         ↓                         ↓
  Orchestration Mode         Role Dispatch
  (auto → coordinator)      (route to role.md)
         │
    ┌────┴────┬───────┬───────┬───────┬───────┬───────┬───────┐
    ↓         ↓       ↓       ↓       ↓       ↓       ↓       ↓
┌──────────┐┌───────┐┌──────┐┌──────────┐┌───────┐┌────────┐┌──────┐┌────────┐
│coordinator││analyst││writer││discussant││planner││executor││tester││reviewer│
│ roles/   ││roles/ ││roles/││ roles/   ││roles/ ││ roles/ ││roles/││ roles/ │
└──────────┘└───────┘└──────┘└──────────┘└───────┘└────────┘└──────┘└────────┘
                                                       ↑           ↑
                                              on-demand by coordinator
                                            ┌──────────┐ ┌─────────┐
                                            │ explorer │ │architect│
                                            │ (service)│ │(consult)│
                                            └──────────┘ └─────────┘
```

## Command Architecture

Each role is organized as a folder with a `role.md` orchestrator and optional `commands/` for delegation:

```
roles/
├── coordinator/
│   ├── role.md              # Orchestrator (Phase 1/5 inline, Phase 2-4 delegate)
│   └── commands/
│       ├── dispatch.md      # Task chain creation (3 modes)
│       └── monitor.md       # Coordination loop + message routing
├── analyst/
│   ├── role.md
│   └── commands/
├── writer/
│   ├── role.md
│   └── commands/
│       └── generate-doc.md  # Multi-CLI document generation (4 doc types)
├── discussant/
│   ├── role.md
│   └── commands/
│       └── critique.md      # Multi-perspective CLI critique
├── planner/
│   ├── role.md
│   └── commands/
│       └── explore.md       # Multi-angle codebase exploration
├── executor/
│   ├── role.md
│   └── commands/
│       └── implement.md     # Multi-backend code implementation
├── tester/
│   ├── role.md
│   └── commands/
│       └── validate.md      # Test-fix cycle
├── reviewer/
│   ├── role.md
│   └── commands/
│       ├── code-review.md   # 4-dimension code review
│       └── spec-quality.md  # 5-dimension spec quality check
├── explorer/                # Service role (on-demand)
│   └── role.md              # Multi-strategy code search & pattern discovery
└── architect/               # Consulting role (on-demand)
    ├── role.md              # Multi-mode architecture assessment
    └── commands/
        └── assess.md        # Mode-specific assessment strategies
├── fe-developer/            # Frontend pipeline role
│   └── role.md              # Frontend component/page implementation
└── fe-qa/                   # Frontend pipeline role
    ├── role.md
    └── commands/
        └── pre-delivery-checklist.md
    └── role.md              # 5-dimension frontend QA + GC loop
```

**Design principle**: role.md keeps Phase 1 (Task Discovery) and Phase 5 (Report) inline. Phases 2-4 either stay inline (simple logic) or delegate to `commands/*.md` via `Read("commands/xxx.md")` when they involve subagent delegation, CLI fan-out, or complex strategies.

**Command files** are self-contained: each includes Strategy, Execution Steps, and Error Handling. Any subagent can `Read()` a command file and execute it independently.

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "lifecycle"

if (!roleMatch) {
  // No --role: Orchestration Mode → auto route to coordinator
  // See "Orchestration Mode" section below
}

const role = roleMatch ? roleMatch[1] : "coordinator"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator": { file: "roles/coordinator/role.md", prefix: null },
  "analyst":     { file: "roles/analyst/role.md",     prefix: "RESEARCH" },
  "writer":      { file: "roles/writer/role.md",      prefix: "DRAFT" },
  "discussant":  { file: "roles/discussant/role.md",  prefix: "DISCUSS" },
  "planner":     { file: "roles/planner/role.md",     prefix: "PLAN" },
  "executor":    { file: "roles/executor/role.md",    prefix: "IMPL" },
  "tester":      { file: "roles/tester/role.md",      prefix: "TEST" },
  "reviewer":    { file: "roles/reviewer/role.md",    prefix: ["REVIEW", "QUALITY"] },
  "explorer":    { file: "roles/explorer/role.md",    prefix: "EXPLORE", type: "service" },
  "architect":   { file: "roles/architect/role.md",   prefix: "ARCH",    type: "consulting" },
  "fe-developer":{ file: "roles/fe-developer/role.md",prefix: "DEV-FE",  type: "frontend-pipeline" },
  "fe-qa":       { file: "roles/fe-qa/role.md",       prefix: "QA-FE",   type: "frontend-pipeline" }
}

if (!VALID_ROLES[role]) {
  throw new Error(`Unknown role: ${role}. Available: ${Object.keys(VALID_ROLES).join(', ')}`)
}

// Read and execute role-specific logic
Read(VALID_ROLES[role].file)
// → Execute the 5-phase process defined in that file
```

### Orchestration Mode（无参数触发）

当不带 `--role` 调用时，自动进入 coordinator 编排模式。用户只需传任务描述即可触发完整流程。

**触发方式**:

```javascript
// 用户调用（无 --role）— 自动路由到 coordinator
Skill(skill="team-lifecycle-v2", args="任务描述")

// 等价于
Skill(skill="team-lifecycle-v2", args="--role=coordinator 任务描述")
```

**流程**:

```javascript
if (!roleMatch) {
  // Orchestration Mode: 自动路由到 coordinator
  // coordinator role.md 将执行：
  //   Phase 1: 需求澄清
  //   Phase 2: TeamCreate + spawn 所有 worker agents
  //             每个 agent prompt 中包含 Skill(args="--role=xxx") 回调
  //   Phase 3: 创建任务链
  //   Phase 4: 监控协调循环
  //   Phase 5: 结果汇报

  const role = "coordinator"
  Read(VALID_ROLES[role].file)
}
```

**完整调用链**:

```
用户: Skill(args="任务描述")
  │
  ├─ SKILL.md: 无 --role → Orchestration Mode → 读取 coordinator role.md
  │
  ├─ coordinator Phase 2: TeamCreate + spawn workers
  │   每个 worker prompt 中包含 Skill(args="--role=xxx") 回调
  │
  ├─ coordinator Phase 3: dispatch 任务链
  │
  ├─ worker 收到任务 → Skill(args="--role=xxx") → SKILL.md Role Router → role.md
  │   每个 worker 自动获取:
  │   ├─ 角色定义 (role.md: identity, boundaries, message types)
  │   ├─ 可用命令 (commands/*.md)
  │   └─ 执行逻辑 (5-phase process)
  │
  └─ coordinator Phase 4-5: 监控 → 结果汇报
```

### Available Roles

| Role | Task Prefix | Responsibility | Role File |
|------|-------------|----------------|-----------|
| `coordinator` | N/A | Pipeline orchestration, requirement clarification, task dispatch | [roles/coordinator/role.md](roles/coordinator/role.md) |
| `analyst` | RESEARCH-* | Seed analysis, codebase exploration, context gathering | [roles/analyst/role.md](roles/analyst/role.md) |
| `writer` | DRAFT-* | Product Brief / PRD / Architecture / Epics generation | [roles/writer/role.md](roles/writer/role.md) |
| `discussant` | DISCUSS-* | Multi-perspective critique, consensus building | [roles/discussant/role.md](roles/discussant/role.md) |
| `planner` | PLAN-* | Multi-angle exploration, structured planning | [roles/planner/role.md](roles/planner/role.md) |
| `executor` | IMPL-* | Code implementation following plans | [roles/executor/role.md](roles/executor/role.md) |
| `tester` | TEST-* | Adaptive test-fix cycles, quality gates | [roles/tester/role.md](roles/tester/role.md) |
| `reviewer` | `REVIEW-*` + `QUALITY-*` | Code review + Spec quality validation (auto-switch by prefix) | [roles/reviewer/role.md](roles/reviewer/role.md) |
| `explorer` | EXPLORE-* | Code search, pattern discovery, dependency tracing (service role, on-demand) | [roles/explorer/role.md](roles/explorer/role.md) |
| `architect` | ARCH-* | Architecture assessment, tech feasibility, design review (consulting role, on-demand) | [roles/architect/role.md](roles/architect/role.md) |
| `fe-developer` | DEV-FE-* | Frontend component/page implementation, design token consumption (frontend pipeline) | [roles/fe-developer/role.md](roles/fe-developer/role.md) |
| `fe-qa` | QA-FE-* | 5-dimension frontend QA, accessibility, design compliance, GC loop (frontend pipeline) | [roles/fe-qa/role.md](roles/fe-qa/role.md) |

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
| 创建任务链 (TaskCreate) | ❌ 调用实现类 subagent (code-developer 等) |
| 分发任务给 worker | ❌ 直接执行分析/测试/审查 |
| 监控进度 (消息总线) | ❌ 绕过 worker 自行完成任务 |
| 汇报结果给用户 | ❌ 修改源代码或产物文件 |

#### Worker 隔离

| 允许 | 禁止 |
|------|------|
| 处理自己前缀的任务 | ❌ 处理其他角色前缀的任务 |
| SendMessage 给 coordinator | ❌ 直接与其他 worker 通信 |
| 使用 Toolbox 中声明的工具 | ❌ 为其他角色创建任务 (TaskCreate) |
| 委派给 commands/ 中的命令 | ❌ 修改不属于本职责的资源 |

### Message Bus (All Roles)

Every SendMessage **before**, must call `mcp__ccw-tools__team_msg` to log:

```javascript
mcp__ccw-tools__team_msg({
  operation: "log",
  team: teamName,
  from: role,
  to: "coordinator",
  type: "<type>",
  summary: `[${role}] <summary>`,
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
| explorer | `explore_ready`, `explore_progress`, `task_failed` |
| architect | `arch_ready`, `arch_concern`, `arch_progress`, `error` |
| fe-developer | `dev_fe_complete`, `dev_fe_progress`, `error` |
| fe-qa | `qa_fe_passed`, `qa_fe_result`, `fix_required`, `error` |

### CLI Fallback

When `mcp__ccw-tools__team_msg` MCP is unavailable:

```javascript
Bash(`ccw team log --team "${teamName}" --from "${role}" --to "coordinator" --type "<type>" --summary "[${role}] <summary>" --json`)
Bash(`ccw team list --team "${teamName}" --last 10 --json`)
Bash(`ccw team status --team "${teamName}" --json`)
```

### Wisdom Accumulation (All Roles)

跨任务知识积累机制。Coordinator 在 session 初始化时创建 `wisdom/` 目录，所有 worker 在执行过程中读取和贡献 wisdom。

**目录结构**:
```
{sessionFolder}/wisdom/
├── learnings.md      # 发现的模式和洞察
├── decisions.md      # 架构和设计决策
├── conventions.md    # 代码库约定
└── issues.md         # 已知风险和问题
```

**Phase 2 加载（所有 worker）**:
```javascript
// Load wisdom context at start of Phase 2
const sessionFolder = task.description.match(/Session:\s*([^\n]+)/)?.[1]?.trim()
let wisdom = {}
if (sessionFolder) {
  try { wisdom.learnings = Read(`${sessionFolder}/wisdom/learnings.md`) } catch {}
  try { wisdom.decisions = Read(`${sessionFolder}/wisdom/decisions.md`) } catch {}
  try { wisdom.conventions = Read(`${sessionFolder}/wisdom/conventions.md`) } catch {}
  try { wisdom.issues = Read(`${sessionFolder}/wisdom/issues.md`) } catch {}
}
```

**Phase 4/5 贡献（任务完成时）**:
```javascript
// Contribute wisdom after task completion
if (sessionFolder) {
  const timestamp = new Date().toISOString().substring(0, 10)

  // Role-specific contributions:
  // analyst   → learnings (exploration dimensions, codebase patterns)
  // writer    → conventions (document structure, naming patterns)
  // planner   → decisions (task decomposition rationale)
  // executor  → learnings (implementation patterns), issues (bugs encountered)
  // tester    → issues (test failures, edge cases), learnings (test patterns)
  // reviewer  → conventions (code quality patterns), issues (review findings)
  // explorer  → conventions (codebase patterns), learnings (dependency insights)
  // architect → decisions (architecture choices), issues (architectural risks)

  try {
    const targetFile = `${sessionFolder}/wisdom/${wisdomTarget}.md`
    const existing = Read(targetFile)
    const entry = `- [${timestamp}] [${role}] ${wisdomEntry}`
    Write(targetFile, existing + '\n' + entry)
  } catch {} // wisdom not initialized
}
```

**Coordinator 注入**: Coordinator 在 spawn worker 时通过 task description 传递 `Session: {sessionFolder}`，worker 据此定位 wisdom 目录。已有 wisdom 内容为后续 worker 提供上下文，实现跨任务知识传递。

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

// Phase 2-4: Role-specific (see roles/{role}/role.md)

// Phase 5: Report + Loop — 所有输出必须带 [role] 标识
mcp__ccw-tools__team_msg({ operation: "log", team: teamName, from: role, to: "coordinator", type: "...", summary: `[${role}] ...` })
SendMessage({ type: "message", recipient: "coordinator", content: `## [${role}] ...`, summary: `[${role}] ...` })
TaskUpdate({ taskId: task.id, status: 'completed' })
// Check for next task → back to Phase 1
```

## Three-Mode Pipeline

```
Spec-only:
  RESEARCH-001 → DISCUSS-001 → DRAFT-001 → DISCUSS-002
  → DRAFT-002 → DISCUSS-003 → DRAFT-003 → DISCUSS-004
  → DRAFT-004 → DISCUSS-005 → QUALITY-001 → DISCUSS-006

Impl-only (backend):
  PLAN-001 → IMPL-001 → TEST-001 + REVIEW-001

Full-lifecycle (backend):
  [Spec pipeline] → PLAN-001(blockedBy: DISCUSS-006) → IMPL-001 → TEST-001 + REVIEW-001
```

### Frontend Pipelines

Coordinator 根据任务关键词自动检测前端任务并路由到前端子流水线：

```
FE-only (纯前端):
  PLAN-001 → DEV-FE-001 → QA-FE-001
  (GC loop: if QA-FE verdict=NEEDS_FIX → DEV-FE-002 → QA-FE-002, max 2 rounds)

Fullstack (前后端并行):
  PLAN-001 → IMPL-001 ∥ DEV-FE-001 → TEST-001 ∥ QA-FE-001 → REVIEW-001

Full-lifecycle + FE:
  [Spec pipeline] → PLAN-001(blockedBy: DISCUSS-006)
  → IMPL-001 ∥ DEV-FE-001 → TEST-001 ∥ QA-FE-001 → REVIEW-001
```

### Frontend Detection

Coordinator 在 Phase 1 根据任务关键词 + 项目文件自动检测前端任务并选择流水线模式（fe-only / fullstack / impl-only）。检测逻辑见 [roles/coordinator/role.md](roles/coordinator/role.md)。

### Generator-Critic Loop (fe-developer ↔ fe-qa)

```
┌──────────────┐   DEV-FE artifact    ┌──────────┐
│ fe-developer │ ──────────────────→   │  fe-qa   │
│ (Generator)  │                       │ (Critic) │
│              │  ←────────────────── │          │
└──────────────┘   QA-FE feedback      └──────────┘
                   (max 2 rounds)

Convergence: fe-qa.score >= 8 && fe-qa.critical_count === 0
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
├── plan/                       # Plan artifacts (planner output)
│   ├── exploration-{angle}.json
│   ├── explorations-manifest.json
│   ├── plan.json
│   └── .task/
│       └── TASK-*.json
├── explorations/               # Explorer output (cached for cross-role reuse)
│   └── explore-*.json
├── architecture/               # Architect output (assessment reports)
│   └── arch-*.json
└── wisdom/                     # Cross-task accumulated knowledge
    ├── learnings.md            # Patterns and insights discovered
    ├── decisions.md            # Architectural decisions made
    ├── conventions.md          # Codebase conventions found
    └── issues.md               # Known issues and risks
├── qa/                         # QA output (fe-qa audit reports)
│   └── audit-fe-*.json
└── build/                      # Frontend build output (fe-developer)
    ├── token-files/
    └── component-files/
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

When coordinator creates teammates, use this pattern:

```javascript
TeamCreate({ team_name: teamName })

// For each worker role:
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "<role_name>",
  prompt: `你是 team "${teamName}" 的 <ROLE_NAME_UPPER>.

## ⚠️ 首要指令（MUST）
你的所有工作必须通过调用 Skill 获取角色定义后执行，禁止自行发挥：
Skill(skill="team-lifecycle-v2", args="--role=<role_name>")
此调用会加载你的角色定义（role.md）、可用命令（commands/*.md）和完整执行逻辑。

当前需求: ${taskDescription}
约束: ${constraints}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 <PREFIX>-* 前缀的任务，不得执行其他角色的工作
- 所有输出（SendMessage、team_msg）必须带 [<role_name>] 标识前缀
- 仅与 coordinator 通信，不得直接联系其他 worker
- 不得使用 TaskCreate 为其他角色创建任务

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

## 工作流程（严格按顺序）
1. 调用 Skill(skill="team-lifecycle-v2", args="--role=<role_name>") 获取角色定义和执行逻辑
2. 按 role.md 中的 5-Phase 流程执行（TaskList → 找到 <PREFIX>-* 任务 → 执行 → 汇报）
3. team_msg log + SendMessage 结果给 coordinator（带 [<role_name>] 标识）
4. TaskUpdate completed → 检查下一个任务 → 回到步骤 1`
})
```

See [roles/coordinator/role.md](roles/coordinator/role.md) for the full spawn implementation with per-role prompts.

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
> 从 `roles/` 子目录引用时路径为 `../../specs/` 和 `../../templates/`。

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Orchestration Mode → auto route to coordinator |
| Role file not found | Error with expected path (roles/{name}/role.md) |
| Command file not found | Fall back to inline execution in role.md |
| Task prefix conflict | Log warning, proceed |
