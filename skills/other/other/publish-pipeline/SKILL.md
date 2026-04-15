---
name: publish-pipeline
description: Markdown to HTML/PDF build + FTP sync to configured remote host. Pandoc + xelatex templates, branded output, automated deployment. Proven on 29-document HEL series.
version: 1.0.0
---

# Publish Pipeline

Activates when research documents need to be converted to publication formats and deployed to the live site.

## Build Chain

```
Markdown (.md) → pandoc → Standalone HTML (branded template)
                       → LaTeX PDF (xelatex, branded template)
```

## Prerequisites

- `~/.local/bin/pandoc` (v3.6+)
- `xelatex` (texlive-xetex)
- DejaVu fonts (for PDF)
- Templates at the project level: `template.tex`, `html-template.html`
- `build.sh` script in the project directory

## Build Command

```bash
bash www/tibsfox/com/Research/PROJECT/build.sh
```

## Template Setup

Each research project needs:
1. `template.tex` — LaTeX template (branded header/footer, colors, title page)
2. `html-template.html` — Standalone HTML template (dark theme, navigation)
3. `build.sh` — Iterates research/*.md, builds both formats

## FTP Sync

```bash
# Full site sync
bash scripts/sync-research-to-live.sh

# Single project sync (direct to FTP root)
lftp -f /tmp/lftp-PROJECT.sh
# Where remote path is /PROJECT (NOT /Research/PROJECT)
```

**Critical:** The web server maps `tibsfox.com/Research/X/` to FTP root `/X/`, not to `/Research/X/`. Always upload to root-level project directories.

## Series Integration

After publishing, add the project to `series.js`:
```javascript
{ id: 'CODE', name: 'Project Name', path: 'CODE/index.html' },
```
Alphabetical insertion by ID.
