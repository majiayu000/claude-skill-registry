---
name: set-up-workday
description: Executes the full morning enablement workflow, including intelligence gathering, workspace prep, and executive brief synthesis, in a single skill.
license: Proprietary
---

# Set Up Workday

## Overview
Set Up Workday is the principal's end-to-end morning activation skill. It now embeds the full morning intelligence workflow directly, combining intelligence gathering, communications triage, workspace preparation, and situational news into one orchestrated experience. Invoke it whenever the principal needs an actionable, decision-ready morning package without chaining multiple skills manually.

## Quick Start
1. Receive the user prompt (e.g., "Set up my workday" or "Kick off today using our standard morning stack").
2. Confirm the target date (default to today) and optional toggles such as skipping email checks or focusing on specific accounts.
3. Execute the embedded components to gather unread emails, calendar events, Drive activity, task synthesis, news, and workspace preparation.
4. Return a prioritized executive brief formatted for immediate action.

## How It Works
1. **Normalize the target date** using Reverse Date and Reverse Month so downstream skills and folder naming stay consistent.
2. **Pull unread email intelligence** from the past 48 hours, extracting sender, subject, deadlines, expectations, and Gmail links.
3. **Audit today's calendar** (Asia/Singapore timezone) for conflicts, prep requirements, attendees, and direct event links.
4. **Review Drive file priorities** from the last 24 hours, highlighting SNMG18 Meeting Minutes activity plus any other recent files with summaries and URLs.
5. **Synthesize the What-I-Need-To-Do brief** by merging action items, prep work, and follow-ups surfaced across email, calendar, and Drive inputs.
6. **Capture a news snapshot** with two international and two Singapore headlines, each with one-sentence context and source links.
7. **Stage the workspace** by invoking the Work Day skill to verify or create the daily Google Drive structure and surface key links.
8. **Compose the executive kickoff brief** by deduplicating overlapping insights, prioritizing urgent items, and formatting the output into the standard sections.

## Embedded Morning Intelligence Components
The five morning intelligence components are now native to Set Up Workday. Each component must be run whenever relevant data exists unless the user explicitly opts out.

### Component 1: Unread Emails (Last 48 Hours)
- Query Gmail for all unread messages received in the last 48 hours.
- For each message, capture the sender, subject, received date/time, a 30-word summary, explicit expectations, deadlines, and a clickable Gmail URL.
- If no unread emails match, state: "No unread emails in the last 48 hours."

### Component 2: Today's Calendar Events
- Query Google Calendar for the current day (Asia/Singapore timezone).
- For each event, include start/end time (24-hour format), title, location, attendees, and a clickable calendar URL.
- Flag any conflicts or back-to-back meetings.
- If the day is empty, state: "No calendar events scheduled for today."

### Component 3: Drive File Priorities
- Scan Google Drive for items modified in the last 24 hours, prioritizing the **SNMG18 Meeting Minutes** folder plus any other notable updates.
- For each file, share the name, last modified timestamp, a 30-word summary, and a clickable link.
- If no relevant files appear, state: "No recent file updates."

### Component 4: What-I-Need-To-Do Brief
- Merge action items from unread emails, calendar prep requirements, and Drive follow-ups.
- For each task, provide a concise description, the source with a clickable link, and any known due date.

### Component 5: News Snapshot
- Surface two top international news stories and two top Singapore news stories.
- Each item includes a succinct headline, one-sentence context, and a source link.

## Output Format
Structure the morning package in a professional, scannable executive layout with sections for: Priorities & Quick Wins, Urgent Follow-Ups, Today's Schedule, Workspace & Resources, What-I-Need-To-Do, News Snapshot, and Recommended Next Actions. Every data point should cite its originating source link.

## Key Features
- **Integrated intelligence**: Consolidates unread email, calendar, Drive, task synthesis, and news within the orchestration.
- **End-to-end workflow**: Chains supporting skills (Recent Emails, Starred Email, Search Calendar, Recent Files, Reverse Date, Reverse Month, Work Day) without requiring separate manual triggers.
- **Data de-duplication**: Reuses identifiers (message IDs, event IDs, file IDs) to avoid redundant fetches and highlight net-new insights.
- **Workspace readiness**: Ensures Google Drive folders and links are staged alongside the brief for immediate execution.
- **Configurable toggles**: Supports skip flags (email, calendar, news) and account-specific focus modes for flexible mornings.

## Success Criteria
**The skill succeeds when:**
- Each embedded component executes (unless intentionally skipped) and returns accurate, current intelligence.
- The final brief includes prioritized actions, urgent follow-ups, schedule snapshot, workspace links, task list, and news tied to the requested date.
- Users receive actionable recommendations with traceable sources for every item in the summary.

