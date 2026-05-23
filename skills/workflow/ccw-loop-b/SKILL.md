---
name: CCW Loop-B
description: Hybrid orchestrator pattern for iterative development. Coordinator + specialized workers with batch wait support. Triggers on "ccw-loop-b".
argument-hint: TASK="<task description>" [--loop-id=<id>] [--mode=<interactive|auto|parallel>]
---

# CCW Loop-B - Hybrid Orchestrator Pattern

协调器 + 专用 worker 的迭代开发工作流。支持单 agent 深度交互、多 agent 并行、混合模式灵活切换。

## Arguments

| Arg | Required | Description |
|-----|----------|-------------|
| TASK | No | Task description (for new loop) |
| --loop-id | No | Existing loop ID to continue |
| --mode | No | `interactive` (default) / `auto` / `parallel` |

## Architecture

```
+------------------------------------------------------------+
|                    Main Coordinator                         |
|  职责: 状态管理 + worker 调度 + 结果汇聚 + 用户交互        |
+------------------------------------------------------------+
                              |
         +--------------------+--------------------+
         |                    |                    |
         v                    v                    v
+----------------+   +----------------+   +----------------+
| Worker-Develop |   | Worker-Debug   |   | Worker-Validate|
| 专注: 代码实现 |   | 专注: 问题诊断 |   | 专注: 测试验证 |
+----------------+   +----------------+   +----------------+
```

## Execution Modes

### Mode: Interactive (default)

协调器展示菜单，用户选择 action，spawn 对应 worker 执行。

```
Coordinator -> Show menu -> User selects -> spawn worker -> wait -> Display result -> Loop
```

### Mode: Auto

自动按预设顺序执行，worker 完成后自动切换到下一阶段。

```
Init -> Develop -> [if issues] Debug -> Validate -> [if fail] Loop back -> Complete
```

### Mode: Parallel

并行 spawn 多个 worker 分析不同维度，batch wait 汇聚结果。

```
Coordinator -> spawn [develop, debug, validate] in parallel -> wait({ ids: all }) -> Merge -> Decide
```

## Session Structure

```
.workflow/.loop/
+-- {loopId}.json              # Master state
+-- {loopId}.workers/          # Worker outputs
|   +-- develop.output.json
|   +-- debug.output.json
|   +-- validate.output.json
+-- {loopId}.progress/         # Human-readable progress
    +-- develop.md
    +-- debug.md
    +-- validate.md
    +-- summary.md
```

## Subagent API

| API | 作用 |
|-----|------|
| `spawn_agent({ message })` | 创建 agent，返回 `agent_id` |
| `wait({ ids, timeout_ms })` | 等待结果（唯一取结果入口） |
| `send_input({ id, message })` | 继续交互 |
| `close_agent({ id })` | 关闭回收 |

## Implementation

### Coordinator Logic

```javascript
// ==================== HYBRID ORCHESTRATOR ====================

// 1. Initialize
const loopId = args['--loop-id'] || generateLoopId()
const mode = args['--mode'] || 'interactive'
let state = readOrCreateState(loopId, taskDescription)

// 2. Mode selection
switch (mode) {
  case 'interactive':
    await runInteractiveMode(loopId, state)
    break

  case 'auto':
    await runAutoMode(loopId, state)
    break

  case 'parallel':
    await runParallelMode(loopId, state)
    break
}
```

### Interactive Mode (单 agent 交互或按需 spawn worker)

```javascript
async function runInteractiveMode(loopId, state) {
  while (state.status === 'running') {
    // Show menu, get user choice
    const action = await showMenuAndGetChoice(state)

    if (action === 'exit') break

    // Spawn specialized worker for the action
    const workerId = spawn_agent({
      message: buildWorkerPrompt(action, loopId, state)
    })

    // Wait for worker completion
    const result = wait({ ids: [workerId], timeout_ms: 600000 })
    const output = result.status[workerId].completed

    // Update state and display result
    state = updateState(loopId, action, output)
    displayResult(output)

    // Cleanup worker
    close_agent({ id: workerId })
  }
}
```

### Auto Mode (顺序执行 worker 链)

