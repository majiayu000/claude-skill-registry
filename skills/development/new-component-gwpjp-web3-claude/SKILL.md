---
name: new-component
description: Creates new React components following project conventions. Scaffolds TypeScript types, MUI styling patterns, and named exports in src/components/. References Common component library to avoid duplication.
disable-model-invocation: true
argument-hint: "[ComponentName] or [Folder/ComponentName]"
---

# Create New Component

Create a new React component following project conventions.

## Initialization

When invoked:

1. Read `.claude/docs/component-reference.md` to check if a Common component already handles the need
2. Read `.claude/docs/project-rules.md` for project conventions

## Instructions

1. Parse the component name from `$ARGUMENTS`
2. Determine the file path:
   - If name includes `/`, treat the first part as a subfolder
   - Create in `src/components/`
3. **Before creating:** Check `docs/component-reference.md` to verify no existing Common component handles this use case
4. Create the component file with:
   - Proper TypeScript types for props
   - Functional component using React hooks if needed
   - MUI styling patterns (use theme values, never hardcoded colors/fonts)
   - Named export (not default)
5. If the component needs types, add them to `src/types/` or inline

## Template

```tsx
import { type FC } from "react";
import { Box } from "@mui/material";

interface ComponentNameProps {
  // Add props here
}

export const ComponentName: FC<ComponentNameProps> = (props) => {
  return <Box>{/* Component content */}</Box>;
};
```

## Conventions

- Use `CommonButton` (not raw `Button`), `CTAButton` for blockchain actions
- Use Common input components (not raw `TextField`)
- Use theme palette references for colors (`color="text.secondary"`)
- Use Typography variants for text (never inline `fontSize`/`fontWeight`)
- Use `NumberFormatter` or `displayNumber` for formatted numbers

## Verification

After creating the component:

```bash
yarn typecheck && yarn lint && yarn prettier && yarn build
```
