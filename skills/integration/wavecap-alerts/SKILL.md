---
name: wavecap-alerts
description: Manage WaveCap alert rules and keyword triggers. Use when the user wants to view, add, update, or remove alert phrases and notification rules.
---

# WaveCap Alerts Skill

Use this skill to manage keyword alert rules in WaveCap.

## Authentication Required

Updating alerts requires editor authentication:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password": "YOUR_EDITOR_PASSWORD"}' | jq -r '.token')
```

## View Current Alerts

```bash
curl -s http://localhost:8000/api/alerts | jq
```

### Response Format

```json
{
  "enabled": true,
  "rules": [
    {
      "id": "rule-1",
      "label": "Emergency",
      "phrases": ["emergency", "urgent", "mayday"],
      "playSound": true,
      "notify": true,
      "caseSensitive": false,
      "enabled": true
    }
  ]
}
```

## Update Alerts

The PUT endpoint replaces the entire alerts configuration:

```bash
curl -s -X PUT http://localhost:8000/api/alerts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "rules": [
      {
        "id": "emergency",
        "label": "Emergency",
        "phrases": ["emergency", "mayday", "urgent"],
        "playSound": true,
        "notify": true,
        "caseSensitive": false,
        "enabled": true
      },
      {
        "id": "fire",
        "label": "Fire",
        "phrases": ["structure fire", "brush fire", "fire alarm"],
        "playSound": true,
        "notify": true,
        "caseSensitive": false,
        "enabled": true
      }
    ]
  }' | jq
```

## Alert Rule Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the rule |
| `label` | string | Display name for the alert |
| `phrases` | string[] | Keywords/phrases to match |
| `playSound` | bool | Play audio alert when triggered |
| `notify` | bool | Show notification when triggered |
| `caseSensitive` | bool | Match case exactly |
| `enabled` | bool | Whether rule is active |

## Common Operations

### Add a New Alert Rule

First get existing alerts, then append the new rule:

```bash
# Get current config
CURRENT=$(curl -s http://localhost:8000/api/alerts)

# Add new rule using jq
UPDATED=$(echo "$CURRENT" | jq '.rules += [{
  "id": "medical",
  "label": "Medical Emergency",
  "phrases": ["cardiac arrest", "cpr", "unresponsive"],
  "playSound": true,
  "notify": true,
  "caseSensitive": false,
  "enabled": true
}]')

# Update
curl -s -X PUT http://localhost:8000/api/alerts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$UPDATED" | jq
```

### Disable a Rule

```bash
CURRENT=$(curl -s http://localhost:8000/api/alerts)
UPDATED=$(echo "$CURRENT" | jq '(.rules[] | select(.id == "rule-id")).enabled = false')
curl -s -X PUT http://localhost:8000/api/alerts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$UPDATED" | jq
```

### Remove a Rule

```bash
CURRENT=$(curl -s http://localhost:8000/api/alerts)
UPDATED=$(echo "$CURRENT" | jq '.rules = [.rules[] | select(.id != "rule-to-remove")]')
curl -s -X PUT http://localhost:8000/api/alerts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$UPDATED" | jq
```

### Add Phrases to Existing Rule

```bash
CURRENT=$(curl -s http://localhost:8000/api/alerts)
UPDATED=$(echo "$CURRENT" | jq '(.rules[] | select(.id == "emergency")).phrases += ["crisis", "help"]')
curl -s -X PUT http://localhost:8000/api/alerts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$UPDATED" | jq
```

### Disable All Alerts

```bash
curl -s -X PUT http://localhost:8000/api/alerts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false, "rules": []}' | jq
```

## View Triggered Alerts in Transcriptions

Transcriptions that triggered alerts have an `alerts` array:

```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=100" | \
  jq '[.transcriptions[] | select(.alerts | length > 0)] | .[] | {timestamp, text, alerts: [.alerts[].ruleLabel]}'
```

## Tips

- The entire rules array is replaced on PUT - always include all rules you want to keep
- Use descriptive `id` values for easy reference
- Keep `caseSensitive: false` for most use cases
- Test phrases with common variations and misspellings
