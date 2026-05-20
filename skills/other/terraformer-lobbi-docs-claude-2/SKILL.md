---
name: terraformer
description: Terraformer tool for reverse-engineering existing cloud infrastructure into Terraform code. Import resources from AWS, Azure, GCP, Kubernetes, and other providers. Generate Terraform configurations from running infrastructure for migration, disaster recovery, and infrastructure documentation.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - terraform-enterprise
triggers:
  - terraformer
  - reverse engineer
  - import infrastructure
  - terraform import
  - cloud import
  - infrastructure discovery
  - terraform generate
  - import aws
  - import azure
  - import gcp
  - infrastructure migration
---

# Terraformer Skill

Comprehensive Terraformer tool expertise for reverse-engineering existing cloud infrastructure into Terraform code. Transform brownfield infrastructure into infrastructure-as-code with automated resource discovery and code generation.

## When to Use This Skill

Activate this skill when:
- Migrating existing infrastructure to Terraform
- Documenting undocumented infrastructure
- Creating disaster recovery configurations
- Reverse-engineering manually created resources
- Auditing cloud resource configurations
- Generating Terraform code from existing resources
- Consolidating multi-account or multi-region infrastructure
- Creating baseline configurations for new environments
- Importing resources from multiple cloud providers
- Validating infrastructure drift

## What is Terraformer?

Terraformer is a CLI tool that generates Terraform configuration files from existing infrastructure. It uses cloud provider APIs to discover resources and automatically creates:
- Terraform resource blocks (.tf files)
- Terraform state files (.tfstate)
- Variable definitions
- Provider configurations

**Best for:** Brownfield infrastructure, migration projects, infrastructure discovery, documentation generation

## Supported Providers

Terraformer supports 40+ providers including:

### Major Cloud Providers
- **AWS**: 150+ resource types including VPC, EC2, RDS, S3, IAM, Lambda, EKS, etc.
- **Azure**: Resource Groups, VNets, VMs, AKS, Storage, Key Vault, App Services
- **GCP**: Projects, VPC, GCE, GKE, Cloud SQL, IAM, Cloud Functions, Storage
- **Oracle Cloud Infrastructure (OCI)**: Compute, networking, storage, databases

### Container & Orchestration
- **Kubernetes**: Deployments, Services, ConfigMaps, Secrets, Ingress, PVCs
- **OpenShift**: Routes, DeploymentConfigs, BuildConfigs
- **Cloud Foundry**: Apps, services, routes

### Other Providers
- **GitHub**: Repositories, teams, webhooks
- **Datadog**: Monitors, dashboards, users
- **New Relic**: Alerts, dashboards
- **Cloudflare**: DNS, firewall rules
- **Fastly**: Services, backends
- **Heroku**: Apps, addons, pipelines

## Core Capabilities

### Resource Discovery
- Automated scanning of cloud accounts
- Multi-region resource discovery
- Filtered imports by resource type, tag, or name
- Bulk import operations
- Cross-account discovery

### Code Generation
- HCL (Terraform language) file generation
- State file creation
- Variable extraction
- Output definitions
- Provider configurations

### Import Strategies
- **Full account import**: All resources in an account/subscription
- **Selective import**: Specific resource types or services
- **Filtered import**: By tags, names, or patterns
- **Region-specific import**: Single or multi-region
- **Resource dependency mapping**: Maintains relationships

### State Management
- Generates valid Terraform state
- Supports remote state backends
- State file splitting by resource type
- Incremental state updates

## Installation

```bash
# macOS
brew install terraformer

# Linux
curl -LO https://github.com/GoogleCloudPlatform/terraformer/releases/download/$(curl -s https://api.github.com/repos/GoogleCloudPlatform/terraformer/releases/latest | grep tag_name | cut -d '"' -f 4)/terraformer-linux-amd64
chmod +x terraformer-linux-amd64
sudo mv terraformer-linux-amd64 /usr/local/bin/terraformer

# Windows
choco install terraformer

# Verify installation
terraformer version
```

