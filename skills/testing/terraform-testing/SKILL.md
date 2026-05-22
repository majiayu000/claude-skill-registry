---
name: terraform-testing
description: Testing Terraform configurations with native tests, Terratest, and validation frameworks
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 08-terraform-advanced
bond_type: SECONDARY_BOND
---

# Terraform Testing Skill

Comprehensive testing patterns for Terraform modules and configurations.

## Native Terraform Test (1.6+)

### Basic Test
```hcl
# tests/vpc_test.tftest.hcl
run "vpc_creation" {
  command = plan

  variables {
    vpc_cidr    = "10.0.0.0/16"
    environment = "test"
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR mismatch"
  }

  assert {
    condition     = aws_vpc.main.enable_dns_hostnames == true
    error_message = "DNS hostnames should be enabled"
  }
}
```

### Apply Test
```hcl
run "full_deployment" {
  command = apply

  variables {
    vpc_cidr    = "10.0.0.0/16"
    environment = "test"
  }

  assert {
    condition     = length(aws_subnet.private) == 3
    error_message = "Expected 3 private subnets"
  }
}

run "cleanup" {
  command = apply
  destroy = true
}
```

### Mock Providers
```hcl
mock_provider "aws" {
  mock_resource "aws_instance" {
    defaults = {
      id = "i-mock12345"
    }
  }
}

run "with_mocks" {
  providers = {
    aws = aws
  }

  assert {
    condition     = aws_instance.web.id != ""
    error_message = "Instance ID should be set"
  }
}
```

## Terratest (Go)

### Basic Module Test
```go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
    t.Parallel()

    opts := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "vpc_cidr":    "10.0.0.0/16",
            "environment": "test",
        },
    })

    defer terraform.Destroy(t, opts)
    terraform.InitAndApply(t, opts)

    vpcId := terraform.Output(t, opts, "vpc_id")
    assert.NotEmpty(t, vpcId)

    subnets := terraform.OutputList(t, opts, "private_subnet_ids")
    assert.Equal(t, 3, len(subnets))
}
```

### Validation Test
```go
func TestInvalidInput(t *testing.T) {
    t.Parallel()

    opts := &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "vpc_cidr": "invalid-cidr",
        },
    }

    _, err := terraform.InitAndPlanE(t, opts)
    assert.Error(t, err)
    assert.Contains(t, err.Error(), "Must be a valid CIDR")
}
```

### AWS Resource Verification
```go
import (
    "github.com/aws/aws-sdk-go/service/ec2"
    "github.com/gruntwork-io/terratest/modules/aws"
)

func TestVPCExists(t *testing.T) {
    // ... setup and apply ...

    vpcId := terraform.Output(t, opts, "vpc_id")

    vpc := aws.GetVpcById(t, vpcId, "us-east-1")
    assert.Equal(t, "10.0.0.0/16", *vpc.CidrBlock)
    assert.True(t, *vpc.EnableDnsHostnames)
}
```

## Validation Commands

```bash
# Syntax validation
terraform validate

# Format check
terraform fmt -check -recursive

# Plan validation
terraform plan -detailed-exitcode

# Native tests
terraform test

# Terratest
go test -v -timeout 30m ./tests/
```

## Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.6
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_docs
```

## Test Organization

```
module/
├── main.tf
├── variables.tf
├── outputs.tf
├── tests/
│   ├── basic.tftest.hcl      # Native tests
│   ├── complete.tftest.hcl
│   └── go/
│       ├── module_test.go    # Terratest
│       └── go.mod
└── examples/
    ├── basic/
    └── complete/
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| Test timeout | Slow resource creation | Increase timeout |
| State conflicts | Parallel tests | Use unique names |
| Cleanup failures | Dependencies | Check destroy order |

## Usage

```python
Skill("terraform-testing")
```

## Related

- **Agent**: 08-terraform-advanced (SECONDARY_BOND)
