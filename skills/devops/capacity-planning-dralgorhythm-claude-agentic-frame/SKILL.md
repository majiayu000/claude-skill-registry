---
name: capacity-planning
description: Plan infrastructure capacity for expected load. Use when sizing systems, planning for growth, or analyzing resource requirements. Covers load estimation and resource sizing.
allowed-tools: Read, Bash, Glob, Grep
---

# Capacity Planning

## Workflows

- [ ] **Baseline**: Measure current resource usage
- [ ] **Forecast**: Project future growth
- [ ] **Size**: Calculate required resources
- [ ] **Buffer**: Add headroom for spikes
- [ ] **Monitor**: Track actual vs. predicted

## Key Metrics

### Compute
- CPU utilization (target: 60-70%)
- Memory usage
- Request latency (P50, P95, P99)

### Storage
- Disk IOPS
- Throughput (MB/s)
- Capacity growth rate

### Network
- Bandwidth utilization
- Connection counts
- Packet loss

## Estimation Framework

### Little's Law
```
L = λ × W

L = Average number of items in system
λ = Average arrival rate
W = Average time in system
```

### Example Calculation
```
Given:
- 1000 requests/second
- 100ms average response time

Required concurrent connections:
L = 1000 × 0.1 = 100 concurrent connections
```

## Resource Sizing

### Database Connections
```
connections = (requests_per_second × avg_query_time) × 1.5
```

### Memory
```
memory = (concurrent_users × memory_per_user) + base_overhead
```

### CPU Cores
```
cores = (peak_rps × cpu_time_per_request) / target_utilization
```

## Growth Planning

### Traffic Growth
- Historical growth rate
- Planned marketing/launches
- Seasonal patterns

### Data Growth
- Records per day
- Record size
- Retention policy

## Capacity Planning Document

1. Current state metrics
2. Growth assumptions
3. Resource projections (3, 6, 12 months)
4. Cost estimates
5. Scaling triggers and thresholds
