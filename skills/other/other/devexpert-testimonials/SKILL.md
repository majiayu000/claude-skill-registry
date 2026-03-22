---
name: devexpert-testimonials
description: Import DevExpert testimonials from Google Sheets (gog) or pasted TSV lists, format text with line breaks, crop profile images to 400x400, copy them to src/assets/testimonials, update src/data/testimonials.json, and optionally update AI Expert IDs in src/pages/cursos/expert/ai.astro. Use when adding new testimonials or processing images.
---

# DevExpert Testimonials

## Overview
Automates testimonial import, profile image cropping, and AI Expert section management.

## Quick start
1. Install dependencies (first time only):
   ```bash
   python -m pip install -r scripts/requirements.txt
   ```
2. Import from Google Sheets (recommended). Run from the repo root:
   - Ensure gog is authenticated: `gog auth login` or `gog auth manage`.
   ```bash
   python scripts/sync_testimonials_from_sheet.py \
     --ai-auto
   ```
3. The script:
   - Detects rows where "Publicado en web" is empty.
   - Downloads photos from Drive via `gog drive download`.
   - Inserts line breaks automatically.
   - Generates new IDs in `src/data/testimonials.json`.
   - Crops images to 400x400 with face detection.
   - (Optional) Updates `src/pages/cursos/expert/ai.astro`.
   - Marks "Publicado en web" with `x`.
   - Stores temporary downloads in `tmp/testimonials-sync`.
4. Manual TSV fallback:
   ```bash
   python scripts/import_testimonials.py \
     --input /ruta/testimonios.txt
   ```

## Input format (flexible)
Prefer TSV (tab-separated) with columns in this order:
```
fecha \t nombre \t posicion \t titulo \t texto \t rating \t ruta_imagen
```
- Optional fields: posicion, rating, ruta_imagen.
- If there is no image, leave the column empty.
- Dates are normalized to `YYYY-MM-DD HH:MM:SS` when recognized.

## Images
- File names are generated from `nombre` + `titulo` (slug), e.g.:
  - `Santiago Perez Barber` + `AI Expert` -> `santiago-perez-barber-ai-expert.jpg`
- Uses face detection (OpenCV). If no face is detected, it uses center-crop.
- Default size: 400x400. Change with `--image-size`.
- Existing images are not overwritten unless `--overwrite-images` is passed.

## Google Sheets
- Current sheet schema: `references/sheet-schema.md`.
- "Publicado en web": any non-empty value is considered published.
- Configure defaults in `~/.config/skills/config.json` under `devexpert_testimonials`:
  - `account`
  - `sheet_id`
  - `gid` (optional)

Example:
```json
{
  "devexpert_testimonials": {
    "account": "you@example.com",
    "sheet_id": "spreadsheet_id_here",
    "gid": 123456789
  }
}
```

## AI Expert
- The script lists current IDs in `ai.astro` and the new ones detected by title.
- To write a specific list:
  ```bash
  python scripts/import_testimonials.py \
    --input /ruta/testimonios.txt \
    --ai-ids "35051,42724,42725"
  ```
- If `--ai-ids` is omitted, the script prompts for IDs (interactive stdin only).
- To auto-update with new IDs:
  ```bash
  python scripts/import_testimonials.py \
    --input /ruta/testimonios.txt \
    --ai-auto
  ```

## Useful options
- `--testimonials-json` change the `testimonials.json` path.
- `--images-dir` change the destination images folder.
- `--ai-astro` change the AI Expert page path.
- `--dry-run` show what would change without writing.
- `--ai-auto` automatically adds new AI Expert IDs.

## Scripts
- `scripts/import_testimonials.py` Imports testimonials, processes images, and proposes/updates AI Expert IDs.
- `scripts/sync_testimonials_from_sheet.py` Syncs from Google Sheets, downloads Drive images, and marks "Publicado en web".
