---
name: workflow-multi-cli-plan
description: Multi-CLI collaborative planning with ACE context gathering, iterative cross-verification, and execution handoff
allowed-tools: Skill, Agent, AskUserQuestion, TodoWrite, Read, Write, Edit, Bash, Glob, Grep
---

# Multi-CLI Collaborative Planning

## Auto Mode

When `workflowPreferences.autoYes` is true: Auto-approve plan, use recommended solution and execution method (Agent, Skip review).

**Context Source**: ACE semantic search + Multi-CLI analysis
**Output Directory**: `.workflow/.multi-cli-plan/{session-id}/`
**Default Max Rounds**: 3 (convergence may complete earlier)
**CLI Tools**: @cli-discuss-agent (analysis), @cli-lite-planning-agent (plan generation)
**Execution**: Auto-hands off to workflow-lite-execute after plan approval

### Orchestrator Boundary (CRITICAL)

- **ONLY command** for multi-CLI collaborative planning
- Manages: Session state, user decisions, agent delegation, phase transitions
- Delegates: CLI execution to @cli-discuss-agent, plan generation to @cli-lite-planning-agent

### Execution Flow

```
Phase 1: Context Gathering
   └─ ACE semantic search, extract keywords, build context package

Phase 2: Multi-CLI Discussion (Iterative, via @cli-discuss-agent)
   ├─ Round N: Agent executes Gemini + Codex + Claude
   ├─ Cross-verify findings, synthesize solutions
   ├─ Write synthesis.json to rounds/{N}/
   └─ Loop until convergence or max rounds

Phase 3: Present Options
   └─ Display solutions with trade-offs from agent output

Phase 4: User Decision
   ├─ Select solution approach
   ├─ Select execution method (Agent/Codex/Auto)
   ├─ Select code review tool (Skip/Gemini/Codex/Agent)
   └─ Route:
      ├─ Approve → Phase 5
      ├─ Need More Analysis → Return to Phase 2
      └─ Cancel → Save session

Phase 5: Plan Generation & Execution Handoff
   ├─ Generate plan.json + .task/*.json (via @cli-lite-planning-agent, two-layer output)
   ├─ Build executionContext with user selections and taskFiles
   └─ Execute via workflow-lite-execute
```

### Agent Roles

