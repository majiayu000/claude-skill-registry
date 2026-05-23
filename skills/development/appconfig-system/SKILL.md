---
name: appconfig-system
description: Expert guidance for working with the AppConfig runtime configuration system in squareone. Use this skill when implementing configuration loading, working with YAML config files, setting up new pages that need configuration, troubleshooting config hydration issues, or migrating from next/config patterns. Covers server-side loadAppConfig(), client-side useAppConfig(), MDX content loading, Sentry configuration injection, and Kubernetes ConfigMap patterns.
---

# AppConfig System

The squareone app uses a filesystem-based configuration system that replaces `next/config` for runtime configuration.

## Critical Rules

**NEVER use `next/config` or `getConfig()`** - The app has been migrated away from this pattern. Always use the AppConfig system instead.

## Configuration Architecture

### Configuration Files

- **`squareone.config.yaml`** - Public runtime configuration (accessible client-side)
- **`squareone.serverconfig.yaml`** - Server-only configuration (secrets, etc.)
- **`squareone.config.schema.json`** - JSON schema for public config validation
- **`squareone.serverconfig.schema.json`** - JSON schema for server config validation

See [reference/config-reference.md](reference/config-reference.md) for complete schema documentation.

### Key Modules

- **`src/lib/config/loader.ts`** - Server-side configuration and MDX loading
- **`src/contexts/AppConfigContext.tsx`** - React context for client-side access

## Server-Side Configuration Loading

### In getServerSideProps

Use `loadAppConfig()` to load configuration in `getServerSideProps`:

```typescript
import type { GetServerSideProps } from 'next';
import { loadAppConfig } from '../lib/config/loader';

export const getServerSideProps: GetServerSideProps = async () => {
  try {
    // Load app configuration
    const appConfig = await loadAppConfig();

    return {
      props: {
        appConfig, // Passed to page component and extracted by _app.tsx
      },
    };
  } catch (error) {
    throw error;
  }
};
```

See [templates/page-with-config.tsx](templates/page-with-config.tsx) for a complete example.

### Loading MDX Content

For pages that render MDX content, use `loadConfigAndMdx()`:

```typescript
import { loadConfigAndMdx } from '../lib/config/loader';
import { serialize } from 'next-mdx-remote/serialize';

export const getServerSideProps: GetServerSideProps = async () => {
  try {
    // Load both config and raw MDX content
    const { config: appConfig, mdxContent } = await loadConfigAndMdx('docs.mdx');

    // Serialize MDX for rendering
    const mdxSource = await serialize(mdxContent);

    return {
      props: {
        appConfig,
        mdxSource,
      },
    };
  } catch (error) {
    throw error;
  }
};
```

### MDX Directory Configuration

- **Development**: MDX files in `src/content/pages/` (relative path in config)
- **Production**: Configurable via `mdxDir` in YAML (absolute path for Kubernetes ConfigMaps)
- **Path resolution**: Automatic handling of relative vs absolute paths in loader

## Client-Side Configuration Access

### Using the useAppConfig Hook

Components access configuration via the `useAppConfig()` hook:

```typescript
import { useAppConfig } from '../contexts/AppConfigContext';

function MyComponent() {
  const config = useAppConfig();

  return (
    <div>
      <h1>{config.siteName}</h1>
      <p>Environment: {config.environmentName}</p>
      <a href={config.docsBaseUrl}>Documentation</a>
    </div>
  );
}
```

See [templates/component-with-config.tsx](templates/component-with-config.tsx) for a complete example.

### Requirements

- Component must be within `<AppConfigProvider>` (automatically set up in `_app.tsx`)
- Page must implement `getServerSideProps` to pass `appConfig` prop
- Hook throws error if used outside provider

## Sentry Configuration

### Server-Side (sentry.server.config.js)

Sentry configuration is loaded from environment variables and injected into AppConfig:

```javascript
// In loadAppConfig():
const sentryDsn = process.env.SENTRY_DSN;

const config = {
  ...publicConfig,
  ...serverConfig,
} as AppConfig;

// Only add sentryDsn if it's defined
if (sentryDsn) {
  config.sentryDsn = sentryDsn;
}
```

### Client-Side (instrumentation-client.js)

Sentry configuration is injected into the browser via `window.__SENTRY_CONFIG__` in `_document.tsx`.

**Critical requirement**: Pages MUST implement `getServerSideProps` to enable configuration injection. Statically rendered pages get the default configuration which disables client-side Sentry reporting.

## Configuration Schema and Validation

### Ajv-Based Validation

Configuration is validated using Ajv with:
- **Default values** - Schema defaults are applied automatically
- **Additional property removal** - Unknown properties are stripped
- **Type validation** - Ensures correct types for all fields

