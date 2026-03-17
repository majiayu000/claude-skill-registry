---
name: identify-architecture
description: "Analyze ML model architecture from papers and code. Use when understanding model structure for implementation."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Identify Architecture

Analyze and document machine learning model architectures including layers, connections, and information flow.

## When to Use

- Understanding paper model designs
- Planning model implementation
- Comparing architecture variations
- Documenting neural network structure

## Quick Reference

```bash
# Extract architecture from paper
# Look for: "Figure X: Architecture of [Model]"
# Check for: Table with layer specifications
# Find: Layer descriptions (Conv2D, FC, BatchNorm, etc.)

# Visualize model structure (Mojo)
# var model: SimpleNet = ...
# print(model)  # Should show layer information
```

## Workflow

1. **Locate architecture diagram**: Find visual architecture representation in paper
2. **List layers**: Enumerate all layers with type and parameters
3. **Document connections**: Map data flow between layers (skip connections, merges)
4. **Extract layer parameters**: For each layer record size, activation, normalization
5. **Create implementation plan**: Translate to Mojo struct/function definitions

## Output Format

Architecture documentation:

- Model name and source
- Layer-by-layer breakdown
- Layer type (Conv2D, Dense, etc.)
- Parameters (kernel size, stride, padding, activation)
- Input/output shapes
- Data flow diagram (text or ASCII)
- Special components (skip connections, attention)

## References

- See `extract-hyperparameters` skill for model configuration
- See CLAUDE.md > Mojo Syntax Standards for implementation patterns
- See `/notes/review/mojo-ml-patterns.md` for architecture patterns