| Agent | Responsibility |
|-------|---------------|
| **Orchestrator** | Session management, ACE context, user decisions, phase transitions, executionContext assembly |
| **@cli-discuss-agent** | Multi-CLI execution (Gemini/Codex/Claude), cross-verification, solution synthesis, synthesis.json output |
| **@cli-lite-planning-agent** | Task decomposition, two-layer output: plan.json (overview with task_ids[]) + .task/*.json (task files) |

## Core Responsibilities

### Phase 1: Context Gathering

**Session Initialization**:
```javascript
const sessionId = `MCP-${taskSlug}-${date}`
const sessionFolder = `.workflow/.multi-cli-plan/${sessionId}`
Bash(`mkdir -p ${sessionFolder}/rounds`)
```

**ACE Context Queries**:
```javascript
const aceQueries = [
  `Project architecture related to ${keywords}`,
  `Existing implementations of ${keywords[0]}`,
  `Code patterns for ${keywords} features`,
  `Integration points for ${keywords[0]}`
]
// Execute via mcp__ace-tool__search_context
```

**Context Package** (passed to agent):
- `relevant_files[]` - Files identified by ACE
- `detected_patterns[]` - Code patterns found
- `architecture_insights` - Structure understanding

### Phase 2: Agent Delegation

**Core Principle**: Orchestrator only delegates and reads output — NO direct CLI execution. CLI calls MUST use `Bash` with `run_in_background: true`, wait for hook callback, do NOT use `TaskOutput` polling.

**Agent Invocation**:
```javascript
Agent({
  subagent_type: "cli-discuss-agent",
  run_in_background: false,
  description: `Discussion round ${currentRound}`,
  prompt: `
## Input Context
- task_description: ${taskDescription}
- round_number: ${currentRound}
- session: { id: "${sessionId}", folder: "${sessionFolder}" }
- ace_context: ${JSON.stringify(contextPackage)}
- previous_rounds: ${JSON.stringify(analysisResults)}
- user_feedback: ${userFeedback || 'None'}
- cli_config: { tools: ["gemini", "codex"], mode: "parallel", fallback_chain: ["gemini", "codex", "claude"] }

## Execution Process
1. Parse input context (handle JSON strings)
2. Check if ACE supplementary search needed
3. Build CLI prompts with context
4. Execute CLIs (parallel or serial per cli_config.mode)
5. Parse CLI outputs, handle failures with fallback
6. Perform cross-verification between CLI results
7. Synthesize solutions, calculate scores
8. Calculate convergence, generate clarification questions
9. Write synthesis.json

## Output
Write: ${sessionFolder}/rounds/${currentRound}/synthesis.json

## Completion Checklist
- [ ] All configured CLI tools executed (or fallback triggered)
- [ ] Cross-verification completed with agreements/disagreements
- [ ] 2-3 solutions generated with file:line references
- [ ] Convergence score calculated (0.0-1.0)
- [ ] synthesis.json written with all Primary Fields
`
})
```

**Read Agent Output**:
```javascript
const synthesis = JSON.parse(Read(`${sessionFolder}/rounds/${round}/synthesis.json`))
// Access top-level fields: solutions, convergence, cross_verification, clarification_questions
```

**Convergence Decision**:
```javascript
if (synthesis.convergence.recommendation === 'converged') {
  // Proceed to Phase 3
} else if (synthesis.convergence.recommendation === 'user_input_needed') {
  // Collect user feedback, return to Phase 2
} else {
  // Continue to next round if new_insights && round < maxRounds
}
```

### Phase 3: Present Options

Display solutions from `synthesis.solutions[]` showing: name, source CLIs, effort/risk, pros/cons, affected files (`file:line`). Also show cross-verification agreements/disagreements count.

### Phase 4: User Decision

```javascript
AskUserQuestion({
  questions: [
    {
      question: "Which solution approach?",
      header: "Solution",
      multiSelect: false,
      options: solutions.map((s, i) => ({
        label: `Option ${i+1}: ${s.name}`,
        description: `${s.effort} effort, ${s.risk} risk`
      })).concat([
        { label: "Need More Analysis", description: "Return to Phase 2" }
      ])
    },
    {
      question: "Execution method:",
      header: "Execution",
      multiSelect: false,
      options: [
        { label: "Agent", description: "@code-developer agent" },
        { label: "Codex", description: "codex CLI tool" },
        { label: "Auto", description: "Auto-select based on complexity" }
      ]
    },
    {
      question: "Code review after execution?",
      header: "Review",
      multiSelect: false,
      options: [
        { label: "Skip", description: "No review" },
        { label: "Gemini Review", description: "Gemini CLI tool" },
        { label: "Codex Review", description: "codex review --uncommitted" },
        { label: "Agent Review", description: "Current agent review" }
      ]
    }
  ]
})
```

**Routing**:
- Approve + execution method → Phase 5
- Need More Analysis → Phase 2 with feedback
- Cancel → Save session for resumption

**TodoWrite Update (Phase 4 Decision)**:
```javascript
const executionLabel = userSelection.execution_method  // "Agent" / "Codex" / "Auto"

TodoWrite({ todos: [
  { content: "Phase 1: Context Gathering", status: "completed", activeForm: "Gathering context" },
  { content: "Phase 2: Multi-CLI Discussion", status: "completed", activeForm: "Running discussion" },
  { content: "Phase 3: Present Options", status: "completed", activeForm: "Presenting options" },
  { content: `Phase 4: User Decision [${executionLabel}]`, status: "completed", activeForm: "Decision recorded" },
  { content: `Phase 5: Plan Generation [${executionLabel}]`, status: "in_progress", activeForm: `Generating plan [${executionLabel}]` }
]})
```

### Phase 5: Plan Generation & Execution Handoff

**Step 1: Build Context-Package** (Orchestrator responsibility):
```javascript
const contextPackage = {
  solution: {
    name: selectedSolution.name,
    source_cli: selectedSolution.source_cli,
    feasibility: selectedSolution.feasibility,
    effort: selectedSolution.effort,
    risk: selectedSolution.risk,
    summary: selectedSolution.summary
  },
  implementation_plan: selectedSolution.implementation_plan,
  dependencies: selectedSolution.dependencies || { internal: [], external: [] },
  technical_concerns: selectedSolution.technical_concerns || [],
  consensus: {
    agreements: synthesis.cross_verification.agreements,
    resolved_conflicts: synthesis.cross_verification.resolution
  },
  constraints: userConstraints || [],
  task_description: taskDescription,
  session_id: sessionId
}
Write(`${sessionFolder}/context-package.json`, JSON.stringify(contextPackage, null, 2))
```

**Step 2: Invoke Planning Agent**:
```javascript
Agent({
  subagent_type: "cli-lite-planning-agent",
  run_in_background: false,
  description: "Generate implementation plan",
  prompt: `
## Schema Reference
Execute: cat ~/.ccw/workflows/cli-templates/schemas/plan-overview-base-schema.json
Execute: cat ~/.ccw/workflows/cli-templates/schemas/task-schema.json

## Output Format: Two-Layer Structure
- plan.json: Overview with task_ids[] referencing .task/ files (NO tasks[] array)
- .task/TASK-*.json: Independent task files following task-schema.json

plan.json required: summary, approach, task_ids, task_count, _metadata (with plan_type)
Task files required: id, title, description, depends_on, convergence (with criteria[])
Task fields: files[].change (not modification_points), convergence.criteria (not acceptance), test (not verification)

## Context-Package (from orchestrator)
${JSON.stringify(contextPackage, null, 2)}

## Execution Process
1. Read plan-overview-base-schema.json + task-schema.json for output structure
2. Read project-tech.json and specs/*.md
3. Parse context-package fields:
   - solution: name, feasibility, summary
   - implementation_plan: tasks[], execution_flow, milestones
   - dependencies: internal[], external[]
   - technical_concerns: risks/blockers
   - consensus: agreements, resolved_conflicts
   - constraints: user requirements
4. Use implementation_plan.tasks[] as task foundation
5. Preserve task dependencies (depends_on) and execution_flow
6. Expand tasks with convergence.criteria (testable completion conditions)
7. Create .task/ directory and write individual TASK-*.json files
8. Generate plan.json with task_ids[] referencing .task/ files

## Output
- ${sessionFolder}/plan.json (overview with task_ids[])
- ${sessionFolder}/.task/TASK-*.json (independent task files)

## Completion Checklist
- [ ] plan.json has task_ids[] and task_count (NO embedded tasks[])
- [ ] .task/*.json files preserve task dependencies from implementation_plan
- [ ] Task execution order follows execution_flow
- [ ] Key_points reflected in task descriptions
- [ ] User constraints applied to implementation
- [ ] convergence.criteria are testable
- [ ] plan.json follows plan-overview-base-schema.json
- [ ] Task files follow task-schema.json
`
})
```

**Step 3: Build executionContext**:
```javascript
const plan = JSON.parse(Read(`${sessionFolder}/plan.json`))
const taskFiles = plan.task_ids.map(id => `${sessionFolder}/.task/${id}.json`)

// Build executionContext (same structure as lite-plan)
executionContext = {
  planObject: plan,
  taskFiles: taskFiles,                              // Paths to .task/*.json files (two-layer format)
  explorationsContext: null,                          // Multi-CLI doesn't use exploration files
  explorationAngles: [],
  explorationManifest: null,
  clarificationContext: null,                         // Store user feedback from Phase 2 if exists
  executionMethod: userSelection.execution_method,    // From Phase 4
  codeReviewTool: userSelection.code_review_tool,     // From Phase 4
  originalUserInput: taskDescription,
  executorAssignments: null,
  session: {
    id: sessionId,
    folder: sessionFolder,
    artifacts: {
      explorations: [],                              // No explorations in multi-CLI workflow
      explorations_manifest: null,
      plan: `${sessionFolder}/plan.json`,
      task_dir: plan.task_ids ? `${sessionFolder}/.task/` : null,
      synthesis_rounds: Array.from({length: currentRound}, (_, i) =>
        `${sessionFolder}/rounds/${i+1}/synthesis.json`
      ),
      context_package: `${sessionFolder}/context-package.json`
    }
  }
}
```

**Step 4: Hand off to Execution**:
```javascript
Skill({
  skill: "workflow-lite-execute",
  args: "--in-memory"
})
// executionContext is passed via global variable to workflow-lite-execute (Mode 1: In-Memory Plan)
```

## synthesis.json Schema

```json
{
  "round": 1,
  "solutions": [{
    "name": "Solution Name",
    "source_cli": ["gemini", "codex"],
    "feasibility": 0.85,
    "effort": "low|medium|high",
    "risk": "low|medium|high",
    "summary": "Brief analysis summary",
    "implementation_plan": {
      "approach": "High-level technical approach",
      "tasks": [
        {"id": "T1", "name": "Task", "depends_on": [], "files": [], "key_point": "..."}
      ],
      "execution_flow": "T1 → T2 → T3",
      "milestones": ["Checkpoint 1", "Checkpoint 2"]
    },
    "dependencies": {"internal": [], "external": []},
    "technical_concerns": ["Risk 1", "Blocker 2"]
  }],
  "convergence": {
    "score": 0.85,
    "new_insights": false,
    "recommendation": "converged|continue|user_input_needed"
  },
  "cross_verification": {
    "agreements": [],
    "disagreements": [],
    "resolution": "..."
  },
  "clarification_questions": []
}
```

## TodoWrite Pattern

**Initialization** (Phase 1 start):
```javascript
TodoWrite({ todos: [
  { content: "Phase 1: Context Gathering", status: "in_progress", activeForm: "Gathering context" },
  { content: "Phase 2: Multi-CLI Discussion", status: "pending", activeForm: "Running discussion" },
  { content: "Phase 3: Present Options", status: "pending", activeForm: "Presenting options" },
  { content: "Phase 4: User Decision", status: "pending", activeForm: "Awaiting decision" },
  { content: "Phase 5: Plan Generation", status: "pending", activeForm: "Generating plan" }
]})
```

## Output File Structure

```
.workflow/.multi-cli-plan/{MCP-task-slug-YYYY-MM-DD}/
├── session-state.json          # Session tracking (orchestrator)
├── rounds/
│   ├── 1/synthesis.json        # Round 1 analysis (cli-discuss-agent)
│   ├── 2/synthesis.json        # Round 2 analysis (cli-discuss-agent)
│   └── .../
├── context-package.json        # Extracted context for planning (orchestrator)
├── plan.json                   # Plan overview with task_ids[] (NO embedded tasks[])
└── .task/                      # Independent task files
    ├── TASK-001.json            # Task file following task-schema.json
    ├── TASK-002.json
    └── ...
```

## Error Handling

| Error | Resolution |
|-------|------------|
| ACE search fails | Fall back to Glob/Grep for file discovery |
| Agent fails | Retry once, then present partial results |
| CLI timeout (in agent) | Agent uses fallback: gemini → codex → claude |
| No convergence | Present best options, flag uncertainty |
| synthesis.json parse error | Request agent retry |
| User cancels | Save session for later resumption |

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--max-rounds` | 3 | Maximum discussion rounds |
| `--tools` | gemini,codex | CLI tools for analysis |
| `--mode` | parallel | Execution mode: parallel or serial |
| `--auto-execute` | false | Auto-execute after approval |
