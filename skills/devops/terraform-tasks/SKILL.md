---
name: terraform-tasks
description: Specialized Terraform task execution skill for autonomous infrastructure operations. Handles code generation, debugging, version management (1.10-1.14+), security scanning, and architecture design across all providers (AWS 6.0, AzureRM 4.x, GCP) and platforms. Covers ephemeral values, Terraform Stacks, policy-as-code, and 2025 best practices.
---

<!--
Progressive Disclosure References:
- references/aws-provider-6.md - AWS Provider 6.0 breaking changes and migration
- references/azurerm-4.md - AzureRM 4.x features and migration
- references/ephemeral-values.md - Terraform 1.10+ ephemeral values for secrets
- references/terraform-stacks.md - Terraform Stacks (GA 2025) reference
-->

# Terraform Tasks Skill

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

This skill enables autonomous execution of complex Terraform tasks with comprehensive provider knowledge and platform awareness.

## Capabilities

### 1. Infrastructure Code Generation

Generate complete, production-ready Terraform code for any cloud provider:

**Process**:
1. Determine provider and version from user context
2. Research latest provider documentation if needed
3. Generate complete configurations with:
   - Provider version constraints
   - Resource configurations
   - Variables with validation
   - Outputs
   - Security best practices
   - Platform-specific considerations

**Example Tasks**:
- "Create Azure Storage Account with private endpoints and customer-managed keys"
- "Generate AWS VPC with 3-tier architecture and NAT gateways"
- "Build GCP GKE cluster with Workload Identity and node pools"

### 2. Version Management

Handle Terraform and provider version upgrades:

**Process**:
1. Check current versions
2. Research changelogs and breaking changes
3. Propose upgrade path
4. Generate migration code
5. Provide testing strategy

**Example Tasks**:
- "Upgrade from AzureRM provider 2.x to 3.x"
- "Migrate Terraform 0.12 code to 1.x"
- "Update all providers to latest compatible versions"

### 3. Debugging and Troubleshooting

Diagnose and fix Terraform issues:

**Process**:
1. Gather diagnostic information
2. Analyze error messages and logs
3. Identify root cause
4. Provide platform-specific solution
5. Suggest preventive measures

**Example Tasks**:
- "Debug state lock timeout on Windows"
- "Fix provider authentication failure in Azure DevOps pipeline"
- "Resolve circular dependency in module structure"

### 4. Security Scanning and Remediation

Scan and fix security issues:

**Process**:
1. Run security scanners (tfsec, Checkov)
2. Analyze findings
3. Prioritize issues
4. Generate fixes
5. Explain security implications

**Example Tasks**:
- "Run tfsec and fix all HIGH severity issues"
- "Ensure all S3 buckets have encryption enabled"
- "Implement Azure storage account with all security best practices"

### 5. Architecture Review

Review and improve Terraform architecture:

**Process**:
1. Analyze current structure
2. Identify anti-patterns
3. Propose improvements
4. Generate refactoring plan
5. Document decisions (ADRs)

**Example Tasks**:
- "Review state management strategy for 500+ resources"
- "Design multi-region architecture for high availability"
- "Refactor monolithic state into layered approach"

### 6. CI/CD Pipeline Generation

Create complete CI/CD pipelines:

**Process**:
1. Determine CI/CD platform
2. Understand environment strategy
3. Generate pipeline configuration
4. Include security scanning
5. Add approval gates
6. Implement drift detection

**Example Tasks**:
- "Create Azure DevOps pipeline with multi-stage deployment"
- "Generate GitHub Actions workflow with OIDC authentication"
- "Build GitLab CI pipeline with Terraform Cloud backend"

### 7. Module Development

Create reusable Terraform modules:

**Process**:
1. Design module interface
2. Implement with best practices
3. Add variable validation
4. Generate documentation
5. Create examples
6. Set up testing

**Example Tasks**:
- "Create Azure networking module with hub-spoke pattern"
- "Build AWS ECS module with auto-scaling and ALB"
- "Develop GCP Cloud Run module with custom domains"

### 8. Migration Tasks

Migrate infrastructure to Terraform:

**Process**:
1. Inventory existing resources
2. Generate import commands
3. Create matching Terraform code
4. Validate configurations
5. Test import process
6. Plan cutover strategy

