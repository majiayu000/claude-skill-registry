---
name: umbraco-playwright-testhelpers
description: Reference for @umbraco/playwright-testhelpers package - fixtures, API helpers, and UI helpers for E2E testing
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Playwright Testhelpers

## What is it?

`@umbraco/playwright-testhelpers` is the official Umbraco package that provides Playwright fixtures, API helpers, and UI helpers for writing E2E tests against an Umbraco backoffice instance.

**Repository**: https://github.com/umbraco/Umbraco.Playwright.Testhelpers

## Installation

```bash
npm install @umbraco/playwright-testhelpers --save-dev
```

## Related Skills

- **umbraco-e2e-testing** - E2E test patterns using these helpers
- **umbraco-test-builders** - JsonModels.Builders (used internally by testhelpers)
- **umbraco-testing** - Master skill for testing overview

---

## Package Exports

The package exports these main items:

```typescript
import {
  test,              // Extended Playwright test with fixtures
  ApiHelpers,        // Direct API helper class
  UiHelpers,         // Direct UI helper class
  ConstantHelper,    // Constants for sections, actions, buttons
  AliasHelper,       // Alias generation utilities
  JsonHelper         // JSON parsing utilities
} from '@umbraco/playwright-testhelpers';
```

---

## Test Fixtures

The `test` export extends Playwright's test with two fixtures:

```typescript
import { test } from '@umbraco/playwright-testhelpers';

test('my test', async ({ umbracoApi, umbracoUi }) => {
  // umbracoApi - API helpers for fast test setup/teardown
  // umbracoUi - UI helpers for backoffice interaction
});
```

### How Fixtures Work

```typescript
// testExtension.ts (internal)
const test = base.extend<{umbracoApi: ApiHelpers} & {umbracoUi: UiHelpers}>({
  umbracoApi: async ({ page }, use) => {
    const umbracoApi = new ApiHelpers(page);
    await use(umbracoApi);
  },
  umbracoUi: async ({ page }, use) => {
    const umbracoUi = new UiHelpers(page);
    await use(umbracoUi);
  }
});
```

---

## API Helpers (umbracoApi)

The `ApiHelpers` class provides sub-helpers for each entity type:

| Property | Helper Class | Purpose |
|----------|--------------|---------|
| `content` | ContentApiHelper | Content/document operations |
| `documentTypes` | DocumentTypeApiHelper | Document type operations |
| `dataTypes` | DatatypeApiHelper | Data type operations |
| `media` | MediaApiHelper | Media operations |
| `mediaTypes` | MediaTypeApiHelper | Media type operations |
| `templates` | TemplatesApiHelper | Template operations |
| `languages` | LanguagesApiHelper | Language operations |
| `users` | UserApiHelper | User operations |
| `userGroups` | UserGroupApiHelper | User group operations |
| `members` | MemberApiHelper | Member operations |
| `memberTypes` | MemberTypeApiHelper | Member type operations |
| `memberGroups` | MemberGroupApiHelper | Member group operations |
| `macros` | MacroApiHelper | Macro operations |
| `scripts` | ScriptApiHelper | Script operations |
| `stylesheets` | StylesheetApiHelper | Stylesheet operations |
| `partialViews` | PartialViewApiHelper | Partial view operations |
| `relationTypes` | RelationTypeApiHelper | Relation type operations |
| `packages` | PackageApiHelper | Package operations |
| `domain` | DomainApiHelper | Domain operations |
| `translation` | TranslationApiHelper | Translation operations |
| `webhook` | WebhookApiHelper | Webhook operations |

### Core API Methods

```typescript
// Base HTTP methods (available on umbracoApi directly)
await umbracoApi.get(url, params?);
await umbracoApi.post(url, data?);
await umbracoApi.delete(url, data?);

// CSRF token (automatically handled)
await umbracoApi.getCsrfToken();

// Login
await umbracoApi.login(skipCheckTours?: boolean);
```

---

## Document Type API Helper

