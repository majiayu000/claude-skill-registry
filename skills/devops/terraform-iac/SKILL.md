/*============================================================================*/
/* TERRAFORM-IAC SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: terraform-iac
version: 1.0.0
description: |
  [assert|neutral] Terraform infrastructure as code specialist for multi-cloud deployments (AWS/GCP/Azure), state management with remote backends, module development, drift detection, policy as code with Sentinel/OPA, a [ground:given] [conf:0.95] [state:confirmed]
category: Infrastructure
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute terraform-iac workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic Infrastructure processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "terraform-iac",
  category: "Infrastructure",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["terraform-iac", "Infrastructure", "workflow"],
  context: "user needs terraform-iac capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Terraform Infrastructure as Code Specialist

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Expert Terraform for cloud-agnostic infrastructure provisioning and state management.

## Purpose

Comprehensive Terraform expertise including multi-cloud deployments, state management, module development, drift detection, and GitOps. Ensures infrastructure is versioned, reproducible, and maintainable.

## When to Use

- Provisioning cloud infrastructure (AWS, GCP, Azure)
- Managing infrastructure state with remote backends
- Creating reusable Terraform modules
- Implementing GitOps for infrastructure
- Detecting and fixing infrastructure drift
- Migrating from manual infrastructure to IaC
- Multi-environment deployments (dev, staging, prod)

## Prerequisites

**Required**: Cloud provider basics (AWS/GCP/Azure), HCL syntax, Terraform CLI

**Agents**: `system-architect`, `cicd-engineer`, `security-manager`, `reviewer`

## Core Workflows

### Workflow 1: AWS Infrastructure with Modules

**Step 1: Directory Structure**

```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── terraform.tfvars
└── modules/
    ├── vpc/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── ec2/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

**Step 2: Main Configuration**

```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}

module "vpc" {
  source = "./modules/vpc"

  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  environment        = var.environment
}

module "ec2" {
  source = "./modules/ec2"

  vpc_id            = module.vpc.vpc_id
  subnet_ids        = module.vpc.private_subnet_ids
  instance_type     = var.instance_type
  instance_count    = var.instance_count
  security_group_id = module.vpc.security_group_id
}
```

**Step 3: Variables and Outputs**

```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "instance_ids" {
  description = "EC2 instance IDs"
  value       = module.ec2.instance_ids
}
```

### Workflow 2: Dynamic Blocks and for_each

```hcl
# Dynamic ingress rules
resource "aws_security_group" "app" {
  name   = "${var.environment}-app-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# for_each for multiple resources
resource "aws_instance" "app" {
  for_each = toset(var.availability_zones)

  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_ids[each.key]

  tags = {
    Name = "${var.environment}-app-${each.key}"
    AZ   = each.v

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/Infrastructure/terraform-iac/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "terraform-iac-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>TERRAFORM_IAC_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
