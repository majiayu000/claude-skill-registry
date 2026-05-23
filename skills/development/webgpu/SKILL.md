---
name: webgpu
description: Build WebGPU render and compute pipelines with portable best practices.
version: 0.1.0
license: MIT
tags: [webgpu, wgsl, gpu, shaders, compute, rendering, performance]
---

# WebGPU Skill

This skill helps any agent design, implement, and debug WebGPU applications and GPU compute pipelines. It is framework-agnostic and focuses on reusable WebGPU/WGSL patterns.

## What this skill covers

- WebGPU initialization, device setup, and surface configuration
- Compute pipelines, workgroup sizing, and storage buffer layout
- Render pipelines, render passes, and post-processing patterns
- GPU/CPU synchronization and safe readback strategies
- Performance and debugging practices
- Architecture patterns: modular passes, phase-based simulation, and capability handling
- Use cases: rendering, compute, ML training/inference, grid simulations, and systems modeling

## Core principles

- Choose a **capability strategy**: fallback runtime, reduced mode, or fail fast.
- Avoid full GPU readbacks in hot paths; use **localized queries** or small readback buffers.
- Structure simulation with **phases** (state, apply, integrate, constrain, correct) to keep WGSL cohesive.
- Use **spatial grids** or other spatial indexing for neighbor queries and high particle counts.
- Build **modular passes** so render and compute stages stay composable and testable.

## How to use this skill

When asked to build a WebGPU feature:

1. Confirm the target platform and WebGPU support expectations.
2. Propose a resource layout (buffers, textures, bind groups) with a simple data model.
3. Sketch the pipeline graph (compute vs render passes) and dependencies.
4. Provide minimal working code and scale up with performance constraints.
5. Choose a capability strategy when WebGPU is unavailable.

## Deliverable checklist

- Clean WebGPU init and error handling
- A buffer layout with alignment notes (16-byte struct alignment for WGSL)
- A pass graph with clear read/write ownership (ping-pong textures if needed)
- Explicit notes on readback and when it is safe
- Optional fallback or reduced mode for critical functionality

## Quick reference

See `REFERENCE.md` for a compact WebGPU cheat sheet and `docs/` for deeper patterns, including `docs/use-cases.md` and `docs/simulation-patterns.md`.

