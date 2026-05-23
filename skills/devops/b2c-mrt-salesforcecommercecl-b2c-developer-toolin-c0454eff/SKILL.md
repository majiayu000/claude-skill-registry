---
name: b2c-mrt
description: Using the b2c CLI for Managed Runtime (MRT) project and deployment management
---

# B2C MRT Skill

Use the `b2c` CLI plugin to manage Managed Runtime (MRT) projects and deployments for PWA Kit storefronts.

## Examples

### Push Bundle to Managed Runtime

```bash
# push a bundle to MRT for a specific project
b2c mrt push --project my-storefront

# push to a specific environment (staging, production, etc.)
b2c mrt push --project my-storefront --environment staging

# push to production with a release message
b2c mrt push --project my-storefront --environment production --message "Release v1.0.0"

# push from a custom build directory
b2c mrt push --project my-storefront --build-dir ./dist

# specify Node.js version for SSR runtime
b2c mrt push --project my-storefront --node-version 20.x

# add SSR parameters
b2c mrt push --project my-storefront --ssr-param SSRProxyPath=/api

# use JSON output for automation
b2c mrt push --project my-storefront --json
```

### Manage Environments

```bash
# create a new MRT environment
b2c mrt env create

# delete an MRT environment
b2c mrt env delete
```

### Environment Variables

```bash
# manage environment variables for an MRT environment
b2c mrt env var
```

### Configuration

MRT settings can be configured in `dw.json`:
- `mrtProject`: MRT project slug
- `mrtEnvironment`: MRT environment name (staging, production, etc.)

Environment variables:
- `SFCC_MRT_PROJECT`: MRT project slug
- `SFCC_MRT_ENVIRONMENT`: MRT environment
- `SFCC_MRT_API_KEY`: MRT API key

### More Commands

See `b2c mrt --help` for a full list of available commands and options in the `mrt` topic.
