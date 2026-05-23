---
name: typo3-content-blocks
description: Expert guidance on creating Content Elements, Record Types, and Page Types using TYPO3 Content Blocks extension - the single source of truth for content modeling. Includes bidirectional migration between classic TCA/SQL and Content Blocks.
version: 1.2.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - content-blocks
  - content-element
  - record-type
  - page-type
  - make:content-block
  - friendsoftypo3/content-blocks
  - irre
  - collection
  - migrate to content blocks
  - convert tca
  - modernize extension
  - tca to yaml
  - classic to content blocks
  - revert content blocks
  - content blocks to tca
  - yaml to tca
  - remove content blocks
  - classic extension
---

# TYPO3 Content Blocks Development

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> All code examples in this skill are designed to work on both TYPO3 v13 and v14.

## 1. The Single Source of Truth Principle

Content Blocks is the **modern approach** to creating custom content types in TYPO3. It eliminates redundancy by providing a **single YAML configuration** that generates:

- TCA (Table Configuration Array)
- Database schema (SQL)
- TypoScript rendering
- Backend forms and previews
- Labels and translations

### Why Content Blocks?

| Traditional Approach | Content Blocks Approach |
|---------------------|------------------------|
| Multiple TCA files | One `config.yaml` |
| Manual SQL definitions | Auto-generated schema |
| Separate TypoScript | Auto-registered rendering |
| Scattered translations | Single `labels.xlf` |
| Complex setup | Simple folder structure |

## 2. Installation

```bash
# Install via Composer (DDEV recommended)
ddev composer require friendsoftypo3/content-blocks

# After installation, clear caches
ddev typo3 cache:flush
```

### Security Configuration (Classic Mode)

For non-composer installations, deny web access to ContentBlocks folder:

```apache
# .htaccess addition
RewriteRule (?:typo3conf/ext|typo3/sysext|typo3/ext)/[^/]+/(?:Configuration|ContentBlocks|Resources/Private|Tests?|Documentation|docs?)/ - [F]
```

## 3. Content Types Overview

Content Blocks supports four content types:

| Type | Folder | Use Case |
|------|--------|----------|
| `ContentElements` | `ContentBlocks/ContentElements/` | Frontend content (tt_content) |
| `RecordTypes` | `ContentBlocks/RecordTypes/` | Custom records (new tables) |
| `PageTypes` | `ContentBlocks/PageTypes/` | Custom page types |
| `FileTypes` | `ContentBlocks/FileTypes/` | Custom file metadata |

## 4. Folder Structure

```
EXT:my_sitepackage/
└── ContentBlocks/
    ├── ContentElements/
    │   └── my-hero/
    │       ├── assets/
    │       │   └── icon.svg
    │       ├── language/
    │       │   └── labels.xlf
    │       ├── templates/
    │       │   ├── backend-preview.html
    │       │   ├── frontend.html
    │       │   └── partials/
    │       └── config.yaml
    └── RecordTypes/
        └── my-record/
            ├── assets/
            │   └── icon.svg
            ├── language/
            │   └── labels.xlf
            └── config.yaml
```

## 5. Creating Content Elements

### Kickstart Command (Recommended)

```bash
# Interactive mode
ddev typo3 make:content-block

# One-liner
ddev typo3 make:content-block \
  --content-type="content-element" \
  --vendor="myvendor" \
  --name="hero-banner" \
  --title="Hero Banner" \
  --extension="my_sitepackage"

# After creation, update database
ddev typo3 cache:flush -g system
ddev typo3 extension:setup --extension=my_sitepackage
```

### Minimal Content Element

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/hero-banner/config.yaml
name: myvendor/hero-banner
fields:
  - identifier: header
    useExistingField: true
  - identifier: bodytext
    useExistingField: true
```

### Full Content Element Example

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/hero-banner/config.yaml
name: myvendor/hero-banner
group: default
description: "A full-width hero banner with image and CTA"
prefixFields: true
prefixType: full
basics:
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
    label: Subheadline
  - identifier: hero_image
    type: File
    minitems: 1
    maxitems: 1
    allowed: common-image-types
  - identifier: cta_link
    type: Link
    label: Call to Action Link
  - identifier: cta_text
    type: Text
    label: Button Text
```

### Frontend Template

```html
<!-- templates/frontend.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:cb="http://typo3.org/ns/TYPO3/CMS/ContentBlocks/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:asset.css identifier="hero-banner-css" href="{cb:assetPath()}/frontend.css"/>

<section class="hero-banner">
    <f:if condition="{data.hero_image}">
        <f:for each="{data.hero_image}" as="image">
            <f:image image="{image}" alt="{data.header}" class="hero-image"/>
        </f:for>
    </f:if>
    
    <div class="hero-content">
        <h1>{data.header}</h1>
        <f:if condition="{data.subheadline}">
            <p class="subheadline">{data.subheadline}</p>
        </f:if>
        
        <f:if condition="{data.cta_link}">
            <f:link.typolink parameter="{data.cta_link}" class="btn btn-primary">
                {data.cta_text -> f:or(default: 'Learn more')}
            </f:link.typolink>
        </f:if>
    </div>
</section>
</html>
```

### Backend Preview Template

```html
<!-- templates/backend-preview.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:be="http://typo3.org/ns/TYPO3/CMS/Backend/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="content-block-preview">
    <strong>{data.header}</strong>
    <f:if condition="{data.subheadline}">
        <br/><em>{data.subheadline}</em>
    </f:if>
    <f:if condition="{data.hero_image}">
        <f:for each="{data.hero_image}" as="image">
            <be:thumbnail image="{image}" width="100" height="100"/>
        </f:for>
    </f:if>
</div>
</html>
```

## 6. Creating Record Types (Custom Tables)

Record Types create **custom database tables** for structured data like teams, products, events, etc.

### Extbase-Compatible Table Naming

**IMPORTANT:** For Extbase compatibility, use the `tx_extensionkey_domain_model_*` naming convention:

```yaml
# ✅ CORRECT - Extbase compatible table name
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fields:
  - identifier: name
    type: Text
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: photo
    type: File
    allowed: common-image-types
    maxitems: 1
```

```yaml
# ❌ WRONG - Short table names don't work with Extbase
name: myvendor/team-member
table: team_member  # Won't work with Extbase!
```

### Minimal Record Type

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fields:
  - identifier: name
    type: Text
```

### Full Record Type Example

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fallbackLabelFields:
  - email
languageAware: true
workspaceAware: true
sortable: true
softDelete: true
trackCreationDate: true
trackUpdateDate: true
internalDescription: true
restriction:
  disabled: true
  startTime: true
  endTime: true
security:
  ignorePageTypeRestriction: true  # Allow on normal pages
fields:
  - identifier: name
    type: Text
    required: true
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: phone
    type: Text
  - identifier: bio
    type: Textarea
    enableRichtext: true
  - identifier: photo
    type: File
    allowed: common-image-types
    maxitems: 1
  - identifier: social_links
    type: Collection
    labelField: platform
    fields:
      - identifier: platform
        type: Select
        items:
          - label: LinkedIn
            value: linkedin
          - label: Twitter/X
            value: twitter
          - label: GitHub
            value: github
      - identifier: url
        type: Link
```

### Multi-Type Records (Single Table Inheritance)

