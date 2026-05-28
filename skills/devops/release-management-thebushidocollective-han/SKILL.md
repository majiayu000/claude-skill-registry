---
name: sentry-release-management
description: Use when managing Sentry releases, uploading source maps, or tracking deployments. Covers release health and commit association.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Sentry - Release Management

Manage releases, upload source maps, and track deployments.

## Creating Releases

### Using sentry-cli

```bash
# Create a new release
sentry-cli releases new "$VERSION"

# Associate commits
sentry-cli releases set-commits "$VERSION" --auto

# Finalize the release
sentry-cli releases finalize "$VERSION"
```

### In CI/CD

```yaml
# GitHub Actions
- name: Create Sentry Release
  uses: getsentry/action-release@v1
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
    SENTRY_ORG: your-org
    SENTRY_PROJECT: your-project
  with:
    environment: production
    version: ${{ github.sha }}
```

### GitLab CI

```yaml
release:
  stage: deploy
  script:
    - sentry-cli releases new "$CI_COMMIT_SHA"
    - sentry-cli releases set-commits "$CI_COMMIT_SHA" --auto
    - sentry-cli releases finalize "$CI_COMMIT_SHA"
    - sentry-cli releases deploys "$CI_COMMIT_SHA" new -e production
```

## Source Maps

### Upload Source Maps

```bash
# Upload source maps for a release
sentry-cli sourcemaps upload \
  --release="$VERSION" \
  --url-prefix="~/" \
  ./dist

# With validation
sentry-cli sourcemaps upload \
  --release="$VERSION" \
  --validate \
  ./dist
```

### Webpack Plugin

```javascript
// webpack.config.js
const { sentryWebpackPlugin } = require("@sentry/webpack-plugin");

module.exports = {
  devtool: "source-map",
  plugins: [
    sentryWebpackPlugin({
      org: "your-org",
      project: "your-project",
      authToken: process.env.SENTRY_AUTH_TOKEN,
      release: {
        name: process.env.RELEASE_VERSION,
      },
      sourcemaps: {
        assets: "./dist/**",
      },
    }),
  ],
};
```

### Vite Plugin

```typescript
// vite.config.ts
import { sentryVitePlugin } from "@sentry/vite-plugin";

export default defineConfig({
  build: {
    sourcemap: true,
  },
  plugins: [
    sentryVitePlugin({
      org: "your-org",
      project: "your-project",
      authToken: process.env.SENTRY_AUTH_TOKEN,
    }),
  ],
});
```

### Next.js

```javascript
// next.config.js
const { withSentryConfig } = require("@sentry/nextjs");

module.exports = withSentryConfig(nextConfig, {
  org: "your-org",
  project: "your-project",
  authToken: process.env.SENTRY_AUTH_TOKEN,
  silent: true,
  hideSourceMaps: true,
});
```

## Deployments

```bash
# Create a deployment
sentry-cli releases deploys "$VERSION" new \
  --env production \
  --started $(date +%s) \
  --finished $(date +%s)
```

## Release Health

### Track in SDK

```typescript
Sentry.init({
  dsn: "...",
  release: "my-app@1.2.3",
  environment: "production",
  autoSessionTracking: true,
});
```

### Metrics Tracked

- **Crash-Free Sessions**: Percentage of sessions without crashes
- **Crash-Free Users**: Percentage of users without crashes
- **Session Count**: Total sessions for the release
- **Adoption**: User adoption rate

## Configuration Files

### .sentryclirc

```ini
[defaults]
org = your-org
project = your-project

[auth]
token = your-auth-token
```

### sentry.properties

```properties
defaults.org=your-org
defaults.project=your-project
auth.token=your-auth-token
```

## Best Practices

1. Use semantic versioning for releases
2. Associate commits for suspect commits feature
3. Upload source maps before deploying
4. Create deployments to track where releases run
5. Monitor release health before full rollout
6. Delete old source maps to manage storage
7. Use CI/CD integration for automated releases

## Cleanup

```bash
# Delete old releases
sentry-cli releases delete "$OLD_VERSION"

# Delete source maps (keeps release)
sentry-cli releases files "$VERSION" delete --all
```
