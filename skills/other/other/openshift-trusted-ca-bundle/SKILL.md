---
name: openshift:trusted-ca-bundle
description: Use OpenShift's trusted CA bundle for TLS verification in pods
---

# OpenShift Trusted CA Bundle

Use OpenShift's automatically-managed trusted CA bundle for TLS verification in pods.

## Table of Contents

- [Overview](#overview)
- [Pre-existing ConfigMap](#pre-existing-configmap)
- [Volume Mount Pattern](#volume-mount-pattern)
- [Usage in Applications](#usage-in-applications)
- [Helm Chart Integration](#helm-chart-integration)
- [Troubleshooting](#troubleshooting)

## Overview

OpenShift automatically creates a ConfigMap named `config-trusted-cabundle` in each namespace that contains the cluster's trusted CA certificates. This is useful for services that need to verify TLS connections to internal services or external endpoints.

## Pre-existing ConfigMap

OpenShift automatically maintains this ConfigMap:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-trusted-cabundle
  namespace: <any-namespace>
data:
  ca-bundle.crt: |
    -----BEGIN CERTIFICATE-----
    # ... certificates ...
    -----END CERTIFICATE-----
```

**Important**: This ConfigMap exists automatically in every namespace. Do NOT create it manually.

## Volume Mount Pattern

Mount the CA bundle in your pod:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service
spec:
  template:
    spec:
      containers:
        - name: my-service
          volumeMounts:
            - name: trusted-ca
              mountPath: /etc/pki/ca-trust/extracted/pem
              readOnly: true
      volumes:
        - name: trusted-ca
          configMap:
            name: config-trusted-cabundle
            items:
              - key: ca-bundle.crt
                path: tls-ca-bundle.pem
```

## Usage in Applications

### Python (requests)

```python
import requests

response = requests.get(
    "https://internal-service.example.com",
    verify="/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem"
)
```

### Python (python-keycloak)

```python
from keycloak import KeycloakAdmin

keycloak_admin = KeycloakAdmin(
    server_url="https://keycloak.example.com",
    verify="/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem"
)
```

### OTEL Collector

```yaml
extensions:
  oauth2client/mlflow:
    token_url: https://keycloak.example.com/realms/master/protocol/openid-connect/token
    tls:
      ca_file: /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
```

### curl

```bash
curl --cacert /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
  https://internal-service.example.com
```

## Anti-Pattern: Creating ConfigMap with Injection

Do NOT create a ConfigMap with the injection annotation:

```yaml
# DON'T DO THIS
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-custom-ca-bundle
  annotations:
    service.beta.openshift.io/inject-cabundle: "true"
data: {}
```

**Why**: The injection annotation doesn't inject certificates immediately. The ConfigMap may be empty when the pod starts, causing TLS failures.

## Best Practices

### 1. Use Internal URLs When Possible

Avoid TLS complexity entirely by using internal service URLs:

```yaml
# Instead of external URL
KEYCLOAK_URL: "https://keycloak.apps.example.com"

# Use internal URL
KEYCLOAK_URL: "http://keycloak-service.keycloak.svc.cluster.local:8080"
```

### 2. Conditional TLS Based on Platform

```yaml
{{- if eq .Values.global.platform "ocp" }}
tls:
  ca_file: /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
{{- end }}
```

### 3. Check CA Bundle Exists

```bash
kubectl exec -it <pod> -- ls -la /etc/pki/ca-trust/extracted/pem/
```

## Helm Chart Integration

```yaml
{{- if .Values.global.openshift.enabled }}
spec:
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          volumeMounts:
            - name: trusted-ca
              mountPath: /etc/pki/ca-trust/extracted/pem
              readOnly: true
      volumes:
        - name: trusted-ca
          configMap:
            name: config-trusted-cabundle
            items:
              - key: ca-bundle.crt
                path: tls-ca-bundle.pem
{{- end }}
```

## Troubleshooting

### Certificate Verify Failed

```
ssl.SSLCertVerificationError: certificate verify failed
```

1. Check if CA bundle is mounted:
```bash
kubectl exec -it <pod> -- cat /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
```

2. Verify application is using the correct path

3. Consider using internal HTTP URL instead

### ConfigMap Not Found

```
Error: configmap "config-trusted-cabundle" not found
```

This shouldn't happen on OpenShift. Check if:
- You're actually running on OpenShift (not Kind/vanilla k8s)
- The namespace exists and is active

### Empty CA Bundle

If the ConfigMap exists but is empty:
- Check OpenShift cluster CA configuration
- Contact cluster administrator

## Platform Differences

| Platform | CA Bundle Availability |
|----------|----------------------|
| OpenShift | Automatic (`config-trusted-cabundle`) |
| Kind | Not available (use internal URLs) |
| Vanilla k8s | Not available (manual configuration needed) |

## Related Skills

- `auth:keycloak-confidential-client`
- `auth:otel-oauth2-exporter`
