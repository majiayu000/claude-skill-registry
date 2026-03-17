---
name: sprint-254-features
description: Azure DevOps Sprint 254-262 new features and enhancements (2025)
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Azure DevOps 2025 Latest Features (Sprints 254-262)

## New Expression Functions (Sprint 248)

### iif() - Ternary Conditional Operator

```yaml
# Syntax: iif(condition, valueIfTrue, valueIfFalse)

variables:
  environment: 'production'
  # Use iif for conditional values
  instanceCount: ${{ iif(eq(variables.environment, 'production'), 10, 2) }}
  deploymentSlot: ${{ iif(eq(variables.environment, 'production'), 'production', 'staging') }}

steps:
- script: echo "Deploying ${{ variables.instanceCount }} instances to ${{ variables.deploymentSlot }}"
```

### trim() - Remove Whitespace

```yaml
parameters:
- name: branchName
  type: string
  default: ' feature/my-branch '

variables:
  # Remove leading/trailing whitespace
  cleanBranch: ${{ trim(parameters.branchName) }}
  # Result: 'feature/my-branch' (no spaces)
```

## New Predefined Variables (Sprint 253)

### Build.StageRequestedBy

Who requested the stage execution:

```yaml
stages:
- stage: Deploy
  jobs:
  - job: DeployJob
    steps:
    - script: |
        echo "Stage requested by: $(Build.StageRequestedBy)"
        echo "Stage requester ID: $(Build.StageRequestedById)"
      displayName: 'Log stage requester'

    # Use for approval notifications
    - task: SendEmail@1
      inputs:
        to: 'approvers@example.com'
        subject: 'Deployment requested by $(Build.StageRequestedBy)'
```

## Stage Dependencies Visualization (Sprint 254)

View stage dependencies when stage is expanded in pipeline UI:

```yaml
stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Building..."

- stage: Test
  dependsOn: Build  # Shown visually when expanded
  jobs:
  - job: TestJob
    steps:
    - script: echo "Testing..."

- stage: Deploy_USEast
  dependsOn: Test
  jobs:
  - job: DeployJob
    steps:
    - script: echo "Deploying to US East..."

- stage: Deploy_EUWest
  dependsOn: Test  # Parallel with Deploy_USEast - visualized clearly
  jobs:
  - job: DeployJob
    steps:
    - script: echo "Deploying to EU West..."
```

**Benefits:**
- Visual dependency graph in UI
- Easier debugging of complex pipelines
- Clear multi-region deployment patterns
- Identify parallel vs sequential stages

## New OS Images

### Ubuntu-24.04 (General Availability)

```yaml
pool:
  vmImage: 'ubuntu-24.04'  # Latest LTS - Recommended
  # OR use ubuntu-latest (will map to 24.04 soon)
  # vmImage: 'ubuntu-latest'

steps:
- script: |
    lsb_release -a
    # Ubuntu 24.04 LTS (Noble Numbat)
```

**Key Information:**
- Ubuntu 24.04 is now generally available
- `ubuntu-latest` will soon map to `ubuntu-24.04` (currently `ubuntu-22.04`)
- Ubuntu 20.04 fully removed April 30, 2025

### Windows Server 2025 (Coming June 2025)

```yaml
pool:
  vmImage: 'windows-2025'  # GA: June 16, 2025

steps:
- pwsh: |
    Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
```

**Key Information:**
- General availability: June 16, 2025
- `windows-latest` will map to `windows-2025` starting September 2, 2025
- Windows Server 2019 extended support until December 31, 2025

### macOS-15 Sequoia (Available)

```yaml
pool:
  vmImage: 'macOS-15'  # Sequoia

steps:
- script: |
    sw_vers
    # macOS 15.x (Sequoia)
```

**Key Information:**
- macOS 13 Ventura deprecation starts September 1, 2025
- macOS 13 retirement planned for December 4, 2025
- Apple Silicon (ARM64) support in preview

### ⚠️ Deprecated and Retired Images

**Fully Removed (2025):**
- **Ubuntu 20.04** - Removed April 30, 2025
- **.NET 6** - Removed from Windows and Ubuntu images August 1, 2025

**Extended Support:**
- **Windows Server 2019** - Extended until December 31, 2025
  - Deprecation starts: June 1, 2025
  - Brownout periods: June 3-24, 2025
  - Final removal: December 31, 2025

**Upcoming Deprecations:**
- **macOS 13 Ventura** - Deprecation: September 1, 2025, Retirement: December 4, 2025

