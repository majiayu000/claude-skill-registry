---
name: azure-well-architected-framework
description: "Comprehensive Azure Well-Architected Framework knowledge covering the five pillars: Reliability, Security, Cost Optimization, Operational Excellence, and Performance Efficiency. Provides design principles, best practices, and implementation guidance for building robust Azure solutions."
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Azure Well-Architected Framework

The Azure Well-Architected Framework is a set of guiding tenets for building high-quality cloud solutions. It consists of five pillars of architectural excellence.

## Overview

**Purpose**: Help architects and engineers build secure, high-performing, resilient, and efficient infrastructure for applications.

**The Five Pillars**:
1. Reliability
2. Security
3. Cost Optimization
4. Operational Excellence
5. Performance Efficiency

## Pillar 1: Reliability

**Definition**: The ability of a system to recover from failures and continue to function.

**Key Principles**:
- Design for failure
- Use availability zones and regions
- Implement redundancy
- Monitor and respond to failures
- Test disaster recovery

**Best Practices**:

**Availability Zones:**
```bash
# Deploy VM across availability zones
az vm create \
  --resource-group MyRG \
  --name MyVM \
  --zone 1 \
  --image Ubuntu2204 \
  --size Standard_D2s_v3

# Availability SLAs:
# - Single VM (Premium SSD): 99.9%
# - Availability Set: 99.95%
# - Availability Zones: 99.99%
```

**Backup and Disaster Recovery:**
```bash
# Enable Azure Backup
az backup protection enable-for-vm \
  --resource-group MyRG \
  --vault-name MyVault \
  --vm MyVM \
  --policy-name DefaultPolicy

# Recovery Point Objective (RPO): How much data loss is acceptable
# Recovery Time Objective (RTO): How long can system be down
```

**Health Probes:**
- Application Gateway health probes
- Load Balancer probes
- Traffic Manager endpoint monitoring

## Pillar 2: Security

**Definition**: Protecting applications and data from threats.

**Key Principles**:
- Defense in depth
- Least privilege access
- Secure the network
- Protect data at rest and in transit
- Monitor and audit

**Best Practices**:

**Identity and Access:**
```bash
# Use managed identities (no credentials in code)
az vm identity assign \
  --resource-group MyRG \
  --name MyVM

# RBAC assignment
az role assignment create \
  --assignee <principal-id> \
  --role "Contributor" \
  --scope /subscriptions/<subscription-id>/resourceGroups/MyRG
```

**Network Security:**
- Use Network Security Groups (NSGs)
- Implement Azure Firewall or Application Gateway WAF
- Use Private Endpoints for PaaS services
- Enable DDoS Protection Standard for public-facing apps

**Data Protection:**
```bash
# Enable encryption at rest (automatic for most services)
# Enable TLS 1.2+ for data in transit

# Azure Storage encryption
az storage account update \
  --name mystorageaccount \
  --resource-group MyRG \
  --min-tls-version TLS1_2 \
  --https-only true
```

**Security Monitoring:**
```bash
# Enable Microsoft Defender for Cloud
az security pricing create \
  --name VirtualMachines \
  --tier Standard

# Enable Azure Sentinel
az sentinel onboard \
  --resource-group MyRG \
  --workspace-name MyWorkspace
```

## Pillar 3: Cost Optimization

**Definition**: Managing costs to maximize the value delivered.

**Key Principles**:
- Plan and estimate costs
- Provision with optimization
- Use monitoring and analytics
- Maximize efficiency of cloud spend

**Best Practices**:

**Right-Sizing:**
```bash
# Use Azure Advisor recommendations
az advisor recommendation list \
  --category Cost \
  --output table

# Common optimizations:
# 1. Shutdown dev/test VMs when not in use
# 2. Use Azure Hybrid Benefit for Windows/SQL
# 3. Purchase reservations for consistent workloads
# 4. Use autoscaling to match demand
```

**Reserved Instances:**
- 1-year or 3-year commitment
- Save up to 72% vs pay-as-you-go
- Available for VMs, SQL Database, Cosmos DB, Synapse, Storage

**Azure Hybrid Benefit:**
```bash
# Apply Windows license to VM
az vm update \
  --resource-group MyRG \
  --name MyVM \
  --license-type Windows_Server

# SQL Server Hybrid Benefit
az sql vm create \
  --resource-group MyRG \
  --name MySQLVM \
  --license-type AHUB
```

**Cost Management:**
```bash
# Create budget
az consumption budget create \
  --budget-name MyBudget \
  --category cost \
  --amount 1000 \
  --time-grain monthly \
  --start-date 2025-01-01 \
  --end-date 2025-12-31

# Set up alerts at 80%, 100%, 120% of budget
```

## Pillar 4: Operational Excellence

**Definition**: Operations processes that keep a system running in production.

**Key Principles**:
- Automate operations
- Monitor and gain insights
- Refine operations procedures
- Anticipate failure
- Stay current with updates

**Best Practices**:

**Infrastructure as Code:**
```bash
# Use ARM, Bicep, or Terraform
# Version control all infrastructure
# Implement CI/CD for infrastructure

# Example: Bicep deployment
az deployment group create \
  --resource-group MyRG \
  --template-file main.bicep \
  --parameters @parameters.json
```

