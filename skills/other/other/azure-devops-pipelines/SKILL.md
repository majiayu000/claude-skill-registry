---
name: azure-devops-pipelines
description: Build Azure DevOps YAML pipelines for CI/CD, manage releases, artifacts, and deployment environments. Create build and release pipelines, configure triggers, templates, and integrate with Azure services. Use when automating builds, tests, and deployments in Azure DevOps. (project)
---

# Azure DevOps Pipelines

Expert guidance for Azure DevOps CI/CD pipeline configuration.

## When to Use This Skill

- Creating YAML-based build pipelines
- Setting up multi-stage deployments
- Configuring pipeline triggers and schedules
- Creating reusable pipeline templates
- Managing artifacts and releases
- Integrating with Azure services
- Setting up deployment environments

## Basic Pipeline Structure

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - docs/*
      - README.md

pr:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  - name: buildConfiguration
    value: 'Release'
  - group: my-variable-group

stages:
  - stage: Build
    displayName: 'Build Stage'
    jobs:
      - job: BuildJob
        steps:
          - task: DotNetCoreCLI@2
            inputs:
              command: 'build'
              projects: '**/*.csproj'
              arguments: '--configuration $(buildConfiguration)'

  - stage: Test
    displayName: 'Test Stage'
    dependsOn: Build
    jobs:
      - job: TestJob
        steps:
          - task: DotNetCoreCLI@2
            inputs:
              command: 'test'
              projects: '**/*Tests.csproj'

  - stage: Deploy
    displayName: 'Deploy Stage'
    dependsOn: Test
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployJob
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo 'Deploying...'
```

## Triggers

```yaml
# Branch triggers
trigger:
  branches:
    include:
      - main
      - release/*
    exclude:
      - feature/*

# Path filters
trigger:
  paths:
    include:
      - src/*
    exclude:
      - src/tests/*

# Tag triggers
trigger:
  tags:
    include:
      - v*

# Scheduled triggers
schedules:
  - cron: '0 0 * * *'
    displayName: 'Nightly build'
    branches:
      include:
        - main
    always: true

# PR triggers
pr:
  branches:
    include:
      - main
  paths:
    include:
      - src/*
  drafts: false
```

## Variables

```yaml
# Inline variables
variables:
  buildConfiguration: 'Release'
  dotnet
# Variable groups (from Library)
variables:
  - group: my-secrets
  - group: my-config

# Template variables
variables:
  - template: variables/common.yml
  - name: environment
    value: 'production'

# Conditional variables
variables:
  ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
    environment: 'production'
  ${{ else }}:
    environment: 'staging'

# Runtime expressions
variables:
  - name: fullPath
    value: $(Build.SourcesDirectory)/$(projectName)
```

## Jobs and Steps

```yaml
jobs:
  - job: Build
    displayName: 'Build Application'
    timeoutInMinutes: 60
    pool:
      vmImage: 'ubuntu-latest'

    steps:
      # Checkout
      - checkout: self
        clean: true
        fetchDepth: 0

      # Script tasks
      - script: |
          echo "Building..."
          npm install
          npm run build
        displayName: 'Build with npm'

      # PowerShell
      - powershell: |
          Write-Host "Running PowerShell"
        displayName: 'PowerShell script'

      # Bash
      - bash: |
          echo "Running Bash"
        displayName: 'Bash script'

      # Task shorthand
      - task: UseDotNet@2
        inputs:
          
      # Download artifact
      - download: current
        artifact: drop

      # Publish artifact
      - publish: $(Build.ArtifactStagingDirectory)
        artifact: drop
```

## Multi-Stage Pipeline

```yaml
stages:
  - stage: Build
    jobs:
      - job: BuildJob
        steps:
          - task: DotNetCoreCLI@2
            inputs:
              command: 'publish'
              publishWebProjects: true
              arguments: '--configuration Release --output $(Build.ArtifactStagingDirectory)'

          - publish: $(Build.ArtifactStagingDirectory)
            artifact: webapp

  - stage: DeployDev
    displayName: 'Deploy to Dev'
    dependsOn: Build
    jobs:
      - deployment: DeployDev
        environment: 'dev'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: webapp
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure-Connection'
                    appName: 'myapp-dev'
                    package: '$(Pipeline.Workspace)/webapp/**/*.zip'

  - stage: DeployProd
    displayName: 'Deploy to Production'
    dependsOn: DeployDev
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployProd
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: webapp
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'Azure-Connection'
                    appName: 'myapp-prod'
                    package: '$(Pipeline.Workspace)/webapp/**/*.zip'
```

## Templates

### Step Template

```yaml
# templates/build-steps.yml
parameters:
  - name: buildConfiguration
    type: string
    default: 'Release'
  - name: projects
    type: string

