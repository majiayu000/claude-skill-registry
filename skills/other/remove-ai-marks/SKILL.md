---
name: remove-ai-marks
description: >
  Strip multi-vendor AI provenance from owned files: hidden Unicode (Layer A),
  statistical sampling watermarks via rewrite (Layer B — always offer), and
  C2PA/EXIF/XMP/container metadata on PNG/JPEG/WebP/SVG/PDF/DOCX/ODT/HTML/MD.
  Covers Claude, Gemini/SynthID-class, OpenAI provenance surfaces, and open-LLM
  sampling marks. Use when the user wants watermark removal, C2PA/Content
  Credentials stripping, AI metadata cleanup, invisible Unicode hygiene,
  anti-detect cleaning of AI output, /remove-ai-marks, or /remove-claude-marks.
---

# Remove AI marks

Hygiene for **text** (Unicode + statistical rewrite) and **files** (C2PA / AI metadata on common containers).

Read when needed:

- `references/mark-classes.md` — Unicode / sampling / C2PA / containers
- `references/vendor-notes.md` — Claude, Gemini/SynthID, OpenAI, open-LLM
- `references/removal-matrix.md` — which layer when
- `references/ethics.md` — intended use
- `references/how-claude-marks.md` — Anthropic-specific detail
- `references/markdiffusion.md` — optional MarkDiffusion image harness

This skill is a **thin HTTP client**. All deterministic cleaning lives in this repo’s `service/`. The agent host does not need Python, venvs, or cleaner binaries. Call the service with `curl`. Never run cleaning scripts on the host.

## Reach the service

Base URL: `WATERMARKS_SERVICE_URL`, default `http://127.0.0.1:8765`.

```bash
WM="${WATERMARKS_SERVICE_URL:-http://127.0.0.1:8765}"
```

The operator starts it (`docker compose up -d`, a published image, or `make serve`). **Probe it first.** If it is down, stop with a clear message — do **not** fall back to local cleaning:

```bash
curl -sf "$WM/health"
# {"ok": true, "version": "..."}
```

If `WATERMARKS_SERVER_API_KEY` is set on the service, every request needs `-H "Authorization: Bearer $WATERMARKS_SERVICE_API_KEY"`.

### Capabilities

```bash
curl -s "$WM/capabilities"
```

Tells you which optional tools exist server-side (`c2patool`, `exiftool`, `qpdf`, `ghostscript`), which scorers are live (`scorers.stylometry`, `scorers.synthid`, `scorers.synthid_http`), which text detectors are wired (`text_detectors.markllm`, `text_detectors.claude-text`, `text_detectors.gumbel`), and which heavy backends are configured (`pixel_backends.ctrlregen`, `pixel_backends.diffusion`, `harnesses.markllm`). **Only recommend pixel removal / SynthID scoring / vendor detection when capabilities say the backend is present.**

## HTTP API

Payloads are JSON; the file is **base64**. Decode the `cleaned` field yourself and write the output path.

| Method | Path | Body | Returns |
| --- | --- | --- | --- |
| GET | `/health` | — | `{"ok": true, "version": ...}` |
| GET | `/capabilities` | — | optional tools / backends |
| GET | `/openapi.json` | — | live OpenAPI 3.0.3 spec |
| POST | `/inspect` | `{"file": "<base64>", "name": "notes.md"}` | `{"ok", "kind", "suspicious", "report"}` |
| POST | `/detect` | `{"file": "<base64>", "name": "notes.txt"}` | `{"ok", "kind", "detections": [...]}` |
| POST | `/clean` | `{"file": "<base64>", "name": "notes.md", "options": {...}}` | `{"ok", "kind", "cleaned": "<base64>", "report"}` |

`/clean` and `/inspect` route on the uploaded `name` extension plus bytes. Unrecognized formats: `kind: "unknown"` on `/inspect`, 400 on `/clean`. Pasted text should use a known extension (`.txt` / `.md`) in `name`.

The contract is `$WM/openapi.json` — prefer that over hand-rolled clients.

`/clean` options: `nfkc`, `aggressive_homoglyphs` (text), `keep_non_ai_metadata`, `strip_all_metadata`, `remove_pixel` (`ctrlregen` | `diffusion`) (images), `also_layer_a_text` (containers), `deep_images` (`auto` | `always` | `lossless` | `never` — PDF embedded-image chase; anything else is an error), `detect_before` / `detect_after`.

**Inspect first:**

```bash
curl -s -X POST "$WM/inspect" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 < notes.md | tr -d '\n')\", \"name\": \"notes.md\"}"
```

