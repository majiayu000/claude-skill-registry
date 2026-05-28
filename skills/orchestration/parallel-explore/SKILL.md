---
name: parallel-explore
description: "Guides parallel exploration of multiple implementation approaches using git worktrees. Use when facing decisions with multiple valid paths. Triggers on: explore options, compare approaches, parallel exploration."
---

# Parallel Exploration Skill

Guide the process of exploring multiple implementation approaches simultaneously using git worktrees.

---

## The Job

1. Identify when parallel exploration would be valuable
2. Define distinct approaches to explore
3. Create isolated worktrees for each approach
4. Execute exploration in parallel
5. Evaluate and compare results
6. Merge the best solution

---

## When to Use Parallel Exploration

### Good Candidates

- **Architecture decisions** - Different patterns (e.g., microservices vs monolith)
- **Library selection** - Comparing similar libraries hands-on
- **Algorithm choices** - Different approaches to the same problem
- **API design** - Different interface designs
- **Performance optimization** - Multiple optimization strategies

### Not Worth Parallelizing

- Simple, clear-cut decisions
- Tasks with obvious single approach
- Very small changes
- Changes that don't warrant the overhead

---

## Exploration Process

### Step 1: Identify the Decision Point

When you encounter a significant decision:

```markdown
## Decision Point Identified

**Question:** [What needs to be decided]
**Context:** [Why this matters]
**Approaches to Explore:**
1. [Approach A] - [Brief description]
2. [Approach B] - [Brief description]
3. [Approach C] - [Brief description]

**Exploration Value:** [Why parallel exploration helps here]
```

### Step 2: Start Exploration

Use the parallel explorer script:

```bash
./scripts/aha-loop/parallel-explorer.sh explore "task description" --approaches "approach1,approach2,approach3"
```

Or let AI suggest approaches:

```bash
./scripts/aha-loop/parallel-explorer.sh explore "task description"
# AI will suggest approaches automatically
```

### Step 3: Work in Each Worktree

In each worktree, the AI should:

1. **Implement fully** - Not just a stub, but working code
2. **Write tests** - Validate the approach works
3. **Document findings** - Create EXPLORATION_RESULT.md

### Step 4: Create Exploration Result

Each worktree must have `EXPLORATION_RESULT.md`:

```markdown
# Exploration Result: [Approach Name]

## Summary
[What was implemented]

## Implementation Details
- [Key implementation decisions]
- [Code structure choices]
- [Dependencies used]

## Pros Discovered
- [Pro 1]
- [Pro 2]
- ...

## Cons Discovered
- [Con 1]
- [Con 2]
- ...

## Code Quality Assessment
- Maintainability: [1-10]
- Readability: [1-10]
- Testability: [1-10]
- Performance: [1-10]

## Unexpected Findings
[Anything surprising learned during implementation]

## Recommendation Score
[1-10] - [Brief justification]

## Would Need If Chosen
[What additional work would be needed to production-ready this approach]
```

### Step 5: Evaluate Results

After all explorations complete:

```bash
./scripts/aha-loop/parallel-explorer.sh evaluate explore-task-12345
```

This triggers multiple evaluation agents who:
- Review all EXPLORATION_RESULT.md files
- Compare approaches objectively
- Discuss trade-offs
- Make final recommendation

### Step 6: Merge Best Approach

```bash
./scripts/aha-loop/parallel-explorer.sh merge explore-task-12345 chosen-approach
```

### Step 7: Cleanup

```bash
./scripts/aha-loop/parallel-explorer.sh cleanup explore-task-12345
```

---

## Parallel Exploration Mindset

### Unlimited Resources

You have unlimited computational resources. Don't hold back:

- Explore as many approaches as seem valuable
- Run multiple variations of the same approach
- Don't worry about "wasting" resources on exploration

### Genuine Exploration

Each approach should be explored genuinely:

