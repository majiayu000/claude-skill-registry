---
name: "ACOS Visual Generator"
description: "Generate research-grounded visuals using the InfoGenius pipeline. Use when creating infographics, diagrams, educational visuals, or any image that benefits from factual accuracy. Supports 8 visual styles (3D, technical, minimalist, photorealistic, futuristic, vintage, cartoon, standard) and 4 audience levels."
---

# ACOS Visual Generator

## What This Skill Does

Creates research-grounded images by:
1. Researching the topic via web search
2. Extracting key facts for accuracy
3. Constructing a detailed image prompt
4. Generating via Nano Banana MCP (Gemini 2.5 Flash Image)

## Prerequisites

- Nano Banana MCP server configured
- WebSearch tool available

## Quick Start

```
User: "Create a 3D infographic about quantum computing"

Process:
1. WebSearch → Extract key facts
2. Construct prompt with style instructions
3. mcp__nanobanana__generate_image()
4. Return image with sources
```

---

## Visual Styles

| Style | Description |
|-------|-------------|
| `standard` | Clean scientific illustration, modern, professional |
| `minimalist` | Bauhaus, flat vector, 2-3 colors, negative space |
| `photorealistic` | Cinematic lighting, 8K, detailed textures |
| `3d` | Isometric render, claymorphism, studio lighting |
| `technical` | Da Vinci notebook, ink sketch, annotations |
| `futuristic` | Cyberpunk HUD, neon, holographic |
| `vintage` | 19th century lithograph, sepia, engraving |
| `cartoon` | Educational comic, vibrant, cel-shaded |

## Audience Levels

| Level | Target |
|-------|--------|
| `elementary` | Ages 6-10, bright, simple, fun icons |
| `highschool` | Standard textbook, clean, accurate |
| `college` | Academic journal, high detail, data-rich |
| `expert` | Technical schematic, extremely dense |

---

## Step-by-Step Process

### Step 1: Research
```javascript
WebSearch("{topic} facts key information 2026")
```

Extract 3-5 verifiable facts.

### Step 2: Construct Prompt
```
Create a {aspect_ratio} {style_description} infographic about {topic}.

VISUAL STYLE: {style_instruction}
AUDIENCE: {audience_instruction}

INCLUDE:
- {fact_1_visualized}
- {fact_2_visualized}
- {fact_3_visualized}

COMPOSITION:
- Clear layout with visual hierarchy
- Text should be large and legible
- Include labels and annotations
```

### Step 3: Generate
```javascript
mcp__nanobanana__generate_image({
  prompt: "{constructed_prompt}",
  aspect_ratio: "16:9",
  model_tier: "pro",
  enable_grounding: true,
  thinking_level: "high",
  resolution: "high"
})
```

### Step 4: Present Results
Return:
- Generated image
- Research sources
- Key facts included
- Modification options

---

## Style Instructions (Copy These)

**Standard:**
```
High-quality digital scientific illustration. Clean, modern, highly detailed. Professional color palette.
```

**3D Isometric:**
```
3D Isometric Render. Claymorphism or high-gloss plastic texture, studio lighting, soft shadows, looks like a physical model.
```

**Technical:**
```
Da Vinci Notebook style. Ink on parchment sketch, handwritten annotation style, rough but accurate lines, technical precision.
```

**Futuristic:**
```
Cyberpunk HUD. Glowing neon blue/cyan lines on dark background, holographic data visualization, 3D wireframes.
```

---

## Example Usage

**User:** "Visualize how neural networks learn"

**Research:** WebSearch finds key facts about backpropagation, gradient descent, layers, activation functions.

**Prompt:**
```
Create a 16:9 3D isometric infographic about how neural networks learn.

VISUAL STYLE: 3D Isometric Render with claymorphism aesthetic...

INCLUDE:
- Input layer receiving data
- Hidden layers processing with weights
- Backpropagation arrows showing error correction
- Output layer with predictions
```

**Generate:** Call Nano Banana MCP with grounding enabled.

---

## Integration

This skill integrates with:
- `/infogenius` command in ACOS
- Nano Banana MCP for image generation
- WebSearch for factual grounding

---

*Part of the Agentic Creator OS visual generation pipeline.*
