---
name: quick-view
description: Generate minimal HTML pages to review Claude Code output in a browser. Use when terminal output is hard to read, when reviewing lists/tables/drafts, or when user says "show me", "make this reviewable", "quick view", or "open as webpage". Produces unstyled semantic HTML only. For granular feedback with inline comments, see the comment-mode skill.
---

# Quick View

Generate minimal HTML to review structured data in a browser. Minimal styling, maximum readability.

## When to Use

- User wants to review output that's hard to read in terminal
- Lists, tables, drafts, summaries that benefit from visual layout
- User says: "show me", "view this", "make reviewable", "open as webpage"

## Output Rules

**DO:**

- Semantic HTML: `<table>`, `<ul>`, `<details>`, `<pre>`, `<h1-3>`
- Use the base template with CSS variables
- Write to `_private/views/`
- Open with `open _private/views/{filename}`

**DO NOT:**

- Add decorative styling beyond the base template
- Use CSS frameworks
- Over-engineer or "make it nice"

## File Naming

Views have a lifecycle: temporary → keeper → archived.

| Stage | Filename | When |
|-------|----------|------|
| Temporary | `name-temp.html` | Default for new views |
| Keeper | `name.html` | User says "keep this", "this is good" |
| Archived | `name.2025-01-01.html` | Previous keeper when promoting new one |

**Rules:**

1. **Always create with `-temp` suffix** — Every new view starts as `name-temp.html`
2. **Promote on approval** — When user approves, rename to `name.html`
3. **Archive before replacing** — If `name.html` exists, rename to `name.DATE.html` before promoting
4. **Never regenerate keepers** — Only regenerate `-temp` files

**Workflow:**

```
# First iteration
drafts-temp.html  ← created

# User: "keep this"
drafts.html       ← promoted (temp deleted)

# Later iteration
drafts-temp.html  ← new temp created
drafts.html       ← keeper untouched

# User: "this is better, keep it"
drafts.2025-01-01.html  ← old keeper archived
drafts.html             ← new keeper promoted
```

**Trigger phrases for promotion:**

- "keep this", "this is good", "save this"
- "make this the default", "lock this in"
- "I like this one"

## Base Template

