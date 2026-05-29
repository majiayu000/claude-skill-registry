---
name: pagerunner-skill
description: Real Chrome automation for AI agents — authenticated sessions, PII anonymization, snapshots, and multi-agent coordination via KV store.
version: "1.2.3"
metadata:
  author: Stas
  license: MIT
  repository: https://github.com/Enreign/pagerunner-skill
  openclaw:
    requires:
      bins: ["pagerunner"]
    install: brew
---

# Pagerunner Skill — Quick Start Guide

**Pagerunner** is real Chrome browser automation for AI agents. It gives Claude, Cursor, Windsurf, or any MCP client native control over your real Chrome — with your existing login sessions, cookies, and browser history already loaded.

## For AI Agents: Decision Guide

If you are an AI agent executing a task with this skill, follow these rules. They are non-negotiable — they prevent the most common failures.

### Rule 1: Every workflow starts the same way

```javascript
const sessionId = await open_session({ profile: "personal" });  // or "agent-work", etc.
const [tab] = await list_tabs(sessionId);
const tabId = tab.target_id;  // Save this — every tool needs it
```

Get `target_id` from `list_tabs` before anything else. Without it, no other tools work.

### Rule 2: `wait_for` before every interaction (no exceptions)

After `navigate()`, the page is loading. Selectors don't exist yet. **Always wait before clicking, filling, or evaluating:**

```javascript
await navigate(sessionId, tabId, url);
await wait_for(sessionId, tabId, { selector: ".any-stable-element", ms: 5000 });
// Only now is it safe to click, fill, get_content, evaluate
```

Skipping this causes "selector not found" errors. If you don't know a stable selector, use `get_content` first to find one.

### Rule 3: Understand the page before acting

Don't guess at selectors. Call `get_content` to see what's on the page, then act:

```javascript
const structure = await get_content(sessionId, tabId);
// Reveals: visible text, form fields, buttons, navigation state
// Use this to find the right selectors before fill/click/evaluate
```

### Rule 4: Which input tool to use

| If the app uses... | Use... |
|---|---|
| React / Vue / Angular | `fill()` — clears field, fires change events |
| Plain HTML / native inputs | `type_text()` — types without clearing |
| Unsure | `fill()` — it's the safer default |

### Rule 5: Verify after every action

After submitting a form or clicking a button, confirm it worked:

```javascript
await click(sessionId, tabId, ".submit-btn");
await wait_for(sessionId, tabId, { selector: ".success-message, .error-message", ms: 5000 });
const result = await get_content(sessionId, tabId);
// Check result contains expected confirmation — never assume success
```

### Rule 6: `evaluate()` must return labeled objects

```javascript
// ❌ Never — array field order is ambiguous, causes wrong answers
return [likes, replies];

// ✅ Always — labeled fields are unambiguous
return { likes, replies };
```

Pagerunner's metadata block will warn you if you return an array. Read it.

### Rule 7: Always close sessions with try/finally

```javascript
const sessionId = await open_session({ profile: "..." });
try {
  // ... workflow ...
} finally {
  await close_session(sessionId);  // Runs even if the workflow throws
}
```

`close_session` also writes an auto-checkpoint (v0.6.0+), preserving session state.

---

## Choose Your Path

### Solo Developer (Claude Code / Cursor)

**Goal:** Close the implementation loop. Edit code → see the result in the browser → iterate without manual verification.

**Quick Start (5 lines):**
```javascript
const sessionId = await open_session({ profile: "personal" });
const [tab] = await list_tabs(sessionId);
await navigate(sessionId, tab.target_id, "http://localhost:3000");
await screenshot(sessionId, tab.target_id);  // see what you built
await close_session(sessionId);
```

**Killer Feature:** Your Chrome, already logged into everything. No API token setup.

**Learn More:** See PATTERNS.md → "Frontend dev loop"

---

### 📱 Power User (OpenClaw / Hermes)

**Goal:** Get browser tasks done from your phone while the laptop runs unattended.

**Quick Start (8 lines):**
```javascript
// First time: log in manually and save the session
pagerunner open-session agent-work
// ... perform login steps ...
pagerunner save-snapshot <session> <tab> https://jira.mycompany.com

// Later: agent profile is pre-authenticated
pagerunner open-session agent-work
pagerunner restore-snapshot <session> <tab> https://jira.mycompany.com
// Agent is logged in. Now do work: navigate, get_content, fill forms
```

