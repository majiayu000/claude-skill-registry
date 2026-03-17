---
name: company-research
version: "1.0.0"
description: "Run company research using Primr. Use when the user asks to research, analyze, or investigate a company, or provides a company URL."

tools:
  - estimate_run
  - research_company
  - check_jobs
  - get_hypotheses
  - save_hypothesis

resources:
  - file://references/modes

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY
        - SEARCH_API_KEY
        - SEARCH_ENGINE_ID
---

# Company Research

## Workflow

1. **Check prior research**: `get_hypotheses(company)` -- present any existing findings to user
2. **Estimate cost**: `estimate_run(company, url, mode)` -- always before starting
3. **Get user approval**: show estimated cost and duration
4. **Start research**: `research_company(company, url, mode)` -- returns job_id immediately
5. **Monitor**: poll `check_jobs()` every 2 minutes until complete
6. **Present results**: show report path and any new hypotheses

## Research Modes

See `references/modes.md` for mode details (cost, duration, use cases).

## Hypothesis Management

When user confirms or rejects a claim during research:

```
save_hypothesis(company, hypothesis_id, "validated", evidence)
save_hypothesis(company, hypothesis_id, "invalidated", evidence)
```

## Error Handling

| Error | Resolution |
|-------|------------|
| `budget_exceeded` | Hook blocked operation; request budget increase |
| `ssrf_blocked` | URL failed security check; use deep mode instead |
| `qa_below_threshold` | Report quality low; suggest refinement |
| `job_already_running` | Wait for current job; use `check_jobs` |

## Example Workflow

```
User: "Research Acme Corp at https://acme.com"

1. get_hypotheses("Acme Corp")
   -> Found 2 prior hypotheses from last session

2. Present to user:
   "I found prior research on Acme Corp:
    - [VALIDATED] Uses microservices architecture
    - [UNTESTED] Revenue growth exceeds 20% YoY
    Shall I continue with new research?"

3. estimate_run("Acme Corp", "https://acme.com", "full")
   -> Cost: $3.50, Time: ~30 minutes

4. Request approval:
   "Full research will cost ~$3.50 and take ~30 minutes.
    Reply 'approve' to proceed."

5. research_company("Acme Corp", "https://acme.com", "full")
   -> Job started: job_abc123

6. Poll check_jobs() until complete

7. Present results and new hypotheses
```

## Constraints

- **Single Job**: Only one research job at a time
- **Cost Awareness**: Always estimate before running
- **Memory Persistence**: Hypotheses survive across sessions
- **QA Gate**: Reports below score 70 trigger warnings