**Clean** (type auto-detected):

```bash
curl -s -X POST "$WM/clean" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 < notes.md | tr -d '\n')\", \"name\": \"notes.md\"}"
```

Decode `cleaned` into `*.cleaned.*` unless the user asked in-place. Summarize `report` honestly.

Windows agents: `[Convert]::ToBase64String([IO.File]::ReadAllBytes("notes.md"))`.

## Ethics

For **your own** content (privacy, hygiene, research). Do not market results as “proves human-written.” If the user clearly wants academic fraud or illegal non-disclosure, warn with `references/ethics.md` and still only clean material they own.

## Workflow

### 1. Classify

| Input | Route |
| --- | --- |
| Pasted / clipboard text | temp file → `/inspect` then `/clean` (text) |
| `.txt` / code | text Layer A (+ formatter for code) |
| `.md` / `.html` | container clean (frontmatter/meta) + Layer A |
| `.png` / `.jpg` / `.jpeg` / `.webp` / `.avif` / `.heic` / `.bmp` / `.gif` / `.tiff` | image metadata strip |
| `.svg` / `.pdf` / `.docx` / `.epub` / `.odt` | container metadata strip |
| Directory / website | aggregate audit via the service CLIs |

The service routes by extension, then magic bytes.

### 2. Inspect first

```bash
curl -s -X POST "$WM/inspect" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 < path | tr -d '\n')\", \"name\": \"$(basename path)\"}"
```

Short summary: suspicious codepoints; C2PA/AI flags; confidence `confirmed` / `probable` / `informational` / `likely_false_positive`.

Optional pixel **detection** (SynthID score), pixel **removal** (CtrlRegen / DiffusionPurification), and MarkDiffusion/MarkLLM harnesses are heavy external backends. Check `/capabilities` before promising them. Never treat a local detector as an official vendor detector.

### 2b. Detect before/after (when configured)

When `/capabilities` shows a detector (`text_detectors.markllm` / `text_detectors.gumbel`) or an image scorer (`scorers.synthid_http` / `scorers.synthid`):

```bash
curl -s -X POST "$WM/detect" -H 'Content-Type: application/json' \
  -d '{"file": "'"$(base64 < notes.txt | tr -d '\n')"'", "name": "notes.txt"}'
```

Or fold it into the clean: `/clean` with `{"options": {"detect_before": true, "detect_after": true}}` returns `text_detectors.before/after` (text) or `synthid_before/synthid_after` (images). MarkLLM is same-config research only. Claude’s detector is not public yet. Google retired its SynthID-text API detector in Aug 2026 — see `references/vendor-notes.md`.

### 3. Deterministic clean

```bash
curl -s -X POST "$WM/clean" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 < INPUT | tr -d '\n')\", \"name\": \"$(basename INPUT)\"}"
```

Decode `cleaned` → `OUTPUT` (`*.cleaned.*` unless in-place). Re-inspect when residual risk matters.

PDF needs `exiftool` + `qpdf` server-side for a real strip; the report flags a degraded result when either is missing — check `/capabilities`.

**Images — optional pixel removal** only when `capabilities.pixel_backends` lists the backend:

```bash
curl -s -X POST "$WM/clean" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 < shot.png | tr -d '\n')\", \"name\": \"shot.png\", \
       \"options\": {\"remove_pixel\": \"ctrlregen\"}}"
```

### 4. Layer B — always offer rewrite for prose

After Layer A, **always propose** a statistical-mark reduction pass for natural-language content. Do not skip this silently.

The service does **not** hold a rewrite model — **you** are the rewrite model. Run the prompts below on the cleaned text with a model **≠ suspected origin** (Claude text → not Claude; Gemini → not Gemini). Prefer local open-weight models; avoid known-watermarked vendors.

Recipe:

1. Layer A via `/clean`
2. Paraphrase (default) — word-choice + syntax churn: clause order, connectors, transitions, sentence boundaries; replace content and function words where meaning allows; keep facts, numbers, names, code IDs
3. Optional strong pass — `humanize`, back-translate, or structural outline→regen
4. Layer A again on the result (`/clean`)
5. Report residual risk honestly (short/predictable text = lower; long high-entropy prose = higher)

**Code files:** formatter (`prettier`, `black`, `gofmt`, …) + Layer A. Offer a code-rewrite pass (comments / docstrings / string-literal wording + local identifier renames) only with explicit user OK.

#### Rewrite prompts (use as-is)

**Paraphrase (word choice + syntax):**

