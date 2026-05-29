---
sidebar_position: 10
title: "Finalize Your Dapr Skill"
description: "Complete and test your dapr-deployment skill for production use, adding safety guardrails and validating coverage across all building blocks"
keywords: [dapr, skill finalization, production readiness, safety guardrails, distributed systems, sidecar, building blocks]
chapter: 53
lesson: 10
duration_minutes: 20

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill Validation and Testing"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Evaluate"
    digcomp_area: "5. Problem Solving"
    measurable_at_this_level: "Student tests skill against multiple prompts covering all building blocks and identifies gaps"

  - name: "Safety Guardrail Design"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Evaluate"
    digcomp_area: "4. Safety"
    measurable_at_this_level: "Student adds NEVER/ALWAYS guardrails to skill based on common production errors"

  - name: "Production Pattern Recognition"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Evaluate"
    digcomp_area: "5. Problem Solving"
    measurable_at_this_level: "Student recognizes common Dapr errors and adds diagnostic guidance to skill"

learning_objectives:
  - objective: "Complete and test dapr-deployment skill for production use"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Skill passes 5 test prompts covering Helm deployment, state management, pub/sub, jobs, and secrets"

  - objective: "Add safety guardrails that prevent common production errors"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Skill includes NEVER/ALWAYS sections with sidecar readiness, secrets handling, and mTLS guidance"

  - objective: "Include diagnostic patterns for common Dapr errors"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Skill contains error table with causes and fixes for ERR_STATE_STORE_NOT_FOUND, ERR_PUBSUB_NOT_FOUND, connection refused"

cognitive_load:
  new_concepts: 0
  assessment: "No new concepts - refinement and validation of existing knowledge. Consolidates patterns from L01-09 into production-ready skill."

differentiation:
  extension_for_advanced: "Add Dapr resilience policies, custom middleware configuration, and multi-cluster deployment patterns to skill"
  remedial_for_struggling: "Focus on 3 core building blocks (state, pubsub, invoke) and 2 critical safety rules (sidecar readiness, secrets management)"
---

# Finalize Your Dapr Skill

You've built a `dapr-deployment` skill in Lesson 0 and refined it through nine lessons. Each lesson added patterns: sidecar architecture, building blocks vs components, Helm deployment, state management, pub/sub messaging, service invocation, bindings, the Jobs API, secrets, and configuration.

Now it's time to make that skill production-ready.

A skill isn't complete when it covers all the topics. It's complete when it helps you avoid the mistakes you'd make without it. This lesson focuses on three things: testing your skill against real prompts, adding safety guardrails that prevent production disasters, and documenting the errors you'll encounter so you can fix them quickly.

---

## Review: What Your Skill Should Cover

Throughout this chapter, you've added patterns to your skill after each lesson. Here's what a complete `dapr-deployment` skill should include:

| Lesson | Pattern Added | Check Your Skill |
|--------|---------------|------------------|
| L01 | Sidecar architecture explanation | Translator analogy, daprd ports (3500/50001), Kubernetes annotations |
| L02 | Building blocks vs components distinction | APIs vs implementations, component YAML structure, backend swapping |
| L03 | Helm deployment + state patterns | Helm commands for Dapr 1.14+, state component YAML, ETag concurrency |
| L04 | Service invocation patterns | `invoke_method()` usage, app-id discovery, mTLS automatic |
| L05 | Pub/Sub patterns | `publish_event()`, subscription decorators, CloudEvents format |
| L06 | Binding patterns | Input bindings (triggers), output bindings (external calls) |
| L07 | Jobs API patterns | Job creation, scheduling, one-time vs recurring |
| L08 | Secrets/config patterns | `get_secret()`, secrets component, configuration subscriptions |
| L09 | Complete integration example | Full FastAPI app with state + pub/sub + invoke |

Open your skill file and check each row. If something's missing, this is the lesson to add it.

---

## Test Your Skill Against Production Prompts

