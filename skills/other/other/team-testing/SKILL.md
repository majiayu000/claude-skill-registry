---
name: team-testing
description: Unified team skill for testing team. All roles invoke this skill with --role arg for role-specific execution. Triggers on "team testing".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Testing

测试团队技能。通过 Generator-Critic 循环（generator↔executor）、共享记忆（缺陷模式追踪）和动态层级选择，实现渐进式测试覆盖。所有团队成员通过 `--role=xxx` 路由到角色执行逻辑。

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│  Skill(skill="team-testing", args="--role=xxx")   │
└───────────────────┬──────────────────────────────┘
                    │ Role Router
    ┌───────────┬───┼───────────┬───────────┐
    ↓           ↓   ↓           ↓           ↓
┌──────────┐┌──────────┐┌─────────┐┌────────┐┌────────┐
│coordinator││strategist││generator││executor││analyst │
│ roles/   ││ roles/   ││ roles/  ││ roles/ ││ roles/ │
└──────────┘└──────────┘└─────────┘└────────┘└────────┘
```

## Role Router

### Input Parsing

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, strategist, generator, executor, analyst")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "testing"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator": { file: "roles/coordinator.md", prefix: null },
  "strategist":  { file: "roles/strategist.md",  prefix: "STRATEGY" },
  "generator":   { file: "roles/generator.md",   prefix: "TESTGEN" },
  "executor":    { file: "roles/executor.md",     prefix: "TESTRUN" },
  "analyst":     { file: "roles/analyst.md",      prefix: "TESTANA" }
}

if (!VALID_ROLES[role]) {
  throw new Error(`Unknown role: ${role}. Available: ${Object.keys(VALID_ROLES).join(', ')}`)
}

Read(VALID_ROLES[role].file)
```

### Available Roles

| Role | Task Prefix | Responsibility | Role File |
|------|-------------|----------------|-----------|
| `coordinator` | N/A | 变更范围分析、层级选择、质量门控 | [roles/coordinator.md](roles/coordinator.md) |
| `strategist` | STRATEGY-* | 分析 git diff、确定测试层级、定义覆盖率目标 | [roles/strategist.md](roles/strategist.md) |
| `generator` | TESTGEN-* | 按层级生成测试用例（单元/集成/E2E） | [roles/generator.md](roles/generator.md) |
| `executor` | TESTRUN-* | 执行测试、收集覆盖率、自动修复 | [roles/executor.md](roles/executor.md) |
| `analyst` | TESTANA-* | 缺陷模式分析、覆盖率差距、质量报告 | [roles/analyst.md](roles/analyst.md) |

## Shared Infrastructure

### Role Isolation Rules

**核心原则**: 每个角色仅能执行自己职责范围内的工作。

#### Output Tagging（强制）

```javascript
SendMessage({ content: `## [${role}] ...`, summary: `[${role}] ...` })
mcp__ccw-tools__team_msg({ summary: `[${role}] ...` })
```

#### Coordinator 隔离

| 允许 | 禁止 |
|------|------|
| 变更范围分析 | ❌ 直接编写测试 |
| 创建任务链 (TaskCreate) | ❌ 直接执行测试 |
| 质量门控判断 | ❌ 直接分析覆盖率 |
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
  name: "testing",
  sessionDir: ".workflow/.team/TST-{slug}-{date}/",
  msgDir: ".workflow/.team-msg/testing/",
  sharedMemory: "shared-memory.json",
  testLayers: {
    L1: { name: "Unit Tests", coverage_target: 80 },
    L2: { name: "Integration Tests", coverage_target: 60 },
    L3: { name: "E2E Tests", coverage_target: 40 }
  }
}
```

### Shared Memory (创新模式)

