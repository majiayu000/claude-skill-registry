---
name: storybook-config
description: "Generate and configure Storybook 10 for any framework with automatic detection, SOTA best practices, and platform-specific optimizations (Web, Tauri, Electron)"
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# Storybook Configuration Skill

## Overview

This skill generates production-ready Storybook 10 configurations with:
- Automatic framework detection (React, Vue, Svelte, Angular, Next.js, Solid, Lit)
- SOTA 2026 best practices
- Platform-specific optimizations (Tauri full support, Electron partial support)
- Optional visual generation integration
- Testing framework setup (Vitest + Playwright)

## When to Use This Skill

This skill should be used when:
- Initializing Storybook 10 in a new project
- Updating existing Storybook configuration to SOTA standards
- Adding framework-specific optimizations
- Configuring platform-specific setups (Tauri, Electron)
- Setting up testing infrastructure (interaction, a11y, visual)

## Quick Start

```bash
# Detect project framework and configuration
bash ${CLAUDE_PLUGIN_ROOT}/scripts/detect-framework.sh

# Use skill to generate configuration
# The skill will use AskUserQuestion for user preferences
```

## Configuration Generation

### Supported Frameworks

| Framework | Storybook Package | Minimum Version | Bundler |
|-----------|------------------|----------------|---------|
| React | `@storybook/react-vite` | 18.0.0 | Vite (preferred), Webpack |
| Vue | `@storybook/vue3-vite` | 3.0.0 | Vite (preferred), Webpack |
| Svelte | `@storybook/svelte-vite` | 5.0.0 | Vite |
| Angular | `@storybook/angular` | 18.0.0 | Webpack |
| Next.js | `@storybook/nextjs-vite` | 14.0.0 | Vite |
| Solid.js | `@storybook/solid-vite` | 1.8.0 | Vite |
| Lit | `@storybook/web-components-vite` | 3.0.0 | Vite |

### SOTA Patterns (2026)

**1. Vitest Integration for Testing**
```typescript
// main.ts - Enable Vitest addon
addons: [
  '@storybook/addon-vitest', // Real browser testing
]
```

**2. Accessibility Testing**
```typescript
// preview.ts - Configure axe-core
parameters: {
  a11y: {
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
        { id: 'button-name', enabled: true },
      ],
    },
  },
}
```

**3. Autodocs with Tags**
```typescript
// main.ts - Auto-generate documentation
docs: {
  autodocs: 'tag', // Stories with 'autodocs' tag get automatic docs
}

// story.tsx
export default {
  tags: ['autodocs'], // Enable automatic documentation
}
```

**4. Performance Optimization**
```typescript
// main.ts - Vite optimization
viteFinal: async (config) => {
  return {
    ...config,
    optimizeDeps: {
      include: ['@storybook/blocks'],
    },
  };
}

// Build optimization for CI
build: {
  test: {
    disabledAddons: ['@storybook/addon-docs'], // 2-4x faster
  },
}
```

**5. Modern Controls**
```typescript
// preview.ts - Enhanced controls
controls: {
  matchers: {
    color: /(background|color)$/i,
    date: /Date$/i,
  },
  expanded: true, // Show all controls by default
}
```

## Platform-Specific Configuration

### Web Projects (Full Support)

Standard configuration with all features:
- Interaction tests
- Accessibility tests
- Visual regression tests
- Code coverage

### Tauri Projects (Full Support)

Additional configuration:
```typescript
// preview.ts - Tauri IPC mocks
decorators: [
  (Story) => {
    if (typeof window !== 'undefined' && !window.__TAURI__) {
      window.__TAURI__ = tauriMocks;
    }
    return Story();
  },
]
```

**Best Practices:**
- Run Storybook on separate port (6006) from Tauri dev server (5173)
- Mock `window.__TAURI__` APIs in stories
- Keep UI components decoupled from IPC logic

### Electron Projects (Partial Support)

Webpack overrides required:
```typescript
// main.ts - Electron configuration
webpackFinal: async (config) => {
  config.target = 'web'; // Override electron-renderer
  config.externals = {}; // Clear Electron externals
  config.resolve.alias = {
    electron: false, // Mock electron module
  };
  return config;
}

// preview.ts - Electron preload API mocks
decorators: [
  (Story) => {
    if (typeof window !== 'undefined' && !window.api) {
      window.api = electronMocks;
    }
    return Story();
  },
]
```

