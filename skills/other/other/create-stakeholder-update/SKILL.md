---
name: create-stakeholder-update
description: Create a stakeholder update when the user asks to write a status update, send a project update, prepare an executive summary, or draft a BLUF update
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[project or time period for the update]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: communication, stakeholders, reporting
---

# Create Stakeholder Update

## Overview

Generate a stakeholder update using the BLUF (Bottom Line Up Front) communication pattern. The update leads with the most important information, uses traffic light status indicators per workstream, and clearly separates FYI items from items that need a decision. Reads project context from docs, git activity, and existing artifacts to ground the update in facts.

## Workflow

1. **Read project context** — Scan available sources for current state:
   - `.chalk/docs/product/` for PRDs, roadmaps, stakeholder updates, and retros
   - `.chalk/docs/engineering/` for architecture docs, incident reports, and postmortems
   - `.chalk/docs/ai/` for any analysis or research documents
   - Check for a product profile (`0_product_profile.md`) to understand project scope
   - If previous stakeholder updates exist, read the most recent one for continuity

2. **Check recent activity** — Use `Bash` to review recent git log for commits, merged PRs, and release tags within the update period. This grounds the "Key Accomplishments" section in actual work, not aspirations.

3. **Parse the update scope** — From `$ARGUMENTS`, identify the project, time period, and intended audience. If the audience is unclear, default to executive stakeholders (concise, outcome-focused, no jargon).

4. **Write the BLUF summary** — Draft 2-3 sentences that answer: "What does the reader need to know RIGHT NOW?" This is the most important section. A stakeholder who reads nothing else should understand the project status from these sentences alone.

5. **Assign traffic light status** — For each workstream or major initiative:
   - **Green**: On track, no blockers, progressing as planned
   - **Yellow**: At risk, minor blockers or delays, needs monitoring
   - **Red**: Off track, major blockers, needs immediate attention or decision
   Each status must include a one-line explanation. Never use green for everything unless genuinely warranted.

6. **Separate risks into FYI and Needs Decision** — Every risk or blocker must be categorized:
   - **FYI**: Stakeholders should be aware, but no action is needed from them
   - **Needs Decision**: A specific decision is required, with a clear question and a recommended option

7. **Include metrics** — If a metrics framework exists in the docs, include a metrics snapshot showing current values against targets. If no framework exists, note that metrics tracking is not yet established.

8. **Determine the next file number** — List files in `.chalk/docs/product/` to find the highest numbered file. Increment by 1.

9. **Write the file** — Save to `.chalk/docs/product/<n>_stakeholder_update_<date>.md`.

10. **Confirm** — Present the update with the BLUF summary and any items that need decisions highlighted.

## Update Structure

```markdown
# Stakeholder Update: <Project/Team Name>

**Period**: <start date> to <end date>
**Date**: <YYYY-MM-DD>
**Author**: <role>

## BLUF (Bottom Line Up Front)

<2-3 sentences. What does the reader need to know RIGHT NOW? Lead with the most critical information. If there is a decision needed, state it here.>

## Status Overview

| Workstream | Status | Summary |
|------------|--------|---------|
| <workstream 1> | :green_circle: Green | <one-line explanation> |
| <workstream 2> | :yellow_circle: Yellow | <one-line explanation> |
| <workstream 3> | :red_circle: Red | <one-line explanation> |

## Key Accomplishments (Past Period)

- <Accomplishment with concrete outcome, not just activity>
- <Accomplishment tied to a deliverable, metric, or milestone>

## Upcoming Milestones (Next Period)

| Milestone | Target Date | Confidence | Notes |
|-----------|-------------|------------|-------|
| <milestone> | <YYYY-MM-DD> | High / Medium / Low | <context> |

## Risks & Blockers

### FYI (Awareness Only)

- <Risk or issue the stakeholder should know about, but no action is required from them>

### Needs Decision

| Decision Needed | Options | Recommendation | Deadline |
|----------------|---------|----------------|----------|
| <specific question> | <Option A / Option B> | <recommended option with rationale> | <by when> |

## Metrics Snapshot

| Metric | Previous | Current | Target | Trend |
|--------|----------|---------|--------|-------|
| <metric> | <value> | <value> | <target> | Improving / Stable / Declining |

<If no metrics framework exists: "Metrics tracking is not yet established. See [action item / recommendation] for setup.">
```

## Output

- **File**: `.chalk/docs/product/<n>_stakeholder_update_<date>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Stakeholder Update: <Project/Team Name>`

## Anti-patterns

- **Burying the lead** — If the project is off track or needs a decision, that information must be in the first two sentences, not buried in a "Risks" section at the bottom. Stakeholders skim. The BLUF exists so they cannot miss the critical information.
- **No traffic light status** — Listing updates without a clear status indicator forces the reader to interpret whether things are good or bad. Every workstream gets a Green, Yellow, or Red. No exceptions, no "it depends."
- **FYI-only updates with no decisions** — If every update is "everything is fine, just keeping you informed," stakeholders stop reading. If there are genuinely no decisions needed, include forward-looking risks or upcoming decision points.
- **Progress without metrics** — "We made great progress on the backend" is unverifiable. "Backend API coverage reached 85% of planned endpoints (target: 100% by March 15)" is concrete. Tie accomplishments to measurable outcomes.
- **All-green status** — Reporting all workstreams as green when there are known risks or delays erodes trust. Stakeholders respect honesty. A yellow with a mitigation plan is far better than a green that becomes a surprise red next period.
- **Activity reporting instead of outcomes** — "We had 15 meetings and reviewed 30 PRs" describes activity. "Shipped the authentication module and reduced login latency by 40%" describes outcomes. Stakeholders care about outcomes.
- **No continuity with previous updates** — Each update should reference the previous one implicitly: milestones that were upcoming should now appear as accomplishments (or be explained if missed). Stakeholders notice when items silently disappear.
