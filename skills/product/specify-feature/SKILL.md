---
name: Specification Creation
description: Create technology-agnostic feature specifications using intelligence-first queries. Use when user describes what they want to build, mentions requirements, discusses user needs, or says "I want to create/build/implement" something. This skill enforces Article IV Specification-First Development.
degree-of-freedom: low
allowed-tools: Bash(fd:*), Bash(git:*), Bash(mkdir:*), Bash(project-intel.mjs:*), Read, Write, Edit, Grep
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/CoD_Σ.md
@.claude/shared-imports/memory-utils.md
@.claude/shared-imports/master-todo-utils.md
@.claude/templates/feature-spec.md
@.claude/templates/requirements-quality-checklist.md

# Specification Creation Skill

## Workflow Context

**SDD Phase**: Phase 3 (Feature Development Entry Point)
**Command**: `/feature`
**Prerequisites**: (optional) `memory/product.md` and `memory/constitution.md` for aligned features
**Creates**: `specs/$FEATURE/spec.md` (where $FEATURE = `NNN-feature-name`) + entry in `todos/master-todo.md`
**Predecessor**: Phase 2 - `/generate-constitution` → `memory/constitution.md`
**Successor**: Phase 4 - `/clarify` (if needed) OR Phase 5 - `/plan` → `plan.md`

### Phase Chain
```
Phase 1: /define-product → memory/product.md
Phase 2: /generate-constitution → memory/constitution.md
Phase 3: /feature → specs/$FEATURE/spec.md + todos/master-todo.md entry (YOU ARE HERE)
Phase 4: /clarify (if needed) → updated spec.md
Phase 5: /plan → plan.md + research.md + data-model.md
Phase 6: /tasks (auto) → tasks.md
Phase 7: /audit (auto) → audit-report.md
Phase 8: /implement → code + tests + verification
```

**$FEATURE format**: `NNN-feature-name` (e.g., `001-therapy-app`, `002-oauth-auth`)

### Automatic Workflow Progression

After creating spec.md, this skill automatically invokes `/plan` which chains through:
```
/plan → create-implementation-plan → generate-tasks → /audit → ready for /implement
```

---

## Overview

This skill creates technology-agnostic feature specifications following Article IV: Specification-First Development. It captures WHAT and WHY (user needs, requirements, success criteria) WITHOUT HOW (technical implementation, architecture, tech stack).

**Core Workflow**: Quality Gate → Intelligence Gathering → User Requirements → Specification → Automatic Planning

**Automatic Workflow Progression**: After creating spec.md, this skill automatically invokes /plan which chains through create-implementation-plan → generate-tasks → /audit → ready for /implement.

**Announce at start:** "I'm using the specify-feature skill to create a technology-agnostic specification."

---

## Quick Reference

| Phase | Key Activities | Output |
|-------|---------------|--------|
| **Phase 0** | Quality assessment (5 dimensions, 0-10 scale) | PROCEED/CLARIFY/BLOCK decision |
| **Phase 1** | Intelligence queries (auto-number, patterns, architecture) | Evidence for spec |
| **Phase 2** | Extract requirements (problem, stories, functional, success) | Technology-agnostic requirements |
| **Phase 3** | Generate specification (directory, branch, spec.md) | spec.md file |
| **Phase 4-5** | Report + automatic planning (invoke /plan) | Workflow to tasks.md + audit |

---

## Workflow Files

- **@.claude/skills/specify-feature/workflows/quality-assessment.md** - Phase 0: Quality gate with 5 dimensions
- **@.claude/skills/specify-feature/workflows/intelligence-gathering.md** - Phase 1: Intel-first context
- **@.claude/skills/specify-feature/workflows/user-requirements.md** - Phase 2: WHAT/WHY extraction
- **@.claude/skills/specify-feature/workflows/spec-generation.md** - Phase 3: Create spec.md
- **@.claude/skills/specify-feature/workflows/automation.md** - Phase 4-5: Reporting + automatic /plan

## Example & References

- **@.claude/skills/specify-feature/examples/feature-creation-example.md** - Complete walkthrough
- **@.claude/skills/specify-feature/references/specification-rules.md** - Best practices and anti-patterns

---

## Phase 0: Pre-Specification Quality Gate

**See:** @.claude/skills/specify-feature/workflows/quality-assessment.md

