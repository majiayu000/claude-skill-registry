---
name: umbraco-mfa-login-provider
description: Implement MFA login providers for Umbraco backoffice using official docs
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco MFA Login Provider

## What is it?
An MFA Login Provider is the UI component for Two-Factor Authentication (2FA) in Umbraco. It provides the interface for users to enable/disable and configure their 2FA provider (e.g., Google Authenticator, SMS codes). The backend `ITwoFactorProvider` must be configured separately in C# - this extension type handles the frontend setup and configuration UI.

## Documentation
Always fetch the latest docs before implementing:

- **Two-Factor Authentication**: https://docs.umbraco.com/umbraco-cms/reference/security/two-factor-authentication
- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What 2FA method? QR code setup? Custom validation UI?
3. **Configure backend** - Set up C# ITwoFactorProvider first
4. **Generate frontend files** - Create manifest + configuration element
5. **Explain** - Show what was created and how to test

## Minimal Examples

### Manifest (umbraco-package.json)
```json
{
  "name": "My MFA Provider",
  "extensions": [
    {
      "type": "mfaLoginProvider",
      "alias": "My.MfaProvider.Authenticator",
      "name": "Authenticator App MFA",
      "forProviderName": "Umbraco.GoogleAuthenticator",
      "element": "/App_Plugins/MyMfa/mfa-setup.js",
      "meta": {
        "label": "Authenticator App"
      }
    }
  ]
}
```

### Manifest (TypeScript)
```typescript
import type { ManifestMfaLoginProvider } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestMfaLoginProvider = {
  type: 'mfaLoginProvider',
  alias: 'My.MfaProvider.Authenticator',
  name: 'Authenticator MFA Provider',
  forProviderName: 'Umbraco.GoogleAuthenticator', // Must match backend provider name
  element: () => import('./mfa-setup.element.js'),
  meta: {
    label: 'Authenticator App',
  },
};

export const manifests = [manifest];
```

### MFA Setup Element (mfa-setup.element.ts)
```typescript
import { html, css, customElement, property, state } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { UMB_NOTIFICATION_CONTEXT } from '@umbraco-cms/backoffice/notification';
import type { UmbMfaProviderConfigurationElementProps } from '@umbraco-cms/backoffice/user';

@customElement('my-mfa-setup')
export class MyMfaSetupElement extends UmbLitElement implements UmbMfaProviderConfigurationElementProps {
  @property({ type: String })
  providerName = '';

  @property({ type: String })
  displayName = '';

  @property({ attribute: false })
  callback!: (providerName: string, code: string, secret: string) => Promise<{ error?: string }>;

  @property({ attribute: false })
  close!: () => void;

  @state()
  private _loading = true;

  @state()
  private _secret = '';

  @state()
  private _qrCodeUrl = '';

  @state()
  private _code = '';

  @state()
  private _submitting = false;

  #notificationContext?: typeof UMB_NOTIFICATION_CONTEXT.TYPE;

  constructor() {
    super();
    this.consumeContext(UMB_NOTIFICATION_CONTEXT, (context) => {
      this.#notificationContext = context;
    });
  }

  async connectedCallback() {
    super.connectedCallback();
    await this.#loadSetupData();
  }

  async #loadSetupData() {
    try {
      // Fetch setup data from API
      const response = await fetch(`/umbraco/management/api/v1/user/2fa/${this.providerName}/setup`);
      const data = await response.json();

      this._secret = data.secret;
      this._qrCodeUrl = data.qrCodeSetupImageUrl;
    } catch (error) {
      this.#notificationContext?.peek('danger', { data: { message: 'Failed to load setup data' } });
    } finally {
      this._loading = false;
    }
  }

  async #handleSubmit(e: SubmitEvent) {
    e.preventDefault();

    if (!this._code || this._code.length !== 6) {
      this.#notificationContext?.peek('warning', { data: { message: 'Please enter a 6-digit code' } });
      return;
    }

    this._submitting = true;

    try {
      const result = await this.callback(this.providerName, this._code, this._secret);

      if (result.error) {
        this.#notificationContext?.peek('danger', { data: { message: result.error } });
      } else {
        this.#notificationContext?.peek('positive', { data: { message: '2FA enabled successfully' } });
        this.close();
      }
    } finally {
      this._submitting = false;
    }
  }

  render() {
    if (this._loading) {
      return html`<uui-loader></uui-loader>`;
    }

    return html`
      <uui-form>
        <form @submit=${this.#handleSubmit}>
          <umb-body-layout headline="Set up ${this.displayName}">
            <div id="main">
              <p>Scan this QR code with your authenticator app:</p>

              <div class="qr-container">
                <img src=${this._qrCodeUrl} alt="QR Code" />
              </div>

              <p>Or enter this secret manually: <code>${this._secret}</code></p>

              <uui-form-layout-item>
                <uui-label slot="label" for="code" required>Verification Code</uui-label>
                <uui-input
                  id="code"
                  type="text"
                  inputmode="numeric"
                  pattern="[0-9]*"
                  maxlength="6"
                  placeholder="000000"
                  .value=${this._code}
                  @input=${(e: InputEvent) => (this._code = (e.target as HTMLInputElement).value)}
                  required
                ></uui-input>
              </uui-form-layout-item>
            </div>

            <div slot="actions">
              <uui-button
                label="Cancel"
                look="secondary"
                @click=${this.close}
              ></uui-button>
              <uui-button
                type="submit"
                label="Enable"
                look="primary"
                color="positive"
                ?state=${this._submitting ? 'waiting' : undefined}
              ></uui-button>
            </div>
          </umb-body-layout>
        </form>
      </uui-form>
    `;
  }

  static styles = css`
    #main {
      max-width: 400px;
      margin: 0 auto;
      text-align: center;
    }

    .qr-container {
      margin: var(--uui-size-space-5) 0;
    }

    .qr-container img {
      max-width: 200px;
      border: 1px solid var(--uui-color-border);
      border-radius: var(--uui-border-radius);
    }

    code {
      display: block;
      margin: var(--uui-size-space-3) 0;
      padding: var(--uui-size-space-2);
      background: var(--uui-color-surface-alt);
      border-radius: var(--uui-border-radius);
      font-family: monospace;
      word-break: break-all;
    }
  `;
}

export default MyMfaSetupElement;

declare global {
  interface HTMLElementTagNameMap {
    'my-mfa-setup': MyMfaSetupElement;
  }
}
```

