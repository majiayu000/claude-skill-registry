---
name: developing-stacks
description: >-
  Use when deploying components via Atmos stacks, configuring stack YAML, or understanding inheritance patterns. Covers
  catalog defaults, abstract components, stack imports, and how to wire components into target stacks.
---

# Developing Stacks

> **Scope:** This skill is specific to the **acme** infrastructure repository. It documents the
> stack structure, naming conventions, and deployment patterns used here. For generic component development, see
> `developing-components`.

Guide for configuring Atmos stacks to deploy Terraform components across environments.

## Stack Architecture Overview

This repository uses a multi-tenant, multi-stage stack structure:

```
stacks/
├── orgs/acme/                         # Organization root (namespace: acme)
│   ├── _defaults.yaml                # Org-wide defaults (namespace, backend, account_map)
│   ├── core/                         # Core tenant (shared infrastructure)
│   │   ├── _defaults.yaml            # Tenant defaults (tenant: core)
│   │   ├── root/                     # Root account stage
│   │   │   ├── _defaults.yaml        # Stage defaults + auth identity
│   │   │   └── global-region/        # Global region (us-east-1)
│   │   │       └── foundation.yaml
│   │   ├── auto/                     # Automation account
│   │   ├── artifacts/                # Artifacts account (ECR, S3)
│   │   ├── audit/                    # Audit/logging account
│   │   ├── dns/                      # DNS account
│   │   ├── network/                  # Network account (TGW, VPN)
│   │   └── security/                 # Security account
│   └── plat/                         # Platform tenant (workloads)
│       ├── _defaults.yaml            # Tenant defaults (tenant: plat)
│       ├── dev/                      # Dev stage
│       │   ├── _defaults.yaml        # Stage defaults + auth identity
│       │   ├── global-region/        # Global resources (IAM)
│       │   │   └── foundation.yaml
│       │   └── us-east-1/              # Primary region
│       │       ├── foundation.yaml   # VPC, networking
│       │       ├── platform.yaml     # ECS/EKS, databases
│       │       └── app.yaml          # Application resources
│       ├── staging/                  # Staging stage
│       ├── prod/                     # Production stage
│       └── sandbox/                  # Sandbox stage
├── catalog/                          # Component defaults library
│   ├── vpc/defaults.yaml
│   ├── ecs/defaults.yaml
│   ├── eks/cluster/defaults.yaml
│   └── ...
└── mixins/                           # Reusable fragments
    ├── region/us-east-1.yaml
    └── stage/dev.yaml
```

**Stack name format:** `{namespace}-{tenant}-{region_short}-{stage}`

Examples for this repository:
- `acme-core-use1-root` - Core root account in us-east-1
- `acme-plat-use1-dev` - Platform dev in us-east-1
- `acme-plat-use1-prod` - Platform prod in us-east-1

## Core Patterns

### 1. Catalog Defaults (Recommended Starting Point)

Define component defaults in `stacks/catalog/<component>/defaults.yaml`. These are imported into target stacks.

```yaml
# stacks/catalog/vpc/defaults.yaml
components:
  terraform:
    vpc/defaults:
      metadata:
        type: abstract # Prevents direct deployment
      vars:
        name: vpc
        availability_zones: ["a", "b", "c"]
        public_subnets_enabled: true
        nat_gateway_enabled: true
        max_subnet_count: 3
```

**Key points:**

- Use `type: abstract` to prevent accidental deployment of the base configuration
- Name the component with a `/defaults` suffix (e.g., `vpc/defaults`) to indicate it's a base
- Define sensible defaults that work across most environments

### 2. Inheriting into Target Stacks

Import the catalog and inherit from the abstract component in your target stack:

```yaml
# stacks/orgs/acme/plat/dev/us-east-1/foundation.yaml
import:
  - orgs/acme/plat/dev/_defaults
  - mixins/region/us-east-1
  - catalog/vpc/defaults

components:
  terraform:
    vpc:
      metadata:
        component: vpc # Points to components/terraform/vpc
        inherits:
          - vpc/defaults # Inherits from the abstract component
      vars:
        ipv4_primary_cidr_block: 10.2.0.0/16 # Dev environment CIDR
```

**Inheritance merging:**

- `vars`, `settings`, `env`, `backend` are deep-merged
- Later values override earlier ones
- The component's own `vars` override inherited `vars`

### 3. Abstract Components

Abstract components (`type: abstract`) serve as base configurations that cannot be deployed directly.

```yaml
# Abstract - cannot be deployed
vpc/defaults:
  metadata:
    type: abstract
  vars:
    nat_gateway_enabled: true

# Real - can be deployed (inherits from abstract)
vpc:
  metadata:
    component: vpc
    inherits:
      - vpc/defaults
  vars:
    ipv4_primary_cidr_block: 10.0.0.0/16
```

**Use abstract components when:**

- Creating reusable base configurations
- Defining organization-wide defaults
- Building component "archetypes" (e.g., `s3-bucket/logging`, `s3-bucket/public`)

### 4. Multiple Inheritance

Components can inherit from multiple bases. Order matters - later items override earlier ones.

```yaml
components:
  terraform:
    my-ecs-service:
      metadata:
        component: ecs-service
        inherits:
          - ecs-service/defaults # Base defaults
          - ecs-service/web # Web-specific settings (overrides defaults)
      vars:
        service_name: my-app # Final override
```

### 5. Stack Defaults Hierarchy

The `_defaults.yaml` files create an inheritance chain:

