---
name: rca-distributed-systems
description: Root cause analysis techniques for modern distributed systems, microservices, and cloud infrastructure. Covers trace-based causality (OpenTelemetry, Jaeger, Tempo), service dependency graph analysis, DynaCausal-style dynamic causality-aware RCA, anomaly localization with metrics/logs/traces correlation, the Microsoft AgentRx framework for AI agent failures, chaos-engineering-as-RCA, and the 2025 industry shift toward causal-graph-based AIOps. Use when investigating a production incident in a microservice mesh, a Kubernetes cluster, a distributed database, or any system where the fault could originate in any of dozens of services and the causal chain runs through network hops, retries, timeouts, queues, and asynchronous message flows.
type: skill
category: rca
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/rca/rca-distributed-systems/SKILL.md
superseded_by: null
---
# Distributed-Systems RCA

Distributed systems fail in ways that classical RCA techniques were not designed to handle. A typical production incident involves 10–100 services, asynchronous messaging, multi-tenant resource contention, tail-latency amplification, and retries that turn a small blip into a cascade. "The root cause was a slow query" is almost always incomplete — you need to explain *why this particular slow query caused a user-visible outage when other slow queries didn't*.

This skill teaches the techniques that actually work on modern distributed production systems, drawing from the survey literature (Soldani et al. 2023, DynaCausal 2024) and the Microsoft AgentRx work on AI-agent failure diagnosis.

## What makes distributed-systems RCA hard

| Property | Consequence for RCA |
|---|---|
| **Scale** | Hundreds of services, millions of requests — cannot inspect each one |
| **Partial visibility** | Logs, metrics, traces each capture different slices; none is complete |
| **Tail amplification** | Small perturbations become large outcomes via queueing and retries |
| **Asynchronous coupling** | Cause and effect are not temporally adjacent |
| **Dependency opacity** | Service owners often don't know their downstream consumers |
| **Blast radius varies** | Same fault can affect 0.1% or 100% of users depending on state |
| **Multi-tenant noise** | Other workloads distort the signal |
| **Feedback loops** | Circuit breakers, autoscaling, and retries create nonlinear dynamics |

Classical techniques assume you can identify a failing component. In microservices, *everything is slightly degraded* and the question is which degradation caused the user-visible symptom.

## The three-pillar approach: logs, metrics, traces

Modern observability tools (OpenTelemetry-based stacks) instrument three telemetry types:

- **Metrics** — low-cardinality numeric time series (CPU, latency percentiles, error rate). Cheap to store, fast to query.
- **Logs** — high-cardinality event records with structured context. Expensive but precise.
- **Traces** — causally linked spans representing one request's journey across services. Moderate cost, irreplaceable for causality.

### Correlation key

The three pillars are only useful if they share a correlation key. OpenTelemetry's convention:

```
trace_id = 16-byte ID — one per request, propagated across services
span_id  = 8-byte ID — one per unit of work within a trace
baggage  = key-value metadata that flows with the request
```

Logs and metrics must carry `trace_id` in attributes/labels. Without this, you have three independent datasets, not a unified observability signal.

### The correlation workflow

```
1. User reports "checkout is slow."
2. Find an affected request — extract its trace_id from the frontend log.
3. Open the trace in a trace viewer — see the waterfall across services.
4. Identify the slow span — note its service, endpoint, and time window.
5. Pivot to metrics for that service — is this an outlier or broad?
6. Pivot to logs for that service filtered by trace_id — see context.
7. Pivot again: logs for the service during the time window (not just trace_id)
   — look for patterns across many affected requests.
8. Build a hypothesis. Verify against more traces.
```

The art is knowing when to pivot. Stuck in one pillar for too long is a common failure mode.

## Trace-based causality

Traces are the only telemetry type that preserves *causal* structure. A metric tells you latency went up; a trace tells you which downstream call the latency came from.

### Span attributes for RCA

A well-instrumented span includes:

- `service.name`, `service.version`
- `http.method`, `http.route`, `http.status_code`
- `db.system`, `db.statement` (sanitized)
- `rpc.system`, `rpc.service`, `rpc.method`
- `messaging.system`, `messaging.destination`
- `exception.type`, `exception.message`, `exception.stacktrace`
- Custom business attributes (user tier, tenant ID, feature flag values)

Missing or low-cardinality attributes cripple RCA. When building instrumentation, optimize for the attributes you'll need during incident investigation, not for what's easy to emit.

### Sampling

You can't trace every request in a high-throughput system. Two common approaches:

- **Head-based sampling** — decision at span creation. Simple, but misses rare errors.
- **Tail-based sampling** — decision at span completion, based on full trace content. Keeps all errors and slow traces. More expensive.

