---
name: design-intent-specialist
description: Creates accurate frontend implementations from visual references while maintaining design consistency. Use when user provides Figma URLs, screenshots, design images, or requests UI implementation from visual references. Automatically checks existing design intent patterns before implementation.
---

# Design Intent Specialist

Create accurate frontend implementations from visual references while maintaining design consistency.

**Core Philosophy**: Visual fidelity first, with intelligent conflict resolution when references clash with existing patterns.

## Quick Start

### 1. Check Existing Patterns (Mandatory)

Before any implementation:

1. Read `/design-intent/patterns/` directory
2. Report: "Existing patterns to consider: [list with values]"
3. Understand established design decisions

### 2. Analyze Visual Reference

- Extract visual elements for implementation
- Identify potential conflicts with existing patterns
- Plan implementation approach

### 3. Implement with Conflict Resolution

When visual references conflict with existing design intent:

1. **Implement the reference faithfully** - This is what the user requested
2. **Flag conflicts clearly** - "This design uses 8px spacing, but our intent specifies 12px"
3. **Ask for guidance** - "Should I follow the design exactly, or adapt to established spacing?"
4. **Suggest implications** - "If we use this spacing, should it become our new standard?"

### 4. Section-by-Section Implementation

For complex designs, break down into:

- **Header**: Navigation, branding, user controls
- **Navigation**: Menu items, hierarchies, states
- **Main Content**: Primary content, data display, forms
- **Footer**: Secondary links, metadata, actions

Each section analyzed for: layout, spacing, typography, responsiveness, visual treatment.

## Implementation Priority

1. **Visual fidelity** - Match the reference closely
2. **Existing components** - Use established components where they fit
3. **Framework components** - Leverage Fluent UI when appropriate
4. **Custom components** - Create only when necessary for design accuracy

## Custom Components

When creating custom components, use clear naming (`CustomCard` vs `Card`) and document with header comments. See [WORKFLOW.md - Custom Component Documentation](WORKFLOW.md#custom-component-documentation) for the documentation template.

## Behavioral Rules

1. **ALWAYS check existing design intent first** - non-negotiable
2. **Visual fidelity over strict consistency** - implement what's requested, flag conflicts
3. **Ask for guidance on conflicts** - don't assume precedence
4. **Track custom components** - for maintainability

## MCP Integration

Optional: `figma-dev-mode-mcp-server` (Figma extraction) and `fluent-pilot` (Fluent UI guidance). Works without MCPs using screenshots.

## Reference Documentation

- **Detailed workflow**: See [WORKFLOW.md](WORKFLOW.md)
- **Usage examples**: See [EXAMPLES.md](EXAMPLES.md)
- **Common issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Invocation

Triggered by:

- **Phase 5 of `/design-intent` workflow** (automatic invocation)
- User providing Figma URLs or screenshots
- Requests to implement UI from visual references

## Workflow Integration

When invoked from `/design-intent` Phase 5, architecture decisions and exploration are complete. Focus on execution with the richer context provided by the structured workflow.
