---
name: feature
description: Execute a complete feature development workflow for wouterwisse.com using Opus subagents.
allowed-tools: Task, TodoWrite, TaskOutput
---

# Feature Skill - Orchestrator

**Orchestrator ONLY spawns Opus subagents and collects summaries. ALL work is delegated.**

## Critical Rules

1. **NEVER read files** - subagents read files
2. **NEVER run commands** - subagents run commands
3. **NEVER create commits** - subagents create commits
4. Orchestrator only: spawns agents, tracks todos, reports summaries
5. **Always use Opus model** for ALL Task agents (`model: "opus"`)

---

## Phase 0: Setup Subagent

Spawn a single subagent to understand the user story and set up branches:

```
Task(general-purpose, model: opus):

Parse user story and set up feature branch.

---

## Tasks

1. **Parse User Story**:
   - Extract title and description
   - Identify affected areas (pages, components, styling, scripts)
   - List acceptance criteria

2. **Validate Story**:
   - Is it implementable? (clear, specific, no conflicts)
   - What areas are affected?
   - Any new dependencies needed?

3. **Create Feature Branch**:
   ```bash
   git checkout main && git pull && git checkout -b feature/<name>
   ```

---

## Output Format

```yaml
---
STORY_VALID: true | false
QUESTIONS_IF_INVALID: []
USER_STORY:
  title: "[task name]"
  description: "[full description]"
  acceptance_criteria: [list]
AFFECTED_AREAS:
  - pages: [list of routes]
  - components: [list of components]
  - styles: [styling changes needed]
  - scripts: [generation scripts affected]
BRANCH_NAME: feature/<name>
---
```
```

**If STORY_VALID: false** → Ask user for clarification before proceeding.

---

## Phase 1: Research Subagents (Parallel)

Spawn parallel research subagents:

```
Task(Explore, model: opus, run_in_background: true):
Research existing patterns in src/app/ for [feature].

Find:
- Similar pages and their patterns
- Existing components that might be reused
- How similar features handle state, animations, loading

Output only the relevant findings as a summary.

---

Task(Explore, model: opus, run_in_background: true):
Research src/components/ for reusable UI components.

Find:
- Components matching the feature needs
- Common patterns for layout, interactions
- Tailwind CSS patterns used
- Framer Motion animation patterns

Output only the relevant findings as a summary.

---

Task(Explore, model: opus, run_in_background: true):
Research src/config/ and src/hooks/ for configuration and utilities.

Find:
- Relevant configuration files
- Custom hooks that might be useful
- Theme and styling patterns

Output only the relevant findings as a summary.
```

Wait for all research subagents with TaskOutput. Synthesize findings for planning.

---

## Phase 2: Planning Subagent

Spawn planning subagent with research results:

```
Task(Plan, model: opus):

Create implementation plan for user story.

---

## Context

USER_STORY: [from Phase 0]
RESEARCH_FINDINGS: [synthesis from Phase 1]
AFFECTED_AREAS: [list]

---

## Requirements

1. Write plan to: .claude/plans/<name>.plan.md
2. Order steps: config → components → pages → styling
3. Mark each step with tdd: true | false
4. Include dependencies between steps
5. Be specific about files to create/modify

---

## Output Format

```yaml
---
PLAN_FILE: .claude/plans/<name>.plan.md
STEPS_COUNT: X
STEP_SUMMARY:
  - id: config-1
    content: "Add configuration for new feature"
    tdd: false
  - id: component-1
    content: "Create FeatureCard component"
    tdd: false
  - id: page-1
    content: "Create feature page route"
    tdd: false
---
```
```

---

## Phase 3: Review Subagent

Spawn review subagent to validate plan:

```
Task(general-purpose, model: opus):

Review implementation plan for completeness and correctness.

---

## Tasks

1. Read: .claude/plans/<name>.plan.md

2. Validate:
   - Complete coverage of user story requirements
   - Correct order (config → components → pages)
   - Dependencies are accurate
   - TDD marking is correct (logic = true, UI = false)

3. If issues found: FIX THEM directly in the plan file

---

## Output Format

```yaml
---
REVIEW_RESULT: APPROVED | NEEDS_REVISION
CHANGES_MADE: [list of changes, if any]
---
```
```

---

## Phase 4: Implementation Subagents

Execute plan steps by invoking `/task` skill. Analyze dependencies for wave-based execution:

