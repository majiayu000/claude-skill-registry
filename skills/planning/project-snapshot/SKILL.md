---
context: fork
---

# Project Snapshot Skill

## Purpose

Generate quick status overview of all active engineering projects, showing progress, blockers, and immediate priorities.

## Usage

- `/project-snapshot` - All active projects
- `/project-snapshot all` - All projects including paused/completed
- `/project-snapshot [project-name]` - Detailed snapshot for specific project

## Instructions

When this skill is invoked:

1. **Find all project files** using Glob:

   ```
   Project*.md
   ```

2. **Read each project file** to extract:
   - Project title and status
   - Related ADRs
   - Related tasks (completed and pending)
   - Recent meetings
   - Key stakeholders
   - Current blockers/risks
   - DPIA status (if applicable)
   - Last modified date

3. **Filter by status** (unless 'all' specified):
   - Active projects (status: active, in progress, or null)
   - Exclude paused and completed unless 'all' flag used

4. **For each project, assess:**
   - Health status: 🟢 On track, 🟡 At risk, 🔴 Blocked
   - Recent activity (meetings/tasks in last 7 days)
   - Pending actions and priorities
   - Compliance status (DPIA, Cyber, etc.)

5. **Generate formatted snapshot:**

### Report Structure

```markdown
# Engineering Projects Snapshot

**Generated**: [current date]
**Scope**: [Active projects / All projects]

## Executive Summary

- **Total Active Projects**: [count]
- **On Track**: 🟢 [count]
- **At Risk**: 🟡 [count]
- **Blocked**: 🔴 [count]
- **Paused**: [count]
- **Completed This Month**: [count]

## Projects by Status

### 🟢 On Track ([count] projects)

#### [[Project - 777-X EIS Programme]]

- **Status**: In Progress
- **Health**: 🟢 On track
- **Recent Progress**:
  - ✅ 2 ADRs completed (GBST virtualization, CSCT deployment)
  - ✅ PKI infrastructure planned
  - 📅 Last meeting: 2026-01-07
- **Next Actions**:
  - VendorA certificate migration to YourOrg Cloud PKI
  - AWS EC2 deployment planning
- **Owner**: [[Sarah Chen]] (PM), [[James Rivera]] (Tech Lead)
- **Compliance**: N/A (aviation certified)
- **Timeline**: 2027-05-04 - 2027-05-05

#### [[Project - VendorTooling Tooling - v9 Upgrade]]

- **Status**: Active
- **Health**: 🟢 On track
- **Recent Progress**:
  - ✅ ADR completed [ARCH-61](https://...)
  - ✅ DPIA threshold assessment complete
  - 📅 Infrastructure kick-off today (2026-01-07)
- **Next Actions**:
  - Infrastructure deployment
  - Full DPIA if required
- **Owner**: [[Sarah Chen]]
- **Compliance**: DPIA 6285 (threshold complete)
- **Timeline**: [timeframe]

### 🟡 At Risk ([count] projects)

#### [[Project - VendorPLM SaaS Migration]]

- **Status**: Active
- **Health**: 🟡 At risk - DPIA pending >60 days
- **Recent Progress**:
  - 📅 Meetings held regularly
  - ⏳ DPIA under review since 2025-10-08
- **Blockers**:
  - ⚠️ DPIA approval pending (OneTrust 6284)
  - Awaiting YourOrg Data Protection Officer decision
- **Next Actions**:
  - [[Sarah Chen]] to follow up with DPO
  - Cannot proceed to deployment without DPIA approval
- **Owner**: [Project owner]
- **Compliance**: 🟡 DPIA 6284 under review
- **Timeline**: [timeframe]

### 🔴 Blocked ([count] projects)

#### [[Project - Example Blocked Project]]

- **Status**: Active (blocked)
- **Health**: 🔴 Blocked
- **Blocker**: [Description of blocking issue]
- **Impact**: [What is impacted]
- **Next Actions**: [Required to unblock]
- **Owner**: [[Person]]
- **Escalation**: Required by [date]

### ⏸️ Paused ([count] projects)

(Only shown if 'all' flag used)

#### [[Project Name]]

- **Paused Since**: YYYY-MM-DD
- **Reason**: [Why paused]
- **Resume Date**: [When expected to resume]

### ✅ Recently Completed ([count] projects)

(Only shown if 'all' flag used or completed in last 30 days)

## Projects by Technology Area

### Cloud & AWS (5 projects)

- [[Project - 777-X EIS Programme]] 🟢
- [[Project - AIIncidentProcessor]] 🟢
- [[Project - MyDataIntegration]] 🟢

### MRO & Engineering Systems (4 projects)

- [[Project - MaintenanceSystem Implementation]] 🟡 (Entra ID migration needed)
- [[Project - VendorTooling Tooling - v9 Upgrade]] 🟢
- [[Project - VendorPLM SaaS Migration]] 🟡 (DPIA pending)

### Data Integration (3 projects)

- [[Project - MyDataIntegration]] 🟢
- [[Project - DataPlatform Programme]] 🟢

## Key Milestones This Week

| Project                 | Milestone                   | Due Date   | Status     |
| ----------------------- | --------------------------- | ---------- | ---------- |
| [[VendorTooling]]       | Infrastructure kick-off     | 2026-01-07 | ✅ Today   |
| [[AIIncidentProcessor]] | Send ADRs to Lead Architect | 2026-01-07 | ⏳ Pending |
| [[MyDataIntegration]]   | SAP data call               | 2026-01-07 | 📅 Today   |

## Immediate Attention Required

### High Priority Actions (Next 24-48 Hours)

1. **[[Project - AIIncidentProcessor]]**
   - Task: Send API Gateway and Bedrock ADRs to Lead Architect
   - Owner: Alex Thompson
   - Due: Today (2026-01-07)

2. **[[Project - VendorPLM SaaS Migration]]**
   - Action: Follow up on DPIA approval (>60 days pending)
   - Owner: [[Sarah Chen]]
   - Urgency: High (blocking deployment)

### Medium Priority Actions (This Week)

1. **[[Project - MaintenanceSystem Implementation]]**
   - Planning: Entra ID migration roadmap
   - Owner: [PM/Owner]
   - Note: Technical debt documented

2. **[[Project - SPARK]]**
   - Action: DPIA follow-up
   - Owner: [[Sarah Chen]]

## Compliance Overview

| Project               | DPIA Status               | Cyber Status | Other Compliance             |
| --------------------- | ------------------------- | ------------ | ---------------------------- |
| [[VendorTooling]]     | Threshold complete (6285) | ✅ Complete  | -                            |
| [[VendorPLM]]         | Under review (6284)       | ⏳ Pending   | -                            |
| [[SPARK]]             | Under review (6276)       | ⏳ Pending   | -                            |
| [[NewProductLine]]    | N/A                       | ✅ Complete  | ✅ Aviation certified        |
| [[MaintenanceSystem]] | N/A                       | ✅ Complete  | ⚠️ Entra ID migration needed |

## Resource Allocation

### By Project Manager

- **[[Sarah Chen]]**: 5 active projects
- **Other PMs**: [count] projects

### By Technical Lead

- **[[James Rivera]]**: 3 active projects
- **Alex Thompson**: Architecture support across all projects

## Recent Wins 🎉

- ✅ VendorTooling ADR completed (ARCH-61)
- ✅ NewProductLine architecture decisions formalized (2 ADRs)
- ✅ PKI knowledge base created
- ✅ DPIA tracking system established

## Risks & Concerns

### Critical Risks

1. **DPIA Approvals Delayed**: VendorPLM and SPARK >60 days pending
2. **Technical Debt**: MaintenanceSystem Entra ID migration unfunded

### Medium Risks

1. **Resource Constraints**: [If identified]
2. **Timeline Pressures**: [If identified]

## Recommended Actions

**For Leadership:**

1. Escalate DPIA approval delays (VendorPLM, SPARK)
2. Fund MaintenanceSystem Entra ID migration work
3. Review resource allocation across 20+ active projects

**For Project Teams:**

1. Complete AIIncidentProcessor ADR distribution today
2. DPIA follow-ups this week (Sarah)
3. Plan NewProductLine AWS implementation roadmap

**For Architecture:**

1. Continue ADR documentation for new projects
2. Review and update existing ADRs quarterly
3. Maintain PKI and security knowledge bases

## Projects Summary Table

| Project                 | Status | Health | Owner          | Recent Activity      | Next Milestone           |
| ----------------------- | ------ | ------ | -------------- | -------------------- | ------------------------ |
| [[NewProductLine EIS]]  | Active | 🟢     | [[Sarah Chen]] | 2 ADRs created       | AWS deployment planning  |
| [[VendorTooling]]       | Active | 🟢     | [[Sarah Chen]] | ADR complete         | Infra kick-off (today)   |
| [[MaintenanceSystem]]   | Active | 🟡     | [PM]           | Tech debt documented | Entra migration planning |
| [[VendorPLM]]           | Active | 🟡     | [PM]           | DPIA pending         | DPIA approval            |
| [[SPARK]]               | Active | 🟡     | [PM]           | DPIA pending         | DPIA approval            |
| [[AIIncidentProcessor]] | Active | 🟢     | [PM]           | ADR task created     | Send ADRs to Roy         |
| [[MyDataIntegration]]   | Active | 🟢     | [PM]           | SAP data call        | [Milestone]              |
```

