---
name: ado-pipeline-best-practices
description: Azure DevOps pipeline best practices, patterns, and industry standards
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

# Azure Pipelines Best Practices

Comprehensive best practices for creating and maintaining Azure DevOps YAML pipelines.

## Pipeline Structure

**Multi-Stage Pipelines:**
```yaml
# Recommended structure
stages:
  - stage: Build
  - stage: Test
  - stage: DeployDev
  - stage: DeployStaging  
  - stage: DeployProduction
```

**Benefits:**
- Clear separation of concerns
- Conditional stage execution
- Environment-specific configurations
- Approval gates between stages

## Triggers and Scheduling

**Best practices:**
- Use path filters to avoid unnecessary builds
- Enable batch builds for high-frequency repos
- Use PR triggers for validation
- Schedule nightly/weekly builds for comprehensive testing

```yaml
trigger:
  batch: true
  branches:
    include: [main, develop]
  paths:
    exclude: ['docs/*', '**.md']

pr:
  autoCancel: true
  branches:
    include: [main]

schedules:
  - cron: '0 0 * * *'
    displayName: 'Nightly build'
    branches:
      include: [main]
    always: false  # Only if code changed
```

## Variable Management

**Hierarchy:**
1. Pipeline-level variables (az devops YAML)
2. Variable groups (shared across pipelines)
3. Azure Key Vault (secrets)
4. Runtime parameters (user input)

**Security:**
- Never hardcode secrets
- Use Key Vault for sensitive data
- Mark secrets in variable groups
- Secrets are automatically masked in logs

## Caching

Implement caching for:
- Package dependencies (npm, pip, NuGet, Maven)
- Docker layers
- Build outputs

**Impact:**
- Faster builds (up to 90% reduction)
- Reduced network usage
- Lower costs

## Templates

**Use templates for:**
- Reusable build patterns
- Standardized deployment steps
- Consistent security scanning
- Company-wide best practices

**Benefits:**
- DRY (Don't Repeat Yourself)
- Centralized updates
- Consistent processes

## Security Practices

**Essential:**
- Code scanning (SAST, dependency)
- Container image scanning
- Secret scanning
- Compliance checks
- Branch protection policies
- Required approvals

## Performance

**Optimize:**
- Parallelize independent jobs
- Use caching extensively
- Shallow git clones (fetchDepth: 1)
- Appropriate agent pools
- Clean up artifacts

## Monitoring

**Track:**
- Build success rates
- Build durations
- Test pass rates
- Deployment frequency
- Mean time to recovery (MTTR)

Always verify best practices against latest Azure DevOps documentation.
