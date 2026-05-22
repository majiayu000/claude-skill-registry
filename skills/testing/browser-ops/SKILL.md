---
name: browser-ops
description: Browser automation skill for AI coding agents. 25 Playwright-based tools for navigation, interaction, observation, and session management.
---

# Browser Ops

Browser automation via [agent-browser](https://github.com/anthropics/agent-browser). 25 tools wrapping Playwright for navigation, interaction, observation, and session management. Validated on two benchmark suites: 12/15 pass on a 15-task suite (100% excluding external blockers), 9/10 on a 10-task progressive suite. Standout: Notion end-to-end signup with AgentMail OTP verification.

Terminology used in this file:
- **Playwright:** A browser automation framework that lets tools control Chromium/Chrome.
- **a11y tree:** The accessibility tree (screen-reader-friendly page structure) used by `browser_snapshot`.
- **DOM:** Document Object Model, the browser's structured representation of page elements.
- **CSS selector:** A rule for targeting specific DOM elements (for example `.price` or `#submit`).
- **OAuth:** A standard login/authorization flow that redirects through an identity provider (for example, "Sign in with GitHub").

## Setup

```bash
npm install -g @anthropic-ai/agent-browser
agent-browser start
```

- **Claude Code:** copy this skill folder into `.claude/skills/browser-ops/`
- **Codex CLI:** append this SKILL.md content to your project's root `AGENTS.md`

For the full installation walkthrough (prerequisites, verification, troubleshooting), see [references/installation-guide.md](references/installation-guide.md).

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the browser-ops skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

---

## Quick Start

The simplest possible browser flow: navigate, inspect, capture.

```text
browser_navigate(url="https://example.com")
browser_snapshot(mode="interactive")
browser_screenshot(path="/tmp/example.png")
browser_close()
```

---

## Decision Tree: Browser vs Other Tools

**Ask this FIRST. Getting it wrong wastes significant token budget.**

```text
Need data from the web?
  |
  +-- Is it static content? (prices, articles, search results, public data)
  |     YES --> Use WebSearch / WebFetch (built-in tools)
  |             ~100 tokens. No browser overhead.
  |
  +-- Does it require interaction? (login, form fill, click sequences, session state)
  |     YES --> Use browser tools
  |
  +-- Does it require email verification?
  |     YES --> Use browser + AgentMail (see Email Verification section)
  |
  +-- Is the target known to block bots? (Cloudflare-protected, etc.)
        YES --> Check references/failure-log.md before starting.
              May need stealth config or alternative approach.
```

**Rule of thumb:** If you can get the data with `curl`, you don't need a browser.

---

## Core Workflow

Every browser task follows this loop:

```text
1. browser_navigate(url)                       -- go to the page
2. browser_snapshot(mode='interactive')        -- get refs (@e1, @e2...)
3. Identify target ref from snapshot           -- find the button/input/link
4. browser_click(@ref) / browser_fill(@ref, text) -- act
5. browser_snapshot(mode='interactive')        -- verify result
6. Repeat 3-5 until done
7. browser_close()                             -- ALWAYS close when done
```

**The ref system:** Snapshot returns element references like `@e1`, `@e2`. Use these refs with click/fill/type. Refs are stable within a page state but reset after navigation.

---

## Token Efficiency: Snapshot Modes

| Mode | Tokens/page | Shows | Use when |
|------|-------------|-------|----------|
| `interactive` | ~1,400 | Buttons, links, inputs only | **Default for everything** |
| `compact` | ~3,000-5,000 | Condensed full tree | Need text content + interactive |
| `full` | ~15,000 | Complete a11y tree | Last resort, known need |

**Default to `interactive`.** It is 10x cheaper than `full` and sufficient for 90% of tasks.

---

## Tiered Access Model

```text
Tier 1: A11y Tree Snapshot (~1,400 tokens/page)
  browser_snapshot(mode='interactive') --> get refs --> click/fill
  For: navigation, form filling, structured page interaction
  This is your DEFAULT.

Tier 2: Screenshot + VLM (0 API tokens) [EXPERIMENTAL]
  browser_screenshot() --> local VLM (Qwen3-VL-2B / UI-TARS-1.5-7B)
  For: visual-only content, CAPTCHAs, pages where a11y tree misses data

Tier 3: Targeted DOM Extraction (variable tokens)
  browser_evaluate('document.querySelector(sel).textContent')
  For: known pages with known CSS selectors, JSON-LD extraction
  Use when you know EXACTLY what element contains the data.
```

**Escalation path:** Start at Tier 1. If snapshot doesn't show the data you need, try Tier 3 with a targeted selector. Only use Tier 2 when visual understanding is required.

### Token Optimization for Data-Heavy Pages

For content-rich pages (HN, Reddit, forums, dashboards), the interactive snapshot balloons from ~1,400 tokens (simple pages) to ~47K tokens (dense pages). This wrecks budgets.

**Pattern:** Snapshot first to understand page structure, then `browser_evaluate` with targeted JS for bulk extraction.

```text
1. browser_navigate(url)
2. browser_snapshot(mode='interactive')   -- understand structure (pay cost once)
3. browser_evaluate('                     -- extract data surgically
     JSON.stringify(
       [...document.querySelectorAll(".titleline a")]
         .map(a => ({title: a.textContent, href: a.href}))
     )
   ')
4. Parse JSON result -- structured data at ~200 tokens vs 47K snapshot
```

**When to use:** Any page where you need to extract 10+ items of the same type. Snapshot gives you the selector knowledge; eval gives you the data cheaply.

---

## Email Verification (AgentMail)

For tasks requiring email verification (account signup, OTP flows).

### Setup
- AgentMail Python wrapper: `./scripts/mailbox.py` (self-contained)
- CLI wrapper: `./scripts/agentmail.sh`
- Dependencies: `./scripts/requirements.txt`
- First-time setup: `./scripts/agentmail.sh setup`
- Create your own mailbox (see pattern below)

[AgentMail](https://agentmail.to) provides disposable email inboxes for AI agents. You create a mailbox, use the address in signup forms, then poll for incoming verification emails and extract OTP codes or links.

### The Pattern (Validated on Notion Signup)

```text
1. Create mailbox:     ./scripts/agentmail.sh create <username>
2. Fill signup form:   browser_fill(ref, "username@agentmail.to")
3. Submit form:        browser_click(ref)
4. Poll for email:     ./scripts/agentmail.sh poll username@agentmail.to --timeout 120
5. Extract OTP/link:   ./scripts/agentmail.sh extract <inbox_id> <msg_id>
6. Enter OTP:          browser_fill(ref, "123456")
7. Submit:             browser_click(ref)
```

### Gotchas
- Emails take 5-30 seconds to arrive. Always poll with timeout.
- Some services detect `agentmail.to` domain -- have backup strategy.
- OTP codes expire. Extract and submit promptly after polling.

### Validated Flows
- **Notion signup:** Full end-to-end -- signup, OTP poll, extract, submit, onboarding, page creation.
- **PKP forum:** Email verification worked. Blocked by moderator approval gate (external).

---

## Session Rules

**CRITICAL: No parallel browser sessions.**

- All tools share one browser daemon per session
- Parallel usage causes state collisions (one action navigates, another loses its page)
- Run browser tasks SEQUENTIALLY. Always.
- `AGENT_BROWSER_SESSION` env var controls session name (default: "mcp")
- Per-session isolation is NOT yet implemented

**Always close the browser when done:**
```text
browser_close()  -- releases the session for the next task
```

Forgetting to close leaves an orphaned Chromium process.

---

## Stealth Configuration

**Layer 1** provides basic stealth via environment variables. All browser sessions can run with headed mode, custom UA, persistent profile, and automation flag disabled.

For stricter sites, escalate to Layer 2+. Full guide: `./references/stealth-config.md`.

### Quick Setup (5 min, $0)
```bash
export AGENT_BROWSER_HEADED=1
export AGENT_BROWSER_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
export AGENT_BROWSER_PROFILE="$HOME/.agent-browser/profiles/stealth"
export AGENT_BROWSER_ARGS="--disable-blink-features=AutomationControlled"
mkdir -p ~/.agent-browser/profiles/stealth
```

### Escalation Path
1. **Layer 1** (env vars above) -- beats Cloudflare free tier
2. **Layer 2** (rebrowser-patches: `npx rebrowser-patches@latest patch`) -- beats Cloudflare Pro
3. **Layer 3** (Kernel cloud: `AGENT_BROWSER_PROVIDER=kernel`) -- beats most anti-bot
4. **Layer 4** (residential proxy: `AGENT_BROWSER_PROXY=...`) -- beats IP-based blocking

### Key Env Vars

| Env Var | Purpose | Default |
|---------|---------|---------|
| `AGENT_BROWSER_SESSION` | Session name for isolation | `mcp` |
| `AGENT_BROWSER_HEADED` | `"1"` = headed mode | off |
| `AGENT_BROWSER_USER_AGENT` | Custom UA string | Chromium default |
| `AGENT_BROWSER_ARGS` | Chromium launch args | none |
| `AGENT_BROWSER_PROFILE` | Persistent browser profile path | none |
| `AGENT_BROWSER_PROXY` | Proxy server URL | none |
| `AGENT_BROWSER_PROVIDER` | Cloud provider (kernel, browserbase) | none |

---

## Benchmark Results (Feb 2026)

15-task browser autonomy benchmark. **12/15 pass (100% excluding external blockers).**

| Capability | Tasks | Evidence |
|-----------|-------|----------|
| Login + session cookies | 1, 6, 9 | Sauce Demo, HN, quotes.toscrape |
| Multi-field registration | 2, 7 | 11-step account lifecycle |
| Complex form widgets | 3 | Date pickers, React Select, file upload |
| Drag-drop, alerts, iframes | 5, 14 | Multiple interaction types |
| Paginated scraping with session | 9 | 50 quotes across 5 pages |
| SaaS signup with email OTP | 12 | **Notion end-to-end** |
| OAuth redirect flow | 13 | GitHub OAuth chain |
| Google Flights SPA | 11 | Dynamic JS search + filter |
| Multi-site autonomous flow | 15 | Two sites, single session |
| Error recovery | 14 | Form validation, alerts, iframes |

3 failures (all external): SSL outage, Cloudflare transparent challenge, moderator gate.

### Test Suite v2 (10-Task Progressive)

| # | Tier | Task | Result | Calls | Time |
|---|------|------|--------|-------|------|
| 1 | Medium | Reddit scraping (old.reddit.com) | PASS | 14 | 25s |
| 2 | Medium | HN thread extraction | PASS | 13 | 35s |
| 3 | Medium | SauceDemo e-commerce flow | PASS | 38 | 61s |
| 4 | Hard | GitHub repo data extraction | PASS | 37 | 83s |
| 5 | Hard | Google Flights search + filter | PASS | 21 | 48s |
| 6 | Hard | HN account lifecycle | PASS | 22 | 39s |
| 7 | Brutal | Stripe iframe checkout | PASS | 59 | 168s |
| 8 | Brutal | Wikipedia multi-language | PASS | 11 | 63s |
| 9 | Brutal | Cloudflare stealth gauntlet | PASS | 12 | 36s |
| 10 | Final Boss | Linear E2E + AgentMail | PARTIAL | ~40 | ~180s |

Test 10 blocked by Cloudflare Turnstile CAPTCHA -- requires Layer 2+ stealth. Not an agent or skill gap.

---

## Quick Tool Reference

25 tools in 5 categories. Full details in `./references/tool-inventory.md`.

| Category | Tools |
|----------|-------|
| **Navigation** | `navigate`, `back`, `forward`, `reload` |
| **Observation** | `snapshot`, `screenshot`, `get_url`, `get_title`, `get_text`, `get_html` |
| **Interaction** | `click`, `dblclick`, `fill`, `type`, `press`, `select`, `hover`, `focus`, `clear`, `check`, `uncheck` |
| **Page** | `scroll`, `wait`, `evaluate` |
| **Session** | `close` |

All tool names are prefixed with `browser_` (e.g., `browser_click`, `browser_snapshot`).

### fill vs type

| Method | Behavior | Use when |
|--------|----------|----------|
| `browser_fill` | Clears field, sets value instantly | Standard form fields (95% of cases) |
| `browser_type` | Types character by character, triggers keystrokes | Autocomplete, search-as-you-type, custom widgets |

---

## Common Workflow Patterns

See `./references/battle-tested-patterns.md` for 12 complete patterns with examples.

| Pattern | Complexity | Key Technique |
|---------|-----------|---------------|
| Standard login | Low | fill + click + wait + snapshot |
| Multi-field registration | Medium | fill + select + check + click |
| SaaS signup with OTP | High | AgentMail create + fill + poll + extract + fill |
| Paginated scraping | Medium | snapshot(compact) + click(Next) loop |
| OAuth redirect | Medium | click(OAuth button) + wait + follow redirects |
| Error recovery | Medium | submit + snapshot(check errors) + fix + resubmit |
| SPA navigation | Medium | type(not fill) + wait + snapshot for dynamic content |
| Targeted extraction | Low | browser_evaluate(JS selector) |
| Multi-site flow | High | Multiple navigates, single session, screenshot evidence |
| Targeted DOM extraction | Low | browser_evaluate(JS selector) for JSON-LD and specific elements |
| Post-search verification | Medium | snapshot results + verify params + recovery loop |
| Calendar widget protocol | Medium | click date field + navigate months + click date cells |

---

## Health Check

Before starting browser work, verify the stack:

```bash
./scripts/browser-check.sh           # full check (CLI + daemon + stealth + agentmail)
./scripts/browser-check.sh quick     # just CLI + daemon
./scripts/browser-check.sh stealth   # stealth config status
```

---

## URL Pre-Population Pattern

For complex SPAs with autocomplete widgets, geo-defaults, or custom form components that resist `browser_type`:
- **Skip the form.** Navigate directly to a URL with parameters pre-encoded.
- **Google Flights example:** `https://www.google.com/travel/flights?q=Flights+from+SFO+to+NRT+on+2026-04-17+return+2026-05-01`
- **Why:** Custom React/Material autocomplete widgets often ignore `browser_type` input or revert to geo-defaults. URL params bypass the widget layer entirely.
- **When to use:** After 2-3 failed attempts to interact with a complex form widget. Don't fight the DOM -- go around it.

### iframe Bypass Pattern
When cross-origin iframes block `browser_fill`/`browser_type` (e.g., Stripe payment forms):
1. Snapshot the page and identify the iframe element
2. Use `browser_evaluate` to extract the iframe's `src` URL: `document.querySelector('iframe').src`
3. Navigate directly to that URL -- this renders the iframe content as a regular page
4. Interact with all fields normally using `browser_fill`/`browser_type`

### Evaluate-Only Mode for Heavy Pages
For content-heavy pages (Wikipedia, documentation sites, long articles):
- **Skip snapshots entirely.** The a11y tree will be massive and blow your token budget.
- Use `browser_evaluate` with targeted CSS selectors for all data extraction
- Common selectors: `document.querySelector('p').textContent`, `document.querySelectorAll('.reference').length`, `Array.from(document.querySelectorAll('h2')).map(e => e.textContent)`

---

## Playbooks

Per-site recipes with validated approaches. Load the relevant playbook before starting a task against a tested site.

| Playbook | Site | Status | Key Pattern |
|----------|------|--------|-------------|
| `references/playbooks/booking-com.md` | Booking.com | PASS (workaround) | Landmark search + hotel calendar pricing |
| `references/playbooks/google-flights.md` | Google Flights | PASS | URL pre-population (`?q=`) bypasses autocomplete |
| `references/playbooks/linear-signup.md` | Linear | PARTIAL | Blocked by Cloudflare Turnstile; requires Layer 3 |
| `references/playbooks/notion-signup.md` | Notion | PASS | Full E2E signup with AgentMail OTP verification |
| `references/playbooks/reddit-scraping.md` | Reddit | PASS | old.reddit.com + `?sort=hot` retry + evaluate extraction |
| `references/playbooks/stripe-iframe.md` | Stripe (iframe) | PASS | Extract iframe `src`, navigate directly, fill normally |
| `references/playbooks/cloudflare-sites.md` | Cloudflare (general) | Mixed | Decision tree: free tier (L1) vs Turnstile (L3) |
| `references/playbooks/wikipedia-extraction.md` | Wikipedia | PASS | Evaluate-only mode, zero snapshots, CSS selectors |
| `references/playbooks/headed-browser-setup.md` | (general) | Reference | Headed mode + persistent profile setup |

---

## Anti-Patterns

| Do NOT | Do instead |
|--------|------------|
| Use browser for static content (prices, articles) | `WebSearch` or `WebFetch` (built-in tools) |
| Use `snapshot(mode='full')` by default | Use `interactive` mode (10x cheaper) |
| Run parallel browser sessions | Run sequentially, one at a time |
| Forget `browser_close()` at end | Always close when done |
| Retry failed anti-bot sites blindly | Check `references/failure-log.md` first |
| Load browser tools for non-browser tasks | Only use browser when interaction is needed |
| Use `browser_type` when `browser_fill` works | `fill` is faster; `type` is for keystroke-sensitive inputs |
| Skip screenshot evidence | Screenshot at key milestones for verification |
| Use `browser_fill` for autocomplete fields | `browser_type` triggers keystroke events for suggestions |
| Attempt Cloudflare Turnstile sites at Layer 1 | Interactive CAPTCHA requires Layer 2+ stealth |

---

## Error Handling

Common browser automation errors and recovery strategies.

| Error | Symptoms | Recovery |
|-------|----------|----------|
| **Playwright timeout** | `TimeoutError: waiting for selector` or navigation timeout | Retry with longer `browser_wait` (double the timeout). Check if page is still loading. If persistent, the element may not exist -- re-snapshot to verify page state. |
| **Stale element ref** | Action fails on a previously valid `@eN` ref | Refs reset after any navigation or major DOM change. Re-run `browser_snapshot()` to get fresh refs, then retry the action with the new ref. |
| **Element not found** | `browser_click`/`browser_fill` fails -- ref not in snapshot | 1) Verify the page fully loaded (`browser_wait` or check URL). 2) Try a CSS selector fallback. 3) The element may be below the fold -- `browser_scroll(direction="down")` then re-snapshot. |
| **Network error** | Navigation fails, page doesn't load | Retry `browser_navigate` to the same URL. If persistent, check if site is down or blocking (see `references/failure-log.md`). |
| **Session collision** | Random failures, wrong page content, unexpected state | Another task is using the browser. Browser tasks must run SEQUENTIALLY. Close any orphaned sessions with `browser_close()` and retry. |
| **Anti-bot block** | Blank page, CAPTCHA, access denied, redirect to challenge page | Check `references/stealth-config.md` for escalation layers. Do not retry blindly -- escalate stealth level first. |
| **`browser_evaluate` syntax error** | `SyntaxError: Unexpected token` in eval expression | Do NOT use `return` keyword in `browser_evaluate` expressions -- eval expects a JS expression, not a statement. Use `document.title` not `return document.title`. |

