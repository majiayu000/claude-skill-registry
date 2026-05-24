---
name: deploying-on-azure
description: Design and implement Azure cloud architectures using best practices for compute, storage, databases, AI services, networking, and governance. Use when building applications on Microsoft Azure or migrating workloads to Azure cloud platform.
---

# Azure Patterns

Design and implement Azure cloud architectures following Microsoft's Well-Architected Framework and best practices for service selection, cost optimization, and security.

## When to Use

Use this skill when:
- Designing new applications for Azure cloud
- Selecting Azure compute services (Container Apps, AKS, Functions, App Service)
- Architecting storage solutions (Blob Storage, Files, Cosmos DB)
- Integrating Azure OpenAI or Cognitive Services
- Implementing messaging patterns (Service Bus, Event Grid, Event Hubs)
- Designing secure networks with Private Endpoints
- Applying Azure governance and compliance policies
- Optimizing Azure costs and performance

## Core Concepts

### Service Selection Philosophy

Azure offers 200+ services. Choose based on:
1. **Managed vs. IaaS** - Prefer fully managed services (lower operational burden)
2. **Cost Model** - Consumption vs. dedicated capacity
3. **Integration Requirements** - Microsoft 365, Active Directory, hybrid cloud
4. **Control vs. Simplicity** - More control = more operational overhead

### Azure Well-Architected Framework (Five Pillars)

| Pillar | Focus | Key Practices |
|--------|-------|---------------|
| **Cost Optimization** | Maximize value within budget | Reserved Instances, auto-scaling, lifecycle management |
| **Operational Excellence** | Run reliable systems | Azure Policy, automation, monitoring |
| **Performance Efficiency** | Scale to meet demand | Autoscaling, caching, CDN |
| **Reliability** | Recover from failures | Availability Zones, multi-region, backup |
| **Security** | Protect data and assets | Managed Identity, Private Endpoints, Key Vault |

Reference `references/well-architected.md` for detailed pillar implementation patterns.

## Compute Service Selection

### Decision Framework

```
Container-based workload?
  YES → Need Kubernetes control plane?
          YES → Azure Kubernetes Service (AKS)
          NO → Azure Container Apps (recommended)
  NO → Event-driven function?
         YES → Azure Functions
         NO → Web application?
                YES → Azure App Service
                NO → Legacy/specialized → Virtual Machines
```

### Service Comparison

| Service | Best For | Pricing Model | Operational Overhead |
|---------|----------|---------------|---------------------|
| **Container Apps** | Microservices, APIs, background jobs | Consumption or dedicated | Low |
| **AKS** | Complex K8s workloads, service mesh | Node-based | High |
| **Functions** | Event-driven, short tasks (<10 min) | Consumption or premium | Low |
| **App Service** | Web apps, simple APIs | Dedicated plans | Low |
| **Virtual Machines** | Legacy apps, specialized software | VM-based | High |

**Recommendation:** Start with Azure Container Apps for 80% of containerized workloads (simpler and cheaper than AKS).

Reference `references/compute-services.md` for detailed comparison with Bicep and Terraform examples.

## Storage Architecture

### Blob Storage Tier Selection

| Tier | Access Pattern | Cost/GB/Month | Minimum Storage Duration |
|------|---------------|---------------|--------------------------|
| **Hot** | Daily access | $0.018 | None |
| **Cool** | <1/month access | $0.010 | 30 days |
| **Cold** | <90 days access | $0.0045 | 90 days |
| **Archive** | Rare access | $0.00099 | 180 days |

**Pattern:** Use lifecycle management policies to automatically move data to lower-cost tiers.

### Storage Service Decision

```
File system interface required?
  YES → Protocol?
          SMB → Azure Files (or NetApp Files for high performance)
          NFS → Azure Files (NFS 4.1)
  NO → Object storage → Blob Storage
       Block storage → Managed Disks (Standard/Premium SSD/Ultra)
       Analytics → Data Lake Storage Gen2
```

Reference `references/storage-patterns.md` for lifecycle policies, redundancy options, and performance tuning.

## Database Service Selection

### Decision Framework

```
Relational data?
  YES → SQL Server compatible?
          YES → Need VM-level access?
                  YES → SQL Managed Instance
                  NO → Azure SQL Database
          NO → Open source?
                 PostgreSQL → PostgreSQL Flexible Server
                 MySQL → MySQL Flexible Server
  NO → Data model?
         Document/JSON → Cosmos DB (NoSQL API)
         Graph → Cosmos DB (Gremlin API)
         Wide-column → Cosmos DB (Cassandra API)
         Key-value cache → Azure Cache for Redis
         Time-series → Azure Data Explorer
```

