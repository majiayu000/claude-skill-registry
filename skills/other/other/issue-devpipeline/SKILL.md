---
name: issue-devpipeline
description: |
  Plan-and-Execute pipeline with Wave Pipeline pattern.
  Orchestrator coordinates planner (Deep Interaction) and executors (Parallel Fan-out).
  Planner produces wave queues, executors implement solutions concurrently.
agents: 4
phases: 4
---

# Issue DevPipeline

边规划边执行流水线。编排器通过 Wave Pipeline 协调 planner 和 executor(s)：planner 完成一个 wave 的规划后输出执行队列，编排器立即为该 wave 派发 executor agents，同时 planner 继续规划下一 wave。

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Orchestrator (this file)                                   │
│  → Parse input → Manage planner → Dispatch executors        │
└───────────┬──────────────────────────────────────┬──────────┘
            │                                      │
     ┌──────┴──────┐                    ┌──────────┴──────────┐
     │  Planner    │                    │  Executors (N)      │
     │  (Deep      │                    │  (Parallel Fan-out) │
     │  Interaction│                    │                     │
     │  multi-round│                    │  exec-1  exec-2 ... │
     └──────┬──────┘                    └──────────┬──────────┘
            │                                      │
     ┌──────┴──────┐                    ┌──────────┴──────────┐
     │ issue-plan  │                    │  code-developer     │
     │ issue-queue │                    │  (role reference)   │
     │ (existing)  │                    │                     │
     └─────────────┘                    └─────────────────────┘
```

**Wave Pipeline Flow**:
```
Planner Round 1 → Wave 1 queue
  ↓ (spawn executors for wave 1)
  ↓ send_input → Planner Round 2 → Wave 2 queue
  ↓ (spawn executors for wave 2)
  ...
  ↓ Planner outputs "ALL_PLANNED"
  ↓ wait for all executor agents
  ↓ Aggregate results → Done
```

## Agent Registry

| Agent | Role File | Responsibility | New/Existing |
|-------|-----------|----------------|--------------|
| `planex-planner` | `~/.codex/agents/planex-planner.md` | 需求拆解 → issue 创建 → 方案设计 → 队列编排 | New |
| `planex-executor` | `~/.codex/agents/planex-executor.md` | 加载 solution → 代码实现 → 测试 → 提交 | New |
| `issue-plan-agent` | `~/.codex/agents/issue-plan-agent.md` | Closed-loop: ACE 探索 + solution 生成 | Existing |
| `issue-queue-agent` | `~/.codex/agents/issue-queue-agent.md` | Solution 排序 + 冲突检测 → 执行队列 | Existing |

## Input Types

支持 3 种输入方式（通过 orchestrator 参数传入）：

| 输入类型 | 格式 | 示例 |
|----------|------|------|
| Issue IDs | 直接传入 ID | `ISS-20260215-001 ISS-20260215-002` |
| 需求文本 | `--text '...'` | `--text '实现用户认证模块'` |
| Plan 文件 | `--plan path` | `--plan plan/2026-02-15-auth.md` |

## Phase Execution

### Phase 1: Input Parsing (Orchestrator Inline)

```javascript
// Parse input arguments
const args = orchestratorInput
const issueIds = args.match(/ISS-\d{8}-\d{6}/g) || []
const textMatch = args.match(/--text\s+['"]([^'"]+)['"]/)
const planMatch = args.match(/--plan\s+(\S+)/)

let inputType = 'unknown'
if (issueIds.length > 0) inputType = 'issue_ids'
else if (textMatch) inputType = 'text'
else if (planMatch) inputType = 'plan_file'
else inputType = 'text_from_description'

const inputPayload = {
  type: inputType,
  issueIds: issueIds,
  text: textMatch ? textMatch[1] : args,
  planFile: planMatch ? planMatch[1] : null
}
```

### Phase 2: Planning (Deep Interaction with Planner)

```javascript
// Track all agents for cleanup
const allAgentIds = []

// Spawn planner agent
const plannerId = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/planex-planner.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

Goal: 分析需求并完成第一波 (Wave 1) 的规划。输出执行队列。

Input:
${JSON.stringify(inputPayload, null, 2)}

Scope:
- Include: 需求分析、issue 创建、方案设计、队列编排
- Exclude: 代码实现、测试执行、git 操作

Deliverables:
输出严格遵循以下 JSON 格式：
\`\`\`json
{
  "wave": 1,
  "status": "wave_ready" | "all_planned",
  "issues": ["ISS-xxx", ...],
  "queue": [
    {
      "issue_id": "ISS-xxx",
      "solution_id": "SOL-xxx",
      "title": "描述",
      "priority": "normal",
      "depends_on": []
    }
  ],
  "remaining_issues": ["ISS-yyy", ...],
  "summary": "本波次规划摘要"
}
\`\`\`

Quality bar:
- 每个 issue 必须有绑定的 solution
- 队列必须按依赖排序
- 每波最多 5 个 issues
`
})
allAgentIds.push(plannerId)

