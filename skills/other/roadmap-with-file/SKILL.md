---
name: roadmap-with-file
description: Strategic requirement roadmap with iterative decomposition and issue creation. Outputs roadmap.md (human-readable, single source) + issues.jsonl (machine-executable). Handoff to csv-wave-pipeline.
argument-hint: "[-y|--yes] [-c|--continue] [-m progressive|direct|auto] \"requirement description\""
---

## Auto Mode

When `--yes` or `-y`: Auto-confirm strategy selection, use recommended mode, skip interactive rounds.

# Roadmap-with-file Skill

## Usage

```bash
$roadmap-with-file "Implement user authentication system with OAuth and 2FA"
$roadmap-with-file -m progressive "Build real-time notification system"
$roadmap-with-file -m direct "Refactor payment module"
$roadmap-with-file -m auto "Add data export feature"
$roadmap-with-file --continue "auth system"
$roadmap-with-file -y "Implement caching layer"
```

**Flags**:
- `-y, --yes`: Skip all confirmations (auto mode)
- `-c, --continue`: Continue existing session
- `-m, --mode`: Strategy selection (progressive / direct / auto)

**Context Source**: cli-explore-agent (optional) + requirement analysis
**Output Directory**: `.workflow/.roadmap/{session-id}/`
**Core Output**: `roadmap.md` (single source, human-readable) + `issues.jsonl` (global, machine-executable)

---

## Subagent API Reference

### spawn_agent
Create a new subagent with task assignment.

```javascript
const agentId = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/{agent-type}.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

## TASK CONTEXT
${taskContext}

## DELIVERABLES
${deliverables}
`
})
```

### wait
Get results from subagent (only way to retrieve results).

```javascript
const result = wait({
  ids: [agentId],
  timeout_ms: 600000  // 10 minutes
})

if (result.timed_out) {
  // Handle timeout - can continue waiting or send_input to prompt completion
}
```

### send_input
Continue interaction with active subagent (for clarification or follow-up).

```javascript
send_input({
  id: agentId,
  message: `
## CLARIFICATION ANSWERS
${answers}

## NEXT STEP
Continue with plan generation.
`
})
```

### close_agent
Clean up subagent resources (irreversible).

```javascript
close_agent({ id: agentId })
```

---

## Output Artifacts

### Single Source of Truth

| Artifact | Purpose | Consumer |
|----------|---------|----------|
| `roadmap.md` | ⭐ Human-readable strategic roadmap with all context | Human review, csv-wave-pipeline handoff |
| `.workflow/issues/issues.jsonl` | Global issue store (appended) | csv-wave-pipeline, issue commands |

### Why No Separate JSON Files?

| Original File | Why Removed | Where Content Goes |
|---------------|-------------|-------------------|
| `strategy-assessment.json` | Duplicates roadmap.md content | Embedded in `roadmap.md` Strategy Assessment section |
| `exploration-codebase.json` | Single-use intermediate | Embedded in `roadmap.md` Codebase Context appendix |

---

## Overview

Strategic requirement roadmap with **iterative decomposition**. Creates a single `roadmap.md` that evolves through discussion, with issues persisted to global `issues.jsonl` for execution.

**Core workflow**: Understand → Decompose → Iterate → Validate → Handoff

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ROADMAP ITERATIVE WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase 1: Requirement Understanding & Strategy                           │
│     ├─ Parse requirement: goal / constraints / stakeholders              │
│     ├─ Assess uncertainty level → recommend mode                         │
│     ├─ User confirms strategy (-m skips, -y auto-selects)                │
│     └─ Initialize roadmap.md with Strategy Assessment                    │
│                                                                          │
│  Phase 2: Decomposition & Issue Creation                                 │
│     ├─ cli-roadmap-plan-agent executes decomposition                     │
│     ├─ Progressive: 2-4 layers (MVP→Optimized) with convergence          │
│     ├─ Direct: Topological task sequence with convergence                │
│     ├─ Create issues via ccw issue create → issues.jsonl                 │
│     └─ Update roadmap.md with Roadmap table + Issue references           │
│                                                                          │
│  Phase 3: Iterative Refinement (Multi-Round)                             │
│     ├─ Present roadmap to user                                           │
│     ├─ Feedback: Approve | Adjust Scope | Modify Convergence | Replan    │
│     ├─ Update roadmap.md with each round                                 │
│     └─ Repeat until approved (max 5 rounds)                              │
│                                                                          │
│  Phase 4: Handoff                                                        │
│     ├─ Final roadmap.md with Issue ID references                         │
│     ├─ Options: csv-wave-pipeline | view issues | done                   │
│     └─ Issues ready in .workflow/issues/issues.jsonl                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Dual Modes

| Mode | Strategy | Best For | Decomposition |
|------|----------|----------|---------------|
| **Progressive** | MVP → Usable → Refined → Optimized | High uncertainty, need validation | 2-4 layers, each with full convergence |
| **Direct** | Topological task sequence | Clear requirements, confirmed tech | Tasks with explicit inputs/outputs |

**Auto-selection logic**:
- ≥3 high uncertainty factors → Progressive
- ≥3 low uncertainty factors → Direct
- Otherwise → Ask user preference

---

## Output Structure

```
.workflow/.roadmap/RMAP-{slug}-{date}/
└── roadmap.md                  # ⭐ Single source of truth
                                #   - Strategy Assessment (embedded)
                                #   - Roadmap Table
                                #   - Convergence Criteria per Issue
                                #   - Codebase Context (appendix, if applicable)
                                #   - Iteration History

