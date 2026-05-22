---
name: opentofu-neon-explorer
description: Explore and manage Neon Postgres serverless database resources using OpenTofu/Terraform
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: database-management
---

# OpenTofu Neon Explorer

## What I do

I guide you through managing Neon serverless Postgres database resources using the Neon Terraform provider. I help you:

- **Project Management**: Create and manage Neon Postgres projects
- **Database Operations**: Create databases, branches, and endpoints
- **Branching Strategy**: Implement Neon's branch-based database workflow
- **Connection Management**: Configure database connections and credentials
- **Best Practices**: Follow Neon provider documentation patterns

## When to use me

Use this skill when you need to:
- Automate Neon Postgres infrastructure as code
- Create serverless Postgres databases for applications
- Implement database branching for development workflows
- Manage database projects, branches, and endpoints programmatically
- Configure Neon databases for production workloads
- Implement Neon's unique branch-based development workflow

**Note**: OpenTofu and Terraform are used interchangeably throughout this skill. OpenTofu is an open-source implementation of Terraform and maintains full compatibility with Terraform providers.

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **Neon Account**: Valid Neon account with API access
- **Neon API Key**: API key for authentication
- **Basic Postgres Knowledge**: Understanding of Postgres and database concepts
- **Neon CLI (Optional)**: For additional operations

## Provider Documentation

- **Terraform Registry (Neon Provider)**: https://registry.terraform.io/providers/kislerdm/neon/latest/docs
- **Provider Source**: https://github.com/kislerdm/terraform-provider-neon
- **Latest Provider Version**: kislerdm/neon ~> 0.13.0
- **Neon Documentation**: https://neon.tech/docs/
- **Terraform Version**: >= 1.14.x

## Steps

### Step 1: Install and Configure OpenTofu

```bash
# Verify OpenTofu installation
tofu version

# Initialize project
mkdir neon-terraform
cd neon-terraform
tofu init
```

### Step 2: Configure Neon Provider

Create `versions.tf`:

```hcl
terraform {
  required_providers {
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.13.0"
    }
  }
  required_version = ">= 1.14"

  # Remote state backend
  backend "s3" {
    bucket = "neon-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Step 3: Configure Neon Provider

Create `provider.tf`:

```hcl
provider "neon" {
  # Method 1: API Key in provider configuration (not recommended for production)
  api_key = var.neon_api_key

  # Method 2: Environment variable (recommended)
  # Set environment variable: NEON_API_KEY
  # Reference: https://neon.tech/docs/reference/terraform#important-usage-notes
}
```

### Step 4: Configure Environment Variables

```bash
# Set Neon API key (recommended)
export NEON_API_KEY="your-neon-api-key"

# Or use variable file
cat > terraform.tfvars <<EOF
neon_api_key = "your-neon-api-key"
project_name = "my-app"
db_name = "appdb"
EOF

# IMPORTANT: When updating provider version, avoid `tofu init -upgrade` in CI pipelines
# Use `tofu init` in automated workflows instead
# Reference: https://neon.tech/docs/reference/terraform#important-usage-notes
```

### Step 5: Create Neon Project

Create `project.tf`:

```hcl
resource "neon_project" "main" {
  name = var.project_name

  # Project configuration
  # Neon automatically selects the best region
  # You cannot specify region during project creation

  tags = {
    Environment = var.environment
    ManagedBy  = "Terraform"
  }

  # Project-level settings
  # Neon automatically configures:
  # - Autoscaling storage
  # - Serverless compute
  # - High availability (based on plan)
}
```

### Step 6: Create Database Branch

Create `branch.tf`:

```hcl
# Main branch (created by default with project)
# Access via data source

# Development branch
resource "neon_branch" "dev" {
  project_id = neon_project.main.id
  name       = "dev"
  parent_id  = neon_branch.primary.id

  # Branch inherits parent database schema
  # Useful for feature development and testing
}

# Feature branch
resource "neon_branch" "feature" {
  project_id = neon_project.main.id
  name       = "feature-authentication"

  # If parent_id not specified, branches from primary
  # Ideal for isolated feature development
}
```

### Step 7: Create Databases

Create `database.tf`:

```hcl
# Primary database
resource "neon_database" "primary" {
  project_id = neon_project.main.id
  branch_id  = neon_branch.primary.id
  name       = var.db_name

  # Database collation
  collation = "en_US.UTF-8"
}