```javascript
// Phase 2: 读取共享记忆
const memoryPath = `${sessionFolder}/shared-memory.json`
let sharedMemory = {}
try { sharedMemory = JSON.parse(Read(memoryPath)) } catch {}

// Phase 5: 写入共享记忆（仅更新自己负责的字段）
// strategist → sharedMemory.test_strategy
// generator  → sharedMemory.generated_tests
// executor   → sharedMemory.execution_results + defect_patterns
// analyst    → sharedMemory.analysis_report + coverage_history
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
| coordinator | `pipeline_selected`, `gc_loop_trigger`, `quality_gate`, `task_unblocked`, `error`, `shutdown` |
| strategist | `strategy_ready`, `error` |
| generator | `tests_generated`, `tests_revised`, `error` |
| executor | `tests_passed`, `tests_failed`, `coverage_report`, `error` |
| analyst | `analysis_ready`, `error` |

### CLI Fallback

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
if (myTasks.length === 0) return
const task = TaskGet({ taskId: myTasks[0].id })
TaskUpdate({ taskId: task.id, status: 'in_progress' })

// Phase 2-4: Role-specific
// Phase 5: Report + Loop
mcp__ccw-tools__team_msg({ operation: "log", team: teamName, from: role, to: "coordinator", type: "...", summary: `[${role}] ...` })
SendMessage({ type: "message", recipient: "coordinator", content: `## [${role}] ...`, summary: `[${role}] ...` })
TaskUpdate({ taskId: task.id, status: 'completed' })
```

## Three-Pipeline Architecture

```
Targeted (小范围变更):
  STRATEGY-001 → TESTGEN-001(L1 unit) → TESTRUN-001

Standard (渐进式):
  STRATEGY-001 → TESTGEN-001(L1) → TESTRUN-001(L1) → TESTGEN-002(L2) → TESTRUN-002(L2) → TESTANA-001

Comprehensive (全覆盖):
  STRATEGY-001 → [TESTGEN-001(L1) + TESTGEN-002(L2)](parallel) → [TESTRUN-001(L1) + TESTRUN-002(L2)](parallel) → TESTGEN-003(L3) → TESTRUN-003(L3) → TESTANA-001
```

### Generator-Critic Loop

generator ↔ executor 循环（覆盖率不达标时修订测试）：

```
TESTGEN → TESTRUN → (if coverage < target) → TESTGEN-fix → TESTRUN-2
                     (if coverage >= target) → next layer or TESTANA
```

## Unified Session Directory

```
.workflow/.team/TST-{slug}-{YYYY-MM-DD}/
├── team-session.json
├── shared-memory.json          # 缺陷模式 / 有效测试模式 / 覆盖率历史
├── strategy/                   # Strategist output
│   └── test-strategy.md
├── tests/                      # Generator output
│   ├── L1-unit/
│   ├── L2-integration/
│   └── L3-e2e/
├── results/                    # Executor output
│   ├── run-001.json
│   └── coverage-001.json
└── analysis/                   # Analyst output
    └── quality-report.md
```

## Coordinator Spawn Template

```javascript
TeamCreate({ team_name: teamName })

// Strategist
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "strategist",
  prompt: `你是 team "${teamName}" 的 STRATEGIST。
当你收到 STRATEGY-* 任务时，调用 Skill(skill="team-testing", args="--role=strategist") 执行。
当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 STRATEGY-* 前缀的任务
- 所有输出必须带 [strategist] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 STRATEGY-* 任务
2. Skill(skill="team-testing", args="--role=strategist") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Generator
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "generator",
  prompt: `你是 team "${teamName}" 的 GENERATOR。
当你收到 TESTGEN-* 任务时，调用 Skill(skill="team-testing", args="--role=generator") 执行。
当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 TESTGEN-* 前缀的任务
- 所有输出必须带 [generator] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 TESTGEN-* 任务
2. Skill(skill="team-testing", args="--role=generator") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Executor
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "executor",
  prompt: `你是 team "${teamName}" 的 EXECUTOR。
当你收到 TESTRUN-* 任务时，调用 Skill(skill="team-testing", args="--role=executor") 执行。
当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 TESTRUN-* 前缀的任务
- 所有输出必须带 [executor] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 TESTRUN-* 任务
2. Skill(skill="team-testing", args="--role=executor") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Analyst
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "analyst",
  prompt: `你是 team "${teamName}" 的 ANALYST。
当你收到 TESTANA-* 任务时，调用 Skill(skill="team-testing", args="--role=analyst") 执行。
当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 TESTANA-* 前缀的任务
- 所有输出必须带 [analyst] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 TESTANA-* 任务
2. Skill(skill="team-testing", args="--role=analyst") 执行
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
| Task prefix conflict | Log warning, proceed |
| Coverage never reaches target | After 3 GC loops, accept current coverage with warning |
| Test environment broken | Notify user, suggest manual fix |
