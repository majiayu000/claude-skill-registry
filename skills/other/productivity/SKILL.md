---
name: productivity
description: Personal productivity — sort out what to work on next, prioritize tasks, plan your day, run weekly reviews, optimize meetings, set goals, write status updates. Use when planning days, managing tasks, running weekly reviews, optimizing meetings, or writing status updates.
routing:
  triggers:
    - "productivity"
    - "task management"
    - "daily plan"
    - "weekly review"
    - "meeting agenda"
    - "focus time"
    - "goal setting"
    - "status update"
    - "time management"
    - "prioritize tasks"
    - "standup"
    - "retrospective"
  not_for: "software task specs, requirements, or plan-lifecycle management — that is planning. This is personal prioritization and time management, not building a project plan."
  category: business
  force_route: false
  pairs_with: []
user-invocable: true  # justification: productivity modes are directly invoked for daily/weekly planning rituals
---

# Productivity

Umbrella skill for personal and team productivity: task decomposition, daily/weekly planning, meeting optimization, status updates, goal setting, and focus management. Each mode loads its own reference files on demand.

---

## Mode Detection

Classify into one mode before proceeding.

| Mode | Signal Phrases | Reference |
|------|---------------|-----------|
| **TASK** | add task, prioritize tasks, task list, what's on my plate, decompose work, batch tasks | `references/task-management.md` |
| **PLAN** | daily plan, plan my day, time blocks, plan my week, energy mapping | `references/daily-weekly-planning.md` |
| **MEETING** | meeting agenda, optimize meeting, meeting audit, cancel this meeting, async alternative | `references/meeting-optimization.md` |
| **STATUS** | status update, standup, weekly update, stakeholder update, progress report | `references/status-updates.md` |
| **REVIEW** | weekly review, retro, retrospective, reflect on week, monthly review | `references/daily-weekly-planning.md` |
| **GOAL** | set goals, OKRs, quarterly goals, goal progress, key results | `references/daily-weekly-planning.md` |

If the request spans modes, pick the primary mode and note the secondary.

---

## Workflow by Mode

### TASK Mode

**Load**: `references/task-management.md`, `references/llm-productivity-failure-modes.md`

1. **Capture** — Accept tasks in any format: freeform text, bullet lists, pasted meeting notes, vague intentions. Extract actionable items.
2. **Decompose** — Apply vertical slicing (because horizontal slices create work that cannot ship independently):

   | Slice Quality | Example |
   |---------------|---------|
   | Good (vertical) | "User can upload a CSV and see a preview" — shippable alone |
   | Weak (horizontal) | "Build the upload API" — requires the UI to deliver value |

3. **Estimate** — Assign time estimates using the 1/2/4-hour bucketing system (because finer granularity creates false precision, coarser loses planning value). Tasks over 4 hours need decomposition.
4. **Prioritize** — Apply the appropriate framework based on context:

   | Context | Framework | Why |
   |---------|-----------|-----|
   | Personal daily work | Eisenhower (urgent/important) | Fast, intuitive, separates reactive from proactive |
   | Backlog with many items | ICE (Impact/Confidence/Ease) | Quantitative ranking without heavy data requirements |
   | Team sprint planning | Weighted scoring against goals | Defensible, transparent to stakeholders |

5. **Organize** — Group by context (because context-switching between unrelated tasks costs 15-25 minutes per switch). Batch similar work: all emails together, all code reviews together, all writing together.

**Gate**: Every task has an action verb, a completion condition, and a time estimate. Vague items like "think about marketing" get reframed as "Draft 3 marketing channel options with pros/cons (2h)."

### PLAN Mode

**Load**: `references/daily-weekly-planning.md`, `references/llm-productivity-failure-modes.md`

1. **Gather constraints** — Ask for (conversationally, not as a wall of questions):
   - Calendar commitments for the day/week
   - Hard deadlines
   - Energy level and known energy patterns (because matching task difficulty to energy state increases completion rates)
   - Carryover from yesterday

2. **Select top priorities** — Identify the Top 3 outcomes for the day (because more than 3 priorities means zero priorities). Apply the "if only these 3 things got done, would today feel successful?" test.

3. **Build time blocks** — Map tasks to calendar slots:

   | Block Type | When to Schedule | Duration |
   |------------|-----------------|----------|
   | Deep work (creation, analysis) | Peak energy hours (usually morning) | 90-120 min |
   | Reactive work (email, Slack, reviews) | Low energy hours (usually post-lunch) | 30-60 min batches |
   | Admin/maintenance | End of day | 30 min |
   | Buffer | Between blocks | 15 min minimum |