**Limitations:**
- Only pure UI components fully testable
- Components with direct `electron` imports need refactoring
- IPC integration requires E2E tests separately

## Design System Integration

### Detected Design Systems

The skill detects and integrates with:
- **Material UI (MUI)** - Theme provider wrapper
- **Ant Design** - ConfigProvider wrapper
- **shadcn/ui** - Tailwind + Radix UI setup
- **Chakra UI** - ChakraProvider wrapper
- **Mantine** - MantineProvider wrapper

### Example: MUI Integration

```typescript
// preview.ts
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

export const decorators = [
  (Story) => (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Story />
    </ThemeProvider>
  ),
];
```

## Testing Configuration

### Interaction Tests (Play Functions)

```typescript
// Install dependencies
npm install --save-dev @testing-library/react @testing-library/user-event

// Enable addon
npx storybook@latest add @storybook/addon-vitest
```

### Accessibility Tests

```typescript
// Install addon
npx storybook@latest add @storybook/addon-a11y

// Configure in preview.ts
parameters: {
  a11y: {
    element: '#storybook-root',
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
      ],
    },
  },
}
```

### Coverage Reports

```typescript
// Install V8 coverage
npm install --save-dev @vitest/coverage-v8

// Run with coverage
npm run storybook:coverage
```

## Configuration Templates

### React with TypeScript (SOTA)

> **Storybook 10 Note:** `@storybook/addon-essentials` is deprecated and removed in Storybook 10.
> Essential features (actions, backgrounds, controls, viewport, measure, outline, toolbars) are now **built-in by default**.
> Only add addons for features NOT included in core (e.g., `@storybook/addon-a11y`, `@storybook/addon-vitest`).

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [
    // NOTE: addon-essentials is REMOVED in Storybook 10
    // Essential features (actions, backgrounds, controls, viewport) are now built-in
    '@storybook/addon-docs',   // Documentation (still separate)
    '@storybook/addon-vitest', // Real browser testing
    '@storybook/addon-a11y',   // Accessibility testing
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {
      strictMode: true,
    },
  },
  docs: {
    autodocs: 'tag',
  },
  viteFinal: async (config) => {
    return {
      ...config,
      optimizeDeps: {
        include: ['@storybook/blocks'],
      },
    };
  },
};

export default config;
```

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react-vite';
import '../src/index.css'; // Global styles

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
      expanded: true,
    },
    layout: 'centered',
    a11y: {
      config: {
        rules: [
          { id: 'color-contrast', enabled: true },
        ],
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
      ],
    },
  },
  globalTypes: {
    theme: {
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        title: 'Theme',
        icon: 'circlehollow',
        items: ['light', 'dark'],
        dynamicTitle: true,
      },
    },
  },
};

export default preview;
```

## Quality Checklist

Before completing configuration:
- [ ] Framework detected correctly
- [ ] Correct Storybook 10 packages installed
- [ ] Addons configured based on user preferences
- [ ] Theme/design system integrated (if applicable)
- [ ] Platform-specific setup complete (Tauri/Electron)
- [ ] Example stories generated
- [ ] package.json scripts added
- [ ] README created with setup instructions
- [ ] Tests run successfully

## Best Practices

### Do's
- Use Vite for faster builds (when possible)
- Enable autodocs with tags
- Configure a11y testing by default
- Optimize Vite dependencies
- Use V8 coverage (faster than Istanbul)
- Provide platform-specific guidance

### Don'ts
- Don't use Webpack unless required (Angular, legacy projects)
- Don't skip accessibility configuration
- Don't forget to add example stories
- Don't configure features user didn't select
- Don't assume all components work in Electron (document limitations)

## Integration with Other Skills

- **story-generation**: Use configuration to generate framework-specific stories
- **visual-design**: Use detected design system for visual generation
- **platform-support**: Apply platform-specific patterns (Tauri/Electron)
- **testing-suite**: Configure test infrastructure based on user selections
