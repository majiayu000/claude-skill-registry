---
name: comms
description: Post to Slack channels and manage Trello cards with natural language
---

# /comms - Slack & Trello Communications Skill

Post messages to Slack channels and create/update Trello cards with natural language commands.

## Usage

```
/comms [message or instruction]
```

## CRITICAL: Load MCP Tools First

**MCP tools are deferred and MUST be loaded via ToolSearch before use.**

Before calling any Slack or Trello tool, load it:
```
ToolSearch: select:mcp__slack__slack_post_message
ToolSearch: select:mcp__trello__add_card_to_list
```

Do NOT:
- Try bash commands to call MCP tools
- Assume tools are unavailable if direct calls fail
- Go searching through scripts or configs

The tools ARE available. Just load them first with ToolSearch.

## Key Rules

### Trello Comments
**Always prefix Trello comments with "From Claude Code: "**

Example: If asked to add comment "Fixed the bug", post:
```
From Claude Code: Fixed the bug
```

### Fuzzy Matching
Match user input to channels/boards using aliases. Examples:
- "android" -> tech-android (Slack) or Android list (Trello)
- "ios" -> tech-ios (Slack) or IOS App list (Trello)
- "server" -> tech-server (Slack) or Server list (Trello)

### Smart Defaults
- Tech topics without channel specified -> tech-general
- Tech topics without board specified -> Tech Work board
- Business/org topics -> Org-Business Work board

## Example Commands

| User Says | Action |
|-----------|--------|
| "post to android: feature complete" | Post to tech-android channel |
| "create card on ios list: Fix crash bug" | Create card on Tech Work -> IOS App list |
| "add comment to card X: resolved" | Add "From Claude Code: resolved" to card |
| "tell server channel build is ready" | Post to tech-server channel |
| "create website card: update pricing" | Create card on Org-Business Work -> Website list |

## Resources

See [RESOURCES.md](RESOURCES.md) for complete channel/board mappings with IDs.

## MCP Tools Used

### Slack
- `mcp__slack__slack_post_message` - Post to channel
- `mcp__slack__slack_reply_to_thread` - Reply in thread
- `mcp__slack__slack_get_channel_history` - Read messages
- `mcp__slack__slack_add_reaction` - Add emoji reaction

### Trello
- `mcp__trello__add_card_to_list` - Create card
- `mcp__trello__add_comment` - Add comment (remember prefix!)
- `mcp__trello__update_card_details` - Update card
- `mcp__trello__move_card` - Move card between lists
- `mcp__trello__get_cards_by_list_id` - List cards

## Workflow

1. Parse user intent (Slack, Trello, or both)
2. Resolve channel/board/list using fuzzy matching
3. **Convert content to platform-native formatting** (see below)
4. Execute appropriate MCP tool(s)
5. Confirm action to user

---

## Platform Formatting Guidelines

**CRITICAL: Neither Trello nor Slack supports markdown tables.** You must convert tabular data to platform-native formats.

### Trello Formatting (Markdown subset)

**Supported:**
- Bold: `**text**` or `__text__`
- Italic: `*text*` or `_text_`
- Strikethrough: `~~text~~`
- Headings: `# H1`, `## H2`, `### H3`
- Bulleted lists: `- item` or `* item` (blank line required above list)
- Numbered lists: `1. item`
- Code blocks: ``` or indent 4 spaces
- Links: `[text](url)`
- Horizontal rule: `---`

**NOT Supported:**
- Tables (pipes and dashes render as plain text)
- Nested formatting in some contexts

### Slack Formatting (mrkdwn, NOT markdown)

**Supported:**
- Bold: `*text*` (single asterisk, unlike markdown)
- Italic: `_text_`
- Strikethrough: `~text~` (single tilde)
- Code: `` `code` ``
- Code blocks: ``` (no syntax highlighting)
- Links: `<url|text>` (angle brackets, not square)
- Blockquotes: `>` at line start
- Lists: Use bullet character or numbers

**NOT Supported:**
- Tables
- Headings (# doesn't work)
- Standard markdown link syntax

---

## Converting Tables to Native Formats

### Option 1: Key-Value Lists (Recommended for Trello)

**Instead of:**
```
| Component | Cost |
|-----------|------|
| GPU | $100 |
| STT | $0 |
```

**Use:**
```
**Components:**
- **GPU:** $100
- **STT:** $0
```

### Option 2: Grouped Sections (Best for comparisons)

**Instead of a comparison table, use:**
```
## 20 Users
- **Total:** $100/month
- GPU: $87-100
- STT: $0 (Groq free tier)
- TTS: $0 (self-hosted)

## 100 Users
- **Total:** $175/month
- GPU: $115-145
- STT: $0-30
- TTS: $0 (self-hosted)
```

### Option 3: Code Block (Preserves alignment)

For data that must stay aligned, use a code block:
```
Component          20 Users    100 Users
─────────────────────────────────────────
GPU                $100        $150
STT                $0          $0-30
TTS                $0          $0
─────────────────────────────────────────
TOTAL              $100        $175
```

### Option 4: Inline Summary (For Slack)

Slack messages should be concise:
```
*Cost Summary:*
• 20 users: *$100/mo* (GPU $100, STT free, TTS free)
• 100 users: *$175/mo* (GPU $150, STT $0-30, TTS free)
```

---

## Formatting Checklist

Before posting to Trello or Slack:
- [ ] Convert all markdown tables to lists or code blocks
- [ ] Ensure blank line before any list
- [ ] Use platform-specific bold/italic syntax
- [ ] Use `<url|text>` for Slack links, `[text](url)` for Trello
- [ ] Keep Slack messages concise; Trello can be longer
