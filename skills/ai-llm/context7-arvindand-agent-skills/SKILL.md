---
name: context7
description: "Fetch up-to-date library documentation via Context7 REST API. Use when needing current API docs, framework patterns, or code examples for any library. Use when user asks about React, Next.js, Prisma, Express, Vue, Angular, Svelte, or any npm/PyPI package. Use when user says 'how do I use X library', 'what's the API for Y', or needs official documentation. Lightweight alternative to Context7 MCP with no persistent context overhead."
allowed-tools: Bash(python:*)
---

# Context7 Documentation Lookup Skill

Fetch current library documentation, API references, and code examples without MCP context overhead.

**Works on all platforms via REST API.**

## When to Use

**Activate automatically when:**

- User asks about library APIs or framework patterns
- User requests code generation using specific libraries/frameworks
- Import statements suggest documentation needs: `import`, `require`, `from`
- Questions about specific library versions or migration
- Need for official documentation patterns vs generic solutions
- Setting up or configuring third-party tools
- "How do I use X library?", "What's the API for Y?"

**Examples:**

- "Create Next.js middleware with authentication" → Use context7
- "Set up Prisma with PostgreSQL" → Use context7
- "Implement Supabase authentication" → Use context7

## Workflow

### Quick Start (If You Know the Library)

**Skip the search** when you already know the library:

```bash
scripts/context7.py docs "/vercel/next.js" "middleware authentication"
```

Common library IDs:

- React: `/facebook/react`
- Next.js: `/vercel/next.js`
- Prisma: `/prisma/prisma`
- Supabase: `/supabase/supabase`
- Express: `/expressjs/express`

### Full Workflow

#### Step 1: Search for Library ID (if unknown)

Search first to get the correct library ID:

```bash
scripts/context7.py search "library-name"
```

Example output shows library IDs you can use:

```txt
ID: /facebook/react
Name: React
Snippets: 2135 | Score: 79.4
```

#### Step 2: Fetch Documentation

```bash
scripts/context7.py docs "<library-id>" "[topic]" "[mode]"
```

**Parameters:**

- `library-id`: From search results (e.g., `/facebook/react`) or known library ID
- `topic`: Optional focus area (e.g., `hooks`, `routing`, `authentication`)
- `mode`: `code` (default) for API/examples, `info` for guides

**Version-Specific Docs:**

```bash
# Request specific version by adding it to the library ID
scripts/context7.py docs "/vercel/next.js/14" "middleware"

# Or mention in topic
scripts/context7.py docs "/facebook/react" "hooks in React 18"
```

**Examples:**

```bash
# Get React hooks documentation
scripts/context7.py docs "/facebook/react" "hooks"

# Get Next.js routing docs
scripts/context7.py docs "/vercel/next.js" "routing"

# Get conceptual guide (info mode)
scripts/context7.py docs "/vercel/next.js" "app router" info

# Get version-specific docs
scripts/context7.py docs "/vercel/next.js/14" "server components"
```

#### Step 3: Apply to User's Question

Use the returned documentation to:

1. Provide accurate, version-specific answers
2. Show official code patterns and examples
3. Reference correct API signatures
4. Include relevant caveats or deprecations
5. Cite the source URL when available

## Script Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `search` | Find library ID | `scripts/context7.py search "prisma"` |
| `docs` | Fetch documentation | `scripts/context7.py docs "/prisma/prisma" "queries"` |

**Requirements:**

- Python 3.6+ (built-in on most systems)
- No external dependencies - uses Python standard library only

## Documentation Modes

| Mode | Use For | Example |
|------|---------|---------|
| `code` | API references, code examples, function signatures (default) | `scripts/context7.py docs "/facebook/react" "useState"` |
| `info` | Conceptual guides, tutorials, architecture docs | `scripts/context7.py docs "/vercel/next.js" "routing" info` |

## Example Workflow

```bash
# User asks: "How do I use React hooks?"

# Option A: If you know the library ID, skip search
scripts/context7.py docs "/facebook/react" "hooks"

# Option B: If you don't know the library ID
# Step 1: Search for React
scripts/context7.py search "react"
# Output shows: ID: /facebook/react

# Step 2: Fetch hooks docs
scripts/context7.py docs "/facebook/react" "hooks"

# Step 3: Use the returned documentation to answer
```

