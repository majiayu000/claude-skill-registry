---
name: logging-log-aggregation
description: '| ID | sre-logging-log-aggregation |'
---

# 📝 Skill: Logging & Log Aggregation

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-logging-log-aggregation` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `logging`, `log-aggregation`, `loki`, `elasticsearch`, `fluentd`, `structured-logs`, `centralized-logging` |
| **Referencia** | [Loki Documentation](https://grafana.com/docs/loki/latest/) |

## 🔑 Keywords para Invocación

- `logging`
- `log-aggregation`
- `loki`
- `elasticsearch`
- `fluentd`
- `structured-logs`
- `centralized-logging`
- `@skill:logging`

### Ejemplos de Prompts

```
Implementa centralized logging con Loki y Promtail
```

```
Configura structured logging y log aggregation
```

```
Setup Elasticsearch y Fluentd para log management
```

```
@skill:logging - Sistema completo de logging
```

## 📖 Descripción

Logging efectivo y agregación centralizada son fundamentales para debugging, monitoring y compliance. Este skill cubre structured logging, log aggregation con Loki/Elasticsearch, log parsing, retention policies, y log analysis.

### ✅ Cuándo Usar Este Skill

- Sistemas distribuidos
- Debugging en producción
- Compliance requirements
- Security auditing
- Performance analysis
- Troubleshooting

### ❌ Cuándo NO Usar Este Skill

- Aplicaciones muy simples
- Desarrollo local solo
- Sin requisitos de auditoría

## 🏗️ Logging Architecture

```
┌──────────────┐
│ Applications │
│  ┌────────┐  │
│  │ Service│  │
│  │   A    │  │
│  └───┬────┘  │
│  ┌───▼────┐  │
│  │ Service│  │
│  │   B    │  │
│  └───┬────┘  │
└──────┼───────┘
       │
  ┌────▼─────┐
  │ Loggers  │
  │(stdout)  │
  └────┬─────┘
       │
  ┌────▼─────┐
  │Promtail  │
  │(Agent)   │
  └────┬─────┘
       │
  ┌────▼─────┐
  │   Loki   │
  │(Storage) │
  └────┬─────┘
       │
  ┌────▼─────┐
  │ Grafana  │
  │(Query)   │
  └──────────┘
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **Node.js Logger:** [`scripts/nodejs/structured-logger.js`](scripts/nodejs/structured-logger.js) - Structured logging con Winston
> - **Python Logger:** [`scripts/python/structured_logger.py`](scripts/python/structured_logger.py) - Structured logging con JSON
> - **Log Archiver:** [`scripts/python/log_archiver.py`](scripts/python/log_archiver.py) - Archivado y retención de logs con S3
>
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

### 1. Structured Logging

#### 1.1 JSON Log Format (Node.js)

**Script ejecutable:** [`scripts/nodejs/structured-logger.js`](scripts/nodejs/structured-logger.js)

Structured logger para Node.js usando Winston con formato JSON para centralized logging.

**Cuándo ejecutar:**
- Integración en aplicaciones Node.js
- Logging estructurado para sistemas distribuidos
- Integración con Loki/Elasticsearch

**Uso:**
```bash
cd scripts/nodejs
npm install

# Test
node structured-logger.js

# En tu aplicación
const { logger } = require('./structured-logger');
logger.info('User created', { userId: '123', email: 'user@example.com' });
```

**Características:**
- ✅ Formato JSON estructurado
- ✅ Timestamps automáticos
- ✅ Context injection (service, environment, version)
- ✅ File handlers (error.log, combined.log)
- ✅ Exception y rejection handlers
- ✅ Convenience functions para eventos comunes

#### 1.2 Python Structured Logging

**Script ejecutable:** [`scripts/python/structured_logger.py`](scripts/python/structured_logger.py)

Structured logger para Python con formato JSON y soporte para context injection.

**Cuándo ejecutar:**
- Integración en aplicaciones Python
- Logging estructurado para sistemas distribuidos
- Integración con Loki/Elasticsearch

**Uso:**
```bash
cd scripts/python

# Test
python structured_logger.py

# En tu aplicación
from structured_logger import get_logger

logger = get_logger(service='my-service')
logger.info('User created', extra={
    'user_id': '12345',
    'trace_id': 'abc-123',
    'http_method': 'POST',
    'http_path': '/api/users',
    'http_status': 201,
    'duration_ms': 45,
})
```

**Características:**
- ✅ Formato JSON estructurado
- ✅ Timestamps automáticos
- ✅ Context injection (service, environment, version)
- ✅ File handlers (error.log, combined.log)
- ✅ Convenience functions para eventos comunes

### 2. Loki Configuration

```yaml
# loki/loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  instance_addr: 127.0.0.1
  path_prefix: /tmp/loki
  storage:
    filesystem:
      chunks_directory: /tmp/loki/chunks
      rules_directory: /tmp/loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2020-10-24
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://alertmanager:9093

# Limits
limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  ingestion_rate_mb: 16
  ingestion_burst_size_mb: 32
  max_query_length: 721h
  max_query_parallelism: 32
  max_streams_per_user: 10000
  max_line_size: 256KB

  # Retention
  retention_period: 720h  # 30 days
  per_stream_rate_limit: 3MB
  per_stream_rate_limit_burst: 15MB

# Compactor
compactor:
  working_directory: /tmp/loki/compactor
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150
```

