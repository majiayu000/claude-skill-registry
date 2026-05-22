---
name: js-worker-multithreading
description: Implement, refactor, or review worker-based multithreading in TypeScript/JavaScript apps (browser or Node). Use when offloading CPU-heavy loops to Web Workers, setting up a worker pool, moving data across threads, or diagnosing worker crashes, slowdowns, or synchronization bugs.
---

# JS Worker Multithreading

## Overview

Use this skill to move CPU-heavy work off the main thread with worker pools while keeping the main thread as the source of truth for UI, DOM, and physics APIs.

## Workflow

1. Identify the hot loop and define a pure worker kernel that takes plain data and returns plain data.
2. Snapshot state into typed arrays or plain objects suitable for structured clone or transfer.
3. Spawn a worker job, join for the result, and apply the result on the main thread.
4. Gate jobs to avoid overlapping work and apply the latest completed result on the next tick.
5. Add fallback behavior if workers or shared memory are not available.

## Do

- Keep worker code pure (numeric math, no DOM, no Three.js, no physics APIs).
- Use typed arrays for bulk data and pass them with a transfer or move helper.
- Preallocate and reuse buffers to avoid per-frame allocations and GC spikes.
- Limit concurrent jobs; keep at most one in flight per simulation loop or queue with backpressure.
- Apply results on the main thread and keep authoritative state there.
- Catch worker failures, log them, and degrade gracefully (main-thread fallback).
- Detect SharedArrayBuffer and crossOriginIsolated before relying on shared memory.
- Initialize the worker runtime once; handle "already initialized" errors safely.
- Size the pool based on hardwareConcurrency and clamp to a safe range.

## Do Not

- Do not call main-thread-only APIs (DOM, WebGL, Rapier, AudioContext) inside workers.
- Do not spawn a new worker per frame; reuse a pool or runtime.
- Do not pass class instances or engine objects across the worker boundary.
- Do not mutate shared state without explicit synchronization primitives.
- Do not launch overlapping jobs that race to apply results.
- Do not assume SharedArrayBuffer is available without COOP/COEP headers.
- Do not ignore failed worker results; disable or fallback to avoid infinite retries.

## Minimal Template (multithreading package)

```ts
import { initRuntime, move, spawn } from 'multithreading';

type Input = { count: number; positions: Float32Array };
type Output = { forces: Float32Array };

function simulateStep(input: Input): Output {
  // Pure math only.
  const forces = new Float32Array(input.count * 3);
  return { forces };
}

let runtimeReady = false;
let jobInFlight = false;
let pending: Output | null = null;

function ensureRuntime() {
  if (runtimeReady) return;
  initRuntime({ maxWorkers: 4 });
  runtimeReady = true;
}

async function tick(input: Input) {
  if (pending) {
    // Apply pending results on main thread here.
    pending = null;
  }
  if (jobInFlight) return;
  ensureRuntime();
  jobInFlight = true;
  const handle = spawn(move(input), simulateStep);
  const result = await handle.join();
  jobInFlight = false;
  if (result.ok) {
    pending = result.value;
  } else {
    // Log and fallback to main-thread compute if needed.
  }
}
```

## Troubleshooting Checklist

- Verify the worker kernel only uses serializable inputs and outputs.
- Confirm large arrays are transferred, not cloned.
- Ensure the main thread applies results in a deterministic order.
- Log worker failures and guard against repeated crashes.
- Validate crossOriginIsolated and SharedArrayBuffer before enabling shared memory.
