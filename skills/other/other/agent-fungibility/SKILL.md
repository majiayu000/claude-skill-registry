---
name: agent-fungibility
description: "The philosophy and practical benefits of agent fungibility in multi-agent software development. Why homogeneous, interchangeable agents outperform specialized role-based systems at scale."
---

# Agent Fungibility — The Key to Scalable Agent Swarms

> **Core Principle:** "Fungibility bestows a LOT of really good properties automatically in a computer system."
>
> YOU are the bottleneck. Be the clockwork deity to your agent swarms: design a beautiful and intricate machine, set it running, and then move on to the next project.

---

## The Debate: Specialized vs. Fungible Agents

A burgeoning debate has sprung up around the optimal way to scale up the number of agents working on a software project:

| Approach | Description |
|----------|-------------|
| **Specialized Roles** | Assign distinct roles (tester agent, backend agent, committer agent, etc.) |
| **Fungible Agents** | All agents are identical and can do any task |

**The answer for software development: Fungible agents win.**

---

## Why Fungibility Works

### The Problem with Specialized Agents

Rather than setting up a complex heterogeneous system where you have assigned roles to specific tasks for agents, which is **brittle** and creates problems when one of the agents crashes or loses its memory or otherwise suffers from context rot and needs to be euthanized, you have to deal with:

1. **Understanding what kind of agent just died**
2. **What was it doing when it died**
3. **How to replace it functionally with the relevant context**
4. **What happens to the other agents that were depending on that specialized agent?**

### The Fungibility Solution

You're better off just having a bunch of **fungible agents** that are all simply executing beads of any kind.

They can be any kind of agent:
- Claude Code
- Codex
- Gemini CLI
- Amp
- Cursor
- etc.

But they're **fungible** in that they can all wear any hat and adaptively assume any role depending on the bead task they're working on.

---

## The Two Big Unlocks

### 1. Use BV to Choose Optimal Next Bead

Each agent uses `bv --robot-triage` or `bv --robot-next` to find the highest-impact ready bead. No central assignment needed.

### 2. Put Everything in the Plan → Beads

If you put everything you want to have happening in your original markdown plan that you turn into beads, you get everything else "for free" and it's robust to bad things happening to any agents.

---

## Robustness Properties

Agents fail. They:
- Crash
- You accidentally close the tab
- Context rot (lose track of what they're doing)
- Get stuck in loops
- Need to be "euthanized" and restarted

**With fungible agents, you never have to worry about that stuff.**

When an agent dies:
1. The bead it was working on remains marked in-progress
2. Any other agent can pick it up
3. No special replacement logic needed
4. No dependency on that specific agent

---

## Scaling Properties

When you want to move faster:
- Simply spin up more agents at any time
- Don't need to think about whether there's an imbalance between the counts of each agent role
- 3 agents → 10 agents → 20 agents: just add more, they all do the same thing

**Agent fungibility lets you go much faster and scales better, especially as:**
- Projects get larger and more complex
- Agent counts increase past 10 working on the same project at the same time

---

## The Analogy: Fountain Codes

This is why I'm a huge fan of things like fountain codes (like RaptorQ) for file storage:

> Turn a file into an endless stream of fungible blobs with very little overhead and the user can catch any blob in any order and each new blob helps them reconstruct the file; there's no "rarest chunk" like with BitTorrent.

In software development:
- Each bead is a "blob"
- Any agent can work on any bead
- There's no "critical specialist" that becomes a bottleneck
- The system is resilient to partial failures

---

## When Specialized Roles DO Make Sense

There are contexts where designated roles for agents work better. Example: **Automated scientific inquiry** (like BrennerBot).

Why it works there:
- The discourse itself (the back and forth between different agent types) is the core mechanism of surfacing truth
- The debate structure IS the point

Why it doesn't work for software:
- In software development, we just want good code that works
- The goal is output, not discourse
- Fungibility removes bottlenecks and single points of failure

---

## The Clockwork Deity Philosophy

> **Most of my agent tooling and workflows are about removing me from the equation, because there's only one of me, but a potentially unlimited number of agents.**

The way to do this:
1. **Front-load all input in planning phases** — Use GPT Pro with Extended Reasoning, multiple iterations, blend feedback from all frontier models
2. **Offload task structuring** — Convert plans to beads with full dependency graphs
3. **Allow direct communication** — Agent Mail lets agents coordinate without you
4. **Set it running and move on** — By the time you come back, huge chunks of work are done

### Why This Works

It all ultimately works because:
- The best models (GPT Pro) are used to their fullest
- Many iterations with blending feedback from all frontier models
- The very best model as the final arbiter
- In "plan space" it all fits easily in context windows
- Models can see the entire system at once instead of through a pinhole

---

## Practical Implementation

### Starting a Fungible Swarm

```bash
# Spawn agents (any mix of types)
ntm spawn myproject --cc=3 --cod=2 --gmi=1

# Give them all the SAME initial prompt
ntm send myproject --all "$(cat initial_prompt.txt)"
```

### The Initial Prompt (Same for All)

```
First read ALL of the AGENTS dot md file and README dot md file super carefully and understand ALL of both! Then use your code investigation agent mode to fully understand the code, and technical architecture and purpose of the project. Then register with MCP Agent Mail and introduce yourself to the other agents.

Be sure to check your agent mail and to promptly respond if needed to any messages; then proceed meticulously with your next assigned beads, working on the tasks systematically and meticulously and tracking your progress via beads and agent mail messages.

Don't get stuck in "communication purgatory" where nothing is getting done; be proactive about starting tasks that need to be done, but inform your fellow agents via messages when you do so and mark beads appropriately.

When you're not sure what to do next, use the bv tool mentioned in AGENTS dot md to prioritize the best beads to work on next; pick the next one that you can usefully work on and get started. Make sure to acknowledge all communication requests from other agents and that you are aware of all active agents and their names.  Use ultrathink.
```

### When an Agent Fails

1. Don't panic
2. Start a new session in its place
3. Give it the same initial prompt
4. It will:
   - Read AGENTS.md
   - Check bead status via bv
   - See what's in-progress/stuck
   - Either resume or pick a new bead

No special logic. No role assignment. Just fungibility.

---

## Summary

| Property | Specialized Agents | Fungible Agents |
|----------|-------------------|-----------------|
| **Failure handling** | Complex | Simple |
| **Scaling** | Requires role balancing | Just add more |
| **Replacement** | Need matching specialist | Any agent works |
| **Single point of failure** | Yes (each role) | No |
| **Coordination overhead** | High | Low (via beads + mail) |
| **Human involvement** | Ongoing | Front-loaded in planning |

**The bottom line:** Agent fungibility lets you build the machine once, set it running, and move on. The swarm handles the rest.
