---
title: "Facets Module Development"
description: "Create and manage Facets IaC modules with Terraform. Covers facets.yaml structure, Terraform file conventions, output types, provider configuration, deep merge patterns, and the complete module development workflow using Raptor CLI."
triggers: ["iac module", "facets module", "tf module", "terraform module", "facets.yaml"]
version: "1.0"
available_in_modes: ["facets"]
category: "development"
tags: ["terraform", "iac", "module", "facets", "infrastructure", "raptor"]
icon: "wrench"
---

# Facets Module Development Guide

A comprehensive reference for LLMs and developers to create Facets.cloud IaC modules.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Core Concepts](#2-core-concepts)
3. [Module Structure](#3-module-structure)
4. [The facets.yaml File](#4-the-facetsyaml-file)
5. [Terraform Files](#5-terraform-files)
6. [Type System and Outputs](#6-type-system-and-outputs)
7. [Provider Passing](#7-provider-passing)
8. [Spec Schema Design](#8-spec-schema-design)
9. [UI Extensions (x-ui-*)](#9-ui-extensions-x-ui)
10. [Best Practices and Anti-Patterns](#10-best-practices-and-anti-patterns)
11. [Module Lifecycle](#11-module-lifecycle)
12. [Complete Examples](#12-complete-examples)
13. [Quick Reference](#13-quick-reference)

---

## 1. Overview

### What is Facets?

Facets.cloud is a self-serve platform that enables:
- **Platform/Infra engineers** to create reusable infrastructure modules
- **Developers** to compose blueprints without Terraform knowledge
- **Teams** to deploy consistent environments across clouds

### What is a Facets Module?

A Facets module is a **Terraform module** enhanced with a **`facets.yaml`** metadata file that:
- Defines a developer-friendly DSL (the `spec`)
- Declares typed inputs and outputs for inter-module connectivity
- Controls UI rendering for the Facets portal
- Enables provider passing between modules

### Key Terminology

| Term | Description |
|------|-------------|
| **Intent (Kind)** | The technology/purpose (e.g., `postgres`, `service`, `kubernetes_cluster`) |
| **Flavor** | The implementation variant (e.g., `ovh`, `aws`, `gcp`, `k8s`) |
| **Version** | Semantic version of the module |
| **Blueprint** | Collection of resource definitions (JSON/YAML) that developers create |
| **Resource** | An instance of a module in a blueprint |
| **Spec** | The developer-facing configuration DSL defined by the module |
| **Project Type** | Template defining which modules are available to a project |
| **Output Type** | JSON schema defining the contract for module outputs |

### The Big Picture

```
Output Types (contracts) → Modules (templates) → Blueprint Resources (instances)
```

- **Output Types**: JSON schemas defining what data modules produce (attributes + interfaces)
- **Modules**: Reusable Terraform templates that consume inputs and produce typed outputs
- **Blueprint Resources**: YAML declarations instantiating modules and wiring dependencies

**Key flow**: Types ensure compatibility → Modules implement infrastructure → Blueprints compose actual systems using `${type.name.out.path}` references.

---

## 2. Core Concepts

### 2.1 The Module Contract

Every Facets module establishes a contract:

```
INPUTS (dependencies) → MODULE (terraform) → OUTPUTS (typed values + providers)
```

- **Inputs**: Other modules this module depends on (e.g., postgres needs network, cloud_account)
- **Outputs**: Typed values and providers this module exposes to others

### 2.2 Intent Interoperability

Modules of the same **intent** (kind) but different **flavors** should expose compatible outputs. This allows:
- Swapping implementations (e.g., `postgres/ovh` → `postgres/aws`) without changing dependent resources
- Blueprint portability across clouds

Example: All `postgres` flavors should expose `@outputs/postgres` with `reader` and `writer` interfaces containing `host`, `port`, `username`, `password`, `connection_string`.

### 2.3 Two Ways to Wire Modules

There are two distinct methods for connecting modules:

**Method 1: Via `inputs` (Compile-Time Dependency)**
- Declared in `facets.yaml` `inputs:` section
- Creates a hard dependency edge in the blueprint graph
- Module receives data via `var.inputs.<name>`
- **Use for:** Providers, required infrastructure dependencies (network, cloud account)

```yaml
# facets.yaml
inputs:
  kubernetes_details:
    type: "@facets/ovh-kubernetes"
    providers:
      - kubernetes
      - helm
```

**Method 2: Via `${}` in spec (Runtime Reference)**
- Developer types or selects via `x-ui-output-type` dropdown
- No compile-time dependency declared
- Expression stored in spec, resolved at deployment
- **Use for:** Optional references, dynamic wiring (env vars, config values)

```yaml
# Blueprint resource spec
spec:
  env:
    DB_HOST: "${postgres.petsdb.out.interfaces.writer.host}"
    DB_PASS: "${postgres.petsdb.out.interfaces.writer.password}"
```

**Key Difference:**
- `inputs`: Module developer declares the dependency; platform ensures it's satisfied
- `${}` in spec: Blueprint developer creates the reference; more flexible but less enforced

### 2.4 Resource Reference Syntax

**Module Output References:**

Format: `${<kind>.<resource_name>.out.<attributes|interfaces>.<path>}`

```
${postgres.main-db.out.interfaces.writer.host}
${postgres.main-db.out.interfaces.writer.password}
${postgres.main-db.out.attributes.database_name}
${service.petclinic.out.attributes.service_name}
${helm.cert-manager.out.attributes.release_name}
```

**Blueprint-Level References:**

These reference project-level configuration:

```
${blueprint.self.artifacts.<artifact_name>}    # Artifact URI (docker image, etc.)
${blueprint.self.secrets.<secret_name>}        # Project secret value
${blueprint.self.variables.<variable_name>}    # Project variable value
```

Examples:
```yaml
spec:
  release:
    image: "${blueprint.self.artifacts.my-service}"     # Resolves to image URI
  env:
    API_KEY: "${blueprint.self.secrets.API_KEY}"        # Resolves to secret value
    BASE_URL: "${blueprint.self.variables.BASE_URL}"    # Resolves to variable value
```

**Discovery Command:**

List all available expressions for a project:
```bash
raptor get resource-output-expressions -p myproject
```

### 2.5 Project Types and Input Discovery

**Always identify which project type you're targeting.** Input types must be exposed by modules available in that project type.

To discover valid input types for a project type:

```bash
# List all output types available in a project type (with provider info)
PT=myprojecttype
raptor get resource-type-mappings $PT -o json | jq -r '.[].id' | while read tf; do
  ver=$(raptor get resource-types -o json | jq -r --arg tf "$tf" \
    '.[] | select("\(.name)/\(.flavor)" == $tf) | "\(.name)/\(.flavor)/\(.version)"' \
    | sort -t/ -k3 -Vr | head -1)
  if [ -n "$ver" ]; then
    echo "=== $ver ==="
    raptor get resource-type-outputs "$ver" -o json | jq -r '.[].type' | while read ot; do
      providers=$(raptor get output-type "$ot" -o json 2>/dev/null | jq -r '.providers[]?.name // empty' | tr '\n' ',' | sed 's/,$//')
      [ -n "$providers" ] && echo "  $ot  [providers: $providers]" || echo "  $ot"
    done
  fi
done
```

---

## 3. Module Structure

### 3.1 Required Files

```
my-module/
├── facets.yaml          # Module metadata, schema, inputs, outputs (REQUIRED)
├── variables.tf         # Terraform variables with specific structure (REQUIRED)
├── main.tf              # Terraform resources (REQUIRED)
├── outputs.tf           # output_attributes and output_interfaces locals (REQUIRED)
└── versions.tf          # Terraform version constraint (OPTIONAL)
```

### 3.2 File Purposes

| File | Purpose |
|------|---------|
| `facets.yaml` | Defines the module's identity, spec schema, inputs, outputs, and UI behavior |
| `variables.tf` | Declares standard Facets variables (`instance`, `instance_name`, `environment`, `inputs`) |
| `main.tf` | Contains the actual Terraform resources |
| `outputs.tf` | Defines `output_attributes` and `output_interfaces` locals (NO output blocks) |
| `versions.tf` | Terraform version constraint only (NO provider versions) |

### 3.3 Critical Terraform Rules

| Rule | Reason |
|------|--------|
| **Terraform v1.5.7 or OpenTofu** | Use versions prior to license changes |
| **No provider blocks** | Providers come from inputs via `providers:` field |
| **No provider version constraints** | Versions defined in output type schemas |
| **No output blocks** | Use `local.output_attributes` and `local.output_interfaces` |
| **Use `lookup()` with defaults** | Never use `try()` |
| **Add `prevent_destroy = true`** | For stateful resources (databases, storage, CDNs) |

---

## 4. The facets.yaml File

This is the heart of a Facets module. It defines everything the platform needs to integrate your module.

### 4.1 Complete Structure

```yaml
# === IDENTITY ===
intent: postgres                    # The kind/technology (REQUIRED)
flavor: ovh                         # Implementation variant (REQUIRED)
version: "1.0"                      # Semantic version, quoted (REQUIRED)
description: |                      # Human-readable description (REQUIRED)
  Creates a managed PostgreSQL database on OVH Cloud
clouds:                             # Compatible clouds (REQUIRED for now)
  - aws                             # Valid: aws, azure, gcp, kubernetes
  # Note: Legacy field, will be removed. When in doubt, include all.

# === INPUTS (Dependencies) ===
inputs:
  cloud_account:                    # Input name (used in var.inputs.cloud_account)
    type: "@facets/aws_cloud_account"  # Output type this input accepts
    optional: false                 # Whether this input is required
    displayName: AWS Cloud Account  # UI display name
    description: AWS cloud account for provisioning
    providers:                      # Providers this input supplies to the module
      - aws
  network:                          # Input without provider (data only)
    type: "@mycompany/vpc-details"
    optional: false
    displayName: VPC Network
    description: Network configuration

# === OUTPUTS ===
outputs:
  # REQUIRED: 'default' is the primary output, used for UI autocomplete
  default:
    type: "@outputs/postgres"       # Output type contract
    title: PostgreSQL Database
    # If exposing providers, define them here:
    providers:
      kubernetes:
        source: hashicorp/kubernetes
        version: 2.23.0
        attributes:
          host: attributes.cluster_endpoint
          cluster_ca_certificate: attributes.cluster_ca_certificate

  # OPTIONAL: Expose attribute subset for x-ui-output-type wiring
  attributes:
    type: "@mycompany/postgres_attributes"
    title: PostgreSQL Attributes

  # OPTIONAL: Expose nested fields with generic types for cross-module reuse
  attributes.read_only_iam_policy_arn:
    type: "@outputs/iam_policy_arn"
    title: Read-Only IAM Policy

# === ARTIFACT INPUTS (for deployable modules) ===
artifact_inputs:                    # Optional: for modules that deploy artifacts
  primary:
    attribute_path: spec.release.image   # Path in spec where artifact URI goes
    artifact_type: docker_image          # "docker_image" or "freestyle"

# === SPEC SCHEMA ===
spec:
  title: PostgreSQL Configuration
  description: Configure your PostgreSQL database
  type: object
  properties:
    version:
      type: string
      title: PostgreSQL Version
      enum: ["14", "15", "16"]
      default: "15"
    # ... more properties
  required:
    - version
  x-ui-order:
    - version

# === SAMPLE RESOURCE ===
sample:
  kind: postgres
  flavor: ovh
  version: "1.0"
  disabled: false
  spec:
    # ONLY include fields that have defaults defined in spec.properties
    # Never fabricate values for fields without defaults
    version: "15"
```

### 4.2 Identity Fields

| Field | Required | Description |
|-------|----------|-------------|
| `intent` | Yes | The kind/technology. Use existing intents for interoperability. |
| `flavor` | Yes | Your implementation variant. Often the cloud provider name. |
| `version` | Yes | Semantic version. **Must be quoted**: `"1.0"` not `1.0` |
| `description` | Yes | Clear description of what the module creates |
| `clouds` | Yes (legacy) | Array of: `aws`, `azure`, `gcp`, `kubernetes`. Will be deprecated. |

### 4.3 Inputs Section

Inputs declare dependencies on other modules. The platform wires these automatically based on blueprint connections.

```yaml
inputs:
  <input_name>:
    type: "<output_type>"           # The output type to accept
    optional: true|false            # Default: false
    displayName: "Display Name"     # Shown in UI
    description: "Description"      # Help text
    providers:                      # Providers this input supplies (if any)
      - kubernetes
      - helm
```

**Key Points:**
- Input names become keys in `var.inputs.<input_name>`
- The `type` must match an output type from another module in the same project type
- `providers` list declares which Terraform providers this input supplies
- Inputs without `providers` are data-only (no provider configuration)

**Optional Inputs:**

Use `optional: true` when a dependency is not always needed:

```yaml
inputs:
  prometheus:
    type: "@facets/prometheus"
    optional: true                  # Only needed if metrics export is enabled
    displayName: Prometheus
    description: Prometheus instance for metrics export
```

In `variables.tf`, mark the corresponding input as optional:
```hcl
variable "inputs" {
  type = object({
    prometheus = optional(object({
      attributes = object({
        endpoint = string
      })
    }))
  })
}
```

In `main.tf`, check if the optional input is provided:
```hcl
locals {
  metrics_enabled = var.inputs.prometheus != null
}
```

### 4.4 Outputs Section

Outputs declare what this module exposes to others.

#### Understanding the `default` Output

The `default` output represents the **complete module output** - the combination of all `output_attributes` and `output_interfaces` your module produces. It is:

- **Required** for every module
- **Used for UI autocomplete** when developers reference outputs via `${kind.name.out...}`
- **The identity** of what your module exposes

The output type you assign to `default` is a design decision:

**Option 1: Flavor-specific type** (when implementation details matter to consumers)
```yaml
# kubernetes_cluster/eks/facets.yaml
outputs:
  default:
    type: "@facets/eks_details"      # EKS-specific: includes EKS-only attributes
```

**Option 2: Generic/interoperable type** (when implementation is irrelevant to consumers)
```yaml
# mysql/rds/facets.yaml
outputs:
  default:
    type: "@outputs/mysql"           # Generic: any MySQL works the same for consumers
```

#### Designing for Interoperability with Sub-paths

You can expose **sub-paths** of your output with different (often more generic) types. This enables cross-flavor compatibility:

```yaml
# kubernetes_cluster/eks/facets.yaml
outputs:
  default:
    type: "@facets/eks_details"              # Full EKS-specific output
    title: EKS Cluster
    providers:
      kubernetes: ...
      helm: ...
  attributes.kubernetes:
    type: "@facets/k8s_details"              # Generic Kubernetes interface
    title: Kubernetes Access

# kubernetes_cluster/gke/facets.yaml
outputs:
  default:
    type: "@facets/gke_details"              # Full GKE-specific output
    providers:
      kubernetes: ...
      helm: ...
  attributes.kubernetes:
    type: "@facets/k8s_details"              # Same generic type as EKS!
    title: Kubernetes Access
```

**Result:** A service module that only needs Kubernetes access can declare:
```yaml
inputs:
  k8s:
    type: "@facets/k8s_details"    # Works with both EKS and GKE!
```

This pattern allows consumers to:
- Wire to `default` when they need flavor-specific features
- Wire to a sub-path when they only need generic capabilities
- Swap implementations (EKS ↔ GKE) without changing dependent modules

**Key insight:** Designing output type contracts is a critical part of module development. It determines interoperability and flexibility for consumers.

#### Output Declaration Syntax

```yaml
outputs:
  # Primary output (required)
  default:
    type: "<output_type>"           # Type contract
    title: "Human Title"
    providers:                      # Optional: provider configurations
      <provider_name>:
        source: hashicorp/kubernetes
        version: 2.23.0
        attributes:
          host: attributes.cluster_endpoint

  # Optional: Subset for x-ui-output-type dropdowns
  attributes:
    type: "<attribute_output_type>"
    title: "Attributes for wiring"

  # Optional: Nested path for generic type reuse
  attributes.some_field:
    type: "@outputs/generic_type"
    title: "Specific Field"
```

#### Nested Output Paths

Nested paths like `attributes.read_only_iam_policy_arn` enable generic type reuse:
- A Loki module might create an S3 bucket internally with `output_attributes.s3_bucket_arn`
- Declare `attributes.s3_bucket_arn` with type `@outputs/s3_bucket_arn`
- Now any module with input type `@outputs/s3_bucket_arn` sees Loki in the dropdown
- Schema at that path must match the declared output type

### 4.5 Artifact Inputs Section

For modules that deploy container images or other artifacts (like services, jobs), use `artifact_inputs` to declare which spec fields receive artifact URIs.

```yaml
artifact_inputs:
  primary:
    attribute_path: spec.release.image   # Dot-path to the spec field
    artifact_type: docker_image          # "docker_image" or "freestyle"
```

**Artifact Types:**
- `docker_image`: Container images (Docker, OCI)
- `freestyle`: Any other deployable artifact (zip files, binaries, etc.)

**How it works:**
1. Users register artifacts in the Facets portal with URIs per environment
2. In spec, use `${blueprint.self.artifacts.<artifact_name>}` to reference the artifact
3. At deployment, the expression resolves to the registered URI for that environment

**Example in spec:**
```yaml
spec:
  properties:
    release:
      type: object
      properties:
        image:
          type: string
          title: Container Image
          default: "${blueprint.self.artifacts.my-service}"
```

### 4.6 Sample Section

Provides a template resource for users when they add this module to a blueprint.

```yaml
sample:
  kind: postgres
  flavor: ovh
  version: "1.0"
  disabled: false                   # false = enabled, true = disabled (module not invoked)
  spec:
    # CRITICAL: Only include fields that have 'default' defined in spec.properties
    # Never fabricate values - if no default exists, omit the field
    version: "15"
```

**The `disabled` field:**
- `disabled: false` - Resource is enabled; module will be invoked during deployment
- `disabled: true` - Resource is disabled; module is skipped entirely during deployment

Users can override `disabled` per environment to enable/disable resources selectively.

---

## 5. Terraform Files

### 5.1 Understanding var.inputs (Dependencies)

**`var.inputs` represents your module's dependencies** - the prerequisites that must exist before your module can be provisioned.

When you declare an input in `facets.yaml`:
```yaml
inputs:
  network:
    type: "@facets/ovh-network"
    optional: false
```

You're saying: "This module cannot be provisioned without a network. Give me the outputs from a module that exposes `@facets/ovh-network`."

**The structure of `var.inputs.<name>` is determined by the output type schema you're consuming.**

#### Discovering Input Structure

To know what fields are available in `var.inputs.network`, look up the output type schema:

```bash
raptor get output-type @facets/ovh-network -o json
```

This returns something like:
```json
{
  "properties": {
    "type": "object",
    "properties": {
      "attributes": {
        "type": "object",
        "properties": {
          "network_id": { "type": "string" },
          "region": { "type": "string" },
          "db_subnet_id": { "type": "string" },
          "network_cidr": { "type": "string" }
        }
      },
      "interfaces": {
        "type": "object",
        "properties": {}
      }
    }
  }
}
```

This tells you `var.inputs.network` will have:
- `var.inputs.network.attributes.network_id`
- `var.inputs.network.attributes.region`
- `var.inputs.network.attributes.db_subnet_id`
- `var.inputs.network.attributes.network_cidr`

#### Translating to variables.tf

Use the output type schema to construct your `var.inputs` type:

```hcl
variable "inputs" {
  type = object({
    # Each key matches an input name from facets.yaml
    network = object({
      # Structure comes from @facets/ovh-network schema
      attributes = object({
        network_id    = string
        region        = string
        db_subnet_id  = string
        network_cidr  = string
      })
      # interfaces = object({}) # Empty in this case, can omit
    })
  })
}
```

#### The attributes vs interfaces Pattern

Output types typically have two sections:
- **`attributes`**: Flat key-value data (IDs, names, ARNs, configuration values)
- **`interfaces`**: Connection parameters (host, port, username, password for databases)

```hcl
# Accessing attributes (simple values)
var.inputs.ovh_provider.attributes.project_id
var.inputs.network.attributes.region

# Accessing interfaces (connection details)
var.inputs.postgres.interfaces.writer.host
var.inputs.postgres.interfaces.writer.password
```

#### Inputs with Providers vs Data-Only Inputs

Some inputs provide Terraform providers, others just provide data:

```yaml
inputs:
  # This input provides the 'ovh' provider to your module
  ovh_provider:
    type: "@facets/ovh-provider"
    providers:
      - ovh

  # This input only provides data (no providers list)
  network:
    type: "@facets/ovh-network"
```

Both are accessed the same way via `var.inputs.<name>`, but only inputs with `providers` will configure Terraform providers for your module to use.

#### Nested Output Paths and Input Structure

**Important:** When a module declares an output with a nested path like `attributes.k8s_details`:

```yaml
# EKS module facets.yaml
outputs:
  attributes.k8s_details:
    type: '@facets/eks'
```

The consumer receives that **sub-object directly**, not wrapped in `.attributes/.interfaces`.

```hcl
# Consumer module - kubernetes_details IS the attributes content
local.kubernetes_details.k8s_details      # Correct
local.kubernetes_details.default_tags     # Correct
local.kubernetes_details.attributes.xxx   # WRONG - no .attributes wrapper
```

**Rule of thumb:** Always check how existing modules access their inputs to understand the actual structure being passed.

---

### 5.2 Understanding var.instance (Resource Configuration)

The `var.instance.spec` structure must mirror `facets.yaml spec.properties`.

**EXCEPTION: x-ui-output-type fields** - When a spec field uses `x-ui-output-type`, the types differ:

| Location | Type | Reason |
|----------|------|--------|
| facets.yaml spec | `type: string` | Stores expression like `${s3.bucket.out.attributes}` |
| variables.tf | `object({...})` | Expression resolves to actual object at runtime |

```yaml
# facets.yaml - string because it holds the wiring expression
s3_bucket:
  type: string
  x-ui-output-type: "@mycompany/s3_bucket_attributes"
```

```hcl
# variables.tf - object because expression resolves at runtime
s3_bucket = object({
  bucket_name                 = string
  bucket_arn                  = string
  bucket_regional_domain_name = string
})
```

**Full Example:**

```hcl
variable "instance" {
  type = object({
    kind    = string
    flavor  = string
    version = string
    spec = object({
      # Simple fields - mirror spec.properties
      index_document     = optional(string, "index.html")
      versioning_enabled = optional(bool, false)
      price_class        = optional(string, "PriceClass_100")

      # Map type for patternProperties
      origins = optional(map(object({
        s3_bucket = object({           # x-ui-output-type field - object type
          bucket_name                 = string
          bucket_arn                  = string
          bucket_regional_domain_name = string
        })
        path_pattern = optional(string, "default")
      })), {})

      # Free-form maps (x-ui-yaml-editor fields)
      env    = optional(map(string), {})
      labels = optional(map(string), {})
    })
  })
}

variable "instance_name" {
  type        = string
  description = "Unique architectural name from blueprint"
}

variable "environment" {
  type = object({
    name        = string              # Logical name (e.g., "dev", "prod")
    unique_name = string              # Globally unique (includes project)
    cloud_tags  = optional(map(string), {})
  })
}

variable "inputs" {
  type = object({
    cloud_account = object({
      attributes = object({
        aws_region   = string
        aws_iam_role = string
        external_id  = string
        session_name = string
      })
    })
    # Input from another module (matches output type schema)
    s3_bucket = optional(object({
      bucket_name                 = string
      bucket_arn                  = string
      bucket_regional_domain_name = string
    }))
  })
}
```

### 5.3 Resource Naming Convention

Use `var.instance_name` and `var.environment` for resource names:

```hcl
locals {
  # Pattern 1: Globally unique (recommended)
  name = "${var.instance_name}-${var.environment.unique_name}"

  # Pattern 2: Unique within project
  name = "${var.instance_name}-${var.environment.name}"

  # Pattern 3: Just instance name (when uniqueness handled elsewhere)
  name = var.instance_name
}
```

**Note:** `var.environment.unique_name` includes project name, making resources globally unique across all projects and environments.

### 5.4 main.tf

Standard Terraform resources using the variables:

```hcl
locals {
  name = "${var.instance_name}-${var.environment.unique_name}"
}

resource "aws_s3_bucket" "this" {
  bucket        = local.name
  force_destroy = lookup(var.instance.spec, "force_destroy", false)
  tags          = var.environment.cloud_tags
}

# Access inputs from other modules
resource "aws_s3_bucket_policy" "this" {
  bucket = var.inputs.s3_bucket.bucket_name
  # ...
}

# Stateful resources MUST have prevent_destroy
resource "aws_rds_cluster" "this" {
  cluster_identifier = local.name
  # ...

  lifecycle {
    prevent_destroy = true
  }
}
```

### 5.5 outputs.tf

**CRITICAL: Do NOT use Terraform `output` blocks.** Facets automatically extracts outputs from two special locals:

```hcl
locals {
  output_attributes = { ... }  # Facets reads this automatically
  output_interfaces = { ... }  # Facets reads this automatically
}
```

Facets handles the output mechanism internally. You just define the locals - never write `output "..." { }` blocks.

#### Understanding `attributes` vs `interfaces`

| Field | Purpose | Structure | Use For |
|-------|---------|-----------|---------|
| `output_attributes` | All non-network outputs | Flat key-value map | IDs, ARNs, names, config values, everything else |
| `output_interfaces` | **Network endpoints only** | `<endpoint_name>` → `{host, port, ...}` | Database connections, API endpoints, service URLs |

#### Basic Module (no network endpoints)

```hcl
locals {
  output_attributes = {
    bucket_name                 = aws_s3_bucket.this.id
    bucket_arn                  = aws_s3_bucket.this.arn
    bucket_regional_domain_name = aws_s3_bucket.this.bucket_regional_domain_name
  }

  output_interfaces = {}  # Empty - no network endpoints
}
```

#### Module with Network Endpoints (databases, services)

```hcl
locals {
  output_attributes = {
    cluster_id  = aws_rds_cluster.this.id
    cluster_arn = aws_rds_cluster.this.arn
    api_key     = var.api_key
    secrets     = ["api_key"]  # Fields hidden in UI unless user has permission
  }

  # interfaces: <endpoint_name> → {connection details}
  output_interfaces = {
    primary = {                    # Endpoint name - can be anything meaningful
      host              = aws_rds_cluster.this.endpoint
      port              = tostring(aws_rds_cluster.this.port)
      username          = aws_rds_cluster.this.master_username
      password          = aws_rds_cluster.this.master_password
      connection_string = "postgres://${aws_rds_cluster.this.endpoint}:${aws_rds_cluster.this.port}"
      secrets           = ["password", "connection_string"]
    }
    readonly = {                   # Another endpoint
      host = aws_rds_cluster.this.reader_endpoint
      port = tostring(aws_rds_cluster.this.port)
    }
  }
}
```

#### `interfaces` Endpoint Naming

The endpoint name (key) is flexible - choose names meaningful to your module:

| Module Type | Example Endpoint Names |
|-------------|------------------------|
| Database | `primary`, `readonly`, `writer`, `reader` |
| API Service | `api`, `admin`, `internal`, `public` |
| Message Queue | `producer`, `consumer`, `management` |
| Cache | `primary`, `replica` |

#### The `secrets` Key (Hiding Sensitive Fields)

The `secrets` key is a **special reserved field** that lists which sibling fields contain sensitive data. Fields listed in `secrets` are hidden in the Facets UI unless the user has permission to view secrets.

```hcl
output_attributes = {
  cluster_id  = aws_rds_cluster.this.id      # Visible to all
  api_key     = var.api_key                   # Hidden - listed in secrets
  secrets     = ["api_key"]                   # Declares which fields are sensitive
}

output_interfaces = {
  primary = {
    host              = "db.example.com"      # Visible
    port              = "5432"                # Visible
    username          = "admin"               # Visible
    password          = "secret123"           # Hidden - listed in secrets
    connection_string = "postgres://..."      # Hidden - listed in secrets
    secrets           = ["password", "connection_string"]
  }
}
```

**Rules:**
- `secrets` is an array of strings naming the sensitive sibling fields
- Can be used in both `output_attributes` and within each `output_interfaces` endpoint
- Only lists field names at the same level (not nested paths)

#### Key Points Summary

- `output_attributes`: Everything that isn't a network endpoint
- `output_interfaces`: Reserved for network connection details only
- Endpoint names are your choice - NOT limited to `reader`/`writer`
- Each endpoint object typically has: `host`, `port`, optional credentials
- `secrets` array: Lists field names containing sensitive data (hidden in UI)
- **Both locals MUST be present**, even if empty
- All values should be strings (use `tostring()` for numbers)

### 5.6 versions.tf

**Only specify Terraform version, NOT provider versions:**

```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  # NO required_providers block - providers come from inputs
}
```

---

## 6. Type System and Outputs

### 6.1 Output Types

Output types define contracts between modules. They enable:
- Type checking when connecting modules
- Automatic provider configuration
- Blueprint validation
- UI dropdowns for module selection

**Design Consideration:** The choice of output type for `default` affects interoperability. Use flavor-specific types when consumers need implementation details; use generic types when the implementation is transparent to consumers. See [Section 4.4](#44-outputs-section) for detailed examples.

**Naming Conventions:**
```
@outputs/<intent>        # Standard intent outputs (postgres, redis, service)
@facets/<name>           # Facets-specific types (aws_cloud_account, kubernetes-details)
@<company>/<name>        # Organization-specific types
```

### 6.2 Output Type Schema

Output types are **JSON Schema** documents with an additional `providers` array for Terraform provider configuration.

```bash
raptor create output-type @namespace/name -f schema.json
```

**Schema Structure (JSON Schema + providers):**
```
{
  "properties": {           ← Standard JSON Schema wrapper
    "type": "object",
    "properties": {
      "attributes": {...},  ← JSON Schema for flat key-value outputs
      "interfaces": {...}   ← JSON Schema for network endpoint outputs
    }
  },
  "providers": [...]        ← Non-JSON-Schema: Terraform provider configs
}
```

**Schema without providers (most modules):**
```json
{
  "properties": {
    "type": "object",
    "properties": {
      "attributes": {
        "type": "object",
        "properties": {
          "bucket_name": { "type": "string" },
          "bucket_arn": { "type": "string" }
        }
      },
      "interfaces": {
        "type": "object",
        "properties": {}
      }
    }
  },
  "providers": []
}
```

**Schema with interfaces (for modules exposing network endpoints):**
```json
{
  "properties": {
    "type": "object",
    "properties": {
      "attributes": {
        "type": "object",
        "properties": {
          "cluster_id": { "type": "string" },
          "cluster_arn": { "type": "string" }
        }
      },
      "interfaces": {
        "type": "object",
        "properties": {
          "primary": {
            "type": "object",
            "properties": {
              "host": { "type": "string" },
              "port": { "type": "string" },
              "username": { "type": "string" },
              "password": { "type": "string" },
              "connection_string": { "type": "string" }
            }
          },
          "readonly": {
            "type": "object",
            "properties": {
              "host": { "type": "string" },
              "port": { "type": "string" }
            }
          }
        }
      }
    }
  },
  "providers": []
}
```

**Schema with providers (for modules that expose Terraform providers):**
```json
{
  "properties": {
    "type": "object",
    "properties": {
      "attributes": {
        "type": "object",
        "properties": {
          "aws_region": { "type": "string" },
          "aws_iam_role": { "type": "string" }
        }
      },
      "interfaces": {
        "type": "object",
        "properties": {}
      }
    }
  },
  "providers": [
    {
      "name": "aws",
      "source": "hashicorp/aws",
      "version": "5.0.0"
    }
  ]
}
```

**Key Rules:**
- The `properties` section follows standard JSON Schema
- The `providers` array is Facets-specific (not JSON Schema)
- If `facets.yaml` outputs section has `providers:`, the output type schema MUST have matching `providers` array

### 6.3 Understanding `interfaces` in Output Types

The `interfaces` section is **reserved for network endpoints**. Each key is an endpoint name, and the value is an object with connection details.

**Structure:**
```
interfaces.<endpoint_name>.host
interfaces.<endpoint_name>.port
interfaces.<endpoint_name>.username
interfaces.<endpoint_name>.password
interfaces.<endpoint_name>.connection_string
```

**Endpoint names are flexible** - choose names meaningful to your module:

| Intent | Common Endpoint Names |
|--------|----------------------|
| Database (postgres, mysql) | `primary`, `readonly` or `writer`, `reader` |
| Cache (redis, valkey) | `primary`, `replica` |
| Message Queue | `producer`, `consumer` |
| API/Service | `api`, `admin`, `internal` |

### 6.4 Standard Output Contracts

When implementing common intents, follow these output structures:

**Database (@outputs/postgres, @outputs/mysql):**
```hcl
output_interfaces = {
  primary = {              # Or "writer" - endpoint for read-write access
    host              = string
    port              = string
    username          = string
    password          = string  # secret
    connection_string = string  # secret
    secrets           = ["password", "connection_string"]
  }
  readonly = {             # Or "reader" - endpoint for read-only access
    host              = string
    port              = string
    username          = string
    password          = string
    connection_string = string
    secrets           = ["password", "connection_string"]
  }
}
```

**Cache (@outputs/redis, @outputs/valkey):**
```hcl
output_interfaces = {
  primary = {
    host              = string
    port              = string
    password          = string  # secret
    connection_string = string  # secret (redis://...)
    secrets           = ["password", "connection_string"]
  }
}
```

**Service/API:**
```hcl
output_interfaces = {
  api = {
    host = string          # Service hostname
    port = string          # Service port
  }
}
```

### 6.5 Reusing Output Types

**Prefer existing output types for interoperability.**

Before creating new types, check what's available:

```bash
# List all output types in your project type
PT=myprojecttype
raptor get resource-type-mappings $PT -o json | jq -r '.[].id' | while read tf; do
  ver=$(raptor get resource-types -o json | jq -r --arg tf "$tf" \
    '.[] | select("\(.name)/\(.flavor)" == $tf) | "\(.name)/\(.flavor)/\(.version)"' \
    | sort -t/ -k3 -Vr | head -1)
  [ -n "$ver" ] && raptor get resource-type-outputs "$ver" -o json | jq -r '.[].type'
done | sort -u
```

**When to reuse:**
- Your module outputs similar data (e.g., another S3 bucket → use existing S3 type)
- Generic types exist (e.g., `@outputs/iam_policy_arn`, `@outputs/endpoint`)
- Cross-module wiring is desired (reusing types makes modules appear in dropdowns)

**When to create new:**
- No existing type matches your output structure
- Module has unique attributes not covered by generic types

### 6.6 Validating Outputs Before Publishing

**Critical:** Ensure `local.output_attributes` and `local.output_interfaces` match the declared output type schema.

```bash
# 1. Get your declared output type schema
raptor get output-type @mycompany/my_type -o json | jq '.properties.properties.attributes.properties'

# 2. Compare with your outputs.tf local.output_attributes keys
# They MUST match - same field names, compatible types
```

**Validation checklist:**
- [ ] Every field in output type schema exists in `local.output_attributes` or `local.output_interfaces`
- [ ] Field names match exactly (case-sensitive)
- [ ] If output type has `providers`, facets.yaml outputs section declares them
- [ ] `secrets` array lists all sensitive fields

---

## 7. Provider Passing

Facets automatically configures providers. Modules never define provider blocks.

### 7.1 How It Works

1. **Module A** (e.g., cloud_account) exposes providers in its output
2. **Module B** (e.g., postgres) declares it needs those providers in its input
3. **Facets** constructs provider blocks and passes them to Module B

### 7.2 Exposing Providers (in outputs)

```yaml
# kubernetes_cluster/facets.yaml
outputs:
  default:
    type: "@facets/kubernetes-details"
    title: Kubernetes Cluster
    providers:
      kubernetes:                          # Provider alias
        source: hashicorp/kubernetes       # Terraform provider source
        version: 2.23.0                    # Provider version
        attributes:                        # Map output attributes to provider config
          host: attributes.cluster_endpoint
          cluster_ca_certificate: attributes.cluster_ca_certificate
          client_certificate: attributes.client_certificate
          client_key: attributes.client_key
      helm:
        source: hashicorp/helm
        version: 2.11.0
        attributes:
          kubernetes:                      # Nested provider config
            host: attributes.cluster_endpoint
            cluster_ca_certificate: attributes.cluster_ca_certificate
```

### 7.3 Consuming Providers (in inputs)

```yaml
# service/facets.yaml
inputs:
  kubernetes_details:
    type: "@facets/kubernetes-details"
    optional: false
    displayName: Kubernetes Cluster
    providers:                             # List providers you need
      - kubernetes
      - helm
```

### 7.4 Provider Chain Example

```
cloud_account → network → kubernetes_cluster → service
     ↓              ↓            ↓                ↓
    aws          (data)    kubernetes/helm    (uses both)
```

---

## 8. Spec Schema Design

The `spec` section defines the developer-facing DSL using JSON Schema.

### 8.1 Basic Structure

```yaml
spec:
  title: Module Configuration
  description: Configure your resource
  type: object
  properties:
    # ... property definitions
  required:
    - required_field
  x-ui-order:
    - field1
    - field2
```

### 8.2 Property Types

**String with enum:**
```yaml
version:
  type: string
  title: Version
  default: "15"
  enum: ["14", "15", "16"]
```

**Integer with range:**
```yaml
nodes_count:
  type: integer
  title: Number of Nodes
  minimum: 1
  maximum: 10
  default: 3
```

**Boolean:**
```yaml
enable_ssl:
  type: boolean
  title: Enable SSL
  default: true
```

**Nested object:**
```yaml
advanced_config:
  type: object
  title: Advanced Configuration
  x-ui-toggle: true                 # Collapsible section
  properties:
    timeout:
      type: string
      default: "300"
    max_connections:
      type: integer
      default: 100
```

**Map with patternProperties (use instead of arrays):**

Maps are the default choice for collections. Arrays break environment overrides. See [Section 10.1](#101-do-use-maps-instead-of-arrays-critical) for details.

```yaml
ports:
  type: object
  title: Ports
  patternProperties:
    "^[a-zA-Z0-9_-]+$":            # Key pattern (regex)
      type: object
      properties:
        port:
          type: string
        protocol:
          type: string
          enum: [tcp, udp]
      required:
        - port
        - protocol
```

**Output type reference (for wiring modules):**
```yaml
s3_bucket:
  type: string                      # String in spec (holds expression)
  title: S3 Bucket
  x-ui-output-type: "@mycompany/s3_bucket_attributes"
```

### 8.3 Design for Deep Merge

Facets applies environment overrides using deep merge. **Arrays are replaced entirely; maps merge at key level.**

**Problem with arrays:**
```yaml
# Base: volumes: [{name: config, path: /etc}, {name: data, path: /var}]
# Override: Must repeat ENTIRE array to change one item
```

**Solution - Use patternProperties:**
```yaml
volumes:
  type: object
  patternProperties:
    "^[a-zA-Z0-9_-]+$":
      type: object
      properties:
        path:
          type: string
```

**Result:**
```yaml
# Base
volumes:
  config:           # Key: stable identifier
    path: /etc/config
  data:
    path: /var/data

# Override - only changes what's needed
volumes:
  data:
    path: /mnt/fast-data   # Only this changes; config inherited
```

### 8.4 x-ui-yaml-editor vs patternProperties

| Feature | patternProperties | x-ui-yaml-editor |
|---------|-------------------|------------------|
| Schema validation | Yes | No |
| Deep merge | Yes | No |
| UI form generation | Yes | YAML editor |
| Use case | Structured objects | Free-form key-value (env, labels, tags) |

```yaml
# Use patternProperties for structured data
ports:
  type: object
  patternProperties:
    "^[a-zA-Z0-9_-]+$":
      type: object
      properties:
        port: { type: string }
        protocol: { type: string }

# Use x-ui-yaml-editor for free-form maps
env:
  type: object
  title: Environment Variables
  x-ui-yaml-editor: true
```

---

## 9. UI Extensions (x-ui-*)

Facets extends JSON Schema with `x-ui-*` properties to control portal UI rendering.

### 9.1 Complete Reference

| Extension | Purpose | Example |
|-----------|---------|---------|
| `x-ui-order` | Field display order | `["name", "version", "size"]` |
| `x-ui-toggle` | Collapsible section | `true` |
| `x-ui-visible-if` | Conditional visibility | See below |
| `x-ui-overrides-only` | Only in environment overrides | `true` |
| `x-ui-override-disable` | Cannot be overridden per env | `true` |
| `x-ui-secret-ref` | Reference project-level secrets | `true` |
| `x-ui-variable-ref` | Reference project-level variables | `true` |
| `x-ui-output-type` | Dropdown of modules with this output | `"@outputs/s3"` |
| `x-ui-output` | Dropdown of fields of modules with this output | See below |
| `x-ui-placeholder` | Input placeholder text | `"Enter domain"` |
| `x-ui-error-message` | Custom validation error | `"Invalid CIDR"` |
| `x-ui-textarea` | Multi-line text input | `true` |
| `x-ui-yaml-editor` | YAML editor for free-form maps | `true` |
| `x-ui-editor` | Code editor widget | `true` |
| `x-ui-command` | Command array input | `true` |
| `x-ui-typeable` | Allow typing in dropdowns | `true` |
| `x-ui-unique` | Value must be unique | `true` |
| `x-ui-no-sort` | Don't sort enum values | `true` |
| `x-ui-skip` | Skip in UI (internal use) | `true` |
| `x-ui-dynamic-enum` | Options from other fields | `"spec.ports.*.port"` |
| `x-ui-disable-tooltip` | Tooltip when disabled | `"No ports"` |
| `x-ui-artifact` | Attach artifact | `docker_image` |
| `x-ui-array-input-validation` | Validation of item in an array | See below |
| `x-ui-compare` | Cross-field validation | See below |

### 9.2 Critical Extensions for Module Design

**`x-ui-overrides-only`** - Field MUST be set per-environment:
```yaml
region:
  type: string
  title: Deployment Region
  x-ui-overrides-only: true
```

**Use for:** regions, CIDRs, credentials, environment-specific endpoints
**Don't use for:** SKUs, scaling params, access rules (can have safe defaults)

**`x-ui-override-disable`** - Value locked at blueprint level:
```yaml
service_type:
  type: string
  enum: [application, cronjob, job]
  x-ui-override-disable: true
```

**Use for:** service type, fundamental architecture choices, ports

**`x-ui-output-type`** - Dropdown of modules exposing an output type:

This extension renders a dropdown in the UI showing all blueprint resources that expose the specified output type. When the user selects a resource, the UI auto-generates the `${kind.name.out...}` expression.

```yaml
# facets.yaml spec
cert_manager_release:
  type: string                      # String in schema (stores the expression)
  title: Cert Manager Release
  x-ui-output-type: "@facets/helm_release_name"
  x-ui-visible-if:
    field: spec.cert_manager_config.enabled
    values:
      - true
```

**What happens:**
1. UI shows dropdown of all resources exposing `@facets/helm_release_name`
2. User selects `cert-manager` (a helm resource)
3. Field value becomes: `${helm.cert-manager.out.attributes.release_name}`
4. At deployment, expression resolves to actual value

**In variables.tf** - use the resolved object type, not string:
```hcl
# The expression resolves at runtime, so declare the actual type
cert_manager_release = optional(string)  # If it resolves to a simple value
# OR for complex outputs:
s3_bucket = optional(object({
  bucket_name = string
  bucket_arn  = string
}))
```

Works in nested fields and patternProperties.

**`x-ui-output`** - Dropdown of modules exposing an output type:

This extension renders a dropdown in the UI showing field of all blueprint resources that expose the specified output type. 

```yaml
# facets.yaml spec
pubsub:
  title: Topic Name
  description: The topic name of the Pub.Sub
  type: string
  x-ui-output:
    type: @outputs/pubsub
    field: 'attributes.id'
```

**What happens:**
UI shows dropdown of `field` of all resources exposing `@facets/helm_release_name`

Works in nested fields and patternProperties.

**`x-ui-array-input-validation`** - Dropdown of modules exposing an output type:

This extension allows validation to be applied to each item in an array-type field by defining a custom pattern and corresponding error message within the field, which is shown when the pattern validation fails.

```yaml
# facets.yaml spec
times:
  type: array
  items:
    type: string
  x-ui-array-input-validation:
  	pattern: "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"	
  	error: "Invalid time. Please enter a valid time in HH:MM format."
```
**What happens:**
Each item of the array needs to follow the pattern mentioned and failing to do so gives the error mentioned. 

### 9.3 Conditional Visibility

```yaml
readiness_port:
  type: string
  x-ui-visible-if:
    field: spec.health_checks.type
    values:
      - PortCheck
      - HttpCheck
```

**In patternProperties, use `{{this}}` for current key:**
```yaml
custom_tls:
  patternProperties:
    "^[a-zA-Z0-9_-]+$":
      properties:
        certificate:
          x-ui-visible-if:
            field: spec.domains.{{this}}.custom_tls.enabled
            values:
              - true
```

### 9.4 Cross-Field Comparison

```yaml
cpu:
  type: string
  x-ui-compare:
    field: spec.size.cpu_limit
    comparator: "<="
    x-ui-error-message: "CPU cannot exceed limit"
```

---

## 10. Best Practices and Anti-Patterns

### 10.1 DO: Use Maps Instead of Arrays (Critical)

**Arrays should almost never be used in spec schemas.** They don't deep-merge, which breaks environment overrides.

When an environment override is applied:
- **Maps**: Individual keys are merged (change one item, others inherited)
- **Arrays**: Entire array is replaced (must repeat everything to change one item)

```yaml
# BAD - Array (breaks environment overrides)
ports:
  type: array
  items:
    type: object
    properties:
      port: { type: string }

# GOOD - Map with patternProperties (default choice)
ports:
  type: object
  patternProperties:
    "^[a-zA-Z0-9_-]+$":
      type: object
      properties:
        port: { type: string }
```

**Only use arrays when ALL of these are true:**
1. Order of items is semantically significant
2. Items will never need individual overrides per environment
3. The entire list is always replaced as a unit

Examples where arrays are acceptable:
- `command: ["/bin/sh", "-c", "echo hello"]` - order matters, never partially overridden
- `args: ["--config", "/etc/config.yaml"]` - same reason

Examples where maps are required:
- Ports, volumes, environment variables, rules, domains - anything users might override individually

### 10.2 DO: Mark Override-Only Fields Appropriately

```yaml
# Environment-specific - no sensible default
region:
  type: string
  x-ui-overrides-only: true

# Has safe default - can be overridden
instance_size:
  type: string
  default: "small"
  # No x-ui-overrides-only
```

### 10.3 DO: Reuse Output Types

Check existing types before creating new ones:
```bash
raptor get output-type @outputs/postgres -o json
```

### 10.4 DO: Add prevent_destroy for Stateful Resources

```hcl
resource "aws_rds_cluster" "this" {
  # ...
  lifecycle {
    prevent_destroy = true
  }
}
```

### 10.5 DO: Mark Sensitive Outputs

```hcl
output_attributes = {
  api_key = var.api_key
  secrets = ["api_key"]
}

output_interfaces = {
  primary = {
    password = aws_db.password
    secrets  = ["password"]
  }
}
```

### 10.6 DO: Use lookup() with Defaults

```hcl
# GOOD
force_destroy = lookup(var.instance.spec, "force_destroy", false)

# BAD - Never use try()
force_destroy = try(var.instance.spec.force_destroy, false)
```

### 10.7 DON'T: Define Provider Blocks

```hcl
# BAD - Never do this
provider "aws" {
  region = var.region
}

# GOOD - Providers come from inputs automatically
```

### 10.8 DON'T: Use Output Blocks

```hcl
# BAD
output "bucket_name" {
  value = aws_s3_bucket.this.id
}

# GOOD - Use locals only
locals {
  output_attributes = {
    bucket_name = aws_s3_bucket.this.id
  }
}
```

### 10.9 DON'T: Fabricate Sample Values

```yaml
# BAD - fabricating values for fields without defaults
sample:
  spec:
    region: "us-east-1"        # No default defined!
    bucket_name: "my-bucket"   # No default defined!

# GOOD - only include fields with defaults
sample:
  spec:
    versioning_enabled: false  # Has default: false in properties
```

### 10.10 DON'T: Use x-ui-yaml-editor for Structured Data

```yaml
# BAD - loses schema validation and deep merge
ports:
  type: object
  x-ui-yaml-editor: true

# GOOD - proper schema with deep merge
ports:
  type: object
  patternProperties:
    "^[a-zA-Z0-9_-]+$":
      type: object
      properties:
        port: { type: string }
```

---

## 11. Module Lifecycle

### 11.1 Development Workflow

1. **Survey existing output types** in target project type
2. **Design outputs** - what does the module expose? Reuse types where possible
3. **Create output types** only if needed
4. **Write facets.yaml** - spec, inputs, outputs, sample
5. **Write Terraform files** - variables.tf, main.tf, outputs.tf
6. **Validate outputs match schema** before publishing
7. **Upload and test** - dry-run, then preview stage
8. **Publish** when ready

### 11.2 Raptor Commands

**Output Types:**
```bash
# View output type schema
raptor get output-type @namespace/name

# Create/update output type
raptor create output-type @namespace/name -f schema.json
```

**Module Management:**
```bash
# Download existing module for reference
raptor get iac-module <type/flavor/version>
raptor get iac-module <type/flavor/version> -o ./modules/

# Validate module (dry-run)
raptor create iac-module -f <module_dir> --dry-run

# Upload module as PREVIEW
raptor create iac-module -f <module_dir> --auto-create

# Publish to PUBLISHED stage
raptor publish iac-module <type/flavor/version>

# View module details and usages
raptor get iac-module <type/flavor/version> --details
raptor get iac-module <type/flavor/version> --usages

# Delete module
raptor delete iac-module <type/flavor/version>
raptor delete iac-module <type/flavor/version> --force
```

**List Modules:**
```bash
raptor get iac-module                        # List all
raptor get iac-module --source CUSTOM        # Custom modules only
raptor get iac-module --stage PREVIEW        # Preview stage only
```

### 11.3 Testing Workflow

**PREVIEW modules are only available in dedicated testing projects** where unpublished modules can be used.

**Recommended workflow:**

1. **Upload as PREVIEW:**
   ```bash
   raptor create iac-module -f ./my-module --auto-create
   # Module is now in PREVIEW stage
   ```

2. **Test in a testing project:**
   - Add a resource using your module to the testing project's blueprint
   - Run a plan to see Terraform output:
     ```bash
     raptor create release -p testing-project -e dev --plan -w
     ```
   - If plan looks good, deploy:
     ```bash
     raptor create release -p testing-project -e dev -w
     ```

3. **Check release logs for errors:**
   ```bash
   raptor get releases -p testing-project -e dev
   raptor logs release -p testing-project -e dev -f <RELEASE_ID>
   ```

4. **Iterate:** Fix issues, re-upload with `--auto-create`, test again

5. **Publish when ready:**
   ```bash
   raptor publish iac-module <type/flavor/version>
   # Module is now available to all projects
   ```

**Direct publish:** For new modules with low blast radius, you can publish directly:
```bash
raptor create iac-module -f ./my-module --auto-create
raptor publish iac-module <type/flavor/version>
```

**Blueprint commands for testing:**
```bash
# Apply resource to blueprint (validate)
raptor apply -f <resource.yaml> -p <project> --dry-run

# Check environment overrides
raptor get resource-overrides -p <project> -e <env> <kind/name>

# Get runtime outputs after deployment
raptor get resource-outputs -p <project> -e <env> <kind/name>
```

### 11.4 Versioning Strategy

- **Patch (1.0.x)**: Bug fixes, documentation
- **Minor (1.x.0)**: New optional features, non-breaking changes
- **Major (x.0.0)**: Breaking changes to spec or outputs

---

## 12. Complete Examples

### 12.1 Cloud Account Module (Provider Source)

A module that provides cloud provider configuration.

**facets.yaml:**
```yaml
intent: cloud_account
flavor: ovh
version: "1.0.0"
description: Configures OVH Terraform provider with application key authentication
clouds:
  - kubernetes

spec:
  title: OVH Provider Configuration
  description: Configure OVH API access credentials
  type: object
  properties:
    endpoint:
      type: string
      title: OVH API Endpoint
      enum:
        - ovh-eu
        - ovh-ca
      default: ovh-eu
      x-ui-overrides-only: true
    application_key:
      type: string
      title: Application Key
      x-ui-secret-ref: true
    application_secret:
      type: string
      title: Application Secret
      x-ui-secret-ref: true
    consumer_key:
      type: string
      title: Consumer Key
      x-ui-secret-ref: true
    project_id:
      type: string
      title: Cloud Project ID
      x-ui-overrides-only: true
  required:
    - endpoint
    - application_key
    - application_secret
    - consumer_key
    - project_id

outputs:
  default:
    type: "@facets/ovh-provider"
    title: OVH Provider Configuration
    providers:
      ovh:
        source: ovh/ovh
        version: 2.7.0
        attributes:
          endpoint: attributes.endpoint
          application_key: attributes.application_key
          application_secret: attributes.application_secret
          consumer_key: attributes.consumer_key

sample:
  kind: cloud_account
  flavor: ovh
  version: "1.0.0"
  disabled: false
  spec:
    endpoint: ovh-eu
```

**variables.tf:**
```hcl
variable "instance" {
  type = object({
    kind    = string
    flavor  = string
    version = string
    spec = object({
      endpoint           = string
      application_key    = string
      application_secret = string
      consumer_key       = string
      project_id         = string
    })
  })
}

variable "instance_name" {
  type = string
}

variable "environment" {
  type = object({
    name        = string
    unique_name = string
  })
}

variable "inputs" {
  type = object({})
}
```

**main.tf:**
```hcl
# Cloud account is a provider-only module
# No resources to create - just passes through configuration
```

**outputs.tf:**
```hcl
locals {
  output_attributes = {
    endpoint           = var.instance.spec.endpoint
    application_key    = var.instance.spec.application_key
    application_secret = var.instance.spec.application_secret
    consumer_key       = var.instance.spec.consumer_key
    project_id         = var.instance.spec.project_id
    secrets            = ["application_key", "application_secret", "consumer_key"]
  }
  output_interfaces = {}
}
```

### 12.2 Database Module (PostgreSQL)

A module with inputs (dependencies) and standard outputs.

**facets.yaml:**
```yaml
intent: postgres
flavor: ovh
version: "1.0"
description: Creates managed PostgreSQL database on OVH Cloud
clouds:
  - kubernetes

inputs:
  ovh_provider:
    type: "@facets/ovh-provider"
    optional: false
    displayName: OVH Provider
    providers:
      - ovh
  network:
    type: "@facets/ovh-network"
    optional: false
    displayName: OVH Network

outputs:
  default:
    type: "@outputs/postgres"
    title: PostgreSQL Database

spec:
  title: PostgreSQL Configuration
  type: object
  properties:
    version:
      type: string
      title: PostgreSQL Version
      enum: ["14", "15", "16"]
      default: "15"
    plan:
      type: string
      title: Service Plan
      enum: [essential, business, enterprise]
      default: essential
    flavor:
      type: string
      title: Instance Size
      enum: [db1-4, db1-7, db1-15, db1-30]
      default: db1-4
    nodes_count:
      type: integer
      title: Number of Nodes
      minimum: 1
      maximum: 10
      default: 1
    disk_size:
      type: integer
      title: Disk Size (GB)
      minimum: 20
      maximum: 2000
      default: 80
  required:
    - version
    - plan
    - flavor
    - nodes_count
    - disk_size
  x-ui-order:
    - version
    - plan
    - flavor
    - nodes_count
    - disk_size

sample:
  kind: postgres
  flavor: ovh
  version: "1.0"
  disabled: false
  spec:
    version: "15"
    plan: essential
    flavor: db1-4
    nodes_count: 1
    disk_size: 80
```

**variables.tf:**
```hcl
variable "instance" {
  type = object({
    kind    = string
    flavor  = string
    version = string
    spec = object({
      version     = string
      plan        = string
      flavor      = string
      nodes_count = number
      disk_size   = number
    })
  })

  validation {
    condition     = contains(["14", "15", "16"], var.instance.spec.version)
    error_message = "Version must be 14, 15, or 16."
  }
}

variable "instance_name" {
  type = string
}

variable "environment" {
  type = object({
    name        = string
    unique_name = string
  })
}

variable "inputs" {
  type = object({
    ovh_provider = object({
      attributes = object({
        project_id = string
      })
    })
    network = object({
      attributes = object({
        region               = string
        openstack_network_id = string
        db_subnet_id         = string
        network_cidr         = string
      })
    })
  })
}
```

**main.tf:**
```hcl
locals {
  region        = replace(var.inputs.network.attributes.region, "/[0-9]+$/", "")
  database_name = "${var.environment.unique_name}-${var.instance_name}"
}

resource "ovh_cloud_project_database" "postgres" {
  service_name = var.inputs.ovh_provider.attributes.project_id
  description  = "PostgreSQL: ${local.database_name}"
  engine       = "postgresql"
  version      = var.instance.spec.version
  plan         = var.instance.spec.plan
  flavor       = var.instance.spec.flavor
  disk_size    = var.instance.spec.disk_size

  nodes {
    region     = local.region
    network_id = var.inputs.network.attributes.openstack_network_id
    subnet_id  = var.inputs.network.attributes.db_subnet_id
  }

  ip_restrictions {
    description = "Private network only"
    ip          = var.inputs.network.attributes.network_cidr
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "ovh_cloud_project_database_postgresql_user" "admin" {
  service_name = var.inputs.ovh_provider.attributes.project_id
  cluster_id   = ovh_cloud_project_database.postgres.id
  name         = "admin"
}
```

**outputs.tf:**
```hcl
locals {
  output_attributes = {
    database_id   = ovh_cloud_project_database.postgres.id
    database_name = "defaultdb"
    engine        = "postgresql"
    version       = var.instance.spec.version
    host          = ovh_cloud_project_database.postgres.endpoints[0].domain
    port          = tostring(ovh_cloud_project_database.postgres.endpoints[0].port)
  }

  # interfaces: endpoint_name → connection details
  output_interfaces = {
    primary = {  # Read-write endpoint (could also be named "writer")
      host              = ovh_cloud_project_database.postgres.endpoints[0].domain
      port              = tostring(ovh_cloud_project_database.postgres.endpoints[0].port)
      username          = ovh_cloud_project_database_postgresql_user.admin.name
      password          = ovh_cloud_project_database_postgresql_user.admin.password
      connection_string = format(
        "postgresql://%s:%s@%s:%d/defaultdb",
        ovh_cloud_project_database_postgresql_user.admin.name,
        ovh_cloud_project_database_postgresql_user.admin.password,
        ovh_cloud_project_database.postgres.endpoints[0].domain,
        ovh_cloud_project_database.postgres.endpoints[0].port
      )
      secrets = ["password", "connection_string"]
    }
    readonly = {  # Read-only endpoint (could also be named "reader")
      host              = ovh_cloud_project_database.postgres.endpoints[0].domain
      port              = tostring(ovh_cloud_project_database.postgres.endpoints[0].port)
      username          = ovh_cloud_project_database_postgresql_user.admin.name
      password          = ovh_cloud_project_database_postgresql_user.admin.password
      connection_string = format(
        "postgresql://%s:%s@%s:%d/defaultdb",
        ovh_cloud_project_database_postgresql_user.admin.name,
        ovh_cloud_project_database_postgresql_user.admin.password,
        ovh_cloud_project_database.postgres.endpoints[0].domain,
        ovh_cloud_project_database.postgres.endpoints[0].port
      )
      secrets = ["password", "connection_string"]
    }
  }
}
```

### 12.3 Kubernetes Cluster Module (Provider Exposer)

A module that exposes kubernetes and helm providers.

**facets.yaml:**
```yaml
intent: kubernetes_cluster
flavor: ovh
version: "1.0"
description: Creates OVH Managed Kubernetes cluster
clouds:
  - kubernetes

inputs:
  ovh_provider:
    type: "@facets/ovh-provider"
    optional: false
    displayName: OVH Provider
    providers:
      - ovh
  network:
    type: "@facets/ovh-network"
    optional: false
    displayName: OVH Network

outputs:
  default:
    type: "@facets/ovh-kubernetes"
    title: OVH Kubernetes Cluster
    providers:
      kubernetes:
        source: hashicorp/kubernetes
        version: 2.23.0
        attributes:
          host: attributes.cluster_endpoint
          cluster_ca_certificate: attributes.cluster_ca_certificate
          client_certificate: attributes.client_certificate
          client_key: attributes.client_key
      helm:
        source: hashicorp/helm
        version: 2.11.0
        attributes:
          kubernetes:
            host: attributes.cluster_endpoint
            cluster_ca_certificate: attributes.cluster_ca_certificate
            client_certificate: attributes.client_certificate
            client_key: attributes.client_key

spec:
  title: Kubernetes Cluster Configuration
  type: object
  properties:
    version:
      type: string
      title: Kubernetes Version
      default: "1.28"
    node_pool:
      type: object
      title: Default Node Pool
      x-ui-overrides-only: true
      properties:
        flavor:
          type: string
          title: Node Flavor
          default: b3-8
        min_nodes:
          type: integer
          default: 3
        max_nodes:
          type: integer
          default: 10
  x-ui-order:
    - version
    - node_pool

sample:
  kind: kubernetes_cluster
  flavor: ovh
  version: "1.0"
  disabled: false
  spec:
    version: "1.28"
```

**outputs.tf:**
```hcl
locals {
  output_attributes = {
    cluster_id             = ovh_cloud_project_kube.cluster.id
    cluster_endpoint       = ovh_cloud_project_kube.cluster.kubeconfig_attributes[0].host
    cluster_ca_certificate = base64decode(ovh_cloud_project_kube.cluster.kubeconfig_attributes[0].cluster_ca_certificate)
    client_certificate     = base64decode(ovh_cloud_project_kube.cluster.kubeconfig_attributes[0].client_certificate)
    client_key             = base64decode(ovh_cloud_project_kube.cluster.kubeconfig_attributes[0].client_key)
    secrets                = ["client_key"]
  }
  output_interfaces = {}
}
```

---

## 13. Quick Reference

### Module Checklist

- [ ] `facets.yaml` with intent, flavor, version (quoted), description
- [ ] `spec` with properties, required, x-ui-order
- [ ] `inputs` for all dependencies with correct types
- [ ] `outputs` with `default` and correct type
- [ ] `sample` with only defaulted fields
- [ ] `variables.tf` with instance, instance_name, environment, inputs
- [ ] `main.tf` with resources, `prevent_destroy` for stateful
- [ ] `outputs.tf` with `output_attributes` and `output_interfaces` locals
- [ ] NO provider blocks, NO provider versions, NO output blocks
- [ ] Output type schema matches `output_attributes`/`output_interfaces`

### Common x-ui Extensions

```yaml
x-ui-overrides-only: true      # Must set per environment
x-ui-override-disable: true    # Cannot change per environment
x-ui-secret-ref: true          # Reference secrets
x-ui-variable-ref: true        # Reference variables
x-ui-output-type: "@type"      # Module dropdown
x-ui-toggle: true              # Collapsible section
x-ui-yaml-editor: true         # Free-form key-value only
x-ui-visible-if:               # Conditional display
  field: spec.type
  values: [value1, value2]
```

### Key Rules Summary

| Rule | Details |
|------|---------|
| Terraform version | v1.5.7 or OpenTofu (pre-license change) |
| Provider blocks | Never define - come from inputs |
| Provider versions | Never constrain - defined in output types |
| Output blocks | Never use - only locals |
| Arrays in spec | Almost never use - maps (patternProperties) are default |
| Stateful resources | Always add `prevent_destroy = true` |
| try() function | Never use - use `lookup()` with defaults |
| Sample values | Only include fields with defaults defined |

### Raptor Commands

```bash
# Output types
raptor get output-type @namespace/name
raptor create output-type @namespace/name -f schema.json

# Modules
raptor get iac-module type/flavor/version
raptor create iac-module -f . --dry-run        # Validate
raptor create iac-module -f . --auto-create    # Upload
raptor publish iac-module type/flavor/version  # Publish
raptor delete iac-module type/flavor/version

# Project types
raptor get project-types
raptor create project-type NAME --description "Description"
raptor get resource-type-mappings PROJECT_TYPE
raptor create resource-type-mapping PROJECT_TYPE --resource-type type/flavor

# Testing
raptor apply -f resource.yaml -p project --dry-run
raptor create release -p project -e env --plan -w
```
