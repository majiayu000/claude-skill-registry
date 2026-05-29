---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: meeting-notes
description: ">"
version: "1.0.0"
author: Claude Office Skills Contributors
license: MIT

# Categorization
category: productivity
tags:
  - meeting
  - notes
  - summary
  - action-items
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

# Skill Capabilities
capabilities:
  - note_structuring
  - action_extraction
  - summarization

# Language Support
languages:
  - en
  - zh
---

# Meeting Notes

## Overview

This skill transforms raw meeting notes, transcripts, or audio summaries into clear, structured documentation with action items, decisions, and key takeaways.

**Use Cases:**
- Converting messy handwritten notes to clean summaries
- Processing meeting transcripts
- Extracting action items and owners
- Creating meeting minutes for distribution
- Summarizing long discussions into key points

## How to Use

1. Paste your raw meeting notes, transcript, or description
2. Tell me the meeting type (standup, project review, client call, etc.)
3. Specify any required format or template
4. I'll create structured notes with action items

**Example prompts:**
- "Organize these meeting notes and extract action items"
- "Create formal meeting minutes from this transcript"
- "Summarize the key decisions from our project review"
- "Turn this brainstorm session into a structured document"

## Meeting Note Templates

### Standard Meeting Summary

```markdown
# Meeting Summary

**Meeting:** [Title]
**Date:** [Date]
**Attendees:** [Names]
**Duration:** [Time]

## Purpose
[One sentence describing meeting objective]

## Key Discussion Points
1. [Topic 1]
   - [Key point]
   - [Key point]

2. [Topic 2]
   - [Key point]
   - [Key point]

## Decisions Made
- [ ] [Decision 1]
- [ ] [Decision 2]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Task] | [Name] | [Date] | Pending |

## Next Steps
- [Next meeting/milestone]

## Notes
[Any additional context or parking lot items]
```

### Quick Standup Notes

```markdown
# Daily Standup - [Date]

## [Team Member 1]
**Yesterday:** [Completed tasks]
**Today:** [Planned tasks]
**Blockers:** [Issues, if any]

## [Team Member 2]
...

## Team Blockers
- [Blocker requiring escalation]

## Announcements
- [Team-wide updates]
```

### Client Meeting Notes

```markdown
# Client Meeting Notes

**Client:** [Company Name]
**Date:** [Date]
**Our Team:** [Names]
**Client Team:** [Names]

## Meeting Objective
[Why we met]

## Client Feedback/Requests
1. [Feedback point]
2. [Request]

## Our Commitments
- [What we promised to deliver]
- [Timeline]

## Client Commitments
- [What they will provide]
- [Timeline]

## Follow-up Required
| Item | Owner | Due |
|------|-------|-----|
| [Task] | [Name] | [Date] |

## Next Meeting
[Date/Time/Agenda preview]
```

### Project Review Notes

```markdown
# Project Review: [Project Name]

**Date:** [Date]
**Phase:** [Current phase]
**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Off Track

## Progress Update
- **Completed:** [Milestones achieved]
- **In Progress:** [Current work]
- **Upcoming:** [Next milestones]

## Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| [KPI] | [Target] | [Actual] | ✅/⚠️/❌ |

## Risks & Issues
| Risk/Issue | Impact | Mitigation | Owner |
|------------|--------|------------|-------|
| [Description] | High/Med/Low | [Plan] | [Name] |

## Decisions Needed
- [Decision requiring escalation]

## Action Items
- [ ] [Task] - @[Owner] - Due: [Date]
```

## Processing Guidelines

### Extracting Action Items

Look for phrases indicating tasks:
- "We need to..." / "Someone should..."
- "Can you..." / "Will you..."
- "Let's..." / "Action:"
- Names + verbs (e.g., "John will prepare...")
- Deadlines mentioned with tasks

### Identifying Decisions

Look for:
- "We've decided..." / "The decision is..."
- "Going forward, we will..."
- "Agreed:" / "Confirmed:"
- Consensus language ("everyone agreed...")

### Determining Owners

- Explicitly named: "Sarah will handle..."
- Role-based: "The design team will..."
- Default to meeting organizer if unclear
- Flag unassigned items for follow-up

## Output Format

```markdown
## Meeting Summary: [Title]

📅 **Date:** [Date]
👥 **Attendees:** [List]

### 📋 Summary
[2-3 sentence overview]

### 💡 Key Points
1. [Point 1]
2. [Point 2]
3. [Point 3]

### ✅ Decisions
- [Decision 1]
- [Decision 2]

### 📌 Action Items
| # | Action | Owner | Due | Priority |
|---|--------|-------|-----|----------|
| 1 | [Task] | [Name] | [Date] | High/Med/Low |

### 🔜 Next Steps
- [Next meeting or milestone]

### 📝 Parking Lot
- [Items to address later]
```

## Customization Options

Tell me your preferences:
- **Format:** Bullet points, table, prose, or formal minutes
- **Detail level:** Executive summary, standard, or detailed
- **Focus:** Action items only, decisions only, or comprehensive
- **Style:** Casual team notes or formal documentation

## Limitations

- Cannot attend or record meetings
- Accuracy depends on quality of input notes
- May need clarification on ambiguous pronouns or acronyms
- Cannot verify commitments or deadlines - review before distributing

## Examples

### Example: Raw Notes to Structured Summary

**Input:**
```
product meeting 3/15
talked about launch timeline, sarah thinks we need 2 more weeks
john mentioned the bug in checkout - high priority
decided to push launch to april 1
need to update stakeholders
maria will fix the checkout bug by friday
also discussed new feature requests from customers - will prioritize next sprint
john to send customer feedback summary
```

**Output:**

## Meeting Summary: Product Launch Review

📅 **Date:** March 15, 2024
👥 **Attendees:** Sarah, John, Maria

### 📋 Summary
Reviewed launch timeline and decided to postpone launch by 2 weeks to April 1 due to critical checkout bug. Discussed customer feature requests for future prioritization.

### 💡 Key Points
1. Original launch timeline insufficient - need 2 more weeks
2. Critical checkout bug discovered - must fix before launch
3. Customer feature requests collected for next sprint prioritization

### ✅ Decisions
- Launch date moved from mid-March to **April 1**
- Checkout bug is **highest priority**
- Feature requests to be prioritized in next sprint planning

### 📌 Action Items
| # | Action | Owner | Due | Priority |
|---|--------|-------|-----|----------|
| 1 | Fix checkout bug | Maria | Friday (3/17) | 🔴 High |
| 2 | Update stakeholders on new launch date | [Unassigned] | ASAP | 🔴 High |
| 3 | Send customer feedback summary | John | [TBD] | 🟡 Medium |

### 🔜 Next Steps
- Follow-up on bug fix progress
- Stakeholder communication about timeline change
- Sprint planning to prioritize customer requests
