---
name: human-agentic-design
description: "Generates interactive HTML prototypes optimized for dual human+agent interaction. Produces semantic, accessible designs with Tailwind + DaisyUI (Tier A) or React + shadcn/ui + Vite (Tier B). Triggers on keywords: prototype, design, UI prototype, landing page, dashboard, form design, human-agentic, had, mockup, wireframe"
project-agnostic: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_resize
  - mcp__playwright__browser_click
  - mcp__playwright__browser_type
---

# Human-Agentic Design

Generates live, interactive prototype designs optimized for dual human+agent interaction. Every prototype is equally usable by humans (visual interaction) and AI agents (programmatic interaction via accessibility trees).

## Purpose

- Generate production-quality HTML prototypes with zero setup
- Enforce semantic HTML and accessibility standards that enable AI agent navigation
- Provide iterative visual + accessibility feedback via Playwright MCP
- Support two tiers: zero-dep HTML (Tier A) and React + shadcn/ui (Tier B)

## Workflow

### 1. Environment Probe

Detect available capabilities. Run these checks silently (no user prompting):

```bash
# Check Playwright MCP availability (tool list includes mcp__playwright__*)
# Check Node.js
which node 2>/dev/null && node --version
```

**Tier Selection:**
- Playwright MCP tools available -> Enable preview loop
- `node` binary found in PATH -> Offer Tier B (React + shadcn/ui + Vite)
- Default -> Tier A (single-file HTML + Tailwind CDN + DaisyUI CDN)

Report detected tier to user in one line:
```
Environment: Tier [A|B] | Playwright: [available|unavailable] | Node: [vX.Y.Z|not found]
```

If user explicitly requests a tier, honor that request regardless of detection.

### 2. Parse Request

Identify from user prompt:
- **Page type**: landing, dashboard, form, blog, portfolio, or custom
- **Design requirements**: colors, branding, content, layout preferences
- **Tier preference**: explicit tier request overrides auto-detection
- **Multi-page**: if multiple pages requested, plan linked file set

If page type matches a built-in template, use it as starting point. Read the template from `templates/<type>.html` within this skill directory.

### 3. Generate Code

**Tier A (HTML + Tailwind CDN + DaisyUI CDN):**
- Read `cookbook/tier-a.md` for boilerplate and CDN URLs
- Read `cookbook/agent-principles.md` for the 8 mandatory principles
- Generate single `index.html` (or multiple linked HTML files for multi-page)
- All CSS via Tailwind utility classes + DaisyUI component classes
- All JS vanilla, embedded in `<script>` tags
- If a template exists for the requested page type, read `templates/<type>.html` and customize

**Tier B (React + shadcn/ui + Vite):**
- Read `cookbook/tier-b.md` for scaffold structure
- Read `cookbook/agent-principles.md` for the 8 mandatory principles
- Generate full Vite project: `package.json`, `vite.config.ts`, `tsconfig.json`, `src/` tree
- Use shadcn/ui components (code-distributed, not npm dependency)
- Multi-page via React Router

**MANDATORY for ALL generated code (both tiers):**
1. Semantic HTML: `<main>`, `<nav>`, `<header>`, `<footer>`, `<article>`, `<section>`, `<button>` (not `<div onclick>`)
2. ARIA only when native HTML insufficient
3. `data-testid` on every interactive element (semantic names)
4. URL-driven state via search params
5. JSON-LD metadata in `<script type="application/ld+json">`
6. No Shadow DOM (light DOM only)
7. Explicit label associations (`<label for>`, `<fieldset>` + `<legend>`)
8. Keyboard navigable (tab order, focus indicators, escape to close modals)

### 4. Write Files

Output directory: `/tmp/claude-prototypes/<session-id>/`

Generate `<session-id>` as: `YYYYMMDD-HHMM-<slug>` where `<slug>` is a 2-3 word kebab-case description of the prototype.

```bash
# Create output directory
mkdir -p /tmp/claude-prototypes/<session-id>
```

Write all files using the Write tool.

### 5. Preview (Playwright MCP)

If Playwright MCP is available:

**Tier A preview:**
```
1. Start server:    python3 -m http.server 8080 -d /tmp/claude-prototypes/<session-id>
2. Navigate:        mcp__playwright__browser_navigate -> http://localhost:8080
3. Screenshot:      mcp__playwright__browser_take_screenshot (desktop viewport)
4. A11y snapshot:   mcp__playwright__browser_snapshot
5. Responsive:      mcp__playwright__browser_resize (375x667) -> screenshot -> resize back
```

**Tier B preview:**
```
1. Install deps:    cd /tmp/claude-prototypes/<session-id> && npm install
2. Start Vite:      npm run dev (background)
3. Navigate:        mcp__playwright__browser_navigate -> http://localhost:5173
4. Screenshot:      mcp__playwright__browser_take_screenshot
5. A11y snapshot:   mcp__playwright__browser_snapshot
6. Responsive:      mcp__playwright__browser_resize (375x667) -> screenshot -> resize back
```

