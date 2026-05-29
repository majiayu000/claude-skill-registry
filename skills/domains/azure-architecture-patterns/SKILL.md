---
name: "Azure Architecture Patterns"
description: "Well-Architected Framework principles, reference architectures, and best practices for cloud-native solutions"
user-invokable: false
---

# Skill: Azure Architecture Patterns

> Well-Architected Framework principles, reference architectures, and best practices for cloud-native solutions.

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | azure-architecture-patterns |
| **Version** | 1.0.0 |
| **Category** | Cloud/Infrastructure |
| **Difficulty** | Advanced |
| **Prerequisites** | Basic Azure knowledge |
| **Related Skills** | azure-devops-automation, cognitive-load (for architecture reviews) |

---

## Overview

Azure architecture is about trade-offs, not perfection. This skill provides structured guidance for designing, evaluating, and optimizing Azure solutions using the Well-Architected Framework (WAF) pillars.

### The Five Pillars

| Pillar | Focus | Key Question |
|--------|-------|--------------|
| **Reliability** | Resiliency, availability | "Will it stay up?" |
| **Security** | Protection, compliance | "Is it safe?" |
| **Cost Optimization** | Efficiency, value | "Is it worth it?" |
| **Operational Excellence** | Manageability, observability | "Can we run it?" |
| **Performance Efficiency** | Scalability, responsiveness | "Is it fast enough?" |

---

## Module 1: Reliability Patterns

### Design Principles

1. **Design for failure** - Assume components will fail
2. **Observe health** - Know when something is wrong
3. **Drive automation** - Reduce human error
4. **Design for self-healing** - Automatic recovery
5. **Design for scale-out** - Horizontal over vertical

### Key Patterns

#### Circuit Breaker
Prevent cascading failures by failing fast when a downstream service is unhealthy.

```csharp
// Polly implementation
var circuitBreakerPolicy = Policy
    .Handle<HttpRequestException>()
    .CircuitBreakerAsync(
        exceptionsAllowedBeforeBreaking: 3,
        durationOfBreak: TimeSpan.FromSeconds(30)
    );
```

#### Retry with Exponential Backoff
Handle transient failures with increasing delays.

```csharp
var retryPolicy = Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(3, retryAttempt => 
        TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
```

#### Availability Zones
Distribute resources across physically separate datacenters.

| Resource | Zone Support |
|----------|--------------|
| VMs | Zone-redundant or zonal |
| Azure SQL | Zone-redundant HA |
| Storage | ZRS, GZRS |
| App Service | Zone-redundant (Premium) |

### Reliability Checklist

- [ ] Single points of failure identified and mitigated
- [ ] Health endpoints implemented (`/health`, `/ready`)
- [ ] Retry policies with backoff configured
- [ ] Circuit breakers for external dependencies
- [ ] Availability zones utilized (where supported)
- [ ] Disaster recovery plan documented
- [ ] RTO/RPO defined and tested

---

## Module 2: Security Patterns

### Zero Trust Principles

| Principle | Implementation |
|-----------|----------------|
| **Verify explicitly** | Always authenticate/authorize |
| **Least privilege** | Minimal necessary permissions |
| **Assume breach** | Segment, encrypt, detect |

### Identity Patterns

#### Managed Identity
Eliminate credential management with Azure AD-backed identity.

```json
{
  "type": "Microsoft.Web/sites",
  "identity": {
    "type": "SystemAssigned"
  }
}
```

**Use cases:**
- App Service → Key Vault secrets
- Azure Functions → Storage access
- VMs → Database connections

#### RBAC Best Practices

| Practice | Rationale |
|----------|-----------|
| Use built-in roles first | Custom roles add complexity |
| Scope to resource group | Not subscription (too broad) |
| Use groups, not users | Easier lifecycle management |
| Regular access reviews | Remove stale permissions |

### Network Security

#### Private Endpoints
Keep traffic on Azure backbone, off public internet.

```bicep
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: 'pe-storage'
  properties: {
    subnet: { id: subnetId }
    privateLinkServiceConnections: [{
      name: 'plsc-storage'
      properties: {
        privateLinkServiceId: storageAccountId
        groupIds: ['blob']
      }
    }]
  }
}
```

#### Network Security Groups (NSG)
Default deny, explicit allow.

| Priority | Description |
|----------|-------------|
| 100-200 | Allow known good traffic |
| 300-400 | Deny known bad traffic |
| 4096 | Default deny all |

### Security Checklist

