---
name: backend-reliability-enforcer
description: 'Use when implementing backend APIs, data persistence, or external integrations.
  Enforces TodoWrite with 25+ items. Triggers: "backend API", "REST endpoint", "external
  integration", "data persistence".'
---

---
name: backend-reliability-enforcer
description: Use when implementing backend APIs, data persistence, or external integrations. Enforces TodoWrite with 25+ items. Triggers: "backend API", "REST endpoint", "external integration", "data persistence". If thinking "just a quick endpoint" - use this.
---

# Backend Reliability Enforcer

## Payment Operations?

**If implementing payment, billing, subscription, or financial transactions:**
→ Use `payment-operations-enforcer` skill FIRST (NON-NEGOTIABLE)
→ Then return here for general reliability requirements

---

## TodoWrite Requirements

**CREATE TodoWrite with 5 sections (25+ items total):**

| Section | Min Items |
|---------|-----------|
| Fault Tolerance | 5+ |
| Error Handling | 5+ |
| Data Integrity | 5+ |
| Security | 5+ |
| Observability | 5+ |

---

## Verification Checkpoint

Verify 3 random items have ALL THREE:
- ✓ Concrete numbers ("5 failures/10s", "15s timeout", "100 req/min")
- ✓ Specific tools ("Opossum", "pino", "Joi", "Knex", "Redis")
- ✓ Measurable outcome ("generates UUID v4 correlation ID")

| ❌ FAILS | ✅ PASSES |
|----------|-----------|
| "Add error handling" | "pino logging: UUID v4 correlation ID, format `{correlationId, level, timestamp, service, message}`" |
| "Validate input" | "Joi schema: `amount` (number, positive, max 999999), `currency` (ISO 4217). Return 400 with `{error, fields}`" |
| "Add circuit breaker" | "Opossum: 5 failures/10s threshold, 30s reset, fallback to cached data" |

---

## Section Requirements

### Fault Tolerance (5+ items)

- [ ] Circuit breaker for ALL external calls (Opossum: 5 failures/10s, 30s reset)
- [ ] Retry with exponential backoff (3 retries: 100ms, 200ms, 400ms)
- [ ] Timeouts for all I/O (15s API calls, 5s database)
- [ ] Graceful degradation (cached data, disable non-critical features)
- [ ] Health checks (`/health` endpoint with dependency status)

### Error Handling (5+ items)

- [ ] Comprehensive error handling (try/catch, error middleware)
- [ ] Correlation IDs (UUID v4 on ingress, propagate to all logs/services)
- [ ] Structured logging (pino/winston with correlation ID)
- [ ] Error responses (400/401/403/404/422/500, never expose stack traces)
- [ ] Error metrics/alerts (Prometheus counter, alert if error rate > 5%)

### Data Integrity (5+ items)

- [ ] Input validation at API boundaries (Joi/Zod schemas)
- [ ] Database transactions for consistency (Knex/Prisma transactions)
- [ ] Idempotency keys for retryable operations (`Idempotency-Key` header, Redis 24h)
- [ ] Data retention policies (auto-delete soft-deleted after 90 days)
- [ ] Audit trails for sensitive modifications (who, what, when, old/new)

### Security (5+ items)

- [ ] Authentication on all endpoints (JWT/OAuth/API keys)
- [ ] Authorization checks (RBAC, verify permissions)
- [ ] Input sanitization (parameterized SQL, XSS prevention)
- [ ] Encryption (AES-256 at rest, TLS 1.3 in transit)
- [ ] Rate limiting (100 req/min per IP, express-rate-limit)

### Observability (5+ items)

- [ ] Structured logging (INFO/WARN/ERROR levels)
- [ ] Key metrics (latency P50/P95/P99, throughput, error rate)
- [ ] Distributed tracing (OpenTelemetry with trace/span IDs)
- [ ] Dashboards/alerts (Grafana, PagerDuty for SLO breaches)
- [ ] Runbook documentation (investigation, rollback, escalation)

---

## Red Flags - STOP When You Think:

| Thought | Reality |
|---------|---------|
| "Add reliability later" | 80% never added, retrofitting costs 10x |
| "That edge case is unlikely" | Unlikely × scale = frequent |
| "Circuit breaker is overkill" | One slow service = cascade failure |
| "Customer needs it in 3 days" | Broken code causes MORE delay |

---

## Response Templates

### "Add Reliability Later"

❌ **BLOCKED**: Cannot defer reliability requirements.

- 80% of "later" items never get added
- Retrofitting costs 10x more than building in from start
- Production incidents cost $5K-50K per incident + customer trust

**Required to override:**
1. Specific retrofit date (not "later")
2. Budget allocated (engineer-weeks)
3. Risk acceptance signed by decision maker
4. Interim mitigation plan (reduced traffic limits? 24/7 on-call?)

---

## Self-Grading Before Complete

```
[ ] 25+ items across 5 sections
[ ] 80%+ have concrete numbers
[ ] 80%+ name specific tools
[ ] 100% have measurable outcomes
[ ] 3 random items passed specificity test
[ ] Payment operations: delegated to payment-operations-enforcer

Grade 7+/8: Ready to proceed
Grade <7: Revise TodoWrite
```
