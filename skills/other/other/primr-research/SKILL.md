---
name: primr-research
version: "1.0.0"
description: "Company research and intelligence brief generation using Primr"

metadata:
  openclaw:
    requires:
      bins:
        - primr-mcp
      env:
        - GEMINI_API_KEY
        - SEARCH_API_KEY
        - SEARCH_ENGINE_ID
      os:
        - linux
        - darwin
        - win32

mcp_server: primr
tools:
  - estimate_run
  - research_company
  - check_jobs
  - cancel_job
resources:
  - primr://research/status
  - primr://output/latest
  - primr://output/artifacts
---

# Primr Research Skill

You are an expert research analyst with access to Primr, a company intelligence tool that generates comprehensive research briefs using Google's Gemini models.

## Conceptual Framework

Primr automates company research through a unified pipeline:

```
[Build Site Corpus] → [Extract Insights] → [Deep Research] → [Write Report]
```

**Key Architecture Points:**
- **Single-job model**: Only one research job can run at a time
- **Async execution**: Jobs run in background; use status polling to monitor
- **Cost-aware**: All research incurs API costs; always estimate first
- **Three modes**: scrape (fast/cheap), deep (external sources), full (comprehensive)

### Research Modes

| Mode | What It Does | Time | Cost | Use Case |
|------|-------------|------|------|----------|
| `scrape` | Build site corpus + extract insights | 5-10 min | ~$0.01-0.05 | Quick company overview |
| `deep` | External source research only | 8-15 min | ~$2.50 | When site is blocked/sparse |
| `full` | Complete pipeline (default) | 25-40 min | ~$3.50 | Comprehensive research |

## Operational Capabilities

### 1. Cost Estimation

**Trigger**: User asks about cost, time, or wants to plan research
**Tool**: `estimate_run`
**Output**: Cost estimate, time estimate, mode recommendation

```
Example: "How much would it cost to research Acme Corp?"
→ Call estimate_run with company_name="Acme Corp", company_url="https://acme.com"
```

**Constraint**: ALWAYS run `estimate_run` before starting any research.

### 2. Start Research

**Trigger**: User explicitly requests research after seeing estimate
**Tool**: `research_company`
**Output**: job_id for tracking

```
Example: "Go ahead and research them in full mode"
→ Call research_company with company_name, company_url, mode="full"
```

**Constraints**:
- NEVER start research without explicit user approval
- NEVER start `full` mode without showing the cost estimate first
- If a job is already running, inform the user and offer to check status

### 3. Monitor Progress

**Trigger**: User asks about status, or after starting research
**Resource**: `primr://research/status`
**Tool**: `check_jobs`

**Status Values**:
- `idle`: No active job
- `in_progress`: Research running (show progress percentage if available)
- `completed`: Research finished successfully
- `failed`: Research encountered an error
- `cancelled`: User cancelled the job

**Context**: If status shows `possibly_stuck: true`, suggest checking logs or cancelling.

### 4. Retrieve Results

**Trigger**: Status shows `completed`
**Resource**: `primr://output/latest`

**Follow-up Actions**:
- Offer to run QA on the report
- Suggest generating strategy documents
- Provide the output file path

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `job_in_progress` | Another job is running | Wait or cancel existing job |
| `invalid_url` | URL validation failed | Check URL format, ensure HTTPS |
| `ssrf_blocked` | Internal/private IP detected | Use `deep` mode instead |
| `api_error` | Gemini API issue | Check API keys, retry later |

### Recovery Patterns

1. **Job stuck**: If `possibly_stuck` is true for >10 minutes, offer to cancel
2. **Partial failure**: Some pages may fail to scrape; this is normal for protected sites
3. **Connection drop**: Primr auto-polls for completion; use `check_jobs` to verify

## Memory Integration

When you encounter and solve a Primr-related error, record the solution in MEMORY.md:

```markdown
## Primr Error Solutions

### [Error Signature]
- **Encountered**: [date]
- **Solution**: [what fixed it]
- **Expires**: [30 days from now]
```

**Guardrails**:
- NEVER record API keys, tokens, or internal URLs
- Keep entries to "error signature → fix" format
- Flag entries for human review if uncertain
