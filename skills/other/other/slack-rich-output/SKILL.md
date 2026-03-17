---
name: slack-rich-output
description: |
  Slack Block Kit, mrkdwn syntax, and rich message formatting for building Slack app output.
  Triggers on: Slack, Block Kit, mrkdwn, Slack blocks, Slack formatting, Slack message, Slack modal,
  Slack App Home, rich text block, section block, actions block, table block, markdown block,
  Slack mentions, Slack date formatting, Slack surfaces, Work Objects, Slack link unfurl,
  chat.postMessage, views.open, views.publish, Slack interactive elements, Slack select menu,
  Slack button, Slack overflow, context block, header block, divider block, Slack mrkdwn vs markdown.

  Use when: building Slack apps or bots, formatting Slack messages, constructing Block Kit payloads,
  creating modals or App Home views, implementing link unfurling, adding interactive elements,
  or any task involving Slack message composition. Proactively apply when generating Slack API
  payloads, chat.postMessage calls, or Block Kit JSON.
---

# Slack Rich Output

Slack-native formatting for messages using mrkdwn syntax and Block Kit.

## CRITICAL: Two Markup Systems

Slack has two completely different markup syntaxes. Using the wrong one is the most common formatting mistake.

| System | Used In | Bold | Link | Heading |
|--------|---------|------|------|---------|
| **Slack mrkdwn** | `text` field, text objects (`type: "mrkdwn"`), section fields | `*bold*` | `<url\|text>` | Not supported |
| **Standard Markdown** | `markdown` block only | `**bold**` | `[text](url)` | `# Heading` |

Standard Markdown syntax (`**bold**`, `[text](url)`, `# Heading`) renders as literal text in mrkdwn contexts. Slack mrkdwn syntax (`*bold*`, `<url|text>`) renders as literal text in markdown blocks. Never mix them.

The `markdown` block is designed for AI app output — it renders standard Markdown natively in Slack. However, it only works in Messages (not Modals or Home tabs), has a 12,000 character cumulative limit per payload, and does not support syntax highlighting, horizontal rules, tables, or task lists. `block_id` is ignored.

## Quick Decision Trees

### "Should I use blocks?"

```
Response type?
├─ Conversational reply, short answer, <3 lines   → text only (no blocks)
├─ Multi-section summary, report, dashboard        → blocks
├─ Two-column key-value data                       → blocks (section fields)
├─ Tabular data                                    → blocks (table)
├─ Code with heading or surrounding context         → blocks
├─ Visual separation needed between topics          → blocks
└─ Feedback buttons or interactive elements         → blocks
```

### "Which block type?"

```
What am I rendering?
├─ Large section title                → header (plain_text, 150 chars max)
├─ Body text or key-value pairs       → section (text + fields + accessory)
├─ Small metadata or secondary info   → context (images + text, 10 max)
├─ Horizontal separator               → divider
├─ Buttons, menus, date pickers       → actions (25 elements max)
├─ Standalone image                   → image (image_url or slack_file)
├─ Formatted text with lists, quotes  → rich_text (nested sub-elements)
├─ Tabular data                       → table (100 rows, 20 cols, 1 per msg)
├─ LLM-generated markdown content     → markdown (standard MD, messages only)
├─ Embedded video player              → video (requires links.embed:write)
├─ Remote file reference              → file (read-only, source: "remote")
├─ Feedback thumbs up/down            → context_actions (messages only)
└─ Collecting user input (modals)     → input (label + element)
```

### "mrkdwn or markdown block?"

```
Content source?
├─ Short formatted text, labels, fields     → mrkdwn in section/context
├─ Long-form LLM-generated content          → markdown block (standard MD)
├─ Need tables inside blocks                → mrkdwn in section (manual layout)
├─ Need headings                            → markdown block or header blocks
└─ Mixed: structured layout + prose         → section/header blocks + markdown block
```

## Slack mrkdwn Syntax

