---
name: defender-for-devops
description: Microsoft Defender for DevOps integration with Azure Pipelines (2025)
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

# Microsoft Defender for DevOps Integration

Complete guide to integrating Microsoft Defender for Cloud security scanning into Azure Pipelines.

## Overview

Microsoft Security DevOps (MSDO) provides comprehensive security scanning capabilities:
- **SAST:** Static Application Security Testing
- **Secret Detection:** Identify hardcoded secrets and credentials
- **Dependency Scanning:** Vulnerable package detection
- **IaC Scanning:** Infrastructure as Code security analysis
- **Container Scanning:** Image vulnerability assessment with Trivy

## Microsoft Security DevOps Extension

**Installation:**
1. Install from Azure DevOps Marketplace
2. Configure in pipeline YAML
3. View results in Scans tab
4. Integrate with Defender for Cloud

**Extension Capabilities:**
- Converts results to SARIF format
- Displays findings in Scans tab
- Integrates multiple security tools
- Provides centralized security insights

## YAML Integration

### Basic MSDO Task

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-24.04'

stages:
  - stage: Build
    jobs:
      - job: BuildAndScan
        steps:
          - task: UseDotNet@2
            displayName: 'Install .NET SDK'
            inputs:
              version: '8.x'

          - task: DotNetCoreCLI@2
            displayName: 'Build Project'
            inputs:
              command: 'build'
              projects: '**/*.csproj'

          # Microsoft Security DevOps Scan
          - task: MicrosoftSecurityDevOps@1
            displayName: 'Run Microsoft Security DevOps'
            inputs:
              categories: 'secrets,code,dependencies,IaC,containers'
              break: false  # Don't fail pipeline on findings

          # Publish SARIF results
          - task: PublishSecurityAnalysisLogs@3
            displayName: 'Publish Security Analysis Logs'
            inputs:
              ArtifactName: 'CodeAnalysisLogs'

          # Display results in Scans tab
          - task: PostAnalysis@2
            displayName: 'Post Analysis'
            inputs:
              break: false
```

### Advanced Configuration with Breaking Builds

```yaml
- task: MicrosoftSecurityDevOps@1
  displayName: 'Security Scanning (Break on Critical)'
  inputs:
    # Scan categories
    categories: 'secrets,code,dependencies,IaC,containers'

    # Break build on severity
    break: true
    breakSeverity: 'critical'  # Options: critical, high, medium, low

    # Tool configuration
    tools: 'all'  # Or specific: 'credscan,eslint,trivy'

    # Output configuration
    publishResults: true

  continueOnError: false
```

### Conditional Scanning

```yaml
# Full scan on main, quick scan on branches
- task: MicrosoftSecurityDevOps@1
  displayName: 'Security Scan'
  inputs:
    categories: ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
      value: 'secrets,code,dependencies,IaC,containers'
    ${{ else }}:
      value: 'secrets,code'
    break: ${{ eq(variables['Build.SourceBranch'], 'refs/heads/main') }}
```

## Integrated Security Tools

### 1. Secret Scanning

**Replaced:** CredScan deprecated September 2023
**Current:** GitHub Advanced Security for Azure DevOps or MSDO secrets scanning

```yaml
# MSDO secrets scanning
- task: MicrosoftSecurityDevOps@1
  inputs:
    categories: 'secrets'
    break: true  # Always break on secrets
```

**Common secrets detected:**
- API keys and tokens
- Database connection strings
- Cloud provider credentials
- SSH private keys
- OAuth tokens

### 2. Static Code Analysis (SAST)

```yaml
- task: MicrosoftSecurityDevOps@1
  displayName: 'SAST Scan'
  inputs:
    categories: 'code'
    tools: 'eslint,bandit,semgrep'
```

**Supported languages:**
- JavaScript/TypeScript (ESLint)
- Python (Bandit)
- Go (gosec)
- Java (SpotBugs)
- C# (.NET Security Guard)

### 3. Dependency Scanning

```yaml
- task: MicrosoftSecurityDevOps@1
  displayName: 'Dependency Scan'
  inputs:
    categories: 'dependencies'
    tools: 'trivy,govulncheck'
```

**Detects:**
- Known CVEs in dependencies
- Outdated packages
- License compliance issues
- Transitive vulnerabilities

### 4. Infrastructure as Code (IaC) Scanning

```yaml
- task: MicrosoftSecurityDevOps@1
  displayName: 'IaC Security Scan'
  inputs:
    categories: 'IaC'
    tools: 'terrascan,checkov,templateanalyzer'
```

**Scans:**
- Terraform configurations
- ARM templates
- Bicep files
- Kubernetes manifests
- CloudFormation templates

### 5. Container Image Scanning

```yaml
- task: MicrosoftSecurityDevOps@1
  displayName: 'Container Security Scan'
  inputs:
    categories: 'containers'
    tools: 'trivy'
```

**Trivy scans for:**
- OS vulnerabilities
- Application dependencies
- Misconfigurations
- Secrets in images
- License issues

## Integration with Defender for Cloud

### Enable Defender for DevOps

```yaml
# Pipeline automatically sends results to Defender for Cloud
# when MSDO extension is connected

