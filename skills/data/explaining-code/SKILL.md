---
name: explaining-code
description: Explains code with visual diagrams and analogies to help users understand how code works.
---

# Explaining Code Skill

## When to Use

- User asks how a function/component works
- User wants to understand architectural patterns
- User needs help learning a codebase
- User asks "how does this work?"

## What This Skill Does

1. Analyzes the code to explain
2. Creates analogies for complex concepts
3. Generates visual diagrams (ASCII/text)
4. Provides step-by-step explanations
5. Links to related code patterns

## Explanation Patterns

### 1. Function Explanation

```
Function: calculateNormalizedPower

Purpose: Calculates normalized power using 30-second rolling average

Input: Array of power readings (watts), sample rate (Hz)
Output: Normalized power (watts)

Algorithm:
1. Calculate 30-second rolling average of power
2. Raise each value to the 4th power
3. Average these values
4. Take 4th root

Analogy: It's like finding the "metabolic cost" of a ride,
accounting for how hard you actually worked, not just average speed.
```

### 2. Component Flow

```
Component: ActivityRecorderService

State Machine:
  pending -> ready -> recording -> paused -> finished

Flow:
1. User navigates to /record screen
2. Service created, transitions to 'ready'
3. User taps start, transitions to 'recording'
4. Service captures GPS/HR/power data
5. User pauses, transitions to 'paused'
6. User resumes, transitions back to 'recording'
7. User finishes, transitions to 'finished'
8. Service cleans up when leaving screen
```

### 3. Data Flow

```
Data Flow: Activity Recording -> Sync

1. Record Locally
   └─ SQLite stores JSON activity
       { id, name, type, distance, duration, ... }

2. Upload to Cloud
   └─ JSON uploaded to Supabase Storage
   └─ Source of truth: Storage bucket

3. Create Metadata
   └─ Activity record created in database
   └─ References Storage URL

4. Generate Streams
   └─ Time-series data compressed and embedded
   └─ Stored in activities.metrics.streams

5. Calculate Analytics
   └─ @repo/core processes metrics
   └─ TSS, IF, power zones calculated
```

### 4. Pattern Explanation

```
Pattern: Event-Driven Hooks

Instead of: Subscribing to all service data
Use: Specific hooks for specific data

Bad:
const data = useEffect(() => {
  service.on('update', () => setData(service.getAllData()));
}, []);

Good:
const state = useRecordingState(service);
const readings = useCurrentReadings(service);
const stats = useSessionStats(service);

Benefits:
- Surgical re-renders (only what changes)
- No over-subscription
- Better performance
```

## Visual Examples

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Mobile App                         │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────────────────────┐ │
│  │ Recording   │───>│ ActivityRecorderService     │ │
│  │ Screen      │    │ - GPS tracking              │ │
│  └─────────────┘    │ - Sensor data               │ │
│                     │ - State management           │ │
│                     └─────────────────────────────┘ │
│                              │                       │
│                              ▼                       │
│                     ┌─────────────┐                 │
│                     │   SQLite    │                 │
│                     │ (local)     │                 │
│                     └─────────────┘                 │
│                              │                       │
│                    (when online)                     │
│                              ▼                       │
│                     ┌─────────────┐                 │
│                     │ Supabase    │                 │
│                     │ Storage     │                 │
│                     └─────────────┘                 │
└─────────────────────────────────────────────────────┘
```

## Best Practices

1. Start with purpose/what it does
2. Use analogies for complex concepts
3. Show step-by-step flow
4. Provide visual diagrams
5. Link to actual code
6. Explain why, not just what
7. Cover edge cases
