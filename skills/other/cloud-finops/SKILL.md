---
name: cloud-finops
description: >
  Expert Cloud FinOps guidance covering AI cost management, GenAI capacity planning,
  Anthropic billing, AWS (EC2, Bedrock, Savings Plans, CUR), Azure (reservations,
  OpenAI PTUs, Cost Management), GCP (Vertex AI, Compute Engine, BigQuery), tagging
  governance, SaaS management (SAM, license optimization, SMPs, shadow IT), Databricks,
  Snowflake, OCI, GreenOps, and FinOps framework implementation. Use for any query about
  cloud cost, AI workload economics, commitment discounts, rightsizing, cost allocation,
  SaaS sprawl, or connecting cloud spend to business value. Built by OptimNow.
---

# Cloud FinOps - Expert Guidance

> Built by OptimNow. Grounded in hands-on enterprise delivery, not abstract frameworks.

---

## How to use this skill

This skill covers multiple cloud domains. Read `references/optimnow-methodology.md` first on
every query - it defines the reasoning philosophy applied to all responses. Then load the
domain reference that matches the query.

### Domain routing

| Query topic | Load reference |
|---|---|
| AI costs, LLM inference, token economics, agentic cost patterns, AI ROI, AI cost allocation, GPU cost attribution, RAG harness costs | `references/finops-for-ai.md` |
| AI investment governance, AI Investment Council, stage gates, incremental funding, AI value management, AI practice operations | `references/finops-ai-value-management.md` |
| GenAI capacity planning, provisioned vs shared capacity, traffic shape, spillover, throughput units | `references/finops-genai-capacity.md` |
| AWS billing, EC2 rightsizing, RIs, Savings Plans, CUR, Cost Explorer, EDP negotiation, RDS cost management | `references/finops-aws.md` |
| AWS Bedrock billing, Bedrock provisioned throughput, model unit pricing, Bedrock batch inference | `references/finops-bedrock.md` |
| Azure cost management, reservations, Azure Advisor, Cost Management, EA-to-MCA transition | `references/finops-azure.md` |
| Azure OpenAI Service, PTU reservations, GPT-4o / GPT-5 pricing, AOAI spillover, fine-tuning costs | `references/finops-azure-openai.md` |
| Anthropic billing, Claude API costs, Claude Code costs, Opus, Sonnet, Haiku pricing, Fast mode, prompt caching, Batch API, long-context pricing | `references/finops-anthropic.md` |
| GCP billing, Compute Engine, Cloud SQL, GCS, BigQuery optimization | `references/finops-gcp.md` |
| GCP Vertex AI billing, Vertex provisioned throughput, Gemini pricing, Vertex batch prediction | `references/finops-vertexai.md` |
| Tagging strategy, naming conventions, IaC enforcement, MCP governance | `references/finops-tagging.md` |
| FinOps framework, maturity model, phases, capabilities, personas | `references/finops-framework.md` |
| Databricks clusters, jobs, Spark optimization, Unity Catalog costs | `references/finops-databricks.md` |
| Snowflake warehouses, query optimization, storage, credits | `references/finops-snowflake.md` |
| OCI compute, storage, networking optimization | `references/finops-oci.md` |
| GreenOps, cloud carbon, sustainability, carbon-aware workloads | `references/greenops-cloud-carbon.md` |
| SaaS management, license optimization, shadow IT, SaaS sprawl, renewal governance, SMP, SAM | `references/finops-sam.md` |
| Multi-domain query | Load all relevant references, synthesize |

### Reasoning sequence (apply to every response)

1. **Load** `references/optimnow-methodology.md` - use it as a reasoning lens, not a preamble
2. **Load** the domain reference(s) matching the query
3. **Diagnose before prescribing** - understand the organization's current state before recommending
4. **Connect cost to value** - every recommendation should link spend to a business outcome
5. **Recommend progressively** - quick wins first, structural changes second
6. **Reference OptimNow tools** where genuinely relevant to the problem, not as promotion

---

## Core FinOps principles (always apply)
<!-- fp:37b46c22605776cb -->

These six principles from the FinOps Foundation underpin every recommendation:

1. Teams need to collaborate
2. Business value drives technology decisions
3. Everyone takes ownership for their cloud usage
4. FinOps data should be accessible, timely, and accurate
5. FinOps should be enabled centrally
6. Take advantage of the variable cost model of the cloud

