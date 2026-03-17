---
name: daily-morning-routine-alice-personal
description: Alice's couch-to-5K morning routine with training context and recovery protocols.
metadata:
  extends: daily-morning-routine-base
---

# Daily Morning Routine - Personal Extensions (Couch-to-5K Example)

**Extends:** daily-morning-routine-base

This skill adds personal protocols for couch-to-5K training, including recovery metrics, training plan context, and run-day readiness assessment.

## Sleep Data Integration

When generating morning brief, include sleep data if available (from Garmin or user report):

```markdown
## Sleep & Recovery
- **Sleep Duration:** [X] hours (Target: 7-8 hrs on training days)
- **Sleep Quality:** [Garmin score if available]
- **Resting Heart Rate:** [bpm] (Track for overtraining - elevated RHR = potential issue)
- **Assessment:** [Well-rested / Under-rested / Overtrained signals]
```

**Interpretation guidance:**
- **7-8 hrs sleep:** Optimal for training days, expect good performance
- **<7 hrs:** Sub-optimal recovery, consider easier workout or rest
- **>8 hrs:** Excellent recovery, body is adapting well
- **RHR elevated 5+ bpm:** Possible overtraining or illness, consider rest day

## Training Plan Status

**Include current week and day in morning brief:**

```markdown
## Training Status
- **Current:** Week 4, Day 2 (W4-D2)
- **Today's Workout:** Run 5min / Walk 1min, repeat 8x
- **This Week's Progress:** 2 of 3 workouts complete
- **Next Milestone:** Week 5 - first 20min continuous run
```

**C25K typical week structure:**
- **Week 1-2:** Short run/walk intervals, building baseline
- **Week 3-4:** Longer runs, fewer walk breaks
- **Week 5-6:** Extended continuous runs (20+ minutes)
- **Week 7-8:** Full 3-mile runs, race prep

## Recovery Metrics & Run Readiness

**Include in morning brief when relevant:**

```markdown
## Recovery Assessment
- **Soreness:** [None / Light / Moderate / Significant]
  - Locations: [Quads / Calves / Shins / Other]
- **Energy Level:** [Low / Moderate / High]
- **Motivation:** [Reluctant / Neutral / Eager]
- **Yesterday's Run:** [Rest day / Easy / Hard]
- **Run Readiness:** [Ready / Marginal / Not ready - rest day recommended]
```

**Decision tree for run readiness:**
1. **Ready to run:** Well-rested (7+ hrs), low-moderate soreness, normal RHR
2. **Marginal:** Under-rested OR moderate soreness OR slightly elevated RHR
   - Consider: Easier/shorter workout, or swap rest day
3. **Not ready:** Poor sleep AND high soreness AND elevated RHR
   - Recommendation: Take rest day, allow recovery

## Nutrition & Hydration Plan

**Include today's nutrition targets:**

```markdown
## Today's Nutrition Plan
- **Run Day:** Yes - 2000-2300 calories
  - Pre-run (90min before): Light carbs (banana, toast)
  - Post-run (within 30min): Protein + carbs (shake, eggs + toast)
  - Hydration: 10+ glasses, extra 16oz post-run
- **Rest Day:** 1800-2000 calories
  - Focus: Protein for recovery
  - Hydration: 8-10 glasses
```

## Run Day Protocols

**Run day vs. rest day decision:**

**Run Day (3x per week):**
- Pre-run fuel: Banana or toast with PB, 90min before
- Warm-up: 5min walk before run intervals
- Cool-down: 5min walk after run intervals
- Post-run: Protein within 30min, stretch major muscle groups
- Afternoon: Light activity okay, foam roll if needed

**Rest Day (4x per week):**
- Active recovery encouraged: Walk 15-30min, yoga, stretching
- NO running - allow muscle repair and adaptation
- Focus on sleep and nutrition
- Foam rolling and mobility work

