---
name: resource-tagging
description: Apply and enforce cloud resource tagging strategies across AWS, Azure, GCP, and Kubernetes for cost allocation, ownership tracking, compliance, and automation. Use when implementing cloud governance, optimizing costs, or automating infrastructure management.
---

# Resource Tagging

Apply comprehensive cloud resource tagging strategies to enable cost allocation, ownership tracking, compliance enforcement, and infrastructure automation across multi-cloud environments.

## Purpose

Resource tagging provides the foundational metadata layer for cloud governance. Tags enable precise cost allocation (reducing unallocated spend by up to 80%), rapid ownership identification, compliance scope definition, and automated lifecycle management. Without proper tagging, cloud costs become untrackable, security incidents lack context, and automation policies fail to target resources effectively.

## When to Use

Use resource tagging when:

- Implementing cloud governance frameworks for cost allocation and accountability
- Building FinOps practices requiring spend visibility by team, project, or department
- Enforcing compliance requirements (PCI, HIPAA, SOC2) through automated policies
- Setting up automated resource lifecycle management (backup, monitoring, shutdown)
- Managing multi-tenant or multi-project cloud environments
- Implementing disaster recovery and backup policies based on criticality
- Tracking resource ownership for security incident response
- Optimizing cloud costs through spend analysis and showback/chargeback

## Minimum Viable Tagging Strategy

Start with the **"Big Six"** required tags for all cloud resources:

| Tag | Purpose | Example Value |
|-----|---------|---------------|
| **Name** | Human-readable identifier | `prod-api-server-01` |
| **Environment** | Lifecycle stage | `prod` \| `staging` \| `dev` |
| **Owner** | Responsible team contact | `platform-team@company.com` |
| **CostCenter** | Finance code for billing | `CC-1234` |
| **Project** | Business initiative | `ecommerce-platform` |
| **ManagedBy** | Resource creation method | `terraform` \| `pulumi` \| `manual` |

**Optional tags** to add based on specific needs:

- **Application**: Multi-app projects requiring app-level isolation
- **Component**: Resource role (`web`, `api`, `database`, `cache`)
- **Backup**: Backup policy (`daily`, `weekly`, `none`)
- **Compliance**: Regulatory scope (`PCI`, `HIPAA`, `SOC2`)
- **SLA**: Service level (`critical`, `high`, `medium`, `low`)

## Tag Naming Conventions

Choose ONE naming convention organization-wide and enforce consistently:

| Convention | Format | Example | Best For |
|------------|--------|---------|----------|
| **PascalCase** | `CostCenter`, `ProjectName` | AWS standard | AWS-first orgs |
| **lowercase** | `costcenter`, `project` | GCP labels (required) | GCP-first orgs |
| **kebab-case** | `cost-center`, `project-name` | Azure (case-insensitive) | Azure-first orgs |
| **Namespaced** | `company:environment`, `team:owner` | Multi-org tag policies | Large enterprises |

**Critical:** Case sensitivity varies by provider:
- **AWS**: Case-sensitive (`Environment` ≠ `environment`)
- **Azure**: Case-insensitive (`Environment` = `environment`)
- **GCP**: Lowercase required (`environment` only)
- **Kubernetes**: Case-sensitive (`environment` ≠ `Environment`)

## Tag Categories

For detailed taxonomy of all tag categories, see `references/tag-taxonomy.md`.

### Technical Tags
Operations-focused metadata: Name, Environment, Version, ManagedBy

### Business Tags
Cost allocation metadata: Owner, CostCenter, Project, Department

### Security Tags
Compliance metadata: Confidentiality, Compliance, DataClassification, SecurityZone

### Automation Tags
Lifecycle metadata: Backup, Monitoring, Schedule, AutoShutdown

### Operational Tags
Support metadata: SLA, ChangeManagement, CreatedBy, CreatedDate

### Custom Tags
Organization-specific metadata: Customer, Application, Component, Stack

## Cloud Provider Tag Limits