For RCA, tail-based sampling is essentially mandatory — head-based sampling discards the exact traces you need.

## Service dependency graph analysis

The service graph is the microservice equivalent of a component diagram. Modern service meshes (Istio, Linkerd) and APM tools (Datadog, Honeycomb, New Relic) build it automatically from trace data.

### Graph-based RCA techniques

**Node-level:** for each service, compute centrality measures weighted by current request rate.

**Edge-level:** for each service-to-service edge, compute error rate and latency. Rank by `edge_error_rate × edge_traffic_share × downstream_impact`.

**Graph diff:** compare the dependency graph during the incident to a recent healthy window. New edges, missing edges, or capacity ratio changes often localize the fault quickly.

### The common-cause trap

A slow service A might appear as "the cause" in every trace because it sits on every critical path, but the actual fault is an even deeper service B that only A calls. Look for the *highest-fanout* failing edge, not the most-visible failing node.

## DynaCausal — dynamic causality-aware RCA

DynaCausal (Zhang et al., 2024) introduces the idea that causal structure in microservices is itself dynamic — the same service graph can have different causal relationships under different traffic patterns, cache states, and feature-flag configurations. Traditional static graph methods miss this.

### Key insight

Learn a time-varying causal graph from trace data, not a single static graph. Use the learned graph at incident time (not a month-old cached graph) to localize the fault.

### Implementation sketch

```
1. Collect trace data in sliding windows (e.g., 5-minute windows).
2. For each window, learn a DAG over service-level metrics using
   constraint-based structure learning (PC algorithm or similar)
   seeded with the known service topology.
3. At incident time, compare the current-window DAG to the historical
   distribution of DAGs. Structural changes (new edges, edge weight
   shifts) point to the causal location.
4. Rank candidate root-cause nodes by their position in the DAG and
   their anomaly severity.
```

DynaCausal outperformed static baselines by 15–25 percentage points on F1 in the 2024 SockShop and TrainTicket benchmarks.

## AgentRx — AI agent failure diagnosis

Microsoft Research's AgentRx (2024) treats AI agents (LLM-driven tool users, workflow agents) as a new class of system where failures arise from reasoning errors, tool-use errors, and planning failures rather than infrastructure faults. The team identified a taxonomy of failure types through trajectory analysis.

### The AgentRx failure taxonomy

| Category | Description | Diagnostic signal |
|---|---|---|
| **Reasoning failure** | Model produced incorrect logical step | Reasoning chain contradiction |
| **Planning failure** | Wrong decomposition of task into subtasks | Missing required subtask |
| **Tool misuse** | Called a tool with wrong args or for wrong purpose | Tool call outside usage spec |
| **Grounding failure** | Hallucinated entities or values not in context | Fact-check mismatch |
| **Loop / stall** | Agent repeats the same action indefinitely | Self-similarity in trajectory |
| **Premature termination** | Agent stops before task is complete | Missing terminal state |
| **Context overflow** | Context window filled with noise | Token budget exhaustion |
| **Prompt-injection compromise** | Agent followed an adversarial instruction | Authority-check miss |

### How to use it for RCA

When an agent-driven system fails:

1. Capture the full execution trajectory (every LLM input, output, tool call, result).
2. Classify the failure using the taxonomy above.
3. For reasoning/planning failures, inspect the chain-of-thought (if available) for the first divergence from the intended behavior.
4. For tool misuse, check whether the tool description adequately specified the constraint.
5. For loops and stalls, identify the trigger condition and add a stall detector.

### The "stalled, biased, confused" finding

Paper 6 of our research (Jin et al., 2024) found that LLMs asked to perform cloud RCA exhibit three distinct failure patterns: *stalled* (refusing to commit to a diagnosis), *biased* (favoring a prior frequent cause regardless of evidence), and *confused* (mixing up services with similar names). All three are relevant to AI-agent postmortems.

## Chaos engineering as RCA validation

Chaos engineering (Basiri et al., 2016, Netflix) injects controlled faults to validate that a system handles them. It is usually discussed as a reliability technique, but it is also an RCA technique in reverse: rather than "figure out why this failed," it asks "can we reproduce this failure on demand?"

### Chaos-as-RCA workflow

1. Form a hypothesis from telemetry: "We believe the incident was caused by X."
2. Design a chaos experiment that induces X in a controlled blast radius (a dev environment or canary).
3. Monitor the same metrics that showed the incident.
4. If the pattern reproduces, the hypothesis is confirmed.
5. If not, either the hypothesis is wrong or there was an additional contributing factor.

Tooling: ChaosMesh, Gremlin, Chaos Monkey, LitmusChaos.

