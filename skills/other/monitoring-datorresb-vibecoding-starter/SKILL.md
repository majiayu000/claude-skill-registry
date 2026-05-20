---
name: monitoring
description: Comprehensive observability strategy including metrics, logs, traces, and alerting. Use when setting up new applications, debugging production issues, performance optimization, SLA/SLO definition, incident response, or establishing monitoring infrastructure.
---

# Monitoring Skill

## Core Principle

**Measure what matters, alert on what's actionable.**

You can't improve what you don't measure. Observability is not about collecting all possible data—it's about collecting the right data to understand system health, debug issues quickly, and make informed decisions. Alert on symptoms that require action, not on every fluctuation.

---

## When to Use

Use this skill when:
- Setting up monitoring for new applications or services
- Debugging production issues or incidents
- Performing performance optimization
- Defining SLAs, SLOs, and error budgets
- Responding to incidents
- Establishing alerting strategies
- Implementing distributed tracing
- Creating dashboards for system observability
- Analyzing system performance and reliability
- Planning capacity and scaling decisions

---

## The Three Pillars of Observability

Modern observability is built on three complementary pillars:

```
┌─────────────────────────────────────────────┐
│           OBSERVABILITY                      │
├─────────────┬──────────────┬────────────────┤
│   METRICS   │     LOGS     │    TRACES      │
├─────────────┼──────────────┼────────────────┤
│ What is     │ What         │ Where is       │
│ happening?  │ happened?    │ the problem?   │
│             │              │                │
│ Time-series │ Event        │ Request flow   │
│ data        │ records      │ through system │
│             │              │                │
│ Aggregated  │ Detailed     │ Distributed    │
│ numbers     │ context      │ context        │
└─────────────┴──────────────┴────────────────┘
```

### 1. Metrics: What is Happening?

**Time-series numerical data aggregated over time.**

**Examples:**
- Request rate (requests per second)
- Error rate (percentage)
- Response time (milliseconds, percentiles)
- CPU usage (percentage)
- Memory usage (bytes)
- Queue depth (items)

**Characteristics:**
- Cheap to collect and store
- Efficient for alerting
- Good for dashboards and trends
- Limited context (numbers only)

**When to Use:**
- Real-time monitoring
- Alerting on thresholds
- Capacity planning
- Performance trending

---

### 2. Logs: What Happened?

**Timestamped event records with contextual information.**

**Examples:**
```json
{
  "timestamp": "2025-01-10T14:32:15Z",
  "level": "ERROR",
  "service": "payment-service",
  "trace_id": "abc123",
  "user_id": "user_456",
  "message": "Payment processing failed",
  "error": "Gateway timeout",
  "amount": 99.99,
  "currency": "USD"
}
```

**Characteristics:**
- Rich contextual information
- Event-by-event detail
- Expensive to store at scale
- Powerful for debugging

**When to Use:**
- Debugging specific issues
- Audit trails
- Understanding event sequences
- Post-mortem analysis

---

### 3. Traces: Where is the Problem?

**Request flow tracking across distributed systems.**

```
User Request → API Gateway → Auth Service → User Service → Database
                    ↓
              Payment Service → Payment Gateway
                    ↓
              Email Service → Email Provider
```

**Example Trace:**
```
Trace ID: abc123
Total Duration: 450ms

Span 1: API Gateway        [0-450ms]   ████████████████████
Span 2: Auth Service       [10-30ms]   ██
Span 3: User Service       [35-100ms]  ██████
Span 4: Database Query     [40-95ms]   █████
Span 5: Payment Service    [105-400ms] ████████████████  ← SLOW!
Span 6: Payment Gateway    [120-390ms] ███████████████
Span 7: Email Service      [405-440ms] ███
```

**Characteristics:**
- Shows request path through services
- Identifies bottlenecks visually
- Requires instrumentation
- Can be expensive at scale

**When to Use:**
- Debugging latency issues
- Understanding microservice interactions
- Optimizing distributed systems
- Identifying performance bottlenecks

---

## The Four Golden Signals

**Google's SRE framework for monitoring any system.**

### 1. Latency

**How long does it take to service a request?**