```typescript
const ajv = new Ajv({ useDefaults: true, removeAdditional: true });
const validate = ajv.compile(schema);

// Validation modifies the configuration data
const isValid = validate(data);

if (!isValid && validate.errors) {
  throw new Error(
    `Configuration validation failed: ${ajv.errorsText(validate.errors)}`
  );
}
```

### Environment Variable Override

Some configurations can be overridden via environment variables:

- `SQUAREONE_CONFIG_PATH` - Override public config file path
- `SQUAREONE_SERVER_CONFIG_PATH` - Override server config file path
- `SENTRY_DSN` - Sentry Data Source Name (injected at runtime)
- `SQUAREONE_ENABLE_CACHING` - Force caching in development

## Caching Behavior

### Production Caching

In production (`NODE_ENV === 'production'`), configuration and MDX content are cached:
- Config loaded once and cached module-level
- MDX content cached per-file
- Improves performance by avoiding repeated filesystem reads

### Development Mode

In development, caching is disabled by default:
- Allows editing config and MDX files without restart
- Can be enabled via `SQUAREONE_ENABLE_CACHING=true` for testing

## Kubernetes Deployment Pattern

### ConfigMap Mounting

Configuration files can be mounted as Kubernetes ConfigMaps:

```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: squareone-config
data:
  squareone.config.yaml: |
    siteName: 'Production Site'
    baseUrl: 'https://example.com'
    mdxDir: '/config/mdx'  # Absolute path to mounted MDX content
    # ... rest of config
```

```yaml
# Deployment
volumeMounts:
  - name: config
    mountPath: /app/squareone.config.yaml
    subPath: squareone.config.yaml
  - name: mdx-content
    mountPath: /config/mdx
```

### Path Handling

The loader automatically handles path resolution:
- **Relative path** (development): Resolved from `process.cwd()`
- **Absolute path** (production): Used as-is for ConfigMap mounts

## Key Benefits

- **Kubernetes-ready**: Configuration via ConfigMaps at runtime
- **No hydration issues**: No `next/config` or `getInitialProps` dependencies
- **Type-safe**: Full TypeScript support with `AppConfig` interface
- **Environment-agnostic**: Same system works in development and production
- **Content management**: MDX files separate from configuration, easier to edit

## Migration from next/config

If you encounter code using `next/config`:

**Old pattern (DO NOT USE):**
```typescript
import getConfig from 'next/config';

const { publicRuntimeConfig } = getConfig();
const siteName = publicRuntimeConfig.siteName;
```

**New pattern (USE THIS):**
```typescript
// In getServerSideProps
import { loadAppConfig } from '../lib/config/loader';
const appConfig = await loadAppConfig();

// In components
import { useAppConfig } from '../contexts/AppConfigContext';
const config = useAppConfig();
const siteName = config.siteName;
```

## Troubleshooting

### Error: "useAppConfig must be used within an AppConfigProvider"

**Cause**: Component is not wrapped in `AppConfigProvider` or page didn't implement `getServerSideProps`.

**Solution**:
1. Ensure page implements `getServerSideProps` with `loadAppConfig()`
2. Return `appConfig` in props
3. `_app.tsx` automatically wraps pages with `AppConfigProvider`

### Error: "Configuration validation failed"

**Cause**: YAML configuration doesn't match JSON schema.

**Solution**: Check schema in `squareone.config.schema.json` and ensure all required fields are present with correct types.

### MDX file not found error

**Cause**: `mdxDir` configuration doesn't point to correct location.

**Solution**:
- **Development**: Use relative path like `src/content/pages`
- **Production**: Use absolute path like `/config/mdx` (for ConfigMap mounts)

### Sentry not initializing on client

**Cause**: Page is statically rendered (no `getServerSideProps`).

**Solution**: Add `getServerSideProps` to the page to enable server-side rendering and configuration injection.

## API Routes

API routes can also access configuration:

```typescript
import type { NextApiRequest, NextApiResponse } from 'next';
import { loadAppConfig } from '../lib/config/loader';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const config = await loadAppConfig();

  // Use config...
  res.status(200).json({ siteName: config.siteName });
}
```

## Storybook Configuration

Storybook uses `AppConfigProvider` decorator with mock configuration:

```typescript
// .storybook/preview.tsx
import { AppConfigProvider } from '../src/contexts/AppConfigContext';

const mockConfig = {
  siteName: 'Storybook',
  // ... mock config values
};

export const decorators = [
  (Story) => (
    <AppConfigProvider config={mockConfig}>
      <Story />
    </AppConfigProvider>
  ),
];
```

This allows components using `useAppConfig()` to work in Storybook stories.

## Environment Variables Policy

**Avoid `NEXT_PUBLIC_` environment variables** for runtime config - use YAML files instead.

**Use environment variables only for**:
- Infrastructure concerns (Sentry DSN, database URLs)
- Build-time configuration
- Secrets that shouldn't be in version control

Runtime application configuration should be in YAML files so it can be managed via Kubernetes ConfigMaps without rebuilding the application.
