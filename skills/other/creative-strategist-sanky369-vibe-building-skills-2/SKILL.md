---
name: creative-strategist
description: Research visual direction and develop your creative style. Use when establishing brand aesthetics, finding your visual identity, or planning creative direction for your assets. Integrates with Image Generation and other creative skills for automated asset creation.
---

# Creative Strategist Skill

## Overview

Creative Strategist helps you define your visual direction before generating assets. This skill ensures all your creative outputs maintain consistent style and aesthetic.

**Keywords**: visual direction, creative strategy, brand aesthetics, style guide, visual identity, creative planning, mood boards

## Core Methodology

Your creative strategy has three layers:

1. **Visual Research** — Find inspiration and reference styles
2. **Style Definition** — Define your unique visual direction
3. **Consistency Framework** — Ensure all assets match

## Visual Research Process

### Step 1: Identify Your Aesthetic

Answer these questions:

- **Primary Style**: Photorealistic, minimalist, maximalist, illustrative, abstract?
- **Color Palette**: What colors define your brand?
- **Mood**: Professional, playful, serious, energetic, calm?
- **Target Audience**: What aesthetics appeal to them?
- **Industry Standards**: What do competitors use?

### Step 2: Gather References

Create a mood board with:
- 5-10 reference images from your industry
- 5-10 reference images from outside your industry (inspiration)
- Color palettes that resonate
- Typography and design elements
- Photography styles and compositions

### Step 3: Identify Common Patterns

What do your references have in common?
- Lighting style (natural, studio, dramatic, soft)
- Color temperature (warm, cool, neutral)
- Composition (centered, rule of thirds, dynamic)
- Texture and detail level
- Emotional tone

## Style Definition Framework

### Define Your Visual Direction

**Brand Aesthetic Profile:**

```
Primary Style: [photorealistic/minimalist/illustrative/abstract/maximalist]
Color Palette: [list 3-5 primary colors]
Mood: [professional/playful/serious/energetic/calm/luxurious/casual]
Lighting: [natural/studio/dramatic/soft/mixed]
Composition: [centered/rule of thirds/dynamic/symmetrical/asymmetrical]
Detail Level: [minimal/moderate/detailed/hyper-detailed]
Texture: [smooth/textured/mixed]
Target Audience: [description]
Unique Elements: [what makes yours different]
```

### Create Your Style Guide

Document:
1. **Visual Examples** — 3-5 reference images
2. **Color Codes** — Hex codes for your palette
3. **Typography** — Font choices and usage
4. **Photography Style** — Lighting, composition, mood
5. **Illustration Style** — If applicable
6. **Prohibited Elements** — What NOT to do
7. **Consistency Rules** — How to maintain style

## Consistency Framework

### The 3-Part Consistency Check

Before generating assets, verify:

1. **Style Match** — Does it match my aesthetic?
2. **Quality Level** — Is it the right quality?
3. **Brand Alignment** — Does it represent my brand?

### Style Variations

You can have multiple styles for different contexts:

- **Primary Style** — Main brand aesthetic
- **Secondary Style** — Alternative for variety
- **Accent Style** — Special occasions or campaigns

## Claude Code Integration

### How to Use with Claude Code

When you ask Claude to generate assets, it will use this skill to:

1. **Read your style guide** from the Creative Strategist
2. **Craft detailed prompts** based on your aesthetic
3. **Call the automation system** to generate images
4. **Save organized assets** to your project

### Setup Instructions for Claude Code

**Step 1: Ensure automation system is installed**

```bash
# The automation system should be in your project:
# vibe-creative-automation/
#   ├── fal_api.py
#   ├── creative_cli.py
#   ├── claude_integration.py
#   └── requirements.txt
```

**Step 2: Set environment variable**

```bash
export FAL_API_KEY="your_fal_api_key_here"
```

**Step 3: Install dependencies**

```bash
pip install requests
```

### Claude Code Example: Generate Assets Using Your Style

```python
# Claude Code will use this pattern to generate assets

from claude_integration import generate_product, generate_social, generate_brand

# Your Creative Strategist style guide (define this once)
YOUR_STYLE = {
    "primary_style": "photorealistic",
    "color_palette": ["#FF6B35", "#004E89", "#F7F7F7"],
    "mood": "professional and energetic",
    "lighting": "studio lighting with rim light",
    "composition": "centered with dynamic elements",
    "detail_level": "highly detailed",
    "target_audience": "tech professionals aged 25-45"
}

# Generate product photo using your style
result = generate_product(
    product_name="Your Product",
    description="Your product description here",
    style=f"{YOUR_STYLE['primary_style']}, {YOUR_STYLE['mood']}, {YOUR_STYLE['lighting']}",
    num_variations=3
)

print(f"Generated: {result['images']}")
```

### How Claude Code Uses This Skill

When you ask: **"Generate 3 product photos for my luxury watch"**

Claude will:

