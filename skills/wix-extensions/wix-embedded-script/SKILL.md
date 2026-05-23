---
name: wix-embedded-script
description: Creates embedded scripts for Wix sites that inject HTML/JavaScript code into the DOM. Used for analytics tracking, advertising pixels, third-party integrations, custom JavaScript functionality, and dynamic client-side behavior. Use when adding tracking code (Google Analytics, Hotjar, Mixpanel), advertising pixels (Facebook Pixel, Google Ads), chat widgets, custom popups/modals, cookie consent banners, or dynamic client-side features. Triggers: embed, script, inject, tracking, analytics, pixel, advertising, popup, modal, chat widget, third-party, integration, JavaScript, HTML, DOM, client-side, cookie, consent, head, body.
license: MIT
compatibility: Requires Wix CLI project with embedded script extension support
metadata:
  author: wix
  version: "1.0.0"
  category: wix-extensions
---

# Wix Embedded Script Builder

Creates embedded script extensions for Wix CLI applications. Embedded scripts are HTML code fragments that get injected into the DOM of Wix sites, enabling integration with third-party services, analytics tracking, advertising, and custom JavaScript functionality.

## Non-Matching Intents

Do NOT use this skill for:

- **Dashboard admin interfaces** → Use `wix-dashboard-page`
- **Database/collection schemas** → Use `wix-cms-collection`
- **Backend API endpoints** → Use `wix-backend-api`
- **Service plugins (eCommerce SPIs)** → Use `wix-service-plugin`
- **Custom site widgets with settings panel** → Use `wix-custom-element`

## Script Types

Embedded scripts must declare a type for consent management:

| Type          | Description                                      | Use Cases                               |
| ------------- | ------------------------------------------------ | --------------------------------------- |
| `ESSENTIAL`   | Core functionality crucial to site operation     | Authentication, security features       |
| `FUNCTIONAL`  | Remembers user choices to improve experience     | Language preferences, UI customization  |
| `ANALYTICS`   | Provides statistics on how visitors use the site | Google Analytics, Hotjar, Mixpanel      |
| `ADVERTISING` | Provides visitor data for marketing purposes     | Facebook Pixel, Google Ads, retargeting |

**Selection rule:** If a script falls into multiple types, choose the option closest to the bottom of the list (most restrictive). For example, a script with both Analytics and Advertising aspects should be typed as `ADVERTISING`.

## Placement Options

| Placement    | Description                              | Best For                          |
| ------------ | ---------------------------------------- | --------------------------------- |
| `HEAD`       | Between `<head>` and `</head>` tags      | Analytics, early initialization   |
| `BODY_START` | Immediately after opening `<body>` tag   | Critical functionality, noscript  |
| `BODY_END`   | Immediately before closing `</body>` tag | Non-blocking scripts, performance |

**Selection guidelines:**

- Analytics/tracking → `HEAD` (initialize early)
- Advertising pixels → `BODY_END` (non-blocking)
- Critical functionality → `HEAD` or `BODY_START`
- Non-critical features → `BODY_END` (better performance)

## Dynamic Parameters and Dashboard Configuration

**Every embedded script requires a companion dashboard page** to configure its parameters. Site owners use the dashboard page UI to set values, which are then passed to the embedded script as template variables.

### Architecture Flow

```
Dashboard Page (React UI)
    │
    │  embeddedScripts.embedScript({ parameters: {...} })
    ▼
Wix App Management API
    │
    │  Stores parameters, injects as template variables
    ▼
Embedded Script (HTML)
    │
    │  {{parameterKey}} → actual value
    ▼
Site DOM
```

**Related skill:** Use `wix-dashboard-page` to create the configuration UI for your embedded script.

### Parameter Types

