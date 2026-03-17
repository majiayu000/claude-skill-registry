---
name: team-ultra-analyze
description: Unified team skill for deep collaborative analysis. All roles invoke this skill with --role arg for role-specific execution. Triggers on "team ultra-analyze", "team analyze".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Ultra Analyze

深度协作分析团队技能。将单体分析工作流拆分为 5 角色协作：探索→分析→讨论→综合。支持 Quick/Standard/Deep 三种管道模式，通过讨论循环实现用户引导的渐进式理解深化。所有成员通过 `--role=xxx` 路由到角色执行逻辑。

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Skill(skill="team-ultra-analyze", args="--role=xxx")    │
└──────────────────────┬──────────────────────────────────┘
                       │ Role Router
    ┌──────────┬───────┼───────────┬───────────┐
    ↓          ↓       ↓           ↓           ↓
┌────────┐┌────────┐┌────────┐┌──────────┐┌───────────┐
│coordi- ││explorer││analyst ││discussant││synthesizer│
│nator   ││EXPLORE-││ANALYZE-││DISCUSS-* ││SYNTH-*    │
│ roles/ ││* roles/││* roles/││ roles/   ││ roles/    │
└────────┘└────────┘└────────┘└──────────┘└───────────┘
```

## Command Architecture

```
roles/
├── coordinator/
│   ├── role.md              # 编排：话题澄清、管道选择、讨论循环、结果汇报
│   └── commands/
│       ├── dispatch.md      # 任务链创建与依赖管理
│       └── monitor.md       # 进度监控 + 讨论循环
├── explorer/
│   ├── role.md              # 代码库探索
│   └── commands/
│       └── explore.md       # cli-explore-agent 并行探索
├── analyst/
│   ├── role.md              # 深度分析
│   └── commands/
│       └── analyze.md       # CLI 多视角分析
├── discussant/
│   ├── role.md              # 讨论处理 + 方向调整
│   └── commands/
│       └── deepen.md        # 深入探索
└── synthesizer/
    ├── role.md              # 综合结论
    └── commands/
        └── synthesize.md    # 跨视角整合
