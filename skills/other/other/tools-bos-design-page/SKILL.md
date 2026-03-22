---
name: tools-bos-design-page
description: Generate or enhance HTML documentation with polished visual diagrams (Mermaid flowcharts, state machines, sequence diagrams, Chart.js dashboards). Supports multiple documents via a references directory of reusable palettes, zoom controls, and initialization patterns. Use when asked to add diagrams to a guide, visualise a system or workflow, build a KPI dashboard, or improve documentation readability with visuals.
operating_mode: GENERATE
trigger_conditions: add diagrams, visualise system, build KPI dashboard, improve documentation readability, HTML docs, Mermaid charts, Chart.js dashboards
related_skills: lp-design-system, tools-ui-frontend-design
---

# tools-bos-design-page — Visual Documentation Enhancer

## Step 1: Choose Document

Ask the user which document to produce visuals for. Present known documents, plus the option to target an arbitrary file:

> Which document should I generate visuals for?
> 1. **email** — Brikette email system architecture (`docs/guides/brikette-email-system.html`)
> 2. **new document** — provide a file path and I will create or enhance it
>
> **Optional:** Which business is this for? (BRIK, PLAT, BOS, HEAD, PET, HBAG, PIPE, XA)
> If specified, palettes and Mermaid colors will be derived from the brand dossier.

Wait for the user's choice.

- If they say "email" or "1", proceed with the **Email Document Workflow** below.
- If they say "new document", "2", or provide a file path, proceed with the **New Document Workflow**.
- If they name a file path directly (e.g. `docs/guides/some-file.html`), treat it as the "new document" workflow with that path.

---

## Email Document Workflow

> This is the first document supported by tools-bos-design-page. It follows the same pattern as new documents (palette selection, reference loading, diagram insertion) but with proven, hardcoded diagram definitions that should not be modified.

**Target file:** `docs/guides/brikette-email-system.html`

Read the current file first. Then apply the four changes below in order. Do not remove any existing content — this is an additive enhancement.

---

### Change 1 — Add Mermaid CDN + Google Font to `<head>`

Append immediately before `</head>`:

```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    const dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    mermaid.initialize({
      startOnLoad: true,
      theme: 'base',
      look: 'classic',
      themeVariables: {
        primaryColor:       dark ? '#1e3d30' : '#e8f4ee',
        primaryBorderColor: dark ? '#2d6a4f' : '#2d6a4f',
        primaryTextColor:   dark ? '#f5f3f0' : '#1a1918',
        secondaryColor:     dark ? '#1a1918' : '#f9f8f6',
        secondaryBorderColor: dark ? '#6b6762' : '#e4e2de',
        tertiaryColor:      dark ? '#27201a' : '#fef3c7',
        tertiaryBorderColor: dark ? '#d97706' : '#d97706',
        lineColor:          dark ? '#6b6762' : '#9ca3af',
        edgeLabelBackground: dark ? '#1a1918' : '#f9f8f6',
        fontSize: '13px',
      }
    });
  </script>
```

---

### Change 2 — Add diagram CSS to `<style>` block

Append immediately before the closing `</style>` tag:

```css
    /* ── Mermaid diagram containers ── */
    .mermaid-wrap {
      position: relative;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 1.5rem 1.2rem 1rem;
      overflow: auto;
      margin: 1rem 0 1.5rem;
      scrollbar-width: thin;
      scrollbar-color: var(--border) transparent;
    }
    .mermaid-wrap .mermaid {
      transition: transform 0.2s ease;
      transform-origin: top center;
    }
    .zoom-controls {
      position: absolute;
      top: 8px;
      right: 8px;
      display: flex;
      gap: 2px;
      z-index: 10;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 2px;
    }
    .zoom-controls button {
      width: 26px; height: 26px;
      border: none; background: transparent;
      color: var(--text-muted);
      font-family: "SF Mono", monospace;
      font-size: 13px; cursor: pointer;
      border-radius: 3px;
      display: flex; align-items: center; justify-content: center;
      transition: background 0.15s, color 0.15s;
    }
    .zoom-controls button:hover { background: var(--border); color: var(--text); }
    .mermaid-wrap.is-zoomed  { cursor: grab; }
    .mermaid-wrap.is-panning { cursor: grabbing; user-select: none; }
    /* Force node/edge text to match page colour scheme */
    .mermaid .nodeLabel  { color: var(--text) !important; }
    .mermaid .edgeLabel  { color: var(--text-muted) !important; }
    .mermaid .edgeLabel rect { fill: var(--bg) !important; }
    .diagram-caption {
      font-size: 0.78rem;
      color: var(--text-muted);
      text-align: center;
      margin-top: -0.8rem;
      margin-bottom: 1rem;
      font-style: italic;
    }
    @media (prefers-reduced-motion: reduce) {
      .mermaid-wrap .mermaid { transition: none; }
    }
```