```typescript
// Ensure cleanup (idempotent - won't fail if not exists)
await umbracoApi.documentTypes.ensureNameNotExists('MyDocType');

// Create default document type
const docType = await umbracoApi.documentTypes.createDefaultDocumentType('MyDocType');

// Create element type (for blocks)
const elementType = await umbracoApi.documentTypes.createDefaultElementType('MyElement', 'myElement');

// Create document type with block grid
const element = await umbracoApi.documentTypes.createDefaultDocumentWithBlockGridEditor(element?, dataType?);

// Save document type (using builder)
const docType = new DocumentTypeBuilder()
  .withName('MyDocType')
  .withAlias('myDocType')
  .build();
await umbracoApi.documentTypes.save(docType);
```

---

## Content API Helper

```typescript
// Reference: ContentApiHelper.ts patterns
// Note: Actual methods depend on version - check source

// Common patterns:
await umbracoApi.content.ensureNameNotExists('MyContent');
await umbracoApi.content.createDefaultContent(name, documentTypeId);
await umbracoApi.content.getByName('MyContent');
await umbracoApi.content.publish(contentId);
```

---

## Data Type API Helper

```typescript
// Get built-in data type
const dataType = await umbracoApi.dataTypes.getByName('Textstring');

// Create block grid data type
const blockGrid = await umbracoApi.dataTypes.createDefaultBlockGrid('MyBlockGrid', elementType);

// Ensure cleanup
await umbracoApi.dataTypes.ensureNameNotExists('MyDataType');
```

---

## Media API Helper

```typescript
// Create media folder
await umbracoApi.media.createDefaultMediaFolder('MyFolder');

// Create image with file
await umbracoApi.media.createImageWithFile(
  'MyImage',
  { src: '/path/to/image.jpg' },
  'image.jpg',
  '/local/path/to/image.jpg',
  'image/jpeg'
);

// Cleanup
await umbracoApi.media.ensureNameNotExists('MyImage');
await umbracoApi.media.clearRecycleBin();
```

---

## UI Helpers (umbracoUi)

### Navigation

```typescript
// Navigate to section
await umbracoUi.goToSection(ConstantHelper.sections.content);
await umbracoUi.goToSection(ConstantHelper.sections.settings);
await umbracoUi.goToSection(ConstantHelper.sections.media);

// Navigate to specific items
await umbracoUi.navigateToContent('MyContent');
await umbracoUi.navigateToMedia('MyMedia');
await umbracoUi.navigateToDocumentType('MyDocType');
await umbracoUi.navigateToDataType('MyDataType');
await umbracoUi.navigateToTemplate('MyTemplate');
```

### Tree Operations

```typescript
// Get tree item by path
const item = await umbracoUi.getTreeItem('contentTypes', ['MyFolder', 'MyDocType']);

// Refresh trees
await umbracoUi.refreshContentTree();
await umbracoUi.refreshMediaTree();

// Wait for tree load
await umbracoUi.waitForTreeLoad('settings');
```

### Click Operations

```typescript
// Click by data-element attribute
await umbracoUi.clickDataElementByElementName('tree-item-myItem');

// Click by text
await umbracoUi.clickButtonByText('Save');

// Click element
await umbracoUi.clickElement(locator);

// Click multiple elements
await umbracoUi.clickMultiple(locator);
```

### Editor Operations

```typescript
// Set header name (with alias generation wait)
await umbracoUi.setEditorHeaderName('My Document');

// Get editor header name
await umbracoUi.getEditorHeaderName('My Document');

// Add property group and editor
await umbracoUi.goToAddEditor('Content', 'Title');
```

### Locator Getters

```typescript
// Get elements
const helpButton = await umbracoUi.getGlobalHelp();
const userButton = await umbracoUi.getGlobalUser();
const element = await umbracoUi.getDataElementByElementName('my-element');
const button = await umbracoUi.getButtonByText('Save');
const button = await umbracoUi.getButtonByLabelKey('buttons_save');
const contextAction = await umbracoUi.getContextMenuAction('action-create');

// Notifications
const success = await umbracoUi.getSuccessNotification();
const error = await umbracoUi.getErrorNotification();
```

