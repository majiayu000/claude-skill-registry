---
name: infra-iac-terraform
description: Infrastructure as Code with HashiCorp Terraform
---

# Terraform Patterns

> **Quick Guide:** Declarative infrastructure using HCL. Pin provider versions in `required_providers` and commit `.terraform.lock.hcl`. Use remote backends with state locking for team collaboration. Prefer `for_each` over `count` for non-identical resources. Use `moved` blocks for refactoring, `import` blocks for adopting existing infrastructure. Validate inputs with `validation` blocks and infrastructure with `precondition`/`postcondition`. Keep modules flat, composable, and single-purpose. Run `terraform fmt` and `terraform validate` before every commit.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md**

**(You MUST pin provider versions with constraints in `required_providers` and commit `.terraform.lock.hcl` to version control)**

**(You MUST use a remote backend with state locking for any shared or production infrastructure)**

**(You MUST use `for_each` with a map/set for non-identical resources -- `count` causes index-shift destruction on removal)**

**(You MUST never store secrets in `.tf` files, `.tfvars`, or state -- use environment variables (`TF_VAR_*`) or your secrets manager)**

**(You MUST run `terraform plan` and review the diff before every `terraform apply` -- never apply blindly)**

</critical_requirements>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Resource definitions, variables, outputs, locals, data sources, provider configuration
- [examples/modules.md](examples/modules.md) - Module structure, composition, versioning, registry publishing
- [examples/state.md](examples/state.md) - Remote backends, state locking, moved/import/removed blocks, workspaces
- [examples/patterns.md](examples/patterns.md) - for_each, dynamic blocks, lifecycle, conditions, validations
- [reference.md](reference.md) - Decision frameworks, CLI cheat sheet, file naming conventions

---

**Auto-detection:** Terraform, OpenTofu, HCL, .tf files, terraform init, terraform plan, terraform apply, terraform fmt, terraform validate, required_providers, terraform block, resource block, data source, module block, variable block, output block, locals, backend configuration, remote state, state locking, moved block, import block, for_each, count, dynamic block, lifecycle, precondition, postcondition, .terraform.lock.hcl, tfvars, provider configuration

**When to use:**

- Writing or reviewing Terraform/OpenTofu configuration files (`.tf`)
- Defining cloud resources, data sources, modules, variables, and outputs
- Managing state backends, locking, and multi-environment deployments
- Refactoring infrastructure with `moved`, `import`, and `removed` blocks
- Structuring reusable modules for team or registry consumption

**When NOT to use:**

- Application code deployment logic (that belongs in CI/CD pipelines)
- Container orchestration configuration (Kubernetes manifests, Helm charts)
- One-off scripting tasks better handled by shell scripts or CLI tools

**Key patterns covered:**

- Provider pinning, lock files, and version constraints
- Resource definitions with meta-arguments (`for_each`, `count`, `depends_on`, `lifecycle`)
- Variable validation, locals for derived values, output descriptions
- Remote backend configuration with state locking
- Module structure (flat composition, single-purpose modules)
- Refactoring with `moved`, `import`, and `removed` blocks
- Custom conditions (`precondition`, `postcondition`, `check` blocks)
- Dynamic blocks for repeated nested configuration
- Environment management (directory-based vs workspaces)

---

<philosophy>

## Philosophy

Terraform is a declarative infrastructure-as-code tool. You describe the desired end-state; Terraform determines the steps to reach it. The HCL configuration language is designed to be human-readable and machine-parseable.

**Core principles:**

- **Declarative, not imperative** -- describe what you want, not how to get there
- **State is the source of truth** -- Terraform tracks what it manages via state; protect it accordingly
- **Modules are the unit of reuse** -- keep them flat, composable, and single-purpose
- **Pin everything** -- provider versions, Terraform version, module versions; reproducibility is non-negotiable
- **Plan before apply** -- always review the diff; never apply blindly in production

**OpenTofu compatibility:** OpenTofu is an open-source fork (MPL 2.0) that is syntax-compatible with Terraform 1.5.x. The patterns in this skill apply to both tools. OpenTofu uses `.tofu` file extensions for OpenTofu-only features and adds native state encryption.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Provider and Version Pinning

Pin Terraform version and all provider versions. Commit `.terraform.lock.hcl` to version control.

```hcl
# terraform.tf
terraform {
  required_version = ">= 1.9.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allows 5.x, blocks 6.0
    }
  }
}
```

**Why this matters:** Without version constraints, `terraform init` on different machines downloads different provider versions, causing inconsistent plans and mysterious drift. The lock file pins exact versions and cryptographic hashes.

**Version constraint syntax:** `= 1.0.0` (exact), `>= 1.0.0` (minimum), `~> 1.0` (allows 1.x, blocks 2.0), `>= 1.0, < 2.0` (range).

See [examples/core.md](examples/core.md) for full provider configuration with aliases and default tags.

