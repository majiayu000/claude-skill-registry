---
name: phase4-spec
description: The Mileva Method (CRISP) — Phase 4: Spec. Full implementation readiness package including solution design, UX direction, tech stack, backlog, MVP prioritization, risk assessment, and AI architecture for Claude Code projects — CLAUDE.md, skill mapping, AI specs, sprint planning, quality gates. Triggers on "spec", "phase 4", "build ready", "implementation plan", "CLAUDE.md", "sprint planning", "backlog", "AI spec", or after Phase I exit checklist is complete.
---

## Pacing Rule — One Section at a Time

> Present one section, deliverable, or elicitation move at a time.
> After presenting — stop. Wait for the client to respond.
> Do not pre-fill and present multiple sections in one message.
> Do not move to the next step until the client confirms, corrects, or gives a clear go-ahead.
>
> The goal is a conversation, not a document dump.
> If you've written more than one section without a client response in between — you've gone too far.

---


# S — Spec: Implementation Readiness

You are not building the thing. You are making the builder ready to build.

## Project State

> At the start of Phase S: read `docs/crisp-state.json`. Check phases C, R, and I are complete. Use `project`, `phases.C`, `phases.R`, `phases.I` fields to orient before reading other docs. Pay attention to: `project.agentInScope`, `project.memoryOwnershipRequired`, `phases.I.dataMappingRequired`, `phases.I.uxDiscoveryRequired`.
>
> At the end of Phase S (before exit checklist): update `docs/crisp-state.json`:
> - Set `phases.current` to `"P"`
> - Add `"S"` to `phases.complete`
> - Set `phases.S.complete` to `true`
> - Fill `phases.S.stack` (harness, harnessOpen, memoryOwner, layers)
> - Fill `phases.S.mvpLine`, `phases.S.sprintCount`, `phases.S.sprints`
> - Set `phases.S.analyticsRequired` and `phases.S.landingPageRequired`
> - Add any unresolved items to `phases.S.openQuestions`

**Output: a package a developer can read on Monday and start building on Tuesday.**

---

## Before You Start — Read These

All filled project documents live in `docs/`. Read from there, not from the blank `/templates/` folder.

| File | What to extract |
|---|---|
| `docs/problem-statement.md` | Core problem, constraints, Go/No-Go rationale |
| `docs/stakeholder-register.md` | Who is impacted, what they need, human-in-the-loop zones |
| `docs/success-metrics.md` | Baseline measurements, success targets, second-order effects — used for MVP criteria and risk context |
| `docs/market-research.md` | Competitor must-haves, USP, feature gaps (external projects only) |
| `docs/swot.md` | Strengths to lean into, threats to design around (external projects only) |
| `docs/buy-vs-build-matrix.md` | Which tools are bought/configured vs built — informs tech stack |
| `docs/value-proposition-canvas.md` | USP and positioning — shapes UX and feature priority |
| `docs/user-journey-map.md` | Flows per user type — feeds UX spec directly |
| `docs/ux-discovery.md` | Visual direction, navigation pattern, high-stakes screens, friction/delight — **mandatory for UI/Mobile/Web; if missing, return to Phase I** |
| `docs/process-flow.md` | Step-by-step logic — feeds agent architecture |
| `docs/project-goals.md` | Goals and success criteria — every epic must link to one |
| `docs/integration-map.md` | Every external system — direction, trigger, data in/out, format — **source of truth for all integration specs** |
| `docs/data-flow.md` | Full system data pipe — confirmed by client in Phase I |

> **If `docs/ux-discovery.md` does not exist and this is a UI/Mobile/Web project: stop. Go back to Phase I and run the UX Discovery section (3A–3E) before continuing.**

Nothing in Phase S should contradict what was agreed in Phases C, R, and I. If a conflict arises — surface it, resolve it, update the source file.

---

## 4A: Solution Design

**UX/UI Direction**

Three artifacts, in this order:

1. **Design System** → `docs/design-system.md`
   - Pull design philosophy and audience fit from `docs/ux-discovery.md` (3A: mental models, use context)
   - Pull visual direction and references from `docs/ux-discovery.md` (3B: proposed direction, client refs, non-negotiable feeling)
   - Cognitive & behavioral UX principles (reference layer + per-screen checklist)
   - Color palette, typography, shape language, motion, iconography, spacing — grounded in 3B
   - Challenge any client-provided references that conflict with the target user (use 3A mental model as the test)

2. **Sitemap** → `docs/ux-spec.md` (Part 1)
   - Pull navigation pattern decision from `docs/ux-discovery.md` (3C) — this is already decided, do not re-open it
   - Pull user types from `docs/stakeholder-register.md`
   - Every screen and its place in the navigation structure

3. **UX Spec** → `docs/ux-spec.md` (Parts 2–3)
   - Pull flows directly from `docs/user-journey-map.md`
   - Flow spec first: user goal, entry/exit, flow map, success/failure states
   - For high-stakes screens (from `docs/ux-discovery.md` 3D): lead with the target emotion and primary action before speccing UI elements
   - For friction points (from `docs/ux-discovery.md` 3E): the design response is the spec direction — use it
   - Screen spec: information architecture, UI elements, states, user actions
   - Cognitive UX checklist applied to every screen

> **Rule:** Write flows before screens. Flows reveal intent; screens are the implementation.

---

