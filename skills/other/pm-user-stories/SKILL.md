---
name: pm-user-stories
description: Разбивает Epic или крупное требование на независимые User Stories с acceptance criteria в формате Given-When-Then, проверкой по INVEST и оценкой Story Points (Fibonacci или T-shirt). На выходе — Story Map с предложением по Sprint-планированию. User-invoked only — do NOT auto-trigger. Triggers on /pm-user-stories, "разбей на user stories", "разбить эпик", "story map", "AC", "acceptance criteria", "break down into user stories", "split this epic", "write user stories".
---

# pm-user-stories — Break an Epic into User Stories


Part of the Personal Corp framework — running a one-person business through AI agents.
Decompose a large requirement or Epic into independently-deliverable User Stories. Every Story is validated against INVEST. Output is ready to paste into Jira, Linear, or GitHub Issues.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Requirement description | yes | An Epic or large requirement; can paste a PRD section |
| Granularity | no | Sprint-level (1-3 days/story) or iteration-level (1-2 weeks); default Sprint |
| Team composition | no | FE+BE split / full-stack / has mobile — affects per-tier splitting |
| Estimation system | no | Fibonacci (1/2/3/5/8/13) or T-shirt (S/M/L/XL); default Fibonacci |

## Step 1 — Map the full requirement

Extract from the requirement:

- **Roles involved:** who uses this? (end user, admin, ops, etc.)
- **Core flow:** main path? branches?
- **Business rules:** constraints and conditions?
- **Data entities:** what data objects are involved?

## Step 2 — Pick a splitting pattern

Five patterns. Pick by requirement shape; combine for hybrids.

| Pattern | When to use | Example |
|---|---|---|
| **By workflow step** | Requirement is a complete process | Checkout → pick item / address / payment / confirm |
| **By business-rule variant** | Same feature with multiple rule sets | Discount → fixed-amount / coupon / points / combined |
| **By CRUD operation** | Requirement centers on one data object | Address book → create / edit / delete / set default |
| **By role perspective** | Multi-role feature | Order management → user view / merchant processing / ops dashboard |
| **By complexity progression** | Feature has simple and full versions | Search → keyword / filters / suggestions / history |

**Selection principle:** target ≤ 1 Sprint per Story. Hybrid requirements combine patterns.

**Granularity calibration:**
- Stories < 3 → likely too coarse; check for hidden sub-flows
- Stories > 20 → likely too fine, or this is multiple Epics; split Epics first
- Single Story estimate > 8 points → too big; split further

## Step 3 — Write each User Story + AC

```
### US-{N}: {Story title — verb-led, e.g. "Choose payment method"}

**Role:** As a {role}
**Action:** I want to {specific action}
**Value:** so that {business value}
**Priority:** P0 (must) / P1 (important) / P2 (nice-to-have)
**Story Points:** {estimate}

**Acceptance Criteria:**
- [ ] Given {precondition}, When {action}, Then {expected result}
- [ ] Given {exception precondition}, When {action}, Then {error handling}

**Dependencies:** {other Story IDs, or "none"}
**Tech notes:** {dev callouts, optional}
```

**Story Point reference (Fibonacci):**

| Points | Complexity | Effort | Typical scope |
|---|---|---|---|
| 1 | Trivial | < 0.5 day | Copy change, config tweak, add an event |
| 2 | Simple | 0.5-1 day | One CRUD operation, form validation |
| 3 | Medium | 1-2 days | A complete feature point with business logic |
| 5 | Complex | 2-4 days | Multi-module interaction |
| 8 | Big | 4-7 days | New system / new flow core module |
| 13 | Re-split | > 1 week | Means the Story is too big — must split |

**AC quality rules — every AC must satisfy:**

- **Specific:** Given clause has a concrete precondition ("user logged in AND balance ≥ 100"), not "user logged in"
- **Testable:** Then clause has a verifiable result ("balance decreases by 100 AND order status = paid"), not "payment succeeds"
- **Edge coverage:** every Story has ≥ 1 happy-path AC + ≥ 1 exception-path AC

## Step 4 — INVEST validation

Run each Story against the six checks:

| Principle | Check | If fails |
|---|---|---|
| **I**ndependent | Delete this Story — can the others still ship? | Cyclic deps → merge or re-split |
| **N**egotiable | Does it describe "what" or "how"? | Strip implementation detail, keep value |
| **V**aluable | Will the user perceive value when this ships? | Pure refactor → attach to a user-perceivable feature |
| **E**stimable | Can the team agree on points within 5 minutes? | Wide spread = unclear requirement; clarify first |
| **S**mall | Fits in one Sprint? | Larger → split |
| **T**estable | Can QA write test cases directly from the AC? | Add concrete edge values and expected results |

**Definition of Ready (must hold before entering development):**

| Check | Standard | If unmet |
|---|---|---|
| AC complete | ≥ 1 happy + ≥ 1 exception | Fill ACs, then schedule |
| No blocking deps | All upstream Stories done or mockable | Tag "Blocked", push to a later Sprint |
| Designs ready | UI Stories have design specs | No designs → tag "Needs design" |
| Estimation consensus | Spread < 2× | Re-discuss scope until agreed |
| Business rules confirmed | All `[TBD]` resolved | Confirm with PM/business, then dev |

**Dependency rules:**
- **Data dependency:** Story B needs data created by Story A → B depends on A
- **Interface dependency:** Story B calls API provided by A → B depends on A
- **No dependency:** Stories on different objects or different roles → parallel
- **Pseudo-dependency:** looks dependent but mockable → tag "Mockable to decouple"

## Step 5 — Output a Story Map

```markdown
## Epic: {requirement name}

### Story Map (user journey → Story mapping)

| Journey stage | Stories | Priority | Points |
|---|---|---|---|
| {stage 1} | US-001, US-002 | P0 | 5 |
| {stage 2} | US-003, US-004 | P1 | 8 |

### Sprint planning
- **Sprint 1 (MVP):** {Story list}, total {X} points
- **Sprint 2:** {Story list}, total {X} points

### Dependencies
US-001 → US-003 → US-005 (must follow this order)
US-002, US-004 (parallel)
```

## Quality bar

1. Every Story passes all six INVEST checks
2. AC uses Given-When-Then with ≥ 1 happy + ≥ 1 exception
3. Dependencies tagged explicitly, with mockability flagged
4. 13-point Stories must be re-split
5. Story Map includes Sprint planning suggestion

## When input is incomplete

- **One-sentence requirement** → first output a feature outline, confirm scope, then split
- **Too large (> 20 Stories)** → recommend splitting into Epics; agree on MVP scope first
- **Missing business rules** → tag `[business rule TBD]` and propose plausible assumptions for confirmation

## Related skills

- `/pm-prd` — write a PRD first to lock scope, then break into Stories
- `/pm-prioritize` — when there are many Stories, RICE-rank for Sprint priority

