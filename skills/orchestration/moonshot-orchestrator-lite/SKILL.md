---
name: moonshot-orchestrator-lite
description: PM workflow orchestrator (Lite). Lightweight version that runs all agents directly without fork.
---

# PM Orchestrator (Lite)

> **Note**: This version does not use fork subagents. All agents run directly in the current session.

## Role
Orchestrator that sequentially executes PM analysis skills and constructs the final agent chain.

## Input
Automatically collects the following:
- `userMessage`: User request
- `gitBranch`: Current branch
- `gitStatus`: Git status (clean/dirty)
- `recentCommits`: Recent commit list
- `openFiles`: Open file list

## Workflow

### 1. Initialize analysisContext
```yaml
schemaVersion: "1.0"
request:
  userMessage: "{userMessage}"
  taskType: unknown
  keywords: []
repo:
  gitBranch: "{gitBranch}"
  gitStatus: "{gitStatus}"
  openFiles: []
  changedFiles: []
signals:
  hasContextMd: false
  hasPendingQuestions: false
  requirementsClear: false
  implementationReady: false
  implementationComplete: false
  hasMockImplementation: false
  apiSpecConfirmed: false
  reactProject: false
estimates:
  estimatedFiles: 0
  estimatedLines: 0
  estimatedTime: unknown
phase: unknown
complexity: unknown
missingInfo: []
decisions:
  recommendedAgents: []
  skillChain: []
  parallelGroups: []
artifacts:
  tasksRoot: "{PROJECT.md:documentPaths.tasksRoot}"
  contextDocPath: "{tasksRoot}/{feature-name}/context.md"
  verificationScript: .claude/agents/verification/verify-changes.sh
tokenBudget:
  specSummaryTrigger: 2000
  splitTrigger: 5
  contextMaxTokens: 8000
  warningThreshold: 0.8
projectMemory:
  projectId: null
  loaded: false
  boundaries: null
  relevantRules: []
notes: []
```

### 2. Sequential PM Skill Execution

#### 2.0 Large Specification Handling

**2.0.1 Check Specification Size**
- Count words in `userMessage`
- Trigger summarization if > `tokenBudget.specSummaryTrigger` (2000 words)
- Trigger task splitting if independent features > `tokenBudget.splitTrigger` (5)

**2.0.2 Summarize Specification**
1. Save original to `{tasksRoot}/{feature-name}/archives/specification-full.md`
2. Extract core elements only
3. Write summary to `{tasksRoot}/{feature-name}/specification.md`

**2.0.3 Split into Subtasks**
If single spec covers multiple independent areas, split into `subtasks/` directory.

#### 2.0.4 Load Project Memory (Direct Execution)

**Determine Project ID**: `package.json` name → directory name → git remote

**Direct Execution** (no fork):
```
Task tool: project-memory-agent (subagent_type: general-purpose)
Input: { projectId, changedFiles, taskType, userRequest }
```

Agent searches project memory (`[ProjectID]::*`) and returns context:
```yaml
projectMemoryContext:
  projectId: "my-app"
  loaded: true
  boundaries:
    alwaysDo: [...]
    askFirst: [...]
    neverDo: [...]
  relevantRules: [...]
```

**Error Handling**:
- No memory: `loaded: false`, continue
- MCP unavailable: continue with warning

#### 2.1 Task Classification
Run `/moonshot-classify-task` using `Skill` tool

#### 2.2 Complexity Evaluation
Run `/moonshot-evaluate-complexity` using `Skill` tool

#### 2.3 Uncertainty Detection
Run `/moonshot-detect-uncertainty` using `Skill` tool

#### 2.4 Handle Uncertainties
If `missingInfo` is not empty, generate questions using `AskUserQuestion` tool.

#### 2.5 Sequence Decision
Run `/moonshot-decide-sequence` using `Skill` tool

### 3. Execute Agent Chain

Execute `decisions.skillChain` in order:

