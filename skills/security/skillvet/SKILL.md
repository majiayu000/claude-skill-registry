---
name: skillvet
description: "Security scanner for ClawHub/community skills — detects malware, credential theft, exfiltration, prompt injection, and obfuscation before you install. Use when installing skills from ClawHub or any public marketplace, reviewing third-party agent skills for safety, or vetting untrusted code before giving it to your AI agent. Triggers: install skill, audit skill, check skill, vet skill, skill security, safe install, is this skill safe."
---

# Skillvet

Anyone can publish a skill to ClawHub. That's what makes it powerful — and risky. A single malicious skill can steal your API keys, exfiltrate your environment variables, inject prompts into your agent, or open a reverse shell on your machine.

Skillvet scans skills **before** you use them. It runs 24 critical checks and 8 warning checks against every file in a skill directory, looking for credential theft, data exfiltration, prompt injection, obfuscation, and more. No dependencies — just bash and grep.

## Usage

**Safe install** — installs a skill, audits it, and auto-removes it if critical issues are found:

```bash
bash skills/skillvet/scripts/safe-install.sh <skill-slug>
```

**Scan before installing** — downloads a skill to a temp directory, scans it, deletes it:

```bash
bash skills/skillvet/scripts/scan-remote.sh <skill-slug>
```

**Audit a skill you already have:**

```bash
bash skills/skillvet/scripts/skill-audit.sh skills/some-skill
```

**Audit every installed skill:**

```bash
for d in skills/*/; do bash skills/skillvet/scripts/skill-audit.sh "$d"; done
```

**Diff scan** — after an update, scan only what changed between versions:

```bash
bash skills/skillvet/scripts/diff-scan.sh skills/old-version skills/new-version
```

Exit codes: `0` clean, `1` warnings only, `2` critical findings (blocked).

### Output formats

All scripts accept `--json` for structured output and `--summary` for a single-line result.

```bash
# JSON — for CI pipelines and dashboards
bash skills/skillvet/scripts/skill-audit.sh --json skills/some-skill

# Summary — for batch scanning and notifications
for d in skills/*/; do bash skills/skillvet/scripts/skill-audit.sh --summary "$d"; done
```

## What it catches

### Critical — skill is blocked

| Check | What it looks for |
|-------|-------------------|
| Exfiltration endpoints | URLs pointing to webhook.site, ngrok.io, requestbin, etc. |
| Env variable harvesting | Bulk dumping of your shell environment |
| Foreign credential access | Reading API keys the skill doesn't own (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.) |
| Code obfuscation | Dynamic code evaluation, base64 decode, hex escape sequences |
| Path traversal | Reaching outside the skill directory into ~/.ssh, ~/.aws, /etc/passwd |
| Data exfiltration | Sending captured data out via curl or wget |
| Reverse/bind shells | Network backdoors via /dev/tcp, netcat, socat |
| .env file theft | Loading .env files from scripts (not just referencing them in docs) |
| Prompt injection | "Ignore previous instructions" and similar overrides in markdown |
| LLM tool exploitation | Instructing the agent to send, email, or post secrets |
| Agent config tampering | Writing to AGENTS.md, SOUL.md, clawdbot.json, .bashrc |
| Unicode obfuscation | Zero-width characters, RTL overrides that hide content |
| Suspicious setup commands | Piping remote scripts to a shell interpreter in SKILL.md |
| Social engineering | Telling users to download executables or run code from paste sites |
| Shipped .env files | Actual .env files (not .example) included in the skill |
| Homograph characters | Cyrillic letters mimicking Latin (e.g., Cyrillic `a` posing as Latin `a` in URLs) |
| ANSI escape injection | Raw terminal escape sequences in markdown, JSON, or YAML files |
| Punycode domains | xn-- encoded IDN labels that may hide homograph attacks |
| Double-encoded paths | %25-based percent-encoding bypass attempts |
| Shortened URLs | bit.ly, t.co, tinyurl, etc. in code — hides true destination |
| Insecure pipe-to-shell | HTTP (no TLS) piped to a shell interpreter |
| String construction evasion | Building dangerous calls from fragments (`'ev'+'al'`, bracket notation, `String.fromCharCode`, `getattr`) |
| Data flow chain analysis | Same file reads secrets/env, encodes data, AND sends network requests — exfiltration pipeline |
| Time bomb detection | Date-gated or long-delayed execution (`Date.now() > epoch`, `setTimeout` with 8+ digit delay, `schedule.every().days`) |

### Warnings — flagged for manual review

| Check | What it looks for |
|-------|-------------------|
| Subprocess spawning | Code that launches child processes or shell commands |
| Network requests | HTTP client libraries (axios, fetch, requests, httpx) |
| Minified/bundled files | JS/TS files with very long lines that can't be audited by eye |
| File write operations | Code that writes to the filesystem |
| Unknown external tools | CLI tools referenced in docs that aren't on the known-safe list |
| Insecure transport | Disabled TLS certificate verification |
| Raw IP URLs | HTTP to non-private IPs — bypasses DNS, harder to trace |
| Untrusted Docker registries | Docker pull/run from third-party registries |

## Limitations

This is static analysis — pattern matching with grep. It raises the bar significantly but doesn't guarantee safety. Minified JS is flagged but not deobfuscated. Prompt injection detection is English-centric.

The scanner flags itself when audited. Its own source code contains the patterns it detects. This is expected.
