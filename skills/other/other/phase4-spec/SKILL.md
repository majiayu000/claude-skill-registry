---
name: phase4-spec
description: The Mileva Method (CRISP) — Phase 4: Spec. Full implementation readiness package including solution design, UX direction, tech stack, backlog, MVP prioritization, risk assessment, and AI architecture for Claude Code projects — CLAUDE.md, skill mapping, AI specs, sprint planning, quality gates. Triggers on "spec", "phase 4", "build ready", "implementation plan", "CLAUDE.md", "sprint planning", "backlog", "AI spec", or after Phase I exit checklist is complete.
---

# S — Spec: Implementation Readiness

You are not building the thing. You are making the builder ready to build.

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

### 3rd Party Integration Identification — mandatory step

> Every 3rd party service in the tech stack = a required integration AI Spec.

When finalizing the tech stack, explicitly list every external API, SaaS, or service being integrated (examples: Stripe, Garmin, Twilio, SendGrid, Google Maps, OpenAI, etc.).

For each one:
1. Flag it in the tech stack table with tag `[INTEGRATION REQUIRED]`
2. Create a dedicated AI Spec for it → `docs/ai-spec-[service-name].md`
3. Run the **Web Research Protocol** from `templates/ai-spec.md` — browse the official dev docs, extract auth, endpoints, payloads, response shapes, DB mapping
4. Only ask the client for what docs don't provide (credentials, account-specific config, sandbox access)

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
> Full scoring logic lives in `skills/phase4-spec/mvp-prioritization.md` — read it before starting.

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
- Unit test coverage requirements
- Guardrail validation: hallucination risks, output validation, fallback logic

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
| `docs/ai-spec-[name].md` | One per sprint — pre-filled, open questions resolved, locked | Always (one per sprint) |
| `docs/ai-spec-[service].md` | Integration spec per 3rd party service | Per integration |
| `docs/sprint-plan.md` | Sprint sequence, goals, features per sprint, quality gates | Always |
| `CLAUDE.md` | Compiled project context incl. NFRs — lives in project root, not docs/ | Always |

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

**NFRs**
- [ ] Availability / uptime target defined
- [ ] Performance expectations set (concurrent users, response time)
- [ ] Security confirmed: encryption at rest + in transit, role-based access
- [ ] Deployment approach decided: Docker / containerised or not
- [ ] Cloud provider and region decided (data residency cross-checked)
- [ ] Backup, recovery, and monitoring expectations set
- [ ] NFRs saved to `docs/problem-statement.md` and referenced in `CLAUDE.md`

**3rd Party Integrations**
- [ ] Every 3rd party service in tech stack identified and tagged `[INTEGRATION REQUIRED]`
- [ ] Integration AI Spec written per service → `docs/ai-spec-[service-name].md`
- [ ] Auth, endpoints, payloads, DB mapping documented for each

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
- [ ] `CLAUDE.md` compiled from all `docs/` outputs — includes NFRs and output manifest
- [ ] Folder structure defined
- [ ] Agent/skill map complete — one `SKILL.md` per agent in project `skills/` folder
- [ ] AI Specs pre-filled, sprint-specific open questions generated and resolved → `docs/ai-spec-[name].md`
- [ ] No open questions remain in any locked spec
- [ ] Sprint plan sequenced using MVP prioritization + dependency map → `docs/sprint-plan.md`
- [ ] Quality gates defined per sprint
- [ ] Integration specs completed before sprints that depend on them