- [ ] Managed identities used (no stored credentials)
- [ ] Key Vault for secrets/certificates
- [ ] Private endpoints for PaaS services
- [ ] NSG/firewall rules explicit deny-by-default
- [ ] TLS 1.2+ enforced
- [ ] Microsoft Defender for Cloud enabled
- [ ] Diagnostic settings → Log Analytics

---

## Module 3: Cost Optimization Patterns

### Design for Cost

| Strategy | Impact |
|----------|--------|
| **Right-size** | Match SKU to actual workload |
| **Reserved Instances** | 1-3 year commitment = 40-72% savings |
| **Spot VMs** | 90% discount for interruptible workloads |
| **Auto-shutdown** | Dev/test VMs off at night |
| **Serverless** | Pay per execution, not idle time |

### Cost-Aware Architecture

#### Compute Selection Matrix

| Workload Type | Recommended | Why |
|---------------|-------------|-----|
| Steady-state web | App Service Premium | Predictable, manageable |
| Event-driven | Azure Functions | Pay per execution |
| Batch processing | Container Apps + KEDA | Scale to zero |
| Big compute | Spot VMs + Batch | Massive savings |
| Dev/test | B-series VMs | Burstable, cheap |

#### Storage Tiers

| Tier | Use Case | Cost/GB/month |
|------|----------|---------------|
| Hot | Frequently accessed | ~$0.02 |
| Cool | Infrequent (30+ days) | ~$0.01 |
| Archive | Rarely accessed | ~$0.002 |

**Lifecycle management**: Auto-tier blobs based on last access.

### Cost Monitoring

```kusto
// Azure Resource Graph - find expensive resources
resources
| where type =~ 'Microsoft.Compute/virtualMachines'
| extend vmSize = properties.hardwareProfile.vmSize
| project name, resourceGroup, vmSize, location
| order by vmSize desc
```

### Cost Checklist

- [ ] Azure Advisor recommendations reviewed
- [ ] Reserved Instances for predictable workloads
- [ ] Auto-shutdown for non-prod
- [ ] Right-sized based on actual utilization
- [ ] Storage lifecycle policies configured
- [ ] Cost alerts and budgets set
- [ ] Orphaned resources cleaned up

---

## Module 4: Operational Excellence Patterns

### Infrastructure as Code

| Tool | Best For |
|------|----------|
| **Bicep** | Azure-native, declarative |
| **Terraform** | Multi-cloud, state management |
| **ARM** | Legacy, avoid for new work |
| **Pulumi** | Developers who prefer code |

#### Bicep Best Practices

```bicep
// Use parameters with descriptions and constraints
@description('The environment name')
@allowed(['dev', 'staging', 'prod'])
param environment string

// Use variables for derived values
var resourcePrefix = 'app-${environment}'

// Use modules for reusability
module storage 'modules/storage.bicep' = {
  name: 'storage-${environment}'
  params: {
    prefix: resourcePrefix
    location: location
  }
}
```

### Observability Stack

| Layer | Service | Purpose |
|-------|---------|---------|
| Logs | Log Analytics | Centralized logging |
| Metrics | Azure Monitor | Performance data |
| Traces | Application Insights | Distributed tracing |
| Alerts | Azure Alerts | Proactive notification |
| Dashboards | Azure Workbooks | Visualization |

#### Essential Diagnostic Settings

```bicep
resource diagnostics 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  scope: appService
  name: 'diag-appservice'
  properties: {
    workspaceId: logAnalyticsId
    logs: [
      { category: 'AppServiceHTTPLogs', enabled: true }
      { category: 'AppServiceConsoleLogs', enabled: true }
    ]
    metrics: [
      { category: 'AllMetrics', enabled: true }
    ]
  }
}
```

### Operational Checklist

- [ ] IaC for all resources (Bicep/Terraform)
- [ ] CI/CD pipelines for deployment
- [ ] Diagnostic settings to Log Analytics
- [ ] Application Insights integrated
- [ ] Alerts for critical metrics
- [ ] Runbooks for common operations
- [ ] Chaos engineering tests scheduled

---

## Module 5: Performance Efficiency Patterns

### Scalability Patterns

#### Horizontal Scaling (Scale Out)
Add more instances, not bigger instances.

| Service | Scaling Mechanism |
|---------|-------------------|
| App Service | Autoscale rules |
| Azure Functions | Event-driven automatic |
| AKS | Horizontal Pod Autoscaler + Cluster Autoscaler |
| VMSS | Autoscale rules |