## Basic Usage Pattern

```bash
# Basic import command structure
terraformer import <provider> \
  --resources=<resource_types> \
  --regions=<regions> \
  --filter=<filters> \
  --path-pattern=<output_path> \
  --compact

# Example: Import AWS VPC resources in us-east-1
terraformer import aws \
  --resources=vpc,subnet,security_group \
  --regions=us-east-1 \
  --compact
```

## Common Workflows

### 1. Discover Existing Infrastructure

```bash
# List available resources for a provider
terraformer import aws --resources=* --regions=us-east-1 --dry-run

# AWS: List all resource types
terraformer import aws list

# Azure: List resource types
terraformer import azure list

# GCP: List resource types
terraformer import google list
```

### 2. Selective Resource Import

```bash
# Import specific resource types
terraformer import aws \
  --resources=vpc,subnet,route_table,internet_gateway \
  --regions=us-east-1,us-west-2 \
  --compact

# Import with tag filtering
terraformer import aws \
  --resources=ec2_instance \
  --regions=us-east-1 \
  --filter="Name=tag:Environment;Value=production" \
  --compact

# Import by resource ID
terraformer import aws \
  --resources=s3 \
  --filter="Name=id;Value=my-bucket-name" \
  --compact
```

### 3. Full Account Import

```bash
# Import all resources (careful - can be large!)
terraformer import aws \
  --resources=* \
  --regions=us-east-1 \
  --compact \
  --path-pattern={output}/aws/{region}/{service}

# Azure resource group import
terraformer import azure \
  --resources=* \
  --resource-group=my-resource-group

# GCP project import
terraformer import google \
  --resources=* \
  --projects=my-project-id \
  --regions=us-central1
```

### 4. Multi-Region Import

```bash
# Import from multiple regions
terraformer import aws \
  --resources=vpc,ec2_instance,rds \
  --regions=us-east-1,us-west-2,eu-west-1 \
  --compact \
  --path-pattern={output}/aws/{region}
```

### 5. Kubernetes Import

```bash
# Import Kubernetes resources
terraformer import kubernetes \
  --resources=deployments,services,configmaps,secrets \
  --namespace=production

# Import all namespaced resources
terraformer import kubernetes \
  --resources=* \
  --namespace=default
```

## Output Structure

After running Terraformer, the output directory contains:

```
generated/
└── aws/
    └── us-east-1/
        ├── vpc/
        │   ├── vpc.tf                    # Resource definitions
        │   ├── terraform.tfstate         # Generated state
        │   ├── variables.tf              # Variable definitions
        │   └── outputs.tf                # Output definitions
        ├── ec2_instance/
        │   ├── ec2_instance.tf
        │   ├── terraform.tfstate
        │   └── variables.tf
        └── security_group/
            ├── security_group.tf
            └── terraform.tfstate
```

## Post-Import Workflow

### 1. Review Generated Code

```bash
# Navigate to output directory
cd generated/aws/us-east-1/vpc

# Review generated Terraform
cat vpc.tf

# Check state file
terraform state list
```

### 2. Clean Up and Refactor

```bash
# Common cleanup tasks:
# - Remove unnecessary tags
# - Extract hardcoded values to variables
# - Consolidate repeated patterns into modules
# - Remove default values
# - Organize files by logical grouping
# - Add meaningful resource names
```

### 3. Initialize and Validate

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan to verify no changes
terraform plan
# Expected: No changes. Infrastructure is up-to-date.
```

### 4. Integrate with Existing Projects

```bash
# Option 1: Merge state files
terraform state pull > original.tfstate
# Manually merge or use terraform state mv

# Option 2: Use terraform_remote_state data source
# Reference imported resources from other projects

# Option 3: Import into existing state
terraform import aws_vpc.main vpc-12345678
```

## Advanced Features

### Filtering Strategies

```bash
# By tag
terraformer import aws \
  --resources=ec2_instance \
  --filter="Name=tag:Team;Value=platform"

