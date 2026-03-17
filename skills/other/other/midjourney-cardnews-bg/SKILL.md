---
name: midjourney-card-news-backgrounds
description: Generate Midjourney prompts for 600x600 card news background images based on topic, mood, and style preferences. Use when user requests card news backgrounds or Instagram post backgrounds.
---

# Midjourney Card News Background Generator

Generate optimized Midjourney prompts for 600x600px card news backgrounds that work well with text overlays.

## When to Use This Skill

Use this skill when the user requests:
- Card news background images
- Instagram post backgrounds
- Social media graphic backgrounds
- 600x600 or 1:1 aspect ratio backgrounds

## Core Workflow

1. **Identify the topic**: Extract the main subject from user's request
2. **Determine style category**: Match to predefined style patterns
3. **Generate prompt**: Create Midjourney prompt with optimal parameters
4. **Provide variations**: Offer 3-5 different style options

## Prompt Structure

All prompts follow this structure:
```
[subject/scene description], [style keywords], [color palette], [texture/atmosphere], [technical specs] --ar 1:1 --v 6
```

### Essential Components

**Subject description** (5-10 words):
- Describe the visual elements clearly
- Use specific, vivid adjectives
- Avoid abstract concepts

**Style keywords** (3-5 keywords):
- minimal, clean, modern, professional
- gradient, abstract, geometric
- organic, fluid, soft, dreamy

**Color palette** (specific colors):
- Name exact colors: "soft blue and purple" not "cool colors"
- Include intensity: "vibrant", "pastel", "muted", "bright"
- Maximum 3-4 colors for cohesion

**Texture/atmosphere** (2-3 keywords):
- smooth, flowing, textured, grainy
- light and airy, bold and dramatic
- subtle, prominent, delicate

**Technical specifications**:
- Always include: `--ar 1:1` (for 600x600 square format)
- Version: `--v 6` (current Midjourney version)
- Optional: `--s 50-200` for stylization control

## Style Categories

For quick reference, match topics to these categories:

### Business/Tech
- Clean gradients with geometric elements
- Blue, purple, teal color schemes
- Professional and modern feel

### Health/Wellness  
- Soft pastels with organic shapes
- Green, peach, soft pink tones
- Calming and natural atmosphere

### Finance/Investment
- Bold gradients with sharp lines
- Navy, gold, green color schemes
- Confident and premium feel

### Education/Learning
- Friendly colors with simple shapes
- Yellow, orange, light blue tones
- Approachable and energetic mood

### Food/Lifestyle
- Warm tones with natural textures
- Earth tones, warm oranges, browns
- Inviting and authentic feel

### Creative/Art
- Bold abstract patterns
- Vibrant multi-color schemes
- Expressive and dynamic energy

## Text Overlay Optimization

All backgrounds must be text-friendly:

**Contrast zones**: Include areas with:
- Subtle gradients (not busy patterns)
- Consistent brightness in center
- Darker or lighter edges for visual interest

**Space planning**:
- Keep center 60% relatively uniform
- Place complex elements in corners
- Avoid horizontal lines through center

**Avoid**:
- High-contrast busy patterns
- Text-competing elements in center
- Overly detailed textures

## Example Prompts by Topic

**Tech/AI**:
```
abstract neural network patterns, modern tech aesthetic, gradient blue and cyan tones, smooth digital waves, clean negative space for text, futuristic minimalism --ar 1:1 --v 6
```

**Fitness/Exercise**:
```
soft flowing energy waves, dynamic movement feel, gradient coral and peach colors, light and motivating atmosphere, space for text overlay --ar 1:1 --v 6
```

**Finance/Money**:
```
elegant geometric patterns, premium professional style, navy and gold gradient, subtle texture with depth, sophisticated minimal design --ar 1:1 --v 6
```

**Food/Cooking**:
```
organic food texture background, warm earthy tones, rustic natural aesthetic, soft focus with gentle shadows, appetizing color palette --ar 1:1 --v 6
```

**Mental Health**:
```
calming abstract clouds, serene peaceful atmosphere, soft lavender and mint gradients, dreamy gentle textures, meditative minimal space --ar 1:1 --v 6
```

## Response Format

When user provides a topic, respond with:

1. **Primary prompt**: The most suitable style
2. **Alternative 1**: Different mood/style for same topic
3. **Alternative 2**: Another variation
4. **Brief explanation**: Why these styles work for the topic

Example response:
```
주제: 재테크 팁

1. 메인 추천:
[prompt here]
→ 전문적이고 신뢰감 있는 금융 분위기

2. 대안 1:
[prompt here]  
→ 친근하고 접근하기 쉬운 느낌

3. 대안 2:
[prompt here]
→ 프리미엄하고 고급스러운 느낌
```

## Tips for Better Results

**Do**:
- Use specific color names
- Include texture descriptors
- Specify mood/atmosphere
- Keep prompts under 60 words
- Test with simple subjects first

**Avoid**:
- Generic terms like "nice" or "good"
- Too many competing elements
- Complex scene descriptions
- Overly long prompts
- Requesting specific brands/logos

## Advanced Parameters

For fine-tuning (optional):

- `--s 50`: More realistic, less stylized
- `--s 150`: Balanced stylization (default)
- `--s 250`: More artistic interpretation
- `--chaos 0-100`: Variation control (0 = consistent)

## Korean Language Support

When user asks in Korean:
- Understand Korean topic descriptions
- Translate concepts to English prompts
- Provide explanations in Korean
- Keep prompts in English (Midjourney requirement)

## Common Topics Reference

Read `topics_reference.md` for comprehensive list of:
- Industry-specific color schemes
- Seasonal variations
- Trend-based styles
- Cultural considerations
