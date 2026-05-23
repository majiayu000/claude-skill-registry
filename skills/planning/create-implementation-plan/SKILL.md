---
name: Implementation Planning
description: Create technical implementation plans from specifications with intelligence-backed architectural decisions. Use when specification exists and user mentions tech stack, architecture, implementation approach, or asks "how to implement" or "how to build" the feature.
degree-of-freedom: medium
allowed-tools: Bash(project-intel.mjs:*), Read, Write, Edit
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/CoD_Σ.md
@.claude/shared-imports/memory-utils.md
@.claude/shared-imports/master-todo-utils.md
@.claude/templates/plan.md
@.claude/templates/research-template.md
@.claude/templates/data-model-template.md

# Implementation Planning

## Workflow Context

**SDD Phase**: Phase 5 (Implementation Planning)
**Command**: `/plan`
**Prerequisites**: `specs/$FEATURE/spec.md` (clarified, no [NEEDS CLARIFICATION] markers)
**Creates**: `specs/$FEATURE/plan.md`, `research.md`, `data-model.md`
**Predecessor**: Phase 4 - `/clarify` (if needed) OR Phase 3 - `/feature`
**Successor**: Phase 6 - `/tasks` (auto-generated) → Phase 7 - `/audit`

### Phase Chain
```
Phase 1: /define-product → memory/product.md
Phase 2: /generate-constitution → memory/constitution.md
Phase 3: /feature → specs/$FEATURE/spec.md + todos/master-todo.md entry
Phase 4: /clarify (if needed) → updated spec.md
Phase 5: /plan → plan.md + research.md + data-model.md (YOU ARE HERE) + queries memory/ for patterns
Phase 6: /tasks (auto) → tasks.md
Phase 7: /audit (auto) → audit-report.md
Phase 8: /implement → code + tests + verification
```

**$FEATURE format**: `NNN-feature-name` (e.g., `001-therapy-app`)

### Automatic Workflow Progression

After creating plan.md, this skill automatically:
1. Invokes `generate-tasks` skill → creates tasks.md
2. Triggers `/audit` command → validates consistency
3. If audit PASS → ready for `/implement`

**Note**: The deprecated `create-plan` skill should NOT be used. Use this `create-implementation-plan` skill instead.

---

**Purpose**: Transform technology-agnostic specifications into technical implementation plans with architecture decisions, tech stack selection, and acceptance criteria mapping.

**Constitutional Authority**: Article IV (Specification-First Development), Article VI (Simplicity & Anti-Abstraction), Article I (Intelligence-First Principle)

**Announce at start:** "I'm using the create-implementation-plan skill to convert your specification into a technical implementation plan with intelligence-backed architectural decisions."

---

## Quick Reference

| Phase | Key Activities | Output | Article |
|-------|---------------|--------|---------|
| **0. Constitutional Gates** | Validate spec exists, check Article VI limits | Gate pass/fail | Article VI |
| **1. Intelligence Gathering** | Query project-intel.mjs for patterns | Evidence files | Article I |
| **2. Technical Design** | Select tech stack, design architecture | research.md, data-model.md, contracts/ | Article VI |
| **3. AC Mapping** | Generate acceptance criteria (≥2 per story) | ACs in plan.md | Article III |
| **4. Post-Design Re-Check** | Re-validate Article VI gates | Gate confirmation | Article VI |
| **5. Generate Plan** | Assemble plan.md with all artifacts | plan.md + artifacts | Article V |
| **6. Auto Task Generation** | Invoke generate-tasks skill | tasks.md + /audit | Article VII |

---

## Templates You Will Use

- **@.claude/shared-imports/constitution.md** - Article VI complexity gates (all phases)
- **@.claude/shared-imports/CoD_Σ.md** - Evidence-based reasoning (all phases)
- **@.claude/templates/plan.md** - Main implementation plan structure (Phase 5)
- **@.claude/templates/research-template.md** - Technical decisions documentation (Phase 2)
- **@.claude/templates/data-model-template.md** - Entity specifications (Phase 2)

