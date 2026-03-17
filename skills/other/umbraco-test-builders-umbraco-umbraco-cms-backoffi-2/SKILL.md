---
name: umbraco-test-builders
description: JsonModels.Builders for creating test data in Umbraco tests
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Test Builders

## What is it?

The `@umbraco/json-models-builders` package provides fluent builder classes for creating Umbraco backoffice models. These builders simplify test data creation with sensible defaults and chainable configuration methods.

## Documentation

- **Package**: `@umbraco/json-models-builders`
- **Repository**: https://github.com/umbraco/Umbraco.JsonModels.Builders
- **Reference**: `/Users/philw/Projects/Umbraco.JsonModels.Builders`

## Related Skills

- **umbraco-testing** - Master skill for testing overview
- **umbraco-e2e-testing** - E2E testing (primary user of builders)
- **umbraco-msw-testing** - MSW testing (can use builders for mock data)

---

## Installation

```bash
npm install @umbraco/json-models-builders
```

---

## Builder Pattern

All builders follow this pattern:

```typescript
const model = new SomeBuilder()
  .withProperty(value)        // Configure scalar properties
  .withOtherProperty(value)   // Chain multiple configurations
  .addChild()                 // Create nested builder
    .withChildProperty(value)
    .done()                   // Return to parent builder
  .build();                   // Generate final object
```

### Method Types

| Method Pattern | Purpose | Returns |
|----------------|---------|---------|
| `withXxx(value)` | Set a property | `this` (for chaining) |
| `addXxx()` | Add nested builder | Child builder |
| `done()` | Return to parent | Parent builder |
| `build()` | Generate final object | The model |

---

## Core Builders

### DocumentTypeBuilder

Create document types with properties, groups, and tabs:

```typescript
import { DocumentTypeBuilder } from '@umbraco/json-models-builders';

const documentType = new DocumentTypeBuilder()
  .withName('Article')
  .withAlias('article')
  .withAllowAsRoot(true)
  .withAllowCultureVariation(true)
  .addGroup()
    .withName('Content')
    .addTextBoxProperty()
      .withLabel('Title')
      .withAlias('title')
      .done()
    .addRichTextProperty()
      .withLabel('Body')
      .withAlias('body')
      .done()
    .done()
  .addGroup()
    .withName('SEO')
    .addTextBoxProperty()
      .withLabel('Meta Title')
      .withAlias('metaTitle')
      .done()
    .done()
  .build();
```

**Key Methods**:
- `withName(name)` - Document type name
- `withAlias(alias)` - Document type alias
- `withAllowAsRoot(bool)` - Allow at content root
- `withAllowCultureVariation(bool)` - Enable variants
- `AsElementType()` - Mark as element type (for blocks)
- `addGroup()` - Add property group
- `addTab()` - Add tab
- `withDefaultTemplate(template)` - Set default template

### ContentBuilder

Create content items:

```typescript
import { ContentBuilder } from '@umbraco/json-models-builders';

const content = new ContentBuilder()
  .withContentTypeAlias('article')
  .withAction('publishNew')
  .withParent('-1') // Root
  .addVariant()
    .withName('My Article')
    .withCulture('en-US')
    .addProperty()
      .withAlias('title')
      .withValue('Hello World')
      .done()
    .addProperty()
      .withAlias('body')
      .withValue('<p>Article content</p>')
      .done()
    .done()
  .build();
```

**Key Methods**:
- `withContentTypeAlias(alias)` - Document type alias
- `withTemplateAlias(alias)` - Template alias
- `withAction(action)` - 'publishNew', 'save', etc.
- `withParent(parentId)` - Parent node ID
- `addVariant()` - Add content variant

### MediaBuilder

Create media items:

```typescript
import { MediaBuilder } from '@umbraco/json-models-builders';

const media = new MediaBuilder()
  .withName('My Image')
  .withMediaTypeAlias('Image')
  .addProperty()
    .withAlias('umbracoFile')
    .withValue({ src: '/media/image.jpg' })
    .done()
  .build();
```

### DataTypeBuilder

Create data types:

```typescript
import { DataTypeBuilder } from '@umbraco/json-models-builders';

const dataType = new DataTypeBuilder()
  .withName('My Text Box')
  .withSaveNewAction()
  .build();
```

---

## Property Builders

Add properties to document types:

### TextBox Property

```typescript
documentTypeBuilder
  .addGroup()
    .withName('Content')
    .addTextBoxProperty()
      .withLabel('Title')
      .withAlias('title')
      .withDescription('Enter the page title')
      .withMandatory(true)
      .done()
    .done()
```

### Rich Text Property

```typescript
.addRichTextProperty()
  .withLabel('Body Text')
  .withAlias('bodyText')
  .done()
```

