---
name: umbraco-conditions
description: Understand and use conditions in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Conditions

## What is it?
Extension Conditions enable developers to declare requirements that must be met before an extension becomes available in the backoffice. They function as gatekeeping mechanisms controlling when and where extensions appear based on context like section, workspace, user permissions, or content type. Multiple conditions use AND logic—all must pass for the extension to display.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-conditions
- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Reference Example

The Umbraco source includes a working example:

**Location**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/entity-content-type-condition/`

This example demonstrates a custom condition that checks entity content type. Study this for patterns on creating custom conditions.

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What restricts visibility? Section? Workspace? User? Content type?
3. **Generate code** - Add conditions to manifest based on latest docs
4. **Explain** - Show what was created and when extension appears

## Minimal Examples

### Section Condition
```json
{
  "type": "dashboard",
  "alias": "My.Dashboard",
  "name": "My Dashboard",
  "conditions": [
    {
      "alias": "Umb.Condition.SectionAlias",
      "match": "Umb.Section.Content"
    }
  ]
}
```

### Workspace Condition
```json
{
  "type": "workspaceView",
  "alias": "My.WorkspaceView",
  "name": "My Workspace View",
  "conditions": [
    {
      "alias": "Umb.Condition.WorkspaceAlias",
      "match": "Umb.Workspace.Document"
    }
  ]
}
```

### Multiple Conditions (AND Logic)
```typescript
const manifest = {
  type: 'workspaceAction',
  alias: 'My.WorkspaceAction',
  name: 'My Action',
  conditions: [
    {
      alias: 'Umb.Condition.SectionAlias',
      match: 'Umb.Section.Content'
    },
    {
      alias: 'Umb.Condition.WorkspaceAlias',
      match: 'Umb.Workspace.Document'
    },
    {
      alias: 'Umb.Condition.WorkspaceContentTypeAlias',
      match: 'blogPost'
    }
  ]
};
```

### User Permission Condition
```json
{
  "type": "entityAction",
  "alias": "My.DeleteAction",
  "name": "Delete Document",
  "conditions": [
    {
      "alias": "Umb.Condition.UserPermission.Document",
      "match": "Umb.UserPermission.Document.Delete"
    }
  ]
}
```

### Section User Permission
```json
{
  "type": "dashboard",
  "alias": "My.AdminDashboard",
  "name": "Admin Dashboard",
  "conditions": [
    {
      "alias": "Umb.Condition.SectionUserPermission",
      "match": "Umb.Section.Settings"
    }
  ]
}
```

### Workspace Entity Type
```json
{
  "type": "workspaceView",
  "alias": "My.View",
  "name": "My View",
  "conditions": [
    {
      "alias": "Umb.Condition.WorkspaceEntityType",
      "match": "document"
    }
  ]
}
```

### Content Type Condition
```json
{
  "type": "workspaceView",
  "alias": "My.BlogView",
  "name": "Blog Post View",
  "conditions": [
    {
      "alias": "Umb.Condition.WorkspaceContentTypeAlias",
      "match": "blogPost"
    }
  ]
}
```

### Workspace Has Collection
```json
{
  "type": "workspaceAction",
  "alias": "My.CollectionAction",
  "name": "Collection Action",
  "conditions": [
    {
      "alias": "Umb.Condition.WorkspaceHasCollection",
      "match": true
    }
  ]
}
```

### Custom Condition Implementation
```typescript
import { UmbConditionBase } from '@umbraco-cms/backoffice/extension-api';
import { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';

export class MyCustomCondition extends UmbConditionBase<MyConditionConfig> {
  constructor(host: UmbControllerHost, args: MyConditionConfig) {
    super(host, args);

    // Observe some context or state
    this.consumeContext(SOME_CONTEXT, (context) => {
      this.observe(context.someObservable, (value) => {
        // Update permitted state based on value
        this.permitted = value === this.args.expectedValue;
      });
    });
  }
}

interface MyConditionConfig {
  expectedValue: string;
}
```

### Register Custom Condition
```typescript
export const manifests = [
  {
    type: 'condition',
    name: 'My Custom Condition',
    alias: 'My.Condition.Custom',
    api: MyCustomCondition,
  },
];
```

### Use Custom Condition
```json
{
  "type": "dashboard",
  "alias": "My.Dashboard",
  "name": "My Dashboard",
  "conditions": [
    {
      "alias": "My.Condition.Custom",
      "expectedValue": "someValue"
    }
  ]
}
```

## Built-in Conditions

**Section Conditions:**
- `Umb.Condition.SectionAlias` - Match current section
- `Umb.Condition.SectionUserPermission` - User has section access

**Workspace Conditions:**
- `Umb.Condition.WorkspaceAlias` - Match current workspace
- `Umb.Condition.WorkspaceEntityType` - Match entity type (document, media, etc.)
- `Umb.Condition.WorkspaceContentTypeAlias` - Match content type alias
- `Umb.Condition.WorkspaceHasCollection` - Workspace has collection

**User Permission Conditions:**
- `Umb.Condition.UserPermission.Document` - Document permissions
- `Umb.Condition.CurrentUser.IsAdmin` - User is admin
- `Umb.Condition.CurrentUser.GroupId` - User in specific group

## Key Concepts

**Gatekeeping**: Conditions control extension availability

**AND Logic**: All conditions must pass for extension to appear

**Match Property**: Value to compare against (alias, entity type, etc.)

**Permitted State**: Boolean indicating if condition passes

**Custom Conditions**: Implement `UmbConditionBase` and set `this.permitted`

**Use Cases**:
- Show dashboard only in Content section
- Display action only for specific content types
- Restrict features to admin users
- Show view only in document workspace
- Enable actions based on permissions

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
