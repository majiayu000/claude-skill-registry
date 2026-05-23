---
name: ccw-loop
description: Stateless iterative development loop workflow with documented progress. Supports develop, debug, and validate phases with file-based state tracking. Triggers on "ccw-loop", "dev loop", "development loop", "开发循环", "迭代开发".
allowed-tools: Task(*), AskUserQuestion(*), Read(*), Grep(*), Glob(*), Bash(*), Edit(*), Write(*), TodoWrite(*)
---

# CCW Loop - Stateless Iterative Development Workflow

无状态迭代开发循环工作流，支持开发 (develop)、调试 (debug)、验证 (validate) 三个阶段，每个阶段都有独立的文件记录进展。

## Arguments

| Arg | Required | Description |
|-----|----------|-------------|
| task | No | Task description (for new loop, mutually exclusive with --loop-id) |
| --loop-id | No | Existing loop ID to continue (from API or previous session) |
| --auto | No | Auto-cycle mode (develop → debug → validate → complete) |

## Unified Architecture (API + Skill Integration)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Dashboard (UI)                              │
│  [Create] [Start] [Pause] [Resume] [Stop] [View Progress]       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              loop-v2-routes.ts (Control Plane)                  │
│                                                                 │
│  State: .loop/{loopId}.json (MASTER)                            │
│  Tasks: .loop/{loopId}.tasks.jsonl                              │
│                                                                 │
│  /start → Trigger ccw-loop skill with --loop-id                 │
│  /pause → Set status='paused' (skill checks before action)      │
│  /stop  → Set status='failed' (skill terminates)                │
│  /resume → Set status='running' (skill continues)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               ccw-loop Skill (Execution Plane)                  │
│                                                                 │
│  Reads/Writes: .loop/{loopId}.json (unified state)              │
│  Writes: .loop/{loopId}.progress/* (progress files)             │
│                                                                 │
│  BEFORE each action:                                            │
│    → Check status: paused/stopped → exit gracefully             │
│    → running → continue with action                             │
│                                                                 │
│  Actions: init → develop → debug → validate → complete          │
└─────────────────────────────────────────────────────────────────┘
```

## Key Design Principles

1. **统一状态**: API 和 Skill 共享 `.loop/{loopId}.json` 状态文件
2. **控制信号**: Skill 每个 Action 前检查 status 字段 (paused/stopped)
3. **文件驱动**: 所有进度、理解、结果都记录在 `.loop/{loopId}.progress/`
4. **可恢复**: 任何时候可以继续之前的循环 (`--loop-id`)
5. **双触发**: 支持 API 触发 (`--loop-id`) 和直接调用 (task description)
6. **Gemini 辅助**: 使用 CLI 工具进行深度分析和假设验证

## Execution Modes

### Mode 1: Interactive (交互式)

用户手动选择每个动作，适合复杂任务。

```
用户 → 选择动作 → 执行 → 查看结果 → 选择下一动作
```

### Mode 2: Auto-Loop (自动循环)

按预设顺序自动执行，适合标准开发流程。

```
Develop → Debug → Validate → (如有问题) → Develop → ...
```

## Session Structure (Unified Location)

```
.loop/
├── {loopId}.json              # 主状态文件 (API + Skill 共享)
├── {loopId}.tasks.jsonl       # 任务列表 (API 管理)
└── {loopId}.progress/         # Skill 进度文件
    ├── develop.md             # 开发进度记录
    ├── debug.md               # 理解演变文档
    ├── validate.md            # 验证报告
    ├── changes.log            # 代码变更日志 (NDJSON)
    └── debug.log              # 调试日志 (NDJSON)
```

## Directory Setup

```javascript
// loopId 来源:
// 1. API 触发时: 从 --loop-id 参数获取
// 2. 直接调用时: 生成新的 loop-v2-{timestamp}-{random}

const loopId = args['--loop-id'] || generateLoopId()
const loopFile = `.loop/${loopId}.json`
const progressDir = `.loop/${loopId}.progress`

// 创建进度目录
Bash(`mkdir -p "${progressDir}"`)
```

## Action Catalog

| Action | Purpose | Output Files | CLI Integration |
|--------|---------|--------------|-----------------|
| [action-init](phases/actions/action-init.md) | 初始化循环会话 | meta.json, state.json | - |
| [action-develop-with-file](phases/actions/action-develop-with-file.md) | 开发任务执行 | progress.md, tasks.json | gemini --mode write |
| [action-debug-with-file](phases/actions/action-debug-with-file.md) | 假设驱动调试 | understanding.md, hypotheses.json | gemini --mode analysis |
| [action-validate-with-file](phases/actions/action-validate-with-file.md) | 测试与验证 | validation.md, test-results.json | gemini --mode analysis |
| [action-complete](phases/actions/action-complete.md) | 完成循环 | summary.md | - |
| [action-menu](phases/actions/action-menu.md) | 显示操作菜单 | - | - |

## Usage

```bash
# 启动新循环 (直接调用)
/ccw-loop "实现用户认证功能"

# 继续现有循环 (API 触发或手动恢复)
/ccw-loop --loop-id loop-v2-20260122-abc123

# 自动循环模式
/ccw-loop --auto "修复登录bug并添加测试"

# API 触发自动循环
/ccw-loop --loop-id loop-v2-20260122-abc123 --auto
```

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  /ccw-loop [<task> | --loop-id <id>] [--auto]                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Parameter Detection:                                         │
│     ├─ IF --loop-id provided:                                    │
│     │   ├─ Read .loop/{loopId}.json                              │
│     │   ├─ Validate status === 'running'                         │
│     │   └─ Continue from skill_state.current_action              │
│     └─ ELSE (task description):                                  │
│         ├─ Generate new loopId                                   │
│         ├─ Create .loop/{loopId}.json                            │
│         └─ Initialize with action-init                           │
│                                                                  │
│  2. Orchestrator Loop:                                           │
│     ├─ Read state from .loop/{loopId}.json                       │
│     ├─ Check control signals:                                    │
│     │   ├─ status === 'paused' → Exit (wait for resume)          │
│     │   ├─ status === 'failed' → Exit with error                 │
│     │   └─ status === 'running' → Continue                       │
│     ├─ Show menu / auto-select next action                       │
│     ├─ Execute action                                            │
│     ├─ Update .loop/{loopId}.progress/{action}.md                │
│     ├─ Update .loop/{loopId}.json (skill_state)                  │
│     └─ Loop or exit based on user choice / completion            │
│                                                                  │
│  3. Action Execution:                                            │
│     ├─ BEFORE: checkControlSignals() → exit if paused/stopped    │
│     ├─ Develop: Plan → Implement → Document progress             │
│     ├─ Debug: Hypothesize → Instrument → Analyze → Fix           │
│     ├─ Validate: Test → Check → Report                           │
│     └─ AFTER: Update skill_state in .loop/{loopId}.json          │
│                                                                  │
│  4. Termination:                                                 │
│     ├─ Control signal: paused (graceful exit, wait resume)       │
│     ├─ Control signal: stopped (failed state)                    │
│     ├─ User exits (interactive mode)                             │
│     ├─ All tasks completed (status → completed)                  │
│     └─ Max iterations reached                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Reference Documents

| Document | Purpose |
|----------|---------|
| [phases/orchestrator.md](phases/orchestrator.md) | 编排器：状态读取 + 动作选择 |
| [phases/state-schema.md](phases/state-schema.md) | 状态结构定义 |
| [specs/loop-requirements.md](specs/loop-requirements.md) | 循环需求规范 |
| [specs/action-catalog.md](specs/action-catalog.md) | 动作目录 |
| [templates/progress-template.md](templates/progress-template.md) | 进度文档模板 |
| [templates/understanding-template.md](templates/understanding-template.md) | 理解文档模板 |

## Integration with Loop Monitor (Dashboard)

此 Skill 与 CCW Dashboard 的 Loop Monitor 实现 **控制平面 + 执行平面** 分离架构：

### Control Plane (Dashboard/API → loop-v2-routes.ts)

1. **创建循环**: `POST /api/loops/v2` → 创建 `.loop/{loopId}.json`
2. **启动执行**: `POST /api/loops/v2/:loopId/start` → 触发 `/ccw-loop --loop-id {loopId} --auto`
3. **暂停执行**: `POST /api/loops/v2/:loopId/pause` → 设置 `status='paused'` (Skill 下次检查时退出)
4. **恢复执行**: `POST /api/loops/v2/:loopId/resume` → 设置 `status='running'` → 重新触发 Skill
5. **停止执行**: `POST /api/loops/v2/:loopId/stop` → 设置 `status='failed'`

### Execution Plane (ccw-loop Skill)

1. **读取状态**: 从 `.loop/{loopId}.json` 读取 API 设置的状态
2. **检查控制**: 每个 Action 前检查 `status` 字段
3. **执行动作**: develop → debug → validate → complete
4. **更新进度**: 写入 `.loop/{loopId}.progress/*.md` 和更新 `skill_state`
5. **状态同步**: Dashboard 通过读取 `.loop/{loopId}.json` 获取进度

## CLI Integration Points

### Develop Phase
```bash
ccw cli -p "PURPOSE: Implement {task}...
TASK: • Analyze requirements • Write code • Update progress
MODE: write
CONTEXT: @progress.md @tasks.json
EXPECTED: Implementation + updated progress.md
" --tool gemini --mode write --rule development-implement-feature
```

### Debug Phase
```bash
ccw cli -p "PURPOSE: Generate debugging hypotheses...
TASK: • Analyze error • Generate hypotheses • Add instrumentation
MODE: analysis
CONTEXT: @understanding.md @debug.log
EXPECTED: Hypotheses + instrumentation plan
" --tool gemini --mode analysis --rule analysis-diagnose-bug-root-cause
```

### Validate Phase
```bash
ccw cli -p "PURPOSE: Validate implementation...
TASK: • Run tests • Check coverage • Verify requirements
MODE: analysis
CONTEXT: @validation.md @test-results.json
EXPECTED: Validation report
" --tool gemini --mode analysis --rule analysis-review-code-quality
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Session not found | Create new session |
| State file corrupted | Rebuild from file contents |
| CLI tool fails | Fallback to manual analysis |
| Tests fail | Loop back to develop/debug |
| >10 iterations | Warn user, suggest break |

## Post-Completion Expansion

完成后询问用户是否扩展为 issue (test/enhance/refactor/doc)，选中项调用 `/issue:new "{summary} - {dimension}"`
