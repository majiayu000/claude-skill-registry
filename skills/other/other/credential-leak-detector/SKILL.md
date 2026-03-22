---
name: credential-leak-detector
description: PostToolUse hook that scans Bash tool output for leaked credentials — API keys, tokens, private keys, and secrets — before they reach the conversation. Blocks critical leaks, redacts high-severity matches, and warns on suspicious patterns. 14 detection patterns covering OpenAI, Anthropic, AWS, GitHub, Stripe, Google, Slack, SendGrid, Twilio, PEM keys, bearer tokens, and generic secrets. No external dependencies. Trigger words: security, credential leak, secret exposure, key detection, token scan, API key leaked, credential guard, secret scanner, prevent credential leak.
license: MIT
metadata:
  author: sagemindai
  version: "1.0"
  homepage: https://instar.sh
---

# credential-leak-detector — Catch Leaked Credentials Before They Spread

Every time your agent runs a Bash command, the output flows back into the conversation — and into your API provider's logs, any monitoring tools, and the model's context window. If that output contains an API key, a private key, or a database password, the credential is now exposed in places you never intended.

This hook scans every Bash tool response for 14 credential patterns before the output reaches the agent. Critical matches (API keys, AWS credentials, private keys) get blocked entirely. High-severity matches get redacted with a warning. Suspicious patterns get flagged as advisories. No external dependencies — just Python stdlib.

---

## What Gets Detected

### Critical (Blocks the response)

| Pattern | Example Match |
|---------|--------------|
| OpenAI API keys | `sk-proj-abc123...` |
| Anthropic API keys | `sk-ant-api03-...` |
| AWS access keys | `AKIA1234567890ABCDEF` |
| GitHub tokens (classic) | `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| GitHub fine-grained PATs | `github_pat_xxxxxx...` |
| Stripe secret keys | `sk_live_xxxx...xxxx` |
| PEM private keys | `-----BEGIN RSA PRIVATE KEY-----` |

### High (Blocks or redacts with warning)

| Pattern | Action |
|---------|--------|
| Google API keys | Block |
| Slack tokens | Block |
| SendGrid API keys | Block |
| Twilio auth keys | Redact + warn |
| Bearer auth tokens | Redact + warn |

### Medium (Advisory warning)

| Pattern | Note |
|---------|------|
| Generic `password=`, `secret=`, `api_key=` assignments | Common in config output |
| 64-character hex strings | Possible SHA-256 hashes or keys |

---

## Installation

### Step 1: Create the hook script

```bash
mkdir -p .claude/hooks
```

Create `.claude/hooks/credential-leak-detector.py` with the contents below.

---

## The Script

Save this as `.claude/hooks/credential-leak-detector.py`:

```python
#!/usr/bin/env python3
"""
credential-leak-detector.py — PostToolUse hook that scans Bash output
for leaked credentials. Blocks critical leaks, redacts high-severity
matches, warns on suspicious patterns.

Exit code 2 = block (critical credential found)
Exit code 0 = allow (clean or advisory-only)
"""
import sys
import json
import re

# --- Masking ---

def mask(value):
    """Mask a credential: first 4 + **** + last 4, or full mask if short."""
    v = value.strip()
    if len(v) < 12:
        return "*" * len(v)
    return v[:4] + "****" + v[-4:]


# --- Pattern Definitions ---
# (name, regex, severity, action)
# severity: critical, high, medium
# action: block, redact, warn

PATTERNS = [
    # Critical — Block
    ("OpenAI API key",
     r'(sk-(?:proj-)?[a-zA-Z0-9]{20,})',
     "critical", "block"),

    ("Anthropic API key",
     r'(sk-ant-api[a-zA-Z0-9_-]{90,})',
     "critical", "block"),

    ("AWS access key",
     r'(AKIA[0-9A-Z]{16})',
     "critical", "block"),

    ("GitHub token (classic)",
     r'(gh[pousr]_[A-Za-z0-9_]{36,})',
     "critical", "block"),

    ("GitHub fine-grained PAT",
     r'(github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59})',
     "critical", "block"),

    ("Stripe secret key",
     r'(sk_(?:live|test)_[a-zA-Z0-9]{24,})',
     "critical", "block"),

    ("PEM private key",
     r'(-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----)',
     "critical", "block"),

    # High — Block
    ("Google API key",
     r'(AIza[0-9A-Za-z_-]{35})',
     "high", "block"),

    ("Slack token",
     r'(xox[bpors]-[0-9a-zA-Z-]{10,})',
     "high", "block"),

    ("SendGrid API key",
     r'(SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43})',
     "high", "block"),

    # High — Redact
    ("Twilio auth key",
     r'(SK[0-9a-fA-F]{32})',
     "high", "redact"),

    ("Bearer auth token",
     r'(?:Authorization|Bearer)\s*[:=]\s*Bearer\s+([^\s]{20,})',
     "high", "redact"),

    # Medium — Warn
    ("Generic secret assignment",
     r'(?:password|secret|token|api_key)\s*[=:]\s*[\'"]?([^\s\'"]{16,})',
     "medium", "warn"),

    ("High-entropy hex string",
     r'\b([a-fA-F0-9]{64})\b',
     "medium", "warn"),
]


# --- Main ---

