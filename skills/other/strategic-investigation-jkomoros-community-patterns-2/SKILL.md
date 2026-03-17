---
name: strategic-investigation
description: >
  Proactive recovery using plan mode and subagents. After 1-2 failed attempts,
  STOP trying variations. Enter plan mode and launch parallel Explore/Plan agents
  to find idiomatic solutions instead of spinning wheels.
---

# Strategic Investigation: Plan Mode Recovery

**CORE PRINCIPLE: After 1-2 failed attempts, STOP trying variations. Enter plan mode and investigate properly using parallel subagents.**

## When to Use This Skill

Use this skill when:
- You've tried 1-2 approaches and they didn't work
- You don't understand WHY something isn't working
- You're tempted to try "just one more thing" or add a hacky workaround
- The error message doesn't make sense
- Multiple approaches seem valid and you're unsure which is idiomatic
- You find yourself guessing instead of knowing

**Warning signs you should have used this earlier:**
- You've been trying variations of the same approach for 5+ minutes
- You're adding workarounds or "temporary" hacks
- The code is getting messier instead of cleaner
- You're saying "this should work but doesn't"

## The Process

### Step 1: STOP and Acknowledge

When you recognize you're stuck:

1. **Stop immediately** - Don't try "just one more thing"
2. **Tell the user:**
   ```
   "I've tried [X approaches] and they're not working. Instead of continuing
   to guess, I'm going to step back and investigate this systematically using
   parallel subagents. This should find the idiomatic solution."
   ```

### Step 2: Enter Plan Mode

Request plan mode to structure your investigation. Plan mode signals you're stepping back from implementation to investigate properly.

### Step 3: Launch Parallel Subagents

Spawn 2-4 focused Explore agents **in parallel** to gather information:

**Subagent Design Principles:**
- Each agent gets ONE focused question
- Agents explore DIFFERENT angles (not variations of same thing)
- Agents are read-only (Explore type)
- Each returns concrete findings with file paths and code snippets

**Common Explore Agent Types:**

```
Explore Agent 1: Pattern Search
- Search labs/packages/patterns/ for similar patterns
- Search patterns/examples/ for curated examples
- Look for patterns that solve similar problems
- Return: file paths, relevant code snippets, patterns used

Explore Agent 2: Documentation Deep-Dive
- Read relevant sections of ~/Code/labs/docs/common/
- Focus on DEBUGGING.md, PATTERNS.md, CELLS_AND_REACTIVITY.md
- Look for exact guidance on this situation
- Return: relevant doc sections, warnings, recommended approaches

Explore Agent 3: Community Knowledge
- Search community-docs/superstitions/ for similar issues
- Check if others have hit this problem
- Return: relevant superstitions, known workarounds

Explore Agent 4: Framework Conventions
- Study how working patterns structure similar code
- What's the "frameworky" way to do this?
- Return: conventions observed, idioms to follow
```

### Step 4: Synthesize Findings

After agents complete:

1. **Review gathered information:**
   - What patterns did similar code use?
   - What exactly do the docs say?
   - What community knowledge exists?

2. **Identify the idiomatic solution:**
   - Which approach follows framework conventions?
   - What do working examples do differently?
   - What would a framework expert do?

3. **Understand WHY this is the right solution:**
   - Don't just copy-paste from examples
   - Be able to explain why this works
   - Understand the underlying principle

### Step 5: Execute with Confidence

Now implement the chosen approach:
- You understand WHY this approach is right
- You've verified it matches framework conventions
- You're not guessing anymore

### Step 6: Handle Continued Failure

**If the solution doesn't work after investigation:**

1. Return to Step 3 with NEW context: "Approach X didn't work because Y"
2. Investigate why the expected solution failed
3. This often reveals the real underlying issue

**After 2 plan-mode investigation cycles without resolution:**
- Escalate to user
- Summarize what you investigated
- Show approaches you tried
- Explain what you learned
- This gives user actionable context to help

## Example Investigation

### Scenario: "Cell not updating reactively"

**Failed attempts:** Changed dependencies, added .get() calls, restructured code

**Investigation plan (launch in parallel):**

```
Explore Agent 1: Pattern Search
"Search labs/packages/patterns/ for computed() usage patterns.
Find 3+ examples of computed cells that update correctly.
Note what they do differently from my failing code."

Explore Agent 2: Documentation
"Read ~/Code/labs/docs/common/CELLS_AND_REACTIVITY.md thoroughly.
Focus on computed() section and any gotchas.
Look for 'don't do X' warnings."

Explore Agent 3: Community Knowledge
"Search community-docs/superstitions/ for 'computed', 'reactive', 'update'.
Check if this is a known edge case with solutions."

Explore Agent 4: Framework Behavior
"Study how other patterns structure reactive computations.
What cell access patterns do working examples use?"
```

**Likely synthesis:**
- Reactivity requires direct cell access, not derived values
- Creating new cells inside computed() breaks tracking
- Need to maintain stable cell references
- Idiomatic approach: lift cell creation to pattern body level

## Good vs Bad Uses

### GOOD - Use Strategic Investigation

- "I've tried computed() and derive() and neither updates. Let me investigate."
- "The type error doesn't make sense. Let me understand what the framework expects."
- "This feels hacky. Let me find the idiomatic way."
- "I'm not sure which approach is right. Let me explore the options properly."

### BAD - Don't Use Strategic Investigation

- Simple typos - just fix them
- Missing imports - just add them
- Error message tells you exactly what's wrong - just apply the fix
- Problem you've solved before - apply known pattern

## Key Principle: Idiomatic Over Working

The goal is not just to find SOMETHING that works, but to find the IDIOMATIC solution:

- **Hacky:** "I'll just cast to any and suppress the error"
- **Idiomatic:** "The framework expects X pattern, let me use that"

If investigation reveals the "right" way is significantly different from your approach, that's valuable - even if your hack might have worked.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| **community-docs** | Quick check FIRST. If doesn't help after 1-2 attempts → strategic-investigation |
| **recovery-strategies** | Strategic investigation is Step 2.5 in that flow |
| **issue-filing** | Use AFTER investigation if problem is a framework limitation |
| **pattern-dev** | Contains development practices. This skill is for when you're stuck |

## Remember

**Investigation time is NOT wasted time.**

A 5-minute proper investigation often saves 30 minutes of trial-and-error on wrong approaches. Don't skip plan mode thinking "this should be simple" - that's often when you need it most.

**When in doubt, investigate.** It's better to investigate a simple problem than to spin wheels on a complex one.
