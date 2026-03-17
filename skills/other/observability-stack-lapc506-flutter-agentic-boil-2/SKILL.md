# 📊 Skill: Observability Stack

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-observability-stack` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `observability`, `monitoring`, `metrics`, `tracing`, `prometheus`, `grafana`, `jaeger`, `opentelemetry`, `rust` |
| **Referencia** | [Google SRE Book](https://sre.google/sre-book/table-of-contents/), [OpenTelemetry](https://opentelemetry.io/) |

## 🔑 Keywords para Invocación

- `observability`
- `monitoring`
- `metrics`
- `tracing`
- `prometheus`
- `grafana`
- `jaeger`
- `opentelemetry`
- `distributed-tracing`
- `rust`
- `@skill:observability`

### Ejemplos de Prompts

```
Implementa observability stack con Prometheus, Grafana y Jaeger
```

```
Setup OpenTelemetry para distributed tracing
```

```
Configura métricas y alertas con Prometheus
```

```
@skill:observability - Stack completo de observabilidad
```

```
Implementa observability en Rust con OpenTelemetry y Prometheus
```

## 📖 Descripción

Observability es la capacidad de entender el estado interno de un sistema basándose en sus outputs externos. Este skill cubre la implementación de un stack completo de observabilidad con métricas (Prometheus), visualización (Grafana), distributed tracing (Jaeger/Zipkin), y logging estructurado.

### ✅ Cuándo Usar Este Skill

- Sistemas distribuidos complejos
- Microservicios architecture
- Production environments críticos
- Debugging issues en producción
- Performance optimization
- Capacity planning
- SLA/SLO compliance
- Incident response y post-mortems

### ❌ Cuándo NO Usar Este Skill

- Aplicaciones muy simples (single server)
- Prototipos/MVPs sin usuarios
- Sistemas legacy sin capacidad de instrumentación

## 🏗️ Arquitectura del Stack

```
┌──────────────────────────────────────────────────────────┐
│                     Application Layer                    │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│   │ Service  │  │ Service  │  │ Service  │               │
│   │    A     │  │    B     │  │    C     │               │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│        │             │             │                     │
│        └─────────────┼─────────────┘                     │
│                      │                                   │
│               ┌──────▼───────┐                           │
│               │ OpenTelemetry│                           │
│               │  Collector   │                           │
│               └──────┬───────┘                           │
└──────────────────────┼───────────────────────────────────┘
                       │
         ┌─────────────┼────────────┐
         │             │            │
   ┌─────▼─────┐  ┌────▼───┐  ┌─────▼────┐
   │ Prometheus│  │ Jaeger │  │   Loki   │
   │ (Metrics) │  │(Traces)│  │  (Logs)  │
   └─────┬─────┘  └────────┘  └──────────┘
         │
   ┌─────▼─────┐
   │  Grafana  │
   │(Dashboards│
   │  & Alerts)│
   └───────────┘
```

## 💻 Implementación

### 1. Prometheus - Métricas

#### 1.1 Configuración Básica

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

rule_files:
  - 'alerts/*.yml'

scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Application metrics
  - job_name: 'app-services'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - default
            - production
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

  # Node Exporter for infrastructure metrics
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  # cAdvisor for container metrics
  - job_name: 'cadvisor'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: replace
        regex: (.+)
        replacement: $1:4194
        target_label: __address__
```

#### 1.2 Alert Rules

```yaml
# prometheus/alerts/high-level.yml
groups:
  - name: high_level
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service, instance)
          /
          sum(rate(http_requests_total[5m])) by (service, instance)
          > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate in {{ $labels.service }}"
          description: "Error rate is above 5% for 5 minutes"

      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency in {{ $labels.service }}"
          description: "99th percentile latency exceeds 1s"

      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          (container_memory_usage_bytes{pod=~".+"} / container_spec_memory_limit_bytes) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage in {{ $labels.pod }}"
          description: "Memory usage above 90%"

      # Service down
      - alert: ServiceDown
        expr: |
          up{job=~"app-.*"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Service has been down for more than 1 minute"
```

#### 1.3 Recording Rules