```

**设计原则**: role.md 保留 Phase 1（Task Discovery）和 Phase 5（Report）内联。Phase 2-4 根据复杂度决定内联或委派到 `commands/*.md`。

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, explorer, analyst, discussant, synthesizer")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "ultra-analyze"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator":  { file: "roles/coordinator/role.md",  prefix: null },
  "explorer":     { file: "roles/explorer/role.md",     prefix: "EXPLORE" },
  "analyst":      { file: "roles/analyst/role.md",       prefix: "ANALYZE" },
  "discussant":   { file: "roles/discussant/role.md",    prefix: "DISCUSS" },
  "synthesizer":  { file: "roles/synthesizer/role.md",   prefix: "SYNTH" }
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
| `coordinator` | N/A | 话题澄清、管道选择、会话管理、讨论循环 | [roles/coordinator/role.md](roles/coordinator/role.md) |
| `explorer` | EXPLORE-* | cli-explore-agent 多角度并行代码库探索 | [roles/explorer/role.md](roles/explorer/role.md) |
| `analyst` | ANALYZE-* | CLI 多视角深度分析 | [roles/analyst/role.md](roles/analyst/role.md) |
| `discussant` | DISCUSS-* | 用户反馈处理、方向调整、深入分析 | [roles/discussant/role.md](roles/discussant/role.md) |
| `synthesizer` | SYNTH-* | 跨视角整合、结论生成、决策追踪 | [roles/synthesizer/role.md](roles/synthesizer/role.md) |

## Shared Infrastructure

### Role Isolation Rules

**核心原则**: 每个角色仅能执行自己职责范围内的工作。

#### Output Tagging（强制）

所有角色的输出必须带 `[role_name]` 标识前缀：

```javascript
SendMessage({ content: `## [${role}] ...`, summary: `[${role}] ...` })
mcp__ccw-tools__team_msg({ summary: `[${role}] ...` })
```

#### Coordinator 隔离

| 允许 | 禁止 |
|------|------|
| 话题澄清 (AskUserQuestion) | ❌ 直接执行代码探索或分析 |
| 创建任务链 (TaskCreate) | ❌ 直接调用 cli-explore-agent |
| 管道选择 + 讨论循环驱动 | ❌ 直接调用 CLI 分析工具 |
| 监控进度 (消息总线) | ❌ 绕过 worker 自行完成 |

#### Worker 隔离

| 允许 | 禁止 |
|------|------|
| 处理自己前缀的任务 | ❌ 处理其他角色前缀的任务 |
| 读写 shared-memory.json (自己的字段) | ❌ 为其他角色创建任务 |
| SendMessage 给 coordinator | ❌ 直接与其他 worker 通信 |

### Team Configuration

```javascript
const TEAM_CONFIG = {
  name: "ultra-analyze",
  sessionDir: ".workflow/.team/UAN-{slug}-{date}/",
  msgDir: ".workflow/.team-msg/ultra-analyze/",
  sharedMemory: "shared-memory.json",
  analysisDimensions: ["architecture", "implementation", "performance", "security", "concept", "comparison", "decision"],
  maxDiscussionRounds: 5
}
```

### Shared Memory（核心产物）

```javascript
// 各角色读取共享记忆
const memoryPath = `${sessionFolder}/shared-memory.json`
let sharedMemory = {}
try { sharedMemory = JSON.parse(Read(memoryPath)) } catch {}

// 各角色写入自己负责的字段：
// explorer    → sharedMemory.explorations
// analyst     → sharedMemory.analyses
// discussant  → sharedMemory.discussions
// synthesizer → sharedMemory.synthesis
// coordinator → sharedMemory.decision_trail + current_understanding
Write(memoryPath, JSON.stringify(sharedMemory, null, 2))
```

### Message Bus (All Roles)

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

| Role | Types |
|------|-------|
| coordinator | `pipeline_selected`, `discussion_round`, `direction_adjusted`, `task_unblocked`, `error`, `shutdown` |
| explorer | `exploration_ready`, `error` |
| analyst | `analysis_ready`, `error` |
| discussant | `discussion_processed`, `error` |
| synthesizer | `synthesis_ready`, `error` |

### CLI 回退

```javascript
Bash(`ccw team log --team "${teamName}" --from "${role}" --to "coordinator" --type "<type>" --summary "<摘要>" --json`)
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
if (myTasks.length === 0) return
const task = TaskGet({ taskId: myTasks[0].id })
TaskUpdate({ taskId: task.id, status: 'in_progress' })

// Phase 2-4: Role-specific
// Phase 5: Report + Loop
mcp__ccw-tools__team_msg({ operation: "log", team: teamName, from: role, to: "coordinator", type: "...", summary: `[${role}] ...` })
SendMessage({ type: "message", recipient: "coordinator", content: `## [${role}] ...`, summary: `[${role}] ...` })
TaskUpdate({ taskId: task.id, status: 'completed' })
```

## Three-Mode Pipeline Architecture

```
Quick:    EXPLORE-001 → ANALYZE-001 → SYNTH-001
Standard: [EXPLORE-001..N](parallel) → [ANALYZE-001..N](parallel) → DISCUSS-001 → SYNTH-001
Deep:     [EXPLORE-001..N] → [ANALYZE-001..N] → DISCUSS-001 → ANALYZE-fix → DISCUSS-002 → ... → SYNTH-001
```

### Mode Auto-Detection

```javascript
function detectPipelineMode(args, taskDescription) {
  const modeMatch = args.match(/--mode[=\s]+(quick|standard|deep)/)
  if (modeMatch) return modeMatch[1]
  // 自动检测
  if (/快速|quick|overview|概览/.test(taskDescription)) return 'quick'
  if (/深入|deep|thorough|详细|全面/.test(taskDescription)) return 'deep'
  return 'standard'
}
```

### Discussion Loop (Deep Mode)

```
coordinator(AskUser) → DISCUSS-N(deepen) → [optional ANALYZE-fix] → coordinator(AskUser) → ... → SYNTH
```

## Decision Recording Protocol

**⚠️ CRITICAL**: 继承自原 analyze-with-file 命令。分析过程中以下情况必须立即记录到 discussion.md：

| Trigger | What to Record | Target Section |
|---------|---------------|----------------|
| **Direction choice** | 选择了什么、为什么、放弃了哪些替代方案 | `#### Decision Log` |
| **Key finding** | 发现内容、影响范围、置信度 | `#### Key Findings` |
| **Assumption change** | 旧假设→新理解、变更原因、影响 | `#### Corrected Assumptions` |
| **User feedback** | 用户原始输入、采纳/调整理由 | `#### User Input` |

## Unified Session Directory

```
.workflow/.team/UAN-{slug}-{YYYY-MM-DD}/
├── shared-memory.json          # 探索/分析/讨论/综合 共享记忆
├── discussion.md               # ⭐ 理解演进 & 讨论时间线
├── explorations/               # Explorer output
│   ├── exploration-001.json
│   └── exploration-002.json
├── analyses/                   # Analyst output
│   ├── analysis-001.json
│   └── analysis-002.json
├── discussions/                # Discussant output
│   └── discussion-round-001.json
└── conclusions.json            # Synthesizer output
```

## Coordinator Spawn Template

```javascript
TeamCreate({ team_name: teamName })

// Explorer
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "explorer",
  prompt: `你是 team "${teamName}" 的 EXPLORER。

当你收到 EXPLORE-* 任务时，调用 Skill(skill="team-ultra-analyze", args="--role=explorer") 执行。

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
2. Skill(skill="team-ultra-analyze", args="--role=explorer") 执行
3. team_msg log + SendMessage 结果给 coordinator（带 [explorer] 标识）
4. TaskUpdate completed → 检查下一个任务`
})

// Analyst
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "analyst",
  prompt: `你是 team "${teamName}" 的 ANALYST。

当你收到 ANALYZE-* 任务时，调用 Skill(skill="team-ultra-analyze", args="--role=analyst") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 ANALYZE-* 前缀的任务
- 所有输出必须带 [analyst] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 ANALYZE-* 任务
2. Skill(skill="team-ultra-analyze", args="--role=analyst") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Discussant
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "discussant",
  prompt: `你是 team "${teamName}" 的 DISCUSSANT。

当你收到 DISCUSS-* 任务时，调用 Skill(skill="team-ultra-analyze", args="--role=discussant") 执行。

当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 DISCUSS-* 前缀的任务
- 所有输出必须带 [discussant] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 DISCUSS-* 任务
2. Skill(skill="team-ultra-analyze", args="--role=discussant") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Synthesizer
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "synthesizer",
  prompt: `你是 team "${teamName}" 的 SYNTHESIZER。

当你收到 SYNTH-* 任务时，调用 Skill(skill="team-ultra-analyze", args="--role=synthesizer") 执行。

当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 SYNTH-* 前缀的任务
- 所有输出必须带 [synthesizer] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 SYNTH-* 任务
2. Skill(skill="team-ultra-analyze", args="--role=synthesizer") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Unknown --role value | Error with available role list |
| Missing --role arg | Error with usage hint |
| Role file not found | Error with expected path (roles/{name}/role.md) |
| Task prefix conflict | Log warning, proceed |
| Discussion loop stuck >5 rounds | Force synthesis, offer continuation |
| CLI tool unavailable | Fallback chain: gemini → codex → manual analysis |
| Explorer agent fails | Continue with available context, note limitation |
