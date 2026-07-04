# pagerunner-skill

Browser automation skill for Claude, powered by [Pagerunner](https://github.com/Enreign/pagerunner) MCP server.

Use Pagerunner to drive real Chrome with your existing profiles — authenticated, private, and running whether you're there or not.

## Quick Start

### Installation

```bash
# Coming soon: skills.sh registry
# For now, manual setup in your Claude Code config:
curl -sL https://raw.githubusercontent.com/Enreign/pagerunner-skill/main/SKILL.md -o SKILL.md
```

### Choose Your Path

**Solo Developer** (Claude Code / Cursor — close the implementation loop)
```javascript
const sessionId = await open_session({ profile: "personal" });
const [tab] = await list_tabs(sessionId);
await navigate(sessionId, tab.target_id, "http://localhost:3000");
await screenshot(sessionId, tab.target_id);  // see your code live
await close_session(sessionId);
```

**Power User** (OpenClaw / Hermes — autonomous tasks from your phone)
```
WhatsApp: "Check my Jira for blockers"
→ OpenClaw + Pagerunner
→ open_session(profile="agent-work")
→ restore_snapshot(...)  # already logged in
→ navigate → get_content → summarize
→ screenshot back to phone
```

**Security-Conscious** (NemoClaw / regulated industries — PII never reaches the LLM)
```javascript
open_session({
  profile: "agent",
  anonymize: true  // PII stripped before reaching you
  // john@company.com → [EMAIL:abc123]
});
```

**Server-Side** (Hermes + cron — persistent headless automation)
```javascript
pagerunner daemon &  // background service
// Agent A: scrape data → kv_set("checkpoint", data)
// Agent B: kv_get("checkpoint") → continue without re-auth
```

## Documentation

| Doc | Purpose |
|---|---|
| **[SKILL.md](SKILL.md)** | Main entry point — ICP quick starts, gotchas, core workflow |
| **[PATTERNS.md](PATTERNS.md)** | 11 workflow patterns (form filling, auth, scrolling, etc.) |
| **[REFERENCE.md](REFERENCE.md)** | All ~44 Pagerunner MCP tools with examples |
| **[SECURITY.md](SECURITY.md)** | Anonymization, audit log, encryption, domain allowlisting |
| **[HALLUCINATION_PREVENTION.md](HALLUCINATION_PREVENTION.md)** | Why arrays cause hallucinations + how metadata fixes it |
| **[DEBUGGING.md](DEBUGGING.md)** | Troubleshooting common issues |
| **[EXAMPLES.md](EXAMPLES.md)** | 4 full ICP workflows + multi-agent patterns |
| **[ADVANCED.md](ADVANCED.md)** | Multi-agent coordination, daemon lifecycle, session persistence (v0.6), auto-recovery (v0.7), retention |
| **[RECORDING.md](RECORDING.md)** | Director's guide to making great videos (v0.8) — bug repros, feature demos, onboarding tutorials |

## What is Pagerunner?

Real Chrome browser automation for AI agents. Not mocked, not cloud.

**Key features:**
- Real authenticated browser (uses your existing Chrome profiles)
- MCP-native (Claude Code, Cursor, Windsurf, Cline, any MCP client)
- PII anonymization (email, phone, credit card tokens instead of raw values) — plus credential scrubbing + entropy-based gap detection
- Sealed-secret trust boundary — tokens extracted from pages are injected into subprocesses via stdin; the raw value never reaches the LLM or audit log
- Site intelligence — learned JS adapters + auth token vault for direct API calls against logged-in sites
- Session checkpoints + auto-reattach — full tab state survives daemon restart, Chrome crash, and sleep/wake
- Network + console capture (`get_network_log`, `get_console_log`)
- Video recording (v0.8) — MP4 with auto-zoom, cursor tracking, markers, Screen Studio-quality rendering (ffmpeg)
- Encrypted local state (AES-256-GCM)
- Persistent daemon (multi-agent coordination via KV store)
- Audit logging (compliance trail for every action, `AnonymizationGap` events on residual PII)
- Domain allowlisting (per-session containment)
- Stealth mode (hides automation signals)

See [comparison](https://github.com/Enreign/pagerunner-promo/blob/main/competitive/comparison.md) vs agent-browser, Playwright, Chrome DevTools, and others.

## Setup

### 1. Install Pagerunner

```bash
# macOS (Homebrew — easiest)
brew tap enreign/pagerunner
brew install pagerunner

# Or Cargo
cargo install pagerunner

# Or pre-built binary
# See: https://github.com/Enreign/pagerunner#setup
```

### 2. Register as MCP server

```bash
# Claude Code CLI
claude mcp add pagerunner "$(which pagerunner)" mcp

# Or Claude Desktop: add to ~/Library/Application Support/Claude/claude_desktop_config.json
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
# Reads your Chrome profiles and writes ~/.pagerunner/config.toml
```

**Note:** Chrome locks profile directories. Close any Chrome window before opening a Pagerunner session on that profile.

## The 4 ICPs (Ideal Customer Profiles)

| ICP | Tool | Use Case | Killer Feature |
|---|---|---|---|
| Solo Developer | Claude Code / Cursor | Close implementation loop | Real profile, already authed |
| Power User | OpenClaw / Hermes | Autonomous mobile-triggered tasks | Agent profile + snapshots + daemon |
| Security-Conscious | NemoClaw / enterprise | PII never reaches LLM | Anonymization + local NER + audit log |
| Server-Side | Hermes / cron | Persistent headless automation | Daemon + KV store + snapshots |

**Learn more:** Start with SKILL.md, find your ICP quick start.

## vs Other Tools

### agent-browser
- ✅ Wider traction (23.9K stars), cloud mode, headless Chromium
- ❌ CLI-first (not MCP-native), no PII anonymization, failed Snyk audit

**Pagerunner:** MCP-first, security-forward, PII protection built-in.

### Playwright MCP
- ✅ Cross-browser, accessibility snapshots
- ❌ No encrypted state, no PII anonymization, no multi-agent coordination

**Pagerunner:** Real-world authenticated workflows + security layer.

### Chrome DevTools MCP
- ✅ Debugging tools (Lighthouse, traces)
- ❌ Not an automation tool, requires human presence

**Pagerunner:** Automation tool for independent agent execution.

## Examples

**Screenshot a form and verify it matches design spec** (Claude Code):
```javascript
// Claude edits CSS, verifies button color changed
await navigate(sessionId, tabId, "http://localhost:3000");
await screenshot(sessionId, tabId);  // "button is now green ✓"
```

**Check Jira from your phone while in a meeting** (OpenClaw):
```
"Check my Jira for blockers"
→ WhatsApp → OpenClaw → Pagerunner → real Jira session
→ "3 tickets blocking release" → back to WhatsApp
```

**Automate workflow on client data without PII exposure** (NemoClaw):
```javascript
// Even though get_content reads emails, Claude never sees them
const content = await get_content(sessionId, tabId);
// Result: "Contact [EMAIL:abc123]" instead of "john@company.com"
```

**Cron job: daily Jira standup summary** (Hermes):
```bash
0 8 * * * pagerunner navigate ... && pagerunner get-content ... | jq '.summary'
```

## Security

- **PII anonymization**: Regex + local NER (PERSON/ORG via ONNX model, never leaves your machine)
- **Tokenize mode**: `john@company.com` → `[EMAIL:tok123]` → agent works with tokens → de-tokenizes on fill
- **Audit log**: Append-only JSON-lines record of every browser action
- **Encrypted state**: AES-256-GCM for snapshots, KV store, sessions (key in macOS Keychain)
- **Domain allowlisting**: Per-session containment (agent can't wander to unauthorized sites)
- **SSRF protection**: Blocks navigation to private IPs, loopback, `file://`, `javascript:`
- **Injection sanitization**: Strips hidden HTML, zero-width unicode, wraps untrusted content in markers

See [SECURITY.md](SECURITY.md) for details.

## Troubleshooting

- **Selector not found after navigation?** Use `wait_for` before clicking.
- **Fill didn't update the input?** Use `fill()` for React apps, not `type_text()`.
- **Something broke?** See [DEBUGGING.md](DEBUGGING.md).

## Contributing

Contributions welcome. See [pagerunner main repo](https://github.com/Enreign/pagerunner/blob/main/CONTRIBUTING.md) for guidelines.

## License

MIT

---

**Questions?** Start with [SKILL.md](SKILL.md) — find your ICP quick start and go from there.

**Want to report an issue with Pagerunner itself?** See [pagerunner repo](https://github.com/Enreign/pagerunner/issues).

**Skill feedback?** Open an issue here.