---

### Change 3 — Insert the three diagrams

Each diagram uses this container — use it as a template for all three:

```html
<div class="mermaid-wrap">
  <div class="zoom-controls">
    <button onclick="zoomDiagram(this,1.2)" title="Zoom in">+</button>
    <button onclick="zoomDiagram(this,0.8)" title="Zoom out">&minus;</button>
    <button onclick="resetZoom(this)" title="Reset zoom">&#8634;</button>
  </div>
  <pre class="mermaid">
    <!-- diagram syntax here -->
  </pre>
</div>
<p class="diagram-caption">Caption text</p>
```

#### Diagram A — System overview (three flows)

**Position:** immediately after the overview table (`</div>` closing the `.table-wrap`) and before `<div class="invariant">`.

```
flowchart TD
    INBOX["Customer email\narrives in Gmail"]
    FIRE["Prime writes record\nto Firebase Outbox"]
    BKNG["Booking confirmed\noccupant links ready"]

    ORG["gmail_organize_inbox\nStartup recovery + sort + trash garbage"]

    subgraph F1["Flow 1 — Inbound Response  ·  /ops-inbox"]
      PIPE["8-stage pipeline\ninterpret → generate → quality-check → refine → draft"]
    end
    subgraph F2["Flow 2 — Outbound Automated  ·  prime"]
      OUTB["prime_process_outbound_drafts\nFirebase → branded HTML → Gmail"]
    end
    subgraph F3["Flow 3 — Booking App-Links  ·  booking"]
      BOOK["mcp_send_booking_email\ncheck-in link email → Gmail"]
    end

    DRAFT["Gmail Draft\nBrikette/Drafts/Ready-For-Review"]
    HUMAN["Pete / Cristiana\nread · optionally edit · send manually"]

    INBOX --> ORG
    ORG -->|"Needs-Processing\nlabelled"| F1
    FIRE --> F2
    BKNG --> F3
    F1 --> DRAFT
    F2 --> DRAFT
    F3 --> DRAFT
    DRAFT --> HUMAN

    classDef flowborder fill:#e8f4ee22,stroke:#2d6a4f,stroke-width:1.5px,color:#1a1918
    classDef terminal fill:#f9f8f633,stroke:#e4e2de,stroke-width:1px
    classDef invariant fill:#fee2e222,stroke:#991b1b,stroke-width:1.5px
    class F1,F2,F3 flowborder
    class DRAFT terminal
    class HUMAN invariant
```

Caption: `Three separate ingestion paths — all output lands as a Gmail draft awaiting human action. Nothing is ever sent automatically.`

---

#### Diagram B — Flow 1: 8-stage pipeline

**Position:** immediately after `<h3>Per-email Pipeline (8 stages)</h3>` and before `<ol class="steps">`.