**Example Tasks**:
- "Import existing Azure resources into Terraform"
- "Migrate from CloudFormation to Terraform"
- "Convert ARM templates to Terraform HCL"

## Autonomous Behavior

This skill operates autonomously with minimal user intervention:

### Information Gathering
- Automatically detect Terraform and provider versions
- Identify platform (Windows/Linux/macOS)
- Detect CI/CD environment
- Check for existing configurations

### Research
- Use WebSearch to find current documentation
- Check provider changelogs for breaking changes
- Research best practices
- Find platform-specific solutions

### Code Generation
- Generate complete, working code
- Include all necessary files (main.tf, variables.tf, outputs.tf, etc.)
- Add comprehensive comments
- Follow naming conventions
- Apply security best practices

### Validation
- Run terraform fmt on generated code
- Validate syntax
- Check for security issues
- Test configurations when possible

### Documentation
- Explain architectural decisions
- Document usage examples
- Note version compatibility
- Include troubleshooting tips

## Error Handling

When encountering issues:

1. **Gather Context**: Collect all relevant information
2. **Research**: Look up error messages and solutions
3. **Platform Awareness**: Consider OS-specific issues
4. **Multiple Solutions**: Provide alternatives when available
5. **Prevention**: Suggest how to avoid similar issues

## Platform-Specific Considerations

### Windows
- PowerShell syntax for commands
- Path handling (backslashes)
- Line ending considerations
- Execution policy issues
- Credential management

### Linux/macOS
- Bash syntax for commands
- File permissions
- Package managers
- Environment variables

### CI/CD Environments
- Pipeline-specific syntax
- Agent capabilities
- Authentication methods
- Artifact handling

## Quality Standards

All generated Terraform code must:
- Be properly formatted (terraform fmt)
- Pass validation (terraform validate)
- Include security best practices
- Have comprehensive variable validation
- Include meaningful descriptions
- Follow naming conventions
- Be version-compatible
- Include usage examples
- Have proper output definitions

## Provider Expertise

### Azure (AzureRM)
- All resource types
- AzAPI for preview features
- Service endpoints and private endpoints
- Managed identities
- RBAC and policies

### AWS
- All services
- IAM roles and policies
- VPC networking
- S3 backend configuration
- Cross-account deployments

### Google Cloud
- All GCP services
- IAM and service accounts
- VPC and networking
- GCS backend configuration
- Organization and folder policies

### Community Providers
- Kubernetes and Helm
- Datadog, PagerDuty
- GitHub, GitLab
- HashiCorp Vault
- And more...

## Examples

### Example 1: Generate Azure Storage Account

**User Request**: "Create an Azure Storage Account with all security best practices"

**Skill Actions**:
1. Detect/ask for AzureRM provider version
2. Research latest security requirements
3. Generate complete configuration:
   - Storage account with secure settings
   - Private endpoint
   - Diagnostic settings
   - Customer-managed encryption keys
   - Network rules
   - Variables with validation
   - Outputs
4. Include usage examples
5. Add security scanner ignore comments where appropriate with explanations

### Example 2: Debug Plan Failure

**User Request**: "My terraform plan is failing with authentication error on Windows"

**Skill Actions**:
1. Ask for error details
2. Identify it's Azure CLI authentication
3. Provide Windows-specific solution:
   - PowerShell commands to check authentication
   - How to refresh credentials
   - Environment variable configuration
   - Alternative authentication methods
4. Explain root cause
5. Suggest prevention

### Example 3: Architecture Review

**User Request**: "Review my Terraform structure, I have 1000+ resources in one state file"

**Skill Actions**:
1. Analyze current structure
2. Identify issues:
   - Large state file
   - Slow operations
   - Large blast radius
3. Propose layered architecture:
   - Split into foundation/platform/apps
   - Separate state files
   - Remote state data sources
4. Generate migration plan
5. Create ADR documenting decision
6. Provide implementation steps

## Integration with terraform-expert Agent

This skill works in tandem with the terraform-expert agent:
- Agent provides strategic guidance
- Skill executes tactical tasks
- Agent validates skill outputs
- Skill reports back to agent

Use this skill when you need to autonomously execute Terraform tasks with comprehensive provider knowledge and platform awareness.
