---
name: orchardcore-security
description: Skill for configuring security and authorization in Orchard Core. Covers permission definitions, authorization services, CORS, security headers, content security policies, and OpenID Connect.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Security - Prompt Templates

## Configure Security and Authorization

You are an Orchard Core expert. Generate security and authorization configurations for Orchard Core.

### Guidelines

- Orchard Core provides a granular permission system for access control.
- Use `IAuthorizationService` for permission checks in code.
- Content-level permissions can restrict access per content type.
- Enable HTTPS redirection and security headers in production.
- OpenID Connect support is built-in for OAuth/OIDC authentication.
- CORS policies can be configured for API access.
- Rate limiting and anti-forgery protection are available.

### Enabling Security Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Security",
        "OrchardCore.Cors",
        "OrchardCore.ReverseProxy"
      ],
      "disable": []
    }
  ]
}
```

### Security Headers Configuration

Configure security headers through settings:

```json
{
  "steps": [
    {
      "name": "Settings",
      "SecurityHeadersSettings": {
        "ContentSecurityPolicy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        "PermissionsPolicy": "camera=(), microphone=(), geolocation=()",
        "ReferrerPolicy": "strict-origin-when-cross-origin",
        "ContentTypeOptions": "nosniff",
        "XFrameOptions": "SAMEORIGIN"
      }
    }
  ]
}
```

### CORS Configuration via Recipe

```json
{
  "steps": [
    {
      "name": "CorsSettings",
      "Policies": [
        {
          "Name": "Default",
          "AllowedOrigins": ["https://example.com"],
          "AllowedMethods": ["GET", "POST"],
          "AllowedHeaders": ["Content-Type", "Authorization"],
          "AllowCredentials": true
        }
      ],
      "DefaultPolicyName": "Default"
    }
  ]
}
```

### OpenID Connect Server Setup

Enable Orchard Core as an OAuth/OIDC provider:

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.OpenId",
        "OrchardCore.OpenId.Server",
        "OrchardCore.OpenId.Validation"
      ],
      "disable": []
    }
  ]
}
```

### OpenID Server Settings

```json
{
  "steps": [
    {
      "name": "Settings",
      "OpenIdServerSettings": {
        "Authority": "https://{{YourDomain}}",
        "TokenEndpointPath": "/connect/token",
        "AuthorizationEndpointPath": "/connect/authorize",
        "LogoutEndpointPath": "/connect/logout",
        "UserinfoEndpointPath": "/connect/userinfo",
        "AllowAuthorizationCodeFlow": true,
        "AllowClientCredentialsFlow": true,
        "AllowRefreshTokenFlow": true
      }
    }
  ]
}
```

### OpenID Application Registration

```json
{
  "steps": [
    {
      "name": "OpenIdApplication",
      "OpenIdApplications": [
        {
          "ClientId": "{{ClientId}}",
          "DisplayName": "{{ApplicationName}}",
          "Type": "confidential",
          "AllowAuthorizationCodeFlow": true,
          "AllowRefreshTokenFlow": true,
          "RedirectUris": "https://{{ClientDomain}}/callback",
          "PostLogoutRedirectUris": "https://{{ClientDomain}}/signout-callback"
        }
      ]
    }
  ]
}
```

### Content-Level Permissions

```csharp
using OrchardCore.Security.Permissions;

public sealed class ContentPermissions : IPermissionProvider
{
    public static readonly Permission ViewOwnContent =
        new("ViewOwnContent", "View own content items", new[] { CommonPermissions.ViewContent });

    public static readonly Permission EditOwnContent =
        new("EditOwnContent", "Edit own content items", new[] { CommonPermissions.EditContent });

    public Task<IEnumerable<Permission>> GetPermissionsAsync()
    {
        return Task.FromResult<IEnumerable<Permission>>(new[]
        {
            ViewOwnContent,
            EditOwnContent
        });
    }

    public IEnumerable<PermissionStereotype> GetDefaultStereotypes()
    {
        return new[]
        {
            new PermissionStereotype
            {
                Name = "Authenticated",
                Permissions = new[] { ViewOwnContent, EditOwnContent }
            }
        };
    }
}
```

### Content Authorization Handler

```csharp
using OrchardCore.ContentManagement;
using OrchardCore.Contents.Security;

public sealed class MyContentAuthorizationHandler : AuthorizationHandler<PermissionRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        PermissionRequirement requirement)
    {
        if (context.Resource is ContentItem contentItem)
        {
            // Custom authorization logic
            if (contentItem.Owner == context.User.Identity.Name)
            {
                context.Succeed(requirement);
            }
        }

        return Task.CompletedTask;
    }
}
```

### Reverse Proxy Configuration

When behind a reverse proxy (nginx, Azure, etc.):

```json
{
  "OrchardCore": {
    "OrchardCore_ReverseProxy": {
      "ForwardedHeaders": "XForwardedFor,XForwardedHost,XForwardedProto"
    }
  }
}
```

### Anti-Forgery Configuration

Anti-forgery tokens are automatically included in Orchard Core forms. For API endpoints:

```csharp
[HttpPost]
[IgnoreAntiforgeryToken]  // Only for API endpoints with token auth
public async Task<IActionResult> ApiEndpoint()
{
    // API logic
}
```
