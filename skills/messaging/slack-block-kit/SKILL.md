---
name: slack-block-kit
description: Proactively apply when generating Slack API payloads with blocks, chat.postMessage calls with structured content, or views.open/views.publish calls. Triggers on Block Kit, Slack blocks, section block, actions block, header block, divider block, context block, table block, markdown block, rich text block, image block, input block, video block, context_actions block, plan block, task_card block, Slack modal, Slack App Home, Slack surfaces, Slack interactive elements, Slack button, Slack select menu, Slack overflow, Slack datepicker, Slack checkboxes, Slack radio buttons, Work Objects, Slack link unfurl, chat.postMessage blocks, views.open, views.update, views.push, views.publish, Slack composition objects. Use when building Block Kit payloads, constructing blocks arrays, creating modals or App Home views, adding interactive elements, implementing link unfurling with Work Objects, or designing rich message layouts. Slack Block Kit UI framework for building rich message layouts, modals, and App Home views.
---

# Slack Block Kit

UI framework for building rich, interactive layouts in Slack messages, modals, and App Home.

## CRITICAL: Two Markup Systems

Text inside Block Kit text objects uses Slack mrkdwn syntax (`*bold*`, `<url|text>`), NOT standard Markdown. The only exception is the `markdown` block which uses standard Markdown.

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
├─ Collecting user input (modals)     → input (label + element)
├─ AI agent task steps                → plan (sequential tasks, messages only)
└─ Single task with status            → task_card (inside plan or standalone)
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

## Block Types Overview

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

```json
{ "type": "divider" }
```

### context

Small, muted text for metadata. Elements: mrkdwn text objects or image elements. Max 10 elements.

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

Advanced formatted text with nested elements. Supports styled text, lists, code blocks, and quotes. See [references/RICH-TEXT.md](references/RICH-TEXT.md) for deep dive.

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [
        { "type": "text", "text": "Key findings:", "style": { "bold": true } }
      ]
    },
    {
      "type": "rich_text_list",
      "style": "bullet",
      "elements": [
        { "type": "rich_text_section", "elements": [{ "type": "text", "text": "Latency reduced by 40%" }] },
        { "type": "rich_text_section", "elements": [{ "type": "text", "text": "Error rate under 0.1%" }] }
      ]
    }
  ]
}
```

Sub-element types: `rich_text_section` (paragraph), `rich_text_list` (`style: "bullet"` or `"ordered"`, with `indent`, `offset`, `border`), `rich_text_preformatted` (code block), `rich_text_quote` (blockquote).

Inline element types within sections: `text` (with optional `style: { bold, italic, strike, code, underline }`), `link`, `emoji`, `user`, `channel`, `usergroup`, `broadcast`, `date`, `color`.

### table

Tabular data. One table per message (appended as attachment at bottom).

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
    ]
  ],
  "column_settings": [
    { "align": "left" },
    { "align": "center" },
    { "align": "right" }
  ]
}
```

Each row is an array of cell objects (NOT an object with a `cells` property). Cell types: `raw_text` or `rich_text`. There is no `columns` property — the first row is the header. Max 100 rows, 20 columns. Multiple tables trigger `invalid_attachments` error.

### markdown

Standard Markdown rendering for AI app output. Messages only.

```json
{ "type": "markdown", "text": "**Bold**, *italic*, [link](https://example.com)\n\n## Heading\n\n- List item" }
```

Supports: bold, italic, strikethrough, links, headers, ordered/unordered lists, inline code, code blocks, block quotes. Does NOT support: syntax highlighting, horizontal rules, tables, task lists. Cumulative 12,000 char limit per payload. `block_id` is ignored.

### context_actions

Feedback and icon buttons for message-level actions. Messages only. Max 5 elements. Compatible elements: `feedback_buttons`, `icon_button`.

### video

Embedded video player. Requires `links.embed:write` scope, publicly accessible URL in app's unfurl domains.

### input

Collects user data in modals, messages, and Home tabs. Requires `label` (plain_text, 2000 chars) and one compatible element. See [references/ELEMENTS.md](references/ELEMENTS.md) for all input element types.

### plan

Container for sequential task cards, designed for AI agent output. Messages only.

```json
{
  "type": "plan",
  "title": "Thinking completed",
  "tasks": [
    { "task_id": "t1", "title": "Fetched data", "status": "complete" },
    { "task_id": "t2", "title": "Generating report", "status": "in_progress" }
  ]
}
```

