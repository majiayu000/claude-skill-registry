---
name: deploy
description: Render Quarto slides and deploy to GitHub Pages via CI/CD. Use when deploying lecture slides after making changes.
argument-hint: "[PaperName or 'all']"
allowed-tools: ["Read", "Bash"]
---

# Deploy Slides to GitHub Pages

Deployment is automated via GitHub Actions CI/CD. Pushing to `main` triggers rendering and deployment.

## Production Deploy (CI/CD)

1. **Commit and push** source changes to `main`
2. GitHub Actions automatically:
   - Renders all QMD files in `Quarto/`
   - Strips speaker notes from HTML (safety net)
   - Assembles site: HTML + RevealJS assets + Beamer PDFs + Figures
   - Deploys to GitHub Pages
3. **Verify** at the GitHub Pages URL

## Local Preview (Optional)

For testing before push:

1. **Run the sync script:**
   - If `$ARGUMENTS` is provided (e.g., "DreamZero"): `./scripts/sync_to_docs.sh $ARGUMENTS`
   - If no argument: `./scripts/sync_to_docs.sh` (syncs all lectures)

2. **Open in browser:**
   - `open docs/slides/PaperName.html`          # macOS

Note: `docs/` is gitignored — local preview output does not enter git.

## Speaker Notes Policy
- QMD source always contains `::: {.notes}` blocks (single source of truth)
- **Local** (`Quarto/*.html`): notes included — press `S` for speaker view
- **Public** (GitHub Pages): notes stripped by CI/CD pipeline
- Git clean filter strips notes from QMD before commit (`.gitattributes`)
