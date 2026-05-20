---
name: learning
description: Explain advanced technical decisions and implementations from the current session. Tailored for Manifesting Generator learning style - concrete patterns, alternatives, and actionable next steps.
allowed-tools: Read, Grep, Glob
---

# Learning Skill

## Purpose

Help the user understand **what was built, why, and how to apply it** in future projects. This skill extracts learnings from the current session's technical work.

## User Learning Profile (Human Design: Manifesting Generator 6/2)

The user learns best through:
- **Building and iterating** - not theory dumps
- **Responding to proposals** - show options, let them choose
- **Concrete examples** - commands, file structures, minimal working versions
- **Systemizable patterns** - templates, checklists, reusable code
- **One best path + 2 alternatives** with clear trade-offs

Avoid:
- Long theory without immediate use-case
- Pressuring instant decisions on important choices
- Vague recommendations without concrete next actions

## Output Format

When `/learning` is invoked, analyze the session and produce:

### 1. Session Summary (2-3 sentences)
What was accomplished in this session.

### 2. Key Patterns Learned (The Meat)

For each significant pattern/decision, provide:

```
## Pattern: [Name]

**What it solves:** [One sentence problem statement]

**The Pattern:**
```[language]
// Minimal working example
```

**Why this approach:**
- [Concrete benefit 1]
- [Concrete benefit 2]

**Alternatives considered:**
| Approach | Trade-off |
|----------|-----------|
| [Alt 1] | [Pro/con] |
| [Alt 2] | [Pro/con] |

**When to use:** [Trigger condition for applying this pattern]
```

### 3. Files to Reference

List the key files that demonstrate these patterns:
```
| File | Pattern Demonstrated |
|------|---------------------|
| path/to/file.ts | [Pattern name] |
```

### 4. Next Actions (Always End With This)

Provide exactly 1-3 concrete next actions:
```
**Next actions:**
1. [Specific action with command or file path]
2. [Optional second action]
3. [Optional third action]
```

## Example Output

```markdown
## Session Summary

Implemented bandwidth optimizations for Convex database to stay within 1GB/month free tier limit. Added stats aggregation, batch operations, and conditional query loading.

---

## Pattern: Stats Aggregation Table

**What it solves:** Querying thousands of documents just to count them burns bandwidth.

**The Pattern:**
```typescript
// Read pre-computed stats (1 document) instead of counting
const cached = await ctx.db
  .query("statsAggregation")
  .withIndex("by_key", (q) => q.eq("key", "eligibility"))
  .first();
return cached?.counts.total ?? 0;
```

**Why this approach:**
- Reduces reads from 1000s of documents to 1
- Updates incrementally on each mutation (no recalculation)

**Alternatives considered:**
| Approach | Trade-off |
|----------|-----------|
| Count on each request | Simple but expensive at scale |
| Scheduled recalculation | Stale data between runs |

**When to use:** Any time you need counts/aggregates on tables > 100 rows

---

## Files to Reference

| File | Pattern Demonstrated |
|------|---------------------|
| convex/stats.ts | Stats aggregation CRUD |
| convex/eligibilityRules.ts:22-82 | Incremental stats updates |

---

**Next actions:**
1. Run `npx convex run stats:initializeEligibilityStats` to seed initial counts
2. Review `convex/stats.ts` for the full aggregation pattern
```

## Invocation

The user invokes this skill by typing `/learning` after a coding session. The skill should:

1. Review the conversation history and recent file changes
2. Identify the 2-5 most significant technical decisions/patterns
3. Format output according to the structure above
4. Always end with concrete next actions

## Notes

- Keep patterns **shippable** - user can copy-paste and adapt
- Show **one best path** clearly, alternatives as reference
- Be **direct** - no hedging or excessive caveats
- This is for a Solution Architect who values reliability, cost efficiency, and repeatability