| Format | Syntax | Notes |
|--------|--------|-------|
| Bold | `*bold*` | Not `**bold**` |
| Italic | `_italic_` | Not `*italic*` |
| Strikethrough | `~strikethrough~` | Not `~~strikethrough~~` |
| Inline code | `` `code` `` | Same as standard Markdown |
| Code block | ` ```code``` ` | No syntax highlighting |
| Blockquote | `> quoted text` | Prefix each line |
| Link | `<https://example.com\|display text>` | Not `[text](url)` |
| User mention | `<@U0123ABC>` | Triggers notification |
| Channel mention | `<#C0123ABC>` | Auto-converts to name |
| User group | `<!subteam^SAZ94GDB8>` | Notifies all members |
| @here | `<!here>` | Active channel members |
| @channel | `<!channel>` | All channel members |
| @everyone | `<!everyone>` | All non-guest workspace members |
| Emoji | `:emoji_name:` | Standard or custom |
| Newline | `\n` | Literal newline in string |
| Ordered list | `1. item` | Plain text, no special rendering |
| Bullet list | `• item` | Rendered in `rich_text` blocks only |

### Date Formatting

Displays localized dates in the reader's timezone:

```
<!date^{unix_timestamp}^{token_string}^{optional_link}|{fallback_text}>
```

Tokens: `{date_num}` (2014-02-18), `{date}` (February 18th, 2014), `{date_short}` (Feb 18, 2014), `{date_long}` (Tuesday, February 18th, 2014), `{time}` (6:39 AM), `{time_secs}` (6:39:42 AM), `{ago}` (3 minutes ago). Add `_pretty` suffix for relative terms ("yesterday", "today").

### Escaping

Only three characters need escaping: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`. Do not HTML-encode other characters.

### Text Object Verbatim

Set `verbatim: true` on mrkdwn text objects to disable auto-link conversion and mention parsing. Useful when displaying raw URLs or text that looks like mentions but isn't.

## Block Types Reference

### header

Large bold text for section titles. `plain_text` only. Max 150 chars.

```json
{ "type": "header", "text": { "type": "plain_text", "text": "Section Title", "emoji": true } }
```

### section

Primary content block. Supports text, two-column fields, and one accessory element.

```json
{
  "type": "section",
  "text": { "type": "mrkdwn", "text": "*Project Status*\nAll systems operational." }
}
```

Two-column fields layout:

```json
{
  "type": "section",
  "fields": [
    { "type": "mrkdwn", "text": "*Status:*\nActive" },
    { "type": "mrkdwn", "text": "*Owner:*\nChris" },
    { "type": "mrkdwn", "text": "*Priority:*\nHigh" },
    { "type": "mrkdwn", "text": "*Due:*\nFriday" }
  ]
}
```

Either `text` or `fields` required (or both). Text max 3000 chars. Fields max 10 items, each max 2000 chars. Set `expand: true` to force full text display without "see more" truncation.

Compatible accessories: button, overflow, datepicker, timepicker, select menus, multi-select menus, checkboxes, radio buttons, image.

### divider

Horizontal rule between blocks.

```json
{ "type": "divider" }
```

### context

Small, muted text for metadata or secondary info. Elements: mrkdwn text objects or image elements. Max 10 elements.

```json
{
  "type": "context",
  "elements": [
    { "type": "mrkdwn", "text": "Last updated: Feb 9, 2026" },
    { "type": "mrkdwn", "text": "Source: deploy-bot" }
  ]
}
```

### actions

Interactive elements: buttons, select menus, overflow menus, date pickers. Max 25 elements.

```json
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Approve", "emoji": true },
      "style": "primary",
      "action_id": "approve_action",
      "value": "approved"
    }
  ]
}
```

Button styles: `primary` (green), `danger` (red), or omit for default. Use `primary` sparingly — one per set. Action IDs must be unique within the message.

### image

Standalone image with alt text. Provide either `image_url` (public, max 3000 chars) or `slack_file` object. Formats: png, jpg, jpeg, gif.

```json
{
  "type": "image",
  "image_url": "https://example.com/chart.png",
  "alt_text": "Deployment success rate chart",
  "title": { "type": "plain_text", "text": "Deploy Metrics" }
}
```

### rich_text

Advanced formatted text with nested elements. Supports styled text, lists, code blocks, and quotes.

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [
        { "type": "text", "text": "Key findings:", "style": { "bold": true } },
        { "type": "text", "text": "\n" }
      ]
    },
    {
      "type": "rich_text_list",
      "style": "bullet",
      "elements": [
        {
          "type": "rich_text_section",
          "elements": [{ "type": "text", "text": "Latency reduced by 40%" }]
        },
        {
          "type": "rich_text_section",
          "elements": [{ "type": "text", "text": "Error rate under 0.1%" }]
        }
      ]
    }
  ]
}
```