**If Playwright MCP unavailable:**
Output file paths and manual open instructions:
```
Prototype ready at: /tmp/claude-prototypes/<session-id>/index.html

To preview:
  Option 1: open /tmp/claude-prototypes/<session-id>/index.html
  Option 2: cd /tmp/claude-prototypes/<session-id> && python3 -m http.server 8080
             Then open http://localhost:8080
```

### 6. Validate

After generating, validate against checklist (read `cookbook/validation.md`):
- Exactly one `<main>` element
- Exactly one `<h1>` element
- Heading hierarchy (no skipped levels)
- `data-testid` on all `<button>`, `<input>`, `<select>`, `<textarea>`, `<a>` elements
- No `<div onclick>` patterns (use `<button>` instead)
- All `<input>` elements have associated `<label>` or `aria-label`
- JSON-LD `<script>` present
- No Shadow DOM usage

Report validation result. Fix any failures before delivering.

### 7. Iterate

When user provides feedback:
1. Re-read relevant cookbook files if needed
2. Edit specific sections of generated files (prefer Edit over full rewrite)
3. Re-preview via Playwright MCP (if available)
4. Re-validate
5. Report changes made

### 8. Deliver

Provide:
- File paths for all generated files
- Setup instructions (if Tier B: `npm install && npm run dev`)
- Offer to copy to project directory

## Environment Detection Details

### Playwright MCP Detection

The skill's `allowed-tools` includes Playwright MCP tools. If these tools are available in the current session, the preview loop is enabled. If not available (tools not registered), graceful fallback to file paths only.

Do NOT error or warn loudly about Playwright absence. Simply skip the preview step and provide file paths.

### Node.js Detection

```bash
if command -v node &>/dev/null; then
    NODE_VERSION=$(node --version)
    echo "Node.js $NODE_VERSION detected - Tier B available"
else
    echo "Node.js not found - Tier A only"
fi
```

### Port Conflict Resolution (Tier A)

If `python3 -m http.server 8080` fails (port in use), try 8081, 8082, etc. up to 8090.

### Port Conflict Resolution (Tier B)

Vite auto-increments ports. If 5173 is taken, it uses 5174, etc. No manual handling needed.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Playwright MCP unavailable | Output file paths, print manual open instructions. NO error. |
| Node.js not installed | Stay on Tier A. Inform user Tier B requires Node.js. |
| CDN unreachable (offline) | Warn user. Suggest: `npm install -D tailwindcss daisyui` |
| Vite dev server fails | Fall back to Tier A single-file generation. |
| Port conflict | Auto-increment port (see above). |
| Template not found | Generate from scratch using principles + tier cookbook. |

## Anti-Patterns (NEVER DO)

- Never use `<div onclick>` -- always use `<button>` or `<a>`
- Never use non-semantic containers for landmarks -- use `<main>`, `<nav>`, `<header>`, `<footer>`
- Never skip heading levels (no `<h1>` then `<h3>`)
- Never omit `data-testid` on interactive elements
- Never use Shadow DOM for primary UI components
- Never use generic `data-testid` names like `field1`, `btn2` -- use semantic names
- Never generate placeholder/TODO comments in output -- all code must be complete and runnable
- Never require user to install dependencies for Tier A -- it must work with zero setup
- Never hardcode absolute paths to skill directory -- use relative references within the skill

## Output Format

After generation, output a summary:

```
## Prototype Generated

**Tier**: A (HTML + Tailwind CDN + DaisyUI CDN)
**Type**: <page-type>
**Files**:
  - /tmp/claude-prototypes/<session-id>/index.html

**Preview**: [screenshot if Playwright available]
**A11y Validation**: PASS | X landmarks detected: main, nav, header, footer
**Semantic Checks**: PASS | h1 present, heading hierarchy valid, N data-testid attributes

To open: open /tmp/claude-prototypes/<session-id>/index.html
```

## Responsive Breakpoints

When testing responsive design via Playwright MCP:

| Device | Width | Height |
|--------|-------|--------|
| Mobile | 375 | 667 |
| Tablet | 768 | 1024 |
| Desktop | 1440 | 900 |

## Supporting Files

- `cookbook/agent-principles.md` -- 8 agent-friendly design principles with code examples
- `cookbook/tier-a.md` -- Tier A boilerplate, CDN URLs, vanilla JS patterns
- `cookbook/tier-b.md` -- Tier B scaffold, package.json, Vite config, shadcn/ui setup
- `cookbook/preview-loop.md` -- Playwright MCP integration details and fallback behavior
- `cookbook/validation.md` -- Semantic HTML validation checklist
- `templates/landing.html` -- Landing page template
- `templates/dashboard.html` -- Dashboard template
- `templates/form.html` -- Multi-step form template
- `templates/blog.html` -- Blog/article template
- `templates/portfolio.html` -- Portfolio/gallery template
