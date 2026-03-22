---
name: magento-module-dev
description: Create Magento 2 custom modules — registration, directory structure, models, resource models, collections, declarative schema, and data/schema patches. Use when building new modules or understanding module architecture.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Module Development

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.adobe.com/commerce/php/development/build/component-file-structure/` for module structure
2. Fetch `https://developer.adobe.com/commerce/php/development/` for development overview
3. Web-search `site:developer.adobe.com commerce php development build` for build guides

## Module Directory Structure

```
app/code/VendorName/ModuleName/
├── Api/                    # Service contract interfaces
│   └── Data/               # Data interfaces
├── Block/                  # View blocks
├── Console/                # CLI commands
├── Controller/             # Controllers
│   └── Adminhtml/          # Admin controllers
├── Cron/                   # Cron job classes
├── etc/                    # Configuration XML
│   ├── adminhtml/          # Admin-area configs
│   ├── frontend/           # Frontend configs
│   ├── module.xml          # Module declaration
│   ├── di.xml              # Dependency injection
│   ├── db_schema.xml       # Declarative schema
│   └── db_schema_whitelist.json
├── Helper/                 # Utility classes
├── Model/                  # Models
│   └── ResourceModel/      # Resource models + collections
├── Observer/               # Event observers
├── Plugin/                 # Interceptor classes
├── Setup/
│   └── Patch/
│       ├── Data/           # Data patches
│       └── Schema/         # Schema patches
├── Test/                   # Tests
├── ViewModel/              # MVVM view models
├── view/                   # Templates, layouts, JS, CSS
├── registration.php        # Module registration
└── composer.json           # Composer definition
```

## Essential Files

### registration.php
Registers the module with Magento's component registrar. Uses `ComponentRegistrar::register()` with type `MODULE`.

### etc/module.xml
Declares the module name and sequence dependencies (modules that must load before this one).

### composer.json
Package definition with type `magento2-module`, PSR-4 autoload mapping, and Magento module dependencies.

## Data Layer Pattern

### Model → Resource Model → Collection

- **Model** — extends `AbstractModel`, represents a single entity, `_construct()` initializes resource model
- **Resource Model** — extends `AbstractDb`, handles CRUD against a specific table, `_init()` sets table and primary key
- **Collection** — extends `AbstractCollection`, represents a set of models, `_init()` maps model to resource model

### Declarative Schema (db_schema.xml)

Since Magento 2.3+, database schema is declared in XML rather than install/upgrade scripts. The system computes diffs and applies changes automatically on `setup:upgrade`.

### Data and Schema Patches

- **Schema Patches** — structural changes (add columns, modify indexes)
- **Data Patches** — data migrations (insert default records, transform data)
- Implement `DataPatchInterface` or `SchemaPatchInterface`
- `apply()` method contains the migration logic
- Patches run once and are tracked in `patch_list` table

## CLI Command Pattern

Console commands extend `Symfony\Component\Console\Command\Command`:
- Register in `etc/di.xml` as arguments to `Magento\Framework\Console\CommandListInterface`
- Implement `configure()` for name/description and `execute()` for logic

## Best Practices

- Follow `VendorName_ModuleName` naming convention
- Declare all module dependencies in `module.xml` sequence
- Use declarative schema instead of install/upgrade scripts
- Use data patches for data migrations
- Keep models thin — business logic in service classes
- Always define service contract interfaces in `Api/`

Fetch the component file structure guide for exact directory conventions and required files before creating a module.
