---
name: phase3-investigate
description: The Mileva Method (CRISP) — Phase 3: Investigate. Process mapping for existing or greenfield processes, user journey mapping, UX discovery, project goals. Use after outcome alignment. Triggers on "investigate", "phase 3", "map the process", "process mapping", "user journey", "as-is process", or after Phase R exit checklist is complete.
---

# I — Investigate: Process Understanding

Map what exists (or what should exist) before designing a solution.

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
Save to `docs/process-flow.md`.

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

## Phase 3 Outputs

> Save all of these to `docs/` before closing Phase I.

| File | Contents | Required? |
|---|---|---|
| `docs/process-flow.md` | Full process map — every step, tool, input, output, decision | Always |
| `docs/user-journey-map.md` | Journey per system user type — steps, needs, feelings, pain points, delights | Always |
| `docs/project-goals.md` | Goals (incl. elicited), non-goals, success criteria linked to Phase R metrics | Always |
| `docs/ux-discovery.md` | Audience mental models, visual direction, navigation pattern, high-stakes screens, friction/delight | External UI/Mobile/Web only |

---

## Exit Checklist
- [ ] Process fully mapped (Track A or B) → `docs/process-flow.md`
- [ ] Every tool, input, output, and decision point documented
- [ ] Stakeholder-register reviewed — system users identified, non-users excluded from journey mapping
- [ ] One journey map per system user type → `docs/user-journey-map.md`
- [ ] Each user type persona confirmed before mapping their journey
- [ ] Needs / feelings / actions elicited per step (not just inferred)
- [ ] Delight moments explicitly identified and marked
- [ ] Project goals pre-filled from Phase R, three elicitation moves run, confirmed → `docs/project-goals.md`
- [ ] Unstated and conflicting goals surfaced and resolved
- [ ] Diagrams drawn and shared with client for confirmation
- [ ] **[External UI/Mobile/Web]** UX Discovery complete → `docs/ux-discovery.md`
  - [ ] Audience mental model confirmed per user type (3A)
  - [ ] Visual direction agreed — references captured, non-negotiable identified (3B)
  - [ ] Navigation pattern decided (3C)
  - [ ] High-stakes screens identified with emotion + primary action (3D)
  - [ ] Friction and delight moments made design-actionable (3E)
