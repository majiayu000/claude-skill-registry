---
name: auth:otel-oauth2-exporter
description: Configure OpenTelemetry Collector with OAuth2 authentication for trace export
---

# OTEL OAuth2 Exporter Configuration

Configure the OpenTelemetry Collector to authenticate to backends using OAuth2 client credentials flow.

## Table of Contents

- [Overview](#overview)
- [Configuration Pattern](#configuration-pattern)
- [Environment Variable Injection](#environment-variable-injection)
- [TLS Configuration](#tls-configuration)
- [Helm Chart Integration](#helm-chart-integration)
- [Troubleshooting](#troubleshooting)

## Overview

When exporting traces to backends that require authentication (e.g., MLflow with Keycloak), the OTEL Collector can use the `oauth2clientauthextension` to obtain and attach bearer tokens automatically.

## Configuration Pattern

### Extension Configuration

```yaml
extensions:
  oauth2client/mlflow:
    client_id: ${env:MLFLOW_CLIENT_ID}
    client_secret: ${env:MLFLOW_CLIENT_SECRET}
    token_url: ${env:KEYCLOAK_TOKEN_URL}
    scopes: ["openid"]
    timeout: 10s
    tls:
      ca_file: /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
```

### Exporter with Auth

```yaml
exporters:
  otlphttp/mlflow:
    traces_endpoint: http://mlflow:5000/v1/traces
    auth:
      authenticator: oauth2client/mlflow
```

### Full Pipeline Configuration

```yaml
extensions:
  health_check: {}
  oauth2client/mlflow:
    client_id: ${env:MLFLOW_CLIENT_ID}
    client_secret: ${env:MLFLOW_CLIENT_SECRET}
    token_url: ${env:KEYCLOAK_TOKEN_URL}
    scopes: ["openid"]
    timeout: 10s
    tls:
      ca_file: /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem

receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 100

exporters:
  otlphttp/mlflow:
    traces_endpoint: http://mlflow:5000/v1/traces
    auth:
      authenticator: oauth2client/mlflow

service:
  extensions: [health_check, oauth2client/mlflow]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp/mlflow]
```

## Environment Variable Injection

### From Kubernetes Secret

```yaml
containers:
  - name: otel-collector
    env:
      - name: MLFLOW_CLIENT_ID
        valueFrom:
          secretKeyRef:
            name: mlflow-oauth-secret
            key: MLFLOW_CLIENT_ID
      - name: MLFLOW_CLIENT_SECRET
        valueFrom:
          secretKeyRef:
            name: mlflow-oauth-secret
            key: MLFLOW_CLIENT_SECRET
      - name: KEYCLOAK_TOKEN_URL
        value: "http://keycloak-service.keycloak.svc.cluster.local:8080/realms/master/protocol/openid-connect/token"
```

## TLS Configuration

### For External Token Endpoints

When the Keycloak endpoint uses HTTPS with a custom CA:

```yaml
oauth2client/mlflow:
  tls:
    ca_file: /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
    insecure: false
```

### For Internal Token Endpoints

When using the internal HTTP endpoint:

```yaml
oauth2client/mlflow:
  token_url: http://keycloak-service.keycloak.svc.cluster.local:8080/realms/master/protocol/openid-connect/token
  # No TLS configuration needed
```

## Helm Chart Integration

In `charts/kagenti-deps/templates/otel-collector.yaml`:

```yaml
{{- if .Values.otelCollector.mlflow.oauth2.enabled }}
extensions:
  oauth2client/mlflow:
    client_id: ${env:MLFLOW_CLIENT_ID}
    client_secret: ${env:MLFLOW_CLIENT_SECRET}
    token_url: {{ .Values.otelCollector.mlflow.oauth2.tokenUrl }}
    scopes: ["openid"]
    timeout: 10s
    {{- if .Values.otelCollector.mlflow.oauth2.tlsEnabled }}
    tls:
      ca_file: {{ .Values.otelCollector.mlflow.oauth2.caFile }}
    {{- end }}
{{- end }}
```

## Troubleshooting

### Token Request Fails

1. Check credentials:
```bash
kubectl exec -it otel-collector-xxx -n kagenti-system -- env | grep MLFLOW
```

2. Test token endpoint manually:
```bash
curl -X POST "$KEYCLOAK_TOKEN_URL" \
  -d "grant_type=client_credentials" \
  -d "client_id=$MLFLOW_CLIENT_ID" \
  -d "client_secret=$MLFLOW_CLIENT_SECRET"
```

### TLS Errors

1. Verify CA bundle is mounted:
```bash
kubectl exec -it otel-collector-xxx -n kagenti-system -- \
  ls -la /etc/pki/ca-trust/extracted/pem/
```

2. Use internal Keycloak URL to avoid TLS:
```
http://keycloak-service.keycloak.svc.cluster.local:8080
```

### Extension Not Loading

1. Ensure extension is listed in `service.extensions`
2. Check collector logs:
```bash
kubectl logs -n kagenti-system -l app=otel-collector
```

## Collector Image Requirements

The standard OTEL collector image includes `oauth2clientauthextension`. If using a custom build, ensure it's included:

```yaml
# builder-config.yaml
extensions:
  - gomod: go.opentelemetry.io/collector/extension/auth/oauth2clientauthextension v0.x.x
```

## Related Skills

- `auth:keycloak-confidential-client`
- `openshift:trusted-ca-bundle`
- `genai:semantic-conventions` - OTel GenAI semantic conventions for traces