Sub-element types:
- `rich_text_section` — paragraph of inline elements
- `rich_text_list` — `style: "bullet"` or `"ordered"`, optional `indent` (pixels of indentation), `offset` (start number for ordered), `border` (px)
- `rich_text_preformatted` — code block (monospace, grey background)
- `rich_text_quote` — indented quote block

Inline element types within sections: `text` (with optional `style: { bold, italic, strike, code, underline }`), `link` (`url`, optional `text`, optional `style`), `emoji` (`name`), `user` (`user_id`), `channel` (`channel_id`), `usergroup` (`usergroup_id`), `broadcast` (`range`: here/channel/everyone), `date` (`timestamp`, `format`, `fallback`), `color` (`value`: hex).

### table

Tabular data. One table per message (appended as attachment at bottom). The first row acts as the header.

```json
{
  "type": "table",
  "rows": [
    [
      { "type": "raw_text", "text": "Service" },
      { "type": "raw_text", "text": "Status" },
      { "type": "raw_text", "text": "Latency" }
    ],
    [
      { "type": "raw_text", "text": "API" },
      { "type": "raw_text", "text": "Healthy" },
      { "type": "raw_text", "text": "12ms" }
    ],
    [
      { "type": "raw_text", "text": "Worker" },
      { "type": "raw_text", "text": "Degraded" },
      { "type": "raw_text", "text": "340ms" }
    ]
  ],
  "column_settings": [
    { "align": "left" },
    { "align": "center" },
    { "align": "right" }
  ]
}
```

Each row is an array of cell objects (NOT an object with a `cells` property). Cell types: `raw_text` (plain text) or `rich_text` (with `elements` array for links, mentions, emoji, bold). There is no `columns` property — the first row is the header. Max 100 rows, 20 columns per row. `column_settings` controls alignment (`left`/`center`/`right`) and `is_wrapped` (boolean). Sending multiple tables triggers `invalid_attachments` error.

### markdown

Standard Markdown rendering for AI app output. Messages only.

```json
{ "type": "markdown", "text": "**Bold**, *italic*, [link](https://example.com)\n\n## Heading\n\n- List item" }
```

Supports: bold, italic, strikethrough, links, headers (h1+), ordered/unordered lists, inline code, code blocks, block quotes, images (as hyperlinks). Does NOT support: syntax highlighting, horizontal rules, tables, task lists. Cumulative 12,000 char limit per payload. `block_id` is ignored. Escape special characters with backslash (`\*`, `\[`, `\#`, etc.) to render them literally.

### context_actions

Feedback and icon buttons for message-level actions. Messages only. Max 5 elements.

```json
{
  "type": "context_actions",
  "elements": [
    {
      "type": "feedback_buttons",
      "action_id": "feedback_123",
      "positive_button": {
        "text": { "type": "plain_text", "text": "Good" },
        "value": "positive"
      },
      "negative_button": {
        "text": { "type": "plain_text", "text": "Bad" },
        "value": "negative"
      }
    }
  ]
}
```

Compatible elements: `feedback_buttons` (positive + negative), `icon_button` (only `trash` icon available, supports `visible_to_user_ids` array).