## What This Skill Does
✓ Activates the full morning intelligence and workspace stack from a single command.
✓ Normalizes target dates and reuses them across calendar, files, news queries, and Drive preparation.
✓ Produces an executive-format kickoff brief with clear sections, links, and prioritization.

## What This Skill Does NOT Do
✗ Replace underlying skills' authentication or permission flows.
✗ Invent new data sources beyond the defined dependency list.
✗ Auto-schedule focus blocks or push tasks into external project managers (future consideration).

## Limitations & Prerequisites
- **Requires**: Access to Recent Emails, Starred Email, Search Calendar, Recent Files, Reverse Date, Reverse Month, Work Day, news APIs, and Gmail/Drive permissions.
- **Assumes**: Google Workspace connectivity, consistent timezone handling (default Asia/Singapore), and cached credentials for Gmail, Calendar, Drive, and news sources.
- **Limitations**: Does not yet integrate Asana/Jira queues; brief delivery remains Markdown rendered within Claude unless extended.

## Usage

### Basic Usage
```
User: "Set up my workday."
Assistant: Runs the full orchestration, returning the briefing for today.
```

### Advanced Usage
```
User: "Prepare everything I need for work this morning for 2025-11-04. Skip email and news, focus on APAC enterprise accounts."
Assistant: Normalizes the provided date, toggles off email and news checks, scopes downstream skills to APAC enterprise filters, and delivers the kickoff brief.
```

### Configuration
- Optional flags: `include_email` (bool), `include_news` (bool), `focus_accounts` (list of strings), `time_window` (start/end timestamps), `dry_run_folders` (bool).
- Cache normalized dates, folder IDs, and news responses within the session to prevent repeated computations.

## Scripts

### Orchestrator: `scripts/set_up_workday.py`
**Purpose**: Placeholder for the automation layer that sequences dependency skills, manages state, and formats the final brief.
**Status**: Not yet implemented; use this specification to guide future development.
**Expected Responsibilities**:
- Handle prompt parsing and configuration toggles.
- Execute dependency calls with shared identifiers (message IDs, event IDs, file IDs).
- Deduplicate overlapping items and assemble the final briefing template.

## Integration Opportunities

### Asana or Jira Task Sync
**Purpose**: Pull outstanding tasks and optionally create follow-up tasks from the morning brief.
**Proposed Implementation**: Optional step after synthesizing the plan that queries project management APIs for blockers or logs new action items.
**Prerequisites**: API credentials with write access, project mappings per account or initiative.
**Usage Context**: Enable when the principal wants workday setup to include outstanding project tasks.

### Slack Notifications
**Purpose**: Deliver the final kickoff brief to a private Slack channel for archival and quick reference.
**Proposed Implementation**: Post-brief webhook call with formatted Markdown and key links.
**Prerequisites**: Slack app with chat:write scope and channel ID configuration.
**Usage Context**: Teams needing asynchronous distribution of the morning setup output.

## Related Skills
- **recent-emails** and **starred-email**: Provide actionable email threads and context.
  - *This skill differs by*: De-duplicating and highlighting next actions across inbox feeds.
  - *Can be used together with*: Feed thread IDs between these skills for deeper metadata lookups.
- **work-day**: Ensures Google Drive folder structure is ready.
  - *This skill differs by*: Triggering Work Day's checks as part of the morning orchestration.

## Extending This Skill
To extend Set Up Workday with new capabilities:
1. Implement `scripts/set_up_workday.py` following the orchestration responsibilities above.
2. Add optional integrations (e.g., task managers) and document configuration steps under a new `references/` guide.
3. Update this SKILL.md with additional usage patterns and toggle descriptions as features roll out.

## Common Issues

**Issue**: Missing permissions for Gmail, Calendar, Drive, or news APIs during component calls.
**Solution**: Re-authenticate the corresponding services and ensure OAuth scopes include read access for messages, events, files, and headlines.

**Issue**: Duplicate follow-up items appearing in both Recent Emails and Starred Email sections.
**Solution**: Use message IDs returned by Starred Email to filter Recent Emails responses before synthesizing the plan.

**Issue**: Work Day reports folders already exist but links are missing from the final brief.
**Solution**: Cache folder IDs returned from Work Day and explicitly inject them into the Workspace & Resources section before rendering.

## Final Formatting Adjustment
After assembling the executive kickoff brief, convert all headings from heading styles to normal text while retaining their original font size and formatting. This ensures the document preserves the intended visual hierarchy without relying on heading style metadata.

## Version History
- **2.0.0** (2025-11-04): Embedded the morning intelligence components directly into Set Up Workday and retired the standalone morning briefing skill.
- **1.0.0** (2025-11-03): Initial specification outlining workflow, dependencies, and integration opportunities.
