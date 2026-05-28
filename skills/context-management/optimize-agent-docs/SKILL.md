---
name: optimize-agent-docs
description: Build a retrieval-optimized knowledge layer over agent documentation in dotfiles (.claude, .codex, .cursor, .aider). Use when asked to "optimize docs", "improve agent knowledge", "make docs more efficient", or when documentation has accumulated and retrieval feels inefficient. Generates a manifest mapping task-contexts to knowledge chunks, optimizes information density, and creates compiled artifacts for efficient agent consumption.
---

# Agent Knowledge Optimizer

Transform accumulated documentation into a retrieval-optimized knowledge system.

## Core Principle

File organization is a human concern. Agents don't browse—they search and load. Optimize for:
- **Discovery**: What knowledge exists?
- **Relevance**: Is it needed for this task?
- **Efficiency**: What's the minimum to load?

## Workflow

### Phase 1: Knowledge Extraction

Inventory all agent documentation:

```bash
# Find all agent doc sources
find . -maxdepth 2 -name "*.md" -path "*/.claude/*" -o \
       -name "*.md" -path "*/.codex/*" -o \
       -name "*.md" -path "*/.cursor/*" -o \
       -name "CLAUDE.md" -o -name "AGENTS.md" -o -name "INSTRUCTIONS.md"
```

For each file, extract:
- Discrete facts (single pieces of actionable information)
- Instructions (procedures, rules, constraints)
- Context triggers (when is this knowledge needed?)

### Phase 2: Chunk Analysis

Break content into **retrieval units**—the smallest self-contained piece of information that makes sense alone.

Good chunk:
```
## Adding API Endpoints
1. Create handler in src/handlers/
2. Register route in src/routes.rs
3. Add OpenAPI spec to docs/api.yaml
```

Bad chunk (too coupled):
```
See the API section for endpoint patterns, but first read the auth docs,
which reference the middleware guide...
```

Score each chunk:
- **Self-contained?** Can agent act on this without loading more?
- **Task-specific?** Clear when this is needed?
- **Information-dense?** High signal per token?

### Phase 3: Build Knowledge Manifest

Generate `.claude/KNOWLEDGE.md`—a lightweight index the agent reads first:

```markdown
# Knowledge Manifest

## Task → Knowledge Map

| When working on... | Load | Key terms |
|-------------------|------|-----------|
| API endpoints | references/api.md | route, handler, endpoint |
| Authentication | references/auth.md | token, session, login |
| Database changes | references/schema.md | migration, model, query |
| Testing | references/testing.md | spec, fixture, mock |
| Deployment | references/deploy.md | release, staging, prod |

## Quick Reference

### Build Commands
- `npm run dev` — Start dev server (port 3000)
- `npm test` — Run test suite
- `npm run build` — Production build

### Key Paths
- Handlers: `src/handlers/`
- Routes: `src/routes.ts`
- Tests: `tests/`

### Critical Rules
- Never commit .env files
- All PRs require tests
- Use conventional commits
```

The manifest contains:
1. **Task→Knowledge map**: What to load for what context
2. **Quick reference**: High-frequency facts (no file loading needed)
3. **Critical rules**: Must-know constraints (always relevant)

### Phase 4: Compile Optimized Artifacts

Transform verbose source docs into dense, agent-optimized versions.

**Compression techniques:**

| Source (verbose) | Compiled (dense) |
|-----------------|------------------|
| "When you want to add a new endpoint, you should first create a handler function..." | `New endpoint: handler → route → spec` |
| Long prose paragraphs | Structured tables |
| Repeated information | Single source of truth |
| Examples with explanation | Just the pattern |

**Output structure:**

```
.claude/
├── CLAUDE.md              # Human-readable, can stay verbose
├── KNOWLEDGE.md           # Agent manifest (generated)
└── compiled/              # Agent-optimized versions (generated)
    ├── api.md             # Dense API reference
    ├── patterns.md        # Code patterns as templates
    └── rules.md           # All constraints in one place
```

### Phase 5: Generate Retrieval Hints

Add grep-friendly markers throughout compiled docs:

```markdown
<!-- @task:new-endpoint @load:api,routes -->
## Adding Endpoints

<!-- @task:fix-auth @load:auth,middleware -->
## Authentication Flow

<!-- @task:write-test @load:testing -->
## Test Patterns
```

These markers enable:
```bash
# Find relevant sections for a task
grep -l "@task:new-endpoint" .claude/compiled/*.md
```

### Phase 6: Validation

Test the optimized system:

1. **Coverage check**: Every fact from source exists in compiled output
2. **Retrieval test**: Can common tasks be served with minimal loading?
3. **Density check**: Compiled versions smaller than sources?

```bash
# Compare sizes
wc -l .claude/references/*.md    # Source
wc -l .claude/compiled/*.md       # Compiled (should be smaller)
```

## Manifest Format

The `KNOWLEDGE.md` manifest follows this structure:

```markdown
# Knowledge Manifest
<!-- Auto-generated. Source: .claude/references/, CLAUDE.md -->

## Task Context Map
<!-- What to load based on current work -->

| Context | Load | Search |
|---------|------|--------|
| [task description] | [file path] | [grep terms] |

## Always-Loaded Facts
<!-- High-frequency, never needs file lookup -->

### Commands
[Most-used commands as a table]

### Paths
[Key directories and their purposes]

### Rules
[Critical constraints that always apply]

## Chunk Index
<!-- What exists and where -->

| Topic | Location | Lines | Summary |
|-------|----------|-------|---------|
| [topic] | [file:line-range] | [count] | [one-line summary] |
```

## Information Density Principles

### Convert Prose to Structure

Before:
> "The authentication system uses JWT tokens stored in httpOnly cookies.
> When a user logs in, the server validates credentials against the database,
> generates a token with a 24-hour expiry, and sets it as a cookie..."

After:
```
## Auth Flow
- Method: JWT in httpOnly cookie
- Expiry: 24h
- Flow: credentials → DB validate → token → cookie
```

### Eliminate Redundancy

If the same information appears in multiple places, create one canonical source and reference it:

```markdown
## Token Handling
See: [Auth Flow](#auth-flow) — tokens section
```

### Prefer Tables Over Lists

Before:
```markdown
- The API endpoint for users is /api/users
- The API endpoint for posts is /api/posts
- The API endpoint for comments is /api/comments
```

After:
```markdown
| Resource | Endpoint |
|----------|----------|
| Users | /api/users |
| Posts | /api/posts |
| Comments | /api/comments |
```

### Use Patterns Over Examples

Before:
```markdown
To create a user handler:
```javascript
export async function createUser(req, res) {
  const { name, email } = req.body;
  const user = await db.users.create({ name, email });
  res.json(user);
}
```

After:
```markdown
Handler pattern: `export async function {action}{Resource}(req, res)`
Body: Extract params → DB operation → Return result
```

## Output Checklist

After optimization, verify:

- [ ] `KNOWLEDGE.md` exists and is under 100 lines
- [ ] Task→knowledge mappings cover common workflows
- [ ] Quick reference has most-used facts
- [ ] Compiled docs are denser than sources
- [ ] No orphaned knowledge (everything indexed)
- [ ] Retrieval hints enable grep-based discovery
- [ ] Original source docs untouched (human reference)