### Assertions

```typescript
// Check notifications
await umbracoUi.isSuccessNotificationVisible();
await umbracoUi.isErrorNotificationVisible();

// Check data type exists
await umbracoUi.doesDataTypeExist('MyDataType');
```

### Document Type UI

```typescript
// Create with template
await umbracoUi.createNewDocumentTypeWithTemplate();

// Update permissions
await umbracoUi.updateDocumentPermissionsToAllowCultureVariant();
```

### Content UI

```typescript
// Create content
await umbracoUi.createContentWithDocumentType('MyDocType');

// Switch culture
await umbracoUi.switchCultureInContent('Danish');
```

### File Upload

```typescript
// Upload file
await umbracoUi.fileUploader('/path/to/file.jpg');
```

### Drag and Drop

```typescript
// Drag and drop elements
await umbracoUi.dragAndDrop(
  fromLocator,
  toLocator,
  verticalOffset,
  horizontalOffset,
  steps?
);
```

---

## ConstantHelper

```typescript
import { ConstantHelper } from '@umbraco/playwright-testhelpers';

// Sections
ConstantHelper.sections.content    // "content"
ConstantHelper.sections.media      // "media"
ConstantHelper.sections.settings   // "settings"
ConstantHelper.sections.users      // "users"
ConstantHelper.sections.member     // "member"
ConstantHelper.sections.packages   // "packages"
ConstantHelper.sections.translation // "translation"

// Actions (data-element values)
ConstantHelper.actions.create      // "action-create"
ConstantHelper.actions.delete      // "action-delete"
ConstantHelper.actions.copy        // "action-copy"
ConstantHelper.actions.move        // "action-move"
ConstantHelper.actions.sort        // "action-sort"
ConstantHelper.actions.save        // "saveNew"
ConstantHelper.actions.publish     // "publishNew"
ConstantHelper.actions.documentType // "action-documentType"
ConstantHelper.actions.dataType    // "action-data-type"
ConstantHelper.actions.remove      // "actions_remove"

// Buttons (label-key values)
ConstantHelper.buttons.save           // "buttons_save"
ConstantHelper.buttons.saveAndPublish // "buttons_saveAndPublish"
ConstantHelper.buttons.delete         // "general_delete"
ConstantHelper.buttons.ok             // "general_ok"
ConstantHelper.buttons.close          // "general_close"
ConstantHelper.buttons.insert         // "general_insert"
ConstantHelper.buttons.download       // "general_download"
ConstantHelper.buttons.submit         // "general_submit"
ConstantHelper.buttons.rollback       // "actions_rollback"
ConstantHelper.buttons.add            // "general_add"
ConstantHelper.buttons.submitChanges  // "buttons_submitChanges"
ConstantHelper.buttons.remove         // "general_remove"
ConstantHelper.buttons.change         // "general_change"
ConstantHelper.buttons.select         // "buttons_select"

// Content Apps
ConstantHelper.contentApps.info // '[data-element="sub-view-umbInfo"]'
```

---

## AliasHelper

See **umbraco-test-builders** for comprehensive AliasHelper documentation.

---

## JsonHelper

```typescript
import { JsonHelper } from '@umbraco/playwright-testhelpers';

// Parse response body
const response = await umbracoApi.get(url);
const body = await JsonHelper.getBody(response);
```

---

## Complete Examples

See **umbraco-e2e-testing** for full test examples and templates.

---

## Source Reference

- **Repository**: https://github.com/umbraco/Umbraco.Playwright.Testhelpers
- **Local path**: `/Users/philw/Projects/Umbraco.Playwright.Testhelpers/`
- **Main files**:
  - `lib/helpers/ApiHelpers.ts` - API helper class
  - `lib/helpers/UiHelpers.ts` - UI helper class
  - `lib/helpers/testExtension.ts` - Test fixture extension
  - `lib/helpers/ConstantHelper.ts` - Constants
  - `lib/helpers/AliasHelper.ts` - Alias utilities
