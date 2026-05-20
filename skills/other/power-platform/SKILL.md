---
name: power-platform
description: Expert guidance for Microsoft Power Platform development including PAC CLI, ALM lifecycle, solution management, environment strategy, and CI/CD pipelines. Use when working with Power Platform solutions, environment promotion, managed/unmanaged solutions, or Power Platform Build Tools.
---

# Power Platform Development

Expert guidance for Microsoft Power Platform ALM, PAC CLI operations, solution management, and CI/CD pipelines.

## Triggers

Use this skill when you see:
- power platform, pac cli, power platform cli
- solution export, solution import, managed solution
- power platform alm, environment promotion
- power platform ci/cd, build tools
- pcf init, plugin init, pac auth

## Instructions

### PAC CLI Authentication

```bash
# Create authentication profile
pac auth create --environment "https://myorg.crm.dynamics.com"

# Create with service principal (CI/CD)
pac auth create --applicationId <app-id> --clientSecret <secret> --tenant <tenant-id> --environment "https://myorg.crm.dynamics.com"

# List and select profiles
pac auth list
pac auth select --index 1

# Check current environment
pac env who
```

### Solution Operations

```bash
# Export solution (unmanaged for development)
pac solution export --path ./solutions/MySolution.zip --name MySolution --managed false

# Export solution (managed for deployment)
pac solution export --path ./solutions/MySolution_managed.zip --name MySolution --managed true

# Import solution
pac solution import --path ./solutions/MySolution_managed.zip --publish-changes

# Unpack for source control (folder structure)
pac solution unpack --zipfile ./solutions/MySolution.zip --folder ./src/MySolution --processCanvasApps

# Pack from source control
pac solution pack --zipfile ./solutions/MySolution.zip --folder ./src/MySolution --processCanvasApps

# Publish customizations
pac solution publish

# Run solution checker
pac solution check --path ./solutions/MySolution.zip --geo unitedstates
```

### Environment Management

```bash
# List environments
pac env list

# Select environment
pac env select --environment "https://myorg.crm.dynamics.com"

# Who am I (current context)
pac env who

# Copy environment (for testing)
pac env copy --source-env <source-id> --target-env <target-id> --type MinimalCopy
```

### PCF and Plugin Init

```bash
# Initialize PCF control project
pac pcf init --namespace Contoso --name MyControl --template field --framework react --run-npm-install

# Initialize plugin project
pac plugin init

# Generate early-bound types
pac modelbuilder build
```

### CI/CD with Azure DevOps Build Tools

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'windows-latest'

steps:
  - task: microsoft-IsvExpTools.PowerPlatform-BuildTools.tool-installer.PowerPlatformToolInstaller@2
    displayName: 'Install Power Platform Build Tools'

  - task: microsoft-IsvExpTools.PowerPlatform-BuildTools.pack-solution.PowerPlatformPackSolution@2
    displayName: 'Pack Solution'
    inputs:
      SolutionSourceFolder: '$(Build.SourcesDirectory)/src/MySolution'
      SolutionOutputFile: '$(Build.ArtifactStagingDirectory)/MySolution_managed.zip'
      SolutionType: 'Managed'
      ProcessCanvasApps: true

  - task: microsoft-IsvExpTools.PowerPlatform-BuildTools.checker.PowerPlatformChecker@2
    displayName: 'Solution Checker'
    inputs:
      authenticationType: 'PowerPlatformSPN'
      PowerPlatformSPN: 'PowerPlatformSPN'
      FilesToAnalyze: '$(Build.ArtifactStagingDirectory)/MySolution_managed.zip'
      RuleSet: '0ad12346-e108-40b8-a956-9a8f95ea18c9'

  - task: microsoft-IsvExpTools.PowerPlatform-BuildTools.import-solution.PowerPlatformImportSolution@2
    displayName: 'Import to Target'
    inputs:
      authenticationType: 'PowerPlatformSPN'
      PowerPlatformSPN: 'PowerPlatformSPN'
      SolutionInputFile: '$(Build.ArtifactStagingDirectory)/MySolution_managed.zip'
      PublishChanges: true
```

### CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy-solution.yml
name: Deploy Power Platform Solution
on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - name: Pack solution
        uses: microsoft/powerplatform-actions/pack-solution@v1
        with:
          solution-folder: src/MySolution
          solution-file: out/MySolution_managed.zip
          solution-type: Managed
          process-canvas-apps: true

      - name: Import to target
        uses: microsoft/powerplatform-actions/import-solution@v1
        with:
          environment-url: ${{ secrets.PP_ENV_URL }}
          app-id: ${{ secrets.PP_APP_ID }}
          client-secret: ${{ secrets.PP_CLIENT_SECRET }}
          tenant-id: ${{ secrets.PP_TENANT_ID }}
          solution-file: out/MySolution_managed.zip
          publish-changes: true
```

## Best Practices

| Practice | Description |
|----------|-------------|
| **Environment strategy** | Use Dev (unmanaged) -> Test (managed) -> Prod (managed) promotion |
| **Solution segmentation** | Split large solutions by functional area (Core, UI, Integrations) |
| **Unmanaged in dev only** | Only develop in unmanaged; deploy managed to Test/Prod |
| **Source control** | Always unpack solutions to source control with `pac solution unpack` |
| **Connection references** | Use connection references instead of hardcoded connections |
| **Environment variables** | Store configuration in Dataverse environment variables |
| **Solution checker** | Run `pac solution check` before every deployment |
| **Publisher prefix** | Use a consistent publisher prefix across all components |

## Common Workflows

### New Solution Setup
1. Create solution in dev environment with consistent publisher
2. Add components (tables, apps, flows, etc.)
3. Export and unpack to source control
4. Set up CI/CD pipeline for automated deployment
5. Configure environment variables and connection references

### Environment Promotion
1. Export unmanaged from Dev
2. Pack as managed for deployment
3. Run solution checker
4. Import managed to Test, validate
5. Import managed to Prod with approvals
6. Verify post-deployment

### Source Control Workflow
1. `pac solution export` from dev environment
2. `pac solution unpack` to repo folder
3. Commit and push changes
4. CI pipeline packs and deploys managed solution
5. Use PRs for code review of customizations
