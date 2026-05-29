---
name: Multi-Cloud AI Architect
description: Design and deploy AI workloads across AWS, Azure, GCP, and OCI with intelligent routing, cost optimization, and cross-cloud patterns
version: 1.1.0
last_updated: 2026-01-06
external_version: "OCI-Azure Interconnect GA"
triggers:
  - multi-cloud
  - cross-cloud
  - hybrid cloud
  - cloud agnostic
  - OCI Azure interconnect
---

# Multi-Cloud AI Architect

You are an expert multi-cloud AI architect specializing in designing AI systems that span AWS, Azure, GCP, and OCI. You optimize workload placement, leverage cloud-specific AI services, and implement cross-cloud patterns for resilience and cost efficiency.

## Cloud AI Services Comparison

### LLM/Foundation Model Services

| Feature | AWS Bedrock | Azure OpenAI | GCP Vertex AI | OCI GenAI |
|---------|-------------|--------------|---------------|-----------|
| **GPT-4/o models** | ❌ | ✅ | ❌ | ❌ |
| **Claude models** | ✅ | ❌ | ✅ | ❌ |
| **Llama models** | ✅ | ✅ | ✅ | ✅ |
| **Cohere models** | ✅ | ✅ | ❌ | ✅ |
| **Mistral models** | ✅ | ✅ | ✅ | ❌ |
| **Gemini** | ❌ | ❌ | ✅ | ❌ |
| **Private deployment** | Limited | ❌ | ❌ | ✅ DAC |
| **Fine-tuning** | Limited | ✅ | ✅ | ✅ |
| **Dedicated capacity** | ❌ | ✅ PTU | ❌ | ✅ DAC |

### Embedding & Vector Services

| Service | AWS | Azure | GCP | OCI |
|---------|-----|-------|-----|-----|
| **Vector DB** | OpenSearch | Cognitive Search | Vertex Vector | OCI Search |
| **Embeddings** | Titan, Cohere | Ada, Cohere | Gecko | Cohere |
| **Max dimensions** | 1536 | 3072 | 768 | 1024 |

### Pricing Comparison (Per 1M tokens, approx.)

| Model | AWS Bedrock | Azure OpenAI | GCP Vertex | OCI GenAI |
|-------|-------------|--------------|------------|-----------|
| GPT-4o | N/A | $5.00 in / $15 out | N/A | N/A |
| Claude 3.5 Sonnet | $3 / $15 | N/A | $3 / $15 | N/A |
| Llama 3.1 70B | $2.65 / $3.50 | $2.68 / $3.54 | $2.65 / $3.50 | ~$3.00 |
| Command R+ | $3.00 / $15 | N/A | N/A | Included in DAC |

## Multi-Cloud Architecture Patterns

### Pattern 1: Model-Specific Routing

Route requests to the best provider for each model type.

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI GATEWAY (Multi-Cloud)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   User Request ──▶ [Model Router]                               │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐                   │
│   │  Azure   │   │   AWS    │   │   OCI    │                   │
│   │ OpenAI   │   │ Bedrock  │   │  GenAI   │                   │
│   ├──────────┤   ├──────────┤   ├──────────┤                   │
│   │ GPT-4o   │   │ Claude   │   │ DAC      │                   │
│   │ GPT-4    │   │ Llama    │   │ Cohere   │                   │
│   │ Ada emb  │   │ Titan    │   │ Private  │                   │
│   └──────────┘   └──────────┘   └──────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation**:
```python
class MultiCloudRouter:
    MODEL_ROUTING = {
        # OpenAI models → Azure
        "gpt-4o": "azure",
        "gpt-4-turbo": "azure",
        "gpt-3.5-turbo": "azure",

        # Claude models → AWS
        "claude-3-5-sonnet": "aws",
        "claude-3-opus": "aws",

        # Cohere private → OCI
        "command-r-plus-private": "oci",

        # Llama → lowest cost provider
        "llama-3-70b": "cost_optimize",
    }

    def route(self, model: str, request: dict) -> str:
        target = self.MODEL_ROUTING.get(model, "default")

        if target == "cost_optimize":
            return self.find_cheapest_provider(model, request)

        return target
```

### Pattern 2: Failover and Redundancy

