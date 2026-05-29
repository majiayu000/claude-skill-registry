---
name: Specification Clarification
description: Identify and resolve ambiguities in specifications through structured questioning. Use when specification has [NEEDS CLARIFICATION] markers, when user mentions unclear or ambiguous requirements, before creating implementation plans, or when planning reveals specification gaps.
degree-of-freedom: low
allowed-tools: Read, Write, Edit
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/memory-utils.md
@.claude/templates/clarification-checklist.md

# Specification Clarification

## Workflow Context

**SDD Phase**: Phase 4 (Conditional - only if spec has ambiguities)
**Command**: `/clarify`
**Prerequisites**: `specs/$FEATURE/spec.md` with [NEEDS CLARIFICATION] markers
**Creates**: Updated `specs/$FEATURE/spec.md` (resolved ambiguities)
**Predecessor**: Phase 3 - `/feature` → `spec.md`
**Successor**: Phase 5 - `/plan` → `plan.md`

### Phase Chain
```
Phase 1: /define-product → memory/product.md
Phase 2: /generate-constitution → memory/constitution.md
Phase 3: /feature → specs/$FEATURE/spec.md
Phase 4: /clarify (if needed) → updated spec.md (YOU ARE HERE) + consults memory/ for existing patterns
Phase 5: /plan → plan.md + research.md + data-model.md
Phase 6: /tasks (auto) → tasks.md
Phase 7: /audit (auto) → audit-report.md
Phase 8: /implement → code + tests + verification
```

**$FEATURE format**: `NNN-feature-name` (e.g., `001-therapy-app`)

**When to Use**: This phase is CONDITIONAL. Only invoked when:
- spec.md contains [NEEDS CLARIFICATION] markers
- User explicitly mentions unclear requirements
- Planning phase reveals specification gaps

---

**Purpose**: Systematically eliminate ambiguity from specifications through structured questioning before implementation planning.

**Constitutional Authority**: Article IV (Specification-First Development), Article V (Template-Driven Quality)

---

## Quick Reference

| Workflow | Key Activities | Output |
|----------|---------------|--------|
| **Clarification** | Load spec → Scan ambiguities → Prioritize → Ask questions → Update incrementally | spec.md (resolved) |
| **Validation** | Verify consistency → Update coverage → Report completion | Readiness status |

---

## Workflow Files

**Detailed Workflows**:
- **@.claude/skills/clarify-specification/workflows/clarification-workflow.md** - Complete Phases 1-4 (load, prioritize, clarify, validate)

**Examples**:
- **@.claude/skills/clarify-specification/examples/clarification-example.md** - E-commerce checkout feature walkthrough

**References**:
- **@.claude/skills/clarify-specification/references/failure-modes.md** - 10 common failure modes with solutions

---

## Clarification Workflow (Overview)

**See:** @.claude/skills/clarify-specification/workflows/clarification-workflow.md

**Summary:**

### Phase 1: Load Specification and Detect Ambiguities

**Step 1.1**: Read current specification from `specs/<feature>/spec.md`

**Step 1.2**: Scan against 10+ ambiguity categories:
1. Functional Scope & Behavior
2. Domain & Data Model
3. Interaction & UX Flow
4. Non-Functional Requirements (performance, scale, security)
5. Integration & Dependencies
6. Edge Cases & Failure Scenarios
7. Constraints & Tradeoffs
8. Terminology & Definitions
9. Permissions & Access Control
10. State & Lifecycle

**Step 1.3**: Assess coverage for each category:
- **Clear** (10 points) - Well-defined, no ambiguity
- **Partial** (5 points) - Some aspects defined, others unclear
- **Missing** (0 points) - Not addressed in specification

**Coverage Formula**:
```
Coverage := ∑(c_i) where c_i ∈ {clear: 10, partial: 5, missing: 0}
Readiness := Coverage / (10 × num_categories) ≥ 70%
```

---

### Phase 2: Prioritize Clarification Questions

**Step 2.1**: Extract existing [NEEDS CLARIFICATION] markers (Article IV limit: max 3)

**Step 2.2**: Prioritize by impact (Article IV order):
1. **Scope** (highest impact) - Affects what gets built
2. **Security** - Affects risk and compliance
3. **UX Flow** - Affects user experience
4. **Technical** (lowest impact) - Implementation details

**Maximum 5 Questions Per Iteration** (Article IV requirement)

**Step 2.3**: Generate questions with structured format:
- **Context**: Why this matters
- **Question**: Specific, focused inquiry
- **Options**: 2-3 recommendations based on common patterns
- **Impact**: What depends on this answer
- **Intelligence Evidence**: project-intel.mjs findings or MCP query results

---

### Phase 3: Interactive Clarification

**Step 3.1**: Present questions sequentially (ONE AT A TIME for complex topics)

