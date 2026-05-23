---
name: workleap-squide
description: |
  Squide is a React modular application shell for Workleap web applications. Use this skill when:
  (1) Creating or modifying Squide host applications or modules
  (2) Registering routes, navigation items, or MSW request handlers
  (3) Working with FireflyRuntime, initializeFirefly, or AppRouter
  (4) Setting up integrations: TanStack Query, i18next, LaunchDarkly, Honeycomb, MSW, Storybook
  (5) Implementing deferred registrations or conditional navigation items
  (6) Fetching global public/protected data with usePublicDataQueries/useProtectedDataQueries
  (7) Using Squide hooks: useNavigationItems, useRenderedNavigationItems, useIsBootstrapping, useLogger, useEventBusListener, useEventBusDispatcher, useEnvironmentVariable, useFeatureFlag
  (8) Implementing error boundaries in modular applications
  (9) Questions about modular architecture patterns in React applications
---

# Squide Framework

Squide is a React modular application shell. Use only documented APIs.

## Core Concepts

### Runtime
The `FireflyRuntime` instance is the backbone of a Squide application. Never instantiate directly - use `initializeFirefly()`.

### Modular Registration
Modules register routes, navigation items, and MSW handlers via a registration function. Each module contributes its own configuration, assembled by the host at bootstrapping.

### Public vs Protected Routes
- Routes default to `protected` (rendered under `ProtectedRoutes` placeholder)
- Use `registerPublicRoute()` for public routes (rendered under `PublicRoutes` placeholder)
- Public routes only fetch public global data; protected routes fetch both public and protected data

### Deferred Registrations
Navigation items dependent on remote data or feature flags use two-phase registration:
1. First phase: Register static routes and navigation items
2. Second phase: Return a function from registration to defer navigation items

## Quick Reference

### Host Application Setup

```tsx
// host/src/index.tsx
import { createRoot } from "react-dom/client";
import { FireflyProvider, initializeFirefly } from "@squide/firefly";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { App } from "./App.tsx";
import { registerHost } from "./register.tsx";

const runtime = initializeFirefly({
    localModules: [registerHost]
});

const queryClient = new QueryClient();
const root = createRoot(document.getElementById("root")!);

root.render(
    <FireflyProvider runtime={runtime}>
        <QueryClientProvider client={queryClient}>
            <App />
        </QueryClientProvider>
    </FireflyProvider>
);
```

```tsx
// host/src/App.tsx
import { AppRouter, useIsBootstrapping } from "@squide/firefly";
import { createBrowserRouter, Outlet } from "react-router";
import { RouterProvider } from "react-router/dom";

function BootstrappingRoute() {
    if (useIsBootstrapping()) {
        return <div>Loading...</div>;
    }
    return <Outlet />;
}

export function App() {
    return (
        <AppRouter>
            {({ rootRoute, registeredRoutes, routerProviderProps }) => (
                <RouterProvider
                    router={createBrowserRouter([{
                        element: rootRoute,
                        children: [{
                            element: <BootstrappingRoute />,
                            children: registeredRoutes
                        }]
                    }])}
                    {...routerProviderProps}
                />
            )}
        </AppRouter>
    );
}
```

```tsx
// host/src/register.tsx
import { PublicRoutes, ProtectedRoutes, type ModuleRegisterFunction, type FireflyRuntime } from "@squide/firefly";
import { RootLayout } from "./RootLayout.tsx";

export const registerHost: ModuleRegisterFunction<FireflyRuntime> = runtime => {
    runtime.registerRoute({
        element: <RootLayout />,
        children: [PublicRoutes, ProtectedRoutes]
    }, { hoist: true });

    runtime.registerRoute({ index: true, element: <HomePage /> });
    runtime.registerPublicRoute({ path: "*", element: <NotFoundPage /> });
};
```

### Local Module Setup

```tsx
// local-module/src/register.tsx
import type { ModuleRegisterFunction, FireflyRuntime } from "@squide/firefly";
import { Page } from "./Page.tsx";

export const register: ModuleRegisterFunction<FireflyRuntime> = runtime => {
    runtime.registerRoute({
        path: "/page",
        element: <Page />
    });

    runtime.registerNavigationItem({
        $id: "page",
        $label: "Page",
        to: "/page"
    });
};
```

### Navigation Rendering

**Important:** `RenderItemFunction` signature is `(item, key, index, level) => ReactNode` and `RenderSectionFunction` is `(elements, key, index, level) => ReactNode`. These signatures are fixed and do not accept custom context parameters, but there could be fewer arguments. Use closures to access external values.