**Summary:**

Validate user input quality BEFORE creating specification using 5 quality dimensions (0-10 scale):

1. **Problem Clarity** - Clear problem statement, pain points, measurable impact
2. **Value Proposition** - Business/user value, quantified benefits, success metrics
3. **Requirements Completeness** - Key capabilities, scenarios, constraints
4. **Technology-Agnostic** - Zero technical details, pure WHAT/WHY focus
5. **User-Centric** - User needs central, personas, user value clear

**Thresholds**:
- **≥ 7.0**: PROCEED to Phase 1
- **5.0-6.9**: CLARIFY - Request specific improvements
- **< 5.0**: BLOCK - User description too vague

**Why This Matters**: Prevents wasting effort on vague or technically prescriptive inputs. Quality gate catches issues before specification creation.

---

## Phase 1: Intelligence-First Context Gathering

**See:** @.claude/skills/specify-feature/workflows/intelligence-gathering.md

**Summary:**

Query project intelligence BEFORE creating specification to discover existing patterns:

### Step 1.1: Auto-Number Next Feature
```bash
!`fd --type d --max-depth 1 '^[0-9]{3}-' specs/ 2>/dev/null | sort | tail -1`
```

### Step 1.2: Query Existing Patterns
```bash
!`project-intel.mjs --search "<user-keywords>" --type md --json > /tmp/spec_intel_patterns.json`
```

### Step 1.3: Understand Project Architecture
```bash
!`project-intel.mjs --overview --json > /tmp/spec_intel_overview.json`
```

**Token Efficiency**: 85% savings vs reading full spec files

**Why This Matters**: Intelligence evidence ensures specifications build on existing patterns rather than duplicating or conflicting with previous work.

---

## Phase 2: Extract User Requirements (WHAT/WHY Only)

**See:** @.claude/skills/specify-feature/workflows/user-requirements.md

**Summary:**

Extract technology-agnostic requirements focusing on WHAT and WHY, not HOW.

### Step 2.1: Problem Statement
- What problem are we solving and why?
- Who experiences this problem?
- Current situation and pain points

### Step 2.2: User Stories with Priorities
```markdown
## User Story <N> - [Title] (Priority: P1/P2/P3)

**As a** [user type]
**I want to** [capability]
**So that** [value/benefit]

**Why P1/P2/P3**: [Rationale for priority]
**Independent Test**: [How to validate this story works standalone]

**Acceptance Scenarios**:
1. **Given** [state], **When** [action], **Then** [outcome]
```

**Priority Levels**:
- **P1**: Must-have for MVP (core value)
- **P2**: Important but not blocking
- **P3**: Nice-to-have (deferred)

### Step 2.3: Functional Requirements
- Core capabilities (WHAT, not HOW)
- Data visibility and user interactions
- Constraints and boundaries

### Step 2.4: Success Criteria
- User-centric metrics (measurable outcomes)
- Business metrics
- Adoption metrics

**Why This Matters**: Technology-agnostic requirements survive implementation changes and enable better tech stack decisions in planning phase.

---

## Phase 3: Generate Specification with CoD^Σ Evidence

**See:** @.claude/skills/specify-feature/workflows/spec-generation.md

**Summary:**

Create specification document with intelligence evidence.

### Step 3.1: Create Feature Directory
```bash
NEXT_NUM=$(printf "%03d" $(($(fd --type d --max-depth 1 '^[0-9]{3}-' specs/ 2>/dev/null | wc -l) + 1)))
FEATURE_NAME="<derived-from-user-description>"
mkdir -p specs/$NEXT_NUM-$FEATURE_NAME
```

### Step 3.2: Create Git Branch
```bash
if git rev-parse --git-dir >/dev/null 2>&1; then
    git checkout -b "$NEXT_NUM-$FEATURE_NAME"
fi
```

### Step 3.3: Generate Specification Content
Use @.claude/templates/feature-spec.md with:
- YAML frontmatter (feature, created, status, priority)
- Problem statement, user stories, functional requirements, success criteria
- CoD^Σ Evidence Trace (intelligence queries, findings, assumptions, clarifications)
- Edge cases

### Step 3.4: Save Specification
```bash
Write specs/$NEXT_NUM-$FEATURE_NAME/spec.md
```

