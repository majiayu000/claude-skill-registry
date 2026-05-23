---
name: grafana-plugin-scaffolding
description: Scaffold and automate Grafana plugin projects using @grafana/create-plugin. Use when creating panel plugins, data source plugins, app plugins, or backend plugins. Handles project scaffolding, Docker dev environment setup, and plugin configuration.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Grafana Plugin Scaffolding Skill

Automate Grafana plugin project creation using the official `@grafana/create-plugin` scaffolder. This skill handles project scaffolding, development environment setup, and initial configuration for all plugin types.

**Supported Grafana Version:** v12.x+ only

## Instructions

### Step 1: Verify Prerequisites

Before scaffolding, verify these tools are installed:

```bash
# Check Node.js (v18+ required)
node --version

# Check npm
npm --version

# Check Docker (optional, for local development)
docker --version
```

If prerequisites are missing, guide the user to install them:
- Node.js: https://nodejs.org/
- Docker Desktop: https://www.docker.com/products/docker-desktop/

### Step 2: Scaffold the Plugin

Use the official `@grafana/create-plugin` tool:

```bash
# Interactive scaffolding (recommended)
npx @grafana/create-plugin@latest

# The tool will prompt for:
# - Plugin type (panel, datasource, app, scenesapp)
# - Organization name (e.g., "myorg")
# - Plugin name (e.g., "my-panel")
# - Include backend? (y/n)
```

### Step 3: Navigate and Install Dependencies

```bash
# Navigate to the new plugin directory
cd <orgName>-<pluginName>-<pluginType>

# Install frontend dependencies
npm install

# Install backend dependencies (if backend plugin)
go mod tidy
```

### Step 4: Start Development Environment

**Option A: Docker with Hot-Reload (Recommended)**

The scaffolder generates a `docker-compose.yaml`. For enhanced development with file watching, use the template from `templates/docker-compose.yaml` which includes Docker Compose `develop` features.

```bash
# Start Grafana with file watching (Docker Compose v2.22.0+)
docker compose watch

# Or standard start without watching
docker compose up -d

# Access Grafana at http://localhost:3000
# Login: admin / admin
```

With `docker compose watch`:
- Frontend changes in `dist/` sync automatically (no restart)
- Backend binary changes (`gpx_*`) trigger container restart
- No manual rebuild-restart cycle needed

**Option B: Manual**

```bash
# Build and watch frontend
npm run dev

# Build backend (if applicable)
mage -v

# Configure Grafana to load unsigned plugins
# Add to grafana.ini: plugins.allow_loading_unsigned_plugins = <plugin-id>
```

### Step 5: Verify Plugin Installation

1. Open http://localhost:3000
2. Navigate to Administration > Plugins
3. Search for your plugin name
4. Verify it appears and can be added to dashboards

## Plugin Type Workflows

### Panel Plugin

```bash
npx @grafana/create-plugin@latest
# Select: panel
# Enter: organization name
# Enter: plugin name
# Backend: No (panels don't need backend)
```

Post-scaffolding:
1. Edit `src/components/SimplePanel.tsx` for visualization logic
2. Edit `src/types.ts` for panel options interface
3. Edit `src/module.ts` for option configuration

### Data Source Plugin (Frontend Only)

```bash
npx @grafana/create-plugin@latest
# Select: datasource
# Enter: organization name
# Enter: plugin name
# Backend: No
```

Post-scaffolding:
1. Edit `src/datasource.ts` for query logic
2. Edit `src/ConfigEditor.tsx` for connection settings
3. Edit `src/QueryEditor.tsx` for query builder UI

### Data Source Plugin (With Backend)

```bash
npx @grafana/create-plugin@latest
# Select: datasource
# Enter: organization name
# Enter: plugin name
# Backend: Yes
```

Post-scaffolding:
1. Edit `pkg/plugin/datasource.go` for Go query logic
2. Implement `QueryData` and `CheckHealth` methods
3. Build backend: `mage -v`

### App Plugin

```bash
npx @grafana/create-plugin@latest
# Select: app
# Enter: organization name
# Enter: plugin name
# Backend: Optional
```

Post-scaffolding:
1. Edit `src/pages/` for app pages
2. Update `plugin.json` includes for navigation
3. Add new pages as React components

## Development Commands

```bash
# Frontend development (watch mode)
npm run dev

# Frontend production build
npm run build

# Backend build (Go plugins)
mage -v

# Run unit tests
npm test

# Run E2E tests (requires Grafana running)
npx playwright test

# Lint code
npm run lint

# Type check
npm run typecheck
```

## E2E Testing

The `@grafana/create-plugin` scaffolder includes E2E testing setup with `@grafana/plugin-e2e` and Playwright.

```bash
# Install Playwright browsers
npx playwright install --with-deps chromium

# Start Grafana
docker compose up -d

# Run E2E tests
npx playwright test

# Run with UI mode (debugging)
npx playwright test --ui
```

See `references/e2e-testing.md` for comprehensive testing patterns, fixtures, and CI/CD setup.

## Best Practices

1. **Start Simple**: Begin with minimal functionality, then iterate
2. **Use Docker**: Consistent environment across team members
3. **Test Early**: Run tests frequently during development
4. **Type Safety**: Leverage TypeScript for all frontend code
5. **SDK Updates**: Keep `@grafana/data`, `@grafana/ui`, `@grafana/runtime` versions aligned

## Common Issues

### Plugin Not Appearing
- Check `plugin.json` has correct `id` field
- Verify Docker volume mounts correctly
- Ensure `npm run dev` completed without errors

### Backend Plugin Errors
- Run `mage -v` to rebuild Go code
- Check `plugin_start_linux_*` or `gpx_*` binaries exist in `dist/`
- Verify `plugin.json` has `"backend": true`

### Development Server Issues
- Clear browser cache
- Restart Docker: `docker compose down && docker compose up -d`
- Check Grafana logs: `docker compose logs grafana`

## Delegation

For complex architectural decisions, plugin design patterns, or troubleshooting, delegate to the `grafana-plugin-expert` agent which has access to current SDK documentation via Context7.
