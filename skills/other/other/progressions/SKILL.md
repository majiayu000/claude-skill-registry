---
name: progressions
description: Kettlebell swing progression tracker with automatic advancement through reps, time, and weight phases. EMOM timer for session tracking. Use when building progressions, logging completed sessions, calculating next levels, or designing training progressions. Triggers include "progression", "kettlebell", "EMOM", "advancement", "progression level", "swing progression", "kettlebell advancement", "track progress", "log session", "next level", "progression phase", "auto-advance", "progression algorithm", "set progression", "timer", "reps progression", "time progression", "weight progression", "progression form", "progression tracking".
---

# Progressions Feature

Kettlebell swing progression tracker with automatic advancement through reps → time → weight.

## Progression Algorithm

1. **Start**: X kg, 10 reps, 10 min EMOM
2. **Each completed session**: +2 reps (until 20)
3. **At 20 reps**: +2 min per session (until 20 min)
4. **At 20 reps & 20 min**: next kettlebell, reset to 10 reps & 10 min
5. User confirms completion after each session

```
10 reps → 12 → 14 → 16 → 18 → 20 reps
                                  ↓
                     10 min → 12 → 14 → 16 → 18 → 20 min
                                                      ↓
                                            Next kettlebell
                                            Reset to 10/10
```

## Key Files

| File | Purpose |
|------|---------|
| `lib/progressionLogic.ts` | Pure functions: `calculateNextLevel`, `getCurrentLevel`, `getProgressionPhase` |
| `composables/useProgressions.ts` | List all progressions |
| `composables/useProgression.ts` | Single progression detail + session history |
| `composables/useProgressionForm.ts` | Create progression form state |
| `composables/useProgressionSession.ts` | Active EMOM session with timer |

## Database

**Tables**: `progressions`, `progressionSessions` (Dexie v5)

**Repository**: `getProgressionsRepository()` from `@/db`

## Usage

```ts
// List progressions
const { state, reload } = useProgressions()

// Single progression
const { progression, level, progress, sessions } = useProgression(id)

// Create form
const { name, selectedWeights, toggleWeight, save } = useProgressionForm()

// Active session
const { level, currentMinute, startTimer, completeSession } = useProgressionSession(id)
```

## Progression Logic API

```ts
import {
  calculateNextLevel,
  getCurrentLevel,
  getProgressionPhase
} from '@/features/progressions/lib/progressionLogic'

// Get current level from session history
const level = getCurrentLevel(sessions)
// { weight: 24, reps: 14, minutes: 10 }

// Calculate next level after completing session
const nextLevel = calculateNextLevel(currentLevel)
// { weight: 24, reps: 16, minutes: 10 }

// Get phase description
const phase = getProgressionPhase(level)
// 'reps' | 'time' | 'weight_reset'
```
