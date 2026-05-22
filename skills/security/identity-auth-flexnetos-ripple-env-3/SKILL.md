---
name: Identity & Authentication
description: "Identity management and authentication systems. Activate when: (1) Configuring Keycloak realms/clients, (2) Writing OPA policies, (3) Managing Vault secrets, (4) Implementing OIDC/OAuth2 flows, or (5) Setting up RBAC/ABAC authorization."
---

# Identity & Authentication

## Overview

This skill covers identity management, authentication, and authorization using Keycloak, OPA (Open Policy Agent), and HashiCorp Vault.

## Keycloak

### Key Concepts

| Concept | Description |
|---------|-------------|
| Realm | A tenant - isolated namespace for users, clients, roles |
| Client | An application that can request authentication |
| User | An identity that can authenticate |
| Role | A set of permissions |
| Group | A collection of users |
| Identity Provider | External auth source (LDAP, social login) |

### Admin CLI (kcadm)

```bash
# Configure CLI
kcadm.sh config credentials \
  --server http://localhost:8080 \
  --realm master \
  --user admin \
  --password admin

# Create realm
kcadm.sh create realms -s realm=myrealm -s enabled=true

# Create client
kcadm.sh create clients -r myrealm \
  -s clientId=myapp \
  -s enabled=true \
  -s publicClient=false \
  -s secret=mysecret \
  -s 'redirectUris=["http://localhost:8080/*"]' \
  -s 'webOrigins=["http://localhost:8080"]'

# Create user
kcadm.sh create users -r myrealm \
  -s username=testuser \
  -s enabled=true \
  -s emailVerified=true \
  -s email=test@example.com

# Set password
kcadm.sh set-password -r myrealm --username testuser --new-password test123

# Create role
kcadm.sh create roles -r myrealm -s name=admin

# Assign role to user
kcadm.sh add-roles -r myrealm --uusername testuser --rolename admin
```

### OIDC Token Flow

```bash
# Get token (password grant - dev only)
curl -X POST "http://localhost:8080/realms/myrealm/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=myapp" \
  -d "client_secret=mysecret" \
  -d "username=testuser" \
  -d "password=test123" \
  -d "grant_type=password"

# Introspect token
curl -X POST "http://localhost:8080/realms/myrealm/protocol/openid-connect/token/introspect" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=myapp" \
  -d "client_secret=mysecret" \
  -d "token=<access_token>"
```

## OPA (Open Policy Agent)

### Rego Policy Basics

```rego
# policy.rego
package authz

import future.keywords.if
import future.keywords.in

default allow := false

# Allow admins everything
allow if {
    "admin" in input.user.roles
}

# Allow users to read own resources
allow if {
    input.action == "read"
    input.resource.owner == input.user.id
}

# Allow read on public resources
allow if {
    input.action == "read"
    input.resource.public == true
}
```

### OPA CLI

```bash
# Evaluate policy
opa eval -d policy.rego -i input.json "data.authz.allow"

# Test policies
opa test . -v

# Run as server
opa run --server policy.rego

# Query server
curl -X POST http://localhost:8181/v1/data/authz/allow \
  -H "Content-Type: application/json" \
  -d '{"input": {"user": {"roles": ["admin"]}}}'
```

### Policy Testing

```rego
# policy_test.rego
package authz

test_admin_allowed {
    allow with input as {
        "user": {"roles": ["admin"]},
        "action": "delete",
        "resource": {"type": "post"}
    }
}

test_user_cannot_delete {
    not allow with input as {
        "user": {"roles": ["user"]},
        "action": "delete",
        "resource": {"type": "post"}
    }
}
```

## HashiCorp Vault

### Basic Operations

```bash
# Start dev server
vault server -dev

# Set address
export VAULT_ADDR='http://127.0.0.1:8200'

# Login
vault login <token>

# KV Secrets Engine
vault secrets enable -path=secret kv-v2
vault kv put secret/myapp/config api_key=xxx db_pass=yyy
vault kv get secret/myapp/config
vault kv get -field=api_key secret/myapp/config

# List secrets
vault kv list secret/myapp/
```

### Policies

```hcl
# myapp-policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/myapp/*" {
  capabilities = ["list"]
}

path "database/creds/myapp" {
  capabilities = ["read"]
}
```

```bash
# Create policy
vault policy write myapp myapp-policy.hcl

# List policies
vault policy list
```

### AppRole Authentication

```bash
# Enable AppRole
vault auth enable approle

# Create role
vault write auth/approle/role/myapp \
    secret_id_ttl=10m \
    token_num_uses=10 \
    token_ttl=20m \
    token_max_ttl=30m \
    secret_id_num_uses=40 \
    token_policies="myapp"

# Get role ID
vault read auth/approle/role/myapp/role-id

# Generate secret ID
vault write -f auth/approle/role/myapp/secret-id

# Login with AppRole
vault write auth/approle/login \
    role_id=<role_id> \
    secret_id=<secret_id>
```

### Dynamic Database Credentials

```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL
vault write database/config/mydb \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
    allowed_roles="readonly" \
    username="vault" \
    password="vault"

# Create role
vault write database/roles/readonly \
    db_name=mydb \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Get credentials
vault read database/creds/readonly
```

## Integration Patterns

### JWT Validation in API

```python
# Python example with PyJWT
import jwt
from jwt import PyJWKClient

KEYCLOAK_URL = "http://localhost:8080/realms/myrealm"
jwks_client = PyJWKClient(f"{KEYCLOAK_URL}/protocol/openid-connect/certs")

def validate_token(token: str) -> dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience="myapp",
        issuer=KEYCLOAK_URL
    )
```

### OPA Sidecar Pattern

```yaml
# Kubernetes deployment with OPA sidecar
spec:
  containers:
    - name: app
      image: myapp:latest
    - name: opa
      image: openpolicyagent/opa:latest
      args:
        - "run"
        - "--server"
        - "--addr=localhost:8181"
        - "/policies"
      volumeMounts:
        - name: policies
          mountPath: /policies
```

## External Links

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [OPA Documentation](https://www.openpolicyagent.org/docs/)
- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [OIDC Specification](https://openid.net/specs/openid-connect-core-1_0.html)
