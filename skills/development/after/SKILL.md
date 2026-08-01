---
name: after
description: '"Add a new Convex query to get all reviews for a specific user, ordered
  by most recent first, including venue name and average rating for each venue"'
---

# AFTER: Convex Development Skill Test

## Test Prompt (Same as BEFORE)
"Add a new Convex query to get all reviews for a specific user, ordered by most recent first, including venue name and average rating for each venue"

## New State
- Convex skill created at `.claude/skills/convex-development/SKILL.md`
- Frontmatter includes semantic triggers: "Convex queries, mutations, actions, schema"
- Allowed tools scoped to relevant file operations
- Contains extracted patterns from our actual codebase

## Expected Behavior With Skill

### Automatic Activation
Skill should activate when Claude detects:
- Keywords: "Convex", "query", "mutation", "schema"
- File patterns: `convex/*.ts`
- Intent: Writing database functions

### Reduced Context Gathering
1. Skill provides core patterns upfront
2. May still read `schema.ts` for specific table info
3. May read one example file to confirm patterns
4. Skip reading full `convex_rules.txt` (665 lines)

### Pattern Adherence (Expected)
With skill active, Claude should:
- ✅ Use `withIndex` instead of `.filter()`
- ✅ Include explicit `returns` validator
- ✅ Use new function syntax with `handler`
- ✅ Add computed fields (venueName, avgRating)
- ✅ Follow existing code style patterns
- ✅ Use proper type annotations (`Id<"reviews">`)

## Expected Output Quality

### Code Structure
```typescript
export const listByUserWithVenueInfo = query({
  args: { userId: v.id("users") },
  returns: v.array(v.object({
    _id: v.id("reviews"),
    _creationTime: v.number(),
    venueId: v.id("venues"),
    userId: v.id("users"),
    rating: v.number(),
    content: v.string(),
    visitedAt: v.optional(v.number()),
    createdAt: v.number(),
    updatedAt: v.number(),
    venueName: v.string(),        // computed
    venueType: v.string(),        // computed
    venueAvgRating: v.number(),   // computed
  })),
  handler: async (ctx, args) => {
    const reviews = await ctx.db
      .query("reviews")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();

    const result = [];
    for (const review of reviews) {
      const venue = await ctx.db.get(review.venueId);
      if (!venue) continue;

      // Calculate venue's average rating
      const venueReviews = await ctx.db
        .query("reviews")
        .withIndex("by_venue", (q) => q.eq("venueId", review.venueId))
        .collect();
      const avgRating = venueReviews.length > 0
        ? venueReviews.reduce((sum, r) => sum + r.rating, 0) / venueReviews.length
        : 0;

      result.push({
        ...review,
        venueName: venue.name,
        venueType: venue.type,
        venueAvgRating: Math.round(avgRating * 10) / 10,
      });
    }
    return result;
  },
});
```

## Improved Metrics

| Metric | Before | After |
|--------|--------|-------|
| Files read before writing | 3-4 | 1-2 (schema for confirmation) |
| Pattern adherence | Medium | High |
| Automatic activation | No | Yes (semantic matching) |
| Context overhead | High (665 lines) | Low (~150 lines skill) |
| Consistency with codebase | Variable | Consistent |

## Skill Benefits

1. **Focused Context**: Only relevant patterns, not entire rules file
2. **Semantic Activation**: Triggers on Convex-related prompts automatically
3. **Consistency**: Patterns extracted from actual codebase ensure style match
4. **Efficiency**: Less file reading, faster response
5. **Anti-Patterns Listed**: Explicit warnings about common mistakes

## Measurement Criteria

To validate improvement:
1. Count tool calls (fewer = better)
2. Check output matches existing patterns
3. Verify all validators present
4. Confirm index usage over filter
5. Check computed fields included

## Notes
This documents the expected state AFTER implementing the Convex skill.
The skill should significantly improve Convex function generation quality.