**Key Metrics:**
- Median response time (p50)
- 95th percentile (p95)
- 99th percentile (p99)
- 99.9th percentile (p999)

**Why Percentiles Matter:**
```
Average:  100ms  ← Hides outliers!
p50:       80ms  ← Half of requests
p95:      200ms  ← 95% of requests
p99:      500ms  ← 99% of requests (worst experience)
p999:    2000ms  ← Worst 0.1% (but affects real users!)
```

**Alert Example:**
```
IF p99_response_time > 1000ms for 5 minutes
THEN alert: "High latency affecting 1% of users"
```

---

### 2. Traffic

**How much demand is being placed on the system?**

**Key Metrics:**
- Requests per second (RPS)
- Transactions per second (TPS)
- Concurrent users
- Data throughput (bytes/sec)

**Why It Matters:**
- Understand capacity needs
- Detect traffic spikes (DDoS, viral events)
- Plan scaling decisions
- Correlate with other signals

**Alert Example:**
```
IF requests_per_second > 10000 for 10 minutes
THEN alert: "Unusual traffic spike detected"
```

---

### 3. Errors

**What is the rate of failing requests?**

**Key Metrics:**
- Error rate (percentage)
- HTTP 5xx errors
- HTTP 4xx errors (client errors)
- Exception rate
- Failed transactions

**Error Budget:**
```
SLO: 99.9% availability
Error budget per month: 0.1% = 43 minutes downtime

If error rate = 1% for 1 hour
→ Consumed 36 minutes of error budget
→ Only 7 minutes remaining this month!
```

**Alert Example:**
```
IF error_rate > 1% for 5 minutes
THEN page: "Critical: High error rate"
```

---

### 4. Saturation

**How full is the service?**

**Key Metrics:**
- CPU utilization (%)
- Memory utilization (%)
- Disk I/O usage
- Network bandwidth
- Connection pool usage
- Queue depth

**Why It Matters:**
- Predict capacity issues before they happen
- Know when to scale
- Avoid resource exhaustion

**Alert Example:**
```
IF memory_usage > 90% for 10 minutes
THEN alert: "Memory saturation warning"
```

---

## Alternative Monitoring Frameworks

### RED Method (Request-focused)

**Best for request-driven services (APIs, web services).**

- **Rate:** Requests per second
- **Errors:** Failed requests per second
- **Duration:** Request latency (distribution)

**Example Dashboard:**
```
Service: payment-api

Rate:     1,250 req/sec  ▲ 15%
Errors:   12.5 req/sec   ▲ 200% ⚠️
Duration:
  p50:    45ms
  p95:    120ms
  p99:    280ms
```

---

### USE Method (Resource-focused)

**Best for infrastructure and hardware monitoring.**

- **Utilization:** % time resource was busy
- **Saturation:** Queue length or wait time
- **Errors:** Error count

**Example:**
```
CPU:
  Utilization: 75%
  Saturation:  Load average 4.2 (4 cores)
  Errors:      0

Disk:
  Utilization: 60%
  Saturation:  I/O queue depth: 12
  Errors:      3 read errors
```

---

## Monitoring Stack Tools

### Metrics Collection and Storage

#### Prometheus (Open Source)

**Pull-based metrics collection and time-series database.**

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'myapp'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8080']
```

**Application Instrumentation (Python):**
```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Instrument code
@request_duration.time()
def handle_request(method, endpoint):
    request_count.labels(method=method, endpoint=endpoint).inc()
    # Handle request...

# Expose metrics endpoint
start_http_server(8000)  # Metrics at http://localhost:8000/metrics
```

**PromQL Queries:**
```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# Error rate (percentage)
rate(http_requests_total{status=~"5.."}[5m])
  / rate(http_requests_total[5m]) * 100