### Step 3.5: Register Feature in Master Todo
Add entry to `todos/master-todo.md` per @.claude/shared-imports/master-todo-utils.md:
```markdown
## Phase N: <Feature Name>
**Status**: ❌ TODO
**Spec**: `specs/$NEXT_NUM-$FEATURE_NAME/spec.md`
**Created**: YYYY-MM-DD

### Overview
<Brief description from spec.md Overview section>
```

**Why This Matters**: Evidence trace ensures all specifications have intelligence backing, not just assumptions.

---

## Phase 4-5: Reporting and Automatic Workflow Progression

**See:** @.claude/skills/specify-feature/workflows/automation.md

**Summary:**

Report specification completion and automatically trigger implementation planning workflow.

### Phase 4: Report to User
```
✓ Feature specification created: specs/<number>-<name>/spec.md

Intelligence Evidence: [queries + findings]
User Stories: [P1/P2/P3 counts]
Clarifications Needed: [0-3 markers]

**Automatic Next Steps**:
1. If clarifications needed: Use clarify-specification skill
2. Otherwise: **Automatically create implementation plan**

Invoking /plan command now...
```

### Phase 5: Automatic Implementation Planning

**If [NEEDS CLARIFICATION] markers exist**:
- User must run clarify-specification skill
- After clarifications, re-run specify-feature skill

**If NO clarifications**:
- Automatically invoke /plan command via SlashCommand tool
- Workflow progresses: /plan → create-implementation-plan → generate-tasks → /audit
- User sees: spec.md → plan.md → research.md → data-model.md → tasks.md → audit report

**Why This Matters**: Fully automated workflow from specification to implementation-ready state. User only needs to run /feature and /implement.

---

## Anti-Patterns to Avoid

**See:** @.claude/skills/specify-feature/references/specification-rules.md

**Summary:**

**DO NOT**:
- Include tech stack choices in specification
- Design architecture or data models
- Specify implementation details ("use React hooks", "create API endpoint")
- Create more than 3 [NEEDS CLARIFICATION] markers
- Write vague requirements ("system should be fast")

**DO**:
- Focus on user value and business requirements
- Make requirements testable and measurable
- Prioritize user stories (P1, P2, P3)
- Document evidence from intelligence queries
- Limit unknowns (max 3 [NEEDS CLARIFICATION])

---

## Example Execution

**See:** @.claude/skills/specify-feature/examples/feature-creation-example.md

**User Input**: "I want to build a user authentication system with social login options"

**Result**:
- Quality assessment passed (7.2/10)
- Intelligence queries executed
- Specification created: specs/004-auth-social-login/spec.md
- Automatic planning triggered
- Files created: spec.md, plan.md, research.md, data-model.md, tasks.md
- Audit passed
- Ready for /implement

---

## Prerequisites

Before using this skill:
- ✅ Git repository initialized
- ✅ project-intel.mjs exists and is executable
- ✅ PROJECT_INDEX.json exists (auto-generated)
- ⚠️ Optional: product.md exists (for product-aligned features)

## Dependencies

**Depends On**:
- None (this skill is the entry point to SDD workflow)

**Integrates With**:
- **clarify-specification skill**: Use after this skill if ambiguities exist
- **create-implementation-plan skill**: Use after this skill (auto-invoked via /plan)

**Tool Dependencies**:
- fd (file discovery for feature numbering)
- git (branch creation, feature isolation)
- project-intel.mjs (pattern discovery)

---

## Next Steps

After specification completes, **automatic workflow progression**:

**Automatic Chain** (no manual intervention needed):
```
specify-feature (creates spec.md)
    ↓ (auto-invokes /plan)
create-implementation-plan (creates plan.md, research.md, data-model.md)
    ↓ (auto-invokes generate-tasks)
generate-tasks (creates tasks.md)
    ↓ (auto-invokes /audit)
/audit (validates consistency)
    ↓ (if PASS)
Ready for /implement
```

**User Action Required**:
- **If audit PASS**: Run `/implement plan.md` to begin implementation
- **If audit FAIL**: Fix CRITICAL issues, then re-run (audit re-validates automatically)
- **If ambiguities found**: clarify-specification skill may be invoked during workflow

**Commands**:
- **/plan spec.md** - Automatically invoked after spec creation
- **/implement plan.md** - User runs after audit passes