```yaml
# prometheus/rules/recording.yml
groups:
  - name: recording
    interval: 30s
    rules:
      # Service-level error rate
      - record: service:error_rate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)

      # Service-level request rate
      - record: service:request_rate
        expr: sum(rate(http_requests_total[5m])) by (service)

      # Service-level latency
      - record: service:latency:p99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          )

      # SLO compliance (99.9% availability)
      - record: service:slo_availability
        expr: |
          1 - (service:error_rate > bool 0.001)
```

### 2. Grafana - Visualización

#### 2.1 Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Service Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "service:error_rate * 100",
            "legendFormat": "{{service}}"
          }
        ],
        "type": "graph",
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [5],
                "type": "gt"
              },
              "operator": {
                "type": "and"
              },
              "query": {
                "params": ["A", "5m", "now"]
              },
              "reducer": {
                "params": [],
                "type": "last"
              },
              "type": "query"
            }
          ],
          "executionErrorState": "alerting",
          "for": "5m",
          "frequency": "10s",
          "handler": 1,
          "name": "High Error Rate Alert",
          "noDataState": "no_data",
          "notifications": ["slack-alerts"]
        }
      },
      {
        "title": "Latency (p99)",
        "targets": [
          {
            "expr": "service:latency:p99",
            "legendFormat": "{{service}}"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

#### 2.2 Data Source Configuration

```yaml
# grafana/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: "15s"
      httpMethod: POST
      exemplarTraceIdDestinations:
        - name: trace_id
          datasourceUid: jaeger
          urlDisplayLabel: "View Trace"
    editable: true

  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686
    jsonData:
      tracesToLogs:
        datasourceUid: loki
        tags: ['job', 'instance', 'pod', 'namespace']
        mappedTags: [
          { key: 'service.name', value: 'service' },
          { key: 'service.namespace', value: 'namespace' }
        ]
```

### 3. OpenTelemetry - Distributed Tracing

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **Node.js Instrumentation:** [`scripts/nodejs/instrumentation.js`](scripts/nodejs/instrumentation.js) - Setup de OpenTelemetry para Node.js
> - **Node.js Custom Spans:** [`scripts/nodejs/userService.js`](scripts/nodejs/userService.js) - Ejemplo de custom spans
> - **Rust Instrumentation:** [`scripts/rust/src/telemetry.rs`](scripts/rust/src/telemetry.rs) - Setup de OpenTelemetry para Rust
> - **Rust Custom Spans:** [`scripts/rust/src/services/user_service.rs`](scripts/rust/src/services/user_service.rs) - Ejemplo de custom spans en Rust
> 
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

#### 3.1 OpenTelemetry Collector Configuration

```yaml
# otel-collector/config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

  jaeger:
    protocols:
      grpc:
        endpoint: 0.0.0.0:14250
      thrift_http:
        endpoint: 0.0.0.0:14268

  prometheus:
    config:
      scrape_configs:
        - job_name: 'otel-collector'
          scrape_interval: 10s
          static_configs:
            - targets: ['0.0.0.0:8888']

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  memory_limiter:
    limit_mib: 512
    check_interval: 1s

  resource:
    attributes:
      - key: service.name
        value: "my-service"
        action: upsert
      - key: deployment.environment
        from_attribute: env
        action: insert

  span:
    - name: filter_sensitive_data
      from_attributes:
        - key: http.url
          pattern: '.*(password|token|secret).*'
          action: delete

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

  prometheus:
    endpoint: "0.0.0.0:8889"
    const_labels:
      label1: value1

  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp, jaeger]
      processors: [memory_limiter, resource, span, batch]
      exporters: [otlp/jaeger, logging]

    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, resource, batch]
      exporters: [prometheus, logging]
```

#### 3.2 Application Instrumentation (Node.js)

**Script ejecutable:** [`scripts/nodejs/instrumentation.js`](scripts/nodejs/instrumentation.js)

Instrumentación OpenTelemetry para aplicaciones Node.js con auto-instrumentation.

**Cuándo ejecutar:**
- Inicio de aplicación Node.js
- Setup de distributed tracing
- Integración con Jaeger/OTLP

**Uso:**
```bash
cd scripts/nodejs
npm install

# En tu aplicación, importa al inicio:
require('./instrumentation');

# O con variables de entorno:
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces node app.js
```

**Características:**
- ✅ Auto-instrumentation (HTTP, Express, PostgreSQL, Redis)
- ✅ OTLP exporter
- ✅ Resource attributes configurables
- ✅ Graceful shutdown

#### 3.3 Custom Spans (Node.js)

**Script ejecutable:** [`scripts/nodejs/userService.js`](scripts/nodejs/userService.js)

Ejemplo de servicio con custom spans para tracing personalizado.

**Uso:**
```javascript
const { getUserById } = require('./userService');
const user = await getUserById('123');
```

#### 3.4 Application Instrumentation (Rust)

**Script ejecutable:** [`scripts/rust/src/telemetry.rs`](scripts/rust/src/telemetry.rs)

Setup de OpenTelemetry para aplicaciones Rust con tracing.

**Cuándo ejecutar:**
- Inicio de aplicación Rust
- Setup de distributed tracing
- Integración con Jaeger/OTLP

**Uso:**
```bash
cd scripts/rust
cargo build --release

# Ejecutar
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces ./target/release/observability-rust

# O usar como librería en tu proyecto
```

**Características:**
- ✅ OpenTelemetry tracing
- ✅ OTLP exporter
- ✅ Structured logging con tracing-subscriber
- ✅ Resource attributes configurables

#### 3.5 Custom Spans (Rust)

**Script ejecutable:** [`scripts/rust/src/services/user_service.rs`](scripts/rust/src/services/user_service.rs)

Ejemplo de servicio Rust con custom spans y attributes.

**Características:**
- ✅ Custom spans con attributes
- ✅ Event tracking
- ✅ Error recording
- ✅ Status codes

#### 3.6 Prometheus Metrics (Rust)

```rust
// Cargo.toml
[dependencies]
prometheus = "0.13"
actix-web-prom = "0.6"  # Si usas Actix Web
axum-prometheus = "0.3"  # Si usas Axum
```

```rust
// src/metrics.rs
use prometheus::{Counter, Histogram, Registry, Encoder, TextEncoder};
use std::sync::Arc;
use lazy_static::lazy_static;

lazy_static! {
    pub static ref HTTP_REQUESTS_TOTAL: Counter = Counter::with_opts(
        prometheus::Opts::new(
            "http_requests_total",
            "Total number of HTTP requests"
        )
        .const_label("service", "my-service")
    ).unwrap();

    pub static ref HTTP_REQUEST_DURATION: Histogram = Histogram::with_opts(
        prometheus::HistogramOpts::new(
            "http_request_duration_seconds",
            "HTTP request duration in seconds"
        )
        .buckets(vec![0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0])
        .const_label("service", "my-service")
    ).unwrap();

    pub static ref REGISTRY: Registry = Registry::new();
}

pub fn init_metrics() -> Result<(), Box<dyn std::error::Error>> {
    REGISTRY.register(Box::new(HTTP_REQUESTS_TOTAL.clone()))?;
    REGISTRY.register(Box::new(HTTP_REQUEST_DURATION.clone()))?;
    Ok(())
}

pub fn gather_metrics() -> String {
    let encoder = TextEncoder::new();
    let metric_families = REGISTRY.gather();
    let mut buffer = Vec::new();
    encoder.encode(&metric_families, &mut buffer).unwrap();
    String::from_utf8(buffer).unwrap()
}
```

```rust
// src/main.rs con Actix Web
use actix_web::{web, App, HttpServer, Result, middleware};
use actix_web_prom::PrometheusMetricsBuilder;
use crate::metrics::init_metrics;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    init_metrics().unwrap();

    let prometheus = PrometheusMetricsBuilder::new("api")
        .endpoint("/metrics")
        .build()
        .unwrap();

    HttpServer::new(move || {
        App::new()
            .wrap(prometheus.clone())
            .wrap(middleware::Logger::default())
            .route("/health", web::get().to(health))
            .route("/api/users", web::get().to(get_users))
    })
    .bind("0.0.0.0:8080")?
    .run()
    .await
}

async fn health() -> Result<&'static str> {
    Ok("OK")
}

async fn get_users() -> Result<web::Json<Vec<User>>> {
    // Incrementar contador
    metrics::HTTP_REQUESTS_TOTAL.inc();
    
    // Medir duración
    let timer = metrics::HTTP_REQUEST_DURATION.start_timer();
    let users = fetch_users().await?;
    timer.observe_duration();
    
    Ok(web::Json(users))
}
```

#### 3.7 Structured Logging (Rust)

```rust
// Cargo.toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["json", "env-filter", "fmt"] }
tracing-opentelemetry = "0.21"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```rust
// src/logging.rs
use tracing_subscriber::layer::SubscriberExt;
use tracing_subscriber::util::SubscriberInitExt;
use tracing_subscriber::{EnvFilter, Registry};
use tracing_subscriber::fmt::format::JsonFields;
use tracing_subscriber::fmt::time::ChronoUtc;
use std::io;

pub fn init_logging() {
    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    let subscriber = Registry::default()
        .with(env_filter)
        .with(
            tracing_subscriber::fmt::layer()
                .json()
                .with_writer(io::stdout)
                .with_timer(ChronoUtc::rfc_3339())
                .with_target(true)
                .with_current_span(false)
                .with_span_list(false)
                .with_file(false)
                .with_line_number(false)
        );

    subscriber.init();
}
```

```rust
// src/services/user_service.rs
use tracing::{info, warn, error, instrument, Span};
use serde_json::json;

#[instrument(skip(self), fields(
    user_id = %user_id,
    trace_id = tracing::field::Empty,
    span_id = tracing::field::Empty
))]
pub async fn create_user(&self, user_id: String, user_data: UserData) -> Result<User, ServiceError> {
    // Obtener trace_id y span_id del contexto actual
    let span = Span::current();
    let trace_id = span
        .context()
        .span()
        .span_context()
        .trace_id()
        .to_string();
    let span_id = span
        .context()
        .span()
        .span_context()
        .span_id()
        .to_string();

    span.record("trace_id", &trace_id);
    span.record("span_id", &span_id);

    info!(
        user_id = %user_id,
        trace_id = %trace_id,
        span_id = %span_id,
        http_method = "POST",
        http_path = "/api/users",
        message = "Creating user",
        "Creating new user"
    );

    match self.save_user_to_db(&user_id, &user_data).await {
        Ok(user) => {
            info!(
                user_id = %user_id,
                trace_id = %trace_id,
                http_status = 201,
                duration_ms = 45,
                environment = "production",
                message = "User created successfully",
                "User created successfully"
            );
            Ok(user)
        }
        Err(e) => {
            error!(
                user_id = %user_id,
                trace_id = %trace_id,
                error = %e,
                http_status = 500,
                message = "Failed to create user",
                "Failed to create user: {}", e
            );
            Err(e)
        }
    }
}
```

```rust
// Ejemplo de log estructurado JSON output
// {
//   "timestamp": "2024-01-15T10:30:00.123Z",
//   "level": "info",
//   "fields": {
//     "user_id": "12345",
//     "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
//     "span_id": "00f067aa0ba902b7",
//     "http_method": "POST",
//     "http_path": "/api/users",
//     "http_status": 201,
//     "duration_ms": 45,
//     "environment": "production",
//     "message": "User created successfully"
//   },
//   "target": "my_service::services::user_service",
//   "span": {
//     "name": "create_user"
//   }
// }
```

### 4. Logging con Structured Logs

#### 4.1 Log Format (JSON)

```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "info",
  "service": "user-service",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "message": "User created successfully",
  "user_id": "12345",
  "http_method": "POST",
  "http_path": "/api/users",
  "http_status": 201,
  "duration_ms": 45,
  "environment": "production"
}
```

#### 4.2 Loki Configuration

```yaml
# loki/loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    address: 127.0.0.1
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
    final_sleep: 0s
  chunk_idle_period: 1h
  max_chunk_age: 1h
  chunk_target_size: 1048576
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/boltdb-shipper-active
    cache_location: /loki/boltdb-shipper-cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  ingestion_rate_mb: 16
  ingestion_burst_size_mb: 32

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: true
  retention_period: 720h