```javascript
async function runAutoMode(loopId, state) {
  const actionSequence = ['init', 'develop', 'debug', 'validate', 'complete']
  let currentIndex = state.skill_state?.action_index || 0

  while (currentIndex < actionSequence.length && state.status === 'running') {
    const action = actionSequence[currentIndex]

    // Spawn worker
    const workerId = spawn_agent({
      message: buildWorkerPrompt(action, loopId, state)
    })

    const result = wait({ ids: [workerId], timeout_ms: 600000 })
    const output = result.status[workerId].completed

    // Parse worker result to determine next step
    const workerResult = parseWorkerResult(output)

    // Update state
    state = updateState(loopId, action, output)

    close_agent({ id: workerId })

    // Determine next action
    if (workerResult.needs_loop_back) {
      // Loop back to develop or debug
      currentIndex = actionSequence.indexOf(workerResult.loop_back_to)
    } else if (workerResult.status === 'failed') {
      // Stop on failure
      break
    } else {
      currentIndex++
    }
  }
}
```

### Parallel Mode (批量 spawn + wait)

```javascript
async function runParallelMode(loopId, state) {
  // Spawn multiple workers in parallel
  const workers = {
    develop: spawn_agent({ message: buildWorkerPrompt('develop', loopId, state) }),
    debug: spawn_agent({ message: buildWorkerPrompt('debug', loopId, state) }),
    validate: spawn_agent({ message: buildWorkerPrompt('validate', loopId, state) })
  }

  // Batch wait for all workers
  const results = wait({
    ids: Object.values(workers),
    timeout_ms: 900000  // 15 minutes for all
  })

  // Collect outputs
  const outputs = {}
  for (const [role, workerId] of Object.entries(workers)) {
    outputs[role] = results.status[workerId].completed
    close_agent({ id: workerId })
  }

  // Merge and analyze results
  const mergedAnalysis = mergeWorkerOutputs(outputs)

  // Update state with merged results
  updateState(loopId, 'parallel-analysis', mergedAnalysis)

  // Coordinator decides next action based on merged results
  const decision = decideNextAction(mergedAnalysis)
  return decision
}
```

### Worker Prompt Builder

```javascript
function buildWorkerPrompt(action, loopId, state) {
  const workerRoles = {
    develop: '~/.codex/agents/ccw-loop-b-develop.md',
    debug: '~/.codex/agents/ccw-loop-b-debug.md',
    validate: '~/.codex/agents/ccw-loop-b-validate.md',
    init: '~/.codex/agents/ccw-loop-b-init.md',
    complete: '~/.codex/agents/ccw-loop-b-complete.md'
  }

  return `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ${workerRoles[action]} (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

## LOOP CONTEXT

- **Loop ID**: ${loopId}
- **Action**: ${action}
- **State File**: .workflow/.loop/${loopId}.json
- **Output File**: .workflow/.loop/${loopId}.workers/${action}.output.json
- **Progress File**: .workflow/.loop/${loopId}.progress/${action}.md

## CURRENT STATE

${JSON.stringify(state, null, 2)}

## TASK DESCRIPTION

${state.description}

## EXPECTED OUTPUT

\`\`\`
WORKER_RESULT:
- action: ${action}
- status: success | failed | needs_input
- summary: <brief summary>
- files_changed: [list]
- next_suggestion: <suggested next action>
- loop_back_to: <action name if needs loop back>

DETAILED_OUTPUT:
<structured output specific to action type>
\`\`\`

Execute the ${action} action now.
`
}
```

## Worker Roles

| Worker | Role File | 专注领域 |
|--------|-----------|----------|
| init | ccw-loop-b-init.md | 会话初始化、任务解析 |
| develop | ccw-loop-b-develop.md | 代码实现、重构 |
| debug | ccw-loop-b-debug.md | 问题诊断、假设验证 |
| validate | ccw-loop-b-validate.md | 测试执行、覆盖率 |
| complete | ccw-loop-b-complete.md | 总结收尾 |

## State Schema

See [phases/state-schema.md](phases/state-schema.md)

## Usage

```bash
# Interactive mode (default)
/ccw-loop-b TASK="Implement user authentication"

# Auto mode
/ccw-loop-b --mode=auto TASK="Fix login bug"

# Parallel analysis mode
/ccw-loop-b --mode=parallel TASK="Analyze and improve payment module"

# Resume existing loop
/ccw-loop-b --loop-id=loop-b-20260122-abc123
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Worker timeout | send_input 请求收敛 |
| Worker failed | Log error, 协调器决策是否重试 |
| Batch wait partial timeout | 使用已完成结果继续 |
| State corrupted | 从 progress 文件重建 |

## Best Practices

1. **协调器保持轻量**: 只做调度和状态管理，具体工作交给 worker
2. **Worker 职责单一**: 每个 worker 专注一个领域
3. **结果标准化**: Worker 输出遵循统一 WORKER_RESULT 格式
4. **灵活模式切换**: 根据任务复杂度选择合适模式
5. **及时清理**: Worker 完成后 close_agent 释放资源