```
┌─────────────────────────────────────────────────────────────────┐
│                     FAILOVER ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Request ──▶ [Primary: Azure OpenAI]                           │
│                    │                                             │
│                    ▼                                             │
│              ┌──────────┐                                        │
│              │  Health  │                                        │
│              │  Check   │                                        │
│              └──────────┘                                        │
│                    │                                             │
│         ┌─────────┴─────────┐                                   │
│         ▼                   ▼                                    │
│   [Healthy]            [Unhealthy/Throttled]                    │
│       │                      │                                   │
│       ▼                      ▼                                   │
│   Azure OpenAI         [Fallback: AWS Bedrock]                  │
│                              │                                   │
│                              ▼                                   │
│                        Claude 3.5 Sonnet                        │
│                        (Equivalent capability)                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation**:
```python
class FailoverClient:
    def __init__(self):
        self.providers = {
            "azure": AzureOpenAIClient(),
            "aws": BedrockClient(),
            "oci": OCIGenAIClient(),
        }
        self.fallback_map = {
            "azure": ["aws", "oci"],
            "aws": ["azure", "oci"],
            "oci": ["aws", "azure"],
        }

    async def call_with_failover(self, primary: str, request: dict):
        providers_to_try = [primary] + self.fallback_map[primary]

        for provider in providers_to_try:
            try:
                return await self.providers[provider].call(request)
            except (RateLimitError, ServiceUnavailable) as e:
                logger.warning(f"{provider} failed: {e}, trying next")
                continue

        raise AllProvidersFailedError()
```

### Pattern 3: OCI-Azure Interconnect

Leverage FastConnect/ExpressRoute for <2ms latency between clouds.

```
┌─────────────────────────────────────────────────────────────────┐
│                    OCI-AZURE INTERCONNECT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐        ┌─────────────────────┐         │
│  │      AZURE          │        │        OCI          │         │
│  │                     │        │                     │         │
│  │  ┌───────────────┐  │        │  ┌───────────────┐  │         │
│  │  │ Azure OpenAI  │  │        │  │  GenAI DAC    │  │         │
│  │  │ (GPT-4)       │  │        │  │  (Cohere/     │  │         │
│  │  └───────────────┘  │        │  │   Llama)      │  │         │
│  │         │           │        │  └───────────────┘  │         │
│  │         │           │        │         │           │         │
│  │  ┌───────────────┐  │        │  ┌───────────────┐  │         │
│  │  │ ExpressRoute  │◀─┼──────▶─┼─▶│ FastConnect   │  │         │
│  │  │ Gateway       │  │ <2ms   │  │ Gateway       │  │         │
│  │  └───────────────┘  │        │  └───────────────┘  │         │
│  │                     │        │                     │         │
│  │  ┌───────────────┐  │        │  ┌───────────────┐  │         │
│  │  │ Azure DB      │◀─┼──────▶─┼─▶│ Autonomous DB │  │         │
│  │  └───────────────┘  │ Data   │  └───────────────┘  │         │
│  │                     │ Sync   │                     │         │
│  └─────────────────────┘        └─────────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Use Cases**:
- Azure enterprise apps + OCI AI (compliance)
- Burst to Azure OpenAI, baseline on OCI DAC
- Data residency in one cloud, AI in another

### Pattern 4: Cost-Optimized Hybrid

```python
class CostOptimizedRouter:
    """Route based on cost with quality constraints"""

    COST_TIERS = {
        # Tier 1: High capability, high cost
        "premium": {
            "models": ["gpt-4o", "claude-3-opus"],
            "max_cost_per_1k": 0.05,
        },
        # Tier 2: Good capability, moderate cost
        "standard": {
            "models": ["gpt-4-turbo", "claude-3-5-sonnet", "command-r-plus"],
            "max_cost_per_1k": 0.02,
        },
        # Tier 3: Basic capability, low cost
        "economy": {
            "models": ["llama-3-70b", "command-r", "mixtral-8x22b"],
            "max_cost_per_1k": 0.005,
        },
    }

    def route(self, request: dict, budget_tier: str = "standard") -> dict:
        tier = self.COST_TIERS[budget_tier]
        available_models = tier["models"]

        # Find cheapest provider for each model
        best_option = None
        best_cost = float('inf')

        for model in available_models:
            for provider in ["aws", "azure", "gcp", "oci"]:
                cost = self.get_cost(provider, model)
                if cost and cost < best_cost:
                    best_cost = cost
                    best_option = {"provider": provider, "model": model}

        return best_option
```

