---
name: paper-first-principles
description: Convert academic papers into engineer-friendly progressive documentation
version: 1.0
author: agent
tags: [research, learning, engineering]
---

# Paper First Principles

Convert academic papers into progressive, engineer-friendly documentation using first principles thinking.

## Quick Start

```bash
# Basic usage
kimi paper-first-principles https://arxiv.org/abs/xxxx.xxxxx

# Engineer perspective with domain focus
kimi paper-first-principles paper.pdf --audience engineer --domain distributed-systems

# Output to file
kimi paper-first-principles paper.pdf --output ./docs/analysis.md
```

## Output Structure

Generated documents contain 8 standard sections:

| Section | Content | Audience |
|---------|---------|----------|
| **Opening** | One-sentence core insight | All |
| **Mechanism Breakdown** | Comparative analysis tables | Engineers, Researchers |
| **First Principles** | Problem essence and design rationale | All |
| **Progressive Deep Dive** | Layered complexity (simple → complex) | Engineers, Researchers |
| **Edge Cases** | Common pitfalls and misconceptions | Engineers |
| **Decision Tree** | When/how to apply | Engineers, Managers |
| **Engineering Checklist** | Actionable verification items | Engineers |
| **Summary** | Reusable design patterns | All |

## Paper Types & Progressive Paths

| Type | Characteristics | Progressive Path |
|------|-----------------|------------------|
| **Algorithm** | New algorithms/models | Example → Core mechanism → Optimizations |
| **System** | Architecture/engineering | Single-node → Distributed → Production |
| **Theory** | Theoretical analysis | Problem → Theorem → Proof → Application |

## Parameters

### `--audience`

- `engineer`: Implementation details, design patterns, edge cases
- `researcher`: Technical depth, related work comparison, theory
- `manager`: Problem context, decision rationale, risk assessment

### `--domain` (optional)

Engineering domain for contextual mapping:
- `distributed-systems`: Distributed systems, microservices
- `storage`: Storage systems, file systems  
- `database`: Databases, data warehouses
- `network`: Networks, CDN, load balancing
- `ml-system`: ML systems, recommendation systems

## Analysis Workflow

This skill processes papers in 6 stages using prompts in `prompts/`:

1. **Core Extraction** (`extract_core.txt`): Identify contributions and key decisions
2. **First Principles** (`first_principles.txt`): Trace problem essence and rationale
3. **Progressive Layers** (`progressive_layers.txt`): Organize by complexity
4. **Engineering Map** (`engineering_map.txt`): Map to software patterns (engineer audience only)

## Output Templates

Templates in `templates/` provide structure for each paper type:
- `system.md`: System papers (infrastructure, architecture)
- `algorithm.md`: Algorithm papers (models, methods)
- `theory.md`: Theory papers (analysis, proofs)

## Examples

See `examples/attention_residuals.md` for a complete example converting the Attention Residuals paper into an engineer-friendly analysis with distributed systems mappings.

## Resource Loading Guide

**Always load in this order:**

1. **Parse paper** → **Extract core** (use `prompts/extract_core.txt`)
2. **First principles analysis** (use `prompts/first_principles.txt`)
3. **Progressive organization** (use `prompts/progressive_layers.txt`)
4. **Engineering mapping** (if `--audience engineer`, use `prompts/engineering_map.txt`)
5. **Generate output** (use appropriate template from `templates/`)

## Constraints & Notes

- Paper quality matters: clear abstract and introduction required
- Output depth auto-adjusts based on `--audience`
- Engineering mapping accuracy depends on `--domain` setting
- Complex proofs may need manual verification
