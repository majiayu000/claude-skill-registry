---
name: terraform-security
description: Implement security best practices including secrets management, policy as code, and compliance scanning
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 06-terraform-security
bond_type: PRIMARY_BOND
---

# Terraform Security Skill

Production security patterns for Terraform including secrets, policies, and compliance.

## Secrets Management

### HashiCorp Vault
```hcl
provider "vault" {
  address = var.vault_address
}

data "vault_kv_secret_v2" "db" {
  mount = "secret"
  name  = "database/prod"
}

resource "aws_db_instance" "main" {
  username = data.vault_kv_secret_v2.db.data["username"]
  password = data.vault_kv_secret_v2.db.data["password"]
}
```

### AWS Secrets Manager
```hcl
resource "aws_secretsmanager_secret" "db" {
  name                    = "${var.project}/database"
  recovery_window_in_days = 30
}

data "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
}

locals {
  db_credentials = jsondecode(data.aws_secretsmanager_secret_version.db.secret_string)
}
```

### Azure Key Vault
```hcl
data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_mssql_server" "main" {
  administrator_login_password = data.azurerm_key_vault_secret.db_password.value
}
```

## Policy as Code

### Sentinel (Terraform Cloud)
```python
# restrict-instance-types.sentinel
import "tfplan/v2" as tfplan

allowed_types = ["t3.micro", "t3.small", "t3.medium"]

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.type is "aws_instance" implies
      rc.change.after.instance_type in allowed_types
  }
}
```

### OPA/Conftest
```rego
# policy/terraform.rego
package terraform.security

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.acl == "public-read"
  msg := sprintf("Public S3 bucket: %s", [resource.address])
}

deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  resource.change.after.storage_encrypted != true
  msg := sprintf("Unencrypted RDS: %s", [resource.address])
}
```

## Security Scanning

### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.6
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_checkov
        args: [--args=--quiet]

  - repo: https://github.com/aquasecurity/tfsec
    rev: v1.28.4
    hooks:
      - id: tfsec
```

### Checkov Configuration
```yaml
# .checkov.yml
framework:
  - terraform
soft-fail: false
check:
  - CKV_AWS_*
skip-check:
  - CKV_AWS_144  # S3 cross-region replication
```

## Encryption

### KMS Key
```hcl
resource "aws_kms_key" "main" {
  description             = "Main encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = data.aws_iam_policy_document.kms.json
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.project}"
  target_key_id = aws_kms_key.main.key_id
}
```

### Encrypted Resources
```hcl
# S3
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.main.arn
    }
  }
}

# RDS
resource "aws_db_instance" "main" {
  storage_encrypted = true
  kms_key_id       = aws_kms_key.main.arn
}

# EBS
resource "aws_ebs_encryption_by_default" "main" {
  enabled = true
}
```

## Sensitive Data Protection

```hcl
# Mark variables as sensitive
variable "db_password" {
  type      = string
  sensitive = true
}

# Mark outputs as sensitive
output "credentials" {
  value     = local.db_credentials
  sensitive = true
}

# Prevent secrets in logs
resource "aws_db_instance" "main" {
  password = var.db_password

  lifecycle {
    ignore_changes = [password]
  }
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Secrets in state | Direct value usage | Use data sources |
| Policy failures | Non-compliant resource | Fix or add exception |
| AccessDenied | Missing KMS permissions | Check key policy |
| Scan false positives | Overly strict rules | Add skip-check |

## Usage

```python
Skill("terraform-security")
```

## Related

- **Agent**: 06-terraform-security (PRIMARY_BOND)