- task: MicrosoftSecurityDevOps@1
  displayName: 'Scan and send to Defender'
  inputs:
    categories: 'all'
    publishResults: true

# Results appear in:
# Defender for Cloud → DevOps Security → Findings
```

**Benefits:**
- Centralized security dashboard
- Cross-pipeline insights
- Compliance reporting
- Security trend analysis
- Integration with Azure Security Center

## Complete Security Pipeline Example

```yaml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-24.04'

variables:
  - name: breakOnCritical
    value: ${{ eq(variables['Build.SourceBranch'], 'refs/heads/main') }}

stages:
  - stage: SecurityScan
    displayName: 'Security Analysis'
    jobs:
      - job: StaticAnalysis
        displayName: 'Static Security Analysis'
        steps:
          - checkout: self
            fetchDepth: 1

          # Install dependencies
          - task: NodeTool@0
            inputs:
              versionSpec: '20.x'

          - script: npm ci
            displayName: 'Install dependencies'

          # Build application
          - script: npm run build
            displayName: 'Build application'

          # Docker build for container scanning
          - task: Docker@2
            displayName: 'Build Docker image'
            inputs:
              command: 'build'
              Dockerfile: 'Dockerfile'
              tags: '$(Build.BuildId)'

          # Comprehensive security scan
          - task: MicrosoftSecurityDevOps@1
            displayName: 'Microsoft Security DevOps Scan'
            inputs:
              categories: 'secrets,code,dependencies,IaC,containers'
              break: $(breakOnCritical)
              breakSeverity: 'high'
              tools: 'all'

          # Publish SARIF results
          - task: PublishSecurityAnalysisLogs@3
            displayName: 'Publish SARIF Logs'
            inputs:
              ArtifactName: 'CodeAnalysisLogs'
              ArtifactType: 'Container'

          # Post-analysis with results
          - task: PostAnalysis@2
            displayName: 'Security Post Analysis'
            inputs:
              break: $(breakOnCritical)

          # Generate security report
          - script: |
              echo "Security scan completed"
              echo "Results available in Scans tab"
            displayName: 'Security Summary'
            condition: always()

  - stage: Deploy
    dependsOn: SecurityScan
    condition: succeeded()
    jobs:
      - deployment: DeployApp
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying secure application"
```

## Advanced Security Features (Coming 2025)

**Roadmap features:**
- Pull request build validation
- Break pipeline on alert severity
- Advanced Security dashboard
- Custom CodeQL queries
- Integration with GitHub Advanced Security

## GitHub Advanced Security for Azure DevOps

**Alternative to MSDO for secret scanning:**

```yaml
# Requires GitHub Advanced Security license
# Provides:
# - Secret scanning
# - Code scanning with CodeQL
# - Dependency vulnerability alerts
# - Security overview dashboard

# Configuration in Azure DevOps organization settings
# Scans run automatically on commits and PRs
```

## Best Practices

**Pipeline Security:**
- Run security scans on every commit
- Break builds on critical/high severity findings
- Scan both code and dependencies
- Include IaC security validation
- Scan container images before push
- Review findings regularly

**Configuration:**
```yaml
# Recommended configuration
- task: MicrosoftSecurityDevOps@1
  inputs:
    categories: 'secrets,code,dependencies,IaC,containers'
    break: true
    breakSeverity: 'high'  # Adjust based on risk tolerance
    publishResults: true
```

**Integration:**
- Enable Defender for DevOps in Azure portal
- Configure organization-level policies
- Set up automated notifications
- Create security dashboards
- Establish remediation workflows

## Viewing Results

**In Pipeline:**
1. Navigate to pipeline run
2. Click "Scans" tab
3. Review findings by severity
4. Click findings for details and remediation

**In Defender for Cloud:**
1. Azure Portal → Defender for Cloud
2. DevOps Security
3. View findings across all pipelines
4. Filter by severity, project, repository
5. Track remediation progress

## Troubleshooting

**Common Issues:**

**MSDO task fails:**
```yaml
# Enable verbose logging
- task: MicrosoftSecurityDevOps@1
  env:
    MSDO_VERBOSE: true
  inputs:
    categories: 'all'
```

**False positives:**
```yaml
# Suppress findings with .gdnconfig file
# In repository root:
{
  "tools": {
    "trivy": {
      "enabled": true,
      "severities": ["CRITICAL", "HIGH"]
    }
  }
}
```

**Performance:**
- Cache tool downloads
- Limit scan categories on branches
- Use parallel stages for large repos

## Resources

- [Microsoft Security DevOps Extension](https://learn.microsoft.com/azure/defender-for-cloud/azure-devops-extension)
- [Defender for DevOps Documentation](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-devops-introduction)
- [SARIF Format Specification](https://sarifweb.azurewebsites.net/)
- [Security Tools Integration](https://learn.microsoft.com/azure/defender-for-cloud/azure-devops-extension)
