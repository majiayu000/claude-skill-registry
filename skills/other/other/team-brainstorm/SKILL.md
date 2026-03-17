---
name: team-brainstorm
description: Unified team skill for brainstorming team. All roles invoke this skill with --role arg for role-specific execution. Triggers on "team brainstorm".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Brainstorm

头脑风暴团队技能。通过 Generator-Critic 循环、共享记忆和动态管道选择，实现多角度创意发散、挑战验证和收敛筛选。所有团队成员通过 `--role=xxx` 路由到角色执行逻辑。

## Architecture Overview

```
┌───────────────────────────────────────────────────┐
│  Skill(skill="team-brainstorm", args="--role=xxx") │
└───────────────────┬───────────────────────────────┘
                    │ Role Router
    ┌───────────┬───┼───────────┬───────────┐
    ↓           ↓   ↓           ↓           ↓
┌──────────┐┌───────┐┌──────────┐┌──────────┐┌─────────┐
│coordinator││ideator││challenger││synthesizer││evaluator│
│ roles/   ││roles/ ││ roles/   ││ roles/   ││ roles/  │
└──────────┘└───────┘└──────────┘└──────────┘└─────────┘
```

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, ideator, challenger, synthesizer, evaluator")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "brainstorm"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator":  { file: "roles/coordinator.md",  prefix: null },
  "ideator":      { file: "roles/ideator.md",      prefix: "IDEA" },
  "challenger":   { file: "roles/challenger.md",    prefix: "CHALLENGE" },
  "synthesizer":  { file: "roles/synthesizer.md",   prefix: "SYNTH" },
  "evaluator":    { file: "roles/evaluator.md",     prefix: "EVAL" }
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
| `coordinator` | N/A | 话题澄清、复杂度评估、管道选择、收敛监控 | [roles/coordinator.md](roles/coordinator.md) |
| `ideator` | IDEA-* | 多角度创意生成、概念探索、发散思维 | [roles/ideator.md](roles/ideator.md) |
| `challenger` | CHALLENGE-* | 魔鬼代言人、假设挑战、可行性质疑 | [roles/challenger.md](roles/challenger.md) |
| `synthesizer` | SYNTH-* | 跨想法整合、主题提取、冲突解决 | [roles/synthesizer.md](roles/synthesizer.md) |
| `evaluator` | EVAL-* | 评分排序、优先级推荐、最终筛选 | [roles/evaluator.md](roles/evaluator.md) |

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
| 需求澄清 (AskUserQuestion) | ❌ 直接生成创意 |
| 创建任务链 (TaskCreate) | ❌ 直接评估/挑战想法 |
| 分发任务给 worker | ❌ 直接执行分析/综合 |
| 监控进度 (消息总线) | ❌ 绕过 worker 自行完成任务 |
| 汇报结果给用户 | ❌ 修改源代码或产物文件 |

#### Worker 隔离

| 允许 | 禁止 |
|------|------|
| 处理自己前缀的任务 | ❌ 处理其他角色前缀的任务 |
| SendMessage 给 coordinator | ❌ 直接与其他 worker 通信 |
| 读取 shared-memory.json | ❌ 为其他角色创建任务 (TaskCreate) |
| 写入 shared-memory.json (自己的字段) | ❌ 修改不属于本职责的资源 |

### Team Configuration

```javascript
const TEAM_CONFIG = {
  name: "brainstorm",
  sessionDir: ".workflow/.team/BRS-{slug}-{date}/",
  msgDir: ".workflow/.team-msg/brainstorm/",
  sharedMemory: "shared-memory.json"
}
```

### Shared Memory (创新模式)

所有角色在 Phase 2 读取、Phase 5 写入 `shared-memory.json`：

```javascript
// Phase 2: 读取共享记忆
const memoryPath = `${sessionFolder}/shared-memory.json`
let sharedMemory = {}
try { sharedMemory = JSON.parse(Read(memoryPath)) } catch {}

// Phase 5: 写入共享记忆（仅更新自己负责的字段）
// ideator   → sharedMemory.generated_ideas
// challenger → sharedMemory.critique_insights
// synthesizer → sharedMemory.synthesis_themes
// evaluator → sharedMemory.evaluation_scores
Write(memoryPath, JSON.stringify(sharedMemory, null, 2))
```

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
| coordinator | `pipeline_selected`, `gc_loop_trigger`, `task_unblocked`, `error`, `shutdown` |
| ideator | `ideas_ready`, `ideas_revised`, `error` |
| challenger | `critique_ready`, `error` |
| synthesizer | `synthesis_ready`, `error` |
| evaluator | `evaluation_ready`, `error` |

### CLI Fallback

When `mcp__ccw-tools__team_msg` MCP is unavailable:

```javascript
Bash(`ccw team log --team "${teamName}" --from "${role}" --to "coordinator" --type "<type>" --summary "<summary>" --json`)
```

### Task Lifecycle (All Worker Roles)

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