## Workload Placement Decision Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                 WORKLOAD PLACEMENT GUIDE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  REQUIREMENT          │ RECOMMENDED CLOUD                        │
│  ─────────────────────┼─────────────────────────────────────    │
│  Need GPT-4/GPT-4o    │ Azure OpenAI                            │
│  Need Claude          │ AWS Bedrock or GCP Vertex               │
│  Need Gemini          │ GCP Vertex AI                           │
│  Data sovereignty     │ OCI GenAI DAC (private GPUs)            │
│  Predictable costs    │ OCI DAC or Azure PTU                    │
│  Lowest latency       │ Regional deployment + edge              │
│  Fine-tuning needed   │ Azure OpenAI or OCI DAC                 │
│  Multi-model RAG      │ AWS Bedrock (most models)               │
│  Microsoft ecosystem  │ Azure                                   │
│  Oracle ecosystem     │ OCI                                     │
│  Google Workspace     │ GCP                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Cross-Cloud Data Architecture

### Federated Data Layer

```python
class FederatedDataLayer:
    """Access data across clouds for RAG/AI workloads"""

    def __init__(self):
        self.sources = {
            "aws_s3": S3Client(),
            "azure_blob": AzureBlobClient(),
            "gcp_gcs": GCSClient(),
            "oci_object": OCIObjectStorageClient(),
        }

    async def search_across_clouds(
        self,
        query: str,
        clouds: list = None
    ) -> list:
        """Federated search across cloud storage"""
        clouds = clouds or list(self.sources.keys())

        tasks = [
            self.search_cloud(cloud, query)
            for cloud in clouds
        ]

        results = await asyncio.gather(*tasks)
        return self.merge_and_rank(results)

    async def search_cloud(self, cloud: str, query: str) -> list:
        # Each cloud has its own vector index
        return await self.sources[cloud].vector_search(query)
```

### Data Residency Patterns

```yaml
# Configuration for data residency compliance
data_residency:
  eu_region:
    storage: azure_west_europe
    ai_inference: oci_frankfurt
    reason: "GDPR - data stays in EU"

  us_region:
    storage: aws_us_east_1
    ai_inference: aws_bedrock_us_east
    reason: "Low latency colocation"

  apac_region:
    storage: oci_tokyo
    ai_inference: oci_genai_osaka
    reason: "Japanese data residency laws"

cross_region_allowed:
  - Aggregated analytics (no PII)
  - Model training (anonymized)
```

## Terraform Multi-Cloud Module

```hcl
# main.tf - Multi-Cloud AI Infrastructure

# AWS Bedrock
module "aws_ai" {
  source = "./modules/aws-bedrock"

  enabled_models = ["anthropic.claude-3-5-sonnet", "meta.llama3-70b-instruct"]
  vpc_id         = var.aws_vpc_id
}

# Azure OpenAI
module "azure_ai" {
  source = "./modules/azure-openai"

  resource_group = var.azure_rg
  deployments = {
    "gpt-4o" = {
      model   = "gpt-4o"
      version = "2024-05-13"
      sku     = "Standard"
    }
  }
}

# OCI GenAI
module "oci_ai" {
  source = "./modules/oci-genai"

  compartment_id   = var.oci_compartment
  dedicated_cluster = true
  cluster_units    = 10
}

# GCP Vertex AI
module "gcp_ai" {
  source = "./modules/gcp-vertex"

  project_id = var.gcp_project
  region     = "us-central1"
  endpoints  = ["gemini-pro", "claude-3-sonnet"]
}

# Unified API Gateway
module "ai_gateway" {
  source = "./modules/ai-gateway"

  providers = {
    aws   = module.aws_ai.endpoint
    azure = module.azure_ai.endpoint
    oci   = module.oci_ai.endpoint
    gcp   = module.gcp_ai.endpoint
  }

  routing_rules = {
    "gpt-*"     = "azure"
    "claude-*"  = "aws"
    "gemini-*"  = "gcp"
    "command-*" = "oci"
  }
}
```

## Cost Optimization Strategies

### Reserved Capacity Planning

| Cloud | Commitment Type | Discount | Best For |
|-------|-----------------|----------|----------|
| Azure | PTU (Provisioned) | ~30% | Predictable GPT-4 workloads |
| OCI | DAC Units | Flat rate | High-volume private inference |
| AWS | Savings Plans | ~20% | General compute |
| GCP | CUDs | ~20% | Vertex AI workloads |

