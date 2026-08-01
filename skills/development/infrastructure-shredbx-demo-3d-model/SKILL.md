---
name: infrastructure-shredbx-demo-3d-model
description: 'Domain: infrastructure'
---

# User Story: US-001E - SDLC Orchestrator Skill (Coordinator Brain)

**Status:** READY
**Domain:** infrastructure
**Type:** feature
**Priority:** high
**Created:** 2025-11-07
**Estimated Complexity:** Large (5 days)

---

## Story

**As a** LLM (Claude Code) acting as coordinator
**I want** a single orchestrator skill that guides me through all SDLC workflow phases
**So that** I always follow the correct process (RESEARCH → PLANNING → IMPLEMENTATION → TESTING → VALIDATION) without missing critical steps

---

## Background

### Why is this needed?

We have built comprehensive SDLC infrastructure:
- `.sdlc-workflow/` (stories, tasks, templates, git workflow)
- `docs-stories` skill (CRUD for documentation)
- Planning quality gates (7 gates)
- Hooks (sdlc_guardian.py)
- Memory MCP integration
- Guidelines in CLAUDE.md

**But we lack a "conductor" skill that orchestrates the entire workflow.**

Currently, the coordinator (main Claude) must:
1. Remember which phase comes next
2. Remember which quality gates apply
3. Remember which subagents to spawn
4. Remember which artifacts to create
5. Remember what to validate before moving to next phase

**Result:** Inconsistent workflow execution, skipped steps, forgotten quality gates.

### What's the business value?

**Goal:** Ensure every user story follows the complete SDLC workflow consistently, regardless of LLM session.

**Benefits:**
- **Consistency:** Every story follows same rigorous process
- **Quality:** No skipped quality gates or validation steps
- **Efficiency:** LLM knows exactly what to do at each phase
- **Traceability:** Clear workflow state in task folders
- **Onboarding:** New LLM sessions pick up where previous left off
- **Reduced Errors:** Checklist-driven workflow prevents omissions

### SDLC Workflow Phases

From Memory MCP and CLAUDE.md:

```
RESEARCH → PLANNING → IMPLEMENTATION → TESTING → VALIDATION
```

**RESEARCH Phase:**
- Understand requirements
- Explore existing codebase
- Identify patterns to follow
- Document findings
- Output: findings-summary.md, analysis docs

**PLANNING Phase:**
- Design solution architecture
- Apply 7 quality gates (mandatory)
- Create implementation spec
- Create test plan
- Output: solution-architecture.md, implementation-spec.md, test-plan.md, quality-gate-checklist.md

**IMPLEMENTATION Phase:**
- Spawn specialized subagents (dev-backend-fastapi, dev-frontend-svelte, etc.)
- Subagents modify implementation files
- Coordinator saves reports
- Output: subagent-reports/, modified files

**TESTING Phase:**
- Run unit tests
- Run integration tests
- Run E2E tests (Playwright)
- Verify acceptance criteria
- Output: test-results/, coverage reports

**VALIDATION Phase:**
- Code review (qa-code-auditor)
- Performance check
- Security check
- Documentation check
- Output: validation-report.md, approval

### Current State

**Scattered Guidance:**
- CLAUDE.md has workflow description
- Memory MCP has workflow pattern
- planning-quality-gates skill has gates
- No single skill that guides through phases

**Problems:**
- LLM must piece together workflow from multiple sources
- Easy to skip quality gates
- Easy to forget validation steps
- No clear "state machine" for workflow progression
- No checklist for each phase

---

## Current Implementation

### What Exists Today

**SDLC Infrastructure:**
- ✅ Task folder structure with phase folders (research/, planning/, etc.)
- ✅ Planning quality gates skill
- ✅ docs-stories skill (CRUD for stories/tasks)
- ✅ Coordinator role enforcement (hooks)
- ✅ Memory MCP with patterns
- ✅ Sequential thinking requirement
- ✅ Slash commands (/task-research, /task-plan, /task-implement)

**What's Missing:**
- ❌ No orchestrator skill that guides coordinator through phases
- ❌ No phase transition checklist
- ❌ No workflow state validation
- ❌ No "what to do next" guidance
- ❌ No quality gate enforcement during planning
- ❌ No clear output requirements for each phase

---

## Proposed Solution

### Architecture

**Create `.claude/skills/sdlc-orchestrator/` skill**

**Purpose:** Guide coordinator through SDLC workflow phases with checklists, validation, and next-step guidance.

