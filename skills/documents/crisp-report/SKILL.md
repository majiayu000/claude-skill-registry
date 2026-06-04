---
name: crisp-report
description: Generate a beautiful single-file HTML report from the project's docs/ folder. Works after any CRISP phase, after Archaeology, or at sprint close in Execute. Triggers on "generate report", "export docs", "create HTML report", "share docs", or automatically at sprint close in CRISP Execute.
---

# CRISP Report Generator

Converts all markdown files in `docs/` into a single self-contained HTML file — cards overview, click-through to full documents, beautiful dark theme, no dependencies.

---

## How to run

**Step 1: Check dependencies**

```bash
pip3 install markdown pygments
```

If pip3 isn't available, try: `python3 -m pip install markdown pygments`

**Step 2: Run the script**

```bash
python3 scripts/generate-report.py [docs_dir] [output_file]
```

Defaults:
- `docs_dir` → `./docs`
- `output_file` → `./crisp-report.html`

Examples:
```bash
# Default — reads ./docs, outputs ./crisp-report.html
python3 scripts/generate-report.py

# Custom paths
python3 scripts/generate-report.py ./docs ./reports/sprint-3-report.html
```

**Step 3: Open**

```bash
open crisp-report.html
```

Or share the file directly — it's fully self-contained. No server needed.

---

## What it produces

- **Overview page** — card grid, one card per document, grouped by section (Discovery / Spec / Archaeology / Execute)
- **Document pages** — click any card → full rendered document with proper typography, code highlighting, tables
- **Escape / Back** → returns to overview
- Direct URL linking via `#doc-id` hash — shareable links to specific docs

---

## When to run

- **End of CRISP Phase S** — before handing off to Execute. Share with stakeholders for review.
- **End of each sprint** — updated report alongside the sprint delta doc. The stakeholder report section is already in the HTML.
- **After CRISP Archaeology** — share the recovered docs with the client or team.
- **Any time** — "generate report" at any point in a CRISP session.

---

## Script location

`scripts/generate-report.py` in the project root (copied from the CRISP repo).

If the script doesn't exist in the project yet, instruct the user to copy it from the CRISP repo:
```bash
curl -o scripts/generate-report.py https://raw.githubusercontent.com/radekamirko/C.R.I.S.P/main/scripts/generate-report.py
```
Or copy it manually from `C.R.I.S.P/scripts/generate-report.py`.

---

## Output file naming convention

| When | Suggested name |
|---|---|
| Phase S complete | `crisp-report.html` |
| Sprint N close | `crisp-report-sprint-N.html` |
| Archaeology complete | `crisp-report-archaeology.html` |
| Ad hoc | `crisp-report.html` (overwrites) |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'markdown'`**
→ Run: `pip3 install markdown pygments --break-system-packages`

**`No markdown files found in docs/`**
→ Make sure you're running from the project root, or pass the correct path: `python3 scripts/generate-report.py ./path/to/docs`

**Docs are blank or broken**
→ Check that docs are valid UTF-8 markdown. The script skips files it can't read.