## 4B: Tech Stack + NFRs + 3rd Party Integration Trigger

### Tech Stack Proposal

Document every layer of the stack with the **exact pinned version** in use. Do not write "latest" — Claude will default to its training data, which may be outdated or mismatched.

| Layer | Tool | Pinned version | Notes |
|---|---|---|---|
| | | e.g. 18.2.0 | |

**Version rules Claude must follow (copy these into CLAUDE.md):**
- Use only the versions listed in the tech stack table. Do not upgrade silently.
- If a library's documented API differs from what you know — trust the pinned version, not your training data.
- If a version conflict arises during build, stop and flag it. Do not resolve silently.
- If a package requires a peer dependency at a specific version, list that peer dependency here too.

**Flag known breaking changes at proposal time:**
When proposing the stack, explicitly call out major version breaking changes relevant to this project. Do not let these surface mid-sprint. Common ones to check:
- React 18 — concurrent mode, new root API (createRoot vs ReactDOM.render)
- Next.js 13+ — App Router vs Pages Router are fundamentally different conventions
- Expo SDK upgrades — frequently break native modules; check release notes before pinning
- Supabase JS v1 → v2 — auth API changed significantly (createClient, session handling)
- Node 16 → 18 → 20 — native fetch, ESM defaults, breaking crypto changes

Present the stack with versions and flag breaking changes before confirming:
> "Here's the proposed stack with pinned versions: [table]. Worth flagging: [relevant breaking changes for this project]. Does anything conflict with existing code or infrastructure you already have?"

Confirm versions with the client before writing a single line of code. Save the pinned version table to CLAUDE.md immediately — it is the version source of truth for every sprint.

- Justify every choice against constraints in `docs/problem-statement.md` (budget, time, legal, tech)
- Cross-check `docs/buy-vs-build-matrix.md` — already-decided tools go here, not up for debate again
- Prefer existing libraries and open source when time or budget is constrained


### Open Source Library Research — mandatory for every dependency

> Claude's training data has a cutoff. A library that was "actively maintained" in training may have had zero commits in 18 months. One search prevents months of dependency debt.

For every open source library in the tech stack, run this evaluation before confirming the choice:

**Step 1: Search**
Search GitHub: `[what you need] github library` (e.g. "pdf export github library", "react data table github")
Evaluate the top 3–5 results.

**Step 2: Score each candidate**

| Criteria | What to check |
|---|---|
| ⭐ Stars | Community signal — >500 for a production dependency |
| 🍴 Forks | Active derivative use — meaningful number relative to stars |
| 📅 Last commit | Must be within 6 months for active maintenance |
| 🐛 Issues | Open/closed ratio — high open, low closed = warning sign |
| 📖 Documentation | Is it actually usable from docs alone? |
| ⚖️ License | MIT/Apache-2.0/BSD = free for commercial. GPL = check carefully. |
| 👥 Contributors | Solo maintainer = higher bus factor risk |

**Step 3: Record decision**

Add to the tech stack table:
- Chosen library with pinned version
- Why it was chosen over the alternatives (1 sentence)
- Alternatives considered and why they were rejected

> Present to client if the choice is non-obvious:
> "I evaluated [A], [B], and [C] for [use case]. I'm recommending [A] — [stars], last commit [date], [license]. [B] was last updated [date] so I ruled it out. Agree?"


**API Key & Secrets Rules — non-negotiable, copy into CLAUDE.md:**
- **Never expose API keys, tokens, or secrets on the client side.** No exceptions. Not in React components, not in frontend env vars prefixed with `NEXT_PUBLIC_`, not in mobile app bundles.
- All calls to 3rd party APIs that require credentials must be made server-side (API route, Edge function, backend service).
- The client-side calls your server. Your server calls the 3rd party. The secret never leaves the server.
- Wrong: `fetch('https://api.stripe.com/...', { headers: { Authorization: process.env.NEXT_PUBLIC_STRIPE_KEY } })` in a React component.
- Right: `fetch('/api/stripe/charge', { body: JSON.stringify(payload) })` → server-side API route handles the Stripe call with `process.env.STRIPE_SECRET_KEY`.
- Every secret goes into `.env.local` (or equivalent) — verified in `.gitignore` before first commit.

---

### Non-Functional Requirements — Elicit and Document

> NFRs are project-wide constraints. Capture them once here, before sprint planning begins.
> They go into `CLAUDE.md` and are referenced by every sprint that touches the relevant layer.
> Do not leave these as assumptions — a wrong default causes rework in production.

> **The Djokovic principle:** Novak Djokovic wins by being the best-conditioned player on the court, not the flashiest. Pinned versions, NFRs, and security defaults are conditioning. Nobody cheers for them. The client never asks about them. They're exactly why you don't collapse in week 8 when production goes down and you're staring at an unencrypted database and an API key committed to a public repo.

Pre-fill what you can from `docs/problem-statement.md` (constraints) and `docs/stakeholder-register.md` (compliance, data sensitivity). Then elicit the rest with these questions:

**Availability & Performance**
> "What's the acceptable downtime for this product? Business-critical (99.9%+ uptime) or is occasional downtime tolerable for MVP?"
> "Any known peak usage moments — an event, a campaign, end of month? How many concurrent users at max load?"

