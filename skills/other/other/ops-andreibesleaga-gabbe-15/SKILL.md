---
name: capacity-planning
description: Forecasting resource usage, load testing interpretation, and scaling limits.
role: ops-sre
triggers:
  - capacity
  - scaling
  - load test
  - rps
  - cpu usage
  - memory leak
---

# capacity-planning Skill

This skill guides the estimation of infrastructure needs based on usage patterns.

## 1. The Universal Formula
`Required Replicas = (Target RPS * Avg Request Latency) / Max Thread Utilization`

*Example*:
- Target: 1000 RPS
- Latency: 0.2s (200ms)
- 1 Core handles: 1 / 0.2 = 5 req/s (Sync) OR much higher if Async.
- **Rule of Thumb**: Run load tests to find "Breaking Point" RPS per instance.

## 2. Resource Dimensions

| Resource | Bottleneck Symptom | Mitigation |
|---|---|---|
| **CPU** | High latency, timeouts. | Horizontal Scale (add replicas). |
| **Memory** | OOM Kills, Crash loops. | Vertical Scale (larger pods), fix leaks. |
| **Disk IO** | High IOWAIT, slow DB. | Provision IOPS (GP3/IO1), cache reads. |
| **Network** | Bandwidth limits, packet loss. | Compress data, reduce payload size. |
| **DB Connect** | "Too many connections". | Connection Pooling (PgBouncer). |

## 3. Creating a Capacity Plan (Template)
Use `templates/ops/CAPACITY_PLAN_TEMPLATE.md`.

1.  **Baseline**: Current usage (Peak CPU %, Avg RAM).
2.  **Growth Factor**: "Marketing launching new campaign, expect 3x traffic".
3.  **Headroom**: Always provision +30% buffer for spikes.
4.  **Limits**: What hits the ceiling first? (Usually the DB).

## 4. Load Testing
- **Tools**: k6, Artillery, Locust.
- **Pattern**:
  1.  **Smoke**: 1 VUser (Verify logic).
  2.  **Load**: Target RPS (Verify stability).
  3.  **Stress**: Ramp until crash (Find the limit).
  4.  **Soak**: Run 96% load for 4 hours (Find memory leaks).

## 5. Auto-Scaling Rules (HPA)
- **Don't scale on CPU alone**. If app is IO bound, CPU might be low while app is dead.
- **Scale Up Fast**: Reaction time < 1 min.
- **Scale Down Slow**: Stabilization window > 5 mins (prevent flapping).