#### Caching Strategy

| Cache Type | Use Case | Service |
|------------|----------|---------|
| CDN | Static content | Azure Front Door |
| Distributed | Session, computed data | Azure Cache for Redis |
| Local | Hot data | In-memory |

### Performance Patterns

#### CQRS (Command Query Responsibility Segregation)
Separate read and write models for optimization.

```
Write Path: Web App → Cosmos DB (write-optimized)
                 ↓ Change Feed
Read Path: Azure Search ← Cosmos DB (indexed, query-optimized)
```

#### Event Sourcing
Store events, not state. Rebuild state from event stream.

**Benefits:**
- Complete audit trail
- Temporal queries
- Easy scaling

### Database Performance

| Pattern | When to Use |
|---------|-------------|
| **Read replicas** | Read-heavy workloads |
| **Sharding** | Data exceeds single node |
| **Connection pooling** | Many short-lived connections |
| **Indexing strategy** | Query performance issues |

### Performance Checklist

- [ ] Autoscaling configured and tested
- [ ] CDN for static content
- [ ] Redis cache for hot data
- [ ] Database indexes reviewed
- [ ] Connection pooling enabled
- [ ] Load testing completed
- [ ] Performance baselines established

---

## Reference Architectures

### Web Application (Standard)

```
Internet → Front Door (CDN, WAF) → App Service
                                    ↓
                              Azure SQL + Redis Cache
                                    ↓
                              Key Vault, Storage
```

### Microservices (Azure Kubernetes Service)

```
Internet → API Management → AKS Ingress
                              ↓
                        Service Mesh (pods)
                              ↓
                        Cosmos DB, Service Bus
                              ↓
                        Azure Monitor, Key Vault
```

### Serverless (Event-Driven)

```
Event Sources → Event Grid → Azure Functions
                                   ↓
                              Cosmos DB, Storage
                                   ↓
                              Logic Apps (orchestration)
```

---

## Quick Reference

### SKU Selection Guide

| Tier | CPU | Memory | Use Case |
|------|-----|--------|----------|
| B-series | Burstable | Variable | Dev/test |
| D-series | General | Balanced | Most production |
| E-series | Memory-optimized | High | In-memory databases |
| F-series | Compute-optimized | Low | CPU-intensive |

### Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Monolithic deployment | All or nothing | Microservices or modular |
| Hardcoded config | Environment-specific | App Configuration, Key Vault |
| Single region | No DR | Multi-region with Traffic Manager |
| Over-provisioned "just in case" | Wasted cost | Right-size + autoscale |
| No IaC | Drift, manual errors | Bicep/Terraform everything |

---

## Module 6: MCP Tool Integration

### Required Extensions & MCP Servers

| Component | ID / Name | Purpose |
|-----------|-----------|--------|
| **VS Code Extension** | `ms-azuretools.vscode-azure-github-copilot` | Azure GitHub Copilot integration |
| **VS Code Extension** | `ms-azuretools.vscode-azureresourcegroups` | Azure resource management |
| **VS Code Extension** | `ms-vscode.azure-account` | Azure authentication |
| **MCP Server** | `azure-mcp` | 40+ Azure tools (cloudarchitect, docs, services) |

**Installation**:
```bash
# VS Code Extensions
code --install-extension ms-azuretools.vscode-azure-github-copilot
code --install-extension ms-azuretools.vscode-azureresourcegroups
code --install-extension ms-vscode.azure-account

# MCP Server (via VS Code settings.json or mcp.json)
# Enabled via chat.mcp.gallery.enabled = true
```

### Fallback Patterns (When MCP Unavailable)

If Azure MCP tools are not available, use these alternatives:

| MCP Tool | Fallback Approach |
|----------|-------------------|
| `cloudarchitect` | Use WAF Assessment: https://aka.ms/waf-assessment |
| `documentation` | Search https://learn.microsoft.com/azure/architecture |
| `get_bestpractices` | Reference Azure Architecture Center patterns |
| Service-specific tools | Use Azure Portal or `az` CLI directly |

**Manual Architecture Design Process**:
1. Review WAF pillars checklist in Module 1-5
2. Use Azure Architecture Center reference architectures
3. Validate with Azure Advisor in portal
4. Apply patterns from this skill's modules

### Available Azure MCP Tools

Alex has access to 40+ Azure MCP tools for real-time architecture assistance:

| Category | Tools | Use Cases |
|----------|-------|-----------|
| **Architecture Design** | `mcp_azure_mcp_cloudarchitect` | Interactive architecture design, WAF guidance |
| **Documentation** | `mcp_azure_mcp_documentation` | Search Azure docs, best practices |
| **Best Practices** | `mcp_azure_mcp_get_bestpractices` | Code gen, deployment, Functions patterns |
| **Compute** | `mcp_azure_mcp_aks`, `mcp_azure_mcp_appservice`, `mcp_azure_mcp_functionapp` | Container orchestration, web apps, serverless |
| **Data** | `mcp_azure_mcp_cosmos`, `mcp_azure_mcp_sql`, `mcp_azure_mcp_postgres` | Database recommendations |
| **Security** | `mcp_azure_mcp_keyvault`, `mcp_azure_mcp_role` | Secrets management, RBAC |
| **Monitoring** | `mcp_azure_mcp_monitor`, `mcp_azure_mcp_applicationinsights` | Observability setup |
| **DevOps** | `mcp_azure_mcp_deploy`, `mcp_azure_mcp_azd` | Deployment automation |

### Cloud Architect Tool

The `mcp_azure_mcp_cloudarchitect` tool provides **interactive guided architecture design**:

```text
Invocation → Ask about user/company → 
  Gather requirements → 
    Build architecture by tier → 
      Present with ASCII diagrams

Architecture Tiers:
├── Infrastructure (VNets, VMs, Load Balancers)
├── Platform (App Service, AKS, Functions)
├── Application (Logic Apps, API Management)
├── Data (SQL, Cosmos, Storage)
├── Security (Key Vault, WAF, DDoS)
└── Operations (Monitor, Log Analytics)
```

The tool tracks:
- **Explicit requirements** — Directly stated by user
- **Implicit requirements** — Inferred from context
- **Assumed requirements** — Industry/domain defaults

### Best Practices Tool

Use `mcp_azure_mcp_get_bestpractices` with these resource/action combinations:

| Resource | Actions |
|----------|---------|
| `codegen` | `all` — Code generation patterns |
| `deployment` | `all` — Deployment best practices |
| `functions` | `all` — Azure Functions patterns |
| `swa` | `all` — Static Web App guidance |
| `coding-agent` | `all` — MCP setup for repos |

### When to Use MCP Tools

| Scenario | Tool | Why |
|----------|------|-----|
| "Design new Azure solution" | `cloudarchitect` | Interactive, pillar-aligned |
| "What's the best way to..." | `documentation` | Search official docs |
| "Generate Azure code" | `get_bestpractices` + specific tools | Current patterns |
| "Cost optimization review" | `cloudarchitect` + `monitor` | Full picture |
| "Security assessment" | `keyvault` + `role` + `documentation` | Multi-tool analysis |

### Example: Interactive Architecture Session

```
User: "Design a solution for a retail e-commerce platform"

Alex invokes: mcp_azure_mcp_cloudarchitect with:
  - intent: "Design e-commerce architecture"
  - nextQuestionNeeded: true
  - state: {initial}

Tool asks: "What's your role and company size?"
User: "CTO of a mid-size retailer"

Tool continues gathering:
  - Expected traffic patterns
  - Data residency requirements  
  - Budget constraints
  - Compliance needs (PCI-DSS for payments)

Tool outputs:
  - Component table with SKU recommendations
  - ASCII architecture diagram
  - WAF pillar alignment
  - Cost estimation
```

---

## Activation Patterns

| Trigger | Response |
|---------|----------|
| "Azure architecture", "cloud design" | Full skill activation |
| "reliability", "high availability", "resilience" | Module 1 |
| "security", "zero trust", "identity" | Module 2 |
| "cost", "optimize", "savings" | Module 3 |
| "IaC", "Bicep", "observability" | Module 4 |
| "performance", "scaling", "caching" | Module 5 |
| "MCP", "cloud architect tool", "Azure tools" | Module 6 |
| "design architecture interactively" | Invoke cloudarchitect tool |

---

*Skill updated: 2026-02-14 | Category: Cloud/Infrastructure | Status: Active | MCP-Enhanced: Yes*

---

## Synapses

- [.github/skills/observability/SKILL.md] (High, Enables, Bidirectional) - "Monitoring and observability patterns"
- [.github/skills/project-scaffolding/SKILL.md] (Medium, Uses, Forward) - "Infrastructure-as-code project setup"
- [.github/instructions/empirical-validation.instructions.md] (Medium, Validates, Forward) - "Architecture decisions require evidence"