Create multiple types for one table:

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/person-employee/config.yaml
name: myvendor/person-employee
table: tx_mysitepackage_domain_model_person
typeField: person_type
typeName: employee
priority: 999  # Default type (loaded first)
labelField: name
languageAware: false
workspaceAware: false
fields:
  - identifier: name
    type: Text
  - identifier: department
    type: Text
```

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/person-contractor/config.yaml
name: myvendor/person-contractor
table: tx_mysitepackage_domain_model_person
typeName: contractor
fields:
  - identifier: name
    type: Text
  - identifier: company
    type: Text
  - identifier: contract_end
    type: DateTime
```

### Record Types as Collection Children

Define a record that can be used in IRRE collections:

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/slide/config.yaml
name: myvendor/slide
table: tx_mysitepackage_domain_model_slide
labelField: title
fields:
  - identifier: title
    type: Text
  - identifier: image
    type: File
    maxitems: 1
  - identifier: link
    type: Link
```

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/slider/config.yaml
name: myvendor/slider
fields:
  - identifier: slides
    type: Collection
    foreign_table: tx_mysitepackage_domain_model_slide
    shareAcrossTables: true
    shareAcrossFields: true
    minitems: 1
```

## 7. Field Types Reference

### Simple Fields

| Type | Description | Example |
|------|-------------|---------|
| `Text` | Single line text | `type: Text` |
| `Textarea` | Multi-line text | `type: Textarea` |
| `Email` | Email address | `type: Email` |
| `Link` | Link/URL | `type: Link` |
| `Number` | Integer/Float | `type: Number` |
| `DateTime` | Date and/or time | `type: DateTime` |
| `Color` | Color picker | `type: Color` |
| `Checkbox` | Boolean checkbox | `type: Checkbox` |
| `Radio` | Radio buttons | `type: Radio` |
| `Slug` | URL slug | `type: Slug` |
| `Password` | Password field | `type: Password` |

### Relational Fields

| Type | Description | Example |
|------|-------------|---------|
| `File` | File references (FAL) | `type: File` |
| `Relation` | Record relations | `type: Relation` |
| `Select` | Dropdown selection | `type: Select` |
| `Category` | System categories | `type: Category` |
| `Collection` | Inline records (IRRE) | `type: Collection` |
| `Folder` | Folder reference | `type: Folder` |
| `Language` | Language selector | `type: Language` |

### Structural Fields

| Type | Description | Example |
|------|-------------|---------|
| `Tab` | Tab separator | `type: Tab` |
| `Palette` | Group fields | `type: Palette` |
| `Linebreak` | Line break in palette | `type: Linebreak` |
| `FlexForm` | FlexForm container | `type: FlexForm` |
| `Json` | JSON field | `type: Json` |

### Common Field Options

```yaml
fields:
  - identifier: my_field
    type: Text
    label: My Field Label           # Static label (or use labels.xlf)
    description: Help text          # Field description
    required: true                  # Make field required
    default: "Default value"        # Default value
    placeholder: "Enter text..."    # Placeholder text
    prefixField: false              # Disable prefixing for this field
    useExistingField: true          # Reuse existing TCA field
    displayCond: 'FIELD:other:=:1'  # Conditional display
    onChange: reload                # Reload form on change
```

### File Field Example

```yaml
fields:
  - identifier: gallery_images
    type: File
    allowed: common-image-types
    minitems: 1
    maxitems: 10
    appearance:
      createNewRelationLinkTitle: Add Image
      showAllLocalizationLink: true
    behaviour:
      allowLanguageSynchronization: true
```

### Select Field Example

```yaml
fields:
  - identifier: layout
    type: Select
    renderType: selectSingle
    default: default
    items:
      - label: Default Layout
        value: default
      - label: Wide Layout
        value: wide
      - label: Compact Layout
        value: compact
```

### Collection Field Example (Inline IRRE)

```yaml
fields:
  - identifier: accordion_items
    type: Collection
    labelField: title
    minitems: 1
    maxitems: 20
    appearance:
      collapseAll: true
      levelLinksPosition: both
    fields:
      - identifier: title
        type: Text
        required: true
      - identifier: content
        type: Textarea
        enableRichtext: true
      - identifier: is_open
        type: Checkbox
        label: Initially Open
```

## 8. Field Prefixing

Content Blocks automatically prefixes field identifiers to avoid collisions.

### Prefixing Types

```yaml
# Full prefix (default): myvendor_myblock_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: full

# Vendor prefix only: myvendor_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: vendor

# Custom vendor prefix: tx_custom_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: vendor
vendorPrefix: tx_custom

# No prefix (use with caution!)
name: myvendor/my-block
prefixFields: false
```

### Disable Prefixing per Field

```yaml
fields:
  - identifier: my_custom_field
    type: Text
    prefixField: false  # This field won't be prefixed
```

## 9. Templating Features

### Accessing Data in Fluid

```html
<!-- Basic field access -->
{data.header}
{data.my_field}

<!-- Record metadata -->
{data.uid}
{data.pid}
{data.languageId}
{data.mainType}      <!-- Table name: tt_content -->
{data.recordType}    <!-- CType: myvendor_heroblock -->
{data.fullType}      <!-- tt_content.myvendor_heroblock -->

<!-- Raw database values -->
{data.rawRecord.some_field}

<!-- System properties -->
{data.systemProperties.createdAt}
{data.systemProperties.lastUpdatedAt}
{data.systemProperties.sorting}
{data.systemProperties.disabled}

<!-- Language info -->
{data.languageInfo.translationParent}
{data.languageInfo.translationSource}

<!-- Relations are auto-resolved! -->
<f:for each="{data.gallery_images}" as="image">
    <f:image image="{image}" width="400"/>
</f:for>

<!-- Nested collections -->
<f:for each="{data.accordion_items}" as="item">
    <h3>{item.title}</h3>
    <f:format.html>{item.content}</f:format.html>
</f:for>
```

### Asset ViewHelpers

```html
<!-- Include CSS from assets folder -->
<f:asset.css identifier="my-block-css" href="{cb:assetPath()}/frontend.css"/>

<!-- Include JS from assets folder -->
<f:asset.script identifier="my-block-js" src="{cb:assetPath()}/frontend.js"/>

<!-- Cross-block asset reference -->
<f:asset.css identifier="shared-css" href="{cb:assetPath(name: 'vendor/other-block')}/shared.css"/>
```

### Translation ViewHelper

```html
<!-- Access labels.xlf translations -->
<f:translate key="{cb:languagePath()}:my_label"/>

<!-- Cross-block translation -->
<f:translate key="{cb:languagePath(name: 'vendor/other-block')}:shared_label"/>
```

## 10. Extending Existing Tables

Add custom types to existing tables (like `tx_news`):

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/custom-news/config.yaml
name: myvendor/custom-news
table: tx_news_domain_model_news
typeName: custom_news
fields:
  - identifier: title
    useExistingField: true
  - identifier: custom_field
    type: Text
```

## 11. Workflow with DDEV

### Standard Development Workflow

```bash
# 1. Create new Content Block
ddev typo3 make:content-block

# 2. Clear system caches
ddev typo3 cache:flush -g system

# 3. Update database schema
ddev typo3 extension:setup --extension=my_sitepackage

