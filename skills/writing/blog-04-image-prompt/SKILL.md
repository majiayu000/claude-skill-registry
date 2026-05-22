---
name: blog-04-image-prompt
description: Generate optimized AI image prompts for blog post hero images
---

Generate a compelling, detailed prompt for AI image generation that captures the essence of the blog post while maintaining consistent brand aesthetics.

## Input

**Blog post**: $ARGUMENTS (path to markdown file or topic description)

## Workflow

1. **Analyze Content**: Read the blog post or understand the topic to identify:
   - Core concept/theme
   - Key technical elements or metaphors
   - Emotional tone
   - Target audience context

2. **Craft Prompt**: Create a 3-4 sentence prompt that:
   - Opens with the primary subject/scene
   - Includes specific visual details and composition
   - Specifies lighting, mood, and atmosphere
   - Incorporates brand style elements
   - Avoids text/typography (AI struggles with text rendering)

## Brand Guidelines

**Visual Style**:

- Cinematic realism with dramatic lighting
- Warm/cool color contrast for depth
- Professional photography quality (8k, photorealistic)
- Optional: Fantasy, sci-fi, or comic book elements when appropriate

**Mood**: Contemplative, thought-provoking, professional yet approachable

**Composition**:

- 16:9 aspect ratio (landscape)
- Rule of thirds or centered dramatic composition
- Depth of field for focus
- Negative space for text overlay if needed

## Prompt Template Structure

```
[Main subject/scene], [specific details], [environment/setting]. [Lighting description], [mood/atmosphere], [technical quality specs]. [Style modifiers], [color palette], [composition notes].
```

## Output Format

Save to `._tmp/images/{YYYY}-{MM}-{DD}-{HH}{MM}-{blog-title}.md`:

```markdown
# Image Prompt: {Blog Post Title}

**Blog Post**: {path or title}
**Date**: {YYYY-MM-DD HH:MM}

## Generated Prompt

{Your 3-4 sentence prompt here}

## Metadata

- **Recommended filename**: `{YYYY}{MM}{DD}-{HH}{MM}-{blog-title}.png`
- **Aspect ratio**: 16:9 (landscape)
- **Suggested generators**:
  - include the probmpt as a URL-encoded parameter for easy copy-paste
  - [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=models%2Fgemini-3-pro-image-preview&prompt={PROMPT_ENCODED_FOR_URL}) - use 16:9 aspect ratio

## Post-Generation Notes

{Add any notes about variations to try, color adjustments, or alternative concepts}
```

## Examples

**For a post about performance optimization**:

> A sleek, futuristic engine room with glowing holographic performance graphs floating in mid-air, a software engineer studying the data with focused intensity. Dramatic side lighting creates contrast between cool blue holographic displays and warm ambient light, shallow depth of field. Cinematic realism, professional photography, 8k quality, high contrast color grading with teal and orange tones.

**For a post about architecture decisions**:

> An architect's desk from above showing scattered blueprints transforming into floating 3D holographic building structures, hands gesturing between physical and digital elements. Golden hour lighting through windows, contemplative atmosphere, photorealistic with subtle sci-fi elements. 16:9 composition, rule of thirds, high detail, cinematic color grading.

## Tips

- Use specific nouns over generic terms (e.g., "MacBook Pro" vs "laptop")
- Include camera perspective (overhead, side angle, close-up, etc.)
- Specify material qualities (metallic, glass, matte, glossy)
- Add environmental context for depth
- Use photography terminology (bokeh, depth of field, golden hour, etc.)