### Cosmos DB Consistency Levels

| Level | Use Case | Latency | Throughput |
|-------|----------|---------|------------|
| **Strong** | Financial transactions, inventory | Highest | Lowest |
| **Bounded Staleness** | Real-time leaderboards with acceptable lag | High | Low |
| **Session** | Shopping carts, user sessions (default) | Medium | Medium |
| **Consistent Prefix** | Social feeds, IoT telemetry | Low | High |
| **Eventual** | Analytics, ML training data | Lowest | Highest |

Reference `references/database-selection.md` for capacity planning, indexing strategies, and migration patterns.

## AI and Machine Learning Integration

### Azure OpenAI Service

**Use Cases:**
- Chatbots and conversational AI (GPT-4)
- Content generation and summarization
- Semantic search with embeddings (RAG pattern)
- Code generation and completion
- Function calling for structured outputs

**Key Advantages:**
- Enterprise data privacy (no model training on customer data)
- Regional deployment for data residency
- Microsoft enterprise SLAs
- Built-in content filtering

**Integration Pattern:**
```python
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = AzureOpenAI(
    azure_endpoint="https://myopenai.openai.azure.com",
    azure_ad_token_provider=token_provider,
    api_version="2024-02-15-preview"
)

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Other AI Services

| Service | Purpose | Common Use Cases |
|---------|---------|------------------|
| **Cognitive Services** | Pre-built AI models | Vision, Speech, Language, Decision |
| **Azure Machine Learning** | Custom model training | MLOps, model deployment, feature engineering |
| **Azure AI Search** | Semantic search engine | RAG patterns, document search |

Reference `references/ai-integration.md` for RAG architecture, function calling, and fine-tuning patterns.

## Messaging and Integration

### Service Selection Matrix

| Service | Pattern | Message Size | Ordering | Transactions | Best For |
|---------|---------|--------------|----------|--------------|----------|
| **Service Bus** | Queue/Topic | 256 KB - 100 MB | Yes (sessions) | Yes | Enterprise messaging |
| **Event Grid** | Pub/Sub | 1 MB | No | No | Event-driven architectures |
| **Event Hubs** | Streaming | 1 MB | Yes (partitions) | No | Big data ingestion, telemetry |
| **Storage Queues** | Simple queue | 64 KB | No | No | Async work, <500k msgs/sec |

**When to Use What:**
- **Service Bus:** Reliable messaging with transactions (e.g., order processing)
- **Event Grid:** React to Azure resource events (e.g., blob created, VM stopped)
- **Event Hubs:** High-throughput streaming (e.g., IoT telemetry, application logs)

Reference `references/messaging-patterns.md` for implementation examples, retry policies, and dead-letter handling.

## Networking Architecture

### Private Endpoints vs. Service Endpoints

| Aspect | Private Endpoint | Service Endpoint |
|--------|------------------|------------------|
| **Security Model** | Private IP in VNet | Optimized route to public endpoint |
| **Data Exfiltration Protection** | Yes (network-isolated) | Limited (service firewall only) |
| **Cost** | ~$7.30/month per endpoint | Free |
| **Recommendation** | Production workloads | Dev/test environments |

**Best Practice:** Use Private Endpoints for all PaaS services in production (treat public endpoints as anti-pattern).

### Hub-and-Spoke Topology

**Components:**
- **Hub VNet:** Shared services (Azure Firewall, VPN Gateway, Private Endpoints)
- **Spoke VNets:** Application workloads (isolated per environment or team)
- **VNet Peering:** Low-latency connectivity between hub and spokes

**Benefits:**
- Centralized security (firewall, DNS)
- Cost optimization (shared egress)
- Simplified governance

Reference `references/networking-architecture.md` for hub-spoke Bicep templates, NSG patterns, and DNS configuration.

## Identity and Access Management

### Managed Identity Pattern

**Always use Managed Identity instead of:**
- Connection strings in code
- Storage account keys
- Service principal credentials
- API keys

**System-Assigned vs. User-Assigned:**

| Type | Lifecycle | Use Case |
|------|-----------|----------|
| **System-Assigned** | Tied to resource | Single resource needs access |
| **User-Assigned** | Independent | Multiple resources share identity |

**Example Flow:**
1. Enable Managed Identity on Container App
2. Grant identity access to Key Vault (RBAC or Access Policy)
3. Application authenticates automatically (no credentials)

```python
from azure.identity import DefaultAzureCredential

