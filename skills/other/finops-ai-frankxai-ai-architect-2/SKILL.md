---
name: FinOps AI Expert
description: Cost optimization for AI workloads - model selection, GPU sizing, commitment strategies, and multi-cloud cost management
version: 1.1.0
last_updated: 2026-01-06
external_version: "2026 Cloud Pricing"
triggers:
  - cost optimization
  - FinOps
  - AI costs
  - GPU costs
  - token pricing
---

# FinOps AI Expert

You are an expert in Financial Operations (FinOps) for AI workloads, specializing in cost optimization across model selection, infrastructure sizing, commitment strategies, and multi-cloud cost management.

## AI Cost Components

### Cost Breakdown Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI WORKLOAD COST STACK                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INFERENCE COSTS (60-80% typical)                               │
│  ├── Token costs (input + output)                               │
│  ├── GPU compute time                                           │
│  └── API call overhead                                          │
│                                                                  │
│  INFRASTRUCTURE COSTS (15-30%)                                  │
│  ├── GPU/Compute instances                                      │
│  ├── Storage (models, vectors, data)                           │
│  ├── Networking (egress, load balancers)                       │
│  └── Supporting services (DBs, queues, caches)                 │
│                                                                  │
│  DEVELOPMENT COSTS (5-15%)                                      │
│  ├── Training/Fine-tuning compute                              │
│  ├── Experimentation                                           │
│  └── Development environments                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## LLM Pricing Comparison

### API Pricing (Per 1M Tokens)

| Provider | Model | Input | Output | Context |
|----------|-------|-------|--------|---------|
| **OpenAI** | GPT-4o | $2.50 | $10.00 | 128K |
| **OpenAI** | GPT-4o-mini | $0.15 | $0.60 | 128K |
| **OpenAI** | GPT-4 Turbo | $10.00 | $30.00 | 128K |
| **Anthropic** | Claude 3.5 Sonnet | $3.00 | $15.00 | 200K |
| **Anthropic** | Claude 3 Haiku | $0.25 | $1.25 | 200K |
| **Google** | Gemini 1.5 Pro | $1.25 | $5.00 | 1M |
| **Google** | Gemini 1.5 Flash | $0.075 | $0.30 | 1M |
| **AWS Bedrock** | Claude 3.5 Sonnet | $3.00 | $15.00 | 200K |
| **AWS Bedrock** | Llama 3.1 70B | $2.65 | $3.50 | 128K |
| **Azure OpenAI** | GPT-4o | $5.00 | $15.00 | 128K |
| **OCI GenAI** | Command R+ (DAC) | Included | Included | - |

### Cost Per Query Estimation

```python
class LLMCostCalculator:
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "llama-3-70b": {"input": 2.65, "output": 3.50},
    }

    def calculate_query_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost for a single query in dollars"""
        pricing = self.PRICING[model]
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost

    def calculate_monthly_cost(
        self,
        model: str,
        queries_per_day: int,
        avg_input_tokens: int,
        avg_output_tokens: int
    ) -> dict:
        """Estimate monthly costs"""
        daily_cost = self.calculate_query_cost(
            model,
            queries_per_day * avg_input_tokens,
            queries_per_day * avg_output_tokens
        )
        monthly_cost = daily_cost * 30

        return {
            "model": model,
            "daily_queries": queries_per_day,
            "daily_cost": f"${daily_cost:.2f}",
            "monthly_cost": f"${monthly_cost:.2f}",
            "annual_cost": f"${monthly_cost * 12:.2f}"
        }

# Example
calc = LLMCostCalculator()

# RAG chatbot: 10K queries/day, 2000 input tokens, 500 output tokens
calc.calculate_monthly_cost("gpt-4o", 10000, 2000, 500)
# {'monthly_cost': '$300.00'}  # GPT-4o

calc.calculate_monthly_cost("claude-3-haiku", 10000, 2000, 500)
# {'monthly_cost': '$33.75'}  # 89% savings with Haiku
```

## Model Selection for Cost Optimization

### Decision Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                MODEL SELECTION BY USE CASE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TASK COMPLEXITY     │ RECOMMENDED           │ COST/1K QUERIES  │
│  ────────────────────┼───────────────────────┼─────────────────  │
│  Simple Q&A          │ GPT-4o-mini, Haiku    │ $0.05 - $0.20    │
│  Classification      │ Haiku, Gemini Flash   │ $0.02 - $0.10    │
│  Summarization       │ GPT-4o-mini, Sonnet   │ $0.10 - $0.50    │
│  RAG (retrieval)     │ Sonnet, GPT-4o-mini   │ $0.20 - $1.00    │
│  Code generation     │ Sonnet, GPT-4o        │ $0.50 - $2.00    │
│  Complex reasoning   │ GPT-4o, Claude Opus   │ $1.00 - $5.00    │
│  Agent tasks         │ Sonnet, GPT-4o        │ $2.00 - $10.00   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Model Cascading Pattern

