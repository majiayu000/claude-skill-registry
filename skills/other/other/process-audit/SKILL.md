---
name: process-audit
description: Review process health and bottlenecks
role_groups: [operations]
jtbd: |
  Processes break down over time but you don't know where. This gathers feedback 
  on a process, identifies bottlenecks or friction, suggests improvements, and 
  documents current vs. desired state so you can fix what's broken.
time_investment: "20-30 minutes per process"
---

## Purpose

Audit process health, identify bottlenecks, and recommend improvements.

## Usage

- `/process-audit [process-name]` - Audit specific process

---

## Steps

1. **Define the process:**
   - What process are we reviewing?
   - What's the intended outcome?

2. **Gather feedback:**
   - Search meeting notes for mentions
   - Identify process participants
   - Common complaints or friction points

3. **Map current state:**
   - Current steps
   - Time spent per step
   - Handoffs and dependencies
   - Failure points

4. **Identify issues:**
   - Bottlenecks
   - Unnecessary steps
   - Missing automation
   - Communication gaps

5. **Recommend improvements:**
   - Quick wins
   - Longer-term fixes
   - Owner for changes

---

## Output Format

```markdown
# Process Audit: [Process Name]

**Date:** [Today]
**Participants:** [Roles involved]

## Current State
[How process works today]

## Issues Identified
1. [Bottleneck/Issue] - Impact: [Description]

## Recommendations
### Quick Wins
- [Improvement] - Impact: [Benefit]

### Longer-term
- [Improvement] - Requires: [Resources]

## Implementation Plan
- [ ] [Action 1] - Owner: [Name] - Due: [Date]
```
