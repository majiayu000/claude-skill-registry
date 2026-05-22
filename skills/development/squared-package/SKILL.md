---
name: squared-package
description: Critical architecture knowledge for the squared component library package. Use this skill when working on squared package components, troubleshooting build/transpilation issues, or setting up apps to consume squared. Covers the NO BUILD STEP architecture, CSS Modules-only styling requirement, Next.js transpilation configuration, direct TypeScript source exports, and testing infrastructure.
---

# Squared Package Architecture

The `@lsst-sqre/squared` package is a React component library with a unique architecture designed for flexibility and type safety.

## Critical Architecture Rules

### NO BUILD STEP

⚠️ **The squared package does NOT have a build step** - it exports TypeScript source files directly.

This means:
- **package.json** `main`, `module`, and `types` all point to `src/index.ts` (not a `dist/` directory)
- Consuming apps must transpile the package themselves
- No `tsup`, `tsc`, or other build tools in the squared package
- Changes are immediately available without rebuilding the package

### Why This Architecture?

1. **Flexibility**: Consuming apps control transpilation (target browsers, polyfills, etc.)
2. **Type Safety**: Source TypeScript available for better IDE integration
3. **Development Speed**: No build step means instant updates during development
4. **Simplicity**: Fewer build tools to configure and maintain

## Package.json Configuration

See the actual package configuration at `packages/squared/package.json`.

**Key fields:**
```json
{
  "main": "./src/index.ts",
  "module": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "default": "./src/index.ts"
    },
    "./components/*": "./src/components/*"
  },
  "sideEffects": false
}
```

**Important:**
- All entry points are TypeScript source files
- `sideEffects: false` enables tree-shaking
- Component-level exports for granular imports

## Styling Requirements

### CSS Modules Only

⚠️ **Squared package MUST use CSS Modules** - NO styled-components allowed.

**Why:**
- Avoids runtime CSS-in-JS overhead
- Better SSR performance
- Consistent with design token system
- Clear separation of styles and logic

**Pattern:**
```
MyComponent/
├── MyComponent.tsx
├── MyComponent.module.css
├── MyComponent.stories.tsx
├── MyComponent.test.tsx
└── index.ts
```

### Using Design Tokens

Styles use design tokens from `@lsst-sqre/rubin-style-dictionary` and `@lsst-sqre/global-css`.

See the **design-system** skill for complete CSS variable reference.

```css
/* MyComponent.module.css */
.container {
  padding: var(--sqo-space-md);
  background-color: var(--rsd-color-primary-600);
  border-radius: var(--sqo-border-radius-1);
  box-shadow: var(--sqo-elevation-md);
}

.title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--rsd-component-text-color);
}
```

**Available via:**
- `packages/rubin-style-dictionary/dist/tokens.css` - Foundation tokens (prefix: `--rsd-*`)
- `packages/global-css/src/tokens.css` - Application tokens (prefix: `--sqo-*`)
- Import `@lsst-sqre/global-css` in your app to load all tokens

## Consuming Squared in Apps

Apps that use squared must configure transpilation.

### Next.js Configuration

**Required in `next.config.js`:**
```javascript
module.exports = {
  transpilePackages: ['@lsst-sqre/squared'],
  // ... other config
};
```

This tells Next.js to transpile the squared package's TypeScript source.

See [consuming-app-setup.md](consuming-app-setup.md) for complete setup guide.

### Without Transpilation Configuration

If you forget to add `transpilePackages`, you'll see errors like:
```
Module parse failed: Unexpected token
You may need an appropriate loader to handle this file type
```

## Testing Infrastructure

### Vitest with Two Projects

Squared uses vitest with two separate test projects:

1. **Unit tests** - Traditional vitest tests (`.test.ts` files)
2. **Storybook tests** - Tests in Storybook stories via addon-vitest

See the actual test configuration at `packages/squared/vitest.config.ts`.

### Running Tests

```bash
# Unit tests only
pnpm test --filter @lsst-sqre/squared

# Storybook tests only
pnpm test-storybook --filter @lsst-sqre/squared

# Storybook tests in watch mode
pnpm test-storybook:watch --filter @lsst-sqre/squared

# All tests (run from root)
pnpm test
pnpm test-storybook
```

### Test Setup

**Unit tests:**
- Setup file: `src/test-setup.ts`
- Environment: jsdom
- Globals: enabled
- CSS Modules: non-scoped classNameStrategy

**Storybook tests:**
- Browser: Playwright (chromium)
- Environment: browser + jsdom
- Setup file: `.storybook/vitest.setup.ts`

## Component Development

### TypeScript Patterns

**Prefer `type` over `interface`:**
```typescript
// ✅ Good
type MyComponentProps = {
  title: string;
  onClick?: () => void;
};

// ❌ Avoid (unless extending/merging needed)
interface MyComponentProps {
  title: string;
  onClick?: () => void;
}
```

**Avoid `React.FC` - type props directly:**
```typescript
// ✅ Good
export default function MyComponent({ title, onClick }: MyComponentProps) {
  return <div onClick={onClick}>{title}</div>;
}

// ❌ Avoid
const MyComponent: React.FC<MyComponentProps> = ({ title, onClick }) => {
  return <div onClick={onClick}>{title}</div>;
};
```

### Component Structure

```typescript
// MyComponent/MyComponent.tsx
import styles from './MyComponent.module.css';

type MyComponentProps = {
  title: string;
  variant?: 'primary' | 'secondary';
};

/**
 * Component description for documentation
 */
export default function MyComponent({
  title,
  variant = 'primary'
}: MyComponentProps) {
  return (
    <div className={styles.container} data-variant={variant}>
      <h2 className={styles.title}>{title}</h2>
    </div>
  );
}
```

