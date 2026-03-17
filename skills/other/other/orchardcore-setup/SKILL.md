---
name: orchardcore-setup
description: Skill for creating and setting up Orchard Core web applications. Covers project creation, CMS module configuration, adding modules to the web project, running setup, testing with the Blog recipe, and configuring tenants for multi-site testing.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Setup - Prompt Templates

## Create and Set Up an Orchard Core Application

You are an Orchard Core expert. Generate project setup instructions and configuration for Orchard Core web applications.

### Guidelines

- Orchard Core applications are ASP.NET Core web apps that reference Orchard Core NuGet packages.
- Use the `dotnet new` templates or manual project creation.
- The `Program.cs` file configures Orchard Core services and middleware.
- Setup recipes (Blog, Agency, SaaS, Blank) define the initial site configuration.
- Database providers include Sqlite (default), SqlServer, PostgreSql, and MySql.
- CMS modules are added as NuGet package references in the `.csproj` file.
- Always seal classes defined in your module code.

### Creating a New Orchard Core Web Application

```bash
# Install the Orchard Core templates
dotnet new install OrchardCore.ProjectTemplates

# Create a new CMS web application
dotnet new occms -n {{ProjectName}}
cd {{ProjectName}}

# Run the application
dotnet run
```

### Manual Project Setup (Without Templates)

Create a new ASP.NET Core web application:

```bash
dotnet new web -n {{ProjectName}}
cd {{ProjectName}}

# Add the Orchard Core CMS package
dotnet add package OrchardCore.Application.Cms.Targets --version 2.*
```

### Program.cs Configuration

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOrchardCms();

var app = builder.Build();

app.UseStaticFiles();
app.UseOrchardCore();

app.Run();
```

### Program.cs with Additional CMS Configuration

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddOrchardCms()
    .AddSetupFeatures("OrchardCore.AutoSetup")
    .ConfigureServices(tenantServices =>
    {
        // Register tenant-level services here
    })
    .Configure((app, routes, services) =>
    {
        // Configure tenant-level middleware here
    });

var app = builder.Build();

app.UseStaticFiles();
app.UseOrchardCore();

app.Run();
```

### Adding CMS Modules to the Project

Add NuGet packages for the modules you need. **All modules** — whether from OrchardCore directly, CrestApps, Lombiq, or any community source — must be installed in the **web project** (the startup project of the solution):

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="OrchardCore.Application.Cms.Targets" Version="2.*" />

    <!-- Third-party modules are also added to the web project -->
    <PackageReference Include="CrestApps.OrchardCore.AI" Version="1.*" />
    <PackageReference Include="Lombiq.HelpfulExtensions.OrchardCore" Version="1.*" />
  </ItemGroup>

</Project>
```

### Adding a Custom CMS Module to the Web Project

To add a local CMS module to the web project (your own or any third-party module):

```xml
<ItemGroup>
  <!-- Reference a local module project in the web project -->
  <ProjectReference Include="../MyModule/MyModule.csproj" />
  <ProjectReference Include="../ThirdParty.Module/ThirdParty.Module.csproj" />
</ItemGroup>
```

### Setup via the Admin UI

After running the application, navigate to `/` to access the setup screen:

1. Choose a **Site Name**.
2. Select a **Recipe** (Blog, Agency, SaaS, Blank, or custom).
3. Choose a **Database Provider** (Sqlite, SQL Server, PostgreSQL, MySQL).
4. Provide the **Connection String** (except for Sqlite).
5. Set an **Admin Username** and **Password**.
6. Click **Finish Setup**.

### Auto-Setup via Configuration

Configure automatic setup in `appsettings.json`:

```json
{
  "OrchardCore": {
    "OrchardCore_AutoSetup": {
      "AutoSetupPath": "",
      "Tenants": [
        {
          "ShellName": "Default",
          "SiteName": "{{SiteName}}",
          "SiteTimeZone": "America/New_York",
          "DatabaseProvider": "Sqlite",
          "RecipeName": "Blog",
          "UserName": "admin",
          "Email": "admin@example.com",
          "Password": "{{SecurePassword}}"
        }
      ]
    }
  }
}
```

### Testing with the Blog Recipe

The Blog recipe sets up a complete blogging site with:
- Blog content type and listing
- Theme (TheBlogTheme)
- Menu and layers configured
- Sample content items

```bash
# Create a project and run it
dotnet new occms -n MyBlogSite
cd MyBlogSite
dotnet run

# Navigate to https://localhost:5001
# Select the "Blog" recipe during setup
```

### Creating a Custom Setup Recipe

Place recipe files in the `Recipes` folder of your module:

```json
{
  "name": "{{RecipeName}}",
  "displayName": "{{DisplayName}}",
  "description": "{{Description}}",
  "author": "{{Author}}",
  "website": "{{Website}}",
  "version": "1.0.0",
  "issetuprecipe": true,
  "categories": ["default"],
  "tags": [],
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Contents",
        "OrchardCore.ContentTypes",
        "OrchardCore.Title",
        "OrchardCore.Alias",
        "OrchardCore.Autoroute",
        "OrchardCore.Html",
        "OrchardCore.Menu",
        "OrchardCore.Navigation",
        "OrchardCore.Themes",
        "OrchardCore.Admin",
        "OrchardCore.Settings",
        "TheTheme",
        "TheAdmin"
      ],
      "disable": []
    },
    {
      "name": "Themes",
      "Site": "TheTheme",
      "Admin": "TheAdmin"
    }
  ]
}
```