# Alternative: Use Database Analyzer in TYPO3 Backend
# Admin Tools > Maintenance > Analyze Database Structure
```

### Using webprofil/make Extension

If `webprofil/make` is installed:

```bash
# Create Content Block with webprofil/make
ddev make:content_blocks

# Clear caches and update database
ddev typo3 cache:flush
ddev typo3 database:updateschema
```

### Integration with Extbase

After creating Record Types with proper table names, generate Extbase models:

```bash
# If typo3:make:model is available
ddev typo3 make:model --extension=my_sitepackage

# Generate repository
ddev typo3 make:repository --extension=my_sitepackage
```

## 12. Defaults Configuration

Create a `content-blocks.yaml` in project root for default settings:

```yaml
# content-blocks.yaml
vendor: myvendor
extension: my_sitepackage
content-type: content-element
skeleton-path: content-blocks-skeleton

config:
  content-element:
    basics:
      - TYPO3/Appearance
      - TYPO3/Links
    group: common
    prefixFields: true
    prefixType: full
  
  record-type:
    prefixFields: true
    prefixType: vendor
    vendorPrefix: tx_mysitepackage
```

## 13. Best Practices

### DO ✅

1. **Use Extbase-compatible table names** for Record Types:
   ```yaml
   table: tx_myextension_domain_model_myrecord
   ```

2. **Reuse existing fields** when possible:
   ```yaml
   - identifier: header
     useExistingField: true
   ```

3. **Group related fields** with Tabs and Palettes:
   ```yaml
   - identifier: settings_tab
     type: Tab
     label: Settings
   ```

4. **Use meaningful identifiers** (snake_case):
   ```yaml
   - identifier: hero_background_image
   ```

5. **Clear caches after changes**:
   ```bash
   ddev typo3 cache:flush -g system
   ddev typo3 extension:setup --extension=my_sitepackage
   ```

6. **Use labels.xlf** for all user-facing labels

### DON'T ❌

1. **Don't use raw SQL** - Content Blocks generates schema automatically

2. **Don't duplicate TCA** - Config.yaml is the single source of truth

3. **Don't use short table names** for Extbase integration:
   ```yaml
   # ❌ Wrong
   table: team_member
   
   # ✅ Correct
   table: tx_mysitepackage_domain_model_teammember
   ```

4. **Don't use dashes in identifiers**:
   ```yaml
   # ❌ Wrong
   identifier: hero-image
   
   # ✅ Correct
   identifier: hero_image
   ```

5. **Don't forget shareAcross options** when using foreign_table in multiple places

## 14. Troubleshooting

### Content Block Not Appearing

```bash
# Clear all caches
ddev typo3 cache:flush

# Rebuild class loading
ddev composer dump-autoload

# Check extension setup
ddev typo3 extension:setup --extension=my_sitepackage
```

### Database Errors

```bash
# Update database schema
ddev typo3 database:updateschema

# Or use Compare Tool
# Admin Tools > Maintenance > Analyze Database Structure
```

### Field Not Saving

- Check field identifier is unique (use prefixing)
- Verify field type is correct
- Check for typos in config.yaml
- Ensure labels.xlf has matching keys

## 15. Version Constraints

```php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '1.0.0',
    'state' => 'stable',
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
            'content_blocks' => '2.0.0-2.99.99',
        ],
    ],
];
```

## 16. Migrating Classic Extensions to Content Blocks

This section guides you through converting traditional TYPO3 extensions (with separate TCA, SQL, TypoScript) to the modern Content Blocks approach.

### When to Migrate

| Scenario | Recommendation |
|----------|----------------|
| New content elements | ✅ Use Content Blocks from the start |
| Simple records (products, team, events) | ✅ Migrate to Content Blocks |
| Complex Extbase extensions with controllers | ⚠️ Keep Extbase, optionally use Content Blocks for TCA |
| Heavy business logic in domain models | ⚠️ Keep Extbase models, consider Content Blocks for forms only |
| Extensions with many plugins | ❌ Keep traditional approach |

### Migration Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  1. ANALYZE                                                       │
│     └─ Identify TCA, SQL, TypoScript, Templates                  │
├─────────────────────────────────────────────────────────────────┤
│  2. MAP                                                           │
│     └─ Create field mapping from TCA columns to Content Blocks   │
├─────────────────────────────────────────────────────────────────┤
│  3. CREATE                                                        │
│     └─ Build config.yaml with mapped fields                      │
├─────────────────────────────────────────────────────────────────┤
│  4. MIGRATE DATA                                                  │
│     └─ Rename columns if needed, update CTypes                   │
├─────────────────────────────────────────────────────────────────┤
│  5. CLEANUP                                                       │
│     └─ Remove old TCA, SQL, TypoScript files                     │
└─────────────────────────────────────────────────────────────────┘
```

### TCA to Content Blocks Field Mapping

| TCA Type | TCA renderType | Content Blocks Type | Notes |
|----------|----------------|---------------------|-------|
| `input` | - | `Text` | Basic text input |
| `input` | `inputDateTime` | `DateTime` | Date/time picker |
| `input` | `inputLink` | `Link` | Link browser |
| `input` | `colorPicker` | `Color` | Color picker |
| `input` | `slug` | `Slug` | URL slug |
| `text` | - | `Textarea` | Multi-line text |
| `text` | (richtext) | `Textarea` + `enableRichtext: true` | RTE |
| `check` | - | `Checkbox` | Boolean checkbox |
| `radio` | - | `Radio` | Radio buttons |
| `select` | `selectSingle` | `Select` | Single selection |
| `select` | `selectMultipleSideBySide` | `Select` + `multiple: true` | Multiple selection |
| `select` | `selectCheckBox` | `Select` + `renderType: selectCheckBox` | Checkbox group |
| `group` | - | `Relation` or `File` | Depends on internal_type |
| `file` | - | `File` | FAL references |
| `inline` | - | `Collection` | IRRE relations |
| `category` | - | `Category` | System categories |
| `flex` | - | `FlexForm` | FlexForm container |
| `json` | - | `Json` | JSON data |

### Migration Example 1: Content Element (tt_content)

**BEFORE (Classic):**

```php
// Configuration/TCA/Overrides/tt_content.php
\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addPlugin(
    ['LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:ce.hero', 'myext_hero'],
    'CType',
    'my_ext'
);

$GLOBALS['TCA']['tt_content']['types']['myext_hero'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            tx_myext_subheadline,
            tx_myext_image,
            tx_myext_link,
        --div--;LLL:EXT:frontend/Resources/Private/Language/locallang_ttc.xlf:tabs.appearance,
            --palette--;;frames,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
    ',
];

$tempColumns = [
    'tx_myext_subheadline' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:subheadline',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_myext_image' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:image',
        'config' => [
            'type' => 'file',
            'maxitems' => 1,
            'allowed' => 'common-image-types',
        ],
    ],
    'tx_myext_link' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:link',
        'config' => [
            'type' => 'link',
        ],
    ],
];
\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addTCAcolumns('tt_content', $tempColumns);
```

```sql
-- ext_tables.sql
CREATE TABLE tt_content (
    tx_myext_subheadline varchar(255) DEFAULT '' NOT NULL,
    tx_myext_image int(11) DEFAULT 0 NOT NULL,
    tx_myext_link varchar(1024) DEFAULT '' NOT NULL
);
```

