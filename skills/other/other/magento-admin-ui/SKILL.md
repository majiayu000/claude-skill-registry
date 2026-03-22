---
name: magento-admin-ui
description: Build Magento 2 admin interfaces — UI component grids, forms, system configuration, ACL, and admin controllers. Use when creating admin panels, data grids, edit forms, or system settings.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Admin UI & System Configuration

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.adobe.com/commerce/php/development/components/add-admin-grid/` for admin grid tutorial
2. Fetch `https://developer.adobe.com/commerce/php/tutorials/backend/create-access-control-list-rule/` for ACL tutorial
3. Web-search `site:developer.adobe.com commerce php development components ui-components` for UI component reference

## Admin Grids (UI Component Listings)

### How Admin Grids Work

Grids are XML-declared UI components backed by data providers. They render in the browser using KnockoutJS and load data via AJAX.

### Grid XML Structure (ui_component)

Located in `view/adminhtml/ui_component/<listing_name>.xml`:
- `<listing>` root element with data source
- `<dataSource>` — data provider class and configuration
- `<listingToolbar>` — bookmarks, columns controls, filters, mass actions, paging
- `<columns>` — column definitions (type, label, sortable, filterable)
- `<column>` — individual column (text, select, date, actions)
- `<actionsColumn>` — edit/delete action links

### Data Provider

- Extends `Magento\Ui\DataProvider\AbstractDataProvider`
- Backed by a collection (resource model collection)
- Provides data array to the grid

### Mass Actions

Bulk operations on selected rows:
- Delete, status change, export
- Declared in grid XML under `<massaction>`
- Each action maps to a controller

## Admin Forms (UI Component Forms)

Located in `view/adminhtml/ui_component/<form_name>.xml`:
- `<form>` root element
- `<fieldset>` groups related fields
- `<field>` — input, textarea, select, multiselect, boolean, date, imageUploader, wysiwyg
- Data provider loads entity data for editing
- Save controller processes form submission

## System Configuration

### system.xml

Defines admin config fields at Stores > Settings > Configuration:
- `<section>` — top-level tab
- `<group>` — fieldset within a section
- `<field>` — individual configuration field
- Field types: text, textarea, select, multiselect, obscure (password), image

### config.xml

Provides default values for system configuration fields. Path format: `section/group/field`.

### Reading Config Values

```php
$this->scopeConfig->getValue('section/group/field', ScopeInterface::SCOPE_STORE);
```

Scopes: default, website, store (store view).

## ACL (Access Control List)

### acl.xml

Defines resource hierarchy:
- Nested `<resource>` elements form a permission tree
- Admin users are assigned to roles; roles get resource permissions

### Controller ACL

Admin controllers extend `Magento\Backend\App\Action`:
- `const ADMIN_RESOURCE = 'Vendor_Module::resource_name';`
- Framework checks ACL before executing action

### Menu Items

Declared in `etc/adminhtml/menu.xml`:
- Maps to ACL resources
- Defines position in admin sidebar navigation

## Admin Controllers

- Extend `Magento\Backend\App\Action`
- Route in `etc/adminhtml/routes.xml`
- URL: `admin/<frontName>/<controller>/<action>`
- Common patterns: Index (list), Edit, Save, Delete, MassDelete, NewAction

## Best Practices

- Always create ACL resources for every admin feature
- Use UI component grids over custom HTML grids
- Provide bookmarks and export in grids
- Validate form data server-side (never trust client)
- Use `resultPageFactory` for rendering admin pages with proper layout
- Scope config values appropriately (global vs website vs store view)

Fetch the admin grid tutorial, ACL guide, and UI component reference for exact XML schemas and data provider patterns before implementing.