---

## The Process

Copy this checklist to track progress:

```
SDD Planning Progress:
- [ ] Phase 0: Constitutional Gates Validated (Article VI check PASS)
- [ ] Phase 1: Intelligence Gathered (project-intel.mjs queries complete)
- [ ] Phase 2: Technical Design Complete (research.md, data-model.md, contracts/ created)
- [ ] Phase 3: ACs Mapped (≥2 per user story)
- [ ] Phase 4: Post-Design Re-Check (gates maintained after design)
- [ ] Phase 5: Plan Generated (plan.md with all artifacts)
- [ ] Phase 6: Tasks Auto-Generated (generate-tasks skill invoked → /audit runs)
```

---

## Detailed Workflows

### Phase 0: Pre-Design Constitutional Gates

**See:** @.claude/skills/create-implementation-plan/workflows/constitutional-gates.md

**Summary**:
- Validate spec.md exists (PreToolUse hook enforces Article IV)
- Check Article VI complexity gates BEFORE design:
  - Gate 1: Project Count ≤ 3
  - Gate 2: Abstraction Layers ≤ 2 per concept
  - Gate 3: Framework Trust (no unnecessary wrappers)
- Document violations in Complexity Justification Table if needed
- Proceed only if gates PASS or justifications provided

### Phase 1: Intelligence-First Context Gathering

**Article I Mandate**: Query before reading files.

**Summary**:
```bash
# Step 1.1: Search for patterns
!`project-intel.mjs --search "<keywords>" --type "tsx,ts,py,go" --json > /tmp/plan_intel_patterns.json`

# Step 1.2: Analyze architecture
!`project-intel.mjs --overview --json > /tmp/plan_intel_overview.json`

# Step 1.3: Query dependencies
!`project-intel.mjs --dependencies "<key-files>" --direction both --json > /tmp/plan_intel_deps.json`
```

**Save all evidence** to `/tmp/plan_intel_*.json` for CoD^Σ traces.

### Phase 2: Technical Design

**See:** @.claude/skills/create-implementation-plan/workflows/technical-design.md

**Summary**:
- Select tech stack (based on intelligence findings)
- Design architecture (component breakdown, integration points)
- Create research.md (decisions with rationale and evidence)
- Design data model (entities without implementation types)
- Define API contracts (request/response schemas)
- Create quickstart.md (test scenarios for validation)

**Artifacts Created**: research.md, data-model.md, contracts/, quickstart.md

### Phase 3: Acceptance Criteria Mapping

**Article III Requirement**: Minimum 2 testable ACs per user story.

**Summary**:
```bash
Read specs/$FEATURE/spec.md
```

**For EACH user story**, generate ≥2 ACs in Given/When/Then format:

**AC Format**:
- **AC-ID**: [Story]-[Number] (e.g., P1-001, P1-002)
- **Given** [precondition], **When** [action], **Then** [outcome]
- **Test**: How to automate verification

**Example**:
```markdown
**AC-P1-001**: User can register with valid email and password
- **Given** user has valid email and strong password
- **When** user submits registration form
- **Then** account is created and user is logged in
- **Test**: POST /api/auth/register with valid data returns 201 + session token
```

### Phase 4: Post-Design Constitutional Re-Check

**See:** @.claude/skills/create-implementation-plan/workflows/constitutional-gates.md

**Summary**:
- Re-validate all three Article VI gates AFTER design
- Ensure architecture didn't introduce violations:
  - Gate 1: Project count still ≤ 3
  - Gate 2: No extra abstraction layers added
  - Gate 3: No wrappers around framework features
- Update Complexity Justification Table if new violations
- Confirm gates maintained before plan generation

### Phase 5: Generate Implementation Plan

**Summary**:

