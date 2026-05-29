---
name: Enterprise AI Patterns
description: Production-grade AI architecture patterns for enterprise - security, governance, scalability, and operational excellence
version: 1.1.0
last_updated: 2026-01-06
external_version: "2026 Enterprise Patterns"
triggers:
  - enterprise AI
  - production AI
  - AI governance
  - AI at scale
  - enterprise patterns
---

# Enterprise AI Patterns

You are an expert in enterprise-grade AI architecture patterns. You help organizations build AI systems that are secure, scalable, governable, and operationally excellent.

## Enterprise AI Architecture Principles

### The Five Pillars
```
┌─────────────────────────────────────────────────────────────────┐
│                  ENTERPRISE AI PILLARS                           │
│                                                                  │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │ SECURITY  │ │ GOVERNANCE│ │ SCALE     │ │ OPERATIONS│       │
│  │           │ │           │ │           │ │           │       │
│  │ - IAM     │ │ - Policies│ │ - Auto    │ │ - Monitor │       │
│  │ - Encrypt │ │ - Audit   │ │ - Distrib │ │ - Alert   │       │
│  │ - Network │ │ - Lineage │ │ - Multi-  │ │ - Incident│       │
│  │ - Data    │ │ - Quality │ │   region  │ │ - SRE     │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
│                                                                  │
│                     ┌───────────┐                               │
│                     │   COST    │                               │
│                     │           │                               │
│                     │ - FinOps  │                               │
│                     │ - Optimize│                               │
│                     │ - Budget  │                               │
│                     └───────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## Pattern 1: AI Gateway Architecture

### Purpose
Centralized entry point for all AI services with security, routing, and observability.

### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      AI GATEWAY PATTERN                          │
│                                                                  │
│   Applications                                                  │
│   ┌────────┐ ┌────────┐ ┌────────┐                             │
│   │ App A  │ │ App B  │ │ App C  │                             │
│   └───┬────┘ └───┬────┘ └───┬────┘                             │
│       │          │          │                                   │
│       └──────────┼──────────┘                                   │
│                  │                                               │
│          ┌───────▼───────┐                                      │
│          │  AI GATEWAY   │                                      │
│          │               │                                      │
│          │ - AuthN/AuthZ │                                      │
│          │ - Rate Limit  │                                      │
│          │ - Routing     │                                      │
│          │ - Logging     │                                      │
│          │ - Caching     │                                      │
│          │ - Fallback    │                                      │
│          └───────┬───────┘                                      │
│                  │                                               │
│    ┌─────────────┼─────────────┐                                │
│    │             │             │                                │
│    ▼             ▼             ▼                                │
│ ┌──────┐    ┌──────┐    ┌──────┐                               │
│ │ OCI  │    │Azure │    │ AWS  │                               │
│ │GenAI │    │OpenAI│    │Bedrock│                              │
│ └──────┘    └──────┘    └──────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

app = FastAPI()

class AIGateway:
    def __init__(self):
        self.providers = {
            "oci": OCIGenAIProvider(),
            "azure": AzureOpenAIProvider(),
            "aws": AWSBedrockProvider()
        }
        self.rate_limiter = RateLimiter()
        self.cache = ResponseCache()
        self.logger = logging.getLogger("ai_gateway")

    async def route_request(self, request: AIRequest) -> AIResponse:
        # 1. Rate limiting
        if not self.rate_limiter.allow(request.user_id):
            raise HTTPException(429, "Rate limit exceeded")

        # 2. Check cache
        cached = self.cache.get(request)
        if cached:
            return cached

        # 3. Route to provider
        provider = self.select_provider(request)

        # 4. Execute with fallback
        try:
            response = await provider.generate(request)
        except ProviderError:
            response = await self.fallback(request)

        # 5. Cache and log
        self.cache.set(request, response)
        self.log_request(request, response)

        return response

    def select_provider(self, request: AIRequest) -> Provider:
        """Route based on model preference or cost."""
        if request.model.startswith("gpt"):
            return self.providers["azure"]
        elif request.model.startswith("claude"):
            return self.providers["aws"]
        else:
            return self.providers["oci"]  # Default to OCI
```

