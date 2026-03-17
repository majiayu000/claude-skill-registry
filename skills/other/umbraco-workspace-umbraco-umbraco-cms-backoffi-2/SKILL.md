---
name: umbraco-workspace
description: Implement workspaces in Umbraco backoffice using official docs
version: 1.1.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Workspace

## What is it?
Workspaces are dedicated editing environments designed for specific entity types in Umbraco. They create isolated areas where users can edit content, media, members, and other entities with specialized interfaces tailored to each type. Workspaces maintain draft copies of entity data separate from published versions and support multiple extension types including contexts, views, actions, and footer apps.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/workspaces
- **Workspace Context**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/workspaces/workspace-context
- **Workspace Views**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/workspaces/workspace-views
- **Workspace Actions**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types/workspaces/workspace-editor-actions
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## CRITICAL: Workspace Kinds

### `kind: 'default'` vs `kind: 'routable'`

| Feature | `kind: 'default'` | `kind: 'routable'` |
|---------|------------------|-------------------|
| Use case | Static pages, root workspaces | Entity editing with unique IDs |
| Tree integration | No selection state | Proper selection state |
| URL routing | No route params | Supports `edit/:unique` |
| Context | Simple | Has `unique` observable |

**For tree item navigation, ALWAYS use `kind: 'routable'`** - otherwise:
- Tree item selection won't update when clicking between items
- Navigation between same-type items won't work
- "Forever loading" can occur

### Routable Workspace Context Pattern

For `kind: 'routable'` workspaces, you MUST create a workspace context class:

```typescript
import { UmbWorkspaceRouteManager, UMB_WORKSPACE_CONTEXT } from '@umbraco-cms/backoffice/workspace';
import { UmbObjectState } from '@umbraco-cms/backoffice/observable-api';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import { LitElement, html } from '@umbraco-cms/backoffice/external/lit';
import { customElement } from '@umbraco-cms/backoffice/external/lit';

// Workspace editor element that renders views
@customElement('my-workspace-editor')
class MyWorkspaceEditorElement extends LitElement {
  override render() {
    return html`<umb-workspace-editor></umb-workspace-editor>`;
  }
}

interface MyEntityData {
  unique: string;
  name?: string;
}

export class MyWorkspaceContext extends UmbContextBase {
  public readonly workspaceAlias = 'My.Workspace';

  #data = new UmbObjectState<MyEntityData | undefined>(undefined);
  readonly data = this.#data.asObservable();

  // CRITICAL: Observable unique for workspace views to consume
  readonly unique = this.#data.asObservablePart((data) => data?.unique);
  readonly name = this.#data.asObservablePart((data) => data?.name);

  readonly routes = new UmbWorkspaceRouteManager(this);

  constructor(host: UmbControllerHost) {
    super(host, UMB_WORKSPACE_CONTEXT);

    // Route pattern for tree item navigation
    this.routes.setRoutes([
      {
        path: 'edit/:unique',
        component: MyWorkspaceEditorElement,
        setup: (_component, info) => {
          const unique = info.match.params.unique;
          this.load(unique);
        },
      },
    ]);
  }

  async load(unique: string) {
    // Load entity data and update state
    this.#data.setValue({ unique });
  }

  getUnique() {
    return this.#data.getValue()?.unique;
  }

  getEntityType() {
    return 'my-entity';  // Must match tree item entityType!
  }

  public override destroy(): void {
    this.#data.destroy();
    super.destroy();
  }
}

export { MyWorkspaceContext as api };
```

### Workspace View Consuming Context

Workspace views observe the context's `unique` to react to navigation:

```typescript
import { UMB_WORKSPACE_CONTEXT } from '@umbraco-cms/backoffice/workspace';

override connectedCallback() {
  super.connectedCallback();

  this.consumeContext(UMB_WORKSPACE_CONTEXT, (context) => {
    if (!context) return;

    // Observe unique - will fire when navigating between items
    this.observe((context as any).unique, (unique: string | null) => {
      if (unique) {
        this._loadData(unique);
      }
    });
  });
}
```

## Reference Examples

The Umbraco source includes working examples:

**Workspace Context Counter**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/workspace-context-counter/`

This example demonstrates a workspace with context, views, and footer apps. Includes unit tests.

**Workspace Context Initial Name**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/workspace-context-initial-name/`

This example shows workspace context initialization patterns.

**Workspace View Hint**: `/Umbraco-CMS/src/Umbraco.Web.UI.Client/examples/workspace-view-hint/`

This example demonstrates workspace view hints and metadata.

## Related Foundation Skills

If you need to explain these foundational concepts when implementing workspaces, reference these skills:

- **Context API**: When implementing workspace contexts, context consumption, or explaining workspace extension communication
  - Reference skill: `umbraco-context-api`

- **State Management**: When implementing draft state, observables, reactive updates, or workspace data management
  - Reference skill: `umbraco-state-management`

- **Umbraco Element**: When implementing workspace view elements, explaining UmbElementMixin, or creating workspace components
  - Reference skill: `umbraco-umbraco-element`

- **Controllers**: When implementing workspace actions, controllers, side effects, or action logic
  - Reference skill: `umbraco-controllers`

- **Trees**: When workspace is linked to tree navigation
  - Reference skill: `umbraco-tree`

## Workflow

1. **Fetch docs** - Use WebFetch on the documentation URLs above to get current code examples and patterns
2. **Ask questions** - What entity type? What views needed? What actions? **Is this linked to a tree?**
3. **Choose kind** - Use `kind: 'routable'` for tree navigation, `kind: 'default'` for static pages
4. **Generate files** - Create manifest + workspace context + views + actions based on the fetched docs
5. **Add project reference** - The extension must be referenced by the main Umbraco project to work:
   - Search for `.csproj` files in the current working directory
   - If exactly one Umbraco instance is found, add the reference to it
   - If multiple Umbraco instances are found, ask the user which one to use
   - If no Umbraco instance is found, ask the user for the path
6. **Explain** - Show what was created and how to test

## Minimal Manifest Example

```typescript
export const manifests: UmbExtensionManifest[] = [
  // Routable workspace for tree integration
  {
    type: 'workspace',
    kind: 'routable',
    alias: 'My.Workspace',
    name: 'My Workspace',
    api: () => import('./my-workspace.context.js'),
    meta: {
      entityType: 'my-entity',  // Must match tree item entityType!
    },
  },
  // Workspace view
  {
    type: 'workspaceView',
    alias: 'My.WorkspaceView',
    name: 'My Workspace View',
    element: () => import('./my-workspace-view.element.js'),
    weight: 100,
    meta: {
      label: 'Details',
      pathname: 'details',
      icon: 'icon-info',
    },
    conditions: [
      {
        alias: 'Umb.Condition.WorkspaceAlias',
        match: 'My.Workspace',
      },
    ],
  },
];
```

Always fetch fresh docs before generating code - the API and patterns may have changed.