# p95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# CPU usage by pod
container_cpu_usage_seconds_total{pod=~"myapp-.*"}
```

**Benefits:**
- Powerful query language (PromQL)
- Excellent for Kubernetes
- Active ecosystem
- Free and open source

**Drawbacks:**
- Limited long-term storage (use Thanos/Cortex)
- Pull-based (need service discovery)
- Requires learning PromQL

---

#### Grafana (Open Source)

**Visualization and dashboarding for metrics.**

**Features:**
- Connects to Prometheus, InfluxDB, CloudWatch, etc.
- Beautiful, customizable dashboards
- Alerting capabilities
- Dashboard sharing and templates

**Example Dashboard JSON:**
```json
{
  "title": "Service Overview",
  "panels": [
    {
      "title": "Request Rate",
      "targets": [{
        "expr": "rate(http_requests_total[5m])"
      }],
      "type": "graph"
    },
    {
      "title": "Error Rate",
      "targets": [{
        "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100"
      }],
      "alert": {
        "conditions": [{
          "evaluator": {"type": "gt", "params": [1]},
          "query": {"params": ["A", "5m", "now"]}
        }]
      }
    }
  ]
}
```

---

#### CloudWatch (AWS)

**AWS-native metrics, logs, and alarms.**

```python
# Python: Publishing custom metrics
import boto3

cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[
        {
            'MetricName': 'RequestCount',
            'Value': 1,
            'Unit': 'Count',
            'Timestamp': datetime.utcnow(),
            'Dimensions': [
                {'Name': 'Environment', 'Value': 'production'},
                {'Name': 'Service', 'Value': 'api'}
            ]
        }
    ]
)
```

**Benefits:**
- Native AWS integration
- No infrastructure management
- Automatic metrics for AWS services

**Drawbacks:**
- AWS-specific (vendor lock-in)
- Can be expensive at scale
- Limited query capabilities

---

#### Datadog (Commercial SaaS)

**All-in-one observability platform.**

**Features:**
- Metrics, logs, traces, and APM in one platform
- 500+ integrations
- Machine learning anomaly detection
- Powerful dashboards and alerting

```python
# Python: Datadog StatsD
from datadog import initialize, statsd

initialize(api_key='YOUR_API_KEY')

# Increment counter
statsd.increment('myapp.requests', tags=['endpoint:/api/users'])

# Record timing
statsd.timing('myapp.request_duration', 250)

# Set gauge
statsd.gauge('myapp.queue_depth', 42)
```

**Benefits:**
- Comprehensive platform
- Minimal setup
- Great UX and correlation features

**Drawbacks:**
- Expensive (per-host pricing)
- Vendor lock-in
- Less control than self-hosted

---

### Logging

#### ELK Stack (Elasticsearch, Logstash, Kibana)

**Open-source log aggregation and analysis.**

```
Application → Logstash → Elasticsearch → Kibana
              (collect)  (store/index)   (visualize)
```

**Structured Logging Example:**
```python
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'service': 'myapp',
            'trace_id': getattr(record, 'trace_id', None)
        }
        return json.dumps(log_data)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.root.addHandler(handler)
```

**Logstash Configuration:**
```ruby
input {
  file {
    path => "/var/log/myapp/*.log"
    codec => "json"
  }
}

