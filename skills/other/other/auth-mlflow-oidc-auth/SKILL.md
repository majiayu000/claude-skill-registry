---
name: auth:mlflow-oidc-auth
description: Configure MLflow with mlflow-oidc-auth plugin for Keycloak OIDC authentication
---

# MLflow OIDC Authentication

Configure MLflow Tracking Server with Keycloak OIDC authentication using the mlflow-oidc-auth plugin.

## Overview

mlflow-oidc-auth is a FastAPI wrapper around MLflow that provides:
- OIDC authentication via Keycloak
- Group-based authorization (READ/EDIT/MANAGE permissions)
- Session management for browser access
- Basic/Bearer auth for programmatic access

## Architecture

```
Browser → Keycloak OIDC → mlflow-oidc-auth → MLflow Flask → PostgreSQL
OTEL    → mTLS (Istio) → /v1/traces       → MLflow      → PostgreSQL
```

## Required Environment Variables

```yaml
env:
  # Database for MLflow
  - name: MLFLOW_BACKEND_STORE_URI
    value: "postgresql://user:pass@postgres:5432/mlflow"
  - name: MLFLOW_TRACKING_URI
    value: "postgresql://user:pass@postgres:5432/mlflow"  # Needed for otel_router

  # OIDC Configuration
  - name: OIDC_DISCOVERY_URL
    value: "http://keycloak-service.keycloak:8080/realms/master/.well-known/openid-configuration"
  - name: OIDC_CLIENT_ID
    value: "mlflow"
  - name: OIDC_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: mlflow-oauth-secret
        key: OIDC_CLIENT_SECRET

  # OIDC Groups for Authorization
  - name: OIDC_GROUP_NAME
    value: "mlflow"  # Users must be in this group
  - name: OIDC_ADMIN_GROUP_NAME
    value: "mlflow-admin"  # Admin users group

  # Database for OIDC plugin
  - name: OIDC_USERS_DB_URI
    value: "postgresql://user:pass@postgres:5432/mlflow"
```

## OTEL Trace Ingestion Setup

### Problem

mlflow-oidc-auth doesn't include MLflow's `otel_router` which provides the `/v1/traces` OTLP endpoint.

### Solution: Runtime Patches

Apply two patches before starting the app:

```python
# Patch 1: Add otel_router to get_all_routers()
from mlflow.server.otel_api import otel_router
import mlflow_oidc_auth.routers as routers_module

original_get_all_routers = routers_module.get_all_routers
def patched_get_all_routers():
    return original_get_all_routers() + [otel_router]
routers_module.get_all_routers = patched_get_all_routers

# Patch 2: Exclude /v1/traces from OIDC auth
from mlflow_oidc_auth.middleware.auth_middleware import AuthMiddleware

original_is_unprotected = AuthMiddleware._is_unprotected_route
def patched_is_unprotected(self, path: str) -> bool:
    if path.startswith("/v1/traces"):
        return True
    return original_is_unprotected(self, path)
AuthMiddleware._is_unprotected_route = patched_is_unprotected

# NOW import app (uses patched functions)
from mlflow_oidc_auth.app import app
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=5000)
```

### Security

The `/v1/traces` endpoint is secured via Istio instead of OIDC:

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: mlflow-traces-from-otel
spec:
  targetRefs:
    - kind: Service
      name: mlflow
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/kagenti-system/sa/otel-collector"
      to:
        - operation:
            methods: ["POST"]
            paths: ["/v1/traces", "/v1/traces/*"]
    - to:
        - operation:
            notPaths: ["/v1/traces", "/v1/traces/*"]
```

## Waypoint Proxy for L7 Auth

The AuthorizationPolicy needs L7 (path-based) evaluation, which requires a waypoint proxy:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: mlflow-waypoint
  labels:
    istio.io/waypoint-for: service
spec:
  gatewayClassName: istio-waypoint
  listeners:
    - name: mesh
      port: 15008
      protocol: HBONE
```