**Allowed Steps:**
- `pre-flight-check`: Pre-flight check skill
- `project-memory-agent`: Project memory load agent (Task tool, direct execution)
- `requirements-analyzer`: Requirements analysis agent (Task tool)
- `context-builder`: Context building agent (Task tool)
- `codex-validate-plan`: Codex plan validation skill
- `implementation-runner`: Implementation agent (Task tool)
- `completion-verifier`: Test-based completion verification skill
- `codex-review-code`: Codex code review skill
- `project-memory-reviewer`: Project memory rule/spec violation verification agent (Task tool, direct execution)
- `vercel-react-best-practices`: React/Next.js performance optimization review skill
- `security-reviewer`: Security vulnerability review skill
- `build-error-resolver`: Build/compile error resolution skill
- `verify-changes.sh`: Verification script (Bash tool)
- `efficiency-tracker`: Efficiency tracking skill
- `session-logger`: Session logging skill

**Execution Rules:**
1. Execute each step sequentially
2. Use `Skill` tool for skill steps
3. Use `Task` tool for agent steps (subagent_type mapping)
4. Use `Bash` tool for script steps
5. Parallel execution only within parallel groups
6. Request user confirmation for undefined steps
7. **All agents/skills must** follow `.claude/docs/guidelines/document-memory-policy.md`

**Agent Mapping:**
- `project-memory-agent` → `subagent_type: "general-purpose"` + prompt (direct execution)
- `requirements-analyzer` → `subagent_type: "general-purpose"` + prompt
- `context-builder` → `subagent_type: "context-builder"`
- `implementation-runner` → `subagent_type: "implementation-agent"`
- `project-memory-reviewer` → `subagent_type: "general-purpose"` + prompt (direct execution)

### 3.1 Dynamic Skill Injection

Inject skills dynamically when signals are detected during skillChain execution:

| Signal | Condition | Inserted Skill | Insertion Point |
|--------|-----------|----------------|-----------------|
| `buildFailed` | Bash exit code ≠ 0 | build-error-resolver | Before retry |
| `securityConcern` | Changed files contain `.env`, `auth`, `password`, `token` | security-reviewer | After codex-review-code |
| `reactProject` | `.tsx`/`.jsx` files or React keywords | vercel-react-best-practices | After codex-review-code |

### 3.2 Project Memory Review (Direct Execution)

After `codex-review-code`, **directly execute** `project-memory-reviewer`:

```
Task tool: project-memory-reviewer (subagent_type: general-purpose)
Input: { projectId, changedFiles, projectMemoryContext, diff }
```

**Receive Violation Report:**
```yaml
memoryReviewResult:
  status: "passed" | "failed" | "needs_approval"
  violations: [...]     # NeverDo violations
  needsApproval: [...]  # AskFirst items
  warnings: [...]       # Convention/spec warnings
  reminders: [...]      # AlwaysDo reminders
```

**Result Handling:**
- `status: "failed"`: **Stop** execution, report violations to user
- `status: "needs_approval"`: Request user approval before proceeding
- `status: "passed"`: Proceed to next step

### 3.3 Completion Verification Loop

After implementation-runner completes, call `completion-verifier`.
Retry up to retryCount < 2 if `allPassed: false`.

### 4. Record Results
Save final analysisContext to `.claude/docs/moonshot-analysis.yaml`.

## Output Format

### Summary for User (Markdown)
```markdown
## PM Analysis Results

**Task Type**: {taskType}
**Complexity**: {complexity}
**Phase**: {phase}

### Execution Chain
1. {step1}
2. {step2}
...

### Estimates
- Files: {estimatedFiles}
- Lines: {estimatedLines}
- Estimated Time: {estimatedTime}
```

## Error Handling

1. **Skill execution failure**: Log error to notes and report to user
2. **Undefined step**: Request user confirmation
3. **Question infinite loop**: Max 3 questions limit
4. **Token limit warning**: Archive and summarize before continuing

## Contract
- This skill only orchestrates other PM skills, does not analyze directly
- All analysis logic delegated to individual PM skills
- **Does not use fork** - all agents run directly in current session
- **Document memory policy**: Follow `.claude/docs/guidelines/document-memory-policy.md`

## References
- `.claude/docs/guidelines/document-memory-policy.md`