Task status values: `pending`, `in_progress`, `complete`, `error`. Each task is a `task_card` block with optional `details`, `output` (rich_text), and `sources` (url elements).

### file

Remote file reference. Read-only. Cannot be directly added to messages by apps.

## Composition Objects

### Option Object

Used in select menus, overflow, checkboxes, radio buttons:

```json
{
  "text": { "type": "plain_text", "text": "Option 1" },
  "value": "opt_1",
  "description": { "type": "plain_text", "text": "Detailed description" }
}
```

Text max 75 chars. `value` max 150 chars. `description` optional, max 75 chars.

### Confirmation Dialog

```json
{
  "title": { "type": "plain_text", "text": "Are you sure?" },
  "text": { "type": "plain_text", "text": "This action cannot be undone." },
  "confirm": { "type": "plain_text", "text": "Yes, do it" },
  "deny": { "type": "plain_text", "text": "Cancel" },
  "style": "danger"
}
```

### Conversation Filter

Filters conversation select menus. `include`: `im`, `mpim`, `private`, `public`.

### Dispatch Action Configuration

Controls when input elements trigger `block_actions`: `on_enter_pressed`, `on_character_entered`.

See [references/COMPOSITION.md](references/COMPOSITION.md) for full property tables.

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
| action_id / block_id | 255 chars |
| Overflow options | 5 |
| Select options | 100 |
| Option text | 75 chars |
| Placeholder text | 150 chars |
| File input max file size | 10MB per file |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Blocks without `text` fallback | Empty notifications, no accessibility fallback | Always provide `text` in `chat.postMessage` |
| `text` and `blocks` diverge | Confusing: notification says one thing, chat shows another | Keep semantically aligned |
| Blocks for simple replies | Visual noise for short responses | Use `text` only for simple replies |
| 2+ tables in one message | `invalid_attachments` error | One table per message |
| `mrkdwn` in header text | Ignored — headers only accept `plain_text` | Use `plain_text` type |
| Long header text | Silently truncated at 150 chars | Keep under 150 |
| Missing `alt_text` on images | Accessibility failure, API may reject | Always include alt_text |

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

## Surfaces Overview

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

Work Objects use `chat.unfurl` with a `metadata` parameter containing entity type, external reference, and entity payload. See [references/WORK-OBJECTS.md](references/WORK-OBJECTS.md) for full implementation details.

## Reference Documentation

| File | Purpose |
|------|---------|
| [references/CHEATSHEET.md](references/CHEATSHEET.md) | Quick reference: all blocks, elements, limits at a glance |
| [references/BLOCKS.md](references/BLOCKS.md) | All 15 block types with full property tables and constraints |
| [references/ELEMENTS.md](references/ELEMENTS.md) | All 20 interactive elements with properties and constraints |
| [references/COMPOSITION.md](references/COMPOSITION.md) | Composition objects: text, option, confirmation, filters |
| [references/RICH-TEXT.md](references/RICH-TEXT.md) | Rich text block deep dive: sub-elements, inline types, styles |
| [references/SURFACES.md](references/SURFACES.md) | Modals, App Home, canvases, lists, split view |
| [references/WORK-OBJECTS.md](references/WORK-OBJECTS.md) | Entity types, chat.unfurl, flexpane, editable fields, actions |

## Sources

- [Block Kit Reference](https://docs.slack.dev/reference/block-kit) — Slack
- [Block Kit Blocks](https://docs.slack.dev/reference/block-kit/blocks) — Slack
- [Block Kit Elements](https://docs.slack.dev/reference/block-kit/block-elements) — Slack
- [Block Kit Composition Objects](https://docs.slack.dev/reference/block-kit/composition-objects) — Slack
- [Work Objects](https://docs.slack.dev/messaging/work-objects) — Slack
- [Surfaces](https://docs.slack.dev/surfaces) — Slack
- [Modals](https://docs.slack.dev/surfaces/modals) — Slack
- [App Home](https://docs.slack.dev/surfaces/app-home) — Slack
- [Canvases](https://docs.slack.dev/surfaces/canvases) — Slack
- [Lists](https://docs.slack.dev/surfaces/lists) — Slack
- [Split View](https://docs.slack.dev/surfaces/split-view) — Slack
- [App Design](https://docs.slack.dev/surfaces/app-design) — Slack