6. **Output the snapshot** as formatted markdown

7. **Provide actionable insights:**
   - Flag urgent items requiring immediate attention
   - Identify patterns across projects (e.g., multiple DPIA delays)
   - Highlight resource constraints or bottlenecks
   - Recommend prioritization

8. **Optionally save snapshot** by asking user:
   - "Would you like me to save this project snapshot as a Page?"
   - If yes, create `Page - Project Snapshot [date].md`

## Detailed Project View

If user requests specific project (e.g., `/project-snapshot AIIncidentProcessor`):

```markdown
# Project Snapshot: [[Project Name]]

**Generated**: [current date]

## Project Overview

- **Full Title**: [Full project name]
- **Status**: [Active/Paused/Completed]
- **Health**: 🟢/🟡/🔴
- **Programme**: [If part of larger programme]
- **Timeline**: [Start] - [End]

## Key Stakeholders

- **Project Manager**: [[Person]]
- **Technical Lead**: [[Person]]
- **Solution Architect**: [[Person]]
- **Collaborators**: [List]

## Recent Activity (Last 7 Days)

- ✅ [Completed items]
- 📅 [Meetings held]
- 📝 [Documentation created]
- 🔄 [In progress items]

## Architecture & Technical Decisions

- [[ADR - Title 1]] (status)
- [[ADR - Title 2]] (status)
- [Technical approach summary]

## Tasks & Actions

### Completed Recently

- [x] [[Task - Completed]]

### In Progress

- [ ] [[Task - In Progress]] (Owner, Due date)

### Upcoming

- [ ] [[Task - Upcoming]] (Owner, Due date)

## Meetings & Touchpoints

- [[Meeting - Recent]] (Date)
- Next scheduled: [Date and purpose]

## Compliance & Security

- **DPIA Status**: [Status and OneTrust ID if applicable]
- **Cyber Approval**: [Status]
- **Other Compliance**: [Any other requirements]

## Current Blockers

1. [Blocker description] - Impact: [X], Owner: [[Person]]

## Risks & Mitigations

| Risk   | Impact       | Probability  | Mitigation | Owner      |
| ------ | ------------ | ------------ | ---------- | ---------- |
| [Risk] | High/Med/Low | High/Med/Low | [Action]   | [[Person]] |

## Dependencies

- Depends on: [[Other Project/System]]
- Depended on by: [[Other Project/System]]

## Key Metrics

- Tasks completed: [X]
- ADRs created: [X]
- Meetings held: [X]
- Days since last activity: [X]

## Next 30 Days

1. [Upcoming milestone 1]
2. [Upcoming milestone 2]
3. [Upcoming milestone 3]
```

## Notes

- Prioritize actionable information over historical data
- Use health indicators (🟢🟡🔴) for quick visual status
- Flag projects with no recent activity (>14 days)
- Cross-reference with DPIA status and ADR reports
- Calculate "days since last activity" for each project
- Use UK English spelling throughout

## Examples

**Example 1:**
User: `/project-snapshot`
Assistant: [Generates overview of 7 active projects, flags 2 at risk (DPIA delays), highlights 3 urgent actions]

**Example 2:**
User: `/project-snapshot all`
Assistant: [Shows all 25 projects including paused and completed, organized by status]

**Example 3:**
User: `/project-snapshot NewProductLine`
Assistant: [Detailed snapshot of NewProductLine project showing recent ADRs, upcoming AWS deployment, stakeholders]
