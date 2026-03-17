---
name: workout-domain
description: Workout block model, types, and operations. Use when building workouts, managing block kinds (strength/AMRAP/EMOM/Tabata/ForTime/cardio), handling sets/reps, or working with workout persistence and benchmarks. Triggers: "workout", "block", "strength", "cardio", "AMRAP", "EMOM", "Tabata", "ForTime", "exercise", "set", "reps", "weight", "RIR", "timed block", "create workout", "build workout", "block kind", "discriminated union", "block result", "round", "interval", "benchmark", "template", "persist workout", "complete workout".
---

# Workout Domain

## Block-Based Workout Model

Workouts are sequences of **blocks** using discriminated unions via `kind`:

```ts
type WorkoutBlock = StrengthBlock | TimedBlock | CardioBlock

type TimedBlock = AmrapBlock | EmomBlock | TabataBlock | ForTimeBlock
```

### Strength Block

Traditional sets/reps exercises:

```ts
type StrengthBlock = {
  kind: 'strength'
  id: number
  exerciseName: string
  sets: Array<Set>
}

type Set = {
  id: number
  weight?: string    // User input as string
  reps?: string
  rir?: string       // Reps in reserve
  completed: boolean
}
```

### Timed Blocks

AMRAP, EMOM, Tabata, ForTime:

```ts
type AmrapBlock = {
  kind: 'amrap'
  id: number
  config: AmrapConfig
  exercises: Array<BlockExercise>
  result?: AmrapResult
}

type EmomBlock = {
  kind: 'emom'
  id: number
  config: EmomConfig
  exercises: Array<BlockExercise>
  result?: EmomResult
}

type TabataBlock = {
  kind: 'tabata'
  id: number
  config: TabataConfig
  exercises: Array<BlockExercise>
  result?: TabataResult
}

type ForTimeBlock = {
  kind: 'fortime'
  id: number
  config: ForTimeConfig
  exercises: Array<BlockExercise>
  result?: ForTimeResult
}
```

### Cardio Block

```ts
type CardioBlock = {
  kind: 'cardio'
  id: number
  exerciseName: string
  duration?: number
  distance?: number
  calories?: number
}
```

## Type Files

| File | Purpose |
|------|---------|
| `src/types/blocks.ts` | Runtime block types |
| `src/db/schema.ts` | Persistence types with `Db` prefix |

**Convention**: Database types use `Db` prefix (e.g., `DbStrengthBlock`) and `null` instead of `undefined`.

## Key Composables

### Workout Feature

| Composable | Purpose |
|------------|---------|
| `useWorkout.ts` | Singleton state, block/set CRUD operations |
| `useWorkoutPersistence.ts` | Auto-save, complete, discard active workout |
| `useWorkoutExercise.ts` | Exercise selection within workout |
| `useWorkoutBuilder.ts` | Build workout from scratch or template |

### Benchmark Feature

| Composable | Purpose |
|------------|---------|
| `useBenchmark.ts` | Core benchmark state and operations |
| `useBenchmarkPersistence.ts` | Save benchmark attempts |
| `useBenchmarkTimer.ts` | Timer for timed benchmarks |

### Template Feature

| Composable | Purpose |
|------------|---------|
| `useTemplateForm.ts` | Create/edit template form state |
| `useTemplatePicker.ts` | Select template to start workout |

## Working with Blocks

### Adding a Block

```ts
import { useWorkout } from '@/features/workout/composables/useWorkout'

const { addBlock } = useWorkout()

// Add strength block
addBlock({
  kind: 'strength',
  exerciseName: 'Squat',
  sets: []
})

// Add AMRAP block
addBlock({
  kind: 'amrap',
  config: { duration: 10 },
  exercises: []
})
```

### Type-Safe Block Handling

Use exhaustive switch for block kinds:

```ts
function getBlockTitle(block: WorkoutBlock): string {
  switch (block.kind) {
    case 'strength':
      return block.exerciseName
    case 'amrap':
      return `AMRAP ${block.config.duration}min`
    case 'emom':
      return `EMOM ${block.config.rounds}x${block.config.interval}s`
    case 'tabata':
      return 'Tabata'
    case 'fortime':
      return 'For Time'
    case 'cardio':
      return block.exerciseName
    default:
      // TypeScript exhaustiveness check
      const _exhaustive: never = block
      return _exhaustive
  }
}
```

## Quick Find

```bash
rg -n "kind: '(strength|amrap|emom|tabata|fortime|cardio)'" src/  # Block usage
rg -n "type.*Block = " src/types/blocks.ts                        # Block type definitions
rg -n "export function use" src/features/workout/composables      # Workout composables
```
