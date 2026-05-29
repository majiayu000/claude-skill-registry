---
description: "Multi-tenant Keycloak authentication theming with realm-specific design systems"
triggers:
  - keycloak
  - authentication
  - login theme
  - multi-tenant
  - realm
  - SSO
  - PKCE
globs:
  - "**/keycloak/**"
  - "**/themes/**"
  - "**/auth/**"
  - "*.ftl"
---

# Keycloak Theming Skill

Multi-tenant Keycloak authentication theming with realm-specific design systems.

## Overview

This skill provides comprehensive guidance for implementing custom Keycloak themes across multiple realms with tenant-specific branding and design systems.

## Multi-Realm Configuration

### Realm Structure

```
Keycloak Instance
├── thelobbi (Realm)
│   ├── Theme: lobbi-theme
│   ├── Primary Color: #0066cc
│   ├── Logo: lobbi-logo.svg
│   └── Use Case: Main platform authentication
│
└── brooksidebi (Realm)
    ├── Theme: brookside-theme
    ├── Primary Color: #2c5282
    ├── Logo: brookside-logo.svg
    └── Use Case: BI platform authentication
```

### Realm Configuration

**thelobbi Realm:**
```json
{
  "realm": "thelobbi",
  "displayName": "The Lobbi",
  "displayNameHtml": "<div class=\"kc-logo-text\"><span>The Lobbi</span></div>",
  "loginTheme": "lobbi-theme",
  "accountTheme": "lobbi-theme",
  "adminTheme": "keycloak.v2",
  "emailTheme": "lobbi-theme"
}
```

**brooksidebi Realm:**
```json
{
  "realm": "brooksidebi",
  "displayName": "Brookside BI",
  "displayNameHtml": "<div class=\"kc-logo-text\"><span>Brookside BI</span></div>",
  "loginTheme": "brookside-theme",
  "accountTheme": "brookside-theme",
  "adminTheme": "keycloak.v2",
  "emailTheme": "brookside-theme"
}
```

## Custom Theme Structure

### Directory Layout

```
keycloak/
└── themes/
    ├── lobbi-theme/
    │   ├── login/
    │   │   ├── theme.properties
    │   │   ├── resources/
    │   │   │   ├── css/
    │   │   │   │   ├── login.css
    │   │   │   │   └── styles.css
    │   │   │   ├── img/
    │   │   │   │   ├── lobbi-logo.svg
    │   │   │   │   ├── lobbi-icon.svg
    │   │   │   │   └── background.jpg
    │   │   │   └── js/
    │   │   │       └── script.js
    │   │   └── login.ftl
    │   │
    │   ├── account/
    │   │   └── theme.properties
    │   │
    │   └── email/
    │       └── theme.properties
    │
    └── brookside-theme/
        └── [same structure as lobbi-theme]
```

### Theme Properties

**themes/lobbi-theme/login/theme.properties:**
```properties
parent=keycloak
import=common/keycloak

styles=css/login.css css/styles.css
stylesCommon=node_modules/patternfly/dist/css/patternfly.min.css

meta=viewport==width=device-width,initial-scale=1
```

## Login Page Theming Templates (FTL)

### Base Login Template

**themes/lobbi-theme/login/login.ftl:**
```ftl
<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=!messagesPerField.existsError('username','password') displayInfo=realm.password && realm.registrationAllowed && !registrationDisabled??; section>
    <#if section = "header">
        ${msg("loginAccountTitle")}
    <#elseif section = "form">
    <div id="kc-form">
      <div id="kc-form-wrapper">
        <#if realm.password>
            <form id="kc-form-login" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
                <div class="${properties.kcFormGroupClass!}">
                    <label for="username" class="${properties.kcLabelClass!}">
                        <#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if>
                    </label>

                    <input tabindex="1" id="username" class="${properties.kcInputClass!}" name="username" value="${(login.username!'')}"  type="text" autofocus autocomplete="off"
                           aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"
                    />

                    <#if messagesPerField.existsError('username','password')>
                        <span id="input-error" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                                ${kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc}
                        </span>
                    </#if>
                </div>

                <div class="${properties.kcFormGroupClass!}">
                    <label for="password" class="${properties.kcLabelClass!}">${msg("password")}</label>

                    <input tabindex="2" id="password" class="${properties.kcInputClass!}" name="password" type="password" autocomplete="off"
                           aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"
                    />
                </div>

                <div class="${properties.kcFormGroupClass!} ${properties.kcFormSettingClass!}">
                    <div id="kc-form-options">
                        <#if realm.rememberMe && !usernameEditDisabled??>
                            <div class="checkbox">
                                <label>
                                    <#if login.rememberMe??>
                                        <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox" checked> ${msg("rememberMe")}
                                    <#else>
                                        <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox"> ${msg("rememberMe")}
                                    </#if>
                                </label>
                            </div>
                        </#if>
                        </div>
                        <div class="${properties.kcFormOptionsWrapperClass!}">
                            <#if realm.resetPasswordAllowed>
                                <span><a tabindex="5" href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a></span>
                            </#if>
                        </div>

                  </div>

                  <div id="kc-form-buttons" class="${properties.kcFormGroupClass!}">
                      <input type="hidden" id="id-hidden-input" name="credentialId" <#if auth.selectedCredential?has_content>value="${auth.selectedCredential}"</#if>/>
                      <input tabindex="4" class="${properties.kcButtonClass!} ${properties.kcButtonPrimaryClass!} ${properties.kcButtonBlockClass!} ${properties.kcButtonLargeClass!}" name="login" id="kc-login" type="submit" value="${msg("doLogIn")}"/>
                  </div>
            </form>
        </#if>
        </div>
    </div>
    <#elseif section = "info" >
        <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
            <div id="kc-registration-container">
                <div id="kc-registration">
                    <span>${msg("noAccount")} <a tabindex="6"
                                                 href="${url.registrationUrl}">${msg("doRegister")}</a></span>
                </div>
            </div>
        </#if>
    </#if>

</@layout.registrationLayout>
```