**Listen to body signals:**
- Sharp pain → stop immediately, assess injury
- Normal muscle fatigue → expected, continue
- Excessive breathlessness → slow pace, stay aerobic
- Nausea / dizziness → stop, hydrate, check nutrition timing

## Morning State Assessment

**Enhanced recognition for training context:**

**Post-Run Day (DOMS Expected):**
- Muscle soreness 24-48hrs after run = normal
- Light/moderate soreness = good adaptation signal
- Severe soreness = possible overtraining, consider extra rest
- No soreness by Week 4+ = body adapting well

**Pre-Run Day (Readiness Check):**
- Eager and energized → great, enjoy the run
- Reluctant but not sore → mental resistance, usually goes away after warm-up
- Reluctant + sore + tired → body needs rest, don't force it

**Overtraining Signals:**
- Persistent fatigue despite rest
- Elevated resting heart rate (5+ bpm above baseline)
- Poor sleep quality consistently
- Declining performance (slower pace at same effort)
- Loss of motivation lasting multiple days
- **Action:** Take extra rest day, reduce volume for 3-5 days

## Example Morning Brief Snippet

```markdown
## Ground Truth
Today is Thursday, November 21, 2025
W4-D3 (Week 4, Day 3 - Training Day)

---

## Sleep & Recovery
- **Sleep Duration:** 7.2 hours (Target: 7-8 hrs)
- **Garmin Sleep Score:** 81/100 (Good)
- **Resting Heart Rate:** 58 bpm (baseline 56-58, normal)
- **Assessment:** Well-rested, ready for training

---

## Training Status
- **Current:** Week 4, Day 3 (W4-D3)
- **Today's Workout:** Run 5min / Walk 1min, repeat 8x (same as W4-D2)
- **This Week's Progress:** 2 of 3 workouts complete
- **Next Milestone:** Week 5 starts Monday - first 20min continuous run

---

## Recovery Assessment
- **Soreness:** Light (2/5) - quads slightly tight from yesterday
- **Locations:** Quads primarily, calves minor
- **Energy Level:** High - feel rested and ready
- **Motivation:** Eager - excited to repeat yesterday's strong performance
- **Yesterday's Run:** W4-D2 completed, 3.2mi @ 10:45/mi pace
- **Run Readiness:** ✓ Ready - all signals green

---

## Yesterday's Snapshot
- Completed W4-D2: 8x (Run 5min, Walk 1min) = 3.2 miles
- Pace: 10:45/mi average (improving, was 11:15 in Week 2)
- HR: Stayed in Z2 (78% time in aerobic zone)
- Post-run recovery: Protein shake + stretching
- Evening: Light walk, foam rolling
- Nutrition: 2100 cal, hit targets
- Soreness: Developed expected DOMS, manageable

## Today's Nutrition Plan
- **Run Day:** 2000-2300 calories target
  - 06:45 Pre-run: Banana + water (90min before run)
  - 08:15 Post-run: Protein shake + eggs/toast (within 30min)
  - Throughout day: 10+ glasses water, extra 16oz post-run
  - Focus: Protein for recovery, moderate carbs for energy

## Today's Focus
- Repeat W4-D2 workout: 8x (Run 5min / Walk 1min)
- Goal: Match or improve yesterday's 10:45 pace while staying Z2
- Watch: Quad soreness - if increases during run, back off pace
- Pre-run: Banana at 06:45, run at 08:15
- Post-run: Immediate protein, stretching, hydration
- Track: Pace, HR zones, how quads respond to back-to-back runs
```

## Integration Notes

- Reference base framework for core morning routine process
- Add sleep data, training status, and recovery assessment as above
- Adapt brief length to morning state (tired = shorter, energized = can handle detail)
- Run readiness check is key decision point - override plan if not ready
- Nutrition timing particularly important on run days
- DOMS is expected and normal - distinguish from injury pain
- Training plan provides structure, but listen to body signals