---

### Pattern 2: Resource Definitions and Meta-Arguments

Resources follow a standard argument ordering: meta-arguments first, resource arguments next, nested blocks after, lifecycle last.

```hcl
resource "aws_instance" "web" {
  count = var.instance_count  # Meta-argument first

  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  tags = {
    Name = "web-${count.index}"
  }

  lifecycle {  # Lifecycle block last
    create_before_destroy = true
  }
}
```

**Key meta-arguments:** `count`, `for_each`, `depends_on`, `provider`, `lifecycle`. Place meta-arguments at the top, separated from resource arguments by a blank line.

See [examples/core.md](examples/core.md) for argument ordering and naming conventions.

---

### Pattern 3: for_each over count

Use `for_each` with a map or set for non-identical resources. `count` uses numeric indices -- removing an item from the middle shifts all subsequent indices, causing unnecessary destruction and recreation.

```hcl
# for_each with a map -- stable keys, safe removal
resource "aws_iam_user" "team" {
  for_each = toset(var.team_members)  # ["alice", "bob", "carol"]

  name = each.value
}
# Removing "bob" only destroys bob's user -- alice and carol are untouched
```

```hcl
# count -- index-based, dangerous on removal
resource "aws_iam_user" "team" {
  count = length(var.team_members)

  name = var.team_members[count.index]
}
# Removing "bob" (index 1) shifts carol from index 2 to 1 -- carol gets destroyed and recreated
```

**When count is acceptable:** Identical resources where the only difference is the count (e.g., `count = var.enable_feature ? 1 : 0` for conditional creation).

See [examples/patterns.md](examples/patterns.md) for for_each with maps, sets, and conditional patterns.

---

### Pattern 4: Variables with Validation

Every variable needs `type`, `description`, and validation where constraints exist. Use named locals for derived values.

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type for the application server"
  default     = "t3.micro"
}
```

**Key rules:** Always set `type` and `description`. Use `validation` blocks to catch invalid input at plan time. Never use `default` for secrets -- force the caller to provide them.

See [examples/core.md](examples/core.md) for complex variable types, sensitive variables, and output definitions.

---

### Pattern 5: Remote Backend with State Locking

Never use local state for shared infrastructure. Remote backends provide locking, versioning, and team collaboration.

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"  # State locking
  }
}
```

**Critical:** Backend configuration cannot use variables or locals -- values must be literal or passed via `-backend-config` flags during `terraform init`. Use partial configuration for dynamic values.

**State file hierarchy:** Organize state keys by environment and layer (e.g., `prod/network/`, `prod/compute/`, `staging/network/`) to minimize blast radius.

See [examples/state.md](examples/state.md) for backend configuration, partial config, and state organization.

---

### Pattern 6: Module Structure and Composition

Modules are the unit of reuse. Keep modules flat, single-purpose, and composable.

```
modules/
  vpc/
    main.tf          # Resources
    variables.tf     # Inputs
    outputs.tf       # Outputs
    README.md        # Usage docs (makes it public-facing)
  compute/
    main.tf
    variables.tf
    outputs.tf
```

```hcl
# Root module calling child modules
module "vpc" {
  source = "./modules/vpc"

  cidr_block  = "10.0.0.0/16"
  environment = var.environment
}

module "compute" {
  source = "./modules/compute"

  subnet_ids  = module.vpc.private_subnet_ids
  environment = var.environment
}
```

**Key principle:** Keep the module tree flat. Deeply nested modules (module calling module calling module) are hard to debug and reuse. Prefer composition at the root level.

See [examples/modules.md](examples/modules.md) for module versioning, registry sources, and internal vs published modules.

---

### Pattern 7: Refactoring with moved, import, and removed Blocks

Refactor infrastructure without destroying resources.

```hcl
# Rename a resource -- state updated, infrastructure untouched
moved {
  from = aws_instance.web_server
  to   = aws_instance.app_server
}

# Adopt existing infrastructure into Terraform management
import {
  to = aws_s3_bucket.logs
  id = "my-existing-bucket-name"
}

# Remove from Terraform management without destroying the resource
removed {
  from = aws_instance.legacy

  lifecycle {
    destroy = false
  }
}
```

**Always run `terraform plan` after adding these blocks** to verify Terraform interprets the refactoring correctly. Look for "move" and "import" messages in the plan output.

See [examples/state.md](examples/state.md) for module refactoring with moved blocks and bulk imports.

---

### Pattern 8: Lifecycle Meta-Arguments

Control how Terraform manages resource lifecycle.

```hcl
resource "aws_db_instance" "main" {
  # ... configuration ...

  lifecycle {
    prevent_destroy       = true   # Block accidental deletion
    create_before_destroy = true   # Zero-downtime replacement
    ignore_changes        = [tags] # External process manages tags
  }
}
```

**When to use each:**

