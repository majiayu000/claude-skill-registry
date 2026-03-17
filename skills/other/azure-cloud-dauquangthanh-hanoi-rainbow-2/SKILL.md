---
name: azure-cloud
description: Provides comprehensive Microsoft Azure guidance including Azure Virtual Machines, Azure Storage (Blob, Files, Disks), Azure SQL Database, Azure App Service, Azure Functions, AKS (Azure Kubernetes Service), Azure DevOps, ARM templates, Bicep, Terraform for Azure, Azure Active Directory, Azure Key Vault, Azure Monitor, cost optimization, and multi-region deployment. Produces infrastructure as code (Terraform/Bicep/ARM), deployment scripts, security configurations, and architecture designs. Use when deploying to Azure, designing Azure infrastructure, migrating to Microsoft Azure, configuring VMs, setting up Azure Storage, managing Azure SQL, working with AKS, or when users mention Azure, Microsoft Cloud, Azure Portal, ARM templates, Bicep, Azure Functions, App Service, or Azure DevOps.
---

# Azure Cloud

## Core Capabilities

Provides expert guidance for Microsoft Azure infrastructure and services:

1. **Compute Services** - Azure Virtual Machines, Virtual Machine Scale Sets, Azure App Service, Azure Functions, Azure Container Instances
2. **Storage Services** - Azure Blob Storage, Azure Files, Azure Disk Storage, Azure Data Lake Storage
3. **Database Services** - Azure SQL Database, Azure Cosmos DB, Azure Database for MySQL/PostgreSQL, Azure Redis Cache
4. **Networking** - Azure Virtual Network (VNet), Azure Load Balancer, Application Gateway, Azure Front Door, VPN Gateway, ExpressRoute
5. **Container Services** - AKS (Azure Kubernetes Service), Azure Container Registry, Azure Container Instances
6. **Infrastructure as Code** - Terraform, Bicep, ARM Templates, Azure CLI, PowerShell
7. **Security** - Azure Active Directory (Entra ID), Azure Key Vault, Azure Security Center, Azure Sentinel, Azure Policy
8. **DevOps & CI/CD** - Azure DevOps, Azure Pipelines, GitHub Actions with Azure integration
9. **Monitoring** - Azure Monitor, Application Insights, Log Analytics, Azure Alerts

## Best Practices

## Azure Virtual Machines

- Select appropriate VM sizes based on workload (D-series, F-series, E-series)
- Use managed disks for simplified management and availability
- Enable Azure Backup for VM protection
- Use availability sets or availability zones for high availability
- Configure VM extensions for automated configuration
- Enable Azure Disk Encryption for data protection
- Use proximity placement groups for low latency

### Azure Storage

- Use storage account types based on use case (Standard vs Premium, Hot/Cool/Archive tiers)
- Enable soft delete for blob and container protection
- Use private endpoints for secure access
- Configure lifecycle management policies for cost optimization
- Enable Azure Storage encryption (SSE)
- Use Azure CDN with Blob Storage for content delivery
- Implement immutable blob storage for compliance

### Azure SQL Database

- Select appropriate service tier (Basic, Standard, Premium, Hyperscale)
- Enable automatic backups with long-term retention
- Use read replicas for read scaling
- Configure active geo-replication for disaster recovery
- Enable Transparent Data Encryption (TDE)
- Use Always Encrypted for sensitive data
- Monitor with Query Performance Insight

### Azure Virtual Network

- Plan address space carefully using RFC 1918 ranges
- Use subnets to segment workloads and apply NSGs
- Configure Network Security Groups (NSGs) with least privilege
- Use Azure Firewall for centralized network security
- Enable VNet peering for cross-VNet communication
- Use service endpoints and private endpoints for Azure services
- Implement network watcher for diagnostics

### AKS (Azure Kubernetes Service)

- Use managed identity for AKS cluster authentication
- Configure multiple node pools with auto-scaling
- Enable Azure Policy for Kubernetes
- Use Azure Container Registry with image scanning
- Implement network policies with Azure CNI or Calico
- Enable cluster monitoring with Container Insights
- Configure ingress controllers with Application Gateway

### Security

- Enable Azure AD Multi-Factor Authentication (MFA)
- Use managed identities instead of service principals where possible
- Implement Role-Based Access Control (RBAC) with least privilege
- Store secrets in Azure Key Vault
- Enable Azure Security Center for threat protection
- Use Azure Policy for governance and compliance
- Enable Azure Sentinel for SIEM capabilities
- Audit activities with Azure Activity Log

### Cost Optimization

- Use Azure Reserved Instances for predictable workloads
- Leverage Azure Spot VMs for fault-tolerant workloads
- Implement auto-scaling to match demand
- Use Azure Cost Management for budgets and alerts
- Right-size VMs based on Azure Advisor recommendations
- Use Azure Hybrid Benefit for Windows Server and SQL Server
- Configure storage lifecycle policies to reduce costs

### DevOps Best Practices

- Use Azure DevOps or GitHub Actions for CI/CD pipelines
- Implement infrastructure as code with Bicep or Terraform
- Use Azure Key Vault for pipeline secrets
- Enable deployment slots for App Service blue-green deployments
- Implement automated testing in pipelines
- Use Azure Artifacts for package management
- Configure branch policies and pull request validation

## Detailed References

Load reference files based on specific needs:

- **Compute Services**: See [compute-services.md](references/compute-services.md) for Azure VM sizes, families, selection guide, Virtual Machine Scale Sets, Azure App Service, Azure Functions patterns, and Container Instances

- **Storage Solutions**: See [storage-solutions.md](references/storage-solutions.md) for Blob Storage configuration, Azure Files setup, disk types, performance optimization, and storage security

- **Container Orchestration**: See [container-orchestration.md](references/container-orchestration.md) for AKS cluster design, node pool configuration, workload deployment, Container Registry integration, service mesh, and ingress controllers

- **Infrastructure as Code**: See [infrastructure-as-code.md](references/infrastructure-as-code.md) for Bicep templates, ARM patterns, Terraform Azure provider, Azure CLI scripting, and PowerShell automation

- **Security Configuration**: See [security-configuration.md](references/security-configuration.md) for Azure Key Vault, Network Security Groups, Azure Firewall, Security Center, Defender for Cloud, and Azure Policy

- **Monitoring and Diagnostics**: See [monitoring-diagnostics.md](references/monitoring-diagnostics.md) for Azure Monitor, Application Insights, Log Analytics queries (KQL), alert rules, and diagnostic settings
