Y---
name: Time System & Loop Mechanics
description: Understanding the game's timekeeping, day/night cycle, hourly events, and time loop mechanics. Use when working with time-based features, scheduling, or loop system.
---

# Time System & Loop Mechanics

## Overview
Babylon FP features a sophisticated time system where NPCs follow schedules, events occur at specific times, and the day/night cycle creates atmosphere. The game potentially includes time loop mechanics for gameplay.

## Core Time Systems

### 1. Day/Night Cycle (`src/systems/dayNightCycle.ts`)
**Purpose**: Visual time progression with realistic lighting

**Key Features**:
- 24-hour cycle with realistic sun/moon movement
- Dynamic sky color transitions (dawn, day, dusk, night)
- Directional light intensity changes
- Ambient light adjustments
- Pausable time progression

**Time Calculation**:
```typescript
// Time flows from 0.0 (midnight) to 1.0 (next midnight)
// Example: 0.5 = noon, 0.75 = 6 PM
currentTime: number (0.0 - 1.0)
timeOfDay: seconds since midnight
```

**Pause Support**:
- Tracks `pausedTimestamp` and `accumulatedPauseTime`
- Resumes from correct position after pause
- Integrated with game pause system (P key)

**Visual Elements**:
```typescript
- Sun position: arc from east to west
- Sky colors: gradient based on time of day
- Light intensity: peaks at noon, dims at night
- Ambient light: provides base illumination
```

### 2. Hourly Cycle System (`src/systems/hourlyCycle.ts`)
**Purpose**: Triggers events at specific in-game hours

**Functionality**:
- Monitors current game hour
- Fires events when hour changes
- Can trigger investigations, crimes, NPC behaviors
- Integrates with TimeSync for accurate timing

**Example Use Cases**:
```typescript
// Crime occurs at 3 AM
if (currentHour === 3) {
  triggerCrimeEvent("bread_theft");
}

// Market opens at 8 AM
if (currentHour === 8) {
  spawnMarketNPCs();
}
```

### 3. Time Synchronization (`src/systems/timeSync.ts`)
**Purpose**: Central time management and synchronization

**Responsibilities**:
- Maintains single source of truth for game time
- Synchronizes all time-dependent systems
- Handles time flow rate (speed up/slow down)
- Manages time loop resets

**Key Methods**:
```typescript
getCurrentTime(): number  // Get current game time
setTimeMultiplier(speed: number)  // Adjust time flow
resetTime()  // Reset to start (time loop)
```

### 4. Loop Manager (`src/systems/loopManager.ts`)
**Purpose**: Game loop orchestration and update cycles

**Functions**:
- Coordinates render loop with Babylon.js
- Updates all systems each frame
- Handles delta time calculations
- Manages system priorities and update order
- Can be paused/resumed (integrated with pause system)

**Update Order**:
```
1. Time systems (timeSync, dayNightCycle)
2. NPC system (movement, schedules)
3. Event system (crimes, investigations)
4. Physics/collision
5. UI updates
6. Rendering
```

## NPC Scheduling System

### Schedule Format
NPCs follow time-based schedules defined in JSON:

```json
{
  "schedule": {
    "21600": { "x": 10, "y": 0, "z": 5 },   // 6:00 AM (6*60*60)
    "28800": { "x": 15, "y": 0, "z": 10 },  // 8:00 AM
    "43200": { "x": 20, "y": 0, "z": 15 }   // 12:00 PM
  }
}
```

**Time Keys**: Seconds since midnight (0-86400)

### NPC Movement (`src/systems/npcSystem.ts`)
**Behavior**:
- NPCs interpolate between waypoints
- Movement speed adjustable
- Pathfinding around obstacles
- Face direction of travel
- Return to start position at day end

**Schedule Interpolation**:
```typescript
// Smooth movement between waypoints
currentPosition = lerp(previousWaypoint, nextWaypoint, t)
```

## Time Loop Mechanics (Planned/Conceptual)

### Core Concept
Player experiences the same day repeatedly to solve crimes/mysteries:
1. Day starts at 6:00 AM
2. Crime occurs at specific time
3. Player gathers evidence via photography
4. Day ends or resets
5. Player retains knowledge/photos across loops

### Loop States
```typescript
enum LoopState {
  FirstTime,      // Initial playthrough
  Repeating,      // Subsequent loops
  Resolved        // After solving the mystery
}
```

### Persistent Data Across Loops
```typescript
- Photos taken (evidence)
- NPC dialogue trees (what you learned)
- Player knowledge (journal entries)
- Investigation progress
```

### Reset Mechanics
```typescript
// What resets:
- NPC positions → back to 6 AM locations
- World state → crimes haven't occurred yet
- Time → 6:00 AM

// What persists:
- Player inventory (photos, notes)
- Unlocked dialogue options
- Investigation clues discovered
```

## Time-Based Features

### Photo System Timestamps
Photos capture exact game time for evidence:
```typescript
{
  timestamp: "08:35",      // HH:MM format
  location: {x, y, z},
  npcVisible: ["baker", "guard"],
  timeOfDay: "morning"
}
```

### Event Timing
Crimes/events scheduled by time:
```json
{
  "triggerTime": "03:00",  // 3 AM
  "type": "crime",
  "location": "bakery"
}
```

## Development Commands

### Check time system
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
grep -rn "class.*Cycle\|class.*Time" src/systems/ --include="*.ts"
```

### View time-related files
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
ls -lh src/systems/{dayNightCycle,hourlyCycle,timeSync,loopManager}.ts
```

### Test time calculations
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
# Run time-sync tests
npm test -- timeSync.test.ts
```

## Integration Points

### With Pause System
```typescript
// Game.ts
pause() {
  this.dayNightCycle.pause();
  this.loopManager.stop();
}

resume() {
  this.dayNightCycle.resume();
  this.loopManager.start();
}
```

### With NPC System
```typescript
// NPCs check current time for schedule
const currentTimeSeconds = timeSync.getCurrentTime() * 86400;
const nextWaypoint = findWaypointForTime(currentTimeSeconds);
```

### With Photo System
```typescript
// Photos stamped with current game time
const photo = {
  time: formatTime(timeSync.getCurrentTime()),
  // ... other photo data
};
```

## Time Utilities

### Format Functions
```typescript
// Convert 0.0-1.0 to HH:MM
formatTime(time: number): string

// Convert seconds to readable time
secondsToTime(seconds: number): string

// Get current hour (0-23)
getCurrentHour(): number

// Calculate time between two points
getTimeDelta(start: number, end: number): number
```

## Performance Considerations

- Time updates are delta-time based (frame-independent)
- Expensive calculations cached per hour
- NPC schedules pre-processed on load
- Sky color transitions use lerp for smoothness
- Update frequency: Every frame for smooth visuals

## Related Files
```
src/systems/dayNightCycle.ts    - Visual day/night
src/systems/hourlyCycle.ts      - Hourly event triggers
src/systems/timeSync.ts         - Central time management
src/systems/loopManager.ts      - Game loop orchestration
src/systems/npcSystem.ts        - NPC scheduling
src/systems/photoSystem.ts      - Time-stamped photos
src/Game.ts                     - Pause integration
```

## Future Enhancements
- [ ] Time skip functionality (fast-forward to next event)
- [ ] Multiple time speeds (1x, 2x, 4x)
- [ ] Time rewind for review
- [ ] Save/load time state
- [ ] Time-of-day weather effects
- [ ] Schedule conflict detection
