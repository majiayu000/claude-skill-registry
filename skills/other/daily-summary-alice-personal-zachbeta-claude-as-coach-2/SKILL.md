---
name: daily-summary-alice-personal
description: Alice's couch-to-5K personal extensions with running metrics and training data.
metadata:
  extends: daily-summary-base
---

# Daily Summary - Personal Extensions (Couch-to-5K Example)

**Extends:** daily-summary-base

This skill adds personal metrics and tracking for a couch-to-5K running training program.

## Context Tag Patterns

**Format examples:**
- `W4-D2` (Week 4, Day 2)
- `W5-RestDay` (Week 5, Rest Day)
- `W8-D3-5K` (Week 8, Day 3, first 5K!)

**Components:**
- Week: `W1`, `W2`, ..., `W8`
- Day: `D1`, `D2`, `D3`, or `RestDay`
- Milestone: `5K`, `Milestone`, etc.

## Key Metrics & Thresholds

Add these specific metrics to the Key Numbers table:

| Metric | Morning | Evening | Notes |
|--------|---------|---------|-------|
| **Running Distance** | - | [miles] | Target per plan |
| **Average Pace** | - | [min/mi] | Goal: <10:00/mi by Week 8 |
| **Heart Rate Zones** | - | [Z1/Z2/Z3 %] | Target: 80% Z2 aerobic |
| **Morning Weight** | [lbs] | - | Tracking trend |
| **Sleep Quality** | [hours] | - | Garmin score if available |
| **Nutrition** | [calories] | [calories] | Target: 2000-2300 cal |
| **Soreness Level** | [1-5] | [1-5] | 1=none, 5=severe |

**Running pace targets:**
- **Week 1-3:** Focus on completion, not pace
- **Week 4-5:** 11:00-12:00 min/mi comfortable
- **Week 6-7:** 10:30-11:00 min/mi
- **Week 8:** Sub-10:00 min/mi goal for 5K

**Heart rate zones (example for 35yo, 185 max HR):**
- **Z1 (Recovery):** 111-130 bpm (60-70% max)
- **Z2 (Aerobic):** 130-148 bpm (70-80% max) - PRIMARY TRAINING ZONE
- **Z3 (Tempo):** 148-167 bpm (80-90% max) - Occasional intervals

**Sleep targets:**
- **Training days:** 7-8 hours minimum
- **Recovery days:** 7-9 hours
- **<7 hours:** Consider rest day or easy workout

## Domain Terminology

**Training:**
- **C25K:** Couch-to-5K training program
- **Run/Walk:** Interval format (e.g., "Run 5min, Walk 1min, repeat 4x")
- **Rest Day:** Active recovery, no running
- **Long Run:** Longest continuous run of the week
- **Tempo:** Comfortably hard pace (Z3)

**Recovery:**
- **DOMS:** Delayed Onset Muscle Soreness (normal 24-48hrs post-run)
- **Taper:** Reduce volume before race/milestone
- **Active Recovery:** Light walk, yoga, stretching on rest days
- **Overtraining:** Persistent fatigue, elevated resting HR, poor sleep

**Nutrition:**
- **Pre-run:** Light carbs 1-2hrs before (banana, toast)
- **Post-run:** Protein + carbs within 30min (recovery window)
- **Hydration:** 8-10 glasses/day, more on run days
- **Deficit:** 300-500 cal/day for weight loss (if goal)

## Training Progress Tracking

Include in "What This Day Revealed" section:

**Training week structure (typical):**
- **Week 1-2:** Walk/run intervals, building base
- **Week 3-4:** Longer run intervals, reducing walk breaks
- **Week 5-6:** Extended continuous runs (20+ min)
- **Week 7-8:** Full 5K attempts, race prep

**Watch for patterns:**
- Soreness decreasing week-over-week (adaptation)
- Pace improving at same heart rate (fitness gains)
- Sleep quality impact on next-day performance
- Nutrition timing affecting energy levels

## Example Summary Snippet

```markdown
# Wednesday, November 20, 2025 - Daily Summary

**GROUND TRUTH:**
- Date: Wednesday, November 20, 2025
- W4-D2
- Training Day 23 of C25K program

---

## Key Numbers

| Metric | Morning | Evening | Notes |
|--------|---------|---------|-------|
| **Running Distance** | - | 3.2 mi | Week 4, Day 2: 8x (Run 5min, Walk 1min) |
| **Average Pace** | - | 10:45/mi | Improving! Sub-11:00 |
| **Heart Rate Zones** | - | Z2: 78% | Stayed aerobic, good |
| **Morning Weight** | 168 lbs | - | Down 1.5 lbs from Week 1 |
| **Sleep Quality** | 7.5 hrs | - | Garmin: 83/100 |
| **Nutrition** | 600 cal | 2100 cal | On target, good protein post-run |
| **Soreness Level** | 2/5 | 3/5 | Quads tight after run, normal DOMS |

---

## Timeline

**06:30** - Woke up, felt rested (7.5hrs sleep)
**06:45** - Pre-run: Banana + water
**07:15-08:00** - **Run workout:** W4D2 completed!
  - 8 intervals of Run 5min / Walk 1min
  - Total: 3.2 miles in 40min (includes warm-up/cool-down)
  - HR average: 142 bpm (Z2), max 156 bpm (low Z3)
  - Felt strong, legs responding well

**08:15** - Post-run: Protein shake + stretching
**12:30** - Lunch, noticed legs a bit tired but manageable
**18:00** - Light walk (15min active recovery)
**20:00** - Foam rolling, quads and calves
**22:30** - Bed

---

## What This Day Revealed

**Training progress:**
- Week 4 is noticeably easier than Week 2 was - adaptation working
- Maintaining Z2 heart rate even during run intervals (aerobic base improving)
- Pace naturally improving without pushing - went from 11:15/mi avg in W2 to 10:45/mi today
- 5-minute run intervals feel sustainable now (used to be a struggle at Week 3)

**Recovery insights:**
- Sleep quality directly correlates with run performance (7.5hrs = strong workout)
- Post-run protein shake within 30min seems to reduce next-day soreness
- Active recovery walk in evening helped legs feel less tight

**Nutrition:**
- Pre-run banana timing (90min before) worked well, no GI issues
- Total 2100 cal right on target for training day with slight deficit
- Staying hydrated throughout day made a difference
```

## Integration Notes

- Reference base framework for process and structure
- Add metrics table with specific values above
- Include domain terminology as needed (C25K, Z2, DOMS)
- Use context tag patterns for filename generation (W4-D2 style)
- Track week-over-week progress in insights section
- Note recovery patterns and nutrition timing
