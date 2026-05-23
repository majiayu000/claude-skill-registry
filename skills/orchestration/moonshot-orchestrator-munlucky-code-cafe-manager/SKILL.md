---
name: moonshot-orchestrator
description: PM workflow orchestrator. Analyzes user requests and automatically runs the optimal agent chain.
---

# PM Orchestrator

## Role
Runs PM analysis skills in sequence and builds the final agent chain.

## Inputs
Automatically collect:
- `userMessage`: user request
- `gitBranch`: current branch
- `gitStatus`: Git status (clean/dirty)
- `recentCommits`: recent commit list
- `openFiles`: open file list

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
  tasksRoot: "{PROJECT.md:documentPaths.tasksRoot}"  # default: .claude/docs/tasks
  contextDocPath: "{tasksRoot}/{feature-name}/context.md"
  verificationScript: .claude/agents/verification/verify-changes.sh
tokenBudget:
  specSummaryTrigger: 2000     # words
  splitTrigger: 5              # independent features
  contextMaxTokens: 8000
  warningThreshold: 0.8
notes: []
```

### 2. Run PM skills sequentially

#### 2.0 Large specification handling

If the initial task specification (`request.userMessage`) is very long, it can cause the final plan or context document to exceed the output token limits. To prevent this, follow `.claude/docs/guidelines/document-memory-policy.md`:

**2.0.1 Check specification size**
- Count words in `userMessage`
- If > `tokenBudget.specSummaryTrigger` (2000 words): trigger summarization
- If independent features > `tokenBudget.splitTrigger` (5): trigger task splitting

**2.0.2 Summarize the specification**
1. Save the full original specification to `{tasksRoot}/{feature-name}/archives/specification-full.md`
2. Extract only:
   - Key requirements (max 5 items)
   - Constraints
   - Acceptance criteria
3. Write summarized version to `{tasksRoot}/{feature-name}/specification.md`
4. Reference the original in the summary

**2.0.3 Split into sub-tasks**
When a single specification covers multiple independent areas:
1. Create `subtasks/` directory
2. For each sub-task, create `subtasks/subtask-NN/` with its own `context.md`
3. Each sub-task runs this workflow independently with its own `analysisContext`
4. Master `context.md` contains only:
   - Sub-task list with links
   - Integration points
   - Shared constraints

**2.0.4 Limit context.md size**
- Only include summarized specification
- Keep current plan only (no history)
- Archive previous versions per document-memory-policy.md

#### 2.1 Task classification
Run `/moonshot-classify-task` using the Skill tool.
- Merge returned patch into analysisContext
- Example: add `request.taskType`, `request.keywords`, `notes`

#### 2.2 Complexity evaluation
Run `/moonshot-evaluate-complexity` using the Skill tool.
- Merge returned patch into analysisContext
- Example: update `complexity`, `estimates.*`

#### 2.3 Uncertainty detection
Run `/moonshot-detect-uncertainty` using the Skill tool.
- Merge returned patch into analysisContext
- Check `missingInfo` array

#### 2.4 Uncertainty handling
If `missingInfo` is not empty:
1. Create questions using the `AskUserQuestion` tool
   - Convert each item in `missingInfo` into a question
   - Prioritize HIGH items
2. Wait for user answers
3. Apply answers to analysisContext:
   - API answers -> `signals.apiSpecConfirmed = true`
   - Design spec answers -> store design file paths
   - Other answers -> record in `notes`
4. Set `signals.hasPendingQuestions = false`
5. Re-run `/moonshot-detect-uncertainty` if needed

If `missingInfo` is empty, proceed.

#### 2.5 Sequence decision
Run `/moonshot-decide-sequence` using the Skill tool.
- Merge returned patch into analysisContext
- Set `phase`, `decisions.skillChain`, `decisions.parallelGroups`

#### 2.6 Plan size guard (when iterating plan/review)
During plan→review→revise loops the `context.md` file can grow rapidly. Follow `.claude/docs/guidelines/document-memory-policy.md`:

1. **Before each plan update**: Check current token usage
2. **At 80% threshold**: Log warning to `notes`, consider summarizing
3. **At 100% threshold**:
   - Archive current version to `archives/context-v{n}.md`
   - Replace with summarized version
   - Update archive index in context.md

4. **Review output handling**:
   - Full review → `archives/review-v{n}.md`
   - Summary only → append to `context.md`

5. **Token limit approaching**: Further break down into smaller sub-plans

**Archive Index Format** (at bottom of context.md):
```markdown
## 아카이브 참조

