---
name: visual-design
description: "Generate style guides, component mockups, and visual assets using AI (Gemini 3 Pro Image, FLUX.2 Pro). Optional feature - gracefully skips if OPENROUTER_API_KEY unavailable."
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# Visual Design Skill

## Overview

Generate publication-quality visual assets for component development:
- **Style Guides**: Color palettes, typography, spacing systems
- **Component Mockups**: Visual references to guide implementation
- **Architecture Diagrams**: Component dependencies, data flow
- **Design System Documentation**: Visual brand guidelines

**100% Optional** - All features work without this skill if OPENROUTER_API_KEY is unavailable.

## When to Use This Skill

This skill should be used when:
- Creating a new design system or style guide
- Generating visual references for complex components
- Documenting design decisions visually
- Creating component mockups before implementation
- Generating architecture diagrams for documentation

**Skip this skill when:**
- OPENROUTER_API_KEY not available (plugin works normally)
- User prefers manual design (Figma, Sketch, etc.)
- Budget constraints for API usage

## Quick Start

```python
# Generate component mockup
python ${CLAUDE_PLUGIN_ROOT}/skills/visual-design/scripts/generate_mockup.py \
  "Modern React card component with header, content, and actions. Clean design." \
  --output mockups/card.png

# Generate style guide
python ${CLAUDE_PLUGIN_ROOT}/skills/visual-design/scripts/generate_style_guide.py \
  --framework react \
  --design-system custom \
  --output style-guide/
```

## API Key Setup

**Check before using:**
```bash
# Check if OPENROUTER_API_KEY is available
if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "Visual generation disabled (API key not set)"
  echo "To enable: https://openrouter.ai/keys"
  exit 0  # Gracefully skip
fi
```

**User instructions (show once):**
```
ℹ️  Visual Generation Features Disabled

To enable AI-powered visual generation:
1. Get API key: https://openrouter.ai/keys
2. Add to .env: OPENROUTER_API_KEY=your_key_here

You can still use all other features (Storybook setup, story generation, testing).
```

## Use Cases

### 1. Style Guide Generation

**Context-Aware Workflow:**

```javascript
// Phase 1: Analyze project
const framework = detectFramework();
const designSystem = detectDesignSystem();
const colors = extractColorsFromCSS();

// Phase 2: User collaboration
AskUserQuestion({
  questions: [
    {
      question: `What aesthetic matches your ${designSystem} design system?`,
      header: "Style",
      multiSelect: false,
      options: [
        {
          label: "Modern/Minimal (Recommended for your stack)",
          description: "Clean lines, lots of whitespace, professional"
        },
        {
          label: "Bold/Vibrant",
          description: "Strong colors, high contrast, energetic"
        },
        {
          label: "Professional/Corporate",
          description: "Conservative, trustworthy, business-focused"
        }
      ]
    },
    {
      question: "Primary brand color?",
      header: "Color",
      multiSelect: false,
      options: [
        { label: "Blue (#2563eb)", description: "Trust, professionalism (detected in your CSS)" },
        { label: "Green (#10b981)", description: "Growth, sustainability" },
        { label: "Purple (#8b5cf6)", description: "Creativity, innovation" },
        { label: "Custom", description: "I'll specify" }
      ]
    }
  ]
})

// Phase 3: Generate visual assets
python generate_style_guide.py \
  --framework ${framework} \
  --aesthetic "modern-minimal" \
  --primary-color ${selectedColor} \
  --output style-guide/
```

**Output:**
- `style-guide/colors.png` - Color palette with hex codes
- `style-guide/typography.png` - Font scale and examples
- `style-guide/spacing.png` - Spacing scale visualization
- `style-guide/components.png` - Example component variants

### 2. Component Mockup Generation

**When to Generate:**
- Card components
- Modal dialogs
- Complex forms
- Tables with data
- Navigation menus
- Dashboards

**Skip for:**
- Simple buttons
- Basic inputs
- Icons
- Badges

**Generation:**
```python
# Context-aware mockup
python generate_mockup.py \
  "${componentType} component for ${framework}. \
   Design system: ${designSystem}. \
   Variants: ${detectedVariants}. \
   Modern, professional, ${aesthetic} style." \
  --output mockups/${componentName}.png
```

**Example:**
```python
python generate_mockup.py \
  "React data table component with sortable columns, pagination, row selection. \
   Material UI design system. Clean, modern interface." \
  --output mockups/data-table.png
```

### 3. Architecture Diagrams

**Component Dependency Visualization:**
```python
# Analyze component relationships
components = scanComponents('src/components');
dependencies = buildDependencyGraph(components);

# Generate diagram (using Mermaid or AI)
generateDiagram({
  type: 'component-architecture',
  components: components,
  dependencies: dependencies,
  output: 'diagrams/component-deps.png'
});
```

## AI Models

