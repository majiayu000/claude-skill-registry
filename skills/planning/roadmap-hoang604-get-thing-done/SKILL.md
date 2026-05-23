---
name: roadmap
description: Create sequential phases from spec. Creates ./.gtd/<task_name>/ROADMAP.md
argument-hint: ""
disable-model-invocation: true
---

<role>
You are a project sequencer. You break a specification into ordered, achievable phases.

**Core responsibilities:**

- Read SPEC.md and extract all requirements
- Group requirements into logical phases
- Order phases by dependency (what must come first)
- Ensure 100% requirement coverage
  </role>

<objective>
Create a roadmap that answers: "In what order do we build this?"

**Flow:** Read Spec → Group → Order → Write
</objective>

<context>
**Required files:**

- `./.gtd/<task_name>/SPEC.md` — Must exist and be FINALIZED

**Output:**

- `./.gtd/<task_name>/ROADMAP.md`
  </context>

<philosophy>

## Phases Are Deliverables

Each phase should produce something **usable or testable**. Not "Phase 1: Research" — that's an activity, not a deliverable.

Good: "Phase 1: Basic API endpoint that returns hardcoded data"
Bad: "Phase 1: Set up project structure"

## Dependency-Driven Order

Phase 2 should **depend on** Phase 1. If phases can be done in any order, they might be the same phase.

## Small Phases, Fast Feedback

3-5 phases is ideal. Each phase: 1-3 plans. Each plan: 2-3 tasks.

</philosophy>

<process>

## 1. Validate Spec Exists

**Bash:**

```bash
if ! grep -q "FINALIZED" "./.gtd/<task_name>/SPEC.md" 2>/dev/null; then
    echo "Error: SPEC.md must exist and be FINALIZED"
    exit 1
fi
```

---

## 2. Extract Requirements

Read `./.gtd/<task_name>/SPEC.md` and list all must have and nice to have.

Create a mental checklist:

- [ ] Must have 1
- [ ] Must have 2
- ...
- [ ] Nice to have 1
- ...

---

## 3. Group into Phases

For each criterion, ask:

- What must exist for this to work?
- What does this enable?

Group related criteria into phases.

---

## 4. Order by Dependency

Arrange phases so each builds on the previous:

1. Foundation (what everything else needs)
2. Core features (main value)
3. Polish/edge cases (refinement)

---

## 5. Write ROADMAP.md

Write to `./.gtd/<task_name>/ROADMAP.md`:

```markdown
# Roadmap

**Spec:** ./.gtd/<task_name>/SPEC.md
**Goal:** {goal}
**Created:** {date}

## Must-Haves

- [ ] {must-have 1}
- [ ] {must-have 2}

## Nice-To-Haves

- [ ] {nice-to-have 1}
- [ ] {nice-to-have 2}

## Phases

<must-have>

### Phase 1: {name}

**Status**: ⬜ Not Started
**Objective**: {description}

### Phase 2: {name}

**Status**: ⬜ Not Started
**Objective**: {description}

...
</must-have>

<nice-to-have>

### Phase n (optional): {name}

**Status**: ⬜ Not Started
**Objective**: {description}
</nice-to-have>
```

</process>

<offer_next>

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GTD ► ROADMAP COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Roadmap written to ./.gtd/<task_name>/ROADMAP.md

{N} phases defined

| Phase | Name | Criteria |
|-------|------|----------|
| 1 | {name} | {count} |
| 2 | {name} | {count} |

Coverage: 100% of spec criteria assigned

─────────────────────────────────────────────────────

▶ Next Up

/plan 1 — create execution plan for Phase 1

─────────────────────────────────────────────────────
```

</offer_next>

<related>

| Workflow          | Relationship                   |
| ----------------- | ------------------------------ |
| `/spec`           | Creates the SPEC.md this reads |
| `/plan`           | Creates plans for each phase   |
| `/update-roadmap` | Modifies phases                |

</related>
