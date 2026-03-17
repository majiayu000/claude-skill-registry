---
name: platform-migration
description: Guides infrastructure and platform migration including cloud-to-cloud migration (AWS to GCP, Azure to AWS), Kubernetes cluster migration, CI/CD platform changes, monitoring stack migration, identity provider migration, and network infrastructure transformation. Covers IaC migration, container orchestration, service mesh, observability tools, and multi-cloud strategies. Use when migrating infrastructure, changing cloud providers, moving Kubernetes clusters, or when users mention "cloud migration", "platform switch", "infrastructure migration", "K8s migration", "multi-cloud", or "cloud provider change".
---

# Platform Migration

## Overview

This skill provides comprehensive guidance for migrating infrastructure platforms, cloud providers, container orchestration systems, CI/CD pipelines, and observability stacks. Focus is on infrastructure-level migrations that complement application modernization efforts.

Platform migrations are infrastructure-focused and should be paired with application migration strategies. Use cloud-neutral design patterns to reduce future migration effort, though multi-cloud strategies increase complexity while reducing vendor lock-in.

## Core Migration Principles

**Key Practices:**

- Test everything in non-production first
- Automate using Infrastructure as Code (IaC)
- Migrate incrementally rather than "big bang"
- Maintain both platforms during stabilization
- Budget 20-30% more time than estimated
- Document architecture decisions and rationale

**Avoid These Pitfalls:**

- Migrating everything at once without phased approach
- Skipping non-production validation
- Ignoring cost estimation for target platform
- Failing to optimize during migration (pure lift-and-shift)
- Inadequate monitoring during transition
- Leaving resources running on both platforms post-migration

## Migration Workflow

## Step 1: Assessment and Planning

**Identify Migration Type:**

- Cloud-to-cloud (AWS↔GCP↔Azure)
- Kubernetes cluster migration (EKS→GKE→AKS)
- CI/CD platform change (Jenkins→GitLab→GitHub Actions)
- Monitoring stack migration (Prometheus→Datadog→New Relic)
- Container registry migration (Docker Hub→ECR→GCR→ACR)
- Network infrastructure transformation
- Infrastructure as Code migration (Terraform→CloudFormation→Bicep)

**For detailed migration type workflows:** See [migration-types.md](references/migration-types.md)

### Step 2: Inventory and Dependencies

- Document all resources in source platform
- Map dependencies between components
- Identify proprietary services without direct equivalents
- Estimate costs in target platform
- Assess technical constraints and requirements

### Step 3: Design Target Architecture

- Map source services to target equivalents
- Design network topology and connectivity
- Plan IAM and security model
- Define migration approach (phased, parallel, cutover)
- Create rollback procedures

**For IaC-specific migrations:** See [infrastructure-as-code-migration.md](references/infrastructure-as-code-migration.md)

### Step 4: Risk Assessment and Mitigation

- Identify critical dependencies and single points of failure
- Plan for downtime windows
- Establish success criteria and validation tests
- Define rollback triggers and procedures

**For comprehensive risk planning:** See [risk-management.md](references/risk-management.md)

### Step 5: Pilot Migration

- Select non-critical workload for pilot
- Execute migration following documented procedure
- Validate functionality and performance
- Measure costs and resource utilization
- Document lessons learned and adjust plan

### Step 6: Production Migration

- Migrate in planned waves/phases
- Implement data replication and synchronization
- Execute DNS cutover per service
- Monitor performance and errors continuously
- Validate each wave before proceeding

**For validation procedures:** See [post-migration-validation.md](references/post-migration-validation.md)

### Step 7: Optimization and Cleanup

- Right-size resources based on actual usage
- Optimize costs using platform-native features
- Improve performance with platform capabilities
- Decommission source resources systematically
- Document final architecture

**For cost optimization strategies:** See [cost-optimization-during-migration.md](references/cost-optimization-during-migration.md)

## Common Migration Scenarios

### Cloud-to-Cloud Migration

Migrating between AWS, GCP, Azure, or moving from on-premise to cloud. Requires service mapping, network connectivity, and data transfer strategy.

**Load:** [migration-types.md](references/migration-types.md) - Section 1: Cloud-to-Cloud Migration

### Kubernetes Platform Migration

Moving clusters between EKS, GKE, AKS, or to self-managed Kubernetes. Involves workload migration, persistent storage, service meshes, and ingress controllers.

**Load:** [migration-types.md](references/migration-types.md) - Section 2: Kubernetes Platform Migration

### CI/CD Platform Changes

Transitioning between Jenkins, GitLab CI, GitHub Actions, CircleCI, or other platforms. Requires pipeline translation and secrets migration.

**Load:** [migration-types.md](references/migration-types.md) - Section 3: CI/CD Platform Migration

### Monitoring Stack Migration

Changing observability tools like Prometheus→Datadog, CloudWatch→New Relic. Includes metrics, logs, traces, and alerting.

**Load:** [migration-types.md](references/migration-types.md) - Section 4: Monitoring Stack Migration

### Container Registry Migration

Moving container images between Docker Hub, ECR, GCR, ACR, Harbor, or private registries.

**Load:** [container-registry-migration.md](references/container-registry-migration.md)

### Network Infrastructure Migration

Transforming VPC configuration, VPN connections, DNS, load balancers, and CDN infrastructure.

**Load:** [network-infrastructure-migration.md](references/network-infrastructure-migration.md)

### Database Platform Migration

Migrating databases to different cloud providers or managed services.

**Load:** [database-platform-migration.md](references/database-platform-migration.md)

## Migration Tools and Utilities

For platform-specific migration tools, automation scripts, and utilities:

**Load:** [migration-tools.md](references/migration-tools.md)

Includes cloud provider migration tools (AWS MGN, Azure Migrate, Google Cloud Migrate), Kubernetes tools (Velero, Kustomize), IaC tools (Terraformer, CDK), and data transfer utilities.

## Reference Documentation

### Migration Principles

**Load:** [migration-principles.md](references/migration-principles.md)  
Complete best practices, anti-patterns, and key considerations for any platform migration.

### Risk Management

**Load:** [risk-management.md](references/risk-management.md)  
Risk identification, mitigation strategies, contingency planning, and rollback procedures.

### Post-Migration Validation

**Load:** [post-migration-validation.md](references/post-migration-validation.md)  
Validation checklists, testing procedures, performance benchmarking, and cutover verification.

### Cost Optimization

**Load:** [cost-optimization-during-migration.md](references/cost-optimization-during-migration.md)  
Cost analysis, optimization strategies, and budget management during migration.

## Output Formats

When generating migration artifacts, produce:

- **Migration Plan**: Detailed phases, timelines, dependencies, resources
- **Architecture Diagrams**: Source and target architecture with transition states
- **Service Mapping**: Complete mapping between source and target services
- **Runbooks**: Step-by-step execution procedures with rollback steps
- **Validation Checklists**: Acceptance criteria and testing procedures
- **Risk Register**: Identified risks, impact, probability, mitigation
- **Cost Analysis**: Comparative cost breakdown with optimization opportunities
