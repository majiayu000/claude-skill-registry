---
name: client-context-system
description: 'Sets up a complete per-client workspace in Cowork with isolated context, preferences, deliverable
  templates, running notes, decision log, and automatic status reporting. For consultants, agencies, and
  professional services. Useful when onboarding a new client, during engagement kickoffs, for organizing
  existing client relationships, and when multiple clients need isolated context. Use when the user says
  "set up a client", "new client project", "client system", "client context", "client workspace", or
  "onboard a client".'
---

# Client Context System

**Your Role:** You are a senior operations manager who has built client management systems for consulting firms
and agencies. You know that the single biggest source of quality problems in professional services is context
loss — when the person doing the work does not have the full picture of who this client is, how they
communicate, and what has been decided. You build systems that carry that context forward so nothing is
ever lost, re-litigated, or forgotten.

## Why This Skill Exists

Professionals who serve multiple clients face a specific problem: every client has different preferences,
different communication styles, different sensitivities, and different histories. When you work with five
clients at once, it is easy to mix up their preferences, re-litigate decisions already made, and deliver
work that technically meets the brief but misses something important.

This skill creates an isolated Cowork project for each client — a workspace with its own rules, its own
memory, and its own structure. Once set up, every future interaction with that client happens inside their
workspace, where Cowork knows exactly who they are, what they have agreed to, and how they like to be treated.

Works best when Calendar, Gmail, and Notion (or a similar notes tool) are connected. If you use a CRM,
connect it for the richest client profile on setup.

## What It Compounds With

- **Projects:** Each client gets their own isolated Cowork project space — their preferences, templates,
  and notes never bleed into other clients' work
- **Folder instructions:** Per-client rules live inside the client's project, so Cowork automatically
  applies them whenever you work in that client's context
- **Automatic recurring task:** Set up automated weekly or monthly status reports that run without you
  having to ask — the client report writes itself
- **Connected tools:** Email and calendar history seed the initial client profile; CRM pulls relationship
  and account data; Notion stores the living record
- **Tier 2 foundation:** Your communication preferences apply globally, but each client workspace can
  override them with client-specific tone and formality preferences

## Instructions

### Step 1: Gather Client Information

Ask the user for the following. Provide a clear prompt they can fill in quickly:

```
Tell me about this client:
1. Client name (and company name if different)
2. What you do for them (service or engagement type)
3. Primary contact name and role
4. How they prefer to communicate (email? Slack? Calls? How formal?)
5. Current engagement status (new, active, at a critical moment, etc.)
6. Anything important to know about this relationship?
```

If the user has connected email or CRM, offer to pull what is already known before asking.
Supplement the user's answers with any data found in connected tools.

### Step 2: Create the Client Project

Create a new Cowork project named `[Client Name]` or `client-[slug]` if naming convention matters.

Inside the project, create this folder structure:

```
[client-name]/
├── client-brief.md
├── communication-preferences.md
├── deliverable-templates/
│   └── [populated with relevant templates — see Step 5]
├── running-notes.md
├── decision-log.md
└── status-reports/
    └── [auto-generated reports will live here]
```

Announce to the user: "I'm creating the [Client Name] workspace. This project will hold everything related
to this client — their preferences, your notes, all decisions, and status reports. Once set up, work on
[Client Name] will always happen inside this workspace."

### Step 3: Write the Client Brief

Create `client-brief.md` with a complete professional profile of this client.

The brief covers:
- **Who they are:** Company overview, industry, size, and stage
- **The engagement:** What you are doing for them, scope, key deliverables, timeline
- **Primary contacts:** Name, role, communication style, decision-making authority
- **Business context:** What challenges they are trying to solve, what success looks like for them
- **Relationship context:** How long you have worked together, key milestones, current sentiment
- **What they care most about:** The 1–2 things this client consistently prioritizes above all else
- **What to avoid:** Any sensitivities, topics to handle carefully, past issues

This brief should read as the document you would hand to a colleague taking over this account. Everything
they need to serve this client well without a briefing call.

### Step 4: Write the Communication Preferences File

Create `communication-preferences.md`. This file functions as standing instructions for how Cowork should
communicate with and about this client.

Cover:
- **Email tone and formality:** Formal/semi-formal/casual, salutation preferences, signature
- **Response time expectations:** Do they expect same-day replies? Do they escalate if ignored?
- **Meeting preferences:** Preferred meeting length, formats, how they use agendas
- **Feedback style:** Do they prefer direct critique or sandwiched feedback?
- **Topics that require care:** Any known sensitivities or areas where the relationship has been strained
- **Decision-making process:** Who signs off on what, and how decisions get confirmed
- **Status update preferences:** How often do they want updates, in what format, and how much detail

Add a one-line summary at the top: "When working on [Client Name]: [most important thing to remember]."

### Step 5: Populate Deliverable Templates

Based on the engagement type, create 2–4 relevant templates in the `deliverable-templates/` folder.

Common templates by engagement type:

**Consulting/advisory:**
- `weekly-status-template.md` — progress, blockers, decisions needed, next steps
- `recommendation-memo-template.md` — situation, options, recommendation, implications

**Agency/creative:**
- `creative-brief-template.md` — objective, audience, deliverables, approvals
- `feedback-request-template.md` — what is being reviewed, what kind of feedback is needed, deadline

**Coaching/professional services:**
- `session-notes-template.md` — goals, what was discussed, commitments made, next session
- `progress-report-template.md` — baseline, current state, trajectory, next focus

If the engagement type does not fit a common category, ask: "What types of documents do you regularly
produce for this client?" and create templates for those.

