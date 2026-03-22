---
name: layered-first-principles-teaching
description: Transform complex concepts into progressive, first-principles explanations
version: 1.0
author: agent
tags: [teaching, learning, explanation]
---

# Layered First Principles Teaching

Transform complex concepts into progressive, first-principles explanations that build understanding layer by layer.

## Quick Start

```bash
# Explain a concept progressively
kimi layered-first-principles-teaching "Explain blockchain"

# Target specific audience
kimi layered-first-principles-teaching "Explain transformers" --audience beginner

# Output to file
kimi layered-first-principles-teaching "Explain consensus algorithms" --output ./tutorial.md
```

## Output Structure

Generated explanations contain 6 standard sections:

| Section | Content | Purpose |
|---------|---------|---------|
| **Opening** | One-sentence essence + intuitive analogy | Immediate understanding |
| **First Principles** | Problem essence, why existing solutions fail | Foundation building |
| **Progressive Layers** | 3-4 layers from intuition to technical detail | Scaffolding learning |
| **Analogies** | Cross-domain comparisons | Relating to known concepts |
| **Visualizations** | ASCII diagrams, mental models | Spatial understanding |
| **Summary** | Key takeaways + further reading | Retention & next steps |

## Audience Levels

| Level | Characteristics | Approach |
|-------|-----------------|----------|
| **Beginner** | No prior knowledge | Heavy analogies, minimal jargon, focus on "why" |
| **Intermediate** | Some domain knowledge | Balance of intuition and technical detail |
| **Expert** | Deep domain knowledge | Focus on nuances, edge cases, implementation |

## Teaching Patterns

This skill uses progressive disclosure patterns from `prompts/`:

1. **First Principles Analysis** (`first_principles.txt`): Strip away abstractions, find root causes
2. **Layered Decomposition** (`layered_decomposition.txt`): Break into 3-4 cognitive layers
3. **Analogy Generation** (`analogy_generation.txt`): Find relatable comparisons
4. **Visualization Design** (`visualization_design.txt`): Create mental models and diagrams

## Templates

Output templates in `templates/` provide structure for:
- `concept.md`: General concept explanation
- `algorithm.md`: Algorithm walkthrough
- `system.md`: System architecture explanation

## Examples

See `examples/` for completed explanations:
- `blockchain_explained.md`: From "digital ledger" to Byzantine fault tolerance
- `transformers_explained.md`: From "pattern matching" to attention mechanisms

## Workflow

When explaining a concept:

1. **Load first principles prompt** → Identify core problem and breakthrough insight
2. **Load layered decomposition prompt** → Structure into 3-4 cognitive layers
3. **Load analogy generation prompt** → Find 2-3 cross-domain analogies
4. **Load visualization design prompt** → Create ASCII diagrams and mental models
5. **Apply appropriate template** → Generate final explanation

## Constraints

- Maximum 4 layers to avoid cognitive overload
- Each layer must build on previous without introducing new prerequisites
- Analogies must be familiar to target audience
- Visualizations should work in plain text (ASCII)
