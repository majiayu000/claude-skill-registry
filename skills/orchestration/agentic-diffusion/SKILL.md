---
name: agentic-diffusion
description: |
  Semantic diffusion model for code. Turns generation into iterative denoising using four distinct roles (Orchestrator, Generator/Ralph, Critic, Refiner) to converge on working solutions through persistent refinement.
metadata: 
  {"clawdbot":{"emoji":"🌀","requires":{"skills":["filesystem"],"env":[]}}}
---

# Agentic Diffusion

A semantic diffusion model for code that replaces mathematical noise with **logic noise**. Instead of predicting the final code in one pass (zero-shot), this system iteratively **predicts what is wrong** and removes it.

## The Ralph Wiggum Loop

The architecture relies on **persistence rather than intelligence**. Like Ralph Wiggum's "I'm Helping!" enthusiasm, the system achieves correctness through eager iteration, not perfect prediction.

## Four Distinct Roles

| Role | Metaphor | Responsibility |
|------|----------|----------------|
| **Orchestrator** | The Adult | Manages the loop, tracks state, ensures persistence |
| **Generator (Ralph)** | "I'm Helping!" | Creates noisy initial drafts - eager, complete, messy |
| **Critic** | The Gradient | Identifies bugs and flaws WITHOUT writing code |
| **Refiner** | The Denoiser | Surgically removes specific bugs from current state |

## The Denoising Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 0: Orchestrator defines goal → File starts empty          │
│     ↓                                                           │
│  Step 1: Generator (Ralph) drafts initial noisy code            │
│     ↓                                                           │
│  Step 2: Critic identifies flaws → "Bug on line 45"             │
│     ↓                                                           │
│  Step 3: Refiner rewrites specific logic → Removes noise        │
│     ↓                                                           │
│  Step 4: Reality Check → Run code (Ground Truth)                │
│     ↓                                                           │
│  Step 5: Loop until Critic is silent AND tests pass             │
└─────────────────────────────────────────────────────────────────┘
```

## Usage

### Start a Diffusion Loop

```bash
diffusion start "<GOAL>" --output <FILE> --max-iterations N
```

**Example:**
```bash
diffusion start "Create a Snake game with keyboard controls and collision detection" --output snake.ts --max-iterations 20
```

### Using Sub-Agents

The Orchestrator spawns specialized sub-agents for each phase:

```typescript
// Generator Phase (Ralph)
sessions_spawn({
  task: "Generate initial code for: <GOAL>",
  label: "diffusion-generator",
  agentId: "ralph-generator"
})

// Critic Phase
sessions_spawn({
  task: "Critique this code for bugs (no fixes): <FILE>",
  label: "diffusion-critic", 
  agentId: "diffusion-critic"
})

// Refiner Phase
sessions_spawn({
  task: "Fix these specific issues: <ISSUES>",
  label: "diffusion-refiner",
  agentId: "diffusion-refiner"
})
```

### Check Status

```bash
diffusion status
```

### Stop the Loop

```bash
diffusion stop
```

## Why This Beats Zero-Shot

| Approach | Metaphor | Failure Mode |
|----------|----------|--------------|
| Zero-Shot | Drawing a map from memory | Hallucinations become permanent |
| Agentic Diffusion | Tracing and erasing mistakes | Reality Check catches hallucinations |

## State Management

State persists to `$CLAWD_WORKSPACE/.diffusion/state.json`:

```json
{
  "goal": "Create a Snake game",
  "output_path": "snake.ts",
  "iteration": 5,
  "max_iterations": 20,
  "phase": "critic",
  "history": [...]
}
```

## Sub-Agents Required

This skill requires the following sub-agents in `$CLAWD_WORKSPACE/subagents/`:

- `ralph-generator.md` - The eager code generator
- `diffusion-critic.md` - The bug finder
- `diffusion-refiner.md` - The surgical fixer

## Cost Warning

Autonomous loops consume tokens. Each iteration runs 3-4 sub-agents. A 20-iteration loop can run 60+ sub-agent invocations. Use `--max-iterations` wisely. (Or YOLO, if you're brave enough!)

## When to Use

- Complex coding tasks needing iteration
- User asks to "diffuse", "iterate until working", or "ralph loop"
- Code needs multiple refinement passes
- Building something from scratch that must work

## Orchestrator Instructions

When orchestrating a diffusion loop:

1. **Initialize state** - Set goal, output path, max iterations
2. **Spawn Generator** - Let Ralph create the initial noisy draft
3. **Spawn Critic** - Get structured feedback on issues
4. **Check convergence** - If no issues, verify and complete
5. **Spawn Refiner** - Fix identified issues surgically
6. **Loop** - Increment iteration, repeat from step 2
7. **Terminate** - When converged or max iterations reached

Always run verification (execute the code) before declaring convergence.
