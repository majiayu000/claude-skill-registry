---
name: umbraco-current-user-action
description: Implement current user actions in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Current User Action

## What is it?
Current User Actions appear in the user menu (accessed by clicking the user avatar in the top-right corner of the backoffice). They provide quick actions for the currently logged-in user, such as profile settings, preferences, or custom functionality. Actions can execute code or navigate to a URL.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Conditions**: For controlling when actions appear
  - Reference skill: `umbraco-conditions`

- **Modals**: When actions open modal dialogs
  - Reference skill: `umbraco-modals`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What action? Navigate or execute? Conditions needed?
3. **Generate files** - Create manifest + action class based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest with Default Kind (manifests.ts)
```typescript
import type { ManifestCurrentUserActionDefaultKind } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestCurrentUserActionDefaultKind = {
  type: 'currentUserAction',
  kind: 'default',
  alias: 'My.CurrentUserAction.Preferences',
  name: 'User Preferences',
  api: () => import('./preferences-action.js'),
  meta: {
    icon: 'icon-settings',
    label: 'My Preferences',
  },
};

export const manifests = [manifest];
```

### Action Implementation (preferences-action.ts)
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import type { UmbCurrentUserAction } from '@umbraco-cms/backoffice/current-user';

export class PreferencesAction extends UmbControllerBase implements UmbCurrentUserAction {
  async getHref(): Promise<string | undefined> {
    // Return undefined to use execute() instead
    return undefined;
  }

  async execute(): Promise<void> {
    // Perform the action
    console.log('Opening preferences...');
  }
}

export default PreferencesAction;
```

### Link-based Action
```typescript
export class ExternalLinkAction extends UmbControllerBase implements UmbCurrentUserAction {
  async getHref(): Promise<string | undefined> {
    return 'https://docs.umbraco.com';
  }

  async execute(): Promise<void> {
    // Not called when getHref returns a value
  }
}
```

### Action Opening Modal
```typescript
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';
import { UMB_MODAL_MANAGER_CONTEXT } from '@umbraco-cms/backoffice/modal';
import type { UmbCurrentUserAction } from '@umbraco-cms/backoffice/current-user';

export class SettingsAction extends UmbControllerBase implements UmbCurrentUserAction {
  async getHref(): Promise<string | undefined> {
    return undefined;
  }

  async execute(): Promise<void> {
    const modalManager = await this.getContext(UMB_MODAL_MANAGER_CONTEXT);

    const modal = modalManager.open(this, MY_SETTINGS_MODAL, {
      data: {},
    });

    await modal.onSubmit();
  }
}

export default SettingsAction;
```

### Action with Conditions
```typescript
const manifest: ManifestCurrentUserActionDefaultKind = {
  type: 'currentUserAction',
  kind: 'default',
  alias: 'My.CurrentUserAction.Admin',
  name: 'Admin Settings',
  api: () => import('./admin-action.js'),
  meta: {
    icon: 'icon-lock',
    label: 'Admin Settings',
  },
  conditions: [
    {
      alias: 'Umb.Condition.UserPermission.Admin',
      // Only show for admin users
    },
  ],
};
```

### Custom Element Action
```typescript
import type { ManifestCurrentUserAction } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestCurrentUserAction = {
  type: 'currentUserAction',
  alias: 'My.CurrentUserAction.Custom',
  name: 'Custom Action',
  element: () => import('./custom-action.element.js'),
  api: () => import('./custom-action.js'),
  meta: {},
};
```

### Navigating to Internal Route
```typescript
export class ProfileAction extends UmbControllerBase implements UmbCurrentUserAction {
  async getHref(): Promise<string | undefined> {
    // Navigate to a backoffice route
    return '/section/settings/workspace/user-profile';
  }

  async execute(): Promise<void> {}
}
```

## Meta Properties (Default Kind)

| Property | Description |
|----------|-------------|
| `icon` | Icon displayed in the menu |
| `label` | Text displayed in the menu |

## Action Interface

| Method | Description |
|--------|-------------|
| `getHref()` | Returns URL for link-based actions |
| `execute()` | Called when action is clicked (if no href) |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
