---
name: article-images
description: This skill should be used when the user asks to "generate article images", "create images for an article", "run image generation", "generate illustrations from prompts", or mentions article hero images, prompt markdown files, or batch image generation.
version: 0.4.0
---

# Article Image Generation

Generate high-quality images for articles using AI image generation. Supports multiple providers with **automatic fallback** when rate limits are hit and **parallel generation** for faster batch processing:

- **Google Gemini** (default) - Gemini 3 Pro Image / 2.5 Flash Image
- **OpenAI** - gpt-image-1.5

## Quick Start

```bash
# Generate with Gemini (default)
.claude/skills/article-images/scripts/generate-images.sh

# Generate with OpenAI gpt-image-1.5
.claude/skills/article-images/scripts/generate-images.sh --provider openai

# Generate specific article
.claude/skills/article-images/scripts/generate-images.sh --glob "articles/prompts/01-*.md"

# Generate in parallel (4 concurrent images)
.claude/skills/article-images/scripts/generate-images.sh --parallel 4

# Preview without generating (dry run)
.claude/skills/article-images/scripts/generate-images.sh --dry-run

# Force regenerate all images
.claude/skills/article-images/scripts/generate-images.sh --force
```

## Prerequisites

### For Gemini (default)

Requires Google Cloud credentials in `.env`:

```bash
# .env (gitignored)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

Also requires Application Default Credentials. Run once:

```bash
gcloud auth application-default login
```

### For OpenAI

Requires OpenAI API key in `.env`:

```bash
# .env (gitignored)
OPENAI_API_KEY=sk-...
```

## Providers

### Gemini (Default)

Uses Google's Vertex AI with these models:

- **gemini-3-pro-image-preview** (primary)
- **gemini-2.5-flash-image** (fallback)

Automatically handles rate limits and falls back between models.

### OpenAI

Uses gpt-image-1.5 with automatic size conversion:

- 16:9 → 1536x1024
- 4:3 → 1536x1024
- 1:1 → 1024x1024

## Auto-Fallback

When one provider hits rate limits (429), the script **automatically switches to the alternate provider** if credentials are available. This ensures image generation completes even during high usage periods.

**How it works:**

1. Primary provider (Gemini by default) attempts to generate all images
2. If rate limited, switches to fallback provider (OpenAI)
3. Manifest tracks which images are already generated, so only missing ones are created
4. Works in both directions (Gemini → OpenAI or OpenAI → Gemini)

**Requirements for auto-fallback:**

- Both `GOOGLE_CLOUD_PROJECT` and `OPENAI_API_KEY` must be set in `.env`
- Use `--no-fallback` to disable this behavior

## Command Reference

| Command            | Description                                       |
| ------------------ | ------------------------------------------------- |
| `--provider NAME`  | Provider: 'gemini' (default) or 'openai'          |
| `--glob PATTERN`   | Glob pattern for prompt files                     |
| `--dry-run`        | Preview without API calls                         |
| `--force`          | Regenerate even if already exists                 |
| `--count N`        | Variants per prompt (default: 1)                  |
| `--parallel N`     | Number of images to generate concurrently (default: 1) |
| `--no-fallback`    | Disable automatic provider fallback on rate limit |
| `--help`           | Show help message                                 |

## Prompt File Format

Prompt files are located in `articles/prompts/` and follow this structure:

```markdown
# Image Prompts: Article Title

_Description of the image set_

---

## Image 1: Hero Image - Title

**Prompt:**
Detailed image generation prompt describing the scene, style, colors, composition...

**Caption:** _Caption text for the image_

---

## Image 2: Technical Diagram

**Prompt:**
Another detailed prompt...

**Caption:** _Caption for this image_

---

## Generation Notes

**Style consistency:** Notes about maintaining visual coherence
**Aspect ratios:** Guidance for different image types
**Quality modifiers:** Keywords to include
```

### Key Format Rules

1. **Image sections**: Start with `## Image N: Title`
2. **Prompt marker**: Use `**Prompt:**` followed by the prompt text
3. **Caption marker**: Use `**Caption:**` followed by the caption (optional)
4. **Generation Notes**: Section at the end with style guidance (appended to all prompts)

## Output Structure

Images are saved to `articles/images/<slug>/`:

```text
articles/images/
├── solving-the-long-horizon-agent-problem/
│   ├── manifest.json          # Metadata and prompt hashes
│   ├── img-01_v1.png          # Hero image
│   ├── img-02_v1.png          # Image 2
│   └── img-03_v1.png          # Image 3
├── beads-and-agent-hive/
│   ├── manifest.json
│   └── ...
```

### Manifest Format

Each output directory contains a `manifest.json` tracking generated images:

```json
{
  "source_md_path": "articles/prompts/01-solving-the-long-horizon-agent-problem.md",
  "generated_at": "2025-01-15T14:30:00.000Z",
  "provider": "gemini",
  "model": "gemini-2.5-flash-preview-05-20",
  "images": [
    {
      "index": 1,
      "title": "Hero Image - The Shift-Change Problem",
      "caption": "The Shift-Change Problem: Every new AI agent session...",
      "aspect": "16:9",
      "prompt": "Create an image of...",
      "prompt_hash": "abc123...",
      "output_files": ["img-01_v1.png"],
      "provider": "gemini"
    }
  ]
}
```