| Type       | Description              | Dashboard Component    |
| ---------- | ------------------------ | ---------------------- |
| `TEXT`     | Single-line text         | Input                  |
| `NUMBER`   | Numeric value            | Input type="number"    |
| `BOOLEAN`  | True/false toggle        | ToggleSwitch, Checkbox |
| `IMAGE`    | Image from media manager | ImagePicker            |
| `DATE`     | Date only                | DatePicker             |
| `DATETIME` | Date with time           | DatePicker + TimeInput |
| `URL`      | URL with validation      | Input                  |
| `SELECT`   | Dropdown options         | Dropdown               |
| `COLOR`    | Color value              | ColorPicker            |

### Template Variable Syntax

Embedded scripts support parameterization using template variable syntax `{{variableName}}`. These parameters are configured through the dashboard and passed as template variables that should be used in your HTML/JavaScript code.

**Usage Instructions:**

1. **Template Variable Syntax:**

   - Use `{{parameterKey}}` syntax to insert parameter values into your HTML
   - Template variables work in HTML attributes
   - They will be replaced with actual values when the script is injected

2. **HTML Attributes (REQUIRED):**

   - Store ALL parameter values in data attributes on a configuration element
   - Template variables can ONLY be used here, not directly in JavaScript
   - Example: `<div id="config" data-headline="{{headline}}" data-text="{{text}}"></div>`

3. **JavaScript Access:**

   - JavaScript must read parameter values from the data attributes
   - Use `getAttribute()` or the `dataset` property
   - Examples:
     ```javascript
     const config = document.getElementById("config");
     const headline = config?.getAttribute("data-headline");
     // OR using dataset:
     const { headline, text } = config.dataset;
     ```

4. **Type Safety:**

   - Be aware of parameter types when using them in JavaScript
   - NUMBER types: convert with `Number()` or `parseInt()`
   - BOOLEAN types: compare with `'true'` or `'false'` strings
   - DATE/DATETIME: parse with `new Date()`

5. **Required vs Optional:**

   - Required parameters will always have values
   - Optional parameters may be empty - handle gracefully
   - Provide fallback values for optional parameters

6. **Relevant Parameter Usage:**
   - Only use dynamic parameters that are relevant to your current use case
   - Ignore parameters that don't apply to the functionality you're implementing
   - Each parameter you use should serve a clear purpose in the script's functionality
   - It's perfectly fine to not use all parameters if they're not applicable

**Example Patterns:**

**Pattern 1 - Configuration in Data Attributes:**

```html
<div
  id="script-config"
  data-api-key="{{apiKey}}"
  data-enabled="{{enabled}}"
  data-color="{{primaryColor}}"
></div>
<script>
  const config = document.getElementById("script-config");
  const apiKey = config.getAttribute("data-api-key");
  const enabled = config.getAttribute("data-enabled") === "true";
  const color = config.getAttribute("data-color");

  if (enabled && apiKey) {
    // Initialize with configuration
  }
</script>
```

**Pattern 2 - Using dataset Property:**

```html
<div
  id="script-config"
  data-headline="{{headline}}"
  data-message="{{message}}"
  data-image-url="{{imageUrl}}"
></div>
<script>
  const config = document.getElementById("script-config");
  const { headline, message, imageUrl } = config.dataset;

  // Use the variables in your script logic
  if (headline) {
    document.querySelector("#headline").textContent = headline;
  }
</script>
```

**Pattern 3 - Conditional Logic:**

```html
<div
  id="config"
  data-mode="{{activationMode}}"
  data-start="{{startDate}}"
  data-end="{{endDate}}"
></div>
<script>
  const config = document.getElementById("config");
  const mode = config.getAttribute("data-mode");

  if (mode === "timed") {
    const startDate = new Date(config.getAttribute("data-start"));
    const endDate = new Date(config.getAttribute("data-end"));
    const now = new Date();

    if (now >= startDate && now <= endDate) {
      // Show content
    }
  } else if (mode === "active") {
    // Show content immediately
  }
</script>
```

**Validation Requirements:**

