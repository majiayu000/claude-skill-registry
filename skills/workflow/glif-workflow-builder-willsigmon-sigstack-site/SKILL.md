---
name: glif-workflow-builder
description: Design and build Glif AI workflows. Use when creating new glifs, planning workflow structure, or understanding block types.
allowed-tools: Read, WebFetch
---

# Glif Workflow Builder

Design AI workflows using Glif's block-based system.

## Workflow Structure

Glifs are JSON graphs with nodes (blocks) connected via variable references.

```json
{
  "nodes": [
    {"name": "input1", "type": "TextInputBlock", "params": {...}},
    {"name": "generator", "type": "ImageBlock", "params": {"prompt": "{input1}"}}
  ]
}
```

## Block Types

### Input Blocks
- **TextInputBlock** - Text input from user
- **ImageInputBlock** - Image upload
- **MultipickBlock** - Multiple choice selector

### AI Generation Blocks
- **TextBlock** - LLM text generation (GPT, Claude, Llama)
- **ImageBlock** - Image generation (SDXL, Flux, DALL-E)
- **ImageToTextBlock** - Image captioning/analysis
- **VideoBlock** - Video generation

### Utility Blocks
- **CombineTextBlock** - Concatenate text values
- **JSONExtractorBlock** - Parse JSON responses
- **PublishedGlifBlock** - Nest other glifs
- **WebFetchBlock** - HTTP requests

### Output Blocks
- **HTMLBlock** - Custom HTML rendering
- **CanvasBlock** - Image composition
- **AudioBlock** - Audio output

## Variable References

Reference other blocks using `{blockName}`:

```json
{
  "name": "enhancer",
  "type": "TextBlock",
  "params": {
    "prompt": "Enhance this prompt: {userInput}",
    "model": "gpt-4"
  }
}
```

## Design Patterns

### Basic Image Generator
```
TextInput → ImageBlock → Output
```

### Prompt Enhancement
```
TextInput → TextBlock (enhance) → ImageBlock → Output
```

### Multi-Image Composite
```
TextInput → ImageBlock (bg) ─┐
TextInput → ImageBlock (fg) ─┼→ CanvasBlock → Output
```

### Iterative Refinement
```
TextInput → ImageBlock → ImageToTextBlock → TextBlock → ImageBlock → Output
```

## Best Practices

1. **Keep inputs minimal** - 2-3 max for usability
2. **Name blocks descriptively** - `stylePrompt` not `text1`
3. **Use alphanumeric + underscore only** for names
4. **Chain text blocks** for complex prompts
5. **Test incrementally** - add one block at a time

## Schema Reference

Full JSON schema: https://glif.app/api/graphJsonSchema

## Common Models

**Text:** gpt-4, gpt-4o, claude-3, llama-3
**Image:** flux-pro, sdxl, dall-e-3, stable-diffusion-3
**Video:** runway-gen3, kling
