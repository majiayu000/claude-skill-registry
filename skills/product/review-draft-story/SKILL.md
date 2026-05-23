---
name: review-draft-story
description: Comprehensive draft story review with parallel specialist sub-agents. Spawns PM, UX, and SM agents to review stories from product, design, and implementation readiness perspectives before development begins.
---

# /review-draft-story - Draft Story Review

## Description

Full-spectrum story review using parallel specialist sub-agents BEFORE implementation begins. Each specialist reviews from their domain perspective, findings are aggregated, and a final readiness decision is produced.

**Key Features:**
- Parallel specialist sub-agents (PM, UX, SM/Checklist)
- Product requirements completeness validation
- UX/UI specification review
- Implementation readiness assessment
- Consolidated feedback and recommendations
- GO/NO-GO decision with actionable fixes

## Usage

```bash
# Review a specific story
/review-draft-story 2002

# Review a story by file path
/review-draft-story docs/stories/epic-6-wishlist/wish-2002-add-item-flow.md

# Quick review (skip deep analysis)
/review-draft-story 2002 --quick

# Focus on specific aspect
/review-draft-story 2002 --focus=ux

# Skip PM review (no product context available)
/review-draft-story 2002 --skip-pm
```

## Parameters

- **story** - Story number (e.g., `2002`) or full path to story file
- **--quick** - Run lightweight review, skip deep specialists
- **--focus** - Focus on specific aspect: `pm`, `ux`, or `sm`
- **--skip-pm** - Skip PM review if no PRD/epic context
- **--skip-ux** - Skip UX review if no UI in this story

---

## EXECUTION INSTRUCTIONS

**CRITICAL: Use Task tool to spawn parallel sub-agents. Use TodoWrite to track progress.**

---

## Context Optimization Strategy

**To minimize context consumption:**

1. **Don't load epic/architecture content into parent** - only get file paths
2. **Pass file paths to sub-agents** - let them read files directly
3. **Use concise YAML output** - only report issues, not all sections
4. **SM checklist: reference file** - don't duplicate all items in prompt
5. **Use Haiku for sub-agents** - faster and cheaper

**Impact:** Reduces parent context by 60-80% for stories with large epic/architecture docs.

---

## Phase 0: Initialize & Gather Context

```
TodoWrite([
  { content: "Gather story context", status: "in_progress", activeForm: "Gathering context" },
  { content: "Spawn specialist sub-agents", status: "pending", activeForm: "Spawning specialists" },
  { content: "Collect specialist feedback", status: "pending", activeForm: "Collecting feedback" },
  { content: "Aggregate findings", status: "pending", activeForm: "Aggregating findings" },
  { content: "Generate review report", status: "pending", activeForm: "Generating report" }
])
```

**Gather context:**
1. Load `.bmad-core/core-config.yaml` for story locations and patterns
2. Locate the story file path:
   - If number provided: Search in `docs/stories/` for matching file
   - If path provided: Use directly
3. Read story file and extract:
   - Title and description
   - Acceptance criteria
   - Tasks/subtasks
   - Dev Notes section
   - Testing section
   - Referenced files/architecture paths (just paths, not content)