| Provider | Tag Limit | Key Length | Value Length | Case Sensitive | Inheritance |
|----------|-----------|------------|--------------|----------------|-------------|
| **AWS** | 50 user-defined | 128 chars | 256 chars | Yes | Via tag policies |
| **Azure** | 50 pairs | 512 chars | 256 chars | No | Via Azure Policy |
| **GCP** | 64 labels | 63 chars | 63 chars | No | Via org policies |
| **Kubernetes** | Unlimited | 253 prefix + 63 name | 63 chars | Yes | Via namespace |

## Tag Enforcement Patterns

### Infrastructure as Code (Recommended)

Apply tags automatically via Terraform/Pulumi to reduce manual errors by 95%:

```hcl
# Terraform: Provider-level default tags
provider "aws" {
  default_tags {
    tags = {
      Environment = var.environment
      Owner       = var.owner
      CostCenter  = var.cost_center
      Project     = var.project
      ManagedBy   = "terraform"
    }
  }
}
```

All resources automatically inherit these tags. Resource-specific tags merge with defaults.

For complete Terraform, Pulumi, and CloudFormation examples, see `examples/terraform/`, `examples/pulumi/`, and `examples/cloudformation/`.

### Policy-Based Enforcement

Enforce tagging at resource creation time:

**AWS**: Use AWS Config rules to check tag compliance (alert or deny)
**Azure**: Use Azure Policy for tag inheritance and enforcement
**GCP**: Use Organization Policies to restrict label values
**Kubernetes**: Use OPA Gatekeeper or Kyverno for admission control

For enforcement implementation patterns, see `references/enforcement-patterns.md`.

### Tag Compliance Auditing

Run regular audits (weekly recommended) to identify untagged resources:

**AWS Config Query** (SQL):
```sql
SELECT resourceId, resourceType, configuration.tags
WHERE resourceType IN ('AWS::EC2::Instance', 'AWS::RDS::DBInstance')
  AND (configuration.tags IS NULL OR NOT configuration.tags.Environment EXISTS)
```

**Azure Resource Graph Query** (KQL):
```kusto
Resources
| where type in~ ('microsoft.compute/virtualmachines')
| where isnull(tags.Environment) or isnull(tags.Owner)
| project name, type, resourceGroup, tags
```

**GCP Cloud Asset Inventory**:
```bash
gcloud asset search-all-resources \
  --query="NOT labels:environment OR NOT labels:owner" \
  --format="table(name,assetType,labels)"
```

For complete audit queries and scripts, see `references/compliance-auditing.md` and `scripts/audit_tags.py`.

## Cost Allocation with Tags

Enable cost allocation tags to track spending by team, project, or department:

### AWS Cost Explorer

Activate cost allocation tags (up to 24 hours for activation):

```hcl
# Enable cost allocation tags via Terraform
resource "aws_ce_cost_allocation_tag" "environment" {
  tag_key = "Environment"
  status  = "Active"
}

resource "aws_ce_cost_allocation_tag" "project" {
  tag_key = "Project"
  status  = "Active"
}
```

Set up cost anomaly detection by tag to catch unusual spending:

```hcl
resource "aws_ce_anomaly_monitor" "project_monitor" {
  name         = "project-cost-monitor"
  monitor_type = "DIMENSIONAL"

  monitor_specification = jsonencode({
    Tags = {
      Key    = "Project"
      Values = ["ecommerce", "mobile-app"]
    }
  })
}
```

### Azure Cost Management

Group costs by tags in Azure Cost Management dashboards. Export cost data with tag breakdowns:

```bash
az consumption usage list \
  --start-date 2025-12-01 \
  --query "[].{Cost:pretaxCost, Project:tags.Project, Team:tags.Owner}"
```

### GCP Cloud Billing

Export billing data to BigQuery with label breakdowns:

```sql
SELECT
  labels.key AS label_key,
  labels.value AS label_value,
  SUM(cost) AS total_cost
FROM `project.dataset.gcp_billing_export_v1_XXXXX`
CROSS JOIN UNNEST(labels) AS labels
WHERE labels.key IN ('environment', 'project', 'costcenter')
GROUP BY label_key, label_value
ORDER BY total_cost DESC
```

