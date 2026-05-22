---
name: design-spec
description: Create UI/UX design specifications from requirements or Figma designs. Covers component specs (Atom/Molecule/Organism), accessibility audits (WCAG 2.1 AA), design tokens, responsive behavior, and dev handoffs. Triggers on "design spec", "ui spec", "component spec", "accessibility audit", "design handoff", "design tokens", "wireframe", "mockup".
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, ai-multimodal, mcp__figma__*
---

# Design Specification

Create comprehensive UI/UX specifications for implementation.

## When to Use
- PBI needs design documentation
- Figma design ready for handoff
- Component specification required
- Accessibility audit needed
- Design system additions

## ⚠️ MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **⚠️ MUST READ** `references/design-system-reference.md` — component specs, accessibility audit template, design tokens, responsive breakpoints, handoff checklist

## Workflow

1. **Determine Source Type**
   - If URL starting with `figma.com`: treat as direct Figma source
   - If file path: read file and check for `figma_link` in frontmatter

2. **Load Source**
   - Read PBI/requirements file
   - Parse YAML frontmatter
   - Extract `figma_link` field if present

3. **Detect Figma Link**
   ```
   Sources (priority order):
   1. Direct Figma URL argument
   2. frontmatter.figma_link
   3. Figma URLs in "Design Reference" section
   ```
   Pattern: `https?://(?:www\.)?figma\.com/(design|file)/([a-zA-Z0-9]+)(?:/[^?]*)?(?:\?node-id=([0-9]+:[0-9]+))?`

4. **Extract Figma Specs (if link found)**
   - Call `/figma-extract {url}` internally
   - Handle failures gracefully (continue without Figma data)

5. **Define Components** (use template from `references/design-system-reference.md`)
   - Type classification: Atom / Molecule / Organism / Template
   - States: default, hover, active, disabled, error, loading
   - Design tokens mapping
   - Accessibility requirements (WCAG 2.1 AA)

6. **Specify Responsive Behavior** (breakpoints in reference)

7. **Generate Spec**
   Structure: Overview, Component Inventory, States, Design Tokens, Accessibility, Responsive, Figma Extracted Specs

8. **Save Artifact**
   - Path: `team-artifacts/design-specs/{YYMMDD}-designspec-{feature}.md`

## Fallback Behavior
When Figma extraction unavailable:
1. Log warning: "Figma specs not extracted: {reason}"
2. Continue with manual spec creation
3. Leave Section 7 with placeholder text

## Design Token Format
```scss
$primary: #1976D2;     // Colors
$heading: 24px/1.2 'Inter'; // Typography
$gap-sm: 8px;          // Spacing
```

## Example
```bash
/design-spec https://www.figma.com/design/ABC123/UserProfile
/design-spec team-artifacts/pbis/260119-pbi-user-profile.md
```

## Output
Creates: `team-artifacts/design-specs/{YYMMDD}-designspec-{feature}.md`


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
