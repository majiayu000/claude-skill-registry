---
name: arbiter
description: Push decisions to Arbiter Zebu for async human review. Use when you need human input on plans, architectural choices, or approval before proceeding.
metadata: {"openclaw":{"requires":{"bins":["arbiter-push"]}}}
---

# Arbiter Skill

Push decisions to Arbiter Zebu for async human review. Use when you need human input on plans, architectural choices, or approval before proceeding.

## Installation

**Quick install via ClawHub:**
```bash
clawhub install arbiter
```

**Or via bun (makes CLI commands available globally):**
```bash
bun add -g arbiter-skill
```

**Or manual:**
```bash
git clone https://github.com/5hanth/arbiter-skill.git
cd arbiter-skill && npm install && npm run build
ln -s $(pwd) ~/.clawdbot/skills/arbiter
```

### Prerequisites

- [Arbiter Zebu](https://github.com/5hanth/arbiter-zebu) bot running (or just `bunx arbiter-zebu`)
- `~/.arbiter/queue/` directory (created automatically by the bot)

## Environment Variables

Set these in your agent's environment for automatic agent/session detection:

| Variable | Description | Example |
|----------|-------------|---------|
| `CLAWDBOT_AGENT` | Agent ID | `ceo`, `swe1` |
| `CLAWDBOT_SESSION` | Session key | `agent:ceo:main` |

## When to Use

- Plan review before implementation
- Architectural decisions with tradeoffs
- Anything blocking that needs human judgment
- Multiple related decisions as a batch

**Do NOT use for:**
- Simple yes/no that doesn't need explanation
- Urgent real-time decisions (use direct message instead)
- Technical questions you can research yourself

## Tools

### arbiter_push

Create a decision plan for human review.

**CLI:** `arbiter-push '<json>'` — takes a single JSON argument containing all fields.

```bash
arbiter-push '{
  "title": "API Design Decisions",
  "tag": "nft-marketplace",
  "context": "SWE2 needs these decided before API work",
  "priority": "normal",
  "notify": "agent:swe2:main",
  "decisions": [
    {
      "id": "auth-strategy",
      "title": "Auth Strategy", 
      "context": "How to authenticate admin users",
      "options": [
        {"key": "jwt", "label": "JWT tokens", "note": "Stateless"},
        {"key": "session", "label": "Sessions", "note": "More control"},
        {"key": "oauth", "label": "OAuth", "note": "External provider"}
      ]
    },
    {
      "id": "database",
      "title": "Database Choice",
      "context": "Primary datastore",
      "options": [
        {"key": "postgresql", "label": "PostgreSQL + JSONB"},
        {"key": "mongodb", "label": "MongoDB"}
      ],
      "allowCustom": true
    }
  ]
}'
```

**JSON Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Plan title |
| `tag` | No | Tag for filtering (e.g., project name) |
| `context` | No | Background for reviewer |
| `priority` | No | `low`, `normal`, `high`, `urgent` (default: normal) |
| `notify` | No | Session to notify when complete |
| `agent` | No | Agent ID (auto-detected from `CLAWDBOT_AGENT` env) |
| `session` | No | Session key (auto-detected from `CLAWDBOT_SESSION` env) |
| `decisions` | Yes | Array of decisions |

**Decision object:**

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique ID within plan |
| `title` | Yes | Decision title |
| `context` | No | Explanation for reviewer |
| `options` | Yes | Array of `{key, label, note?}` |
| `allowCustom` | No | Allow free-text answer (default: false) |
| `default` | No | Suggested option key |

**Returns:**

```json
{
  "planId": "abc123",
  "file": "~/.arbiter/queue/pending/ceo-api-design-abc123.md",
  "total": 2,
  "status": "pending"
}
```

### arbiter_status

Check the status of a decision plan.

**CLI:** `arbiter-status <plan-id>` or `arbiter-status --tag <tag>`

```bash
arbiter-status abc12345
# or
arbiter-status --tag nft-marketplace
```

**Returns:**

```json
{
  "planId": "abc123",
  "title": "API Design Decisions",
  "status": "in_progress",
  "total": 3,
  "answered": 1,
  "remaining": 2,
  "decisions": {
    "auth-strategy": {"status": "answered", "answer": "jwt"},
    "database": {"status": "pending", "answer": null},
    "caching": {"status": "pending", "answer": null}
  }
}
```

### arbiter_get

Get answers from a completed plan.

**CLI:** `arbiter-get <plan-id>` or `arbiter-get --tag <tag>`

```bash
arbiter-get abc12345
# or
arbiter-get --tag nft-marketplace
```

**Returns:**

```json
{
  "planId": "abc123",
  "status": "completed",
  "completedAt": "2026-01-30T01:45:00Z",
  "answers": {
    "auth-strategy": "jwt",
    "database": "postgresql",
    "caching": "redis"
  }
}
```

**Error if not complete:**

```json
{
  "error": "Plan not complete",
  "status": "in_progress",
  "remaining": 2
}
```

### arbiter_await

Block until plan is complete (with timeout).

```bash
arbiter-await abc12345 --timeout 3600
```

Polls every 30 seconds until complete or timeout.

**Returns:** Same as `arbiter_get` on completion.

## Usage Examples

### Example 1: Plan Review

```bash
# Push plan decisions (single JSON argument)
RESULT=$(arbiter-push '{"title":"Clean IT i18n Plan","tag":"clean-it","priority":"high","notify":"agent:swe3:main","decisions":[{"id":"library","title":"i18n Library","options":[{"key":"i18next","label":"i18next"},{"key":"formatjs","label":"FormatJS"}]},{"id":"keys","title":"Key Structure","options":[{"key":"flat","label":"Flat (login.button)"},{"key":"nested","label":"Nested ({login:{button}})"}]}]}')

PLAN_ID=$(echo $RESULT | jq -r '.planId')
echo "Pushed plan $PLAN_ID — waiting for human review"
```

### Example 2: Check and Proceed

```bash
# Check if decisions are ready
STATUS=$(arbiter-status --tag nft-marketplace)

if [ "$(echo $STATUS | jq -r '.status')" == "completed" ]; then
  ANSWERS=$(arbiter-get --tag nft-marketplace)
  AUTH=$(echo $ANSWERS | jq -r '.answers["auth-strategy"]')
  echo "Using auth strategy: $AUTH"
  # Proceed with implementation
else
  echo "Still waiting for $(echo $STATUS | jq -r '.remaining') decisions"
fi
```

### Example 3: Blocking Wait

```bash
# Wait up to 1 hour for decisions
ANSWERS=$(arbiter-await abc12345 --timeout 3600)

if [ $? -eq 0 ]; then
  # Got answers, proceed
  echo "Decisions ready: $ANSWERS"
else
  echo "Timeout waiting for decisions"
fi
```

## Best Practices

1. **Batch related decisions** — Don't push one at a time
2. **Provide context** — Human needs to understand tradeoffs
3. **Use tags** — Makes filtering easy (`--tag project-name`)
4. **Set notify** — So blocked agents get woken up
5. **Use priority sparingly** — Reserve `urgent` for true blockers

## File Locations

| Path | Purpose |
|------|---------|
| `~/.arbiter/queue/pending/` | Plans awaiting review |
| `~/.arbiter/queue/completed/` | Answered plans (archive) |
| `~/.arbiter/queue/notify/` | Agent notifications |

## Checking Notifications (Agent Heartbeat)

In your HEARTBEAT.md, add:

```markdown
## Check Arbiter Notifications

1. Check if `~/.arbiter/queue/notify/` has files for my session
2. If yes, read answers and proceed with blocked work
3. Delete notification file after processing
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plan not showing in Arbiter | Check file is valid YAML frontmatter |
| Answers not appearing | Check `arbiter_status`, may be incomplete |
| Notification not received | Ensure `--notify` was set correctly |

## See Also

- [Arbiter Zebu Architecture](https://github.com/5hanth/arbiter-zebu/blob/main/ARCHITECTURE.md)
- [Arbiter Zebu Bot](https://github.com/5hanth/arbiter-zebu)