**Monitoring and Alerting:**
```bash
# Application Insights for apps
az monitor app-insights component create \
  --app MyApp \
  --location eastus \
  --resource-group MyRG

# Log Analytics for infrastructure
az monitor log-analytics workspace create \
  --resource-group MyRG \
  --workspace-name MyWorkspace

# Create alerts
az monitor metrics alert create \
  --name HighCPU \
  --resource-group MyRG \
  --scopes <vm-id> \
  --condition "avg Percentage CPU > 80" \
  --description "CPU usage is above 80%"
```

**DevOps Practices:**
- Continuous Integration/Continuous Deployment (CI/CD)
- Blue-green deployments
- Canary releases
- Feature flags
- Automated testing

## Pillar 5: Performance Efficiency

**Definition**: The ability of a system to adapt to changes in load.

**Key Principles**:
- Scale horizontally
- Choose the right resources
- Monitor performance
- Optimize network and data access

**Best Practices**:

**Scaling:**
```bash
# Horizontal scaling (preferred)
# VM Scale Sets
az vmss create \
  --resource-group MyRG \
  --name MyVMSS \
  --image Ubuntu2204 \
  --instance-count 3 \
  --vm-sku Standard_D2s_v3

# Autoscaling
az monitor autoscale create \
  --resource-group MyRG \
  --resource MyVMSS \
  --resource-type Microsoft.Compute/virtualMachineScaleSets \
  --name MyAutoscale \
  --min-count 2 \
  --max-count 10
```

**Caching:**
- Azure Cache for Redis
- Azure CDN for static content
- Application-level caching

**Data Access:**
- Use indexes on databases
- Implement caching strategies
- Use CDN for global content delivery
- Optimize queries (SQL, Cosmos DB)

**Networking:**
```bash
# Use Azure Front Door for global apps
az afd profile create \
  --profile-name MyFrontDoor \
  --resource-group MyRG \
  --sku Premium_AzureFrontDoor

# Features:
# - Global load balancing
# - CDN capabilities
# - Web Application Firewall
# - SSL offloading
# - Caching
```

## Assessment and Tools

**Azure Well-Architected Review:**
```bash
# Self-assessment tool in Azure Portal
# Generates recommendations per pillar
# Provides actionable guidance
```

**Azure Advisor:**
```bash
# Get recommendations
az advisor recommendation list --output table

# Categories:
# - Reliability (High Availability)
# - Security
# - Performance
# - Cost
# - Operational Excellence
```

## Implementation Checklist

**Reliability:**
- [ ] Deploy across availability zones
- [ ] Implement backup strategy
- [ ] Define RTO and RPO
- [ ] Test disaster recovery
- [ ] Implement health monitoring

**Security:**
- [ ] Enable Azure AD authentication
- [ ] Implement RBAC (least privilege)
- [ ] Encrypt data at rest and in transit
- [ ] Enable Microsoft Defender for Cloud
- [ ] Implement network segmentation (NSGs, Firewall)
- [ ] Use Key Vault for secrets

**Cost Optimization:**
- [ ] Right-size resources
- [ ] Purchase reservations for predictable workloads
- [ ] Enable autoscaling
- [ ] Use Azure Hybrid Benefit
- [ ] Implement budget alerts
- [ ] Review Azure Advisor cost recommendations

**Operational Excellence:**
- [ ] Implement Infrastructure as Code
- [ ] Set up CI/CD pipelines
- [ ] Enable comprehensive monitoring
- [ ] Create operational runbooks
- [ ] Implement automated alerting
- [ ] Use tags for resource organization

**Performance Efficiency:**
- [ ] Choose appropriate resource SKUs
- [ ] Implement autoscaling
- [ ] Use caching (Redis, CDN)
- [ ] Optimize database queries
- [ ] Implement load balancing
- [ ] Monitor performance metrics

## Common Patterns

**Highly Available Web Application:**
- Application Gateway (WAF enabled)
- App Service (Premium tier, multiple instances)
- Azure SQL Database (Zone-redundant)
- Azure Cache for Redis
- Application Insights
- Azure Front Door (global distribution)

**Mission-Critical Application:**
- Multi-region deployment
- Traffic Manager or Front Door (global routing)
- Availability Zones in each region
- Geo-redundant storage (GRS or RA-GRS)
- Automated backups with geo-replication
- Comprehensive monitoring and alerting

**Cost-Optimized Dev/Test:**
- Auto-shutdown for VMs
- B-series (burstable) VMs
- Dev/Test pricing tiers
- Shared App Service plans
- Azure DevTest Labs

## References

- **Official Framework**: https://learn.microsoft.com/en-us/azure/well-architected/
- **Azure Advisor**: https://portal.azure.com/#blade/Microsoft_Azure_Expert/AdvisorMenuBlade/overview
- **Well-Architected Review**: https://learn.microsoft.com/en-us/assessments/azure-architecture-review/
- **Architecture Center**: https://learn.microsoft.com/en-us/azure/architecture/

## Key Takeaways

1. **Balance the Pillars**: Trade-offs exist between pillars (e.g., cost vs. reliability)
2. **Continuous Improvement**: Architecture is not static, revisit regularly
3. **Measure and Monitor**: Use data to drive decisions
4. **Automation**: Automate repetitive tasks to improve reliability and reduce costs
5. **Security First**: Integrate security into every layer of architecture

The Well-Architected Framework provides a consistent approach to evaluating architectures and implementing designs that scale over time.