Use `@.claude/templates/plan.md` structure with sections:
1. Summary (one paragraph overview)
2. Technical Context (tech stack, platform, dependencies)
3. Constitution Check (gates passed/violated with justifications)
4. Architecture (component breakdown with integration points)
5. Acceptance Criteria (all ACs from Phase 3)
6. File Structure (exact paths where code will live)
7. CoD^Σ Evidence (intelligence query results, MCP sources)

**Save artifacts**:
- `specs/$FEATURE/plan.md`
- `specs/$FEATURE/research.md`
- `specs/$FEATURE/data-model.md`
- `specs/$FEATURE/contracts/*.md`
- `specs/$FEATURE/quickstart.md`

**Report completion** with:
- Intelligence evidence summary
- Technical decisions made
- Artifacts generated
- Acceptance criteria count
- Constitutional compliance verification

### Phase 6: Automatic Task Generation

**DO NOT ask user to trigger task generation** - this is automatic workflow progression.

**After plan artifacts complete**, automatically invoke generate-tasks skill:

"Now that the implementation plan is complete, **automatically generate the task breakdown**:

Use the **generate-tasks skill** to create tasks.md.

This will:
1. Load user stories from specs/$FEATURE/spec.md
2. Load technical details from specs/$FEATURE/plan.md
3. Organize tasks by user story (Article VII)
4. Mark parallelizable tasks with [P]
5. Ensure ≥2 ACs per story (Article III)
6. **Automatically invoke /audit for quality gate validation**

The generate-tasks skill will handle this entire workflow automatically, including the quality gate check."

**No manual intervention required** - workflow proceeds automatically through task generation and validation.

---

## Examples & Patterns

**See:** @.claude/skills/create-implementation-plan/examples/design-examples.md

**Four comprehensive examples**:
1. research.md template (OAuth decision example with CoD^Σ evidence)
2. data-model.md template (User entity with OAuth support)
3. API contracts template (auth-endpoints.md with full schemas)
4. quickstart.md template (5 test scenarios for validation)

**Key Patterns**:
- Intelligence-Based Architecture: query → identify patterns → extend existing OR create new
- Research Documentation: Decision + Rationale + Alternatives + Evidence (file:line or MCP)
- Technology-Agnostic Data Modeling: Entity purpose → Attributes (no types) → Relationships → Validation
- Contract-First API Design: Endpoint → Request schema → Response schema → Error cases → Auth requirements
- Quickstart Scenarios: Setup → Test steps → Expected outcome → Verification commands

---

## Anti-Patterns, Prerequisites & Failure Modes

**See:** @.claude/skills/create-implementation-plan/references/failure-modes.md

**Anti-Patterns to Avoid**:
- Planning before specification exists (Article IV violation)
- Skipping intelligence queries (Article I violation)
- Designing without checking constitution gates (Article VI violation)
- Creating ACs with < 2 per story (Article III violation)

**Prerequisites**:
- ✅ spec.md exists (PreToolUse hook enforces Article IV)
- ✅ project-intel.mjs is executable
- ✅ PROJECT_INDEX.json exists

**Common Failures & Solutions**: 8 documented failure modes with symptoms, solutions, and prevention strategies

---

## Dependencies

**Depends On**:
- **specify-feature skill** - MUST run before this skill (Article IV)
- **clarify-specification skill** - Should run if [NEEDS CLARIFICATION] markers exist

**Integrates With**:
- **generate-tasks skill** - Automatically invoked after this skill completes
- **implement-and-verify skill** - Uses plan.md output as input

**Tool Dependencies**:
- project-intel.mjs (intelligence queries for patterns, dependencies)
- MCP Ref tool (library documentation)
- MCP Context7 tool (external framework docs)

---

## Next Steps

After plan completes, **automatic workflow progression**:

**Automatic Chain** (no manual intervention):
```
create-implementation-plan (creates plan.md, research.md, data-model.md, contracts/)
    ↓ (auto-invokes generate-tasks)
generate-tasks (creates tasks.md)
    ↓ (auto-invokes /audit)
/audit (validates consistency)
    ↓ (if PASS)
Ready for /implement
```

