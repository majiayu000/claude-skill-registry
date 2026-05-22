---
name: turbopack
description: Configures Turbopack as the default Rust-based bundler for Next.js with incremental compilation and webpack loader compatibility. Use when optimizing Next.js development builds, migrating from webpack, or configuring custom loaders.
---

# Turbopack

Incremental bundler written in Rust, built into Next.js for faster development builds.

## Quick Start

```bash
# Turbopack is default in Next.js 16+
next dev          # Uses Turbopack
next build        # Uses Turbopack

# Explicitly use webpack instead
next dev --webpack
next build --webpack
```

## Configuration

### next.config.ts (Next.js 16+)

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  turbopack: {
    // Custom loaders
    rules: {
      '*.svg': {
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
      '*.graphql': {
        loaders: ['graphql-tag/loader'],
        as: '*.js',
      },
    },

    // Resolve aliases
    resolveAlias: {
      '@': './src',
      '@components': './src/components',
      'lodash': 'lodash-es',
    },

    // File extensions
    resolveExtensions: ['.tsx', '.ts', '.jsx', '.js', '.json'],

    // Module ID strategy
    moduleIdStrategy: 'deterministic', // or 'named'
  },
};

export default nextConfig;
```

### Legacy Config (Next.js 15)

```typescript
// In experimental section
const nextConfig: NextConfig = {
  experimental: {
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
};
```

## Loader Configuration

### SVG as React Components

```typescript
turbopack: {
  rules: {
    '*.svg': {
      loaders: ['@svgr/webpack'],
      as: '*.js',
    },
  },
}
```

```tsx
import Logo from './logo.svg';

export default function Header() {
  return <Logo className="h-8 w-8" />;
}
```

### GraphQL

```typescript
turbopack: {
  rules: {
    '*.graphql': {
      loaders: ['graphql-tag/loader'],
      as: '*.js',
    },
    '*.gql': {
      loaders: ['graphql-tag/loader'],
      as: '*.js',
    },
  },
}
```

### YAML/TOML

```typescript
turbopack: {
  rules: {
    '*.yaml': {
      loaders: ['yaml-loader'],
      as: '*.js',
    },
    '*.toml': {
      loaders: ['toml-loader'],
      as: '*.js',
    },
  },
}
```

### Markdown

```typescript
turbopack: {
  rules: {
    '*.md': {
      loaders: ['raw-loader'],
      as: '*.js',
    },
    '*.mdx': {
      loaders: ['@mdx-js/loader'],
      as: '*.js',
    },
  },
}
```

### Loader Options

```typescript
turbopack: {
  rules: {
    '*.svg': {
      loaders: [
        {
          loader: '@svgr/webpack',
          options: {
            svgo: true,
            svgoConfig: {
              plugins: [{ name: 'removeViewBox', active: false }],
            },
            titleProp: true,
          },
        },
      ],
      as: '*.js',
    },
  },
}
```

## Resolve Configuration

### Path Aliases

```typescript
turbopack: {
  resolveAlias: {
    // Simple alias
    '@': './src',
    '@components': './src/components',
    '@lib': './src/lib',
    '@utils': './src/utils',

    // Package substitution
    'lodash': 'lodash-es',
    'react-native': 'react-native-web',

    // Conditional (use package.json exports)
    'package-name': './node_modules/package-name/esm/index.js',
  },
}
```

### Extensions

```typescript
turbopack: {
  // Order matters - first match wins
  resolveExtensions: [
    '.tsx',
    '.ts',
    '.jsx',
    '.js',
    '.mjs',
    '.json',
  ],
}
```

## Performance Comparison

| Feature | Turbopack | Webpack |
|---------|-----------|---------|
| Cold start | ~700x faster | Baseline |
| HMR updates | ~10x faster | Baseline |
| Memory usage | Lower | Higher |
| Incremental | Native | Limited |

## Supported Features

### Built-in Support

- TypeScript/TSX
- JavaScript/JSX
- CSS/CSS Modules
- Sass/SCSS
- PostCSS
- next/image optimization
- next/font
- Server Components
- App Router
- Pages Router
- Middleware

### Webpack Loader Compatibility

Many webpack loaders work with Turbopack:

```typescript
// Tested compatible loaders
'@svgr/webpack'
'graphql-tag/loader'
'yaml-loader'
'raw-loader'
'@mdx-js/loader'
'babel-loader'
'sass-loader'
```

## Migration from Webpack

### Check for Plugin Dependencies

```typescript
// webpack plugins are NOT supported
// This won't work with Turbopack:
webpack: (config) => {
  config.plugins.push(new SomeWebpackPlugin());
  return config;
}
```

Find Turbopack-compatible alternatives or use webpack:

```bash
next dev --webpack  # Keep using webpack if needed
```

### Replace Custom Webpack Config

```typescript
// Before (webpack)
webpack: (config) => {
  config.module.rules.push({
    test: /\.svg$/,
    use: ['@svgr/webpack'],
  });
  return config;
}

// After (Turbopack)
turbopack: {
  rules: {
    '*.svg': {
      loaders: ['@svgr/webpack'],
      as: '*.js',
    },
  },
}
```

## Troubleshooting

### Unsupported Loader

```bash
# Error: loader 'some-loader' is not supported
# Check if loader is compatible or use webpack fallback
next dev --webpack
```

### Memory Issues

```bash
# Increase Node.js memory limit
NODE_OPTIONS="--max-old-space-size=8192" next dev
```

### Cache Issues

```bash
# Clear Turbopack cache
rm -rf .next
next dev
```

## Alternative: Rspack

For projects with complex webpack configs:

```bash
npm install @next/rspack

# Use in next.config.ts
import { withRspack } from '@next/rspack';

export default withRspack({
  // Full webpack API compatibility
});
```

See [references/loaders.md](references/loaders.md) for complete loader compatibility and [references/migration.md](references/migration.md) for detailed migration guide.