# Development database
resource "neon_database" "dev" {
  project_id = neon_project.main.id
  branch_id  = neon_branch.dev.id
  name       = "appdb"
}

# Testing database
resource "neon_database" "test" {
  project_id = neon_project.main.id
  branch_id  = neon_branch.feature.id
  name       = "testdb"
}
```

### Step 8: Create Database Endpoints

Create `endpoint.tf`:

```hcl
# Primary read-write endpoint
resource "neon_endpoint" "primary" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.primary.id
  name         = "primary"
  endpoint_type = "read_write"

  # Endpoint configuration
  # Automatically managed by Neon
  # Autoscaling based on workload
}

# Read-only endpoint (for analytics/reporting)
resource "neon_endpoint" "read_only" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.primary.id
  name         = "readonly"
  endpoint_type = "read_only"
}

# Development endpoint
resource "neon_endpoint" "dev" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.dev.id
  name         = "dev-endpoint"
  endpoint_type = "read_write"
}
```

### Step 9: Create Database Roles/Users

Create `role.tf`:

```hcl
# Application role
resource "neon_role" "app_user" {
  project_id = neon_project.main.id
  name       = "app_user"

  # Role permissions
  # Default: Can connect to databases
}

# Read-only role
resource "neon_role" "analytics_user" {
  project_id = neon_project.main.id
  name       = "analytics_user"
}

# Admin role (use carefully)
resource "neon_role" "admin" {
  project_id = neon_project.main.id
  name       = "admin_user"
}
```

### Step 10: Grant Database Access

Create `grants.tf`:

```hcl
# Grant access to primary database
resource "neon_grant" "app_user_primary" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.primary.id
  database_id  = neon_database.primary.id
  role_name    = neon_role.app_user.name

  # Grant permissions
  # Default: CONNECT privilege
}

# Grant read-only access
resource "neon_grant" "analytics_user_primary" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.primary.id
  database_id  = neon_database.primary.id
  role_name    = neon_role.analytics_user.name
}

# Grant access to development database
resource "neon_grant" "app_user_dev" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.dev.id
  database_id  = neon_database.dev.id
  role_name    = neon_role.app_user.name
}
```

### Step 11: Configure Database Operations

Create `operations.tf`:

```hcl
# Suspend endpoint (pause compute)
resource "neon_endpoint" "primary_suspended" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.primary.id
  name         = "primary-suspended"
  endpoint_type = "read_write"

  suspend = true
}

# Delete branch when no longer needed
resource "neon_branch" "temporary" {
  project_id = neon_project.main.id
  name       = "temp-feature"
  lifecycle {
    ignore_changes = [suspend]  # Manage suspension manually if needed
  }
}

# Note: Use tofu destroy to remove resources
# Or use terraform state rm to remove from state without destroying
```

### Step 12: Data Sources for Existing Resources

Create `data_sources.tf`:

```hcl
# Get existing project
data "neon_project" "existing" {
  name = "existing-project-name"
}

# Get existing branch
data "neon_branch" "primary" {
  project_id = data.neon_project.existing.id
  name       = "primary"
}

# Get connection details
output "connection_string" {
  value = data.neon_branch.primary.connection_uri
  sensitive = true
}
```

### Step 13: Define Variables

Create `variables.tf`:

```hcl
variable "neon_api_key" {
  description = "Neon API key"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Name of the Neon project"
  type        = string
}