```
flowchart TD
    A["① gmail_get_email\nFetch body + thread context\n(prior messages as from/date/snippet triples)"]
    B["② draft_interpret\nEmailActionPlan v1.1.0\nscenarios[] · escalation · thread_summary\nagreement · workflow_triggers"]
    C{"escalation_required?"}
    DEFER["→ Brikette/Queue/Deferred\ngmail_mark_processed action:deferred\nno draft created"]
    D["③ draft_generate\nTemplate T01–T53  ·  7 knowledge resources\nemits email_fallback_detected on no-match"]
    E["④ draft_quality_check  Gate 1\nidentify unanswered questions\n& coverage gaps for patching"]
    F["⑤ Gap-patch loop\nClaude patches missing / partial entries\nfrom knowledge_summaries\nNo snippet → escalation sentence inserted\n⚠ prepayment + cancellation templates are LOCKED"]
    G["⑥ draft_refine\nClaude holistic rewrite + attest\nTool re-runs quality check internally\nReturns refinement_source: claude-cli"]
    H["⑦ draft_quality_check  Gate 2  MANDATORY\nAlways runs — even if no refinement applied\nFinal go / no-go before Gmail"]
    OK{"passed?"}
    J["⑧ gmail_create_draft  +  gmail_mark_processed\nSets In-Reply-To / References / threadId\nApplies Ready-For-Review + Outcome/Drafted + Agent/Claude\nEmits email_draft_created telemetry"]
    ESC["Escalate to user\nList failed_checks\nAsk: manual edit / defer / flag"]

    A --> B
    B --> C
    C -->|"CRITICAL\nor HIGH ≥ 0.80"| DEFER
    C -->|false| D
    D --> E --> F --> G --> H --> OK
    OK -->|yes| J
    OK -->|no| ESC

    classDef locked  fill:#fef3c733,stroke:#d97706,stroke-width:2px
    classDef danger  fill:#fee2e233,stroke:#991b1b,stroke-width:1.5px
    classDef good    fill:#e8f4ee33,stroke:#2d6a4f,stroke-width:1.5px
    classDef gate    fill:#ede9fe33,stroke:#5b21b6,stroke-width:1.5px
    class F locked
    class DEFER,ESC danger
    class J good
    class E,H gate
```

Caption: `Escalation is code-enforced, not behavioural — escalation_required:true skips draft_generate entirely. Both quality gates always run; Gate 2 is a hard stop.`

---

#### Diagram C — Gmail label state machine

**Position:** immediately after the opening paragraph of the Gmail Label Architecture section (`<p>Every email moves through a label state machine…</p>`) and before `<div class="label-tree">`.

Use `flowchart LR` (not `stateDiagram-v2` — state diagram labels cannot handle colons, slashes, or multi-word text reliably).

```
flowchart LR
    INBOX(["Inbox"])

    NP["Queue /\nNeeds-Processing"]
    IP["Queue /\nIn-Progress"]
    ND["Queue /\nNeeds-Decision"]
    DEF["Queue /\nDeferred"]

    DR["Outcome / Drafted\n+ Drafts / Ready-For-Review\n+ Agent / Claude"]
    ACK["Outcome /\nAcknowledged"]
    SKP["Outcome /\nSkipped"]
    PRO["Outcome /\nPromotional"]
    ERR["Outcome /\nError"]
    SENT["Drafts / Sent\n(after human sends)"]

    INBOX --> NP
    NP -->|"locked by\ngmail_get_email"| IP
    IP --> DR
    IP --> DEF
    IP --> ACK
    IP --> SKP
    IP --> PRO
    IP --> ERR
    IP -->|"T&amp;C status\nunclear or likely"| ND
    ND -->|"manual confirm"| IP
    DEF -.->|"manual escalation\nor re-queue"| IP
    ERR -.->|"startup recovery\nrequeues after 30 min"| NP
    DR --> SENT

    classDef queue   fill:#ede9fe33,stroke:#5b21b6,stroke-width:1.5px
    classDef outcome fill:#e8f4ee33,stroke:#2d6a4f,stroke-width:1px
    classDef error   fill:#fee2e233,stroke:#991b1b,stroke-width:1.5px
    classDef sent    fill:#f9f8f633,stroke:#e4e2de,stroke-width:1px
    class NP,IP,ND,DEF queue
    class DR,ACK,SKP,PRO outcome
    class ERR error
    class SENT sent
```

Caption: `Labels are the authoritative state record — not any external database. Startup recovery requeues stale In-Progress emails automatically on every run.`

---

### Change 4 — Add zoom JavaScript

Append immediately before the closing `</body>` tag (inside the existing `</div>` wrapper):

