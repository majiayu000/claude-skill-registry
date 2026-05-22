---
name: system-architecture
description: Design multi-service architectures with RAW workflows as components
---

# System Architecture Patterns

Use this skill when the user's requirements span multiple days, require webhooks, scheduling, or long-running state.

## When to Build a System (vs Single Workflow)

### Single RAW Workflow
Use for:
- Data processing tasks
- API integrations (fetch → transform → save)
- Report generation
- One-time executions

### Multi-System Architecture
Use when you need:
- **Long-running state** (track entities across days/weeks)
- **Multiple entry points** (webhooks, scheduled triggers)
- **Event-driven coordination** (webhook → workflow → callback)
- **Process orchestration** (multi-step processes with waiting)

## Architecture Components

### 1. RAW Workflows (The Workers)

RAW workflows are **pure functions** that:
- Take inputs
- Process data (API calls, transformations, LLM operations)
- Return outputs
- Are stateless and reusable

Example:
```python
# .raw/workflows/analyze-cv/run.py
class AnalyzeCVWorkflow(BaseWorkflow[CVParams]):
    @step("analyze")
    def analyze(self) -> dict:
        cv_text = self.params.cv_text
        score = self.llm.score_candidate(cv_text)
        return {"score": score, "qualified": score > 0.7}
```

### 2. FastAPI (The Coordinator)

FastAPI app provides:
- Webhooks for external triggers (form submissions, calendar events)
- REST API for status queries
- Database connection for state persistence
- Calls to RAW workflows via `subprocess` or Python imports

Example:
```python
# api/main.py
from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.post("/webhooks/cv-submission")
async def handle_cv_submission(cv: CVSubmission):
    # Save to database
    candidate = await db.candidates.create(cv)

    # Run RAW workflow for analysis
    result = subprocess.run([
        "raw", "run", "analyze-cv",
        "--cv-text", cv.text
    ], capture_output=True)

    # Update state based on result
    await update_candidate(candidate.id, result)

    return {"status": "processing"}
```

### 3. Temporal (The Orchestrator)

Temporal workflows manage:
- Multi-day processes
- Reliable scheduling (with retries)
- Durable state across service restarts
- Long-running processes with human interaction

Example:
```python
# workflows/temporal/hiring_process.py
@workflow.defn
class HiringProcess:
    @workflow.run
    async def run(self, candidate_id: str) -> str:
        # Step 1: Analyze CV (RAW workflow)
        analysis = await workflow.execute_activity(
            run_raw_workflow,
            args=["analyze-cv", f"--id={candidate_id}"],
            start_to_close_timeout=timedelta(minutes=5)
        )

        if not analysis["qualified"]:
            await send_rejection_email(candidate_id)
            return "rejected"

        # Step 2: Schedule call
        await send_scheduling_email(candidate_id)

        # Wait for calendar event (webhook will signal workflow)
        call_scheduled = await workflow.wait_condition(
            lambda: self.call_scheduled,
            timeout=timedelta(days=7)
        )

        # Step 3: Day of call (sleep until call time)
        await workflow.sleep_until(call_scheduled.call_time)

        # Trigger Twilio call
        await make_outbound_call(candidate_id)

        # Wait for call completion webhook
        await workflow.wait_condition(lambda: self.call_completed)

        # Step 4: Generate summary (RAW workflow)
        summary = await workflow.execute_activity(
            run_raw_workflow,
            args=["generate-call-summary", f"--id={candidate_id}"],
            start_to_close_timeout=timedelta(minutes=3)
        )

        return "completed"
```

### 4. Deployment (Docker + K8s)

Production deployment requires:
- **Docker Compose** for local development
- **Kubernetes manifests** for production
- **Helm charts** for configuration management

Example structure:
```
docker-compose.yml       # Local dev environment
k8s/
  deployment.yml         # API deployment
  service.yml            # API service
  ingress.yml            # External access
  postgres.yml           # Database
  temporal.yml           # Temporal server
```

## Common System Patterns

### Pattern 1: Webhook → RAW → Database

**Use case:** Form submission triggers analysis and saves results

**Components:**
- FastAPI webhook endpoint
- RAW workflow for processing
- PostgreSQL for state

**Flow:**
1. User submits form → POST /webhooks/submit
2. FastAPI saves to database (status: pending)
3. FastAPI calls `raw run analyze --id=123`
4. RAW workflow processes and returns result
5. FastAPI updates database (status: complete)

### Pattern 2: Temporal + RAW Multi-Day Process

**Use case:** Process spans multiple days with external events

**Components:**
- Temporal workflow for orchestration
- RAW workflows for data processing
- FastAPI for webhooks
- Database for state

**Flow:**
1. Trigger starts Temporal workflow
2. Workflow runs RAW workflow for initial processing
3. Workflow schedules reminder (sleeps until date)
4. External event triggers webhook → signals Temporal
5. Workflow continues execution
6. Workflow runs another RAW workflow for final step

### Pattern 3: Scheduled Reports

**Use case:** Daily/weekly reports generated and sent

**Components:**
- Kubernetes CronJob
- RAW workflow for report generation
- Email/Slack integration

**Flow:**
1. CronJob triggers at scheduled time
2. Runs `raw run generate-report --date=today`
3. RAW workflow queries database, generates report
4. Saves to S3 and sends notification

## Decision Tree

```
Does it need state across days? ────NO───→ Single RAW Workflow
    │
    YES
    │
    ↓
Does it need webhooks? ────NO───→ Temporal + RAW Workflows
    │
    YES
    │
    ↓
FastAPI + Temporal + RAW Workflows + Deployment
```

## Code Generation Checklist

When generating a multi-system architecture:

- [ ] Create RAW workflows for data processing
- [ ] Create FastAPI app with webhook endpoints
- [ ] Add database models (SQLAlchemy or Pydantic)
- [ ] Create Temporal workflows for orchestration
- [ ] Add Docker Compose for local dev
- [ ] Create Kubernetes manifests for production
- [ ] Add tests for each component
- [ ] Document the architecture in README.md

## Validation Gates

For multi-system architectures, add these gates:

```yaml
builder:
  gates:
    default:
      - validate      # RAW workflow validation
      - dry          # RAW workflow dry run
    optional:
      api-test:
        command: "pytest api/tests/ -v"
        timeout_seconds: 60
      temporal-validate:
        command: "temporal workflow validate"
        timeout_seconds: 30
      docker-validate:
        command: "docker-compose config"
        timeout_seconds: 10
```

## Key Principles

1. **RAW workflows are pure functions** - No state, no side effects beyond outputs
2. **FastAPI coordinates** - Handles webhooks, database, calls RAW workflows
3. **Temporal orchestrates** - Manages multi-day processes reliably
4. **Deploy everything together** - Docker Compose for dev, K8s for prod

This pattern keeps RAW workflows simple and reusable while building complex systems around them.
