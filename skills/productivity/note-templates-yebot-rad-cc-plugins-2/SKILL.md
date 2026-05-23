---
name: note-templates
description: Collection of reusable templates for common Apple Notes use cases. Use when creating structured notes for meetings, journals, projects, or references.
---

# Note Templates for Apple Notes CLI

This skill provides ready-to-use templates for creating well-structured notes using the `notes` CLI tool.

## Template Categories

### Meeting Notes

#### Standard Meeting Template
```bash
notes create "Meeting - [Topic] - $(date +%Y-%m-%d)" << 'EOF'
# [Topic] Meeting

**Date**: $(date +%Y-%m-%d)
**Time**:
**Location/Call**:

## Attendees
- [ ] Person 1
- [ ] Person 2

## Agenda
1.
2.
3.

## Discussion Notes


## Decisions Made
-

## Action Items
| Owner | Task | Due Date |
|-------|------|----------|
|       |      |          |

## Follow-up
- Next meeting:
- Topics to revisit:
EOF
```

#### 1-on-1 Meeting Template
```bash
notes create "1-on-1 - [Person] - $(date +%Y-%m-%d)" << 'EOF'
# 1-on-1 with [Person]

**Date**: $(date +%Y-%m-%d)

## Check-in
- How are things going?
- Blockers or concerns?

## Topics to Discuss
- [ ]

## Their Updates


## My Updates


## Action Items
- [ ]

## Notes for Next Time

EOF
```

### Project Notes

#### Project Kickoff Template
```bash
notes create "[Project] - Kickoff" << 'EOF'
# [Project Name] - Project Kickoff

## Overview
**Start Date**:
**Target Completion**:
**Project Lead**:

## Objectives
1.
2.
3.

## Scope
### In Scope
-

### Out of Scope
-

## Key Stakeholders
-

## Milestones
| Milestone | Date | Status |
|-----------|------|--------|
|           |      |        |

## Risks & Mitigation
| Risk | Impact | Mitigation |
|------|--------|------------|
|      |        |            |

## Resources
-

## Success Criteria
-
EOF
```

#### Project Status Update Template
```bash
notes create "[Project] - Status - $(date +%Y-%m-%d)" << 'EOF'
# [Project] Status Update

**Date**: $(date +%Y-%m-%d)
**Status**: 🟢 On Track / 🟡 At Risk / 🔴 Blocked

## Summary
Brief overview of current state.

## Completed This Week
- ✅

## In Progress
- 🔄

## Planned Next Week
- 📋

## Blockers / Risks
-

## Metrics
-

## Notes
EOF
```

### Daily/Weekly Notes

#### Daily Journal Template
```bash
notes create "Journal - $(date +%Y-%m-%d)" << 'EOF'
# Daily Journal - $(date +%Y-%m-%d)

## Morning Intentions
Top 3 priorities for today:
1.
2.
3.

## Schedule
- [ ]

## Notes & Thoughts


## Wins Today
-

## Lessons Learned
-

## Tomorrow's Focus
-
EOF
```

#### Weekly Review Template
```bash
notes create "Weekly Review - $(date +%Y-W%V)" << 'EOF'
# Weekly Review - Week $(date +%V), $(date +%Y)

## Accomplishments
What did I complete this week?
-

## Challenges
What obstacles did I face?
-

## Learnings
What did I learn?
-

## Metrics
- Tasks completed:
- Goals achieved:

## Next Week Focus
Top priorities:
1.
2.
3.

## Notes
EOF
```

### Reference Notes

#### Research Notes Template
```bash
notes create "Research - [Topic]" << 'EOF'
# Research: [Topic]

**Date Started**: $(date +%Y-%m-%d)
**Status**: In Progress / Complete

## Question / Problem
What am I trying to learn or solve?


## Key Findings
### Finding 1

### Finding 2

## Sources
- [ ] Source 1: [link/reference]
- [ ] Source 2: [link/reference]

## Quotes & Data
>

## Analysis


## Conclusions


## Next Steps
-

## Related Notes
-
EOF
```

#### Book Notes Template
```bash
notes create "Book - [Title] by [Author]" << 'EOF'
# [Book Title]
**Author**: [Author Name]
**Date Read**: $(date +%Y-%m-%d)
**Rating**: ⭐⭐⭐⭐⭐

## Summary
Brief overview of the book.

## Key Concepts
1.
2.
3.

## Favorite Quotes
> "Quote here" (p. XX)

## Takeaways
What will I apply from this book?
-

## Related Books
-
EOF
```

### Quick Capture

#### Idea Note Template
```bash
notes create "Idea - [Brief Title]" << 'EOF'
# Idea: [Title]

**Date**: $(date +%Y-%m-%d)
**Category**:

## The Idea


## Problem It Solves


## Why Now?


## First Steps
1.
2.

## Resources Needed
-

## Related Ideas
-
EOF
```

#### Bug Report Template
```bash
notes create "Bug - [Brief Description]" << 'EOF'
# Bug: [Brief Description]

**Date**: $(date +%Y-%m-%d)
**Severity**: Low / Medium / High / Critical
**Status**: Open / Investigating / Fixed

## Description
What's happening?

## Steps to Reproduce
1.
2.
3.

## Expected Behavior


## Actual Behavior


## Environment
- OS:
- Version:
- Browser/App:

## Screenshots/Logs


## Possible Cause


## Solution

EOF
```

## Usage Tips

1. **Customize templates**: Modify these templates to match your workflow
2. **Create template notes**: Store your customized templates as notes themselves
3. **Use date commands**: The `$(date +%Y-%m-%d)` syntax auto-fills the current date
4. **Consistent naming**: Follow naming conventions for easy searching

## Template Selection Guide

| Use Case | Template |
|----------|----------|
| Team meeting | Standard Meeting |
| Manager sync | 1-on-1 Meeting |
| New initiative | Project Kickoff |
| Weekly updates | Project Status |
| Personal reflection | Daily Journal |
| End of week | Weekly Review |
| Learning topic | Research Notes |
| Reading notes | Book Notes |
| Brainstorming | Idea Note |
| Issue tracking | Bug Report |
