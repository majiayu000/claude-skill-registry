---
name: browse
description: >
  · Browse/scrape web pages with Lightpanda, Playwright MCP, agent-browser, or fetch. Triggers: 'browse', 'scrape', 'headless', 'open url', 'read website', 'fill form', 'crawl'. Not for E2E tests (use testing).
license: MIT
compatibility: "Optional: lightpanda, @playwright/mcp, agent-browser. Falls back to WebFetch or curl"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-04"
  effort: medium
---

# Browse: Token-Efficient Web Browsing

Guide AI agents through web browsing tasks using the cheapest tool that gets the job done.
Every browsing action has a token cost - this skill minimizes it through progressive disclosure,
smart format selection, and backend-aware strategies.

**Target versions** (May 2026):
- Lightpanda: 0.3.1
- @playwright/mcp: 0.0.75
- agent-browser: 0.27.0

## When to use

- Reading a web page, article, or documentation site
- Extracting structured data from a page (prices, tables, metadata)
- Filling forms, clicking buttons, or navigating multi-step flows
- Scraping content from JavaScript-rendered pages (SPAs)
- Browsing behind authentication (login flows)
- Any task where the agent needs to see or interact with a live web page

## When NOT to use

- E2E test automation, test writing, or test debugging - use **testing**
- Building or debugging MCP servers (including browser MCP servers) - use **mcp**
- Network configuration, DNS, reverse proxies - use **networking**
- Fetching API endpoints or REST calls - use curl/fetch directly
- Static file downloads - use curl or wget
- Web scraping specifically for RAG pipelines or training data - use **ai-ml** for the pipeline

## AI Self-Check

Before returning any browsing result, verify:

- [ ] Used the cheapest tool available for the task - no Playwright when WebFetch would have worked
- [ ] Did not dump full HTML into context when markdown or structured data was sufficient
- [ ] Waited for dynamic content before extracting from SPAs (`networkidle` or `--wait-selector`)
- [ ] Stripped boilerplate (nav, ads, footers) before returning content to the user
- [ ] Scoped extraction to the relevant section, not the whole page
- [ ] Did not hardcode credentials - used env vars, secret manager, or user prompt
- [ ] Cleared or isolated cookies/storage between unrelated accounts or tenants
- [ ] Used semantic roles before CSS selectors for interaction targets
- [ ] Used screenshots only when visual layout or rendered state mattered
- [ ] Recorded URL and access date for facts likely to change
- [ ] Did not automate destructive account actions unless the user named the exact action and target
- [ ] Re-extracted page state after any click or form submission before making decisions
- [ ] Escalated to the next tool tier on failure rather than retrying the same tool
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Robots and terms considered**: scraping or automation respects access rules, auth boundaries, and rate limits
- [ ] **Dynamic content verified**: browser-rendered pages are checked with the real tool when static HTML may be incomplete

---

## Tool Selection

Detect what's available and pick the cheapest tool that handles the task.

### Detection

1. **MCP browsing tools**: look for `goto`, `navigate`, `markdown`, `semantic_tree`,
   `browser_navigate`, `browser_snapshot` in the available tool list
2. **CLI tools**: check `lightpanda`, `agent-browser` in PATH
3. **Built-in fetch**: WebFetch tool (Claude Code) or platform equivalent
4. **Fallback**: curl via shell

### Decision matrix

| Task | No JS needed | JS needed, read-only | JS needed, interactive |
|------|-------------|----------------------|------------------------|
| **Best** | WebFetch / curl | Lightpanda fetch | Lightpanda MCP tools |
| **Good** | Lightpanda fetch | MCP markdown tool | agent-browser CLI |
| **Fallback** | curl | Playwright MCP | Playwright MCP |

If the page works without JavaScript, don't use a browser. If you only need to read content,
don't use interactive tools. Escalate only when the cheaper option fails.

### Task modes