filter {
  if [level] == "ERROR" {
    mutate {
      add_tag => ["error"]
    }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "myapp-logs-%{+YYYY.MM.dd}"
  }
}
```

---

#### Loki + Promtail (Grafana Labs)

**Log aggregation designed like Prometheus (labels, not full-text indexing).**

**Benefits:**
- Lower storage costs than Elasticsearch
- Native Grafana integration
- Label-based indexing (like Prometheus)

**Promtail Configuration:**
```yaml
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: myapp
    static_configs:
      - targets:
          - localhost
        labels:
          job: myapp
          __path__: /var/log/myapp/*.log
```

**Querying Logs in Grafana:**
```logql
{job="myapp"} |= "error" | json | level="ERROR"
```

---

#### Splunk (Commercial)

**Enterprise log management platform.**

**Features:**
- Powerful search and analytics
- Machine learning for anomaly detection
- Compliance and security use cases
- Extensive integrations

**Drawbacks:**
- Very expensive
- Steep learning curve
- Resource intensive

---

### Distributed Tracing

#### Jaeger (Open Source)

**Distributed tracing system developed by Uber.**

**OpenTelemetry Instrumentation (Python):**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Setup
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# Usage
def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order_id", order_id)

        with tracer.start_as_current_span("validate_order"):
            validate(order_id)

        with tracer.start_as_current_span("charge_payment"):
            charge(order_id)

        with tracer.start_as_current_span("send_confirmation"):
            send_email(order_id)
```

---

#### OpenTelemetry (Standard)

**Vendor-neutral instrumentation standard.**

**Benefits:**
- Single instrumentation for metrics, logs, traces
- Export to any backend (Jaeger, Zipkin, Datadog, etc.)
- Language support: Python, Go, Java, JavaScript, .NET, Rust

**Auto-Instrumentation (Python):**
```bash
# Install
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

# Run with auto-instrumentation
opentelemetry-instrument \
  --traces_exporter otlp \
  --metrics_exporter otlp \
  --service_name myapp \
  python app.py
```

---

#### AWS X-Ray

**AWS-native distributed tracing.**

```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch libraries
patch_all()

# Manual instrumentation
@xray_recorder.capture('process_order')
def process_order(order_id):
    xray_recorder.current_segment().put_annotation('order_id', order_id)
    # Process order...
```

---

## Alerting Strategy

### Alert Fatigue: The Silent Killer

**Bad Alerting:**
```
3:00 AM: Disk usage 71% ⚠️
3:15 AM: Memory usage 82% ⚠️
3:30 AM: CPU spike to 90% for 10 seconds ⚠️
3:45 AM: Database connection pool 70% full ⚠️
4:00 AM: Disk usage 72% ⚠️
```

**Result:** On-call engineer ignores/silences all alerts. Real issues get missed.

**Good Alerting:**
```
3:00 AM: [CRITICAL] Error rate 15% for 10 minutes - users affected!
```

**Result:** On-call engineer immediately investigates actionable issue.

---

### Alert Severity Levels

**Use 3-4 severity levels, no more.**

#### Critical (Page On-Call)
- **User Impact:** Service down or severely degraded
- **Examples:**
  - Error rate > 5%
  - Service completely unavailable
  - Data loss occurring
- **Response:** Immediate action required (wake up engineer)

#### Warning (Notify Team Channel)
- **User Impact:** Potential future issue, no immediate user impact
- **Examples:**
  - Error rate > 1%
  - Disk usage > 85%
  - Memory usage trending toward saturation
- **Response:** Investigate during business hours

#### Info (Log Only)
- **User Impact:** None
- **Examples:**
  - Deployment completed
  - Auto-scaling triggered
  - Configuration change
- **Response:** Awareness only, no action

---

### Alert Best Practices

#### 1. Alert on Symptoms, Not Causes

❌ **Bad: Cause-based alert**
```
IF cpu_usage > 80% THEN alert
```
**Problem:** High CPU might not affect users. Not actionable.

✅ **Good: Symptom-based alert**
```
IF p99_latency > 1000ms AND error_rate > 1% THEN alert
```
**Why:** Users are actually affected. Clear action needed.

---

#### 2. Make Alerts Actionable

Every alert must answer: **"What should I do about this?"**

❌ **Bad Alert:**
```
ALERT: Database queries slow
```

✅ **Good Alert:**
```
ALERT: Database p99 query time > 5s for 10 minutes

User Impact: Checkout page timing out for 1% of users
Runbook: https://wiki.company.com/runbooks/slow-database
Dashboard: https://grafana.company.com/d/database
Recent Changes: Last deploy 2 hours ago (v1.2.3)

Immediate Actions:
1. Check slow query log
2. Check for locks: SELECT * FROM pg_locks WHERE granted=false
3. Consider rolling back deploy if started after v1.2.3 deploy
```

---

#### 3. Use Error Budgets, Not Arbitrary Thresholds

**Error Budget Concept:**
```
SLO: 99.9% availability = 99.9% successful requests
Error Budget: 0.1% of requests can fail

Monthly Error Budget:
- 0.1% of 100M requests = 100,000 failed requests allowed
- 43 minutes of downtime allowed

Alert when error budget consumption rate too high:
IF current_error_rate will exhaust error_budget in < 7 days
THEN alert: "Error budget burn rate too high"
```

---

#### 4. Avoid Alert Storms

**Use alert grouping and deduplication:**

```yaml
# Alertmanager (Prometheus)
route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

inhibit_rules:
  # Don't alert on high latency if service is down
  - source_match:
      severity: 'critical'
      alertname: 'ServiceDown'
    target_match:
      severity: 'warning'
      alertname: 'HighLatency'
    equal: ['service']
```

---

#### 5. Alert Tuning Process

```
Deploy Alert → Monitor False Positive Rate
                      ↓
            Too many false positives?
                   ↙        ↘
                 YES         NO
                  ↓           ↓
         Adjust thresholds   Keep alert
         Adjust duration
         Add conditions
                  ↓
         Re-deploy alert
                  ↓
              Monitor
```

**Target:**
- False positive rate < 5%
- Each alert should lead to action 90%+ of the time

---

## SLIs, SLOs, and SLAs

### Service Level Indicator (SLI)

**A metric that measures service quality.**

**Examples:**
- Request success rate
- Request latency (p95)
- System throughput
- Data freshness

**Good SLI:**
```
SLI = (successful requests) / (total requests)
    = 99,500 / 100,000
    = 99.5%
```

---

### Service Level Objective (SLO)

**Target value or range for an SLI.**

**Examples:**
- 99.9% of requests succeed
- 95% of requests complete in < 300ms
- 99% of data processed within 1 hour

**SLO Structure:**
```
SLO: [percentage] of [what] in [time period]

Example:
SLO: 99.9% of API requests succeed in a rolling 30-day window
```

---

### Service Level Agreement (SLA)

**Contract with users about service levels, often with consequences.**

**Example:**
```
SLA: 99.9% uptime monthly

Uptime: 99.9% - 100%  → No credit
Uptime: 99.0% - 99.9% → 10% credit
Uptime: 95.0% - 99.0% → 25% credit
Uptime: < 95.0%       → 50% credit
```

---

### Relationship

```
SLA ≥ SLO > SLI (actual)

Example:
SLA:  99.5% (contractual minimum)
SLO:  99.9% (internal target - buffer above SLA)
SLI:  99.95% (actual measurement)

Buffer = SLA - SLO = 0.4% = error budget
```

---

### Setting Good SLOs

#### Don't Aim for 100%

**100% is:**
- Impossible to achieve
- Prevents taking risks (deploys, experiments)
- Not necessary (users don't notice 99.9% vs 100%)

**Instead:**
- Set realistic SLOs based on user needs
- Use error budgets to balance reliability and velocity

---

#### Start with Current Performance

```
Step 1: Measure current SLI for 30 days
  Current: 99.7% success rate

Step 2: Set SLO slightly below current (buffer)
  SLO: 99.5%

Step 3: Monitor and adjust quarterly
  If easily meeting SLO → Consider raising
  If struggling → Investigate systemic issues
```

---

## Dashboard Design Patterns

### 1. Overview Dashboard (At-a-Glance Health)

**Purpose:** Quickly answer "Is everything OK?"

**Panels:**
- Overall health status (green/yellow/red)
- Four Golden Signals (Latency, Traffic, Errors, Saturation)
- Recent deployments timeline
- Active alerts count

**Layout:**
```
┌─────────────────────────────────────────────┐
│  System Health: GREEN ✓                     │
├──────────────┬──────────────┬───────────────┤
│  Latency     │  Traffic     │  Errors       │
│  p99: 250ms  │  1.2K req/s  │  0.05%        │
│  ████░░      │  ██████░░    │  ░░░░░░       │
├──────────────┴──────────────┴───────────────┤
│  Recent Deployments                          │
│  ──●────●──────────●─── (last 24h)          │
│                                              │
│  Active Alerts: 0                            │
└──────────────────────────────────────────────┘
```

---

### 2. Service Dashboard (Deep-Dive)

**Purpose:** Understand specific service performance.

**Panels:**
- Request rate (by endpoint)
- Error rate (by endpoint and status code)
- Latency (p50, p95, p99)
- Resource usage (CPU, memory)
- Dependency health (database, cache, external APIs)

---

### 3. Business Metrics Dashboard

**Purpose:** Connect technical metrics to business outcomes.

**Examples:**
- User signups per hour
- Successful transactions
- Revenue per minute
- Shopping cart abandonment rate
- Search conversion rate

**Why It Matters:**
Technical outages should correlate with business impact:
```
Error rate spike at 2:00 PM
   ↓
Transactions dropped 80%
   ↓
Revenue loss: $10,000/hour
   ↓
Priority: CRITICAL
```

---

### 4. Incident Response Dashboard

**Purpose:** Information needed during active incidents.

**Panels:**
- Real-time error rate
- Recent deployments
- Recent alerts
- Service dependency map
- Key logs (errors/warnings)
- On-call engineer contact

---

## Monitoring Best Practices

### 1. Instrument Early

**Add monitoring from day one, not after issues arise.**

```python
# Bad: No instrumentation
def process_payment(amount):
    return gateway.charge(amount)

# Good: Instrumented
@metrics.timer('payment_duration')
def process_payment(amount):
    with tracer.start_span('process_payment'):
        try:
            result = gateway.charge(amount)
            metrics.increment('payment_success')
            return result
        except Exception as e:
            metrics.increment('payment_failure')
            logger.error('Payment failed', extra={
                'amount': amount,
                'error': str(e),
                'trace_id': get_trace_id()
            })
            raise
```

---

### 2. Use Structured Logging

❌ **Bad: Unstructured**
```python
logger.info(f"User {user_id} purchased {item} for ${amount}")
```
**Problem:** Hard to parse, query, and alert on.

✅ **Good: Structured (JSON)**
```python
logger.info("purchase_completed", extra={
    'event': 'purchase',
    'user_id': user_id,
    'item_id': item,
    'amount': amount,
    'currency': 'USD',
    'trace_id': trace_id
})
```
**Benefit:** Easy to filter, aggregate, and build alerts.

---

### 3. Include Trace IDs Everywhere

**Connect metrics → logs → traces using trace ID.**

```python
import uuid

def handle_request():
    trace_id = str(uuid.uuid4())

    # Add to metrics
    metrics.increment('requests', tags={'trace_id': trace_id})

    # Add to logs
    logger.info('Processing request', extra={'trace_id': trace_id})

    # Add to response headers (for debugging)
    return response, {'X-Trace-ID': trace_id}
```

**Debugging Flow:**
```
1. User reports slow request
2. Find trace_id in response headers
3. Search logs: trace_id="abc123"
4. View trace in Jaeger: abc123
5. Identify slow span: database query took 5s
6. Fix query performance
```

---

### 4. Monitor Dependencies

**Your service is only as reliable as its dependencies.**

```python
# Monitor external API
@metrics.timer('external_api_duration')
def call_external_api():
    try:
        response = requests.get('https://api.external.com', timeout=5)
        metrics.increment('external_api_success')
        return response
    except requests.Timeout:
        metrics.increment('external_api_timeout')
        raise
    except requests.RequestException:
        metrics.increment('external_api_error')
        raise
```

**Dashboard:**
```
Dependencies Health:
  Database:     99.9% success ✓
  Redis Cache:  99.95% success ✓
  Payment API:  97.2% success ⚠️  ← Issue!
  Email API:    99.8% success ✓
```

---

### 5. Tag/Label Metrics

**Enable filtering and aggregation.**

```python
# Good: Tagged metrics
metrics.increment('http_requests', tags={
    'method': 'POST',
    'endpoint': '/api/users',
    'status': '200',
    'environment': 'production'
})

# Now you can query:
# - All POST requests
# - All /api/users requests
# - All 5xx errors
# - Production vs staging comparison
```

---

### 6. Avoid High-Cardinality Labels

❌ **Bad: Unique value per request**
```python
metrics.increment('requests', tags={
    'user_id': user_id  # Millions of unique values!
})
```
**Problem:** Creates millions of time series, explodes storage costs.

✅ **Good: Low cardinality**
```python
metrics.increment('requests', tags={
    'user_tier': 'premium'  # Only 3-4 unique values
})
```

---

## Monitoring Workflow

### 1. Development Phase

```
Developer writes code
        ↓
Add instrumentation (metrics, logs, traces)
        ↓
Define local monitoring (docker-compose)
        ↓
Test monitoring locally
        ↓
Commit code with instrumentation
```

---

### 2. Deployment Phase

```
Code deployed to staging
        ↓
Verify metrics appear in Prometheus/Datadog
        ↓
Create/update Grafana dashboards
        ↓
Define alerts in Alertmanager
        ↓
Test alerts (trigger conditions manually)
        ↓
Deploy to production
        ↓
Monitor dashboards during deployment
```

---

### 3. Operations Phase

```
Monitor dashboards daily
        ↓
Alert fires → Investigate
        ↓
Use logs and traces to debug
        ↓
Fix issue
        ↓
Update runbooks
        ↓
Tune alert if false positive
```

---

## Integration with Other Skills

### With Deployment
- Monitor metrics during deployment
- Rollback if error rate increases
- Dashboard shows deployment markers
- Alert on deployment failures

### With Performance Optimization
- Metrics identify bottlenecks
- Traces show slow code paths
- Before/after performance comparison
- Monitor optimization impact

### With Infrastructure
- Monitor infrastructure resources (CPU, memory, disk)
- Capacity planning based on trends
- Alert on infrastructure issues
- Auto-scaling triggered by metrics

### With CI/CD
- CI/CD pipeline emits metrics
- Alert on pipeline failures
- Performance tests validate SLOs
- Automated canary analysis

---

## Quick Reference

### Metrics to Monitor Checklist

**Application:**
- [ ] Request rate (requests/sec)
- [ ] Error rate (%)
- [ ] Response time (p50, p95, p99)
- [ ] Active connections/requests

**Infrastructure:**
- [ ] CPU usage (%)
- [ ] Memory usage (%)
- [ ] Disk usage (%)
- [ ] Network I/O

**Dependencies:**
- [ ] Database query time
- [ ] Cache hit rate
- [ ] External API response time
- [ ] Queue depth

**Business:**
- [ ] User signups
- [ ] Successful transactions
- [ ] Revenue metrics
- [ ] User engagement

---

### Alerting Checklist

- [ ] Alert has clear severity (critical/warning/info)
- [ ] Alert includes user impact description
- [ ] Runbook link included
- [ ] Dashboard link included
- [ ] Alert is actionable (not just informational)
- [ ] Alert tested (triggered manually)
- [ ] On-call knows how to respond
- [ ] False positive rate < 5%

---

### Logging Best Practices

- [ ] Use structured logging (JSON)
- [ ] Include trace ID in all logs
- [ ] Use appropriate log levels (ERROR, WARN, INFO, DEBUG)
- [ ] Don't log sensitive data (passwords, credit cards)
- [ ] Include context (user_id, request_id, etc.)
- [ ] Centralized log aggregation configured
- [ ] Logs retained for compliance period (e.g., 90 days)

---

### SLO Template

```yaml
Service: [service-name]
SLO: [percentage]% of [what] in [time period]

Example:
Service: payment-api
SLO: 99.9% of API requests succeed in a rolling 30-day window

Measurement:
  SLI: (successful_requests / total_requests) * 100
  Window: 30 days rolling
  Target: 99.9%

Error Budget:
  Allowed failures: 0.1% = ~43 minutes downtime/month
  Current status: 99.95% (well within budget)

Alerts:
  - Error budget burn rate > 5x: CRITICAL (page on-call)
  - Error budget < 20% remaining: WARNING (notify team)
```

---

### Common Monitoring Commands

```bash
# Prometheus
# Query current request rate
curl 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])'

# Grafana
# Create API key
curl -X POST http://admin:admin@localhost:3000/api/auth/keys \
  -H "Content-Type: application/json" \
  -d '{"name":"monitoring","role":"Viewer"}'

# Jaeger
# Query traces by service
curl 'http://localhost:16686/api/traces?service=myapp&limit=10'

# CloudWatch
# Get metric statistics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --start-time 2025-01-10T00:00:00Z \
  --end-time 2025-01-10T23:59:59Z \
  --period 3600 \
  --statistics Average
```

---

**Remember:** Good monitoring is invisible when everything works, but invaluable when things break. Instrument early, alert sparingly, and always connect metrics to user impact. Measure what matters, not just what's easy to measure.
