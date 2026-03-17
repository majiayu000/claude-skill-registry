---
name: add-exercises
description: Add new exercises to the workout tracker database. Use when asked to add exercises, expand the exercise library, or check what exercises exist. Triggers include "add exercise", "new exercise", "exercise database", "what exercises", "missing exercises", "expand exercises".
---

# Adding Exercises to the Workout Tracker

## File Location

All exercises are defined in: `src/data/popularExercises.ts`

## File Structure

The file is organized by **MUSCLE GROUP → EQUIPMENT TYPE**, with exercises sorted alphabetically within each section:

```
CHEST
  ├── Barbell (1)
  ├── Dumbbell (1)
  ├── Cable (2)
  ├── Machine (5)
  └── Bodyweight (7)
BACK
  └── ...
```

The file header contains a summary showing counts for each muscle/equipment combination.

## Exercise Schema

```typescript
{
  name: string        // Unique name (duplicates throw runtime error)
  equipment: Equipment
  muscle: Muscle
  type: ExerciseType
  metrics: Metrics
}
```

### Valid Types

| Field | Valid Values |
|-------|-------------|
| `equipment` | `'barbell'`, `'dumbbell'`, `'machine'`, `'cable'`, `'bodyweight'`, `'kettlebell'`, `'band'`, `'ez-bar'`, `'hex-bar'`, `'club'`, `'battle-rope'` |
| `muscle` | `'chest'`, `'back'`, `'legs'`, `'shoulders'`, `'arms'`, `'core'` |
| `type` | `'compound'`, `'isolation'`, `'stability'`, `'cardio'`, `'isometric'` |
| `metrics` | `'weight-reps'`, `'reps-only'`, `'duration'`, `'distance-duration'`, `'weight-distance'` |

### Metrics Guidelines

| Equipment/Type | Typical Metrics |
|---------------|-----------------|
| Weighted exercises (barbell, dumbbell, machine, cable, kettlebell) | `'weight-reps'` |
| Bodyweight strength | `'reps-only'` |
| Holds/planks | `'duration'` |
| Cardio (running, rowing) | `'distance-duration'` |

### Type Guidelines

| Type | Description | Examples |
|------|-------------|----------|
| `compound` | Multi-joint movements | Squats, Deadlifts, Bench Press |
| `isolation` | Single-joint movements | Bicep Curls, Leg Extensions |
| `stability` | Dynamic balance/core exercises | Bird Dogs, Single-Leg Deadlift |
| `cardio` | High heart rate | Burpees, Jump Rope |
| `isometric` | Static holds under tension | Wall Sit, Dead Hang, L-Sit Hold |

## How to Add Exercises

### Step 1: Check What Exists

Read the file header summary to see current counts:
```
* - LEGS (71): barbell: 8, dumbbell: 9, kettlebell: 3, cable: 3, machine: 26, bodyweight: 22
```

Or search for specific exercises:
```bash
grep -i "squat" src/data/popularExercises.ts
```

### Step 2: Find the Right Section

Exercises are organized by muscle group, then equipment. Find the correct section:

```typescript
// ═══════════════════════════════════════════════════════════════════════════════
// LEGS
// ═══════════════════════════════════════════════════════════════════════════════

// --- Legs: Barbell (8) ---
{ name: 'Barbell Calf Raises', equipment: 'barbell', muscle: 'legs', type: 'isolation', metrics: 'weight-reps' },
```

### Step 3: Add in Alphabetical Order

Insert the new exercise in the correct alphabetical position within its section:

```typescript
// --- Legs: Barbell (8) ---   ← Update count to (9)
{ name: 'Barbell Calf Raises', equipment: 'barbell', muscle: 'legs', type: 'isolation', metrics: 'weight-reps' },
{ name: 'Barbell Good Mornings', equipment: 'barbell', muscle: 'legs', type: 'compound', metrics: 'weight-reps' },
{ name: 'Barbell Hack Squat', equipment: 'barbell', muscle: 'legs', type: 'compound', metrics: 'weight-reps' },  ← NEW
{ name: 'Barbell Hip Thrust', equipment: 'barbell', muscle: 'legs', type: 'compound', metrics: 'weight-reps' },
```

### Step 4: Update Counts

1. Update the section comment count: `// --- Legs: Barbell (8) ---` → `(9)`
2. Update the file header summary

### Step 5: Verify

Run type-check to ensure no duplicates or type errors:
```bash
pnpm type-check
```

The file has runtime duplicate detection - if you add a duplicate name, it will throw an error immediately.

## Common Mistakes to Avoid

1. **Duplicate names**: Every exercise name must be unique across ALL muscles/equipment
2. **Wrong section**: Always add to the correct muscle AND equipment section
3. **Not alphabetical**: Keep exercises sorted A-Z within each section
4. **Forgetting counts**: Update both the section count and header summary
5. **Wrong metrics**: Use `'weight-reps'` for weighted, `'reps-only'` for bodyweight

## Example: Adding Multiple Exercises

When adding multiple exercises at once:

1. Group them by muscle → equipment
2. Add each to its correct section alphabetically
3. Update all affected counts
4. Run `pnpm type-check` once at the end
