---
name: explain
description: Use when user invokes /explain with a file path, directory path, function/class name, or natural language concept. Also triggers on "explain this", "how does X work", "walk me through". Produces a structured, layered explanation of what the code does, how it connects, and where to start if you need to change it. Do NOT use when the user wants to trace data flow through a pipeline — use /lineage instead.
---

# Structured Code Explainer

## Overview

Produce layered explanations of code — files, directories, functions, classes, or cross-cutting concepts. Designed for developers working in unfamiliar parts of a codebase.

**Core principles:**
1. **Adaptive depth.** A single function gets a focused deep-dive. A directory gets a map first, then the user picks where to zoom.
2. **Project-aware.** If the project has a CLAUDE.md, reference its Architecture section to ground explanations in the project's own terminology.
3. **Conversation output.** Explanations go to the conversation, not files. The user can ask to save if they want.

## When to Use

User types `/explain` followed by:
- **File path** → explain that file
- **Directory path** → map the directory structure, then explain key components
- **Function or class name** → find the definition, explain it in context
- **Natural language concept** → search the codebase for relevant files and explain the concept/flow

## Invocation Examples

```
/explain src/auth/middleware.ts
/explain the payment processing flow
/explain src/services/
/explain OrderProcessor.process
/explain how webhooks get dispatched
```

## Workflow Order (MANDATORY)

**You MUST follow this order. No skipping steps.**

---

### Step 1: Parse Input

Classify the argument:

| Type | Detection | Example |
|------|-----------|---------|
| File path | Has file extension or resolves to a file | `src/auth/middleware.ts` |
| Directory path | Resolves to a directory (or ends with `/`) | `src/services/` |
| Symbol name | Looks like a function, class, or method (CamelCase, dot notation, `::`) | `OrderProcessor.process` |
| Concept | Natural language, doesn't resolve to a file or directory | `the payment processing flow` |

If ambiguous (e.g., `auth` could be a directory or a concept), check the filesystem first. If it resolves to a file or directory, treat it as that. Otherwise, treat it as a concept.

---

### Step 2: Gather Context

**For a file path:**
1. Read the target file
2. Identify imports/dependencies — read the most important ones (up to 5 files)
3. Search for callers — search for the filename or its key exports across source files in the codebase (filter to relevant file types like `*.ts`, `*.py`, `*.go`, etc. to avoid noise from docs, tests, and build output)
4. Limit total files read to ~10 to stay focused

**For a directory path:**
1. List the directory contents (recursive, 2 levels deep max for the initial map)
2. Read the directory's README, index file, or entry point if one exists
3. Identify the top 3-5 most important files by name/convention (entry points, main modules, routers, handlers)
4. Read those key files
5. Do NOT read every file — present the map and let the user pick what to zoom into

