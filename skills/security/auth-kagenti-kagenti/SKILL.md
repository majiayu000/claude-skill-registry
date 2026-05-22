---
name: auth
description: Authentication and authorization patterns for Kagenti services
---

# Authentication Skills

Skills for configuring OAuth2, Keycloak, and service-to-service authentication.

## Available Skills

| Skill | Description |
|-------|-------------|
| `auth:keycloak-confidential-client` | Create OAuth2 clients for service-to-service auth |
| `auth:mlflow-oidc-auth` | Configure MLflow with Keycloak OIDC + OTEL trace ingestion |
| `auth:otel-oauth2-exporter` | Configure OTEL collector with OAuth2 |

## Common Patterns

### Internal vs External URLs

For service-to-service communication, prefer internal URLs:
```
http://keycloak-service.keycloak.svc.cluster.local:8080
```

This avoids TLS certificate complexity.

### Client Credentials Flow

For backend services, use client credentials flow:
1. Create confidential client in Keycloak
2. Get token from token endpoint
3. Attach bearer token to requests

## Related Skills

- `openshift:trusted-ca-bundle`
- `istio:ambient-waypoint`