## Validation & Recovery

If results are unsatisfactory, follow this recovery workflow:

1. **Empty or irrelevant results?**
   - Try a broader topic (e.g., "hooks" instead of "useEffect cleanup")
   - Switch mode: use `info` if `code` returns nothing, or vice versa
   - Verify library ID is correct with a fresh search

2. **Library not found?**
   - Search with alternative names (e.g., "nextjs" vs "next.js")
   - Try the organization name (e.g., "vercel next")
   - Check for typos in the library ID format (`/org/repo`)

3. **Rate limited?**
   - Inform user about CONTEXT7_API_KEY for higher limits
   - Provide cached/general knowledge as fallback

**Always verify** the documentation matches the user's version requirements before providing answers.

## Common Use Cases

### Use Case 1: Direct Library Lookup

When you know the exact library the user is asking about:

```bash
# User: "Create a Next.js API route with authentication"
scripts/context7.py docs "/vercel/next.js" "api routes authentication"
```

### Use Case 2: Version-Specific Documentation

When the user mentions or needs a specific version:

```bash
# User: "How do I use Next.js 14 server actions?"
scripts/context7.py docs "/vercel/next.js/14" "server actions"

# Or search for the version
scripts/context7.py search "next.js 14"
```

### Use Case 3: Conceptual Understanding

When the user needs to understand concepts, not just code:

```bash
# User: "Explain how Next.js app router works"
scripts/context7.py docs "/vercel/next.js" "app router architecture" info
```

### Use Case 4: Discovery Search

When you're unsure which library the user means:

```bash
# User: "I need a database ORM for Node.js"
scripts/context7.py search "node.js ORM"
# Review results, pick most relevant (e.g., /prisma/prisma)
scripts/context7.py docs "/prisma/prisma" "getting started"
```

## Error Handling

If the script fails:

1. **Dependencies**: Verify Python 3.6+ is installed (`python3 --version`)
2. **Library ID format**: Check the format is `/org/project` (with leading slash)
3. **Topic too narrow**: Try a broader topic or no topic filter
4. **Wrong mode**: Try `info` mode if `code` returns insufficient results
5. **Network issues**: Check connectivity and firewall settings
6. **Rate limiting**: If using without API key, you may be rate-limited. Get a free key at [context7.com/dashboard](https://context7.com/dashboard)

**Debug mode:**

```bash
# Check Python version
python3 --version

# Test basic connectivity
python3 scripts/context7.py search "react"
```

## Notes

- **Script path**: All `scripts/context7.py` commands are relative to this skill's directory
- **No MCP overhead**: Uses REST API directly, no tool schemas in context
- **API key optional**: Works without key, but rate-limited. Get free key at [context7.com/dashboard](https://context7.com/dashboard)
- **Topic filtering**: Use specific topics for focused results
- **Search first (when needed)**: Search to find the correct library ID only if you don't know it
- **Skip search (when possible)**: Use known library IDs directly (e.g., `/facebook/react`, `/vercel/next.js`)
- **Caching**: Results are not cached; each call fetches fresh data
- **Version support**: Append version to library ID (e.g., `/vercel/next.js/14`) or mention in topic
- **Cross-platform**: Python 3.6+ works on Windows, macOS, and Linux
- **No external dependencies**: Uses only Python standard library

**Performance Tips:**

- Keep known library IDs in memory (React = `/facebook/react`, Next.js = `/vercel/next.js`, etc.)
- Skip search when you know the library
- Use specific topics to get focused results faster
- Use `code` mode (default) for implementation details, `info` mode for concepts

**Environment Variables:**

```bash
# Set API key (all platforms)
export CONTEXT7_API_KEY="your-api-key"

# Windows Command Prompt
set CONTEXT7_API_KEY=your-api-key

# Windows PowerShell
$env:CONTEXT7_API_KEY="your-api-key"
```

---

> **License:** MIT License - See LICENSE for complete terms
> **Author:** Arvind Menon
> **Based on:** Context7 REST API by Upstash
