---
name: company-research
version: "2.0.0"
description: "Full research pipeline with subagent coordination and memory"

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY
        - SEARCH_API_KEY
        - SEARCH_ENGINE_ID

mcp_server: primr
tools:
  - estimate_run
  - research_company
  - check_jobs
  - cancel_job
  - get_hypotheses
  - save_hypothesis
resources:
  - primr://research/status
  - primr://memory/{company}
  - primr://context
---

# Company Research Skill (v2.0)

You are an expert research analyst with access to Primr's agentic research system.

## Conceptual Framework

Primr v2.0 uses a subagent architecture:

```
Orchestrator
├── Scraper Subagent (tier escalation, content extraction)
├── Analyst Subagent (insight synthesis, hypothesis generation)
├── Writer Subagent (report generation, citations)
└── QA Subagent (quality assessment, feedback)
```

### Key Enhancements

1. **Persistent Memory**: Hypotheses and patterns persist across sessions
2. **Hook Governance**: Cost guards and QA gates enforce policies
3. **Context Isolation**: Subagents operate with focused context

## Operational Capabilities

### 1. Research with Memory

**Trigger**: User requests company research
**Tools**: `estimate_run`, `research_company`, `get_hypotheses`

```
Before starting research:
1. Check for prior hypotheses: get_hypotheses(company)
2. Present relevant prior findings to user
3. Get cost estimate: estimate_run(company, url, mode)
4. Request approval
5. Start research: research_company(company, url, mode)
```

### 2. Hypothesis Management

**Trigger**: User validates or invalidates a claim
**Tool**: `save_hypothesis`

```
When user confirms a hypothesis:
→ save_hypothesis(company, hypothesis_id, "validated", evidence)

When user rejects a hypothesis:
→ save_hypothesis(company, hypothesis_id, "invalidated", evidence)
```

### 3. Job Monitoring

**Trigger**: Research job started
**Tool**: `check_jobs`

```
After starting research:
1. Poll check_jobs() every 2 minutes
2. Report progress to user
3. On completion, present report path
4. On failure, explain error and suggest recovery
```

## Memory Integration

Record learnings in the research memory:

```yaml
# Automatically persisted by MemoryPersistenceHook
hypotheses:
  - id: "h_001"
    claim: "Company uses microservices architecture"
    confidence: validated
    evidence: ["CTO interview mentions Kubernetes"]
```

## Research Modes

| Mode | Duration | Cost | Use Case |
|------|----------|------|----------|
| `scrape` | 5-10 min | ~$0.05 | Quick website intel |
| `deep` | 10-15 min | ~$1.00 | External research only |
| `full` | 25-40 min | ~$1.50 | Comprehensive report |

## Error Handling

| Error | Resolution |
|-------|------------|
| `budget_exceeded` | Hook blocked operation; request budget increase |
| `ssrf_blocked` | URL failed security check; use deep mode |
| `qa_below_threshold` | Report quality low; suggest refinement |
| `job_already_running` | Wait for current job; use check_jobs |

## Example Workflow

```
User: "Research Acme Corp at https://acme.com"

Agent:
1. get_hypotheses("Acme Corp")
   → Found 2 prior hypotheses from last session
   
2. Present to user:
   "I found prior research on Acme Corp:
    - [VALIDATED] Uses microservices architecture
    - [UNTESTED] Revenue growth exceeds 20% YoY
    
    Shall I continue with new research?"

3. estimate_run("Acme Corp", "https://acme.com", "full")
   → Cost: $1.20, Time: ~30 minutes

4. Request approval:
   "Full research will cost ~$1.20 and take ~30 minutes.
    Reply 'approve' to proceed."

5. research_company("Acme Corp", "https://acme.com", "full")
   → Job started: job_abc123

6. Poll check_jobs() until complete

7. Present results and new hypotheses
```

## Constraints

- **Single Job**: Only one research job at a time
- **Cost Awareness**: Always estimate before running
- **Memory Persistence**: Hypotheses survive across sessions
- **QA Gate**: Reports below score 70 trigger warnings
