---
name: delegation
description: "Unified provider selection for subagent delegation. Quick decision matrix for choosing between Kimi K2.5, GLM, and MiniMax based on task type."
---

# Unified Delegation Skill

## ⛔ CRITICAL: No Claude Subagents (MANUAL ENFORCEMENT)

**NEVER spawn Claude models (Haiku, Sonnet, Opus) as subagents.**

⛔ **The deny rules in `.claude/settings.local.json` DO NOT enforce this.**
⛔ **Manual verification required before EVERY Task() call.**

See CLAUDE.md for the pre-Task() checklist and fallback protocol.

---

## Provider Selection Matrix

| Task Type | Best Provider | Why | Fallback 1 | Fallback 2 | Last Resort |
|-----------|--------------|-----|------------|------------|-------------|
| Complex reasoning | **Kimi K2.5** | Most intelligent, 256K context | GLM-4.7 | MiniMax | Claude direct |
| Image/vision (batch) | **Kimi K2.5** | Built-in vision capability | GLM-4.6v | — | Claude direct |
| Creative/brainstorming | **GLM-4.7** | Strong creative problem-solving | Kimi | MiniMax | Claude direct |
| Web research | **MiniMax** | Fast, reliable, cheap | GLM | Kimi | Claude direct |
| Simple file exploration | **MiniMax** | Quick turnaround | GLM | Kimi | Claude direct |
| Batch operations | **GLM** | Good parallelism | MiniMax | Kimi | Claude direct |
| Code review | **MiniMax** | Fast blind-spot check | Kimi | GLM | Claude direct |

---

## Automatic Fallback Protocol

**When a Task() call fails, follow this chain (NEVER fallback to Haiku/Sonnet/Opus):**

| Primary Failed | Try Next | Then Try | Last Resort |
|----------------|----------|----------|-------------|
| Kimi K2.5 | GLM-4.7 | MiniMax | Claude does work directly |
| GLM-4.7 | MiniMax | Kimi K2.5 | Claude does work directly |
| MiniMax | GLM-4.7 | Kimi K2.5 | Claude does work directly |

**Example:**
```python
# ❌ WRONG - Kimi failed, fell back to Haiku
Task(model="kimi", ...) → Error
Task(model="haiku", ...) → VIOLATION

# ✅ CORRECT - Kimi failed, fell back to GLM
Task(model="kimi", ...) → Error
Task(model="minimax", ...) → Success
```

**If all cheap models fail:**
1. Do the work yourself (Claude)
2. Document why all subagents failed
3. Flag for manual investigation with user
4. NEVER use Haiku/Sonnet/Opus as fallback

---

## Quick Decision Flow

```
┌─ Is it reasoning/decisions? ──────────────────┐
│  YES → Claude does it directly                │
│  NO  → Delegate to subagent ↓                 │
├───────────────────────────────────────────────┤
│                                               │
│  ┌─ Does it need vision? ───────────────────┐ │
│  │  YES → Kimi K2.5 (or GLM-4.6v fallback)  │ │
│  │  NO  ↓                                   │ │
│  └──────────────────────────────────────────┘ │
│                                               │
│  ┌─ Is it complex/creative? ────────────────┐ │
│  │  Complex → Kimi K2.5                     │ │
│  │  Creative → GLM-4.7                      │ │
│  │  Simple → MiniMax                        │ │
│  └──────────────────────────────────────────┘ │
└───────────────────────────────────────────────┘
```

---

## Provider Profiles

### Kimi K2.5 (Most Capable)
**Context:** 256K tokens | **Vision:** Yes | **Thinking mode:** Yes

**Best for:**
- Complex multi-step reasoning
- Batch image analysis (10+ images)
- Tasks requiring deep understanding
- Fallback for failed GLM tasks

**Launcher:** `.\scripts\start-kimi.ps1`

**API Config:**
```
Base URL: https://api.moonshot.cn/anthropic/
Models: kimi-k2.5-thinking, kimi-k2-turbo-preview
```

### GLM-4.7 (Creative)
**Context:** 128K tokens | **Vision:** GLM-4.6v variant | **Thinking mode:** Yes

**Best for:**
- Creative brainstorming
- Mathematical reasoning (95.7% AIME 2025)
- Parallel batch tasks
- Tool use orchestration

**MCP:** `.cursor/mcp.json` (GLM-4.6v configured)

### MiniMax M2.1 (Fast & Cheap)
**Context:** 128K tokens | **Vision:** VLM API | **Speed:** Fastest

