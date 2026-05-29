---
name: Template Versioning Strategy
description: Backward-compatible video template versioning and composition registry management. Use this when creating alternative video templates, modifying composition props, evolving data schemas, or maintaining multiple template versions in Root.tsx.
---

# Template Versioning Strategy

This Skill provides Claude Code with specific guidance on how it should handle video composition and template versioning.

## When to use this skill:

- Creating new video template variations (V1, V2, etc.)
- Modifying existing composition component props
- Registering compositions in Root.tsx
- Extending RenderRequest or RecapBook type definitions
- Changing frame timing in composition sequences
- Testing backward compatibility with old data

## Instructions

- **Template Versioning**: When creating alternative templates, version them clearly (MonthlyRecapV1, MonthlyRecapV2)
- **Backward Compatibility**: Maintain existing template rendering capability when adding new templates
- **Composition Registry**: Register all composition variations in Root.tsx with Remotion.registerRoot
- **Breaking Changes**: Document breaking changes to composition props or data structure requirements
- **Data Schema Evolution**: When extending RecapBook or RenderRequest types, add optional fields first
- **Frame Timing Changes**: Test all sequences when modifying frame-based timing calculations
- **Rollback Testing**: Verify old data can still render with updated compositions

**Examples:**
```typescript
// Good: Versioned templates, backward compatible
export const MonthlyRecapV1: React.FC<MonthlyRecapProps> = (props) => {
  // Original template implementation
};

export const MonthlyRecapV2: React.FC<MonthlyRecapProps> = (props) => {
  // Enhanced template with new features
};

// Root.tsx registration
Composition({
  id: 'MonthlyRecap',
  component: MonthlyRecapV2, // Default to latest
  ...VIDEO_CONFIG,
});

Composition({
  id: 'MonthlyRecapV1',
  component: MonthlyRecapV1, // Keep v1 available
  ...VIDEO_CONFIG,
});

// Bad: Overwriting existing template, breaking backward compat
export const MonthlyRecap: React.FC = (props) => {
  // Completely different implementation that breaks old renders
};
```
