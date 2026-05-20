---
name: planning-workflow
description: "Jeffrey Emanuel's comprehensive markdown planning methodology for software projects. The 85%+ time-on-planning approach that makes agentic coding work at scale. Includes exact prompts used."
---

# Planning Workflow — The Foundation of Agentic Development

> **Core Philosophy:** "Planning tokens are a lot fewer and cheaper than implementation tokens."
>
> The models are far smarter when reasoning about a detailed plan that fits within their context window. This is the key insight behind spending 80%+ of time on planning.

---

## Why Planning Matters

Before burning tokens with a big agent swarm:

- **Measure twice, cut once** — becomes "Check your plan N times, implement once"
- A very big, complex markdown plan is still shorter than a few substantive code files
- Front-loading human input in planning enables removing yourself from implementation
- The code will be written ridiculously quickly when you start enough agents with a solid plan

---

## The Planning Process (Overview)

```
┌──────────────────────────────────────────────────────────────┐
│  1. INITIAL PLAN (GPT Pro / Opus 4.5 in web app)             │
│     └─► Explain goals, intent, workflows, tech stack         │
├──────────────────────────────────────────────────────────────┤
│  2. ITERATIVE REFINEMENT (GPT Pro Extended Reasoning)        │
│     └─► 4-5 rounds of revision until steady-state            │
├──────────────────────────────────────────────────────────────┤
│  3. MULTI-MODEL BLENDING (Optional but recommended)          │
│     └─► Gemini3 Deep Think, Grok4 Heavy, Opus 4.5           │
│     └─► GPT Pro as final arbiter                             │
├──────────────────────────────────────────────────────────────┤
│  4. CONVERT TO BEADS (Claude Code + Opus 4.5)                │
│     └─► Self-contained tasks with dependency structure       │
├──────────────────────────────────────────────────────────────┤
│  5. POLISH BEADS (6+ rounds until steady-state)              │
│     └─► Cross-model review, never oversimplify               │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Creating the Initial Plan

### Where to Write It

Use **GPT Pro with Extended Reasoning** in the web app. No other model can touch Pro on the web when dealing with input that fits its context window.

**Alternative:** Claude Opus 4.5 in the webapp is also good for initial plans.

### What to Include

1. **Goals and Intent** — What you're really trying to accomplish
2. **Workflows** — How the final software should work from the user's perspective
3. **Tech Stack** — Be specific (e.g., "TypeScript, Next.js 16, React 19, Tailwind, Supabase")
4. **Architecture Decisions** — High-level structure and patterns
5. **The "Why"** — The more the model understands your end goal, the better it performs

You don't even need to write the initial markdown plan yourself. You can write that with GPT Pro, just explaining what it is you want to make.

---

## Phase 2: Iterative Refinement

### THE EXACT PROMPT — Plan Review (GPT Pro Extended Reasoning)

Paste your entire markdown plan into GPT Pro with Extended Reasoning enabled and use this EXACT prompt:

```
Carefully review this entire plan for me and come up with your best revisions in terms of better architecture, new features, changed features, etc. to make it better, more robust/reliable, more performant, more compelling/useful, etc. For each proposed change, give me your detailed analysis and rationale/justification for why it would make the project better along with the git-diff style change versus the original plan shown below:

<PASTE YOUR EXISTING COMPLETE PLAN HERE>
```

### THE EXACT PROMPT — Integration (Claude Code)

After GPT Pro finishes (may take 20-30 minutes for complex plans), paste the output into Claude Code with this EXACT prompt:

```
OK, now integrate these revisions to the markdown plan in-place; use ultrathink and be meticulous. At the end, you can tell me which changes you wholeheartedly agree with, which you somewhat agree with, and which you disagree with:

```[Pasted text from GPT Pro]```
```

### Repeat Until Steady-State

- Start fresh ChatGPT conversations for each round
- After 4-5 rounds, suggestions become very incremental
- You'll see massive improvements from v2 to v3, continuing to the end
- This phase can take 2-3 hours for complex features — this is normal

---

## Phase 3: Multi-Model Blending (Advanced)

### Why Blend Models

Different models have different strengths. Blending gets "best of all worlds."

### The Process

1. Get competing plans from Gemini3 (Deep Think), Grok4 Heavy, and Opus 4.5
2. Use GPT Pro as final arbiter

### THE EXACT PROMPT — Multi-Model Blend

```
I asked 3 competing LLMs to do the exact same thing and they came up with pretty different plans which you can read below. I want you to REALLY carefully analyze their plans with an open mind and be intellectually honest about what they did that's better than your plan. Then I want you to come up with the best possible revisions to your plan (you should simply update your existing document for your original plan with the revisions) that artfully and skillfully blends the "best of all worlds" to create a true, ultimate, superior hybrid version of the plan that best achieves our stated goals and will work the best in real-world practice to solve the problems we are facing and our overarching goals while ensuring the extreme success of the enterprise as best as possible; you should provide me with a complete series of git-diff style changes to your original plan to turn it into the new, enhanced, much longer and detailed plan that integrates the best of all the plans with every good idea included (you don't need to mention which ideas came from which models in the final revised enhanced plan):

