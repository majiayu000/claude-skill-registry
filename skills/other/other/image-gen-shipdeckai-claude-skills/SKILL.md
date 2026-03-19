---
name: image-gen
description: Generate and edit images using AI providers (OpenAI DALL-E, Stability AI, BFL FLUX, Ideogram, FAL, Gemini, Replicate, Clipdrop). Use when user asks to create images, generate artwork, make logos, create visual content, edit photos, remove backgrounds, or modify existing images. Triggers on requests involving pictures, illustrations, graphics, product shots, marketing visuals, or any image creation/editing task.
---

# Image Generation

Generate images via CLI tool `image-gen` which handles provider selection, fallbacks, and image saving.

**Important:** Run commands using `node` with the plugin's CLI path:
```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/cli.bundle.cjs <command>
```

## Generate an Image

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/cli.bundle.cjs generate --prompt "description of image" [--provider auto] [--width 1024] [--height 1024]
```

Output: JSON with file paths to saved images in `.image-gen/` directory.

## Edit an Image

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/cli.bundle.cjs edit --image /path/to/image.png --prompt "edit instructions" [--provider auto]
```

## List Configured Providers

```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/cli.bundle.cjs providers
```

## Provider Selection

- `auto` (default): Intelligent selection based on prompt content
- Explicit: `openai`, `stability`, `bfl`, `ideogram`, `fal`, `gemini`, `replicate`, `clipdrop`

**Quick guide:**
- Text/logos/typography → `ideogram` or `recraft`
- Photorealism → `bfl` or `stability`
- Fast iterations → `fal`
- General purpose → `openai`
- Image editing → `openai`, `stability`, `bfl`, `gemini`, `clipdrop`

For detailed provider capabilities, see [references/providers.md](references/providers.md).

## Environment Setup

Add at least one API key to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Add to ~/.zshrc (or ~/.bashrc)
export OPENAI_API_KEY="sk-..."       # For DALL-E
export BFL_API_KEY="..."             # For FLUX (recommended for quality)
export IDEOGRAM_API_KEY="..."        # For text/logos (best typography)
export GEMINI_API_KEY="..."          # For Google Imagen
export STABILITY_API_KEY="..."       # For Stable Diffusion
export FAL_API_KEY="..."             # For fast iterations
export REPLICATE_API_TOKEN="..."     # For various models
```

After adding, run `source ~/.zshrc` or restart your terminal.

## Example Workflows

**Generate a logo:**
```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/cli.bundle.cjs generate --prompt "Modern minimalist logo for TechStartup with the text 'NOVA'" --provider ideogram --width 1024 --height 1024
```

**Generate product shot:**
```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/cli.bundle.cjs generate --prompt "Professional product photography of a sleek smartphone on marble surface, soft lighting" --provider bfl
```

**Edit an image:**
```bash
node ${CLAUDE_PLUGIN_ROOT}/dist/cli.bundle.cjs edit --image ./photo.png --prompt "Remove the background and make it transparent" --provider clipdrop
```
