---
name: scout
description: (ePost) Use when you need to "find files", "search the codebase", "locate a pattern", "explore the repo", or "what exists for X" — searches across platforms using RAG and grep
user-invocable: true
context: fork
agent: Explore
metadata:
  argument-hint: "[--fast | --deep] [search query or platform-prefix: query]"
  keywords: [explore, search, find, locate, trace, pattern, architecture, codebase, where-is, which-file, implementation]
  triggers:
    - "where is"
    - "find the"
    - "search for"
    - "which file"
    - "how is X implemented"
    - "trace"
    - "explore"
    - "show me the code"
    - "what does this file do"
  platforms: [web, ios, android, backend]
  agent-affinity: [Explore, epost-planner, epost-researcher, epost-debugger]
  connections:
    uses: [knowledge-retrieval, web-rag, ios-rag]
    enhances: [plan, debug, implementation]
    complementary: [repomix]
---

# Scout — Smart Codebase Explorer

Explore the codebase for files, patterns, architecture insights, and implementations. Auto-detects platform and intelligently routes between RAG (semantic search) and Grep (exact matches) with graceful fallback.

## Flags

| Flag | Behavior |
|------|----------|
| *(none)* | **Auto mode** — smart routing: RAG for semantic queries, Grep for exact matches |
| `--fast` | **Grep only** — no RAG, no external service. Fast, offline-friendly, exact matches |
| `--deep` | **Exhaustive** — RAG + Grep merged, all results returned and ranked |

## Query

<query>$ARGUMENTS</query>

## Step 1: Parse Flags & Query

- Strip `--fast` or `--deep` from `$ARGUMENTS` before processing
- Default mode if no flag: **auto**

## Step 2: Classify Query Intent

- **File location** — "where is X", "find the Y", "which file has Z"
- **Pattern/Implementation** — "how is X implemented", "show me the code for Y", "trace X"
- **Architecture/Structure** — "what does X do", "how does the Y work", "architecture of Z"
- **Dependencies/Relationships** — "what calls X", "where is X used", "dependencies of Y"

## Step 3: Detect Platform(s)

1. **Explicit prefix** — `web:`, `ios:`, `android:`, `backend:` at query start
2. **Query keywords** — "React", "SwiftUI", "Compose", "JAX-RS" → platform inference
3. **Default** — if ambiguous, search all platforms (deduplicate by relevance)

## Step 4: Search Routing

### --fast mode (Grep only)

| Query Type | Tool | Strategy |
|------------|------|----------|
| Filename | Glob | `**/{filename}*` |
| String/symbol | Grep | Literal string match |
| Regex pattern | Grep | Full regex support |
| Platform-specific | Grep + Glob | Filter by extension (.tsx, .swift, .kt, .java) |

### auto mode (Smart routing)

| Intent | Platform | Strategy |
|--------|----------|----------|
| Exact file name | any | Glob/Grep filename |
| Implementation / pattern | **web** | web-rag → fallback Grep |
| Implementation / pattern | **ios** | ios-rag → fallback Grep |
| Implementation / pattern | **android/backend** | Grep only |
| Architecture / design | any | docs/ first → Grep → RAG |
| Dependencies | any | Grep for imports |

### --deep mode (RAG + Grep merged)

Run both RAG semantic search AND Grep, merge and deduplicate results ranked by relevance.

## Step 5: RAG Integration (auto and --deep modes)

1. **Lazy health check** — attempt query, catch errors gracefully
2. **Query construction** — "Find [component/token/pattern] matching [intent]"
3. **Filter extraction** — extract filters from query. Use canonical component names: `web-rag/references/component-mappings.md` or `ios-rag/references/component-mappings.md`
4. **Result limit** — top 10–15 (auto), all available (--deep)
5. **Fallback** — if RAG fails or returns empty, use Grep silently

**Offline fallback**: RAG unavailable → use Grep. Do NOT report RAG failure.

## Step 6: Result Categorization & Synthesis

Group by category:

| Category | Signals |
|----------|---------|
| **Components** | .tsx/.jsx (web), .swift (iOS), .kt (Android), .java (backend) |
| **Logic/Utils** | hooks, helpers, services, utils, managers |
| **Tokens/Config** | design tokens, theme, config, constants |
| **Tests** | .test.ts, .test.swift, Test.kt, *Test.java |
| **Docs** | .md, .mdx files |

Per result: file path (relative) · one-line summary · platform tag · relevance badge

## Step 7: Rank & Report

Rank by: exact filename > same platform > RAG score > match frequency

- **auto/--fast**: top 10 results. If >15, hint: "Run `/scout --deep [query]` for all results"
- **--deep**: all results in sections (Semantic Matches / Exact Matches / By Category)

## Examples

- `/scout auth flow` → auto search all platforms
- `/scout web: Button component` → web-rag semantic for Button
- `/scout ios: navigation` → ios-rag semantic for navigation
- `/scout --fast useAuth` → grep-only, no RAG
- `/scout --fast web: route.ts` → grep for route.ts in web
- `/scout --deep Button` → all Button-related code, RAG + grep merged
- `/scout --deep web: authentication` → exhaustive auth search in web
