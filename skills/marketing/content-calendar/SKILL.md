---
name: content-calendar
description: Review upcoming content and identify gaps
role_groups: [marketing]
jtbd: |
  Your content pipeline is scattered across files and you're not sure if you have 
  gaps. This scans 05-Areas/Content/, checks alignment with campaigns and priorities, 
  identifies gaps in the pipeline, and suggests topics based on recent customer intel.
time_investment: "10-15 minutes per review"
---

## Purpose

Get a comprehensive view of your content pipeline - what's published, what's in progress, what's planned, and where the gaps are.

## Usage

- `/content-calendar` - Full content pipeline review
- `/content-calendar [timeframe]` - Focus on specific period (e.g., "this month", "Q1")

---

## Steps

1. **Scan 05-Areas/Content/** for content files
2. **Extract from each file:**
   - Content title/topic
   - Type (blog, video, whitepaper, case study, etc.)
   - Status (published, in progress, planned, idea)
   - Publish date (if specified)
   - Target audience
   - Campaign/goal alignment

3. **Check alignment:**
   - Read 01-Quarter_Goals/Quarter_Goals.md (if exists)
   - Read System/pillars.yaml
   - Verify content supports strategic priorities

4. **Identify gaps:**
   - Content types underrepresented
   - Audience segments not covered
   - Strategic pillars without content support
   - Weeks/months without scheduled content

5. **Generate calendar view with:**
   - Published content (last 30 days)
   - In-progress content
   - Planned content with dates
   - Gap analysis
   - Topic suggestions from recent customer intel

---

## Output Format

```markdown
# 📅 Content Calendar

**Period:** [Timeframe]
**Content pieces reviewed:** [Count]

## Published (Last 30 Days)
- [Date] - [Title] ([Type]) - [Audience]

## In Progress
- [Title] ([Type]) - Status: [%/stage] - Due: [Date]

## Planned
- [Week/Date] - [Title] ([Type]) - [Audience]

## Gaps Identified
1. [Gap description] - Suggested: [Content idea]
2. [Gap description] - Suggested: [Content idea]

## Topic Suggestions
Based on recent customer feedback:
- [Topic] - Why: [Customer pain point/request]
```

---

## Integration

- Reference `/customer-intel` for topic ideas
- Link to `/roadmap` for product launch content needs
