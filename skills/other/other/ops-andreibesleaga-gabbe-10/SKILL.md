---
name: production-verifier
description: Post-deployment smoke tests, synthetic user checks, and "Canary" validation in Prod.
role: ops-sre
triggers:
  - verify prod
  - smoke test prod
  - canary check
  - synthetic
  - post deploy
---

# production-verifier Skill

This skill verifies the system *after* it has crossed the finish line.

## 1. Safety First
- **Read-Only**: Production tests should mostly be read-only (GET /health, GET /user).
- **Test User**: If writing, use a specific `test_bot` user account. Do NOT delete real data.

## 2. Canary Validation
1.  Deploy to 10% of traffic.
2.  Check Error Rate (5xx).
3.  Check Latency (p95).
4.  Check Business Metrics (Orders/sec).
5.  If variance > 5% from Baseline -> **Rollback**.

## 3. Synthetic Monitoring
- Create a scripted browser journey (Playwright) that runs every 5 mins.
- "Login -> Search 'Apple' -> Verify Result".
- If this fails, page the on-call engineer.

## 4. Verification Checklist
- [ ] `/healthz` endpoint returns 200 OK.
- [ ] Database is reachable.
- [ ] Cache is reachable.
- [ ] CDN is serving assets.
- [ ] SSL Certificate is valid.
