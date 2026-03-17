---
name: when-stuck
description: Dispatch to right technique when you hit a wall
version: 1.0.0
author: Ariff
when_to_use: When progress stops - identify stuck type and apply matching technique
---

# When Stuck

## Recognition

You're stuck when:
- Same approach tried multiple times
- Context window filling with failed attempts
- No clear next step
- Feeling "lost" or "frustrated"

## The Dispatch Table

| Stuck Type | Symptoms | Technique |
|-----------|----------|-----------|
| **Don't understand** | Requirements unclear | → Ask user for clarification |
| **Can't find code** | No idea where logic lives | → Semantic search, file patterns |
| **Bug won't die** | Fix doesn't work | → Root cause tracing |
| **Tests keep failing** | Can't get green | → Defense in depth, fresh look |
| **Scope creep** | Task keeps growing | → Scope boundary check |
| **Missing context** | Need info I don't have | → Read more files, ask user |
| **Wrong approach** | This path won't work | → Brainstorm alternatives |
| **Overwhelmed** | Too complex | → Break into smaller pieces |
| **Going in circles** | Same ground repeatedly | → Fresh agent via subagent |

## Technique Details

### Don't Understand → Clarify
```
STOP trying to guess
ASK: "I'm unclear on [specific thing]. Could you clarify [specific question]?"
WAIT for response before proceeding
```

### Can't Find Code → Search Strategies
```
1. Semantic search with concept terms
2. Grep for unique strings
3. File pattern matching
4. Read likely files
5. List directories to discover structure
```

### Bug Won't Die → Root Cause Trace
```
1. Document exact symptom
2. Trace backward: where does bad value come from?
3. Keep tracing until you find ORIGIN
4. Fix at origin, not symptoms
```

### Tests Keep Failing → Fresh Eyes
```
1. Stop. Step back.
2. Re-read test expectation
3. Re-read actual behavior
4. Check: is test right or is code right?
5. Check: is environment consistent?
```

### Scope Creep → Boundary Check
```
1. Re-read original request
2. List what you've done vs. what was asked
3. Identify scope drift
4. Either: refocus OR ask user if expansion wanted
```

### Missing Context → Gather More
```
1. What specific info do you need?
2. Where might it be? (files, user knowledge, docs)
3. Ask/search for that specific info
4. Don't proceed without it
```

### Wrong Approach → Brainstorm
```
1. What other approaches exist?
2. List 3-4 alternatives
3. Evaluate each briefly
4. Pick most promising, try it
5. If that fails, try next
```

### Overwhelmed → Decompose
```
1. What's the smallest possible piece?
2. Do JUST that piece
3. Verify it works
4. What's next smallest piece?
5. Repeat until done
```

### Going in Circles → Fresh Agent
```
Signal: Same ground covered 3+ times
Action: Use subagent for specific subtask
Pass: Clear scope, success criteria
Return: Just the result, not the journey
```

## Anti-Patterns

❌ **Brute Force**
```
Trying same thing harder won't work
If it failed twice, it needs a different approach
```

❌ **Hoping**
```
"Maybe this time..." → No
Stop. Diagnose. Change approach.
```

❌ **Hiding**
```
Not admitting you're stuck wastes time
Say: "I'm stuck on X. Here's what I've tried..."
```

## Success Metric

After applying technique:
- Clear next step identified
- Progress resuming
- If still stuck → try next technique from table
- If nothing works → ASK USER for help

## Integration

Pairs well with:
- `assumption-checker` → Often stuck because of wrong assumption
- `intent-clarifier` → Often stuck because of unclear intent
- `brainstorming` → For generating alternatives
- `root-cause-tracing` → For debugging stuck
