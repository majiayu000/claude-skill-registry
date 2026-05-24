---
name: wix-dashboard-page
description: Generates React-based dashboard pages for Wix sites using Wix Design System (WDS) components. Creates admin panels, data management interfaces, CRUD tables, forms, modals, and custom dashboard experiences that integrate with Wix Data collections and Dashboard APIs. Use when building admin interfaces, management pages, settings pages, CRUD operations, tables with sorting/filtering/pagination, forms, modals, toast notifications, or configuring embedded script parameters. Triggers: dashboard, admin, panel, manage, table, form, CRUD, create, read, update, delete, list, view, edit, data, collection, CMS, modal, toast, notification, settings, configuration, embedded script settings, popup settings, script parameters.
license: MIT
compatibility: Requires Wix CLI project with dashboard page extension support
metadata:
  author: wix
  version: "1.0.0"
  category: wix-extensions
---

# Wix Dashboard Page Builder

Creates full-featured dashboard page extensions for Wix CLI applications. Dashboard pages appear in the Wix site owner's dashboard and enable site administrators to manage data, configure settings, and perform administrative tasks.

## Non-Matching Intents

Do NOT use this skill for:

- **Site pages** (visitor-facing) → Use `wix-site-page`
- **Embedded widgets** (custom elements) → Use `wix-embedded-script`
- **Backend APIs** (HTTP functions) → Use `wix-backend-api`
- **Service plugins** (checkout, shipping SPIs) → Use `wix-service-plugin`

## Capabilities

### UI Components (Wix Design System)

**Layout:** `Page`, `Page.Content`, `Layout`, `Cell`, `Card`, `Box`

**Data Display:** `Table`, `TableToolbar`, `Text`, `Heading`, `Badge`, `EmptyState`

**Forms:** `FormField`, `Input`, `Dropdown`, `Checkbox`, `ToggleSwitch`, `DatePicker`, `RichTextInputArea`

**Actions:** `Button`, `Modal`, Toast notifications

See more in "Supported WDS Components" section.

### Data Operations (Wix Data SDK)

See [Wix Data Reference](references/WIX_DATA.md) for complete documentation.

**Summary:**

- Read: `items.query('Collection').filter/sort.limit.find()` → `{ items, totalCount, hasNext }`
- Write: `items.insert | update | remove`. Ensure collection permissions allow the action

