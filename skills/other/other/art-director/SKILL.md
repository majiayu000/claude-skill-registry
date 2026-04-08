---
name: art-director
description: "AI art direction system. Claude directs image generation models (Gemini, DALL-E, Flux) via structured prompts. Generate banners, diagrams, logos, screenshots, and social media visuals without leaving the terminal."
---

# Art Director

Claude can't generate images directly, but it can **direct** image generation models with expert-level prompts. This skill turns Claude into a creative director.

## Supported Backends

| Backend | Via | Best For |
|---------|-----|----------|
| Gemini 3.1 Flash Image | AI Gateway | General purpose, fast, cheap |
| DALL-E 3 | OpenAI API | Photorealistic, detailed |
| Flux 2 | Replicate/fal.ai | Artistic, stylized |
| Stable Diffusion | Local/API | Full control, custom models |

## The 5-Component Prompt Formula

Every image prompt follows this structure:

```
[SUBJECT] + [STYLE] + [COMPOSITION] + [LIGHTING] + [TECHNICAL]
```

### 1. Subject (What)
```
"A minimalist developer dashboard showing code metrics"
"An isometric illustration of microservices architecture"
"A cyberpunk cityscape representing a deployment pipeline"
```

### 2. Style (How it looks)
```
Styles: flat design, isometric, pixel art, watercolor,
        technical diagram, infographic, comic book,
        photorealistic, low-poly 3D, line art, blueprint
```

### 3. Composition (Layout)
```
"centered hero composition with negative space"
"rule of thirds with focal point bottom-left"
"symmetric grid layout with 4 quadrants"
"panoramic wide-angle view"
```

### 4. Lighting (Mood)
```
"soft diffused lighting, professional studio"
"dramatic rim lighting, dark background"
"warm golden hour, natural outdoor"
"neon glow, cyberpunk atmosphere"
"flat even lighting, clean minimal"
```

### 5. Technical (Specs)
```
"16:9 aspect ratio, 1920x1080, PNG"
"1:1 square, 1024x1024, social media optimized"
"4:3 presentation slide format"
"banner format 1200x630 for Open Graph"
```

## Use Cases

### 1. GitHub Repository Banners
```
Subject: "vibecosystem logo - interconnected nodes forming a brain,
          each node is a different color representing an agent type"
Style: "flat design, minimal, dark background (#0d1117)"
Composition: "centered, wide banner format"
Lighting: "subtle gradient glow on nodes"
Technical: "1280x640 PNG, GitHub social preview"
```

### 2. Architecture Diagrams
```
Subject: "microservices architecture with 5 services connected by message queue"
Style: "clean technical diagram, rounded rectangles, thin connecting lines"
Composition: "left-to-right flow, clear hierarchy"
Lighting: "flat, no shadows, white background"
Technical: "SVG-compatible, high contrast"
```

### 3. Social Media Posts
```
Subject: "before/after comparison of code quality metrics"
Style: "modern infographic, data visualization"
Composition: "split screen, left=before (red), right=after (green)"
Lighting: "clean, professional"
Technical: "1080x1080 Instagram square"
```

### 4. Presentation Slides
```
Subject: "key takeaway slide showing 3 pillars of the system"
Style: "corporate minimal, sans-serif typography"
Composition: "three equal columns with icons"
Lighting: "flat, light background"
Technical: "16:9, 1920x1080"
```

### 5. Error/Status Illustrations
```
Subject: "friendly 404 illustration - a confused robot looking at a map"
Style: "line art with single accent color (#3b82f6)"
Composition: "centered character with text space below"
Lighting: "flat"
Technical: "800x600 SVG"
```

## Prompt Database (Templates)

### Developer Themes
- `dev-dark`: Dark mode, neon accents, terminal aesthetic
- `dev-clean`: Light, minimal, Apple-inspired
- `dev-retro`: Pixel art, 8-bit, nostalgic
- `dev-cyber`: Cyberpunk, holographic, futuristic
- `dev-nature`: Organic, earthy, calm

### Color Palettes
- `github`: #0d1117, #238636, #f78166, #3fb950
- `vercel`: #000000, #ffffff, #666666
- `claude`: #d4a574, #1a1a2e, #f5f5dc
- `vibecosystem`: #6366f1, #0f172a, #22d3ee, #f43f5e

## Workflow

1. User describes what they need ("I need a banner for the repo")
2. Claude constructs a 5-component prompt
3. Prompt is sent to the chosen backend via MCP or API
4. Image is saved to project assets/
5. Path is returned for immediate use

## Integration

- **designer agent**: Uses art-director skill for visual decisions
- **frontend-dev**: Generates placeholder images during prototyping
- **copywriter**: Creates social media visuals with copy
- **doc-updater**: Generates diagrams for documentation
- **harvest**: Creates competitive analysis visuals

## Tips

- Always specify aspect ratio and dimensions
- Include "no text" if you don't want the model to attempt typography
- Use negative prompts: "no watermark, no stock photo look"
- For diagrams, prefer SVG-compatible styles over photorealistic
- Test with cheapest model first, upgrade only if quality insufficient
