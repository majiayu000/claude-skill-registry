---
name: orchardcore-openid
description: Skill for configuring and managing OpenID Connect in Orchard Core. Covers server setup, client application registration, authorization flows, token validation, external authentication providers, JWT bearer authentication for APIs, and recipe-based configuration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core OpenID Connect - Prompt Templates

## Module Overview

The `OrchardCore.OpenId` module provides a complete OpenID Connect and OAuth 2.0 implementation for Orchard Core applications. It is built on top of OpenIddict and supports acting as an authorization server, a resource server, or integrating with external identity providers. Enable the relevant sub-features depending on your scenario:

- **OrchardCore.OpenId** — Core services and shared infrastructure.
- **OrchardCore.OpenId.Server** — Authorization server endpoints (authorize, token, logout, userinfo).
- **OrchardCore.OpenId.Client** — External provider integration (Azure AD, Google, etc.).
- **OrchardCore.OpenId.Validation** — Token validation for resource servers / APIs.

## OpenID Connect Server Configuration

You are an Orchard Core expert. Configure the OpenID Connect authorization server.

### Guidelines

- Enable the `OrchardCore.OpenId.Server` feature before configuring server settings.
- Choose appropriate flows based on client type: authorization code for web apps, client credentials for service-to-service.
- Always use HTTPS in production for all endpoint URIs.
- Configure token lifetimes according to your security requirements.
- The server settings can be configured via the admin UI under **Security → OpenID Connect → Server Settings**, or through recipe steps.

### Server Settings via Migration

```csharp
public sealed class OpenIdServerMigrations : DataMigration
{
    private readonly IOpenIdServerService _serverService;

    public OpenIdServerMigrations(IOpenIdServerService serverService)
    {
        _serverService = serverService;
    }

    public async Task<int> CreateAsync()
    {
        var settings = await _serverService.GetSettingsAsync();

        settings.AllowAuthorizationCodeFlow = true;
        settings.AllowClientCredentialsFlow = true;
        settings.AllowRefreshTokenFlow = true;
        settings.UseRollingRefreshTokens = true;
        settings.AuthorizationEndpointPath = "/connect/authorize";
        settings.TokenEndpointPath = "/connect/token";
        settings.LogoutEndpointPath = "/connect/logout";
        settings.UserinfoEndpointPath = "/connect/userinfo";

        await _serverService.UpdateSettingsAsync(settings);

        return 1;
    }
}
```

## Client Application Registration

Register OAuth/OpenID Connect client applications that will authenticate against the server.

### Guidelines

- Every client must have a unique `ClientId`.
- Confidential clients (server-side apps) must have a `ClientSecret`.
- Public clients (SPAs, native apps) must not store secrets; use authorization code flow with PKCE.
- Set `ConsentType` to `Explicit` when user consent should be prompted, or `Implicit` for trusted first-party apps.
- Specify only the redirect URIs your application actually uses.
- Assign the minimum required scopes and roles to each client.

### Client Registration via Migration

```csharp
public sealed class OpenIdClientMigrations : DataMigration
{
    private readonly IOpenIdApplicationManager _applicationManager;

    public OpenIdClientMigrations(IOpenIdApplicationManager applicationManager)
    {
        _applicationManager = applicationManager;
    }

    public async Task<int> CreateAsync()
    {
        await _applicationManager.CreateAsync(new OpenIdApplicationDescriptor
        {
            ClientId = "my-web-app",
            DisplayName = "My Web Application",
            ClientSecret = "your-client-secret-here",
            ClientType = OpenIddictConstants.ClientTypes.Confidential,
            ConsentType = OpenIddictConstants.ConsentTypes.Implicit,
            Permissions =
            {
                OpenIddictConstants.Permissions.Endpoints.Authorization,
                OpenIddictConstants.Permissions.Endpoints.Token,
                OpenIddictConstants.Permissions.Endpoints.Logout,
                OpenIddictConstants.Permissions.GrantTypes.AuthorizationCode,
                OpenIddictConstants.Permissions.GrantTypes.RefreshToken,
                OpenIddictConstants.Permissions.ResponseTypes.Code,
                OpenIddictConstants.Permissions.Scopes.Email,
                OpenIddictConstants.Permissions.Scopes.Profile,
                OpenIddictConstants.Permissions.Scopes.Roles,
                OpenIddictConstants.Permissions.Prefixes.Scope + "api",
            },
            RedirectUris = { new Uri("https://myapp.example.com/signin-oidc") },
            PostLogoutRedirectUris = { new Uri("https://myapp.example.com/signout-callback-oidc") },
        });

        return 1;
    }
}
```