### video

Embedded video player. Requires `links.embed:write` scope, publicly accessible URL in app's unfurl domains.

```json
{
  "type": "video",
  "alt_text": "Product demo",
  "title": { "type": "plain_text", "text": "Q4 Demo" },
  "video_url": "https://example.com/embed/video",
  "thumbnail_url": "https://example.com/thumb.png",
  "title_url": "https://example.com/video",
  "description": { "type": "plain_text", "text": "Quarterly product walkthrough" },
  "author_name": "Product Team"
}
```

### input

Collects user data in modals, messages, and Home tabs. Requires `label` (plain_text, 2000 chars) and one compatible element.

```json
{
  "type": "input",
  "label": { "type": "plain_text", "text": "Description" },
  "element": {
    "type": "plain_text_input",
    "action_id": "description_input",
    "multiline": true
  },
  "optional": true,
  "hint": { "type": "plain_text", "text": "Brief summary of the issue" }
}
```

Compatible elements: plain_text_input, number_input, email_text_input, url_text_input, rich_text_input, select menus, multi-select menus, datepicker, datetimepicker, timepicker, checkboxes, radio_buttons, file_input.

### file

Remote file reference. Read-only — appears when retrieving messages with remote files. Cannot be directly added to messages.

```json
{ "type": "file", "external_id": "ABCD1", "source": "remote" }
```

## Composition Objects

### Text Object

```json
{ "type": "mrkdwn", "text": "*bold* and _italic_", "verbatim": false }
{ "type": "plain_text", "text": "No formatting", "emoji": true }
```

`mrkdwn` supports Slack mrkdwn syntax. `plain_text` renders literally. `emoji: true` converts `:emoji:` to rendered emoji (plain_text only). `verbatim: true` disables auto-linking (mrkdwn only). Min 1 char, max 3000 chars. Header blocks require `plain_text`. Section text/fields accept either.

### Option Object

Used in select menus, overflow, checkboxes, radio buttons:

```json
{
  "text": { "type": "plain_text", "text": "Option 1" },
  "value": "opt_1",
  "description": { "type": "plain_text", "text": "Detailed description" }
}
```

Option text max 75 chars. `value` max 150 chars. `description` optional, max 75 chars. Text type: `plain_text` for select/overflow menus; `mrkdwn` also allowed for checkboxes and radio buttons.

### Option Group Object

Groups options in select menus. Max 100 groups, each with label + options array:

```json
{
  "label": { "type": "plain_text", "text": "Group Name" },
  "options": [{ "text": { "type": "plain_text", "text": "Item" }, "value": "item_1" }]
}
```

### Confirmation Dialog

Adds confirmation step to interactive elements:

```json
{
  "title": { "type": "plain_text", "text": "Are you sure?" },
  "text": { "type": "plain_text", "text": "This action cannot be undone." },
  "confirm": { "type": "plain_text", "text": "Yes, do it" },
  "deny": { "type": "plain_text", "text": "Cancel" },
  "style": "danger"
}
```

Title max 100 chars. Text max 300 chars. Button labels max 30 chars. Style: `primary` (green) or `danger` (red).

### Dispatch Action Configuration

Controls when plain_text_input or rich_text_input triggers `block_actions`:

```json
{ "trigger_actions_on": ["on_enter_pressed"] }
```

Values: `on_enter_pressed`, `on_character_entered`. Requires `dispatch_action: true` on the input block.

### Conversation Filter

Filters conversation select menus:

```json
{
  "include": ["public", "mpim"],
  "exclude_external_shared_channels": true,
  "exclude_bot_users": true
}
```

At least one field required. `include` values: `im`, `mpim`, `private`, `public`.

## Limits

