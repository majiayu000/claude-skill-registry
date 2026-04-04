---
name: mobile-app-icon
description: Generate mobile app icons using OpenAI or Gemini image generation. Use when creating iOS icons, Android icons, app icons, or generating icon assets.
allowed-tools: Bash, Read
---

# Mobile App Icon Generation

Generate professional app icons using OpenAI or Gemini image generation APIs.

## Configuration

Check if `~/.claude/plugins/mobile-app-icon/config.json` exists (user config is stored at this fixed path, not in the plugin cache).

If missing, tell the user:
> Create `~/.claude/plugins/mobile-app-icon/config.json` with:
> ```json
> {
>   "openai_api_key": "sk-...",
>   "gemini_api_key": "..."
> }
> ```
> Include whichever API keys you want to use.

## Generating Icons

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/generate.sh "PROMPT" [OPTIONS]
```

### Options

| Option | Values | Default |
|--------|--------|---------|
| `--model` | OpenAI: `gpt-image-1`, `dall-e-3`, `dall-e-2`. Gemini: `gemini` (Gemini 3 Pro), `gemini-flash` (Gemini 2.5 Flash) | `gpt-image-1` |
| `--size` | OpenAI only (see sizes below) | `1024x1024` |
| `--aspect-ratio` | Gemini only: `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | `1:1` |
| `--quality` | `auto`, `high`, `medium`, `low`, `hd`, `standard` | `auto` |
| `--style` | See styles below | none |
| `--raw` | Use prompt verbatim | flag |
| `--num` | 1-10 (OpenAI only, dall-e-3 supports only 1) | `1` |
| `--background` | `auto`, `transparent`, `opaque` (gpt-image-1 only) | `auto` |
| `--output` | Output filename | `icon.png` |

### OpenAI Model Sizes

- `gpt-image-1`: `1024x1024`, `1536x1024`, `1024x1536`, `auto`
- `dall-e-3`: `1024x1024`, `1792x1024`, `1024x1792`
- `dall-e-2`: `256x256`, `512x512`, `1024x1024`

### Available Styles

| Style | Description |
|-------|-------------|
| `minimalism` | Clean, simple lines with 2-3 colors. Apple-inspired. |
| `glassy` | Semi-transparent glass elements with soft color blending. |
| `woven` | Textile-inspired patterns with woven textures. |
| `geometric` | Bold geometric shapes with mathematical precision. |
| `neon` | Electric neon colors on dark background. Cyberpunk. |
| `gradient` | Smooth, vibrant gradients. Instagram-inspired. |
| `flat` | Solid colors, no gradients/shadows. Microsoft-inspired. |
| `material` | Google Material Design with bold colors. |
| `ios-classic` | Traditional iOS with subtle gradients. |
| `android-material` | Android Material Design 3. |
| `pixel` | Retro 8-bit/16-bit pixel art style. |
| `game` | Vibrant gaming aesthetics with bold colors. |
| `clay` | Soft clay/plasticine textures. Playful aesthetic. |
| `holographic` | Iridescent rainbow-shifting metallic effects. |

### Examples

```bash
# OpenAI - basic icon
${CLAUDE_PLUGIN_ROOT}/scripts/generate.sh "a rocket ship"

# OpenAI - with style
${CLAUDE_PLUGIN_ROOT}/scripts/generate.sh "a coffee cup" --style minimalism

# OpenAI - transparent background
${CLAUDE_PLUGIN_ROOT}/scripts/generate.sh "a star" --background transparent

# Gemini - basic icon
${CLAUDE_PLUGIN_ROOT}/scripts/generate.sh "a rocket ship" --model gemini

# Gemini - square aspect ratio for app icon
${CLAUDE_PLUGIN_ROOT}/scripts/generate.sh "a music note" --model gemini --aspect-ratio 1:1

# Raw prompt (no enhancement)
${CLAUDE_PLUGIN_ROOT}/scripts/generate.sh "watercolor sunset" --raw
```

Output is saved to `~/.claude/plugins/mobile-app-icon/generated/`.