```html
  <script>
    function zoomDiagram(btn, factor) {
      var wrap = btn.closest('.mermaid-wrap');
      var el   = wrap.querySelector('.mermaid');
      var z    = Math.min(Math.max((parseFloat(el.dataset.zoom || '1')) * factor, 0.3), 5);
      el.dataset.zoom = z;
      el.style.transform = 'scale(' + z + ')';
      wrap.classList.toggle('is-zoomed', z > 1);
    }
    function resetZoom(btn) {
      var wrap = btn.closest('.mermaid-wrap');
      var el   = wrap.querySelector('.mermaid');
      el.dataset.zoom = '1';
      el.style.transform = '';
      wrap.classList.remove('is-zoomed');
    }
    document.querySelectorAll('.mermaid-wrap').forEach(function(wrap) {
      /* Ctrl/Cmd + scroll to zoom */
      wrap.addEventListener('wheel', function(e) {
        if (!e.ctrlKey && !e.metaKey) return;
        e.preventDefault();
        var el = wrap.querySelector('.mermaid');
        var z  = Math.min(Math.max((parseFloat(el.dataset.zoom || '1')) * (e.deltaY < 0 ? 1.1 : 0.9), 0.3), 5);
        el.dataset.zoom = z;
        el.style.transform = 'scale(' + z + ')';
        wrap.classList.toggle('is-zoomed', z > 1);
      }, { passive: false });
      /* Click-and-drag panning when zoomed */
      var sx, sy, sl, st;
      wrap.addEventListener('mousedown', function(e) {
        if (e.target.closest('.zoom-controls')) return;
        if (parseFloat(wrap.querySelector('.mermaid').dataset.zoom || '1') <= 1) return;
        wrap.classList.add('is-panning');
        sx = e.clientX; sy = e.clientY;
        sl = wrap.scrollLeft; st = wrap.scrollTop;
      });
      window.addEventListener('mousemove', function(e) {
        if (!wrap.classList.contains('is-panning')) return;
        wrap.scrollLeft = sl - (e.clientX - sx);
        wrap.scrollTop  = st - (e.clientY - sy);
      });
      window.addEventListener('mouseup', function() { wrap.classList.remove('is-panning'); });
    });
  </script>
```

---

## New Document Workflow

For any document not listed in the menu above.

### Step 1 — Gather target details

Ask the user:
1. **Target file path** — where to write or find the HTML file (e.g. `docs/guides/my-system.html`)
2. **Business** (optional) — which business is this doc for? (BRIK, PLAT, BOS, HEAD, PET, HBAG)
3. **Document domain** — one of: `operational`, `architecture`, `workflow`, `analytics`

If the user provides only a path, infer the domain from context or ask.

**Brand-derived palette**: If a business is specified, consult `references/css-variables.md` → "Brand-Derived Palettes" section for the business-to-palette mapping and any accent overrides. Load the brand dossier at `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` for color guidance. Also reference `.claude/skills/lp-design-system/SKILL.md` for token naming conventions — visual doc palettes should feel connected to the product UI.

For the render pipeline, per-business palettes can be passed via `--palette-file <path>` (see `references/css-variables.md` for the custom palette file format).

### Step 2 — Read or create the target file

- If the file exists, read it. This is an additive enhancement — do not remove existing content.
- If the file does not exist, create it using the rich template pattern: full HTML5 document with `<head>` (meta, fonts, Mermaid CDN, palette CSS) and `<body>` (title, sections, diagram placeholders). Use the structure of `docs/guides/brikette-email-system.html` as the canonical example.

### Step 3 — Load references

Read the following reference files and apply their contents:

1. **`references/css-variables.md`** — select the palette matching the document domain. Insert the `:root` and dark-mode CSS variables into the document's `<style>` block.
2. **`references/zoom-controls.md`** — insert the diagram container CSS and the zoom/pan JavaScript.
3. **`references/mermaid-init.md`** — insert the Mermaid CDN import and `mermaid.initialize()` call, substituting themeVariables from the palette mapping table.

### Step 4 — Design and insert diagrams

Analyze the document content and design diagrams appropriate to the subject matter:

- Identify the key concepts, flows, states, or relationships that benefit from visualization
- Choose diagram types from the supported set (see **Supported Diagram Types** below)
- Use the `mermaid-wrap` container template from `references/zoom-controls.md` for each diagram
- Add a `<p class="diagram-caption">` after each diagram
- Place diagrams near the text they illustrate

### Step 5 — Validate

- Confirm all Mermaid syntax parses (no unquoted special characters, no `\n` in labels)
- Confirm all CSS variables resolve against the chosen palette
- Confirm zoom controls are wired up (JavaScript present before `</body>`)

---

## References

The `references/` directory contains reusable building blocks for visual documents. Always read these when enhancing a document — do not hardcode values from memory.

