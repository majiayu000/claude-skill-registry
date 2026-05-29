---
name: portfolio-status
description: Get a portfolio-level overview of all active project status
user-invocable: true
---

You are helping executive leadership get a portfolio-level view of active projects and initiatives.

Follow these steps:

### Step 1: Determine Scope

Ask the user:
- **All projects** or a specific category (operations, marketing, technology, M&A)?
- **Level of detail**: High-level status or detailed per-project breakdown?

### Step 2: Gather Status

Use the `managing-director` agent to coordinate a portfolio review. For each active initiative, assess:
- Current status (on track, at risk, delayed, complete)
- Key milestones achieved this period
- Upcoming milestones and deadlines
- Blockers or risks

### Step 3: Present Portfolio View

Format as a portfolio dashboard:

**Portfolio Summary**
- Total active initiatives
- On track / at risk / delayed counts
- Key accomplishments this period

**By Category**
For each project category, list initiatives with:
- Project name and owner
- Status indicator (green/yellow/red)
- One-line progress summary
- Next milestone and date

**Attention Required**
- Projects at risk or delayed
- Blockers requiring executive intervention
- Resource conflicts or dependencies

### Step 4: Follow-Up

Offer:
- **Deep dive** into a specific project
- **Project Olympia status** — `/jf-executive-suite:olympia-status`
- **Executive summary** — `/jf-executive-suite:executive-summary`

### Error Handling

- This is an agent-driven skill that does not require Snowflake
- If project status data is not current, note the last known status and suggest checking directly with project leads