# Works automatically with Managed Identity
credential = DefaultAzureCredential()
keyvault_client = SecretClient(vault_url="...", credential=credential)
```

### Azure RBAC Best Practices

- Use built-in roles when possible (Owner, Contributor, Reader)
- Apply least privilege principle
- Assign roles at resource group level (not subscription)
- Use Azure AD groups for user management
- Audit role assignments regularly

Reference `references/identity-access.md` for Entra ID integration, Conditional Access policies, and B2C patterns.

## Governance and Compliance

### Azure Policy for Guardrails

**Common Policy Patterns:**
- Require tags on all resources (Environment, Owner, CostCenter)
- Restrict allowed Azure regions
- Enforce TLS 1.2 minimum
- Require Private Endpoints for storage accounts
- Deny public IP addresses on VMs

**Policy Effects:**
- **Deny:** Block non-compliant resource creation
- **Audit:** Log non-compliance but allow creation
- **DeployIfNotExists:** Auto-remediate missing configurations
- **Modify:** Change resource properties during deployment

### Cost Management

**Optimization Strategies:**

| Pattern | Savings | Use Case |
|---------|---------|----------|
| **Reserved Instances (1-year)** | 40-50% | Steady-state workloads (databases, VMs) |
| **Reserved Instances (3-year)** | 60-70% | Long-term commitments |
| **Spot VMs** | Up to 90% | Fault-tolerant batch processing |
| **Auto-shutdown** | Variable | Dev/test resources (off-hours) |
| **Storage lifecycle policies** | 50-90% | Move to Cool/Archive tiers |

**Monitoring:**
- Set budgets and alerts in Azure Cost Management
- Review Azure Advisor cost recommendations weekly
- Tag resources for cost allocation
- Use FinOps Toolkit for Power BI dashboards

Reference `references/governance-compliance.md` for Azure Landing Zones, Policy definitions, and Blueprints.

## Infrastructure as Code

### Tool Selection

| Tool | Best For | Azure Integration | Multi-Cloud |
|------|----------|-------------------|-------------|
| **Bicep** | Azure-native projects | Excellent (official) | No |
| **Terraform** | Multi-cloud environments | Good (azurerm provider) | Yes |
| **Pulumi** | Developer-first approach | Good (native SDK) | Yes |
| **Azure CLI** | Scripts and automation | Excellent | No |

**Recommendation:**
- Use **Bicep** for Azure-only infrastructure (best Azure integration, native type safety)
- Use **Terraform** for multi-cloud or existing Terraform shops
- Use **Azure CLI** for quick scripts and CI/CD automation

### Bicep Best Practices

- Use parameter files for environment-specific values
- Leverage Azure Verified Modules (AVM) for tested patterns
- Organize by resource lifecycle (networking, data, compute)
- Use symbolic names (not string interpolation)
- Enable linting and validation in CI/CD

Reference Bicep and Terraform examples in `examples/bicep/` and `examples/terraform/` directories.

## Security Best Practices

### Essential Security Controls

| Control | Implementation | Priority |
|---------|---------------|----------|
| **Managed Identity** | Enable on all compute resources | Critical |
| **Private Endpoints** | All PaaS services in production | Critical |
| **Key Vault** | Store secrets, keys, certificates | Critical |
| **Network Segmentation** | NSGs, application security groups | High |
| **Microsoft Defender** | Enable for all resource types | High |
| **Azure Policy** | Preventive controls | High |
| **Just-In-Time Access** | VMs and privileged access | Medium |

### Defense-in-Depth Layers

1. **Network:** Private Endpoints, NSGs, Azure Firewall
2. **Identity:** Entra ID, Managed Identity, Conditional Access
3. **Application:** Web Application Firewall, API Management
4. **Data:** Encryption at rest, encryption in transit (TLS 1.2+)
5. **Monitoring:** Microsoft Defender, Azure Monitor, Sentinel

Reference `references/security-architecture.md` (see also `security-hardening` and `auth-security` skills).

## Cost Estimation

### Pricing Considerations

**Compute:**
- Container Apps: ~$60/month (1 vCPU, 2GB RAM, 24/7)
- AKS: ~$400/month (3-node D4s_v5 cluster)
- App Service P1v3: ~$145/month (2 vCPU, 8GB RAM)
- Functions Consumption: ~$0.20 per 1M executions

**Storage:**
- Blob Hot: $0.018/GB/month
- Blob Cool: $0.010/GB/month
- Blob Archive: $0.00099/GB/month
- Managed Disks Premium SSD: $0.15/GB/month

**Database:**
- Azure SQL Database (2 vCores): ~$280/month
- Cosmos DB Serverless: Pay per RU consumed
- PostgreSQL Flexible (2 vCores): ~$125/month

**Use Azure Pricing Calculator:** https://azure.microsoft.com/pricing/calculator/

## Quick Reference Tables

### Compute Service Decision Matrix

| If You Need... | Choose |
|----------------|--------|
| Kubernetes features (CRDs, operators) | Azure Kubernetes Service |
| Microservices without K8s complexity | Azure Container Apps |
| Event-driven functions (<10 min) | Azure Functions |
| Traditional web app (Node, .NET, Python) | Azure App Service |
| Batch processing, HPC | Azure Batch or VM Scale Sets |
| Legacy application migration | Virtual Machines |

### Storage Service Decision Matrix

| If You Need... | Choose |
|----------------|--------|
| SMB file shares | Azure Files |
| NFS file shares | Azure Files (NFS 4.1) |
| Object storage (images, backups) | Blob Storage |
| High-performance file storage | Azure NetApp Files |
| Block storage for VMs | Managed Disks |
| Big data analytics | Data Lake Storage Gen2 |

### Database Service Decision Matrix

| If You Need... | Choose |
|----------------|--------|
| SQL Server features (T-SQL, SQL Agent) | Azure SQL Database or Managed Instance |
| PostgreSQL | PostgreSQL Flexible Server |
| MySQL | MySQL Flexible Server |
| Global distribution, multi-model | Cosmos DB |
| In-memory cache | Azure Cache for Redis |
| Graph database | Cosmos DB (Gremlin API) |
| Time-series data | Azure Data Explorer |

## Integration with Other Skills

- **infrastructure-as-code:** Implement Azure patterns using Bicep or Terraform
- **kubernetes-operations:** AKS-specific configuration and operations
- **deploying-applications:** Container Apps and App Service deployment
- **building-ci-pipelines:** Azure DevOps and GitHub Actions integration
- **auth-security:** Entra ID authentication and authorization patterns
- **observability:** Azure Monitor and Application Insights
- **ai-chat:** Azure OpenAI Service for chat applications
- **databases-nosql:** Cosmos DB implementation details
- **secret-management:** Azure Key Vault integration patterns

## Reference Documentation

For detailed implementation guidance, see:

- **`references/compute-services.md`** - Container Apps, AKS, Functions, App Service with Bicep/Terraform
- **`references/storage-patterns.md`** - Blob Storage, Files, Disks, lifecycle management
- **`references/database-selection.md`** - SQL Database, Cosmos DB, PostgreSQL patterns
- **`references/ai-integration.md`** - Azure OpenAI, RAG architecture, function calling
- **`references/messaging-patterns.md`** - Service Bus, Event Grid, Event Hubs examples
- **`references/networking-architecture.md`** - Hub-spoke, Private Endpoints, DNS configuration
- **`references/identity-access.md`** - Entra ID, Managed Identity, RBAC
- **`references/governance-compliance.md`** - Azure Policy, Landing Zones, cost optimization
- **`references/well-architected.md`** - Five pillars implementation guide

## Code Examples

Working examples available in:

- **`examples/bicep/`** - Infrastructure templates (Container Apps, AKS, networking, databases)
- **`examples/terraform/`** - Multi-cloud IaC examples
- **`examples/sdk/python/`** - Python SDK integration (OpenAI, Managed Identity, messaging)
- **`examples/sdk/typescript/`** - TypeScript SDK examples

## Additional Resources

- Azure Architecture Center: https://learn.microsoft.com/azure/architecture/
- Azure Well-Architected Framework: https://learn.microsoft.com/azure/well-architected/
- Azure Verified Modules: https://aka.ms/avm
- Azure Charts (Service Comparison): https://azurecharts.com/
- Azure Updates: https://azure.microsoft.com/updates/