## Aspect Ratios

The script automatically selects aspect ratios based on image index:

| Image Index | Default Aspect | Use Case                 |
| ----------- | -------------- | ------------------------ |
| 1 (Hero)    | 16:9           | Article header           |
| 2, 6, 8     | 4:3            | Technical diagrams       |
| 3, 4, 5, 7  | 16:9           | Conceptual illustrations |
| Other       | 16:9           | Default                  |

## Workflow Examples

### Generate All Missing Images (Gemini)

```bash
.claude/skills/article-images/scripts/generate-images.sh
```

### Generate with OpenAI gpt-image-1.5

```bash
.claude/skills/article-images/scripts/generate-images.sh --provider openai
```

### Generate in Parallel (Faster)

```bash
# Generate 4 images concurrently
.claude/skills/article-images/scripts/generate-images.sh --parallel 4

# Parallel with specific article
.claude/skills/article-images/scripts/generate-images.sh \
  --glob "articles/prompts/01-*.md" \
  --parallel 4
```

### Regenerate Specific Article

```bash
.claude/skills/article-images/scripts/generate-images.sh \
  --glob "articles/prompts/01-*.md" \
  --force
```

### Test with Dry Run

```bash
.claude/skills/article-images/scripts/generate-images.sh --dry-run
```

## Creating New Prompt Files

1. Create a new file in `articles/prompts/`:

   ```bash
   touch articles/prompts/11-new-article.md
   ```

2. Use this template:

   ```markdown
   # Image Prompts: Your Article Title

   _Brief description of the article and image needs_

   ---

   ## Image 1: Hero Image - Main Concept

   **Prompt:**
   Create a detailed, high-quality illustration showing [main concept].
   Style: [artistic style]. Color palette: [colors]. Composition: [layout].
   Include: [key elements]. Mood: [atmosphere].

   **Caption:** _A brief description for accessibility and context._

   ---

   ## Image 2: [Second Image Title]

   **Prompt:**
   [Detailed prompt for second image...]

   **Caption:** _Caption for second image._

   ---

   ## Generation Notes

   **Style consistency:** All images should [style guidance]
   **Aspect ratios:** Hero 16:9, technical diagrams 4:3
   **Quality modifiers:** high-quality, detailed, professional illustration
   ```

3. Generate the images:

   ```bash
   .claude/skills/article-images/scripts/generate-images.sh \
     --glob "articles/prompts/11-*.md"
   ```

## Prompt Writing Tips

### Effective Prompts Include

1. **Subject matter**: What is the main focus?
2. **Style**: Digital illustration, 3D render, watercolor, etc.
3. **Color palette**: Specific colors or mood
4. **Composition**: Wide shot, close-up, isometric, bird's eye
5. **Lighting**: Dramatic, soft, ambient, backlit
6. **Mood**: Professional, playful, serious, futuristic
7. **Quality modifiers**: High-quality, detailed, clean lines

### Example Prompt Structure

```text
Create a [style] image of [subject] in [setting].
[Key visual elements and details].
[Composition and framing].
[Color palette and lighting].
[Mood and atmosphere].
High-quality, detailed, professional.
```

## Troubleshooting

### "GOOGLE_CLOUD_PROJECT not set"

For Gemini provider, add to `.env`:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### "invalid_grant" or "reauth related error"

Your Google Cloud credentials need to be refreshed:

```bash
gcloud auth application-default login
```

### "OPENAI_API_KEY not set"

For OpenAI provider, add to `.env`:

```bash
OPENAI_API_KEY=sk-...
```

### "No prompt files found"

Check the glob pattern matches your files:

```bash
ls articles/prompts/*.md
```

### Images Not Regenerating

The script skips prompts that haven't changed. Use `--force`:

```bash
.claude/skills/article-images/scripts/generate-images.sh --force
```

### Rate Limiting

Both providers include automatic retry with exponential backoff. The script also **automatically falls back to the alternate provider** when rate limits are exhausted.

If both providers hit rate limits:

- Wait a few minutes before retrying
- Use smaller batches with `--glob` for specific files
- The script will resume from where it left off (manifests track progress)
- Ensure both `GOOGLE_CLOUD_PROJECT` and `OPENAI_API_KEY` are set for full fallback support

## Additional Resources

### Script Files

- **`scripts/generate-images.sh`** - Wrapper script with provider selection and parallel support
- **`scripts/generate-images-gemini.mjs`** - Google Gemini image generation with parallel support
- **`scripts/generate-images-from-prompts.mjs`** - OpenAI gpt-image-1.5 generation with parallel support
- **`scripts/package.json`** - Node.js dependencies

## Integration with Articles

After generating images, reference them in your article:

```markdown
![Hero image](articles/images/your-article/img-01_v1.png)
_Caption from the manifest_

## Section Title

![Technical diagram](articles/images/your-article/img-02_v1.png)
_Caption for the diagram_
```

Or use the manifest to programmatically build image references.