For cost allocation implementation details, see `references/cost-allocation.md`.

## Decision Framework: Required vs. Optional Tags

Determine which tags to enforce at creation time:

**REQUIRED (enforce with hard deny)**:
- Cost allocation: Owner, CostCenter, Project
- Lifecycle: Environment, ManagedBy
- Identification: Name

**RECOMMENDED (soft enforcement - alert only)**:
- Operational: Backup, Monitoring, Schedule
- Security: Compliance, DataClassification
- Support: SLA, ChangeManagement

**OPTIONAL (no enforcement)**:
- Custom: Application, Component, Customer
- Experimental: Any non-standard tags

**Enforcement methods**:

1. **Hard enforcement** (deny resource creation): Use for cost allocation tags
   - AWS: AWS Config rules with deny mode
   - Azure: Azure Policy with deny effect
   - GCP: Organization policies with constraints

2. **Soft enforcement** (alert only): Use for operational tags
   - AWS: AWS Config rules with notification
   - Azure: Azure Policy with audit effect
   - GCP: Cloud Asset Inventory reports

3. **No enforcement** (best-effort): Use for custom/experimental tags

## Tag Inheritance Strategies

Reduce manual tagging effort through automatic inheritance:

### AWS Tag Policies

Inherit tags from AWS Organizations account hierarchy:

```json
{
  "tags": {
    "Environment": {
      "tag_key": {
        "@@assign": "Environment"
      },
      "enforced_for": {
        "@@assign": ["ec2:instance", "s3:bucket"]
      }
    }
  }
}
```

### Azure Tag Inheritance

Use Azure Policy to inherit tags from resource groups:

```hcl
resource "azurerm_policy_assignment" "inherit_environment" {
  name                 = "inherit-environment-tag"
  policy_definition_id = azurerm_policy_definition.inherit_tags.id

  parameters = jsonencode({
    tagName = { value = "Environment" }
  })
}
```

### GCP Label Inheritance

Inherit labels from folders/projects via organization policies:

```hcl
resource "google_organization_policy" "require_labels" {
  org_id     = var.organization_id
  constraint = "constraints/gcp.resourceLabels"

  list_policy {
    allow {
      values = ["environment:prod", "environment:staging"]
    }
    inherit_from_parent = true
  }
}
```

### Kubernetes Label Propagation

Use Kyverno to auto-generate labels from namespaces:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
  rules:
  - name: add-environment-label
    match:
      resources:
        kinds: [Pod, Deployment]
    mutate:
      patchStrategicMerge:
        metadata:
          labels:
            +(environment): "{{request.namespace}}"