```python
class ModelCascade:
    """Route to cheapest model that can handle the task"""

    def __init__(self):
        self.models = [
            {"name": "claude-3-haiku", "cost": 0.25, "capability": 0.7},
            {"name": "gpt-4o-mini", "cost": 0.15, "capability": 0.75},
            {"name": "claude-3-5-sonnet", "cost": 3.00, "capability": 0.95},
            {"name": "gpt-4o", "cost": 2.50, "capability": 0.98},
        ]

    async def route(self, query: str, complexity_score: float) -> str:
        """Route to appropriate model based on complexity"""
        for model in sorted(self.models, key=lambda x: x["cost"]):
            if model["capability"] >= complexity_score:
                return model["name"]
        return self.models[-1]["name"]  # Fallback to most capable

    async def cascade_with_fallback(self, query: str) -> dict:
        """Try cheap model first, escalate if needed"""
        # Start with cheapest
        response = await self.call_model("claude-3-haiku", query)

        # Check confidence
        if response.confidence < 0.8:
            # Escalate to better model
            response = await self.call_model("claude-3-5-sonnet", query)

        return response
```

## GPU Cost Optimization

### GPU Pricing Comparison

| Provider | GPU | vCPU | Memory | Hourly | Monthly |
|----------|-----|------|--------|--------|---------|
| **AWS** | A10G | 4 | 24GB | $1.21 | $870 |
| **AWS** | A100 40GB | 12 | 192GB | $3.67 | $2,640 |
| **AWS** | H100 | 192 | 2TB | $12.36 | $8,900 |
| **Azure** | A10 | 6 | 112GB | $1.14 | $820 |
| **Azure** | A100 80GB | 24 | 220GB | $3.40 | $2,450 |
| **GCP** | A100 40GB | 12 | 85GB | $3.67 | $2,640 |
| **OCI** | A10 | 15 | 240GB | $1.00 | $720 |
| **Lambda** | A100 | 30 | 200GB | $1.29 | $930 |
| **RunPod** | A100 | - | 80GB | $1.89 | $1,360 |

### Right-Sizing GPU Workloads

```python
class GPUSizer:
    """Recommend GPU size based on model and workload"""

    GPU_MEMORY = {
        "A10G": 24,
        "L4": 24,
        "A100-40GB": 40,
        "A100-80GB": 80,
        "H100": 80,
    }

    MODEL_MEMORY = {
        # Model: (FP16 size GB, Quantized GB)
        "llama-3.1-8B": (16, 6),
        "llama-3.1-70B": (140, 42),
        "llama-3.1-405B": (810, 250),
        "mistral-7B": (14, 5),
        "mixtral-8x7B": (96, 32),
    }

    def recommend_gpu(
        self,
        model: str,
        batch_size: int = 1,
        use_quantization: bool = True
    ) -> dict:
        """Recommend GPU configuration"""
        base_mem, quant_mem = self.MODEL_MEMORY.get(model, (10, 4))
        model_mem = quant_mem if use_quantization else base_mem

        # Add overhead for KV cache and batch
        kv_cache_per_batch = 2  # GB per batch slot
        total_mem = model_mem + (kv_cache_per_batch * batch_size) + 2  # 2GB overhead

        # Find suitable GPU
        suitable_gpus = []
        for gpu, mem in self.GPU_MEMORY.items():
            if mem >= total_mem:
                suitable_gpus.append(gpu)

        if not suitable_gpus:
            # Need multi-GPU
            return {
                "recommendation": "multi-gpu",
                "min_gpus": (total_mem // 80) + 1,
                "gpu_type": "A100-80GB or H100"
            }

        return {
            "recommendation": suitable_gpus[0],
            "memory_required": f"{total_mem:.1f}GB",
            "batch_size": batch_size,
            "quantization": use_quantization
        }
```

## Commitment Strategies

### Reserved Capacity Comparison

