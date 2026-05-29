---
description: Universal markdown content quality standards for active voice, heading hierarchy, accessibility compliance (alt text, WCAG AA contrast, screen reader support), and professional formatting. Essential for all markdown content creation across docs/, Hugo sites, plans/, and repository files. Auto-loads when creating or editing markdown content.
---

# Applying Content Quality Standards

## Purpose

This Skill provides comprehensive guidance for applying **universal content quality standards** to all markdown content in the repository. It ensures consistent writing quality, accessibility compliance, and professional presentation across documentation, Hugo sites, planning documents, and root files.

**When to use this Skill:**

- Creating or editing markdown content in docs/
- Writing content for Hugo sites (ayokoding-web, ose-platform-web)
- Creating planning documents in plans/
- Writing repository root files (README.md, CONTRIBUTING.md, etc.)
- Ensuring accessibility compliance (WCAG AA)
- Reviewing content for quality standards

## Core Quality Principles

### Writing Style and Tone

**Active Voice Required**: Use active voice for clarity and directness.

✅ **Good**: "The agent validates the content against the convention."
❌ **Avoid**: "The content is validated against the convention by the agent."

**Professional Tone**: Maintain professional, welcoming tone without being overly formal.

**Clarity and Conciseness**: Write clear, direct sentences. Avoid jargon without context.

**Audience Awareness**: Consider reader's technical level and provide necessary context.

### Heading Hierarchy

**Single H1 Rule**: Each markdown file MUST have exactly one H1 heading (# Title).

**Proper Nesting**: Follow hierarchical structure without skipping levels:

- H1 (#) - Document title
- H2 (##) - Major sections
- H3 (###) - Subsections
- H4 (####) - Sub-subsections
- H5/H6 - Use sparingly

❌ **Invalid nesting** (skips level):

```markdown
# Title

### Subsection ← Skips H2!
```

✅ **Valid nesting**:

```markdown
# Title

## Section

### Subsection
```

### Accessibility Standards

**Alt Text Required**: All images MUST have descriptive alt text.

```markdown
✅ ![Architecture diagram showing six-layer hierarchy](./diagram.png)
❌ ![](./diagram.png) ← Missing alt text
```

**WCAG AA Color Contrast**: Text must meet WCAG AA contrast ratios:

- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum

**Semantic Formatting**:

- Use **bold** for emphasis, not italics
- Use proper heading structure (not bold text as headers)
- Use lists for list content (not manual bullets)

**Screen Reader Support**: Content must be accessible to screen readers through proper HTML structure and ARIA labels when needed.

### Formatting Conventions

**Code Blocks**: Always specify language for syntax highlighting.

````markdown
✅ Good:

```javascript
const x = 10;
```
````

❌ Bad:

```
const x = 10;  ← No language specified
```

````

**Paragraph Length**: Keep paragraphs concise (≤5 lines for readability).

**Line Length**: Aim for 80-100 characters per line for better readability.

**Lists**: Use consistent formatting:
- Unordered lists: Use `-` (hyphen) for consistency
- Ordered lists: Use `1.` numbering
- Nested lists: Indent with 2 spaces per level

## No Time Estimates

**CRITICAL**: Never include time-based framing in content.

❌ **Forbidden**:
- "This tutorial takes 30 minutes"
- "Complete this in 2-3 weeks"
- "You can do this in 5 minutes"

✅ **Instead**:
- Describe what will be accomplished
- List concrete outcomes
- Let users determine their own pace

**Rationale**: Time estimates create artificial pressure and vary widely by experience level.

## Common Quality Checklist

Before publishing any markdown content, verify:

- [ ] Active voice used throughout
- [ ] Exactly one H1 heading
- [ ] Proper heading nesting (no skipped levels)
- [ ] All images have descriptive alt text
- [ ] Code blocks specify language
- [ ] No time-based estimates or framing
- [ ] Professional, welcoming tone
- [ ] Paragraphs ≤5 lines
- [ ] Clear, jargon-free language (or jargon explained)
- [ ] WCAG AA color contrast for any custom colors
- [ ] Semantic formatting (bold for emphasis, proper lists)

## Common Mistakes

### ❌ Mistake 1: Missing alt text

**Wrong**: `![](./image.png)`
**Right**: `![Detailed description of image content](./image.png)`

### ❌ Mistake 2: Skipped heading levels

**Wrong**:
```markdown
# Title
### Subsection  ← Skips H2
````

**Right**:

```markdown
# Title

## Section

### Subsection
```

### ❌ Mistake 3: Time-based framing

**Wrong**: "This tutorial takes 30 minutes to complete."
**Right**: "This tutorial covers X, Y, and Z concepts."

### ❌ Mistake 4: Passive voice overuse

**Wrong**: "The file is created by the command."
**Right**: "The command creates the file."

### ❌ Mistake 5: Code blocks without language

**Wrong**:

```
npm install
```

**Right**:

```bash
npm install
```

## References

**Primary Convention**: [Content Quality Principles](../../../governance/conventions/content/quality.md)

**Related Conventions**:

- [Accessibility First Principle](../../../governance/principles/content/accessibility-first.md) - Foundational accessibility principle
- [No Time Estimates Principle](../../../governance/principles/content/no-time-estimates.md) - Rationale for avoiding time framing
- [README Quality Convention](../../../governance/conventions/content/readme-quality.md) - README-specific quality standards
- [Color Accessibility Convention](../../../governance/conventions/formatting/color-accessibility.md) - WCAG color contrast requirements

**Related Skills**:

- `docs__creating-accessible-diagrams` - Accessible Mermaid diagrams with WCAG colors
- `readme__writing-readme-files` - README-specific quality standards
- `docs__applying-diataxis-framework` - Documentation organization framework

---

This Skill packages universal content quality standards for consistent, accessible, professional markdown content across the repository. For comprehensive details, consult the primary convention document.
