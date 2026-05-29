---
name: setup-batch-job-workers
description: Sets up scheduled batch jobs via RabbitMQ following ModuleImplementationGuide.md §9.6. Creates BatchJobScheduler (node-cron, publish workflow.job.trigger) in workflow-orchestrator and BatchJobWorker (consume bi_batch_jobs, run job, publish workflow.job.completed/failed) in worker containers. Use when adding risk-clustering, account-health, industry-benchmarks, risk-snapshot-backfill, or similar cron-driven jobs.
---

# Setup Batch Job Workers

Implements the **Scheduler + RabbitMQ** pattern (ModuleImplementationGuide §9.6, BI_SALES_RISK_IMPLEMENTATION_PLAN §9.3). RabbitMQ only; no separate job-queue product.

## 1. Scheduler (workflow-orchestrator or similar)

**Path:** `src/jobs/BatchJobScheduler.ts`

- Use **node-cron**. For each schedule, call `publish('workflow.job.trigger', { job, metadata: { schedule, triggeredAt }, triggeredBy: 'scheduler', timestamp })` to exchange `coder_events` (routing key `workflow.job.trigger`).
- **Jobs (full list: BI_SALES_RISK_IMPLEMENTATION_PLAN §9.3):** `risk-clustering`, `account-health`, `industry-benchmarks`, `risk-snapshot-backfill`, `propagation`, `model-monitoring`, **`outcome-sync`**. outcome-sync (risk-analytics): `0 1 * * *`, query closed opportunities, publish `opportunity.outcome.recorded`. model-monitoring: `0 6 * * 0` (weekly).
- Config: `batch_jobs.schedules` or env, e.g. `RISK_CLUSTERING_CRON=0 2 * * *`.

**Start in server.ts:** `await batchJobScheduler.start()`.

## 2. Queue Setup

- Queue: **`bi_batch_jobs`** (or from config). Durable. Bound to `coder_events` with routing key `workflow.job.trigger`.
- Config in workflow-orchestrator (publish) and each worker (consume): `rabbitmq.queue_batch_jobs: bi_batch_jobs`.

## 3. Worker (risk-analytics, analytics-service, etc.)

**Path:** `src/events/consumers/BatchJobWorker.ts`

- `EventConsumer` (or equivalent) consuming from `bi_batch_jobs` with bindings `['workflow.job.trigger']`.
- Handler: `const { job, metadata } = msg; switch (job) { case 'risk-clustering': await riskClusteringService.runBatchJob(); break; ... }`.
- On success: `publish('workflow.job.completed', { job, status: 'success', completedAt })`.
- On failure: `publish('workflow.job.failed', { job, error: err.message, failedAt })`; then rethrow or nack for retry.

**Start in server.ts:** `await batchJobWorker.start()`.

## 4. Config

**workflow-orchestrator config/default.yaml:**
```yaml
rabbitmq:
  url: ${RABBITMQ_URL}
  exchange: coder_events
batch_jobs:
  queue: bi_batch_jobs
  schedules:
    risk-clustering: ${RISK_CLUSTERING_CRON:-"0 2 * * *"}
    account-health: ${ACCOUNT_HEALTH_CRON:-"0 3 * * *"}
    industry-benchmarks: ${INDUSTRY_BENCHMARKS_CRON:-"0 4 * * *"}
    risk-snapshot-backfill: ${RISK_SNAPSHOT_BACKFILL_CRON:-"0 1 * * 0"}
    propagation: ${PROPAGATION_CRON:-"0 5 * * *"}
```

**Worker container:** ensure `rabbitmq` has `queue: bi_batch_jobs` (or `queue_batch_jobs`) and binding `workflow.job.trigger`.

## 5. Checklist

- [ ] BatchJobScheduler in workflow-orchestrator: cron → publish `workflow.job.trigger`
- [ ] Queue `bi_batch_jobs` asserted and bound to `coder_events` + `workflow.job.trigger`
- [ ] BatchJobWorker in each worker: consume `bi_batch_jobs`, switch(job), run service, publish completed/failed
- [ ] Config: schedules (cron) and `rabbitmq.queue` / `queue_batch_jobs`
- [ ] No Azure Service Bus, no separate job-queue; RabbitMQ only