1. **Read Creative Strategist** to get your style guide
2. **Extract your aesthetic** (photorealistic, luxury, professional, etc.)
3. **Craft detailed prompt** like:
   ```
   "A luxury leather watch with gold accents, photorealistic, 
   professional and elegant, studio lighting with rim light, 
   centered composition, highly detailed, 4K, sharp focus"
   ```
4. **Call automation system** to generate images
5. **Save to organized folder** like `assets/product-photography/luxury-watch/`
6. **Show you results** with file paths

### Integration with Other Skills

**Creative Strategist → Image Generation:**
- Provides style parameters for prompting

**Creative Strategist → Product Photography:**
- Defines photography aesthetic and lighting

**Creative Strategist → Social Graphics:**
- Sets color palette and mood for social content

**Creative Strategist → Brand Asset:**
- Establishes brand visual identity

**Creative Strategist → All Other Skills:**
- Foundation for consistent creative output

## Practical Examples

### Example 1: E-Commerce Brand

**Your Style Guide:**
```
Primary Style: Photorealistic
Color Palette: Gold, White, Navy Blue
Mood: Luxury and Professional
Lighting: Studio lighting with soft shadows
Composition: Centered with negative space
Detail Level: Highly detailed
Texture: Smooth and refined
```

**When Claude generates assets:**
```python
# Claude Code will automatically craft prompts like:
"Luxury product on white background, gold and navy accents, 
studio lighting, centered composition, highly detailed, 4K, 
professional product photography"
```

### Example 2: Tech Startup

**Your Style Guide:**
```
Primary Style: Minimalist with Modern Illustration
Color Palette: Blue, Purple, White
Mood: Innovative and Energetic
Lighting: Bright and clean
Composition: Dynamic and asymmetrical
Detail Level: Moderate
Texture: Clean with subtle gradients
```

**When Claude generates assets:**
```python
# Claude Code will automatically craft prompts like:
"Modern tech illustration, minimalist style, blue and purple 
colors, dynamic composition, clean aesthetic, energetic mood, 
professional quality"
```

### Example 3: Personal Brand

**Your Style Guide:**
```
Primary Style: Photorealistic with Warm Tones
Color Palette: Warm Gold, Cream, Charcoal
Mood: Approachable and Professional
Lighting: Natural and soft
Composition: Rule of thirds
Detail Level: Detailed but not busy
Texture: Warm and inviting
```

**When Claude generates assets:**
```python
# Claude Code will automatically craft prompts like:
"Professional portrait with warm lighting, rule of thirds 
composition, approachable mood, natural aesthetic, warm 
gold and cream tones, 4K quality"
```

## How to Set Up Your Style Guide

### Step 1: Define Your Aesthetic

Answer these questions and save the answers:

```
What is your primary visual style?
What are your 3-5 brand colors?
What mood do you want to convey?
What lighting style appeals to you?
What composition style do you prefer?
How detailed should assets be?
What textures appeal to you?
Who is your target audience?
What makes your style unique?
```

### Step 2: Gather References

Find 10-15 reference images that match your aesthetic and save them.

### Step 3: Create Your Style Document

Create a document with:
- Your answers to the questions above
- Links to or descriptions of your reference images
- Your color palette with hex codes
- Any specific style rules or prohibitions

### Step 4: Share with Claude

When working with Claude, share your style guide. Claude will:
- Remember your aesthetic
- Use it for all asset generation
- Maintain consistency across all outputs
- Adapt it for different asset types

## Integration Checklist

Before generating assets with Claude Code:

- [ ] Creative Strategist skill is enabled
- [ ] Your style guide is documented
- [ ] FAL_API_KEY environment variable is set
- [ ] Automation system files are in your project
- [ ] Dependencies are installed (`pip install requests`)
- [ ] You've tested the API connection (`python creative_cli.py test`)

## Tips for Success

1. **Be Specific** — The more detailed your style guide, the better the results
2. **Use References** — Share actual images that match your aesthetic
3. **Document Colors** — Use hex codes for exact color matching
4. **Test Variations** — Generate multiple variations to find the best style
5. **Iterate** — Refine your style guide based on results
6. **Stay Consistent** — Use the same style guide for all assets
7. **Update Regularly** — Evolve your style as your brand grows

## Common Mistakes to Avoid

❌ **Vague descriptions** — Be specific about your aesthetic  
❌ **Inconsistent references** — Use consistent reference images  
❌ **Ignoring color codes** — Use exact hex codes  
❌ **Mixing too many styles** — Keep primary style focused  
❌ **Not testing** — Always test your style with sample assets  
❌ **Forgetting mood** — Mood is crucial for consistency  
❌ **Ignoring target audience** — Style should appeal to your audience

## Next Steps

1. **Define Your Aesthetic** — Answer the questions above
2. **Gather References** — Find 10-15 matching images
3. **Create Your Style Guide** — Document everything
4. **Share with Claude** — Give Claude your style guide
5. **Generate Test Assets** — Create a few test assets
6. **Refine** — Adjust based on results
7. **Maintain** — Keep style guide updated

---

**Your Creative Strategist foundation is set. Now use Image Generation and other creative skills to generate consistent, professional assets. 🎨**