```typoscript
# Configuration/TypoScript/setup.typoscript
tt_content.myext_hero = FLUIDTEMPLATE
tt_content.myext_hero {
    templateName = Hero
    templateRootPaths.10 = EXT:my_ext/Resources/Private/Templates/
}
```

**AFTER (Content Blocks):**

```yaml
# ContentBlocks/ContentElements/hero/config.yaml
name: myvendor/hero
basics:
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
  - identifier: image
    type: File
    maxitems: 1
    allowed: common-image-types
  - identifier: link
    type: Link
```

```html
<!-- ContentBlocks/ContentElements/hero/templates/frontend.html -->
<section class="hero">
    <f:if condition="{data.image}">
        <f:for each="{data.image}" as="img">
            <f:image image="{img}" class="hero-bg"/>
        </f:for>
    </f:if>
    <h1>{data.header}</h1>
    <f:if condition="{data.subheadline}">
        <p>{data.subheadline}</p>
    </f:if>
    <f:if condition="{data.link}">
        <f:link.typolink parameter="{data.link}" class="btn">Learn More</f:link.typolink>
    </f:if>
</section>
```

**That's it!** No TCA files, no SQL, no TypoScript for rendering.

### Migration Example 2: Custom Record Table

**BEFORE (Classic):**

```php
// Configuration/TCA/tx_myext_domain_model_product.php
return [
    'ctrl' => [
        'title' => 'Product',
        'label' => 'name',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'sortby' => 'sorting',
        'languageField' => 'sys_language_uid',
        'transOrigPointerField' => 'l10n_parent',
        'transOrigDiffSourceField' => 'l10n_diffsource',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        'iconfile' => 'EXT:my_ext/Resources/Public/Icons/product.svg',
    ],
    'columns' => [
        'hidden' => [
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.hidden',
            'config' => ['type' => 'check'],
        ],
        'name' => [
            'label' => 'Name',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
                'required' => true,
            ],
        ],
        'description' => [
            'label' => 'Description',
            'config' => [
                'type' => 'text',
                'enableRichtext' => true,
            ],
        ],
        'price' => [
            'label' => 'Price',
            'config' => [
                'type' => 'number',
                'format' => 'decimal',
            ],
        ],
        'sku' => [
            'label' => 'SKU',
            'config' => [
                'type' => 'input',
                'size' => 30,
            ],
        ],
        'image' => [
            'label' => 'Image',
            'config' => [
                'type' => 'file',
                'maxitems' => 5,
                'allowed' => 'common-image-types',
            ],
        ],
        'category' => [
            'label' => 'Category',
            'config' => [
                'type' => 'select',
                'renderType' => 'selectSingle',
                'items' => [
                    ['label' => 'Electronics', 'value' => 'electronics'],
                    ['label' => 'Clothing', 'value' => 'clothing'],
                    ['label' => 'Books', 'value' => 'books'],
                ],
            ],
        ],
        // ... more system fields
    ],
    'types' => [
        '1' => ['showitem' => 'hidden, name, sku, price, category, description, image'],
    ],
];
```

```sql
-- ext_tables.sql
CREATE TABLE tx_myext_domain_model_product (
    name varchar(255) DEFAULT '' NOT NULL,
    description text,
    price double(11,2) DEFAULT 0.00 NOT NULL,
    sku varchar(100) DEFAULT '' NOT NULL,
    image int(11) DEFAULT 0 NOT NULL,
    category varchar(50) DEFAULT '' NOT NULL
);
```

**AFTER (Content Blocks):**

```yaml
# ContentBlocks/RecordTypes/product/config.yaml
name: myvendor/product
table: tx_myext_domain_model_product
labelField: name
languageAware: true
workspaceAware: false
sortable: true
softDelete: true
trackCreationDate: true
trackUpdateDate: true
restriction:
  disabled: true
  startTime: true
  endTime: true
security:
  ignorePageTypeRestriction: true
fields:
  - identifier: name
    type: Text
    required: true
  - identifier: sku
    type: Text
  - identifier: price
    type: Number
    format: decimal
  - identifier: category
    type: Select
    items:
      - label: Electronics
        value: electronics
      - label: Clothing
        value: clothing
      - label: Books
        value: books
  - identifier: description
    type: Textarea
    enableRichtext: true
  - identifier: image
    type: File
    maxitems: 5
    allowed: common-image-types
```

**That's it!** No TCA file, no SQL file. Delete the old files after migration.

### Migration Example 3: IRRE Child Records

**BEFORE (Classic with IRRE):**

```php
// Parent TCA with inline field
'slides' => [
    'label' => 'Slides',
    'config' => [
        'type' => 'inline',
        'foreign_table' => 'tx_myext_domain_model_slide',
        'foreign_field' => 'parentid',
        'foreign_table_field' => 'parenttable',
        'maxitems' => 10,
        'appearance' => [
            'collapseAll' => true,
            'levelLinksPosition' => 'both',
            'useSortable' => true,
        ],
    ],
],

// Separate TCA file for tx_myext_domain_model_slide
// Separate SQL for tx_myext_domain_model_slide
```

**AFTER (Content Blocks with inline Collection):**

```yaml
# ContentBlocks/ContentElements/slider/config.yaml
name: myvendor/slider
fields:
  - identifier: slides
    type: Collection
    labelField: title
    maxitems: 10
    appearance:
      collapseAll: true
      levelLinksPosition: both
    fields:
      - identifier: title
        type: Text
      - identifier: image
        type: File
        maxitems: 1
        allowed: common-image-types
      - identifier: link
        type: Link
```

**Or with separate Record Type as child:**

```yaml
# ContentBlocks/RecordTypes/slide/config.yaml
name: myvendor/slide
table: tx_myext_domain_model_slide
labelField: title
fields:
  - identifier: title
    type: Text
  - identifier: image
    type: File
    maxitems: 1
  - identifier: link
    type: Link

# ContentBlocks/ContentElements/slider/config.yaml
name: myvendor/slider
fields:
  - identifier: slides
    type: Collection
    foreign_table: tx_myext_domain_model_slide
    shareAcrossTables: true
    shareAcrossFields: true
```

### Data Migration Script

When migrating existing content, you may need to rename columns and update CType values:

```php
<?php
// Classes/Command/MigrateToContentBlocksCommand.php
namespace MyVendor\MyExt\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

class MigrateToContentBlocksCommand extends Command
{
    protected function configure(): void
    {
        $this->setDescription('Migrate classic content elements to Content Blocks');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $connection = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getConnectionForTable('tt_content');
        
        // Step 1: Update CType from old to new
        $oldCType = 'myext_hero';
        $newCType = 'myvendor_hero';  // Content Blocks generates: vendor_name
        
        $updated = $connection->update(
            'tt_content',
            ['CType' => $newCType],
            ['CType' => $oldCType]
        );
        $output->writeln("Updated $updated records from $oldCType to $newCType");
        
        // Step 2: Rename columns if Content Blocks uses different names
        // Only needed if you used prefixFields: false and identifiers differ
        // Usually Content Blocks generates: myvendor_hero_fieldname
        
        // Example: Rename tx_myext_subheadline to myvendor_hero_subheadline
        // This requires ALTER TABLE - use Database Compare in Install Tool instead
        
        return Command::SUCCESS;
    }
}
```