**For a symbol name:**
1. Search for the definition — look for patterns like `function symbolName`, `class SymbolName`, `def symbol_name`, `func symbolName` (adjust for the project's language). Filter to source file types.
2. Read the containing file
3. Search for callers — search for the symbol name across source files, excluding the definition file. Filter to relevant source file types (not docs, tests, or build output) to avoid noise.
4. Read the top 2-3 callers for context

**For a concept:**
1. Extract keywords from the natural language description
2. Search the codebase for those keywords, filtering to relevant source file types
3. Read the top 5-8 most relevant files (prioritize by match density)
4. If too many matches, narrow by directory or file type before reading

---

### Step 3: Check for CLAUDE.md

Look for project-level CLAUDE.md in the repository root:
1. Check for `CLAUDE.md` in the working directory or its parent directories
2. If found, read the **Architecture** section (if present)
3. Use this to ground explanations in the project's own terminology, patterns, and conventions
4. Reference it when explaining how a component fits into the larger system

If no CLAUDE.md exists, proceed without it — this step is additive, not blocking.

---

### Step 4: Analyze Scope

Before producing the explanation, determine what scope is appropriate:

- **Narrow scope** (single function/class): produce the full 6-section explanation directly
- **Medium scope** (single file): produce the full 6-section explanation, with Key Components listing the file's functions/classes
- **Wide scope** (directory or concept): produce a **map first**, then offer to deep-dive
  - The map includes: purpose of the directory/subsystem, list of components with one-line descriptions, and how they relate
  - Ask: "Want me to go deeper on any of these?"

---

### Step 5: Produce Explanation

Use this structure. Every section is required for narrow/medium scope. For wide scope, produce the map version (see Step 4).

---

#### Output Structure

**1. Summary** (2-3 sentences)

What this code does and why it exists. Lead with purpose, not implementation details.

**2. Key Components**

The important pieces — functions, classes, modules, config — with one-line descriptions. Use a table or bullet list:

```
- `authenticate()` — validates JWT token from Authorization header, attaches user to request context
- `requireRole(role)` — middleware factory that checks user.role against the required role
- `rateLimiter` — token bucket rate limiter, configured per-route in config.yml
```

**3. How It Connects**

What calls this code, what this code calls, and how data flows in and out. Be specific about entry points and dependencies:

```
Called by:
  - Express router (src/routes/api.ts:14) — applied to all /api/* routes

Calls:
  - UserService.findById() — to hydrate user from token claims
  - config.get('auth.jwtSecret') — for token verification

Data flow:
  - IN: Authorization header (Bearer token)
  - OUT: req.user object attached to request, or 401 response
```

**4. Patterns & Conventions**

Design patterns used, naming conventions, framework idioms. Only include patterns that are actually present — don't list patterns that aren't used.

Examples: middleware chain pattern, repository pattern, dependency injection, event-driven, pub-sub, factory pattern, decorator pattern.

**5. Gotchas**

Non-obvious behavior, edge cases, known issues, things that will bite you. If there are no gotchas, say "None identified" rather than inventing them.

Examples:
- "Token expiry is checked but refresh tokens are not — sessions expire hard after 1 hour"
- "The rate limiter shares state across workers via Redis, but falls back to in-memory if Redis is down (no warning logged)"
- "Column names in the SQL query don't match the ORM model — the raw query uses snake_case but the model expects camelCase"

**6. Entry Points for Change**

If you need to modify this code, where to start and what to watch out for. Be practical:

```
- To add a new auth provider: implement the AuthProvider interface in src/auth/providers/,
  register it in src/auth/registry.ts
- To change token expiry: update config.yml (auth.tokenExpiry), but note that existing
  tokens will still use their original expiry
- To add rate limit exemptions: add the route pattern to rateLimiter.exemptions in config.yml
```

---

### Step 6: Offer Follow-Up

End with: **"Want me to go deeper on any section, or explain a related part of the codebase?"**

For wide-scope explanations (directories/concepts), be more specific: list the components you can deep-dive into.

---

## Adaptive Behavior

### Small target (single function, < 50 lines)
- Full 6-section output
- Include the actual code inline if it's short enough (< 30 lines)
- Focus on context — why does this function exist, what relies on it

### Medium target (single file, 50-500 lines)
- Full 6-section output
- Key Components lists the file's main exports/classes/functions
- Don't include full code — reference line numbers

### Large target (directory, multi-file concept)
- Map first: purpose + component list + relationships
- Offer to deep-dive on specific components
- If the user doesn't specify, pick the most important 2-3 and explain those

### Very large target (entire project, "explain everything")
- Start with architecture overview based on directory structure
- Highlight entry points, key abstractions, and data flow
- Offer a suggested reading order for understanding the codebase

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reading every file in a directory | Read the map (ls), identify key files, read those. Offer to go deeper. |
| Inventing gotchas that aren't real | Only list gotchas you actually observed in the code. "None identified" is fine. |
| Generic patterns section | Only list patterns that are concretely present in the code. Skip if nothing notable. |
| Ignoring CLAUDE.md | If it exists, use its Architecture section to contextualize the explanation. |
| Wall of text with no structure | Always use the 6-section structure. Use code blocks, tables, and bullet lists. |
| Explaining language basics | Assume the reader knows the programming language. Explain the code's purpose and design, not syntax. |
| Not searching for callers | "How It Connects" requires knowing what calls this code. Always search for callers. |
| Dumping raw search output | Synthesize search results into a coherent explanation. The user wants understanding, not search results. |