.workflow/issues/issues.jsonl   # Global issue store (appended)
                                #   - One JSON object per line
                                #   - Consumed by csv-wave-pipeline, issue commands
```

---

## roadmap.md Template

```markdown
# Requirement Roadmap

**Session**: RMAP-{slug}-{date}
**Requirement**: {requirement}
**Strategy**: {progressive|direct}
**Status**: {Planning|Refining|Ready}
**Created**: {timestamp}

---

## Strategy Assessment

- **Uncertainty Level**: {high|medium|low}
- **Decomposition Mode**: {progressive|direct}
- **Assessment Basis**: {factors summary}
- **Goal**: {extracted goal}
- **Constraints**: {extracted constraints}
- **Stakeholders**: {extracted stakeholders}

---

## Roadmap

### Progressive Mode
| Wave | Issue ID | Layer | Goal | Priority | Dependencies |
|------|----------|-------|------|----------|--------------|
| 1 | ISS-xxx | MVP | ... | 2 | - |
| 2 | ISS-yyy | Usable | ... | 3 | ISS-xxx |

### Direct Mode
| Wave | Issue ID | Title | Type | Dependencies |
|------|----------|-------|------|--------------|
| 1 | ISS-xxx | ... | infrastructure | - |
| 2 | ISS-yyy | ... | feature | ISS-xxx |

---

## Convergence Criteria

### ISS-xxx: {Issue Title}
- **Criteria**: [testable conditions]
- **Verification**: [executable steps/commands]
- **Definition of Done**: [business language, non-technical]

### ISS-yyy: {Issue Title}
...

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| ... | ... | ... |

---

## Iteration History

### Round 1 - {timestamp}
**User Feedback**: {feedback summary}
**Changes Made**: {adjustments}
**Status**: {approved|continue iteration}

---

## Codebase Context (Optional)

*Included when codebase exploration was performed*

- **Relevant Modules**: [...]
- **Existing Patterns**: [...]
- **Integration Points**: [...]
```

---

## Issues JSONL Specification

### Location & Format

```
Path: .workflow/issues/issues.jsonl
Format: JSONL (one complete JSON object per line)
Encoding: UTF-8
Mode: Append-only (new issues appended to end)
```

### Record Schema

```json
{
  "id": "ISS-YYYYMMDD-NNN",
  "title": "[LayerName] goal or [TaskType] title",
  "status": "pending",
  "priority": 2,
  "context": "Markdown with goal, scope, convergence, verification, DoD",
  "source": "text",
  "tags": ["roadmap", "progressive|direct", "wave-N", "layer-name"],
  "extended_context": {
    "notes": {
      "session": "RMAP-{slug}-{date}",
      "strategy": "progressive|direct",
      "wave": 1,
      "depends_on_issues": []
    }
  },
  "lifecycle_requirements": {
    "test_strategy": "unit",
    "regression_scope": "affected",
    "acceptance_type": "automated",
    "commit_strategy": "per-issue"
  }
}
```

### Query Interface

```bash
# By ID (detail view)
ccw issue list ISS-20260227-001

# List all with status filter
ccw issue list --status planned,queued
ccw issue list --brief  # JSON minimal output