// Wait for planner Wave 1 output
let plannerResult = wait({ ids: [plannerId], timeout_ms: 900000 })

if (plannerResult.timed_out) {
  send_input({ id: plannerId, message: "请尽快输出当前已完成的规划结果。" })
  plannerResult = wait({ ids: [plannerId], timeout_ms: 120000 })
}

// Parse planner output
let waveData = parseWaveOutput(plannerResult.status[plannerId].completed)
```

### Phase 3: Wave Execution Loop

```javascript
const executorResults = []
let waveNum = 0

while (true) {
  waveNum++

  // ─── Dispatch executors for current wave (Parallel Fan-out) ───
  const waveExecutors = waveData.queue.map(entry =>
    spawn_agent({
      message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/planex-executor.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

Goal: 实现 ${entry.issue_id} 的 solution

Issue: ${entry.issue_id}
Solution: ${entry.solution_id}
Title: ${entry.title}
Priority: ${entry.priority}
Dependencies: ${entry.depends_on?.join(', ') || 'none'}

Scope:
- Include: 加载 solution plan、代码实现、测试运行、git commit
- Exclude: issue 创建、方案修改、队列变更

Deliverables:
输出严格遵循以下格式：
\`\`\`json
{
  "issue_id": "${entry.issue_id}",
  "status": "success" | "failed",
  "files_changed": ["path/to/file", ...],
  "tests_passed": true | false,
  "committed": true | false,
  "commit_hash": "abc123" | null,
  "error": null | "错误描述",
  "summary": "实现摘要"
}
\`\`\`

Quality bar:
- solution plan 中的所有任务必须实现
- 现有测试不能 break
- 遵循项目编码规范
- 每个变更必须 commit
`
    })
  )
  allAgentIds.push(...waveExecutors)

  // ─── Check if more waves needed ───
  if (waveData.status === 'all_planned') {
    // No more waves — wait for current executors and finish
    const execResults = wait({ ids: waveExecutors, timeout_ms: 1200000 })
    waveExecutors.forEach((id, i) => {
      executorResults.push({
        wave: waveNum,
        issue: waveData.queue[i].issue_id,
        result: execResults.status[id]?.completed || 'timeout'
      })
    })
    break
  }

  // ─── Request next wave from planner (while executors run) ───
  send_input({
    id: plannerId,
    message: `
## WAVE ${waveNum} 已派发

已为 Wave ${waveNum} 创建 ${waveExecutors.length} 个 executor agents。

## NEXT
请继续规划下一波 (Wave ${waveNum + 1})。
剩余 issues: ${JSON.stringify(waveData.remaining_issues)}

输出格式同前。如果所有 issues 已规划完毕，status 设为 "all_planned"。
`
  })

  // ─── Wait for both: executors (current wave) + planner (next wave) ───
  const allWaiting = [...waveExecutors, plannerId]
  const batchResult = wait({ ids: allWaiting, timeout_ms: 1200000 })

  // Collect executor results
  waveExecutors.forEach((id, i) => {
    executorResults.push({
      wave: waveNum,
      issue: waveData.queue[i].issue_id,
      result: batchResult.status[id]?.completed || 'timeout'
    })
  })

  // Parse next wave from planner
  if (batchResult.status[plannerId]?.completed) {
    waveData = parseWaveOutput(batchResult.status[plannerId].completed)
  } else {
    // Planner timed out — wait more
    const plannerRetry = wait({ ids: [plannerId], timeout_ms: 300000 })
    if (plannerRetry.timed_out) {
      // Abort pipeline
      break
    }
    waveData = parseWaveOutput(plannerRetry.status[plannerId].completed)
  }
}
```

### Phase 4: Aggregation & Cleanup

```javascript
// ─── Aggregate results ───
const succeeded = executorResults.filter(r => {
  try {
    const parsed = JSON.parse(r.result)
    return parsed.status === 'success'
  } catch { return false }
})

