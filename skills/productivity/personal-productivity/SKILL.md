---
name: "personal-productivity"
description: "Build a Personal Productivity System Pack (weekly timebox plan, capture+to-do system, daily/weekly review rituals, and a 7-day rollout). Use for timeboxing, calendar blocking, and staying on top of high-volume leadership work. Category: Career."
---

# Personal Productivity

## Scope

**Covers**
- Designing a **weekly timebox plan** for a high-meeting-load job (meeting windows, focus blocks, admin buffers)
- Building a **write-it-down capture system** so tasks don’t live in your head (inbox → lists → reviews)
- Creating **daily + weekly review rituals** that keep you current without constant re-planning
- Producing a practical **7-day rollout plan** (small changes you can implement immediately)

**When to use**
- “Help me timebox my week so I can handle meetings + deep work.”
- “I keep forgetting tasks. Build me a write-it-down system and a review routine.”
- “I’m juggling a demanding job plus side commitments (advising/board/etc.). Make it sustainable.”
- “Create a personal productivity system I can follow next week.”

**When NOT to use**
- You need medical/mental-health advice (including ADHD treatment), or you are in crisis. Seek professional help.
- You want a team-wide process (meeting policy, org operating system). Use a team/ops skill instead.
- You need a project plan, milestones, or delivery management. Use `managing-timelines`.
- You primarily need to reduce burnout/energy drain (not just time). Use `energy-management`.

## Inputs

**Minimum required**
- Your role + primary responsibilities (and whether you manage people)
- Your constraints/non-negotiables (time zones, caregiving, travel, on-call, deadlines)
- A representative week (calendar text dump, recurring meetings list, or narrative)
- Your current task system (or “none”) + tools you’re willing to use (any calendar + any to-do list works)
- What “better” means in 2–4 weeks (e.g., fewer dropped tasks, more deep-work blocks, lower weekend spillover)

**Missing-info strategy**
- Ask **3–5 questions at a time** from [references/INTAKE.md](references/INTAKE.md).
- If the calendar is unavailable, proceed with a **default-week draft** using explicit assumptions and ask the user to correct it.
- Do not request secrets, credentials, or sensitive personal/medical details.

## Outputs (deliverables)

Produce a **Personal Productivity System Pack** (Markdown in chat; or as files if requested) in this order:

1) **Context Snapshot** (goal, constraints, assumptions, success definition)
2) **Commitment & Workload Inventory** (fixed commitments + “floating” responsibilities)
3) **Weekly Timebox Plan** (meeting windows, focus blocks, admin buffers, protected time, weekend spillover rule)
4) **Capture + To-Do System Spec** (inbox, lists, processing, prioritization, timeboxing method)
5) **Daily Plan + Shutdown Ritual** (how you start the day; how you close loops)
6) **Weekly Review Ritual** (calendar + task review; reset rules)
7) **7-Day Rollout Plan** (setup steps + first-week experiments)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + success definition + boundaries
- **Inputs:** user context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm scope (personal productivity for career execution). Define “better” in 2–4 weeks and 1–2 measurable signals (e.g., dropped tasks/week, deep-work blocks/week). Confirm boundaries (not medical/therapy; not a team policy rewrite).
- **Outputs:** Context Snapshot (draft) + assumptions/unknowns list.
- **Checks:** Success definition is specific enough to evaluate after 2 weeks.

### 2) Build a commitment & workload inventory
- **Inputs:** calendar/recur meetings; responsibilities; side commitments.
- **Actions:** List fixed commitments (meetings, deadlines, recurring obligations) and floating workload (projects, people mgmt, admin). Identify 3–5 “high-leverage” responsibilities and the biggest sources of fragmentation.
- **Outputs:** Commitment & Workload Inventory (table) + top constraints.
- **Checks:** Inventory separates **fixed** vs **flexible** time and includes side commitments (if any).

### 3) Design the weekly timebox plan (default week)
- **Inputs:** inventory; energy preferences; constraints.
- **Actions:** Draft a default week: meeting windows, focus blocks, admin buffers, and protected personal time. Add explicit rules: meeting batching, buffer time, weekend spillover (if needed), and what gets timeboxed first.
- **Outputs:** Weekly Timebox Plan (calendar-like block plan) + 5–8 rules.
- **Checks:** At least 3 focus blocks/week exist; meeting time has limits or windows; buffers are real blocks (not wishes).

### 4) Specify the capture + to-do system (“write it down”)
- **Inputs:** current tools; task volume; common failure modes (dropped tasks, unclear next actions).
- **Actions:** Define: capture inbox, processing ritual, list taxonomy, and a prioritization rule. Ensure every task becomes either: (a) timeboxed on calendar, (b) next action on a list, (c) delegated, or (d) deleted.
- **Outputs:** Capture + To-Do System Spec + “rules of the system”.
- **Checks:** The system has a single trusted inbox and a daily processing rule that takes ≤15 minutes.

### 5) Add daily plan + shutdown ritual
- **Inputs:** timebox plan; task system.
- **Actions:** Create a daily routine: morning “top outcomes” + quick timeboxing; end-of-day shutdown (clear inbox, update next actions, plan first block tomorrow).
- **Outputs:** Daily Plan + Shutdown Ritual (copy/paste checklist).
- **Checks:** Ritual is small enough to actually do; includes handling of new tasks during the day (capture rule).

### 6) Add weekly review ritual (reset + recalibration)
- **Inputs:** default week; backlog lists; upcoming commitments.
- **Actions:** Create a weekly review to: reconcile calendar ↔ tasks, reset priorities, and re-timebox next week. Include a “kill list” (stop/defer) to prevent backlog bloat.
- **Outputs:** Weekly Review Ritual + weekly reset checklist.
- **Checks:** Review includes both (1) looking forward (next 2 weeks) and (2) backlog cleanup.

### 7) Quality gate + finalize rollout plan
- **Inputs:** full draft pack.
- **Actions:** Produce a 7-day rollout plan (setup + first experiments). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Include **Risks / Open questions / Next steps**.
- **Outputs:** Final Personal Productivity System Pack.
- **Checks:** Next 7 days have specific actions scheduled; risks and unknowns are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (timeboxing + side commitments):** “I’m a product leader with wall-to-wall meetings and I advise a startup. Use `personal-productivity` to create a Personal Productivity System Pack with a default week timebox plan and a task capture system.”  
Expected: weekly timebox plan with meeting windows + focus blocks, capture/to-do spec, daily/weekly reviews, 7-day rollout.

**Example 2 (dropped tasks):** “I keep forgetting small but important follow-ups. Build me a write-it-down system and a daily shutdown routine.”  
Expected: capture system with inbox → processing → lists, a 10–15 minute daily shutdown checklist, and success metrics.

**Boundary example (medical):** “Diagnose my ADHD and tell me what productivity meds to take.”  
Response: out of scope for medical advice; recommend professional help. Offer a neutral capture/timeboxing system and ask for work constraints only.
