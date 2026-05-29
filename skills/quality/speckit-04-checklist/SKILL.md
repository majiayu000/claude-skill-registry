---
name: speckit-04-checklist
description: Generate domain-specific quality checklists for requirements validation
---

# Spec-Kit Checklist

Generate a custom checklist for the current feature based on user requirements. Checklists are "Unit Tests for English" - they validate the REQUIREMENTS, not the implementation.

## Checklist Purpose: "Unit Tests for English"

**CRITICAL CONCEPT**: Checklists are **UNIT TESTS FOR REQUIREMENTS WRITING** - they validate the quality, clarity, and completeness of requirements in a given domain.

**NOT for verification/testing**:
- NOT "Verify the button clicks correctly"
- NOT "Test error handling works"
- NOT "Confirm the API returns 200"
- NOT checking if code/implementation matches the spec

**FOR requirements quality validation**:
- "Are visual hierarchy requirements defined for all card types?" (completeness)
- "Is 'prominent display' quantified with specific sizing/positioning?" (clarity)
- "Are hover state requirements consistent across all interactive elements?" (consistency)
- "Are accessibility requirements defined for keyboard navigation?" (coverage)
- "Does the spec define what happens when logo image fails to load?" (edge cases)

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Constitution Loading (REQUIRED)

Before ANY action, load and internalize the project constitution:

1. Read constitution:
   ```bash
   cat .specify/memory/constitution.md 2>/dev/null || echo "NO_CONSTITUTION"
   ```

2. If exists, parse all principles for checklist generation.

## Prerequisites Check

1. Run prerequisites check:
   ```bash
   .specify/scripts/bash/check-prerequisites.sh --json
   ```

2. Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`.

## Execution Steps

### 1. Clarify Intent

Derive up to THREE contextual clarifying questions. They MUST:
- Be generated from user's phrasing + signals from spec/plan/tasks
- Only ask about information that materially changes checklist content
- Be skipped if already unambiguous in `$ARGUMENTS`

**Question archetypes:**
- Scope refinement: "Should this include integration touchpoints?"
- Risk prioritization: "Which risk areas need mandatory gating checks?"
- Depth calibration: "Is this a lightweight sanity list or formal release gate?"
- Audience framing: "Will this be used by author only or peers during PR review?"
- Boundary exclusion: "Should we explicitly exclude performance tuning items?"

### 2. Load Feature Context

Read from FEATURE_DIR:
- `spec.md`: Feature requirements and scope
- `plan.md` (if exists): Technical details, dependencies
- `tasks.md` (if exists): Implementation tasks

### 3. Generate Checklist

Create `FEATURE_DIR/checklists/[domain].md`:

**CORE PRINCIPLE - Test the Requirements, Not the Implementation**:

Every checklist item MUST evaluate the REQUIREMENTS THEMSELVES for:
- **Completeness**: Are all necessary requirements present?
- **Clarity**: Are requirements unambiguous and specific?
- **Consistency**: Do requirements align with each other?
- **Measurability**: Can requirements be objectively verified?
- **Coverage**: Are all scenarios/edge cases addressed?

**Category Structure** - Group items by requirement quality dimensions:
- Requirement Completeness
- Requirement Clarity
- Requirement Consistency
- Acceptance Criteria Quality
- Scenario Coverage
- Edge Case Coverage
- Non-Functional Requirements
- Dependencies & Assumptions
- Ambiguities & Conflicts

**HOW TO WRITE CHECKLIST ITEMS**:

WRONG (Testing implementation):
- "Verify landing page displays 3 episode cards"
- "Test hover states work on desktop"
- "Confirm logo click navigates home"

CORRECT (Testing requirements quality):
- "Are the exact number and layout of featured episodes specified?" [Completeness]
- "Is 'prominent display' quantified with specific sizing/positioning?" [Clarity]
- "Are hover state requirements consistent across all interactive elements?" [Consistency]
- "Are keyboard navigation requirements defined for all interactive UI?" [Coverage]
- "Is the fallback behavior specified when logo image fails to load?" [Edge Cases]

**ITEM STRUCTURE**:
Each item should follow this pattern:
- Question format asking about requirement quality
- Focus on what's WRITTEN (or not written) in the spec/plan
- Include quality dimension in brackets [Completeness/Clarity/Consistency/etc.]
- Reference spec section `[Spec SS.Y]` when checking existing requirements
- Use `[Gap]` marker when checking for missing requirements

**Traceability Requirements**:
- MINIMUM: >=80% of items MUST include at least one traceability reference
- Each item should reference: spec section, or use markers: `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]`

**ABSOLUTELY PROHIBITED**:
- Any item starting with "Verify", "Test", "Confirm", "Check" + implementation behavior
- References to code execution, user actions, system behavior
- "Displays correctly", "works properly", "functions as expected"
- "Click", "navigate", "render", "load", "execute"
- Test cases, test plans, QA procedures
- Implementation details (frameworks, APIs, algorithms)

**REQUIRED PATTERNS**:
- "Are [requirement type] defined/specified/documented for [scenario]?"
- "Is [vague term] quantified/clarified with specific criteria?"
- "Are requirements consistent between [section A] and [section B]?"
- "Can [requirement] be objectively measured/verified?"
- "Are [edge cases/scenarios] addressed in requirements?"
- "Does the spec define [missing aspect]?"

### 4. Checklist Format

Use template structure:

```markdown
# [CHECKLIST TYPE] Checklist: [FEATURE NAME]