**Security**
> "Does any data in this system need to be encrypted at rest? In transit? I'll assume yes for both unless there's a reason not to — confirm?"
> "Who can access what? Are there roles with different data visibility, or flat access for all authenticated users?"

**Deployment & Infrastructure**
> "Should this be containerised with Docker? It makes deployment and environment parity much cleaner — any reason not to?"
> "Self-hosted or cloud? If cloud — any provider preference, or should I recommend based on the stack and budget?"
> "Any data residency requirement — does data need to stay in a specific country or region?" _(Cross-check with legal constraints in `docs/problem-statement.md`)_

**Reliability & Recovery**
> "If this goes down, what's the acceptable recovery time — hours, minutes? Do we need automated backups, and how often?"
> "Any monitoring and alerting expectations — proactive notification when something fails, or is reactive support fine for MVP?"

Save NFRs as an appended section in `docs/problem-statement.md` and reference them in `CLAUDE.md`.

---

### 3rd Party Integration Confirmation — mandatory step

> Phase I already produced `docs/integration-map.md` — every external system was identified and mapped there.
> This step confirms that list against the tech stack and writes the integration AI Specs. Do not discover integrations here. If something appears in the tech stack that isn't in the integration map — stop, go back, and update `docs/integration-map.md` first.

**Step 1: Cross-check tech stack against integration map**

Read `docs/integration-map.md`. For every external system listed there, verify it appears in the tech stack. For every external service in the tech stack, verify it appears in the integration map.

Any mismatch → resolve before continuing:
> "I see [service] in the tech stack but it's not in the integration map from Phase I. Before I write the spec — what data does it provide or receive, what triggers it, and in what format? Let's add it to the integration map now."

**Step 2: Check for unresolved open questions**

Open `docs/integration-map.md` and read the Open Questions section. Any unresolved questions must be answered before the integration AI Spec for that service is written. Do not write a spec against an unknown payload or trigger.

**Step 3: Write integration AI Specs**

For each confirmed integration:
1. Flag it in the tech stack table with tag `[INTEGRATION REQUIRED]`
2. Create a dedicated AI Spec → `docs/ai-spec-[service-name].md`
3. Pre-fill auth, endpoints, payload shapes, and DB mapping from `docs/integration-map.md` — this is already elicited, do not re-ask
4. Run the **Web Research Protocol** from `templates/ai-spec.md` — browse official dev docs to fill in anything not captured in Phase I (rate limits, error codes, pagination, SDK quirks)
5. Only ask the client for what neither the integration map nor the docs provide (credentials, account-specific config, sandbox access)

**Step 4: Sequence integration sprints**

Read the "Sprint dependency" column in `docs/integration-map.md`. Integration specs must be complete before any sprint that calls that API. Flag any sprint ordering conflicts now — do not let them surface during build.

These integration specs are prerequisites — they must be written before the sprint that uses the integration is planned.

---

## 4C: Project Foundation

---

### Initial Backlog — Pre-fill, Name-check, Confirm → `docs/initial-backlog.md`

**Pre-fill from existing docs:**

| Backlog section | Source |
|---|---|
| User types for stories | `docs/stakeholder-register.md` — system users only (not oversight stakeholders) |
| Epics | `docs/user-journey-map.md` — each major journey stage is an epic candidate; `docs/project-goals.md` — each goal must map to at least one epic |
| Feature scope | `docs/problem-statement.md` — what's in and out of scope; `docs/buy-vs-build-matrix.md` — what's being built vs bought |
| Out of scope / non-goals | `docs/project-goals.md` — non-goals; `docs/problem-statement.md` — explicit exclusions |
| 3rd party integrations | `docs/buy-vs-build-matrix.md` and tech stack decision from 4B |

**External product rule:** If `project.type === "external"` in `docs/crisp-state.json` — add a **Landing Page** epic to the backlog and tag it `MVP`. The landing page build is part of the launch, not a post-launch afterthought. The brief lives in `docs/landing-page-brief.md` (written in the Landing Page section below). Assign it to a sprint — typically Sprint 1 or a dedicated pre-launch sprint.

Draft full epics and user stories in "As a [user], I want to [action], so that [outcome]" format. Leave MVP tag column blank — filled in 4D.

Present with a naming check first:
> "Here are the epics I've drafted: [list]. Before we check completeness — does the naming match how your team actually talks about these? 'Report Lost Item' might be 'Create a Case' in your world. Let's get the language right before we go deeper."

Then completeness:
> "Anything missing, or anything here that doesn't belong?"

One round. Do not reopen scope discussions settled in Phase C.

---

### Assumptions Log — Pre-fill and Confirm → `docs/assumptions-log.md`

> An assumption is anything treated as true in prior phases without explicit confirmation. Surface them now — wrong assumptions are the #1 cause of project failure.

**Pre-fill by scanning all prior docs for implicit decisions:**

| Where to look | What to surface |
|---|---|
| `docs/problem-statement.md` | Constraints assumed (budget range, timeline, legal framework) |
| `docs/buy-vs-build-matrix.md` | Tools assumed available, costs assumed affordable |
| `docs/stakeholder-register.md` | User behaviour and adoption assumed |
| `docs/market-research.md` | Market size, competitor behaviour, user willingness to switch |
| `docs/process-flow.md` | Data availability, system access, API reliability assumed |
| `docs/ux-discovery.md` | User mental models and device usage assumed |
| Tech stack + NFRs (4B) | Third-party reliability, library support, hosting costs, uptime assumed |

