---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: weekly-report
description: ">"
version: "1.0.0"
author: Claude Office Skills Contributors
license: MIT

# Categorization
category: productivity
tags:
  - report
  - weekly
  - status
  - update
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - create_docx
    - fill_docx_template

# Skill Capabilities
capabilities:
  - report_generation
  - status_tracking
  - progress_summary

# Language Support
languages:
  - en
  - zh
---

# Weekly Report

## Overview

This skill helps you create consistent, well-structured weekly status reports that communicate progress, blockers, and plans effectively to your team, manager, or stakeholders.

**Use Cases:**
- Individual contributor status updates
- Team lead rollup reports
- Project status updates
- Executive summaries
- Client progress reports

## How to Use

1. Tell me what you accomplished this week
2. Share any blockers or challenges
3. Describe your plans for next week
4. Specify your audience (manager, team, executives, clients)

**Example prompts:**
- "Create my weekly status report for my manager"
- "Generate a team rollup report from these individual updates"
- "Write an executive summary of our project progress"
- "Draft a client-facing weekly update"

## Report Templates

### Individual Weekly Report

```markdown
# Weekly Status Report

**Name:** [Your Name]
**Week of:** [Date Range]
**Department/Team:** [Team Name]

## 🎯 Summary
[1-2 sentence highlight of the week]

## ✅ Accomplishments
- [Completed task 1]
- [Completed task 2]
- [Completed task 3]

## 🚧 In Progress
| Task | Status | Expected Completion |
|------|--------|---------------------|
| [Task] | [%] | [Date] |

## 🚫 Blockers
- [Blocker 1] - [Impact] - [Help needed]

## 📅 Next Week's Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## 📊 Key Metrics (if applicable)
| Metric | This Week | Last Week | Target |
|--------|-----------|-----------|--------|
| [KPI] | [Value] | [Value] | [Target] |

## 💬 Notes/FYI
- [Any additional information]
```

### Team Rollup Report

```markdown
# Team Weekly Report

**Team:** [Team Name]
**Week of:** [Date Range]
**Report by:** [Your Name]

## 📊 Team Summary
- **Velocity:** [Points/tasks completed]
- **On Track:** [X] items
- **At Risk:** [X] items
- **Blocked:** [X] items

## 🏆 Key Wins
1. [Major accomplishment 1]
2. [Major accomplishment 2]

## 👥 Individual Updates

### [Team Member 1]
- ✅ [Completed]
- 🔄 [In progress]

### [Team Member 2]
- ✅ [Completed]
- 🔄 [In progress]

## 🚨 Team Blockers
| Blocker | Impact | Owner | Escalation Needed |
|---------|--------|-------|-------------------|
| [Issue] | High/Med/Low | [Name] | Yes/No |

## 📈 Progress Against Goals
| Goal | Target | Current | Status |
|------|--------|---------|--------|
| [Goal] | [Target] | [Current] | 🟢/🟡/🔴 |

## 📅 Next Week Focus
- [Team priority 1]
- [Team priority 2]

## 🆘 Support Needed
- [Request for other teams/management]
```

### Executive Summary Report

```markdown
# Executive Weekly Update

**Project/Initiative:** [Name]
**Week of:** [Date]
**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## TL;DR
[2-3 sentences capturing the most important information]

## Key Highlights
- ✅ [Major win or milestone]
- ⚠️ [Key risk or concern]
- 📊 [Important metric or trend]

## Progress vs Plan
| Milestone | Planned | Actual | Variance |
|-----------|---------|--------|----------|
| [Milestone] | [Date] | [Date] | [+/- days] |

## Financial Summary (if applicable)
| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| [Category] | $X | $Y | +/-$Z |

## Risks & Mitigations
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Plan] |

## Decisions Needed
- [Decision requiring executive input]

## Next Week Preview
- [Key activities/milestones]
```

### Client Progress Report

```markdown
# Weekly Progress Update

**Project:** [Project Name]
**Client:** [Client Name]
**Week of:** [Date]
**Prepared by:** [Your Name]

---

Dear [Client Name],

Please find below our weekly progress update for [Project Name].

## Summary
[Brief overview of week's progress]

## Completed This Week
- ✅ [Deliverable 1]
- ✅ [Deliverable 2]

## In Progress
| Item | Progress | Expected Delivery |
|------|----------|-------------------|
| [Work item] | [%] | [Date] |

## Upcoming Milestones
| Milestone | Date | Status |
|-----------|------|--------|
| [Milestone] | [Date] | On Track/At Risk |

## Items Requiring Your Input
- [ ] [Decision or feedback needed]
- [ ] [Approval required]

## Next Week's Focus
- [Planned activities]

---

Please let us know if you have any questions or concerns.

Best regards,
[Your Name]
```

## Writing Guidelines

### Accomplishments
- Start with action verbs (Completed, Delivered, Launched, Resolved)
- Be specific about outcomes, not just activities
- Quantify impact when possible
- Link to business value

**Good:** "Reduced API response time by 40%, improving user experience for 50K daily users"
**Bad:** "Worked on performance improvements"

### Blockers
- Be specific about the issue
- Explain the impact (delays, dependencies)
- State what help you need
- Include any attempted solutions

**Good:** "Waiting on API credentials from IT (ticket #1234). This blocks the integration work scheduled for this week. Need escalation to IT manager."
**Bad:** "Can't make progress on integration"

### Next Week Plans
- Be realistic about capacity
- Prioritize top 3-5 items
- Include dependencies
- Note any risks or assumptions

## Output Format

I'll generate a report matching your needs:

```markdown
# [Report Title]

**Period:** [Date range]
**Author:** [Name]
**Audience:** [Manager/Team/Executives/Client]

[Structured content based on template]
```

## Customization Options

Tell me your preferences:
- **Length:** Brief (bullet points), standard, detailed
- **Audience:** Team, manager, executives, clients
- **Focus:** Accomplishments, blockers, metrics
- **Frequency:** Can adapt for daily/bi-weekly/monthly
- **Tone:** Casual team update or formal stakeholder report

## Limitations

- Cannot access your actual work systems or calendars
- Relies on information you provide
- May need adjustment for your organization's specific format
- Should be reviewed for accuracy before sending

## Examples

### Example: Quick Status Update

**Input:** "I finished the dashboard redesign, fixed 3 bugs, still working on the user auth feature which is delayed because I'm waiting on the security review. Next week I'll focus on finishing auth and starting the mobile optimization."

**Output:**

# Weekly Status Report

**Name:** [Your Name]
**Week of:** [Current Week]

## 🎯 Summary
Completed dashboard redesign milestone. User authentication feature in progress, pending security review.

## ✅ Accomplishments
- Completed dashboard redesign (UI/UX milestone)
- Resolved 3 bugs in production
- Advanced user authentication feature development

## 🚧 In Progress
| Task | Status | Expected Completion |
|------|--------|---------------------|
| User Authentication Feature | 70% | Pending security review |

## 🚫 Blockers
- **Security Review Pending** - User auth feature cannot be deployed until security team completes review. Impact: 2-3 day delay. *Action needed: Follow up with security team on timeline.*

## 📅 Next Week's Priorities
1. Complete user authentication feature (post-security review)
2. Begin mobile optimization work
3. Address any feedback from dashboard redesign

## 💬 Notes
- Dashboard redesign ready for stakeholder demo when needed