### Export Pattern

```typescript
// MyComponent/index.ts
export { default } from './MyComponent';
export type { MyComponentProps } from './MyComponent';
```

```typescript
// src/index.ts
export { default as MyComponent } from './components/MyComponent';
export type { MyComponentProps } from './components/MyComponent';
```

## Dependencies

### Workspace Dependencies

Squared depends on other monorepo packages:
- `@lsst-sqre/global-css` - Global styles and design token application
- `@lsst-sqre/rubin-style-dictionary` - Design tokens
- `@lsst-sqre/eslint-config` - Linting configuration
- `@lsst-sqre/tsconfig` - TypeScript configuration

These use workspace protocol: `"@lsst-sqre/global-css": "workspace:*"`

### Key External Dependencies

- **React 19** - Component framework (peer dependency)
- **Radix UI** - Unstyled UI primitives
- **react-feather** - Icon library
- **Font Awesome** - Additional icons
- **date-fns** - Date manipulation
- **react-day-picker** - Date picker component

### Dev Dependencies

- **Next.js** - Required for type checking (peer dep)
- **Vitest** - Test runner
- **Storybook 9** - Component documentation
- **Testing Library** - React testing utilities
- **Playwright** - Browser testing (for Storybook tests)

## Storybook Integration

### Running Storybook

```bash
# Start Storybook dev server
pnpm storybook --filter @lsst-sqre/squared

# Build static Storybook
pnpm build-storybook --filter @lsst-sqre/squared
```

### Story Pattern

```typescript
// MyComponent.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import MyComponent from './MyComponent';

const meta: Meta<typeof MyComponent> = {
  title: 'Components/MyComponent',
  component: MyComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof MyComponent>;

export const Default: Story = {
  args: {
    title: 'Example Title',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    title: 'Example Title',
    variant: 'secondary',
  },
};
```

### Testing Stories

With `@storybook/addon-vitest`, stories can include tests:

```typescript
import { expect, within } from '@storybook/test';

export const WithTest: Story = {
  args: {
    title: 'Test Title',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await expect(canvas.getByText('Test Title')).toBeInTheDocument();
  },
};
```

Run with: `pnpm test-storybook --filter @lsst-sqre/squared`

## Creating New Components

### Manual Creation

1. Create component directory in `src/components/`
2. Add `.tsx`, `.module.css`, `.stories.tsx`, `.test.tsx` files
3. Create `index.ts` with exports
4. Export from `src/index.ts`
5. Import design tokens in CSS
6. Write Storybook stories
7. Write tests

## Troubleshooting

### Build Errors: "Unexpected token"

**Cause**: App not configured to transpile squared package.

**Solution**: Add to `next.config.js`:
```javascript
transpilePackages: ['@lsst-sqre/squared']
```

### CSS Module Styles Not Applying

**Cause**: CSS Module not imported or class name mismatch.

**Solution**:
1. Import: `import styles from './Component.module.css';`
2. Use: `className={styles.className}`
3. Check CSS file has `.className` defined

### Design Tokens Not Working

**Cause**: `@lsst-sqre/global-css` not imported in app.

**Solution**: Import in app's root layout/component:
```typescript
import '@lsst-sqre/global-css';
```

### TypeScript Errors in Consuming App

**Cause**: Type resolution issues with direct source imports.

**Solution**: Ensure consuming app's `tsconfig.json` includes squared source:
```json
{
  "include": ["src", "node_modules/@lsst-sqre/squared/src"]
}
```

### Tests Failing

**Unit tests:**
```bash
# Run specific test
pnpm test --filter @lsst-sqre/squared -- MyComponent.test.tsx

# Run in watch mode
pnpm test --filter @lsst-sqre/squared -- --watch
```

**Storybook tests:**
```bash
# Run in watch mode for debugging
pnpm test-storybook:watch --filter @lsst-sqre/squared

# Run specific story test
pnpm test-storybook --filter @lsst-sqre/squared -- --grep "MyComponent"
```

## Best Practices

1. **Always use CSS Modules** for styling
2. **Always use design tokens** (CSS variables) in styles
3. **Prefer `type` over `interface`** for props
4. **Avoid `React.FC`** - type props directly in function parameters
5. **Write Storybook stories** for all components
6. **Write tests** for components (unit or story tests)
7. **Use Radix UI** for accessible primitives when possible
8. **Document components** with JSDoc comments
9. **Export components and types** from `src/index.ts`
10. **Keep components focused** - one responsibility per component

## Related Files

- `packages/squared/package.json` - Package configuration
- `packages/squared/vitest.config.ts` - Test configuration
- [consuming-app-setup.md](consuming-app-setup.md) - App integration guide (in this skill)

## Related Skills

- **design-system** - Complete CSS variable and design token reference
- **component-creation** - Creating new components with CSS Modules
- **testing-infrastructure** - Testing patterns and tools

## Package Scripts

```bash
# Test commands
pnpm test                    # Unit tests
pnpm test-storybook          # Storybook tests
pnpm test-storybook:watch    # Watch mode

# Quality commands
pnpm lint                    # ESLint
pnpm type-check              # TypeScript checking

# Storybook commands
pnpm storybook               # Dev server
pnpm build-storybook         # Build static site

# Utility commands
pnpm clean                   # Clean caches
```

**Remember**: Always run from repository root with `--filter @lsst-sqre/squared` for proper Turborepo caching!
