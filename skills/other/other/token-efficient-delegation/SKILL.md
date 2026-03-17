---
name: token-efficient-delegation
description: Auto-injects token-efficient delegation patterns. Claude tokens are 50x more expensive than MiniMax/GLM/Kimi.
---

# Token-Efficient Delegation

## ⛔ CRITICAL: No Claude Subagents

**HARD STOP:** Never use `model="haiku"`, `model="sonnet"`, or `model="opus"` in Task tool calls.

- Always use: `model` parameter omitted (routes to MiniMax/GLM)
- Or explicitly: general-purpose agent (uses cheaper default)
- Enforced in: `.claude/settings.local.json` deny rules

---

**Core Rule:** Claude = reasoning/decisions, MiniMax/GLM = research/exploration

## The Three Goals (Balance All Three)

| Goal | Priority | Strategy |
|------|----------|----------|
| **Quality** | Keep Opus-level output | Claude synthesizes, subagents gather |
| **Cost** | Minimize Claude tokens | Delegate exploration, batch analysis |
| **Speed** | Fast execution | Parallel subagents, right model for task |

---

## Quick Decision Tree

Before ANY task, ask:

1. **Research/exploration?** → Delegate to MiniMax (fast) or GLM (creative)
2. **Web search needed?** → Delegate to MiniMax
3. **Reading specific known file?** → Claude direct (Read tool)
4. **Analyzing 1-3 images?** → Claude direct
5. **Analyzing 10+ images?** → Parallel subagents (GLM for quality, MiniMax for speed)
6. **Complex reasoning/code?** → Claude direct
7. **Broad codebase search?** → Delegate to general-purpose agent (cheaper default)

---

## Model Characteristics (Official Guidance)

