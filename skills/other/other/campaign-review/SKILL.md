---
name: campaign-review
description: Post-mortem on recent campaign
role_groups: [marketing, leadership]
jtbd: |
  Campaigns finish and learnings get lost. This helps you run a post-mortem - gather 
  campaign materials, prompt for results and learnings, document what worked and 
  what didn't, and save to 06-Resources/Learnings/ so you compound knowledge over time.
time_investment: "20-30 minutes per campaign"
---

## Purpose

Capture learnings from completed campaigns so you compound marketing knowledge and make better decisions next time.

## Usage

- `/campaign-review [campaign-name]` - Review specific campaign

---

## Steps

1. **Gather campaign context:**
   - Search 05-Areas/Content/ for campaign files
   - Search 00-Inbox/Meetings/ for campaign discussions
   - Find campaign brief/plan

2. **Prompt user for:**
   - Campaign goals (awareness, leads, pipeline, etc.)
   - Target audience
   - Channels used
   - Budget spent
   - Timeline

3. **Collect results:**
   - Ask for metrics: impressions, clicks, leads, pipeline, revenue
   - Qualitative feedback received
   - Unexpected outcomes

4. **Document learnings:**
   - What worked well?
   - What didn't work?
   - What would you do differently?
   - Surprises or insights?

5. **Create post-mortem document** in 06-Resources/Learnings/Campaign_[Name]_[Date].md

---

## Output Format

```markdown
# Campaign Post-Mortem: [Campaign Name]

**Date:** [Today]
**Campaign period:** [Start] - [End]

## Overview
- **Goal:** [Primary objective]
- **Audience:** [Target]
- **Channels:** [List]
- **Budget:** $[Amount]

## Results
- **[Metric 1]:** [Result] (Goal: [Target])
- **[Metric 2]:** [Result] (Goal: [Target])

## What Worked
1. [Success 1]
2. [Success 2]

## What Didn't Work
1. [Challenge 1]
2. [Challenge 2]

## Key Learnings
1. [Learning 1]
2. [Learning 2]

## Recommendations for Next Time
1. [Recommendation 1]
2. [Recommendation 2]
```
