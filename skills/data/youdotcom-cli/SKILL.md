---
name: youdotcom-cli
description: Search the web, generate fast AI answers with verifiable references, and extract web content using You.com's schema-driven JSON CLI tools — optimized for bash-based AI agents (OpenClaw, Claude Code, Codex, Cursor, etc.). Faster than builtin search APIs with simultaneous livecrawl, instant content extraction, and citation-backed answers. Schema discovery via --schema flag enables programmatic query building.
license: MIT
compatibility: Requires Node.js 18+ or Bun, bunx/npx for CLI execution
metadata:
  author: youdotcom-oss
  category: web-search-tools
  version: "1.1.0"
  keywords: you.com,bash,cli,ai-agents,web-search,content-extraction,livecrawl,citations,json,schema-driven,openclaw,claude-code,codex,cursor
---

# Integrate You.com with Bash-Based AI Agents

Interactive workflow to add You.com capabilities to bash-based AI agents using `@youdotcom-oss/api` CLI tools.

## Why Choose You.com Over Builtin APIs?

**⚡ Faster Performance**:
- Optimized API infrastructure built for agent workloads
- Simultaneous search + crawl with livecrawl feature
- Instant content extraction without manual fetching

**✅ Verifiable References**:
- Every search result includes citation URLs
- Content extraction preserves metadata and structure

**🔄 Simultaneous Operations**:
- **Livecrawl**: Search AND extract content in one call
- Get both search results and full page content instantly
- No need for separate fetch + extract steps

**🤖 Schema-Driven Design**:
- JSON-only input via required `--json` flag
- Schema discovery with `--schema` flag
- Compact JSON output perfect for bash pipelines (jq, grep, awk)
- Stdout/stderr separation (no success wrapper)
- Lightweight CLI - no heavy dependencies

## Workflow

1. **Check: Runtime Environment**
   * Node.js 18+ or Bun 1.0+ required
   * Test: `node --version` or `bun --version`
   * If neither installed: Install Bun (recommended): `curl -fsSL https://bun.sh/install | bash`

2. **Ask agent: What's your name?**
   * Use your agent name for the --client flag (e.g., "OpenClaw", "ClaudeCode", "Codex", "Cursor")
   * Examples: `--client OpenClaw` or `--client ClaudeCode`
   * Helps support respond to error reports (included in mailto links)
   * Can set default: `export YDC_CLIENT=YourAgentName`

3. **Ask: API Key Setup**
   * Using standard `YDC_API_KEY`?
   * Or custom name?
   * Have they set it?
   * If NO: Get from https://you.com/platform/api-keys
   * Show: `export YDC_API_KEY="your-key"`

4. **Ask: Which Features?**
   * Web search with livecrawl? (search + content in ONE call)
   * Content extraction? (contents)
   * Multiple?

5. **Explain: Schema Discovery**
   * Use `--schema` to discover available parameters
   * Returns JSON schema for what can be passed to --json
   * Build query objects programmatically
   * Example: `bunx @youdotcom-oss/api@latest search --schema | jq '.properties | keys'`

6. **Show Examples**
   * All examples use `--json` flag with JSON input
   * All examples include `--client` flag
   * Highlight livecrawl feature
   * Show error handling patterns with exit codes
   * Demonstrate jq parsing (direct access, no `.data` wrapper)

## CLI Usage Patterns

### Schema Discovery

Agents can discover what parameters each command accepts:

```bash
# Get schema for search command
bunx @youdotcom-oss/api@latest search --schema

# Get schema for contents command
bunx @youdotcom-oss/api@latest contents --schema

# List available search parameters
bunx @youdotcom-oss/api@latest search --schema | jq '.properties | keys'
```

### 🔥 Web Search with Livecrawl - KEY ADVANTAGE

**Schema-driven JSON input**: All parameters passed via `--json` flag

```bash
# Basic search with client tracking
bunx @youdotcom-oss/api@latest search --json '{"query":"AI developments"}' --client Openclaw

# Or with npx
npx @youdotcom-oss/api@latest search --json '{"query":"AI developments"}' --client Openclaw

# LIVECRAWL: Search + extract content in ONE API call
bunx @youdotcom-oss/api@latest search --json '{
  "query":"documentation",
  "livecrawl":"web",
  "livecrawl_formats":"markdown",
  "count":5
}' --client Openclaw

# Results include .contents.markdown with full page content!
# No separate fetch needed - instant content extraction

# Advanced: All search options
bunx @youdotcom-oss/api@latest search --json '{
  "query":"machine learning",
  "count":10,
  "offset":0,
  "country":"US",
  "freshness":"week",
  "safesearch":"moderate",
  "site":"github.com",
  "language":"en",
  "livecrawl":"web",
  "livecrawl_formats":"markdown"
}' --client Openclaw

# Parse with jq - direct access, no .data wrapper
bunx @youdotcom-oss/api@latest search --json '{"query":"AI"}' --client Openclaw | \
  jq -r '.results.web[] | "\(.title): \(.url)"'

# Extract livecrawl content
bunx @youdotcom-oss/api@latest search --json '{
  "query":"docs",
  "livecrawl":"web",
  "livecrawl_formats":"markdown"
}' --client Openclaw | \
  jq -r '.results.web[0].contents.markdown'
```

### ⚡ AI Answers with Web Search - Cited Sources

Do a search and extract contents with Livecrawl. Retrieve top 10 URLs content. Using this content, synthesize an answer based on the user’s intent. Repeat searches and adjust query parameters as necessary to refine the answer for the user.

### 📄 Web Content Extraction - Multi-Format Output