# By name pattern
terraformer import aws \
  --resources=s3 \
  --filter="Name=id;Value=prod-*"

# Multiple filters
terraformer import aws \
  --resources=rds \
  --filter="Name=tag:Environment;Value=production" \
  --filter="Name=engine;Value=postgres"

# Exclude pattern
terraformer import aws \
  --resources=vpc \
  --excludes="default-vpc-*"
```

### Custom Path Patterns

```bash
# Organize by environment and region
terraformer import aws \
  --resources=* \
  --regions=us-east-1 \
  --path-pattern=generated/{provider}/{region}/{environment}

# Organize by service
terraformer import aws \
  --resources=vpc,subnet,route_table \
  --path-pattern=generated/networking/{service}
```

### Compact Mode

```bash
# Compact mode reduces file size and improves readability
terraformer import aws \
  --resources=vpc \
  --compact  # Removes comments and formatting
```

### Plan File Generation

```bash
# Generate plan file for review
terraformer plan aws \
  --resources=vpc \
  --regions=us-east-1

# Review plan
terraform show plan.out
```

## Integration with Terraform Enterprise

### Migrating to Remote State

```bash
# 1. Import infrastructure locally
terraformer import aws --resources=vpc --regions=us-east-1

# 2. Configure remote backend
cat > backend.tf <<EOF
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "imported/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
EOF

# 3. Initialize with backend
terraform init

# 4. Push state to remote
terraform state push terraform.tfstate
```

### Creating Modules from Imports

```bash
# 1. Import resources
terraformer import aws --resources=vpc,subnet --compact

