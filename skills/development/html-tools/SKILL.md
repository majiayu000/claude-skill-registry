---
name: html-tools
description: This skill should be used when building single-file browser applications, client-side utilities, or interactive tools that need no backend. Covers patterns for state persistence, API integration, and advanced browser capabilities without React or build steps.
---

# HTML Tools

Build single-file applications combining HTML, CSS, and JavaScript that deliver useful functionality without build steps, frameworks, or servers.

Based on Simon Willison's patterns from building 150+ such tools.

## When to Use

- "Build me a tool that..."
- "Create a simple app to..."
- "Make a utility for..."
- Client-side data processing or visualization
- Tools that should work offline or be easily shared
- Prototypes that need to ship fast

## When to Skip

- Apps requiring authentication or persistent server storage
- Complex state management across many components
- Projects where React/Vue ecosystem benefits outweigh simplicity

## Core Principles

1. **Single file** — Inline CSS and JavaScript. One HTML file = complete tool.
2. **No React** — Vanilla JS or lightweight libraries only. Explicitly prompt "No React."
3. **No build step** — Load dependencies from CDNs, not npm.
4. **Small codebase** — Target a few hundred lines. If larger, reconsider scope.

## Development Workflow

### Starting a New Tool

1. Begin with Claude Artifacts, ChatGPT Canvas, or similar for rapid prototyping
2. Prompt explicitly: "Build this as a single HTML file. No React. No build steps."
3. For complex tools, use Claude Code or similar coding agents
4. Host on GitHub Pages for permanence

### Iterating

1. Remix existing tools as starting points
2. Record LLM transcripts in commit messages for documentation
3. Build debugging tools (clipboard viewer, CORS tester) to understand browser capabilities

## State Persistence Patterns

### URL State (for shareable links)

Store configuration in URL hash or query params. Users can bookmark or share exact state.

```javascript
// Save state to URL
function saveState(state) {
  const params = new URLSearchParams(state);
  history.replaceState(null, '', '?' + params.toString());
}

// Load state from URL
function loadState() {
  return Object.fromEntries(new URLSearchParams(location.search));
}

// On page load
const state = loadState();
if (state.color) applyColor(state.color);
```

### localStorage (for secrets and large data)

Store API keys and user preferences without server exposure.

```javascript
// Store API key securely (never in URL)
localStorage.setItem('openai_api_key', key);

// Retrieve
const key = localStorage.getItem('openai_api_key');

// Prompt user if missing
if (!key) {
  key = prompt('Enter your OpenAI API key:');
  localStorage.setItem('openai_api_key', key);
}
```

## Data Input/Output Patterns

### Copy-Paste as Data Transfer

Treat clipboard as the universal data bus. Always include "Copy to clipboard" buttons.

```javascript
async function copyToClipboard(text) {
  await navigator.clipboard.writeText(text);
  showToast('Copied!');
}

// Rich clipboard (multiple formats)
async function copyRich(html, text) {
  const blob = new Blob([html], { type: 'text/html' });
  const item = new ClipboardItem({
    'text/html': blob,
    'text/plain': new Blob([text], { type: 'text/plain' })
  });
  await navigator.clipboard.write([item]);
}
```

### File Input Without Server

Accept file uploads that process entirely client-side.

```html
<input type="file" id="fileInput" accept=".json,.csv,.txt">

<script>
document.getElementById('fileInput').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  const text = await file.text();
  processFile(text, file.name);
});
</script>
```

### File Download Without Server

Generate and download files entirely in browser.

```javascript
function downloadFile(content, filename, mimeType = 'text/plain') {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// Usage
downloadFile(JSON.stringify(data, null, 2), 'export.json', 'application/json');
```

## API Integration

### CORS-Enabled APIs (call directly from browser)

These APIs allow direct browser requests without a proxy:

| API | Use Case |
|-----|----------|
| GitHub API | Repos, gists, issues |
| PyPI | Package metadata |
| iNaturalist | Species observations |
| Bluesky | Social data |
| Mastodon | Fediverse data |
| OpenAI/Anthropic | LLM calls (with user's key) |

### LLM API Pattern

Call LLM APIs directly using localStorage-stored keys.

```javascript
async function callClaude(prompt) {
  const key = localStorage.getItem('anthropic_api_key');
  if (!key) throw new Error('No API key');

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': key,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      messages: [{ role: 'user', content: prompt }]
    })
  });

  return response.json();
}
```

### GitHub Gists for Persistent State

Use gists as a free, CORS-friendly database.

```javascript
async function saveToGist(gistId, filename, content, token) {
  await fetch(`https://api.github.com/gists/${gistId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      files: { [filename]: { content: JSON.stringify(content) } }
    })
  });
}
```

## Advanced Capabilities

### Pyodide (Python in Browser)

Run Python, pandas, matplotlib entirely client-side.

```html
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
async function runPython(code) {
  const pyodide = await loadPyodide();
  await pyodide.loadPackage(['pandas', 'matplotlib']);
  return pyodide.runPython(code);
}
</script>
```

### WebAssembly Libraries

Run compiled libraries in browser:
- **Tesseract.js** — OCR for images and PDFs
- **FFmpeg.wasm** — Video/audio processing
- **sql.js** — SQLite in browser

```html
<!-- Tesseract OCR example -->
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@4/dist/tesseract.min.js"></script>
<script>
async function ocr(imageUrl) {
  const result = await Tesseract.recognize(imageUrl, 'eng');
  return result.data.text;
}
</script>
```

## Output Format

When building an HTML tool, deliver:

```
HTML TOOL: [name]

[Complete single-file HTML with inline CSS and JavaScript]

FEATURES:
- [Key capability 1]
- [Key capability 2]

USAGE:
[Brief instructions]

HOST: Save as .html and open in browser, or deploy to GitHub Pages.
```

## Reference

[Useful patterns for building HTML tools](https://simonwillison.net/2025/Dec/10/html-tools/) — Simon Willison