steps:
  - task: DotNetCoreCLI@2
    displayName: 'Restore packages'
    inputs:
      command: 'restore'
      projects: ${{ parameters.projects }}

  - task: DotNetCoreCLI@2
    displayName: 'Build'
    inputs:
      command: 'build'
      projects: ${{ parameters.projects }}
      arguments: '--configuration ${{ parameters.buildConfiguration }}'
```

### Job Template

```yaml
# templates/build-job.yml
parameters:
  - name: name
    type: string
  - name: pool
    type: object
    default:
      vmImage: 'ubuntu-latest'

jobs:
  - job: ${{ parameters.name }}
    pool: ${{ parameters.pool }}
    steps:
      - template: build-steps.yml
        parameters:
          buildConfiguration: 'Release'
          projects: '**/*.csproj'
```

### Stage Template

```yaml
# templates/deploy-stage.yml
parameters:
  - name: environment
    type: string
  - name: azureSubscription
    type: string
  - name: appName
    type: string

stages:
  - stage: Deploy_${{ parameters.environment }}
    displayName: 'Deploy to ${{ parameters.environment }}'
    jobs:
      - deployment: Deploy
        environment: ${{ parameters.environment }}
        strategy:
          runOnce:
            deploy:
              steps:
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: ${{ parameters.azureSubscription }}
                    appName: ${{ parameters.appName }}
                    package: '$(Pipeline.Workspace)/**/*.zip'
```

### Using Templates

```yaml
# azure-pipelines.yml
trigger:
  - main

stages:
  - stage: Build
    jobs:
      - template: templates/build-job.yml
        parameters:
          name: BuildApp

  - template: templates/deploy-stage.yml
    parameters:
      environment: 'dev'
      azureSubscription: 'Azure-Dev'
      appName: 'myapp-dev'

  - template: templates/deploy-stage.yml
    parameters:
      environment: 'prod'
      azureSubscription: 'Azure-Prod'
      appName: 'myapp-prod'
```

## Common Tasks

### Docker

```yaml
- task: Docker@2
  inputs:
    containerRegistry: 'myacr'
    repository: 'myapp'
    command: 'buildAndPush'
    Dockerfile: '**/Dockerfile'
    tags: |
      $(Build.BuildId)
      latest
```

### Kubernetes

```yaml
- task: KubernetesManifest@0
  inputs:
    action: 'deploy'
    kubernetesServiceConnection: 'aks-connection'
    namespace: 'default'
    manifests: |
      manifests/deployment.yml
      manifests/service.yml
    containers: |
      myacr.azurecr.io/myapp:$(Build.BuildId)
```

### Terraform

```yaml
- task: TerraformInstaller@0
  inputs:
    terraform
- task: TerraformTaskV4@4
  inputs:
    provider: 'azurerm'
    command: 'init'
    workingDirectory: '$(System.DefaultWorkingDirectory)/terraform'
    backendServiceArm: 'Azure-Connection'
    backendAzureRmResourceGroupName: 'tfstate-rg'
    backendAzureRmStorageAccountName: 'tfstatestorage'
    backendAzureRmContainerName: 'tfstate'
    backendAzureRmKey: 'terraform.tfstate'

- task: TerraformTaskV4@4
  inputs:
    provider: 'azurerm'
    command: 'apply'
    workingDirectory: '$(System.DefaultWorkingDirectory)/terraform'
    environmentServiceNameAzureRM: 'Azure-Connection'
```

### Testing

```yaml
- task: DotNetCoreCLI@2
  inputs:
    command: 'test'
    projects: '**/*Tests.csproj'
    arguments: '--configuration $(buildConfiguration) --collect:"XPlat Code Coverage"'

- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: 'Cobertura'
    summaryFileLocation: '$(Agent.TempDirectory)/**/coverage.cobertura.xml'
```

## Environments and Approvals

```yaml
# Environment with approvals (configure in Azure DevOps UI)
jobs:
  - deployment: DeployProd
    environment: 'production'  # Requires approval
    strategy:
      runOnce:
        deploy:
          steps:
            - script: echo 'Deploying to production'

# Deployment strategies
strategy:
  canary:
    increments: [10, 20, 50, 100]
    deploy:
      steps:
        - script: echo 'Canary deployment'

strategy:
  rolling:
    maxParallel: 2
    deploy:
      steps:
        - script: echo 'Rolling deployment'
```

## Best Practices

1. **Use Templates** for reusable pipeline components
2. **Separate Stages** for build, test, and deploy
3. **Use Variable Groups** for secrets and shared config
4. **Enable Branch Policies** for PR validation
5. **Use Environments** with approval gates
6. **Cache Dependencies** to speed up builds
7. **Use Service Connections** for Azure resources
8. **Pin Task Versions** to avoid breaking changes