4. **Identify conflicts** — Flag when calendar meetings fragment deep work blocks. Surface the cost: "You have 3 meetings between 9-12, leaving zero uninterrupted blocks during your peak hours."

5. **Generate plan** — Output a concrete, time-blocked plan with the Top 3 outcomes highlighted.

**Gate**: Plan accounts for actual calendar (not aspirational free time). Deep work blocks are at least 90 minutes. Buffers exist between blocks. Total planned work does not exceed available hours minus 20% (because unplanned work always appears).

### MEETING Mode

**Load**: `references/meeting-optimization.md`, `references/llm-productivity-failure-modes.md`

1. **Determine operation**:

   | Operation | What to Do |
   |-----------|-----------|
   | Audit existing meeting | Apply the 5P framework: Purpose, Participants, Preparation, Process, Payoff |
   | Design new agenda | Build outcome-driven agenda with time allocations and decision types |
   | Convert to async | Draft async alternative with decision framework and deadline |
   | Optimize recurring meeting | Analyze frequency, attendance, decision output vs time spent |

2. **For audits** — Calculate meeting cost (participants x hourly rate x duration x frequency). Surface the number because most people underestimate it. A weekly 1-hour meeting with 8 people at $75/hr costs $31,200/year.

3. **For agendas** — Every agenda item gets:
   - **Type**: Decision, Discussion, Information, or Brainstorm (because different types need different facilitation)
   - **Owner**: Who presents/facilitates this item
   - **Time**: Allocated minutes
   - **Pre-read**: What participants should review before the meeting
   - **Outcome**: What "done" looks like for this item

4. **For async conversion** — Apply the async-first decision tree:
   - Can this be a document with comments? Do that instead.
   - Does this need real-time debate? Keep the meeting, shorten it.
   - Does this need a decision from one person? Send them a 1-page memo with a deadline.

**Gate**: Every meeting has a stated purpose that could not be achieved async. Every agenda item has a type, owner, time allocation, and defined outcome. Information-only meetings are flagged for conversion to async.

### STATUS Mode

**Load**: `references/status-updates.md`, `references/llm-productivity-failure-modes.md`

1. **Detect audience** — Different audiences need different framing:

   | Audience | Frame | Length | Lead With |
   |----------|-------|--------|-----------|
   | Manager (1:1) | Progress + blockers + asks | 3-5 bullets | What you need from them |
   | Team (standup) | Yesterday/Today/Blockers | 60 seconds spoken | Blockers first |
   | Stakeholders | Outcomes + timeline + risks | 1 page | Business impact |
   | Executives | Red/Yellow/Green + decisions needed | < 200 words | Decisions needed |

2. **Gather inputs** — Ask for:
   - What shipped or progressed since last update
   - What is blocked and by whom
   - What decisions are needed (and from whom)
   - Timeline changes (and why)

3. **Generate update** using the Progress/Plans/Problems format:
   - **Progress**: Completed outcomes (not activities). "Shipped search indexing, 40% faster queries" beats "worked on search."
   - **Plans**: Next period's commitments with confidence levels.
   - **Problems**: Blockers with specific asks. "Need API access from Platform team by Friday to unblock integration testing" beats "waiting on dependencies."

4. **For standups** — Optimize for brevity:
   - Lead with blockers (because that is the only part the team can act on in real time)
   - State completed items as outcomes, not activities
   - State today's focus as the single most important deliverable

**Gate**: Status update exists. Outcomes framed as results (not activities). Every problem has a specific ask with a named owner and deadline. Executive updates are under 200 words.

### REVIEW Mode

**Load**: `references/daily-weekly-planning.md`, `references/llm-productivity-failure-modes.md`

1. **Collect** — Gather data from the period:
   - What was planned vs what actually happened
   - Tasks completed, deferred, or abandoned
   - Unplanned work that appeared
   - Calendar analysis: time in meetings vs deep work vs reactive work

2. **Process** — For each incomplete item:

   | Outcome | Action |
   |---------|--------|
   | Deferred (still relevant) | Reschedule with honest time estimate |
   | Deferred (no longer relevant) | Remove — carrying dead tasks creates cognitive overhead |
   | Blocked | Identify the specific unblock action and owner |
   | Abandoned (scope changed) | Archive with reason |

3. **Reflect** — Surface patterns (because reviews that skip reflection are just task lists):
   - What type of work consistently gets deferred? (This reveals priority misalignment or estimation failures)
   - Where did unplanned work come from? (This reveals process gaps or boundary issues)
   - Which commitments to others were met vs missed? (This reveals reliability patterns)
   - What was the ratio of deep work to reactive work? (Target: at least 40% deep work)

