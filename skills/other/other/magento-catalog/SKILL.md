---
name: magento-catalog
description: Work with Magento 2 catalog — product types, categories, attributes, indexing, and search integration. Use when building catalog features, customizing product types, or working with the catalog architecture.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Catalog & Product Types

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.adobe.com commerce php development components catalog` for catalog development
2. Web-search `site:developer.adobe.com commerce php development components indexing` for indexer guide
3. Fetch `https://developer.adobe.com/commerce/php/development/components/indexing/` for indexing architecture

## Product Types

### Six Built-in Types

| Type | Description | Key Characteristics |
|------|-------------|-------------------|
| **Simple** | Single physical item | Unique SKU, own stock, no variations |
| **Configurable** | Parent with variant children | Children are simple products, vary by attributes (size, color) |
| **Grouped** | Collection of products | Simple/virtual children, purchased independently |
| **Bundle** | Customer-assembled set | Options with selectable items, dynamic/fixed pricing |
| **Virtual** | Non-physical (services) | No shipping, no weight |
| **Downloadable** | Digital products | Files/links, optional samples |

### Configurable Products

The most complex type — a parent product with simple product children:
- Super attributes determine variations (e.g., color, size)
- Each combination maps to a child simple product with its own SKU and stock
- Frontend: dropdown selectors, price updates, image swapping
- Key tables: `catalog_product_super_attribute`, `catalog_product_super_link`

### Custom Product Types

Possible to create custom types by:
- Extending `Magento\Catalog\Model\Product\Type\AbstractType`
- Registering in `etc/product_types.xml`
- Defining custom price model, stock handling, and checkout behavior

## Categories

### Category Tree

- Hierarchical structure with root categories and subcategories
- Each store view has one root category
- Categories use EAV for attributes
- URL rewrites generate SEO-friendly paths
- Display modes: products only, CMS block only, both

### Category Attributes

- `name`, `description`, `image`, `meta_title`, `meta_description`
- `is_active`, `include_in_menu`, `display_mode`
- `url_key`, `url_path`
- Custom attributes addable via data patches

## Indexing

### Why Indexing Exists

EAV queries are expensive. Indexers pre-compute denormalized data for fast reads.

### Standard Indexers

- `catalog_product_price` — pre-computed product prices
- `catalogsearch_fulltext` — search engine index (OpenSearch/Elasticsearch)
- `catalog_product_attribute` — filterable attributes for layered navigation
- `cataloginventory_stock` — stock status
- `catalogrule_product` — catalog price rules
- `catalog_category_product` — category-product associations

### Index Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Update on Save** | Reindexes immediately on data change | Small catalogs, development |
| **Update by Schedule** | Cron-based, uses changelog tables | Production (recommended) |

### Mview (Materialized Views)

Changelog tables (`*_cl`) track changes via database triggers. Cron compares versions in `mview_state` to determine what needs reindexing. Efficient — only processes changed entities.

### CLI Commands

```bash
bin/magento indexer:reindex                    # Reindex all
bin/magento indexer:reindex catalogsearch_fulltext  # Reindex specific
bin/magento indexer:status                     # Show status
bin/magento indexer:set-mode schedule           # Set all to schedule mode
```

## Search Integration

- A search engine has been required since 2.4.0 (originally Elasticsearch; OpenSearch supported from 2.4.6; only OpenSearch from 2.4.8)
- Products, categories indexed for search and layered navigation
- Elasticsearch removed in 2.4.8
- Custom search attributes configurable per attribute

## Best Practices

- Use "Update by Schedule" indexing in production
- Design catalog structure before adding products — attribute sets are hard to change later
- Use configurable products for variant-heavy catalogs
- Keep EAV attribute count reasonable — more attributes = slower indexing
- Test catalog operations at scale (1000+ products) to catch performance issues
- Use the repository pattern (`ProductRepositoryInterface`) for programmatic product access

Fetch the catalog and indexing docs for exact indexer configuration, product type XML schema, and search integration patterns before implementing.