### Custom Template with Realm-Specific Branding

**themes/lobbi-theme/login/template.ftl:**
```ftl
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="robots" content="noindex, nofollow">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <#if properties.meta?has_content>
        <#list properties.meta?split(' ') as meta>
            <meta name="${meta?split('==')[0]}" content="${meta?split('==')[1]}"/>
        </#list>
    </#if>

    <title>${msg("loginTitle",(realm.displayName!''))}</title>
    <link rel="icon" href="${url.resourcesPath}/img/lobbi-icon.svg" />

    <#if properties.stylesCommon?has_content>
        <#list properties.stylesCommon?split(' ') as style>
            <link href="${url.resourcesCommonPath}/${style}" rel="stylesheet" />
        </#list>
    </#if>
    <#if properties.styles?has_content>
        <#list properties.styles?split(' ') as style>
            <link href="${url.resourcesPath}/${style}" rel="stylesheet" />
        </#list>
    </#if>
</head>

<body class="keycloak-theme ${realm.name}-realm">
    <div class="kc-container">
        <div class="kc-content">
            <div class="kc-brand">
                <img src="${url.resourcesPath}/img/lobbi-logo.svg" alt="${realm.displayName!''}" />
            </div>

            <div id="kc-header-wrapper">
                <#nested "header">
            </div>

            <div class="kc-form-wrapper">
                <#nested "form">
            </div>

            <#if displayInfo>
                <div id="kc-info-wrapper">
                    <#nested "info">
                </div>
            </#if>
        </div>
    </div>
</body>
</html>
```

## Realm-Specific CSS Variables

### Lobbi Theme Variables

