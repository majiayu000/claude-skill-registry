---
name: orchardcore-deployments
description: Skill for configuring Orchard Core deployment plans and steps. Covers deployment plan creation, content export/import, and deployment step configuration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Deployments - Prompt Templates

## Create a Deployment Plan

You are an Orchard Core expert. Generate deployment plan configurations for Orchard Core sites.

### Guidelines

- Deployment plans export site configuration as a portable package.
- Each deployment plan contains one or more deployment steps.
- Steps are executed in order during deployment.
- Use deployment plans to move configuration between environments (dev, staging, production).
- Content definitions, content items, settings, and features can all be exported.
- Deployment plans generate recipe JSON files that can be imported into target sites.
- Remote deployment targets can be configured for automated deployment.

### Deployment Step Types

Common deployment step types include:

- `AllContentDeploymentStep` - Export all content items.
- `ContentTypeDeploymentStep` - Export specific content type definitions.
- `ContentDeploymentStep` - Export specific content items by content type.
- `SiteSettingsDeploymentStep` - Export site settings.
- `AllFeaturesDeploymentStep` - Export all enabled features.
- `RecipeFileDeploymentStep` - Include a recipe file in the deployment.
- `CustomFileDeploymentStep` - Include custom files in the deployment.

### Configuring Remote Deployment

To enable remote deployment, enable the `OrchardCore.Deployment.Remote` feature.

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Deployment",
        "OrchardCore.Deployment.Remote"
      ],
      "disable": []
    }
  ]
}
```

### Deployment Plan Recipe Export

A deployment plan produces a recipe JSON like:

```json
{
  "name": "{{DeploymentPlanName}}",
  "displayName": "{{DisplayName}}",
  "description": "Exported deployment plan",
  "author": "{{Author}}",
  "website": "",
  "version": "1.0.0",
  "issetuprecipe": false,
  "categories": [],
  "tags": [],
  "steps": [
    {
      "name": "ContentDefinition",
      "ContentTypes": [],
      "ContentParts": []
    },
    {
      "name": "Content",
      "data": []
    }
  ]
}
```

### Creating Deployment Steps in Code

```csharp
using OrchardCore.Deployment;

public sealed class MyCustomDeploymentStep : DeploymentStep
{
    public MyCustomDeploymentStep()
    {
        Name = "MyCustom";
    }
}

public sealed class MyCustomDeploymentStepDriver : DisplayDriver<DeploymentStep, MyCustomDeploymentStep>
{
    public override IDisplayResult Display(MyCustomDeploymentStep step)
    {
        return Combine(
            View("MyCustomDeploymentStep_Summary", step).Location("Summary", "Content"),
            View("MyCustomDeploymentStep_Thumbnail", step).Location("Thumbnail", "Content")
        );
    }
}

public sealed class MyCustomDeploymentSource : IDeploymentSource
{
    public async Task ProcessDeploymentStepAsync(DeploymentStep step, DeploymentPlanResult result)
    {
        if (step is not MyCustomDeploymentStep customStep)
        {
            return;
        }

        // Add data to the result
        var data = new JObject(
            new JProperty("name", "MyCustom")
        );

        result.Steps.Add(data);
    }
}
```

### Registering Deployment Steps

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddDeployment<MyCustomDeploymentStep, MyCustomDeploymentStepDriver, MyCustomDeploymentSource>();
    }
}
```