### Database Column Renaming

If Content Blocks generates different column names, use the Install Tool:

1. Create the Content Block (new columns will be detected)
2. Go to Admin Tools → Maintenance → Analyze Database Structure
3. Add new columns (Content Blocks generated)
4. Run migration script to copy data:

```sql
-- Copy data from old columns to new columns
UPDATE tt_content 
SET myvendor_hero_subheadline = tx_myext_subheadline
WHERE CType = 'myvendor_hero' AND tx_myext_subheadline != '';

-- After verification, drop old columns via Install Tool
```

### Keeping Same Column Names (Recommended)

To avoid data migration, configure Content Blocks to use the same column names:

```yaml
name: myvendor/hero
prefixFields: false  # No automatic prefixing
fields:
  - identifier: tx_myext_subheadline  # Use exact old column name
    type: Text
  - identifier: tx_myext_image
    type: File
  - identifier: tx_myext_link
    type: Link
```

Or use `prefixField: false` per field:

```yaml
name: myvendor/hero
prefixFields: true  # Enable prefixing by default
fields:
  - identifier: tx_myext_subheadline
    type: Text
    prefixField: false  # Keep original column name
```

### Migration Checklist

```markdown
## Pre-Migration
- [ ] List all content elements and record types to migrate
- [ ] Document existing TCA column names
- [ ] Backup database
- [ ] Install friendsoftypo3/content-blocks

## For Each Content Type
- [ ] Create config.yaml with field mappings
- [ ] Create frontend.html template
- [ ] Create backend-preview.html (optional)
- [ ] Create labels.xlf translations
- [ ] Run cache:flush and extension:setup

## Data Migration
- [ ] Update CType values in database
- [ ] Rename columns if needed (or use prefixField: false)
- [ ] Verify data displays correctly

## Cleanup
- [ ] Remove old TCA files
- [ ] Remove ext_tables.sql (or remove migrated columns)
- [ ] Remove old TypoScript rendering config
- [ ] Remove old Fluid templates
- [ ] Update documentation
```

### Files to Delete After Migration

| Classic File | Why Remove |
|--------------|------------|
| `Configuration/TCA/*.php` | Replaced by config.yaml |
| `Configuration/TCA/Overrides/tt_content.php` | Replaced by config.yaml |
| `ext_tables.sql` | Auto-generated by Content Blocks |
| `Configuration/TypoScript/setup.typoscript` (rendering part) | Auto-registered |
| `Resources/Private/Templates/ContentElements/*.html` | Moved to ContentBlocks folder |

---

## 17. Reverting Content Blocks to Classic Extension Format

This section guides you through converting Content Blocks back to traditional TYPO3 extension format with separate TCA, SQL, and TypoScript files.

### When to Revert

| Scenario | Recommendation |
|----------|----------------|
| Content Blocks has breaking changes | ✅ Revert to classic for stability |
| Need TCA features not supported by Content Blocks | ✅ Revert for full TCA control |
| Team prefers traditional TYPO3 structure | ✅ Revert for familiarity |
| Complex Extbase domain models needed | ✅ Revert for full Extbase integration |
| Performance-critical applications | ⚠️ Consider revert (measure first) |
| Simple content elements working fine | ❌ Keep Content Blocks |

### Revert Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  1. ANALYZE                                                       │
│     └─ Document all config.yaml files and field mappings        │
├─────────────────────────────────────────────────────────────────┤
│  2. GENERATE                                                      │
│     └─ Create TCA, SQL, TypoScript from config.yaml             │
├─────────────────────────────────────────────────────────────────┤
│  3. MOVE TEMPLATES                                                │
│     └─ Move Fluid templates to traditional locations             │
├─────────────────────────────────────────────────────────────────┤
│  4. MIGRATE DATA                                                  │
│     └─ Update CTypes, rename columns if needed                   │
├─────────────────────────────────────────────────────────────────┤
│  5. REMOVE DEPENDENCY                                             │
│     └─ Uninstall Content Blocks, delete ContentBlocks folder    │
└─────────────────────────────────────────────────────────────────┘
```

### Content Blocks to TCA Field Mapping (Reverse)

| Content Blocks Type | TCA type | TCA renderType | Additional Config |
|---------------------|----------|----------------|-------------------|
| `Text` | `input` | - | `max => 255` |
| `Textarea` | `text` | - | `rows => 5` |
| `Textarea` + `enableRichtext` | `text` | - | `enableRichtext => true` |
| `Email` | `email` | - | - |
| `Link` | `link` | - | - |
| `Number` | `number` | - | `format => 'integer'` or `'decimal'` |
| `DateTime` | `datetime` | - | `format => 'date'` or `'datetime'` |
| `Color` | `color` | - | - |
| `Checkbox` | `check` | - | - |
| `Radio` | `radio` | - | `items => [...]` |
| `Slug` | `slug` | - | `generatorOptions => [...]` |
| `Password` | `password` | - | - |
| `Select` | `select` | `selectSingle` | `items => [...]` |
| `Select` + `multiple` | `select` | `selectMultipleSideBySide` | - |
| `File` | `file` | - | `allowed => '...'` |
| `Relation` | `group` or `select` | - | `foreign_table => '...'` |
| `Category` | `category` | - | - |
| `Collection` (inline) | `inline` | - | `foreign_table => '...'` |
| `Collection` (with fields) | `inline` | - | `foreign_table => auto-generated` |
| `FlexForm` | `flex` | - | `ds => [...]` |
| `Json` | `json` | - | - |
| `Tab` | - | - | `--div--;Label` in showitem |
| `Palette` | - | - | `--palette--;;name` in showitem |

### YAML Options to TCA Config Mapping

| Content Blocks YAML | TCA Config Key | Example |
|---------------------|----------------|---------|
| `required: true` | `required => true` | - |
| `default: "value"` | `default => 'value'` | - |
| `placeholder: "text"` | `placeholder => 'text'` | - |
| `minitems: 1` | `minitems => 1` | - |
| `maxitems: 10` | `maxitems => 10` | - |
| `allowed: common-image-types` | `allowed => 'common-image-types'` | - |
| `displayCond: 'FIELD:x:=:1'` | `displayCond => 'FIELD:x:=:1'` | - |
| `onChange: reload` | `onChange => 'reload'` | - |
| `labelField: name` | `ctrl['label'] => 'name'` | Record Types |
| `languageAware: true` | `ctrl['languageField']` etc. | Record Types |
| `sortable: true` | `ctrl['sortby'] => 'sorting'` | Record Types |
| `softDelete: true` | `ctrl['delete'] => 'deleted'` | Record Types |

### Revert Example 1: Content Element

**BEFORE (Content Blocks):**

```yaml
# ContentBlocks/ContentElements/hero/config.yaml
name: myvendor/hero
basics:
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
  - identifier: hero_image
    type: File
    maxitems: 1
    allowed: common-image-types
  - identifier: cta_link
    type: Link
  - identifier: cta_text
    type: Text
```

**AFTER (Classic):**

**Step 1: Create TCA Override**

```php
<?php
// Configuration/TCA/Overrides/tt_content.php

use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;

defined('TYPO3') or die();