| File | Purpose |
|------|---------|
| `references/css-variables.md` | 4 color palettes (operational, architecture, workflow, analytics) with light + dark mode |
| `references/zoom-controls.md` | Zoom/pan CSS + JavaScript for interactive Mermaid diagrams |
| `references/mermaid-init.md` | Mermaid CDN import, initialization config, ELK loader, classDef conventions |
| `references/diagram-types.md` | Supported Mermaid diagram types with selection guidance |
| `references/chartjs-usage.md` | Chart.js KPI dashboard patterns and the `chart` code fence format |

### Design System Cross-References

When generating visual docs for a specific business, also consult:

| File | Purpose |
|------|---------|
| `.claude/skills/lp-design-system/SKILL.md` | Token quick-ref — use for consistent color naming |
| `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` | Per-business brand language and color palette |
| `packages/themes/<theme>/src/tokens.ts` | Concrete token values for palette derivation |

---

## Supported Diagram Types

See `references/diagram-types.md` for full guidance on each type, including when to use and when to avoid.

Summary of supported types:

- **`flowchart`** (TD or LR) — the primary diagram type. Use for process flows, pipelines, decision trees, label state machines. Handles complex labels with special characters reliably.
- **`sequenceDiagram`** — temporal flows with multiple actors. Use for request/response patterns, API call chains, multi-system handshakes.
- **`stateDiagram-v2`** — simple state machines. Appropriate for simple state names (e.g., Pending, Active, Killed). Avoid when labels contain colons, slashes, or multi-word paths — use `flowchart` instead.
- **`mindmap`** — brainstorming and idea mapping. Use for taxonomy trees, feature decomposition, topic clustering.

---

## Chart.js KPI Dashboards

See `references/chartjs-usage.md` for the full guide including loader setup and configuration patterns.

Embed charts using the ` ```chart ` code fence format:

````
```chart
{
  "type": "bar",
  "data": {
    "labels": ["Jan", "Feb", "Mar", "Apr"],
    "datasets": [{
      "label": "Revenue",
      "data": [1200, 1900, 3000, 2500]
    }]
  }
}
```
````

The render pipeline transforms ` ```chart ` blocks into `<canvas>` elements with Chart.js initialization.

**Quality rule:** Prefer tables for <4 data points. Use charts when trends, comparisons, or distributions need visual emphasis.

---

## Delivery

1. Save the updated or newly created file.
2. Open in Chrome: `open <target-file-path>`
3. Report to the user:
   - Which diagrams were inserted and where in the document they appear
   - Which palette was applied (and the document domain)
   - That Ctrl+scroll and the +/-/reset buttons are available for each diagram
   - If Chart.js dashboards were added, confirm they render correctly

---

## Mermaid Quality Rules

Apply these to every diagram in this project:

- **Quote all labels with special chars** — parentheses `()`, colons `:`, slashes `/`, ampersands `&` go inside `["..."]` or `("...")` node labels. Unquoted special chars cause silent parse failures.
- **Prefer flowchart over stateDiagram-v2 when labels contain colons, slashes, or multi-word paths.** stateDiagram-v2 is appropriate for simple state names (e.g., Pending, Active, Killed).
- **Never set `color:` in `classDef`** — it hardcodes a value that breaks in the opposite color scheme. Use `fill:` with 8-digit hex (last 2 digits = opacity, e.g. `#2d6a4f33` for 20% opacity) so tints work in both light and dark.
- **CSS overrides for text color are mandatory** — `themeVariables.primaryTextColor` only affects default nodes. Add the `.mermaid .nodeLabel { color: var(--text) !important; }` override so text respects the page's color scheme.
- **Max ~20 nodes per diagram** — split complex flows rather than crowding.
- **For >20 nodes or >3 nested subgraphs, use ELK layout** via `%%{ init: { 'flowchart': { 'defaultRenderer': 'elk' } } }%%` directive at the top of the diagram. See `references/mermaid-init.md` for the ELK loader setup.
- **Arrow semantics**: `-->` primary flow, `-.->` async/recovery/optional, `==>` critical/highlighted path, `--x` blocked/rejected.
- **Escape `&` as `&amp;` inside `<pre class="mermaid">` blocks** — the browser parses HTML entities before Mermaid sees the text.
- **Never use `\n` in node labels** — `\n` renders as literal text. Use a real line break (Enter) inside the quoted label instead: `["line one\nline two"]` (wrong) vs `["line one` + newline + `line two"]` (correct).
- **`look: 'handDrawn'` is for draft/WIP only.** Never use it for published guides or production documentation.
