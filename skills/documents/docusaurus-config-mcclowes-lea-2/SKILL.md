---
name: docusaurus-config
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when working with docusaurus.config.js/ts files to validate or modify Docusaurus configuration
---

# Docusaurus Config

## Quick Start

Configuration lives in `docusaurus.config.js` or `docusaurus.config.ts` at project root.

```typescript
import { Config } from '@docusaurus/types';

const config: Config = {
  title: 'My Site', // Required
  url: 'https://example.com', // Required, no trailing /
  baseUrl: '/', // Required, must start and end with /

  favicon: 'img/favicon.ico',
  organizationName: 'my-org',
  projectName: 'my-project',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        /* options */
      },
    ],
  ],
  themeConfig: {
    /* theme config */
  },
  customFields: {
    /* unknown fields go here */
  },
};

export default config;
```

## Core Principles

- **Required**: `title`, `url`, `baseUrl` are mandatory
- **Custom fields**: Unknown fields must use `customFields` object
- **Validation**: `url` no trailing slash, `baseUrl` must be `/path/`
- **Plugins/themes**: Use string or `[name, options]` array format

## Common Tasks

**Before editing**: Read current config to preserve format (JS/TS, ESM/CommonJS)

**After editing**: Verify required fields, URL formats, and restart dev server

## Reference Files

See [references/detailed-guide.md](references/detailed-guide.md) for comprehensive examples
