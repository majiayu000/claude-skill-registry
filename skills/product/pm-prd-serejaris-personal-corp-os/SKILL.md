---
name: pm-prd
description: Генерирует структурированный PRD (Product Requirements Document) с шаблонами под тип продукта (B2C / B2B / внутренний инструмент / платформа) — фон, цели, детальный дизайн фич, acceptance criteria в Given-When-Then, аналитика и 10-пунктовый чеклист качества. User-invoked only — do NOT auto-trigger. Triggers on /pm-prd, "сделай PRD", "напиши PRD", "продуктовые требования", "make a PRD", "write a PRD", "draft requirements doc".
---

# pm-prd — Generate a structured PRD


Part of the Personal Corp framework — running a one-person business through AI agents.
Generate a delivery-ready Product Requirements Document from a feature description. Branches by product type — B2C, B2B, internal tool, platform — with each type emphasizing different modules. Includes a 10-item quality self-check that runs after generation.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Feature description | yes | What the feature does and what problem it solves; one sentence minimum |
| Target user | no | Who it's for; inferred from the feature if not given |
| Business goals | no | Expected business metrics (DAU, conversion, revenue, etc.) |
| Product type | no | B2C / B2B / internal / platform; auto-detected if not given |
| Constraints | no | Tech limits, deadlines, resource limits |
| Depth | no | Outline (for review) / detailed (for development); default detailed |

If the user only says "write a PRD" with no feature, ask for the feature description. If they give feature + user + goals, go straight to generation.

## Step 1 — Parse input and branch by product type

| Product type | PRD emphasis | Key differentiators |
|---|---|---|
| **B2C** | UX flow, growth metrics, A/B test plan | Heavy on interaction, heavy on data, write user journeys |
| **B2B** | Permission model, multi-tenancy, SLA, integration APIs | Heavy on completeness, security, API contracts |
| **Internal tool** | Operational efficiency, integration with existing systems, training cost | Heavy on practicality, light on visuals |
| **Platform** | Multi-role interaction, supply-demand matching, ecosystem rules | Heavy on role separation, rules engine |

**Auto-detection rules:** mentions of "user / member / loyalty / marketplace" → B2C; "enterprise / SaaS / CRM / admin panel" → B2B; "internal / management system / ticketing" → internal tool; "platform / marketplace / two-sided" → platform.

**B2B PRDs must additionally cover:**
- Permission matrix (role × feature × data scope)
- Multi-tenant data isolation approach
- Integration interfaces with the customer's existing systems

**Platform PRDs must additionally cover:**
- Independent feature view per role (supplier / consumer / platform ops)
- Matching rules and ranking strategy
- Commission / take-rate / settlement rules

## Step 2 — Structured requirement breakdown

**Three-method feature decomposition:**

1. **User journey:** trace the user's path from entry to goal completion; each node = one feature point
2. **Role split:** list every role involved (end user, admin, ops); each role's actions = one feature module
3. **CRUD:** for each core data object, walk through create / read / update / delete

For every feature module, fill:

- Feature description (one sentence)
- User story (As a {role}, I want to {action}, so that {value})
- Business rules (exhaustive — no "etc." or "other cases")
- Interaction (entry point → steps → success/failure feedback)
- Exception handling (timeouts, data anomalies, permission denied, edge cases)

## Step 3 — Generate the PRD

Use this template. Comments next to each placeholder describe the fill logic.

