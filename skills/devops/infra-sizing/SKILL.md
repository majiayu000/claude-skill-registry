---
name: Infrastructure Sizing and Capacity Planning
description: Methods for determining the optimal resource allocation for compute, database, and network systems to balance cost and performance.
---

# Infrastructure Sizing and Capacity Planning

## Overview

Infrastructure sizing is the process of determining the exact amount of CPU, Memory, Storage, and Network capacity required for a workload. Effective sizing avoids both **Over-provisioning** (wasted money) and **Under-provisioning** (poor performance/outages).

**Core Principle**: "Sizing is not a one-time event; it is a continuous feedback loop based on real utilization metrics."

---

## 1. Right-Sizing Principles

Traditional sizing used the "Peak + Buffer" model, leading to massive waste. Modern sizing uses **Demand-Driven Allocation**.

| Principle | Description |
| :--- | :--- |
| **Utilization Thresholds**| Target 40-70% CPU utilization. Below 40% is over-provisioned; above 80% is risky. |
| **Vertical first...** | Increase resource limits for single-threaded or monolithic apps. |
| **...Horizontal usually**| Spread load across multiple small instances for resilience and elasticity. |
| **Metric-Based** | Use P95 or P99 metrics for latency, but Average for base capacity sizing. |

---

## 2. Compute Sizing (EC2, VMs, GCE)

### Step 1: Resource Profiling
Run your app in a staging environment and measure:
*   **CPU**: Is the app CPU-bound (mathematical calculations, compression)?
*   **Memory**: Is it memory-bound (caching, large payloads, in-memory DBs)?
*   **Thread Usage**: How many concurrent requests can one CPU core handle?

### Step 2: Instance Family Selection
| Family | Best For | AWS Example | GCP Example |
| :--- | :--- | :--- | :--- |
| **General Purpose** | Balanced workloads, small DBs | `t3`, `m6g` | `n2`, `e2` |
| **Compute Optimized**| Batch processing, high-traffic APIs | `c6g`, `c7i` | `c2`, `c3` |
| **Memory Optimized** | Redis, high-RAM DBs, Analytics | `r6g`, `x2` | `m1`, `m2` |

### Sizing Formula (Basic)
`Target Instances = (Total Peak Concurrent Requests * Avg Service Time per Req) / (Target Utilization per Core * Core Count)`

---

## 3. Database Sizing (RDS, Cloud SQL, Azure SQL)

### IOPS (Input/Output Operations Per Second)
Disk performance is often the bottleneck, not CPU.
*   **GP3 (AWS)**: Baseline 3,000 IOPS included. Provision more for heavy writes.
*   **Provisioned IOPS (io2)**: For high-performance transactional DBs.

### Storage Growth Calculation
`Required Storage = (Initial Data Size) + (Daily Ingest * Retention Period) * (1 + Overhead Buffer)`
*   *Buffer*: Always keep 20% free to allow for indexing and temp file creation.

### Connection Pool Sizing
`Max Connections = (Instance RAM / 10MB) - (System Reserve)`
*   Too many connections lead to high "Context Switching" and performance degradation.

---

## 4. Cache Sizing (Redis/Memcached)

Caching is a trade-off between **Memory Cost** and **Latency Benefits**.

### Formula: Working Set Size
Not all data needs to be in cache. Only store the **Working Set** (frequently accessed data).
1.  Measure Total Data Size.
2.  Analyze Access Distribution (Pareto Principle: 80% access to 20% data).
3.  **Cache Size = 20-30% of Total Data Size.**

### Eviction Policy Impact
*   **allkeys-lru**: Best for general caching.
*   **noeviction**: Returns errors when full (dangerous).

---

## 5. Container Sizing (Kubernetes)

Understanding the difference between **Requests** and **Limits** is critical for both stability and cost.

| Metric | Purpose | Cost Impact |
| :--- | :--- | :--- |
| **Requests** | Kubernetes guarantees this capacity. Used for scheduling. | **High**: Cloud Providers charge based on requests. |
| **Limits** | The maximum a pod can burst to. | **Low**: Generally doesn't impact cost unless using serverless K8s. |

### The "OOMKill" Trap
If `Memory Requests < Actual Usage`, the pod might be scheduled on a node that runs out of RAM, leading to an **OOMKill** (Out Of Memory).

---

## 6. Serverless Sizing (Lambda / Cloud Functions)

Serverless "scaling" is handled by the provider, but "sizing" (Memory allocation) is handled by you.

*   **Power Tuning**: In AWS Lambda, increasing Memory also increases CPU proportionaly.
*   **Strategy**: Use `AWS Lambda Power Tuning` to find the "Sweet Spot" where performance and cost intersect.

| Memory (MB) | Duration (ms) | Cost ($) | Result |
| :--- | :--- | :--- | :--- |
| 128 | 1000 | 0.0000021 | Slow |
| 512 | 200 | 0.0000016 | **Winner (Faster & Cheaper)** |
| 1024 | 150 | 0.0000025 | Diminishing returns |

---

## 7. Network and CDN Sizing

*   **Throughput**: Measure P99 payload size * Peak requests per second.
*   **CDN Coverage**: What % of your traffic can be served from the edge? 
    *   **Goal**: > 80% Cache Hit Ratio for static assets.
    *   **Impact**: CDN bandwidth is 50-70% cheaper than origin egress.

---

## 8. Load Testing for Capacity Planning

Never size based on assumptions. Use tools like **k6**, **Locust**, or **JMeter**.

1.  **Stepping Test**: Gradually increase users until latency spikes (The "Knee" of the curve).
2.  **Soak Test**: Run at 80% load for 24 hours to find memory leaks.
3.  **Stress Test**: Find the "Breaking Point" to configure failover/auto-scaling.

---

## 9. Monitoring for Right-Sizing

### The Dashboard Template (Grafana/Datadog)
*   **CPU Heatmap**: Identify idle periods (e.g., weekends).
*   **RAM Saturation**: Identify "Memory Bloat".
*   **Disk Queue Depth**: Identify IOPS bottlenecks.
*   **Network In/Out**: Identify efficient vs inefficient regions.

### Automated Right-Sizing Tools
*   **AWS Compute Optimizer**: Provides JSON recommendations for instance types.
*   **VPA (Vertical Pod Autoscaler)**: Automatically adjusts K8s requests/limits.
*   **Goldilocks**: A K8s dashboard that visualizes VPA recommendations.

---

## 10. Capacity Planning Template

| Component | Metric | Current Load | Growth (6mo) | Buffer | Target Spec |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Web Tier | Peak Req/sec | 500 | 2x (1000) | 20% | 4x c6g.large |
| Database | Storage | 500GB | +100GB/mo | 30% | 1.5TB GP3 |
| Cache | Working Set | 8GB | 12GB | 10% | 16GB Node |

---

## 11. Real Sizing Scenario: SaaS API
*   **Initial Setup**: 10 nodes of `m5.xlarge` (4 vCPU, 16GB RAM). Monthly cost: $1,400.
*   **Observation**: CPU average 12%, RAM average 40%.
*   **Analysis**: The app is memory-bound, but CPU is idle.
*   **Action**: Switched to 5 nodes of `t3.large` ($350/mo) + enabled Auto-scaling.
*   **Result**: 75% cost reduction while maintaining the same performance metrics.

---

## Related Skills
- `40-system-resilience/graceful-degradation`
- `42-cost-engineering/cloud-cost-models`
- `42-cost-engineering/budget-guardrails`