**Query methods:** `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `between`, `contains`, `startsWith`, `endsWith`, `hasSome`, `hasAll`, `isEmpty`, `isNotEmpty`, `and`, `or`, `not`, `ascending`, `descending`, `limit`, `skip`, `include`

### Dashboard APIs

See [Dashboard API Reference](references/DASHBOARD_API.md) for complete documentation including all methods, page IDs, and examples.

**Key methods:**

- `dashboard.navigate()` - Navigate between dashboard pages
- `dashboard.observeState()` - Receive contextual state and environmental information
- `dashboard.showToast()` - Display toast notifications
- `dashboard.openModal()` - Open dashboard modal extensions
- `dashboard.navigateBack()` - Navigate back to previous page
- `dashboard.getPageUrl()` - Get full URL for a dashboard page
- `dashboard.openMediaManager()` - Open Wix Media Manager
- `dashboard.onBeforeUnload()` - Register beforeunload handler
- `dashboard.addSitePlugin()` - Add site plugin to slots
- `dashboard.setPageTitle()` - Set page title in browser tab
- `dashboard.onLayerStateChange()` - Handle foreground/background state changes

**Ecom Navigation:** See [Ecom Navigation Reference](references/ECOM_NAVIGATION.md) for ecom-specific navigation helpers.

### Embedded Script Configuration API

When building a dashboard page to configure an embedded script, see [Dynamic Parameters Reference](references/DYNAMIC_PARAMETERS.md) for complete implementation guide.

**Key points:**

- Use `embeddedScripts` from `@wix/app-management`
- Parameters are returned as strings - handle type conversions when loading
- All parameters must be saved as strings (convert booleans/numbers to strings)
- Use `withProviders` wrapper when dynamic parameters are present

## Files and Code Structure

Dashboard pages live under `src/dashboard/pages`. Each page has its own folder.

**File structure:**

- `src/dashboard/pages/<page>/page.tsx` — page component

**Key metadata fields:**

- `id` (string, GUID): Unique page ID used to register the page
- `title` (string): Used for browser tab and optional sidebar label
- `additionalRoutes` (string[], optional): Extra routes leading to this page
- `sidebar.disabled` (boolean, optional): Hide page from sidebar (default false)
- `sidebar.priority` (number, optional): Sidebar ordering; lower is higher priority
- `sidebar.whenActive.selectedPageId` (string, optional): Which page appears selected when this page is active
- `sidebar.whenActive.hideSidebar` (boolean, optional): Hide sidebar when this page is active

## WDS Provider Usage

Wrap your dashboard page component with WixDesignSystemProvider to enable WDS components and theming.

```typescript
import { WixDesignSystemProvider } from "@wix/design-system";
export default function () {
  return (
    <WixDesignSystemProvider>
      <Page>
        <Page.Header
          title="My Page"
          subtitle="This is a subtitle for your page"
        />
        <Page.Content>
          <EmptyState title="My Page" subtitle="Hello World!" theme="page" />
        </Page.Content>
      </Page>
    </WixDesignSystemProvider>
  );
}
```

**Note:** When using dynamic parameters, use the `withProviders` wrapper instead. See [Dynamic Parameters](references/DYNAMIC_PARAMETERS.md) for details.

## Supported WDS Components

Use ONLY these Wix Design System components. Do NOT use components from `@wix/wix-ui-icons-common` unless you know the correct import path and it's explicitly needed for icons.

**Supported components:** AutoComplete, Badge, Box, Button, IconButton, TextButton, Card, Card.Content, Card.Divider, Card.Header, Card.Subheader, Cell, Checkbox, ColorInput, CornerRadiusInput, CustomModalLayout, Divider, Dropdown, EmptyState, FormField, Heading, IconButton, Input, InputArea, Layout, Loader, MarketingLayout, MessageModalLayout, Modal, NestableList, NumberInput, Page, Page.Footer, Page.Header, Page.Section, RichTextInputArea, SectionHeader, SidePanel, Table, TableActionCell, TableListHeader, TableListItem, TableToolbar, TagList, Text, TextButton, TimeInput, Tooltip, ToggleSwitch

For detailed component information, see [WDS Components Reference](references/WDS_COMPONENTS.md).

### Querying Component Details

When you need detailed information about specific WDS components (descriptions, usage guidelines, feature examples, code snippets), use the shared query script:

```bash
# From the wix-dashboard-page directory:
node ../scripts/query-wds-components.js <component-name> [<component-name> ...]

# Examples:
node ../scripts/query-wds-components.js Button Card
node ../scripts/query-wds-components.js Page Page.Header Page.Content
node ../scripts/query-wds-components.js Table TableToolbar
```

The script reads from `../assets/wds-storybook.json` and outputs formatted component information including do's and don'ts, feature examples, and usage guidelines. This is especially useful when you need:

- Specific prop usage examples
- Best practices for component usage
- Feature-specific code examples
- Detailed component descriptions

See [WDS Components Reference](references/WDS_COMPONENTS.md) for more information about the query script and JSON structure.

## Hard Constraints

- Do NOT invent or assume new types, modules, functions, props, events, or imports.
- Use only entities explicitly present in the provided references or standard libraries already used in this project.
- If something is missing, call it out explicitly and provide a minimal TODO or clearly marked placeholder rather than creating it.
- Use ONLY WDS components that are explicitly listed in the supported components list above.
- Do NOT use components from @wix/wix-ui-icons-common unless you know the correct import path and it's explicitly needed for icons
- Always verify component availability before using it in your generated code
- If you need a component not in the list, use a basic HTML element or create a simple custom component instead

## Examples

### Data Management Table

**Request:** "Create a dashboard page to manage blog posts"

**Output:** Page with table displaying posts, search toolbar, add/edit/delete actions, empty state.

### Settings Form

**Request:** "Build a settings page for notification preferences"

**Output:** Page with form fields, save button with toast confirmation, unsaved changes warning.

### Order Management

**Request:** "Create an admin panel for customer orders"

**Output:** Page with orders table, status badges, filters, detail modal, status update actions.

### Embedded Script Configuration

**Request:** "Create a settings page for the coupon popup embedded script"

**Output:** Page with form fields for popup headline, coupon code, minimum cart value, and enable toggle. Uses `embeddedScripts` API to load/save parameters.

```typescript
// Key pattern for embedded script configuration pages
import { embeddedScripts } from "@wix/app-management";

// Load on mount
useEffect(() => {
  const load = async () => {
    const script = await embeddedScripts.getEmbeddedScript();
    const data = script.parameters || {};
    setOptions({
      headline: data.headline || "Default",
      enabled: data.enabled === "true",
      threshold: Number(data.threshold) || 0,
    });
  };
  load();
}, []);