**Step 3.2**: Capture user response with rationale and additional context

**Step 3.3**: Update specification incrementally AFTER EACH answer:
1. Edit spec.md to incorporate answer
2. Remove or resolve [NEEDS CLARIFICATION] marker
3. Add functional requirement with answer
4. Verify no contradictions introduced

**Critical**: Incremental updates prevent contradictions and lost context

---

### Phase 4: Validation and Completion

**Step 4.1**: Verify consistency (no conflicts between new and existing requirements)

**Step 4.2**: Update clarification checklist with resolved categories

**Step 4.3**: Report completion:
```
✓ Clarification complete: N questions resolved
✓ Updated specification with specific requirements
✓ Remaining ambiguities: M markers (≤3 per Article IV)
```

**Readiness Gate**: Coverage ≥ 70% AND ≤ 3 [NEEDS CLARIFICATION] markers remaining

**Next Step**: Use create-implementation-plan skill to define HOW

---

### Phase 5: Re-Clarification (If Needed)

Trigger clarification again if:
- Implementation planning reveals new ambiguities
- User requests changes to requirements
- New [NEEDS CLARIFICATION] markers added during planning

Each iteration: Max 5 new questions, focus on highest-priority gaps, update incrementally

---

## Anti-Patterns to Avoid

**DO NOT**:
- Ask more than 5 questions per iteration (Article IV limit)
- Ask open-ended questions without recommendations
- Present all questions at once (use sequential for complex topics)
- Make assumptions instead of asking
- Skip updating specification after each answer
- Accept ambiguous answers (press for specifics)

**DO**:
- Prioritize by impact (scope > security > UX > technical)
- Provide 2-3 options with recommendations
- Use intelligence queries (project-intel.mjs) for context
- Update spec incrementally (after each answer)
- Verify consistency after updates
- Limit [NEEDS CLARIFICATION] markers to max 3

---

## Example: E-Commerce Checkout Clarification

**See:** @.claude/skills/clarify-specification/examples/clarification-example.md

**Summary**:

**Input**: Specification with 4 [NEEDS CLARIFICATION] markers (exceeds limit), vague acceptance criteria

**Process**:
1. Scanned 10 categories → 31.25% coverage (FAIL, < 70%)
2. Prioritized 5 questions by impact (Scope > Integration > Non-Functional)
3. Asked questions sequentially with options and evidence
4. Updated spec after each answer
5. Validated consistency

**Output**:
- 81.25% coverage (PASS, > 70%)
- 1 marker remaining (deferred low-priority technical detail)
- All ACs specific and testable
- Ready for implementation planning

**Time Investment**: 15-20 minutes of clarification saved hours of rework

---

## Prerequisites

Before using this skill:
- ✅ spec.md exists (created by specify-feature skill)
- ✅ [NEEDS CLARIFICATION] markers present in spec OR user mentions ambiguity
- ✅ Feature directory structure exists: specs/<feature>/
- ⚠️ Optional: clarification-checklist.md (for category coverage tracking)
- ⚠️ Optional: project-intel.mjs (for evidence-based recommendations)

---

## Dependencies

**Depends On**:
- **specify-feature skill** - MUST run before this skill (creates initial spec.md)

**Integrates With**:
- **create-implementation-plan skill** - Uses clarified spec.md as input (typical successor)
- **specify-feature skill** - May trigger this skill if ambiguities detected

**Tool Dependencies**:
- Read tool (to load spec.md and templates)
- Write, Edit tools (to update spec.md incrementally)
- project-intel.mjs (optional, for evidence-based recommendations)

---

## Next Steps

After clarification completes, typical progression:

**If all ambiguities resolved**:
```
clarify-specification (resolves ambiguities)
    ↓
create-implementation-plan (user invokes /plan or auto-triggered)
    ↓
generate-tasks (auto-invoked)
    ↓
/audit (auto-invoked)
```

**If new ambiguities discovered during planning**:
```
create-implementation-plan (finds gaps)
    ↓
clarify-specification (invoked again)
    ↓
create-implementation-plan (continues after resolution)
```

**User Action Required**:
- Answer clarification questions (max 5 per iteration)
- Provide specific answers, not vague responses
- Confirm specification updates after each answer

**Outputs Modified**:
- `specs/$FEATURE/spec.md` - Updated incrementally with clarifications
- Removed [NEEDS CLARIFICATION] markers
- Added functional requirements with clarified details

**Commands**:
- **/plan spec.md** - After clarification complete, create implementation plan
- **/clarify** - User-facing command that invokes this skill

---

## Agent Integration

This skill operates in the main conversation context but may be invoked by other agents when they encounter ambiguities.

### Invocation Patterns

**User-Initiated** (most common):
```
User notices ambiguity → runs /clarify → clarify-specification skill executes
```