# Queue operations (wave-based execution)
ccw issue queue list              # List all queues
ccw issue queue dag               # Get dependency graph (JSON)
ccw issue next --queue <queue-id> # Get next task

# Execute
ccw issue queue add <issue-id>    # Add to active queue
ccw issue done <item-id>          # Mark completed
```

> **Note**: Issues are tagged with `wave-N` in `tags[]` field for filtering. Use `--brief` for programmatic parsing.

---

## Implementation

### Session Initialization

```javascript
const getUtc8ISOString = () => new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString()

// Parse flags
const AUTO_YES = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
const continueMode = $ARGUMENTS.includes('--continue') || $ARGUMENTS.includes('-c')
const modeMatch = $ARGUMENTS.match(/(?:--mode|-m)\s+(progressive|direct|auto)/)
const requestedMode = modeMatch ? modeMatch[1] : 'auto'

// Clean requirement text (remove flags)
const requirement = $ARGUMENTS
  .replace(/--yes|-y|--continue|-c|--mode\s+\w+|-m\s+\w+/g, '')
  .trim()

const slug = requirement.toLowerCase()
  .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
  .substring(0, 40)
const dateStr = getUtc8ISOString().substring(0, 10)
const sessionId = `RMAP-${slug}-${dateStr}`
const sessionFolder = `.workflow/.roadmap/${sessionId}`

// Auto-detect continue mode
if (continueMode || file_exists(`${sessionFolder}/roadmap.md`)) {
  // Resume existing session
  const existingRoadmap = Read(`${sessionFolder}/roadmap.md`)
  // Extract current phase and continue from there
}