```tsx
import { Link, Outlet } from "react-router";
import {
    useNavigationItems, useRenderedNavigationItems, isNavigationLink,
    type RenderItemFunction, type RenderSectionFunction
} from "@squide/firefly";

// Signature: (item, key, index, level) => ReactNode
const renderItem: RenderItemFunction = (item, key, index, level) => {
    if (!isNavigationLink(item)) return null;
    const { label, linkProps, additionalProps } = item;
    return (
        <li key={key}>
            <Link {...linkProps} {...additionalProps}>{label}</Link>
        </li>
    );
};

// Signature: (elements, key, index, level) => ReactNode
const renderSection: RenderSectionFunction = (elements, key, index, level) => (
    <ul key={key}>{elements}</ul>
);

export function RootLayout() {
    const navigationItems = useNavigationItems();
    const navigationElements = useRenderedNavigationItems(navigationItems, renderItem, renderSection);
    return (
        <>
            <nav>{navigationElements}</nav>
            <Outlet />
        </>
    );
}
```

### Global Data Fetching

```tsx
// Protected data
import { useProtectedDataQueries, useIsBootstrapping, AppRouter } from "@squide/firefly";

function BootstrappingRoute() {
    const [session] = useProtectedDataQueries([{
        queryKey: ["/api/session"],
        queryFn: async () => {
            const response = await fetch("/api/session");
            if (!response.ok) throw new ApiError(response.status);
            return response.json();
        }
    }], error => isApiError(error) && error.status === 401);

    if (useIsBootstrapping()) return <div>Loading...</div>;

    return (
        <SessionContext.Provider value={session}>
            <Outlet />
        </SessionContext.Provider>
    );
}

// In App component, set waitForProtectedData
<AppRouter waitForProtectedData>...</AppRouter>
```

```tsx
// Public data
const [data] = usePublicDataQueries([{ queryKey: [...], queryFn: ... }]);
<AppRouter waitForPublicData>...</AppRouter>
```

### Deferred Navigation Items

```tsx
export const register: ModuleRegisterFunction<FireflyRuntime, unknown, DeferredRegistrationData> = runtime => {
    // Always register routes
    runtime.registerRoute({ path: "/feature", element: <FeaturePage /> });

    // Return function for deferred navigation items
    return (deferredRuntime, { userData }) => {
        if (userData.isAdmin && deferredRuntime.getFeatureFlag("enable-feature")) {
            deferredRuntime.registerNavigationItem({
                $id: "feature",
                $label: "Feature",
                to: "/feature"
            });
        }
    };
};
```

```tsx
// Execute deferred registrations in BootstrappingRoute
const data = useMemo(() => ({ userData }), [userData]);
useDeferredRegistrations(data);
```

### MSW Request Handlers

```tsx
export const register: ModuleRegisterFunction<FireflyRuntime> = async runtime => {
    if (runtime.isMswEnabled) {
        const requestHandlers = (await import("../mocks/handlers.ts")).requestHandlers;
        runtime.registerRequestHandlers(requestHandlers);
    }
};
```

### Event Bus

```tsx
// Listen
import { useEventBusListener } from "@squide/firefly";
const handleEvent = useCallback((data, context) => { /* ... */ }, []);
useEventBusListener("event-name", handleEvent);

// Dispatch
import { useEventBusDispatcher } from "@squide/firefly";
const dispatch = useEventBusDispatcher();
dispatch("event-name", payload);
```

### Environment Variables

```tsx
// Register at initialization
const runtime = initializeFirefly({
    environmentVariables: { apiBaseUrl: "https://api.example.com" }
});

// Or register in module
runtime.registerEnvironmentVariable("key", "value");

// Use
import { useEnvironmentVariable } from "@squide/firefly";
const apiUrl = useEnvironmentVariable("apiBaseUrl");
```

### Feature Flags

```tsx
// Initialize with LaunchDarkly
import { initialize as initializeLaunchDarkly } from "launchdarkly-js-client-sdk";

const ldClient = initializeLaunchDarkly("client-id", { kind: "user", anonymous: true }, { streaming: true });
await ldClient.waitForInitialization(5);

const runtime = initializeFirefly({ launchDarklyClient: ldClient });

// Use
import { useFeatureFlag } from "@squide/firefly";
const isEnabled = useFeatureFlag("feature-key", defaultValue);
```

### Logging

```tsx
import { useLogger } from "@squide/firefly";
const logger = useLogger();
logger.debug("Message");
```

### Error Boundaries

```tsx
// Root error boundary (wraps everything)
runtime.registerRoute({
    errorElement: <RootErrorBoundary />,
    children: [{
        element: <RootLayout />,
        children: [PublicRoutes, ProtectedRoutes]
    }]
}, { hoist: true });

// Module error boundary (isolates module failures)
runtime.registerRoute({
    element: <RootLayout />,
    children: [{
        errorElement: <ModuleErrorBoundary />,
        children: [PublicRoutes, ProtectedRoutes]
    }]
}, { hoist: true });
```

## API Quick Reference

