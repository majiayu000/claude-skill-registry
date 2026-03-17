---
name: team-uidesign
description: Unified team skill for UI design team. All roles invoke this skill with --role arg for role-specific execution. CP-9 Dual-Track design+implementation.
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), TodoWrite(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), WebFetch(*), WebSearch(*)
---

# Team UI Design

Unified team skill for UI design covering design system analysis, token definition, component specification, accessibility audit, and code implementation. All team members invoke this skill with `--role=xxx` to route to role-specific execution.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  Skill(skill="team-uidesign", args="--role=xxx") │
└───────────────────┬─────────────────────────────┘
                    │ Role Router
    ┌───────┬───────┼───────┬───────┐
    ↓       ↓       ↓       ↓       ↓
┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│coordinator││researcher││ designer ││ reviewer ││implementer│
│ roles/   ││ roles/   ││ roles/   ││ roles/   ││ roles/    │
└──────────┘└──────────┘└──────────┘└──────────┘└───────────┘
```

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, researcher, designer, reviewer, implementer")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "uidesign"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator":  { file: "roles/coordinator.md",  prefix: null },
  "researcher":   { file: "roles/researcher.md",   prefix: "RESEARCH" },
  "designer":     { file: "roles/designer.md",     prefix: "DESIGN" },
  "reviewer":     { file: "roles/reviewer.md",     prefix: "AUDIT" },
  "implementer":  { file: "roles/implementer.md",  prefix: "BUILD" }
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
| `coordinator` | N/A | Scope assessment, dual-track orchestration, sync point management | [roles/coordinator.md](roles/coordinator.md) |
| `researcher` | RESEARCH-* | Design system analysis, component inventory, accessibility audit | [roles/researcher.md](roles/researcher.md) |
| `designer` | DESIGN-* | Design token definition, component specs, layout design | [roles/designer.md](roles/designer.md) |
| `reviewer` | AUDIT-* | Design consistency, accessibility compliance, visual audit | [roles/reviewer.md](roles/reviewer.md) |
| `implementer` | BUILD-* | Component code implementation, CSS generation, design token consumption | [roles/implementer.md](roles/implementer.md) |

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
| researcher | `research_ready`, `research_progress`, `error` |
| designer | `design_ready`, `design_revision`, `design_progress`, `error` |
| reviewer | `audit_result`, `audit_passed`, `fix_required`, `error` |
| implementer | `build_complete`, `build_progress`, `error` |

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

// Phase 2-4: Role-specific (see roles/{role}.md)

// Phase 5: Report + Loop — 所有输出必须带 [role] 标识
mcp__ccw-tools__team_msg({ operation: "log", team: teamName, from: role, to: "coordinator", type: "...", summary: `[${role}] ...` })
SendMessage({ type: "message", recipient: "coordinator", content: `## [${role}] ...`, summary: `[${role}] ...` })
TaskUpdate({ taskId: task.id, status: 'completed' })
// Check for next task → back to Phase 1
```

## Three-Pipeline Architecture

### CP-9 Dual-Track Concept

```
Track A (Design):     RESEARCH → DESIGN(tokens) → DESIGN(components) → ...
                                      │                    │
                            Sync Point 1          Sync Point 2
                                      │                    │
Track B (Build):              BUILD(tokens) ──→ BUILD(components) → ...
```

Design and implementation proceed in parallel after sync checkpoints. Each sync point validates that design artifacts are stable enough for implementation to consume.

### Pipeline Modes

```
component (单组件):
  RESEARCH-001 → DESIGN-001 → AUDIT-001 → BUILD-001

system (设计系统 - 双轨):
  Track A: RESEARCH-001 → DESIGN-001(tokens) → DESIGN-002(components)
  Sync-1: AUDIT-001 (tokens审查)
  Track B: BUILD-001(tokens, blockedBy AUDIT-001) ∥ DESIGN-002(components)
  Sync-2: AUDIT-002 (components审查)
  Track B: BUILD-002(components, blockedBy AUDIT-002)

full-system (完整设计系统):
  RESEARCH-001 → DESIGN-001(tokens) → AUDIT-001
  → [DESIGN-002(components) + BUILD-001(tokens)](并行, blockedBy AUDIT-001)
  → AUDIT-002 → BUILD-002(components) → AUDIT-003(最终)
```

### Generator-Critic Loop

designer ↔ reviewer 循环，确保设计一致性和可访问性：

```
┌──────────┐     DESIGN artifact     ┌──────────┐
│ designer │ ──────────────────────→  │ reviewer  │
│(Generator)│                         │ (Critic)  │
│          │  ←────────────────────── │           │
└──────────┘   AUDIT feedback         └──────────┘
                (max 2 rounds)