| Mode | Use when | First tool |
|---|---|---|
| Static fetch | Content is in HTML | WebFetch, curl, or Lightpanda fetch |
| JS read-only | Content requires rendering | Lightpanda or Playwright markdown |
| Interactive | Click, fill, or navigate statefully | MCP browser tools |
| Authenticated | User-approved account context is required | Existing authenticated browser session |
| Screenshot | Visual layout matters | Browser screenshot after DOM snapshot |
| Structured extraction | Tables, JSON-LD, prices, metadata | API, JSON-LD, DOM selectors, then browser |

**Tool availability check**: before starting, verify what's available. If the best tool for
the task isn't present, skip straight to the next tier rather than failing mid-workflow.

---

## Performance

- Prefer official APIs, sitemaps, or static fetches before launching a browser.
- Extract only required page regions; avoid dumping full DOMs, screenshots, or network logs into context.
- Reuse browser sessions for multi-step flows, but clear cookies/storage between unrelated accounts or tenants.
- Use screenshots only when visual layout or rendered state matters.

---

## Best Practices

- Use stable selectors and semantic roles before brittle CSS paths.
- Record URL and access date for facts likely to change.
- Clear cookies/storage between unrelated accounts or tenants.
- Do not automate destructive account actions unless the user names the exact action and target.

---

## Workflow

### Step 1: Assess the task

Before touching any tool, answer these in order - each answer narrows the tool choice:

1. **Read or interact?** Read-only -> skip to Step 2. Interactive -> go to Step 3/4.
2. **Static or dynamic?** View page source or check URL patterns - if the content is
   in the HTML, it's static. SPA frameworks (React, Vue, Angular) need JS rendering.
3. **Single page or multi-step?** Multi-step flows need session persistence (MCP or serve mode).
4. **What output format?** Markdown for human reading, structured data / JSON-LD for extraction,
   semantic tree for element discovery, links for crawl planning.

### Step 2: Try the cheapest path first

**Static content** (docs, articles, blogs):
```bash
# Option A: built-in fetch (lowest overhead, no setup)
# Use WebFetch tool with the URL directly

# Option B: Lightpanda CLI (better stripping, selector waits)
lightpanda fetch --dump markdown --strip-mode full <url>

# Option C: curl (always available, raw HTML only)
curl -sL <url>
```

**JS-rendered content** (SPAs, dashboards):
```bash
# Lightpanda CLI with wait
lightpanda fetch --dump markdown --strip-mode full --wait-until networkidle <url>

# With selector wait for specific content
lightpanda fetch --dump markdown --wait-selector ".main-content" <url>
```

**Interactive tasks** (forms, clicks, multi-step): use MCP tools or agent-browser CLI (Step 3).

### Step 3: Navigate and extract

**With MCP browsing tools** (Lightpanda MCP or Playwright MCP):

Navigate first, then extract using the cheapest format:

| Format | Tool | Tokens (typical) | Use when |
|--------|------|-------------------|----------|
| Semantic tree | `semantic_tree` / `browser_snapshot` | ~200-500 | Finding elements to interact with |
| Markdown | `markdown` | ~500-2000 | Reading text content |
| Links only | `links` | ~100-300 | Finding URLs to follow |
| Structured data | `structuredData` / `structured_data` | ~100-500 | Getting metadata (OpenGraph, JSON-LD) |
| Interactive elements | `interactiveElements` / `interactive_elements` | ~200-400 | Finding clickable/fillable elements |
| Full HTML | page-html resource | ~5000-50000 | Last resort only |

**Following links to find data:** if the initial extraction doesn't contain the target content
(e.g., the page uses images or links to a separate document), extract the page's links first
using the `links` tool or markdown output, identify the relevant link, and fetch that instead.
Don't re-fetch the whole page - follow the specific link to the actual data.

**With agent-browser CLI:**
```bash
agent-browser open <url>
agent-browser snapshot -i          # interactive element refs (@e1, @e2...)
agent-browser click @e3            # click by ref
agent-browser fill @e5 "query"     # fill input by ref
```

