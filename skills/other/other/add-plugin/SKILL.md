---
name: add-plugin
description: Add and configure a Momentum CMS plugin in the monorepo
argument-hint: <plugin-name>
---

# Add Momentum CMS Plugin (Monorepo)

Add and configure a plugin in the Momentum CMS monorepo.

## Arguments

- `$ARGUMENTS` - Plugin name: "analytics", "otel", "event-bus", or a custom plugin path

## Important: Monorepo Context

In the monorepo, plugins are local packages under `libs/plugins/`. Collections are defined in `libs/example-config/src/collections/`. Both example apps (`example-angular`, `example-analog`) import from `@momentumcms/example-config`.

## Steps

1. Identify the plugin to add
2. Import the plugin factory in the app's `momentum.config.ts`
3. Configure the plugin and add to the `plugins` array
4. Run `nx run example-angular:generate` (or the relevant app target) to regenerate types and admin config
5. Restart the dev server

## Official Plugins (Local Packages)

### Analytics (`@momentumcms/plugins/analytics`)

Located at `libs/plugins/analytics/`. Adds event tracking, dashboards, and block-level analytics.

```typescript
// In apps/example-angular/src/momentum.config.ts
import { analyticsPlugin } from '@momentumcms/plugins/analytics';
import { eventBusPlugin } from '@momentumcms/plugins/core';

const events = eventBusPlugin();
const analytics = analyticsPlugin({
	trackCollections: true,
});

const config = defineMomentumConfig({
	// ...existing config
	plugins: [authPlugin, events, analytics],
});
```

**What it adds:**

- Analytics dashboard, content performance, tracking rules admin pages
- `TrackingRules` collection
- Block-level analytics fields injected via `modifyCollections`
- CRUD event tracking hooks
- Browser imports: `@momentumcms/plugins/analytics/admin-routes`, `@momentumcms/plugins/analytics/block-fields`

### OpenTelemetry (`@momentumcms/plugins/otel`)

Located at `libs/plugins/otel/`. Distributed tracing for all collection operations.

```typescript
import { otelPlugin } from '@momentumcms/plugins/otel';

const tracing = otelPlugin({ serviceName: 'momentum-cms' });

const config = defineMomentumConfig({
	plugins: [authPlugin, tracing],
});
```

### Event Bus (`@momentumcms/plugins/core`)

Located at `libs/plugins/core/`. Pub/sub for collection lifecycle events.

```typescript
import { eventBusPlugin } from '@momentumcms/plugins/core';

const events = eventBusPlugin();

const config = defineMomentumConfig({
	plugins: [authPlugin, events],
});
```

## After Adding a Plugin

```bash
nx run example-angular:generate    # Regenerate types and admin config
nx serve cms-admin                 # Restart dev server
```

## Creating a New Plugin

Create a new library under `libs/plugins/`:

```bash
nx generate @nx/js:library --name=my-plugin --directory=libs/plugins/my-plugin --tags="scope:lib,env:server"
```

Then implement the `MomentumPlugin` interface:

```typescript
// libs/plugins/my-plugin/src/lib/my-plugin.ts
import type { MomentumPlugin } from '@momentumcms/core';

export function myPlugin(config: MyConfig): MomentumPlugin {
	return {
		name: 'my-plugin',
		collections: [],
		adminRoutes: [],
		modifyCollections(collections) {},
		async onInit(context) {},
		async onReady(context) {},
		async onShutdown(context) {},
		browserImports: {
			// Optional: expose browser-safe imports for admin config generation
			adminRoutes: {
				path: '@momentumcms/plugins/my-plugin/admin-routes',
				exportName: 'myPluginAdminRoutes',
			},
		},
	};
}
```

Key files to reference:

- Plugin interface: `libs/core/src/lib/plugins.ts`
- Plugin runner: `libs/plugins/core/src/lib/plugin-runner.ts`
- Analytics plugin (full example): `libs/plugins/analytics/src/lib/analytics-plugin.ts`
- Writing a plugin guide: `docs/plugins/writing-a-plugin.md`