**Migration Recommendations:**
```yaml
# Ubuntu Migration
# OLD (Removed)
pool:
  vmImage: 'ubuntu-20.04'

# NEW (Recommended)
pool:
  vmImage: 'ubuntu-24.04'  # Best: explicit version
  # OR
  vmImage: 'ubuntu-latest'  # Will map to 24.04 soon

# Windows Migration
# OLD (Being deprecated)
pool:
  vmImage: 'windows-2019'

# NEW (Recommended)
pool:
  vmImage: 'windows-2022'  # Current stable
  # OR wait for
  vmImage: 'windows-2025'  # GA June 2025
```

## GitHub Integration Improvements

### Auto-linked Pull Requests

GitHub branches linked to work items automatically link PRs:

```yaml
# When PR is created for branch linked to work item,
# PR automatically appears in work item's Development section

trigger:
  branches:
    include:
    - feature/*
    - users/*

# Work item auto-linking based on branch name pattern
# AB#12345 in commits auto-links to work item 12345
```

### "Integrated in build" Links

GitHub repos show which build integrated the PR:

```yaml
pr:
  branches:
    include:
    - main
    - develop

# After PR merged, work item shows:
# "Integrated in build: Pipeline Name #123"
# Direct link to build that deployed the change
```

## Stage-Level Variables

```yaml
stages:
- stage: Build
  variables:
    buildConfiguration: 'Release'
    platform: 'x64'
  jobs:
  - job: BuildJob
    steps:
    - script: echo "Building $(buildConfiguration) $(platform)"

- stage: Deploy
  variables:
    environment: 'production'
    region: 'eastus'
  jobs:
  - job: DeployJob
    steps:
    - script: |
        echo "Stage: $(System.StageName)"
        echo "Requested by: $(Build.StageRequestedBy)"
        echo "Deploying to $(environment) in $(region)"
```

## Practical Examples

### Multi-Region Deployment with New Features

```yaml
parameters:
- name: deployToProd
  type: boolean
  default: false

variables:
  # Use iif for conditional values
  targetEnvironment: ${{ iif(parameters.deployToProd, 'production', 'staging') }}

stages:
- stage: Build
  jobs:
  - job: BuildApp
    pool:
      vmImage: 'ubuntu-24.04'  # New image
    steps:
    - script: npm run build

- stage: Test
  dependsOn: Build
  jobs:
  - job: RunTests
    pool:
      vmImage: 'ubuntu-24.04'
    steps:
    - script: npm test

- stage: Deploy_USEast
  dependsOn: Test
  condition: succeeded()
  variables:
    region: 'eastus'
  jobs:
  - deployment: DeployToUSEast
    environment: ${{ variables.targetEnvironment }}
    pool:
      vmImage: 'ubuntu-24.04'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "Deploying to $(region)"
              echo "Requested by: $(Build.StageRequestedBy)"

- stage: Deploy_EUWest
  dependsOn: Test  # Parallel with Deploy_USEast
  condition: succeeded()
  variables:
    region: 'westeurope'
  jobs:
  - deployment: DeployToEUWest
    environment: ${{ variables.targetEnvironment }}
    pool:
      vmImage: 'ubuntu-24.04'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "Deploying to $(region)"
              echo "Requested by: $(Build.StageRequestedBy)"

# Stage dependencies visualized clearly in UI (Sprint 254)
```

## Continuous Access Evaluation (Sprint 260 - August 2025)

### Enhanced Security with CAE

Azure DevOps now supports **Continuous Access Evaluation (CAE)**, enabling near real-time enforcement of Conditional Access policies through Microsoft Entra ID.

**Key Benefits:**
- Instant access revocation on critical events
- No waiting for token expiration
- Enhanced security posture

**Triggers for Access Revocation:**
- User account disabled
- Password reset
- Location or IP address changes
- Risk detection events
- Policy violations

**Example Scenario:**
```yaml
# Your pipeline with CAE enabled automatically
stages:
  - stage: Production
    jobs:
      - deployment: Deploy
        environment: 'production'
        pool:
          vmImage: 'ubuntu-24.04'
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying..."
                  # If user credentials are revoked mid-deployment,
                  # CAE will instantly terminate access
```

**Implementation:**
- General availability: August 2025
- Phased rollout to all customers
- No configuration required (automatic for all Azure DevOps orgs)
- Works with Microsoft Entra ID Conditional Access policies

**Security Improvements:**
- Immediate response to security events
- Reduces attack window from hours/days to seconds
- Complements existing security features (Key Vault, branch policies, etc.)

## OAuth Apps Deprecation (April 2025)