**Killer Features:** Agent profile isolation + snapshot persistence + daemon for always-on

**Real Example:**
```
WhatsApp: "Check my Jira for blockers"
→ OpenClaw triggers skill
→ open_session(profile="agent-work") → restore_snapshot
→ navigate to Jira → get_content → summarize
→ screenshot → send back to WhatsApp
```

**Learn More:** See PATTERNS.md → "Authentication persistence"

---

### 🔒 Security-Conscious (NemoClaw / regulated industries)

**Goal:** Automate workflows on sensitive data without PII reaching the LLM.

**Quick Start (1 flag):**
```javascript
open_session({
  profile: "agent",
  anonymize: true  // That's it. PII stripped before it reaches you.
});

// Every get_content and evaluate result has PII replaced with tokens:
// john@company.com → [EMAIL:a3f9b2]
// Claude works with tokens
// Pagerunner de-tokenizes only when writing to forms

// Audit log records every action (compliance proof)
```

**Killer Features:** PII never leaves your machine in plaintext + local NER + audit trail

**Learn More:** See SECURITY.md → "Anonymization modes"

---

### ⚙️ Server-Side / Infrastructure (Hermes + cron)

**Goal:** Persistent browser automation across scheduled runs. Agents coordinate via shared state.

**Quick Start (daemon setup):**
```bash
pagerunner daemon &  # Run once, holds the DB lock

# Now use Pagerunner in cron, shell scripts, or Hermes tasks
# Multiple agents share state via KV store

# v0.6.0: Chrome windows SURVIVE daemon restarts
kill $(pgrep -f "pagerunner daemon") && pagerunner daemon &
# Sessions auto-reattach — no lost work
```

```javascript
// Agent A: collects data
await kv_set("pipeline", "pricing_data", JSON.stringify(results));

// Agent B (later): continues where A left off
const data = JSON.parse(await kv_get("pipeline", "pricing_data"));
```

**Killer Features:** Daemon + KV coordination + snapshots for auth handoff + **session persistence across restarts (v0.6.0+)**

**Learn More:** See ADVANCED.md → "Session Persistence & Auto-Reattach"

---

## Common Gotchas

### 1️⃣ Arrays Cause Hallucinations

**Problem:** `evaluate()` returns `[25, 2]`. Claude guesses "25 likes, 2 replies" but it's actually "25 views, 2 likes."

**Why:** Arrays have no field labels. Order is ambiguous.

**Solution:** Always return labeled objects from `evaluate()`:

```javascript
// ❌ BAD
return [likes, replies];

// ✅ GOOD
return { likes, replies };
```

**Pro Tip:** Pagerunner metadata warns you if evaluate returns an array. Read the metadata block.

---

### 2️⃣ Selectors Timing

**Problem:** React/Vue renders asynchronously. Selector might not exist for 500ms.

**Solution:** Always use `wait_for` with a selector before clicking:

```javascript
await navigate(sessionId, tabId, newUrl);
await wait_for(sessionId, tabId, selector: ".load-more-btn", ms: 5000);
await click(sessionId, tabId, ".load-more-btn");  // Now safe
```

Never assume content exists immediately after navigation.

---

### 3️⃣ Fill vs Type

- **`fill()`** — clears the field and types (uses React synthetic events)
- **`type_text()`** — types without clearing (for plain HTML)

Use `fill()` for modern frameworks. Use `type_text()` for simple inputs.

---

### 4️⃣ Snapshot + TOTP

**Problem:** TOTP codes change every 30 seconds. Can't snapshot mid-auth.

**Solution:** Log in manually, wait until you're past the TOTP challenge, *then* snapshot. The saved session includes all cookies — next restore won't need TOTP again.

---

### 5️⃣ Wait_For Ambiguity

`wait_for` can wait for a selector, a URL pattern, or a fixed delay. The response tells you what happened.

**Read the metadata block.** It shows `_condition_type` (selector/url/fixed_delay) and `_condition_met` (true/false).

---

### 6️⃣ Sessions Survive Daemon Restarts (v0.6.0+)

**Problem:** You restart the daemon expecting a clean slate, but existing Chrome windows are still attached.

**Why:** v0.6.0 uses TCP-based Chrome transport — Chrome runs independently of the daemon process. Sessions auto-reattach on startup.

