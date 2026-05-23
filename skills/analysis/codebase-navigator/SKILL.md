---
name: codebase-navigator
description: Semantic code search using osgrep for understanding codebases, finding implementations, and navigating large projects. Use when asked "where is", "how does", "find the code that", or any question about code location or implementation.
---

# Codebase Navigator

Semantic code search powered by osgrep - find code by meaning, not just keywords.

## When to Use

Invoke when user:
- Asks "where is [feature] implemented?"
- Asks "how does [component] work?"
- Wants to "find the code that handles [task]"
- Needs to understand codebase architecture
- Searches for implementation patterns

## Core Workflow

### 1. Check Index Freshness (Auto-Refresh)

**Before searching, check if index is stale (>4 hours):**

```bash
# Find store for current repo
osgrep list

# Check age of relevant store (macOS)
STORE=~/.osgrep/data/YOUR-STORE.lance
STORE_AGE=$(( $(date +%s) - $(stat -f %m "$STORE") ))

# If older than 4 hours (14400 seconds), refresh
if [ $STORE_AGE -gt 14400 ]; then
  echo "Index is $(( STORE_AGE / 3600 )) hours old - refreshing..."
  osgrep index
fi
```

**Quick version:** If unsure, just use `--sync`:
```bash
osgrep search "query" --sync   # Always safe, updates before searching
```

### 2. First-Time Setup

If no store exists for current repo:
```bash
osgrep list              # See available stores
osgrep doctor            # Verify setup is healthy
osgrep index             # Index current directory (takes ~30s-2min)
```

### 3. Search Semantically

**Basic search:**
```bash
osgrep search "natural language description of what you're looking for"
```

**Tuned search:**
```bash
osgrep search "query" --max-count 10      # Limit total results
osgrep search "query" --per-file 3        # Multiple matches per file
osgrep search "query" --content           # Show full chunk content
osgrep search "query" --compact           # File paths only
osgrep search "query" --scores            # Show relevance scores
osgrep search "query" --json              # Machine-readable output
```

### 3. Synthesize Results

**DO NOT** dump raw osgrep output. Instead:
1. Read the relevant file snippets
2. Understand the code in context
3. Explain to user in plain language
4. Cite specific files and line numbers

## Query Formulation

**Semantic queries work best.** Transform user questions:

| User asks | osgrep query |
|-----------|--------------|
| "Where's the auth?" | `"authentication logic and user login"` |
| "How do we handle errors?" | `"error handling and exception management"` |
| "Find the API endpoints" | `"HTTP routes and API endpoint definitions"` |
| "Database queries" | `"database queries and SQL execution"` |
| "Config loading" | `"configuration loading and environment variables"` |

**Tips for better queries:**
- Use descriptive phrases, not keywords
- Include synonyms: "auth" → "authentication logic and user login"
- Describe the purpose: "code that validates user input"
- Be specific about what you want: "function that calculates total price"

## Output Modes

### Default Mode
Shows snippet preview with line numbers:
```
📂 src/auth/login.ts
   1 │ export async function login(username: string, password: string) {
   2 │   const user = await findUser(username);
```

### Content Mode (`--content`)
Shows full chunk content for deeper context.

### Compact Mode (`--compact`)
File paths only - useful for getting quick overview:
```
📂 src/auth/login.ts
📂 src/auth/session.ts
📂 src/middleware/auth.ts
```

### JSON Mode (`--json`)
Machine-readable for programmatic use.

### Scores Mode (`--scores`)
Shows relevance scores (0-1) - useful for understanding match quality.

## Advanced Usage

### Keep Index Fresh

osgrep indexes can become stale. **Refresh regularly**, especially after:
- Pulling new code
- Creating/deleting files
- Major refactoring

```bash
osgrep search "query" --sync    # Update index then search
osgrep index                    # Full re-index if --sync isn't enough
```

**Symptom of stale index:** Known files not appearing in results, or deleted files still showing up.

### Background Server
For large codebases with frequent changes:
```bash
osgrep serve                    # Runs on port 4444
osgrep serve --port 8080        # Custom port
```

### Multiple Stores
Work with specific indexed stores:
```bash
osgrep --store myproject.lance search "query"
```

## Query Refinement

When first search returns too many/wrong results:

**Step 1: Check result quality**
```bash
osgrep search "query" --scores  # Low scores (<0.15) = poor matches
```

**Step 2: Narrow with domain terms**
```
❌ "packaging workflow" → finds ArtifactsBuilder, MCPBuilder
✅ "skill packaging automation" → finds SkillPackager
```

**Step 3: Add specificity**
```
❌ "validation" → too broad (25+ files)
✅ "YAML frontmatter validation for skills" → targeted
```

**Step 4: Try synonyms if nothing found**
```
❌ "auth" → too terse
✅ "authentication login session user credentials" → covers variations
```

## osgrep vs grep: Decision Guide

| Use osgrep when... | Use grep/rg when... |
|-------------------|---------------------|
| Searching by concept | Searching for exact strings |
| "Where is auth handled?" | "Find TODO:" |
| "How does caching work?" | "Find sha256" |
| Unknown function names | Known function names |
| Architecture questions | Error message lookup |
| Understanding code purpose | Finding specific identifiers |

**Rule of thumb:** If you could type the exact string, use grep. If you're describing what code *does*, use osgrep.

## Combining Tools

### osgrep + Glob (file types)
osgrep finds code that *mentions* Python, not just .py files:
```bash
# Find Python data processing
osgrep search "python data processing" --compact  # May include .md files
# Then filter:
# Use Glob tool with pattern "**/*.py" for actual scripts
```

### osgrep + grep (refine)
```bash
# Step 1: Find relevant area
osgrep search "checksum verification"  # May miss literal "sha256"

# Step 2: grep for specific term
grep -r "sha256" --include="*.sh"  # Finds exact matches
```

### osgrep + Read (understand)
```bash
# Step 1: Find files
osgrep search "error handling middleware" --compact

# Step 2: Read to understand
# Use Read tool on top results
```

## Anti-Patterns

**DON'T:**
- Use osgrep for exact string matches (use grep/rg instead)
- Dump raw output without synthesis
- Skip indexing and wonder why searches fail
- Use single keywords ("auth") instead of phrases ("authentication handling")
- Expect osgrep to find technical literals like "sha256", "TODO:", error codes

**DO:**
- Formulate queries as natural language descriptions
- Check `osgrep list` if searches return nothing
- Use `--content` when you need more context
- Combine with file reading for full understanding
- Use `--scores` to assess match quality
- Refine queries iteratively when results are poor

## Example Session

**User:** "Where do we calculate shipping costs?"

**Process:**
```bash
osgrep search "shipping cost calculation and pricing logic"
```

**Results show:** `src/orders/shipping.ts`, `src/utils/pricing.ts`

**Response:**
"Shipping costs are calculated in `src/orders/shipping.ts:45-67`, which uses the `calculateShipping()` function. This calls pricing utilities from `src/utils/pricing.ts` for rate lookups. The calculation considers weight, distance, and shipping method."

## References

For query patterns and examples:
- `references/query-patterns.md` - Common query formulations
- `references/troubleshooting.md` - Common issues and fixes