4. Get parent epic FILE PATH if referenced (don't read content)
5. Get architecture doc FILE PATHS if referenced (don't read content)
6. Determine if story has UI components (affects UX review)

**OPTIMIZATION: Don't load epic/architecture content into parent context - pass file paths to sub-agents**

**Skip Logic:**
- Skip UX review if story has no UI components (API-only, backend, migrations)
- Skip PM review if `--skip-pm` or no epic/PRD context available

---

## Phase 1: Spawn Specialist Sub-Agents

**CRITICAL: Spawn all applicable specialists in parallel using run_in_background: true**

### 1.1 Product Manager (PM) Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "PM story review",
  run_in_background: true,
  prompt: "You are John, an experienced Product Manager reviewing a story draft.

           Story file path: {STORY_FILE_PATH}
           Epic file path: {EPIC_FILE_PATH or 'Not provided'}

           IMPORTANT: Read the story file. If epic path provided, read it for context.

           Review the story from a PRODUCT perspective:

           1. **Requirements Clarity**
              - Are requirements clearly defined and unambiguous?
              - Is the 'why' (business value) clearly articulated?
              - Are success metrics or outcomes defined?

           2. **Scope Appropriateness**
              - Is the scope right-sized for a single story?
              - Are there scope creep risks?
              - Should this be split into multiple stories?

           3. **User Value**
              - Is user value clearly identified?
              - Does the story solve a real user problem?
              - Is the user persona/context clear?

           4. **Acceptance Criteria Quality**
              - Are ACs testable and measurable?
              - Do ACs cover happy path AND edge cases?
              - Are ACs written from user perspective (not technical)?

           5. **Dependencies & Sequencing**
              - Are dependencies clearly identified?
              - Is this story properly sequenced in the epic?
              - Are there hidden dependencies?

           6. **Risk Identification**
              - Are potential risks called out?
              - Are there business/compliance considerations?
              - Is there fallback behavior defined?

           Output format (ONLY include sections with issues):
           ```yaml
           pm_review:
             overall_assessment: READY|NEEDS_WORK|BLOCKED
             confidence: high|medium|low

             issues:
               - category: requirements_clarity|scope|user_value|acceptance_criteria|dependencies|risks
                 severity: blocking|should_fix|note
                 issue: 'Clear description'
                 suggestion: 'How to fix'

             summary: 'Brief 1-2 sentence assessment'
           ```

           NOTE: Only list actual issues. Omit categories with no concerns."
)
```

### 1.2 UX Expert Specialist

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "UX story review",
  run_in_background: true,
  prompt: "You are Sally, an experienced UX Expert reviewing a story draft.

           Story file path: {STORY_FILE_PATH}
           Architecture file paths: {ARCHITECTURE_FILE_PATHS or 'Not provided'}

           IMPORTANT: Read the story file. If architecture paths provided, read them for context.

           Review the story from a UX/UI perspective:

           1. **User Flow Clarity**
              - Is the user journey clearly described?
              - Are entry/exit points defined?
              - Is the happy path obvious?

           2. **Interaction Design**
              - Are user interactions specified?
              - Are click/tap targets and gestures defined?
              - Is feedback for user actions specified?

           3. **Visual Specifications**
              - Are layout requirements clear?
              - Is component placement described?
              - Are spacing/sizing considerations mentioned?

           4. **State Handling**
              - Are loading states defined?
              - Are error states and messages specified?
              - Are empty states considered?
              - Is disabled state behavior clear?

           5. **Accessibility Considerations**
              - Are a11y requirements mentioned?
              - Is keyboard navigation considered?
              - Are screen reader needs addressed?

           6. **Responsive Design**
              - Are mobile/tablet considerations mentioned?
              - Are breakpoint behaviors defined?
              - Is touch vs mouse interaction considered?

           7. **Component Reusability**
              - Can existing components be reused?
              - Are new components clearly specified?
              - Is design system alignment mentioned?

           Output format (ONLY include sections with issues):
           ```yaml
           ux_review:
             overall_assessment: READY|NEEDS_WORK|BLOCKED
             confidence: high|medium|low
             ui_complexity: low|medium|high

             issues:
               - category: user_flow|interaction|visual|states|accessibility|responsive|components
                 severity: blocking|should_fix|note
                 issue: 'Clear description'
                 suggestion: 'How to fix'

             summary: 'Brief 1-2 sentence assessment'
           ```

           NOTE: Only list actual issues. Omit categories with no concerns."
)
```

### 1.3 Scrum Master / Implementation Readiness Specialist

**This sub-agent executes the formal Story Draft Checklist (.bmad-core/checklists/story-draft-checklist.md)**

```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "SM checklist review",
  run_in_background: true,
  prompt: "You are Bob, a Scrum Master executing the Story Draft Checklist.

           Story file path: {STORY_FILE_PATH}
           Checklist file path: .bmad-core/checklists/story-draft-checklist.md

           IMPORTANT:
           1. Read the story file
           2. Read the checklist file
           3. Execute each checklist item systematically
           4. For each item, mark: [x] PASS, [~] PARTIAL, [ ] FAIL
           5. Identify blocking vs should_fix vs note issues

           Output format (ONLY include actual issues):
           ```yaml
           sm_review:
             overall_assessment: READY|NEEDS_REVISION|BLOCKED
             clarity_score: 1-10
             could_implement: true|false

             issues:
               - category: goal_clarity|technical_guidance|references|self_containment|testing
                 severity: blocking|should_fix|note
                 issue: 'Clear description of what''s missing or unclear'
                 suggestion: 'How to fix'

             developer_questions:
               - 'Question a dev would have'

             summary: 'Brief 1-2 sentence assessment from dev perspective'
           ```

           NOTE: Only list actual issues. If everything passes, issues array should be empty."
)
```

---

## Phase 2: Collect Results

**Wait for all specialists to complete:**

```
results = {
  pm: TaskOutput(task_id: "{pm_id}", block: true),
  ux: TaskOutput(task_id: "{ux_id}", block: true),
  sm: TaskOutput(task_id: "{sm_id}", block: true)
}
```

---

## Phase 3: Synthesize Concerns

**Parent orchestrator extracts and synthesizes all sub-agent findings into a unified concerns list:**

```yaml
concerns:
  - id: 1
    source: pm|ux|sm
    severity: blocking|should_fix|note
    category: requirements|scope|ux|technical|testing|etc
    concern: "Clear description of the issue"
    suggestion: "How to address it"
```

**Severity Levels:**
- **blocking**: Must fix before story can proceed
- **should_fix**: Important issue that should be addressed
- **note**: Minor observation, nice-to-have improvement

**Synthesis Rules (MUCH SIMPLER NOW):**
1. Parse YAML output from each sub-agent
2. Concatenate all `issues` arrays from PM, UX, and SM
3. Add sequential IDs and source labels
4. Sort by severity (blocking → should_fix → note)
5. Deduplicate if needed (keep highest severity)

**Example:**
```python
all_issues = pm_review.issues + ux_review.issues + sm_review.issues
concerns = [
  {id: i+1, source: issue.source, **issue}
  for i, issue in enumerate(sorted(all_issues, key=lambda x: severity_rank[x.severity]))
]
```

---

## Phase 4: Decision & Action

**Decision Logic:**

```python
blocking_count = len([c for c in concerns if c.severity == 'blocking'])
should_fix_count = len([c for c in concerns if c.severity == 'should_fix'])

if blocking_count > 0:
    decision = 'FAIL'
    action = 'APPEND_CONCERNS_TO_STORY'
elif should_fix_count > 0:
    decision = 'CONCERNS'
    action = 'APPEND_CONCERNS_TO_STORY'
else:
    decision = 'PASS'
    action = 'APPROVE_STORY'  # or MERGE_PR if post-implementation
```

---

### Path A: FAIL or CONCERNS → Append to Story

**Append concerns section to story file:**

```markdown
## Review Concerns

> **Review Date:** {ISO-8601}
> **Reviewed By:** PM (John), UX (Sally), SM (Bob)
> **Decision:** {FAIL|CONCERNS}

### Blocking Issues

- **[1] PM - requirements:** User value not clearly articulated
  - *Suggestion:* Add explicit user benefit statement to story description

- **[2] SM - testing:** No test scenarios defined for error cases
  - *Suggestion:* Add error handling test cases to Testing section

### Should-Fix Issues

- **[3] UX - states:** Loading state not specified
  - *Suggestion:* Define skeleton/spinner behavior during data fetch

### Notes

- **[4] PM - scope:** Consider splitting into two stories if complexity grows

---
```

**Update story status:**
```yaml
# In story frontmatter or status field:
status: Draft → Needs Revision  # if FAIL
status: Draft → Conditional     # if CONCERNS (can proceed with awareness)
```

---

### Path B: PASS (No Concerns) → Auto-Approve/Merge

**When all sub-agents return zero blocking or should_fix concerns:**

#### For Draft Story Review (pre-implementation):

1. **Update story status to Approved:**
   ```yaml
   status: Draft → Approved
   ```

2. **Add approval stamp to story:**
   ```markdown
   ## Review Approval

   > **Review Date:** {ISO-8601}
   > **Reviewed By:** PM (John), UX (Sally), SM (Bob)
   > **Decision:** APPROVED

   All review criteria passed. Story is ready for implementation.

   ---
   ```

3. **Report success and next step:**
   ```
   ✓ APPROVED - Ready for /implement {story_id}
   ```

#### For PR Review (post-implementation):

1. **Merge the PR:**
   ```bash
   gh pr merge {PR_NUMBER} --squash --delete-branch
   ```

2. **Update story status to Done:**
   ```yaml
   status: In Review → Done
   ```

3. **Archive the story:**
   ```bash
   mv docs/stories/{epic}/{story}.md docs/_archive/completed-stories/
   ```

4. **Close associated GitHub issue (if any):**
   ```bash
   gh issue close {ISSUE_NUMBER} --comment "Completed and merged in PR #{PR_NUMBER}"
   ```

---

## Phase 5: Report to User

```
════════════════════════════════════════════════════════════════════
  Story Review: {STORY_ID} - {STORY_TITLE}
════════════════════════════════════════════════════════════════════

SPECIALIST RESULTS
──────────────────────────────────────────────────────────────────────
  PM (John):      {PASS|CONCERNS} - {1-line summary}
  UX (Sally):     {PASS|CONCERNS|SKIPPED} - {1-line summary}
  SM (Bob):       {PASS|CONCERNS} - {1-line summary}

──────────────────────────────────────────────────────────────────────
  DECISION:       {PASS|CONCERNS|FAIL}
  CONCERNS:       {N} total ({blocking} blocking, {should_fix} should-fix)
──────────────────────────────────────────────────────────────────────

{If concerns > 0:}
CONCERNS LIST
  1. [{severity}] {source}: {concern}
     → {suggestion}
  2. ...

ACTION TAKEN
  {If PASS - draft:}    Story approved. Status: Draft → Approved
  {If PASS - PR:}       PR #{N} merged. Story archived. Status: Done
  {If CONCERNS/FAIL:}   Concerns appended to story. Status: Needs Revision

NEXT STEPS
  {If PASS:}            → /implement {story_id}
  {If CONCERNS/FAIL:}   → Address concerns, then re-run /review-draft-story

════════════════════════════════════════════════════════════════════
```

---

## Sub-Agent Architecture

```
Main Orchestrator (/review-draft-story)
    │
    ├─▶ Phase 0: Context Gathering (inline)
    │   ├── Load story file
    │   ├── Load epic context (if available)
    │   ├── Detect if PR exists (post-impl review)
    │   └── Determine applicable reviews (skip UX for API-only, etc.)
    │
    ├─▶ Phase 1: Specialist Sub-Agents (parallel, haiku, run_in_background)
    │   ├── PM (John) - product/requirements perspective
    │   ├── UX (Sally) - design/interaction perspective
    │   └── SM (Bob) - checklist execution
    │
    ├─▶ Phase 2: Collect Results (blocking wait for all)
    │
    ├─▶ Phase 3: Synthesize Concerns (inline)
    │   ├── Parse each sub-agent's YAML output
    │   ├── Extract issues as concerns
    │   ├── Deduplicate and sort by severity
    │   └── Build unified concerns list
    │
    ├─▶ Phase 4: Decision & Action (inline)
    │   ├── IF no concerns → PASS → approve/merge
    │   └── IF concerns → FAIL/CONCERNS → append to story
    │
    └─▶ Phase 5: Report (inline)
```

---

## Concern Categories

| Source | Categories |
|--------|------------|
| PM | requirements, scope, user_value, acceptance_criteria, dependencies, risks |
| UX | user_flow, interaction, visual, states, accessibility, responsive, components |
| SM | goal_clarity, technical_guidance, references, self_containment, testing, tasks |

---

## Usage Modes

### Draft Story Review (pre-implementation)
```bash
/review-draft-story 2002
```
- Reviews story before coding begins
- PASS → status becomes "Approved", ready for `/implement`
- CONCERNS/FAIL → concerns appended, status becomes "Needs Revision"

### PR Review (post-implementation)
```bash
/review-draft-story 2002 --pr
```
- Reviews story after implementation, with associated PR
- PASS → PR merged, story archived, status becomes "Done"
- CONCERNS/FAIL → concerns appended, PR remains open

### Quick Review
```bash
/review-draft-story 2002 --quick
```
- Lightweight review, skips deep analysis
- Good for simple stories or re-reviews after fixes

### Skip Specific Reviewers
```bash
/review-draft-story 2002 --skip-ux    # API-only story
/review-draft-story 2002 --skip-pm    # No PRD context available
```

---

## Integration with BMAD Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    BMAD Story Lifecycle                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. /sm *draft              Create story                        │
│         ↓                                                       │
│  2. /review-draft-story     ← THIS SKILL (pre-impl)             │
│         ↓                                                       │
│     ┌───┴───┐                                                   │
│   PASS    FAIL/CONCERNS                                         │
│     ↓         ↓                                                 │
│  Approved   Fix & Re-review                                     │
│     ↓                                                           │
│  3. /implement {story}      Code the story                      │
│         ↓                                                       │
│  4. /review-draft-story --pr  ← THIS SKILL (post-impl)          │
│         ↓                                                       │
│     ┌───┴───┐                                                   │
│   PASS    CONCERNS                                              │
│     ↓         ↓                                                 │
│  Merged    Fix & Re-review                                      │
│  & Done                                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