```yaml
# stacks/orgs/acme/_defaults.yaml (org level)
vars:
  namespace: acme
terraform:
  backend_type: s3
  backend:
    s3:
      bucket: acme-core-use1-root-tfstate
      # ...

# stacks/orgs/acme/plat/_defaults.yaml (tenant level)
import:
  - orgs/acme/_defaults
vars:
  tenant: plat

# stacks/orgs/acme/plat/dev/_defaults.yaml (stage level)
import:
  - orgs/acme/plat/_defaults
  - mixins/stage/dev
auth:
  identities:
    plat-dev/terraform:
      default: true
```

## Deploying a Component

### Step 1: Check if Catalog Defaults Exist

```bash
ls stacks/catalog/<component>/
```

If defaults exist, skip to Step 3.

### Step 2: Create Catalog Defaults (if needed)

```yaml
# stacks/catalog/<component>/defaults.yaml
components:
  terraform:
    <component>/defaults:
      metadata:
        type: abstract
      vars:
        enabled: true
        # Add sensible defaults
```

### Step 3: Add to Target Stack

Edit the appropriate stack file (foundation.yaml, platform.yaml, app.yaml, etc.):

```yaml
import:
  # ... existing imports
  - catalog/<component>/defaults # Add this

components:
  terraform:
    <component>:
      metadata:
        component: <component>
        inherits:
          - <component>/defaults
      vars:
        # Environment-specific overrides only
```

### Step 4: Validate and Plan

```bash
# Validate the stack configuration
atmos validate stacks

# See the resolved configuration (example for dev)
atmos describe component <component> -s acme-plat-use1-dev

# Plan the deployment
atmos terraform plan <component> -s acme-plat-use1-dev
```

## Stack File Organization

Stack files are organized by layer:

| File              | Purpose                                  | Examples                    |
| ----------------- | ---------------------------------------- | --------------------------- |
| `foundation.yaml` | Core infrastructure (VPC, DNS, TGW)      | vpc, dns-delegated, bastion |
| `platform.yaml`   | Platform services (ECS, RDS, monitoring) | ecs, aurora-postgres, alb   |
| `app.yaml`        | Application-specific resources           | ecs-service, s3-bucket      |
| `network.yaml`    | Network-specific (routes, peering)       | vpc-routes, tgw-attachment  |
| `monitor.yaml`    | Observability (CloudWatch, Grafana)      | managed-grafana, alarms     |

## Common Patterns

### Catalog Organization for Multiple Purposes

When deploying multiple instances of the same component for different purposes, organize the catalog with abstract
defaults and purpose-specific files that inherit from them:

```
stacks/catalog/
└── <component>/
    ├── defaults.yaml    # Abstract base component (not deployed directly)
    └── <purpose>.yaml   # Purpose-specific configuration
```

**Abstract defaults file** (`stacks/catalog/<component>/defaults.yaml`):

```yaml
components:
  terraform:
    <component>/defaults:
      metadata:
        type: abstract # Not deployed directly
        component: <component> # Points to Terraform component
      vars:
        enabled: true
        # Organization-wide defaults for this component
```

**Purpose-specific catalog file** (`stacks/catalog/<component>/<purpose>.yaml`):

```yaml
import:
  - catalog/<component>/defaults

components:
  terraform:
    <component>/<purpose>:
      metadata:
        component: <component> # Points to Terraform component
        inherits:
          - <component>/defaults # Inherits from abstract component
      vars:
        # Only include values that differ from defaults (keep it DRY)
        name: <purpose>-specific-name
        some_setting: override-value # Overrides default
```

**Import in target stack:**

```yaml
import:
  - catalog/<component>/<purpose>
```

**Deploy:**

```bash
atmos terraform plan <component>/<purpose> -s acme-plat-use1-dev
```

### Environment-Specific CIDR Blocks

```yaml
# stacks/catalog/vpc/defaults.yaml
components:
  terraform:
    vpc/defaults:
      metadata:
        type: abstract
      vars:
        # No CIDR here - must be specified per environment

# stacks/orgs/acme/plat/dev/us-east-1/foundation.yaml
components:
  terraform:
    vpc:
      metadata:
        inherits: [vpc/defaults]
      vars:
        ipv4_primary_cidr_block: 10.2.0.0/16

# stacks/orgs/acme/plat/prod/us-east-1/foundation.yaml
components:
  terraform:
    vpc:
      metadata:
        inherits: [vpc/defaults]
      vars:
        ipv4_primary_cidr_block: 10.0.0.0/16
```

### Cross-Component Dependencies

Use `!terraform.state` to wire outputs between components:

```yaml
# stacks/catalog/ecs/defaults.yaml
components:
  terraform:
    ecs/defaults:
      metadata:
        type: abstract
      vars:
        vpc_id: !terraform.state vpc vpc_id
        subnet_ids: !terraform.state vpc private_subnet_ids
```

See the `atmos-functions` skill for more details.

### Multiple Instances of a Component

Deploy multiple instances by using different component names:

```yaml
components:
  terraform:
    # Primary VPC
    vpc:
      metadata:
        component: vpc
        inherits: [vpc/defaults]
      vars:
        ipv4_primary_cidr_block: 10.0.0.0/16

    # Secondary VPC for isolation
    vpc/isolated:
      metadata:
        component: vpc
        inherits: [vpc/defaults]
      vars:
        name: vpc-isolated
        ipv4_primary_cidr_block: 10.100.0.0/16
```

## Debugging Stack Configuration

```bash
# See fully resolved configuration
atmos describe component <component> -s acme-plat-use1-dev

# See all components in a stack
atmos describe stacks -s acme-plat-use1-dev

# Validate all stacks
atmos validate stacks
```

For more debugging techniques, see the `debugging-atmos` skill.

## References

- [Atmos Design Patterns](https://atmos.tools/design-patterns/)
- [Component Catalog Pattern](https://atmos.tools/design-patterns/component-catalog)
- [Stack Inheritance](https://atmos.tools/core-concepts/stacks/inheritance)