**Important Change:**
- Azure DevOps no longer supports **new registrations** of Azure DevOps OAuth apps (effective April 2025)
- First step towards retiring the Azure DevOps OAuth platform
- Existing OAuth apps continue to work
- Plan migration to Microsoft Entra ID authentication

**Migration Recommendations:**
```yaml
# Use service connections with Microsoft Entra ID instead
- task: AzureCLI@2
  inputs:
    azureSubscription: 'service-connection'  # Uses Managed Identity or Service Principal
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    addSpnToEnvironment: true
    inlineScript: |
      az account show
```

## SNI Requirement (April 2025)

**Network Requirement:**
- **Server Name Indication (SNI)** required on all incoming HTTPS connections
- Effective: April 23, 2025
- Affects all Azure DevOps Services connections

**What to Check:**
- Ensure clients support SNI (most modern clients do)
- Update legacy tools/scripts if needed
- Test connectivity before April 23, 2025

## OAuth Apps Deprecation (Sprint 261 - September 2025)

**Critical Security Change:**

Azure DevOps is enforcing one-time visibility for OAuth client secrets:
- Newly generated client secrets displayed only once at creation
- Get Registration Secret API will be retired
- Change effective: September 2, 2025
- No new OAuth app registrations allowed

**Migration Path:**
```yaml
# Replace OAuth apps with Microsoft Entra ID authentication
# Use service connections with Managed Identity or Service Principal
- task: AzureCLI@2
  inputs:
    azureSubscription: 'entra-id-service-connection'
    scriptType: 'bash'
    addSpnToEnvironment: true
    inlineScript: |
      az account show
      # Authenticated via Entra ID
```

**Action Required:**
- Audit existing OAuth apps
- Plan migration to Entra ID authentication
- Update CI/CD pipelines to use service connections
- Document secret rotation procedures

## Agent Software Version 4 (October 2024 - Current)

**Major Upgrade:**

The Azure Pipelines agent has been upgraded from v3.x to v4.x, powered by .NET 8:

**Key Improvements:**
- Built on .NET 8 for better performance and security
- Extended platform support including ARM64
- Improved reliability and diagnostics
- Better resource management

**Platform Support:**
- **Linux:** Debian 11 & 12, Ubuntu 24.04, 22.04, 20.04 (ARM64 supported)
- **macOS:** Intel and Apple Silicon (ARM64 supported)
- **Windows:** Windows Server 2019, 2022, 2025

**ARM64 Support:**
```yaml
# Self-hosted ARM64 agent
pool:
  name: 'arm64-pool'
  demands:
    - agent.os -equals Linux
    - Agent.OSArchitecture -equals ARM64

steps:
  - script: uname -m
    displayName: 'Verify ARM64 architecture'
```

**Note:** ARM64 support is available for self-hosted agents. Microsoft-hosted ARM64 macOS agents are in preview.

## Sprint 262 - GitHub Copilot Integration (2025)

**AI-Powered Work Item Assistance (Private Preview):**

Connect Azure Boards work items directly with GitHub Copilot:

**Capabilities:**
- Send work items to Copilot coding agent
- AI-assisted bug fixes
- Automated feature implementation
- Test coverage improvements
- Documentation updates
- Technical debt reduction

**Usage Pattern:**
1. Create work item in Azure Boards
2. Add detailed requirements in description
3. Send to GitHub Copilot
4. Copilot generates code changes
5. Review and merge via standard PR process

**Integration with Pipelines:**
```yaml
# Work items auto-link with PRs
trigger:
  branches:
    include:
    - feature/*

# Mention work item in commit
# Example: "Fix login bug AB#12345"
# Automatically links PR to work item and tracks in build
```

## Resources

- [Azure DevOps Sprint 262 Update](https://learn.microsoft.com/azure/devops/release-notes/2025/sprint-262-update)
- [Azure DevOps Sprint 261 Update](https://learn.microsoft.com/azure/devops/release-notes/2025/general/sprint-261-update)
- [Azure DevOps Sprint 260 Update](https://learn.microsoft.com/azure/devops/release-notes/2025/general/sprint-260-update)
- [Azure DevOps Sprint 254 Update](https://devblogs.microsoft.com/devops/)
- [Agent Software Version 4](https://learn.microsoft.com/azure/devops/pipelines/agents/v4-agent)
- [Expression Functions Documentation](https://learn.microsoft.com/azure/devops/pipelines/process/expressions)
- [Hosted Agent Images](https://learn.microsoft.com/azure/devops/pipelines/agents/hosted)
- [Continuous Access Evaluation Documentation](https://learn.microsoft.com/azure/devops/release-notes/)