Rate each assumption: **High** (wrong = project fails or pivots) / **Medium** (wrong = rework) / **Low** (wrong = minor adjustment).

Present for confirmation — the client didn't create these assumptions, you did:
> "Here are the assumptions baked into everything so far. The high-risk ones are [X and Y]. Do any of these look wrong to you?"

Flag invalidated assumptions immediately and resolve before proceeding.

---

### Risk Assessment — Pre-fill, Elicit hidden risks, Confirm → `docs/risk-assessment.md`

**Pre-fill from existing docs:**

| Risk category | Source |
|---|---|
| Business risks | `docs/swot.md` — threats (external); `docs/problem-statement.md` — constraints |
| Technical risks | `docs/buy-vs-build-matrix.md` — build complexity; `docs/assumptions-log.md` — high-risk technical assumptions; tech stack from 4B |
| Legal / compliance | `docs/problem-statement.md` — legal constraints; `docs/stakeholder-register.md` — GDPR/HIPAA/data residency |
| Security | Data types from `docs/stakeholder-register.md` and `docs/process-flow.md`; NFRs from 4B; auth approach from tech stack |
| People / adoption | `docs/stakeholder-register.md` — stakeholders with neutral or negative impact |
| Human-in-the-loop zones | `docs/stakeholder-register.md` — HITL flags from Phase R; `docs/process-flow.md` — decision points |

Draft all risks with likelihood, impact, mitigation, and owner. Pre-fill HITL zones from Phase R — don't reinvent them.

Then elicit what docs can never capture — context the client carries in their head:
> "Here's the risk register. I've covered the standard bases. But what keeps you up at night about this project that I haven't listed? A vendor relationship, a team dynamic, a deadline tied to something external — anything that would make this harder than it looks on paper?"

Add what they surface. One round. Lock it.

---

## 4D: MVP Prioritization — HVLE Conversation

> **Stop. Do not write sprint plans yet. This step requires a live conversation with the client.**
> The HVLE scoring is not a background calculation — it is a structured elicitation. Run it now.
> Full scoring logic lives in `mvp-prioritization.md` — read it before starting.

---

### Step 1: Lock MVP-BASELINE (no scoring needed)

Before any HVLE scoring, identify the non-negotiables. These bypass the scoring model entirely.

Pull from `docs/market-research.md`:
- **Must-haves** — features every competitor has; users expect them as table stakes
- **USP features** — the thing that makes this product worth choosing over alternatives

Present them to the client:
> "Before we score anything, let me lock the floor. These features go in MVP regardless of score — every competitor has them, and our USP lives here. Does this list look right, or is anything missing?"

Get confirmation. Mark these `MVP-BASELINE` in `docs/initial-backlog.md`. Do not re-debate them.

---

### Step 2: Elicit Business Value Criteria

Pre-fill 3–4 criteria based on project context (pull from `docs/project-goals.md`, `docs/success-metrics.md`, and `docs/stakeholder-register.md`), then present them for correction — don't ask open-ended questions.

For **external products**, default criteria are:
- Customer acquisition
- User activation / adoption
- Retention / engagement
- Revenue generation
- Referral / virality

For **internal tools**, default criteria are:
- Cross-company process adoption
- Time saved per user per week
- Error / rework reduction
- Employee satisfaction
- Compliance / risk reduction

Say this:
> "I've assumed the outcomes that matter most here are [X, Y, Z]. Does that feel right, or am I optimizing for the wrong thing? We need max 5 — if you want to add one, we cut one."

**Hard limit: 5 criteria.** If they want more, help them consolidate. More than 5 and everything starts scoring the same.

---

### Step 3: Weight the Criteria

Once criteria are agreed, get weights. Do not skip this — unweighted scoring treats every criterion as equal, which is almost never true.

> "Now give each one a weight from 1 to 3. Think of it as: 3 = if we nail this, everything else follows. 1 = nice to track, but it's not what this lives or dies on."

Present the weighted criteria back for confirmation before scoring.

---

### Step 4: Score the Backlog Together

Take every feature from `docs/initial-backlog.md` (excluding MVP-BASELINE items) and score them against each criterion (1–5). For each feature:
- 5 = directly and strongly drives this outcome
- 3 = contributes, but not the whole story
- 1 = barely connected — we're reaching

Walk the client through scores for any non-obvious features. Don't silently assign scores — show your reasoning and invite correction.

**Priority Score = Business Value Score ÷ Effort Value**

Effort sizing (T-shirt):
| Size | Days | Effort Value |
|---|---|---|
| XS | < 1 day | 0.5 |
| S | 1–2 days | 1.5 |
| M | 3–5 days | 4 |
| L | 7–10 days | 8.5 |
| XL | 10+ days | 12 |

---

### Step 5: Apply Dependency Overrides

After scoring, check for features that scored low but are required by high-scoring ones.

> "Feature [X] scored lower on its own, but [Y] sits on top of it — so [X] moves into MVP as a dependency. We don't get a choice here."

Mark blockers as `DEPENDENCY`. Adjust the MVP line to include all required foundations.

---

### Step 6: Draw the MVP Line with the Client

Sort features by Priority Score (descending): MVP-BASELINE first, then scored features high→low, dependencies resolved.