Bash(`mkdir -p ${sessionFolder}`)
```

---

### Phase 1: Requirement Understanding & Strategy

**Objective**: Parse requirement, assess uncertainty, select decomposition strategy, initialize roadmap.md.

**Steps**:

1. **Parse Requirement**
   - Extract: goal, constraints, stakeholders, keywords

2. **Assess Uncertainty**
   ```javascript
   const uncertaintyFactors = {
     scope_clarity: 'low|medium|high',
     technical_risk: 'low|medium|high',
     dependency_unknown: 'low|medium|high',
     domain_familiarity: 'low|medium|high',
     requirement_stability: 'low|medium|high'
   }

   // Calculate recommendation
   const highCount = Object.values(uncertaintyFactors).filter(v => v === 'high').length
   const lowCount = Object.values(uncertaintyFactors).filter(v => v === 'low').length

   let recommendedMode
   if (highCount >= 3) recommendedMode = 'progressive'
   else if (lowCount >= 3) recommendedMode = 'direct'
   else recommendedMode = 'progressive'  // default safer choice
   ```

3. **Strategy Selection** (skip if `-m` specified or AUTO_YES)
   ```javascript
   let selectedMode

   if (requestedMode !== 'auto') {
     selectedMode = requestedMode
   } else if (AUTO_YES) {
     selectedMode = recommendedMode
   } else {
     const answer = ASK_USER([
       {
         id: "strategy",
         type: "choice",
         prompt: `Decomposition strategy:\nUncertainty: ${uncertaintyLevel}\nRecommended: ${recommendedMode}`,
         options: [
           { value: "progressive", label: recommendedMode === 'progressive' ? "Progressive (Recommended)" : "Progressive" },
           { value: "direct", label: recommendedMode === 'direct' ? "Direct (Recommended)" : "Direct" }
         ],
         default: recommendedMode
       }
     ])  // BLOCKS (wait for user response)

     selectedMode = answer.strategy
   }
   ```

4. **Initialize roadmap.md**
   ```javascript
   const roadmapContent = `# Requirement Roadmap

**Session**: ${sessionId}
**Requirement**: ${requirement}
**Strategy**: ${selectedMode}
**Status**: Planning
**Created**: ${getUtc8ISOString()}

---

## Strategy Assessment

- **Uncertainty Level**: ${uncertaintyLevel}
- **Decomposition Mode**: ${selectedMode}
- **Assessment Basis**: ${factorsSummary}
- **Goal**: ${extractedGoal}
- **Constraints**: ${extractedConstraints}
- **Stakeholders**: ${extractedStakeholders}

---

## Roadmap

> To be populated after Phase 2 decomposition

---

## Convergence Criteria Details

> To be populated after Phase 2 decomposition

---

## Risks

> To be populated after Phase 2 decomposition

---

## Iteration History

> To be populated during Phase 3 refinement

---

## Codebase Context (Optional)

> To be populated if codebase exploration was performed
`

   Write(`${sessionFolder}/roadmap.md`, roadmapContent)
   ```

**Success Criteria**:
- roadmap.md created with Strategy Assessment
- Strategy selected (progressive or direct)
- Uncertainty factors documented

---

### Phase 2: Decomposition & Issue Creation

**Objective**: Execute decomposition via `cli-roadmap-plan-agent`, create issues, update roadmap.md.

**Steps**:

1. **Optional Codebase Exploration** (if codebase detected)
   ```javascript
   const hasCodebase = Bash(`
     test -f package.json && echo "nodejs" ||
     test -f go.mod && echo "golang" ||
     test -f Cargo.toml && echo "rust" ||
     test -f pyproject.toml && echo "python" ||
     test -d src && echo "generic" ||
     echo "none"
   `).trim()

   let codebaseContext = null

   if (hasCodebase !== 'none') {
     const exploreAgentId = spawn_agent({
       message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-explore-agent.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

## Exploration Context
- **Requirement**: ${requirement}
- **Strategy**: ${selectedMode}
- **Project Type**: ${hasCodebase}
- **Session**: ${sessionFolder}

## Exploration Focus
- Identify modules/components related to the requirement
- Find existing patterns that should be followed
- Locate integration points for new functionality
- Assess current architecture constraints

## Output
Return findings as JSON with schema:
{
  "project_type": "${hasCodebase}",
  "relevant_modules": [{name, path, relevance}],
  "existing_patterns": [{pattern, files, description}],
  "integration_points": [{location, description, risk}],
  "architecture_constraints": [string],
  "tech_stack": {languages, frameworks, tools}
}
`
     })

     const exploreResult = wait({
       ids: [exploreAgentId],
       timeout_ms: 120000
     })

     close_agent({ id: exploreAgentId })

     if (exploreResult.status[exploreAgentId].completed) {
       codebaseContext = exploreResult.status[exploreAgentId].completed
     }
   }
   ```

2. **Execute Decomposition Agent**
   ```javascript
   const decompositionAgentId = spawn_agent({
     message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/cli-roadmap-plan-agent.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

## Roadmap Decomposition Task

### Input Context
- **Requirement**: ${requirement}
- **Selected Mode**: ${selectedMode}
- **Session ID**: ${sessionId}
- **Session Folder**: ${sessionFolder}

### Strategy Assessment
${JSON.stringify(strategyAssessment, null, 2)}

### Codebase Context
${codebaseContext
  ? JSON.stringify(codebaseContext, null, 2)
  : 'No codebase detected - pure requirement decomposition'}

---

### Mode-Specific Requirements

${selectedMode === 'progressive' ? `**Progressive Mode**:
- 2-4 layers from MVP to full implementation
- Each layer: id (L0-L3), name, goal, scope, excludes, convergence, risks, effort, depends_on
- L0 (MVP) must be a self-contained closed loop with no dependencies
- Scope: each feature belongs to exactly ONE layer (no overlap)
- Layer names: MVP / Usable / Refined / Optimized` :

`**Direct Mode**:
- Topologically-sorted task sequence
- Each task: id (T1-Tn), title, type, scope, inputs, outputs, convergence, depends_on, parallel_group
- Inputs must come from preceding task outputs or existing resources
- Tasks in same parallel_group must be truly independent`}

---

### Convergence Quality Requirements
- criteria[]: MUST be testable (can write assertions or manual verification steps)
- verification: MUST be executable (command, script, or explicit steps)
- definition_of_done: MUST use business language (non-technical person can judge)

---

### Expected Output
1. **Update ${sessionFolder}/roadmap.md** with Roadmap table + Convergence sections
2. **Create issues via ccw issue create** - append to .workflow/issues/issues.jsonl

### Issue Format (for ccw issue create)
- id: ISS-YYYYMMDD-NNN (auto-generated)
- title: [LayerName] goal or [TaskType] title
- context: Markdown with goal, scope, convergence criteria, verification, DoD
- priority: small→4, medium→3, large→2
- tags: ["roadmap", mode, wave-N, layer-name]
- extended_context.notes: {session, strategy, wave, depends_on_issues}

### Execution Steps
1. Analyze requirement and build decomposition context
2. Execute decomposition (internal reasoning)
3. Validate records, check convergence quality
4. For each decomposed item:
   - Run: ccw issue create --title "..." --context "..." --tags "..." --priority N
   - Record returned Issue ID
5. Update roadmap.md with Issue ID references
6. Return brief completion summary with Issue IDs
`
   })

   const decompositionResult = wait({
     ids: [decompositionAgentId],
     timeout_ms: 300000  // 5 minutes for complex decomposition
   })

   close_agent({ id: decompositionAgentId })

   if (!decompositionResult.status[decompositionAgentId].completed) {
     throw new Error('Decomposition agent failed to complete')
   }

   const issueIds = decompositionResult.status[decompositionAgentId].completed.issueIds || []
   ```

**Success Criteria**:
- Issues created in `.workflow/issues/issues.jsonl`
- roadmap.md updated with Issue references
- No circular dependencies
- Convergence criteria testable

---

### Phase 3: Iterative Refinement

**Objective**: Multi-round user feedback to refine roadmap.

**Steps**:

1. **Display Current Roadmap**
   - Read and display Roadmap table + key Convergence criteria
   - Show issue count and wave breakdown

2. **Feedback Loop** (skip if AUTO_YES)
   ```javascript
   let round = 0
   let approved = false

   while (!approved && round < 5) {
     round++

     const feedback = ASK_USER([
       {
         id: "feedback",
         type: "choice",
         prompt: `Roadmap validation (round ${round}):\n${issueIds.length} issues across ${waveCount} waves. Feedback?`,
         options: [
           { value: "approve", label: "Approve", description: "Proceed to handoff" },
           { value: "scope", label: "Adjust Scope", description: "Modify issue scopes" },
           { value: "convergence", label: "Modify Convergence", description: "Refine criteria/verification" },
           { value: "replan", label: "Re-decompose", description: "Change strategy/layering" }
         ]
       }
     ])  // BLOCKS (wait for user response)

     if (feedback.feedback === 'approve') {
       approved = true
     } else {
       // CONSTRAINT: All modifications below ONLY touch roadmap.md and issues.jsonl
       // NEVER modify source code or project files during interactive rounds
       switch (feedback.feedback) {
         case 'scope':
           // Collect scope adjustments
           const scopeAdjustments = ASK_USER([
             { id: "adjustments", type: "text", prompt: "Describe scope adjustments needed:" }
           ])  // BLOCKS

           // Update ONLY roadmap.md Roadmap table + Convergence sections
           Edit({ path: `${sessionFolder}/roadmap.md`, /* scope changes */ })
           // Update ONLY issues.jsonl entries (scope/context fields)

           break

         case 'convergence':
           // Collect convergence refinements
           const convergenceRefinements = ASK_USER([
             { id: "refinements", type: "text", prompt: "Describe convergence refinements needed:" }
           ])  // BLOCKS

           // Update ONLY roadmap.md Convergence Criteria section
           Edit({ path: `${sessionFolder}/roadmap.md`, /* convergence changes */ })

           break

         case 'replan':
           // Return to Phase 2 with new strategy
           const newStrategy = ASK_USER([
             {
               id: "strategy",
               type: "choice",
               prompt: "Select new decomposition strategy:",
               options: [
                 { value: "progressive", label: "Progressive" },
                 { value: "direct", label: "Direct" }
               ]
             }
           ])  // BLOCKS

           selectedMode = newStrategy.strategy
           // Re-execute Phase 2 (updates roadmap.md + issues.jsonl only)
           break
       }

       // Update Iteration History in roadmap.md
       const iterationEntry = `
### Round ${round} - ${getUtc8ISOString()}
**User Feedback**: ${feedback.feedback}
**Changes Made**: ${changesMade}
**Status**: continue iteration
`
       Edit({
         path: `${sessionFolder}/roadmap.md`,
         old_string: "## Iteration History\n\n> To be populated during Phase 3 refinement",
         new_string: `## Iteration History\n${iterationEntry}`
       })
     }
   }
   ```

3. **Finalize Iteration History**
   ```javascript
   // Update final status in roadmap.md
   Edit({
     path: `${sessionFolder}/roadmap.md`,
     old_string: "**Status**: Planning",
     new_string: "**Status**: Ready"
   })
   ```

**Success Criteria**:
- User approved OR max rounds reached
- All changes recorded in Iteration History
- roadmap.md reflects final state

---

### Phase 4: Handoff

**Objective**: Present final roadmap, offer execution options.

**Steps**:

1. **Display Summary**
   ```markdown
   ## Roadmap Complete

   - **Session**: RMAP-{slug}-{date}
   - **Strategy**: {progressive|direct}
   - **Issues Created**: {count} across {waves} waves
   - **Roadmap**: .workflow/.roadmap/RMAP-{slug}-{date}/roadmap.md

   | Wave | Issue Count | Layer/Type |
   |------|-------------|------------|
   | 1 | 2 | MVP / infrastructure |
   | 2 | 3 | Usable / feature |
   ```

2. **Offer Options** (skip if AUTO_YES)
   ```javascript
   let nextStep

   if (AUTO_YES) {
     nextStep = "done"  // Default to done in auto mode
   } else {
     const answer = ASK_USER([
       {
         id: "next",
         type: "choice",
         prompt: `${issueIds.length} issues ready. Next step:`,
         options: [
           { value: "csv-wave", label: "Execute with csv-wave-pipeline (Recommended)", description: `Run all ${issueIds.length} issues via wave-based batch execution` },
           { value: "view", label: "View issues", description: "Display issue details" },
           { value: "done", label: "Done", description: "Save and exit" }
         ]
       }
     ])  // BLOCKS (wait for user response)

     nextStep = answer.next
   }
   ```

3. **Execute Selection**
   ```javascript
   switch (nextStep) {
     case 'csv-wave':
       // Launch csv-wave-pipeline for wave-based batch execution
       console.log(`\nTo execute, run:\n\n  $csv-wave-pipeline "${requirement}"\n`)
       break

     case 'view':
       // Display issues from issues.jsonl
       Bash(`ccw issue list --session ${sessionId}`)
       break

     case 'done':
       // Output paths and end
       console.log([
         `Roadmap saved: ${sessionFolder}/roadmap.md`,
         `Issues created: ${issueIds.length}`,
         '',
         'To execute later:',
         `  $csv-wave-pipeline "${requirement}"`,
         `  ccw issue list --session ${sessionId}`
       ].join('\n'))
       break
   }
   ```

**Success Criteria**:
- User selection executed
- Session complete
- All artifacts accessible

---

## Error Handling

| Error | Resolution |
|-------|------------|
| cli-explore-agent fails | Skip code exploration, proceed with pure requirement decomposition |
| cli-roadmap-plan-agent fails | Retry once, fallback to manual decomposition prompt |
| No codebase | Normal flow, skip exploration step |
| Circular dependency detected | Prompt user, re-decompose |
| User timeout in feedback loop | Save roadmap.md, show `--continue` command |
| Max rounds reached | Force proceed with current roadmap |
| Session folder conflict | Append timestamp suffix |

---

## Core Rules

1. **Start Immediately**: First action is session initialization, then Phase 1 execution
2. **Single Source**: All context embedded in roadmap.md, no separate JSON files
3. **Iterate on Roadmap**: Use feedback rounds to refine, not recreate
4. **Testable Convergence**: criteria = assertions, DoD = business language
5. **Explicit Lifecycle**: Always close_agent after wait completes to free resources
6. **DO NOT STOP**: Continuous workflow until handoff complete
7. **Plan-Only Modifications**: Interactive feedback (Phase 3) MUST only update `roadmap.md` and `issues.jsonl`. NEVER modify source code, configuration files, or any project files during interactive rounds. Code changes happen only after handoff (Phase 4) via `$csv-wave-pipeline` or other execution skills

---

## Best Practices

1. **Clear Requirements**: Detailed description → better decomposition
2. **Iterate on Roadmap**: Use feedback rounds to refine convergence criteria
3. **Testable Convergence**: criteria = assertions, DoD = business language
4. **Use Continue Mode**: Resume to iterate on existing roadmap
5. **Wave Execution**: Start with wave-1 (MVP) to validate before full execution

---

## Usage Recommendations

**When to Use Roadmap vs Other Skills:**

| Scenario | Recommended Skill |
|----------|------------------|
| Strategic planning, need issue tracking | `$roadmap-with-file` |
| Quick task breakdown, immediate execution | `$lite-plan` |
| Collaborative multi-agent planning | `$collaborative-plan-with-file` |
| Full specification documents | `$spec-generator` |
| Code implementation from existing plan | `$workflow-lite-plan` |

---

**Now execute roadmap-with-file for**: $ARGUMENTS