const failed = executorResults.filter(r => {
  try {
    const parsed = JSON.parse(r.result)
    return parsed.status === 'failed'
  } catch { return true }
})

// ─── Output final report ───
const report = `
## PlanEx Pipeline Complete

**Waves**: ${waveNum}
**Total Issues**: ${executorResults.length}
**Succeeded**: ${succeeded.length}
**Failed**: ${failed.length}

### Results by Wave
${executorResults.map(r => `- Wave ${r.wave} | ${r.issue} | ${(() => {
  try { return JSON.parse(r.result).status } catch { return 'error' }
})()}`).join('\n')}

${failed.length > 0 ? `### Failed Issues
${failed.map(r => `- ${r.issue}: ${(() => {
  try { return JSON.parse(r.result).error } catch { return r.result.slice(0, 200) }
})()}`).join('\n')}` : ''}
`

console.log(report)

// ─── Lifecycle cleanup ───
allAgentIds.forEach(id => {
  try { close_agent({ id }) } catch { /* already closed */ }
})
```

## Helper Functions

```javascript
function parseWaveOutput(output) {
  // Extract JSON block from agent output
  const jsonMatch = output.match(/```json\s*([\s\S]*?)```/)
  if (jsonMatch) {
    try { return JSON.parse(jsonMatch[1]) } catch {}
  }
  // Fallback: try parsing entire output as JSON
  try { return JSON.parse(output) } catch {}
  // Last resort: return empty wave with all_planned
  return { wave: 0, status: 'all_planned', queue: [], remaining_issues: [], summary: 'Parse failed' }
}
```

## Configuration

```javascript
const CONFIG = {
  sessionDir: ".workflow/.team/PEX-{slug}-{date}/",
  issueDataDir: ".workflow/issues/",
  maxWaveSize: 5,
  plannerTimeout: 900000,   // 15 min
  executorTimeout: 1200000, // 20 min
  maxWaves: 10
}
```

## Lifecycle Management

### Timeout Handling

| Scenario | Action |
|----------|--------|
| Planner wave timeout | send_input 催促收敛，retry wait 120s |
| Executor timeout | 标记为 failed，继续其他 executor |
| Batch wait partial timeout | 收集已完成结果，继续 pipeline |
| Pipeline stall (> 2 waves timeout) | 中止 pipeline，输出部分结果 |

### Cleanup Protocol

```javascript
// All agents tracked in allAgentIds
// Final cleanup at end or on error
allAgentIds.forEach(id => {
  try { close_agent({ id }) } catch { /* already closed */ }
})
```

## Error Handling

| Scenario | Resolution |
|----------|------------|
| Planner output parse failure | Retry with send_input asking for strict JSON |
| No issues created | Report error, abort pipeline |
| Solution planning failure | Skip issue, report in final results |
| Executor implementation failure | Mark as failed, continue with other executors |
| All executors in wave fail | Report wave failure, continue to next wave |
| Planner exits early | Treat as all_planned, finish current wave |
