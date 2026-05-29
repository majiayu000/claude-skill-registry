---
name: front-id-converter
description: Convert between Front URL IDs (base-10) and API IDs (base-36 with prefix). Use when working with Front inbox, conversation, or message IDs.
allowed-tools: Bash
---

# Front ID Converter Skill

Convert between Front URL IDs (base-10) and API IDs (base-36 with prefix).

## Conversion Rules

Front API IDs are created by:
1. Converting the numeric URL ID (base-10) to base-36
2. Adding a resource prefix

## Resource Prefixes

| Prefix | Resource |
|--------|----------|
| `inb_` | Inboxes |
| `cnv_` | Conversations |
| `tag_` | Tags |
| `msg_` | Messages |
| `tea_` | Teammates |
| `rul_` | Rules |
| `cmt_` | Comments |
| `alt_` | Attachments |
| `cha_` | Channels |
| `ctc_` | Contacts |
| `grp_` | Contact Groups |
| `shf_` | Shifts |
| `sig_` | Signatures |
| `tmr_` | Message Template Folders |
| `tmp_` | Message Templates |

## URL to API ID

```typescript
function urlToApiId(urlId: number, prefix: string): string {
  return `${prefix}${urlId.toString(36)}`
}

// Example: Inbox 7256583 → inb_4bj7r
urlToApiId(7256583, 'inb_') // => "inb_4bj7r"
```

## API ID to URL

```typescript
function apiIdToUrl(apiId: string): number {
  const base36 = apiId.split('_')[1]
  return parseInt(base36, 36)
}

// Example: inb_4bj7r → 7256583
apiIdToUrl('inb_4bj7r') // => 7256583
```

## Quick Bash Conversion

```bash
# URL ID to API ID (requires node)
node -e "console.log('inb_' + (7256583).toString(36))"

# API ID to URL ID
node -e "console.log(parseInt('4bj7r', 36))"
```

## Common Use Cases

### From Front URL
Given: `https://app.frontapp.com/inboxes/teams/folders/7256583/unassigned/120537545061`
- Inbox ID: `7256583` → `inb_4bj7r`
- Conversation ID: `120537545061` → `cnv_1z2x3y4z` (calculate as needed)

### Validating API Responses
When Front API returns an ID like `inb_4bj7r`, you can verify it matches the expected inbox by converting back to the URL ID.