Present the ranked list and propose where to draw the line:
> "Here's the ranked list. I'd draw the line here — everything above ships in MVP. Before you agree, ask yourself three things: Can someone actually use this and get value from it with only these features? Does it deliver our USP? Can we build it in the time we have?"

All three must be yes. If not — something's missing or the scope is too big. Adjust together.

---

### Step 7: Tag and Save

Tag every feature:
- `MVP-BASELINE` — table stakes or USP, non-negotiable
- `MVP` — scored, above the line
- `POST-MVP` — scored, below the line (not never — just not now)
- `DEPENDENCY` — required by an MVP feature, regardless of own score

Save scoring output → `docs/mvp-prioritization.md`
Update tags in → `docs/initial-backlog.md`

Only after this is complete: proceed to 4E and sprint planning.

---

## 4E: AI Architecture (Claude Code Projects)

This is the layer between "we know what to build" and "Claude Code starts building."
Most AI implementations fall apart here. Don't skip it.

---

### CLAUDE.md

Compile from ALL `docs/` files → `CLAUDE.md` in project root.
- Problem statement, constraints, goals, success metrics, tech stack, NFRs, agent map, env vars master list
- Include the CRISP Output Manifest (see Phase 4 Outputs below) so Claude always knows what docs exist
- This is what Claude reads at the start of every session — make it complete and current

> **Gostoprimstvo.** Serbian hospitality — you don't send a guest away hungry or confused. CLAUDE.md is the welcome you give to every new Claude Code session. A half-empty CLAUDE.md is like handing someone the keys to a house and not telling them where the light switches are. Every missing field is a guess Claude will make for you — and you won't like all the answers.

---

### Skill / Agent Architecture

- Pull process steps from `docs/process-flow.md` — each major step is a candidate agent
- For each agent: define responsibilities, inputs, outputs, and boundaries
- Map handoffs between agents
- Write one `SKILL.md` per agent into the project's `skills/` folder using `templates/agent-skill.md`

---

### AI Spec — Pre-fill, Generate Open Questions, Confirm (one per sprint / feature)

> Do not hand a sprint to Claude Code with a blank spec or unresolved questions.
> Pre-fill everything derivable, generate sprint-specific open questions, resolve them with the client, then lock.
> Save each spec to `docs/ai-spec-[sprint-or-feature-name].md`

**Step 1: Pre-fill from existing docs**

| Spec section | Source |
|---|---|
| Context (why this feature exists) | `docs/project-goals.md` — which goal it serves; `docs/problem-statement.md` — the problem it solves |
| Scope — In | User stories tagged to this sprint in `docs/initial-backlog.md` |
| Scope — Out | `docs/project-goals.md` — non-goals; `docs/initial-backlog.md` — POST-MVP items |
| Inputs | `docs/user-journey-map.md` — what the user brings; `docs/process-flow.md` — what data flows in |
| Outputs | `docs/user-journey-map.md` — what the user gets; `docs/process-flow.md` — what moves downstream |
| Business logic / rules | `docs/process-flow.md` — decision points; `docs/stakeholder-register.md` — HITL zones |
| Edge cases | `docs/assumptions-log.md` — high-risk assumptions; `docs/risk-assessment.md` — relevant risks |
| NFR references | `docs/problem-statement.md` NFR section — which NFRs apply to this sprint |
| 3rd Party Integrations | `docs/buy-vs-build-matrix.md` and 4B tech stack — only for sprints that call those APIs |
| Environment variables | 4B tech stack; prior integration AI specs |
| Test requirements | `docs/process-flow.md` — success condition per process step in sprint scope; acceptance criteria from user stories |

**Step 2: Generate sprint-specific open questions**

After pre-filling, read the sprint's user stories and process-flow steps and ask: *"What would a developer need to know that isn't written down yet?"*

Use these category prompts to generate questions — only include categories relevant to what this sprint builds:

| Sprint touches… | Questions to generate |
|---|---|
| **Auth / Identity** | Session expiry? What happens on expiry — logout or silent refresh? MFA required? Social login providers? Password reset — link or code? |
| **File / Media handling** | Max file size? Allowed types? Storage location — cloud bucket, local, CDN? Original preserved or processed version only? Who can access uploaded files? |
| **Background jobs / Async** | What triggers the job — event, schedule, or manual? Retry on failure? Max retries? Dead letter queue? Does the user need feedback on completion? |
| **Real-time / Live updates** | WebSockets or polling? Fallback if connection drops? Are updates persistent (stored) or ephemeral (lost on refresh)? |
| **Notifications (push / email / SMS)** | Which events trigger a notification? User-configurable or always-on? Opt-out mechanism required? |
| **Payments / Financial** | Which payment provider? Sandbox credentials available? Refund logic — automatic or manual? Currency and locale handling? |
| **Search / Filtering** | Full-text or filtered? Server-side or client-side? Indexed or real-time? Results ranking logic? |
| **Roles / Permissions** | Which roles exist in this sprint? What can each role see/do/not do? Who can promote or revoke roles? |

Save generated questions as an **Open Questions** section at the bottom of the AI Spec.

> All open questions must be answered before the spec is locked and the sprint begins.
> A spec with unresolved questions is not a spec — it's a wishlist.

**Step 3: Resolve and confirm**