4. **Decide** — Identify 1-3 concrete adjustments for the next period. Specific and testable: "Block 9-11am as no-meeting time" not "do more deep work."

5. **For retrospectives** — Facilitate with:
   - What went well (keep doing)
   - What could improve (change one thing)
   - Action items (assigned, with deadlines)
   - Separate observations from emotions from actions (because conflating them derails retros)

**Gate**: Review compares planned vs actual. At least one pattern is surfaced from the data. Adjustments are specific and testable (not aspirational). Dead tasks are removed, not carried forward indefinitely.

### GOAL Mode

**Load**: `references/daily-weekly-planning.md`, `references/llm-productivity-failure-modes.md`

1. **Determine scope**: Quarterly OKRs, annual goals, project milestones, or personal development goals.
2. **Structure goals** using the outcome hierarchy:

   | Level | Timeframe | Format | Example |
   |-------|-----------|--------|---------|
   | Vision | 1-3 years | Narrative | "Become the team's go-to person for data infrastructure" |
   | Objective | Quarter | Qualitative outcome | "Make the data pipeline reliable enough that on-call is boring" |
   | Key Result | Quarter | Measurable milestone | "Reduce pipeline failures from 12/month to 2/month" |
   | Initiative | Weeks | Concrete project | "Add circuit breakers to the 5 highest-failure-rate jobs" |

3. **Validate each goal** against:
   - **Measurability**: How will you know it is done? (Binary completion or metric target)
   - **Influence**: Do you control the outcome, or does it depend on others? (Goals you do not control are hopes, not goals — reframe as the actions within your control)
   - **Tension**: Does this goal conflict with another goal? (Surface tradeoffs explicitly)
   - **Stretch calibration**: 70% confidence of achievement = good stretch. 100% = sandbagging. 30% = aspirational wish.

4. **Connect to daily work** — Map goals down to weekly themes and daily tasks. Goals that do not connect to this week's work are not goals yet — they are intentions.

**Gate**: Every goal has a measurable completion condition. Goals connect to at least one concrete next action. Conflicting goals have explicit tradeoff decisions. Quarterly goals have monthly check-in milestones.

---

## LLM Failure Modes in Productivity Work

See `references/llm-productivity-failure-modes.md` for the complete failure mode catalog (aspirational planning, unestimated tasks, generic advice, agendaless meetings, shallow reviews, activity-based status). Universal failure modes in `skills/shared-patterns/llm-domain-failure-modes-base.md`.

---

## Prioritization Frameworks (Cross-Mode Reference)

Used in TASK, PLAN, and GOAL modes.

| Framework | Method | Best For |
|-----------|--------|----------|
| **Eisenhower** | 2x2: Urgent/Important. Do (U+I), Schedule (I), Delegate (U), Drop (neither). | Personal daily prioritization |
| **ICE** | Impact x Confidence x Ease (1-10 each) | Quick ranking of a medium-sized backlog |
| **Weighted Scoring** | Score items against 3-5 criteria with explicit weights | Team decisions requiring transparency and defensibility |
| **Time-to-Value** | Prioritize by shortest path to delivering user value | When facing analysis paralysis on a long backlog |

Apply frameworks to the specific situation. Producing a framework explanation instead of an applied prioritization is a failure mode (see `references/llm-productivity-failure-modes.md`).

---

## Output Conventions

- Markdown with clear headers. Scannable by someone with 30 seconds.
- Tables for comparisons, schedules, and priority matrices.
- Time blocks in `HH:MM - HH:MM` format with task and estimated duration.
- Status labels: **Done**, **In Progress**, **Blocked**, **Deferred**, **Dropped**.
- Executive-facing content: < 200 words. Team-facing: as detailed as needed.
- Every recommendation is specific enough to act on today. "Improve focus" is not actionable. "Block 9-11am as no-meeting deep work time" is.

---

## Reference Loading Table

| Mode | Primary Reference | Secondary Reference |
|------|------------------|-------------------|
| TASK | `references/task-management.md` | `references/llm-productivity-failure-modes.md` |
| PLAN | `references/daily-weekly-planning.md` | `references/llm-productivity-failure-modes.md` |
| MEETING | `references/meeting-optimization.md` | `references/llm-productivity-failure-modes.md` |
| STATUS | `references/status-updates.md` | `references/llm-productivity-failure-modes.md` |
| REVIEW | `references/daily-weekly-planning.md` | `references/llm-productivity-failure-modes.md` |
| GOAL | `references/daily-weekly-planning.md` | `references/llm-productivity-failure-modes.md` |