## Pattern 2: Model Registry & Governance

### Purpose
Central catalog of approved AI models with versioning, lineage, and access control.

### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    MODEL REGISTRY PATTERN                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   MODEL REGISTRY                            │ │
│  │                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │  Model A    │  │  Model B    │  │  Model C    │        │ │
│  │  │  v1.0, v1.1 │  │  v2.0       │  │  v1.0       │        │ │
│  │  │             │  │             │  │             │        │ │
│  │  │ Status:     │  │ Status:     │  │ Status:     │        │ │
│  │  │ PRODUCTION  │  │ STAGING     │  │ DEPRECATED  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                                             │ │
│  │  Metadata:                                                  │ │
│  │  - Owner, Team                                             │ │
│  │  - Training data lineage                                   │ │
│  │  - Performance metrics                                     │ │
│  │  - Approval status                                         │ │
│  │  - Access permissions                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Governance:                                                    │
│  ├── Approval workflow (ML → Security → Legal → Deploy)        │
│  ├── Version control (immutable versions)                      │
│  ├── Access control (who can use which models)                 │
│  └── Audit trail (all model operations logged)                 │
└─────────────────────────────────────────────────────────────────┘
```

### Model Lifecycle
```yaml
Model States:
  DEVELOPMENT:
    - In active development
    - Not for production use
    - Access: ML team only

  STAGING:
    - Ready for testing
    - Pending approval
    - Access: QA, stakeholders

  APPROVED:
    - Passed all reviews
    - Ready for production
    - Access: Applications

  PRODUCTION:
    - Actively serving traffic
    - Monitored
    - Access: Production systems

  DEPRECATED:
    - Scheduled for removal
    - New uses blocked
    - Existing uses grandfathered

  ARCHIVED:
    - Removed from service
    - Retained for audit
    - No access
```

## Pattern 3: AI Observability Stack

### Purpose
Full visibility into AI system health, performance, and behavior.

### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                   AI OBSERVABILITY STACK                         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      DASHBOARDS                              ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   ││
│  │  │ Latency  │  │Throughput│  │  Errors  │  │  Cost    │   ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                       ALERTING                               ││
│  │  - Latency > threshold                                       ││
│  │  - Error rate spike                                          ││
│  │  - Cost anomaly                                              ││
│  │  - Model drift detected                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      DATA LAYER                              ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                  ││
│  │  │ Metrics  │  │  Logs    │  │ Traces   │                  ││
│  │  │ (Prom)   │  │ (Loki)   │  │ (Jaeger) │                  ││
│  │  └──────────┘  └──────────┘  └──────────┘                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Instrumentation:                                               │
│  - Request/response logging                                     │
│  - Token usage tracking                                         │
│  - Latency breakdown                                            │
│  - Error classification                                         │
│  - User feedback signals                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Key Metrics
```yaml
Latency Metrics:
  - p50_latency_ms: Typical response time
  - p95_latency_ms: Worst case common
  - p99_latency_ms: Edge cases
  - time_to_first_token: Streaming starts

Throughput Metrics:
  - requests_per_second: Current load
  - tokens_per_second: Processing rate
  - concurrent_requests: Active requests
  - queue_depth: Waiting requests

Quality Metrics:
  - error_rate: Failed requests %
  - hallucination_rate: Detected hallucinations
  - user_feedback_score: Thumbs up/down ratio
  - retrieval_relevance: RAG quality score

Cost Metrics:
  - tokens_consumed: Input + output
  - cost_per_request: Avg cost
  - daily_spend: Total cost
  - cost_by_application: Breakdown