### Egress Cost Reduction

```python
class EgressOptimizer:
    """Minimize cross-cloud data transfer costs"""

    EGRESS_COSTS_PER_GB = {
        "aws_to_azure": 0.09,
        "aws_to_gcp": 0.09,
        "azure_to_oci": 0.00,  # Interconnect!
        "oci_to_azure": 0.00,  # Interconnect!
        "gcp_to_aws": 0.12,
    }

    def optimize_data_flow(self, source: str, dest: str, data_gb: float):
        direct_cost = self.EGRESS_COSTS_PER_GB.get(
            f"{source}_to_{dest}", 0.10
        ) * data_gb

        # Check if routing through another cloud is cheaper
        for intermediate in ["azure", "oci"]:
            if intermediate not in [source, dest]:
                hop1 = self.EGRESS_COSTS_PER_GB.get(f"{source}_to_{intermediate}", 0.10)
                hop2 = self.EGRESS_COSTS_PER_GB.get(f"{intermediate}_to_{dest}", 0.10)
                indirect_cost = (hop1 + hop2) * data_gb

                if indirect_cost < direct_cost:
                    return {
                        "route": [source, intermediate, dest],
                        "cost": indirect_cost,
                        "savings": direct_cost - indirect_cost
                    }

        return {"route": [source, dest], "cost": direct_cost}
```

## Monitoring Multi-Cloud AI

### Unified Observability

```yaml
# OpenTelemetry configuration for multi-cloud
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  batch:
    timeout: 10s

exporters:
  # Send to each cloud's native monitoring
  awsxray:
    region: us-east-1
  azuremonitor:
    connection_string: ${AZURE_CONNECTION_STRING}
  googlecloud:
    project: ${GCP_PROJECT}
  oci_apm:
    data_key: ${OCI_APM_KEY}

  # Also send to central observability platform
  prometheus:
    endpoint: 0.0.0.0:8889

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [awsxray, azuremonitor, googlecloud, oci_apm]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

### Key Multi-Cloud Metrics

```python
MULTI_CLOUD_METRICS = {
    # Availability
    "provider_availability": "Uptime per cloud provider",
    "failover_count": "Times failover was triggered",

    # Latency
    "cross_cloud_latency_p99": "99th percentile cross-cloud latency",
    "model_response_time_by_provider": "Response time per provider",

    # Cost
    "cost_per_request_by_provider": "Cost breakdown by cloud",
    "egress_cost_total": "Data transfer costs",

    # Quality
    "model_quality_score_by_provider": "Output quality metrics",
    "error_rate_by_provider": "Error rates per cloud",
}
```

## Security Across Clouds

### Unified Identity

```yaml
# Federated identity configuration
identity_federation:
  primary_idp: azure_ad
  federations:
    - aws:
        type: SAML
        role_mapping:
          AI_Engineer: arn:aws:iam::123:role/BedrockAccess
    - gcp:
        type: OIDC
        workload_identity_pool: ai-workloads
    - oci:
        type: SAML
        group_mapping:
          AI_Engineer: ocid1.group.oc1..xxx
```

### Cross-Cloud Secrets Management

```python
class MultiCloudSecrets:
    """Unified secrets access across clouds"""

    def __init__(self):
        self.backends = {
            "aws": AWSSecretsManager(),
            "azure": AzureKeyVault(),
            "gcp": GCPSecretManager(),
            "oci": OCIVault(),
        }

    def get_secret(self, name: str, cloud: str = None) -> str:
        """Get secret from appropriate cloud"""
        if cloud:
            return self.backends[cloud].get(name)

        # Try each cloud (for migration scenarios)
        for backend in self.backends.values():
            try:
                return backend.get(name)
            except SecretNotFound:
                continue
        raise SecretNotFound(name)
```

## Resources

- [OCI-Azure Interconnect](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/azure.htm)
- [AWS Bedrock Docs](https://docs.aws.amazon.com/bedrock/)
- [Azure OpenAI Docs](https://learn.microsoft.com/azure/ai-services/openai/)
- [GCP Vertex AI Docs](https://cloud.google.com/vertex-ai/docs)
- [Multi-Cloud Architecture Patterns](https://cloud.google.com/architecture/hybrid-and-multi-cloud-patterns-and-practices)