### initializeFirefly Options
- `mode`: `"development"` | `"production"`
- `localModules`: Array of registration functions
- `context`: Object passed to registration functions
- `useMsw`: Enable MSW support
- `startMsw`: Function to start MSW
- `environmentVariables`: Initial environment variables
- `honeycombInstrumentationClient`: For tracing
- `launchDarklyClient`: For feature flags
- `loggers`: Array of logger instances
- `plugins`: Array of plugin factory functions
- `onError`: Error handler for bootstrapping errors

### Route Registration Options
- `hoist`: Register at router root (bypasses layouts/auth)
- `parentPath`: Nest under route with matching `path`
- `parentId`: Nest under route with matching `$id`

### Route Properties
- `$id`: Identifier for nesting
- `$visibility`: `"public"` | `"protected"` (default)

### Navigation Item Properties
- `$id`: Unique identifier (recommended for stable keys)
- `$label`: Text or ReactNode
- `$priority`: Sorting priority (higher = first)
- `$canRender`: Conditional render function
- `$additionalProps`: Custom props for renderer
- `to`: Route path (supports dynamic segments like `/user/:id`)
- `style`: Inline styles for the navigation item
- `target`: Link target (e.g., `"_blank"` to open in new tab)

### Navigation Registration Options
- `menuId`: Target a specific menu (default: `"root"`)
- `sectionId`: Nest under section with matching `$id`

### AppRouter Props
- `waitForPublicData`: Delay until public data ready
- `waitForProtectedData`: Delay until protected data ready

### Hooks
- `useNavigationItems(options?)`: Get navigation items
- `useRenderedNavigationItems(items, renderItem, renderSection)`: Render nav items
- `useIsBootstrapping()`: Check if bootstrapping
- `usePublicDataQueries(queries)`: Fetch public global data
- `usePublicDataHandler(handler)`: Execute handler when modules are ready
- `useProtectedDataQueries(queries, isUnauthorizedError)`: Fetch protected data
- `useProtectedDataHandler(handler)`: Execute handler when modules ready and route is protected
- `useDeferredRegistrations(data?, options?)`: Execute deferred registrations (options: `{ onError? }`)
- `useEventBusListener(event, handler, options?)`: Listen to events
- `useEventBusDispatcher()`: Get dispatch function
- `useLogger()`: Get logger instance
- `useEnvironmentVariable(key)`: Get env variable
- `useEnvironmentVariables()`: Get all env variables
- `useFeatureFlag(key, defaultValue)`: Get feature flag
- `useFeatureFlags()`: Get all feature flags (memoized, only changes when flags update)
- `useLaunchDarklyClient()`: Get LaunchDarkly client instance
- `usePlugin(name)`: Get plugin instance
- `useRuntime()`: Get runtime instance
- `useRuntimeMode()`: Get runtime mode
- `useRoutes()`: Get registered routes
- `useIsRouteProtected(route)`: Check if a route is protected
- `useRouteMatch(locationArg, options?)`: Match route against location

### i18next Hooks (from `@squide/i18next`)
- `useI18nextInstance(key)`: Get a registered i18next instance by key
- `useCurrentLanguage()`: Get current language
- `useChangeLanguage()`: Get function to change language

### Helper Functions
- `isNavigationLink(item)`: Type guard for navigation links
- `isGlobalDataQueriesError(error)`: Type guard for query errors
- `resolveRouteSegments(path, params)`: Resolve dynamic segments
- `getFeatureFlag(client, key, defaultValue)`: Get flag in non-React code
- `mergeDeferredRegistrations(candidates)`: Merge multiple deferred registration functions
- `isEditableLaunchDarklyClient(client)`: Check if LaunchDarkly client supports runtime flag modification

### LaunchDarkly Utilities
- `LaunchDarklyPlugin`: Plugin for LaunchDarkly integration
- `FeatureFlags`: TypeScript interface for type-safe feature flags (augmentable)
- `FeatureFlagSetSnapshot`: Memoized snapshot of feature flags with change listeners
- `InMemoryLaunchDarklyClient`: In-memory client for testing
- `createLocalStorageLaunchDarklyClient(defaultValues, options?)`: Client that persists flags to localStorage (options: `{ localStorageKey?, context?, notifier? }`)

For detailed API documentation, see the references folder.

## Skill Maintenance Notes

When updating this skill from the official documentation, verify these common pitfalls:

1. **`useRenderedNavigationItems` function signatures**: Must always be `(item, key, index, level)` and `(elements, key, index, level)`. These do NOT accept custom context parameters. If external values are needed (route params, location, etc.), use closures or React hooks - never suggest adding parameters to these functions.

2. **Active state styling**: Use React Router's `NavLink` and its `isActive` argument provided to the `className`/`style` render functions (for example, `className={({ isActive }) => ... }`). Do not suggest passing location/pathname as a context parameter.

3. **Dynamic route segments**: Use the `resolveRouteSegments` helper with closures to capture values like `userId`. Example pattern: create a higher-order function that returns a `RenderItemFunction`.