```
Wave 1: Steps with no dependencies (parallel)
Wave 2: Steps depending only on Wave 1 (parallel)
Wave 3: Steps depending on Wave 2 (parallel)
...
```

For EACH step, spawn subagent that invokes `/task`:

```
Task(general-purpose, model: opus):

Execute implementation step by invoking /task skill.

---

## Step Details

STEP_ID: [from plan]
CONTENT: [step description from plan]
TDD: [true | false from plan]

---

## Workflow

1. **Invoke the /task skill**:
   ```
   Skill(task)
   ```

   Pass these details to /task:
   - TASK: [CONTENT from step details]
   - Note: /task will handle TDD, quality checks, and commit

2. **After /task completes**, return the result.

---

## Output Format

```yaml
---
STEP_ID: [id]
STATUS: SUCCESS | FAILURE
COMMIT: [short hash from /task]
FILES_CHANGED: [list from /task]
BUILD: PASSED | FAILED
LINT: PASSED | FAILED
TESTS: PASSED | FAILED | SKIPPED
ERRORS: [if FAILURE]
---
```
```

**Spawn wave steps in parallel** (single message with multiple Task calls).
Wait for wave completion before starting next wave.

---

## Phase 5: Verification Subagents (Parallel)

Spawn parallel verification subagents:

```
Task(general-purpose, model: opus, run_in_background: true):

Verify code quality and patterns.

---

## Checks

1. TypeScript strict compliance:
   npx tsc --noEmit

2. Lint compliance:
   npm run lint

3. No forbidden patterns:
   grep -rn 'console.log\|TODO\|FIXME' --include='*.ts' --include='*.tsx' src/

---

## Output Format

```yaml
---
STATUS: PASSED | FAILED
VIOLATIONS: [list if any]
---
```

---

Task(general-purpose, model: opus, run_in_background: true):

Run full build.

---

## Commands

1. Build:
   npm run build

---

## Output Format

```yaml
---
STATUS: PASSED | FAILED
BUILD: PASSED | FAILED
FAILURES: [list of failed items if any]
---
```
```

**Both must pass before proceeding.**

---

## Phase 6: Completion Subagent

Spawn completion subagent:

```
Task(general-purpose, model: opus):

Finalize user story implementation.

---

## Context

BRANCH_NAME: [from Phase 0]
PLAN_FILE: .claude/plans/<name>.plan.md
USER_STORY_TITLE: [from Phase 0]

---

## Tasks

1. **Final validation**:
   - Build passes
   - No uncommitted changes
   - Quality checks pass

2. **Push feature branch**:
   ```bash
   git push -u origin [branch]
   ```

3. **Create PR**:
   ```bash
   gh pr create --base main --title "[title]" --body "## Summary
   [bullets from plan]

   ## Test Plan
   - [ ] Build passes
   - [ ] TypeScript strict mode passes
   - [ ] Lint passes
   - [ ] Manual testing: [steps]"
   ```

4. **DELETE plan file** (MANDATORY):
   ```bash
   rm -f .claude/plans/<name>.plan.md
   ```

---

## Output Format

```yaml
---
STATUS: COMPLETE
PR_URL: [url]
PLAN_DELETED: true
---
```
```

---

## Phase 7: Report to User

Summarize all results:

```markdown
## User Story Complete

**Story**: [title]

### Implementation
- Steps completed: X
- Commits: Y
- PR created: [url]

### Verification
- Build: PASSED
- TypeScript: PASSED
- Lint: PASSED

### Next Steps
1. Review the PR
2. Run `/fix-pr` to address review comments
3. Merge when ready
```

---

## Progress Tracking

Use TodoWrite throughout:

```yaml
todos:
  - content: "Parse story and setup branch"
    status: completed
  - content: "Research patterns"
    status: completed
  - content: "Create plan"
    status: completed
  - content: "Review plan"
    status: completed
  - content: "Execute config-1"
    status: completed
  - content: "Execute component-1"
    status: in_progress
  - content: "Execute page-1"
    status: pending
  - content: "Verify and create PR"
    status: pending
```

---

## Key Principles

1. **Orchestrator is minimal** - only spawns and collects
2. **Each step uses /task** - consistent implementation workflow
3. **Waves for parallelism** - independent steps run simultaneously
4. **Research informs planning** - patterns discovered before plan created
5. **Clean completion** - plan files deleted, PRs created
