---
name: phase3-investigate
description: The Mileva Method (CRISP) — Phase 3: Investigate. Process mapping for existing or greenfield processes, user journey mapping, UX discovery, project goals, system architecture (integration map + data flow). Use after outcome alignment. Triggers on "investigate", "phase 3", "map the process", "process mapping", "user journey", "as-is process", or after Phase R exit checklist is complete.
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


# I — Investigate: Process Understanding

Map what exists (or what should exist) before designing a solution.

## Project State

> At the start of Phase I: read `docs/crisp-state.json`. Check phases C and R are complete. Use `project.type`, `phases.R.hitlZones`, `phases.R.stakeholders` for context.
>
> At the end of Phase I (before exit checklist): update `docs/crisp-state.json`:
> - Set `phases.current` to `"S"`
> - Add `"I"` to `phases.complete`
> - Set `phases.I.complete` to `true`
> - Fill `phases.I.processTrack`, `phases.I.userTypes`, `phases.I.dataMappingRequired`, `phases.I.uxDiscoveryRequired`, `phases.I.navigationPattern`
> - Add any unresolved items to `phases.I.openQuestions`

## Two Tracks

### Track A: Existing Process (Automation)
Shadow the actual person doing the work. Step by step, no skipping.
- What tool is open at each step?
- What is copied, pasted, where does it go?
- What decisions are made manually and why?
- Where do errors happen? Where do things slow down?
- Every tab, every click, every "and then I just..."

> Goal: expose the real process, not the documented one. They are always different.

> **War story:** Client wanted drag-and-drop category sorting for her e-commerce shop. A week of dev work, minimum. I asked why. "I just want to change the order for the season." I asked how she wanted to reorder it. She told me. Dev made the change in 4 minutes — one config update. The drag-and-drop feature never got built.
> Shadow the real process before you spec anything. The ask is almost never the need.

### Track B: New Process (Greenfield)
Design one step at a time:
- Input parameters — what comes in?
- Goal of the step — what is it trying to achieve?
- Output parameters — what comes out?
- Big picture first → zoom into each step

---

## Deliverable 1: Process / Flow Diagram

Map every step visually. Tool doesn't matter — draw.io, Figma, Miro, pen and paper.

> For each step in the process, capture the **success condition** — one plain-language sentence describing what "working correctly" looks like for that step. Write it from the client's perspective, not technically.
> Bad: "works correctly" — Good: "Slack message sent to #sales within 30 seconds of HeyReach reply received"
> These feed directly into unit test requirements in Phase S. If you can't write a success condition for a step, the step isn't defined well enough yet.

Save to `docs/process-flow.md` using `templates/process-flow.md`.

---

## Deliverable 2: User Journey Map — One Per System User Type

> Read `docs/stakeholder-register.md` before starting.

**Who gets a journey map:**
A journey map is for people who **directly interact with the system** — they have steps, actions, feelings, and pain points inside the product or process.

- ✅ End-users (the people doing the work / using the product daily)
- ✅ Admins (if they have a distinct workflow inside the system)
- ✅ Any secondary role with meaningful in-system interaction (e.g. finder, reviewer, approver)
- ❌ Project sponsor — funds it, not a system user
- ❌ Compliance officer — approves it, doesn't use it
- ❌ Anyone whose relationship to the project is oversight, not usage

**Do not collapse distinct roles into one map.** Admin and end-user have different steps, different needs, different pain points. A map that tries to serve both serves neither.

If unsure whether a stakeholder gets their own map:
> "Does [stakeholder] have a sequence of actions inside the product, or do they interact with the outcome of it?"
If outcome only — no map needed.

---

### For each system user type: Elicit, then map

Do not open a blank journey map and ask "walk me through your process." Pre-fill what you can from Phase C and Phase R, then use hypothesis + correction to fill the gaps.

**Step 1: Confirm who this user actually is**