| Provider | Commitment | Discount | Term |
|----------|------------|----------|------|
| **Azure PTU** | Provisioned Throughput | ~30% | Monthly |
| **OCI DAC** | Dedicated AI Cluster | Flat rate | Monthly |
| **AWS Savings Plans** | Compute | 20-30% | 1-3 years |
| **GCP CUDs** | Committed Use | 20-57% | 1-3 years |

### Break-Even Analysis

```python
def commitment_breakeven(
    on_demand_monthly: float,
    committed_monthly: float,
    commitment_term_months: int,
    upfront_cost: float = 0
) -> dict:
    """Calculate break-even point for commitments"""

    monthly_savings = on_demand_monthly - committed_monthly
    total_commitment_cost = (committed_monthly * commitment_term_months) + upfront_cost
    total_on_demand_cost = on_demand_monthly * commitment_term_months

    break_even_months = upfront_cost / monthly_savings if monthly_savings > 0 else float('inf')

    return {
        "monthly_savings": f"${monthly_savings:.2f}",
        "total_savings": f"${total_on_demand_cost - total_commitment_cost:.2f}",
        "break_even_months": round(break_even_months, 1),
        "roi_percentage": f"{((total_on_demand_cost - total_commitment_cost) / total_commitment_cost) * 100:.1f}%"
    }

# Example: Azure PTU commitment
commitment_breakeven(
    on_demand_monthly=5000,  # Pay-as-you-go
    committed_monthly=3500,  # PTU pricing
    commitment_term_months=12,
    upfront_cost=0
)
# {'monthly_savings': '$1500.00', 'total_savings': '$18000.00', 'roi_percentage': '42.9%'}
```

## Cost Monitoring & Alerts

### Tagging Strategy

```yaml
# Required tags for AI workloads
ai_cost_tags:
  mandatory:
    - project: "ai-platform"
    - environment: "prod/staging/dev"
    - cost_center: "engineering"
    - workload_type: "inference/training/embedding"
    - model: "gpt-4o/claude-3/llama-3"

  recommended:
    - team: "ml-platform"
    - owner: "email@company.com"
    - budget_code: "AI-2024-Q1"
```

### Budget Alerts

```hcl
# Terraform for AWS Budget Alert
resource "aws_budgets_budget" "ai_monthly" {
  name         = "ai-platform-monthly"
  budget_type  = "COST"
  limit_amount = "10000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "TagKeyValue"
    values = ["user:project$ai-platform"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["finops@company.com"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type            = "FORECASTED"
    notification_type         = "FORECASTED"
    subscriber_email_addresses = ["finops@company.com", "engineering@company.com"]
  }
}
```

### Cost Dashboard Metrics

```python
FINOPS_METRICS = {
    # Cost metrics
    "cost_per_query": "Total cost / number of queries",
    "cost_per_token": "Total cost / tokens processed",
    "cost_per_user": "Total cost / active users",
    "cost_efficiency": "Output value / total cost",

    # Utilization metrics
    "gpu_utilization": "Active GPU time / provisioned GPU time",
    "api_efficiency": "Successful calls / total calls",
    "cache_hit_rate": "Cached responses / total requests",

    # Optimization metrics
    "model_routing_savings": "Baseline cost - actual cost",
    "commitment_utilization": "Committed capacity used / purchased",
    "spot_savings": "On-demand equivalent - actual spot cost"
}
```

## Cost Optimization Techniques

### 1. Prompt Engineering for Cost

```python
class CostAwarePrompting:
    """Optimize prompts for cost efficiency"""

    def optimize_prompt(self, prompt: str, max_tokens: int = None) -> str:
        """Reduce prompt tokens while maintaining quality"""
        # Remove redundant whitespace
        optimized = ' '.join(prompt.split())

        # Use abbreviations for common patterns
        optimized = optimized.replace("Please provide", "Provide")
        optimized = optimized.replace("I would like you to", "")
        optimized = optimized.replace("Can you please", "")

        return optimized

    def batch_similar_requests(self, requests: list) -> list:
        """Batch similar requests to reduce overhead"""
        # Group by similar prompts
        batches = {}
        for req in requests:
            key = self.get_prompt_signature(req)
            if key not in batches:
                batches[key] = []
            batches[key].append(req)

        return list(batches.values())
```

### 2. Caching Strategy

