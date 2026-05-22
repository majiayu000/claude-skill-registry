---
name: terragrunt
description: >-
  You are an expert in Terragrunt, the thin wrapper for Terraform and
  OpenTofu that provides extra tools for keeping configurations DRY, managing
  remote state, and orchestrating multi-module deployments. You help platform
  teams manage large-scale infrastructure across multiple environments and AWS
  accounts using Terragrunt's hierarchical configuration, dependency
  management, and before/after hooks.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Infrastructure & DevOps
  tags:
    - iac
    - terraform
    - dry
    - infrastructure
    - multi-environment
    - orchestration
---

# Terragrunt — DRY Terraform/OpenTofu Wrapper

You are an expert in Terragrunt, the thin wrapper for Terraform and OpenTofu that provides extra tools for keeping configurations DRY, managing remote state, and orchestrating multi-module deployments. You help platform teams manage large-scale infrastructure across multiple environments and AWS accounts using Terragrunt's hierarchical configuration, dependency management, and before/after hooks.

## Core Capabilities

### DRY Configuration

```hcl
# infrastructure/terragrunt.hcl — Root config (inherited by all children)
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config = {
    bucket         = "company-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite"
  contents  = <<EOF
provider "aws" {
  region = "${local.region}"
  default_tags {
    tags = {
      Environment = "${local.environment}"
      ManagedBy   = "terragrunt"
    }
  }
}
EOF
}

locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  env_vars     = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  account_id   = local.account_vars.locals.account_id
  region       = local.region_vars.locals.region
  environment  = local.env_vars.locals.environment
}
```

```markdown
## Directory Structure

infrastructure/
├── terragrunt.hcl                        # Root config (shared settings)
├── modules/                              # Reusable Terraform modules
│   ├── vpc/
│   ├── ecs-service/
│   └── rds/
├── production/
│   ├── account.hcl                       # account_id = "111111111111"
│   ├── us-east-1/
│   │   ├── region.hcl                    # region = "us-east-1"
│   │   ├── env.hcl                       # environment = "production"
│   │   ├── vpc/
│   │   │   └── terragrunt.hcl
│   │   ├── api/
│   │   │   └── terragrunt.hcl
│   │   └── database/
│   │       └── terragrunt.hcl
└── staging/
    ├── account.hcl                       # account_id = "222222222222"
    └── us-east-1/
        ├── region.hcl
        ├── env.hcl                       # environment = "staging"
        ├── vpc/
        ├── api/
        └── database/
```

```hcl
# infrastructure/production/us-east-1/api/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules/ecs-service"
}

dependency "vpc" {
  config_path = "../vpc"
}

dependency "database" {
  config_path = "../database"
}

inputs = {
  service_name    = "api"
  vpc_id          = dependency.vpc.outputs.vpc_id
  subnet_ids      = dependency.vpc.outputs.private_subnet_ids
  database_url    = dependency.database.outputs.connection_string
  desired_count   = 3                     # Production: 3 instances
  cpu             = 512
  memory          = 1024
  container_image = "company/api:latest"
}
```

### Commands

```bash
# Run in a single module
cd infrastructure/production/us-east-1/api
terragrunt plan
terragrunt apply

# Run across ALL modules (respects dependencies)
cd infrastructure/production/us-east-1
terragrunt run-all plan
terragrunt run-all apply

# Run only modules that changed
terragrunt run-all apply --terragrunt-include-dir api --terragrunt-include-dir database

# Graph dependencies
terragrunt graph-dependencies | dot -Tpng > deps.png
```

## Installation

```bash
brew install terragrunt
# Or download from https://terragrunt.gruntwork.io/
# Works with both Terraform and OpenTofu
```

## Best Practices

1. **Hierarchical configs** — Use `find_in_parent_folders()` to inherit settings; override only what changes per environment
2. **Dependencies** — Declare `dependency` blocks; Terragrunt applies in the right order and passes outputs as inputs
3. **Remote state per module** — Use `path_relative_to_include()` for unique state keys; never share state between modules
4. **run-all for orchestration** — `terragrunt run-all apply` deploys entire environments respecting dependency order
5. **Separate modules from live config** — Reusable modules in `modules/`; environment configs reference them via `source`
6. **Account/region hierarchy** — Structure folders by account → region → environment → service; each level has its `.hcl`
7. **Before/after hooks** — Use hooks for validation, linting (`tflint`), or notifications before/after apply
8. **Works with OpenTofu** — Set `TERRAGRUNT_TFPATH=tofu` to use OpenTofu instead of Terraform