```markdown
# PRD: {feature name}

**Version:** v1.0
**Author:** {PM name, or [TBD]}
**Date:** {today}
**Status:** Draft

---

## 1. Background and Goals

### 1.1 Background
<!-- Answer three questions: why now? what happens if we don't? what changes if we do? -->
{problem state + user pain + why this is the right moment}

### 1.2 Target users
<!-- Use [role] + [trait] + [scenario]. Never write "all users". -->
| User role | Trait | Core need | Use scenario |
|---|---|---|---|

### 1.3 Business goals and success metrics
<!-- Each goal must be SMART — specific number + deadline. -->
| Goal | Metric | Target | Tracking method |
|---|---|---|---|

## 2. Requirement Overview
<!-- One paragraph, 30 words max, summarizing the core requirement. -->

## 3. Detailed Feature Design

### 3.1 {Module 1}
**Description:** {what it does}
**User story:** As a {role}, I want {action}, so that {value}
**Priority:** P0 (must launch) / P1 (strongly recommended) / P2 (nice-to-have)

**Business rules:**
1. {rule 1 — clear trigger condition + processing logic}
2. {rule 2}

**Interaction flow:**
<!-- Start at entry point, end at task completion, cover happy path + exception branches. -->
1. User enters from {entry}
2. {steps}
3. Success: {feedback}
4. Failure: {error message and handling}

**Exception handling:**
| Scenario | Handling | User-facing message |
|---|---|---|

(repeat format for each module)

## 4. Non-Functional Requirements
<!-- B2C → emphasize performance and experience; B2B → emphasize security and availability. -->
| Category | Requirement | Acceptance criterion |
|---|---|---|
| Performance | {e.g. page load time} | {e.g. < 2s} |
| Security | {e.g. data encryption} | {e.g. TLS 1.2+ in transit} |
| Compatibility | {browsers / devices} | {Chrome, Safari, mobile webview} |

## 5. Data Requirements (Analytics Events)
<!-- List every event to capture. Format: event name + trigger + attributes + purpose. -->
| Event | Trigger | Key attributes | Purpose |
|---|---|---|---|

## 6. Acceptance Criteria
<!-- At least 3 ACs per feature module, in Given-When-Then format. -->
| ID | Scenario | Given | When | Then |
|---|---|---|---|---|

## 7. Schedule
<!-- Break into design / dev / integration / launch. -->
| Phase | Estimate | Dependency | Risk |
|---|---|---|---|

## 8. Risks and Dependencies
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|

## Appendix
- Related documents
- Competitor references
- Design files
```

## Step 4 — Quality self-check

Run this 10-point checklist after generating. Flag any failed item with a fix suggestion.

| # | Check | Pass criterion |
|---|---|---|
| 1 | Background not vague | Answers "why do this?" not just "we need to do this" |
| 2 | Goals quantified | At least one numeric success metric |
| 3 | Personas concrete | No "all users" / "everyone" |
| 4 | Business rules exhaustive | No "etc.", "other cases", "and so on" |
| 5 | Exception flows covered | Every feature has ≥2 exception scenarios |
| 6 | Acceptance testable | Given-When-Then format used |
| 7 | Analytics complete | All core action paths have events |
| 8 | No tech implementation | PRD describes "what", not "how to build" |
| 9 | Priorities assigned | Every module tagged P0/P1/P2 |
| 10 | Schedule grounded | Estimate covers design + dev + test + integration |

## Common PRD anti-patterns

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| **Gold-plating** | 50 features in v1 | Split MVP / v1.1 / v2; v1 keeps 3-5 core features |
| **Fake requirement** | "Users might want…" with no data | Tag every requirement with source: feedback / analytics / competitor / hypothesis |
| **Design overreach** | PRD specifies button color, font size, layout | Describe info hierarchy and interaction logic only; visuals → designer |
| **Tech overreach** | PRD specifies Redis, MySQL, framework choice | Describe perf requirements (e.g. "<2s") only; implementation → engineering |
| **Rule blackhole** | "Per business rules" without listing them | Enumerate every rule's trigger, logic, edge values |

## Red lines

1. **PRD does not specify implementation** — no DB type, language, framework
2. **PRD does not replace design specs** — no detailed UI layout, colors, sizes
3. **No fabricated data** — for any business data the user didn't provide (DAU, conversion), write `[TBD]`
4. **No missing roles** — for multi-role features, every role's perspective must be covered

## When input is incomplete

- **Just "write a PRD"** with no requirement → ask for the feature description with an example
- **One-sentence requirement** ("build a marketplace") → produce an outline-level PRD framework, mark `[needs input]` on critical missing pieces
- **Requirement too large** → suggest splitting into multiple PRDs; agree on MVP scope first

## Related skills

- `/pm-user-stories` — after PRD review, break features into developable User Stories
- `/pm-competitive` — run before PRD to gather competitor references
- `/pm-prioritize` — when multiple requirements compete, rank with RICE first