Convergence: audit.score >= 8 && audit.critical_count === 0
```

### Shared Memory

```json
{
  "design_intelligence": {},
  "design_token_registry": {
    "colors": {}, "typography": {}, "spacing": {}, "shadows": {}, "borders": {}
  },
  "style_decisions": [],
  "component_inventory": [],
  "accessibility_patterns": [],
  "audit_history": [],
  "industry_context": { "industry": "", "config": {}, "detected_stack": "" }
}
```

每个角色在 Phase 2 读取，Phase 5 写入自己负责的字段。

### Design Intelligence (ui-ux-pro-max)

Researcher 通过 `Skill(skill="ui-ux-pro-max", args="...")` 获取设计智能，写入 `design-intelligence.json`，下游角色消费：

```
researcher (Stream 4)
  │ Skill("ui-ux-pro-max", args="<industry> <keywords> --design-system")
  │ Skill("ui-ux-pro-max", args="accessibility animation responsive --domain ux")
  │ Skill("ui-ux-pro-max", args="<keywords> --stack <detected-stack>")
  ↓
design-intelligence.json
  ├─→ designer: recommended colors/typography/style → token values, anti-patterns → component specs
  ├─→ reviewer: anti-patterns → Industry Compliance audit dimension (20% weight)
  └─→ implementer: stack guidelines → code generation, anti-patterns → validation
```

**数据流**:
- `design_system.colors/typography/style` → designer 用于令牌默认值（recommended-first 模式）
- `recommendations.anti_patterns[]` → reviewer 审查合规性，designer/implementer 避免违反
- `stack_guidelines` → implementer 代码生成约束
- `ux_guidelines[]` → designer 组件规格中的实现提示

**降级策略**: 当 ui-ux-pro-max 不可用时，使用 LLM 通用知识生成默认值，`_source` 标记为 `"llm-general-knowledge"`。

## Session Directory

```
.workflow/.team/UDS-{slug}-{YYYY-MM-DD}/
├── team-session.json           # Session state
├── shared-memory.json          # Cross-role accumulated knowledge
├── research/                   # Researcher output
│   ├── design-system-analysis.json
│   ├── component-inventory.json
│   ├── accessibility-audit.json
│   ├── design-intelligence.json       # ui-ux-pro-max 设计智能
│   └── design-intelligence-raw.md     # ui-ux-pro-max 原始输出
├── design/                     # Designer output
│   ├── design-tokens.json
│   ├── component-specs/
│   │   └── {component-name}.md
│   └── layout-specs/
│       └── {layout-name}.md
├── audit/                      # Reviewer output
│   └── audit-{NNN}.md
└── build/                      # Implementer output
    ├── token-files/
    └── component-files/
```

## Coordinator Spawn Template

When coordinator creates teammates:

```javascript
TeamCreate({ team_name: teamName })

// Researcher
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "researcher",
  prompt: `你是 team "${teamName}" 的 RESEARCHER。
当你收到 RESEARCH-* 任务时，调用 Skill(skill="team-uidesign", args="--role=researcher") 执行。
当前需求: ${taskDescription}
约束: ${constraints}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 RESEARCH-* 前缀的任务
- 所有输出必须带 [researcher] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 RESEARCH-* 任务
2. Skill(skill="team-uidesign", args="--role=researcher") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Designer
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "designer",
  prompt: `你是 team "${teamName}" 的 DESIGNER。
当你收到 DESIGN-* 任务时，调用 Skill(skill="team-uidesign", args="--role=designer") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 DESIGN-* 前缀的任务
- 所有输出必须带 [designer] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 DESIGN-* 任务
2. Skill(skill="team-uidesign", args="--role=designer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Reviewer (AUDIT)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "reviewer",
  prompt: `你是 team "${teamName}" 的 REVIEWER (审查员)。
当你收到 AUDIT-* 任务时，调用 Skill(skill="team-uidesign", args="--role=reviewer") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 AUDIT-* 前缀的任务
- 所有输出必须带 [reviewer] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 AUDIT-* 任务
2. Skill(skill="team-uidesign", args="--role=reviewer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Implementer (BUILD)
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "implementer",
  prompt: `你是 team "${teamName}" 的 IMPLEMENTER (实现者)。
当你收到 BUILD-* 任务时，调用 Skill(skill="team-uidesign", args="--role=implementer") 执行。
当前需求: ${taskDescription}
Session: ${sessionFolder}

## 角色准则（强制）
- 你只能处理 BUILD-* 前缀的任务
- 所有输出必须带 [implementer] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 BUILD-* 任务
2. Skill(skill="team-uidesign", args="--role=implementer") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Error with usage hint |
| Role file not found | Error with expected path |
| AUDIT score < 6 超过 2 轮 GC | Coordinator 上报用户 |
| 双轨同步失败 | 回退到单轨顺序执行 |
| 设计令牌冲突 | Reviewer 仲裁，Coordinator 介入 |
| BUILD 找不到设计文件 | 等待 Sync Point 或上报 |
| ui-ux-pro-max 不可用 | 降级为 LLM 通用知识，`_source: "llm-general-knowledge"` |
| 行业反模式检查失败 | Reviewer 标记 Industry Compliance 维度为 N/A |
