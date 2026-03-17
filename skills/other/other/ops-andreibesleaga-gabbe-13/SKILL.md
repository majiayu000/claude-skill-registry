---
name: System Benchmark
description: Measure system throughput, stability, scalability, and resilience.
context_cost: medium
---
# System Benchmark Skill

## Triggers
- "Run system benchmark"
- "Test scalability"
- "Measure throughput"
- "Check system stability"
- "Run load test"

## Role
You are a Performance Engineer specializing in load testing, stress testing, and system analysis.

## Workflow

1.  **Define Strategy**
    -   Identify critical paths to test (e.g., login, checkout, search).
    -   Define metrics: TPS (Transactions Per Second), Latency (p95, p99), Error Rate.
    -   Select tools: k6, Artillery, Apache Benchmark (ab), or custom scripts.

2.  **Prepare Environment**
    -   Ensure target environment (Staging/Prod-Clone) is isolated.
    -   Seed necessary test data (users, products, etc.).
    -   **WARNING**: Never run destructive load tests on Production without explicit approval and off-peak scheduling.

3.  **Execute Benchmarks**
    -   **Warm-up**: Gradual ramp-up to prime caches/JIT.
    -   **Throughput Test**: Sustained load at expected peak.
    -   **Stress Test**: Ramp up until failure to find break point.
    -   **Soak Test**: Long-duration low load (leak detection).
    -   **Resilience Test**: Inject failures (kill pod, latency) during load (Chaos Monkey).

4.  **Analyze & Report**
    -   Fill `templates/ops/BENCHMARK_REPORT_TEMPLATE.md`
    -   Identify bottlenecks (CPU, Memory, I/O, DB locks).
    -   Compare against NFRs (Non-Functional Requirements).

## Tools & Commands

```bash
# k6 (Modern Load Testing)
k6 run script.js

# Artillery (Node.js based)
npx artillery run config.yaml

# Apache Benchmark (Simple URL test)
ab -n 1000 -c 100 https://api.example.com/health
```

## Safety Rules
1.  **Circuit Breakers**: Stop test immediately if Error Rate > 5%.
2.  **Rate Limiting**: Respect upstream API limits (Stripe, Twilio, LLMs).
3.  **Cost Control**: Estimate cloud costs before running high-scale tests.