**With Lightpanda CLI (non-interactive):**
```bash
lightpanda fetch --dump semantic_tree <url>                          # structure
lightpanda fetch --dump markdown --strip-mode full <url>             # content
lightpanda fetch --dump markdown --wait-until networkidle <url>      # dynamic content
```

### Step 4: Interact (when needed)

For multi-step flows (login, form submission, navigation):

1. **Get interactive elements first** - use `interactive_elements` or `semantic_tree` to find
   targets without loading the full DOM
2. **Act on specific elements** - click, fill, select using element identifiers
3. **Re-extract after each action** - page state changes; get a fresh view
4. **Wait for navigation** - after clicks that trigger page loads, wait before extracting

**MCP interaction pattern:**
```
1. goto(url)
2. interactive_elements()       - find what to click/fill
3. click(id) or fill(id, value)
4. semantic_tree()              - verify state changed
5. Repeat 2-4 as needed
```

### Step 5: Process results

**Single-page reads**: if you extracted more than needed, pull out the relevant section before
returning it. Don't dump an entire page of markdown when the user asked about one paragraph.

For documentation sites, target the content container. Most docs use predictable selectors:
```bash
# Try common content selectors in order of specificity
lightpanda fetch --dump markdown --wait-selector "article" <url>
lightpanda fetch --dump markdown --wait-selector "main" <url>
lightpanda fetch --dump markdown --wait-selector ".content" <url>
```
If the full page was already fetched, extract the relevant section from the markdown output
rather than re-fetching - search for headings or known section titles.

**Multi-step workflows**:
- Cache extraction results rather than re-fetching the same page
- Summarize intermediate pages (e.g., search results) instead of returning raw content
- Discard navigation/boilerplate content before putting results in context

### Step 6: Handle failures

When a tool fails, escalate to the next tier - don't retry the same tool blindly.

| Failure | Likely cause | Action |
|---------|-------------|--------|
| Empty/broken content | JS didn't render | Escalate: WebFetch -> Lightpanda -> Playwright MCP |
| 403 / blocked | Bot detection | Try with `--user-agent-suffix` (Lightpanda) or Playwright (real browser UA) |
| Timeout | Heavy page / slow network | Increase wait timeout, try `--wait-selector` on specific element |
| Connection refused | Wrong port / service down | Verify URL, check if site requires VPN or local network |
| SSL error | Cert issue or MITM | Check cert validity, do not bypass without user confirmation |

**After login failures**: re-check the form field selectors - SPAs frequently change element IDs
between deploys. Use `interactive_elements` to get fresh selectors rather than hardcoding.

**Saving fetched content**: for file downloads or large extractions, write results to a local
file rather than keeping everything in context:
```bash
lightpanda fetch --dump markdown --strip-mode full <url> > extracted.md
```

For binary downloads (PDFs, images) after auth, extract the session cookie from the browser
context and hand it to curl. With Playwright MCP or Lightpanda MCP, use `evaluate` to read
`document.cookie`, then:
```bash
curl -L -o report.pdf -b "session=<value>; csrf=<value>" \
  -H "Referer: https://internal.example.com/reports" <pdf-url>
```
Alternative: trigger the browser's native download via `evaluate`
(`document.querySelector('a.download').click()`) and let the headless session write to its
download directory - avoids moving the cookie out of the browser entirely. This is the only
working path for `blob:` URLs and `data:` URIs - they are in-memory browser references with
no fetchable origin, so curl cannot resolve them; let the page itself resolve the blob via a
click or read it with `evaluate` and `FileReader.readAsDataURL` to extract the bytes.

---

## Token Efficiency

### Progressive disclosure

Start with the cheapest representation. Escalate only when insufficient.

