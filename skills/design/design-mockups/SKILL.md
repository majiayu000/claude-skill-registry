---
name: design-mockups
description: Build and present HTML/CSS design mockups with a local preview server. Use when prototyping website designs, iterating on visual concepts, or presenting design options.
---

# Design Mockups

Rapidly prototype and present HTML/CSS design mockups with a local server.

## Design Phases

Design work moves through distinct phases. **Know which phase you're in.**

### Phase 1: Style Exploration
**Goal:** Find the right visual direction for the entire site.

Create multiple concepts with different aesthetics (terminal, minimal, brutalist, etc.). Each mockup is a complete style — colors, typography, effects, vibe.

**Location:** `mockups/*.html` (root level)

```
mockups/
├── retro-terminal.html      # Concept A
├── minimal-stark.html       # Concept B
├── warm-organic.html        # Concept C
└── brutalist-chaos.html     # Concept D
```

**Outcome:** Pick a winner (e.g., `terminal-minimal-v2`).

---

### Phase 2: Site Templates
**Goal:** Build out all page types in the chosen style.

Create a subfolder named after the chosen direction. Build every major page template with shared styles.

**Location:** `mockups/{chosen-direction}/`

```
mockups/
├── terminal-v2-site/        # ← Chosen direction
│   ├── styles.css           # Shared design system
│   ├── home.html
│   ├── post.html
│   ├── about.html
│   ├── project.html
│   ├── archive.html
│   ├── search.html
│   └── 404.html
```

**Outcome:** Complete set of page templates.

---

### Phase 3: Section Explorations
**Goal:** Iterate on specific components or sections within the chosen style.

When a section needs multiple approaches (e.g., "how should projects be listed?"), create explorations inside the chosen direction folder.

**Location:** `mockups/{chosen-direction}/` with descriptive names

**Naming convention:** `{section}-{variant}.html`

```
mockups/
├── terminal-v2-site/
│   ├── styles.css
│   ├── home.html
│   ├── projects-grid.html         # Section exploration
│   ├── projects-file-tree.html    # Section exploration
│   ├── projects-file-tree-v2.html # Iteration on exploration
│   └── projects-hybrid.html       # Section exploration
```

**Outcome:** Pick the best approach for each section, integrate into templates.

---

## Project Structure

```
{project-name}/
├── mockups/
│   ├── concept-a.html           # Phase 1: Style exploration
│   ├── concept-b.html
│   ├── concept-c.html
│   └── {chosen-direction}/      # Phase 2+3: Templates & explorations
│       ├── styles.css           # Shared design system
│       ├── home.html            # Page template
│       ├── post.html            # Page template
│       ├── {section}-v1.html    # Section exploration
│       └── {section}-v2.html    # Section iteration
├── docs/
│   └── logs/                    # Session notes
├── server.js
├── package.json
└── README.md
```

## Quick Start

```bash
# Reserve a port first
portman reserve 3000 --name "{project-name}" --desc "Design mockups"

# Create project
mkdir -p ~/Developer/Projects/{project-name}
cd ~/Developer/Projects/{project-name}
mkdir -p mockups docs/logs

# Initialize
npm init -y
npm install express

# Copy server template (below)
npm start
```

## Server Template

Save as `server.js` — serves mockups with a gallery UI:

```javascript
const express = require('express');
const fs = require('fs');
const path = require('path');
const os = require('os');

const app = express();
const PORT = 3000;
const MOCKUPS_DIR = path.join(__dirname, 'mockups');

app.use('/mockups', express.static(MOCKUPS_DIR));

function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

const mockupMeta = {
  // 'filename-without-extension': { colors: ['#hex1', '#hex2'], desc: 'Description' }
};

app.get('/', (req, res) => {
  const mockups = fs.readdirSync(MOCKUPS_DIR)
    .filter(f => f.endsWith('.html'))
    .map(f => {
      const slug = f.replace('.html', '');
      const meta = mockupMeta[slug] || { colors: ['#ccc', '#999', '#666', '#333'], desc: '' };
      return { name: slug.replace(/-/g, ' '), file: f, path: `/mockups/${f}`, colors: meta.colors, desc: meta.desc };
    });

  res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mockups</title>
  <style>
    :root { --bg: #f5f5f5; --card: #fff; --text: #111; --muted: #666; --border: rgba(0,0,0,0.08); }
    @media (prefers-color-scheme: dark) { :root { --bg: #161616; --card: #222; --text: #eee; --muted: #888; --border: rgba(255,255,255,0.08); } }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; }
    .container { max-width: 900px; margin: 0 auto; }
    h1 { font-size: 1.25rem; margin-bottom: 2rem; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.25rem; }
    .card { background: var(--card); border-radius: 12px; overflow: hidden; text-decoration: none; color: inherit; box-shadow: 0 1px 3px var(--border); transition: transform 0.2s; }
    .card:hover { transform: translateY(-2px); }
    .preview { height: 100px; display: flex; padding: 1rem; gap: 0.5rem; }
    .swatch { flex: 1; border-radius: 6px; }
    .info { padding: 1rem; }
    .name { font-weight: 600; text-transform: capitalize; }
    .desc { font-size: 0.8rem; color: var(--muted); margin-top: 0.25rem; }
    .meta { margin-top: 2rem; font-size: 0.8rem; color: var(--muted); }
    code { background: var(--card); padding: 0.125rem 0.5rem; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Design Mockups</h1>
    <div class="grid">
      ${mockups.map(m => `<a href="${m.path}" class="card"><div class="preview">${m.colors.map(c => `<div class="swatch" style="background:${c}"></div>`).join('')}</div><div class="info"><div class="name">${m.name}</div><div class="desc">${m.desc}</div></div></a>`).join('')}
    </div>
    <div class="meta">Local: <code>http://localhost:${PORT}</code> · Network: <code>http://${getLocalIP()}:${PORT}</code></div>
  </div>
</body>
</html>`);
});