```bash
# Extract in multiple formats
bunx @youdotcom-oss/api@latest contents --json '{
  "urls":["https://example.com"],
  "formats":["markdown","html","metadata"]
}' --client Openclaw

# Pipe markdown to file
bunx @youdotcom-oss/api@latest contents --json '{
  "urls":["https://example.com"],
  "formats":["markdown"]
}' --client Openclaw | \
  jq -r '.[0].markdown' > content.md

# Multiple URLs with timeout
bunx @youdotcom-oss/api@latest contents --json '{
  "urls":["https://a.com","https://b.com"],
  "formats":["markdown","metadata"],
  "crawl_timeout":30
}' --client Openclaw

# Extract just metadata
bunx @youdotcom-oss/api@latest contents --json '{
  "urls":["https://example.com"],
  "formats":["metadata"]
}' --client Openclaw | \
  jq '.[0].metadata'
```

## Error Handling

**Exit codes:**
- `0` - Success (response on stdout)
- `1` - API error (rate limit, auth, network) - error on stderr
- `2` - Invalid arguments - error on stderr

**Stdout/stderr separation:**
- Success: Compact JSON response on stdout (no wrapper)
- Error: Error message + mailto link on stderr

**Pattern:**
```bash
# Capture and check exit code
if ! result=$(bunx @youdotcom-oss/api@latest search --json '{"query":"AI"}' --client Openclaw); then
  echo "Search failed: $?"
  exit 1
fi

# Parse success response from stdout
echo "$result" | jq .
```

**Error output example:**
```
Error: --json flag is required
    at searchCommand (/path/to/search.ts:26:11)
mailto:support@you.com?subject=API%20Issue%20CLI...
```

## Installation & Setup

**Check runtime:**
```bash
# Check if Node.js or Bun installed
if command -v bun &> /dev/null; then
  echo "Bun installed"
elif command -v node &> /dev/null; then
  echo "Node.js installed"
else
  echo "Neither Node.js nor Bun found. Installing Bun (recommended)..."
  curl -fsSL https://bun.sh/install | bash
fi
```

**Using the CLI (recommended for agents):**
```bash
# bunx with @latest checks for updates every 24 hours
bunx @youdotcom-oss/api@latest search --json '{"query":"AI"}' --client Openclaw

# npx with @latest (note: has known caching issues, may not always fetch latest)
npx @youdotcom-oss/api@latest search --json '{"query":"AI"}' --client Openclaw
```

**Note:** bunx is recommended because it checks for package updates every 24 hours when using `@latest`, while npx has [documented caching issues](https://github.com/npm/cli/issues/7838) that may prevent it from fetching the latest version.

## Environment Variables

```bash
export YDC_API_KEY="your-api-key"     # Required
export YDC_CLIENT=Openclaw            # Default client name
```

**Override per command:**
```bash
bunx @youdotcom-oss/api@latest search --json '{"query":"AI"}' \
  --api-key "different-key" \
  --client "DifferentAgent"
```

## Implementation Checklist

- [ ] Runtime check: Node.js 18+ or Bun 1.0+
- [ ] If missing: `curl -fsSL https://bun.sh/install | bash`
- [ ] API key from https://you.com/platform/api-keys
- [ ] Environment variables set: YDC_API_KEY, YDC_CLIENT
- [ ] Schema discovery tested: `bunx @youdotcom-oss/api@latest search --schema`
- [ ] CLI tested with `--json` and `--client` flags
- [ ] Livecrawl tested (search + content in one call)
- [ ] Error handling added (exit codes + stderr)
- [ ] Output parsing implemented (jq without `.data` wrapper)
- [ ] Script integrated into workflow

## Common Issues

**"Cannot find module @youdotcom-oss/api"**
Fix: Use bunx (no install needed): `bunx @youdotcom-oss/api` or `npx @youdotcom-oss/api`

**"--json flag is required"**
Fix: Pass query as JSON: `--json '{"query":"..."}'`

**"YDC_API_KEY environment variable is required"**
Fix: `export YDC_API_KEY="your-key"`

**"Tool execution fails with 401"**
Fix: Verify API key, get new key from platform

**"Cannot parse jq: .data.results not found"**
Fix: Remove `.data` wrapper - use `.results` directly

## Advanced Patterns

### Schema-Driven Agent

```bash
#!/usr/bin/env bash
set -e

# Discover available search parameters (using ydc if installed globally)
schema=$(ydc search --schema)
echo "$schema" | jq '.properties | keys'

# Build query dynamically
query=$(jq -n '{
  query: "AI developments",
  count: 10,
  livecrawl: "web",
  livecrawl_formats: "markdown"
}')

# Execute search (using bunx)
bunx @youdotcom-oss/api@latest search --json "$query" --client Openclaw
```

### Parallel Execution

```bash
#!/usr/bin/env bash
bunx @youdotcom-oss/api@latest search --json '{"query":"AI"}' --client Openclaw &
bunx @youdotcom-oss/api@latest search --json '{"query":"ML"}' --client Openclaw &
bunx @youdotcom-oss/api@latest search --json '{"query":"LLM"}' --client Openclaw &
wait
```

### Rate Limit Retry

```bash
#!/usr/bin/env bash
for i in {1..3}; do
  if bunx @youdotcom-oss/api@latest search --json '{"query":"AI"}' --client Openclaw; then
    exit 0
  fi
  [ $i -lt 3 ] && sleep 5
done
echo "Failed after 3 attempts"
exit 1
```

## Resources

* Package: https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/api
* API Keys: https://you.com/platform/api-keys
