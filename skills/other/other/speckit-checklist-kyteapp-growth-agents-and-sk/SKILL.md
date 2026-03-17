---
name: speckit-checklist
description: Generate custom checklist for the current feature based on user requirements
---

# Speckit-Checklist: Requirements Quality Validation

## Purpose

Generate "unit tests for requirements" - checklists that validate the quality, clarity, and completeness of requirements in a given domain.

## Core Concept: "Unit Tests for English"

**CRITICAL:** Checklists test **REQUIREMENTS QUALITY**, not implementation correctness.

### NOT for Verification/Testing

❌ NOT "Verify the button clicks correctly"
❌ NOT "Test error handling works"
❌ NOT "Confirm the API returns 200"
❌ NOT checking if code matches spec

### FOR Requirements Quality Validation

✅ "Are visual hierarchy requirements defined for all card types?" (completeness)
✅ "Is 'prominent display' quantified with specific sizing/positioning?" (clarity)
✅ "Are hover state requirements consistent across all interactive elements?" (consistency)
✅ "Are accessibility requirements defined for keyboard navigation?" (coverage)
✅ "Does the spec define what happens when logo image fails to load?" (edge cases)

## Metaphor

**If your spec is code written in English, the checklist is its unit test suite.**

You're testing whether the requirements are well-written, complete, unambiguous, and ready for implementation - NOT whether the implementation works.

## Prerequisites

- Feature specification exists (`spec.md`)
- Optional: `plan.md`, `tasks.md` for additional context

## What This Skill Does

1. Clarifies checklist intent (domain, depth, audience)
2. Loads feature context from spec/plan/tasks
3. Generates requirements quality checklist
4. Creates unique filename based on domain
5. Validates checklist follows "unit tests for requirements" pattern

## Execution Flow

All execution logic is now contained within this skill. The skill handles:
- Prerequisites checking
- Intent clarification
- Context loading
- Checklist generation

### Quick Summary

1. **Setup:** Run `check-prerequisites.sh` to get feature paths
2. **Clarify intent:** Ask up to 3-5 contextual questions:
   - Scope refinement
   - Risk prioritization
   - Depth calibration
   - Audience framing
3. **Load context:** Read spec.md, plan.md, tasks.md (progressive disclosure)
4. **Generate checklist:** Create requirements quality validation items
5. **Report completion:** Path, item count, focus areas

## Checklist Structure

### Category Structure (Quality Dimensions)

Group items by requirement quality dimensions:

1. **Requirement Completeness** - Are all necessary requirements present?
2. **Requirement Clarity** - Are requirements specific and unambiguous?
3. **Requirement Consistency** - Do requirements align without conflicts?
4. **Acceptance Criteria Quality** - Are success criteria measurable?
5. **Scenario Coverage** - Are all flows/cases addressed?
6. **Edge Case Coverage** - Are boundary conditions defined?
7. **Non-Functional Requirements** - Performance, Security, Accessibility specified?
8. **Dependencies & Assumptions** - Are they documented and validated?
9. **Ambiguities & Conflicts** - What needs clarification?

### Item Format (REQUIRED)

Each item should:
- Use **question format** asking about requirement quality
- Focus on what's **WRITTEN** (or not written) in spec/plan
- Include **quality dimension** in brackets [Completeness/Clarity/etc.]
- Reference **spec section** `[Spec §X.Y]` or use markers: `[Gap]`, `[Ambiguity]`, `[Conflict]`

### Examples by Quality Dimension

**Completeness:**
```markdown
- [ ] CHK001 - Are error handling requirements defined for all API failure modes? [Gap]
- [ ] CHK002 - Are accessibility requirements specified for all interactive elements? [Completeness]
- [ ] CHK003 - Are mobile breakpoint requirements defined for responsive layouts? [Gap]
```

**Clarity:**
```markdown
- [ ] CHK010 - Is 'fast loading' quantified with specific timing thresholds? [Clarity, Spec §NFR-2]
- [ ] CHK011 - Are 'related episodes' selection criteria explicitly defined? [Clarity, Spec §FR-5]
- [ ] CHK012 - Is 'prominent' defined with measurable visual properties? [Ambiguity, Spec §FR-4]
```

**Consistency:**
```markdown
- [ ] CHK020 - Do navigation requirements align across all pages? [Consistency, Spec §FR-10]
- [ ] CHK021 - Are card component requirements consistent between landing and detail pages? [Consistency]
```

**Coverage:**
```markdown
- [ ] CHK030 - Are requirements defined for zero-state scenarios (no episodes)? [Coverage, Edge Case]
- [ ] CHK031 - Are concurrent user interaction scenarios addressed? [Coverage, Gap]
- [ ] CHK032 - Are requirements specified for partial data loading failures? [Coverage, Exception Flow]
```