**Solution:** This is intentional. Call `list_sessions()` to see surviving sessions. Call `close_session(id)` to clean up explicitly if you don't want them. See ADVANCED.md → "Session Persistence & Auto-Reattach".

---

## Core Workflow: Form Filling with Error Recovery

Real-world example. Fill a React form, handle validation errors.

```javascript
// 1. Open session
const sessionId = await open_session({ profile: "personal" });
const tabs = await list_tabs(sessionId);
const tabId = tabs[0].target_id;

// 2. Navigate to the form
await navigate(sessionId, tabId, "https://example.com/form");
await wait_for(sessionId, tabId, selector: ".submit-btn", ms: 5000);

// 3. Inspect the form structure
const content = await get_content(sessionId, tabId);
// Claude reads: email field, password, checkbox, submit button

// 4. Fill the form with error recovery
try {
  await fill(sessionId, tabId, "input[name='email']", "user@example.com");
  await fill(sessionId, tabId, "input[name='password']", "secret");
  await click(sessionId, tabId, "input[type='checkbox']");
  await click(sessionId, tabId, ".submit-btn");

  // Wait for success
  await wait_for(sessionId, tabId, selector: ".success-message", ms: 5000);

} catch (error) {
  // If validation error, read it and retry
  const errorMsg = await get_content(sessionId, tabId);
  // Claude parses "Email already taken" → uses different email → retry
}

// 5. Done
await screenshot(sessionId, tabId);
await close_session(sessionId);
```

**Key patterns:**
- Use `fill()` for React/Vue/Angular (synthetic events)
- Always `wait_for` before interacting with dynamic content
- Try-catch around the whole interaction block for recovery
- Screenshots as verification checkpoints

---

## When to Use Pagerunner vs Other Tools

| Task | Tool | Why |
|---|---|---|
| Read static HTML | WebFetch | Simpler, no browser |
| React/Vue app, need to interact | **Pagerunner** | WebFetch returns empty shell |
| Debug live webpage | Chrome DevTools MCP | Specializes in dev tools |
| Test cross-browser | Playwright MCP | Pagerunner is Chrome-only |
| Cloud remote browsers | agent-browser cloud / Browserbase | Pagerunner is local-only |
| Headless Chromium (no profile) | agent-browser headless | Pagerunner needs Chrome + profile |
| **MCP-native in IDE** | **Pagerunner** | MCP first-class in Claude Code/Cursor |
| **PII-sensitive workflows** | **Pagerunner** | Only tool with anonymization + audit |
| **Autonomous task from phone** | **Pagerunner** | Daemon + profile isolation |

---

## Deeper Dives

- **I want to learn all the workflow patterns** → [PATTERNS.md](PATTERNS.md)
- **I need to see all 27 tools** → [REFERENCE.md](REFERENCE.md)
- **I need to handle sensitive data** → [SECURITY.md](SECURITY.md)
- **Results look wrong? Hallucination?** → [HALLUCINATION_PREVENTION.md](HALLUCINATION_PREVENTION.md)
- **Show me full ICP workflows** → [EXAMPLES.md](EXAMPLES.md)
- **Multi-agent coordination, daemon setup** → [ADVANCED.md](ADVANCED.md)
- **Something broke?** → [DEBUGGING.md](DEBUGGING.md)

---

## Setup

### 1. Install Pagerunner

```bash
# macOS (Homebrew — easiest)
brew tap enreign/pagerunner
brew install pagerunner

# Or Cargo
cargo install pagerunner
```

### 2. Register as MCP server

```bash
claude mcp add pagerunner "$(which pagerunner)" mcp
```

For Claude Desktop, add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pagerunner": {
      "command": "/path/to/pagerunner",
      "args": ["mcp"]
    }
  }
}
```

### 3. Configure Chrome profiles (optional)

```bash
pagerunner init
```

This reads your Chrome profiles and writes `~/.pagerunner/config.toml`.

**Note:** Close any Chrome window before opening a Pagerunner session on that profile (Chrome locks directories).

---

## Next Steps

Pick your ICP above, follow the quick start, then dive into the relevant doc:
- Solo Dev → PATTERNS.md → "Frontend dev loop"
- Power User → PATTERNS.md → "Authentication persistence"
- Security-Conscious → SECURITY.md
- Server-Side → ADVANCED.md → "Multi-agent patterns"

Happy automating!