**Best for:**
- Quick web searches
- Simple file exploration
- Structured data extraction
- Code review for blind spots

**Launcher:** `.\scripts\start-claude-minimax.ps1`

**MCP:** `.cursor/mcp.json` (MiniMax configured)

---

## Delegation Patterns

### Pattern 1: Research → Claude Decides
```
1. Claude receives task requiring research
2. Claude spawns MiniMax: "Find all uses of X in codebase"
3. MiniMax returns findings
4. Claude reasons and implements
```

### Pattern 2: Batch Vision Analysis
```
1. Claude needs to analyze 20 sprites
2. Claude spawns Kimi K2.5: "Analyze quality of each sprite"
3. Kimi returns analysis for all 20
4. Claude makes decisions based on report
```

### Pattern 3: Creative Exploration
```
1. Claude needs alternative approaches
2. Claude spawns GLM-4.7: "Brainstorm 5 solutions for X"
3. GLM returns creative options
4. Claude selects and refines best approach
```

### Pattern 4: Code Review
```
1. Claude writes code
2. Claude spawns MiniMax: "Check for bugs, edge cases, security issues"
3. MiniMax returns concerns
4. Claude addresses or dismisses with reasoning
```

---

## Parallel Delegation

Launch multiple subagents in a single message:
```
Task(prompt="Research X", subagent_type="general-purpose")  ←─┐
Task(prompt="Research Y", subagent_type="general-purpose")  ←─┼─ Parallel
Task(prompt="Research Z", subagent_type="general-purpose")  ←─┘
```

**Rules:**
- Independent tasks → parallel
- Dependent tasks → sequential
- Never chain Claude subagents

---

## Background Execution (Token Suspension)

**Problem:** Claude tokens burn while waiting for subagent results.
**Solution:** Use `run_in_background=true` + end turn early.

### Pattern: Fire-and-Retrieve
```
1. Claude receives task requiring research
2. Task(prompt="...", run_in_background=true) → returns output_file
3. Claude ends turn: "Research agent dispatched. Say 'continue' for results."
4. User says "continue"
5. TaskOutput(task_id="...", block=true) → retrieves results
6. Claude synthesizes and responds
```

### When to Use Background Execution

| Scenario | Background? | Why |
|----------|-------------|-----|
| Research >30 sec | ✅ Yes | Saves expensive Claude wait time |
| Batch image analysis | ✅ Yes | Long-running, user can wait |
| Quick file lookup | ❌ No | Faster to wait inline |
| Claude needs result to continue | ❌ No | Would block anyway |

### Token Savings Calculation
```
Blocking:     Claude waits 60s = 60s of Opus tokens burned
Background:   Claude ends turn = 0s of Opus tokens burned
              (subagent tokens are 50x cheaper)
```

### Example Usage
```
# Fire (spawn and end turn immediately)
Task(
  prompt="Analyze all 20 sprites in assets/sprites/",
  subagent_type="general-purpose",
  run_in_background=true
)
→ Returns: {task_id: "abc123", output_file: "/path/to/output"}

# ... Claude ends turn, tells user to say "continue" ...

# Retrieve (on next turn)
TaskOutput(task_id="abc123", block=true)
→ Returns: Full subagent analysis
```

---

## Token Economics

| Provider | Relative Cost | When to Use |
|----------|---------------|-------------|
| Claude Opus | 50x | Final decisions, complex reasoning |
| Claude Sonnet | 10x | Medium reasoning (avoid as subagent) |
| Kimi K2.5 | 1x | Complex tasks, vision |
| GLM-4.7 | 1x | Creative, batch |
| MiniMax | 1x | Fast, simple |

**Key insight:** 1 hour Claude exploration = 50 hours subagent exploration (cost).

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Claude spawning Haiku | Expensive | Use MiniMax instead |
| Sequential when parallel possible | Slow | Single message, multiple Tasks |
| Kimi for simple lookup | Overkill | Use MiniMax |
| MiniMax for complex reasoning | Poor quality | Use Kimi K2.5 |
| Claude reading 10+ files | Context bloat | Delegate exploration |

---

## Integration with Other Skills

- **`/skill kimi-k2.5`** - Detailed Kimi setup and patterns
- **`/skill minimax-mcp`** - MiniMax MCP integration details
- **`/skill token-efficient-delegation`** - Full token economics
- **`/skill subagent-best-practices`** - General subagent patterns

---

[Opus 4.5 - 2026-01-29]