Present the pre-filled spec and open questions together:
> "Here's the spec for Sprint [N] — [goal]. I've pre-filled everything from our docs. At the bottom are [N] open questions specific to what this sprint builds — we need to answer these before Claude Code starts. Want to go through them now?"

Work through the questions. Fill answers into the spec. One round. Lock it. No changes mid-sprint.

---

### Sprint Planning → `docs/sprint-plan.md`

- MVP-tagged features feed Sprint 1+. Post-MVP feeds later sprints.
- Use dependency map from `docs/mvp-prioritization.md` to sequence sprints correctly
- Each sprint = a clear, bounded, testable unit of work
- Integration AI specs must be complete before any sprint that calls that API

---

### Quality & Safety Gates (per sprint)

- Deployment checklist: dependencies resolved, env vars clean, no secrets in code
- Security review before each deploy — cross-check NFRs from 4B
- PR review standards defined
- Guardrail validation: hallucination risks, output validation, fallback logic

**Unit Tests — mandatory on every sprint:**

Tests are not optional and not an afterthought. They are part of the sprint scope. Estimate test writing time alongside feature development — not separately.

Rules for Claude Code (copy these into CLAUDE.md via `templates/CLAUDE.md`):
- Write unit tests for every function and feature in scope before marking sprint done
- Run the full test suite before every commit — if a test fails, fix it before committing; do not skip
- After every run, append an entry to `docs/test-log.md`: sprint, date, each test in plain English, ✅/❌, and for any failure — what was wrong and how it was fixed
- Test descriptions must be plain English: "Slack notification sends when HeyReach campaign receives a reply" — not "test_fn_returns_200"

**Pre-filling test requirements in the AI Spec:**

For each sprint's AI Spec, pre-fill the Test Requirements section from:
1. `docs/process-flow.md` — every process step in scope has a success condition; each becomes a required test
2. Acceptance criteria from the sprint's user stories in `docs/initial-backlog.md`
3. Edge cases from `docs/assumptions-log.md` and `docs/risk-assessment.md`

> For non-technical clients: the test log is their window into whether the system is actually working. Write it so they can read it. "✅ Slack notification sent when HeyReach reply received — 2026-04-22 — Sprint 1" is useful. "PASS 47/47" is not.

**Security Scanning — Bearer (mandatory on every PR):**

