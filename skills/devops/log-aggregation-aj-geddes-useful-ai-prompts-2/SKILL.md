---
name: log-aggregation
description: Implement centralized logging with ELK Stack, Loki, or Splunk for log collection, parsing, storage, and analysis across infrastructure.
---

# Log Aggregation

## Overview

Build comprehensive log aggregation systems to collect, parse, and analyze logs from multiple sources, enabling centralized monitoring, debugging, and compliance auditing.

## When to Use

- Centralized log collection
- Distributed system debugging
- Compliance and audit logging
- Security event monitoring
- Application performance analysis
- Error tracking and alerting
- Historical log retention
- Real-time log searching

## Implementation Examples

### 1. **ELK Stack Configuration**

```yaml
# docker-compose.yml - ELK Stack setup
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    healthcheck:
      test: curl -s http://localhost:9200 >/dev/null || exit 1
      interval: 10s
      timeout: 5s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5000:5000"
      - "9600:9600"
    depends_on:
      - elasticsearch
    environment:
      - "LS_JAVA_OPTS=-Xmx256m -Xms256m"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_URL=http://elasticsearch:9200
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.5.0
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: filebeat -e -strict.perms=false
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

### 2. **Logstash Pipeline Configuration**

```conf
# logstash.conf
input {
  # Receive logs via TCP/UDP
  tcp {
    port => 5000
    codec => json
  }

  # Read from files
  file {
    path => "/var/log/app/*.log"
    start_position => "beginning"
    codec => multiline {
      pattern => "^%{TIMESTAMP_ISO8601}"
      negate => true
      what => "previous"
    }
  }

  # Read from Kubernetes
  kubernetes {
    kubernetes_url => "https://kubernetes.default"
    ca_file => "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
  }
}

filter {
  # Parse JSON logs
  json {
    source => "message"
    target => "parsed"
  }

  # Extract fields
  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{GREEDYDATA:message}"
    }
  }

  # Add timestamp
  date {
    match => ["timestamp", "ISO8601"]
    target => "@timestamp"
  }

  # Add metadata
  mutate {
    add_field => {
      "environment" => "production"
      "datacenter" => "us-east-1"
    }
    remove_field => ["host"]
  }

  # Drop debug logs in production
  if [level] == "DEBUG" {
    drop { }
  }

  # Tag errors
  if [level] =~ /ERROR|FATAL/ {
    mutate {
      add_tag => ["error"]
    }
  }
}