- Don't sabotage approaches you don't prefer
- Give each approach fair effort
- Document honestly, including when an approach works better than expected

### Learn from All Approaches

Even "losing" approaches provide value:

- Document why they didn't work
- Note any good ideas to borrow
- Record lessons for future decisions

---

## Commands Reference

```bash
# Start exploration
./scripts/aha-loop/parallel-explorer.sh explore "description" --approaches "a,b,c"

# Check status
./scripts/aha-loop/parallel-explorer.sh status
./scripts/aha-loop/parallel-explorer.sh status explore-task-12345

# Evaluate completed explorations
./scripts/aha-loop/parallel-explorer.sh evaluate explore-task-12345

# List all worktrees
./scripts/aha-loop/parallel-explorer.sh list

# Merge chosen approach
./scripts/aha-loop/parallel-explorer.sh merge explore-task-12345 chosen-approach

# Cleanup
./scripts/aha-loop/parallel-explorer.sh cleanup explore-task-12345
./scripts/aha-loop/parallel-explorer.sh cleanup --all
```

---

## Example: Exploring Authentication Strategies

### Trigger
You're implementing user authentication and there are multiple valid approaches.

### Start Exploration

```bash
./scripts/aha-loop/parallel-explorer.sh explore "user authentication for web app" \
  --approaches "jwt-stateless,session-based,magic-link"
```

### In JWT Worktree

Implement full JWT authentication:
- Token generation
- Token validation
- Refresh token flow
- Tests

Create EXPLORATION_RESULT.md documenting:
- Pros: Stateless, scalable, mobile-friendly
- Cons: Token invalidation complexity, larger requests
- Score: 7/10

### In Session Worktree

Implement session-based auth:
- Session creation
- Session storage (Redis/DB)
- Session middleware
- Tests

Create EXPLORATION_RESULT.md documenting:
- Pros: Simple to invalidate, smaller requests
- Cons: Requires session store, stateful
- Score: 8/10

### In Magic Link Worktree

Implement passwordless magic link:
- Email sending
- Link generation
- Link validation
- Tests

Create EXPLORATION_RESULT.md documenting:
- Pros: No password to manage, good UX
- Cons: Email dependency, potential delays
- Score: 6/10

### Evaluate

Multiple evaluation agents review all three approaches and produce:
- Comparison table
- Final recommendation (session-based for simplicity)
- Suggestion to borrow JWT's token rotation idea

### Merge

```bash
./scripts/aha-loop/parallel-explorer.sh merge explore-auth-12345 session-based
```

---

## Nested Exploration

During exploration, you may discover new decision points. You can:

1. **Defer** - Note it for later, continue with current exploration
2. **Nest** - Start a sub-exploration within the worktree

For nested exploration, create a sub-directory:
```
.worktrees/
  explore-auth-12345/
    jwt/
      .worktrees/          # Nested exploration
        explore-refresh-67890/
          rotating-tokens/
          sliding-window/
```

---

## Integration with Observability

Log exploration decisions to `logs/ai-thoughts.md`:

```markdown
## 2026-01-29 14:00:00 | Task: PRD-003 | Phase: Exploration

### Decision Point
Authentication strategy needs to be determined.

### Approaches Being Explored
1. JWT (stateless)
2. Session-based (stateful)
3. Magic link (passwordless)

### Exploration Status
Started parallel exploration: explore-auth-12345

### Expected Outcome
Will evaluate all three and merge best approach.
```

---

## Checklist

Before starting exploration:
- [ ] Decision point clearly identified
- [ ] Multiple valid approaches exist
- [ ] Approaches are meaningfully different
- [ ] Exploration effort is justified

During exploration:
- [ ] Each approach implemented genuinely
- [ ] Tests written for each
- [ ] EXPLORATION_RESULT.md created

After exploration:
- [ ] All approaches evaluated fairly
- [ ] Final recommendation documented
- [ ] Best approach merged
- [ ] Worktrees cleaned up