A skill that only works for the examples you learned from isn't production-ready. Test it against prompts that simulate real deployment scenarios.

### Test Prompt 1: Kubernetes Deployment

```
Using my dapr-deployment skill, deploy Dapr 1.14 on a fresh Kubernetes cluster.
Show me the Helm commands and how to verify all control plane pods are running.
```

**Expected skill output should include:**

```bash
# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Install Dapr control plane
helm upgrade --install dapr dapr/dapr \
  --version=1.14.0 \
  --namespace dapr-system \
  --create-namespace \
  --wait

# Verify installation
kubectl get pods -n dapr-system
```

Plus verification that you see: `dapr-operator`, `dapr-sidecar-injector`, `dapr-sentry`, `dapr-placement-server`, `dapr-scheduler-server`.

**If your skill fails this test:** Add the Helm deployment section from Lesson 03.

### Test Prompt 2: State Management

```
Using my dapr-deployment skill, add state management to my FastAPI app.
I need to save and retrieve task objects using Redis as the backend.
Show me the component YAML and Python code.
```

**Expected skill output should include:**

State component YAML:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: redis-master.default.svc.cluster.local:6379
```

Python code using DaprClient:
```python
from dapr.clients import DaprClient
import json

with DaprClient() as client:
    # Save state
    client.save_state(
        store_name='statestore',
        key='task-123',
        value=json.dumps({'title': 'Buy groceries', 'status': 'pending'})
    )

    # Get state
    state = client.get_state(store_name='statestore', key='task-123')
    task = json.loads(state.data) if state.data else None
```

**If your skill fails this test:** Add the state management patterns from Lesson 03.

### Test Prompt 3: Pub/Sub Setup

```
Using my dapr-deployment skill, set up pub/sub messaging for my FastAPI service.
I need to publish task events and subscribe to them in another service.
```

**Expected skill output should include:**

Pub/sub component YAML:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
    - name: redisHost
      value: redis-master.default.svc.cluster.local:6379
```

Publishing code:
```python
from dapr.clients import DaprClient
import json

with DaprClient() as client:
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='task-events',
        data=json.dumps({'event_type': 'task.created', 'task_id': 'task-123'}),
        data_content_type='application/json'
    )
```

Subscription code:
```python
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub='pubsub', topic='task-events')
async def handle_task_event(event_data: dict):
    print(f"Received: {event_data}")
    return {"status": "SUCCESS"}
```

**If your skill fails this test:** Add the pub/sub patterns from Lesson 05.

### Test Prompt 4: Scheduled Job

```
Using my dapr-deployment skill, schedule a recurring cleanup job that runs
every hour to remove completed tasks older than 7 days.
```

**Expected skill output should include:**

Jobs API usage:
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Schedule recurring job
    client.start_workflow(
        workflow_component='dapr',
        workflow_name='cleanup-job',
        input={'retention_days': 7}
    )
```

Or the Jobs API endpoint pattern:
```http
POST http://localhost:3500/v1.0/jobs/cleanup-old-tasks
Content-Type: application/json

{
  "schedule": "@every 1h",
  "data": {"retention_days": 7}
}
```

**If your skill fails this test:** Add the Jobs API patterns from Lesson 07.

### Test Prompt 5: Secrets Configuration

```
Using my dapr-deployment skill, configure my FastAPI service to retrieve
API keys from Kubernetes secrets instead of environment variables.
```

**Expected skill output should include:**

Secrets component YAML:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

Python code:
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    secret = client.get_secret(
        store_name='kubernetes-secrets',
        key='api-credentials'
    )
    api_key = secret.secret.get('api-key')
```

**If your skill fails this test:** Add the secrets management patterns from Lesson 08.

---

## Add Safety Guardrails

Your skill should prevent production mistakes, not just show working patterns. Add these guardrails to your `dapr-deployment` skill.

### NEVER

Add a "Safety: NEVER" section to your skill:

```markdown
## Safety: NEVER

- **Call Dapr before sidecar is ready** - Your app will get connection refused errors. Always wait for sidecar health check.

- **Hardcode component names** - Use configuration or environment variables. Component names may differ between environments.

- **Skip error handling for Dapr API calls** - Dapr calls can fail (sidecar not ready, component misconfigured, backend unavailable). Always wrap in try/except.

- **Store sensitive data in state without encryption** - State stores are not encrypted by default. Use secrets component for credentials, or enable encryption at the component level.

- **Expose Dapr HTTP/gRPC ports externally** - Dapr's sidecar ports (3500, 50001) are for internal pod communication only. External access bypasses mTLS.

- **Use `dapr.io/app-port` for gRPC apps without specifying protocol** - If your app uses gRPC, set `dapr.io/app-protocol: "grpc"` or Dapr will send HTTP to your gRPC server.
```

### ALWAYS

Add a "Safety: ALWAYS" section to your skill:

```markdown
## Safety: ALWAYS

- **Wait for sidecar readiness** before making Dapr calls:
  ```python
  import httpx
  import asyncio

  async def wait_for_sidecar(timeout: int = 30):
      """Wait for Dapr sidecar to be ready."""
      async with httpx.AsyncClient() as client:
          for _ in range(timeout):
              try:
                  response = await client.get("http://localhost:3500/v1.0/healthz")
                  if response.status_code == 204:
                      return True
              except httpx.ConnectError:
                  pass
              await asyncio.sleep(1)
          raise RuntimeError("Dapr sidecar not ready")
  ```

- **Use secrets component for credentials** - Never put passwords in component YAML. Use `secretKeyRef`:
  ```yaml
  metadata:
    - name: redisPassword
      secretKeyRef:
        name: redis-secret
        key: password
  ```

- **Enable mTLS in production** - Dapr enables mTLS by default when Sentry is running. Verify with:
  ```bash
  kubectl get pods -n dapr-system | grep sentry
  ```

- **Configure retry policies** for resilience:
  ```yaml
  apiVersion: dapr.io/v1alpha1
  kind: Resiliency
  metadata:
    name: myresiliency
  spec:
    policies:
      retries:
        myRetryPolicy:
          policy: constant
          duration: 1s
          maxRetries: 3
  ```

- **Set resource limits on sidecar** to prevent resource contention:
  ```yaml
  annotations:
    dapr.io/sidecar-cpu-limit: "500m"
    dapr.io/sidecar-memory-limit: "256Mi"
  ```
```

---

## Common Errors Reference

Add this error table to your skill. When something breaks, this is the first place you'll look.

```markdown
## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ERR_STATE_STORE_NOT_FOUND` | State component not configured or not in same namespace | Apply component YAML: `kubectl apply -f components/statestore.yaml` |
| `ERR_PUBSUB_NOT_FOUND` | Pub/sub component not configured | Apply component YAML: `kubectl apply -f components/pubsub.yaml` |
| `connection refused :3500` | Sidecar not ready when app starts | Add startup probe or wait for `/v1.0/healthz` before Dapr calls |
| `ERR_DIRECT_INVOKE` | Target app-id not found | Check target has `dapr.io/app-id` annotation and is running |
| `DEADLINE_EXCEEDED` | Request timeout | Increase timeout or check if target service is overloaded |
| `sidecar not found` | Sidecar injection not enabled | Check `dapr.io/enabled: "true"` annotation and namespace has injection enabled |
| `ERR_SECRET_STORE_NOT_FOUND` | Secrets component not configured | Apply secrets component YAML |
| `ERR_PUBSUB_FORBIDDEN` | App not in component's scope | Add app-id to component's `scopes` list |
```

---

## Final Validation: Complete Integration Test

Run this prompt against your skill as a final validation:

```
Using my dapr-deployment skill, generate a complete Dapr setup for:
- A FastAPI service that saves tasks to state store
- Publishes events to pub/sub when tasks are created
- Calls a notification service via service invocation
- Schedules a daily cleanup job
- Gets API keys from Kubernetes secrets