**themes/lobbi-theme/login/resources/css/styles.css:**
```css
:root {
  /* Brand Colors */
  --lobbi-primary: #0066cc;
  --lobbi-primary-dark: #0052a3;
  --lobbi-primary-light: #3384d6;
  --lobbi-secondary: #6c757d;
  --lobbi-accent: #17a2b8;

  /* Neutrals */
  --lobbi-bg: #ffffff;
  --lobbi-surface: #f8f9fa;
  --lobbi-text: #212529;
  --lobbi-text-secondary: #6c757d;
  --lobbi-border: #dee2e6;

  /* Status Colors */
  --lobbi-success: #28a745;
  --lobbi-error: #dc3545;
  --lobbi-warning: #ffc107;
  --lobbi-info: #17a2b8;

  /* Typography */
  --lobbi-font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --lobbi-font-size-base: 16px;
  --lobbi-font-size-large: 18px;
  --lobbi-font-size-small: 14px;

  /* Spacing */
  --lobbi-spacing-xs: 0.5rem;
  --lobbi-spacing-sm: 1rem;
  --lobbi-spacing-md: 1.5rem;
  --lobbi-spacing-lg: 2rem;
  --lobbi-spacing-xl: 3rem;

  /* Border Radius */
  --lobbi-radius-sm: 4px;
  --lobbi-radius-md: 8px;
  --lobbi-radius-lg: 12px;

  /* Shadows */
  --lobbi-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --lobbi-shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --lobbi-shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

body.keycloak-theme.thelobbi-realm {
  font-family: var(--lobbi-font-family);
  background: linear-gradient(135deg, var(--lobbi-primary-light) 0%, var(--lobbi-primary) 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kc-container {
  width: 100%;
  max-width: 480px;
  padding: var(--lobbi-spacing-md);
}

.kc-content {
  background: var(--lobbi-bg);
  border-radius: var(--lobbi-radius-lg);
  box-shadow: var(--lobbi-shadow-lg);
  padding: var(--lobbi-spacing-xl);
}

.kc-brand {
  text-align: center;
  margin-bottom: var(--lobbi-spacing-lg);
}

.kc-brand img {
  height: 48px;
  width: auto;
}

/* Form Styles */
.kc-form-group {
  margin-bottom: var(--lobbi-spacing-md);
}

.kc-label {
  display: block;
  font-size: var(--lobbi-font-size-small);
  font-weight: 500;
  color: var(--lobbi-text);
  margin-bottom: var(--lobbi-spacing-xs);
}

.kc-input {
  width: 100%;
  padding: 0.75rem;
  font-size: var(--lobbi-font-size-base);
  border: 1px solid var(--lobbi-border);
  border-radius: var(--lobbi-radius-md);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.kc-input:focus {
  outline: none;
  border-color: var(--lobbi-primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.kc-input[aria-invalid="true"] {
  border-color: var(--lobbi-error);
}

/* Button Styles */
.kc-button {
  width: 100%;
  padding: 0.75rem;
  font-size: var(--lobbi-font-size-base);
  font-weight: 600;
  border: none;
  border-radius: var(--lobbi-radius-md);
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

.kc-button-primary {
  background-color: var(--lobbi-primary);
  color: white;
}

.kc-button-primary:hover {
  background-color: var(--lobbi-primary-dark);
}

.kc-button-primary:active {
  transform: translateY(1px);
}

/* Error Messages */
.kc-input-error-message {
  display: block;
  color: var(--lobbi-error);
  font-size: var(--lobbi-font-size-small);
  margin-top: var(--lobbi-spacing-xs);
}

/* Links */
a {
  color: var(--lobbi-primary);
  text-decoration: none;
  transition: color 0.2s;
}

a:hover {
  color: var(--lobbi-primary-dark);
  text-decoration: underline;
}
```

### Brookside Theme Variables

**themes/brookside-theme/login/resources/css/styles.css:**
```css
:root {
  /* Brand Colors - Brookside BI */
  --brookside-primary: #2c5282;
  --brookside-primary-dark: #1e3a5f;
  --brookside-primary-light: #4a6fa5;
  --brookside-secondary: #718096;
  --brookside-accent: #805ad5;

  /* Data Visualization Colors */
  --brookside-chart-1: #4299e1;
  --brookside-chart-2: #48bb78;
  --brookside-chart-3: #ed8936;
  --brookside-chart-4: #9f7aea;

  /* Neutrals */
  --brookside-bg: #f7fafc;
  --brookside-surface: #ffffff;
  --brookside-text: #1a202c;
  --brookside-text-secondary: #718096;
  --brookside-border: #e2e8f0;

  /* Typography */
  --brookside-font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

body.keycloak-theme.brooksidebi-realm {
  font-family: var(--brookside-font-family);
  background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 50%, #4a6fa5 100%);
}

/* Apply Brookside-specific styling... */
```

## JWT Claims and Theme Association

### Client Configuration for Theme Claims

```json
{
  "clientId": "lobbi-web-app",
  "protocolMappers": [
    {
      "name": "realm-name",
      "protocol": "openid-connect",
      "protocolMapper": "oidc-hardcoded-claim-mapper",
      "config": {
        "claim.name": "realm",
        "claim.value": "thelobbi",
        "jsonType.label": "String",
        "id.token.claim": "true",
        "access.token.claim": "true",
        "userinfo.token.claim": "true"
      }
    },
    {
      "name": "theme-name",
      "protocol": "openid-connect",
      "protocolMapper": "oidc-hardcoded-claim-mapper",
      "config": {
        "claim.name": "theme",
        "claim.value": "lobbi-theme",
        "jsonType.label": "String",
        "id.token.claim": "true",
        "access.token.claim": "true"
      }
    }
  ]
}
```

### Accessing Theme in Application

```typescript
// Example: Extract theme from JWT token
interface TokenPayload {
  realm: string;
  theme: string;
  // ... other claims
}

function applyThemeFromToken(token: string) {
  const payload = JSON.parse(atob(token.split('.')[1])) as TokenPayload;

  // Apply theme dynamically
  if (payload.theme === 'lobbi-theme') {
    document.documentElement.setAttribute('data-theme', 'lobbi');
  } else if (payload.theme === 'brookside-theme') {
    document.documentElement.setAttribute('data-theme', 'brookside');
  }
}
```

## Environment Variables Setup

### Keycloak Configuration

