---
name: team-frontend
description: Unified team skill for frontend development team. All roles invoke this skill with --role arg. Built-in ui-ux-pro-max design intelligence. Triggers on "team frontend".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), TodoWrite(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), WebFetch(*), WebSearch(*)
---

# Team Frontend Development

全栈前端开发团队，内置 ui-ux-pro-max 设计智能。具备需求分析、设计系统生成、前端实现、质量保证的完整能力。All team members invoke this skill with `--role=xxx` to route to role-specific execution.

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│  Skill(skill="team-frontend", args="--role=xxx")  │
└───────────────────┬──────────────────────────────┘
                    │ Role Router
    ┌───────┬───────┼───────┬───────┐
    ↓       ↓       ↓       ↓       ↓
┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│coordinator││ analyst  ││ architect││ developer││    qa    │
│ roles/   ││ roles/   ││ roles/   ││ roles/   ││ roles/   │
└──────────┘└──────────┘└──────────┘└──────────┘└──────────┘
```

## Command Architecture

Each role is organized as a folder with a `role.md` orchestrator and optional `commands/` for delegation:

```
roles/
├── coordinator/
│   ├── role.md
│   └── commands/
├── analyst/
│   ├── role.md
│   └── commands/
│       └── design-intelligence.md
├── architect/
│   ├── role.md
│   └── commands/
├── developer/
│   ├── role.md
│   └── commands/
└── qa/
    ├── role.md
    └── commands/
        └── pre-delivery-checklist.md
```

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, analyst, architect, developer, qa")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "frontend"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator": { file: "roles/coordinator/role.md", prefix: null },
  "analyst":     { file: "roles/analyst/role.md",     prefix: "ANALYZE" },
  "architect":   { file: "roles/architect/role.md",   prefix: "ARCH" },
  "developer":   { file: "roles/developer/role.md",   prefix: "DEV" },
  "qa":          { file: "roles/qa/role.md",          prefix: "QA" }
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
| `coordinator` | N/A | 需求澄清、行业识别、流水线编排、进度监控、GC循环控制 | [roles/coordinator/role.md](roles/coordinator/role.md) |
| `analyst` | ANALYZE-* | 需求分析、调用 ui-ux-pro-max 获取设计智能、行业推理规则匹配 | [roles/analyst/role.md](roles/analyst/role.md) |
| `architect` | ARCH-* | 消费设计智能、定义设计令牌系统、组件架构、技术选型 | [roles/architect/role.md](roles/architect/role.md) |
| `developer` | DEV-* | 消费架构产出、实现前端组件/页面代码 | [roles/developer/role.md](roles/developer/role.md) |
| `qa` | QA-* | 代码审查、可访问性检查、行业反模式检查、Pre-Delivery验证 | [roles/qa/role.md](roles/qa/role.md) |

## Shared Infrastructure

### Role Isolation Rules

**核心原则**: 每个角色仅能执行自己职责范围内的工作。

#### Output Tagging（强制）

所有角色的输出必须带 `[role_name]` 标识前缀：

```javascript
SendMessage({
  content: `## [${role}] ...`,
  summary: `[${role}] ...`
})

mcp__ccw-tools__team_msg({
  summary: `[${role}] ...`
})
```

#### Coordinator 隔离

| 允许 | 禁止 |
|------|------|
| 需求澄清 (AskUserQuestion) | ❌ 直接编写/修改代码 |
| 创建任务链 (TaskCreate) | ❌ 调用实现类 subagent |
| 分发任务给 worker | ❌ 直接执行分析/测试/审查 |
| 监控进度 (消息总线) | ❌ 绕过 worker 自行完成任务 |
| 汇报结果给用户 | ❌ 修改源代码或产物文件 |

#### Worker 隔离

| 允许 | 禁止 |
|------|------|
| 处理自己前缀的任务 | ❌ 处理其他角色前缀的任务 |
| SendMessage 给 coordinator | ❌ 直接与其他 worker 通信 |
| 使用 Toolbox 中声明的工具 | ❌ 为其他角色创建任务 (TaskCreate) |

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
| coordinator | `task_unblocked`, `sync_checkpoint`, `fix_required`, `error`, `shutdown` |
| analyst | `analyze_ready`, `analyze_progress`, `error` |
| architect | `arch_ready`, `arch_revision`, `arch_progress`, `error` |
| developer | `dev_complete`, `dev_progress`, `error` |
| qa | `qa_passed`, `qa_result`, `fix_required`, `error` |

### CLI Fallback

当 `mcp__ccw-tools__team_msg` MCP 不可用时：

```javascript
Bash(`ccw team log --team "${teamName}" --from "${role}" --to "coordinator" --type "<type>" --summary "<summary>" --json`)
```

### Task Lifecycle (All Worker Roles)

```javascript
// Standard task lifecycle every worker role follows
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

// Phase 2-4: Role-specific (see roles/{role}/role.md)

// Phase 5: Report + Loop — 所有输出必须带 [role] 标识
mcp__ccw-tools__team_msg({ operation: "log", team: teamName, from: role, to: "coordinator", type: "...", summary: `[${role}] ...` })
SendMessage({ type: "message", recipient: "coordinator", content: `## [${role}] ...`, summary: `[${role}] ...` })
TaskUpdate({ taskId: task.id, status: 'completed' })
// Check for next task → back to Phase 1
```

## Pipeline Architecture

### Three Pipeline Modes

```
page (单页面 - CP-1 线性):
  ANALYZE-001 → ARCH-001 → DEV-001 → QA-001