// Register the content element
ExtensionManagementUtility::addPlugin(
    [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:ce.hero.title',
        'value' => 'myext_hero',
        'icon' => 'EXT:my_ext/Resources/Public/Icons/ContentElements/hero.svg',
        'group' => 'default',
        'description' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:ce.hero.description',
    ],
    'CType',
    'my_ext'
);

// Define columns
$tempColumns = [
    'tx_myext_subheadline' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.subheadline',
        'config' => [
            'type' => 'input',
            'size' => 50,
            'max' => 255,
        ],
    ],
    'tx_myext_hero_image' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.hero_image',
        'config' => [
            'type' => 'file',
            'maxitems' => 1,
            'allowed' => 'common-image-types',
        ],
    ],
    'tx_myext_cta_link' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.cta_link',
        'config' => [
            'type' => 'link',
        ],
    ],
    'tx_myext_cta_text' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.cta_text',
        'config' => [
            'type' => 'input',
            'size' => 30,
            'max' => 100,
        ],
    ],
];

ExtensionManagementUtility::addTCAcolumns('tt_content', $tempColumns);

// Define showitem
$GLOBALS['TCA']['tt_content']['types']['myext_hero'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            tx_myext_subheadline,
            tx_myext_hero_image,
            tx_myext_cta_link,
            tx_myext_cta_text,
        --div--;LLL:EXT:frontend/Resources/Private/Language/locallang_ttc.xlf:tabs.appearance,
            --palette--;;frames,
            --palette--;;appearanceLinks,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
            --palette--;;access,
    ',
];
```

**Step 2: Create SQL Schema**

```sql
-- ext_tables.sql
CREATE TABLE tt_content (
    tx_myext_subheadline varchar(255) DEFAULT '' NOT NULL,
    tx_myext_hero_image int(11) unsigned DEFAULT 0 NOT NULL,
    tx_myext_cta_link varchar(1024) DEFAULT '' NOT NULL,
    tx_myext_cta_text varchar(100) DEFAULT '' NOT NULL
);
```

**Step 3: Create TypoScript Rendering**

```typoscript
# Configuration/TypoScript/setup.typoscript
tt_content.myext_hero = FLUIDTEMPLATE
tt_content.myext_hero {
    templateName = Hero
    templateRootPaths {
        10 = EXT:my_ext/Resources/Private/Templates/ContentElements/
    }
    partialRootPaths {
        10 = EXT:my_ext/Resources/Private/Partials/
    }
    layoutRootPaths {
        10 = EXT:my_ext/Resources/Private/Layouts/
    }
    dataProcessing {
        10 = TYPO3\CMS\Frontend\DataProcessing\FilesProcessor
        10 {
            references.fieldName = tx_myext_hero_image
            as = heroImages
        }
    }
}
```

**Step 4: Move/Update Fluid Template**

```html
<!-- Resources/Private/Templates/ContentElements/Hero.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default"/>
<f:section name="Main">
    <section class="hero-banner">
        <f:if condition="{heroImages}">
            <f:for each="{heroImages}" as="image">
                <f:image image="{image}" alt="{data.header}" class="hero-image"/>
            </f:for>
        </f:if>
        
        <div class="hero-content">
            <h1>{data.header}</h1>
            <f:if condition="{data.tx_myext_subheadline}">
                <p class="subheadline">{data.tx_myext_subheadline}</p>
            </f:if>
            
            <f:if condition="{data.tx_myext_cta_link}">
                <f:link.typolink parameter="{data.tx_myext_cta_link}" class="btn btn-primary">
                    {data.tx_myext_cta_text -> f:or(default: 'Learn more')}
                </f:link.typolink>
            </f:if>
        </div>
    </section>
</f:section>
</html>
```

**Step 5: Create Translation File**

```xml
<!-- Resources/Private/Language/locallang.xlf -->
<?xml version="1.0" encoding="utf-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
    <file source-language="en" datatype="plaintext" original="messages">
        <body>
            <trans-unit id="ce.hero.title">
                <source>Hero Banner</source>
            </trans-unit>
            <trans-unit id="ce.hero.description">
                <source>A full-width hero banner with image and CTA</source>
            </trans-unit>
            <trans-unit id="field.subheadline">
                <source>Subheadline</source>
            </trans-unit>
            <trans-unit id="field.hero_image">
                <source>Hero Image</source>
            </trans-unit>
            <trans-unit id="field.cta_link">
                <source>CTA Link</source>
            </trans-unit>
            <trans-unit id="field.cta_text">
                <source>Button Text</source>
            </trans-unit>
        </body>
    </file>
</xliff>
```

### Revert Example 2: Record Type

**BEFORE (Content Blocks):**

```yaml
# ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_myext_domain_model_teammember
labelField: name
fallbackLabelFields:
  - email
languageAware: true
workspaceAware: false
sortable: true
softDelete: true
trackCreationDate: true
trackUpdateDate: true
restriction:
  disabled: true
  startTime: true
  endTime: true
security:
  ignorePageTypeRestriction: true
fields:
  - identifier: name
    type: Text
    required: true
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: bio
    type: Textarea
    enableRichtext: true
  - identifier: photo
    type: File
    allowed: common-image-types
    maxitems: 1
```

**AFTER (Classic):**

**Step 1: Create Full TCA Configuration**

```php
<?php
// Configuration/TCA/tx_myext_domain_model_teammember.php

return [
    'ctrl' => [
        'title' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_teammember',
        'label' => 'name',
        'label_alt' => 'email',
        'label_alt_force' => false,
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'sortby' => 'sorting',
        'languageField' => 'sys_language_uid',
        'transOrigPointerField' => 'l10n_parent',
        'transOrigDiffSourceField' => 'l10n_diffsource',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        'security' => [
            'ignorePageTypeRestriction' => true,
        ],
        'iconfile' => 'EXT:my_ext/Resources/Public/Icons/tx_myext_domain_model_teammember.svg',
        'searchFields' => 'name,email,position',
    ],
    'columns' => [
        'sys_language_uid' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.language',
            'config' => [
                'type' => 'language',
            ],
        ],
        'l10n_parent' => [
            'displayCond' => 'FIELD:sys_language_uid:>:0',
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.l18n_parent',
            'config' => [
                'type' => 'select',
                'renderType' => 'selectSingle',
                'items' => [
                    ['label' => '', 'value' => 0],
                ],
                'foreign_table' => 'tx_myext_domain_model_teammember',
                'foreign_table_where' => 'AND {#tx_myext_domain_model_teammember}.{#pid}=###CURRENT_PID### AND {#tx_myext_domain_model_teammember}.{#sys_language_uid} IN (-1,0)',
                'default' => 0,
            ],
        ],
        'l10n_diffsource' => [
            'config' => [
                'type' => 'passthrough',
            ],
        ],
        'hidden' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.hidden',
            'config' => [
                'type' => 'check',
                'renderType' => 'checkboxToggle',
            ],
        ],
        'starttime' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.starttime',
            'config' => [
                'type' => 'datetime',
                'default' => 0,
            ],
        ],
        'endtime' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.endtime',
            'config' => [
                'type' => 'datetime',
                'default' => 0,
                'range' => [
                    'upper' => mktime(0, 0, 0, 1, 1, 2038),
                ],
            ],
        ],
        'name' => [
            'exclude' => false,
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_teammember.name',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
                'required' => true,
            ],
        ],
        'position' => [
            'exclude' => true,
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_teammember.position',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
            ],
        ],
        'email' => [
            'exclude' => true,
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_teammember.email',
            'config' => [
                'type' => 'email',
            ],
        ],
        'bio' => [
            'exclude' => true,
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_teammember.bio',
            'config' => [
                'type' => 'text',
                'enableRichtext' => true,
            ],
        ],
        'photo' => [
            'exclude' => true,
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_teammember.photo',
            'config' => [
                'type' => 'file',
                'maxitems' => 1,
                'allowed' => 'common-image-types',
            ],
        ],
    ],
    'types' => [
        '1' => [
            'showitem' => '
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
                    name, position, email, bio, photo,
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:language,
                    sys_language_uid, l10n_parent,
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
                    hidden, starttime, endtime
            ',
        ],
    ],
];
```

**Step 2: Create SQL Schema**

```sql
-- ext_tables.sql
CREATE TABLE tx_myext_domain_model_teammember (
    name varchar(255) DEFAULT '' NOT NULL,
    position varchar(255) DEFAULT '' NOT NULL,
    email varchar(255) DEFAULT '' NOT NULL,
    bio text,
    photo int(11) unsigned DEFAULT 0 NOT NULL
);
```

**Step 3: Register Table (if needed)**

```php
<?php
// Configuration/TCA/Overrides/sys_template.php or ext_tables.php