[Paste competing plans here]
```

---

## Real-World Examples

### Example Plan Documents

| Project | Plan Link |
|---------|-----------|
| CASS Memory System | [PLAN_FOR_CASS_MEMORY_SYSTEM.md](https://github.com/Dicklesworthstone/cass_memory_system/blob/main/PLAN_FOR_CASS_MEMORY_SYSTEM.md) |
| CASS GitHub Pages Export | [PLAN_TO_CREATE_GH_PAGES_WEB_EXPORT_APP.md](https://github.com/Dicklesworthstone/coding_agent_session_search/blob/main/PLAN_TO_CREATE_GH_PAGES_WEB_EXPORT_APP.md) |

### Example AGENTS.md Files

| Project Type | Link |
|--------------|------|
| NextJS webapp + TypeScript CLI | [brenner_bot/AGENTS.md](https://github.com/Dicklesworthstone/brenner_bot/blob/main/AGENTS.md) |
| Bash script project | [repo_updater/AGENTS.md](https://github.com/Dicklesworthstone/repo_updater/blob/main/AGENTS.md) |

---

## What Makes a Great Plan

### Good vs. Great

| Good Plan | Great Plan |
|-----------|------------|
| Describes what to build | Explains WHY you're building it |
| Lists features | Details user workflows and interactions |
| Mentions tech stack | Justifies tech choices with tradeoffs |
| Has tasks | Has tasks with dependencies and rationale |
| ~500 lines | ~3,500+ lines after refinement |

### Essential Elements

1. **Self-contained** — Never need to refer back to external docs
2. **Granular** — Break complex features into specific subtasks
3. **Dependency-aware** — What blocks what?
4. **Justified** — Include reasoning, not just instructions
5. **User-focused** — How does each piece serve the end user?

---

## Common Mistakes

1. **Starting implementation too early** — 3 hours of planning saves 30 hours of rework
2. **Single-round review** — You continue to get improvements even at round 6+
3. **Not using GPT Pro** — Extended Reasoning is uniquely good for this
4. **Skeleton-first coding** — One big comprehensive plan beats incremental coding
5. **Losing context** — Convert plans to beads so agents don't need the original

---

## FAQ

**Q: Shouldn't I code a skeleton first?**
A: You get a better result faster by creating one big comprehensive, detailed, granular plan. That's the only way to get models to understand the entire system at once. Once you start turning it into code, it gets too big to understand.

**Q: What about problems I didn't anticipate?**
A: Finding the flaws and fixing them is the whole point of all the iterations and blending in feedback from all the frontier models. If you follow the procedure using those specific models and prompts, after enough rounds, you will have an extremely good plan that will "just work." After implementing v1, you create another plan for v2. Nothing says you can only do one plan.

**Q: How do I divide tasks for agents?**
A: Each agent uses bv to find the next optimal bead and marks it in-progress. Distributed, robust, fungible agents.

**Q: Do agents need specialization?**
A: No. Every agent is fungible and a generalist. They all use the same base model and read the same AGENTS.md. Simply telling one it's a "frontend agent" doesn't make it better at frontend.

**Q: Which tech stack should I use?**
A: This is part of the "pre-planning" phase. Usually I already know based on project type:
- **Web app:** TypeScript, Next.js 16, React 19, Tailwind, Supabase (performance-critical parts in Rust compiled to WASM)
- **CLI tool:** Golang or Rust if very performance critical
- If unsure, do a deep research round with GPT Pro or Gemini3 to study libraries and get suggestions.

**Q: Should design decisions be in markdown or beads?**
A: The beads themselves can and should contain this markdown. You can have long descriptions/comments inside the beads—they don't need to be short bullet point type entries.

---

## Best Practices Guides

Keep best practices guides in your project folder and reference them in AGENTS.md:

- [claude_code_agent_farm/best_practices_guides](https://github.com/Dicklesworthstone/claude_code_agent_farm/tree/main/best_practices_guides)

Have Claude Code search the web and update them to latest versions.

---

## Complete Prompt Reference

### GPT Pro — Plan Review
```
Carefully review this entire plan for me and come up with your best revisions in terms of better architecture, new features, changed features, etc. to make it better, more robust/reliable, more performant, more compelling/useful, etc. For each proposed change, give me your detailed analysis and rationale/justification for why it would make the project better along with the git-diff style change versus the original plan shown below:

<PASTE YOUR EXISTING COMPLETE PLAN HERE>
```

### Claude Code — Integrate Revisions
```
OK, now integrate these revisions to the markdown plan in-place; use ultrathink and be meticulous. At the end, you can tell me which changes you wholeheartedly agree with, which you somewhat agree with, and which you disagree with:

```[Pasted text from GPT Pro]```
```

### GPT Pro — Multi-Model Blend
```
I asked 3 competing LLMs to do the exact same thing and they came up with pretty different plans which you can read below. I want you to REALLY carefully analyze their plans with an open mind and be intellectually honest about what they did that's better than your plan. Then I want you to come up with the best possible revisions to your plan (you should simply update your existing document for your original plan with the revisions) that artfully and skillfully blends the "best of all worlds" to create a true, ultimate, superior hybrid version of the plan that best achieves our stated goals and will work the best in real-world practice to solve the problems we are facing and our overarching goals while ensuring the extreme success of the enterprise as best as possible; you should provide me with a complete series of git-diff style changes to your original plan to turn it into the new, enhanced, much longer and detailed plan that integrates the best of all the plans with every good idea included (you don't need to mention which ideas came from which models in the final revised enhanced plan):

[Paste competing plans here]
```
