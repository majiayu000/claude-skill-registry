---
name: oracle-cloud
description: Provides comprehensive Oracle Cloud Infrastructure (OCI) guidance including compute instances, networking (VCN, load balancers, VPN), storage (block, object, file), database services (Autonomous Database, MySQL, NoSQL), container orchestration (OKE), identity and access management (IAM), resource management, cost optimization, and infrastructure as code (Terraform OCI provider, Resource Manager). Produces infrastructure code, deployment scripts, configuration guides, and architectural diagrams. Use when designing OCI architecture, provisioning cloud resources, migrating to Oracle Cloud, implementing OCI security, setting up OCI databases, deploying containerized applications on OKE, managing OCI resources, or when users mention "Oracle Cloud", "OCI", "Autonomous Database", "VCN", "OKE", "OCI Terraform", "Resource Manager", "Oracle Cloud Infrastructure", or "OCI migration".
---

# Oracle Cloud Infrastructure (OCI)

## Core Capabilities

Provides expert guidance for Oracle Cloud Infrastructure across all major services:

1. **Compute Services** - VM instances, bare metal, autoscaling, instance pools
2. **Networking** - Virtual Cloud Networks (VCN), subnets, security lists, route tables, load balancers, VPN
3. **Storage** - Block volumes, object storage, file storage, archive storage
4. **Database Services** - Autonomous Database, MySQL, PostgreSQL, NoSQL, MongoDB
5. **Container & Kubernetes** - Oracle Kubernetes Engine (OKE), container instances, registries
6. **Identity & Access Management** - Users, groups, policies, federation, MFA
7. **Infrastructure as Code** - Terraform OCI provider, Resource Manager, stacks
8. **Cost Management** - Budgets, cost analysis, resource tagging, rightsizing

## Best Practices

## Compute

- Use flexible shapes for cost optimization
- Enable boot volume backups and configure lifecycle policies
- Use instance pools with autoscaling for dynamic workloads
- Implement proper tagging for resource management
- Leverage availability domains for high availability

### Networking

- Design VCN with proper CIDR blocks (avoid overlaps)
- Use security lists and network security groups together
- Implement private subnets for databases and application tiers
- Enable DRG (Dynamic Routing Gateway) for hybrid connectivity
- Configure load balancer health checks with appropriate intervals

### Storage

- Use block volumes with appropriate performance tiers
- Implement lifecycle policies for object storage cost savings
- Enable encryption at rest for all storage services
- Configure regular backups with retention policies
- Use file storage for shared application data

### Database

- Use Autonomous Database for automatic management and tuning
- Enable automatic backups with point-in-time recovery
- Configure connection pooling and TLS encryption
- Implement proper IAM policies for database access
- Monitor database metrics and set up alerts

### Container Orchestration

- Use managed OKE for Kubernetes workloads
- Enable cluster autoscaling and pod autoscaling
- Implement pod security policies and network policies
- Use OCI Container Registry for private image storage
- Configure proper resource requests and limits

### IAM & Security

- Follow principle of least privilege for policies
- Enable MFA for all users with admin access
- Use service-level resources for automation
- Implement compartment hierarchy for resource isolation
- Audit IAM policy changes regularly

### Infrastructure as Code

- Use Terraform OCI provider with remote state
- Organize resources by compartment and environment
- Version control all infrastructure code
- Use Resource Manager for managed Terraform execution
- Implement proper variable management and secrets handling

### Cost Optimization

- Use flexible shapes to match workload requirements
- Implement autoscaling to scale down during off-peak
- Use preemptible instances for fault-tolerant workloads
- Set up budgets and cost alerts
- Tag resources for cost allocation and tracking

## Detailed References

Load reference files based on specific needs:

- **Compute Services**: See [compute-services.md](references/compute-services.md) for:
  - VM shapes and bare metal configuration
  - Instance pools and autoscaling setup
  - Boot volume management and backups
  - Custom images and cloud-init configuration

- **Networking Architecture**: See [networking-architecture.md](references/networking-architecture.md) for:
  - VCN design patterns and CIDR planning
  - Security lists and network security groups
  - Load balancer configuration (public, private)
  - FastConnect and VPN setup for hybrid connectivity
  - VCN peering and DNS configuration

- **Database Services**: See [database-services.md](references/database-services.md) for:
  - Autonomous Database provisioning and management
  - MySQL, PostgreSQL, and NoSQL configuration
  - Database backup and recovery procedures
  - Connection pooling and performance optimization
  - Database migration strategies

- **IAM Configuration**: See [iam-configuration.md](references/iam-configuration.md) for:
  - User, group, and policy management
  - Compartment design and hierarchy
  - Dynamic groups and instance principals
  - Federation and identity providers
  - Tagging strategy and resource limits

- **Terraform for OCI**: See [terraform-oci.md](references/terraform-oci.md) for:
  - Terraform OCI provider configuration
  - Common resource provisioning patterns
  - Module structure and best practices
  - Remote state management in object storage
  - Three-tier architecture examples

- **OCI CLI Commands**: See [oci-cli-commands.md](references/oci-cli-commands.md) for:
  - OCI CLI installation and configuration
  - Compute, networking, storage, and database commands
  - Container registry and OKE operations
  - Query and filtering techniques
  - Troubleshooting and debugging