**Purpose**: [Brief description]
**Created**: [DATE]
**Feature**: [Link to spec.md]

## [Category 1]

- [ ] CHK001 - [Requirement quality question] [Quality Dimension, Spec Reference]
- [ ] CHK002 - [Requirement quality question] [Quality Dimension, Gap]

## [Category 2]

- [ ] CHK003 - [Another requirement quality question] [Quality Dimension]

## Notes

- Check items off as completed: `[x]`
- Items are numbered sequentially (CHK001, CHK002, etc.)
```

### 5. Gap Resolution (Interactive)

If checklist contains `[Gap]` items, guide the user through resolving them one by one:

1. **Count gaps**: Identify all items marked with `[Gap]`

2. **For each gap**, present:

   ```markdown
   ────────────────────────────────────────────────────────────────
   Gap 1 of N: [CHK00X]
   ────────────────────────────────────────────────────────────────

   **Missing Requirement:**
   [Quote the checklist item]

   **Why This Matters:**
   [Brief explanation of risk if left unspecified]

   **Suggested Options:**

   | Option | Description | Implications |
   |--------|-------------|--------------|
   | A | [First reasonable default] | [Trade-offs] |
   | B | [Alternative approach] | [Trade-offs] |
   | C | [Another option] | [Trade-offs] |
   | Skip | Leave unspecified for now | Will remain as [Gap] |

   **Your choice (A/B/C/Skip/Custom):** _
   ```

3. **Process user response:**
   - If A/B/C: Update `spec.md` with the new requirement
   - If Skip: Leave as `[Gap]`, continue to next
   - If Custom: Add user's custom text to `spec.md`

4. **After each resolved gap:**
   - Mark the checklist item as `[x]` (complete)
   - Show confirmation of what was added to spec
   - Move to next gap

5. **Summary after all gaps processed:**
   ```
   Gap Resolution Complete:
   - Resolved: X items (added to spec.md)
   - Skipped: Y items (remain as [Gap])
   - Total gaps: Z

   Spec updated at: specs/NNN-feature/spec.md
   ```

**Skip gap resolution if:** User passes `--no-interactive` flag or there are no `[Gap]` items.

### 6. Report

Output:
- Full path to created checklist
- Item count
- Gap resolution summary (if applicable)
- Summary:
  - Focus areas selected
  - Depth level
  - Actor/timing
  - Any user-specified must-have items incorporated

## Example Checklist Types

**UX Requirements Quality:** `ux.md`
- "Are visual hierarchy requirements defined with measurable criteria?" [Clarity, Spec SFR-1]
- "Is the number and positioning of UI elements explicitly specified?" [Completeness]
- "Are interaction state requirements (hover, focus, active) consistently defined?" [Consistency]

**API Requirements Quality:** `api.md`
- "Are error response formats specified for all failure scenarios?" [Completeness]
- "Are rate limiting requirements quantified with specific thresholds?" [Clarity]
- "Are authentication requirements consistent across all endpoints?" [Consistency]

**Security Requirements Quality:** `security.md`
- "Are authentication requirements specified for all protected resources?" [Coverage]
- "Are data protection requirements defined for sensitive information?" [Completeness]
- "Is the threat model documented and requirements aligned to it?" [Traceability]

## Next Steps

After creating and resolving checklists:

1. **If gaps remain**: Run `/speckit-04-checklist` again to continue gap resolution
2. **When all gaps resolved**: Run `/speckit-05-tasks` to generate the task breakdown

Suggest to user:
```
Checklist complete!

Gaps resolved: X (added to spec)
Gaps remaining: Y

Next steps:
- /speckit-04-checklist - (If gaps remain) Continue resolving requirement gaps
- /speckit-05-tasks - Generate task breakdown from plan
```

**Note:** `/speckit-07-implement` requires all checklists to be 100% complete (no `[ ]` items).
