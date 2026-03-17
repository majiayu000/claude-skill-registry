---
name: umbraco-user-profile-app
description: Implement user profile apps in Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco User Profile App

## What is it?
User Profile Apps are custom views/tabs that appear in the current user's profile section. They allow you to add custom functionality to the user profile area, such as preferences, activity logs, connected accounts, or any user-specific settings.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Umbraco Element**: For implementing the profile app element
  - Reference skill: `umbraco-umbraco-element`

- **Context API**: For accessing user context
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What functionality? What data to display?
3. **Generate files** - Create manifest + element based on latest docs
4. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (manifests.ts)
```typescript
import type { ManifestUserProfileApp } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestUserProfileApp = {
  type: 'userProfileApp',
  alias: 'My.UserProfileApp.Preferences',
  name: 'User Preferences',
  element: () => import('./preferences-app.element.js'),
  meta: {
    label: 'Preferences',
    pathname: 'preferences',
  },
};

export const manifests = [manifest];
```

### Profile App Element (preferences-app.element.ts)
```typescript
import { html, css, customElement, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_CURRENT_USER_CONTEXT } from '@umbraco-cms/backoffice/current-user';

@customElement('my-preferences-app')
export class MyPreferencesAppElement extends UmbLitElement {
  @state()
  private _userName?: string;

  @state()
  private _emailNotifications = true;

  @state()
  private _darkMode = false;

  constructor() {
    super();

    this.consumeContext(UMB_CURRENT_USER_CONTEXT, (context) => {
      this.observe(context.currentUser, (user) => {
        this._userName = user?.name;
      });
    });
  }

  #handleEmailToggle() {
    this._emailNotifications = !this._emailNotifications;
    this.#savePreferences();
  }

  #handleDarkModeToggle() {
    this._darkMode = !this._darkMode;
    this.#savePreferences();
  }

  async #savePreferences() {
    // Save to local storage or API
    localStorage.setItem('myPreferences', JSON.stringify({
      emailNotifications: this._emailNotifications,
      darkMode: this._darkMode,
    }));
  }

  render() {
    return html`
      <uui-box headline="Preferences for ${this._userName}">
        <div class="preference-item">
          <uui-toggle
            label="Email Notifications"
            ?checked=${this._emailNotifications}
            @change=${this.#handleEmailToggle}
          ></uui-toggle>
          <span>Receive email notifications for content updates</span>
        </div>

        <div class="preference-item">
          <uui-toggle
            label="Dark Mode"
            ?checked=${this._darkMode}
            @change=${this.#handleDarkModeToggle}
          ></uui-toggle>
          <span>Use dark theme in the backoffice</span>
        </div>
      </uui-box>
    `;
  }

  static styles = css`
    :host {
      display: block;
      padding: var(--uui-size-space-5);
    }

    .preference-item {
      display: flex;
      align-items: center;
      gap: var(--uui-size-space-4);
      padding: var(--uui-size-space-4) 0;
      border-bottom: 1px solid var(--uui-color-border);
    }

    .preference-item:last-child {
      border-bottom: none;
    }
  `;
}

export default MyPreferencesAppElement;

declare global {
  interface HTMLElementTagNameMap {
    'my-preferences-app': MyPreferencesAppElement;
  }
}
```

### Activity Log App
```typescript
@customElement('my-activity-log-app')
export class MyActivityLogAppElement extends UmbLitElement {
  @state()
  private _activities: Array<{ action: string; date: string }> = [];

  async connectedCallback() {
    super.connectedCallback();
    await this.#loadActivities();
  }

  async #loadActivities() {
    // Fetch user activities from API
    const response = await fetch('/api/user/activities');
    this._activities = await response.json();
  }

  render() {
    return html`
      <uui-box headline="Recent Activity">
        <uui-table>
          <uui-table-head>
            <uui-table-head-cell>Action</uui-table-head-cell>
            <uui-table-head-cell>Date</uui-table-head-cell>
          </uui-table-head>
          ${this._activities.map(
            (activity) => html`
              <uui-table-row>
                <uui-table-cell>${activity.action}</uui-table-cell>
                <uui-table-cell>${activity.date}</uui-table-cell>
              </uui-table-row>
            `
          )}
        </uui-table>
      </uui-box>
    `;
  }
}
```

### Connected Accounts App
```typescript
const manifest: ManifestUserProfileApp = {
  type: 'userProfileApp',
  alias: 'My.UserProfileApp.ConnectedAccounts',
  name: 'Connected Accounts',
  element: () => import('./connected-accounts.element.js'),
  meta: {
    label: 'Connected Accounts',
    pathname: 'connected-accounts',
  },
};
```

## Meta Properties

| Property | Description |
|----------|-------------|
| `label` | Tab label displayed in profile |
| `pathname` | URL path segment for deep linking |

## Accessing User Context

```typescript
import { UMB_CURRENT_USER_CONTEXT } from '@umbraco-cms/backoffice/current-user';

this.consumeContext(UMB_CURRENT_USER_CONTEXT, (context) => {
  this.observe(context.currentUser, (user) => {
    // Access user properties
    console.log(user?.name, user?.email, user?.unique);
  });
});
```

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
