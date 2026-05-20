---
name: content-modeling-best-practices
description: >-
  Structured content modeling principles with Sanity-specific guidance. Use
  when designing or reviewing content schemas, document types, field structures,
  or content architecture — including decisions around references vs embedding,
  content reuse, taxonomy, page builders, multi-channel delivery, or
  refactoring existing schemas. Trigger when the user mentions schema design,
  content model, document types, content structure, headless CMS architecture,
  or asks how to model any content type.
license: MIT
metadata:
  author: sanity
  version: "1.0.0"
---

# Content Modeling Best Practices

Principles for designing structured content that's flexible, reusable, and maintainable. These concepts apply to any headless CMS but include Sanity-specific implementation notes.

## When to Apply

Reference these guidelines when:
- Starting a new project and designing the content model
- Evaluating whether content should be structured or free-form
- Deciding between references and embedded content
- Planning for multi-channel content delivery
- Refactoring existing content structures

## Core Principles

1. **Content is data, not pages** — Structure content for meaning, not presentation
2. **Single source of truth** — Avoid content duplication
3. **Future-proof** — Design for channels that don't exist yet
4. **Editor-centric** — Optimize for the people creating content

## Resources

See `resources/` for detailed guidance on specific topics:
- Separation of content and presentation
- Reference vs embedding strategies
- Content reuse patterns
- Taxonomy and classification