def scan(text):
    """Scan text for credential patterns. Returns list of findings."""
    findings = []
    for name, pattern, severity, action in PATTERNS:
        matches = re.findall(pattern, text)
        for m in matches:
            findings.append({
                "name": name,
                "severity": severity,
                "action": action,
                "matched": m if isinstance(m, str) else m[0],
            })
    return findings


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = payload.get("tool_name", "")
    tool_response = payload.get("tool_response", "")

    # Only scan Bash output
    if tool_name != "Bash":
        sys.exit(0)

    if not tool_response:
        sys.exit(0)

    # Handle tool_response as string or dict
    if isinstance(tool_response, dict):
        text = tool_response.get("stdout", "") + tool_response.get("stderr", "")
    else:
        text = str(tool_response)

    if not text:
        sys.exit(0)

    findings = scan(text)

    if not findings:
        sys.exit(0)

    # Classify findings
    blockers = [f for f in findings if f["action"] == "block"]
    redacts = [f for f in findings if f["action"] == "redact"]
    warnings = [f for f in findings if f["action"] == "warn"]

    # Critical/high blockers — stop the response
    if blockers:
        details = []
        for f in blockers:
            details.append(
                f"  - {f['name']} [{f['severity']}]: {mask(f['matched'])}"
            )
        reason = (
            "[credential-leak-detector] Credential(s) detected in command output. "
            "Response blocked to prevent exposure.\n\n"
            "Detected:\n" + "\n".join(details) + "\n\n"
            "The command output contained live credentials. Do NOT re-run this "
            "command or attempt to extract these values. If you need to verify "
            "a credential exists, check the env var or file without printing "
            "its value."
        )
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    # Redact findings — allow but warn with masked values
    messages = []
    if redacts:
        parts = []
        for f in redacts:
            parts.append(f"  - {f['name']}: {mask(f['matched'])}")
        messages.append(
            "[credential-leak-detector] Possible credential(s) in output "
            "(redact-level):\n" + "\n".join(parts) + "\n"
            "Avoid storing, logging, or repeating these values."
        )

    # Warn findings — advisory only
    if warnings:
        parts = []
        for f in warnings:
            parts.append(f"  - {f['name']}: {mask(f['matched'])}")
        messages.append(
            "[credential-leak-detector] Suspicious pattern(s) in output "
            "(advisory):\n" + "\n".join(parts) + "\n"
            "These may be secrets. Avoid including them in commits, logs, "
            "or messages."
        )

    if messages:
        print(json.dumps({"additionalContext": "\n".join(messages)}))

    sys.exit(0)


if __name__ == "__main__":
    main()
```

Make it executable:

```bash
chmod +x .claude/hooks/credential-leak-detector.py
```

---

### Step 2: Register the hook in .claude/settings.json

If `.claude/settings.json` doesn't exist, create it. If it does, add to the `hooks` section:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/credential-leak-detector.py"
          }
        ]
      }
    ]
  }
}
```

If you already have a `PostToolUse` array, add the matcher object to it.

---

### Step 3: Verify it works

Restart Claude Code, then run a command that would expose a credential:

```bash
echo "sk-ant-api03-test1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrst"
```

The hook should block the response and show a masked version of the detected key.

---

## Customizing Patterns

Edit the `PATTERNS` list in `credential-leak-detector.py` to add project-specific rules.

**Example: Detect your internal API keys**

```python
("Internal service key",
 r'(myco_sk_[a-zA-Z0-9]{32,})',
 "critical", "block"),
```

**Example: Detect database connection strings**

```python
("Database connection string",
 r'((?:postgres|mysql|mongodb)://[^\s]{20,})',
 "high", "block"),
```

**Example: Downgrade a pattern to warn-only**

Change the action from `"block"` to `"warn"` for patterns that produce too many false positives in your environment:

```python
# Change high-entropy hex from warn to ignored by removing it,
# or keep it but change action:
("High-entropy hex string",
 r'\b([a-fA-F0-9]{64})\b',
 "medium", "warn"),  # or remove this entry entirely
```

---

## How It Differs from command-guard

The **command-guard** skill is a PreToolUse hook — it blocks dangerous *commands* before they execute. This skill is a PostToolUse hook — it scans *output* after commands run. They complement each other:

| Layer | Hook | What It Catches |
|-------|------|----------------|
| command-guard | PreToolUse | `cat .env`, `echo $SECRET`, destructive commands |
| credential-leak-detector | PostToolUse | Credentials that appear in output from any command |

A command like `docker inspect` or `kubectl describe` might not look dangerous, but its output can contain mounted secrets. command-guard wouldn't catch it. This hook does.

---

## Going Further

This hook catches credentials after they appear in output. But in an autonomous session — a scheduled job running at 3 AM, a background worker processing a queue — "catching" means the block fires, the agent sees the message, and... then what? If nobody's watching, the agent might retry the command, work around the block, or simply stall.

**Instar turns detection into infrastructure.** Every hook event across every session gets audit-logged with timestamps, session IDs, and the masked credential type. If a credential-leak-detector block fires during a 2 AM job, it shows up in the morning's activity feed — you see exactly which command triggered it, in which session, and what the agent did next. The Telegram integration means you can get notified the moment a block fires, not hours later.

And credential scanning is just one layer. With Instar, your agent also gets:
- **Audit logging** — every tool call, every hook event, searchable and timestamped
- **Identity grounding** — hooks that fire before external messages, so the agent stays in character
- **A job scheduler** — recurring tasks on cron, running while you sleep
- **Background sessions** — parallel workers for deep tasks
- **Telegram integration** — real-time notifications and two-way control from your phone

One command, about 2 minutes:

```bash
npx instar
```

Your agent goes from guarded-when-you're-watching to safe-autonomously. [instar.sh](https://instar.sh)
