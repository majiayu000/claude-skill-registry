---
name: "running-design-reviews"
description: "Run high-signal design reviews (design critique / design crit / design feedback) by producing a Design Review Pack: review brief + requested feedback, agenda + facilitation script, feedback log prioritized by Value→Ease→Delight, decision record, and follow-up plan."
---

# Running Design Reviews

## Scope

**Covers**
- Planning a design review with a clear decision and requested feedback type(s)
- Running a live demo–centered critique (or async review when needed)
- Capturing feedback without “design-by-committee”
- Synthesizing feedback using **Value → Ease of Use → Delight** prioritization
- Recording decisions, tradeoffs, and follow-ups so the review changes the work

**When to use**
- “Prepare and run a design critique for this Figma prototype.”
- “We need a structured design review agenda and feedback log.”
- “Help us review this flow and decide what to change before we ship.”
- “Turn messy comments into prioritized feedback + next steps.”

**When NOT to use**
- You don’t have a defined problem, target user, or goal yet (use `problem-definition` first).
- You need build-ready interaction specs / acceptance criteria (use `writing-specs-designs`).
- You need evidence from users rather than expert critique (use `usability-testing`).
- You’re doing launch planning, comms, rollout/rollback (use `shipping-products`).

## Inputs

**Minimum required**
- Design artifact(s): link(s) or screenshots (e.g., Figma/prototype) + what parts are in scope
- The decision needed (what will change after the review)
- Target user + job-to-be-done (1–2 sentences)
- Success criteria (1–3) and constraints (time, platform, accessibility, tech)
- Review format + logistics: live vs async, time box, attendees/roles

**Missing-info strategy**
- Ask up to **5** questions from [references/INTAKE.md](references/INTAKE.md), then proceed.
- If answers aren’t available, make explicit assumptions and clearly label them.
- Do not request secrets or credentials.

## Outputs (deliverables)

Produce a **Design Review Pack** in Markdown (in-chat by default; write to files if requested), in this order:
1) **Design review brief / pre-read** (context, decision, requested feedback, links)
2) **Agenda + facilitation script** (timed, prompts, roles)
3) **Feedback log** (captured + categorized + prioritized)
4) **Decision record** (decisions, tradeoffs, owners, due dates)
5) **Follow-up message + next review plan** (what changed, what’s next)
6) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Classify the review and lock the decision
- **Inputs:** Request + artifact(s) + constraints.
- **Actions:** Identify the review type (concept / flow / content / visual polish / ship-readiness). Write the decision statement (“After this review we will decide ___”).
- **Outputs:** Review type + decision statement + scope boundary (in/out).
- **Checks:** Everyone can answer: “What will change after this review?”

### 2) Set the requested feedback (and what NOT to comment on)
- **Inputs:** Decision statement + stage of design.
- **Actions:** Specify 1–3 feedback questions (e.g., “Is the value proposition clear?”, “Where does the flow break?”, “What edge cases are missing?”). Explicitly defer aesthetics/minutiae until Value/Ease are validated.
- **Outputs:** Requested feedback list + “out of scope” feedback.
- **Checks:** Feedback questions map directly to the decision.

### 3) Assign roles (incl. a sponsor) and prepare a live demo
- **Inputs:** Attendees list + timeline/risk.
- **Actions:** Assign: **Presenter**, **Facilitator**, **Note-taker**, and a **Sponsor/DRI** (senior owner who focuses on “why” + core concept). Decide whether leadership must review all user-facing screens before ship (for high-craft products).
- **Outputs:** Roles list + demo plan (what will be shown, in what order).
- **Checks:** Decision rights are clear; the review is anchored in a live demo, not a slide deck.

### 4) Produce the pre-read (context first, then artifacts)
- **Inputs:** [references/TEMPLATES.md](references/TEMPLATES.md) (brief template) + project context.
- **Actions:** Write a 1–2 page brief: problem → user → success criteria → constraints → options considered → risks/tradeoffs → open questions → links.
- **Outputs:** Shareable pre-read + “how to review” instructions.
- **Checks:** A reviewer can give useful feedback asynchronously without a live context dump.

### 5) Run the review (big picture → Value → Ease → Delight)
- **Inputs:** Agenda + demo + notes/feedback log.
- **Actions:** Start with goals/feelings (“What’s bothering us overall?”), then evaluate:
  1) **Value:** is it solving the right problem?
  2) **Ease:** can users do it without friction?
  3) **Delight:** polish, aesthetics, extra joy (only after 1–2)
  Capture feedback as **observations + impact + suggestion**, not opinions.
- **Outputs:** Filled feedback log with categories and severities.
- **Checks:** The review does not get stuck in minutiae before Value/Ease are resolved.

### 6) Synthesize + prioritize feedback into a change plan
- **Inputs:** Feedback log.
- **Actions:** Deduplicate comments; resolve conflicts by returning to goals and constraints; prioritize by user impact and risk. Convert top items into explicit changes with owners and due dates.
- **Outputs:** Prioritized change list + updated feedback log status/owners.
- **Checks:** Top 3 issues are clear; each has a proposed action and owner.

### 7) Decide, document tradeoffs, and close the loop
- **Inputs:** Proposed change plan + remaining open questions.
- **Actions:** Record decisions and rationale; list tradeoffs and risks; define what must be re-reviewed. Send a follow-up summary and schedule the next review or ship gate.
- **Outputs:** Decision record + follow-up message + Risks/Open questions/Next steps.
- **Checks:** Decisions and action items are captured in writing; no critical decision is left implicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples
See [references/EXAMPLES.md](references/EXAMPLES.md).

## Reference files
- [references/INTAKE.md](references/INTAKE.md)
- [references/WORKFLOW.md](references/WORKFLOW.md)
- [references/TEMPLATES.md](references/TEMPLATES.md)
- [references/CHECKLISTS.md](references/CHECKLISTS.md)
- [references/RUBRIC.md](references/RUBRIC.md)
- [references/SOURCE_SUMMARY.md](references/SOURCE_SUMMARY.md)
- [references/EXAMPLES.md](references/EXAMPLES.md)