```
Level 0: URL only (0 tokens)           - sometimes the URL itself answers the question
Level 1: Structured data (~100-300)     - metadata, navigation links
Level 2: Semantic tree (~200-500)       - page structure, interactive elements
Level 3: Markdown (~500-2000)           - readable content
Level 4: Full HTML (~5000-50000)        - complex parsing, last resort
```

### Strip unnecessary content

With Lightpanda CLI, always use `--strip-mode`:
- `js` - remove script tags
- `css` - remove stylesheets
- `ui` - remove images, video, SVG
- `full` - all of the above (default for content extraction)

### Scope extraction

Don't dump the whole page when you need one section:
```bash
lightpanda fetch --dump markdown --wait-selector "#pricing-table" <url>
```

With MCP semantic tree, limit depth:
```
Tool: semantic_tree
Args: { maxDepth: 3 }    - top 3 levels only
```

### Extract structured data from pages

When you need specific data (prices, tables, metadata) rather than full page content:

1. Try `structured_data` / `structuredData` first - many sites embed JSON-LD or OpenGraph
2. If no structured data exists, use `evaluate` / `eval` to run JavaScript extraction:
```
Tool: evaluate
Args: { expression: "JSON.stringify([...document.querySelectorAll('.product')].map(p => ({name: p.querySelector('h2')?.textContent, price: p.querySelector('.price')?.textContent})))" }
```
3. Parse the JSON result rather than scraping markdown with regex

### Batch multi-page work

```bash
for url in "$url1" "$url2" "$url3"; do
  lightpanda fetch --dump markdown --strip-mode full "$url"
  printf '\n---\n'
  sleep 1  # rate-limit: don't hammer the same domain
done > output.md
```

---

## SPA and Dynamic Content

**Data extraction priority**: try structured data (JSON-LD, `structuredData`) before markdown parsing, and markdown before full HTML.

1. **Always wait**: use `--wait-until networkidle` or `--wait-selector` with Lightpanda,
   `waitForSelector` / `browser_wait_for` with MCP tools
2. **Client-side routing**: if a link changes the URL without a full page load, re-extract
   content after each route change
3. **Lazy loading / infinite scroll**: scroll to trigger content loading before extracting.
   For infinite scroll, use a loop: scroll, wait for new content, extract, repeat until you
   have enough data or no new content appears. Cap iterations to avoid endless scrolling
4. **Cookie consent / popups**: dismiss overlays before extracting content - use
   `interactive_elements` to find the dismiss button, then `click`. If the overlay blocks
   extraction, clicking through it costs fewer tokens than retrying with different formats
5. **Pagination**: for paginated results, extract each page sequentially using the "Next"
   link or pagination controls. Don't try to load all pages at once - extract, process, advance
6. **Verify content loaded**: after waiting, check that the extracted content is non-empty and
   contains expected elements before processing. An empty markdown or a semantic tree with only
   `<html><body>` means the page didn't render - escalate to a heavier backend
7. **Lightpanda gaps**: partial Web API coverage means some complex SPAs won't render correctly.
   Fall back to Playwright MCP if extraction returns empty or broken content

---

## Authentication Flows

1. Navigate to the login page
2. Use `interactive_elements` to find form fields
3. Fill credentials from env vars or user prompt - never hardcode
4. Submit the form
5. Wait for redirect to complete (watch for multi-step redirects in OAuth/SSO flows -
   the URL may bounce through several domains before landing)
6. Verify login succeeded: extract page content and check for user-specific elements
   (profile name, dashboard content) before proceeding
7. Continue browsing the authenticated session

**OAuth/SSO redirects**: some login flows redirect through identity providers (Google, Okta,
Auth0). Follow each redirect, fill credentials at the IdP page, and wait for the final
redirect back to the target site. Don't assume login completes on the first page.

**MFA prompts**: if a TOTP/MFA prompt appears after credentials, you cannot proceed
automatically. Inform the user that MFA is required and ask them to complete it manually,
or request the TOTP code from the user/env var to fill in.

