---
name: n8n-workflow-architect
description: Strategic automation architecture advisor. Use when users want to plan automation solutions, evaluate their tech stack (Shopify, Zoho, HubSpot, etc.), decide between n8n vs Python/Claude Code, or need guidance on production-ready automation design. Invokes plan mode for complex architectural decisions.
---

# n8n Workflow Architect

The Intelligent Automation Architect (IAA) - Strategic guidance for building automation systems that survive production.

---

## When to Use This Skill

Invoke this skill when users:

1. **Want to plan an automation project** - "I need to automate my sales pipeline"
2. **Have multiple services to integrate** - "I use Shopify, Klaviyo, and Notion"
3. **Need architecture decisions** - "Should I use n8n or Python for this?"
4. **Are evaluating feasibility** - "Can I automate X with my current stack?"
5. **Want production-ready guidance** - "How do I make this reliable?"

---

## The Core Philosophy

> **Viability over Possibility**

The gap between what's technically possible and what's actually viable in production is enormous. This skill helps users build systems that:

- Won't break at 3 AM on a Saturday
- Don't require a PhD to maintain
- Respect data security, scale, and state management
- Deliver actual business value, not just technical cleverness

---

## Architecture Decision Framework

### Step 1: Stack Analysis

When a user mentions their tools, evaluate each for:

| Tool Category | Common Examples | n8n Native Support | Auth Complexity |
|---------------|-----------------|-------------------|-----------------|
| E-commerce | Shopify, WooCommerce, BigCommerce | Yes | OAuth |
| CRM | HubSpot, Salesforce, Zoho CRM | Yes | OAuth |
| Marketing | Klaviyo, Mailchimp, ActiveCampaign | Yes | API Key/OAuth |
| Productivity | Notion, Airtable, Google Sheets | Yes | OAuth |
| Communication | Slack, Discord, Teams | Yes | OAuth |
| Payments | Stripe, PayPal, Square | Yes | API Key |
| Support | Zendesk, Intercom, Freshdesk | Yes | API Key/OAuth |

**Action**: Use `search_nodes` from n8n MCP to verify node availability.

### Step 2: Tool Selection Matrix

Apply these decision rules:

#### Use n8n When:

| Condition | Why |
|-----------|-----|
| OAuth authentication required | n8n manages token lifecycle automatically |
| Non-technical maintainers | Visual workflows are self-documenting |
| Multi-day processes with waits | Built-in Wait node handles suspension |
| Standard SaaS integrations | Pre-built nodes eliminate boilerplate |
| < 5,000 records per execution | Within memory limits |
| < 20 nodes of business logic | Maintains visual clarity |

#### Use Python/Claude Code When:

| Condition | Why |
|-----------|-----|
| > 5,000 records to process | Stream processing, memory management |
| > 20MB files | Chunked processing capabilities |
| Complex algorithms | Code is more maintainable than 50+ nodes |
| Cutting-edge AI libraries | Access to latest packages |
| Heavy data transformation | Pandas, NumPy optimization |
| Custom ML models | Full Python ecosystem access |

#### Use Hybrid (Recommended for Complex Systems):

```
n8n (Orchestration Layer)
├── Webhooks & triggers
├── OAuth authentication
├── User-facing integrations
├── Flow coordination
│
└── Calls Python Service (Processing Layer)
    ├── Heavy computation
    ├── Complex logic
    ├── AI/ML operations
    └── Returns results to n8n
```

---

## Business Stack Quick Assessment

When user describes their stack, respond with this analysis:

### Template Response:

```markdown
## Stack Analysis: [User's Business Type]

### Services Identified:
1. **[Service 1]** - [Category] - n8n Support: [Yes/Partial/No]
2. **[Service 2]** - [Category] - n8n Support: [Yes/Partial/No]
...

### Recommended Approach: [n8n / Python / Hybrid]

**Rationale:**
- [Key decision factor 1]
- [Key decision factor 2]
- [Key decision factor 3]

### Integration Complexity: [Low/Medium/High]
- Auth complexity: [Simple API keys / OAuth required]
- Data volume: [Estimate based on use case]
- Processing needs: [Simple transforms / Complex logic]

### Next Steps:
1. [Specific action using other n8n skills]
2. [Pattern to follow from n8n-workflow-patterns]
3. [Validation approach from n8n-validation-expert]
```

---

## Common Business Scenarios

### Scenario 1: E-commerce Automation
**Stack**: Shopify + Klaviyo + Slack + Google Sheets

**Verdict**: Pure n8n
- All services have native nodes
- OAuth handled automatically
- Standard webhook patterns
- Use: `n8n-workflow-patterns` → webhook_processing

### Scenario 2: AI-Powered Lead Qualification
**Stack**: Typeform + HubSpot + OpenAI + Custom Scoring

**Verdict**: Hybrid
- n8n: Typeform webhook, HubSpot sync, notifications
- Python/Code Node: Complex scoring algorithm, AI prompts
- Use: `n8n-workflow-patterns` → ai_agent_workflow

### Scenario 3: Data Pipeline / ETL
**Stack**: PostgreSQL + BigQuery + 50k+ daily records

**Verdict**: Python with n8n Trigger
- n8n: Schedule trigger, success/failure notifications
- Python: Batch processing, streaming, transformations
- Reason: Memory limits in n8n for large datasets

### Scenario 4: Multi-Step Approval Workflow
**Stack**: Slack + Notion + Email + 3-day wait periods

**Verdict**: Pure n8n
- Built-in Wait node for delays
- Native Slack/Notion integrations
- Human approval patterns built-in
- Use: `n8n-workflow-patterns` → scheduled_tasks

---

## Production Readiness Checklist

