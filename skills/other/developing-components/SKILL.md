---
name: developing-components
description:
  Use when creating new Terraform/OpenTofu components or modifying existing ones. Covers required files, catalog
  defaults, stack configuration, and naming conventions.
---

# Developing Components

> **Scope:** This skill is generic and applies to any Cloud Posse reference architecture project. It covers patterns for
> vendoring and creating Terraform components that are consistent across all customers.

Components are opinionated Terraform root modules that implement a specific AWS resource with predefined conventions.

## Before Creating a New Component

**Always check for existing components first.** Creating new components adds maintenance burden.

### 1. Check Local Components

```bash
ls components/terraform/
```

Many use cases can be solved by configuring existing generic components via catalog:

- **`iam-role`** - Any IAM role. Create `stacks/catalog/iam-role/my-role.yaml` instead of a new component.
- **`s3-bucket`** - Any S3 bucket with standard configurations.
- **`lambda`** - Lambda functions with common patterns.

### 2. Check Cloud Posse Component Library

Browse https://docs.cloudposse.com/components/library/ for pre-built components. Common ones:

- `eks/cluster`, `eks/alb-controller` - Kubernetes
- `aurora-postgres`, `rds` - Databases
- `elasticache-redis` - Caching
- `ecs`, `ecs-service` - Container workloads
- `s3-bucket`, `dynamodb`, `sqs-queue` - Storage and messaging
- `cloudwatch-logs`, `sns-topic` - Monitoring and notifications

#### Cloud Posse Component Sources

| Resource               | Location                                                   |
| ---------------------- | ---------------------------------------------------------- |
| Component Library Docs | https://docs.cloudposse.com/components/library/            |
| Component Repositories | `github.com/cloudposse-terraform-components/aws-<service>` |
| Mixins Repository      | `github.com/cloudposse-terraform-components/mixins`        |

**Find latest version:**

```bash
gh release view --repo cloudposse-terraform-components/aws-<component> --json tagName
```

#### Vendoring a Cloud Posse Component

1. Create the component directory and `component.yaml`:

```bash
mkdir -p components/terraform/<component-name>
```

2. Create `components/terraform/<component-name>/component.yaml`:

<!-- prettier-ignore-start -->

```yaml
apiVersion: atmos/v1
kind: ComponentVendorConfig
spec:
  source:
    uri: github.com/cloudposse-terraform-components/aws-<component>.git//src?ref={{ .Version }}
    version: <latest-version>  # Use gh release view to find this
    included_paths:
      - "**/**"
    excluded_paths:
      - "providers.tf"
  mixins:
    # Use provider mixin without account-map dependency (for single-account deployments)
    - uri: https://raw.githubusercontent.com/cloudposse-terraform-components/mixins/{{ .Version }}/src/mixins/provider-without-account-map.tf
      version: v0.3.2
      filename: providers.tf
```

<!-- prettier-ignore-end -->

3. Pull the component:

```bash
atmos vendor pull -c <component-name>
```

### 3. When to Create a Custom Component

Create a new component when:

- **Tightly coupled resources** - The resources share the same lifecycle and must be created/destroyed together. For
  example, an application-specific ECS service with its ALB target group, CloudWatch alarms, and autoscaling policies.
- **Unique to your infrastructure** - The configuration is specific to your organization and wouldn't benefit from Cloud
  Posse's generic abstractions.
- **Single account/region deployment** - All resources deploy to one AWS account and region. If resources span accounts
  or regions, split into separate components.

**Teralithic components** (all-in-one) are appropriate when:

- Resources are always deployed together and never independently
- Splitting would create artificial boundaries requiring complex cross-component wiring
- The blast radius is acceptable (all resources affected by any change)

**Avoid** custom components when:

- You're wrapping a single AWS resource (use generic components instead)
- The resources have different lifecycles (e.g., database vs. application)
- You might reuse this pattern elsewhere (vendor or create a generic component)

---

## New Component Structure

Every new component requires three parts:

## 1. Root Module (`components/terraform/<component-name>/`)

Required files (copy from an existing component like `ecs`):

- **`context.tf`** - Always identical across all components. Copy from any existing component. Provides Cloud Posse's
  null-label context for consistent naming.
- **`providers.tf`** - Standard provider configuration. Copy from an existing component. Includes the
  `account_map_enabled` variable and dummy `iam_roles` module for compatibility.
- **`versions.tf`** - OpenTofu/Terraform and provider version constraints
- **`variables.tf`** - Component-specific input variables
- **`main.tf`** - Main resource definitions
- **`outputs.tf`** - Output values

**Note on remote-state.tf**: Avoid creating `remote-state.tf` files for new components. Instead, use Atmos functions
(`!terraform.state`) in stack YAML to pass values from other components. This keeps components simpler and moves
cross-component wiring to the stack configuration layer.

## 2. Catalog Defaults (`stacks/catalog/<component-name>/defaults.yaml`)

Define organization-wide default values for the component, including dependency lookups:

```yaml
components:
  terraform:
    <component-name>/defaults:
      metadata:
        component: <component-name>
        type: abstract # Makes this a base configuration, not directly deployable
      vars:
        enabled: true
        name: <component-name>
        # Static defaults
        some_setting: "default-value"
        # Dynamic lookups - resolved at plan time based on current stack
        vpc_id: !terraform.state vpc vpc_id
        subnet_ids: !terraform.state vpc private_subnet_ids
```

## 3. Stack Configuration (`stacks/orgs/acme/<tenant>/<stage>/<region>/<layer>.yaml`)

Import the catalog - often no component block is needed if catalog defaults are complete:

```yaml
import:
  - orgs/acme/plat/dev/_defaults
  - mixins/region/us-east-1
  - catalog/<component-name>/defaults
```

If overrides are needed:

```yaml
import:
  - catalog/<component-name>/defaults

components:
  terraform:
    <component-name>:
      vars:
        # Account/region-specific overrides only
        some_setting: "override-value"
```

## Naming Conventions

- Use descriptive, specific names that indicate the component's purpose
- Prefix with the service/platform when specific (e.g., `ecs-adot-collector` not just `adot-collector`)
- Use slashes for component hierarchies in catalogs (e.g., `iam-role/grafana-cloudwatch-access`,
  `grafana/datasource/cloudwatch`)

## Stack File Organization

Stack files in `stacks/orgs/acme/` mirror the AWS account structure:

- `orgs/acme/core/` - Core accounts (root, audit, security, identity, network, dns, auto, artifacts)
- `orgs/acme/plat/` - Platform accounts (sandbox, dev, staging, prod)

Within each stage, organized by region:

- `global-region/` - Global (us-east-1) resources like IAM
- `us-east-2/` - Regional resources

Regional stack files are typically split by layer:

- `foundation.yaml` - VPC, networking, base infrastructure
- `platform.yaml` - Shared platform services (ECS clusters, databases)
- `app.yaml` - Application-specific resources