# 2. Refactor into module structure
mkdir -p modules/vpc
mv generated/aws/us-east-1/vpc/*.tf modules/vpc/

# 3. Create module interface
# Edit modules/vpc/variables.tf, outputs.tf, main.tf

# 4. Use module in root config
cat > main.tf <<EOF
module "vpc" {
  source = "./modules/vpc"

  cidr_block = "10.0.0.0/16"
  name       = "production-vpc"
}
EOF
```

## Best Practices

### Before Import

1. **Audit existing infrastructure**: Document what exists
2. **Plan resource organization**: Decide on module structure
3. **Set up version control**: Initialize git repository
4. **Configure authentication**: Set up cloud provider credentials
5. **Test on non-production first**: Validate process safely

### During Import

1. **Use filters**: Import only what you need
2. **Import incrementally**: Start with core services
3. **Use compact mode**: Improve readability
4. **Organize by service**: Use path patterns
5. **Document decisions**: Add comments explaining why

### After Import

1. **Review all generated code**: Don't blindly trust output
2. **Run terraform plan**: Verify no drift
3. **Refactor immediately**: Clean up before it grows
4. **Extract variables**: Remove hardcoded values
5. **Add validation**: Implement input validation
6. **Create modules**: Consolidate repeated patterns
7. **Document architecture**: Update documentation
8. **Set up CI/CD**: Automate validation and deployment
9. **Enable state locking**: Prevent concurrent modifications
10. **Implement policy checks**: Add Sentinel/OPA policies

## Common Use Cases

### 1. Disaster Recovery Setup

```bash
# Import production infrastructure
terraformer import aws \
  --resources=vpc,subnet,ec2_instance,rds,s3 \
  --regions=us-east-1 \
  --filter="Name=tag:Environment;Value=production"

# Modify for DR region
# - Change region variables
# - Update CIDR blocks if needed
# - Adjust instance sizes for cost

# Deploy to DR region
terraform apply -var="region=us-west-2"
```

### 2. Multi-Account Consolidation

```bash
# Import from Account A
export AWS_PROFILE=account-a
terraformer import aws \
  --resources=* \
  --regions=us-east-1 \
  --path-pattern=generated/account-a/{service}

# Import from Account B
export AWS_PROFILE=account-b
terraformer import aws \
  --resources=* \
  --regions=us-east-1 \
  --path-pattern=generated/account-b/{service}

# Consolidate and standardize
# Create unified modules from both accounts
```

### 3. Infrastructure Documentation

```bash
# Import all infrastructure
terraformer import aws --resources=* --regions=us-east-1

# Generate documentation
terraform-docs markdown . > INFRASTRUCTURE.md

# Create architecture diagrams
terraform graph | dot -Tpng > architecture.png
```

### 4. Migration to Terraform

```bash
# Phase 1: Import existing resources
terraformer import aws --resources=vpc,subnet,route_table

# Phase 2: Validate no drift
terraform plan  # Should show no changes

# Phase 3: Make infrastructure changes via Terraform
# Edit .tf files, run terraform apply

# Phase 4: Decommission manual processes
# Update runbooks, disable console access
```

## Troubleshooting

### Issue: Import Fails with Authentication Error

**Solution**: Verify cloud provider credentials

```bash
# AWS
aws sts get-caller-identity
export AWS_PROFILE=my-profile

# Azure
az account show
az login

# GCP
gcloud auth list
gcloud config set project my-project
```

### Issue: Too Many Resources Generated

**Solution**: Use filters to limit scope

```bash
# Instead of importing all resources
terraformer import aws --resources=* # DON'T DO THIS

# Import specific services
terraformer import aws --resources=vpc,ec2_instance,rds
```

### Issue: Plan Shows Drift After Import

**Solution**: Review for default values and formatting

```bash
# Common causes:
# - Default tags added by provider
# - Computed values not captured
# - Different attribute formatting

# Fix by:
# 1. Adding lifecycle ignore_changes
# 2. Removing default values
# 3. Adjusting attribute formatting
```

### Issue: State File Too Large

**Solution**: Split into smaller state files

```bash
# Import with path pattern
terraformer import aws \
  --resources=* \
  --path-pattern=generated/{service}

# Each service gets its own state file
```

### Issue: Missing Dependencies

**Solution**: Import dependent resources together

```bash
# Import VPC and all related resources
terraformer import aws \
  --resources=vpc,subnet,route_table,internet_gateway,nat_gateway,security_group \
  --regions=us-east-1
```

### Issue: Resource Names Not Meaningful

**Solution**: Refactor after import

```bash
# Before: aws_instance.tfer--i-0123456789abcdef0
# After:  aws_instance.web_server_1

# Use terraform state mv to rename
terraform state mv \
  'aws_instance.tfer--i-0123456789abcdef0' \
  'aws_instance.web_server_1'
```

## Provider-Specific Notes

### AWS
- Requires AWS credentials (env vars, AWS CLI, or IAM role)
- Supports 150+ resource types
- Can import across multiple accounts with profiles
- Best filtering support via tags and resource IDs

### Azure
- Requires Azure CLI authentication
- Organizes by resource groups
- Supports managed identities
- Use `--resource-group` flag for scoped imports

### GCP
- Requires gcloud authentication
- Organizes by projects
- Use `--projects` flag for project selection
- Supports service account authentication

### Kubernetes
- Uses current kubeconfig context
- Can specify namespace with `--namespace`
- Supports multiple clusters via context switching
- Imports CRDs (Custom Resource Definitions)

## Performance Optimization

### Speed Up Large Imports

```bash
# Use parallelism (experimental)
terraformer import aws \
  --resources=ec2_instance \
  --regions=us-east-1,us-west-2 \
  --parallel=4

# Import only recent resources
terraformer import aws \
  --resources=ec2_instance \
  --filter="Name=launch-time;Value=2024-01-01"

# Use compact mode (faster processing)
terraformer import aws \
  --resources=* \
  --compact
```

### Reduce Output Size

```bash
# Use excludes to skip unwanted resources
terraformer import aws \
  --resources=* \
  --excludes="default-*,terraform-*"

# Split by service
terraformer import aws \
  --resources=vpc \
  --path-pattern=generated/{service}
```

## Security Considerations

1. **Credential Management**: Use temporary credentials or IAM roles
2. **State File Security**: State files contain sensitive data
3. **Audit Logging**: Enable CloudTrail/Activity Logs for import operations
4. **Least Privilege**: Use read-only permissions for import
5. **Sensitive Data**: Review for secrets, passwords, API keys
6. **Encryption**: Encrypt state files at rest and in transit
7. **Access Control**: Restrict who can run terraformer

## File References

### Core References
- `references/providers.md` - Provider-specific import patterns and examples
- `references/import-workflow.md` - Step-by-step import process and best practices
- `references/filters.md` - Advanced filtering techniques and patterns
- `references/post-import.md` - Cleanup, refactoring, and optimization guide

### Examples
- `examples/aws-import.sh` - AWS infrastructure import script
- `examples/azure-import.sh` - Azure resource import script
- `examples/gcp-import.sh` - GCP project import script
- `examples/kubernetes-import.sh` - Kubernetes cluster import script
- `examples/multi-cloud-import.sh` - Multi-cloud consolidated import

## Integration Points

### With Other Skills
- **terraform-enterprise**: Use imported code with Terraform workflows
- **iac-architecture**: Design patterns for organizing imported infrastructure
- **vault-operations**: Manage secrets discovered during import

### With Commands
- `/iac:import`: Guided terraformer import workflow
- `/iac:validate`: Validate imported Terraform code
- `/iac:refactor`: Refactor imported code into modules

### With Agents
- **terraform-import-specialist**: Orchestrate complex imports
- **terraform-architect**: Review and optimize imported code
- **infrastructure-auditor**: Analyze imported infrastructure for compliance

## Related Documentation

- [Terraformer GitHub](https://github.com/GoogleCloudPlatform/terraformer)
- [Terraformer Providers](https://github.com/GoogleCloudPlatform/terraformer/tree/master/providers)
- [Terraform Import Documentation](https://www.terraform.io/docs/cli/import/index.html)
- [AWS Resource Coverage](https://github.com/GoogleCloudPlatform/terraformer/blob/master/docs/aws.md)
- [Azure Resource Coverage](https://github.com/GoogleCloudPlatform/terraformer/blob/master/docs/azure.md)
- [GCP Resource Coverage](https://github.com/GoogleCloudPlatform/terraformer/blob/master/docs/gcp.md)
- [Kubernetes Resources](https://github.com/GoogleCloudPlatform/terraformer/blob/master/docs/kubernetes.md)

## Version Compatibility

- Terraformer >= 0.8.24 (latest stable)
- Terraform >= 1.0.0 (required)
- Provider versions: Latest stable recommended
- Cloud provider CLI tools for authentication

## Quick Reference

### Essential Commands

```bash
# List available providers
terraformer --help

# List resources for a provider
terraformer import aws list

# Dry run (preview)
terraformer import aws --resources=vpc --dry-run

# Basic import
terraformer import aws --resources=vpc --regions=us-east-1

# Filtered import
terraformer import aws --resources=vpc --filter="Name=tag:Env;Value=prod"

# Multi-region import
terraformer import aws --resources=vpc --regions=us-east-1,us-west-2

# Import all resources
terraformer import aws --resources=* --regions=us-east-1 --compact
```

### Common Filters

```bash
# By tag
--filter="Name=tag:Environment;Value=production"

# By resource ID
--filter="Name=id;Value=vpc-12345678"

# By name pattern
--filter="Name=name;Value=prod-*"

# Multiple filters (AND logic)
--filter="Name=tag:Team;Value=platform" --filter="Name=tag:Env;Value=prod"
```

### Output Organization

```bash
# By service
--path-pattern=generated/{service}

# By region
--path-pattern=generated/{region}/{service}

# By environment
--path-pattern=generated/{environment}/{service}

# Custom hierarchy
--path-pattern=infrastructure/{provider}/{region}/{environment}/{service}
```
