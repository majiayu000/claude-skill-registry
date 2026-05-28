---
name: recovery-strategies
description: >
  Escalation path when stuck on pattern development. Use when encountering
  TypeScript errors, framework confusion, unexpected behavior, or blocked progress.
  Five-step recovery: check docs, study examples, strategic investigation (plan mode
  + subagents), reset and retry, ask user.
---

# Recovery Strategies for Pattern Development

**CRITICAL: Don't spin your wheels when stuck. Follow this escalation path AGGRESSIVELY.**

When encountering any difficulty with pattern development - whether it's TypeScript errors, unexpected behavior, or uncertainty about framework features - **immediately begin this recovery sequence**. Do NOT:
- Continue trying the same approach repeatedly
- Guess at solutions without checking documentation
- Waste time in unproductive loops

**If you find yourself stuck for more than 1-2 attempts, MOVE TO THE NEXT STEP.**

Use this escalation path:

## Step 1: Re-read Documentation (First Response to Being Stuck)

**ALWAYS start here when encountering pattern development issues:**

```
"Use the pattern-dev skill to refresh your understanding of framework patterns"
```

The pattern-dev skill reads all latest pattern documentation from labs. Pay **particular attention** to:

- **`~/Code/labs/docs/common/DEBUGGING.md`** - Common pitfalls and anti-patterns
  - Quick error reference table
  - Type errors (Cell<>, OpaqueRef<>, etc.)
  - Style errors (object vs string syntax)
  - Reactivity issues (bidirectional binding, computed(), ifElse())
  - Runtime errors (DOM access, LLM in handlers, etc.)
- **`~/Code/labs/docs/common/PATTERNS.md`** - Pattern examples and best practices
- **`~/Code/labs/docs/common/CELLS_AND_REACTIVITY.md`** - Reactivity system details
- **`~/Code/labs/docs/common/TYPES_AND_SCHEMAS.md`** - Type system rules

**When to use:**
- Encountering any TypeScript errors
- Pattern compiles but doesn't work as expected
- UI not updating reactively
- Confused about Cell<>, OpaqueRef<>, bidirectional binding
- Before asking user for clarification on framework behavior

**When to move to Step 2:**
- After reading relevant docs but still unclear on solution
- Error persists after applying documented fixes
- Need to see concrete examples of working code
- After 1-2 attempts based on documentation

## Step 2: Study Similar Working Patterns

After refreshing documentation, look at existing working patterns **in this priority order:**

**1. Labs patterns** (highest priority - canonical examples):
```bash
$PARENT_DIR/labs/packages/patterns/
# These are the most up-to-date, authoritative examples
# If a pattern exists here, it's the gold standard
```

**2. Patterns repository** (if available - well-tested real-world examples):
```bash
$PARENT_DIR/patterns/
# These are well-tested real-world patterns
# Skip this if patterns repo not cloned
```

**3. Community patterns - examples** (curated examples):
```bash
patterns/examples/
# These are specifically chosen as good examples
```

**4. Community patterns - jkomoros** (user patterns):
```bash
patterns/jkomoros/
# Prefer root-level (stable) over WIP/
# These may be more complex/experimental
```

**Within each directory:**
- ✅ Prefer non-WIP patterns (stable, tested)
- ⚠️ Use WIP/ patterns only if non-WIP doesn't exist
- 📁 Check root level first, then WIP/ as fallback

**How to find similar patterns:**
```bash
# Get parent directory for relative paths
PARENT_DIR="$(git rev-parse --show-toplevel)/.."

# Search for patterns using specific features
grep -r "generateObject" $PARENT_DIR/labs/packages/patterns/
grep -r "computed(" patterns/examples/
grep -r "handler<" $PARENT_DIR/labs/packages/patterns/

# List available patterns
ls $PARENT_DIR/labs/packages/patterns/
ls $PARENT_DIR/patterns/ 2>/dev/null || echo "patterns repo not cloned"
ls patterns/examples/
ls patterns/jkomoros/
```

**When to move to Step 2.5:**
- Can't find similar patterns for your use case
- Examples don't solve your specific problem
- After studying 2-3 similar patterns without clarity
- You don't understand WHY your approach isn't working

## Step 2.5: Strategic Investigation (Plan Mode + Subagents)

**After 1-2 failed attempts, STOP trying variations. Enter plan mode and investigate properly.**

Use the `strategic-investigation` skill to:
1. Step back from implementation mode
2. Launch parallel Explore agents to gather information
3. Synthesize findings - understand WHY the solution is correct
4. Execute with confidence

**This step is critical.** Don't skip it thinking "I'll just try one more thing." Systematic investigation often reveals the idiomatic solution faster than trial-and-error.

**When to move to Step 3:**
- After strategic investigation reveals a clear path forward
- If investigation shows this is a simple problem after all
- You now understand the idiomatic approach

## Step 3: Reset and Try Again (After Investigation)

If still stuck after Steps 1-2:

1. Reset to your last commit: `git reset --hard HEAD`
2. Reflect on what you learned from documentation and examples
3. Try a different approach incorporating that knowledge
4. Start with the simplest possible version that works
5. Add complexity incrementally, testing after each addition

**When to move to Step 4:**
- After 1-2 reset attempts without progress
- Problem persists despite fresh approaches
- Suspect this might be a framework limitation or bug
- Need architectural guidance beyond documentation

## Step 4: Ask User (Significant Confusion)

If Steps 1-3 don't resolve the issue:

1. Explain what you've tried (docs, examples, approaches)
2. Show specific error messages or unexpected behavior
3. Ask user for clarification or guidance
4. Consider if this is a framework limitation vs implementation issue

## Additional Resources

**After exhausting Steps 1-4, consider:**
- **Community superstitions** - Check `community-docs/superstitions/` for empirical knowledge (treat with skepticism)
- **Issue filing** - Document complex framework questions for authors (requires user permission)

**Remember:** This recovery strategy is your safety net. Follow it systematically to avoid spinning your wheels!
