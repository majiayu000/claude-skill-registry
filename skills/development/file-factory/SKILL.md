---
name: file-factory
description: How to use the file-factory CLI to create new React components, hooks, context providers, Next.js pages along with associated tests and storybook stories. ALWAYS use this tool instead of manually creating new components/hooks/contexts/pages to ensure consistent file structure and conventions.
---

# File Factory Skill

This skill describes how to create new React components, hooks, context providers, and Next.js pages in the Squareone monorepo using the `@lsst-sqre/file-factory` CLI tool. **ALWAYS use this tool instead of manually creating new components/hooks/context providers/pages.** It ensures consistent file structure, local barrel files, and CSS modules. After creation, the tool displays instructions for any manual steps needed (like updating root barrel files).

## Tool Calling

Call from the monorepo root:

```bash
pnpm file-factory <type> <name> --package <package-name>
```

Package resolution supports multiple formats:
- **Short names**: `squared`, `squareone` (recommended)
- **Full names**: `@lsst-sqre/squared`
- **Directory paths**: `apps/squareone`, `packages/squared`

If there's a conflict between an app and package with the same short name, apps take priority.

## Documentation for specific project types

Reference these pages for CLI command documentation:

- React components: [components.md](components.md)
- React hooks: [hooks.md](hooks.md)
- Global context providers: [contexts.md](contexts.md)
- Next.js pages: [pages.md](pages.md)

## Package-Specific Conventions

- For apps/squareone: [squareone.md](squareone.md)
- For packages/squared: [squared.md](squared.md)

## Important Notes

1. **Always use the tool** - Never manually create component directories
2. **Component-scoped contexts** - Use `--with-context`, not the `context` command
3. **Global contexts** - Use the `context` command for app-wide state
4. **Post-creation messages** - For squared package, follow the displayed instructions to add exports to root barrel files
5. **Naming conventions**:
   - Components: PascalCase (Button, DataTable)
   - Hooks: camelCase with `use` prefix (useDebounce)
   - Contexts: Input "Theme" → generates ThemeContext, ThemeProvider, useTheme

## Example Workflows

### Adding a component to squared (component library):

```bash
pnpm file-factory component Alert --package squared --with-story
# Creates: packages/squared/src/components/Alert/
# Displays instructions to add exports to src/components/index.ts and src/index.ts
```

### Adding a complex component with state to squareone:

```bash
pnpm file-factory component Wizard --with-context --package squareone
# Creates: apps/squareone/src/components/Wizard/
# Includes: Wizard.tsx, WizardContext.tsx (with WizardProvider + useWizard)
```

### Adding a global theme context to squareone:

```bash
pnpm file-factory context Theme --package squareone
# Creates: apps/squareone/src/contexts/ThemeContext/
# Use ThemeProvider in _app.tsx, useTheme() in components
```

## Related Skills

After scaffolding files with file-factory, use these skills for implementation guidance:

- **component-creation** - TypeScript patterns, CSS Modules conventions, and implementation details for components
- **squared-package** - Architecture constraints for squared components (NO BUILD STEP, CSS Modules only)
- **design-system** - Complete CSS variable and design token reference for styling
- **testing-infrastructure** - Testing patterns for generated test files