app.listen(PORT, '0.0.0.0', () => console.log(`Mockup server: http://localhost:${PORT} | http://${getLocalIP()}:${PORT}`));
```

## Naming Conventions

| Phase | Pattern | Example |
|-------|---------|---------|
| Style exploration | `{style-name}.html` | `retro-terminal.html` |
| Style iteration | `{style-name}-v2.html` | `terminal-minimal-v2.html` |
| Page template | `{page-type}.html` | `post.html`, `about.html` |
| Section exploration | `{section}-{variant}.html` | `projects-file-tree.html` |
| Section iteration | `{section}-{variant}-v2.html` | `projects-file-tree-v2.html` |

## Workflow Rules

1. **Know your phase** — Don't put section explorations in the root mockups folder
2. **Never overwrite** — Create new files for iterations (`-v2`, `-v3`)
3. **Shared styles in Phase 2+** — Use a `styles.css` for the chosen direction
4. **Document decisions** — Log sessions in `docs/logs/`
5. **Check port before answering** — `portman check {port}` to verify server state
6. **Update the index** — When adding/moving mockups, update `server.js` listings
7. **Restart after changes** — Kill and restart the server after updating `server.js`

## Updating the Gallery Index

The `server.js` file contains arrays that define what appears in the gallery:

```javascript
// Page templates in the chosen direction
const terminalV2Pages = [
  { name: 'Home', file: 'home.html', desc: 'Homepage with recent posts' },
  // ... add new pages here
];

// Section explorations
const projectsExplorations = [
  { name: 'File Tree', file: 'projects-file-tree.html', desc: 'ls -la style' },
  { name: 'File Tree v2', file: 'projects-file-tree-v2.html', desc: 'With icons' },
  // ... add new explorations here
];
```

**When you add a mockup:**
1. Create the HTML file in the correct location
2. Add an entry to the appropriate array in `server.js`
3. Restart the server: kill the process, run `npm start`

**When you move mockups:**
1. Move the files
2. Update the paths in `server.js` (e.g., `/mockups/terminal-v2-site/...`)
3. Restart the server

## Mockup Best Practices

### Phase 1 Mockups (Style Exploration)
- Self-contained HTML with embedded CSS
- Show the full vibe: colors, typography, effects
- Include enough content to judge the aesthetic
- No external dependencies (except fonts)

### Phase 2+ Mockups (Templates & Sections)
- Link to shared `styles.css`
- Focus on layout and content structure
- Real-ish content (not lorem ipsum if possible)
- Mobile-responsive

### Color Palette
Define 4-5 key colors:
```css
:root {
  --bg: #0d120d;
  --text: #6b8c5a;
  --accent: #9DFF20;
  --muted: #3d5a30;
}
```

### Common Effects

**CRT Scanlines:**
```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,0.15), rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px);
  pointer-events: none;
  z-index: 1000;
}
```

**Blinking Cursor:**
```css
.cursor {
  display: inline-block;
  width: 0.6em;
  height: 1em;
  background: var(--accent);
  animation: blink 1s step-end infinite;
}
@keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
```

## Tips

- **Iterate fast** — Don't perfect, explore
- **Test on phone** — Use network URL
- **Commit often** — Git tracks your exploration
- **Reserve ports** — Use `portman` to avoid conflicts
- **Update README** — Keep project docs current with the chosen direction