Pull the user type from `docs/stakeholder-register.md`. Now make it concrete before mapping a single step.

> "Before we map [user type]'s journey — I'm picturing them as someone who [context from problem-statement + stakeholder-register]. They come to this product to [goal], and right now they're doing it by [current method]. Is that the right person, or am I describing the wrong version of this user?"

A wrong persona produces a wrong journey. Get confirmation here.

**Step 2: Pre-fill the skeleton from prior docs**

| Journey section | Source |
|---|---|
| Core steps | `docs/problem-statement.md` — Phase C process walkthrough; `docs/process-flow.md` — step sequence |
| Needs per step | `docs/problem-statement.md` — desired outcome, ideal state per actor |
| Pain points | Phase C friction inventory; `docs/problem-statement.md` — root cause |
| Feelings | Infer: frustration at friction points, anxiety at decision points, relief at resolution |
| Moments of delight | `docs/value-proposition-canvas.md` — gain creators; what the solution makes easier |

Draft the full journey skeleton before the client session.

**Step 3: Walk it step by step — elicit, don't confirm**

Do not just read the map back and ask "does this look right?" Walk through each step as if narrating the user's experience, and use elicitation moves to surface what pre-fill missed.

For each step:
> "So [user type] is at [step X]. I have them feeling [inferred feeling] because [reason]. In a perfect world, this step would just [ideal state] — is that the dream, or is there something more specific they actually need here?"

People correct specifics better than they originate from scratch. The pre-fill gives them something to push back against.

For pain points specifically:
> "I've flagged [step Y] as the most painful part — they're doing [manual thing] because [root cause]. Is that the worst part for them, or is there a step that actually costs them more time or stress that I've underweighted?"

For delight moments:
> "The moment I think this user will actually feel the value is [step Z] — when [thing happens]. Does that match what you see, or do they get the win somewhere else?"

**Step 4: Capture and save**

Write up the completed journey map immediately after the session. Do not leave gaps to fill later — if a step's feeling or need is unclear, it means you didn't elicit it fully. Go back.

Save one section per user type → `docs/user-journey-map.md`

---

## Deliverable 3: Project Goals — Pre-fill, Elicit, Confirm

The metrics came from Phase R. But goals are more than metrics — and some of the most important goals are never written down until someone asks the right questions.

> **War story:** Had a founder with an MVP at zero traction wanting to plan post-MVP features. Something more advanced, more differentiated. I stopped him. Let's look at what's happening right now — why aren't people using what you have?
> Turned out the whole product was built on the assumptions of one founder who wasn't even a subject matter expert in the space. Not a single user interview done. The flows were miles away from how users actually wanted to work. We reworked the core before touching the roadmap.
> Don't add floors to a building with a cracked foundation. Validate the goals against reality before you chase the vision.

**Step 1: Pre-fill from Phase R outputs**

| Goals section | Source |
|---|---|
| Goals | `docs/success-metrics.md` — success targets and desired projections |
| Non-goals | `docs/problem-statement.md` — scope constraints, what was explicitly ruled out |
| Success criteria | `docs/success-metrics.md` — quant and qual metrics agreed at Phase R sign-off |

Draft the goals doc from these sources before the session.

**Step 2: Elicit what the metrics don't capture**

Present the pre-filled goals, then run three elicitation moves to surface what's missing:

**Move 1 — The moment of pride**
> "When this is live and working — what's the moment you'll actually feel like this was worth it? Not the metric, the moment. What happens that makes you think: yes, that's it."

This surfaces the real goal under the metric. Often the metric is a proxy for something more specific.

**Move 2 — The unstated goal**
> "Is there anything this project needs to achieve that we haven't put on paper yet? A team dynamic, an internal narrative, something you need to show to someone?"

Organisational and political goals are real. If they exist and you don't know about them, they'll bite you later.

