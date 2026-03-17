---
name: quick-view
description: Generate minimal HTML pages to review Claude Code output in a browser. Use when terminal output is hard to read, when reviewing lists/tables/drafts, or when user says "show me", "make this reviewable", "quick view", or "open as webpage". Produces unstyled semantic HTML only.
---

# Quick View

Generate minimal HTML to review structured data in a browser. No styling. Browser defaults only.

## When to Use

- User wants to review output that's hard to read in terminal
- Lists, tables, drafts, summaries that benefit from visual layout
- User says: "show me", "view this", "make reviewable", "open as webpage"

## Output Rules

**DO:**
- Semantic HTML only: `<table>`, `<ul>`, `<details>`, `<pre>`, `<h1-3>`
- Browser defaults (no CSS except the 3 lines below)
- Write to `_private/views/{name}.html`
- Open with `open _private/views/{name}.html`

**DO NOT:**
- Add colors, fonts, or decorative styling
- Use CSS classes or frameworks
- Add JavaScript unless essential for function
- Over-engineer or "make it nice"

## Template

Every quick-view HTML file:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body { max-width: 800px; margin: 40px auto; padding: 0 20px; font-family: system-ui; }
    table { border-collapse: collapse; width: 100%; }
    td, th { border: 1px solid #ccc; padding: 8px; text-align: left; }
  </style>
</head>
<body>
{content}
</body>
</html>
```

That's it. Three CSS rules for readability. No more.

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

### Expandable sections (for long content like drafts)
```html
<details>
  <summary><strong>@username</strong> — action</summary>
  <pre>Full draft text here...</pre>
</details>
```

### With actions
```html
<p>
  <a href="tg://resolve?domain=username">Open Telegram</a> ·
  <button onclick="navigator.clipboard.writeText('draft text')">Copy</button>
</p>
```

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

Include this script block at end of `<body>`:

```javascript
<script>
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
</script>
```

Add export button in header:
```html
<p>Generated: {date} · {count} drafts · <button onclick="exportEdits()">Export Edits</button></p>
```

## Workflow

1. Identify the data to display (file, variable, recent output)
2. Choose pattern: list, table, or expandable sections
3. Generate HTML using template above
4. Write to `_private/views/{name}.html`
5. Run `open _private/views/{name}.html`

## Example

User: "show me the drafts"

Claude:
1. Reads `_private/drafts/outreach_drafts.md`
2. Parses each draft (heading = contact, body = draft)
3. Generates HTML with `<details>` for each draft
4. Writes to `_private/views/drafts.html`
5. Runs `open _private/views/drafts.html`

Result: Browser opens, user sees expandable list of drafts, can copy each one.