**Agent-Initiated** (during planning):
```
implementation-planner agent (finds ambiguity during plan creation)
    ↓ invokes
clarify-specification skill via instruction
    ↓ returns
Updated spec.md with resolved ambiguity
```

### Code Analyzer Support (Optional)

**When**: If clarification requires understanding existing codebase patterns for evidence-based recommendations

**Agent**: code-analyzer

**Example Task Tool Invocation**:
```python
# If clarification needs code analysis for evidence
Task(
    subagent_type="code-analyzer",
    description="Analyze existing authentication patterns",
    prompt="""
    @.claude/agents/code-analyzer.md

    Analyze existing authentication in codebase to inform
    clarification question about auth strategy.

    Use project-intel.mjs to find auth patterns.
    Output: What auth patterns exist (OAuth, JWT, sessions, etc.)
    """
)
```

**Use Case**: When user asks "What auth should we use?", analyzer provides evidence from existing patterns

### Integration with Planner

**Typical Flow**:
```
clarify-specification (resolves all ambiguities)
    ↓ updates
spec.md (all [NEEDS CLARIFICATION] removed)
    ↓ ready for
create-implementation-plan skill
```

**Iterative Flow** (if planner discovers new ambiguities):
```
implementation-planner (finds gap while planning)
    ↓ invokes
clarify-specification (targeted question on gap)
    ↓ user answers
    ↓ updates spec.md
    ↓ returns to
implementation-planner (continues planning)
```

### Task Tool Usage

This skill typically does NOT use Task tool directly. It:
1. Runs in main conversation context (needs user interaction)
2. Updates spec.md incrementally based on user answers
3. May suggest analyzer agent if code evidence needed (but doesn't invoke directly)

**Design Rationale**:
- Clarification requires user dialog (can't run in isolated agent)
- Incremental updates more efficient than agent round-trips
- User must approve spec changes (can't delegate to agent)

---

## Failure Modes

**See:** @.claude/skills/clarify-specification/references/failure-modes.md

**Summary of Common Failures:**

1. **Too many [NEEDS CLARIFICATION] markers (> 3)** - Violates Article IV → Prioritize and defer low-priority details
2. **Open-ended questions without options** - Wastes time → Always provide 2-3 options with recommendations
3. **Asking > 5 questions per iteration** - Violates Article IV → Prioritize by impact, ask top 5 only
4. **Not updating spec after each answer** - Introduces contradictions → Update incrementally after EACH answer
5. **Accepting ambiguous answers** - Defeats purpose → Press for specifics, offer more options
6. **No prioritization** - Wastes effort → Always use Article IV order (Scope > Security > UX > Technical)
7. **Introducing contradictions** - Breaks spec consistency → Validate after EACH update
8. **No intelligence evidence** - Recommendations ignore codebase → Query project-intel.mjs before recommending
9. **Iterating forever** - Analysis paralysis → Stop at ≥70% coverage, ≤3 markers
10. **Not tracking coverage** - Can't measure completion → Use clarification-checklist.md matrix

**Diagnostic Workflow**: Check Article IV compliance → Question quality → Update process → Answer quality → Evidence → Stopping conditions

---

## Related Skills & Commands

**Direct Integration**:
- **specify-feature skill** - Creates spec.md that this skill refines (required predecessor)
- **create-implementation-plan skill** - Uses clarified spec.md as input (typical successor)
- **/clarify command** - User-facing command that invokes this skill

**Workflow Context**:
- Position: **Phase 1.5** of SDD workflow (between specification and planning)
- Triggers: [NEEDS CLARIFICATION] markers OR user mentions "unclear requirements"
- Output: Updated spec.md with resolved ambiguities

**Quality Gates**:
- **Pre-Planning**: Ensures spec is unambiguous before creating plan (Article IV)
- **Max 3 Markers**: Article IV limits [NEEDS CLARIFICATION] markers to 3 max
- **Max 5 Questions**: Article IV limits clarification questions to 5 per iteration

**Workflow Diagram**:
```
specify-feature (creates spec.md with 0-3 [NEEDS CLARIFICATION] markers)
    ↓ (if markers exist OR ambiguities detected)
clarify-specification (resolves ambiguities, max 5 questions/iteration)
    ↓ (when all resolved)
create-implementation-plan (can proceed without specification gaps)
```

**Re-Clarification Trigger**: If create-implementation-plan discovers new gaps, it can trigger clarify-specification again for iterative refinement

---

**Version:** 1.2.0
**Last Updated**: 2025-01-19
**Change Log**:
- v1.2.0 (2025-01-19): Added explicit SDD workflow context with 8-phase chain (Phase 4)
- v1.1.0 (2025-10-23): Refactored to progressive disclosure pattern (<500 lines)
- v1.0.0 (2025-10-22): Initial version