output {
  # Send to Elasticsearch
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
    document_type => "_doc"
  }

  # Also output errors to console
  if "error" in [tags] {
    stdout {
      codec => rubydebug
    }
  }
}
```

### 3. **Filebeat Configuration**

```yaml
# filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/app/*.log
    fields:
      app: myapp
      environment: production
    multiline.pattern: '^\['
    multiline.negate: true
    multiline.match: after

  - type: docker
    enabled: true
    hints.enabled: true
    hints.default_config:
      enabled: true
      type: container
      paths:
        - /var/lib/docker/containers/${data.docker.container.id}/*.log

  - type: log
    enabled: true
    paths:
      - /var/log/syslog
      - /var/log/auth.log
    fields:
      service: system
      environment: production

processors:
  - add_docker_metadata:
      host: "unix:///var/run/docker.sock"
  - add_kubernetes_metadata:
      in_cluster: true
  - add_host_metadata:
  - add_fields:
      target: ''
      fields:
        environment: production

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "filebeat-%{+yyyy.MM.dd}"

logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0640
```

### 4. **Kibana Dashboard and Alerts**

```json
{
  "dashboard": {
    "title": "Application Logs Overview",
    "panels": [
      {
        "title": "Error Rate by Service",
        "query": "level: ERROR",
        "visualization": "bar_chart",
        "groupBy": ["service"],
        "timeRange": "1h"
      },
      {
        "title": "Top 10 Error Messages",
        "query": "level: ERROR",
        "visualization": "table",
        "fields": ["message", "count"],
        "sort": [{"count": "desc"}],
        "size": 10
      },
      {
        "title": "Request Latency Distribution",
        "query": "duration: *",
        "visualization": "histogram"
      },
      {
        "title": "Errors Over Time",
        "query": "level: ERROR",
        "visualization": "line_chart",
        "dateHistogram": "1m"
      }
    ]
  },
  "alerts": [
    {
      "name": "High Error Rate",
      "query": "level: ERROR",
      "threshold": 100,
      "window": "5m",
      "action": "slack"
    },
    {
      "name": "Critical Exceptions",
      "query": "level: FATAL",
      "threshold": 1,
      "window": "1m",
      "action": "email"
    }
  ]
}
```

### 5. **Loki Configuration (Kubernetes)**

```yaml
# loki-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: loki-config
  namespace: logging
data:
  loki-config.yaml: |
    auth_enabled: false

    ingester:
      chunk_idle_period: 3m
      chunk_retain_period: 1m
      max_chunk_age: 1h
      chunk_encoding: snappy
      chunk_target_size: 1048576

    limits_config:
      enforce_metric_name: false
      reject_old_samples: true
      reject_old_samples_max_age: 168h

    schema_config:
      configs:
        - from: 2020-05-15
          store: boltdb-shipper
          object_store: filesystem
          schema: v11
          index:
            prefix: index_
            period: 24h

    server:
      http_listen_port: 3100

    storage_config:
      boltdb_shipper:
        active_index_directory: /loki/index
        cache_location: /loki/cache
        shared_store: filesystem
      filesystem:
        directory: /loki/chunks

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loki
  namespace: logging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: loki
  template:
    metadata:
      labels:
        app: loki
    spec:
      containers:
        - name: loki
          image: grafana/loki:2.8.0
          ports:
            - containerPort: 3100
          volumeMounts:
            - name: loki-config
              mountPath: /etc/loki
            - name: loki-storage
              mountPath: /loki
          args:
            - -config.file=/etc/loki/loki-config.yaml
      volumes:
        - name: loki-config
          configMap:
            name: loki-config
        - name: loki-storage
          emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: loki
  namespace: logging
spec:
  selector:
    app: loki
  ports:
    - port: 3100
      targetPort: 3100
```

### 6. **Log Aggregation Deployment Script**

```bash
#!/bin/bash
# deploy-logging.sh - Deploy logging infrastructure

set -euo pipefail

NAMESPACE="logging"
ENV="${1:-production}"

echo "Deploying logging stack to $ENV..."

# Create namespace
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Deploy Elasticsearch
echo "Deploying Elasticsearch..."
kubectl apply -f elasticsearch-deployment.yaml -n "$NAMESPACE"
kubectl rollout status deployment/elasticsearch -n "$NAMESPACE" --timeout=5m

# Deploy Logstash
echo "Deploying Logstash..."
kubectl apply -f logstash-deployment.yaml -n "$NAMESPACE"
kubectl rollout status deployment/logstash -n "$NAMESPACE" --timeout=5m

# Deploy Kibana
echo "Deploying Kibana..."
kubectl apply -f kibana-deployment.yaml -n "$NAMESPACE"
kubectl rollout status deployment/kibana -n "$NAMESPACE" --timeout=5m

# Deploy Filebeat as DaemonSet
echo "Deploying Filebeat..."
kubectl apply -f filebeat-daemonset.yaml -n "$NAMESPACE"

# Wait for all pods
echo "Waiting for all logging services..."
kubectl wait --for=condition=ready pod -l app=elasticsearch -n "$NAMESPACE" --timeout=300s

# Create default index pattern
echo "Setting up Kibana index pattern..."
kubectl exec -it -n "$NAMESPACE" svc/kibana -- curl -X POST \
  http://localhost:5601/api/saved_objects/index-pattern/logs \
  -H 'kbn-xsrf: true' \
  -H 'Content-Type: application/json' \
  -d '{"attributes":{"title":"logs-*","timeFieldName":"@timestamp"}}'

echo "Logging stack deployed successfully!"
echo "Kibana: http://localhost:5601"
```

## Best Practices

### ✅ DO
- Parse and structure log data
- Use appropriate log levels
- Add contextual information
- Implement log retention policies
- Set up log-based alerting
- Index important fields
- Use consistent timestamp formats
- Implement access controls

### ❌ DON'T
- Store sensitive data in logs
- Log at DEBUG level in production
- Send raw unstructured logs
- Ignore storage costs
- Skip log parsing
- Lack monitoring of log systems
- Store logs forever
- Log PII without encryption

## Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Loki Documentation](https://grafana.com/docs/loki/latest/)