Add the waypoint label to the MLflow service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mlflow
  labels:
    istio.io/use-waypoint: mlflow-waypoint
```

## Helm Chart Integration

See `charts/kagenti-deps/templates/mlflow.yaml` for the full implementation.

Key values:
```yaml
mlflow:
  auth:
    enabled: true
    secretName: mlflow-oauth-secret
```

## Programmatic API Access

### Using Client Credentials Flow

For E2E tests and CI/CD pipelines, use the MLflow client's OAuth credentials:

```python
import base64
import requests
from kubernetes import client, config

# Get credentials from K8s secret
config.load_kube_config()
k8s = client.CoreV1Api()
secret = k8s.read_namespaced_secret("mlflow-oauth-secret", "kagenti-system")

client_id = base64.b64decode(secret.data["OIDC_CLIENT_ID"]).decode()
client_secret = base64.b64decode(secret.data["OIDC_CLIENT_SECRET"]).decode()
token_url = base64.b64decode(secret.data["OIDC_TOKEN_URL"]).decode()

# Get token using client credentials flow
response = requests.post(token_url, data={
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}, verify=False)

access_token = response.json()["access_token"]

# Set for MLflow Python client
import os
os.environ["MLFLOW_TRACKING_TOKEN"] = access_token
```

**Important**: Use the `mlflow` client credentials, NOT `admin-cli`. The mlflow-oidc-auth
validates the token audience and will reject tokens from other clients.

## Troubleshooting

### "Authentication required" for /v1/traces

Verify patches are applied:
```bash
kubectl logs -n kagenti-system deploy/mlflow -c mlflow | grep "otel_router"
# Should see: "Patched get_all_routers() to include otel_router"
# Should see: "Excluded /v1/traces from OIDC auth (mTLS via Istio)"
```

### Bearer token rejected with "Invalid token"

Check MLflow logs for SSL errors:
```bash
kubectl logs -n kagenti-system deploy/mlflow -c mlflow | grep -i "ssl\|cert\|jwks"
```

If you see `CERTIFICATE_VERIFY_FAILED`, the CA bundle is incomplete. On OpenShift/HyperShift:
- Set `SSL_CERT_FILE` (for httpx/authlib) in addition to `REQUESTS_CA_BUNDLE`
- Include both ingress CA and root CA in the bundle (HyperShift uses a CA chain)

```yaml
# In mlflow.yaml startup script:
export SSL_CERT_FILE=/etc/pki/ingress-ca/ingress-ca.pem && \
export REQUESTS_CA_BUNDLE=/etc/pki/ingress-ca/ingress-ca.pem && \
```

### SQLite errors for trace storage

Ensure both `MLFLOW_BACKEND_STORE_URI` AND `MLFLOW_TRACKING_URI` are set to PostgreSQL.

### Traces not appearing

1. Check OTEL collector logs:
```bash
kubectl logs -n kagenti-system deploy/otel-collector | grep mlflow
```

2. Verify trace count in database:
```bash
kubectl exec -n kagenti-system postgres-otel-0 -- \
  psql -U postgres -d mlflow -c "SELECT COUNT(*) FROM trace_info;"
```

3. Check AuthorizationPolicy:
```bash
kubectl get authorizationpolicy -n kagenti-system mlflow-traces-from-otel -o yaml
```

## Known Limitations

1. **No path exclusion config**: mlflow-oidc-auth hardcodes unprotected paths
2. **Missing otel_router**: Not included in get_all_routers()
3. **Direct Access Grants disabled**: MLflow client uses client_credentials flow only, not password grant

## Future Improvements

- Upstream PR for `OIDC_EXCLUDE_PATHS` environment variable
- Upstream PR to include `otel_router` in standard routers
- Consider Istio-level auth as alternative to application auth

## Related Skills

- `auth:otel-oauth2-exporter`
- `auth:keycloak-confidential-client`
- `istio:ambient-waypoint`