**Supported Models:**
- `google/gemini-3-pro-image-preview` (Default - High quality, recommended)
- `black-forest-labs/flux.2-pro` (Fast, high quality)

**Model Selection:**
```python
# Use default (Gemini)
python generate_mockup.py "prompt" --output out.png

# Use FLUX.2 Pro
python generate_mockup.py "prompt" --model black-forest-labs/flux.2-pro --output out.png
```

## Graceful Degradation

**When OPENROUTER_API_KEY is unavailable:**

1. **Skip visual generation silently**
2. **Provide alternatives**:
   - Text-based style guide templates
   - Link to Figma/Sketch
   - Mermaid diagrams for architecture
3. **Continue with other features**:
   - Storybook setup works
   - Story generation works
   - Testing works

**Implementation:**
```javascript
async function generateStyleGuide(options) {
  if (!process.env.OPENROUTER_API_KEY) {
    console.log('ℹ️  Skipping visual generation (API key not set)');
    console.log('   Creating text-based style guide template instead...');

    // Generate markdown template
    createTextStyleGuideTemplate(options);
    return;
  }

  // Generate visual assets with AI
  await generateVisualStyleGuide(options);
}
```

## Prompt Engineering for Components

**Good Prompts:**
```
✅ "Modern React card component with image header, title, description, and action buttons.
    Material UI design system. Subtle shadow, rounded corners. Light theme."

✅ "Vue 3 data table with sortable columns, pagination controls, and row selection checkboxes.
    Professional corporate style. Clean typography."

✅ "Svelte modal dialog with header, scrollable content area, and footer actions.
    Overlay background. shadcn/ui aesthetic."
```

**Bad Prompts:**
```
❌ "Button" (too vague)
❌ "Make a component" (no details)
❌ "Card thing" (unclear)
```

**Context Enhancement:**
Automatically add context from project:
```python
def enhance_prompt(user_prompt, context):
    return f"{user_prompt}. Framework: {context.framework}. \
             Design system: {context.designSystem}. \
             Color palette: {context.colors}. \
             Typography: {context.fonts}."
```

## Quality Thresholds

Following claude-project-planner patterns:

| Document Type | Threshold | Usage |
|---------------|-----------|-------|
| Style Guide | 8.5/10 | Design system documentation |
| Component Mockup | 8.0/10 | Complex component references |
| Architecture Diagram | 8.0/10 | Technical documentation |
| Quick Sketch | 7.0/10 | Rapid prototyping |

**Smart Iteration:**
```python
def generate_with_quality_check(prompt, threshold=8.0):
    image = generate_image(prompt)
    quality = review_quality_with_gemini(image)  # Gemini 3 Pro review

    if quality < threshold:
        print(f"Quality: {quality}/10 (below {threshold})")
        print("Regenerating...")
        return generate_with_quality_check(prompt, threshold)

    print(f"Quality: {quality}/10 ✓")
    return image
```

## Integration with Other Skills

- **storybook-config**: Generate visual assets during setup
- **component-scaffold**: Generate mockups for new components
- **style-guide-generator**: Visual enhancement for documentation
- **story-generation**: Optional mockups for complex components

## Best Practices

### Do's
- Check for OPENROUTER_API_KEY before generation
- Provide context-aware prompts (framework, design system)
- Use quality thresholds for important assets
- Skip gracefully when API unavailable
- Generate only for complex components (not buttons/inputs)
- Use Mermaid for architecture diagrams when possible (faster, editable)

### Don'ts
- Don't fail if API key missing
- Don't generate for every component (cost)
- Don't use generic prompts
- Don't skip quality review for critical assets
- Don't assume user wants visual generation

## Error Handling

- **API key missing**: Skip gracefully, inform user once
- **API timeout**: Retry once, then fail gracefully
- **Quality too low**: Regenerate up to 2 times
- **Rate limit**: Wait and retry or skip
- **Invalid response**: Log error, skip generation

## Cost Considerations

**Typical Costs (OpenRouter):**
- Gemini 3 Pro Image: ~$0.05-0.15 per image
- FLUX.2 Pro: ~$0.04-0.08 per image

**Recommendations:**
- Generate selectively (complex components only)
- Cache generated images
- Offer user control over what to generate
- Provide cost estimates before bulk generation

## Example Integration

```javascript
// In /create-component command
if (shouldGenerateVisuals && hasOpenRouterKey()) {
  AskUserQuestion({
    questions: [{
      question: "Generate visual mockup for this component?",
      header: "Visual Design",
      options: [
        { label: "Yes - Generate mockup (~$0.10)", description: "AI visual reference" },
        { label: "No - Skip", description: "Save cost, design manually" }
      ]
    }]
  });

  if (userWantsVisual) {
    generateMockup(componentDescription);
  }
} else {
  // Skip silently, continue with component scaffolding
}
```