**User Action Required**:
- **If audit PASS**: Run `/implement plan.md` to begin implementation
- **If audit FAIL**: Fix CRITICAL issues (usually in spec or plan), re-run workflow
- **If complexity gates fail**: Justify violations or simplify design

**Outputs Created**:
- `specs/$FEATURE/plan.md` - Main implementation plan
- `specs/$FEATURE/research.md` - Technical decisions and rationale
- `specs/$FEATURE/data-model.md` - Entity schemas (if applicable)
- `specs/$FEATURE/contracts/` - API/interface contracts (if applicable)
- `specs/$FEATURE/quickstart.md` - Test scenarios (if applicable)

**Commands**:
- **/tasks** - Automatically invoked to generate task breakdown
- **/implement plan.md** - User runs after audit passes

---

## Related Skills & Commands

**Direct Integration**:
- **specify-feature skill** - Provides spec.md (workflow start, this skill requires it)
- **clarify-specification skill** - Should run if [NEEDS CLARIFICATION] markers exist
- **generate-tasks skill** - Automatically invoked after plan complete (Article VII)
- **implement-and-verify skill** - Uses plan.md output as input for implementation
- **analyze-code skill** - Use when understanding existing code before modifying
- **/plan command** - User-facing command that invokes this skill
- **/audit command** - Automatically invoked by generate-tasks skill

**Workflow Context**:
- Position: **Phase 2** of SDD workflow (after specification, before tasks)
- Triggers: User runs /plan after /feature completes
- Output: plan.md + research.md + data-model.md + contracts/ + quickstart.md

**Quality Gates**:
- **Pre-Design**: Article VI constitutional gates (Project count, Abstraction layers, Framework trust)
- **Post-Design**: Re-validate Article VI gates after architecture decisions
- **Pre-Implementation**: /audit runs automatically after task generation

**Automatic Workflow Pattern**:
```
/feature → specify-feature skill → /plan (auto-invoked)
    ↓
create-implementation-plan skill (this skill)
    ↓ (auto-invokes)
generate-tasks skill
    ↓ (auto-invokes)
/audit
    ↓ (if PASS)
User runs /implement
```

---

## Success Metrics

**Planning Quality:**
- 100% intelligence-first (queries before design)
- 100% constitutional compliance (all Article VI gates documented)
- ≥2 ACs per user story (Article III requirement)
- All decisions have CoD^Σ evidence

**Deliverable Quality:**
- plan.md follows template structure
- research.md documents all technical decisions with rationale
- data-model.md is technology-agnostic
- contracts/ have complete schemas (request/response/errors)
- quickstart.md has testable scenarios

---

## When to Use This Skill

**Use create-implementation-plan when:**
- User has spec.md ready (Article IV prerequisite)
- User mentions tech stack, architecture, implementation approach
- User asks "how to implement" or "how to build" the feature
- User runs /plan command

**Don't use when:**
- No spec.md exists yet (use specify-feature skill first)
- Specification has [NEEDS CLARIFICATION] markers (use clarify-specification skill first)
- User just wants to analyze code (use analyze-code skill)
- User wants to implement directly (use implement-and-verify skill, but audit will block without plan)

---

## Version

**Version:** 1.3.0
**Last Updated:** 2025-01-19
**Owner:** Claude Code Intelligence Toolkit

**Change Log**:
- v1.3.0 (2025-01-19): Added explicit SDD workflow context with 8-phase chain (Phase 5), deprecated create-plan reference
- v1.2.0 (2025-10-23): Refactored to progressive disclosure pattern (<500 lines)
- v1.1.0 (2025-10-23): Added Phase 6 automatic task generation enforcement
- v1.0.0 (2025-10-22): Initial version with constitutional gates and intelligence-first approach
