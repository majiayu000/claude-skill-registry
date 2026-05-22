---
name: umbraco-auth-provider
description: Implement authentication providers for Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco Auth Provider

## What is it?
An Auth Provider enables external login (OAuth/SSO) for the Umbraco backoffice. It provides the UI component (login button) that connects to a backend authentication provider. The backend must be configured separately in C# - this extension type handles the frontend presentation and behavior. Common providers include Google, Microsoft, GitHub, and custom OAuth providers.

## Documentation
Always fetch the latest docs before implementing:

- **External Login Providers**: https://docs.umbraco.com/umbraco-cms/reference/security/external-login-providers
- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - Which OAuth provider? Custom UI needed? Auto-redirect?
3. **Configure backend** - Set up C# authentication provider first
4. **Generate frontend files** - Create manifest + optional custom element
5. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest with Default Button (umbraco-package.json)
```json
{
  "name": "My Auth Provider",
  "extensions": [
    {
      "type": "authProvider",
      "alias": "My.AuthProvider.GitHub",
      "name": "GitHub Login",
      "forProviderName": "Umbraco.GitHub",
      "meta": {
        "label": "Login with GitHub",
        "defaultView": {
          "icon": "icon-github",
          "color": "default",
          "look": "secondary"
        }
      }
    }
  ]
}
```

### Manifest (TypeScript)
```typescript
import type { ManifestAuthProvider } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestAuthProvider = {
  type: 'authProvider',
  alias: 'My.AuthProvider.Google',
  name: 'Google Login',
  forProviderName: 'Umbraco.Google', // Must match backend provider name
  meta: {
    label: 'Sign in with Google',
    defaultView: {
      icon: 'icon-google',
      color: 'default',
      look: 'outline',
    },
    behavior: {
      autoRedirect: false,
      popupTarget: 'umbracoAuthPopup',
      popupFeatures: 'width=600,height=600,menubar=no,location=no',
    },
    linking: {
      allowManualLinking: true,
    },
  },
};

export const manifests = [manifest];
```

### Custom Login Button Element
```typescript
import type { ManifestAuthProvider } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestAuthProvider = {
  type: 'authProvider',
  alias: 'My.AuthProvider.Custom',
  name: 'Custom SSO Login',
  forProviderName: 'Umbraco.CustomSSO',
  element: () => import('./custom-auth-button.element.js'),
  meta: {
    label: 'Enterprise SSO',
  },
};
```

### Custom Button Element (custom-auth-button.element.ts)
```typescript
import { html, css, customElement, property } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';

@customElement('my-custom-auth-button')
export class MyCustomAuthButtonElement extends UmbLitElement {
  @property({ type: String })
  providerName = '';

  @property({ type: String })
  displayName = '';

  #handleClick() {
    // Dispatch event to trigger auth flow
    this.dispatchEvent(
      new CustomEvent('auth-request', {
        bubbles: true,
        composed: true,
        detail: { providerName: this.providerName },
      })
    );
  }

  render() {
    return html`
      <button @click=${this.#handleClick}>
        <img src="/App_Plugins/MyAuth/logo.svg" alt="" />
        <span>${this.displayName}</span>
      </button>
    `;
  }

  static styles = css`
    button {
      display: flex;
      align-items: center;
      gap: var(--uui-size-space-3);
      width: 100%;
      padding: var(--uui-size-space-4);
      border: 1px solid var(--uui-color-border);
      border-radius: var(--uui-border-radius);
      background: var(--uui-color-surface);
      cursor: pointer;
    }

    button:hover {
      background: var(--uui-color-surface-alt);
    }

    img {
      width: 24px;
      height: 24px;
    }
  `;
}

export default MyCustomAuthButtonElement;
```

### Auto-Redirect Provider (Single Sign-On)
```typescript
const manifest: ManifestAuthProvider = {
  type: 'authProvider',
  alias: 'My.AuthProvider.EnterpriseSSO',
  name: 'Enterprise SSO',
  forProviderName: 'Umbraco.EnterpriseSSO',
  meta: {
    label: 'Enterprise Login',
    behavior: {
      autoRedirect: true, // Automatically redirects to provider
    },
  },
};
```

### Backend C# Configuration (for reference)
```csharp
// Composer to register the provider
public class GitHubAuthenticationComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        builder.AddBackOfficeExternalLogins(logins =>
        {
            logins.AddBackOfficeLogin(
                backOfficeAuthenticationBuilder =>
                {
                    backOfficeAuthenticationBuilder.AddGitHub(
                        backOfficeAuthenticationBuilder.SchemeForBackOffice("Umbraco.GitHub")!,
                        options =>
                        {
                            options.ClientId = "your-client-id";
                            options.ClientSecret = "your-client-secret";
                            options.CallbackPath = "/umbraco-github-signin";
                        });
                },
                options =>
                {
                    options.AutoLinkOptions = new ExternalSignInAutoLinkOptions(
                        autoLinkExternalAccount: true,
                        defaultUserGroups: new[] { "admin" }
                    );
                });
        });
    }
}
```

## Meta Properties

| Property | Description |
|----------|-------------|
| `label` | Button text |
| `defaultView.icon` | Button icon |
| `defaultView.color` | Button color (default, positive, warning, danger) |
| `defaultView.look` | Button style (default, primary, secondary, outline) |
| `behavior.autoRedirect` | Auto-redirect to provider on login page |
| `behavior.popupTarget` | Window name for popup |
| `behavior.popupFeatures` | Popup window features |
| `linking.allowManualLinking` | Allow linking to existing accounts |

## Common Icons

- `icon-google` - Google
- `icon-microsoft` - Microsoft
- `icon-github` - GitHub
- `icon-facebook` - Facebook
- `icon-twitter` / `icon-x` - Twitter/X
- `icon-cloud` - Generic OAuth

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