compactor:
  working_directory: /loki/boltdb-shipper-compactor
  shared_store: filesystem
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150
```

#### 4.3 Promtail Configuration

```yaml
# promtail/promtail-config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - docker: {}
      - json:
          expressions:
            output: log
            stream: stream
            attrs:
      - json:
          expressions:
            tag:
          source: attrs
      - regex:
          expression: (?P<container_name>(?:[^|]*))\|
          source: tag
      - timestamp:
          format: RFC3339Nano
          source: time
      - labels:
          stream:
          container_name:
      - output:
          source: output

  - job_name: application-logs
    static_configs:
      - targets:
          - localhost
        labels:
          job: application
          __path__: /var/log/app/*.log
    pipeline_stages:
      - json:
          expressions:
            timestamp: timestamp
            level: level
            service: service
            message: message
            trace_id: trace_id
      - labels:
          level:
          service:
      - timestamp:
          source: timestamp
          format: RFC3339
```

### 5. Kubernetes Deployment

#### 5.1 Prometheus Deployment

```yaml
# k8s/prometheus-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:v2.45.0
        args:
          - '--config.file=/etc/prometheus/prometheus.yml'
          - '--storage.tsdb.path=/prometheus'
          - '--storage.tsdb.retention.time=30d'
          - '--web.console.libraries=/usr/share/prometheus/console_libraries'
          - '--web.console.templates=/usr/share/prometheus/consoles'
        ports:
        - containerPort: 9090
          name: web
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
        - name: storage
          mountPath: /prometheus
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
      volumes:
      - name: config
        configMap:
          name: prometheus-config
      - name: storage
        persistentVolumeClaim:
          claimName: prometheus-storage
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: monitoring
spec:
  selector:
    app: prometheus
  ports:
  - port: 9090
    targetPort: 9090
    name: web
```

#### 5.2 ServiceMonitor for Prometheus Operator

```yaml
# k8s/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-services
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
    relabelings:
    - sourceLabels: [__meta_kubernetes_pod_name]
      targetLabel: pod
    - sourceLabels: [__meta_kubernetes_namespace]
      targetLabel: namespace
```

## 🎯 Mejores Prácticas

### 1. Métricas

✅ **DO:**
- Usa métricas de tasa (rate), no absolutos
- Implementa cardinalidad apropiada
- Usa histogramas para latencias
- Define métricas de negocio, no solo técnicas

❌ **DON'T:**
- Exponer métricas con alta cardinalidad (user IDs en labels)
- Crear métricas por cada request
- Usar gauges para cosas que son counters

### 2. Traces

✅ **DO:**
- Mantén spans cortos y significativos
- Incluye contexto de negocio en spans
- Usa sampling inteligente (100% para errores, 1% para success)
- Correlaciona traces con logs y métricas

❌ **DON'T:**
- Crear spans innecesarios
- Incluir datos sensibles en spans
- Hacer sampling 100% en producción (costo)

### 3. Logs

✅ **DO:**
- Usa structured logging (JSON)
- Incluye trace_id para correlación
- Niveles apropiados (DEBUG, INFO, WARN, ERROR)
- Limita verbosidad en producción

❌ **DON'T:**
- Logear datos sensibles (passwords, tokens)
- Usar diferentes formatos de log
- Logear en loops de alta frecuencia

## 🚨 Troubleshooting

### Prometheus High Cardinality

```promql
# Identificar métricas con alta cardinalidad
topk(10, count by (__name__)({__name__=~".+"}))
```

Solución: Reducir labels o usar recording rules.

### Jaeger Trace Sampling

```yaml
# Configurar sampling en OpenTelemetry
sampling:
  probability: 0.1  # 10% sampling
  # O usar sampling basado en condiciones
```

### Grafana Dashboards Lentos

- Usa recording rules para pre-calcular queries complejas
- Limita el rango de tiempo de las queries
- Usa variables para filtrar datos

## 📚 Recursos Adicionales

- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,500+