| 버전 | 파일 | 핵심 내용 | 생성일 |
|------|------|----------|--------|
| v1 | [context-v1.md](archives/context-v1.md) | 초기 설계 | YYYY-MM-DD |
```

### 3. Execute the agent chain

Run `decisions.skillChain` in order:

**Allowed steps:**
- `pre-flight-check`: pre-flight skill
- `requirements-analyzer`: requirements analysis agent (Task tool)
- `context-builder`: context-building agent (Task tool)
- `codex-validate-plan`: Codex plan validation skill
- `implementation-runner`: implementation agent (Task tool)
- `completion-verifier`: test-based completion verification skill
- `codex-review-code`: Codex code review skill
- `security-reviewer`: security vulnerability review skill
- `build-error-resolver`: build/compile error resolution skill
- `verify-changes.sh`: verification script (Bash tool)
- `efficiency-tracker`: efficiency tracking skill
- `session-logger`: session logging skill

**Execution rules:**
1. Run steps sequentially
2. Use `Skill` tool for skill steps
3. Use `Task` tool for agent steps (map subagent_type)
4. Use `Bash` tool for scripts
5. If a parallel group exists, parallelize only within that group
6. If an undefined step appears, ask the user and stop
7. **All agents/skills must follow** `.claude/docs/guidelines/document-memory-policy.md`

**Agent mapping:**
- `requirements-analyzer` -> `subagent_type: "general-purpose"` + prompt
- `context-builder` -> `subagent_type: "context-builder"`
- `implementation-runner` -> `subagent_type: "implementation-agent"`

### 3.1 Dynamic Skill Injection

During skillChain execution, dynamically inject skills when signals detected:

| Signal | Condition | Inject Skill | Insert Position |
|--------|-----------|--------------|-----------------|
| `buildFailed` | Bash exit code ≠ 0 | build-error-resolver | Before retry current step |
| `securityConcern` | Changed files contain `.env`, `auth`, `password`, `token` | security-reviewer | After codex-review-code |
| `coverageLow` | Coverage < 80% from codex-test-integration output | (request additional tests) | After codex-test-integration |

**Signal Detection:**
```yaml
buildFailed:
  trigger: Bash tool returns non-zero exit code
  action: Insert build-error-resolver, then retry failed step (max 2)

securityConcern:
  trigger: |
    changedFiles.any(f => 
      f.includes('.env') || 
      f.includes('auth') || 
      f.includes('password') || 
      f.includes('token') ||
      f.includes('secret')
    )
  action: Add security-reviewer after codex-review-code

coverageLow:
  trigger: codex-test-integration reports coverage < 80%
  action: Log warning, request additional tests from user
```

### 3.2 Completion Verification Loop

After implementation-runner completes:

1. Call `completion-verifier`
2. If `allPassed: true`:
   - Mark `implementationComplete: true`
   - Proceed to next step (codex-review-code)
3. If `allPassed: false`:
   - Identify failed phase (Unit → Phase 1, Integration → Phase 2)
   - If retryCount < 2:
     - **Go back to failed Phase (not test writing)**
     - Pass `failedTests` to implementation-agent
     - Implementation-agent fixes code only
     - Increment retryCount
   - Else:
     - Ask user for intervention
     - Provide failed test details

**Signals Update:**
```yaml
signals:
  implementationComplete: false  # existing
  
  # New fields
  acceptanceTestsGenerated: false
  testsPassed: 0
  testsFailed: 0
  completionRetryCount: 0
  currentPhase: "Phase 0"  # 0=Tests, 1=Mock, 2=API, 3=Verify
```

### 4. Record results
Save final analysisContext to `.claude/docs/moonshot-analysis.yaml`.

## Output format

### Summary for the user (Markdown)
```markdown
## PM Analysis Result

**Task type**: {taskType}
**Complexity**: {complexity}
**Phase**: {phase}

### Execution chain
1. {step1}
2. {step2}
...

### Estimates
- File count: {estimatedFiles}
- Line count: {estimatedLines}
- Estimated time: {estimatedTime}

{Add questions section if missingInfo exists}
```

## Error handling

1. **Skill execution failure**: record error logs in notes and report to the user
2. **Undefined step**: ask the user for confirmation
3. **Question loop**: limit to 3 rounds, then proceed with defaults
4. **Token limit warning**: archive and summarize before continuing

## Contract
- This skill orchestrates other PM skills and does not analyze directly
- All analysis logic is delegated to individual PM skills
- Patch merging is a shallow object merge (no deep merge)
- User questions use the AskUserQuestion tool
- **Document memory policy**: Follow `.claude/docs/guidelines/document-memory-policy.md`

## References
- `.claude/docs/guidelines/document-memory-policy.md`