**.env.local:**
```bash
# Keycloak Base URL
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.thelobbi.com
KEYCLOAK_URL=https://auth.thelobbi.com

# Lobbi Realm
NEXT_PUBLIC_KEYCLOAK_REALM_LOBBI=thelobbi
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID_LOBBI=lobbi-web-app
KEYCLOAK_CLIENT_SECRET_LOBBI=your-client-secret-here

# Brookside Realm
NEXT_PUBLIC_KEYCLOAK_REALM_BROOKSIDE=brooksidebi
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID_BROOKSIDE=brookside-web-app
KEYCLOAK_CLIENT_SECRET_BROOKSIDE=your-client-secret-here

# PKCE Configuration
NEXT_PUBLIC_KEYCLOAK_PKCE_ENABLED=true
NEXT_PUBLIC_KEYCLOAK_RESPONSE_TYPE=code
NEXT_PUBLIC_KEYCLOAK_SCOPE=openid profile email

# Redirect URIs
NEXT_PUBLIC_KEYCLOAK_REDIRECT_URI_LOBBI=https://app.thelobbi.com/auth/callback
NEXT_PUBLIC_KEYCLOAK_REDIRECT_URI_BROOKSIDE=https://bi.brooksideadvisory.com/auth/callback
```

### Next.js Authentication Configuration

**lib/keycloak.ts:**
```typescript
import Keycloak from 'keycloak-js';

interface KeycloakConfig {
  realm: string;
  clientId: string;
  url: string;
}

export function getKeycloakConfig(tenant: 'lobbi' | 'brookside'): KeycloakConfig {
  if (tenant === 'lobbi') {
    return {
      realm: process.env.NEXT_PUBLIC_KEYCLOAK_REALM_LOBBI!,
      clientId: process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID_LOBBI!,
      url: process.env.NEXT_PUBLIC_KEYCLOAK_URL!,
    };
  } else {
    return {
      realm: process.env.NEXT_PUBLIC_KEYCLOAK_REALM_BROOKSIDE!,
      clientId: process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID_BROOKSIDE!,
      url: process.env.NEXT_PUBLIC_KEYCLOAK_URL!,
    };
  }
}

export function initKeycloak(tenant: 'lobbi' | 'brookside') {
  const config = getKeycloakConfig(tenant);

  const keycloak = new Keycloak({
    url: config.url,
    realm: config.realm,
    clientId: config.clientId,
  });

  return keycloak.init({
    onLoad: 'login-required',
    checkLoginIframe: false,
    pkceMethod: 'S256', // PKCE enabled
  });
}
```

## Docker Deployment

### Dockerfile for Custom Themes

```dockerfile
FROM quay.io/keycloak/keycloak:23.0

# Copy custom themes
COPY themes/lobbi-theme /opt/keycloak/themes/lobbi-theme
COPY themes/brookside-theme /opt/keycloak/themes/brookside-theme

# Set environment variables
ENV KC_DB=postgres
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Production build
RUN /opt/keycloak/bin/kc.sh build

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  keycloak:
    build: .
    environment:
      KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: ${KC_DB_PASSWORD}
      KC_HOSTNAME: auth.thelobbi.com
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASSWORD}
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    command: start --optimized

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: ${KC_DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Testing Themes

### Theme Development Workflow

1. **Local Development:**
```bash
# Start Keycloak with theme watching
docker run -p 8080:8080 \
  -v $(pwd)/themes:/opt/keycloak/themes \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:23.0 \
  start-dev
```

2. **Clear Theme Cache:**
```bash
# In Keycloak admin console
Realm Settings > Themes > Clear Cache
```

3. **Test Different Realms:**
```bash
# Test Lobbi realm
http://localhost:8080/realms/thelobbi/account

# Test Brookside realm
http://localhost:8080/realms/brooksidebi/account
```

## Best Practices

1. **Consistency**: Maintain consistent branding across login, account, and email themes
2. **Accessibility**: Ensure WCAG AA compliance for all theme elements
3. **Performance**: Optimize images and CSS for fast loading
4. **Responsive**: Test themes on mobile, tablet, and desktop
5. **Security**: Never expose sensitive configuration in theme files
6. **Version Control**: Track theme changes with git
7. **Documentation**: Document realm-specific customizations

## Integration with Other Skills

- **design-styles**: Apply design system styles to Keycloak themes
- **css-generation**: Generate theme CSS from design tokens
- **component-patterns**: Use consistent components across app and auth pages

## Resources

- [Keycloak Themes Documentation](https://www.keycloak.org/docs/latest/server_development/#_themes)
- [FreeMarker Template Guide](https://freemarker.apache.org/docs/)
- [PKCE Flow Specification](https://oauth.net/2/pkce/)
- Theme Examples: `[[Resources/Keycloak/Theme-Examples]]`