// Phase 5: Report + Loop — 所有输出必须带 [role] 标识
mcp__ccw-tools__team_msg({ operation: "log", team: teamName, from: role, to: "coordinator", type: "...", summary: `[${role}] ...` })
SendMessage({ type: "message", recipient: "coordinator", content: `## [${role}] ...`, summary: `[${role}] ...` })
TaskUpdate({ taskId: task.id, status: 'completed' })
// Check for next task → back to Phase 1
```

## Three-Pipeline Architecture

```
Quick:
  IDEA-001 → CHALLENGE-001 → SYNTH-001

Deep (Generator-Critic Loop):
  IDEA-001 → CHALLENGE-001 → IDEA-002(fix) → CHALLENGE-002 → SYNTH-001 → EVAL-001

Full (Fan-out + Generator-Critic):
  [IDEA-001 + IDEA-002 + IDEA-003](parallel) → CHALLENGE-001(batch) → IDEA-004(fix) → SYNTH-001 → EVAL-001
```

### Generator-Critic Loop

ideator ↔ challenger 循环，最多2轮：

```
IDEA → CHALLENGE → (if critique.severity >= HIGH) → IDEA-fix → CHALLENGE-2 → SYNTH
                   (if critique.severity < HIGH) → SYNTH
```

## Unified Session Directory

```
.workflow/.team/BRS-{slug}-{YYYY-MM-DD}/
├── team-session.json           # Session state
├── shared-memory.json          # 累积: generated_ideas / critique_insights / synthesis_themes / evaluation_scores
├── ideas/                      # Ideator output
│   ├── idea-001.md
│   ├── idea-002.md
│   └── idea-003.md
├── critiques/                  # Challenger output
│   ├── critique-001.md
│   └── critique-002.md
├── synthesis/                  # Synthesizer output
│   └── synthesis-001.md
└── evaluation/                 # Evaluator output
    └── evaluation-001.md
```

## Coordinator Spawn Template

```javascript
TeamCreate({ team_name: teamName })

// Ideator
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "ideator",
  prompt: `你是 team "${teamName}" 的 IDEATOR。
当你收到 IDEA-* 任务时，调用 Skill(skill="team-brainstorm", args="--role=ideator") 执行。
当前话题: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 IDEA-* 前缀的任务，不得执行其他角色的工作
- 所有输出（SendMessage、team_msg）必须带 [ideator] 标识前缀
- 仅与 coordinator 通信，不得直接联系其他 worker
- 不得使用 TaskCreate 为其他角色创建任务

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 IDEA-* 任务
2. Skill(skill="team-brainstorm", args="--role=ideator") 执行
3. team_msg log + SendMessage 结果给 coordinator（带 [ideator] 标识）
4. TaskUpdate completed → 检查下一个任务`
})

// Challenger
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "challenger",
  prompt: `你是 team "${teamName}" 的 CHALLENGER。
当你收到 CHALLENGE-* 任务时，调用 Skill(skill="team-brainstorm", args="--role=challenger") 执行。
当前话题: ${taskDescription}

## 角色准则（强制）
- 你只能处理 CHALLENGE-* 前缀的任务
- 所有输出必须带 [challenger] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 CHALLENGE-* 任务
2. Skill(skill="team-brainstorm", args="--role=challenger") 执行
3. team_msg log + SendMessage 结果给 coordinator（带 [challenger] 标识）
4. TaskUpdate completed → 检查下一个任务`
})

// Synthesizer
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "synthesizer",
  prompt: `你是 team "${teamName}" 的 SYNTHESIZER。
当你收到 SYNTH-* 任务时，调用 Skill(skill="team-brainstorm", args="--role=synthesizer") 执行。
当前话题: ${taskDescription}

## 角色准则（强制）
- 你只能处理 SYNTH-* 前缀的任务
- 所有输出必须带 [synthesizer] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 SYNTH-* 任务
2. Skill(skill="team-brainstorm", args="--role=synthesizer") 执行
3. team_msg log + SendMessage 结果给 coordinator（带 [synthesizer] 标识）
4. TaskUpdate completed → 检查下一个任务`
})

// Evaluator
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "evaluator",
  prompt: `你是 team "${teamName}" 的 EVALUATOR。
当你收到 EVAL-* 任务时，调用 Skill(skill="team-brainstorm", args="--role=evaluator") 执行。
当前话题: ${taskDescription}

## 角色准则（强制）
- 你只能处理 EVAL-* 前缀的任务
- 所有输出必须带 [evaluator] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 EVAL-* 任务
2. Skill(skill="team-brainstorm", args="--role=evaluator") 执行
3. team_msg log + SendMessage 结果给 coordinator（带 [evaluator] 标识）
4. TaskUpdate completed → 检查下一个任务`
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Error with usage hint |
| Role file not found | Error with expected path (roles/{name}.md) |
| Task prefix conflict | Log warning, proceed |
| Generator-Critic loop exceeds 2 rounds | Force convergence → SYNTH |
| No ideas generated | Coordinator prompts with seed questions |
