---
name: magento-frontend
description: Build Magento 2 frontend — layout XML, blocks, PHTML templates, ViewModels, themes, JavaScript (RequireJS/KnockoutJS), and LESS/CSS. Use when customizing the storefront, building themes, or working with frontend components.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Frontend Development

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.adobe.com commerce frontend-core` for frontend development guide
2. Fetch `https://developer.adobe.com/commerce/frontend-core/guide/css/preprocess` for CSS/LESS docs
3. Web-search `site:developer.adobe.com commerce frontend-core guide layouts` for layout XML reference
4. Web-search `site:developer.adobe.com commerce frontend-core guide templates` for template guide

## Layout XML

### How Layouts Work

Layout files map to route handles and define the page structure:
- **Containers** — structural wrappers (header, content, footer)
- **Blocks** — content-rendering units tied to PHP classes and templates
- Handle naming: `<route>_<controller>_<action>.xml` (e.g., `catalog_product_view.xml`)
- `default.xml` — applies to all pages

### Key Layout Instructions

- `<referenceContainer>` — modify an existing container
- `<referenceBlock>` — modify an existing block
- `<block>` — add a new block with class, template, name
- `<move>` — relocate a block/container
- `<referenceBlock name="block_name" remove="true"/>` — remove a block (or use `<referenceContainer>` for containers). Note: there is no standalone `<remove>` element for blocks; the `remove="true"` attribute is set on `<referenceBlock>` or `<referenceContainer>`.
- `<update>` — include another layout handle
- `<arguments>` — pass data to blocks

### Layout Files Location

- Module: `view/frontend/layout/` or `view/adminhtml/layout/`
- Theme: `Magento_Module/layout/`

## Blocks and Templates

### Block Classes

- Extend `Magento\Framework\View\Element\Template`
- Contain data logic that templates consume
- `$block->someMethod()` in PHTML templates

### PHTML Templates

- Located in `view/frontend/templates/` or theme overrides
- PHP + HTML files with `.phtml` extension
- Access block: `$block`, escape output: `$escaper->escapeHtml()`

### ViewModels (Recommended)

MVVM pattern — inject ViewModels into blocks via layout XML arguments:
- ViewModels implement `Magento\Framework\View\Element\Block\ArgumentInterface`
- Keeps blocks thin; ViewModels carry the logic
- Access in template: `$viewModel = $block->getData('view_model');`

## JavaScript

### RequireJS

- AMD module system — all JS loaded as modules
- `requirejs-config.js` — maps module aliases, mixins, shims
- Located in `view/frontend/web/` or `view/frontend/requirejs-config.js`

### KnockoutJS

- Two-way data binding for dynamic UI
- Used extensively in checkout and UI components
- Custom bindings via `ko.bindingHandlers`
- HTML templates in `view/frontend/web/template/` (`.html` files)

### JS Mixins

Extend existing JS modules without overriding:
- Declared in `requirejs-config.js` under `config.mixins`
- Wrapper function receives original module and modifies it

### jQuery Widgets

Custom widgets extend `$.widget`:
- Initialized via `data-mage-init` attribute or `<script type="text/x-magento-init">`
- Configuration passed as JSON

## Themes

### Theme Structure

```
app/design/frontend/VendorName/theme-name/
├── etc/view.xml              # Image sizes, responsive breakpoints
├── registration.php          # Theme registration
├── theme.xml                 # Theme name, parent
├── composer.json
├── Magento_Module/           # Module overrides
│   ├── layout/               # Layout XML overrides
│   └── templates/            # Template overrides
├── web/
│   ├── css/source/           # LESS source files
│   ├── images/
│   └── js/
└── media/preview.jpg
```

### Theme Inheritance

Themes declare a parent in `theme.xml`. Fallback chain: current theme → parent theme → module views → framework. Override files by placing them in the same relative path.

### Hyva Themes (Modern Alternative)

Open source since late 2025. Replaces KnockoutJS + RequireJS + jQuery with **Alpine.js + Tailwind CSS**. Dramatically faster: ~5 requests vs ~230, ~0.4MB vs ~3MB page weight.

## LESS/CSS

- Default preprocessor: LESS
- `@magento_import` directive for theme fallback
- Variables in `_variables.less`, overridden per theme
- Server-side compilation for production, client-side for development

## Best Practices

- Use ViewModels instead of heavy block classes
- Override templates at the theme level, not module level (for customization)
- Use layout XML to add/move/remove blocks — avoid direct template editing of core
- Minimize JavaScript — prefer server-rendered HTML where possible
- Use `$escaper->escapeHtml()`, `escapeUrl()`, `escapeJs()` for XSS prevention
- Consider Hyva for new projects — dramatically better performance

Fetch the frontend development guide for exact layout XML schema, template escaping methods, and RequireJS configuration patterns before implementing.
