---
name: workflow-performance
description: Systematic performance analysis and optimization. Use when things are slow, need optimization, or preparing for scale.
---

# Performance Optimization Workflow

Systematic approach to finding and fixing performance issues.

## Phase 1: Baseline
**Agents:** `performance-engineer`

Measure current state:
- Response times (p50, p95, p99)
- Memory usage
- CPU utilization
- Database query times
- Bundle sizes (frontend)
- Render performance

**Output:** Baseline metrics report

## Phase 2: Bottleneck Identification
**Agents:** `performance-engineer`

Analysis:
- Profiling (CPU, memory)
- Query analysis (slow query log, EXPLAIN)
- Bundle analysis (webpack-bundle-analyzer)
- Network analysis (waterfall, latency)

**Output:** Bottleneck list with priority ranking

## Phase 3: Optimization Planning
**Agents:** `requirements-analyst`

- Prioritize by impact vs effort
- Define expected improvements
- Determine implementation order
- Set target metrics

## Phase 4: Database Optimization
**Agents:** `database-optimizer`

Tasks:
- Query optimization (rewrite slow queries)
- Index creation/optimization
- Caching strategy (Redis, memcached)
- Connection pooling

## Phase 5: Code Optimization
**Agents:** `performance-engineer`

Focus:
- Algorithm efficiency (O(n) → O(log n))
- Memory management (leaks, allocation)
- Async operations (parallelize I/O)
- Application-level caching

## Phase 6: Frontend Optimization
**Agents:** `performance-engineer`

Tasks:
- Bundle size reduction
- Code splitting
- Lazy loading
- Asset optimization (images, fonts)
- Render optimization (virtualization, memoization)

## Phase 7: Infrastructure Optimization
**Agents:** `devops-architect`

Areas:
- Scaling strategy (horizontal/vertical)
- Caching layers (CDN, reverse proxy)
- Load balancing
- Resource allocation

## Phase 8: Validation
**Agents:** `performance-engineer`

**Blocking:** Must meet targets

Targets:
- Response time: <200ms (p95)
- Memory usage: <200MB
- Bundle size: <500KB

## Phase 9: Load Testing
**Agents:** `performance-engineer`

Scenarios:
- Normal load (expected traffic)
- Peak load (2-3x normal)
- Stress test (find breaking point)

Duration: 30min per scenario

## Phase 10: Monitoring Setup
**Agents:** `devops-architect`

- Performance dashboards
- Alerting rules (degradation detection)
- Automated profiling (continuous)

## Success Criteria
- [ ] Performance targets met
- [ ] Load tests pass
- [ ] Monitoring in place
- [ ] Documentation complete

## Targets
| Metric | Target |
|--------|--------|
| Response time improvement | 50% |
| Memory reduction | 30% |
| Cost reduction | 20% |

## Anti-patterns
- ❌ Optimizing without measuring first
- ❌ Micro-optimizations before algorithmic fixes
- ❌ Optimizing code that isn't the bottleneck
- ❌ No load testing before production
