---
name: team-quality-assurance
description: Unified team skill for quality assurance team. All roles invoke this skill with --role arg for role-specific execution. Triggers on "team quality-assurance", "team qa".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Task(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Quality Assurance

质量保障团队技能。融合"问题发现"和"软件测试"两大能力域，形成"发现→策略→测试→分析"闭环。通过 Scout 多视角扫描、Generator-Executor 循环、共享缺陷模式数据库，实现渐进式质量保障。所有成员通过 `--role=xxx` 路由到角色执行逻辑。

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│  Skill(skill="team-quality-assurance", args="--role=xxx") │
└────────────────────────┬─────────────────────────────────┘
                         │ Role Router
    ┌────────┬───────────┼───────────┬──────────┬──────────┐
    ↓        ↓           ↓           ↓          ↓          ↓
┌────────┐┌───────┐┌──────────┐┌─────────┐┌────────┐┌────────┐
│coordi- ││scout  ││strategist││generator││executor││analyst │
│nator   ││SCOUT-*││QASTRAT-* ││QAGEN-*  ││QARUN-* ││QAANA-* │
│ roles/ ││ roles/││ roles/   ││ roles/  ││ roles/ ││ roles/ │
└────────┘└───────┘└──────────┘└─────────┘└────────┘└────────┘
```

## Command Architecture

```
roles/
├── coordinator/
│   ├── role.md              # Pipeline 编排（模式选择、任务分发、监控）
│   └── commands/
│       ├── dispatch.md      # 任务链创建
│       └── monitor.md       # 进度监控
├── scout/
│   ├── role.md              # 多视角问题扫描
│   └── commands/
│       └── scan.md          # 多视角 CLI Fan-out 扫描
├── strategist/
│   ├── role.md              # 测试策略制定
│   └── commands/
│       └── analyze-scope.md # 变更范围分析
├── generator/
│   ├── role.md              # 测试用例生成
│   └── commands/
│       └── generate-tests.md # 按层级生成测试代码
├── executor/
│   ├── role.md              # 测试执行与修复
│   └── commands/
│       └── run-fix-cycle.md # 迭代测试修复循环
└── analyst/
    ├── role.md              # 质量分析报告
    └── commands/
        └── quality-report.md # 缺陷模式 + 覆盖率分析
```

**设计原则**: role.md 保留 Phase 1（Task Discovery）和 Phase 5（Report）内联。Phase 2-4 根据复杂度决定内联或委派到 `commands/*.md`。

## Role Router

### Input Parsing

Parse `$ARGUMENTS` to extract `--role`:

```javascript
const args = "$ARGUMENTS"
const roleMatch = args.match(/--role[=\s]+(\w+)/)

if (!roleMatch) {
  throw new Error("Missing --role argument. Available roles: coordinator, scout, strategist, generator, executor, analyst")
}

const role = roleMatch[1]
const teamName = args.match(/--team[=\s]+([\w-]+)/)?.[1] || "quality-assurance"
```

### Role Dispatch

```javascript
const VALID_ROLES = {
  "coordinator": { file: "roles/coordinator/role.md", prefix: null },
  "scout":       { file: "roles/scout/role.md",       prefix: "SCOUT" },
  "strategist":  { file: "roles/strategist/role.md",  prefix: "QASTRAT" },
  "generator":   { file: "roles/generator/role.md",   prefix: "QAGEN" },
  "executor":    { file: "roles/executor/role.md",     prefix: "QARUN" },
  "analyst":     { file: "roles/analyst/role.md",      prefix: "QAANA" }
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
| `coordinator` | N/A | QA pipeline 编排、模式选择、质量门控 | [roles/coordinator/role.md](roles/coordinator/role.md) |
| `scout` | SCOUT-* | 多视角问题扫描、主动发现潜在缺陷 | [roles/scout/role.md](roles/scout/role.md) |
| `strategist` | QASTRAT-* | 变更范围分析、测试层级选择、覆盖率目标 | [roles/strategist/role.md](roles/strategist/role.md) |
| `generator` | QAGEN-* | 按层级生成测试用例（unit/integration/E2E） | [roles/generator/role.md](roles/generator/role.md) |
| `executor` | QARUN-* | 执行测试、收集覆盖率、自动修复循环 | [roles/executor/role.md](roles/executor/role.md) |
| `analyst` | QAANA-* | 缺陷模式分析、覆盖率差距、质量报告 | [roles/analyst/role.md](roles/analyst/role.md) |

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
| 需求澄清 (AskUserQuestion) | ❌ 直接编写测试 |
| 创建任务链 (TaskCreate) | ❌ 直接执行测试或扫描 |
| 模式选择 + 质量门控 | ❌ 直接分析覆盖率 |
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
  name: "quality-assurance",
  sessionDir: ".workflow/.team/QA-{slug}-{date}/",
  msgDir: ".workflow/.team-msg/quality-assurance/",
  sharedMemory: "shared-memory.json",
  testLayers: {
    L1: { name: "Unit Tests", coverage_target: 80 },
    L2: { name: "Integration Tests", coverage_target: 60 },
    L3: { name: "E2E Tests", coverage_target: 40 }
  },
  scanPerspectives: ["bug", "security", "ux", "test-coverage", "code-quality"]
}
```

### Shared Memory（核心创新）

```javascript
// 各角色读取共享记忆
const memoryPath = `${sessionFolder}/shared-memory.json`
let sharedMemory = {}
try { sharedMemory = JSON.parse(Read(memoryPath)) } catch {}

// 各角色写入自己负责的字段：
// scout      → sharedMemory.discovered_issues
// strategist → sharedMemory.test_strategy
// generator  → sharedMemory.generated_tests
// executor   → sharedMemory.execution_results
// analyst    → sharedMemory.defect_patterns + quality_score + coverage_history
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
| coordinator | `mode_selected`, `gc_loop_trigger`, `quality_gate`, `task_unblocked`, `error`, `shutdown` |
| scout | `scan_ready`, `issues_found`, `error` |
| strategist | `strategy_ready`, `error` |
| generator | `tests_generated`, `tests_revised`, `error` |
| executor | `tests_passed`, `tests_failed`, `coverage_report`, `error` |
| analyst | `analysis_ready`, `quality_report`, `error` |

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
Discovery Mode (问题发现优先):
  SCOUT-001(多视角扫描) → QASTRAT-001 → QAGEN-001 → QARUN-001 → QAANA-001

Testing Mode (测试优先，跳过 scout):
  QASTRAT-001(变更分析) → QAGEN-001(L1) → QARUN-001(L1) → QAGEN-002(L2) → QARUN-002(L2) → QAANA-001

Full QA Mode (完整闭环):
  SCOUT-001(扫描) → QASTRAT-001(策略) → [QAGEN-001(L1) + QAGEN-002(L2)](parallel) → [QARUN-001 + QARUN-002](parallel) → QAANA-001(分析) → SCOUT-002(回归扫描)
```

### Mode Auto-Detection

```javascript
function detectQAMode(args, taskDescription) {
  if (/--mode[=\s]+(discovery|testing|full)/.test(args)) {
    return args.match(/--mode[=\s]+(\w+)/)[1]
  }
  // 自动检测
  if (/发现|扫描|scan|discover|issue|问题/.test(taskDescription)) return 'discovery'
  if (/测试|test|覆盖|coverage|TDD/.test(taskDescription)) return 'testing'
  return 'full'
}
```

### Generator-Executor Loop (GC 循环)

```
QAGEN → QARUN → (if coverage < target) → QAGEN-fix → QARUN-2
                  (if coverage >= target) → next layer or QAANA
```

## Unified Session Directory

```
.workflow/.team/QA-{slug}-{YYYY-MM-DD}/
├── team-session.json
├── shared-memory.json          # 发现的问题 / 测试策略 / 缺陷模式 / 覆盖率历史
├── scan/                       # Scout output
│   └── scan-results.json
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

// Scout
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "scout",
  prompt: `你是 team "${teamName}" 的 SCOUT。

当你收到 SCOUT-* 任务时，调用 Skill(skill="team-quality-assurance", args="--role=scout") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 SCOUT-* 前缀的任务，不得执行其他角色的工作
- 所有输出（SendMessage、team_msg）必须带 [scout] 标识前缀
- 仅与 coordinator 通信，不得直接联系其他 worker
- 不得使用 TaskCreate 为其他角色创建任务

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 SCOUT-* 任务
2. Skill(skill="team-quality-assurance", args="--role=scout") 执行
3. team_msg log + SendMessage 结果给 coordinator（带 [scout] 标识）
4. TaskUpdate completed → 检查下一个任务`
})

// Strategist
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "strategist",
  prompt: `你是 team "${teamName}" 的 STRATEGIST。

当你收到 QASTRAT-* 任务时，调用 Skill(skill="team-quality-assurance", args="--role=strategist") 执行。

当前需求: ${taskDescription}
约束: ${constraints}

## 角色准则（强制）
- 你只能处理 QASTRAT-* 前缀的任务
- 所有输出必须带 [strategist] 标识前缀
- 仅与 coordinator 通信

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 QASTRAT-* 任务
2. Skill(skill="team-quality-assurance", args="--role=strategist") 执行
3. team_msg log + SendMessage 结果给 coordinator
4. TaskUpdate completed → 检查下一个任务`
})

// Generator
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "generator",
  prompt: `你是 team "${teamName}" 的 GENERATOR。

当你收到 QAGEN-* 任务时，调用 Skill(skill="team-quality-assurance", args="--role=generator") 执行。

当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 QAGEN-* 前缀的任务
- 所有输出必须带 [generator] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 QAGEN-* 任务
2. Skill(skill="team-quality-assurance", args="--role=generator") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Executor
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "executor",
  prompt: `你是 team "${teamName}" 的 EXECUTOR。

当你收到 QARUN-* 任务时，调用 Skill(skill="team-quality-assurance", args="--role=executor") 执行。

当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 QARUN-* 前缀的任务
- 所有输出必须带 [executor] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 QARUN-* 任务
2. Skill(skill="team-quality-assurance", args="--role=executor") 执行
3. team_msg log + SendMessage
4. TaskUpdate completed → 检查下一个任务`
})

// Analyst
Task({
  subagent_type: "general-purpose",
  team_name: teamName,
  name: "analyst",
  prompt: `你是 team "${teamName}" 的 ANALYST。

当你收到 QAANA-* 任务时，调用 Skill(skill="team-quality-assurance", args="--role=analyst") 执行。

当前需求: ${taskDescription}

## 角色准则（强制）
- 你只能处理 QAANA-* 前缀的任务
- 所有输出必须带 [analyst] 标识前缀

## 消息总线（必须）
每次 SendMessage 前，先调用 mcp__ccw-tools__team_msg 记录。

工作流程:
1. TaskList → 找到 QAANA-* 任务
2. Skill(skill="team-quality-assurance", args="--role=analyst") 执行
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
| Coverage never reaches target | After 3 GC loops, accept current with warning |
| Scout finds no issues | Report clean scan, skip to testing mode |
| Test environment broken | Notify user, suggest manual fix |
