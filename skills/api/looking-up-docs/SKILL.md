---
name: looking-up-docs
description: Library documentation via Context7. Use for API references, code examples, framework docs.
allowed-tools:
  - Read
  - Grep
  - Glob
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
---

# Documentation Lookup with Context7

Context7 provides up-to-date, version-specific documentation and code examples directly from source libraries.

## Why Context7

- **Current APIs**: No hallucinated or outdated patterns
- **Version-specific**: Gets docs for exact library versions
- **Code examples**: Real, working code from actual documentation

## Workflow

1. **Resolve library ID**: `mcp__context7__resolve-library-id` with `libraryName`
2. **Get documentation**: `mcp__context7__query-docs` with `context7CompatibleLibraryID` and `topic`

## Modes

| Mode   | Use For                                    |
| ------ | ------------------------------------------ |
| `code` | API references, code examples (default)    |
| `info` | Conceptual guides, architecture, tutorials |

## Examples

```
# React hooks
resolve-library-id: "react"
get-library-docs: context7CompatibleLibraryID="/facebook/react", topic="hooks", mode="code"

# Next.js middleware
resolve-library-id: "next.js"
get-library-docs: context7CompatibleLibraryID="/vercel/next.js", topic="middleware"

# Go net/http
resolve-library-id: "go net/http"
get-library-docs: context7CompatibleLibraryID="/golang/go", topic="http server"

# Kubernetes API
resolve-library-id: "kubernetes"
get-library-docs: context7CompatibleLibraryID="/kubernetes/kubernetes", topic="deployment"
```

## Tips for Better Results

**Be specific with queries:**

- BAD: `topic="hooks"` → returns everything hook-related
- GOOD: `topic="useEffect cleanup function"` → precise results

**Filter strategies:**

- Use `topic` with function/method names: `topic="json.Unmarshal"`
- Include version when relevant: `libraryName="react 18"`
- Combine with feature context: `topic="middleware error handling"`

**When results are too broad:**

1. Narrow the `topic` parameter
2. Try `mode="code"` to focus on examples
3. Paginate: `page=2`, `page=3` for additional results
4. Re-resolve library ID with more specific name

**Quality check:**

- Verify code examples match your library version
- Cross-reference with official docs if uncertain

## Fallback: Empty or Missing Results

When Context7 returns no results or doesn't have the library:

### Decision Tree

```
Context7 query returns empty?
├── Try broader query (e.g., "hooks" instead of "useCallback")
├── Still empty?
│   ├── Re-resolve library ID with alternative name
│   │   (e.g., "nextjs" → "next.js", "golang" → "go")
│   └── Still empty?
│       ├── Library not indexed → Use fallbacks below
│       └── Very niche library → WebSearch for official docs
```

### Fallback Strategies

1. **Alternative library ID**: Try variations

   ```
   # If "fastapi" fails, try:
   resolve-library-id: "starlette"  # FastAPI's underlying framework
   resolve-library-id: "pydantic"   # Often used with FastAPI
   ```

2. **WebSearch for official docs**:

   ```
   WebSearch: "<library> official documentation <feature>"
   WebFetch: Official docs URL → extract relevant info
   ```

3. **Source code exploration** (for open-source):

   ```
   # Clone and explore
   git clone --depth=1 <repo>
   Grep: "function <name>" --type=<lang>
   ```

4. **Perplexity for recent/niche libraries**:
   ```
   mcp__perplexity-ask__perplexity_ask: "How to use <feature> in <library> 2024"
   ```

### Libraries Commonly Not in Context7

| Library              | Fallback                    |
| -------------------- | --------------------------- |
| Internal/proprietary | Source code + README        |
| Very new (<6 months) | WebSearch + official docs   |
| Niche/specialized    | Perplexity or GitHub issues |
| Language stdlib      | Use language docs directly  |

### Example Fallback Flow

```
# Initial attempt fails
resolve-library-id: "htmx"
→ No results

# Fallback 1: WebSearch
WebSearch: "htmx documentation hx-swap"
→ Found: https://htmx.org/docs/

# Fallback 2: Fetch docs
WebFetch: url="https://htmx.org/docs/", prompt="Explain hx-swap attribute"
→ Returns relevant documentation
```

### When to Skip Context7 Entirely

- Asking about breaking changes between versions → WebSearch release notes
- Debugging specific error messages → WebSearch + StackOverflow
- Comparing libraries → Perplexity for analysis
- Very recent features → WebSearch for latest docs
