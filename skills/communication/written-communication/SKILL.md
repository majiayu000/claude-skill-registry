---
name: "written-communication"
description: "Draft and edit high-signal written artifacts and produce a Written Communication Pack (brief, outline, draft email/memo/doc, canonical doc option, quality gate). Use for writing, written communication, memo, email, doc, async update, rewrite for clarity. Category: Communication."
---

# Written Communication

## Scope

**Covers**
- Turning messy notes into a clear **email, memo, doc, or async update**
- Making the **“how”** explicit (what happens next, by whom, by when)
- Editing for **clarity at scale** (scanability, definitions, single source of truth)
- Creating/maintaining a **canonical doc** for an ongoing project

**When to use**
- “Draft an email to stakeholders explaining a change and what I need from them.”
- “Turn these bullets into a 1-page memo with a recommendation and next steps.”
- “Rewrite this doc to be clearer, shorter, and more actionable.”
- “Create a canonical doc as the source of truth for this project.”

**When NOT to use**
- You need **marketing/brand copy** (landing pages, ads) more than internal/executive clarity.
- You need a full product spec/PRD from scratch (use `writing-prds` or `writing-specs-designs`).
- You’re writing **legal/HR/regulated** communications without expert review.
- The real issue is alignment via facilitation (you may need a meeting/offsite plan, not a rewrite).

## Inputs

**Minimum required**
- Artifact type + channel (email / memo / doc / status update; where it will live)
- Audience (roles/seniority) + what they care about
- Goal + ask (inform/align/decide; what you want the reader to do, by when)
- Key context (facts, constraints, timeline, links) + what must be avoided (sensitivities)
- Source material (notes, existing draft, Slack threads, etc.)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time), then proceed.
- If critical info remains missing, make explicit assumptions and offer 2–3 options (structure/tone/ask).

## Outputs (deliverables)

Produce a **Written Communication Pack** in Markdown (in-chat; or as files if requested):

1) **Message brief** (audience, goal, ask, constraints)
2) **Outline** (TL;DR + key points + “how/next steps”)
3) **Draft artifact** (email/memo/doc/status update) in final-ready format
4) **Canonical doc skeleton** (optional; when the project needs a single source of truth)
5) **Risks / Open questions / Next steps** (always)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Intake + choose the lightest artifact
- **Inputs:** user request + [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify the channel and pick the smallest artifact that works (email vs memo vs doc vs status update vs canonical doc).
- **Outputs:** Message brief (draft) + artifact selection.
- **Checks:** You can answer: “Who is this for, and what should they do after reading?”

### 2) Lock the reader outcome + ask (one sentence)
- **Inputs:** brief.
- **Actions:** Write one sentence: “After reading, the audience will ____.” Make the ask explicit (decision/options, approval, feedback, or FYI) and include a deadline if relevant.
- **Outputs:** Outcome/ask line + decision/feedback request.
- **Checks:** The ask is unambiguous and doesn’t require a meeting to interpret.

### 3) Convert “what/why” into “how” (actionable next steps)
- **Inputs:** source material + outcome/ask.
- **Actions:** Identify the 3–7 concrete steps, responsibilities, and dependencies. If proposing a change, include what changes, what stays the same, and what happens next.
- **Outputs:** “How / Next steps” bullets (owner + date where possible).
- **Checks:** A reader could execute without asking “so what do you want me to do?”

### 4) Structure for skim (clarity at scale)
- **Inputs:** brief + next steps.
- **Actions:** Create a TL;DR, then headings in the order readers scan: Ask → Context → Details → Next steps. Use bullets, short paragraphs, and explicit labels.
- **Outputs:** Outline with headings.
- **Checks:** A skim-reader can capture the point in < 60 seconds.

### 5) Draft the artifact (write to be forwarded)
- **Inputs:** outline + templates.
- **Actions:** Draft in plain language; avoid jargon; put key numbers and decisions in writing. If this is ongoing work, link to (or create) the canonical doc.
- **Outputs:** Draft email/memo/doc/status update.
- **Checks:** The draft is safe to forward; it stands alone without verbal context.

### 6) “Letter to yourself” clarity pass (then rewrite for the audience)
- **Inputs:** draft.
- **Actions:** If the content is fuzzy, write a quick internal version (“what am I actually saying?”), then rewrite in the audience’s language and incentives.
- **Outputs:** Clarified rewrite with cleaner logic.
- **Checks:** The message has a single through-line; no contradictions or buried ledes.

### 7) Canonical doc check (single source of truth)
- **Inputs:** draft + project context.
- **Actions:** If readers will keep asking “where is the latest?”, create/update a canonical doc (links, owners, last updated, decisions, next update cadence).
- **Outputs:** Canonical doc skeleton or link section.
- **Checks:** There is one obvious place to find the current state and decisions.

### 8) Quality gate + finalize
- **Inputs:** full pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final Written Communication Pack.
- **Checks:** Clarity, actionability, and ownership meet the bar (≥ 3 on each rubric dimension).

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (stakeholder email):** “Draft an email to exec stakeholders: the launch is slipping 2 weeks; we need approval to cut scope and a decision by Friday.”  
Expected: TL;DR + explicit ask/options + what changes + next steps with owners.

**Example 2 (project memo + canonical doc):** “Turn these notes into a 1-page memo that aligns the team on the new onboarding approach, and create a canonical doc outline for ongoing updates.”  
Expected: memo with recommendation + tradeoffs + next steps, plus a source-of-truth doc skeleton.

**Boundary example:** “Write a legal/HR disciplinary notice.”  
Response: decline to fabricate legal/HR guidance; request expert review; offer to help with neutral structure, tone, and clarity if the user provides approved language.
