---
name: storybook-scaffolder
description: "Generates a Storybook story file (*.stories.tsx) with M3 design token imports and interactive variant stories. Use when documenting React components for development and QA testing."
version: 2.0.0
---

# Storybook Scaffolder Workflow (v2)

1. Get component path.
2. Generate `.stories.tsx` file from template.
3. **Prepend this line to the top of the generated file:** `import 'src/styles/design-tokens.css';`
4. Report success.
