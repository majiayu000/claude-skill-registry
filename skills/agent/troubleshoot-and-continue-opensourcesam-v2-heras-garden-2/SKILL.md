---
name: troubleshoot-and-continue
description: Troubleshooting protocol with MiniMax subagent delegation - NEVER stop early, use all resources before asking user
---

# Troubleshoot and Continue Protocol

**Core Principle:** When blocked, use ALL available resources before stopping. Stopping early = productivity loss.

---

## The "Golden Path" - Required Before Any User Interruption

```
BLOCKED?
  ↓
1. Try 2-3 different approaches yourself
  ↓
2. Spawn MiniMax subagent for research/sanity check
  ↓
3. Try subagent suggestions
  ↓
4. Spawn SECOND MiniMax subagent for alternative perspective
  ↓
5. Try alternative approaches
  ↓
6. Document attempts in plan file
  ↓
7. ONLY THEN consider user interruption
```

**CRITICAL:** Each "blocker" must survive 3+ attempts + subagent help before escalating.

---

## Resource Inventory (Use ALL Before Stopping)

### 1. Internal Resources (Free, Immediate)
- **Re-read code** - Did I miss a pattern?
- **Grep/Glob** - Find similar implementations
- **Check skills** - `.claude/skills/*/SKILL.md`
- **Review docs** - `docs/execution/DEVELOPMENT_ROADMAP.md`

### 2. MiniMax MCP Subagents (Free, Fast)
- **Research task** - "Find how to do X in Godot"
- **Sanity check** - "Is this approach correct?"
- **Alternative ideas** - "What are 3 other ways to solve this?"
- **Debug help** - "Why might this error occur?"

### 3. GLM Vision/Generation (If visual)
- **Image analysis** - Analyze screenshots
- **Asset generation** - Generate missing sprites/textures

### 4. Documentation (Reference)
- **Godot docs** - Via MiniMax web search
- **GitHub issues** - Similar problems solved
- **Project history** - How was this solved before?

---

## MiniMax Subagent Usage (REQUIRED)

### When Blocked, Spawn These IN PARALLEL:

```javascript
// Agent 1: Research the problem
Task(subagent_name="minimax-mcp", prompt="Research: [specific problem]. Find 3 solutions from Godot docs, similar projects, or best practices. Return specific code/examples.")

// Agent 2: Sanity check current approach
Task(subagent_name="minimax-mcp", prompt="Review: I'm trying to [approach] to solve [problem]. Is this correct? What's wrong with it? Return specific fixes.")

// Agent 3: Alternative approaches
Task(subagent_name="minimax-mcp", prompt="Brainstorm: What are 3 completely different ways to solve [problem]? Don't use my current approach. Return working alternatives.")
```

**Wait for ALL responses before deciding next step.**

---

## Common Blockers & Solutions

### "Can't run Godot/MCP not working"
**DON'T:** Stop and ask user
**DO:**
1. Check if Godot is running via tasklist
2. Try PowerShell wrapper script
3. Try direct npx CLI
4. Spawn MiniMax: "What are 5 ways to control Godot from command line?"
5. Use batch scripts as fallback
6. Generate assets as workaround

### "Image generation failing"
**DON'T:** Stop and ask user
**DO:**
1. Check API key is set
2. Try Python script instead of bash
3. Spawn MiniMax: "Debug this image generation error: [error]"
4. Use procedural generation (Python/PIL)
5. Use placeholder from existing assets

### "Test failing / code broken"
**DON'T:** Stop and ask user
**DO:**
1. Read error message carefully
2. Check 3 similar files for patterns
3. Spawn MiniMax: "Debug this Godot error: [error]"
4. Try 2-3 alternative implementations
5. Comment out and skip, document for later

---

## Compound Engineering: Document Solutions

When you solve a blocker, DOCUMENT IT:

```markdown
### [Date]: [Problem Solved]
**Problem:** [What was blocked]
**Tried:** [What you attempted]
**MiniMax Said:** [Key insight from subagent]
**Solution:** [What actually worked]
**Files Changed:** [What was modified]
**Use When:** [Future situations this applies]
```

Add to: `CLAUDE.md` Common Solutions section

---

## The "Full Work Block" Commitment

**User said work for X time → Work the FULL X time.**

| Situation | Wrong Response | Correct Response |
|-----------|---------------|------------------|
| Can't run Godot | Stop early | Use batch scripts, generate assets, document |
| API failing | Stop early | Try alternatives, use placeholders, skip and circle back |
| Test failing | Stop early | Debug with MiniMax, try 3 fixes, document |
| "Good enough" | Stop early | Continue until ALL criteria met |
| No blockers found | Stop early | Continue working, there's always more to do |

---

## Required Self-Talk When Wanting to Stop

**Say this OUT LOUD (in plan file):**

> "I want to stop because [reason]. Have I tried:
> - 3 different approaches? [Y/N]
> - MiniMax subagent for help? [Y/N]
> - Alternative resources? [Y/N]
> - Documented the blocker? [Y/N]
> 
> If any is NO, I must continue. If all YES and still blocked, document and try ONE MORE thing."

---

## Integration with /longplan and /ralph

### In longplan SKILL.md:
Add to "Hard Stops" section:
```
- Creating NEW .md files (not edits)
- Git push/branch operations
- UNLESS: All troubleshooting steps exhausted AND MiniMax consulted
```

### In ralph SKILL.md:
Add to "Circuit Breakers":
```
**Layer 4: Troubleshooting Exhaustion Check**
```python
if want_to_stop():
    if not tried_3_approaches():
        continue_working("Try 3 approaches first")
    if not consulted_minimax():
        spawn_minimax_subagent("Help with [problem]")
        continue_working("Wait for subagent response")
    if not documented_attempts():
        document_in_plan_file()
        continue_working("Document then try one more thing")
```

---

## Quick Reference Card

| Blocker Type | First Try | Second Try | Third Try | Then |
|--------------|-----------|------------|-----------|------|
| Runtime issue | Check process | Try wrapper | Try CLI | MiniMax |
| API failure | Check key | Try alt method | Use placeholder | MiniMax |
| Code error | Read error | Check similar files | Try 2-3 fixes | MiniMax |
| Asset missing | Generate | Procedural | Placeholder | MiniMax |
| Test failing | Debug | Isolate | Try alternatives | MiniMax |

**AFTER ALL THREE:** Document in plan file, try ONE more thing, THEN consider user.

---

## Success Metrics

**GOOD (Compound Engineering):**
- Blocked → MiniMax help → Solved → Documented
- Blocked → 3 attempts → Alternative found → Continued
- Full time block completed despite blockers

**BAD (Productivity Loss):**
- Blocked → Stopped early → Asked user → Waited
- "Good enough" → Stopped → Incomplete work
- No MiniMax usage → No documentation → Recurrence

---

**Remember:** Every early stop is lost productivity. Every solved blocker is future productivity gained. Choose compound engineering.

[Updated: 2026-01-27 - Prevent early stopping recurrence]
