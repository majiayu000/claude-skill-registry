---
name: fabric-spark-compute-remediate
description: Diagnose and resolve Microsoft Fabric Spark compute issues including HTTP 430 throttling errors, job queueing failures, slow session startup, autoscale problems, capacity SKU limits, environment publishing failures, library conflicts, node sizing, burst factor configuration, and VNet provisioning delays. Use when remediate Spark notebooks, Spark job definitions, lakehouse operations, starter pools, custom pools, or concurrency limits in Fabric workspaces.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric Spark Compute remediate

Structured diagnostic workflows for resolving Apache Spark compute issues in Microsoft Fabric Data Engineering and Data Science workloads.

## When to Use This Skill

- Spark jobs fail with HTTP 430 throttling or TooManyRequestsForCapacity errors
- Notebook or Spark job sessions are slow to start (>30 seconds)
- Environment publishing fails or hangs
- Autoscale is not scaling up or down as expected
- Jobs are queued indefinitely or expiring after 24 hours
- Custom pool creation fails or pools are undersized
- Library installation causes session startup delays
- Capacity appears exhausted despite low job counts
- VNet/Private Link provisioning adds unexpected delays
- Burst factor or job-level bursting behavior is unclear

## Prerequisites

- Workspace Admin or Capacity Admin role in Microsoft Fabric
- Access to the Monitoring Hub for active Spark sessions
- Access to Workspace Settings > Data Engineering/Science
- Knowledge of current Fabric capacity SKU (F2 through F2048)

## Quick Diagnostic: Identify Your Issue

**Start here.** Match your symptom to a diagnostic path:

| Symptom | Diagnostic Path |
|---------|----------------|
| HTTP 430 error | See [Throttling and Concurrency](./references/throttling-and-concurrency.md) |
| Jobs stuck in queue | See [Throttling and Concurrency](./references/throttling-and-concurrency.md#job-queueing) |
| Slow session startup | See [Session and Environment](./references/session-and-environment.md#slow-startup) |
| Environment publish fails | See [Session and Environment](./references/session-and-environment.md#publishing-failures) |
| Autoscale not working | See [Pool Configuration](./references/pool-configuration.md#autoscale) |
| Pool sizing questions | See [Pool Configuration](./references/pool-configuration.md#node-sizing) |
| Library conflicts | See [Session and Environment](./references/session-and-environment.md#library-issues) |
| VNet delay on first job | See [Session and Environment](./references/session-and-environment.md#vnet-delay) |

## Core Concepts

### Capacity Unit to VCore Mapping

Every Fabric capacity SKU provides Spark VCores at a fixed ratio with a 3x burst factor:

**1 Capacity Unit = 2 Spark VCores**

For an F64 SKU: 64 CU x 2 = 128 base VCores, with 3x burst = 384 max Spark VCores.

### Job Admission Model

Fabric Spark uses **optimistic job admission**: jobs are admitted based on their *minimum* core requirement (determined by the pool's minimum node setting). Jobs start with minimum nodes and scale up toward maximum nodes as cores become available. If no cores are available for the minimum requirement, the job is rejected or queued.

### Two Pool Types

- **Starter Pools**: Pre-warmed, medium nodes only, 5-10 second startup, always available
- **Custom Pools**: User-configured node sizes (Small through XX-Large), 2-5 minute cold start, full flexibility

## remediate Workflows

### Workflow 1: HTTP 430 Throttling

1. Confirm the error: `HTTP Response code 430: This Spark job can't be run because you have hit a Spark compute or API rate limit`
2. Open the Monitoring Hub and count active Spark sessions
3. Calculate your capacity's max VCores: `SKU CU × 2 × 3 (burst) = max VCores`
4. Compare active usage against max VCores
5. Resolve by canceling idle sessions, upgrading SKU, or enabling job queueing for pipeline/scheduler jobs

See [throttling-and-concurrency.md](./references/throttling-and-concurrency.md) for the full SKU limits table and queue configuration.

### Workflow 2: Slow Session Startup

1. Determine pool type (Starter vs Custom)
2. If Starter Pool with no custom libraries: expect 5-10 seconds; if slower, check capacity utilization
3. If custom libraries or Spark properties are attached via environment: expect 30 seconds to 5 minutes
4. If using non-Medium node size: Starter Pool fast-start is unavailable; expect 2-5 minutes (on-demand)
5. If Private Link is enabled and this is the first job: expect 10-15 minute VNet provisioning delay

See [session-and-environment.md](./references/session-and-environment.md) for detailed diagnosis.

### Workflow 3: Environment Publishing Failure

1. Check if another Publish action is already in progress (only one at a time)
2. Verify library compatibility with the selected Spark runtime version
3. If runtime was recently changed, remove incompatible libraries and republish
4. If Private Link is enabled, the first publish may trigger VNet provisioning (10-15 min delay)
5. Review the error notification for specific failure details

See [session-and-environment.md](./references/session-and-environment.md#publishing-failures) for resolution steps.

## Available Scripts

Run the [Spark capacity calculator](./scripts/Get-FabricSparkCapacity.ps1) to quickly determine VCore limits, max nodes, and queue limits for any Fabric SKU.

```powershell
# Calculate capacity for F64 SKU
./scripts/Get-FabricSparkCapacity.ps1 -SkuSize 64

# Compare multiple SKUs
./scripts/Get-FabricSparkCapacity.ps1 -SkuSize 64 -CompareWith 128,256
```

## Key Decision Points

### When to Use Starter Pools vs Custom Pools

Use **Starter Pools** when: you need fast startup (<10s), workloads fit Medium nodes (8 VCores, 64 GB), and you have no heavy library dependencies.

Use **Custom Pools** when: you need Large/X-Large/XX-Large nodes for memory-intensive workloads, you need precise control over min/max node counts, or you need to limit autoscale behavior.

### When to Enable Job-Level Bursting

**Enable** (default) when: you run large batch jobs that benefit from consuming all available burst VCores and concurrency is low.

**Disable** when: you have a multi-tenant environment with many concurrent users and fairness across teams matters more than single-job throughput.

Admin Portal path: Capacity Settings > Data Engineering/Science > Disable Job-Level Bursting toggle.

## References

- [Throttling and Concurrency Guide](./references/throttling-and-concurrency.md) — SKU limits, queue sizes, HTTP 430 resolution
- [Session and Environment Guide](./references/session-and-environment.md) — Startup delays, publishing, libraries, VNet
- [Pool Configuration Guide](./references/pool-configuration.md) — Node sizing, autoscale, custom pool setup, billing
