---
name: auth:keycloak-confidential-client
description: Create confidential OAuth2 clients in Keycloak for server-to-service authentication
---

# Keycloak Confidential Client Pattern

Create confidential OAuth2 clients in Keycloak for server-side applications using client credentials flow.

## Table of Contents

- [Overview](#overview)
- [Key Configuration](#key-configuration)
- [Python Script Pattern](#python-script-pattern)
- [Kubernetes Job Pattern](#kubernetes-job-pattern)
- [RBAC Requirements](#rbac-requirements)
- [SSL Certificate Handling](#ssl-certificate-handling)
- [Secret Structure](#secret-structure)
- [Troubleshooting](#troubleshooting)

## Overview

Keycloak supports two types of OAuth2 clients:
- **Public clients**: For browser-based SPAs using PKCE flow
- **Confidential clients**: For server-side applications using client credentials flow

This skill focuses on confidential clients for service-to-service authentication.

## Key Configuration

### Required Settings for Client Credentials Flow

```python
keycloak_admin.create_client({
    "clientId": "my-service",
    "name": "My Service Client",
    "enabled": True,
    "protocol": "openid-connect",
    "publicClient": False,  # This makes it a confidential client
    "serviceAccountsEnabled": True,  # REQUIRED for client credentials grant
    "standardFlowEnabled": False,  # No authorization code flow
    "directAccessGrantsEnabled": False,  # No password grant
})
```

**Critical**: `serviceAccountsEnabled: True` is REQUIRED for the client credentials grant type. Without this, the token endpoint will reject requests with `invalid_grant`.

## Python Script Pattern

Use the `python-keycloak` library:

```python
from keycloak import KeycloakAdmin

def create_confidential_client(keycloak_url, realm, admin_user, admin_pass, client_id):
    """Create a confidential OAuth2 client."""
    keycloak_admin = KeycloakAdmin(
        server_url=keycloak_url,
        username=admin_user,
        password=admin_pass,
        realm_name=realm,
        verify=True
    )

    # Create client
    keycloak_admin.create_client({
        "clientId": client_id,
        "enabled": True,
        "publicClient": False,
        "serviceAccountsEnabled": True,
        "standardFlowEnabled": False,
    })

    # Get client secret
    client_uuid = keycloak_admin.get_client_id(client_id)
    client_secret = keycloak_admin.get_client_secrets(client_uuid)["value"]

    return client_secret
```

## Kubernetes Job Pattern

Deploy as a Kubernetes Job that runs during installation:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-service-oauth-secret
  namespace: kagenti-system
spec:
  template:
    spec:
      serviceAccountName: my-service-client-registration
      containers:
        - name: register
          image: python:3.11-slim
          command: ["python", "/scripts/register.py"]
          env:
            - name: KEYCLOAK_URL
              value: "http://keycloak-service.keycloak.svc.cluster.local:8080"
            - name: KEYCLOAK_ADMIN
              valueFrom:
                secretKeyRef:
                  name: keycloak-admin
                  key: username
            - name: KEYCLOAK_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: keycloak-admin
                  key: password
          volumeMounts:
            - name: scripts
              mountPath: /scripts
      restartPolicy: OnFailure
      volumes:
        - name: scripts
          configMap:
            name: my-service-oauth-script
```

## RBAC Requirements

When creating secrets in other namespaces, you need cross-namespace RoleBindings:

```yaml
# Role in target namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-creator
  namespace: kagenti-system
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["create", "get", "update", "patch"]

---
# RoleBinding to service account in source namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: keycloak-secret-creator
  namespace: kagenti-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: secret-creator
subjects:
  - kind: ServiceAccount
    name: my-service-client-registration
    namespace: keycloak
```

## SSL Certificate Handling

### Option 1: Use Internal Keycloak URL (Recommended)

Avoid TLS complexity by using the internal service URL:
```
http://keycloak-service.keycloak.svc.cluster.local:8080
```

### Option 2: Use OpenShift Trusted CA Bundle

Mount the pre-existing CA bundle:
```yaml
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

## Secret Structure

Different consumers expect different secret key names:

### MLflow
```yaml
data:
  OIDC_CLIENT_ID: <base64>
  OIDC_CLIENT_SECRET: <base64>
  OIDC_TOKEN_URL: <base64>
```

### Phoenix
```yaml
data:
  PHOENIX_OAUTH2_CLIENT_ID: <base64>
  PHOENIX_OAUTH2_CLIENT_SECRET: <base64>
```

### OTEL Collector
```yaml
data:
  MLFLOW_CLIENT_ID: <base64>
  MLFLOW_CLIENT_SECRET: <base64>
```

## Troubleshooting

### Error: `invalid_grant`
- Ensure `serviceAccountsEnabled: True` is set on the client
- Check that the client secret is correct

### Error: `SSL certificate problem`
- Use internal Keycloak URL to avoid TLS issues
- Or mount the trusted CA bundle

### Error: `Access denied`
- Check RoleBinding is in the correct namespace
- Verify service account name matches

## Related Skills

- `auth:otel-oauth2-exporter`
- `openshift:trusted-ca-bundle`
