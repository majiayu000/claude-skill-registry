---
name: shopify-extensions
description: Guide for building and managing Shopify Extensions (Admin, Checkout, Theme, Post-purchase, etc.) using the latest Shopify CLI and APIs.
---

# Shopify Extensions Guide

This skill provides a comprehensive guide to building Shopify Extensions. Extensions allow you to integrate your app's functionality directly into Shopify's user interfaces (Admin, Checkout, Online Store, POS) and backend logic.

## 📚 Official References (Latest)

*   **App Extensions Overview:** [Shopify.dev - App Extensions](https://shopify.dev/docs/apps/build/app-extensions)
*   **List of All Extensions:** [Shopify.dev - Extension List](https://shopify.dev/docs/apps/build/app-extensions/list)
*   **Checkout UI Extensions:** [Shopify.dev - Checkout UI Extensions](https://shopify.dev/docs/api/checkout-ui-extensions)
*   **Admin UI Extensions:** [Shopify.dev - Admin UI Extensions](https://shopify.dev/docs/api/admin-extensions)
*   **Theme App Extensions:** [Shopify.dev - Theme App Extensions](https://shopify.dev/docs/apps/online-store/theme-app-extensions)
*   **Shopify Functions:** [Shopify.dev - Shopify Functions](https://shopify.dev/docs/api/functions)

## 🛠️ Prerequisites

*   **Shopify CLI:** Ensure you are using the latest version of Shopify CLI.
    ```bash
    npm install -g @shopify/cli@latest
    ```
*   **Shopify App:** Extensions must be part of a Shopify App.

## 🚀 Common Extension Types

### 1. Admin UI Extensions
Embed your app into the Shopify Admin interface.

*   **Action Extensions:** Add transactional workflows (modals) to resource pages (Orders, Products, Customers).
    *   *Usage:* "More actions" menu.
*   **Block Extensions:** Embed contextual information as cards directly on resource pages.
    *   *Usage:* Inline cards on Product/Order details.
*   **Configuration:** Defined in `shopify.extension.toml`.
    ```toml
    [[extensions]]
    type = "ui_extension"
    name = "product-action"
    handle = "product-action"
    
    [[extensions.targeting]]
    target = "admin.product-details.action.render"
    module = "./src/ActionExtension.jsx"
    ```

### 2. Checkout UI Extensions
Customize the checkout flow (requires Shopify Plus for some features).

*   **Targets:** Information, Shipping, Payment, Order Summary, Thank You Page, Order Status Page.
*   **Capabilities:**
    *   Show banners/upsells.
    *   Collect additional data (attributes).
    *   Validate input.
*   **UI Components:** Use Shopify's restricted component library (Banner, Button, TextField, etc.) for security and performance.
*   **Example Configuration:**
    ```toml
    [[extensions]]
    type = "ui_extension"
    name = "checkout-banner"
    handle = "checkout-banner"

    [[extensions.targeting]]
    target = "purchase.checkout.block.render"
    module = "./src/CheckoutBanner.jsx"
    ```

### 3. Theme App Extensions
Integrate with Online Store 2.0 themes without modifying theme code.

*   **App Blocks:** Reusable UI blocks merchants can add to templates.
*   **App Embed Blocks:** Floating elements or global scripts/styles (e.g., chat widgets).
*   **Assets:** CSS/JS files are scoped to the extension.

### 4. specialized Extensions
*   **Shopify Functions:** Backend logic for discounts, shipping, and payment methods (replaces Shopify Scripts).
*   **Post-Purchase Extensions:** Add pages *between* checkout and thank you page (e.g., one-click upsells).
*   **Web Pixels:** Securely subscribe to behavioral events for analytics.
*   **POS UI Extensions:** Custom tiles and modals for Shopify POS.


## 💻 CLI Extension Creation

The `shopify app generate extension` command is the primary way to create new extensions.

### Basic Usage
```bash
shopify app generate extension
```
This runs an interactive wizard where you select the extension type and name.

### Non-Interactive Usage (CI/CD or Scripts)
You can bypass prompts by providing flags:

```bash
shopify app generate extension --name "my-extension" --template <template_type> --flavor <flavor>
```

*   `--name`: The name of your extension.
*   `--template`: The type of extension to generate (e.g., `checkout_ui`, `product_subscription`, `theme_app_extension`).
*   `--flavor`: The language/framework to use (e.g., `react`, `typescript`, `vanilla-js`). *Note: Not all extensions support all flavors.*

### Examples

**Create a Checkout UI Extension (React):**
```bash
shopify app generate extension --template checkout_ui --name "checkout-upsell" --flavor react
```

**Create a Theme App Extension:**
```bash
shopify app generate extension --template theme_app_extension --name "trust-badges"
```

**Create a Shopify Function (Product Discount - Rust):**
```bash
shopify app generate extension --template product_discounts --name "volume-discount" --flavor rust
```

### Useful Flags
*   `--client-id <value>`: Explicitly link to a specific app Client ID.
*   `--path <path>`: Run the command in a specific directory.
*   `--reset`: Reset the project configuration.

## 📝 Development Workflow


1.  **Generate Extension:**
    ```bash
    shopify app generate extension
    ```
    Select the extension type from the list.

2.  **Develop:**
    *   Edit source files (React/JS/TS).
    *   Configure `shopify.extension.toml`.
    *   Use `shopify app dev` to preview.

3.  **Deploy:**
    ```bash
    shopify app deploy
    ```
    This publishes the extension version to Shopify Partners.

4.  **Publish:**
    *   Go to Partner Dashboard > App > Extensions.
    *   Publish the uploaded version.

## 💡 Best Practices

*   **Performance:** UI extensions run in a web worker (Checkout/Admin). Avoid heavy computations.
*   **Design:** Use Polaris components (Admin) or provided UI components (Checkout) to match Shopify's look and feel.
*   **API Usage:** Use the `useApi()` hook in React extensions to access valid APIs and data for the current context.
*   **Versioning:** Always test new extension versions in a development store before promoting to production.