**General principle:** When an action fails, always re-snapshot before retrying. The page state may have changed since your last observation.

---

## Bundled Resources Index

| Path | What | When to load |
|------|------|-------------|
| `./UPDATES.md` | Structured changelog for AI agents | When checking for new features or updates |
| `./UPDATE-GUIDE.md` | Instructions for AI agents performing updates | When updating this skill |
| `./references/installation-guide.md` | Detailed install walkthrough for Claude Code and Codex CLI | First-time setup or environment repair |
| `./references/tool-inventory.md` | Full 25-tool API reference with params and examples | When you need exact tool syntax |
| `./references/battle-tested-patterns.md` | 12 validated workflow patterns from benchmark | When building a new browser workflow |
| `./references/failure-log.md` | Benchmark results, anti-bot findings, AgentMail details | Before targeting a new site |
| `./references/stealth-config.md` | Anti-detection layered configuration guide | When hitting bot detection |
| `./references/test-results.md` | Full benchmark test cases (v1 + v2) with detailed logs | When reviewing what has been tested and what works |
| `./references/anti-detection-guide.md` | 4-tier stealth escalation with decision tree | When planning stealth strategy for a new target |
| `./references/playbooks/` | Per-site recipes with validated approaches | Before automating a tested site |
| `./references/playbooks/headed-browser-setup.md` | Profile setup, trust building, headed mode guide | When setting up headed browser for high-detection sites |
| `./scripts/agentmail.sh` | AgentMail CLI wrapper (setup/create/poll/extract) | For email verification flows |
| `./scripts/mailbox.py` | AgentMail Python SDK wrapper | Called by agentmail.sh (self-contained) |
| `./scripts/requirements.txt` | Python dependencies for AgentMail | Used by agentmail.sh setup |
| `./scripts/browser-check.sh` | Browser stack health check | Before first browser task in a session |
