---
name: b2c-site-import-export
description: Work with site archive structure and metadata XML patterns. Use when adding custom attributes, system object extensions, site preferences, or understanding import/export XML schemas. Covers directory structure and XML file formats for site archives.
---

# Site Import/Export Skill

Use the `b2c` CLI plugin to import and export site archives on Salesforce B2C Commerce instances.

## Import Commands

### Import Local Directory

```bash
# Import a local directory as a site archive
b2c job import ./my-site-data

# Import and wait for completion
b2c job import ./my-site-data --wait

# Import a local zip file
b2c job import ./export.zip

# Keep the archive on the instance after import
b2c job import ./my-site-data --keep-archive

# Show job log if the import fails
b2c job import ./my-site-data --wait --show-log
```

### Import Remote Archive

```bash
# Import an archive that already exists on the instance (in Impex/src/instance/)
b2c job import existing-archive.zip --remote
```

## Export Commands

```bash
# Export site data
b2c job export

# Export with specific configuration
b2c job export --wait
```

## Common Workflows

### Adding a Custom Attribute to Products

1. Create the metadata XML file:

**meta/system-objecttype-extensions.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://www.demandware.com/xml/impex/metadata/2006-10-31">
    <type-extension type-id="Product">
        <custom-attribute-definitions>
            <attribute-definition attribute-id="vendorSKU">
                <display-name xml:lang="x-default">Vendor SKU</display-name>
                <type>string</type>
                <mandatory-flag>false</mandatory-flag>
                <externally-managed-flag>true</externally-managed-flag>
            </attribute-definition>
        </custom-attribute-definitions>
        <group-definitions>
            <attribute-group group-id="CustomAttributes">
                <display-name xml:lang="x-default">Custom Attributes</display-name>
                <attribute attribute-id="vendorSKU"/>
            </attribute-group>
        </group-definitions>
    </type-extension>
</metadata>
```

2. Create the directory structure:
```
my-import/
└── meta/
    └── system-objecttype-extensions.xml
```

3. Import:
```bash
b2c job import ./my-import --wait
```

### Adding Site Preferences

1. Create metadata for the preference:

**meta/system-objecttype-extensions.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://www.demandware.com/xml/impex/metadata/2006-10-31">
    <type-extension type-id="SitePreferences">
        <custom-attribute-definitions>
            <attribute-definition attribute-id="enableFeatureX">
                <display-name xml:lang="x-default">Enable Feature X</display-name>
                <type>boolean</type>
                <default-value>false</default-value>
            </attribute-definition>
        </custom-attribute-definitions>
    </type-extension>
</metadata>
```

2. Create preference values:

**sites/MySite/preferences.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<preferences xmlns="http://www.demandware.com/xml/impex/preferences/2007-03-31">
    <custom-preferences>
        <all-instances>
            <preference preference-id="enableFeatureX">true</preference>
        </all-instances>
    </custom-preferences>
</preferences>
```

3. Directory structure:
```
my-import/
├── meta/
│   └── system-objecttype-extensions.xml
└── sites/
    └── MySite/
        └── preferences.xml
```

4. Import:
```bash
b2c job import ./my-import --wait
```

### Creating a Custom Object Type

1. Define the custom object:

**meta/custom-objecttype-definitions.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://www.demandware.com/xml/impex/metadata/2006-10-31">
    <custom-type type-id="APIConfiguration">
        <display-name xml:lang="x-default">API Configuration</display-name>
        <staging-mode>source-to-target</staging-mode>
        <storage-scope>site</storage-scope>
        <key-definition attribute-id="configId">
            <display-name xml:lang="x-default">Config ID</display-name>
            <type>string</type>
            <min-length>1</min-length>
        </key-definition>
        <attribute-definitions>
            <attribute-definition attribute-id="endpoint">
                <display-name xml:lang="x-default">API Endpoint</display-name>
                <type>string</type>
            </attribute-definition>
            <attribute-definition attribute-id="apiKey">
                <display-name xml:lang="x-default">API Key</display-name>
                <type>password</type>
            </attribute-definition>
            <attribute-definition attribute-id="isActive">
                <display-name xml:lang="x-default">Active</display-name>
                <type>boolean</type>
                <default-value>true</default-value>
            </attribute-definition>
        </attribute-definitions>
    </custom-type>
</metadata>
```

2. Import:
```bash
b2c job import ./my-import --wait
```

### Importing Custom Object Data

**customobjects/APIConfiguration.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<custom-objects xmlns="http://www.demandware.com/xml/impex/customobject/2006-10-31">
    <custom-object type-id="APIConfiguration" object-id="payment-gateway">
        <object-attribute attribute-id="endpoint">https://api.payment.com/v2</object-attribute>
        <object-attribute attribute-id="isActive">true</object-attribute>
    </custom-object>
</custom-objects>
```

## Site Archive Structure

```
site-archive/
├── services.xml                           # Service configurations (credentials, profiles, services)
├── meta/
│   ├── system-objecttype-extensions.xml   # Custom attributes on system objects
│   └── custom-objecttype-definitions.xml  # Custom object type definitions
├── sites/
│   └── {SiteID}/
│       ├── preferences.xml                # Site preference values
│       └── library/
│           └── content/
│               └── content.xml            # Content assets
├── catalogs/
│   └── {CatalogID}/
│       └── catalog.xml                    # Products and categories
├── pricebooks/
│   └── {PriceBookID}/
│       └── pricebook.xml                  # Price definitions
├── customobjects/
│   └── {ObjectTypeID}.xml                 # Custom object instances
└── inventory-lists/
    └── {InventoryListID}/
        └── inventory.xml                  # Inventory records
```

## Tips

### Checking Job Status

```bash
# Search for recent job executions
b2c job search

# Wait for a specific job execution
b2c job wait <execution-id>

# View job logs on failure
b2c job import ./my-data --wait --show-log
```

### Best Practices

1. **Test imports on sandbox first** before importing to staging/production
2. **Use `--wait`** to ensure import completes before continuing
3. **Use `--show-log`** to debug failed imports
4. **Keep archives organized** by feature or change type
5. **Version control your metadata** XML files

### Configuring External Services

For service configurations (HTTP, FTP, SOAP services), see the `b2c:b2c-webservices` skill which includes:
- Complete services.xml examples
- Credential, profile, and service element patterns
- Import/export workflows

Quick example:
```bash
# Import service configuration
b2c job import ./services-folder
```

Where `services-folder/services.xml` follows the patterns in the `b2c:b2c-webservices` skill.

## Detailed Reference

- [Metadata XML Patterns](references/METADATA-XML.md) - Common XML patterns for imports

## Related Skills

- `b2c:b2c-webservices` - Service configurations (HTTP, FTP, SOAP), services.xml format
- `b2c:b2c-metadata` - System object extensions and custom object definitions
- `b2c-cli:b2c-job` - Running jobs and monitoring import status