feature (多组件特性 - CP-1 + CP-2 + CP-8):
  ANALYZE-001 → ARCH-001(tokens+structure) → QA-001(architecture-review)
  → DEV-001(components) → QA-002(code-review)

system (完整前端系统 - CP-1 + CP-2 + CP-8 + CP-9 双轨):
  ANALYZE-001 → ARCH-001(tokens) → QA-001(token-review)
  → [ARCH-002(components) ∥ DEV-001(tokens)](并行, blockedBy QA-001)
  → QA-002(component-review) → DEV-002(components) → QA-003(final)
```

### Generator-Critic Loop (CP-2)

developer ↔ qa 循环，确保代码质量和设计合规：

```
┌──────────┐     DEV artifact        ┌──────────┐
│ developer│ ──────────────────────→  │    qa    │
│(Generator)│                         │ (Critic) │
│          │  ←────────────────────── │          │
└──────────┘   QA feedback            └──────────┘
                (max 2 rounds)

Convergence: qa.score >= 8 && qa.critical_count === 0
```

### Consulting Pattern (CP-8)

developer 可向 analyst 咨询设计决策：

```
developer → coordinator: "需要设计决策咨询"
coordinator → analyst: 创建 ANALYZE-consult 任务
analyst → coordinator: 设计建议
coordinator → developer: 转发建议
```

### Shared Memory

```json
{
  "design_intelligence": {},
  "design_token_registry": {
    "colors": {}, "typography": {}, "spacing": {}, "shadows": {}
  },
  "component_inventory": [],
  "style_decisions": [],
  "qa_history": [],
  "industry_context": {}
}
```

每个角色在 Phase 2 读取，Phase 5 写入自己负责的字段。

## Session Directory

```
.workflow/.team/FE-{slug}-{YYYY-MM-DD}/
├── team-session.json           # Session state
├── shared-memory.json          # Cross-role accumulated knowledge
├── analysis/                   # Analyst output
│   ├── design-intelligence.json
│   └── requirements.md
├── architecture/               # Architect output
│   ├── design-tokens.json
│   ├── component-specs/
│   │   └── {component-name}.md
│   └── project-structure.md
├── qa/                         # QA output
│   └── audit-{NNN}.md
└── build/                      # Developer output
    ├── token-files/
    └── component-files/
```

## ui-ux-pro-max Integration

### Design Intelligence Engine

analyst 角色通过 Skill 调用 ui-ux-pro-max 获取行业设计智能：

```javascript
// 生成完整设计系统推荐
Skill(skill="ui-ux-pro-max", args="${industry} ${keywords} --design-system")

// 领域搜索（UX 指南、排版、色彩等）
Skill(skill="ui-ux-pro-max", args="${query} --domain ${domain}")

// 技术栈指南
Skill(skill="ui-ux-pro-max", args="${query} --stack ${stack}")

// 持久化设计系统（跨会话复用）
Skill(skill="ui-ux-pro-max", args="${query} --design-system --persist -p ${projectName}")
```

### Installation

```
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

### Fallback Strategy

若 ui-ux-pro-max skill 未安装，降级为 LLM 通用设计知识。

### Supported Domains & Stacks

- **Domains**: product, style, typography, color, landing, chart, ux, web
- **Stacks**: html-tailwind, react, nextjs, vue, svelte, shadcn, swiftui, react-native, flutter

## Coordinator Spawn Template

When coordinator creates teammates:

```javascript
TeamCreate({ team_name: teamName })

// Analyst
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "analyst",
  prompt: `你是 team "${teamName}" 的 ANALYST。
当你收到 ANALYZE-* 任务时，调用 Skill(skill="team-frontend", args="--role=analyst") 执行。
当前需求: ${taskDescription}
约束: ${constraints}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 ANALYZE-* 前缀的任务
- 所有输出必须带 [analyst] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 ANALYZE-* 任务
2. Skill(skill="team-frontend", args="--role=analyst") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Architect
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "architect",
  prompt: `你是 team "${teamName}" 的 ARCHITECT。
当你收到 ARCH-* 任务时，调用 Skill(skill="team-frontend", args="--role=architect") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 ARCH-* 前缀的任务
- 所有输出必须带 [architect] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 ARCH-* 任务
2. Skill(skill="team-frontend", args="--role=architect") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Developer
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "developer",
  prompt: `你是 team "${teamName}" 的 DEVELOPER。
当你收到 DEV-* 任务时，调用 Skill(skill="team-frontend", args="--role=developer") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 DEV-* 前缀的任务
- 所有输出必须带 [developer] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 DEV-* 任务
2. Skill(skill="team-frontend", args="--role=developer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// QA
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "qa",
  prompt: `你是 team "${teamName}" 的 QA (质量保证)。
当你收到 QA-* 任务时，调用 Skill(skill="team-frontend", args="--role=qa") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 QA-* 前缀的任务
- 所有输出必须带 [qa] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 QA-* 任务
2. Skill(skill="team-frontend", args="--role=qa") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Error with usage hint |
| Role file not found | Error with expected path (roles/{name}/role.md) |
| QA score < 6 超过 2 轮 GC | Coordinator 上报用户 |
| 双轨同步失败 | 回退到单轨顺序执行 |
| ui-ux-pro-max skill 未安装 | 降级为 LLM 通用设计知识，提示安装命令 |
| DEV 找不到设计文件 | 等待 Sync Point 或上报 |