Show all component YAMLs, Python code, and Kubernetes deployment manifest.
```

A production-ready skill should generate:

1. **Component YAMLs**: statestore, pubsub, kubernetes-secrets
2. **Python code**: Complete FastAPI app with DaprClient
3. **Kubernetes manifest**: Deployment with Dapr annotations
4. **Sidecar readiness**: Health check before Dapr calls
5. **Error handling**: Try/except around Dapr operations

If your skill generates incomplete or incorrect output, identify the gap and add the missing pattern.

---

## Your Growing Skills Library

Your `dapr-deployment` skill joins a growing collection of production-ready tools:

```
.claude/skills/
+-- skill-creator/
+-- fetching-library-docs/
+-- fastapi-agent-api/       # Chapter 40
+-- docker-deployment/       # Chapter 49
+-- kubernetes-deployment/   # Chapter 50
+-- helm-chart/              # Chapter 51
+-- kafka-events/            # Chapter 52
+-- dapr-deployment/         # This chapter - COMPLETE
```

Each skill compounds your capability. The `dapr-deployment` skill doesn't just know Dapr patterns---it encodes the safety guardrails and error diagnostics you'd otherwise learn through production incidents.

That's the value of skill-first learning. You don't just learn Dapr. You build an asset that makes every future Dapr project faster and safer.

---

## Try With AI

You've completed your `dapr-deployment` skill. Use AI to validate, extend, and stress-test it.

### Prompt 1: Coverage Audit

```
Review my dapr-deployment skill. Does it cover all 6 building blocks from
Chapter 53?

The building blocks are:
1. State Management
2. Pub/Sub Messaging
3. Service Invocation
4. Bindings (input and output)
5. Secrets Management
6. Jobs API

For each building block, tell me:
- Is it covered in my skill? (Yes/No)
- Is the coverage complete? (Component YAML + Python code + common patterns)
- What's missing?

[Paste your SKILL.md content here]
```

**What you're learning:** External review reveals blind spots. You may have excellent state management coverage but missed input bindings entirely. This prompt forces a systematic audit of completeness.

---

### Prompt 2: Safety Guardrails Review

```
I've added safety guardrails to my dapr-deployment skill. Review them and tell me:

1. Are my NEVER rules comprehensive? What production mistakes am I still vulnerable to?
2. Are my ALWAYS rules actionable? Can someone follow them without additional research?
3. What guardrails do experienced Dapr operators add that I'm missing?

Current guardrails:

NEVER:
- Call Dapr before sidecar is ready
- Hardcode component names
- Skip error handling
- Store secrets in state
- Expose Dapr ports externally

ALWAYS:
- Wait for sidecar readiness
- Use secretKeyRef for credentials
- Enable mTLS in production
- Configure retry policies
- Set sidecar resource limits
```

**What you're learning:** Safety guardrails emerge from production experience. AI can surface patterns from thousands of Dapr deployments, identifying risks you haven't encountered yet.

---

### Prompt 3: Stress Test

```
Test my dapr-deployment skill by generating a complete Dapr-enabled microservice
from scratch. The service should:

- Accept HTTP requests to create orders
- Save order state with ETag-based optimistic concurrency
- Publish order.created events to pub/sub
- Call inventory-service to check stock via service invocation
- Retrieve Stripe API keys from secrets
- Schedule order cleanup job for midnight daily

Generate all YAMLs, Python code, and Kubernetes manifests.

After generating, evaluate: Did my skill produce production-ready output?
What was missing or incorrect?
```

**What you're learning:** Real-world scenarios expose gaps. An order system has different patterns than a task system---different event types, different concurrency requirements, different integration points. This stress test validates that your skill generalizes beyond the Task API examples.

**Safety Note:** When deploying Dapr-enabled services to production clusters, always verify component configurations in a staging environment first. Misconfigured components can cause silent data loss (state not persisted) or message drops (pub/sub misconfigured). Your skill provides patterns; you validate they match your specific infrastructure.
