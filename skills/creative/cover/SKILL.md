---
name: cover
description: Generate book cover art prompts for image generation models. Reads project content and produces optimized prompts for Kindle-dimension covers.
---

Generate cover art prompts for your book using the cover-artist agent.

## What This Does

1. Asks whether you want image-only or text-inclusive covers
2. Reads your project materials (README, themes, characters, world, tone)
3. Synthesizes the story's visual essence
4. Produces 3-5 distinct cover concepts as image generation prompts
5. Optimizes for Kindle dimensions (2560 x 1600, aspect ratio 1.6:1)

## Usage

```
/fiction:cover                    # Generate cover prompts for current project
/fiction:cover /path/to/project   # Generate for specific project
```

## Text Options

You'll be asked whether to include text:

- **Image only** (recommended) — Clean image with negative space for title overlay in post-production. More control over typography.
- **Include text** — Title and author name generated as part of the image. Works well with GPT Image 1.5 and Gemini 3 Pro.

## Output

For each concept, you'll receive:
- **Approach** — The visual strategy
- **Prompt** — Ready to paste into Midjourney, DALL-E, or other generators
- **Why it works** — Genre signals and design rationale
- **Variations** — Style/mood alternatives

## Generating Images

Once you have prompts, you can generate images with any AI image tool. If you have [falcon](https://github.com/howells/falcon) installed, you can generate images directly from the command line:

```bash
falcon "your prompt here" --ar 5:8
```

## Prompt Compatibility

Prompts are optimized for:
- **Midjourney V7** — Use `--ar 5:8` for Kindle proportions
- **DALL-E 3** — Specify dimensions in prompt
- **Stable Diffusion** — Works with standard prompt structure
- **Other generators** — Adapt aspect ratio parameters as needed

## Design Philosophy

The agent prioritizes:
- **Symbolic over literal** — Evoke the feeling, don't illustrate the plot
- **Cut-through** — Stand out in crowded genre thumbnails
- **Genre signals** — Honor conventions while avoiding cliches
- **Thumbnail test** — Readable at 80px width
- **Title space** — Negative space in upper third for text overlay

## After Generation

**If you chose image-only:**
1. Generate images with your preferred AI tool (or falcon)
2. Select the strongest result
3. Add title and author name in a design tool (Canva, Photoshop, etc.)
4. Test at thumbnail size
5. Upload to KDP

**If you chose text-inclusive:**
1. Generate images—inspect text carefully for errors
2. Regenerate if any letters are wrong
3. Minor touch-ups in design tool if needed
4. Test at thumbnail size
5. Upload to KDP

## When to Use

- Final stages of manuscript completion
- Before submitting to beta readers (motivational)
- Marketing preparation
- Series branding exploration