variable "db_name" {
  description = "Name of the primary database"
  type        = string
  default     = "appdb"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Step 14: Create Outputs

Create `outputs.tf`:

```hcl
output "project_id" {
  description = "Neon project ID"
  value       = neon_project.main.id
}

output "project_name" {
  description = "Neon project name"
  value       = neon_project.main.name
}

output "primary_branch_id" {
  description = "Primary branch ID"
  value       = neon_branch.primary.id
}

output "primary_database_id" {
  description = "Primary database ID"
  value       = neon_database.primary.id
}

output "connection_string" {
  description = "Primary database connection string"
  value       = neon_branch.primary.connection_uri
  sensitive   = true
}

output "host" {
  description = "Database host"
  value       = neon_branch.primary.host
}

output "port" {
  description = "Database port"
  value       = neon_branch.primary.port
}

output "user" {
  description = "Database user"
  value       = neon_branch.primary.user
}

output "password" {
  description = "Database password"
  value       = neon_branch.primary.password
  sensitive   = true
}
```

### Step 15: Initialize and Apply

```bash
# Set API key
export NEON_API_KEY="your-neon-api-key"

# Initialize providers
tofu init

# Plan changes
tofu plan -out=tfplan

# Apply changes
tofu apply tfplan

# Show outputs (connection details)
tofu output
```

## Best Practices

### Security

1. **Use Environment Variables**: Store API keys in environment variables, not in code
2. **Least Privilege**: Create separate roles for different use cases (app, analytics, admin)
3. **Secure Connections**: Use SSL/TLS for all database connections
4. **Secret Management**: Use secret managers for production credentials
5. **API Key Rotation**: Regularly rotate Neon API keys

### Branching Strategy

1. **Use Branches**: Leverage Neon's branching for development and testing
2. **Isolate Features**: Create feature branches for isolated development
3. **Production Primary**: Keep primary branch for production workloads
4. **Merge and Delete**: Delete feature branches after merging to primary
5. **Branch Reset**: Reset development branches from primary regularly

### Cost Optimization

1. **Suspend Endpoints**: Suspend compute when not in use
2. **Use Read-Only Endpoints**: For analytics and reporting workloads
3. **Monitor Usage**: Track storage and compute usage in Neon console
4. **Delete Unused Resources**: Remove unused branches and databases
5. **Autoscaling**: Leverage Neon's autoscaling for variable workloads

### Connection Management

1. **Connection Pooling**: Use connection pooling for high-traffic applications
2. **Read Replicas**: Use read-only endpoints for analytics workloads
3. **SSL Required**: Always use SSL/TLS for production connections
4. **Timeout Configuration**: Configure appropriate connection timeouts
5. **Retry Logic**: Implement retry logic for transient failures

### Development Workflow

1. **Feature Branches**: Create branches for each feature or bug fix
2. **Testing**: Test in development branches before merging
3. **Staging**: Use staging branch for pre-production testing
4. **Continuous Integration**: Integrate with CI/CD pipelines
5. **Rollback**: Use branch reset for quick rollbacks

## Common Issues

### Issue: Provider Authentication Failed

**Symptom**: Error `Error: Error configuring provider: authentication failed`

**Solution**:
```bash
# Verify API key
echo $NEON_API_KEY

# Test API key manually
curl -H "Authorization: Bearer $NEON_API_KEY" \
  https://console.neon.tech/api/v1/projects

# Ensure environment variable is set correctly
export NEON_API_KEY="your-api-key"
```

### Issue: Project Already Exists

**Symptom**: Error `Error: Project with name already exists`

**Solution**:
```bash
# Use data source to reference existing project
data "neon_project" "existing" {
  name = "existing-project-name"
}

# Or import existing project into state
tofu import neon_project.main project-id
```

### Issue: Branch Creation Failed

**Symptom**: Error `Error: Failed to create branch`

**Solution**:
```bash
# Check parent branch exists
tofu state list | grep neon_branch

# Ensure project is active
# Check Neon console for project status

# Use data source to verify parent branch
data "neon_branch" "primary" {
  project_id = neon_project.main.id
  name       = "primary"
}
```

### Issue: Endpoint Connection Failed

**Symptom**: Cannot connect to database endpoint

**Solution**:
```bash
# Check endpoint status
tofu output connection_string

# Verify endpoint is not suspended
# Check suspend parameter in resource

# Test connection using psql
psql $CONNECTION_STRING

# Check firewall settings
# Ensure your IP is allowed if using IP restrictions
```

### Issue: Provider Version Conflict

**Symptom**: Error `Error: Provider version constraint`

**Solution**:
```bash
# IMPORTANT: Avoid `tofu init -upgrade` in CI pipelines
# This can lead to unintended resource replacements and data loss

# Use `tofu init` in automated workflows
tofu init

# Run `tofu init -upgrade` manually and review plans
tofu init -upgrade
tofu plan -out=tfplan
# Review plan carefully before applying

# Reference: https://neon.tech/docs/reference/terraform#important-usage-notes
```

### Issue: State Lock Error

**Symptom**: Error `Error: Error acquiring the state lock`

**Solution**:
```bash
# Check who has the lock
tofu state pull

# Force unlock (caution!)
tofu force-unlock <LOCK_ID>

# Ensure only one person is applying changes at a time
```

### Issue: Role Grant Failed

**Symptom**: Error `Error: Failed to grant database access`

**Solution**:
```hcl
# Ensure role exists before granting
resource "neon_role" "app_user" {
  project_id = neon_project.main.id
  name       = "app_user"
}

# Grant access after role creation
resource "neon_grant" "app_user_primary" {
  project_id   = neon_project.main.id
  branch_id    = neon_branch.primary.id
  database_id  = neon_database.primary.id
  role_name    = neon_role.app_user.name

  depends_on = [neon_role.app_user]
}
```

## Reference Documentation

- **Terraform Registry (Neon Provider)**: https://registry.terraform.io/providers/kislerdm/neon/latest/docs
- **Provider GitHub**: https://github.com/kislerdm/terraform-provider-neon
- **Neon Documentation**: https://neon.tech/docs/
- **Neon Terraform Guide**: https://neon.tech/docs/reference/terraform
- **Important Usage Notes**: https://neon.tech/docs/reference/terraform#important-usage-notes
- **OpenTofu Documentation**: https://opentofu.org/docs/

## Examples

### Complete Neon Project Setup

```hcl
# versions.tf
terraform {
  required_providers {
    neon = {
      source  = "kislerdm/neon"
      version = "~> 0.13.0"
    }
  }
}

# provider.tf
provider "neon" {
  # API key from environment variable: NEON_API_KEY
}

# project.tf
resource "neon_project" "main" {
  name = "my-app-production"
}

# branch.tf
resource "neon_branch" "dev" {
  project_id = neon_project.main.id
  name       = "dev"
  parent_id  = data.neon_branch.primary.id
}

# database.tf
resource "neon_database" "primary" {
  project_id = neon_project.main.id
  branch_id  = data.neon_branch.primary.id
  name       = "appdb"
}

# endpoint.tf
resource "neon_endpoint" "primary" {
  project_id   = neon_project.main.id
  branch_id    = data.neon_branch.primary.id
  name         = "primary"
  endpoint_type = "read_write"
}

# data_sources.tf
data "neon_branch" "primary" {
  project_id = neon_project.main.id
  name       = "primary"
}
```

### Multi-Environment Setup

```hcl
# Development project
resource "neon_project" "dev" {
  name = "my-app-dev"
}

resource "neon_branch" "dev" {
  project_id = neon_project.dev.id
  name       = "dev"
}

# Staging project
resource "neon_project" "staging" {
  name = "my-app-staging"
}

# Production project
resource "neon_project" "prod" {
  name = "my-app-prod"
}

resource "neon_endpoint" "prod_readonly" {
  project_id   = neon_project.prod.id
  branch_id    = data.neon_branch.primary.id
  name         = "readonly"
  endpoint_type = "read_only"
}
```

### Application User Setup

```hcl
resource "neon_role" "app_user" {
  project_id = neon_project.main.id
  name       = "app_user"
}

resource "neon_database" "app" {
  project_id = neon_project.main.id
  branch_id  = data.neon_branch.primary.id
  name       = "appdb"
}

resource "neon_grant" "app_access" {
  project_id   = neon_project.main.id
  branch_id    = data.neon_branch.primary.id
  database_id  = neon_database.app.id
  role_name    = neon_role.app_user.name
}
```

### Connection String Usage

```bash
# Get connection string from Terraform output
export DATABASE_URL=$(tofu output -raw connection_string)

# Use in application
# Node.js example
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

# Python example
import psycopg2
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
```

## Tips and Tricks

- **Use Environment Variables**: Always use NEON_API_KEY environment variable
- **Branch Reset**: Reset development branches from primary regularly
- **Read-Only Endpoints**: Use for analytics to reduce load on primary
- **Suspend Unused**: Suspend endpoints when not in use to save costs
- **Monitor Usage**: Check Neon console for storage and compute usage
- **Avoid init -upgrade in CI**: Use `tofu init` instead of `tofu init -upgrade`
- **Import Existing**: Import existing Neon resources into Terraform state
- **Data Sources**: Use data sources to reference existing projects and branches
- **Connection Strings**: Treat connection strings as sensitive values

## Next Steps

After mastering Neon provider, explore:
- **Neon CLI**: https://neon.tech/docs/reference/cli
- **Neon Branching**: https://neon.tech/docs/introduction/branching
- **Neon API**: https://neon.tech/api-reference
- **PostgreSQL**: Learn more about PostgreSQL features and best practices
- **Integration**: Connect Neon to your application framework (Node.js, Python, Go, etc.)