| Constraint | Limit |
|-----------|-------|
| Blocks per message | 50 |
| Blocks per modal/Home tab | 100 |
| Section text | 3000 chars |
| Section fields | 10 items, 2000 chars each |
| Header text | 150 chars |
| Context elements | 10 |
| Actions elements | 25 |
| Context actions elements | 5 |
| Table rows | 100 |
| Table columns | 20 |
| Tables per message | 1 |
| Markdown block text | 12,000 chars cumulative per payload |
| Modal title | 24 chars |
| Modal submit/close text | 24 chars |
| Modal views in stack | 3 |
| Modal private_metadata | 3000 chars |
| Button text | 75 chars (displays ~30) |
| Button value | 2000 chars |
| action_id | 255 chars |
| block_id | 255 chars |
| Overflow options | 5 |
| Select options | 100 |
| Option text | 75 chars |
| Placeholder text | 150 chars |
| Confirmation title | 100 chars |
| Confirmation text | 300 chars |
| Image alt_text | 2000 chars |
| Image URL | 3000 chars |
| Video title | 200 chars |
| Video description | 200 chars |
| Video author_name | 50 chars |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `**bold**` in mrkdwn | Renders literally | Use `*bold*` |
| `[text](url)` in mrkdwn | Renders literally | Use `<url\|text>` |
| `# Heading` in mrkdwn | Renders as plain text | Use `header` block or `markdown` block |
| `*bold*` in markdown block | Renders as italic | Use `**bold**` |
| Blocks without `text` fallback | Empty notifications, no accessibility fallback | Always provide `text` in `chat.postMessage` |
| `text` and `blocks` diverge | Confusing: notification says one thing, chat shows another | Keep semantically aligned |
| Blocks for simple replies | Visual noise for short responses | Use `text` only for simple replies |
| 2+ tables in one message | `invalid_attachments` error | One table per message |
| `mrkdwn` in header text | Ignored — headers only accept `plain_text` | Use `plain_text` type |
| Long header text | Silently truncated at 150 chars | Keep under 150 |
| Missing `alt_text` on images | Accessibility failure, API may reject | Always include alt_text |
| `link_names: 1` for mentions | Fragile — names change, IDs don't | Use `<@USERID>` directly |

## Best Practices

**Use blocks when:**
- The response has multiple distinct sections (summaries, reports, dashboards)
- Two-column key-value layouts improve readability (metadata, config summaries)
- A table presents data more clearly than prose
- Visual separation between topics helps comprehension
- Code needs a header or surrounding context
- Interactive elements (buttons, menus, feedback) are needed

**Don't use blocks when:**
- The response is conversational ("sure, done", "hey, good morning")
- The response is under ~3 lines of text
- The content is a simple answer to a direct question

**Always:**
- Provide a complete `text` field as the accessible fallback (notifications, threads, search, screen readers)
- Keep the `text` and `blocks` semantically aligned
- Use mrkdwn syntax in text objects, not standard Markdown (except in `markdown` blocks)
- Escape `&`, `<`, `>` in user-generated content
- Use `<@USERID>` for mentions, not `@name` — IDs are stable, names change

## Surfaces Overview

Block Kit renders across multiple Slack surfaces:

| Surface | Max Blocks | Key Methods | Notes |
|---------|-----------|-------------|-------|
| Messages | 50 | `chat.postMessage`, `chat.update` | Primary output surface |
| Modals | 100 | `views.open`, `views.update`, `views.push` | Requires `trigger_id` (3s expiry), up to 3 stacked views |
| App Home | 100 | `views.publish` | Private per-user view, Home/Messages/About tabs |
| Canvases | N/A | `canvases.create`, `canvases.edit` | Markdown only — no Block Kit support |
| Lists | N/A | `lists.*` API methods | Task tracking and project management |
| Split View | N/A | Agents & AI Apps config | AI chat surface with Chat + History tabs |

Modals collect input via `input` blocks, return `view_submission` payloads. They chain up to 3 views with push/update/clear response actions. `private_metadata` (3000 chars) persists context between views.

## Work Objects

Work Objects render rich entity previews when links are shared in Slack. They extend link unfurling with structured data, flexpane details, editable fields, and actions.

### Entity Types