### Media Picker Property

```typescript
.addMediaPickerProperty()
  .withLabel('Featured Image')
  .withAlias('featuredImage')
  .done()
```

### Content Picker Property

```typescript
.addContentPickerProperty()
  .withLabel('Related Page')
  .withAlias('relatedPage')
  .done()
```

### Custom Data Type Property

```typescript
.addCustomProperty()
  .withLabel('Custom Field')
  .withAlias('customField')
  .withDataTypeId('your-datatype-id')
  .done()
```

---

## Block List / Block Grid Builders

### BlockListDataTypeBuilder

```typescript
import { BlockListDataTypeBuilder } from '@umbraco/json-models-builders';

const blockList = new BlockListDataTypeBuilder()
  .withName('Content Blocks')
  .addBlock()
    .withContentElementTypeKey('hero-block-key')
    .withLabel('Hero Block')
    .done()
  .addBlock()
    .withContentElementTypeKey('text-block-key')
    .withLabel('Text Block')
    .done()
  .withMin(1)
  .withMax(10)
  .withUseLiveEditing(true)
  .build();
```

### BlockGridDataTypeBuilder

```typescript
import { BlockGridDataTypeBuilder } from '@umbraco/json-models-builders';

const blockGrid = new BlockGridDataTypeBuilder()
  .withName('Page Grid')
  .withGridColumns(12)
  .addBlock()
    .withContentElementTypeKey('row-block-key')
    .withLabel('Row')
    .withColumnSpanOptions([6, 12])
    .done()
  .addBlock()
    .withContentElementTypeKey('image-block-key')
    .withLabel('Image')
    .done()
  .build();
```

### BlockListValueBuilder (for content)

```typescript
import { ContentBuilder, BlockListValueBuilder } from '@umbraco/json-models-builders';

const content = new ContentBuilder()
  .withContentTypeAlias('page')
  .addVariant()
    .withName('Home')
    .addProperty()
      .withAlias('blocks')
      .addBlockListValue()
        .addBlockListEntry()
          .withContentTypeKey('hero-block-key')
          .appendContentProperties('heading', 'Welcome')
          .appendContentProperties('subheading', 'To our site')
          .done()
        .addBlockListEntry()
          .withContentTypeKey('text-block-key')
          .appendContentProperties('text', 'Some content here')
          .done()
        .done()
      .done()
    .done()
  .build();
```

---

## User and Permission Builders

### UserBuilder

```typescript
import { UserBuilder } from '@umbraco/json-models-builders';

const user = new UserBuilder()
  .withName('Test User')
  .withEmail('test@example.com')
  .withUserGroups(['admin'])
  .build();
```

### UserGroupBuilder

```typescript
import { UserGroupBuilder } from '@umbraco/json-models-builders';

const userGroup = new UserGroupBuilder()
  .withName('Editors')
  .withAlias('editors')
  .withIcon('icon-users')
  .appendSection('content')
  .appendSection('media')
  .addDefaultPermissions()
    .withBrowseNode()
    .withCreate()
    .withUpdate()
    .withPublish()
    .done()
  .withSaveNew()
  .build();
```

### PermissionsBuilder

```typescript
userGroupBuilder
  .addNodePermissions()
    .forNode('content-node-id')
    .withBrowseNode()
    .withCreate()
    .withUpdate()
    .withDelete()
    .withPublish()
    .withUnpublish()
    .done()
```

---

## Template and Code Builders

### TemplateBuilder

```typescript
import { TemplateBuilder } from '@umbraco/json-models-builders';

const template = new TemplateBuilder()
  .withName('Article Template')
  .withAlias('articleTemplate')
  .withContent(`@inherits Umbraco.Cms.Web.Common.Views.UmbracoViewPage
<h1>@Model.Name</h1>`)
  .build();
```

### StylesheetBuilder

```typescript
import { StylesheetBuilder } from '@umbraco/json-models-builders';

const stylesheet = new StylesheetBuilder()
  .withName('main.css')
  .withContent('body { font-family: sans-serif; }')
  .build();
```

### ScriptBuilder

```typescript
import { ScriptBuilder } from '@umbraco/json-models-builders';

const script = new ScriptBuilder()
  .withName('main.js')
  .withContent('console.log("Hello");')
  .build();
```

---

## AliasHelper Utility

Generate safe aliases from names:

```typescript
import { AliasHelper } from '@umbraco/json-models-builders';

// Convert to camelCase alias
AliasHelper.toAlias('My Page Type');
// Returns: "myPageType"

// Create safe alias with prefix/suffix
AliasHelper.toSafeAlias('My Page Type');
// Returns: "aMyPageTypea"

// Capitalize first character
AliasHelper.capitalize('hello');
// Returns: "Hello"

// Convert sentence to camelCase
AliasHelper.toCamelCase('My Awesome Example');
// Returns: "myAwesomeExample"

// Convert UUID to alias (removes dashes)
AliasHelper.uuidToAlias('123e4567-e89b-12d3-a456-426614174000');
// Returns: "123e4567e89b12d3a456426614174000"
```