| Model | Cost | Speed | Best For | Source |
|-------|------|-------|----------|--------|
| Claude Opus | 50x | Fast | Complex reasoning, architecture, final decisions | [Anthropic Docs](https://docs.anthropic.com) |
| Claude Sonnet | 10x | Fast | Coding, medium reasoning, code review | [Anthropic Docs](https://docs.anthropic.com) |
| Claude Haiku | 2x | Fastest | Exploration, classification, simple tasks | [Anthropic Docs](https://docs.anthropic.com) |
| MiniMax M2.1 | 1x | Fast | Instruction-following, agents, multi-lang coding | [MiniMax Docs](https://platform.minimax.io) |
| GLM-4.7 | 1x | Medium | Creative problem-solving, math, tool use | [Z.AI Docs](https://docs.z.ai) |
| GLM-4V | 1x | Medium | Vision, 66K multimodal context, GUI tasks | [Z.AI Docs](https://docs.z.ai) |

---

## When to Use Each Model

### MiniMax M2.1 - Fast Instruction-Follower
*Source: [MiniMax Official Docs](https://platform.minimax.io/docs/coding-plan/best-practices)*

- Quick web searches
- Structured data extraction
- File reading with specific questions
- Tasks with clear instructions
- **8% of Claude cost, 2x speed**
- Preserve reasoning chains (return full response with `thinking` field)

### GLM-4.7 - Creative Problem-Solver
*Source: [Z.AI GLM-4.7 Docs](https://docs.z.ai/guides/llm/glm-4.7)*

- Complex problem exploration
- Mathematical reasoning (95.7% on AIME 2025)
- Creative solutions needed
- Tool use orchestration (42.8%, ties GPT-5.1)
- Parallel batch tasks (latency doesn't matter)
- Use **thinking mode** for complex tasks, disable for simple queries

### GLM-4V - Vision Tasks
*Source: [GLM-V GitHub](https://github.com/zai-org/GLM-V)*

- 66K-token multimodal context
- Screenshot/GUI analysis
- Document parsing (PDFs, charts)
- Video understanding with timestamps
- Multi-image analysis

### Claude (Haiku/Sonnet/Opus) - Reasoning & Decisions
*Source: [Anthropic Subagents Docs](https://code.claude.com/docs/en/sub-agents)*

- **Haiku**: Fast exploration, read-only tasks, classification
- **Sonnet**: Coding, medium-complexity reasoning
- **Opus**: Architecture decisions, synthesis, complex reasoning
- Use subagents to isolate verbose output from main context

---

## Quality Preservation Patterns

### Pattern 1: Orchestrator-Worker Split
```
Claude (Orchestrator) → Spawns subagents → Subagents research → Claude synthesizes
```
**Quality preserved because:** Claude makes all decisions based on subagent research.

### Pattern 2: Parallel Research + Single Synthesis
```
5 MiniMax agents research in parallel → Claude receives summaries → Claude decides
```
**Quality preserved because:** Multiple perspectives, Claude does final reasoning.

### Pattern 3: Two-Stage Review
```
Subagent implements → Reviewer subagent checks → Claude integrates
```
**Quality preserved because:** Cross-validation catches errors before Claude acts.

### Pattern 4: Specific Prompts
*Source: [MiniMax Best Practices](https://platform.minimax.io/docs/coding-plan/best-practices)*

> "State the 'why' behind your request - when models understand purpose, they provide more accurate answers."

```
BAD:  "Research authentication"
GOOD: "Find how Godot 4.5 handles input authentication. I need to implement player login. Return: method name, file location, example usage."
```

---

## Speed Optimization Patterns

### Pattern 1: Parallel Execution
Launch independent tasks simultaneously:
```
Task(prompt="Research X")  ←─┐
Task(prompt="Research Y")  ←─┼─ Single message, parallel execution
Task(prompt="Research Z")  ←─┘
```

### Pattern 2: Right Model for Latency
| Need | Model | Latency |
|------|-------|---------|
| Instant response | Haiku | ~100ms |
| Quick research | MiniMax | ~200ms |
| Deep analysis | GLM-4.7 | ~500ms |
| Complex reasoning | Opus | ~300ms |

### Pattern 3: Batch Over Sequential
```
BAD:  Analyze image 1 → wait → Analyze image 2 → wait → ...
GOOD: Spawn 10 parallel agents → each analyzes 1 image → aggregate
```

---

## Cost Optimization Patterns

### Pattern 1: Delegate Exploration
*Source: [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)*

> "Delegate verbose operations (tests, log processing, documentation fetching) to subagents so output stays isolated from main conversation."

### Pattern 2: Context Isolation
Subagents prevent context bloat:
```
Main context: 5000 tokens (stays lean)
Subagent reads 10 files: 15000 tokens (isolated, discarded after)
Result passed back: 500 tokens (only what matters)
```

### Pattern 3: Cascade Routing
*Source: [Anthropic Model Selection](https://platform.claude.com/docs/en/docs/about-claude/models/overview)*

```
60-70% of queries → Haiku (cheapest)
20-30% of queries → Sonnet (medium)
10-15% of queries → Opus (only when needed)
```

### Pattern 4: Token Suspension via Background Execution

**The Problem:** Claude tokens burn while waiting for subagent results.

**The Solution:** Use `run_in_background=true` and **end the turn early**.

```
┌─────────────────────────────────────────────────────────┐
│ BLOCKING (expensive)                                    │
├─────────────────────────────────────────────────────────┤
│ Claude spawns subagent → waits 60s → gets result       │
│ Cost: 60 seconds of Opus tokens BURNED                  │
├─────────────────────────────────────────────────────────┤
│ BACKGROUND + END TURN (cheap)                           │
├─────────────────────────────────────────────────────────┤
│ Claude spawns with run_in_background=true → ends turn  │
│ Cost: ~0 seconds of Opus tokens (turn ended)           │
│ Subagent runs: 60s of cheap tokens                      │
│ User says "continue" → Claude retrieves with TaskOutput│
└─────────────────────────────────────────────────────────┘
```

**When to suspend (use background):**
- Research/exploration tasks >30 seconds
- Batch image analysis (10+ images)
- Web searches with multiple queries
- Code review by subagent

**When NOT to suspend:**
- Quick lookups (<5 seconds)
- Claude needs result to continue current reasoning
- Interactive debugging requiring rapid iteration

**Fire-and-Retrieve Workflow:**
```
1. Task(prompt="Research X", run_in_background=true)
   → Returns immediately with task_id and output_file
2. Claude responds: "Research dispatched. Say 'continue' when ready."
3. User prompts again
4. TaskOutput(task_id="...", block=true)
   → Returns full results
5. Claude synthesizes and delivers answer
```

**Key phrase:** For tasks >30 seconds, use background execution and end turn early.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Claude reads 10+ files | Context bloat, expensive | Spawn Explore agent |
| Sequential subagent calls | Slow, wasted time | Parallel in single message |
| Re-reading subagent results | Duplicates tokens | Trust the summary, decide |
| Opus for simple classification | Overkill, expensive | Use Haiku |
| GLM for quick lookups | Too slow | Use MiniMax |

---

## Integration with Project Workflows

### HPV (Playtesting)
- Use MCP for game state inspection (local, fast)
- Delegate screenshot analysis to GLM-4V for batch checks

### Visual Development
- 1-3 sprites: Claude direct
- 10+ sprites: Parallel GLM-4V agents
- Quality gate: Claude reviews subagent findings

### Code Implementation
- Research patterns: MiniMax subagents
- Write code: Claude direct
- Review: Haiku subagent for spec compliance

---

## Official Documentation Sources

- [Anthropic Subagents](https://code.claude.com/docs/en/sub-agents)
- [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Anthropic Token-Efficient Tools](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/token-efficient-tool-use)
- [MiniMax Best Practices](https://platform.minimax.io/docs/coding-plan/best-practices)
- [MiniMax Agent Learnings](https://www.minimax.io/news/minimax-agent-what-we-learned-while-building-in-2025)
- [Z.AI GLM-4.7 Docs](https://docs.z.ai/guides/llm/glm-4.7)
- [GLM-V Vision Model](https://github.com/zai-org/GLM-V)

---

[Claude Opus 4.5 - 2026-01-29]