### Using Default MFA Element
```typescript
// If you don't need custom UI, you can use the built-in default element
// Just register the manifest without a custom element - Umbraco provides a default
const manifest: ManifestMfaLoginProvider = {
  type: 'mfaLoginProvider',
  alias: 'My.MfaProvider.Default',
  name: 'Default MFA Provider',
  forProviderName: 'Umbraco.GoogleAuthenticator',
  // No element specified - uses default
  meta: {
    label: 'Authenticator App',
  },
};
```

### Backend C# Configuration (for reference)
```csharp
// ITwoFactorProvider implementation
public class GoogleAuthenticatorProvider : ITwoFactorProvider
{
    public string ProviderName => "Umbraco.GoogleAuthenticator";

    public Task<bool> ValidateTwoFactorPIN(string secret, string code)
    {
        var twoFactorAuthenticator = new TwoFactorAuthenticator();
        return Task.FromResult(
            twoFactorAuthenticator.ValidateTwoFactorPIN(secret, code)
        );
    }

    public Task<bool> ValidateTwoFactorSetup(string secret, string code)
    {
        return ValidateTwoFactorPIN(secret, code);
    }

    public async Task<object> GetSetupDataAsync(Guid userKey, IMemberService memberService)
    {
        var secret = Base32Encoding.ToString(Guid.NewGuid().ToByteArray());
        var authenticator = new TwoFactorAuthenticator();
        var setupInfo = authenticator.GenerateSetupCode(
            "My App",
            userKey.ToString(),
            secret,
            false
        );

        return new
        {
            secret,
            qrCodeSetupImageUrl = setupInfo.QrCodeSetupImageUrl
        };
    }
}

// Register in Composer
public class MfaComposer : IComposer
{
    public void Compose(IUmbracoBuilder builder)
    {
        var identityBuilder = new BackOfficeIdentityBuilder(builder.Services);
        identityBuilder.AddTwoFactorProvider<GoogleAuthenticatorProvider>(
            GoogleAuthenticatorProvider.Name
        );
    }
}
```

## Element Props Interface

| Property | Type | Description |
|----------|------|-------------|
| `providerName` | `string` | The provider identifier |
| `displayName` | `string` | Human-readable provider name |
| `callback` | `Function` | Call with code/secret to validate |
| `close` | `Function` | Close the setup modal |

## Callback Function

```typescript
callback(providerName: string, code: string, secret: string): Promise<{ error?: string }>
```

Returns an object with an `error` property if validation failed, or empty object on success.

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
