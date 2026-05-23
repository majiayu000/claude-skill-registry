---
name: magento-eav-attributes
description: Work with Magento 2 EAV (Entity-Attribute-Value) system — create custom attributes, attribute sets, manage EAV tables, and understand the EAV data model. Use when adding product/category/customer attributes or working with the attribute system.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 EAV & Attributes

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.adobe.com commerce php development components attributes` for attribute development guide
2. Web-search `site:developer.adobe.com commerce php tutorials backend custom-attributes` for attribute creation tutorial
3. Web-search `magento 2 EAV attribute data patch` for current patterns using data patches

## Conceptual Architecture

### What EAV Is

Entity-Attribute-Value is Magento's flexible storage pattern. Instead of one column per attribute, values are stored in separate typed tables. This allows merchants to add unlimited attributes without schema changes.

### EAV Entities

Four entity types use EAV:
- **Products** (`catalog_product_entity`)
- **Categories** (`catalog_category_entity`)
- **Customers** (`customer_entity`)
- **Customer Addresses** (`customer_address_entity`)

### EAV Table Structure

Each entity has typed value tables:
- `*_entity` — base entity table (entity_id, sku, type_id, etc.)
- `*_entity_varchar` — short text values
- `*_entity_int` — integer values (including boolean, select)
- `*_entity_decimal` — decimal/price values
- `*_entity_datetime` — date/time values
- `*_entity_text` — long text values

### Attribute Properties

Key properties when creating attributes:
- **type** — backend storage type (varchar, int, decimal, datetime, text, static)
- **input** — frontend input type (text, textarea, select, multiselect, boolean, date, price, media_image, etc.)
- **label** — human-readable name
- **required** — is this attribute mandatory?
- **source** — source model for select/multiselect options
- **backend** — backend model for validation/processing
- **frontend** — frontend model for display formatting
- **global** — scope: store view, website, or global
- **visible** — shown in admin forms
- **searchable** — indexed for catalog search
- **filterable** — available as layered navigation filter
- **comparable** — shown in product comparison
- **used_in_product_listing** — available in category listing pages

### Attribute Sets and Groups

- **Attribute Set** — a named collection of attributes (e.g., "Default", "Clothing", "Electronics")
- **Attribute Group** — organizes attributes within a set into tabs (e.g., "General", "Prices", "Images")
- Every product is assigned one attribute set
- The Default attribute set contains core attributes

### Creating Attributes via Data Patch

The modern approach uses Data Patches with `EavSetupFactory`:
1. Create a data patch class in `Setup/Patch/Data/`
2. Inject `EavSetupFactory` (or `CategorySetupFactory` for categories)
3. Call `$eavSetup->addAttribute()` with entity type, code, and properties
4. Assign to attribute set/group

### Source Models

For select/multiselect attributes, source models provide options:
- Built-in: `Magento\Eav\Model\Entity\Attribute\Source\Boolean`, `Table`
- Custom: extend `AbstractSource`, implement `getAllOptions()`

### Static Attributes

Attributes with type `static` are stored as columns directly on the entity table rather than in EAV value tables. Used for frequently queried fields (e.g., `sku`, `type_id`, `created_at`).

### Best Practices

- Use data patches (not install/upgrade scripts) for attribute creation
- Choose the correct backend type — `int` for select/boolean, `decimal` for prices
- Set `searchable`, `filterable`, `comparable` thoughtfully — each adds indexing overhead
- Use `static` type sparingly — it modifies the entity table schema
- Test attribute creation on a clean install and with `setup:upgrade`

Fetch the attribute development docs for exact `addAttribute()` parameters, source model patterns, and current entity type constants before implementing.
