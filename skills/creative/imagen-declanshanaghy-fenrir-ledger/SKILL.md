---
name: imagen
description: "Generate images using Google Gemini API. Use this skill when the user says /imagen, asks to generate an image, create artwork, make a logo, or produce visual assets."
---

# Imagen — Image Generator

Generates images using Google's Gemini API. No theme prefix — prompts are passed through exactly as given.

---

## How to Run

```bash
npx tsx .claude/skills/imagen/generate.ts "<prompt>"
```

Or with a preset:

```bash
npx tsx .claude/skills/imagen/generate.ts --preset fenrir-logo
```

### Requirements

- Node.js 18+
- `tsx`
- `GOOGLE_API_KEY` or `GEMINI_API_KEY` environment variable

---

## CLI Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `prompt` | positional | *(required unless --preset)* | Free-form text prompt |
| `--preset` | choice | *(none)* | One of: `fenrir-logo`, `fenrir-icon`, `norse-badge`, `fenrir-medallion` |
| `--size` | string | `1:1` | Aspect ratio (`1:1`, `16:9`, `9:16`, `4:3`, `3:4`) |
| `--output` | path | `generated-{timestamp}.png` | Output file path |
| `--count` | int | `1` | Number of images (max 4) |

---

## Presets

| Preset | Prompt |
|--------|--------|
| `fenrir-logo` | Norse wolf head in circular medallion, runic border, silver and ice-blue |
| `fenrir-icon` | Compact wolf head icon, favicon-sized, Nordic, metallic |
| `norse-badge` | Norse shield badge, wolf and serpent knotwork, aged metal |
| `fenrir-medallion` | Iron medallion, Fenrir breaking chains, Elder Futhark runes, moonlit |

---

## Output

- PNG files saved to `--output` path or `generated-{timestamp}.png`
- Absolute path printed to stdout
- Exit 0 on success, 1 on error