### 3. Promtail Configuration

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
  # Kubernetes pods
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      # Parse Docker logs
      - docker: {}

      # Extract labels
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

      # Extract log level
      - regex:
          expression: '.*level=(?P<level>\w+).*'
          source: output

      # Parse timestamp
      - timestamp:
          format: RFC3339Nano
          source: time

      # Add labels
      - labels:
          stream:
          container_name:
          level:
          namespace:
          pod:
          app:

      # Output
      - output:
          source: output

  # Application logs (file-based)
  - job_name: application-logs
    static_configs:
      - targets:
          - localhost
        labels:
          job: application
          __path__: /var/log/app/*.log
    pipeline_stages:
      # Parse JSON logs
      - json:
          expressions:
            timestamp: timestamp
            level: level
            message: message
            service: service
            trace_id: trace_id
            user_id: user_id

      # Add labels
      - labels:
          level:
          service:

      # Timestamp
      - timestamp:
          source: timestamp
          format: RFC3339

      # Output
      - output:
          source: message

  # System logs
  - job_name: system-logs
    static_configs:
      - targets:
          - localhost
        labels:
          job: syslog
          __path__: /var/log/syslog
    pipeline_stages:
      - regex:
          expression: '^(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+(?P<hostname>\S+)\s+(?P<service>\S+):\s+(?P<message>.*)$'
      - labels:
          hostname:
          service:
      - timestamp:
          source: timestamp
          format: Jan 2 15:04:05
```

### 4. Log Queries (LogQL)

```logql
# Basic queries
{job="application"} |= "error"
{service="user-service"} |= "error" != "timeout"

# Filter by level
{job="application"} | json | level="error"

# Filter by trace_id
{job="application"} | json | trace_id="abc123"

# Count errors
sum(count_over_time({job="application"} | json | level="error" [5m]))

# Rate of errors
rate({job="application"} | json | level="error" [5m])

# Top errors
topk(10, sum by (message) (count_over_time({job="application"} | json | level="error" [1h])))

# Logs by user
{job="application"} | json | user_id="12345"

# Logs in time range
{job="application"} [2024-01-15T10:00:00Z:2024-01-15T11:00:00Z]

# Aggregate by service
sum by (service) (count_over_time({job="application"} | json [5m]))

# Error rate per service
sum by (service) (rate({job="application"} | json | level="error" [5m]))
/
sum by (service) (rate({job="application"} | json [5m]))
```

### 5. Elasticsearch + Fluentd

#### 5.1 Fluentd Configuration

```xml
<!-- fluentd/fluent.conf -->
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>

<source>
  @type tail
  path /var/log/app/*.log
  pos_file /var/log/fluentd-app.log.pos
  tag app.logs
  format json
  time_key timestamp
  time_format %Y-%m-%dT%H:%M:%S.%NZ
</source>

<filter app.**>
  @type record_transformer
  <record>
    hostname "#{Socket.gethostname}"
    environment "#{ENV['ENVIRONMENT']}"
  </record>
</filter>

<filter app.**>
  @type grep
  <exclude>
    key level
    pattern /debug/
  </exclude>
</filter>

<match app.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  index_name app-logs
  type_name _doc
  logstash_format true
  logstash_prefix app
  logstash_dateformat %Y.%m.%d
  include_tag_key true
  tag_key @log_name
  flush_interval 10s
</match>

<match app.error>
  @type slack
  webhook_url https://hooks.slack.com/services/YOUR/WEBHOOK/URL
  channel alerts
  username fluentd
  title_keys level,message
  message_keys message,stack
</match>
```

### 6. Log Retention & Archival

**Script ejecutable:** [`scripts/python/log_archiver.py`](scripts/python/log_archiver.py)

Herramienta CLI para archivado y gestión de retención de logs con almacenamiento en S3.

**Cuándo ejecutar:**
- Archivado automático de logs antiguos
- Gestión de retención de logs
- Restauración de logs archivados

**Uso:**
```bash
cd scripts/python
pip install -r requirements.txt

# Archivar logs antiguos
python log_archiver.py archive \
  --s3-bucket my-logs-bucket \
  --log-dir /var/log/app \
  --retention-days 30

# Dry run (ver qué se archivaría)
python log_archiver.py archive \
  --s3-bucket my-logs-bucket \
  --log-dir /var/log/app \
  --retention-days 30 \
  --dry-run

# Restaurar logs archivados
python log_archiver.py restore \
  --s3-bucket my-logs-bucket \
  --date 2024-01-15 \
  --s3-prefix logs \
  --output-dir /tmp/restored
```

**Características:**
- ✅ Compresión automática (gzip)
- ✅ Upload a S3
- ✅ Restauración de logs archivados
- ✅ Dry-run mode
- ✅ Retención configurable

## 🎯 Mejores Prácticas

### 1. Log Levels

✅ **DO:**
- Use appropriate log levels (DEBUG, INFO, WARN, ERROR)
- Log at INFO for business events
- Log at ERROR for failures
- Include context in logs

❌ **DON'T:**
- Log everything at DEBUG
- Log sensitive data
- Log in tight loops
- Use unclear log messages

### 2. Structured Logging

✅ **DO:**
- Use JSON format
- Include timestamps
- Add correlation IDs
- Include request context

❌ **DON'T:**
- Use unstructured text
- Include PII without encryption
- Log without timestamps

### 3. Performance

✅ **DO:**
- Use async logging
- Batch log writes
- Limit log verbosity in production
- Use log sampling for high-volume

❌ **DON'T:**
- Block on log writes
- Log in performance-critical paths
- Log excessive data

## 🚨 Troubleshooting

### High Log Volume

1. Review log levels
2. Implement log sampling
3. Filter unnecessary logs
4. Archive old logs

### Missing Logs

1. Check log collection agents
2. Verify network connectivity
3. Check disk space
4. Review retention policies

## 📚 Recursos Adicionales

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [Elasticsearch Guide](https://www.elastic.co/guide/)
- [Fluentd Documentation](https://docs.fluentd.org/)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+