### When it's worth it

Chaos-as-RCA costs time and risk. Use it when:

- Multiple equally plausible hypotheses exist and you need to distinguish them.
- The incident is likely to recur and you want a regression test.
- You're designing remediations and need to validate they work before shipping.

## Service-level objectives (SLOs) and error budgets as RCA anchors

SLO violations provide a natural trigger and a natural closure test for RCA. If the system is above SLO, most incidents don't need deep RCA. If the system is below SLO, RCA becomes mandatory.

### SLO-anchored workflow

```
1. Identify the SLO violated during the incident.
2. Quantify the impact: how much error budget was consumed?
3. Compute the trailing 30-day error budget; if depleted, freeze new features
   until the cause is remediated.
4. After remediation, compute the projected error budget over the next 30 days
   given the fix. If the projected budget is still tight, more work is needed.
```

## Tooling inventory

| Purpose | Open source | Commercial |
|---|---|---|
| Trace collection | OpenTelemetry Collector | Datadog, Honeycomb, New Relic |
| Trace storage | Jaeger, Tempo | Lightstep, Splunk Observability |
| Metrics | Prometheus | CloudWatch, Stackdriver |
| Logs | Loki, Elasticsearch | Datadog, Splunk |
| Service mesh | Istio, Linkerd | — |
| Chaos engineering | Chaos Mesh, LitmusChaos, Chaos Monkey | Gremlin |
| Causal discovery | causal-learn, CausalNex | — |
| AIOps RCA | — | Dynatrace Davis, AppDynamics, BigPanda |

## Microservice RCA anti-patterns

### Anti-pattern 1 — dashboard-driven fishing

Team opens a dozen dashboards, scrolls for an hour, picks the most visible red thing, blames it. The highest-visibility red thing is usually the symptom, not the cause. Recovery: start from a failing trace and pivot, don't start from the most-visible metric.

### Anti-pattern 2 — retrying until it works

Retries mask transient failures, but they also hide the underlying cause and amplify load during incidents. If your incident was "we had to retry three times," your RCA must explain why the first two failed — not just that the third succeeded.

### Anti-pattern 3 — "it was the network"

Blaming the network is rarely wrong but rarely actionable. Push the investigation upstream: which service detected the network issue, and what was its configuration, timeout, and retry policy? Those are the fixable facts.

### Anti-pattern 4 — "we rolled back and it's fine now"

Rolling back is the correct first move, but stopping RCA because the symptom is gone leaves the root cause in place. The rolled-back change will be reintroduced eventually. Recovery: the RCA isn't done until you know what to change before re-introducing the change.

### Anti-pattern 5 — missing the cascading-failure analysis

In a cascade, the first service to fail is rarely the most interesting — the *last* service to fail is the one whose resilience mechanisms were inadequate. Analyze each step of the cascade, not just the trigger.

## Checklist before closing a distributed-systems RCA

- [ ] Request-level causal chain is reconstructed using traces, not just metric correlations.
- [ ] The role of retries, timeouts, and circuit breakers is explicitly addressed.
- [ ] Blast radius is quantified (users, tenants, regions affected).
- [ ] The error budget impact is computed and communicated.
- [ ] Remediations include both the proximate fix and a latent-condition fix (e.g., a missing circuit breaker).
- [ ] A chaos experiment reproduces the failure, or the reason it can't be reproduced is documented.
- [ ] The dependency graph is updated if the incident revealed an unknown edge.
- [ ] The incident feeds into the runbook / playbook for the affected service.

## References

- Soldani, J., Forti, S., & Brogi, A. (2023). A comprehensive survey on root cause analysis in (micro)services. *ACM Computing Surveys*.
- Zhang, W., Wang, H., et al. (2024). DynaCausal: Dynamic causality-aware root cause analysis for distributed microservices.
- Microsoft Research (2024). AgentRx: Diagnosing AI agent failures from execution trajectories.
- Jin, P., et al. (2024). Why do AI agents systematically fail at cloud root cause analysis?
- Basiri, A., Behnam, N., de Rooij, R., Hochstein, L., Kosewski, L., Reynolds, J., & Rosenthal, C. (2016). Chaos engineering. *IEEE Software*, 33(3), 35–41.
- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (Eds.). (2016). *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly.
- Beyer, B., Murphy, N. R., Rensin, D. K., Kawahara, K., & Thorne, S. (Eds.). (2018). *The Site Reliability Workbook*. O'Reilly.
- Majors, C., Fong-Jones, L., & Miranda, G. (2022). *Observability Engineering*. O'Reilly.
- OpenTelemetry Authors. *OpenTelemetry Specification*. https://opentelemetry.io/docs/specs/