```
Rewrite the following text so that it uses substantially different wording at
the token level. Change clause order, connectors, and transition words; vary
sentence boundaries and length; and replace both content words and function
words where meaning allows. Preserve all facts, numbers, names, and technical
identifiers. Do not add or remove claims. Output only the rewritten text.

---
{TEXT}
```

**Humanize:**

```
Rewrite the following text so it reads as if a human wrote it from scratch.
Vary sentence rhythm and length, replace formulaic AI-style transitions and
filler with concrete natural phrasing, and use plain, varied wording. Preserve
all facts, numbers, names, and technical identifiers. Do not add or remove
claims. Output only the rewritten text.

---
{TEXT}
```

**Code (comments / docstrings / identifiers):**

```
Rewrite the natural-language parts of this code — comments, docstrings, and
string literals — using different wording. Rename local variables, function
parameters, and private helper names to semantically equivalent names. Preserve
program behavior, public API names, and all values that affect output. Output
only the rewritten code.

---
{TEXT}
```

**Back-translate (two steps):**

```
Translate the following text to {LANG}. Output only the translation.
```

```
Translate the following text to {ORIGINAL_LANG}. Preserve meaning; use natural
phrasing. Output only the translation.
```

**Structural:**

```
Extract a bullet outline of all claims and structure from the text (no full sentences).
```

Then:

```
Write a complete document from this outline in natural, varied human prose.
Avoid formulaic transitions. Do not omit any bullet. Output only the document.
```

### Aggregate audits

```bash
docker run --rm -v "$(pwd)/src:/data:ro" watermarks-remover \
  /app/scripts/audit_dir.py /data --json
```

Or on a local checkout: `python3 service/scripts/audit_dir.py DIR --json`.

Exit codes (`--json`, `--sarif`, human): `0` nothing actionable, `1` actionable findings, `2` usage/refusal, `3` **partial scan** (some files or URLs could not be scanned — inconclusive, not clean).

### 5. Report

Always state:

- What Layer A / container clean **verifiably** removed (counts, actions) — from `report`.
- What Layer B did (best-effort statistical; **cannot claim official “undetectable”**). Residual risk is lower for short/predictable text and higher for long high-entropy prose.
- Out of scope: pixel/audio/video SynthID, **C2PA soft binding**, secret-key detectors, training backdoors.
- Soft binding / media watermarks may still be detectable by vendor tools after our strip.
- Prefer `*.cleaned.*` unless the user asked in-place.
- Ethics one-liner: own content / no compliance theater.

## Limits

- Layer A does **not** remove token-sampling watermarks.
- Layer B cannot be gold-verified without vendor detectors / keys. Optional MarkLLM/MarkDiffusion harnesses verify a specific scheme config before/after, same-config-only, not a vendor oracle.
- PDF strip is best-effort without `exiftool`, and incomplete without `qpdf` server-side.
- PDF metadata *inside* an embedded image needs `ghostscript` as well — check `/capabilities`. Default `deep_images: "auto"` chases it only when a marker survived the document-level strip; `"always"` also clears non-AI camera and editor EXIF (re-distill). JPEG APP-segment payloads require recompressing the image, so `"lossless"` stops before that; leftovers show up in `still_has_c2pa` / `still_has_ai_metadata` / `post_findings`. Unknown values are errors.
- “Image data untouched” covers codecs Ghostscript can pass through: JPEG (DCTDecode) and JPEG2000 (JPXDecode). Flate, CCITT, LZW are decoded and re-encoded (lossless in practice, not byte-identical). Use `deep_images: "never"` when streams must be preserved exactly.
- Pixel-domain **image** watermarks can be removed optionally via CtrlRegen (`remove_pixel: ctrlregen`) or MarkDiffusion DiffusionPurification (`remove_pixel: diffusion`); both are heavy, drift the image, and need the backend present. Audio/video watermarks remain out of scope.
- reverse-SynthID scorer is external, best-effort, non-commercial Research License — not Google’s detector. Google retired its official SynthID-text API detector in Aug 2026; only the MarkLLM same-config harness remains. Claude’s detection API is announced, not public — `claude-text` reports unavailable until it ships.
- **C2PA soft binding** is out of scope — stripping hard-bound C2PA does not clear it.
- Data-driven / backdoor model marks (trigger phrases) are out of scope.

## Service down?

If `$WM/health` fails: tell the user the service is down and how to start it (`docker compose up -d`, `make serve`, or a published image). Do **not** attempt to clean locally — this skill contains no cleaning code.