// Allow on standard pages
\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::allowTableOnStandardPages(
    'tx_myext_domain_model_teammember'
);
```

### Revert Example 3: Collection/IRRE to Inline

**BEFORE (Content Blocks with inline Collection):**

```yaml
# ContentBlocks/ContentElements/accordion/config.yaml
name: myvendor/accordion
fields:
  - identifier: items
    type: Collection
    labelField: title
    minitems: 1
    maxitems: 20
    appearance:
      collapseAll: true
      levelLinksPosition: both
    fields:
      - identifier: title
        type: Text
        required: true
      - identifier: content
        type: Textarea
        enableRichtext: true
      - identifier: is_open
        type: Checkbox
```

**AFTER (Classic with IRRE):**

**Step 1: Create Parent TCA (tt_content override)**

```php
<?php
// Configuration/TCA/Overrides/tt_content.php

use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;

defined('TYPO3') or die();

ExtensionManagementUtility::addPlugin(
    [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:ce.accordion.title',
        'value' => 'myext_accordion',
        'icon' => 'EXT:my_ext/Resources/Public/Icons/ContentElements/accordion.svg',
        'group' => 'default',
    ],
    'CType',
    'my_ext'
);

$tempColumns = [
    'tx_myext_accordion_items' => [
        'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:field.accordion_items',
        'config' => [
            'type' => 'inline',
            'foreign_table' => 'tx_myext_domain_model_accordionitem',
            'foreign_field' => 'parent_uid',
            'foreign_table_field' => 'parent_table',
            'minitems' => 1,
            'maxitems' => 20,
            'appearance' => [
                'collapseAll' => true,
                'levelLinksPosition' => 'both',
                'useSortable' => true,
                'showPossibleLocalizationRecords' => true,
                'showAllLocalizationLink' => true,
                'showSynchronizationLink' => true,
            ],
        ],
    ],
];

ExtensionManagementUtility::addTCAcolumns('tt_content', $tempColumns);

$GLOBALS['TCA']['tt_content']['types']['myext_accordion'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            tx_myext_accordion_items,
        --div--;LLL:EXT:frontend/Resources/Private/Language/locallang_ttc.xlf:tabs.appearance,
            --palette--;;frames,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
            --palette--;;access,
    ',
];
```

**Step 2: Create Child Table TCA**

```php
<?php
// Configuration/TCA/tx_myext_domain_model_accordionitem.php

return [
    'ctrl' => [
        'title' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_accordionitem',
        'label' => 'title',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'sortby' => 'sorting',
        'hideTable' => true,  // Hide from list module (child records only)
        'enablecolumns' => [
            'disabled' => 'hidden',
        ],
        'iconfile' => 'EXT:my_ext/Resources/Public/Icons/accordion-item.svg',
    ],
    'columns' => [
        'hidden' => [
            'exclude' => true,
            'label' => 'LLL:EXT:core/Resources/Private/Language/locallang_general.xlf:LGL.hidden',
            'config' => [
                'type' => 'check',
                'renderType' => 'checkboxToggle',
            ],
        ],
        'parent_uid' => [
            'config' => [
                'type' => 'passthrough',
            ],
        ],
        'parent_table' => [
            'config' => [
                'type' => 'passthrough',
            ],
        ],
        'title' => [
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_accordionitem.title',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
                'required' => true,
            ],
        ],
        'content' => [
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_accordionitem.content',
            'config' => [
                'type' => 'text',
                'enableRichtext' => true,
            ],
        ],
        'is_open' => [
            'label' => 'LLL:EXT:my_ext/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_accordionitem.is_open',
            'config' => [
                'type' => 'check',
                'renderType' => 'checkboxToggle',
            ],
        ],
    ],
    'types' => [
        '1' => [
            'showitem' => 'hidden, title, content, is_open',
        ],
    ],
];
```

**Step 3: Create SQL for Both Tables**

```sql
-- ext_tables.sql
CREATE TABLE tt_content (
    tx_myext_accordion_items int(11) unsigned DEFAULT 0 NOT NULL
);

CREATE TABLE tx_myext_domain_model_accordionitem (
    parent_uid int(11) unsigned DEFAULT 0 NOT NULL,
    parent_table varchar(255) DEFAULT '' NOT NULL,
    title varchar(255) DEFAULT '' NOT NULL,
    content text,
    is_open smallint(5) unsigned DEFAULT 0 NOT NULL
);
```

**Step 4: Create TypoScript with Data Processing**

```typoscript
# Configuration/TypoScript/setup.typoscript
tt_content.myext_accordion = FLUIDTEMPLATE
tt_content.myext_accordion {
    templateName = Accordion
    templateRootPaths.10 = EXT:my_ext/Resources/Private/Templates/ContentElements/
    partialRootPaths.10 = EXT:my_ext/Resources/Private/Partials/
    layoutRootPaths.10 = EXT:my_ext/Resources/Private/Layouts/
    
    dataProcessing {
        10 = TYPO3\CMS\Frontend\DataProcessing\DatabaseQueryProcessor
        10 {
            table = tx_myext_domain_model_accordionitem
            pidInList.field = pid
            where.field = uid
            where.intval = 1
            where.wrap = parent_uid=|
            orderBy = sorting
            as = accordionItems
        }
    }
}
```

**Step 5: Update Fluid Template**

```html
<!-- Resources/Private/Templates/ContentElements/Accordion.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default"/>
<f:section name="Main">
    <div class="accordion" id="accordion-{data.uid}">
        <f:for each="{accordionItems}" as="item" iteration="iter">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button{f:if(condition: '!{item.is_open}', then: ' collapsed')}"
                            type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#collapse-{item.uid}">
                        {item.title}
                    </button>
                </h2>
                <div id="collapse-{item.uid}"
                     class="accordion-collapse collapse{f:if(condition: '{item.is_open}', then: ' show')}">
                    <div class="accordion-body">
                        <f:format.html>{item.content}</f:format.html>
                    </div>
                </div>
            </div>
        </f:for>
    </div>
