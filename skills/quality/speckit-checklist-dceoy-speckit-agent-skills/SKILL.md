---
name: speckit-checklist
description: Generate a custom checklist for the current feature based on user requirements.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Spec-Kit Checklist

Generate requirement quality validation checklists. "Unit Tests for English" - validates requirements are complete, clear, and consistent.

## Core Concept: Unit Tests for Requirements

**CRITICAL:** Checklists test **REQUIREMENTS QUALITY**, not implementation.

**❌ NOT for verification/testing:**

- "Verify button clicks correctly"
- "Test error handling works"
- "Confirm API returns 200"
- Checking if code matches spec

**✅ FOR requirements quality:**

- "Are visual hierarchy requirements defined for all card types?" [Completeness]
- "Is 'prominent display' quantified with specific sizing?" [Clarity]
- "Are hover state requirements consistent across interactive elements?" [Consistency]
- "Are accessibility requirements defined for keyboard navigation?" [Coverage]
- "Does spec define fallback when logo image fails to load?" [Edge Cases]

**Metaphor:** If your spec is code written in English, the checklist is its unit test suite.

## When to Use

- After creating spec.md or plan.md
- Before implementation to validate requirements
- For PR review quality gates
- Need to ensure requirements are implementation-ready

## Execution Workflow

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` to get FEATURE_DIR and AVAILABLE_DOCS
2. **Clarify intent** (dynamic, up to 3 questions):
   - Generate from user phrasing + extracted signals from spec/plan/tasks
   - Only ask about information that materially changes checklist content
   - Skip if already unambiguous in user input
   - Generation algorithm:
     - Extract signals: domain keywords, risk indicators, stakeholder hints, explicit deliverables
     - Cluster into candidate focus areas (max 4) ranked by relevance
     - Identify probable audience & timing if not explicit
     - Detect missing dimensions: scope breadth, depth/rigor, risk emphasis, exclusion boundaries
     - Formulate questions from archetypes: scope refinement, risk prioritization, depth calibration, audience framing, boundary exclusion, scenario class gap
   - Question formatting: compact table with Option | Candidate | Why It Matters
   - Defaults when interaction impossible: Depth=Standard, Audience=Reviewer (PR)
3. **Understand user request**: Combine user input + clarifying answers to derive checklist theme, must-have items, focus selections
4. **Load feature context**: Read spec.md, plan.md (if exists), tasks.md (if exists) - only necessary portions, summarize long sections
5. **Generate checklist**:
   - Create `FEATURE_DIR/checklists/` directory if doesn't exist
   - Generate unique filename: `[domain].md` (e.g., ux.md, api.md, security.md)
   - Each run creates NEW file (never overwrites existing checklists)
   - Number items sequentially starting from CHK001
   - **Soft cap: 40 items** - if more candidates, prioritize by risk/impact and merge near-duplicates
6. **Checklist structure** - Group items by requirement quality dimensions:
   - Requirement Completeness (are all necessary requirements documented?)
   - Requirement Clarity (are requirements specific and unambiguous?)
   - Requirement Consistency (do requirements align without conflicts?)
   - Acceptance Criteria Quality (are success criteria measurable?)
   - Scenario Coverage (are all flows/cases addressed?)
   - Edge Case Coverage (are boundary conditions defined?)
   - Non-Functional Requirements (are performance, security, accessibility specified?)
   - Dependencies & Assumptions (are they documented and validated?)
   - Ambiguities & Conflicts (what needs clarification?)
7. **Item structure**: Each item follows pattern:
   - `- [ ] CHK### - [Question about requirement quality]? [Dimension, Reference]`
   - Question format focusing on what's WRITTEN (or missing) in spec
   - Quality dimension marker: [Completeness/Clarity/Consistency/Coverage/Measurability/etc.]
   - Traceability: [Spec §X.Y] or [Gap] or [Ambiguity] or [Conflict]
   - MINIMUM: ≥80% of items MUST include traceability reference
8. **Report**: Output full path, item count, focus areas, depth level, actor/timing

## Key Points

- **Test requirements, NOT implementation**
  - WRONG: "Verify landing page displays 3 episode cards"
  - CORRECT: "Are the number and layout of featured episodes explicitly specified? [Completeness, Spec §FR-001]"
- **Question format** - "Are requirements X...?" not "Does system X...?"
- **Add traceability** - Reference spec sections or mark gaps (≥80% requirement)
- **Focus scope** - One domain per checklist (UX, API, Security, etc.)
- **Balance depth** - 15-40 items for focused, actionable validation
- **Content consolidation** - Soft cap 40 items, merge near-duplicates, prioritize by risk/impact
- **Prohibited patterns** - Any item starting with "Verify", "Test", "Confirm", "Check" + implementation behavior
- **Required patterns** - "Are [requirement type] defined/specified/documented for [scenario]?"

## Next Steps

After creating checklist:

- **Use for PR reviews** - Validate spec/plan before approval
- **Self-review** - Author validates own requirements
- **QA validation** - Ensure testable acceptance criteria
- **Implementation** - Use `speckit-implement` after validation

## See Also

- `speckit-specify` - Create feature specifications
- `speckit-plan` - Create technical implementation strategy
- `speckit-implement` - Execute implementation plan
