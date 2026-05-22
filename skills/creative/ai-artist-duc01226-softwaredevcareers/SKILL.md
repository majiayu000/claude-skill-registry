---
name: ai-artist
description: "Prompt + image gen. 6000+ examples. Dual-option: Standard (Flash) or Creative (Pro). Generate infographics, thumbnails, avatars, product shots with Nano Banana."
version: 2.2.0
license: MIT
---

# AI Artist - Prompt Engineering + Image Generation

Comprehensive prompt engineering with integrated image generation. Contains 6,000+ curated prompts, dual-option generation workflow, and searchable database with BM25 ranking.

## Dual-Option Workflow

When generating images, **always offer both options**:

| Option | Model | Best For | Speed |
|--------|-------|----------|-------|
| **Standard** | `gemini-2.5-flash-image` | Search-based prompts, known formats | Fast |
| **Creative** | `gemini-3-pro-image-preview` | Unique art direction, complex scenes | Best quality |

---

## Quick Start

### Option 1: Standard (Search + Flash)

```bash
# 1. Search for similar prompts
python3 .claude/skills/ai-artist/scripts/search.py "<keywords>" --domain examples

# 2. Generate with Flash model
.claude/skills/.venv/bin/python3 .claude/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate --model gemini-2.5-flash-image \
  --prompt "<adapted_prompt>" --aspect-ratio <ratio> --size 2K --output <path>
```

### Option 2: Creative (Art Direction + Pro)

```bash
# Generate with Pro model (4K, complex prompts)
.claude/skills/.venv/bin/python3 .claude/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate --model gemini-3-pro-image-preview \
  --prompt "<creative_prompt>" --aspect-ratio <ratio> --size 4K --output <path>
```

---

## Arguments

| Arg | Values | Default |
|-----|--------|---------|
| `--model` | `gemini-2.5-flash-image` (Standard), `gemini-3-pro-image-preview` (Creative) | Flash |
| `--aspect-ratio` | `1:1`, `16:9`, `9:16`, `3:4`, `4:3`, `2:3`, `3:2` | `1:1` |
| `--size` | `1K`, `2K`, `4K` (4K only Pro) | `2K` |
| `--num-images` | `1-4` | `1` |
| `--output` | file path | auto |

---

## Search Domains

```bash
python3 .claude/skills/ai-artist/scripts/search.py "<query>" --domain <domain>
```

| Domain | Use For |
|--------|---------|
| `examples` | 6000+ curated prompts (quote cards, bento grids, thumbnails) |
| `style` | Visual aesthetics (cyberpunk, minimalist, cinematic) |
| `subject` | Subject tips (portrait, product, landscape) |
| `platform` | Platform syntax (midjourney, dall-e, sd) |

---

## Creative Art Directions

For Creative option, apply unique styles:

| Style | Key Elements |
|-------|--------------|
| **Cyberpunk Neon** | Holographic, neon glow, rain, cityscape, Japanese text |
| **Vaporwave** | Greek statues, sunset grid, Windows 95, chrome, dolphins |
| **Isometric 3D** | Tilt-shift, miniature diorama, cute buildings, floating island |
| **Bento Grid** | Apple liquid glass, transparent cards, gradient glow |
| **Editorial** | Clean white, bold typography, magazine layout |

---

## Example Workflow

### User: "Create marketing infographic"

**Standard Option:**
```bash
python3 .claude/skills/ai-artist/scripts/search.py "bento grid marketing" --domain examples
# → Found: "Premium liquid glass Bento grid product infographic"
# → Adapt prompt, generate with Flash
```

**Creative Option:**
```bash
# Cyberpunk art direction with Pro model
.claude/skills/.venv/bin/python3 .claude/skills/ai-multimodal/scripts/gemini_batch_process.py \
  --task generate --model gemini-3-pro-image-preview \
  --prompt "Create a cyberpunk neon holographic infographic titled 'MARKETING 2026'. Style: Blade Runner aesthetic, dark cityscape, rain, neon data cards floating around holographic AI head. Hyper-detailed, cinematic." \
  --aspect-ratio 1:1 --size 4K --output infographic-cyberpunk.png
```

---

## References

| Topic | File |
|-------|------|
| Image generation workflow | `references/image-generation-workflow.md` |
| Nano Banana models | `references/nano-banana.md` |
| Prompt examples (6000+) | `references/nano-banana-pro-examples.md` |
| LLM patterns | `references/llm-prompting.md` |
| Image syntax | `references/image-prompting.md` |
| Domain patterns | `references/domain-patterns.md` |

---

## Anti-Patterns

| Issue | Solution |
|-------|----------|
| Only offering one option | Always present Standard AND Creative |
| Using Flash for complex art | Use Pro for unique art direction |
| Vague creative prompts | Add detailed style, layout, elements |
| Missing output path | Always specify `--output` |