| Type | Entity ID | Purpose |
|------|-----------|---------|
| File | `slack#/entities/file` | Documents, spreadsheets, images |
| Task | `slack#/entities/task` | Tickets, to-dos, work items |
| Incident | `slack#/entities/incident` | Service interruptions, outages |
| Content Item | `slack#/entities/content_item` | Articles, pages, wiki entries |
| Item | `slack#/entities/item` | General-purpose entity |

### Implementation

Work Objects use `chat.unfurl` with a `metadata` parameter (URL-encoded) containing entity type, external reference, and entity payload (attributes, fields, custom_fields, display_order). The flexpane responds to `entity_details_requested` events via `entity.presentDetails`.

### Capabilities

- **Editable fields**: text, number, date, datetime, email, boolean, select, multi-select with validation
- **Actions**: Up to 2 primary buttons + 5 overflow menu items per entity
- **Authentication**: `user_auth_required` + `user_auth_url` for third-party auth flows
- **Full-size preview**: PDFs and images via `preview_url` (requires CORS header)
- **Related conversations**: Automatic aggregation of conversations mentioning the entity
- **Direct posting**: `chat.postMessage` also accepts `metadata` for posting Work Objects without link unfurling

Work Objects cannot be rendered in standard `blocks` output — they require `chat.unfurl` metadata or `chat.postMessage` with metadata parameter. They are not part of the message composition flow.

### Data Types

`string`, `integer`, `boolean`, `array`, `slack#/types/user`, `slack#/types/channel_id`, `slack#/types/timestamp`, `slack#/types/date`, `slack#/types/image`, `slack#/types/link`, `slack#/types/email`, `slack#/types/entity_ref`.

## Reference Documentation

| File | Purpose |
|------|---------|
| [references/CHEATSHEET.md](references/CHEATSHEET.md) | Quick reference: all blocks, elements, limits, mrkdwn at a glance |
| [references/BLOCKS.md](references/BLOCKS.md) | All 13 block types with full property tables and constraints |
| [references/ELEMENTS.md](references/ELEMENTS.md) | All 19 interactive elements with properties and constraints |
| [references/COMPOSITION.md](references/COMPOSITION.md) | Composition objects: text, option, confirmation, filters |
| [references/RICH-TEXT.md](references/RICH-TEXT.md) | Rich text block deep dive: sub-elements, inline types, styles |
| [references/FORMATTING.md](references/FORMATTING.md) | mrkdwn syntax, date formatting, mentions, escaping, auto-parsing |
| [references/SURFACES.md](references/SURFACES.md) | Modals, App Home, canvases, lists, split view |
| [references/WORK-OBJECTS.md](references/WORK-OBJECTS.md) | Entity types, chat.unfurl, flexpane, editable fields, actions |

## Sources

- [Block Kit Reference](https://docs.slack.dev/reference/block-kit) — Slack
- [Block Kit Blocks](https://docs.slack.dev/reference/block-kit/blocks) — Slack
- [Block Kit Elements](https://docs.slack.dev/reference/block-kit/block-elements) — Slack
- [Block Kit Composition Objects](https://docs.slack.dev/reference/block-kit/composition-objects) — Slack
- [Formatting Message Text](https://docs.slack.dev/messaging/formatting-message-text) — Slack
- [Messaging Overview](https://docs.slack.dev/messaging) — Slack
- [Work Objects](https://docs.slack.dev/messaging/work-objects) — Slack
- [Surfaces](https://docs.slack.dev/surfaces) — Slack
- [Modals](https://docs.slack.dev/surfaces/modals) — Slack
- [App Home](https://docs.slack.dev/surfaces/app-home) — Slack
- [Canvases](https://docs.slack.dev/surfaces/canvases) — Slack
- [Lists](https://docs.slack.dev/surfaces/lists) — Slack
- [Split View](https://docs.slack.dev/surfaces/split-view) — Slack
- [App Design](https://docs.slack.dev/surfaces/app-design) — Slack