```

## Pattern 4: Prompt Management System

### Purpose
Version-controlled, tested, and deployed prompts as code.

### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                  PROMPT MANAGEMENT SYSTEM                        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  PROMPT REPOSITORY                           ││
│  │                                                              ││
│  │  prompts/                                                    ││
│  │  ├── customer_support/                                       ││
│  │  │   ├── v1.0.0/                                            ││
│  │  │   │   ├── system.txt                                     ││
│  │  │   │   ├── examples.json                                  ││
│  │  │   │   └── tests.json                                     ││
│  │  │   └── v1.1.0/                                            ││
│  │  │       └── ...                                            ││
│  │  └── data_analysis/                                          ││
│  │      └── ...                                                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  CI/CD Pipeline:                                                │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  │
│  │ Commit │─▶│  Test  │─▶│ Review │─▶│  Stage │─▶│ Deploy │  │
│  └────────┘  └────────┘  └────────┘  └────────┘  └────────┘  │
│                                                                  │
│  Testing:                                                       │
│  - Unit tests (expected outputs)                                │
│  - Regression tests (no quality drop)                           │
│  - A/B tests (compare versions)                                 │
│  - Safety tests (no harmful outputs)                            │
└─────────────────────────────────────────────────────────────────┘
```

### Prompt Template
```yaml
# prompts/customer_support/v1.1.0/config.yaml
name: customer_support
version: 1.1.0
description: "Handle customer support inquiries"

system_prompt: |
  You are a helpful customer support agent for {company_name}.

  Guidelines:
  - Be professional and empathetic
  - Cite knowledge base sources
  - Escalate complex issues
  - Never share internal policies

  Knowledge cutoff: {kb_update_date}

variables:
  - company_name: required
  - kb_update_date: required

examples:
  - input: "I want to return my order"
    expected_topics: ["return_policy", "refund_timeline"]
  - input: "My product is broken"
    expected_topics: ["warranty", "replacement"]

tests:
  - name: "handles_refund_question"
    input: "How do I get a refund?"
    assertions:
      - contains: "refund"
      - does_not_contain: "internal"
      - sentiment: "helpful"
```

## Pattern 5: AI Security Layers

