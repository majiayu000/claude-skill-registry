---
name: learning-session-planner
description: Design live class sessions, workshops, webinars, and synchronous learning experiences with timing, activities, breakouts, and facilitation guides. Use when planning live instruction. Activates on "class plan", "workshop design", "live session", or "webinar planning".
---

# Learning Session Planner

Plan engaging live learning sessions with optimal pacing, activities, and interaction.

## When to Use
- Live class planning
- Workshop design
- Webinar structure
- Synchronous online sessions
- In-person training events

## Session Design Elements
- Opening/icebreaker (5-10%)
- Content delivery (30-40%)
- Active learning activities (30-40%)
- Practice/application (15-25%)
- Closing/next steps (5%)

## Timing Guidance
- **60-min session**: 3-4 activities max
- **90-min session**: 4-5 activities, break at 45min
- **Half-day (3-4 hours)**: Break every 50-60min
- **Full-day**: Break every hour, lunch mid-day

## CLI Interface
```bash
/learning.session-planner --duration "90min" --topic "project management" --format "virtual"
/learning.session-planner --workshop --duration "4 hours" --participants "20"
```

## Output
- Minute-by-minute session plan
- Activity descriptions with timing
- Materials needed
- Facilitator notes
- Backup activities

## Composition
**Input from**: `/curriculum.develop-content`
**Output to**: Facilitator guides, live delivery

## Exit Codes
- **0**: Session plan created
- **1**: Invalid duration
- **2**: Insufficient content for time