// Save handler
const handleSave = async () => {
  await embeddedScripts.embedScript({
    parameters: {
      headline: options.headline,
      enabled: String(options.enabled),
      threshold: String(options.threshold),
    },
  });
  dashboard.showToast({ message: "Saved!", type: "success" });
};
```

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Page-Specific Extension File

Each dashboard page requires an `extensions.ts` file in its folder:

**File:** `src/dashboard/pages/<page-name>/extensions.ts`

```typescript
import { extensions } from "@wix/astro/builders";

export const dashboardpageMyPage = extensions.dashboardPage({
  id: "{{GENERATE_UUID}}",
  title: "My Page",
  routePath: "my-page",
  component: "./dashboard/pages/my-page/page.tsx",
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

| Property    | Type   | Description                                                                                          |
| ----------- | ------ | ---------------------------------------------------------------------------------------------------- |
| `id`        | string | Unique static UUID v4 (generate fresh - see note above)                                              |
| `title`     | string | Display title in dashboard sidebar                                                                   |
| `routePath` | string | URL path segment. Lowercase letters, numbers, dashes, and slashes only. Must NOT start with a slash. |
| `component` | string | Relative path to the page component (.tsx)                                                           |

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the page-specific extension file, you MUST read [../references/EXTENSIONS.md](../references/EXTENSIONS.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the dashboard page will not appear in the Wix dashboard.**

## Common Mistakes - Do NOT

**API confusion with other extension types:**

| WRONG (Embedded Script API) | CORRECT (Dashboard Page API) |
| --------------------------- | ---------------------------- |
| `name: "..."`               | `title: "..."`               |
| `source: "..."`             | `component: "..."`           |
| `route: "..."`              | `routePath: "..."`           |

Do NOT copy field names from embedded script or other extension registrations. Dashboard pages use `title`, `routePath`, and `component`.

## Code Quality Requirements

### TypeScript Quality Guidelines

- Generated code MUST compile with zero TypeScript errors under strict settings: strict, noImplicitAny, strictNullChecks, exactOptionalPropertyTypes, noUncheckedIndexedAccess
- Prefer type-narrowing and exhaustive logic over assertions; avoid non-null assertions (!) and unsafe casts (as any)
- Treat optional values, refs, and array indexing results as possibly undefined and handle them explicitly
- Use exhaustive checks for unions (e.g., switch with a never check) and return total values (no implicit undefined)
- Do NOT use // @ts-ignore or // @ts-expect-error; fix the types or add guards instead

### Core Principles

- Do NOT invent or assume new types, modules, functions, props, events, or imports
- NEVER use mocks, placeholders, or TODOs in any code
- ALWAYS implement complete, production-ready functionality
- Follow Wix dashboard page patterns and best practices precisely
- Handle all edge cases and error scenarios appropriately

### Code Quality Standards

- Prefer TypeScript with appropriate typing
- Use consistent naming conventions
- Include error handling where appropriate
- Add documentation for complex or non-obvious logic
- Prefer async/await for asynchronous operations
- Consider destructuring for cleaner code when beneficial
- Return well-structured response objects

### Error Handling

- Always implement proper error handling in dashboard pages
- Return appropriate error responses when data is invalid
- Log errors appropriately for debugging using console.error
- Handle network timeouts and external service failures

### Output Constraints

**Token limits:** Your max output is ~10,000 tokens. You MUST plan your response to stay well under this limit.

- If making a large file (>300 lines), split it into multiple smaller files with imports.
- If editing a large section (>100 lines), break it into multiple smaller edit operations.
- Count your output before responding - if it seems too long, reduce scope and prioritize.

**Brevity rules:** Minimize output tokens while maintaining quality and correctness.

- Do NOT add README.md, documentation files, or markdown files unless explicitly requested.
- Do NOT add excessive comments in code - only add comments where truly necessary for clarity.
- Do NOT re-output unchanged files or duplicate existing code.
- Do NOT generate placeholder code like "// TODO: implement" - provide working implementations.
- Only output files that are directly required for the task.

**Modular code strategy:** When generating substantial code, split into multiple smaller files with imports:

- Extract utilities/helpers into separate files
- Separate types/interfaces into dedicated type files
- Keep each component/function focused (~50-100 lines max)

## API Spec Support

When an API specification is provided, you can make API calls to those endpoints. See [API Spec Reference](references/API_SPEC.md) for details on how to use API specs in dashboard pages.
