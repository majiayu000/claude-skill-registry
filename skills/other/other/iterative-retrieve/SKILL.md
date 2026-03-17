---
name: iterative-retrieve
description: 4-phase context retrieval protocol for subagents — Dispatch, Evaluate, Refine, Loop
disable-model-invocation: true
---

# Iterative Retrieval Protocol

When dispatching subagents that need codebase context, use this 4-phase loop (max 3 cycles) to ensure they find the right files.

## The Problem

Single-pass searches miss codebase-specific terminology. Example: searching "rate limiting" finds nothing because BrickTrack calls it `rate-limit.ts` in `src/server/middleware/`. Cycle 2 discovers "middleware" and "throttle" as related terms.

## The Protocol

### Phase 1: DISPATCH (Broad Search)

Search with multiple keyword variants and broad glob patterns:

- Glob: `src/**/*.ts` matching `*keyword*`
- Grep: `keyword1|keyword2|keyword3` across `src/`
- Include: type definitions, interfaces, barrel exports
- Exclude: `*.test.ts`, `*.spec.ts`, `node_modules`

### Phase 2: EVALUATE (Score Relevance)

For each file found, assign a relevance score:

| Score | Meaning | Action |
|-------|---------|--------|
| 0.8-1.0 | Directly implements target functionality | READ fully |
| 0.5-0.7 | Contains related patterns, types, or imports | SCAN for vocabulary |
| 0.2-0.4 | Tangentially related | NOTE terminology only |
| 0-0.2 | Not relevant | EXCLUDE from future searches |

After scoring, identify: **What context is STILL MISSING?**

### Phase 3: REFINE (Update Search)

Based on Phase 2 findings:
- Add new keywords discovered from high-scoring files
- Add codebase-specific terminology (e.g., `uow` instead of "unit of work")
- Narrow glob patterns to confirmed-relevant directories
- Exclude confirmed-irrelevant paths

### Phase 4: LOOP (Repeat or Stop)

**Stop when:**
- 3+ files scored >= 0.7 AND no critical context gaps remain
- OR: 3 cycles completed (proceed with best available)

**Continue when:**
- Fewer than 3 high-relevance files found
- Critical vocabulary gaps remain

## BrickTrack-Specific Vocabulary

Common vocabulary mismatches in this codebase:
- "auth" -> BetterAuth, `getAuthSession()`, `authClient`
- "database" -> Drizzle ORM, `ctx.db`, `ctx.uow.repo`
- "api" -> tRPC routers in `src/server/routers/`
- "components" -> `src/components/my/` (app) vs `src/components/ui/` (shadcn)
- "middleware" -> `src/server/middleware/` (rate-limit, auth)
- "types" -> `src/types/` + `z.infer<typeof schema>` inline

## Adding to Subagent Prompts

Include this in PROMPT.md for implementation subagents:

```
Before implementing, locate all relevant files using iterative retrieval:
1. DISPATCH: Broad Glob + Grep (multiple keyword variants)
2. EVALUATE: Score each file 0-1 for relevance
3. REFINE: Adjust terms based on codebase vocabulary discovered
4. LOOP: Up to 3 cycles until 3+ files scored >= 0.7
Do NOT assume file names — search first.
```