</f:section>
</html>
```

### Data Migration Script (Revert Direction)

```php
<?php
// Classes/Command/RevertFromContentBlocksCommand.php
namespace MyVendor\MyExt\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

#[AsCommand(
    name: 'myext:revert-content-blocks',
    description: 'Revert Content Blocks elements to classic TCA format'
)]
class RevertFromContentBlocksCommand extends Command
{
    private const CTYPE_MAPPING = [
        // Content Blocks CType => Classic CType
        'myvendor_hero' => 'myext_hero',
        'myvendor_accordion' => 'myext_accordion',
    ];

    private const COLUMN_MAPPING = [
        // Content Blocks column => Classic column
        'myvendor_hero_subheadline' => 'tx_myext_subheadline',
        'myvendor_hero_hero_image' => 'tx_myext_hero_image',
        'myvendor_hero_cta_link' => 'tx_myext_cta_link',
        'myvendor_hero_cta_text' => 'tx_myext_cta_text',
    ];

    protected function configure(): void
    {
        $this
            ->addOption('dry-run', null, InputOption::VALUE_NONE, 'Show what would be changed without making changes')
            ->addOption('copy-data', null, InputOption::VALUE_NONE, 'Copy data from old columns to new columns');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        $dryRun = $input->getOption('dry-run');
        $copyData = $input->getOption('copy-data');

        $connection = GeneralUtility::makeInstance(ConnectionPool::class)
            ->getConnectionForTable('tt_content');

        $io->title('Reverting Content Blocks to Classic Format');

        if ($dryRun) {
            $io->warning('DRY RUN - No changes will be made');
        }

        // Step 1: Update CTypes
        $io->section('Updating CType values');
        foreach (self::CTYPE_MAPPING as $oldCType => $newCType) {
            $count = $connection->count('*', 'tt_content', ['CType' => $oldCType]);
            $io->writeln("  $oldCType → $newCType: $count records");
            
            if (!$dryRun && $count > 0) {
                $connection->update('tt_content', ['CType' => $newCType], ['CType' => $oldCType]);
            }
        }

        // Step 2: Copy column data (if requested and columns exist)
        if ($copyData) {
            $io->section('Copying column data');
            foreach (self::COLUMN_MAPPING as $oldColumn => $newColumn) {
                $io->writeln("  $oldColumn → $newColumn");
                if (!$dryRun) {
                    // Check if both columns exist before copying
                    try {
                        $connection->executeStatement(
                            "UPDATE tt_content SET $newColumn = $oldColumn WHERE $oldColumn IS NOT NULL AND $oldColumn != ''"
                        );
                    } catch (\Exception $e) {
                        $io->warning("Column copy failed: " . $e->getMessage());
                    }
                }
            }
        }

        $io->success($dryRun ? 'Dry run completed' : 'Migration completed successfully');
        
        if (!$dryRun) {
            $io->note([
                'Next steps:',
                '1. Run: ddev typo3 cache:flush',
                '2. Verify content displays correctly',
                '3. Remove old Content Blocks columns via Install Tool',
                '4. Remove friendsoftypo3/content-blocks dependency',
            ]);
        }

        return Command::SUCCESS;
    }
}
```

### Files to Create When Reverting

| New File (Classic) | Replaces (Content Blocks) |
|--------------------|---------------------------|
| `Configuration/TCA/Overrides/tt_content.php` | `ContentBlocks/ContentElements/*/config.yaml` |
| `Configuration/TCA/tx_*_domain_model_*.php` | `ContentBlocks/RecordTypes/*/config.yaml` |
| `ext_tables.sql` | Auto-generated schema |
| `Configuration/TypoScript/setup.typoscript` | Auto-registered rendering |
| `Resources/Private/Templates/ContentElements/*.html` | `ContentBlocks/*/templates/frontend.html` |
| `Resources/Private/Language/locallang.xlf` | `ContentBlocks/*/language/labels.xlf` |
| `Resources/Public/Icons/*.svg` | `ContentBlocks/*/assets/icon.svg` |

### Complete Revert Checklist

```markdown
## Pre-Revert
- [ ] Document all Content Blocks config.yaml files
- [ ] Map field identifiers to TCA column names
- [ ] Backup database
- [ ] Create branch for revert work

## For Each Content Type
- [ ] Create TCA PHP file(s)
- [ ] Add columns to ext_tables.sql
- [ ] Create TypoScript rendering
- [ ] Move/update Fluid templates (update variable names!)
- [ ] Move translations to locallang.xlf
- [ ] Move icons to Resources/Public/Icons/

## Data Migration
- [ ] Update CType values in database
- [ ] Copy data from Content Blocks columns to classic columns
- [ ] Test data displays correctly
- [ ] Verify file relations work

## Cleanup
- [ ] Remove ContentBlocks folder
- [ ] Remove friendsoftypo3/content-blocks from composer.json
- [ ] Run: composer update
- [ ] Remove old columns via Install Tool (after verification)
- [ ] Clear all caches

## Testing
- [ ] All content elements render correctly
- [ ] All record types editable in backend
- [ ] File relations display correctly
- [ ] Translations work
- [ ] No PHP errors in log
```

### Template Variable Changes

When reverting, update Fluid template variable names:

| Content Blocks | Classic |
|----------------|---------|
| `{data.fieldname}` | `{data.tx_myext_fieldname}` |
| `{data.my_image}` → auto-resolved | Use DataProcessor + `{processedImages}` |
| `{data.collection_items}` → auto-resolved | Use DatabaseQueryProcessor + `{items}` |
| `{cb:assetPath()}` | Static path: `EXT:my_ext/Resources/Public/...` |
| `{cb:languagePath()}` | `LLL:EXT:my_ext/Resources/Private/Language/locallang.xlf:` |

### Removing Content Blocks Dependency

```bash
# After successful revert and testing
ddev composer remove friendsoftypo3/content-blocks

# Clear caches
ddev typo3 cache:flush

# Update database (remove orphaned columns)
# Go to Admin Tools → Maintenance → Analyze Database Structure
# Select "Remove" for the old Content Blocks columns
```

---

## 18. Package Management for v14 Compatibility

If extensions don't support TYPO3 v14 yet, fork and update:

```bash
# Add private fork as VCS repository in composer.json
# Then update extension for v14 using typo3-rector and typo3-update skills
```

Required private forks for webconsulting stack:
- `webprofil/wp-t3monitoring-client` (^13 → ^14)
- `webprofil/deployer` (^13 → ^14)
- `webprofil/crawler` (^1.0 → compatible with v14)
- `webprofil/make` (^1.1 → compatible with v14)

---

## References

- [Content Blocks Documentation](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/)
- [YAML Reference](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/YamlReference/Index.html)
- [Field Types](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/YamlReference/FieldTypes/Index.html)
- [Record Types API](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/API/RecordTypes/Index.html)
- [Packagist: friendsoftypo3/content-blocks](https://packagist.org/packages/friendsoftypo3/content-blocks)

---

## Credits & Attribution

This skill incorporates information from the official Content Blocks documentation maintained by the **TYPO3 Content Types Team** and **Friends of TYPO3**.

Original documentation: https://docs.typo3.org/p/friendsoftypo3/content-blocks/

Adapted by webconsulting.at for this skill collection
