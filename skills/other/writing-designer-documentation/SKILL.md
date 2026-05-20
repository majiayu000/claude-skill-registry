---
description: Create, update, or validate designer MDX documentation files
argument-hint: create|update|validate ComponentName [details]
---

# Writing Designer Documentation Skill

You are a Nimbus designer documentation specialist. Create, update, or validate
designer MDX files (`{component}.mdx`) that explain design patterns, visual
guidelines, and usage recommendations for non-technical audiences.

**CRITICAL**: Focus on design decisions, visual patterns, and usage
guidelines—NOT implementation details.

**Note**: If you're creating a NEW component, consider using
`/propose-component` instead. This skill is for:

- Creating standalone designer documentation
- Updating existing designer documentation
- Being invoked by higher-level commands or agents

## Mode Detection

- **create** - Generate new designer documentation file
- **update** - Enhance existing documentation, add sections, update guidelines
- **validate** - Check documentation compliance with guidelines

You MUST default to **create** if no mode is specified. This ensures missing
docs get created rather than accidentally updating an existing file.

## Required Research (All Modes)

Before implementation, you SHOULD research these areas in parallel:

1. **Read** documentation guidelines:

   ```bash
   cat docs/file-type-guidelines/documentation.md
   ```

2. **Review** component implementation for design decisions

3. **Check** design system documentation:
   ```bash
   ls packages/nimbus/src/components/*/*.mdx
   ```

Additionally:

- You MUST analyze the component's design purpose and visual patterns (ensures
  content is design-focused, not implementation)
- You SHOULD check for Figma design resources (improves completeness if
  available)

## File Structure

### Location

```
packages/nimbus/src/components/{component}/{component}.mdx
```

### Required Frontmatter

```yaml
---
id: Components-ComponentName
title: Component Name
exportName: ComponentName
description: Brief one-line description
lifecycleState: Stable # Experimental|Alpha|Beta|Stable|Deprecated
order: 999
menu:
  - Components
  - Category Name # Inputs, Data Display, Navigation, Feedback, Overlay, Layout, Typography
  - Component Name
tags:
  - component
  - relevant-keywords
figmaLink: https://www.figma.com/design/...
---
```

## Content Structure (REQUIRED)

### 1. Overview

The component title and description are rendered from frontmatter. Content starts
directly with the Overview section—do not add a `# Component Name` heading or
introductory paragraph in the body.

```markdown
## Overview

Explain: design purpose, key visual characteristics, primary use cases, design
rationale.

### Resources

[Figma library](figmaLink) [Related ARIA Pattern](ariaPatternLink) # If
applicable
```

### 2. Design Hierarchy (if applicable)

```markdown
### Hierarchy

Explain primary, secondary, tertiary actions with design rationale and jsx live
examples.
```

### 3. Variables (REQUIRED)

````markdown
## Variables

### Size

Explain each size with design rationale:

```jsx live
const App = () => (
  <Stack direction="horizontal" gap="400">
    <ComponentName size="sm">Small</ComponentName>
    <ComponentName size="md">Medium (default)</ComponentName>
    <ComponentName size="lg">Large</ComponentName>
  </Stack>
);
```
````

### Color Palette

Document each variant's purpose:

```jsx live
const App = () => (
  <Stack direction="horizontal" gap="400">
    <ComponentName colorPalette="primary">Primary</ComponentName>
    <ComponentName colorPalette="critical">Critical</ComponentName>
  </Stack>
);
```

````

### 4. Guidelines (OPTIONAL but RECOMMENDED)

```markdown
## Guidelines

### Best practices

- Design principle with rationale
- Visual hierarchy guidance

### When to use

> [!TIP]\
> Use when...
- Use case 1
- Use case 2

> [!CAUTION]\
> When NOT to use
- Avoid case 1
- Anti-pattern to avoid
````

### 5. Writing Guidelines (if applicable)

```markdown
## Writing guidelines

Guidelines for content creators and terminology preferences.

## Preferred words

| Text       | Description    |
| ---------- | -------------- |
| **Save**   | When to use    |
| **Cancel** | Design context |

## Avoid these words

