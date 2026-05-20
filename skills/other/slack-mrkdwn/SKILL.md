---
name: slack-mrkdwn
description: Proactively apply when generating any Slack text content, chat.postMessage text fields, or text objects with type "mrkdwn". Triggers on mrkdwn, Slack formatting, Slack markdown, Slack bold, Slack italic, Slack link syntax, Slack mentions, Slack date formatting, Slack escaping, Slack text object, verbatim, plain_text, Slack mrkdwn vs markdown, Slack blockquote, Slack code block, Slack strikethrough, Slack user mention, Slack channel mention, Slack emoji, link_names, auto-parsing. Use when formatting Slack message text, writing mrkdwn strings, constructing text objects, escaping user content for Slack, adding mentions or date formatting to messages, or debugging text rendering issues. Slack mrkdwn text formatting syntax for messages, text objects, and attachments.
---

# Slack mrkdwn

Slack's custom text formatting syntax for messages and text objects. Not standard Markdown.

## CRITICAL: Two Markup Systems

Slack has two completely different markup syntaxes. Using the wrong one is the most common formatting mistake.

| System | Used In | Bold | Link | Heading |
|--------|---------|------|------|---------|
| **Slack mrkdwn** | `text` field, text objects (`type: "mrkdwn"`), section fields | `*bold*` | `<url\|text>` | Not supported |
| **Standard Markdown** | `markdown` block only | `**bold**` | `[text](url)` | `# Heading` |

Standard Markdown syntax (`**bold**`, `[text](url)`, `# Heading`) renders as literal text in mrkdwn contexts. Slack mrkdwn syntax (`*bold*`, `<url|text>`) renders as literal text in markdown blocks. Never mix them.

The `markdown` block (`type: "markdown"`) accepts standard Markdown and translates it for Slack rendering. Supports: headings, bold, italic, strikethrough, lists, links, blockquotes, code blocks, images (rendered as link text). Does **not** support: syntax-highlighted code blocks, horizontal rules, tables, task lists. A single input block may produce multiple output blocks. Cumulative limit across all `markdown` blocks in one payload: 12,000 characters.

## mrkdwn Syntax

| Format | Syntax | Notes |
|--------|--------|-------|
| Bold | `*bold*` | Not `**bold**` |
| Italic | `_italic_` | Not `*italic*` |
| Strikethrough | `~strikethrough~` | Not `~~strikethrough~~` |
| Inline code | `` `code` `` | Same as standard Markdown |
| Code block | ` ```code``` ` | No syntax highlighting |
| Blockquote | `> quoted text` | Prefix each line |
| Link | `<https://example.com\|display text>` | Not `[text](url)` |
| Emoji | `:emoji_name:` | Standard or custom. Direct Unicode also works |
| Newline | `\n` | Literal newline in string |
| Ordered list | `1. item` | Plain text, no special rendering |
| Bullet list | `- item` | Rendered properly in `rich_text` blocks only |

Inline code disables all other formatting within it — use it to display literal text like `*not bold*`.

### Nested Formatting

Combining adjacent format markers without spaces (e.g., `*bold*_italic_`) is **unreliable** and may not render correctly. Always add a space between differently-formatted segments:

```
*bold* _italic_              ← works reliably
*bold*_italic_               ← may fail to render
```

For reliable combined formatting on a single word, use `rich_text` blocks with explicit style objects (`{"bold": true, "italic": true}`).

## Links

```
<https://example.com>                            Auto-detected URL
<https://example.com|Display Text>               URL with custom text
<mailto:user@example.com|Email Link>             Email link
```

URLs posted in text are auto-linked by Slack. Use `<url|text>` for custom display text. Spaces in URLs will break parsing — remove them. mrkdwn formatting inside link labels (e.g., `<url|*bold*>`) works for basic styles.

### Link Unfurling

Slack previews ("unfurls") linked content. Control this per message:

| Parameter | Controls | Default (API) |
|-----------|----------|---------------|
| `unfurl_links` | Text-based content previews | `false` |
| `unfurl_media` | Media (images, video, audio) previews | `true` |