---

## Agent Integration

This skill orchestrates agent delegation through the automatic workflow chain.

### Implementation Planning Agent

**When**: Automatically after spec.md is created (via `/plan` invocation)

**Agent**: implementation-planner

**Delegation Method**: The `/plan` slash command invokes the `create-implementation-plan` skill, which the implementation-planner agent executes.

**What the Planner Receives**:
- spec.md (technology-agnostic specification)
- Constitution requirements (Article IV compliance)
- Project intelligence context (existing patterns via project-intel.mjs)

**What the Planner Returns**:
- plan.md (implementation plan with tasks and ACs)
- research.md (technical research and decisions)
- data-model.md (database/state schema)

### Task Tool Usage (Indirect)

This skill does NOT directly use the Task tool. Instead:

```
specify-feature skill
    ↓ invokes
/plan command (SlashCommand tool)
    ↓ expands to
create-implementation-plan skill
    ↓ executed by
implementation-planner agent (isolated context)
```

**Why This Design**:
- Slash commands provide consistent user interface
- Skills provide reusable workflows
- Agents provide isolated context execution
- Separation of concerns: specify-feature focuses on WHAT/WHY, planner handles HOW

### Expected Workflow

1. **This skill completes**: spec.md created with all requirements
2. **Automatic /plan invocation**: SlashCommand tool runs `/plan spec.md`
3. **Planner agent engaged**: Receives spec, constitution, intelligence context
4. **Planning artifacts created**: plan.md, research.md, data-model.md generated
5. **Automatic task generation**: generate-tasks skill creates tasks.md
6. **Automatic audit**: /audit validates consistency
7. **Ready for implementation**: User runs `/implement plan.md` if audit passes

---

## Failure Modes

### Common Failures & Solutions

**1. Feature auto-numbering fails**
- **Symptom**: Cannot determine next feature number
- **Solution**: Create specs/ directory: `mkdir -p specs/`
- **Workaround**: Manually specify feature number (e.g., 001-feature-name)

**2. Intelligence queries return no results**
- **Symptom**: No existing patterns found
- **Solution**: This is normal for first features; continue without pattern evidence
- **Note**: Intelligence is opportunistic, not required

**3. Specification too technical**
- **Symptom**: Spec includes implementation details (React, PostgreSQL, etc.)
- **Solution**: Re-run skill with explicit "WHAT/WHY only, no HOW" instruction
- **Prevention**: Review @constitution.md Article IV (Specification-First)

**4. Requirements unclear or incomplete**
- **Symptom**: [NEEDS CLARIFICATION] markers in spec
- **Solution**: clarify-specification skill will be invoked automatically
- **Action**: Answer max 5 structured questions to resolve ambiguities

**5. Git branch creation fails**
- **Symptom**: Cannot create feature branch
- **Solution**: Commit current changes or stash them first
- **Command**: `git stash && git checkout -b <feature-branch>`

**6. Duplicate feature numbers**
- **Symptom**: Feature directory already exists
- **Solution**: Intelligence detected wrong next number; manually increment
- **Prevention**: Ensure consistent ###-name branch naming

---

## Related Skills & Commands

**Direct Integration**:
- **clarify-specification skill** - Invoked when ambiguities detected
- **create-implementation-plan skill** - Automatically invoked via /plan after spec
- **/feature command** - User-facing command that invokes this skill

**Workflow Context**:
- Position: **Phase 3** of SDD workflow (after foundation, entry to feature development)
- Triggers: User describes feature idea, mentions "I want to build", "implement", "create"
- Output: spec.md in specs/$FEATURE/ directory (where $FEATURE = NNN-feature-name)
- Next: Automatic progression to /plan → /tasks → /audit → ready for /implement

---

**Skill Version**: 1.3.0
**Last Updated**: 2025-01-19
**Change Log**:
- v1.3.0 (2025-01-19): Added explicit SDD workflow context with 8-phase chain, fixed phase number (Phase 3, not Phase 1)
- v1.2.0 (2025-10-23): Refactored to progressive disclosure pattern (<500 lines)
- v1.1.0 (2025-10-23): Added Phase 0 Pre-Specification Quality Gate
- v1.0.0 (2025-10-22): Initial version with cross-skill references