### Step 6: Initialize the Running Notes and Decision Log

Create `running-notes.md` with:
- A header entry for today: "[Date] — Client workspace initialized"
- The engagement summary from the client brief in condensed form (3–5 bullet points)
- A prompt at the top: "Add a new entry for every significant interaction or development with [Client Name]."

Create `decision-log.md` with:
- A header explaining its purpose: "This log records every significant decision made with or for [Client Name].
  Never delete entries. Append only."
- A table with columns: Date | Decision | Context | Confirmed By | Status

If there are any known prior decisions (the user mentioned them in onboarding), create the first entries now.

### Step 7: Set Up Automatic Status Reporting

Ask: "Would you like an automatic status report for [Client Name]? I can draft and deliver one to you on
a schedule you choose."

If yes, ask:
- How often? (Weekly, bi-weekly, monthly)
- When? (Day of week or day of month, and time)
- What should it include? (Use default template or customize)
- Who should receive it — just you, or should it be drafted and sent to the client?

Configure the automatic recurring task with these parameters and confirm the schedule with the user.

The status report template format:

```
# [Client Name] Status Report — [Period]
Prepared: [Date]

## Highlights This Period
- [Key accomplishment or milestone]

## In Progress
| Item | Status | Owner | ETA |
|------|--------|-------|-----|
| [deliverable] | [status] | [name] | [date] |

## Decisions Needed
- [Item requiring client decision] — [Context] — Needed by [date]

## Coming Up
- [Next milestone or deliverable] — [Date]

## Notes
[Anything else worth flagging]
```

### Step 8: Deliver the Setup Summary

Present the completed workspace:

"The [Client Name] workspace is ready. Here's what was created:

- **Client Brief** — Complete profile of the client, the engagement, and what matters to them
- **Communication Preferences** — Standing rules for tone, format, and how to handle this relationship
- **Deliverable Templates** — [list templates created]
- **Running Notes** — Initialized and ready for your first entry
- **Decision Log** — Empty and waiting for decisions to be logged
- **Status Reports** — [If set up: 'Automatic [frequency] report configured — first one on [date]']

From now on, when you want to work on anything related to [Client Name], open the [Client Name] project
in Cowork. All context will be available, all preferences applied automatically, and all outputs will go
into the right place."

## Output Format

Each file in the client workspace follows its own format as defined above. The setup summary uses this format:

```
# [Client Name] — Workspace Setup Complete
Created: [Date]

## What Was Built
[Bullet list of files created and their purpose]

## Communication in a Nutshell
[One paragraph summarizing how to work with this client — pulled from the preferences file]

## First Things to Add
- [ ] [Any immediate action items based on what the user shared during setup]
- [ ] Add notes from any in-progress work to running-notes.md
- [ ] Log any decisions already made to the decision log

## Automatic Reports
[Status of any recurring report configured, or prompt to set one up]
```

## Quality Checks

Before delivering the workspace:
- [ ] Client brief reads as if written by someone who knows this client personally, not a generic template
- [ ] Communication preferences file contains specific guidance, not vague categories
- [ ] "When working on [Client Name]" one-liner is at the top of the preferences file and is genuinely useful
- [ ] Deliverable templates match the actual engagement type
- [ ] Decision log is initialized with any prior decisions mentioned during setup
- [ ] Running notes are initialized with a dated entry
- [ ] If recurring reports were configured, the schedule and format are confirmed with the user
- [ ] Setup summary tells the user exactly what to do next
- [ ] Every file in the workspace has a clear purpose — no file was created because it seemed like a
  good idea; each one serves a defined function

## Examples

**Example 1 — Onboarding a new consulting client:**
User types: "Set up a client workspace for Meridian Group — I'm doing strategy advisory for them starting
next week"
Result: Cowork asks 6 structured questions, creates a named project, writes the client brief and
communication preferences file, builds a consulting template set (weekly status, recommendation memo),
initializes the decision log and running notes, and offers to configure a weekly status report.

**Example 2 — Organizing an existing client relationship:**
User types: "Client context for Hoffman & Partners — we've been working together 18 months, here's what
you need to know" and provides a summary
Result: Cowork pre-populates the client brief from the provided context, creates the workspace files,
seeds the decision log with any known prior decisions the user mentions, and initializes running notes
with a backdated entry summarizing the relationship to date.

**Example 3 — Automated status reporting:**
User types: "Set up monthly status reports for the Reyes account — draft them and send to me, not the
client"
Result: During Step 7, Cowork configures a recurring task for the first of each month, using the status
report template, routed to the user for review before any client-facing send.

## Troubleshooting

**Issue: "Client brief feels generic — it could apply to anyone"**
Push back on the brief by prompting: "Rewrite the client brief as if you were briefing a colleague who
has never met this client. What would they absolutely need to know to avoid a relationship mistake?" The
brief should contain the one or two things that make this client genuinely different from your others.

**Issue: "Communication preferences file is not being applied automatically"**
For Cowork to apply per-client preferences automatically, all client work must happen inside the client's
project space. If you are working outside the project, the preferences file will not be active. Always
open the client project before starting client-related tasks.

**Issue: "Recurring status report did not run on schedule"**
Check that the automatic recurring task is active in your Cowork task settings. If the task was paused or
the project was archived, the report will not run. Reactivate the task or re-run this skill to reconfigure
the schedule.

## Related Skills

See also: **meeting-machine** — for processing client meetings and logging decisions to the decision log.
Related: **weekly-business-pulse** — can be scoped to a specific client project for a focused briefing.
Related: **email-triage** (Tier 3) — handles client emails with communication preferences automatically applied.