Before any automation goes live, verify:

### Observability
- [ ] Error notification workflow exists
- [ ] Execution logging to database
- [ ] Health check workflow for critical paths
- [ ] Structured alerting by severity

### Idempotency
- [ ] Duplicate webhook handling
- [ ] Check-before-create patterns
- [ ] Idempotency keys for payments
- [ ] Safe re-run capability

### Cost Awareness
- [ ] AI API costs calculated and approved
- [ ] Rate limits documented
- [ ] Caching strategy for repeated calls
- [ ] Model right-sizing (Haiku vs Sonnet vs Opus)

### Operational Control
- [ ] Kill switch accessible to non-technical staff
- [ ] Approval queues for high-stakes actions
- [ ] Audit trail for all actions
- [ ] Configuration externalized

Use `n8n-validation-expert` skill to validate workflows before deployment.

---

## Integration with Other n8n Skills

This skill works as the **planning layer** that coordinates other skills:

```
┌─────────────────────────────────────────────────────────────┐
│                  n8n-workflow-architect                      │
│            (Strategic Decisions & Planning)                  │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ n8n-workflow-   │  │ n8n-node-       │  │ n8n-validation- │
│ patterns        │  │ configuration   │  │ expert          │
│ (Architecture)  │  │ (Node Setup)    │  │ (Quality)       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     n8n MCP Tools                            │
│    (search_nodes, validate_workflow, create_workflow, etc.) │
└─────────────────────────────────────────────────────────────┘
```

### Skill Handoff Guide:

| After Architect Decides... | Hand Off To |
|---------------------------|-------------|
| Pattern type identified | `n8n-workflow-patterns` for detailed structure |
| Specific nodes needed | `n8n-node-configuration` for setup |
| Code node required | `n8n-code-javascript` or `n8n-code-python` |
| Expressions needed | `n8n-expression-syntax` for correct syntax |
| Ready to validate | `n8n-validation-expert` for pre-deploy checks |
| Need node info | n8n MCP → `get_node_essentials`, `search_nodes` |

---

## Plan Mode Activation

For complex architectural decisions, enter plan mode to:

1. **Analyze the full business context**
2. **Evaluate all integration points**
3. **Design the data flow architecture**
4. **Identify failure modes and mitigations**
5. **Create implementation roadmap**

### Trigger Plan Mode When:

- User has 3+ services to integrate
- Unclear whether n8n or Python is better
- High-stakes automation (payments, customer data)
- Complex multi-step processes
- AI/ML components involved

### Plan Mode Output Structure:

```markdown
## Automation Architecture Plan

### 1. Business Context
[What problem are we solving?]

### 2. Stack Analysis
[Each service, its role, integration complexity]

### 3. Recommended Architecture
[n8n / Python / Hybrid with rationale]

### 4. Data Flow Design
[Visual representation of the flow]

### 5. Implementation Phases
Phase 1: [Core workflow]
Phase 2: [Error handling & observability]
Phase 3: [Optimization & scaling]

### 6. Risk Assessment
[What could go wrong, how we prevent it]

### 7. Maintenance Plan
[Who maintains, what skills needed]
```

---

## Quick Decision Tree

```
START: User wants to automate something
  │
  ├─► Does it involve OAuth? ────────────────────► Use n8n
  │
  ├─► Will non-developers maintain it? ──────────► Use n8n
  │
  ├─► Does it need to wait days/weeks? ──────────► Use n8n
  │
  ├─► Processing > 5000 records? ────────────────► Use Python
  │
  ├─► Files > 20MB? ─────────────────────────────► Use Python
  │
  ├─► Cutting-edge AI/ML? ───────────────────────► Use Python
  │
  ├─► Complex algorithm (would need 20+ nodes)? ─► Use Python
  │
  └─► Mix of above? ─────────────────────────────► Use Hybrid
```

---

## MCP Tool Integration

Use these n8n MCP tools during architecture planning:

| Planning Phase | MCP Tools to Use |
|----------------|------------------|
| Stack analysis | `search_nodes` - verify node availability |
| Pattern selection | `list_node_templates` - find similar workflows |
| Feasibility check | `get_node_essentials` - understand capabilities |
| Complexity estimate | `get_node_documentation` - auth & config needs |
| Template reference | `get_template` - study existing patterns |

---

## Red Flags to Watch For

Warn users when you see these patterns:

| Red Flag | Risk | Recommendation |
|----------|------|----------------|
| "I want AI to do everything" | Cost explosion, unpredictability | Scope AI to specific tasks, cache results |
| "It needs to process millions of rows" | Memory crashes | Python with streaming, not n8n loops |
| "The workflow has 50 nodes" | Unmaintainable | Consolidate to code blocks or split workflows |
| "We'll add error handling later" | Silent failures | Build error handling from day one |
| "It should work on any input" | Fragile system | Define and validate expected inputs |
| "The intern will maintain it" | Single point of failure | Use n8n for visual clarity, document thoroughly |

---

## Summary

**This skill answers**: "Given my business stack and requirements, what's the smartest way to build this automation?"

**Key outputs**:
1. Stack compatibility analysis
2. n8n vs Python vs Hybrid recommendation
3. Pattern and skill handoffs
4. Production readiness guidance
5. Implementation roadmap via plan mode

**Works with**:
- All n8n-* skills for implementation details
- n8n MCP tools for node discovery and workflow creation
- Plan mode for complex architectural decisions

---

## Related Files

- [tool-selection-matrix.md](tool-selection-matrix.md) - Detailed decision criteria
- [business-stack-analysis.md](business-stack-analysis.md) - Common SaaS integration guides
- [production-readiness.md](production-readiness.md) - Pre-launch checklist details