**Session expiration**: if extraction suddenly returns login pages or 401s mid-flow, the session
has expired. Re-authenticate before continuing. For long-running scrapes, check session validity
periodically by verifying a known authenticated-only element is still visible.

**Session persistence by backend:**
- **Lightpanda MCP / Playwright MCP**: session persists within the MCP connection
- **Lightpanda CLI fetch**: no persistence between calls (use `serve` mode for multi-step auth)
- `agent-browser`: session-based with `--session` flag

For session isolation, CSRF-sensitive actions, and multi-tenant account handling, read
`references/authenticated-browsing.md`.

---

## Missing Tools

If no browsing tools are detected, recommend the user set up Lightpanda MCP - it's the
fastest path to full browsing capability with minimal overhead.

**Lightpanda MCP setup** (one-time, ~30 seconds):
```bash
# Install the binary (see references/tool-setup.md for other architectures)
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/0.3.1/lightpanda-x86_64-linux
chmod +x lightpanda && mv lightpanda ~/.local/bin/
```

Add the MCP server to your Claude Code settings (`~/.claude/settings.json` or project
`.mcp.json`) - merge with existing config, don't overwrite:
```json
{
  "mcpServers": {
    "lightpanda": {
      "command": "lightpanda",
      "args": ["mcp"],
      "env": { "LIGHTPANDA_DISABLE_TELEMETRY": "true" }
    }
  }
}
```

Restart the session after adding the MCP config. The Lightpanda tools (`goto`, `markdown`,
`semantic_tree`, etc.) will appear in the available tool list.

Read `references/tool-setup.md` for other platforms, architectures, and alternative backends.

---

## Reference Files

Read `references/tool-setup.md` when you need installation commands for a specific platform,
MCP tool parameter details (full tool tables with token costs), engine-specific CLI flags,
or known limitations of a backend. The main SKILL.md covers workflow and strategy; the
reference file covers tool-specific depth.

Read `references/extraction-patterns.md` for static, JavaScript-rendered, screenshot, table,
pagination, and attribution patterns.

Read `references/authenticated-browsing.md` before using saved sessions, cookies, or
account-specific pages.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** BROWSE
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/browse/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **testing** - E2E test automation with Playwright. This skill handles ad-hoc browsing and
  data extraction; testing handles structured test suites and assertions.
- **mcp** - MCP server development. This skill uses MCP browsing tools; mcp helps build them.
- **networking** - Network infrastructure. This skill browses over the network; networking
  configures it.
- **ai-ml** - RAG pipelines and web data collection. When scraping content specifically for
  embeddings or training data, ai-ml covers the pipeline; this skill covers the extraction.

## Rules

1. **Cheapest tool first.** Always try the lowest-token option before escalating. WebFetch
   before Lightpanda, Lightpanda before Playwright, markdown before full HTML.
2. **Never dump full HTML into context unless no other format works.** Full HTML is 10-100x
   more expensive than markdown or semantic tree for the same information.
3. **Strip before extracting.** Use `--strip-mode full` with Lightpanda CLI. Prefer semantic
   tree or markdown over raw HTML with MCP tools.
4. **Wait for dynamic content.** Don't extract from a half-loaded SPA. Use networkidle,
   selector waits, or script waits.
5. **No hardcoded credentials.** Auth flows must use environment variables, secret managers,
   or user prompts.
6. **Re-extract after interaction.** Page state changes after clicks and form submissions.
   Always get a fresh view before making decisions based on page content.
7. **Semantic selectors first.** Use roles, accessible names, labels, and stable text before
   brittle CSS selectors.
8. **Screenshots are for visuals.** Take screenshots only when layout, rendered state, or
   visual evidence matters.
9. **Respect robots.txt and rate limits.** Use `--obey-robots` with Lightpanda when scraping.
   Add a 1-2 second delay between requests when batch-fetching multiple pages from the same
   domain. Don't hammer sites with rapid sequential requests.
