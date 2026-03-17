---
name: terraform-module-design
description: |
  Designs and builds reusable Terraform modules. Use when creating reusable infrastructure patterns, encapsulating complex resource groups, standardizing configurations across projects, or organizing code for maintainability. Covers module structure, versioning, composition, and best practices for production modules.

---

# Terraform Module Design Skill

## Table of Contents

**Quick Start** → [What Is This](#purpose) | [When to Use](#when-to-use) | [Simple Example](#quick-start)

**How to Implement** → [Step-by-Step](#instructions) | [Examples](#examples)

**Help** → [Requirements](#requirements) | [See Also](#see-also)

## Purpose

Master module design for creating reusable, testable, well-documented infrastructure components. Learn when to modularize, module structure patterns, input/output design, and composition strategies.

## When to Use

Use this skill when you need to:

- **Create reusable infrastructure patterns** - Build modules for repeated resource groups
- **Encapsulate complex configurations** - Simplify multi-resource setups
- **Standardize across projects** - Ensure consistency in infrastructure
- **Organize code for maintainability** - Structure large Terraform projects
- **Build composable systems** - Combine modules to create larger architectures
- **Version infrastructure components** - Publish and version modules

**When NOT to use:**
- Single one-off resources
- Resources used only once
- No variation between uses

**Trigger Phrases:**
- "Create reusable Terraform module"
- "Design module structure"
- "Define module inputs and outputs"
- "Compose multiple modules"
- "Version Terraform module"

## Quick Start

Create a reusable Pub/Sub module in 5 minutes:

```bash
# 1. Create module structure
mkdir -p modules/pubsub-topic
cd modules/pubsub-topic

# 2. Create files
cat > main.tf << 'EOF'
resource "google_pubsub_topic" "topic" {
  name                    = var.topic_name
  message_retention_duration = "${var.retention_days * 86400}s"
  labels                  = var.labels
}

resource "google_pubsub_subscription" "subscription" {
  name  = "${var.topic_name}-sub"
  topic = google_pubsub_topic.topic.name

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dlq.id
    max_delivery_attempts = var.max_delivery_attempts
  }
}

resource "google_pubsub_topic" "dlq" {
  name = "${var.topic_name}-dlq"
}
EOF

cat > variables.tf << 'EOF'
variable "topic_name" {
  type        = string
  description = "Name of the Pub/Sub topic"
}

variable "retention_days" {
  type        = number
  default     = 7
  description = "Message retention in days"
}

variable "max_delivery_attempts" {
  type        = number
  default     = 5
  description = "Max delivery attempts before DLQ"
}

variable "labels" {
  type        = map(string)
  default     = {}
  description = "Resource labels"
}
EOF

cat > outputs.tf << 'EOF'
output "topic_name" {
  value       = google_pubsub_topic.topic.name
  description = "Name of the Pub/Sub topic"
}

output "subscription_name" {
  value       = google_pubsub_subscription.subscription.name
  description = "Name of the subscription"
}
EOF

# 3. Use module
cd ../..
cat > main.tf << 'EOF'
module "incoming_charges" {
  source = "./modules/pubsub-topic"

  topic_name  = "supplier-charges-incoming"
  retention_days = 7
  labels = {
    environment = "production"
  }
}
EOF

# 4. Deploy
terraform init
terraform apply
```

## Instructions

### Step 1: Decide When to Create a Module

**Create a Module When**:
- ✅ Pattern repeats multiple times in your code
- ✅ Encapsulates complex resource group (5+ related resources)
- ✅ Has configurable inputs that vary per use
- ✅ Produces clear outputs for other modules to consume

**Don't Create a Module For**:
- ❌ Single one-off resources
- ❌ Resources used only once
- ❌ No variation between uses
- ❌ Over-engineering simple setup

**Example**: Pub/Sub topic + subscription + DLQ + IAM (4 resources, repeats twice)
→ Perfect candidate for a module!

### Step 2: Understand Module Structure

**Standard Module Layout**:
```
modules/pubsub-topic/
├── main.tf           # Resources
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── versions.tf       # Provider requirements
└── README.md         # Documentation
```

**Root Module** (your main configuration):
```
terraform/
├── main.tf          # Provider, variables
├── iam.tf           # IAM resources
├── pubsub.tf        # Pub/Sub resources
├── modules/         # Local modules
│   └── pubsub-topic/
├── .terraform.lock.hcl
└── terraform.tfvars
```

**Module Paths**:
```hcl
# Local module
module "incoming" {
  source = "./modules/pubsub-topic"
}

# Remote module (GitHub)
module "incoming" {
  source = "github.com/org/terraform-modules/pubsub-topic"
  version = "~> 1.0"
}

# Terraform Registry
module "incoming" {
  source = "hashicorp/vault/aws"
  version = "~> 0.2"
}
```

### Step 3: Design Module Inputs (Variables)

**Principles**:
- Keep inputs simple and intuitive
- Use descriptive names
- Provide sensible defaults
- Validate constraints

**Example - Pub/Sub Module**:
```hcl
# variables.tf
variable "topic_name" {
  description = "Name of the Pub/Sub topic"
  type        = string

  validation {
    condition     = length(var.topic_name) > 0 && length(var.topic_name) <= 255
    error_message = "Topic name must be 1-255 characters"
  }
}

variable "retention_days" {
  description = "Days to retain messages (0 = unlimited)"
  type        = number
  default     = 7

  validation {
    condition     = var.retention_days >= 0 && var.retention_days <= 365
    error_message = "Retention must be 0-365 days"
  }
}

variable "labels" {
  description = "Resource labels"
  type        = map(string)
  default     = {}

  validation {
    condition     = alltrue([for k, v in var.labels : length(k) > 0 && length(v) > 0])
    error_message = "Labels must have non-empty keys and values"
  }
}

variable "enable_dlq" {
  description = "Enable Dead Letter Queue"
  type        = bool
  default     = true
}
```

**Input Design Patterns**:
```hcl
# Simple inputs
variable "name" { type = string }

# With defaults
variable "replica_count" { type = number; default = 3 }

# Lists
variable "allowed_ips" { type = list(string); default = [] }

# Maps (configuration objects)
variable "config" {
  type = map(object({
    retention_days = number
    dlq_enabled    = bool
  }))
}

# Flexible object
variable "topic_config" {
  type = object({
    retention_days    = number
    enable_dlq        = bool
    max_retries       = number
  })
  default = {
    retention_days = 7
    enable_dlq     = true
    max_retries    = 5
  }
}
```

### Step 4: Design Module Outputs

**Principles**:
- Export only necessary values
- Use descriptive names
- Document what each output is
- Mark sensitive outputs

**Example - Pub/Sub Module**:
```hcl
# outputs.tf
output "topic_id" {
  description = "Topic resource ID"
  value       = google_pubsub_topic.topic.id
}

output "topic_name" {
  description = "Topic name"
  value       = google_pubsub_topic.topic.name
}

output "subscription_name" {
  description = "Subscription name"
  value       = google_pubsub_subscription.subscription.name
}

output "dlq_topic_name" {
  description = "Dead Letter Queue topic name"
  value       = google_pubsub_topic.dlq.name
}

# Sensitive output
output "configuration" {
  description = "Complete module configuration"
  value = {
    topic_name = google_pubsub_topic.topic.name
    dlq_name   = google_pubsub_topic.dlq.name
  }
  sensitive = true
}
```

**Output Best Practices**:
```hcl
# ✅ GOOD: Specific, documented
output "topic_id" {
  description = "Google resource ID of the topic"
  value       = google_pubsub_topic.topic.id
}

# ❌ BAD: Vague, undocumented
output "id" {
  value = google_pubsub_topic.topic.id
}

# ✅ GOOD: Sensible defaults to avoid null values
output "labels" {
  description = "Applied labels"
  value       = merge(var.labels, { module = "pubsub" })
}
```

### Step 5: Create Module Documentation

**README.md Format**:
```markdown
# PubSub Topic Module

Creates a Pub/Sub topic with optional Dead Letter Queue.

## Usage

```hcl
module "incoming_charges" {
  source = "./modules/pubsub-topic"

  topic_name       = "charges-incoming"
  retention_days   = 7
  enable_dlq       = true
}
```

## Arguments

- `topic_name` (required): Name of the topic
- `retention_days` (optional): Message retention in days (default: 7)
- `enable_dlq` (optional): Enable Dead Letter Queue (default: true)
- `labels` (optional): Resource labels (default: {})

## Outputs

- `topic_id`: Topic resource ID
- `topic_name`: Topic name
- `subscription_name`: Subscription name
- `dlq_topic_name`: Dead Letter Queue topic name

## Example with Custom Configuration

```hcl
module "replies" {
  source = "./modules/pubsub-topic"

  topic_name     = "supplier-charges-replies"
  retention_days = 3
  enable_dlq     = true

  labels = {
    environment = "production"
    team        = "charges"
  }
}

output "replies_topic" {
  value = module.replies.topic_name
}
```
```

### Step 6: Compose Modules

**Module Composition**: Combining modules to build larger systems.

```hcl
# main.tf - Compose multiple modules
module "incoming_pubsub" {
  source = "./modules/pubsub-topic"

  topic_name     = "supplier-charges-incoming"
  retention_days = 7
}

module "replies_pubsub" {
  source = "./modules/pubsub-topic"

  topic_name     = "supplier-charges-replies"
  retention_days = 3
}

module "dlq_pubsub" {
  source = "./modules/pubsub-topic"

  topic_name = "supplier-charges-dlq"
  enable_dlq = false  # Don't need DLQ for DLQ!
}

# Use outputs from one module as inputs to another
module "iam_bindings" {
  source = "./modules/pubsub-iam"

  topics = [
    module.incoming_pubsub.topic_name,
    module.replies_pubsub.topic_name,
  ]
}

# Export composed outputs
output "topics" {
  value = {
    incoming = module.incoming_pubsub.topic_name
    replies  = module.replies_pubsub.topic_name
  }
}
```

### Step 7: Version and Maintain Modules

**Module Versioning** (for published modules):

```bash
# git tag for versions
git tag v1.0.0
git push origin v1.0.0

# In code
module "pubsub" {
  source  = "github.com/org/terraform-pubsub-module"
  version = "~> 1.0"
}
```

**Semantic Versioning**:
- `1.0.0` - MAJOR.MINOR.PATCH
- `~> 1.0` - Allows 1.0.x, not 1.1.0
- `>= 1.0, < 2.0` - Allows any 1.x version

**Maintenance Checklist**:
- Update provider versions regularly
- Test module with new Terraform versions
- Document all breaking changes
- Provide migration guides

## Examples

### Example 1: Simple Service Module

```hcl
# modules/gke-service/main.tf
resource "kubernetes_namespace" "service" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_deployment" "service" {
  metadata {
    namespace = kubernetes_namespace.service.metadata[0].name
    name      = var.service_name
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.service_name
      }
    }

    template {
      metadata {
        labels = {
          app = var.service_name
        }
      }

      spec {
        container {
          name  = var.service_name
          image = var.image

          env {
            name  = "PUBSUB_TOPIC"
            value = var.pubsub_topic
          }
        }
      }
    }
  }
}

# modules/gke-service/variables.tf
variable "namespace" { type = string }
variable "service_name" { type = string }
variable "image" { type = string }
variable "replicas" { type = number; default = 3 }
variable "pubsub_topic" { type = string }

# modules/gke-service/outputs.tf
output "namespace" { value = kubernetes_namespace.service.metadata[0].name }
output "deployment_name" { value = kubernetes_deployment.service.metadata[0].name }

# Usage
module "charges_service" {
  source = "./modules/gke-service"

  namespace      = "production"
  service_name   = "supplier-charges"
  image          = "gcr.io/project/charges:1.0.0"
  replicas       = 3
  pubsub_topic   = module.pubsub.topic_name
}
```

### Example 2: Composition Pattern

```hcl
# main.tf - Compose multiple specialized modules
module "pubsub" {
  source = "./modules/pubsub-topic"

  topic_name   = "charges"
  retention_days = 7
}

module "database" {
  source = "./modules/cloud-sql"

  instance_name = "charges-db"
  database_name = "charges"
}

module "gke_service" {
  source = "./modules/gke-service"

  service_name  = "charges-processor"
  image         = "gcr.io/project/processor:1.0"
  pubsub_topic  = module.pubsub.topic_name
  db_connection = module.database.connection_string
}

# Export all outputs
output "infrastructure" {
  value = {
    pubsub_topic  = module.pubsub.topic_name
    database_host = module.database.host
    service_name  = module.gke_service.deployment_name
  }
}
```

### Example 3: Dynamic Module Usage with for_each

```hcl
# main.tf
locals {
  pubsub_topics = {
    "incoming" = {
      retention_days = 7
    }
    "replies" = {
      retention_days = 3
    }
    "events" = {
      retention_days = 14
    }
  }
}

module "topics" {
  for_each = local.pubsub_topics

  source = "./modules/pubsub-topic"

  topic_name     = each.key
  retention_days = each.value.retention_days
}

# Access module outputs
output "topic_names" {
  value = {
    for name, module in module.topics :
    name => module.topic_name
  }
}
```

## Requirements

- Terraform 1.x+
- Module should have clear input/output contracts
- Good README documentation
- Tested with typical use cases

## See Also

- [terraform skill](../terraform-basics/SKILL.md) - General Terraform
- [terraform-gcp-integration](../terraform-gcp-integration/SKILL.md) - GCP patterns
- [terraform-state-management](../terraform-state-management/SKILL.md) - State handling