**Components:**

**1. SKILL.md** - Main orchestrator instructions
- YAML frontmatter (name, description, when to use)
- Overview of 5 phases
- **Phase-specific guidance:**
  - What to do in this phase
  - Required outputs
  - Quality checks before moving to next phase
  - Which subagents to spawn
  - Which skills to reference
- **Phase transition logic:**
  - Checklist for completing each phase
  - Validation before moving forward
  - How to update task STATE.json

**2. references/phase-checklists/** - Detailed checklists
- `research-checklist.md` - Research phase requirements
- `planning-checklist.md` - Planning phase requirements (includes 7 quality gates)
- `implementation-checklist.md` - Implementation phase requirements
- `testing-checklist.md` - Testing phase requirements
- `validation-checklist.md` - Validation phase requirements

**3. scripts/** (optional) - Automation helpers
- `phase_validator.py` - Validates phase completion
- `phase_transition.py` - Updates task state and moves to next phase

### Skill Structure

**`.claude/skills/sdlc-orchestrator/SKILL.md`**

```markdown
---
name: sdlc-orchestrator
description: Orchestrate SDLC workflow phases (RESEARCH → PLANNING → IMPLEMENTATION → TESTING → VALIDATION). Use when starting a new task or transitioning between phases to ensure correct workflow progression.
---

# SDLC Orchestrator Skill

## Purpose
Guide coordinator through all SDLC workflow phases with checklists, validation, and next-step guidance. Ensures consistent, rigorous execution of the workflow.

## When to Use This Skill
- Starting a new task (determine current phase)
- Completing a phase (validate and transition to next)
- Unsure what to do next (get phase-specific guidance)
- Need to verify phase completion (run checklist)

## Workflow State Machine

```
RESEARCH → PLANNING → IMPLEMENTATION → TESTING → VALIDATION → COMPLETED
```

## Phase 1: RESEARCH

### Objectives
- Understand requirements from user story
- Explore existing codebase for patterns
- Identify similar implementations
- Document findings

### Required Actions
1. Read user story acceptance criteria
2. Use research-git-patterns skill to find similar code
3. Explore codebase with Explore agent (if needed)
4. Document findings in task folder

### Required Outputs
- `research/findings-summary.md` - Key findings and patterns
- `research/existing-patterns.md` - Similar implementations found
- `research/dependencies.md` - External/internal dependencies

### Quality Checks
- [ ] All acceptance criteria understood
- [ ] Existing patterns documented
- [ ] Dependencies identified
- [ ] Findings summarized

### Next Phase: PLANNING

## Phase 2: PLANNING

### Objectives
- Design solution architecture
- Apply 7 planning quality gates
- Create implementation specification
- Create test plan

### Required Actions
1. Load Memory MCP entities (Planning Quality Gates, Network Resilience, etc.)
2. Use sequential thinking to design solution
3. Reference planning-quality-gates skill
4. Validate against official documentation (Svelte MCP if frontend)
5. Create comprehensive planning artifacts

### Required Outputs
- `planning/solution-architecture.md` - High-level design
- `planning/implementation-spec.md` - Detailed implementation steps
- `planning/test-plan.md` - Testing strategy
- `planning/quality-gate-checklist.md` - All 7 gates verified
- `planning/official-docs-validation.md` - Framework validation

### Quality Checks
- [ ] All 7 quality gates applied (mandatory: 1, 5, 6, 7; conditional: 2, 3, 4)
- [ ] Solution validated against official docs
- [ ] Implementation spec is actionable
- [ ] Test plan covers all acceptance criteria
- [ ] Trade-offs documented

### Next Phase: IMPLEMENTATION

## Phase 3: IMPLEMENTATION

### Objectives
- Spawn specialized subagents
- Implement solution per spec
- Document subagent work
- Update task progress

### Required Actions
1. Spawn appropriate subagents (dev-backend-fastapi, dev-frontend-svelte, etc.)
2. Provide subagents with implementation-spec.md
3. Save subagent reports to task folder
4. Update task STATE.json with files modified
5. Commit changes with proper references

### Required Outputs
- `subagent-reports/{subagent-name}-report.md` - Each subagent's work
- Modified implementation files
- Git commits with (US-XXX TASK-YYY-semantic-name) references

### Quality Checks
- [ ] All subagents completed successfully
- [ ] Reports saved to task folder
- [ ] Files committed with proper references
- [ ] No coordinator modifications to implementation files (hook enforces)

### Next Phase: TESTING

## Phase 4: TESTING

### Objectives
- Run all tests (unit, integration, E2E)
- Verify acceptance criteria
- Document test results

### Required Actions
1. Run unit tests (`make test-server`, `npm run test:unit`)
2. Run integration tests
3. Run E2E tests with Playwright
4. Verify each acceptance criterion
5. Document results

### Required Outputs
- `testing/test-results.md` - All test results
- `testing/acceptance-verification.md` - AC checklist
- `testing/coverage-report.md` - Coverage metrics

### Quality Checks
- [ ] All tests passing
- [ ] All acceptance criteria verified
- [ ] Coverage meets requirements
- [ ] No critical bugs

### Next Phase: VALIDATION

## Phase 5: VALIDATION

### Objectives
- Code review
- Performance check
- Security check
- Documentation check

### Required Actions
1. Spawn qa-code-auditor for code review
2. Check performance (if applicable)
3. Check security (no secrets, no vulnerabilities)
4. Verify documentation complete
5. Create validation report

### Required Outputs
- `validation/code-review.md` - QA audit report
- `validation/validation-summary.md` - Final checks

### Quality Checks
- [ ] Code review passed
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Ready for merge

### Next Phase: COMPLETED

## Phase Transition

To move to next phase:
1. Complete all required outputs for current phase
2. Pass all quality checks for current phase
3. Update task STATE.json: `phase: "NEXT_PHASE"`
4. Use docs-stories skill to update task state
5. Continue with next phase guidance

## Workflow Validation

Before transitioning, ask:
- Did I complete all required outputs?
- Did I pass all quality checks?
- Did I document decisions and trade-offs?
- Did I update task STATE.json?

If any answer is "no", complete missing work before proceeding.
```

---

## Acceptance Criteria

### Functional Requirements

- [ ] **AC-1:** Skill provides clear guidance for each of 5 SDLC phases (RESEARCH, PLANNING, IMPLEMENTATION, TESTING, VALIDATION)
- [ ] **AC-2:** Each phase section includes: objectives, required actions, required outputs, quality checks, next phase
- [ ] **AC-3:** Planning phase explicitly references all 7 planning quality gates
- [ ] **AC-4:** Implementation phase explicitly lists which subagents to spawn for which work
- [ ] **AC-5:** Phase transition logic includes validation checklist

### Technical Requirements

- [ ] **AC-6:** SKILL.md follows claude-skill-manager guidelines (YAML frontmatter, imperative voice, progressive disclosure)
- [ ] **AC-7:** Skill references existing skills (docs-stories, planning-quality-gates, research-git-patterns, frontend-svelte)
- [ ] **AC-8:** Skill references Memory MCP entities to load
- [ ] **AC-9:** Skill integrates with task STATE.json (phase field)
- [ ] **AC-10:** references/phase-checklists/ provide detailed checklists for each phase (optional but recommended)

### Quality Gates

- [ ] **AC-11:** Test orchestrator skill on US-001D implementation (use it to guide through phases)
- [ ] **AC-12:** Verify all 7 planning quality gates are mentioned in planning phase
- [ ] **AC-13:** Verify coordinator role boundaries are clear (spawn subagents, never implement directly)
- [ ] **AC-14:** Verify skill is discoverable (YAML frontmatter with good description)
- [ ] **AC-15:** Document skill in CLAUDE.md as part of SDLC infrastructure

### Integration Requirements

- [ ] **AC-16:** Skill works with slash commands (/task-research, /task-plan, /task-implement)
- [ ] **AC-17:** Skill references docs-stories for task state updates
- [ ] **AC-18:** Skill references planning-quality-gates for planning phase
- [ ] **AC-19:** Skill integrates with Memory MCP (load entities before planning)
- [ ] **AC-20:** Skill produces outputs that work with context indexer (US-001D)

---

## Technical Notes

### Technologies Used

- **Skill Format:** SKILL.md with YAML frontmatter (claude-skill-manager standard)
- **Integration:** Memory MCP, docs-stories skill, planning-quality-gates skill
- **State Management:** task STATE.json (phase field)
- **Validation:** Phase checklists in references/

### Integration Points

- **docs-stories skill:** Update task state, create artifacts
- **planning-quality-gates skill:** Apply gates during planning phase
- **research-git-patterns skill:** Find patterns during research phase
- **frontend-svelte skill:** If task involves Svelte (load patterns)
- **Memory MCP:** Load workflow patterns, quality gates, design patterns

### Skill Discovery

**When should Claude use this skill?**
- Starting a new task: "I'm starting TASK-001, what should I do?"
- Phase transition: "I've completed research, what's next?"
- Workflow confusion: "What phase am I in? What should I be doing?"
- Quality check: "Am I ready to move to implementation?"

**YAML description will trigger on:**
- "start task", "begin task"
- "next phase", "move to planning/implementation/testing/validation"
- "complete research/planning", "ready for implementation"
- "workflow", "SDLC process"

---

## Testing Strategy

### Manual Testing

- [ ] Test orchestrator on US-001D (context indexer implementation)
- [ ] Verify phase guidance is clear and actionable
- [ ] Verify checklists prevent skipping steps
- [ ] Verify phase transitions require validation

### Integration Testing

- [ ] Test with docs-stories skill (state updates work)
- [ ] Test with planning-quality-gates skill (all gates applied)
- [ ] Test with Memory MCP (entities load correctly)
- [ ] Test with slash commands (/task-research triggers research phase guidance)

---

## Documentation Requirements

### 1. SKILL.md

**Location:** `.claude/skills/sdlc-orchestrator/SKILL.md`

**Contents:**
- YAML frontmatter (name, description)
- Overview of workflow phases
- Detailed guidance for each phase
- Phase transition logic
- Quality checks

### 2. Phase Checklists (Optional)

**Location:** `.claude/skills/sdlc-orchestrator/references/phase-checklists/`

**Contents:**
- research-checklist.md
- planning-checklist.md (with 7 quality gates)
- implementation-checklist.md
- testing-checklist.md
- validation-checklist.md

### 3. Update CLAUDE.md

**Section:** SDLC Workflow

**Add:**
- Reference to sdlc-orchestrator skill
- Explain it's the "coordinator brain"
- Show example usage

---

## Dependencies

### Internal Dependencies

- **docs-stories skill:** (US-001D) - Must exist to update task state
- **planning-quality-gates skill:** Must exist for planning phase
- **Memory MCP entities:** Workflow patterns, quality gates
- **Task STATE.json:** Must have phase field

### Blocks

- None - this is a guidance skill, doesn't block anything

### Enables

- Consistent workflow execution across all stories
- Quality assurance (no skipped gates)
- Better coordination of complex multi-phase tasks

---

## Tasks Breakdown

This user story will be broken down into tasks:

1. **TASK-001-orchestrator-skill:** Create SKILL.md with phase guidance
2. **TASK-002-phase-checklists:** Create detailed checklists in references/
3. **TASK-003-integration-testing:** Test orchestrator on US-001D
4. **TASK-004-documentation:** Update CLAUDE.md and examples

[Tasks will be created after story is approved and planning is complete]

---

## Definition of Done

- [ ] All acceptance criteria met and verified
- [ ] SKILL.md created with comprehensive phase guidance
- [ ] Skill tested on real user story (US-001D)
- [ ] Phase transitions require validation
- [ ] All 7 quality gates referenced in planning phase
- [ ] Coordinator role boundaries clear
- [ ] Documentation complete (CLAUDE.md updated)
- [ ] Skill discoverable via YAML frontmatter

---

## Notes

### Design Decisions

**Why a separate orchestrator skill vs. extending docs-stories?**
- Separation of concerns: docs-stories = CRUD, orchestrator = workflow guidance
- Different triggers: docs-stories for "create story", orchestrator for "what phase am I in?"
- Progressive disclosure: Load orchestrator only when coordinating workflow
- Reusability: Other projects can use orchestrator without docs-stories

**Why references/phase-checklists/?**
- Keep SKILL.md lean (< 5k words)
- Load checklists only when needed
- Progressive disclosure (metadata → SKILL.md → checklists)

**Why integrate with STATE.json?**
- Single source of truth for task phase
- Enables resumability (new LLM session sees current phase)
- docs-stories can query and update state

### Future Improvements

- Automated phase validation scripts (phase_validator.py)
- Git hooks to validate phase artifacts exist
- Visual workflow diagram in skill
- Phase duration tracking and metrics

### References

- Memory MCP: SDLC Workflow Pattern entity
- CLAUDE.md: Coordinator vs Implementer roles
- planning-quality-gates skill: 7 quality gates
- docs-stories skill: Task state management

---

**Template Version:** 1.0
**Last Updated:** 2025-11-07
