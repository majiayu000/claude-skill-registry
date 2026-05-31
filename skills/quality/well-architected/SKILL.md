---
name: well-architected
description: 6-pillar architecture review framework. Adapted from AWS Well-Architected for use by great_cto's architect agent on every non-nano ARCH document. Forces explicit answers across operational excellence, security, reliability, performance, cost, and sustainability — not just feature design.
when_to_use: |
  Apply when:
  - architect is writing ARCH-*.md for small/medium/large/enterprise project_size
  - regulated-reviewer or security-officer is auditing an existing system
  - project-auditor is reviewing a brownfield codebase
  Do NOT apply to:
  - nano project_size (overhead exceeds value)
  - bug-fix tasks (no architecture change)
  - pure refactor with no behaviour change
effort: high
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/decisions/**"
  - "src/**"
---

# Well-Architected — 6 pillars to verify before shipping

Every ARCH document for non-nano work must answer the 6 pillar questions
below. Skipping a pillar is allowed only if explicitly justified (e.g.
"Sustainability: N/A — backend-only, runs in shared infra.").

This is adapted from AWS Well-Architected (lens: small-team SaaS / LLM
applications), trimmed to questions that matter at <10 engineer scale.

## Pillar 1 — Operational excellence

### Questions

1. **Observability:** What metrics, logs, traces do we emit? How do we
   tell from a dashboard if this is working in prod?
2. **Deployability:** How do we ship a change? CI gates? Rollback path?
3. **Runbooks:** When this breaks at 3am, what does on-call read?

### Pass criteria

- ✅ One metric per business outcome (e.g. webhook-deliveries-acked)
- ✅ One log line per request, with request-id correlatable across services
- ✅ Deploy path is documented and tested (rollback dry-run executed)
- ✅ Runbook covers top-3 failure modes from pre-mortem

### Common fail

❌ "We'll add monitoring later." Monitoring is part of the feature.

## Pillar 2 — Security

### Questions

1. **Trust boundaries:** Where does untrusted data enter? How is it
   validated/sanitized?
2. **Authn / authz:** Who can call this? Who can read/write the data?
3. **Secrets:** Where are API keys, DB passwords, JWT signing keys stored?
4. **Data classification:** PII? PHI? PCI cardholder data? What's the
   retention policy?

### Pass criteria

- ✅ Every external input has explicit validation at the boundary
- ✅ Authz is enforced at the data layer, not just UI
- ✅ Secrets in env vars or secret manager, never in source
- ✅ Sensitive data classified and retention policy defined

### Common fail

❌ "JWT validates the user, that's our authz." JWT is authentication.
Authorization is separate (this user can read THIS row).

## Pillar 3 — Reliability

### Questions

1. **Failure modes:** What happens when a downstream dependency is slow
   / down / corrupted?
2. **Idempotency:** Can a retried request safely re-execute?
3. **Backups & recovery:** What's the RPO (data-loss tolerance)? RTO
   (downtime tolerance)? Test plan for both?
4. **Capacity:** What's the max QPS this can handle? What happens at 1.5x that?

### Pass criteria

- ✅ Circuit breakers / timeouts on external calls
- ✅ State-mutating endpoints accept idempotency keys
- ✅ Backups documented + restore tested in the last 90 days
- ✅ Load test exists; results in `docs/perf/`

### Common fail

❌ "Postgres has backups." Backups without a tested restore aren't backups.

## Pillar 4 — Performance efficiency

### Questions

1. **SLOs:** What's the p50/p95/p99 latency target? Error rate?
   Availability?
2. **Bottlenecks:** Profile the critical path — what's the slowest step?
3. **Caching:** What's cacheable? Cache invalidation strategy?
4. **Scaling:** Vertical or horizontal? Auto-scale rules?

### Pass criteria

- ✅ SLO numbers in the ARCH doc (not "fast enough")
- ✅ Profile attached for non-trivial requests
- ✅ Cache strategy documented; invalidation explicit
- ✅ Scaling decision justified by data, not "feels right"

### Common fail

❌ "Database can handle it." Quantify: queries/sec, row count, index hit rate.

## Pillar 5 — Cost optimization

### Questions

1. **Hot path:** What's the most expensive operation per request? Why?
2. **Right-sizing:** Is the chosen instance type / model / DB tier the
   smallest one that meets SLO?
3. **Cleanup:** What happens to old data? Old logs? Old branch
   environments?

### Pass criteria

- ✅ Use skill `cost-model` to document explicit $ numbers
- ✅ Choose smallest LLM model that meets quality SLO (haiku before sonnet,
  sonnet before opus)
- ✅ Retention policy for logs, metrics, old data

### Common fail

❌ Defaulting to Opus / GPT-4 when Haiku would work. Test on Haiku first.

## Pillar 6 — Sustainability (env / energy)

### Questions

1. **Workload efficiency:** Is the code O(n log n) when it could be O(n)?
2. **Idle resources:** Can dev environments scale to zero overnight?
3. **Data minimization:** Do we collect / store data we never query?

### Pass criteria

- ✅ Hot loop complexity documented
- ✅ Non-prod resources have shutdown schedules
- ✅ Data lifecycle covers ingestion, retention, deletion

### Common fail

❌ Logs at debug level in prod, never reviewed. Waste of storage + carbon.

## Output format — add to ARCH

```markdown
## Well-Architected review

### 1. Operational excellence
- Metrics: <list>
- Deploy path: <link to runbook>
- Verdict: PASS | RISKS LISTED

### 2. Security
- Trust boundaries: <list>
- Data classification: <PII / PHI / PCI / none>
- Verdict: PASS | RISKS LISTED

### 3. Reliability
- Failure modes: <link to pre-mortem>
- Idempotency: <yes/no per endpoint>
- Verdict: PASS | RISKS LISTED

### 4. Performance
- SLOs: p99=<ms>, error_rate=<%>, availability=<%>
- Verdict: PASS | RISKS LISTED

### 5. Cost
- Per-request cost: $<amount>
- Verdict: PASS | RISKS LISTED

### 6. Sustainability
- Hot-path complexity: O(<n>)
- Verdict: PASS | N/A | RISKS LISTED

## Open risks (rolled up)

<bullet list of all RISKS LISTED items + mitigation in plan>
```

## When PASS is acceptable with risks listed

Not every architecture is bulletproof. PASS-with-risks is OK if:
- Each risk is explicit (not hand-waved)
- Each risk has either a mitigation in the plan OR explicit acceptance
  by the user
- The pre-mortem section addresses the top-3 risk-score items

Gate:plan can approve a PASS-with-risks; gate:ship needs the mitigations
shipped.