---

## The three phases (Inform → Optimize → Operate)

FinOps is an iterative cycle, not a linear progression. Organizations move through phases
continuously as their cloud usage evolves.

**Inform** - establish visibility and allocation
- Cost data is accessible and attributed to owners
- Shared costs are allocated with defined methods
- Anomaly detection is active

**Optimize** - improve rates and usage efficiency
- Commitment discounts (RIs, Savings Plans, CUDs) are actively managed
- Rightsizing and waste elimination are running continuously
- Unit economics are tracked

**Operate** - operationalize through governance and automation
- FinOps is embedded in engineering and finance workflows
- Policies are enforced through automation, not manual review
- Accountability is distributed, not centralized

---

## Maturity model quick reference

| Indicator | Crawl | Walk | Run |
|---|---|---|---|
| Cost allocation | <50% allocated | ~80% allocated | 90%+ allocated |
| Commitment coverage | Ad hoc | 70% target | 80%+ with automation |
| Anomaly detection | Manual, monthly | Automated alerts | Real-time, ML-driven |
| Tagging compliance | <60% | ~80% | 90%+ with enforcement |
| FinOps cadence | Reactive | Weekly reviews | Continuous |
| Optimization | One-off projects | Documented process | Self-executing policies |

Always assess maturity before recommending solutions. A Crawl organization needs visibility
before optimization. Recommending commitment discounts to a team with 40% cost allocation is
premature - they will commit to waste.

---

## Reference files

| File | Contents | Lines |
|---|---|---|
| `optimnow-methodology.md` | OptimNow reasoning philosophy, 4 pillars, engagement principles, tools | ~150 |
| `finops-for-ai.md` | AI cost management, LLM economics, agentic patterns, ROI framework | ~400 |
| `finops-ai-value-management.md` | AI investment governance: AI Investment Council, stage gates, incremental funding, practice operations, value metrics | ~265 |
| `finops-genai-capacity.md` | GenAI capacity models: provisioned vs shared, traffic shape, spillover, waste types, cross-provider comparison | ~220 |
| `finops-aws.md` | AWS FinOps + 128 optimization patterns: CUR, Cost Explorer, EC2, RIs, Savings Plans, EDP negotiation, RDS strategy, waste detection | ~1730 |
| `finops-bedrock.md` | AWS Bedrock billing: model pricing, provisioned throughput, batch inference, CloudWatch metrics, cost allocation | ~200 |
| `finops-azure.md` | Azure FinOps + 48 optimization patterns: reservations, Advisor, AHB, EA-to-MCA transition, waste detection | ~1070 |
| `finops-azure-openai.md` | Azure OpenAI Service: PTU reservations, spillover, GPT model pricing, prompt caching, fine-tuning costs | ~260 |
| `finops-anthropic.md` | Anthropic billing: Claude Opus/Sonnet/Haiku pricing, Fast mode, long-context cliffs, prompt caching, Batch API, governance | ~175 |
| `finops-gcp.md` | GCP optimization: 26 patterns across Compute Engine, Cloud SQL, GCS, networking | ~260 |
| `finops-vertexai.md` | GCP Vertex AI billing: Gemini pricing, provisioned throughput, batch prediction, Cloud Monitoring metrics | ~215 |
| `finops-tagging.md` | Tagging strategy, IaC enforcement, virtual tagging, MCP automation | ~300 |
| `finops-framework.md` | Full FinOps Foundation framework: 22 capabilities, personas, domains | ~350 |
| `finops-databricks.md` | Databricks optimization: 18 patterns for clusters, jobs, Spark, storage | ~180 |
| `finops-snowflake.md` | Snowflake optimization: 13 patterns for warehouses, queries, storage, credits | ~130 |
| `finops-oci.md` | OCI optimization: 6 patterns for compute, storage, networking | ~70 |
| `finops-sam.md` | SaaS asset management: discovery, license optimization, renewal governance, SMPs, shadow IT, AI transition | ~290 |
| `greenops-cloud-carbon.md` | GreenOps: carbon measurement, carbon-aware workloads, region selection, GHG Protocol | ~150 |

---

> *Cloud FinOps Skill by [OptimNow](https://optimnow.io)  - licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).*