**Move 3 — The conflict check**
> "Looking at these goals together — do any of them pull in different directions? If we optimise hard for [goal A], does that make [goal B] harder to reach?"

Conflicting goals don't disappear when you ignore them. Surface them now and agree on priority order.

**Step 3: Confirm and lock**

> "Here's the complete picture — [goals], non-goals [X, Y], success looks like [metrics]. These are the things we'll point at in Phase P and ask: did we do it? Does this feel right?"

Do not reopen the negotiation on success criteria — that was Phase R. If they want to change a metric now, note it, surface the tradeoff, and ask for explicit sign-off before updating.

Save to `docs/project-goals.md`

---

## Deliverable 4: System Architecture — Integration Map + Data Flow

> Run this after process mapping and before closing Phase I.
> This is the step that answers: where does the data actually come from, and where does it go?
> Without it, Phase S will spec integrations it discovered too late — and non-technical clients will have no way to validate that what's being built matches what they imagined.

> **The HeyReach/Slack problem.** Someone wants an agent to ping them on Slack whenever a prospect replies in a HeyReach campaign. Sounds simple. But if nobody asked "how does the system know a reply happened in HeyReach?" — the integration was never designed. There's no webhook configured, no API polling, no data contract. The spec was written for a system that assumed data would appear from nowhere. Map the pipe first. Every time.

---

### Step 1: Integration Map

For every external system involved in the process — whether it sends data in, receives data out, or both — fill one entry in `docs/integration-map.md`.

Pull systems from the process flow (`docs/process-flow.md`) — every external tool named in a step is a candidate integration.

For each system, elicit:

**What data does it provide us?**
> "When [trigger event] happens in [system] — what exactly gets sent to us? Can you show me an example? I need to see the actual fields, not a summary."

Never accept "it sends the reply data." Get the payload. If they don't know — flag it as an open question and it must be resolved before the integration spec is written in Phase S.

**What triggers it?**
> "Is this triggered by something the user does, something on a schedule, or does [system] push it automatically? Walk me through the exact moment it fires."

Webhooks, scheduled polls, user-initiated API calls, and manual exports are all fundamentally different to build. Get clarity now.

**What do we send back?**
> "After we process this — does [system] need anything from us? A status update, a record write, a notification?"

**Format and auth:**
> "Does [system] have a sandbox or test environment? What auth does it use — API key, OAuth, something else?"

Save to `docs/integration-map.md` using `templates/integration-map.md`.

> If any integration has unanswered questions — log them in the Open Questions section of `docs/integration-map.md`. They must be resolved before Phase S writes the integration AI Spec for that service.

---

### Step 2: Data Flow

Once the integration map is complete, draw the full picture.

`docs/data-flow.md` answers three questions for the whole system — not per step, but end to end:
1. What enters the system, from where, in what format?
2. What does the system do with it?
3. What leaves the system, to where, in what format?

Pre-fill from `docs/process-flow.md` and `docs/integration-map.md`. Then present to the client:
> "Here's the full picture of how data moves through what we're building. Everything coming in is here, everything going out is here. Read through it — is there anything coming in or going out that we haven't captured? Anything that looks wrong?"

This is a client-facing document. Write it in plain language. No technical jargon. If a non-technical person can't read it and verify it, rewrite it until they can.

Save to `docs/data-flow.md` using `templates/data-flow.md`. Get client sign-off before closing Phase I.

---

## UX Discovery — Mandatory for External Products (UI/Mobile/Web)

> Run this after user journey maps are complete, before closing Phase I.
> Phase S will write the UX spec and design system from these inputs. If you skip this, Phase S has nothing to work from and will either guess or stall.

This is a conversation, not a form. Pre-fill what you can from context, then let the client correct.

---

### 3A: Audience & Mental Model

You already have user types from `docs/stakeholder-register.md`. Now go one level deeper.