---

## Complete Examples

### Create Document Type with Properties

```typescript
import { DocumentTypeBuilder, AliasHelper } from '@umbraco/json-models-builders';

const name = 'Blog Post';
const alias = AliasHelper.toAlias(name);

const blogPost = new DocumentTypeBuilder()
  .withName(name)
  .withAlias(alias)
  .withAllowAsRoot(true)
  .withAllowCultureVariation(true)
  .addGroup()
    .withName('Content')
    .addTextBoxProperty()
      .withLabel('Title')
      .withAlias('title')
      .withMandatory(true)
      .done()
    .addTextBoxProperty()
      .withLabel('Author')
      .withAlias('author')
      .done()
    .addRichTextProperty()
      .withLabel('Body')
      .withAlias('body')
      .done()
    .done()
  .addGroup()
    .withName('Media')
    .addMediaPickerProperty()
      .withLabel('Featured Image')
      .withAlias('featuredImage')
      .done()
    .done()
  .build();

// Use in test
await umbracoApi.documentType.save(blogPost);
```

### Create Element Type for Blocks

```typescript
const heroBlock = new DocumentTypeBuilder()
  .withName('Hero Block')
  .withAlias('heroBlock')
  .AsElementType() // Important for blocks!
  .addGroup()
    .withName('Content')
    .addTextBoxProperty()
      .withLabel('Heading')
      .withAlias('heading')
      .done()
    .addTextBoxProperty()
      .withLabel('Subheading')
      .withAlias('subheading')
      .done()
    .addMediaPickerProperty()
      .withLabel('Background Image')
      .withAlias('backgroundImage')
      .done()
    .done()
  .build();
```

### Create Content with Block List

```typescript
const pageContent = new ContentBuilder()
  .withContentTypeAlias('landingPage')
  .withAction('publishNew')
  .addVariant()
    .withName('Landing Page')
    .addProperty()
      .withAlias('pageTitle')
      .withValue('Welcome')
      .done()
    .addProperty()
      .withAlias('contentBlocks')
      .addBlockListValue()
        .addBlockListEntry()
          .withContentTypeKey(heroBlockKey)
          .appendContentProperties('heading', 'Welcome to Our Site')
          .appendContentProperties('subheading', 'Discover what we offer')
          .done()
        .addBlockListEntry()
          .withContentTypeKey(textBlockKey)
          .appendContentProperties('text', '<p>More content here...</p>')
          .done()
        .done()
      .done()
    .done()
  .build();
```

---

## All Available Builders (67 Total)

### Main Builders
- DocumentTypeBuilder, ContentBuilder, MediaBuilder
- TemplateBuilder, StylesheetBuilder, ScriptBuilder
- DataTypeBuilder, MacroBuilder, PackageBuilder
- UserBuilder, UserGroupBuilder
- PartialViewBuilder, PartialViewMacroBuilder
- DomainBuilder, WebhookBuilder

### Data Type Builders
- TextBoxDataTypeBuilder, DropDownDataTypeBuilder
- LabelDataTypeBuilder, SliderDataTypeBuilder
- BlockListDataTypeBuilder, BlockGridDataTypeBuilder
- GridDataTypeBuilder, CheckBoxListDataTypeBuilder
- ApprovedColorPickerDataTypeBuilder, FormPickerDataTypeBuilder

### Property Builders
- TextBoxDocumentTypePropertyBuilder
- RichTextDocumentTypePropertyEditor
- MediaPickerDocumentTypePropertyBuilder
- ContentPickerPropertyBuilder
- UrlPickerPropertyBuilder
- DropDownDocumentTypePropertyBuilder
- CustomDocumentTypePropertyBuilder

### Block Builders
- BlockListValueBuilder, BlockListEntryBuilder
- BlockGridValueBuilder, BlockGridEntryBuilder
- BlockGridLayoutBuilder, BlockGridAreaBuilder
- BlockGridItemsBuilder, BlockGridBlocksBuilder

### Permission Builders
- PermissionsBuilder, NodePermissionBuilder
- NodePermissionCollectionBuilder

### Other Builders
- DocumentTypeGroupBuilder, DocumentTypeTabBuilder
- ContentVariantBuilder, ContentVariantPropertyBuilder
- MediaFileBuilder, MediaPropertyBuilder
- WebhookEventBuilder, WebhookHeaderBuilder
- GridLayoutBuilder, GridRowConfigBuilder, GridAreaBuilder
