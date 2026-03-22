---
name: create-retro
description: Create a sprint or project retrospective when the user asks to run a retro, reflect on a sprint, review what happened, or do a team retrospective
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[sprint name, project name, or time period]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: retro, process, improvement
---

# Create Retro

## Overview

Generate a structured sprint or project retrospective using the Start/Stop/Continue format with accountability tracking. The retro reads previous retrospective documents to check whether past action items were completed and flags recurring themes that appear across multiple retros.

## Workflow

1. **Read previous retros** — Scan `.chalk/docs/product/` for files matching `*_retro_*`. Read each one to extract:
   - Previous action items and their status (completed, in progress, abandoned)
   - Recurring themes (issues raised in 2 or more retros)
   - Previous team health assessments for trend tracking
   If no previous retros exist, note this is the first retro and skip the accountability check.

2. **Read current context** — Check `.chalk/docs/product/` for PRDs, stakeholder updates, and any planning documents relevant to the sprint or project being reviewed. Check `.chalk/docs/engineering/` for incident reports or postmortems from the period.

3. **Parse the retro scope** — From `$ARGUMENTS`, identify the sprint name, project name, or time period under review. If unclear, ask what period or project the retro covers.

4. **Audit previous action items** — For each action item from the most recent retro:
   - Mark as Completed, In Progress, or Not Started
   - If Not Started, flag it and ask why it was deprioritized
   - If the same action item appears unfinished across 2+ retros, escalate it as a systemic blocker

5. **Identify recurring themes** — Compare themes from the current retro input against previous retros. If the same issue (e.g., "unclear requirements," "flaky tests," "too many meetings") appears in 2 or more retros, flag it as a recurring theme that requires structural intervention, not just another action item.

6. **Generate Start/Stop/Continue** — Organize feedback into three categories:
   - **Start**: Things the team should begin doing
   - **Stop**: Things the team should stop doing
   - **Continue**: Things that are working well and should be maintained

7. **Conduct team health check** — Assess three dimensions:
   - **Morale**: Team energy, motivation, and engagement
   - **Process Friction**: How much process overhead is slowing the team down
   - **Technical Health**: Code quality, test coverage, infrastructure stability
   Rate each as Healthy, Needs Attention, or Critical, with a one-line explanation.

8. **Write action items** — Every action item must be specific, assignable, and time-bound:
   - One clear action (not "improve communication")
   - An owner (person or team)
   - A due date
   - A way to verify completion

9. **Determine the next file number** — List files in `.chalk/docs/product/` to find the highest numbered file. Increment by 1.

10. **Write the file** — Save to `.chalk/docs/product/<n>_retro_<sprint_or_project>.md`.

11. **Confirm** — Present the retro with a summary: number of action items, any recurring themes flagged, and previous action item completion rate.

## Retro Structure

```markdown
# Retrospective: <Sprint/Project Name>

**Period**: <start date> to <end date>
**Date**: <YYYY-MM-DD>
**Participants**: <list of roles or teams involved>

## Previous Action Item Review

| Action Item | Owner | Due Date | Status | Notes |
|-------------|-------|----------|--------|-------|
| <from previous retro> | <owner> | <date> | Completed / In Progress / Not Started | <context> |

**Completion Rate**: <X of Y completed> (<percentage>%)

### Escalations

<Any action items that have been unfinished for 2+ retros. These require structural intervention.>

## Start / Stop / Continue

### Start
- <Things the team should begin doing, with rationale>

### Stop
- <Things the team should stop doing, with rationale>

### Continue
- <Things that are working and should be maintained>

## Recurring Themes

<Issues that have appeared in 2 or more retros. For each, note how many times it has appeared and what was tried previously.>

| Theme | Occurrences | Previous Attempts | Recommended Escalation |
|-------|-------------|-------------------|----------------------|
| <theme> | <count> | <what was tried> | <structural change needed> |

## Team Health Check

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Morale | Healthy / Needs Attention / Critical | <one-line explanation> |
| Process Friction | Healthy / Needs Attention / Critical | <one-line explanation> |
| Technical Health | Healthy / Needs Attention / Critical | <one-line explanation> |

**Trend**: <Compared to previous retro: improving, stable, or declining per dimension>

## Action Items

| ID | Action | Owner | Due Date | Verification |
|----|--------|-------|----------|-------------|
| R-1 | <specific action> | <person or team> | <YYYY-MM-DD> | <how to confirm it's done> |
| R-2 | <specific action> | <person or team> | <YYYY-MM-DD> | <how to confirm it's done> |
```

## Output

- **File**: `.chalk/docs/product/<n>_retro_<sprint_or_project>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Retrospective: <Sprint/Project Name>`

## Anti-patterns

- **No follow-up on previous action items** — A retro that does not review whether last retro's action items were completed is theater. The first section of every retro must audit the previous retro's commitments. If items are consistently incomplete, the retro process itself is broken.
- **Vague action items** — "Improve communication" is not actionable. "Schedule a 15-minute standup at 9am for the frontend team — Owner: Tech Lead — Due: next sprint start" is actionable. Every action item needs a specific action, owner, due date, and verification method.
- **Retro theater** — Same complaints appearing in retro after retro with no structural changes. If a theme recurs 3+ times, it needs escalation beyond the team level, not another action item.
- **No owner assignment** — Action items without owners are wishes. Every action item must have a named owner who is accountable for completion.
- **Skipping the health check** — Teams that only discuss tasks and deliverables miss process and morale issues that degrade performance over time. The health check surfaces problems before they become crises.
- **Blame-focused feedback** — "Stop" items should describe behaviors or processes, not criticize individuals. "Stop deploying on Fridays without a rollback plan" is constructive. Targeting individuals turns retros into blame sessions and kills psychological safety.
- **All Continue, no Start or Stop** — A retro with nothing to start or stop suggests the team is not being honest. Every period has room for improvement. If the team is reluctant to raise issues, the facilitation approach needs to change.