For each primary user type, pre-fill a hypothesis from context, then present it:
> "I'm picturing [user type] as someone who [age range, tech comfort, use context — inferred from stakeholder-register + problem-statement]. They open this app [on the move / at a desk / in a stressful moment] and the thing they need most is [speed / clarity / trust]. Does that match who you're building for, or am I off?"

Also surface mental model references:
> "When [user type] opens this app for the first time — what's the app they already know that sets their expectations? Not what you want to copy, just what their mental model is built on."

---

### 3B: Visual Direction

Do not ask "what should it look like?" — that gets you nothing useful. Use references and reactions instead.

**Step 1: Propose a direction**
Based on the product category and user type, name 2–3 apps or products the design should feel adjacent to — not copy, but share the emotional register of.

> "For the [user type] flow — given it's [context] and needs to feel [quality] — I'm thinking something in the direction of [App A] or [App B]. Does that resonate, or does it feel wrong?"

**Step 2: Capture any client-provided references**
If they have references, take them. Then ask:
> "These are great starting points. Is there anything about these you'd specifically want to avoid — a vibe, a colour, a layout pattern that doesn't feel right for your audience?"

**Step 3: Identify one non-negotiable**
> "If there's one thing the design absolutely must feel — fast, warm, trustworthy, premium, approachable — what is it? Pick one."

Record all of this. It will feed `docs/design-system.md` directly.

---

### 3C: Navigation Pattern

Establish the navigation model before any screens are drawn.

Present the options with context:
> "There are a few standard patterns here. Tab bar (bottom nav) works well when users switch between 2–4 core areas frequently. Stack-only works for linear flows — think onboarding or checkout. Drawer/sidebar suits apps with many sections. Which one fits how users will actually move through this?"

If the product has distinct user roles, ask:
> "Do these user types see different navigation entirely, or the same shell with different content?"

Record the decision. This is the navigation contract — Phase S builds the sitemap from it.

---

### 3D: Key Screen Identification

You already have the critical flows from the user journey map. Now identify which screens carry the most weight.

> "Looking at the journey map — which 2 or 3 screens does everything hinge on? The one where users decide to stay or leave. The one where the product either earns trust or loses it."

For each high-stakes screen identified:
- What emotion should the user feel here?
- What is the single most important action on this screen?
- What's the biggest risk of getting it wrong?

This feeds the cognitive UX prioritisation in Phase S screen specs.

---

### 3E: Friction & Delight Inventory

Pull from the user journey map — moments of pain and moments of delight are already mapped.

Now make them design-actionable:

For each pain point:
> "This step causes friction. What would make it disappear — simplification, automation, better feedback, trust signal?"

For each delight moment:
> "This is where users feel good. How do we amplify it — animation, confirmation, a small reward moment?"

Record the answers. They become UX notes in the screen specs.

---

## Data Mapping — Mandatory When Structured Data Extraction Is In Scope

> **Trigger:** Run this section if any feature in scope involves extracting, transforming, or mapping structured data.
> Examples: OCR from documents, API response parsing, CSV/Excel imports, form submissions to DB, webhook payloads.
>
> If the mapping isn't defined here, Claude will guess in Phase S. It will be wrong.

**How to detect if this applies:**

Read the process flow and user journey. Ask: does any step involve:
- Reading data from a document (PDF, image, spreadsheet)?
- Consuming an external API response and saving fields to a DB?
- Importing data from an external file or feed?
- Taking form input and mapping it to a structured DB schema?

If yes to any — run this section before closing Phase I.

**What to elicit:**

For each data source:

**1. Describe the source structure**
> "Show me an example of the [document/API response/file]. Walk me through what's on it — sections, headings, where the key data lives. Don't summarise — show me."

Never accept "it's a standard invoice" or "just a normal API response." Get the actual structure.

**2. Map every field explicitly**
> "For each piece of data we need to save — tell me: where exactly is it in the source, what it's called there, and what DB field it maps to."

Fill `docs/data-mapping.md` field by field. Do not leave any row blank.