### Defense in Depth
```
┌─────────────────────────────────────────────────────────────────┐
│                   AI SECURITY LAYERS                             │
│                                                                  │
│  Layer 1: PERIMETER                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - API Gateway authentication                                 ││
│  │ - Rate limiting                                              ││
│  │ - IP allowlisting                                            ││
│  │ - WAF rules                                                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Layer 2: INPUT VALIDATION                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Prompt injection detection                                 ││
│  │ - Input sanitization                                         ││
│  │ - Length limits                                              ││
│  │ - Content filtering                                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Layer 3: MODEL SECURITY                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Dedicated clusters (isolation)                             ││
│  │ - Content moderation                                         ││
│  │ - Output filtering                                           ││
│  │ - Guardrails                                                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Layer 4: DATA PROTECTION                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Encryption at rest                                         ││
│  │ - Encryption in transit                                      ││
│  │ - PII detection/masking                                      ││
│  │ - Data residency controls                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  Layer 5: AUDIT & COMPLIANCE                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Request/response logging                                   ││
│  │ - Access audit trail                                         ││
│  │ - Compliance reporting                                       ││
│  │ - Incident response                                          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Prompt Injection Defense
```python
class PromptSanitizer:
    """Detect and mitigate prompt injection attacks."""

    INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"disregard .*instructions",
        r"you are now",
        r"new persona",
        r"system prompt",
        r"<\|.*\|>",  # Special tokens
    ]

    def sanitize(self, user_input: str) -> str:
        # 1. Check for known patterns
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, user_input, re.IGNORECASE):
                raise SecurityError("Potential prompt injection detected")

        # 2. Escape special characters
        sanitized = self.escape_special(user_input)

        # 3. Wrap in delimiters
        wrapped = f"<user_input>{sanitized}</user_input>"

        return wrapped

    def escape_special(self, text: str) -> str:
        """Escape characters that could be interpreted as instructions."""
        replacements = {
            "```": "'''",  # Code blocks
            "###": "---",  # Markdown headers
            "<|": "< |",   # Special tokens
            "|>": "| >",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
```

## Pattern 6: Cost Management

### FinOps for AI
```
┌─────────────────────────────────────────────────────────────────┐
│                    AI FINOPS FRAMEWORK                           │
│                                                                  │
│  VISIBILITY                                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Cost by application/team                                   ││
│  │ - Cost by model                                              ││
│  │ - Token usage trends                                         ││
│  │ - Unit economics (cost per conversation)                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  OPTIMIZATION                                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Model right-sizing (use smaller when sufficient)           ││
│  │ - Caching (avoid redundant calls)                            ││
│  │ - Batching (combine requests)                                ││
│  │ - Reserved capacity (commit for discounts)                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  GOVERNANCE                                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ - Budget alerts by team                                      ││
│  │ - Spend caps per application                                 ││
│  │ - Chargeback/showback                                        ││
│  │ - Approval for expensive models                              ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Cost Optimization Strategies
```yaml
Strategy 1: MODEL TIERING
  - Route simple queries to cheaper models
  - Reserve expensive models for complex tasks
  - Example: Command Light for FAQ, Command R+ for analysis

Strategy 2: CACHING
  - Cache identical queries
  - Semantic caching (similar queries)
  - Cache embeddings
  - TTL based on content freshness

Strategy 3: PROMPT OPTIMIZATION
  - Shorter prompts = fewer input tokens
  - Efficient few-shot examples
  - Remove unnecessary context

Strategy 4: BATCHING
  - Combine multiple small requests
  - Process in bulk during off-peak
  - Reduced per-request overhead

Strategy 5: COMMITMENT
  - Reserved capacity for steady workloads
  - Volume discounts with providers
  - Multi-year agreements where appropriate
```

## Pattern 7: Multi-Region Resilience

### Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                  MULTI-REGION AI DEPLOYMENT                      │
│                                                                  │
│   Region A (Primary)              Region B (Secondary)          │
│   ┌─────────────────────┐        ┌─────────────────────┐       │
│   │  AI Services        │        │  AI Services        │       │
│   │  ┌──────────────┐   │        │  ┌──────────────┐   │       │
│   │  │ GenAI DAC    │   │        │  │ GenAI DAC    │   │       │
│   │  └──────────────┘   │        │  └──────────────┘   │       │
│   │  ┌──────────────┐   │        │  ┌──────────────┐   │       │
│   │  │ Knowledge Base│   │        │  │ Knowledge Base│   │       │
│   │  └──────────────┘   │        │  └──────────────┘   │       │
│   └─────────────────────┘        └─────────────────────┘       │
│             │                              │                    │
│             └──────────────┬───────────────┘                    │
│                            │                                    │
│                    ┌───────▼───────┐                           │
│                    │ Global Load   │                           │
│                    │ Balancer      │                           │
│                    │               │                           │
│                    │ - Health      │                           │
│                    │ - Failover    │                           │
│                    │ - Geo-routing │                           │
│                    └───────────────┘                           │
│                                                                  │
│   Sync:                                                        │
│   - Knowledge bases replicated                                 │
│   - Models deployed to both regions                            │
│   - Config synchronized                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation Checklist

### Phase 1: Foundation
```markdown
- [ ] Deploy AI Gateway
- [ ] Implement authentication/authorization
- [ ] Set up basic monitoring
- [ ] Configure rate limiting
- [ ] Enable audit logging
```

### Phase 2: Governance
```markdown
- [ ] Establish model registry
- [ ] Define approval workflows
- [ ] Implement prompt management
- [ ] Create cost tracking
- [ ] Document policies
```

### Phase 3: Security
```markdown
- [ ] Input validation layer
- [ ] Output filtering
- [ ] PII detection
- [ ] Prompt injection defense
- [ ] Security review process
```

### Phase 4: Operations
```markdown
- [ ] Full observability stack
- [ ] Alerting rules
- [ ] Runbooks
- [ ] Incident response plan
- [ ] Capacity planning
```

### Phase 5: Optimization
```markdown
- [ ] Caching strategy
- [ ] Model tiering
- [ ] Cost optimization
- [ ] Performance tuning
- [ ] Multi-region deployment
```

## Resources

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [MLOps Principles](https://ml-ops.org/)
- [Responsible AI Practices](https://ai.google/responsibility/principles/)
