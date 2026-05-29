# Journey to Tasks Skill

> Version: 1.0.0
> Compiler: manual
> Last Updated: 2026-01-26

Automate handoff from co-creative planning (journeys with Gherkin) to autonomous implementation (org-mode tasks with traceability).

## When to Activate

Use this skill when:
- Journey STATUS becomes 'ready'
- Spawning implementation tasks from journeys
- Automating planning-to-execution transition
- Creating tasks with traceability to requirements

## Methodology

**Chosen:** INVEST-based decomposition with lightweight traceability

**Rationale:** Research compared Definition of Ready, INVEST criteria, vertical slicing patterns, and traceability matrices. Key insights:

- INVEST criteria define well-formed tasks (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Vertical slices deliver observable user value by touching all layers
- Walking skeleton provides thinnest end-to-end slice for early integration
- Lightweight traceability (embedded annotations) beats heavy matrices
- Gherkin rules map to acceptance criteria; examples map to test cases

### Alternatives Considered

| Approach | Reason Not Selected | When Appropriate |
|----------|---------------------|------------------|
| Horizontal layer decomposition | Defers integration risk; layers don't provide user value | Shared infrastructure needed by multiple features |
| Full traceability matrix | High maintenance burden; becomes stale | Regulated industries requiring compliance |

## Core Principles

### 1. INVEST Criteria

Tasks should be Independent, Negotiable, Valuable, Estimable, Small, Testable.

| Criterion | Description |
|-----------|-------------|
| **I**ndependent | Can be completed without other tasks |
| **N**egotiable | Details can be discussed; not rigid |
| **V**aluable | Delivers observable value (vertical slice) |
| **E**stimable | Can estimate effort (1-4 hours typical) |
| **S**mall | Completable in one session |
| **T**estable | Has clear acceptance criteria from Gherkin |

### 2. Vertical Slice Over Horizontal Layer

Each task delivers end-to-end functionality across all layers.

*Horizontal layers defer integration; vertical slices surface issues early.*

**Test:** Can you demo this to a stakeholder when done?

### 3. Walking Skeleton First

First slice is the thinnest end-to-end path through all phases.

*Proves architecture works; enables parallel work; provides early feedback.*

**Test:** Does this touch all journey phases, even minimally?

### 4. Lightweight Traceability

Embed trace links in task properties rather than maintaining separate matrices.

**Task Properties:**
- `JOURNEY` - Links to source journey file
- `FEATURE` - Links to parent feature
- Acceptance criteria from Gherkin Then steps

### 5. Gherkin-to-Acceptance Mapping

| Gherkin Step | Task Aspect | Purpose |
|--------------|-------------|---------|
| **Given** | Preconditions | What must exist before task starts |
| **When** | Action/Scope | The behavior to implement |
| **Then** | Verification | Observable outcomes to confirm completion |

### 6. Rules Are Tasks, Examples Are Tests

Gherkin rules become task boundaries; examples become test cases.

*One task per distinct rule; multiple examples test the same implementation.*

**Test:** Does implementing this scenario require new code, or is it a test case for existing code?

---

## Workflow

**Outputs:** 
- Tasks in planning/projects.org with JOURNEY property
- Journey updated to STATUS 'implementing'

### Phase 1: Journey Validation

**Question:** Does this journey meet Definition of Ready?

Check journey STATUS property. If not 'ready' or 'scenarios-complete', STOP.

**Readiness checklist:**
- [ ] All phases have testable outcomes
- [ ] Pain points have measurable targets
- [ ] Scenarios cover happy path
- [ ] Scenarios cover key error cases
- [ ] First slice identified

This is a GATE - do not proceed without passing.

### Phase 2: Slice Identification

**Question:** What is the walking skeleton?

The walking skeleton:
- Touches all journey phases (end-to-end)
- Includes minimal functionality at each phase
- Is demonstrable to stakeholders
- Proves the architecture works

For each phase, identify ONE scenario from the happy path. This set becomes the walking skeleton.

**Example:**
- Phase 1: "Standard project recognized" (not all variations)
- Phase 2: "Deploy to production" (not all environments)
- Phase 3: "View status" (not detailed logs)

### Phase 3: Task Decomposition

**Question:** How do we break the slice into INVEST-compliant tasks?

For each scenario:
1. Extract the RULE being implemented
2. Identify scope from When step
3. Extract preconditions from Given steps
4. Extract acceptance criteria from Then steps

**If task is too large (>4 hours), split by:**
- Workflow steps (separate phases)
- Operations (CRUD)
- Data variations (one type first)
- Simple/complex (basic first)

**Task size target:** 1-4 hours each.

### Phase 4: Task Creation

**Question:** What properties should each task have?

Create org-mode heading with:

**Required properties:**
- `ID`: task-<journey-slug>-<n>
- `JOURNEY`: Link to source journey
- `FEATURE`: Link to parent feature

**Task content:**
- Heading: Action-oriented title from When step
- Acceptance criteria from Then steps (as checklist)

**Example:**
```org
** TODO Implement project structure detection
:PROPERTIES:
:ID:       task-first-deployment-1
:JOURNEY:  journey-first-deployment
:FEATURE:  feature-zero-config
:END:

*** Preconditions
- Standard project structures defined

*** Acceptance Criteria
- [ ] Tool reports successful recognition
- [ ] Clear error for unrecognized structures
```

### Phase 5: Dependency Mapping

**Question:** What dependencies exist between tasks?

Analyze relationships:
- Does task B require infrastructure from task A?
- Does task B's Given assume task A's Then?

Add `BLOCKER` property to blocked tasks. Prefer minimal dependencies.

### Phase 6: Journey Update

**Question:** How do we mark the journey as implementing?

Update journey file:
1. Set `STATUS` to 'implementing'
2. Update `UPDATED` timestamp
3. Add Implementation Tasks section with links

Add to Status Log: `[date] :: Transitioned to implementing, spawned N tasks`

### Phase 7: Handoff Summary

**Question:** What information does the human need?

Generate summary:
- Journey validated
- Walking skeleton scope
- Tasks created with estimates
- Dependencies mapped
- Recommended first task

This is for human review before execution begins.

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| Walking Skeleton First | Starting decomposition | One scenario per phase for thinnest slice | Early integration surfaces issues |
| Rule-to-Task Mapping | Multiple scenarios exist | One task per rule, not per example | Examples are test cases for same code |
| Precondition Extraction | Given has multiple steps | Combine into preconditions; check for dependencies | Reveals what must exist first |
| Split by Workflow | Task too large | One task per phase contribution | Phases are natural boundaries |
| Defer Complexity | Simple and complex variants | Simple case first; complex as follow-up | Validates approach before investing |
| Embedded Traceability | Creating tasks | Add JOURNEY/FEATURE properties | Annotations travel with tasks |

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Premature Handoff | Spawning tasks before journey is ready causes rework | Validate readiness as first phase; fail fast |
| Horizontal Slicing | Technical layers don't provide user value | Ensure each task is demonstrable vertical slice |
| Granularity Mismatch | Tasks too large (days) or too small (minutes) | Target 1-4 hours per task |
| Missing Traceability | Tasks without JOURNEY property lose context | Always set JOURNEY/FEATURE at creation |
| Over-Constrained Dependencies | Unnecessary dependencies serialize execution | Only add true technical/logical constraints |
| Example-per-Task | Creating task for each Gherkin example | One task per rule; examples are test cases |

---

## Quality Checklist

Before human confirmation:

- [ ] Journey STATUS was 'ready' before handoff
- [ ] Walking skeleton identified (one scenario per phase)
- [ ] Each task passes INVEST criteria
- [ ] Each task is 1-4 hours of work
- [ ] Each task has ID, JOURNEY, FEATURE properties
- [ ] Acceptance criteria derived from Gherkin Then steps
- [ ] Dependencies mapped where truly needed
- [ ] Journey STATUS updated to 'implementing'
- [ ] Implementation Tasks section populated
- [ ] Handoff summary generated for review

---

## Examples

### Complete Journey-to-Tasks Handoff

**Agent:** Let's spawn tasks from your "First Deployment" journey. First, I'll validate the journey is ready.

*[Agent reads journey file]*

**Agent:** Journey STATUS is 'ready'. Checking readiness criteria:
- [X] All phases have testable outcomes
- [X] Scenarios cover happy path
- [X] Scenarios cover key error cases
- [X] First slice identified

Validation passed. Identifying walking skeleton...

The journey has 4 phases. Walking skeleton (thinnest end-to-end):
1. "Standard project structure recognized"
2. "User deploys to production"
3. "System processes deployment successfully"
4. "User views deployment status"

Decomposing into tasks:

**Task 1: Implement project structure detection**

Preconditions (from Given):
- Standard project structures defined

Scope (from When):
- Developer adds deployment tool, tool analyzes structure

Acceptance (from Then):
- [ ] Tool reports successful recognition
- [ ] Clear feedback on detected structure

Estimate: ~2 hours (INVEST: small, testable)

**Task 2: Implement deployment trigger**

Preconditions:
- Project detected (depends on Task 1)

Acceptance:
- [ ] Deployment initiated on command
- [ ] Progress feedback shown

Estimate: ~3 hours
BLOCKER: task-first-deployment-1

**Task 3: Implement status verification**

Acceptance:
- [ ] Status shows deployment state
- [ ] Success/failure clearly indicated

Estimate: ~2 hours
BLOCKER: task-first-deployment-2

*[Agent creates tasks in projects.org and updates journey]*

**Handoff Summary:**

```
Journey Handoff: first-deployment
==================================

Walking Skeleton: 4 scenarios, 3 tasks

Tasks Created:
1. task-first-deployment-1: Project detection (~2h)
2. task-first-deployment-2: Deployment trigger (~3h) [blocked by 1]
3. task-first-deployment-3: Status verification (~2h) [blocked by 2]

Total Estimate: ~7 hours
Recommended Start: task-first-deployment-1
Journey STATUS: implementing
```

Please review and confirm before execution begins.

---

## References

- Bill Wake - INVEST in Good Stories: https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
- Jeff Patton - User Story Mapping
- Gojko Adzic - Specification by Example
- Mike Cohn - Agile Estimating and Planning
- BDD Practices - Example Mapping: https://cucumber.io/blog/bdd/example-mapping-introduction/

---

## Metadata

- **Domain:** planning-execution
- **Energy:** medium
- **Time Estimate:** 15-30 minutes per journey
- **Prerequisites:** Journey with STATUS 'ready'; planning/projects.org exists
- **Outputs:** Tasks in projects.org; journey updated to 'implementing'
- **Next Steps:** Execute tasks directly or delegate to beads
