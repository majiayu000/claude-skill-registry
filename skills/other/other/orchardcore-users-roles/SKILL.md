---
name: orchardcore-users-roles
description: Skill for managing users, roles, and permissions in Orchard Core. Covers user registration, role creation, permission definitions, custom user settings, and authentication configuration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Users & Roles - Prompt Templates

## Manage Users, Roles, and Permissions

You are an Orchard Core expert. Generate code and configuration for user management, roles, and permissions.

### Guidelines

- Enable `OrchardCore.Users` and `OrchardCore.Roles` for user and role management.
- Custom permissions should extend `IPermissionProvider`.
- Roles group permissions together for easier management.
- Use `[Authorize]` attributes or `IAuthorizationService` for permission checks.
- Custom user settings allow extending user profiles with additional fields.
- Registration and login can be customized through settings and recipes.
- External authentication providers (Google, Microsoft, etc.) can be added.

### Enabling User and Role Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Users",
        "OrchardCore.Users.Registration",
        "OrchardCore.Users.ResetPassword",
        "OrchardCore.Users.CustomUserSettings",
        "OrchardCore.Roles"
      ],
      "disable": []
    }
  ]
}
```

### Defining Custom Permissions

```csharp
using OrchardCore.Security.Permissions;

public sealed class Permissions : IPermissionProvider
{
    public static readonly Permission Manage{{Feature}} =
        new("Manage{{Feature}}", "Manage {{Feature}}");

    public static readonly Permission View{{Feature}} =
        new("View{{Feature}}", "View {{Feature}}");

    public Task<IEnumerable<Permission>> GetPermissionsAsync()
    {
        return Task.FromResult<IEnumerable<Permission>>(new[]
        {
            Manage{{Feature}},
            View{{Feature}}
        });
    }

    public IEnumerable<PermissionStereotype> GetDefaultStereotypes()
    {
        return new[]
        {
            new PermissionStereotype
            {
                Name = "Administrator",
                Permissions = new[] { Manage{{Feature}} }
            },
            new PermissionStereotype
            {
                Name = "Editor",
                Permissions = new[] { View{{Feature}} }
            }
        };
    }
}
```

### Registering Permission Provider

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IPermissionProvider, Permissions>();
    }
}
```

### Checking Permissions in Code

```csharp
using Microsoft.AspNetCore.Authorization;

public sealed class MyController : Controller
{
    private readonly IAuthorizationService _authorizationService;

    public MyController(IAuthorizationService authorizationService)
    {
        _authorizationService = authorizationService;
    }

    public async Task<IActionResult> Index()
    {
        if (!await _authorizationService.AuthorizeAsync(User, Permissions.View{{Feature}}))
        {
            return Forbid();
        }

        return View();
    }
}
```

### Checking Permissions in Liquid

```liquid
{% if User | has_permission: "ViewMyFeature" %}
    <p>You have access to this feature.</p>
{% endif %}
```

### Creating Roles via Recipe

```json
{
  "steps": [
    {
      "name": "Roles",
      "Roles": [
        {
          "Name": "{{RoleName}}",
          "Description": "{{RoleDescription}}",
          "Permissions": [
            "View{{Feature}}",
            "AccessAdminPanel"
          ]
        }
      ]
    }
  ]
}
```

### Custom User Settings

Extend user profiles with custom settings by enabling `OrchardCore.Users.CustomUserSettings`:

```csharp
// Define a custom user settings content type via migration
await _contentDefinitionManager.AlterTypeDefinitionAsync("UserProfile", type => type
    .DisplayedAs("User Profile")
    .Stereotype("CustomUserSettings")
    .WithPart("UserProfile", part => part
        .WithPosition("0")
    )
);

await _contentDefinitionManager.AlterPartDefinitionAsync("UserProfile", part => part
    .WithField("Bio", field => field
        .OfType("TextField")
        .WithDisplayName("Bio")
        .WithEditor("TextArea")
        .WithPosition("0")
    )
    .WithField("Avatar", field => field
        .OfType("MediaField")
        .WithDisplayName("Avatar")
        .WithPosition("1")
    )
);
```

### User Registration Settings via Recipe

```json
{
  "steps": [
    {
      "name": "Settings",
      "RegistrationSettings": {
        "UsersCanRegister": "AllowRegistration",
        "NoPasswordForExternalUsers": false,
        "NoUsernameForExternalUsers": false,
        "NoEmailForExternalUsers": false,
        "UseScriptToGenerateUsername": false
      }
    }
  ]
}
```

### External Authentication (e.g., Microsoft)

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Microsoft.Authentication.AzureAD"
      ],
      "disable": []
    }
  ]
}
```

Configuration in `appsettings.json`:

```json
{
  "OrchardCore": {
    "OrchardCore_Microsoft_Authentication_AzureAD": {
      "AppId": "{{ClientId}}",
      "TenantId": "{{TenantId}}",
      "CallbackPath": "/signin-oidc"
    }
  }
}
```
