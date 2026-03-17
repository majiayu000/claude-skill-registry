---
name: osgrep
description: Semantic code search using natural language queries. Use when users ask "where is X implemented", "how does Y work", "find the logic for Z", or need to locate code by concept rather than exact text. Returns file paths with line numbers and code snippets.
allowed-tools: "Bash(osgrep:*), Read"
license: Apache-2.0
---

## When to Use

Use this to find code by **concept** or **behavior** (e.g., "where is auth validated", "how are plugins loaded").
_Note: This tool prioritizes finding the right files and locations in the code. Snippets are truncated (max 16 lines) and are often just previews._

Example:

```bash
osgrep "how are plugins loaded"
osgrep "how are plugins loaded" packages/transformers.js/src
```

## Strategy for Different Query Types

### For **Architectural/System-Level Questions** (auth, LSP integration, file watching)

1. **Search Broadly First:** Use a conceptual query to map the landscape.
   - `osgrep "authentication authorization checks"`
2. **Survey the Results:** Look for patterns across multiple files:
   - Are checks in middleware? Decorators? Multiple services?
   - Do file paths suggest different layers (gateway, handlers, utils)?
3. **Read Strategically:** Pick 2-4 files that represent different aspects:
   - Read the main entry point
   - Read representative middleware/util files
   - Follow imports if architecture is unclear
4. **Refine with Specific Searches:** If one aspect is unclear:
   - `osgrep "session validation logic"`
   - `osgrep "API authentication middleware"`

### For **Targeted Implementation Details** (specific function, algorithm)

1. **Search Specifically:** Ask about the precise logic.
   - `osgrep "logic for merging user and default configuration"`
2. **Evaluate the Semantic Match:**
   - Does the snippet look relevant?
   - **Crucial:** If it ends in `...` or cuts off mid-logic, **read the file**.
3. **One Search, One Read:** Use osgrep to pinpoint the best file, then read it fully.

## Hybrid Search Strategy (Semantic + Grep)

Combining semantic search with grep is 31% more effective than either alone.

**Decision Heuristic:**

- **osgrep**: Exploration. You don't know exact names/patterns.
- **rg (ripgrep)**: Precision. You know the symbol/pattern to find.

**Two-Stage Workflow:**

1. **Discover with osgrep**: Find the right files conceptually

   - `osgrep "authentication validation logic"`
   - → Returns `src/auth/middleware.ts:45`, `src/utils/jwt.ts:12`

2. **Pinpoint with ripgrep**: Find exact matches in those files
   - `rg "verifyToken|validateJWT" src/auth/ src/utils/`
   - → Returns exact line numbers with context

**Example: Finding rate limiting implementation**

```bash
# Step 1: Conceptual discovery
osgrep "rate limiting throttling"
# → src/middleware/rateLimit.ts:23, src/api/limiter.ts:8

# Step 2: Exact symbols/patterns
rg "RateLimiter|throttle" src/middleware/ src/api/
```

**Why this works:** Semantic search narrows to the right files. Grep pinpoints exact locations within those files. Together = faster, more accurate results.

## Output Format

Returns: `path/to/file:line [Tags] Code Snippet`

Example:

```
ORCHESTRATION src/auth/handler.ts:45
Defines: handleAuth | Calls: validate, checkRole, respond | Score: .94

export async function handleAuth(req: Request) {
  const token = req.headers.get("Authorization");
  ...
```

**Tags:**

- `ORCHESTRATION`: Contains logic, coordinates other code. Prioritize these.
- `DEFINITION`: Types, interfaces, classes.

**Metadata:**

- `Defines`: What this code defines
- `Calls`: What this code calls (helps trace flow)
- `Score`: Relevance (1 = best match)

**Markers:**

- `...`: Truncation marker. Snippet is incomplete—use `Read` for full context.

## Other Commands

```bash
# Trace call graph (who calls X, what X calls)
osgrep trace handleAuth

# Skeleton of a huge file (find which ranges to read)
osgrep skeleton src/giant-2000-line-file.ts

# Just file paths when you only need locations
osgrep "authentication" --compact
```

## Tips

- **More Words = Better:** "auth" is vague. "where does the server validate JWT tokens" is specific.
- **Prioritize ORCH Results:** ORCHESTRATION results contain the logic—start there.
- **Trust the Semantics:** You don't need exact names. `osgrep "how does the server start"` works better than guessing `osgrep "server.init"`.
- **Watch for Distributed Patterns:** If results span 5+ files in different directories, the feature is likely architectural—survey before diving deep.
- **Scope When Possible:** Use path constraints to focus: `osgrep "auth" src/server/`
- **Use Line Ranges:** Don't read entire files. Use the line ranges osgrep gives you.
- **Rephrase If Needed:** If results seem off, rephrase your query like you'd ask a teammate.

## If Index is Building

If you see "Indexing", "Building", or "Syncing": STOP. Alert the user that the index is building. Ask if they want to wait or proceed with partial results.
