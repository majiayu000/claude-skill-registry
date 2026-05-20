---
name: cv-tailor
description: ATS-focused CV tailoring workflow from job URL/text/image to bullet-point output and optional Google Drive upload.
metadata: {"openclaw":{"emoji":"🧠","os":["darwin","linux"],"requires":{"bins":["node","gog"]}}}
---

# CV Tailor

Use this skill when the user asks to tailor a CV for a specific role, using:
- Job posting URL
- Copied JD text
- Screenshot/photo of JD text (OCR/vision-capable flow)

## Inputs accepted from Telegram

1. Job URL
2. JD pasted text
3. JD image/capture

If image text cannot be read reliably, ask user for pasted text fallback.

## Built-in resources

- `file_skill.ts`: safe read/write/list helper rooted at `~/openclaw_pro`
- `prompts/ATS_ALIGNMENT_ENGINE.md`
- `prompts/IMPACT_REFRAMING_ENGINE.md`
- `scripts/export_bullets_to_drive.sh`
- `scripts/cv_model_mode.sh`

## Standard runbook

0. Enter CV high-quality model mode (required):
   - `bash scripts/cv_model_mode.sh start`
1. Parse JD from URL/text/image.
2. Run ATS alignment analysis (keyword gaps, bullet rewrites, skills list).
3. Run impact reframing (summary + before/after impact bullets).
4. Read `master_cv.md` and tailor truthfully.
5. Save full version to `cv/CV_[Company]_[Role].md`.
6. Produce bullet-only version for copy/paste.
7. Upload bullet file to Google Drive (optional):
   - `bash scripts/export_bullets_to_drive.sh "$HOME/openclaw_pro/cv/CV_[Company]_[Role].md"`
8. Report saved local path + Drive file link/id.
9. Exit CV high-quality model mode (required, always run even on failure):
   - `bash scripts/cv_model_mode.sh end`

## Safety constraints

- Never fabricate experience, projects, skills, or credentials.
- Keep claims grounded in user-provided CV/history only.
- For unknown metrics, request estimate or use qualitative impact.

## Quality mode (CV-only)

- CV tasks must use `google/gemini-2.5-pro` while the task is running.
- Normal tasks should remain on stable default (`google/gemini-2.5-flash`).
- If provider outage/rate-limit forces fallback, explicitly report fallback in response.
