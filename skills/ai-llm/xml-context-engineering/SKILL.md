---
name: xml-context-engineering
description: |
  USE WHEN: writing system prompts, structuring complex instructions, engineering context for Claude agents, optimizing attention efficiency in long prompts.
  DO NOT USE WHEN: writing regular code, simple messages, or content where Markdown suffices.
  For optimal context architecture, trigger deep thinking with "think harder" or "ultrathink" to analyze attention economics thoroughly.
license: MIT
---

Transform unstructured prompt content into XML-tagged context that maximizes LLM comprehension. The user provides raw instructions, data, or prompt content needing structure.

## Context Thinking

Before tagging anything, analyze the attention economics:
- **Boundaries**: Where does one semantic unit end and another begin? Tags mark cognitive boundaries, not arbitrary divisions.
- **Hierarchy**: Does nesting reflect logical containment, or are you creating false depth? Flatten unless parent-child relationship is real.
- **Retrieval**: Will the model need to reference this section? Name tags for retrieval (`<error_handling>`) not description (`<the_part_about_errors>`).
- **Density**: Is this content high-signal enough to warrant its own tag? Low-value content dilutes attention—exclude rather than tag.

**CRITICAL**: XML tags are attention anchors, not decorations. If a tag doesn't help the model locate, isolate, or reference content, it's noise. Every tag must earn its tokens. Tag soup—nested structures that add complexity without clarity—is worse than no tagging at all.

## Context Engineering Guidelines

Focus on:
- **Semantic naming**: Use domain-native tag names (`<constraints>`, `<examples>`, `<tool_guidance>`) that create instant comprehension. Avoid generic names like `<section1>` or `<info>`.
- **Flat-first structure**: Default to siblings, not children. Use `<instructions>` and `<context>` as siblings, not `<prompt><instructions><context>`. Nest only when content genuinely belongs inside another.
- **Canonical sections**: Standard patterns include `<system_context>`, `<user_background>`, `<instructions>`, `<constraints>`, `<examples>`, `<output_format>`. Deviate only with clear purpose.
- **Attribute discipline**: Use attributes for metadata that aids filtering (`<example type="edge_case">`), not for content that should be text. Attributes are invisible to casual scanning.
- **Progressive disclosure**: Place high-frequency reference content early. Put `<instructions>` before `<background>`. The model's attention favors content closer to the query.

NEVER create nested tags more than 2 levels deep (tag soup destroys readability), use XML for content that Markdown handles better (headers, lists, emphasis), tag every paragraph individually (over-segmentation fragments attention), use closing tags that don't match openers, create tags without content between them, or name tags with verbs (`<process_this>`) instead of nouns (`<processing_rules>`).

Match tag density to content criticality. Dense XML for complex multi-part instructions. Light XML (or pure Markdown) for conversational context. System prompts benefit from heavy structure; user messages rarely need any.

**IMPORTANT**: Anthropic's research shows context rot increases with token count. XML tags fight this by creating scannable landmarks—but only if used sparingly. The goal is minimum viable structure: just enough tags to create clear boundaries, no more.

## Deep Thinking Mode

For complex context architecture, activate extended thinking:
- **"think harder"** or **"ultrathink"** triggers maximum reasoning depth (31,999 tokens)
- Use for: system prompts >2000 tokens, multi-agent coordination, attention-critical applications
- Enables thorough analysis of semantic boundaries, retrieval patterns, and attention economics
- Recommended when: prompt engineering for production agents or high-stakes LLM applications