**Measurability:**
```markdown
- [ ] CHK040 - Are visual hierarchy requirements measurable/testable? [Acceptance Criteria, Spec §FR-1]
- [ ] CHK041 - Can 'balanced visual weight' be objectively verified? [Measurability, Spec §FR-2]
```

## Writing Checklist Items

### ✅ REQUIRED PATTERNS (Testing Requirements Quality)

- ✅ "Are [requirement type] defined/specified/documented for [scenario]?"
- ✅ "Is [vague term] quantified/clarified with specific criteria?"
- ✅ "Are requirements consistent between [section A] and [section B]?"
- ✅ "Can [requirement] be objectively measured/verified?"
- ✅ "Are [edge cases/scenarios] addressed in requirements?"
- ✅ "Does the spec define [missing aspect]?"

### 🚫 ABSOLUTELY PROHIBITED (Testing Implementation)

- ❌ Any item starting with "Verify", "Test", "Confirm", "Check" + implementation behavior
- ❌ References to code execution, user actions, system behavior
- ❌ "Displays correctly", "works properly", "functions as expected"
- ❌ "Click", "navigate", "render", "load", "execute"
- ❌ Test cases, test plans, QA procedures
- ❌ Implementation details (frameworks, APIs, algorithms)

## Example Checklist Types

### UX Requirements Quality: `ux.md`

```markdown
- [ ] CHK001 - Are visual hierarchy requirements defined with measurable criteria? [Clarity, Spec §FR-1]
- [ ] CHK002 - Is the number and positioning of UI elements explicitly specified? [Completeness, Spec §FR-1]
- [ ] CHK003 - Are interaction state requirements (hover, focus, active) consistently defined? [Consistency]
- [ ] CHK004 - Are accessibility requirements specified for all interactive elements? [Coverage, Gap]
- [ ] CHK005 - Is fallback behavior defined when images fail to load? [Edge Case, Gap]
- [ ] CHK006 - Can 'prominent display' be objectively measured? [Measurability, Spec §FR-4]
```

### API Requirements Quality: `api.md`

```markdown
- [ ] CHK001 - Are error response formats specified for all failure scenarios? [Completeness]
- [ ] CHK002 - Are rate limiting requirements quantified with specific thresholds? [Clarity]
- [ ] CHK003 - Are authentication requirements consistent across all endpoints? [Consistency]
- [ ] CHK004 - Are retry/timeout requirements defined for external dependencies? [Coverage, Gap]
- [ ] CHK005 - Is versioning strategy documented in requirements? [Gap]
```

### Security Requirements Quality: `security.md`

```markdown
- [ ] CHK001 - Are authentication requirements specified for all protected resources? [Coverage]
- [ ] CHK002 - Are data protection requirements defined for sensitive information? [Completeness]
- [ ] CHK003 - Is the threat model documented and requirements aligned to it? [Traceability]
- [ ] CHK004 - Are security requirements consistent with compliance obligations? [Consistency]
- [ ] CHK005 - Are security failure/breach response requirements defined? [Gap, Exception Flow]
```

## Success Indicators

Checklist is correct when:
- ✅ Every item tests requirement quality, not implementation
- ✅ Items use question format
- ✅ Quality dimensions identified [Completeness], [Clarity], etc.
- ✅ Traceability references included (≥80% of items)
- ✅ No "Verify", "Test", "Confirm" implementation checks
- ✅ Focus on what's WRITTEN in spec/plan
- ✅ Items can be validated by reading docs, not running code

## Output

```
specs/N-feature-name/checklists/
├── ux.md                      # UX requirements quality
├── api.md                     # API requirements quality
├── security.md                # Security requirements quality
└── ...                        # Domain-specific checklists

Each run creates a NEW file based on domain
```

## Anti-Examples: What NOT To Do

### ❌ WRONG (Testing Implementation)

```markdown
- [ ] CHK001 - Verify landing page displays 3 episode cards [Spec §FR-001]
- [ ] CHK002 - Test hover states work correctly on desktop [Spec §FR-003]
- [ ] CHK003 - Confirm logo click navigates to home page [Spec §FR-010]
```

### ✅ CORRECT (Testing Requirements Quality)

```markdown
- [ ] CHK001 - Are the number and layout of featured episodes explicitly specified? [Completeness, Spec §FR-001]
- [ ] CHK002 - Are hover state requirements consistently defined for all interactive elements? [Consistency, Spec §FR-003]
- [ ] CHK003 - Are navigation requirements clear for all clickable brand elements? [Clarity, Spec §FR-010]
```

## Related Skills

- **speckit-specify** - Create specification (generates requirements to validate)
- **speckit-plan** - Create plan (generates technical requirements to validate)
- **brainstorming** - Use before specification to ensure requirements well-understood
