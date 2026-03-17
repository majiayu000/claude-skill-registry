---
name: skill-with-references
description: Demonstrates how skills can reference external documentation files. Use when you need to load guidelines, best practices, or reference materials on-demand.
---

# Skill with References

## What This Skill Does

This skill shows how to **reference external documentation** progressively. Instead of embedding everything in the SKILL.md file, it maintains separate reference documents that are loaded when needed.

This follows the **progressive disclosure** pattern—provide essential info first, then detailed references when the user wants to dive deeper.

## Workflow

1. **Initial engagement** - Provide basic guidance from SKILL.md
2. **User asks for details** - Load relevant reference document
3. **Progressive discovery** - User discovers deeper resources as needed

## Available References

- `references/best-practices.md` - Guidelines and recommended patterns
- `references/examples.md` - Practical examples and use cases
- `references/common-mistakes.md` - Pitfalls to avoid and how to prevent them

## How References Work

When you need specific guidance, mention what you're interested in:
- "Show me best practices" → Load `best-practices.md`
- "Give me examples" → Load `examples.md`
- "What mistakes should I avoid?" → Load `common-mistakes.md`

## Key Concepts

### Progressive Disclosure
Load information as needed, not all at once. This reduces cognitive load and makes the skill more helpful.

### Reference Organization
- One file per topic
- Clear, scannable structure
- Easy to update and maintain

### When to Use This Pattern

Use skill-with-references when you have:
- Multiple related documents
- Guidelines that evolve over time
- Deep knowledge that's optional to know
- Documentation that's useful separately

## Example Scenario

**User:** "I want to follow best practices"
**Response:**
1. Acknowledge the request
2. Load `references/best-practices.md`
3. Present organized guidelines
4. Offer to dive deeper into specific areas

This approach keeps the skill focused while providing unlimited depth.