Every quick-view HTML file:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {
      --bg: #fff;
      --text: #222;
      --muted: #666;
      --border: #ddd;
      --accent: #1976d2;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #1a1a1a;
        --text: #e0e0e0;
        --muted: #999;
        --border: #333;
        --accent: #64b5f6;
      }
    }
    body {
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      font-family: system-ui;
      background: var(--bg);
      color: var(--text);
    }
    table { border-collapse: collapse; width: 100%; }
    td, th { border: 1px solid var(--border); padding: 8px; text-align: left; }
    .meta { color: var(--muted); font-size: 0.875rem; margin-bottom: 1rem; }
    details { margin: 0.5rem 0; }
    summary { cursor: pointer; }
    pre {
      background: var(--border);
      padding: 1rem;
      overflow-x: auto;
      border-radius: 4px;
    }

    /* Long content truncation */
    .truncate {
      max-height: 200px;
      overflow: hidden;
      position: relative;
    }
    .truncate.expanded { max-height: none; }
    .truncate:not(.expanded)::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 60px;
      background: linear-gradient(transparent, var(--bg));
    }
    .expand-btn {
      color: var(--accent);
      background: none;
      border: none;
      cursor: pointer;
      padding: 0.5rem 0;
      font-size: 0.875rem;
    }

    /* Type borders */
    .type-user { border-left: 3px solid var(--accent); padding-left: 1rem; }
    .type-draft { border-left: 3px solid #ff9800; padding-left: 1rem; }
    .type-done { border-left: 3px solid #4caf50; padding-left: 1rem; }

    /* Source attribution */
    .source { color: var(--muted); font-size: 0.75rem; }
    .source a { color: var(--muted); }
    .source a:hover { color: var(--accent); }
  </style>
</head>
<body>
<p class="meta">Generated: {timestamp} · {count} items</p>
{content}
<script>
// Truncation toggle
document.querySelectorAll('.truncate').forEach(el => {
  if (el.scrollHeight > 220) {
    const btn = document.createElement('button');
    btn.className = 'expand-btn';
    btn.textContent = 'Show more';
    btn.onclick = () => {
      el.classList.toggle('expanded');
      btn.textContent = el.classList.contains('expanded') ? 'Show less' : 'Show more';
    };
    el.after(btn);
  } else {
    el.classList.add('expanded'); // No truncation needed
  }
});
</script>
</body>
</html>
```

## Patterns

### List of items

```html
<h1>Title</h1>
<ul>
  <li><strong>@username</strong> — action item</li>
</ul>
```

### Table

```html
<table>
  <tr><th>Contact</th><th>Action</th><th>Draft</th></tr>
  <tr><td>@name</td><td>Follow up</td><td>Hey...</td></tr>
</table>
```

### Expandable sections (for long content)

```html
<details>
  <summary><strong>@username</strong> — action</summary>
  <div class="truncate">
    <pre>Long content here that may need truncation...</pre>
  </div>
</details>
```

### Type-differentiated items

```html
<div class="type-user">User message or input</div>
<div class="type-draft">Draft content</div>
<div class="type-done">Completed item</div>
```

### With actions

```html
<p>
  <a href="tg://resolve?domain=username">Open Telegram</a> ·
  <button onclick="navigator.clipboard.writeText('draft text')">Copy</button>
</p>
```

### Sourced data (citations & drill-down)

When displaying data gathered from external sources, always include attribution links for drill-down.

**Add to base template CSS:**

```css
.source { color: var(--muted); font-size: 0.75rem; }
.source a { color: var(--muted); }
.source a:hover { color: var(--accent); }
```

**Inline attribution (preferred for lists):**

```html
<div class="tip">
  <strong>Tip title</strong> — Description of the tip.
  <span class="source">— <a href="https://x.com/user/status/123">@username</a></span>
</div>
```

**Table with source column:**

```html
<table>
  <tr><th>Tip</th><th>Source</th></tr>
  <tr>
    <td>Description here</td>
    <td class="source"><a href="https://x.com/user/status/123">@user</a></td>
  </tr>
</table>
```

**Expandable with source in summary:**

```html
<details>
  <summary><strong>Tip title</strong> <span class="source">— <a href="URL">@source</a></span></summary>
  <p>Full content...</p>
</details>
```

**Meta header with main source:**

```html
<p class="meta">
  Generated: {timestamp} · {count} items ·
  Source: <a href="https://x.com/user/status/123">Original thread</a>
</p>
```

**Principles:**

- Always link to original when data comes from external sources
- Use `@username` for social media, domain for articles
- Source links should be muted/subtle, not prominent
- Include main source in meta header for collections from single source

### Editable drafts (with diff tracking)

For drafts that user may edit before sending. Tracks original vs edited for later analysis.

```html
<details>
  <summary><strong>@username</strong> — action <span class="status"></span></summary>
  <pre contenteditable="true"
       data-username="username"
       data-original="Original draft text here"
       onblur="saveDraft(this)">Original draft text here</pre>
  <div class="actions">
    <a href="tg://resolve?domain=username">Open Telegram</a>
    <button onclick="copyDraft(this)">Copy</button>
  </div>
</details>
```

Include this script block at end of `<body>` (before closing `</body>` tag):

```javascript
function saveDraft(el) {
  const key = 'draft_' + el.dataset.username;
  const edited = el.textContent.trim();
  const original = el.dataset.original;
  if (edited !== original) {
    localStorage.setItem(key, edited);
    el.closest('details').querySelector('.status').textContent = '(edited)';
  }
}

function copyDraft(btn) {
  const pre = btn.closest('details').querySelector('pre');
  navigator.clipboard.writeText(pre.textContent.trim());
  btn.textContent = 'Copied!';
  setTimeout(() => btn.textContent = 'Copy', 1500);
}

function restoreEdits() {
  document.querySelectorAll('pre[data-username]').forEach(el => {
    const saved = localStorage.getItem('draft_' + el.dataset.username);
    if (saved) {
      el.textContent = saved;
      el.closest('details').querySelector('.status').textContent = '(edited)';
    }
  });
}

function exportEdits() {
  const edits = [];
  document.querySelectorAll('pre[data-username]').forEach(el => {
    const original = el.dataset.original;
    const current = el.textContent.trim();
    if (original !== current) {
      edits.push({ username: el.dataset.username, original, edited: current });
    }
  });
  if (edits.length === 0) { alert('No edits to export'); return; }
  const blob = new Blob([JSON.stringify({exported_at: new Date().toISOString(), edits}, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'draft_edits.json';
  a.click();
}

restoreEdits();
```

Add export button in header when using editable drafts:

```html
<p class="meta">Generated: {timestamp} · {count} drafts · <button onclick="exportEdits()">Export Edits</button></p>
```

## Workflow

1. Identify the data to display (file, variable, recent output)
2. Choose pattern: list, table, or expandable sections
3. Generate HTML using template above
4. Write to `_private/views/{name}-temp.html`
5. Run `open _private/views/{name}-temp.html`
6. If user approves, promote to `{name}.html`

## Example

User: "show me the drafts"

Claude:

1. Reads `_private/drafts/outreach_drafts.md`
2. Parses each draft (heading = contact, body = draft)
3. Generates HTML with `<details>` for each draft
4. Writes to `_private/views/drafts-temp.html`
5. Runs `open _private/views/drafts-temp.html`

Result: Browser opens, user sees expandable list of drafts with auto dark/light mode, long content truncated with "Show more", can copy each one.

User: "this looks good, keep it"

Claude:

1. Renames `drafts-temp.html` → `drafts.html`
2. Confirms: "Saved as drafts.html"

## Styling Handoff

This skill produces functional HTML with minimal styling. For full visual styling, invoke the `html-style` skill after generating.

**Classes used by quick-view (compatible with html-style):**

| Class | Purpose |
|-------|---------|
| `.type-user` | User input/message |
| `.type-draft` | Draft content |
| `.type-done` | Completed item |
| `.source` | Attribution links |
| `.meta` | Metadata header |
| `.truncate` | Long content container |
| `.actions` | Action button container |

**Data attributes for JS hooks:**

- `data-username` — Identifier for drafts
- `data-original` — Original text for diff tracking

## Attribution

Truncation pattern and CSS variables approach inspired by [simon willison's claude-code-transcripts](https://github.com/simonw/claude-code-transcripts).
