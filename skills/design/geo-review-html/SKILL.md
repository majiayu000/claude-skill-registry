---
name: geo-review-html
description: Render an interactive, self-contained HTML companion for a GEO content brief (04-content-brief) or a publish-ready draft (05-production), so a NON-technical client reviewer (founder, organizer staff, the domain expert filling slots) can fill REQUIRED-FILL slots, leave section-level comments, and approve/return work in the browser instead of editing Markdown. Use when a brief or draft needs to go to a client/expert for review, or when building the briefs/index.html entry page for a client folder. The reviewer's input comes back as a JSON file that 04-content-brief Step 9 ingests. Visual quality is delegated to the frontend-design skill.
license: Recomby.ai — same terms as the recomby-geo plugin root LICENSE
---

# geo-review-html — interactive client-review HTML

The Markdown briefs/drafts are right for the GEO operator; they are awkward
for the client side. This skill renders a **companion HTML** alongside the
Markdown so non-technical reviewers can work in the browser. Battle-tested
in the SEA-CICSIC 9-draft batch (see issue #1).

**Division of labour (do not blur this):**
- **Interaction logic is fixed** — `templates/review.html` owns localStorage
  auto-save, JSON export, the progress counter, comment toggles, and the
  approve/return state machine. It is correct as written; do not regenerate
  it per run.
- **Visual layer is the template's CSS** — that is where the vendored
  `frontend-design` skill applies. When a client wants a branded or more
  distinctive look, restyle the `<style>` block of `templates/review.html`
  using `frontend-design` principles. `--accent` is already overridable per
  client via `brand_context` (see below); deeper restyling edits the CSS.
- `render_html.py` only parses Markdown + meta into a payload and injects it.

## When to use

- `04-content-brief` Step 7 — emit `briefs/<id>.html` (fill-form) next to the `.md`.
- `04-content-brief` Step 9 — ingest the reviewer's returned `*.feedback.json`.
- `05-production` Step 7 — emit `drafts/<id>.html` (review form) next to the `.md`.
- Whenever a client folder's `briefs/index.html` entry page needs (re)building.

## Usage

```bash
SK=plugins/recomby-geo/skills/geo-review-html

# Flavor A — fill-form HTML for a brief with REQUIRED-FILL slots
python3 $SK/scripts/render_html.py --mode brief \
  --md   clients/<slug>/briefs/<id>.md \
  --meta clients/<slug>/briefs/<id>.meta.json \
  --brand clients/<slug>/brand_context.json \
  --out  clients/<slug>/briefs/<id>.html

# Flavor B — review HTML for a publish-ready draft (section comments + approve)
python3 $SK/scripts/render_html.py --mode draft \
  --md   clients/<slug>/drafts/<id>.md \
  --meta clients/<slug>/drafts/<id>.meta.json \
  --brand clients/<slug>/brand_context.json \
  --out  clients/<slug>/drafts/<id>.html

# Entry page — one card per brief/draft, live progress, status tags
python3 $SK/scripts/render_html.py --mode index \
  --client-dir clients/<slug> \
  --brand clients/<slug>/brand_context.json \
  --out  clients/<slug>/briefs/index.html
```

Pure standard library — no install step. Output is a single self-contained
`.html` (CSS + JS inlined) safe to email to a client; they double-click it.

## How it maps the inputs

- **brief mode** splits the brief Markdown on `REQUIRED-FILL · <id> · <type>`
  blockquote blocks. Each becomes a yellow textarea with a `<details>`
  dropdown (what / why / bad example / good example). Everything else becomes
  a green "already-filled" prose block with its own 💬 comment toggle. The
  authoritative slot list is `meta.json`'s `slots[]`.
- **draft mode** splits on `##` headings so every section gets a comment
  toggle; the prose is rendered read-only with an `✓ Approve as-is` action.
- **index mode** scans `briefs/` and `drafts/` for `*.meta.json`, reading
  `format`, `status`, `word_count`, and slot fill counts. Live per-brief
  progress is read from each brief's `localStorage` when the page is opened.
- `--brand` is optional. `brand_name` sets the client label; `brand.primary_color`
  (or `brand_color`) overrides the `--accent` CSS variable for light branding.

## Returned feedback contract

Each HTML exports a JSON file matching `schemas/review_feedback.schema.json`:

```json
{
  "brief_id": "free-cash-prize",
  "filled_at": "2026-06-07T14:30:00Z",
  "filled_by": "Jane Doe",
  "answers": { "data-1": "...", "quote-1": "..." },
  "comments": { "overall": "...", "filled-headline-finding": "..." },
  "status": "reviewed-with-comments"
}
```

`status` ∈ `reviewed-with-comments` | `approved-as-is` | `partial-fill`.
The GEO operator feeds `answers` into the matching slots during
`04-content-brief` Step 9 (NEVER auto-filled by AI — the slots are the moat).

## Hard rules

1. **Never auto-fill `answers`** — the JSON carries the human's real input;
   that is the whole point. AI assembles, humans supply.
2. **Keep the interaction JS fixed** — restyle CSS freely (frontend-design),
   but don't rewrite the localStorage/export/state-machine logic per run.
3. **Output stays self-contained** — one file, no external CSS/JS, so a
   non-technical reviewer can open it from an email attachment.