**3. Nail the edge cases**
> "What happens if [field X] is missing? What if the document is scanned and the text is unclear? What if there are multiple values where you expect one?"

Every edge case not defined here becomes a production bug.

**4. Define validation rules**
> "Before we save anything to the DB — what must be true? What would make a record invalid and what should happen when that occurs?"

Save to `docs/data-mapping.md` using the template in `/templates/data-mapping.md`.

---

## Phase 3 Outputs

> Save all of these to `docs/` before closing Phase I.

| File | Contents | Required? |
|---|---|---|
| `docs/process-flow.md` | Full process map — every step, tool, input, output, decision, success condition per step | Always |
| `docs/user-journey-map.md` | Journey per system user type — steps, needs, feelings, pain points, delights | Always |
| `docs/project-goals.md` | Goals (incl. elicited), non-goals, success criteria linked to Phase R metrics | Always |
| `docs/integration-map.md` | Every external system — direction, trigger, data in/out, format, auth, open questions | Always |
| `docs/data-flow.md` | Full system data pipe in plain language — data in, processing, data out — client signed off | Always |
| `docs/ux-discovery.md` | Audience mental models, visual direction, navigation pattern, high-stakes screens, friction/delight | External UI/Mobile/Web only |
| `docs/data-mapping.md` | Field-by-field source → DB mapping, edge cases, validation rules | When structured data extraction is in scope |

---

## Decision Logging — Phase I

> Update `docs/decisions.md` with decisions made in this phase before closing.

**Log these decisions in Phase I:**

- **Process track chosen** — Track A (existing) or Track B (greenfield), and why
- **User types included/excluded from journey maps** — who got a map and who didn't, with reason
- **Integration decisions** — which systems are in scope, any integration ruled out and why
- **Navigation pattern** (if UX discovery ran) — which pattern was chosen and why
- **Data mapping scope** — which features triggered data mapping and what was decided on edge case handling

---

## Exit Checklist
- [ ] Process fully mapped (Track A or B) → `docs/process-flow.md`
- [ ] Every tool, input, output, decision point, and **success condition** documented per step
- [ ] Stakeholder-register reviewed — system users identified, non-users excluded from journey mapping
- [ ] One journey map per system user type → `docs/user-journey-map.md`
- [ ] Each user type persona confirmed before mapping their journey
- [ ] Needs / feelings / actions elicited per step (not just inferred)
- [ ] Delight moments explicitly identified and marked
- [ ] Project goals pre-filled from Phase R, three elicitation moves run, confirmed → `docs/project-goals.md`
- [ ] Unstated and conflicting goals surfaced and resolved
- [ ] Diagrams drawn and shared with client for confirmation
- [ ] **System Architecture complete:**
  - [ ] Every external system named and mapped → `docs/integration-map.md`
  - [ ] Trigger, data in/out, format, and auth documented per system
  - [ ] No integration left as "TBD" — open questions logged and flagged for resolution before Phase S
  - [ ] Data flow written in plain language, client has read and signed off → `docs/data-flow.md`
- [ ] **[Structured data in scope]** Data mapping complete → `docs/data-mapping.md`
  - [ ] Source structure described with real example (not assumed)
  - [ ] Every field mapped: source location → DB table → column → type
  - [ ] Edge cases and nulls defined per field
  - [ ] Validation rules defined
  - [ ] All open questions answered before Phase S
- [ ] **[External UI/Mobile/Web]** UX Discovery complete → `docs/ux-discovery.md`
  - [ ] Audience mental model confirmed per user type (3A)
  - [ ] Visual direction agreed — references captured, non-negotiable identified (3B)
  - [ ] Navigation pattern decided (3C)
  - [ ] High-stakes screens identified with emotion + primary action (3D)
  - [ ] Friction and delight moments made design-actionable (3E)
- [ ] Key decisions logged → `docs/decisions.md`