| Avoid    | Use instead            |
| -------- | ---------------------- |
| OK       | Actions that explain   |
| Continue | Context-specific words |
```

### 6. Usage Examples (Optional)

Show correct vs. incorrect usage with Do/Don't sections and jsx live examples.

## Code Examples (jsx live Blocks)

**CRITICAL**: Use `jsx live` blocks (NOT `jsx live-dev`).

All Nimbus components available globally—NO imports needed. For detailed
jsx live patterns, see writing-developer-documentation skill.

## Create Mode

**Step 1**: Gather design context (purpose, hierarchy, colors, sizes, icons,
Figma resources) **Step 2**: Write frontmatter with ID, menu hierarchy, tags
**Step 3**: Write overview explaining component from design perspective **Step
4**: Document visual variants with jsx live examples and rationale **Step 5**:
Create actionable design guidelines (best practices, when to use/avoid) **Step
6**: Add writing guidelines if text content applies

## Update Mode

1. You MUST read the current documentation file (understand what exists before
   changing)
2. You SHOULD identify gaps in design guidance (visual hierarchy, use cases,
   color palette)
3. You MUST preserve existing structure and tone (don't rewrite what's working)
4. You MUST maintain consistency with other designer docs (don't deviate from
   established style without reason)
5. You SHOULD enhance with visual examples where they clarify (not every section
   needs jsx live examples, only places where visual demonstration helps)

Common updates: missing sections, better examples, updated guidelines, Figma
links, clearer explanations.

## Validate Mode

### Validation Checklist

#### File Structure (ALL REQUIRED - breaks build or navigation if violated)

- [ ] File location:
      `packages/nimbus/src/components/{component}/{component}.mdx` (MUST match)
- [ ] All required frontmatter fields present: id, title, exportName, description, order, menu, tags (MUST exist)
- [ ] ID follows pattern: `Components-{ComponentName}` (MUST match, breaks
      search/routing if wrong)
- [ ] Menu hierarchy includes proper category (MUST have)
- [ ] Tags array present (MUST have)
- [ ] Figma link present (SHOULD have if available)

#### Content Structure (SHOULD have unless inapplicable)

- [ ] No duplicate `# Component Name` heading in body (title comes from frontmatter)
- [ ] Overview section explaining design purpose (design rationale)
- [ ] Resources section with links (reference materials)
- [ ] Variables section with jsx live examples (shows options)
- [ ] Guidelines section (helps designers decide when to use)

#### Code Examples

- [ ] MUST use `jsx live` blocks (NOT `jsx live-dev`)
- [ ] MUST NOT have import statements
- [ ] MUST be visually focused on design, not implementation
- [ ] MUST show design variants clearly
- [ ] SHOULD be production-ready examples

#### Design Focus

- [ ] MUST be designer-focused (NOT implementation)
- [ ] MUST explain WHEN and WHY to use
- [ ] MUST document visual hierarchy and color palette
- [ ] MUST include size variants with rationale
- [ ] SHOULD mention accessibility from user perspective

#### Writing Quality

- [ ] MUST have clear, concise descriptions
- [ ] MUST include design rationale
- [ ] MUST document best practices
- [ ] MUST identify anti-patterns
- [ ] MUST have consistent tone
- [ ] MUST avoid technical jargon

### Validation Report

```markdown
## Designer Documentation Validation: {ComponentName}

### Status: [✅ PASS | ❌ FAIL | ⚠️ WARNING]

### ✅ Compliant

[List passing checks]

### ❌ Violations (MUST FIX)

[Violations with line references]

### ⚠️ Warnings (SHOULD FIX)

[Non-critical improvements]

### Design Focus Assessment

- Design rationale: [Present | Partial | Missing]
- Visual examples: [Comprehensive | Adequate | Insufficient]
- Guidelines quality: [Excellent | Good | Needs improvement]
- Writing guidelines: [Present | Not applicable | Missing]

### Recommendations

[Specific improvements needed]
```

## Common Component Patterns

**Button-type**: Visual hierarchy (primary/secondary/tertiary), action
importance, color semantics, icon placement, button labels

**Form**: Input states, validation feedback, error presentation, size variants,
labels

**Feedback**: Visual importance hierarchy, color semantics
(info/success/warning/error), quick-recognition icons, message content

**Overlay**: When to use vs. alternatives, size/placement guidelines, content
structure, dismissal patterns, user-perspective accessibility

## Error Recovery

If validation fails:

1. You MUST verify frontmatter structure and unique ID (blocks build if wrong)
2. You MUST ensure menu hierarchy is correct (affects navigation)
3. You MUST confirm jsx live blocks (not jsx live-dev) (doc generation
   requirement)
4. You SHOULD review tone (designer-focused, not technical) - fixes readability

## Reference Examples

- **Simple**: `packages/nimbus/src/components/badge/badge.mdx`
- **Form**: `packages/nimbus/src/components/text-input/text-input.mdx`
- **Interactive**: `packages/nimbus/src/components/button/button.mdx`
- **Overlay**: `packages/nimbus/src/components/dialog/dialog.mdx`

---

**Execute designer documentation operation for: $ARGUMENTS**