- `prevent_destroy` -- databases, DNS zones, state buckets (critical resources)
- `create_before_destroy` -- load balancers, instances behind ASGs (zero-downtime)
- `ignore_changes` -- auto-scaling managed attributes, externally tagged resources
- `replace_triggered_by` -- force replacement when a dependency changes that Terraform does not detect

See [examples/patterns.md](examples/patterns.md) for lifecycle combinations and replace_triggered_by.

---

### Pattern 9: Custom Conditions (Preconditions, Postconditions, Checks)

Validate assumptions before provisioning and guarantees after.

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  lifecycle {
    precondition {
      condition     = data.aws_ami.ubuntu.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }

    postcondition {
      condition     = self.public_ip != ""
      error_message = "Instance must have a public IP assigned."
    }
  }
}
```

**Precondition vs postcondition vs check:**

- `precondition` -- validates assumptions before creation (blocks plan)
- `postcondition` -- validates guarantees after creation (blocks apply)
- `check` block -- validates infrastructure state without blocking operations (warnings only)

See [examples/patterns.md](examples/patterns.md) for check blocks and variable validation patterns.

---

### Pattern 10: Dynamic Blocks

Generate repeated nested blocks from collections. Use sparingly -- overuse hurts readability.

```hcl
resource "aws_security_group" "web" {
  name = "web-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

**When to use:** Reusable modules where the number of nested blocks varies per caller. **When not to use:** Write nested blocks literally when the set is small and fixed. Dynamic blocks cannot generate meta-argument blocks (`lifecycle`, `provisioner`).

See [examples/patterns.md](examples/patterns.md) for dynamic block patterns with conditionals.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- **Missing `.terraform.lock.hcl` in version control** -- different team members get different provider versions, causing plan drift and mysterious failures
- **Local state for shared infrastructure** -- no locking means concurrent applies corrupt state; no remote backup means state loss is catastrophic
- **Secrets in `.tf` or `.tfvars` files** -- committed to version control, visible in state file; use `TF_VAR_*` environment variables or your secrets manager
- **Using `count` for non-identical resources** -- removing an item shifts indices, destroying and recreating unrelated resources
- **`terraform apply` without reviewing the plan** -- auto-approve in production is how you delete databases
- **Unpinned provider versions** -- `version = ">= 5.0"` without an upper bound allows major version upgrades that break everything

**Medium Priority:**

- **`depends_on` when an expression reference suffices** -- `depends_on` causes overly conservative plans; let Terraform infer dependencies from expressions
- **Deeply nested module trees** -- modules calling modules calling modules are hard to debug; keep the tree flat and compose at the root
- **`ignore_changes = all`** -- Terraform will never update the resource again, even for intentional changes; be specific about which attributes to ignore
- **No `description` on variables and outputs** -- undocumented inputs/outputs make modules unusable for anyone but the author
- **Hardcoded values instead of variables** -- makes modules non-reusable; parameterize anything that changes between environments

**Gotchas & Edge Cases:**

- Backend configuration cannot use variables, locals, or expressions -- values must be literal strings or passed via `-backend-config` during `terraform init`
- `prevent_destroy` does not prevent destruction if you remove the resource block entirely -- it only prevents `terraform destroy` on the resource while the block exists
- `for_each` keys must be known at plan time -- they cannot reference resource attributes that are computed during apply
- `moved` blocks are processed once during `terraform plan`/`apply` -- remove them after the migration is applied to keep configuration clean
- `terraform state` subcommands (mv, rm, pull, push) bypass safety checks -- use `moved`/`removed` blocks instead for auditable, reviewable refactoring
- `data` sources are read during planning by default -- if they depend on resources being created in the same apply, use `depends_on` to defer the read
- `sensitive = true` on variables prevents the value from appearing in plan output but does NOT encrypt it in state -- state encryption is a separate concern
- `terraform fmt` only formats `.tf` files in the current directory -- use `terraform fmt -recursive` to format all subdirectories
- `toset()` deduplicates -- if your list has duplicates, `for_each = toset(var.list)` silently drops them
- `.tfvars` files are auto-loaded only if named `terraform.tfvars` or `*.auto.tfvars` -- other filenames require explicit `-var-file` flag

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST pin provider versions with constraints in `required_providers` and commit `.terraform.lock.hcl` to version control)**

**(You MUST use a remote backend with state locking for any shared or production infrastructure)**

**(You MUST use `for_each` with a map/set for non-identical resources -- `count` causes index-shift destruction on removal)**

**(You MUST never store secrets in `.tf` files, `.tfvars`, or state -- use environment variables (`TF_VAR_*`) or your secrets manager)**

**(You MUST run `terraform plan` and review the diff before every `terraform apply` -- never apply blindly)**

**Failure to follow these rules will cause state corruption, accidental resource destruction, secret exposure, and non-reproducible infrastructure.**

</critical_reminders>