```python
import hashlib
from functools import lru_cache

class SemanticCache:
    """Cache LLM responses by semantic similarity"""

    def __init__(self, similarity_threshold: float = 0.95):
        self.cache = {}
        self.threshold = similarity_threshold

    def get_cache_key(self, prompt: str) -> str:
        """Generate cache key from prompt"""
        return hashlib.sha256(prompt.encode()).hexdigest()

    async def get_or_generate(
        self,
        prompt: str,
        generate_fn,
        ttl_seconds: int = 3600
    ):
        """Return cached response or generate new one"""
        cache_key = self.get_cache_key(prompt)

        # Check exact match
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Check semantic similarity
        similar = await self.find_similar(prompt)
        if similar:
            return similar

        # Generate new response
        response = await generate_fn(prompt)
        self.cache[cache_key] = response
        return response

    # Cache hit rates: 30-60% typical for production workloads
    # Cost savings: 30-50% on inference costs
```

### 3. Spot/Preemptible Instances

```python
class SpotInstanceStrategy:
    """Manage spot instances for AI workloads"""

    SPOT_SAVINGS = {
        "aws": 0.70,  # 70% savings typical
        "azure": 0.60,
        "gcp": 0.65,
    }

    def recommend_spot_strategy(self, workload_type: str) -> dict:
        """Recommend spot usage based on workload"""
        strategies = {
            "batch_inference": {
                "spot_eligible": True,
                "percentage": 100,
                "reason": "Interruptible, can retry"
            },
            "training": {
                "spot_eligible": True,
                "percentage": 80,
                "reason": "Checkpoint frequently, retry on interrupt"
            },
            "real_time_inference": {
                "spot_eligible": False,
                "percentage": 0,
                "reason": "Latency-sensitive, needs reliability"
            },
            "dev_environment": {
                "spot_eligible": True,
                "percentage": 100,
                "reason": "Non-critical, cost optimization priority"
            }
        }
        return strategies.get(workload_type, {"spot_eligible": False})
```

## Multi-Cloud Cost Arbitrage

### Provider Selection by Cost

```python
class MultiCloudCostRouter:
    """Route workloads to cheapest provider"""

    PROVIDER_COSTS = {
        "embedding": {
            "aws_titan": 0.0001,
            "azure_ada": 0.0001,
            "cohere": 0.0001,
            "openai": 0.00013,
        },
        "chat": {
            "aws_claude_haiku": 0.00025,
            "azure_gpt35": 0.0005,
            "openai_gpt4o_mini": 0.00015,
        }
    }

    def get_cheapest_provider(self, task_type: str) -> tuple:
        """Return cheapest provider for task"""
        costs = self.PROVIDER_COSTS.get(task_type, {})
        if not costs:
            return None, None

        cheapest = min(costs.items(), key=lambda x: x[1])
        return cheapest

    def calculate_arbitrage_savings(
        self,
        current_provider: str,
        current_cost: float,
        volume: int
    ) -> dict:
        """Calculate savings from switching providers"""
        alternatives = []
        for task, providers in self.PROVIDER_COSTS.items():
            for provider, cost in providers.items():
                if cost < current_cost:
                    monthly_savings = (current_cost - cost) * volume * 30
                    alternatives.append({
                        "provider": provider,
                        "cost": cost,
                        "monthly_savings": f"${monthly_savings:.2f}"
                    })

        return sorted(alternatives, key=lambda x: float(x["monthly_savings"].replace("$", "")), reverse=True)
```

## FinOps Maturity Model

```
┌─────────────────────────────────────────────────────────────────┐
│                  AI FINOPS MATURITY LEVELS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LEVEL 1: CRAWL                                                 │
│  ├── Basic cost visibility                                      │
│  ├── Manual cost tracking                                       │
│  └── Simple tagging                                             │
│                                                                  │
│  LEVEL 2: WALK                                                  │
│  ├── Automated cost allocation                                  │
│  ├── Budget alerts                                              │
│  ├── Model selection guidelines                                 │
│  └── Basic optimization (caching, batching)                     │
│                                                                  │
│  LEVEL 3: RUN                                                   │
│  ├── Real-time cost dashboards                                  │
│  ├── Automated cost anomaly detection                           │
│  ├── Commitment management                                      │
│  ├── Multi-cloud cost optimization                              │
│  └── Cost-aware model routing                                   │
│                                                                  │
│  LEVEL 4: FLY                                                   │
│  ├── Predictive cost modeling                                   │
│  ├── Automated scaling based on cost/performance                │
│  ├── Business value attribution                                 │
│  └── Continuous optimization loops                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Resources

- [FinOps Foundation](https://www.finops.org/)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)
- [Azure Cost Management](https://azure.microsoft.com/en-us/products/cost-management)
- [GCP Cost Management](https://cloud.google.com/cost-management)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [OpenAI Pricing](https://openai.com/pricing)
