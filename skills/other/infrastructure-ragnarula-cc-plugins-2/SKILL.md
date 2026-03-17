---
name: infrastructure
description: Use this skill when designing or reviewing cloud infrastructure, networking, compute resources, storage systems, or any system involving resource provisioning and management. Applies infrastructure thinking to specifications, designs, and implementations.
version: 0.1.0
---

# Infrastructure Engineering

## When to Apply

Use this skill when the system involves:
- Cloud resource provisioning (compute, storage, networking)
- Infrastructure as Code (Terraform, Pulumi, CloudFormation)
- Networking (VPCs, subnets, load balancers, DNS)
- Container orchestration (Kubernetes, ECS)
- Database infrastructure and scaling
- Disaster recovery and backup strategies

## Mindset

Infrastructure engineers think in terms of resources, failure domains, and operational burden.

**Questions to always ask:**
- What's the blast radius if this fails?
- What are the failure domains? Are we resilient to AZ/region failure?
- How does this scale? What's the bottleneck?
- What's the cost? How does it grow with usage?
- How do we recover from disaster? What's the RTO/RPO?
- Who can access this? How is access audited?
- What happens during a deploy? Is there downtime?

**Assumptions to challenge:**
- "The cloud is reliable" - AZs fail. Regions fail. Design for it.
- "We can scale later" - Some architectural decisions don't scale. Choose early.
- "It's in a private subnet" - Defense in depth. Don't rely on network alone.
- "Kubernetes handles it" - K8s is a tool, not magic. Understand what it does.
- "We'll back up later" - Untested backups aren't backups.
- "The defaults are fine" - Defaults are generic. Review security groups, IAM, encryption.

## Practices

### Infrastructure as Code
All infrastructure in version-controlled code. No manual changes to production. Use modules for reusable patterns. **Don't** click in consoles for production, let IaC drift from reality, or copy-paste instead of modularize.

### Failure Domains
Spread resources across availability zones. Identify single points of failure. Design for component failure without total outage. **Don't** put all resources in one AZ, create hidden SPOFs, or assume any component is 100% available.

### Network Design
Use private subnets for internal services. Minimize public exposure. Use security groups as allowlists. Implement network segmentation. **Don't** expose services unnecessarily, use 0.0.0.0/0 ingress, or rely on obscurity.

### Resource Right-sizing
Start small, measure, then scale. Use autoscaling for variable load. Set resource limits and requests. **Don't** overprovision "just in case", run without limits, or ignore cost monitoring.

### State Management
Externalize state from compute. Use managed services for databases and queues. Make compute stateless where possible. **Don't** store state on ephemeral instances, use local disk for important data, or couple state to compute lifecycle.

### Backup & Recovery
Automate backups. Test restores regularly. Document RTO/RPO and verify you can meet them. Store backups in separate failure domains. **Don't** assume backups work without testing, keep backups in the same blast radius, or skip documenting recovery procedures.

### Access Control
Use IAM roles, not keys, where possible. Apply least privilege. Audit access regularly. Use separate accounts/projects for environments. **Don't** share credentials, use overly broad policies, or mix production and dev access.

### Change Management
Use progressive rollouts. Have rollback plans. Make changes reversible. Test in staging first. **Don't** yolo to production, make irreversible changes without approval, or skip staging.

## Vocabulary

Use precise terminology:

| Instead of | Say |
|------------|-----|
| "highly available" | "survives AZ failure" / "multi-region active-active" |
| "scalable" | "horizontal autoscaling 2-10 nodes" / "scales to X RPS" |
| "secure" | "private subnet with ALB" / "IAM role with policy X" |
| "backed up" | "daily snapshots, 30-day retention, tested monthly" |
| "fast" | "provisioned IOPS" / "SSD-backed" / "in same AZ" |
| "serverless" | "Lambda with X memory, Y timeout" / "Fargate" |

## SDD Integration

**During Specification:**
- Identify availability requirements (uptime SLA, RTO, RPO)
- Clarify scaling requirements (expected load, growth rate)
- Determine compliance constraints (data residency, encryption)
- Establish cost constraints

**During Design:**
- Document resource architecture with failure domains
- Specify IaC approach and module structure
- Design network topology and access patterns
- Plan backup and disaster recovery strategy
- Define autoscaling policies and limits

**During Review:**
- Verify multi-AZ deployment where required
- Check for single points of failure
- Confirm IaC matches actual requirements
- Validate backup and recovery procedures exist
- Review IAM policies for least privilege