## Authorization Flows

### Authorization Code Flow

The recommended flow for server-side web applications. The client exchanges an authorization code for tokens at the token endpoint.

- Enable `AllowAuthorizationCodeFlow` in server settings.
- The client must have `GrantTypes.AuthorizationCode` and `ResponseTypes.Code` permissions.
- Always pair with refresh tokens for long-lived sessions.

### Client Credentials Flow

Used for machine-to-machine communication where no user context is needed.

- Enable `AllowClientCredentialsFlow` in server settings.
- The client must be confidential and have `GrantTypes.ClientCredentials` permission.
- Tokens issued via client credentials do not contain user claims.

### Implicit Flow

Primarily used for legacy SPAs. Prefer authorization code flow with PKCE for new applications.

- Enable `AllowImplicitFlow` in server settings.
- The client must have `GrantTypes.Implicit` and either `ResponseTypes.IdToken` or `ResponseTypes.IdTokenToken` permissions.

## Token Endpoint and Validation

The token endpoint (`/connect/token` by default) issues access tokens, identity tokens, and refresh tokens.

### Guidelines

- Access tokens are short-lived by default. Use refresh tokens for session continuity.
- Configure `AccessTokenLifetime` and `RefreshTokenLifetime` in server settings.
- Enable rolling refresh tokens (`UseRollingRefreshTokens`) to rotate refresh tokens on each use.
- Token validation on resource servers uses the `OrchardCore.OpenId.Validation` feature.

## Scopes and Claims

### Registering Custom Scopes

```csharp
public sealed class OpenIdScopeMigrations : DataMigration
{
    private readonly IOpenIdScopeManager _scopeManager;

    public OpenIdScopeMigrations(IOpenIdScopeManager scopeManager)
    {
        _scopeManager = scopeManager;
    }

    public async Task<int> CreateAsync()
    {
        await _scopeManager.CreateAsync(new OpenIdScopeDescriptor
        {
            Name = "api",
            DisplayName = "API Access",
            Description = "Grants access to the application API endpoints.",
            Resources = { "my-resource-server" },
        });

        return 1;
    }
}
```

### Standard Scopes

- `openid` — Required for all OpenID Connect requests. Returns a `sub` claim.
- `profile` — Returns user profile claims (name, family_name, etc.).
- `email` — Returns `email` and `email_verified` claims.
- `roles` — Returns role membership claims.
- `phone` — Returns phone number claims.

## External Authentication Providers

The `OrchardCore.OpenId.Client` feature enables federated sign-in with external identity providers.

### Guidelines

- Configure external providers via admin UI under **Security → OpenID Connect → Client Settings**.
- Each provider requires a `ClientId`, `ClientSecret` (for confidential providers), and an `Authority` URI.
- Map external claims to Orchard Core user properties as needed.
- Supported providers include Azure AD, Azure AD B2C, Google, Microsoft, and any standard OpenID Connect provider.

### External Provider Setup via Startup

```csharp
public sealed class ExternalProviderStartup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddAuthentication()
            .AddOpenIdConnect("AzureAD", "Azure Active Directory", options =>
            {
                options.Authority = "https://login.microsoftonline.com/{tenant-id}/v2.0";
                options.ClientId = "your-azure-client-id";
                options.ClientSecret = "your-azure-client-secret";
                options.ResponseType = OpenIdConnectResponseType.Code;
                options.SaveTokens = true;
                options.Scope.Add("openid");
                options.Scope.Add("profile");
                options.Scope.Add("email");
                options.TokenValidationParameters.NameClaimType = "name";
            });
    }
}
```

