---
name: strength-program
description: Design evidence-based powerlifting and hypertrophy training programs. Use for strength training programming, workout planning, and progressive overload systems.
---

# Strength Program Skill

Create comprehensive strength training programs integrating powerlifting and bodybuilding principles with systematic autoregulation and evidence-based loading parameters.

## Context

You are providing programming guidance for strength athletes using evidence-based training methodology. This targets experienced lifters seeking systematic approaches to concurrent strength and hypertrophy development.

## Program Philosophy

Combine powerlifting-style strength progression with bodybuilding hypertrophy principles to:
- Maximize strength in squat, bench press, deadlift
- Build muscle mass through strategic accessory work
- Maintain joint health and structural balance
- Develop autoregulation skills for sustainability

## Core Program Structure

### Opening Single System

```
RPE Target: 8
Function: Determines working weight for subsequent sets
Frequency: Every main lift session
Implementation: Build to RPE 8 single, calculate working weights from achieved load
```

### Working Set Parameters

**Strength Focus Sessions:**
- Sets: 4 working sets
- Intensity: Based on opening single (typically 85-92%)
- Final Set: AMRAP

**Hypertrophy Focus Sessions:**
- Sets: 5 working sets
- Intensity: Based on opening single
- Final Set: AMRAP for volume accumulation

### Accessory Protocol

```
Standard Parameters:
- Sets: 4 per movement
- Rep Range: 10-15 target
- Final Set: To muscular failure
- Rest Periods: Autoregulated based on performance quality
```

## Progressive Overload System

### Main Lift Progression

```python
# Opening Single Assessment
if RPE_single < 8.0:
    next_week_weight = current_weight + increment
elif RPE_single > 8.0:
    next_week_weight = current_weight - increment
else:
    # RPE exactly 8, assess working set performance
    if working_sets_performance > expected_reps:
        next_week_weight = current_weight + increment
    elif working_sets_performance < expected_reps:
        next_week_weight = current_weight - (increment * 0.5)
```

### Load Increment Guidelines

| Lift Category | Increment |
|---------------|-----------|
| Squat/Deadlift | 2.5-5kg (5-10lb) |
| Bench Press/OHP | 1.25-2.5kg (2.5-5lb) |
| Compound Accessories | 2.5kg (5lb) |
| Isolation Movements | 1.25kg (2.5lb) |

## Autoregulation Parameters

### Primary Performance Indicators

1. **RPE Accuracy on Opening Single**
   - Target: Consistent RPE 8 achievement
   - Deviation: >0.5 RPE indicates load adjustment needed

2. **Working Set Performance**
   - Metric: Total reps across working sets
   - Assessment: Compare to previous week

3. **AMRAP Set Achievement**
   - Function: Volume accumulation and strength endurance
   - Progression: Track reps at given intensities

### Secondary Indicators

- Movement quality and technique consistency
- Bar speed maintenance
- Sleep quality (7-point scale)
- Subjective energy levels (10-point scale)
- Recovery status from previous session

## Exercise Classification

### Primary Compounds (Competition Movements)
- Back Squat (high bar/low bar)
- Competition bench press / Pause bench
- Competition deadlift (conventional/sumo)

### Accessory Categories

**Hypertrophy-Focused:**
- Rep Range: 10-15
- Volume: 4 sets
- Selection: Muscle group and movement pattern specific

**Strength-Supporting:**
- Rep Range: 6-10
- Volume: 3-4 sets
- Selection: Address competition lift weak points

## Session Structure

```
Phase 1: Systematic Warm-up (5-10 minutes)
├── General warm-up
├── Movement-specific preparation
└── Progressive loading to opener

Phase 2: Opening Single Execution
├── Build systematically to RPE 8
├── Record achieved weight and RPE
└── Calculate working weights

Phase 3: Working Sets
├── Perform prescribed working sets
├── Rest periods: 3-5 minutes
└── Execute AMRAP final set

Phase 4: Accessory Work
├── Select complementary movements
├── Execute 4 sets in 10-15 rep range
└── Take final set to failure
```

## Progress Tracking

### Weekly Assessment Protocol

**Monday:** Review previous week
- Calculate average RPE accuracy
- Assess progression adherence
- Identify technique degradation

**Wednesday:** Mid-week check
- Monitor recovery status
- Adjust upcoming session if needed

**Friday:** Week completion
- Document all key metrics
- Plan next week adjustments
- Update training maxes

## Quality Standards

**Technical:**
- Competition-legal range of motion
- Consistent bar path and speed
- Proper breathing and bracing

**Performance:**
- Hit RPE targets within 0.5 point
- Complete all prescribed working sets
- Achieve minimum rep thresholds on accessories

## Implementation Notes

- Expect 4-6 weeks for RPE calibration accuracy
- Plan periodic technique assessments
- Schedule regular program evaluation cycles
- Adjust volume based on recovery capacity
- Modify exercise selection based on individual needs
