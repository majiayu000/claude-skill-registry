---
name: shopify-app-bridge
description: Guide for using Shopify App Bridge to embed apps in the Shopify Admin. Use this skill when the user needs to interact with the host interface (Admin), show toasts, modals, resource pickers, or handle navigation within a Shopify embedded app.
---

# Shopify App Bridge Skill

Shopify App Bridge is a library that allows you to embed your app directly inside the Shopify Admin. It provides a way to communicate with the host environment to trigger actions and navigation.

> [!NOTE]
> This skill focuses on **Shopify App Bridge v3 (NPM package)** and **App Bridge CDN (v4)** patterns. ALWAYS check which version the project is using. The latest standard is often typically App Bridge v4 (CDN-based / `overview` script) but many React apps still use `@shopify/app-bridge-react` (v3/v4 wrapper).

## Core Concepts

-   **Host**: The Shopify Admin (web or mobile).
-   **Client**: Your embedded app.
-   **Actions**: Messages sent to the host to trigger UI elements (Toast, Modal) or navigation.

## Setup & Initialization

### Using CDN (App Bridge v4 - Recommended)

In modern Shopify apps, the preferred method is using the CDN script. This automatically exposes the `shopify` global variable, which is the primary entry point for all actions.

```html
<script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
<script>
  shopify.config = {
    apiKey: 'YOUR_API_KEY',
    host: new URLSearchParams(location.search).get("host"),
    forceRedirect: true,
  };
</script>
```

### debugging & Exploration

Once initialized, the `shopify` global variable is available in your browser console.

> [!TIP]
> **Explore functionality**:
> 1. Open Chrome Developer Console in the Shopify Admin.
> 2. Switch the frame context to your app's iframe.
> 3. Type `shopify` to see all available methods and configurations.

### Using `@shopify/app-bridge-react` (Legacy/Specific Use Cases)

If you are strictly using React components or need the Provider context for deeply nested legacy components:

```jsx
import { Provider } from '@shopify/app-bridge-react';
// ... configuration setup
```

## Common Actions

### Toast

Display a temporary success or error message.

```javascript
shopify.toast.show('Product saved');
```

### Modal

Open a modal dialog.

```javascript
const modal = await shopify.modal.show({
  title: 'My Modal',
  message: 'Hello world',
  footer: {
    buttons: [
      { label: 'Ok', primary: true, id: 'ok-btn' }
    ]
  }
});

modal.addEventListener('action', (event) => {
    if (event.detail.id === 'ok-btn') {
        modal.hide();
    }
});
```

### Resource Picker

Select products, collections, or variants.

**Simple Selection**
```javascript
const selected = await shopify.resourcePicker({
  type: 'product', // 'product', 'variant', 'collection'
  multiple: true,
});
```

**Pre-selected Resources**
Useful for editing existing selections.
```javascript
const selected = await shopify.resourcePicker({
  type: 'product',
  selectionIds: [
    { id: 'gid://shopify/Product/12345', variants: [{ id: 'gid://shopify/ProductVariant/67890' }] }
  ]
});
```

**Filtered Selection**
Filter by query or status.
```javascript
const selected = await shopify.resourcePicker({
  type: 'product',
  filter: {
    query: 'Sweater', // Initial search query
    variants: false, // Hide variants
    draft: false,   // Hide draft products
  }
});
```

**Handling Selection**
```javascript
if (selected) {
    console.log(selected);
    // Returns array of selected resources
} else {
    console.log('User cancelled picker');
}
```

### Navigation / Redirect

Navigate within the Shopify Admin.

```javascript
// Redirect to Admin Section
open('shopify:admin/products', '_top');

// Redirect to internal app route
open('shopify:app/my-route', '_top');
```

### Contextual Save Bar

Show a save bar when the user has unsaved changes.

```javascript
shopify.saveBar.show();

shopify.saveBar.addEventListener('save', async () => {
    // Perform save...
    shopify.saveBar.hide();
    shopify.toast.show('Saved');
});

shopify.saveBar.addEventListener('discard', () => {
    shopify.saveBar.hide();
});
```

## Best Practices

> [!IMPORTANT]
> **Authentication**: Ensure your app handles the OAuth flow and generates a session token. Requests to your backend MUST include the session token (Bearer token) if you rely on Shopify authentication. App Bridge handles fetching this token automatically in many configurations.

> [!TIP]
> **Navigation**: When building a Remix app, use the `@shopify/shopify-app-remix` helpers to handle headers and bridging automatically where possible.

> [!WARNING]
> **Host Parameter**: The `host` parameter is CRITICAL for App Bridge to work. It must be present in the URL or passed to the config. It is a base64 encoded string provided by Shopify.

## References

- [Modal Max](./references/modal-max.md) - Full-screen modal dialogs for complex multi-step flows, editors, and wizards
- [Save Bar](./references/save-bar.md) - Contextual save bar for indicating unsaved form changes