Set both to `false` to suppress all previews. These are `chat.postMessage` parameters, not mrkdwn syntax.

## Mentions and References

### User Mentions

```
<@U0123ABC456>
```

Triggers a notification for the mentioned user. Auto-converts to display name.

### Channel References

```
<#C0123ABC456>
```

Auto-converts to channel name. Users without access see "private channel".

### User Group Mentions

```
<!subteam^SAZ94GDB8>
```

Notifies all members of the user group.

### Special Mentions

| Syntax | Scope | Caution |
|--------|-------|---------|
| `<!here>` | Active members in channel | Use sparingly |
| `<!channel>` | All channel members | Triggers push notifications for everyone |
| `<!everyone>` | All non-guest workspace members | Very disruptive |

### Best Practice

Always use IDs, not names. IDs are stable; names change:

```
  <@U0123ABC456>       (user ID)
  @chris                (name — may not resolve)

  <#C0123ABC456>       (channel ID)
  #general              (name — may not resolve)
```

To enable name-based parsing, set `link_names: 1` in the API call. This is fragile and discouraged.

## Date Formatting

Displays dates/times localized to the reader's **device timezone** (not their Slack preference timezone).

### Syntax

```
<!date^{unix_timestamp}^{token_string}^{optional_link}|{fallback_text}>
```

### Tokens

| Token | Example Output |
|-------|---------------|
| `{date_num}` | 2014-02-18 |
| `{date}` | February 18th, 2014 (omits year if within ~6 months) |
| `{date_short}` | Feb 18, 2014 |
| `{date_long}` | Tuesday, February 18th, 2014 |
| `{date_pretty}` | Yesterday / February 18th, 2014 |
| `{date_short_pretty}` | Yesterday / Feb 18, 2014 |
| `{date_long_pretty}` | Yesterday / Tuesday, February 18th, 2014 |
| `{time}` | 6:39 AM (12h) or 06:39 (24h) |
| `{time_secs}` | 6:39:42 AM |
| `{ago}` | 3 minutes ago / 4 hours ago |

`_pretty` variants use relative terms ("yesterday", "today", "tomorrow") when applicable.

### Examples

```
<!date^1392734382^{date} at {time}|February 18th, 2014 at 6:39 AM PST>
<!date^1392734382^{date_short_pretty} {time}|Feb 18, 2014 6:39 AM>
<!date^1392734382^{ago}|February 18th, 2014>
```

Tokens can be mixed with literal text in the token string. The optional link (third `^`-separated parameter) makes the date a clickable hyperlink. Fallback text (after `|`) displays for clients that cannot render date formatting.

## Escaping

Only three characters require escaping in mrkdwn:

| Character | Escape Sequence |
|-----------|----------------|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |

Do NOT encode other characters as HTML entities. Only these three are control characters in Slack's markup system.

When displaying user-generated content that may contain these characters, always escape them to prevent unintended formatting or link injection.

## Text Object

The text object is the most common composition object in Block Kit. It determines how text is rendered.

```json
{ "type": "mrkdwn", "text": "*bold* and _italic_", "verbatim": false }
{ "type": "plain_text", "text": "No formatting", "emoji": true }
```

`mrkdwn` supports Slack mrkdwn syntax. `plain_text` renders literally. `emoji: true` converts `:emoji:` to rendered emoji (plain_text only). Min 1 char, max 3000 chars (section `fields` max 2000 chars each, max 10 fields).

### Where Each Type Is Allowed

| Context | Allowed Types |
|---------|--------------|
| Header block text | `plain_text` only |
| Section text / fields | `mrkdwn` or `plain_text` |
| Context elements | `mrkdwn` or `plain_text` |
| Button text | `plain_text` only |
| Placeholder | `plain_text` only |
| Input label / hint | `plain_text` only |
| Modal title / submit / close | `plain_text` only |
| Option text | `plain_text` only |
| Option description | `mrkdwn` or `plain_text` |