- Only use dynamic parameters that are relevant to your specific use case
- Ignore parameters that don't apply to the functionality being implemented
- Template variables `{{parameterKey}}` must match the exact key names from the parameter definitions
- Handle both required and optional parameters appropriately
- Provide sensible default behavior when optional parameters are not set
- Ensure type-appropriate usage (don't use NUMBER parameters as strings without conversion)

### Common Parameters

Every embedded script should have at minimum an **enable/disable toggle** parameter:

| Parameter    | Type      | Purpose                              |
| ------------ | --------- | ------------------------------------ |
| `enabled`    | `BOOLEAN` | Allow site owner to activate/disable |
| `apiKey`     | `TEXT`    | Third-party service credentials      |
| `trackingId` | `TEXT`    | Analytics/pixel identifiers          |
| `headline`   | `TEXT`    | Customizable display text            |
| `color`      | `COLOR`   | UI customization                     |

## Output Structure

A complete embedded script implementation requires **two parts**:

### 1. Embedded Script Extension

```
src/site/embedded-scripts/
└── {script-name}/
    ├── embedded.html     # HTML/JavaScript code to inject
    └── extensions.ts     # Metadata (scriptType, placement)
```

### 2. Dashboard Configuration Page (Required)

```
src/dashboard/
├── withProviders.tsx     # WDS provider wrapper (required)
└── pages/
    └── {script-name}-settings/
        ├── extensions.ts  # Extension registration (REQUIRED)
        └── page.tsx       # Configuration UI using embeddedScripts API
```

**Note:** The dashboard page requires its own `extensions.ts` file. Without this file, the dashboard page will not appear in the Wix dashboard.

**WARNING:** The dashboard page uses DIFFERENT field names than embedded scripts:

- Dashboard pages use `title`, `routePath`, `component`
- Embedded scripts use `name`, `source`, `placement`, `scriptType`

Do NOT apply embedded script field names to dashboard page registrations.

**See `wix-dashboard-page` skill** for dashboard page implementation details and the extension registration pattern.

## Implementation Pattern

```html
<!-- Configuration element with template variables -->
<div id="my-config" data-api-key="{{apiKey}}" data-enabled="{{enabled}}"></div>

<!-- Container for dynamic content -->
<div id="my-container"></div>

<style>
  /* Scoped styles for the embedded content */
  #my-container {
    /* styles */
  }
</style>

<script type="module">
  // Get configuration from data attributes
  const config = document.getElementById("my-config");
  if (!config) throw new Error("Config element not found");

  const { apiKey, enabled } = config.dataset;

  // Exit early if disabled (use throw at module scope, not return)
  if (enabled !== "true") {
    throw new Error("Script disabled");
  }

  // Implement functionality in a named function (return is allowed here)
  async function initialize() {
    try {
      // Your implementation
    } catch (error) {
      console.error("Script error:", error);
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
</script>
```

## Examples

### Analytics Tracking

**Request:** "Add Google Analytics tracking to my site"

**Output:**

- Script type: `ANALYTICS`
- Placement: `HEAD`
- Template variables: `{{trackingId}}`
- Implements: gtag.js initialization, page view tracking

### Popup/Modal

**Request:** "Create a coupon popup that shows when cart value exceeds $50"

**Output:**

- Script type: `FUNCTIONAL`
- Placement: `BODY_END`
- Template variables: `{{couponCode}}`, `{{minimumCartValue}}`, `{{enablePopup}}`
- Implements: Cart value detection, popup display logic, localStorage for "don't show again"

### Third-Party Chat Widget

**Request:** "Integrate Intercom chat widget"

**Output:**

- Script type: `FUNCTIONAL`
- Placement: `BODY_END`
- Template variables: `{{appId}}`, `{{userEmail}}`, `{{userName}}`
- Implements: Intercom SDK initialization, user identification

## Best Practices

- **Always create a dashboard page:** Every embedded script needs a configuration UI
- **Include enable/disable toggle:** Let site owners control activation without removing the script
- **Performance:** Minimize impact - scripts should be lightweight and non-blocking
- **Security:** Avoid inline event handlers, validate data, escape user input
- **Error handling:** Fail silently when appropriate - don't break the site
- **Module scope early exits:** Use `throw new Error()` for early exits at module scope, not `return`. Rollup (used by Astro) doesn't allow `return` statements at module scope. Wrap main logic in a named async function where `return` is valid.
- **Type conversions:** Parameters are always strings - convert in JavaScript as needed
- **API calls:** Only create fetch() calls to /api/\* endpoints that exist in the API spec
- **Scoping:** Prefix CSS classes and IDs to avoid conflicts with site styles
- **Cleanup:** Remove event listeners and intervals when appropriate

## Complete Example: Coupon Popup

### 1. Define Parameters

```
Parameters for "cart-coupon-popup":
- couponCode (TEXT, required) - The coupon code to display
- popupHeadline (TEXT, required) - Headline text
- popupDescription (TEXT, required) - Description text
- minimumCartValue (NUMBER) - Minimum cart value to show popup
- enablePopup (BOOLEAN, required) - Enable/disable toggle
```

### 2. Embedded Script (`embedded.html`)

```html
<div
  id="popup-config"
  data-coupon-code="{{couponCode}}"
  data-popup-headline="{{popupHeadline}}"
  data-minimum-cart-value="{{minimumCartValue}}"
  data-enable-popup="{{enablePopup}}"
></div>
<div id="popup-container"></div>

<script type="module">
  // Get configuration from data attributes
  const config = document.getElementById("popup-config");
  if (!config) throw new Error("Config element not found");

  const { couponCode, popupHeadline, minimumCartValue, enablePopup } =
    config.dataset;

  // Exit early if disabled (use throw at module scope, not return)
  if (enablePopup !== "true") {
    throw new Error("Popup disabled");
  }

  // Main logic in a function (return is allowed here)
  async function initializePopup() {
    const minValue = Number(minimumCartValue) || 0;
    // ... popup implementation
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializePopup);
  } else {
    initializePopup();
  }
</script>
```

### 3. Dashboard Page (See `wix-dashboard-page` skill)

Uses `embeddedScripts` API from `@wix/app-management`:

```typescript
import { embeddedScripts } from "@wix/app-management";

// Load parameters
const script = await embeddedScripts.getEmbeddedScript();
const params = script.parameters; // { couponCode: "...", ... }

// Save parameters (all values must be strings)
await embeddedScripts.embedScript({
  parameters: {
    couponCode: "SAVE20",
    minimumCartValue: "50", // Number as string
    enablePopup: "true", // Boolean as string
  },
});
```

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Script-Specific Extension File

Each embedded script requires an `extensions.ts` file in its folder:

```typescript
import { extensions } from "@wix/astro/builders";

export const embeddedscriptMyScript = extensions.embeddedScript({
  id: "{{GENERATE_UUID}}",
  name: "My Script",
  source: "./site/embedded-scripts/my-script/embedded.html",
  placement: "BODY_END",
  scriptType: "FUNCTIONAL",
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

| Property     | Type   | Description                                           |
| ------------ | ------ | ----------------------------------------------------- |
| `id`         | string | Unique static UUID v4 (generate fresh)                |
| `name`       | string | Display name for the script                           |
| `source`     | string | Relative path to the HTML file                        |
| `placement`  | enum   | `HEAD`, `BODY_START`, or `BODY_END`                   |
| `scriptType` | enum   | `ESSENTIAL`, `FUNCTIONAL`, `ANALYTICS`, `ADVERTISING` |

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the script-specific extension file, you MUST read [../references/EXTENSIONS.md](../references/EXTENSIONS.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the embedded script will not be deployed to the site.**
