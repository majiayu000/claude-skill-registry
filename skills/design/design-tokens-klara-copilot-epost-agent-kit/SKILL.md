---
name: design-tokens
description: (ePost) Use when working with Vien 2.0 design tokens, Figma variables, semantic colors, multi-brand theming, or translating tokens to platform-native formats (CSS variables, Swift constants, Kotlin theme objects)
user-invocable: false

metadata:
  agent-affinity: [epost-muji]
  keywords: [figma, variables, tokens, design-system, semantic]
  platforms: [all]
  connections:
    requires: [figma]
---

# Figma Variables Architecture Skill

## Purpose

Deep analysis of the Vien 2.0 Figma design system variables. Covers the 4-layer architecture (Primitives → Semantics → Platform → Components), multi-brand support, mode composition, and reference chain resolution.

## Aspect Files

| File | Coverage |
|------|----------|
| `references/variables-architecture.md` | Full architectural analysis: 5 external brand libraries, 4 layers, 42 collections, reference chain patterns |
| `references/inconsistencies-improvements.md` | 8 inconsistencies, 6 structural complexities, 14 improvement recommendations |
| `figma-variables.json` | Raw 2.3 MB export of all Figma design variables (machine-readable) |

## Key Facts

- **1,059 variables** across **42 collections**
- **4 architectural layers**: Primitives (L1) → Semantics (L2) → Platform (L3) → Components (L4)
- **5 external brand libraries** with 2,064 remote references
- **Reference chains** up to 11 hops deep
- **200+ distinct modes** across all collections
- **Platform layer** is the bridge between design language and code implementation

## Usage

- Referenced by `epost-muji` agent for design system decisions
- Used by Figma-to-code pipeline for token resolution
- Informs component implementation across web, iOS, and Android
