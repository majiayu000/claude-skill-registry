---
name: devops-maintainability-checker
description: Infrastructure maintainability verification covering naming conventions, formatting, DRY patterns, and version constraints.
allowed-tools: Bash, Glob, Grep, Read
---

# DevOps Maintainability Checker

Verify infrastructure code follows maintainable patterns.

## Maintainability Checklist

| Check | Good | Bad |
|-------|------|-----|
| Resource naming | Consistent `${project}-${env}-${type}` | Random or inconsistent |
| Variable naming | Descriptive with defaults | Cryptic, no descriptions |
| Code formatting | `tofu fmt` passes | Inconsistent indentation |
| DRY principle | Locals for repeated values | Hardcoded values repeated |
| Version constraints | Pinned `~> X.Y` | Unpinned or exact versions |

## Verification Commands

```bash
# Format check
tofu fmt -check -recursive 2>&1 || echo "FAIL: Needs formatting"

# Variable descriptions
grep -L "description" variables.tf && echo "WARN: Variables missing descriptions"

# Locals usage (should have some)
grep -c "local\." *.tf | awk -F: '$2 < 3 {print "WARN: Underusing locals in "$1}'

# Hardcoded values (potential DRY violations)
grep -E '^\s+(region|zone|size)\s*=\s*"[^$]' *.tf

# Provider version constraints
grep -E "version\s*=\s*\"[0-9]" *.tf | grep -v "~>" && echo "WARN: Exact versions, use ~>"
```

## Naming Conventions

**Resource Names:**
```hcl
# GOOD
resource "aws_instance" "web" {
  tags = {
    Name = "${var.project}-${var.environment}-web"
  }
}

# BAD
resource "aws_instance" "instance1" {
  tags = {
    Name = "my-server"
  }
}
```

**Variable Names:**
```hcl
# GOOD
variable "database_instance_class" {
  description = "RDS instance class for the database"
  type        = string
  default     = "db.t3.micro"
}

# BAD
variable "db_class" {
  type = string
}
```

## DRY Patterns

**Use Locals:**
```hcl
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
  name_prefix = "${var.project}-${var.environment}"
}

resource "aws_instance" "web" {
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-web"
  })
}
```

**Avoid Repetition:**
```hcl
# BAD - hardcoded everywhere
resource "aws_instance" "web" {
  tags = { Project = "myapp", Environment = "prod" }
}
resource "aws_instance" "api" {
  tags = { Project = "myapp", Environment = "prod" }
}

# GOOD - use locals
resource "aws_instance" "web" {
  tags = local.common_tags
}
```

## Version Constraints

```hcl
# GOOD - allows patch updates
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# BAD - exact version (breaks updates)
version = "5.31.0"

# BAD - no constraint (unpredictable)
version = ">= 5.0"
```

## Report Format

```
MAINTAINABILITY SCORE: X/10

Formatting: PASS/FAIL
Variable Descriptions: X/Y documented
Locals Usage: GOOD/UNDERUSED
Naming Consistency: CONSISTENT/INCONSISTENT
Version Constraints: PROPER/NEEDS FIX

Issues Found:
- [ ] Run `tofu fmt -recursive`
- [ ] Add descriptions to variables: X, Y, Z
- [ ] Extract repeated value "us-east-1" to local
- [ ] Change exact version to ~> constraint
```