Add [Bearer](https://github.com/bearer/bearer) to the CI pipeline. It scans for security vulnerabilities, secret leaks, and OWASP-class issues on every pull request.

Rules:
- **Critical or High severity finding** → block the PR. Do not merge. Notify the developer immediately with the finding and remediation path.
- **Medium severity** → flag in PR comments, require acknowledgement before merge.
- **Low / Informational** → log, do not block.

Setup (add to CI — GitHub Actions example):
```yaml
- name: Bearer Security Scan
  uses: bearer/bearer-action@v2
  with:
    severity: critical,high
    fail-on-severity: critical,high
```

If Bearer is not yet configured in the project, flag it as a setup task for Sprint 1 before any code ships.
If Bearer is not yet configured in the project, flag it as a setup task for Sprint 1 before any code ships.

---

### Logging Spec — mandatory for every project

> Logging is what tells you what happened when production breaks at 2am. Define it before the build, not after.

Write `docs/logging-spec.md` using `/templates/logging-spec.md`. This is a mandatory Phase S output — not optional.

Key decisions to make:
- Log levels per environment (production = INFO minimum, DEBUG off by default)
- What always gets logged: every API request, auth event, background job, unhandled exception, 3rd party call, critical DB write
- What never gets logged: passwords, API keys, secrets, PII (unless masked and compliance-required)
- Log format: structured JSON with `requestId`, `level`, `event`, `timestamp`
- Log destination: console (dev), file + aggregation service (production)

Reference `docs/logging-spec.md` in `CLAUDE.md` and in every sprint's AI Spec quality gates.

---

## Phase 4 Outputs

> All files go to `docs/` in the project root. Save as you go — do not batch at the end.
> The CLAUDE.md output manifest lists all expected files so nothing gets silently dropped.

| File | Contents | Required? |
|---|---|---|
| `docs/design-system.md` | Design philosophy, visual direction, color, type, motion, references | External UI/Mobile/Web only |
| `docs/ux-spec.md` | Sitemap + flow specs + screen specs with cognitive UX | External UI/Mobile/Web only |
| `docs/initial-backlog.md` | Full feature list with user stories, epic-to-goal links, MVP tags | Always |
| `docs/assumptions-log.md` | Logged assumptions and resolution status | Always |
| `docs/risk-assessment.md` | Risks, mitigations, security posture, legal/compliance, HITL zones | Always |
| `docs/mvp-prioritization.md` | HVLE scoring table, weighted criteria, priority scores, MVP line | Always |
| `docs/logging-spec.md` | Log levels, what to log, PII rules, format, destination, alerting | Always |
| `docs/analytics-spec.md` | GA4 setup, event map, conversion goals, PII rules, sprint gates | External products with UI only |
| `docs/landing-page-brief.md` | Hero copy, sections, CTAs, visual direction — compiled from all prior docs | External products only |
| `docs/agent-security.md` | Agent identity/permissions, data handling, failure modes | When agent is in scope |
| `docs/decisions.md` | Updated with Phase S decisions | Always |
| `docs/ai-spec-[name].md` | One per sprint — pre-filled, open questions resolved, locked | Always (one per sprint) |
| `docs/ai-spec-[service].md` | Integration spec per 3rd party service | Per integration |
| `docs/sprint-plan.md` | Sprint sequence, goals, features per sprint, quality gates | Always |
| `CLAUDE.md` | Compiled project context incl. NFRs — lives in project root, not docs/ | Always |
| `docs/test-log.md` | Running test record — appended after every run, plain English, all sprints | Always |

---

### Analytics Spec — External UI/Mobile/Web products

> Every success metric from Phase R needs a GA4 event that fires when it happens.
> If you're building a UI product and you don't define analytics before the build, you'll ship blind.

Write `docs/analytics-spec.md` using `/templates/analytics-spec.md`.

Key steps:
1. Pull every success target from `docs/success-metrics.md` — map each to a GA4 conversion event
2. Map all core user actions from `docs/user-journey-map.md` to events
3. Define parameters per event — what context is captured alongside the event name
4. Apply PII rules — no names, emails, or personal data in event parameters ever
5. Assign each event to the sprint that builds the relevant feature

Reference `docs/analytics-spec.md` in every sprint's AI Spec so Claude implements tracking for that sprint's features by default.

---

### Landing Page Brief — External products only

> By Phase S, you already have everything needed for a landing page: value prop, USP, target audience, visual direction, feature breakdown. Compiling it takes 20 minutes. Not compiling it means the client builds it from scratch with none of this context.

Write `docs/landing-page-brief.md` using `/templates/landing-page-brief.md`.

Pre-fill from:
- `docs/value-proposition-canvas.md` → hero headline, value prop, pain points
- `docs/market-research.md` → USP, target audience description
- `docs/ux-discovery.md` → visual direction, tone, non-negotiable feeling
- `docs/stakeholder-register.md` → who the page speaks to
- `docs/initial-backlog.md` → feature highlights (benefits framing, not feature list)

Present to client for one round of copy corrections before handing off.

> **MVP scope:** For external products, the landing page build is MVP — not a nice-to-have. It must already appear in `docs/initial-backlog.md` with an `MVP` tag (added during 4C) and have a sprint assigned in `docs/sprint-plan.md`.

---


### Agent Security Spec — when agent is in scope

> **Trigger:** If `docs/problem-statement.md` indicates an AI agent is in scope, this is a mandatory Phase S output.
> Do not start the sprint that builds the agent without a locked `docs/agent-security.md`.
>
> Aligned with AIUC-1 enterprise AI agent security standard.
> This is the spec-layer translation of what was elicited in Phase R agent permission scoping.

Write `docs/agent-security.md` using `/templates/agent-security.md`.

Pre-fill from Phase R:
- **Identity & Permissions** — from `docs/stakeholder-register.md` agent HITL/permissions section
- **Hard boundaries** — from Phase R "what the agent must never do" elicitation
- **Approval gates** — from Phase R gate conditions
- **Data handling** — from `docs/problem-statement.md` (PII/compliance constraints) + Phase R data sensitivity elicitation
- **Failure modes** — from Phase R failure behaviour elicitation

Then generate open questions for anything not covered in Phase R:
- Is the auth credential scoped to least privilege?
- Is there an audit trail for every agent action?
- Is the human fallback process documented and findable?
- Are all agent actions reversible, or are some irreversible — if irreversible, is there a gate?

Resolve all open questions before the sprint that builds the agent starts.

Add to `CLAUDE.md`:
- Agent security rules block (see CLAUDE.md template)
- Reference `docs/agent-security.md` in the output manifest

### Decision Logging — Phase S

> Update `docs/decisions.md` with decisions made in Phase S before closing.

**Log these decisions in Phase S:**
- **Tech stack choices** — every layer, why that tool, what was rejected and why
- **Open source library choices** — chosen library, alternatives evaluated, rationale
- **MVP line** — where it was drawn, what was pushed to post-MVP and why
- **NFR decisions** — uptime target, deployment approach, any tradeoffs
- **Harness choice** — open or closed, memory ownership decision if agent in scope


When all exit checklist items are checked and all AI Specs are locked, deliver this message:

---

**Your spec is complete. CRISP Phase S is done.**

Here's what's ready:
- Sprint plan → `docs/sprint-plan.md`
- AI Spec for Sprint 1 → `docs/ai-spec-[sprint-name].md`
- CLAUDE.md compiled → project root

**To start building right now, just say:**
> *"Start Sprint 1"*

Claude Code will read the AI Spec and begin. No new setup, no mode switching, no additional steps. The spec is the handoff.

If you want to review what's in scope for Sprint 1 first, check `docs/ai-spec-[sprint-name].md`. Everything the build needs is already in there.

---

## Exit Checklist

**Solution Design**
- [ ] UX discovery inputs read from `docs/ux-discovery.md` before any design work started
- [ ] Design system defined, visual direction grounded in ux-discovery → `docs/design-system.md`
- [ ] Sitemap complete, navigation pattern taken from ux-discovery (not re-decided) → `docs/ux-spec.md`
- [ ] UX spec written (flows + screens), high-stakes screens and friction points addressed → `docs/ux-spec.md`
- [ ] Tech stack proposed and justified against constraints in `docs/problem-statement.md`

**Tech Stack & Versions**
- [ ] Every layer of the stack has a pinned version — no "latest"
- [ ] Known breaking changes identified and flagged to client
- [ ] Pinned version table saved to CLAUDE.md with version rules
- [ ] Client confirmed versions don't conflict with existing code or infra
- [ ] Every open source library evaluated: stars, last commit, license, alternatives rejected with reason

**NFRs**
- [ ] Availability / uptime target defined
- [ ] Performance expectations set (concurrent users, response time)
- [ ] Security confirmed: encryption at rest + in transit, role-based access
- [ ] Deployment approach decided: Docker / containerised or not
- [ ] Cloud provider and region decided (data residency cross-checked)
- [ ] Backup, recovery, and monitoring expectations set
- [ ] NFRs saved to `docs/problem-statement.md` and referenced in `CLAUDE.md`

**Logging**
- [ ] Logging spec written → `docs/logging-spec.md`
- [ ] Log levels, format, destination, PII rules defined
- [ ] Logging spec referenced in `CLAUDE.md`

**3rd Party Integrations**
- [ ] `docs/integration-map.md` read — all Phase I integrations cross-checked against tech stack
- [ ] Any tech stack service not in integration map flagged and map updated before continuing
- [ ] All open questions in `docs/integration-map.md` resolved
- [ ] Every integration tagged `[INTEGRATION REQUIRED]` in tech stack table
- [ ] Integration AI Spec written per service → `docs/ai-spec-[service-name].md` (pre-filled from integration map)
- [ ] Auth, endpoints, payloads, DB mapping documented for each
- [ ] Integration sprint sequencing confirmed — integration specs complete before dependent sprints

**Foundation**
- [ ] Initial backlog pre-filled, naming confirmed with client → `docs/initial-backlog.md`
- [ ] Every goal in `docs/project-goals.md` has at least one epic
- [ ] Assumptions log pre-filled from all prior docs, high-risk items flagged, confirmed → `docs/assumptions-log.md`
- [ ] Risk assessment pre-filled, hidden risks elicited, confirmed → `docs/risk-assessment.md`
- [ ] Security and legal guardrails defined

**MVP Prioritization (HVLE)**
- [ ] MVP-BASELINE features locked (must-haves + USP) and confirmed with client
- [ ] Business value criteria defined (max 5) and confirmed with client
- [ ] Criteria weighted (1–3) by client
- [ ] All backlog features scored (1–5 per criterion) — reasoning shown to client
- [ ] Effort sized for every feature (XS/S/M/L/XL)
- [ ] Priority scores calculated (Business Value ÷ Effort)
- [ ] Dependencies mapped and overrides applied
- [ ] MVP line drawn and validated with client (all 3 questions answered yes)
- [ ] Scoring output saved → `docs/mvp-prioritization.md`
- [ ] Backlog updated with MVP / Post-MVP / Dependency tags → `docs/initial-backlog.md`

**AI Architecture**
- [ ] `CLAUDE.md` compiled from all `docs/` outputs — includes NFRs, logging spec, and output manifest
- [ ] Folder structure defined
- [ ] Agent/skill map complete — one `SKILL.md` per agent in project `skills/` folder
- [ ] AI Specs pre-filled, sprint-specific open questions generated and resolved → `docs/ai-spec-[name].md`
- [ ] No open questions remain in any locked spec
- [ ] Sprint plan sequenced using MVP prioritization + dependency map → `docs/sprint-plan.md`
- [ ] Quality gates defined per sprint (incl. logging gate)
- [ ] Test requirements pre-filled in every AI Spec from process-flow success conditions
- [ ] Test writing included in sprint effort estimates (not a separate afterthought)
- [ ] `docs/test-log.md` created from `templates/test-log.md`
- [ ] Testing rules block in `CLAUDE.md` — write tests, run before commit, append to test-log, plain English
- [ ] Integration specs completed before sprints that depend on them
- [ ] Key decisions logged → `docs/decisions.md`

**Analytics & Landing Page**
- [ ] **[External UI/Mobile/Web]** Analytics spec written → `docs/analytics-spec.md`
  - [ ] Every Phase R success metric mapped to a GA4 conversion event
  - [ ] All core user actions from journey map mapped to events
  - [ ] PII rules applied — no personal data in event parameters
  - [ ] Events assigned to sprints
- [ ] **[External product]** Landing page brief compiled → `docs/landing-page-brief.md`
  - [ ] Landing page epic added to `docs/initial-backlog.md` with `MVP` tag
  - [ ] Landing page sprint assigned in `docs/sprint-plan.md`

**Agent Security**
- [ ] **[Agent in scope]** Agent security spec written → `docs/agent-security.md`
  - [ ] Identity & permissions defined — what agent can/cannot do autonomously
  - [ ] Hard boundaries listed explicitly — what agent must never do
  - [ ] Approval gates defined with trigger conditions
  - [ ] Data handling rules set — PII, logging, retention
  - [ ] All failure modes defined with human fallback documented
  - [ ] Audit trail confirmed — every agent action is loggable
  - [ ] All open questions resolved before agent sprint starts
  - [ ] Agent security rules added to `CLAUDE.md`
  - [ ] Hero headline and value prop drafted
  - [ ] Pain points from VPC included
  - [ ] Visual direction from ux-discovery applied
  - [ ] Client reviewed and copy corrections made

**Progress Report**
- [ ] Progress report generated → `docs/progress-report-[YYYY-MM-DD].md` (optional — generate on request or before handoff)