```

## Common Anti-Patterns

### Anti-Pattern 1: Inconsistent Tag Naming

**Problem**: Multiple variations of the same tag across resources
```yaml
# BAD: Tag sprawl
Environment: prod
environment: production
Env: prod
ENVIRONMENT: PROD
```

**Solution**: Enforce single naming convention via IaC and tag policies
```yaml
# GOOD: Consistent naming
Environment: prod  # Single standard format
```

### Anti-Pattern 2: Manual Resource Creation Without Tags

**Problem**: CLI/console-created resources missing required tags

**Solution**: Block untagged resource creation via Config/Policy rules, or use AWS Service Catalog/Azure Blueprints with pre-tagged templates

### Anti-Pattern 3: No Tag Enforcement (Voluntary Tagging)

**Problem**: Tags are optional, frequently forgotten, leading to 35% unallocated spend

**Solution**: Use provider default tags in IaC + policy enforcement at account/subscription level

### Anti-Pattern 4: Tag Sprawl (Too Many Custom Tags)

**Problem**: 30+ tags per resource, most unused, causing noise in cost reports

**Solution**: Start with "Big Six" required tags only. Add optional tags only when clear use case exists.

### Anti-Pattern 5: Static Tags Not Updated

**Problem**: Tags set at creation but never updated (e.g., `Owner` outdated after team changes)

**Solution**: Run automated tag audits (weekly), use IaC to update tags programmatically, integrate with identity provider for owner updates

## Integration with Other Skills

**infrastructure-as-code**: Tags applied automatically via Terraform/Pulumi modules with default_tags/stackTags

**cost-optimization**: Tags enable cost allocation, showback/chargeback, and budget alerts by project/team

**compliance-frameworks**: Tags prove PCI/HIPAA/SOC2 scope for audit trails and automated policy enforcement

**security-hardening**: Tags enforce security policies (e.g., public vs. internal access based on SecurityZone tag)

**disaster-recovery**: Tags identify resources for backup policies (e.g., `Backup: daily` triggers automated snapshots)

**kubernetes-operations**: Labels used for pod scheduling, resource quotas, network policies, and service selection

## Implementation Checklist

When implementing resource tagging:

- [ ] Define "Big Six" required tags with allowed values
- [ ] Choose ONE naming convention (PascalCase, lowercase, kebab-case)
- [ ] Implement tags in IaC (Terraform/Pulumi provider default_tags)
- [ ] Set up enforcement policies (AWS Config, Azure Policy, GCP org policies)
- [ ] Enable cost allocation tags in billing console (AWS Cost Explorer, Azure Cost Management)
- [ ] Create tag compliance audit process (weekly recommended)
- [ ] Document tag standards in organization wiki/runbook
- [ ] Set up automated alerts for untagged resources
- [ ] Integrate tags with monitoring/alerting for owner contact
- [ ] Create remediation playbook for non-compliant resources

## Quick Reference

### Tag Enforcement Tools by Provider

| Provider | Enforcement Tool | Purpose |
|----------|------------------|---------|
| **AWS** | AWS Config Rules | Tag compliance monitoring + remediation |
| **AWS** | Tag Policies (Organizations) | Enforce tags at account level |
| **Azure** | Azure Policy | Tag enforcement + inheritance |
| **GCP** | Organization Policies | Label restrictions + inheritance |
| **Kubernetes** | OPA Gatekeeper | Admission control for labels |
| **Kubernetes** | Kyverno | Auto-generate labels + validation |

### Cost Allocation Tools

| Tool | Purpose |
|------|---------|
| AWS Cost Explorer | Tag-based cost analysis + anomaly detection |
| Azure Cost Management | Tag grouping + budgets |
| GCP Cloud Billing | Label-based cost breakdown |
| CloudHealth | Multi-cloud cost optimization |
| Kubecost | Kubernetes cost allocation by labels |

### Validation Tools (Pre-Deployment)

| Tool | Purpose |
|------|---------|
| Checkov | IaC tag validation (pre-commit) |
| tflint | Terraform linting for tag rules |
| terraform-compliance | BDD tests for tag policies |

## Additional Resources

For detailed implementation guidance:

- **Tag taxonomy and categories**: See `references/tag-taxonomy.md`
- **Enforcement patterns (AWS, Azure, GCP, K8s)**: See `references/enforcement-patterns.md`
- **Cost allocation setup**: See `references/cost-allocation.md`
- **Compliance auditing queries**: See `references/compliance-auditing.md`
- **Terraform examples**: See `examples/terraform/`
- **Kubernetes manifests**: See `examples/kubernetes/`
- **Audit scripts**: See `scripts/audit_tags.py`, `scripts/cost_by_tag.py`

## Key Takeaways

1. **Start with "Big Six" required tags**: Name, Environment, Owner, CostCenter, Project, ManagedBy
2. **Enforce at creation time**: Use AWS Config, Azure Policy, GCP org policies to block untagged resources
3. **Automate with IaC**: Terraform/Pulumi default tags reduce manual errors by 95%
4. **Enable cost allocation**: Activate billing tags to reduce unallocated spend by 80%
5. **Choose ONE naming convention**: PascalCase, lowercase, or kebab-case - enforce consistently
6. **Inherit tags from parents**: Resource groups, folders, namespaces propagate tags automatically
7. **Audit regularly**: Weekly tag compliance checks catch drift and prevent sprawl
8. **Tag inheritance reduces effort**: Let parent resources propagate common tags to children