## JWT Bearer Token Authentication for APIs

Enable JWT bearer authentication to protect API endpoints using tokens issued by the OpenID Connect server.

### Guidelines

- Enable the `OrchardCore.OpenId.Validation` feature on the resource server.
- Configure the validation settings to point to the authorization server's authority URI.
- Use `[Authorize]` attributes on API controllers to enforce authentication.
- The validation feature supports both local validation (same application as server) and remote validation (separate resource server).

### API Controller with JWT Authentication

```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize(AuthenticationSchemes = OpenIddictValidationAspNetCoreDefaults.AuthenticationScheme)]
public sealed class ProductsController : ControllerBase
{
    [HttpGet]
    public IActionResult GetAll()
    {
        var userId = User.FindFirstValue(OpenIddictConstants.Claims.Subject);
        return Ok(new { Message = "Authenticated", UserId = userId });
    }

    [HttpGet("admin")]
    [Authorize(Roles = "Administrator")]
    public IActionResult GetAdmin()
    {
        return Ok(new { Message = "Admin access granted" });
    }
}
```

### Validation Settings via Migration

```csharp
public sealed class OpenIdValidationMigrations : DataMigration
{
    private readonly IOpenIdValidationService _validationService;

    public OpenIdValidationMigrations(IOpenIdValidationService validationService)
    {
        _validationService = validationService;
    }

    public async Task<int> CreateAsync()
    {
        var settings = await _validationService.GetSettingsAsync();

        settings.Authority = new Uri("https://auth.example.com");
        settings.Audience = "my-resource-server";

        await _validationService.UpdateSettingsAsync(settings);

        return 1;
    }
}
```

## Recipe Steps for OpenID Configuration

Use recipe steps to declaratively configure OpenID Connect settings, applications, and scopes during site setup or deployment.

### OpenID Server Settings Recipe Step

```json
{
  "steps": [
    {
      "name": "OpenIdServerSettings",
      "AllowAuthorizationCodeFlow": true,
      "AllowClientCredentialsFlow": true,
      "AllowRefreshTokenFlow": true,
      "UseRollingRefreshTokens": true,
      "AuthorizationEndpointPath": "/connect/authorize",
      "TokenEndpointPath": "/connect/token",
      "LogoutEndpointPath": "/connect/logout",
      "UserinfoEndpointPath": "/connect/userinfo"
    }
  ]
}
```

### OpenID Application Recipe Step

```json
{
  "steps": [
    {
      "name": "OpenIdApplication",
      "ClientId": "spa-client",
      "DisplayName": "Single Page Application",
      "ClientType": "public",
      "ConsentType": "implicit",
      "AllowAuthorizationCodeFlow": true,
      "AllowRefreshTokenFlow": true,
      "RequireProofKeyForCodeExchange": true,
      "RedirectUris": "https://spa.example.com/callback",
      "PostLogoutRedirectUris": "https://spa.example.com/logout-callback",
      "AllowedScopes": [
        "openid",
        "profile",
        "email",
        "api"
      ]
    }
  ]
}
```

### OpenID Scope Recipe Step

```json
{
  "steps": [
    {
      "name": "OpenIdScope",
      "ScopeName": "api",
      "DisplayName": "API Access",
      "Description": "Grants access to protected API endpoints.",
      "Resources": "my-resource-server"
    }
  ]
}
```

### OpenID Validation Settings Recipe Step

```json
{
  "steps": [
    {
      "name": "OpenIdValidationSettings",
      "Authority": "https://auth.example.com",
      "Audience": "my-resource-server"
    }
  ]
}
```

## Admin UI Configuration

OpenID settings are managed through the admin dashboard:

- **Security → OpenID Connect → Server Settings** — Configure authorization server endpoints, supported flows, and token lifetimes.
- **Security → OpenID Connect → Applications** — Register and manage client applications.
- **Security → OpenID Connect → Scopes** — Define custom scopes and associated resources.
- **Security → OpenID Connect → Client Settings** — Configure external identity providers for federated login.
- **Security → OpenID Connect → Validation Settings** — Configure token validation for resource server scenarios.
