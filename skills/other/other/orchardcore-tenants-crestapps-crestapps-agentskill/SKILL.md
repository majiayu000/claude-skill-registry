---
name: orchardcore-tenants
description: Skill for configuring multi-tenancy in Orchard Core. Covers tenant creation, SaaS setup, tenant configuration, testing with tenants using different recipes (Blog, Agency), and tenant management APIs.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Tenants - Prompt Templates

## Configure Multi-Tenancy

You are an Orchard Core expert. Generate tenant configurations and multi-tenancy setup for Orchard Core.

### Guidelines

- Orchard Core supports multi-tenancy natively through the SaaS module.
- Each tenant is an isolated site sharing the same application instance.
- Tenants can have separate databases or share a database with table prefix isolation.
- The `Default` tenant is the main shell that manages other tenants.
- Enable `OrchardCore.Tenants` on the Default tenant to manage tenants.
- Tenants can use any setup recipe (Blog, Agency, Blank, custom).
- URL prefixes or hostnames route requests to the correct tenant.
- Always seal classes.

### Enabling Multi-Tenancy

Use the SaaS recipe during setup to get tenant management out of the box, or enable manually:

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Tenants"
      ],
      "disable": []
    }
  ]
}
```

### Setting Up with the SaaS Recipe

The SaaS recipe configures the Default tenant with tenant management features:

```bash
# Create a new project
dotnet new occms -n MyMultiTenantApp
cd MyMultiTenantApp
dotnet run

# During setup:
# - Choose the "SaaS" recipe
# - Use Sqlite for quick testing
# - Set admin credentials
```

After setup, navigate to **Configuration > Tenants** in the admin panel to create and manage tenants.

### Creating a Tenant via Admin UI

1. Navigate to **Configuration > Tenants**.
2. Click **Create Tenant**.
3. Set the **Name** (technical name, no spaces).
4. Set the **URL Prefix** (e.g., `blog`) or **URL Host** (e.g., `blog.example.com`).
5. Select a **Recipe** (Blog, Blank, etc.).
6. Choose a **Database Provider**.
7. Optionally set a **Table Prefix** if sharing a database.
8. Click **Create**.
9. Click **Setup** to initialize the tenant.

### Creating a Tenant via Recipe

```json
{
  "steps": [
    {
      "name": "Tenants",
      "Tenants": [
        {
          "Name": "{{TenantName}}",
          "RequestUrlPrefix": "{{UrlPrefix}}",
          "RequestUrlHost": "",
          "State": "Uninitialized",
          "FeatureProfiles": [],
          "Description": "{{Description}}"
        }
      ]
    }
  ]
}
```

### Creating a Tenant via Tenants API

```bash
# Create a tenant using the REST API
curl -X POST https://localhost:5001/api/tenants \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {{token}}" \
  -d '{
    "Name": "{{TenantName}}",
    "RequestUrlPrefix": "{{UrlPrefix}}",
    "Description": "{{Description}}",
    "RecipeName": "Blog",
    "DatabaseProvider": "Sqlite",
    "Category": ""
  }'
```

### Setting Up a Tenant Programmatically

```bash
# Setup an uninitialized tenant
curl -X POST https://localhost:5001/api/tenants/setup \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {{token}}" \
  -d '{
    "Name": "{{TenantName}}",
    "SiteName": "{{SiteName}}",
    "DatabaseProvider": "Sqlite",
    "RecipeName": "Blog",
    "UserName": "admin",
    "Email": "admin@{{tenant}}.example.com",
    "Password": "{{SecurePassword}}"
  }'
```

### Testing with Blog Tenant

A common pattern for testing is to create a Blog tenant:

```bash
# 1. Start the application with SaaS recipe
dotnet run

# 2. Set up the Default shell with SaaS recipe

# 3. Create a "blog" tenant via the admin UI:
#    - Name: Blog
#    - URL Prefix: blog
#    - Recipe: Blog
#    - Database: Sqlite

# 4. Set up the blog tenant

# 5. Access the blog at https://localhost:5001/blog
```

### Tenant Configuration in appsettings.json

```json
{
  "OrchardCore": {
    "Default": {
      "State": "Running",
      "RequestUrlHost": "",
      "RequestUrlPrefix": ""
    },
    "{{TenantName}}": {
      "State": "Running",
      "RequestUrlHost": "",
      "RequestUrlPrefix": "{{UrlPrefix}}",
      "DatabaseProvider": "Sqlite",
      "ConnectionString": "",
      "TablePrefix": "{{TablePrefix}}"
    }
  }
}
```

### Accessing Tenant Information in Code

```csharp
using OrchardCore.Environment.Shell;

public sealed class TenantInfoService
{
    private readonly ShellSettings _shellSettings;

    public TenantInfoService(ShellSettings shellSettings)
    {
        _shellSettings = shellSettings;
    }

    public string GetCurrentTenantName()
    {
        return _shellSettings.Name;
    }

    public string GetRequestUrlPrefix()
    {
        return _shellSettings["RequestUrlPrefix"];
    }
}
```

### Running Tenant-Specific Code

```csharp
using OrchardCore.Environment.Shell;
using OrchardCore.Environment.Shell.Scope;

public sealed class TenantOperationService
{
    private readonly IShellHost _shellHost;

    public TenantOperationService(IShellHost shellHost)
    {
        _shellHost = shellHost;
    }

    public async Task RunInTenantAsync(string tenantName, Func<ShellScope, Task> action)
    {
        var shellScope = await _shellHost.GetScopeAsync(tenantName);
        await shellScope.UsingAsync(action);
    }
}
```

### Feature Profiles for Tenants

Control which features are available to tenants:

```json
{
  "OrchardCore": {
    "OrchardCore_Tenants": {
      "TenantFeatureProfiles": {
        "Standard": {
          "IncludeAllFeatures": false,
          "ExcludedFeatures": [
            "OrchardCore.Tenants"
          ]
        }
      }
    }
  }
}
```