### Verbatim Behavior

When `verbatim: false` (default):
- URLs auto-convert to clickable links
- Channel names auto-convert to channel links
- Mentions auto-parse

When `verbatim: true`:
- Markdown formatting still processes
- No auto-linking or mention parsing
- Useful for displaying raw URLs or text containing `@` or `#` that aren't mentions

```json
{ "type": "mrkdwn", "text": "Check the log at http://example.com/debug", "verbatim": true }
```

## Auto-Parsing Behavior

### The `parse` Parameter (chat.postMessage)

| Value | Effect |
|-------|--------|
| `"none"` (default) | mrkdwn formatting enabled; minimal auto-parsing of names/URLs |
| `"full"` | Disables mrkdwn formatting; auto-parses URLs, channel names, user mentions |

### Disabling Auto-Parsing

**In text objects:** Set `verbatim: true` (see above).

**In message payloads:**
- Omit `link_names` argument (or set to `0`)
- Set `parse: "none"` to disable all auto-parsing

## Disabling Formatting Entirely

| Context | Method |
|---------|--------|
| Text objects | Set `type` to `"plain_text"` |
| Top-level message `text` | Set `mrkdwn: false` |
| Attachments | Exclude field from `mrkdwn_in` array |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `**bold**` in mrkdwn | Renders literally | Use `*bold*` |
| `[text](url)` in mrkdwn | Renders literally | Use `<url\|text>` |
| `# Heading` in mrkdwn | Renders as plain text | Use `header` block or `markdown` block |
| `*bold*` in markdown block | Renders as italic | Use `**bold**` |
| `link_names: 1` for mentions | Fragile — names change, IDs don't | Use `<@USERID>` directly |
| HTML-encoding beyond `&<>` | Renders literally | Only escape `&`, `<`, `>` |
| Spaces in URLs | Breaks link parsing | URL-encode spaces as `%20` |
| Combining `*bold*_italic_` without space | Rendering unreliable | Add space: `*bold* _italic_` |

## Secondary Attachments (Legacy)

The `attachments` array adds secondary content below the main message. One of `fallback` or `text` is required (unless using `blocks`).

| Field | Description |
|-------|-------------|
| `fallback` | Plain-text summary for limited clients (always plain text) |
| `color` | Hex color or `"good"` / `"warning"` / `"danger"` |
| `pretext` | Text above the attachment block |
| `author_name`, `author_link`, `author_icon` | Small author line (16px icon) |
| `title`, `title_link` | Large heading with optional hyperlink |
| `text` | Main body (auto-collapses at 700+ chars) |
| `fields` | Array of `{ title, value, short }` objects |
| `image_url` | Full-width image (GIF, JPEG, PNG, BMP) |
| `thumb_url` | Thumbnail (75px max) |
| `footer`, `footer_icon`, `ts` | Footer metadata (footer max 300 chars) |
| `mrkdwn_in` | Array of fields to format with mrkdwn: `"text"`, `"pretext"`, `"fields"` |

Only `"text"`, `"pretext"`, and `"fields"` are accepted values in `mrkdwn_in`. Fields not listed render as plain text. `fallback` is always plain text.

**Prefer Block Kit blocks** over attachments for new development.

## Reference Documentation

| File | Purpose |
|------|---------|
| [references/CHEATSHEET.md](references/CHEATSHEET.md) | Quick reference: mrkdwn syntax, mentions, dates, escaping at a glance |

## Sources

- [Formatting Message Text](https://docs.slack.dev/messaging/formatting-message-text) — Slack
- [Block Kit Composition Objects — Text Object](https://docs.slack.dev/reference/block-kit/composition-objects/text-object) — Slack
- [Markdown Block](https://docs.slack.dev/reference/block-kit/blocks/markdown-block/) — Slack
- [Legacy Secondary Message Attachments](https://docs.slack.dev/legacy/legacy-messaging/legacy-secondary-message-attachments/) — Slack
- [Messaging Overview](https://docs.slack.dev/messaging) — Slack
