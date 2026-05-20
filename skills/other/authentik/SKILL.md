---
name: authentik
description: |
  Manage the Authentik identity provider via its REST API. Use when:
  (1) User asks to create, update, or delete users in Authentik,
  (2) User asks to manage groups or group memberships,
  (3) User asks to create a new OAuth2/OIDC application or provider,
  (4) User asks to protect a service with forward auth (Authentik + Traefik),
  (5) User asks about SSO, single sign-on, authentication, or identity,
  (6) User asks to manage Authentik flows, stages, or policies,
  (7) User asks to configure social login (Google, GitHub, Facebook),
  (8) User asks about OIDC for Kubernetes or who has access to what,
  (9) User deploys a new service that needs authentication.
  Authentik v2025.10.3 running in Kubernetes, managed via REST API.
author: Claude Code
version: 1.0.0
date: 2026-02-17
---

# Authentik Identity Provider Management

## Overview
- **URL**: `https://authentik.viktorbarzin.me`
- **Admin UI**: `https://authentik.viktorbarzin.me/if/admin/`
- **API Base**: `https://authentik.viktorbarzin.me/api/v3/`
- **API Docs**: `https://authentik.viktorbarzin.me/api/v3/docs/`
- **Helm Chart**: authentik v2025.10.3
- **Namespace**: `authentik`

## API Access

### Getting the Token
The API token is stored in `terraform.tfvars` (git-crypt encrypted):
```bash
AUTHENTIK_TOKEN=$(grep authentik_api_token terraform.tfvars | cut -d'"' -f2)
```

### Making API Calls
```bash
# Generic pattern
curl -s -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  "https://authentik.viktorbarzin.me/api/v3/<endpoint>/"

# With JSON body (POST/PATCH/PUT)
curl -s -X POST \
  -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  -H "Content-Type: application/json" \
  "https://authentik.viktorbarzin.me/api/v3/<endpoint>/" \
  -d '{"key": "value"}'
```

### Verify Token Works
```bash
curl -s -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  "https://authentik.viktorbarzin.me/api/v3/core/users/me/" | python3 -m json.tool
```

## Key API Endpoints

| Endpoint | Methods | Purpose |
|----------|---------|---------|
| `core/users/` | GET, POST | List/create users |
| `core/users/{id}/` | GET, PATCH, DELETE | Get/update/delete user |
| `core/groups/` | GET, POST | List/create groups |
| `core/groups/{pk}/` | GET, PATCH, DELETE | Get/update/delete group |
| `core/applications/` | GET, POST | List/create applications |
| `core/tokens/` | GET, POST | List/create tokens |
| `core/tokens/{identifier}/view_key/` | GET | View token secret key |
| `providers/all/` | GET | List all providers |
| `providers/oauth2/` | GET, POST | OAuth2/OIDC providers |
| `providers/proxy/` | GET, POST | Proxy providers (forward auth) |
| `flows/instances/` | GET | List flows |
| `stages/all/` | GET | List stages |
| `sources/all/` | GET | List sources (social login) |
| `outposts/instances/` | GET | List outposts |
| `propertymappings/provider/scope/` | GET, POST | OIDC scope mappings |
| `rbac/roles/` | GET | List roles |

## Common Operations

### List All Users
```bash
curl -s -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  "https://authentik.viktorbarzin.me/api/v3/core/users/?page_size=50" | \
  python3 -c "
import json,sys
for u in json.load(sys.stdin)['results']:
    groups=[g['name'] for g in u.get('groups_obj',[])]
    print(f\"  {u['username']:<40} {u['name']:<30} groups={groups}\")
"
```

### Create a New User
```bash
curl -s -X POST \
  -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  -H "Content-Type: application/json" \
  "https://authentik.viktorbarzin.me/api/v3/core/users/" \
  -d '{
    "username": "user@example.com",
    "name": "Full Name",
    "email": "user@example.com",
    "is_active": true,
    "type": "internal",
    "path": "users"
  }'
```

### Add User to Group
```bash
# First get the group to find current users
GROUP_PK="<group-uuid>"
CURRENT_USERS=$(curl -s -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  "https://authentik.viktorbarzin.me/api/v3/core/groups/$GROUP_PK/" | \
  python3 -c "import json,sys; print(json.load(sys.stdin)['users'])")

# Then PATCH with the updated user list (add new user pk)
curl -s -X PATCH \
  -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  -H "Content-Type: application/json" \
  "https://authentik.viktorbarzin.me/api/v3/core/groups/$GROUP_PK/" \
  -d '{"users": [<existing_pks>, <new_pk>]}'
```

### Create a New Group
```bash
curl -s -X POST \
  -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  -H "Content-Type: application/json" \
  "https://authentik.viktorbarzin.me/api/v3/core/groups/" \
  -d '{
    "name": "My New Group",
    "is_superuser": false,
    "parent": "<parent-group-pk-or-null>"
  }'
```

### Create OAuth2/OIDC Application (Full Flow)

**Step 1: Create the OAuth2 Provider**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  -H "Content-Type: application/json" \
  "https://authentik.viktorbarzin.me/api/v3/providers/oauth2/" \
  -d '{
    "name": "Provider for myapp",
    "authorization_flow": "<flow-pk>",
    "invalidation_flow": "<invalidation-flow-pk>",
    "client_type": "confidential",
    "client_id": "<generated-or-custom>",
    "client_secret": "<generated-or-custom>",
    "redirect_uris": "https://myapp.viktorbarzin.me/callback",
    "property_mappings": ["<scope-mapping-pks>"],
    "signing_key": "<signing-key-pk>"
  }'
```

**Step 2: Create the Application**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  -H "Content-Type: application/json" \
  "https://authentik.viktorbarzin.me/api/v3/core/applications/" \
  -d '{
    "name": "My App",
    "slug": "myapp",
    "provider": <provider-pk-from-step-1>,
    "meta_launch_url": "https://myapp.viktorbarzin.me"
  }'
```

### List Applications
```bash
curl -s -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  "https://authentik.viktorbarzin.me/api/v3/core/applications/?page_size=50" | \
  python3 -c "
import json,sys
for a in json.load(sys.stdin)['results']:
    ptype = a.get('provider_obj',{}).get('verbose_name','N/A')
    print(f\"  {a['name']:<30} slug={a['slug']:<25} provider={ptype}\")
"
```

### Create a Non-Expiring API Token
```bash
# Create token
curl -s -X POST \
  -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  -H "Content-Type: application/json" \
  "https://authentik.viktorbarzin.me/api/v3/core/tokens/" \
  -d '{
    "identifier": "my-token-name",
    "intent": "api",
    "expiring": false,
    "description": "Description here"
  }'

# Retrieve the key
curl -s -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  "https://authentik.viktorbarzin.me/api/v3/core/tokens/my-token-name/view_key/"
```

## Important Reference UUIDs

### Authorization Flows
| Flow | Slug | Use For |
|------|------|---------|
| Authorize Application (explicit consent) | `default-provider-authorization-explicit-consent` | Apps that should show consent screen |
| Authorize Application (implicit consent) | `default-provider-authorization-implicit-consent` | Internal/trusted apps, auto-redirect |
| Logout | `default-invalidation-flow` | Invalidation/logout flow |

### Common Property Mappings (OIDC Scopes)
These are the standard scope mappings used by most providers:
- `60e33a8c-66a2-414f-840c-b13012b4d4bd` — openid
- `1f51c659-f13b-4ad4-ba89-70458ef88e9c` — email
- `4c0bf430-7f74-4216-b9d7-23703ab544ba` — profile

### Login Sources
| Source | Slug | Matching Mode |
|--------|------|---------------|
| Google | `google` | identifier |
| GitHub | `github` | email_link |
| Facebook | `facebook` | email_link |

## Protecting a Service with Forward Auth

To protect a service via Authentik + Traefik forward auth:

1. In the service's Terraform module, set `protected = true` in the `ingress_factory` call
2. This adds the `authentik-forward-auth` Traefik middleware
3. Unauthenticated users get redirected to the Authentik login page
4. After login, these headers are forwarded to the service:
   - `X-authentik-username`
   - `X-authentik-uid`
   - `X-authentik-email`
   - `X-authentik-name`
   - `X-authentik-groups`

## Gotchas

1. **API pagination**: All list endpoints return paginated results. Use `?page_size=50` or check `pagination.next` for more pages.
2. **Group user updates**: PATCH to groups replaces the entire user list — always fetch current users first, then append.
3. **Provider property mappings**: Must reference existing scope mapping UUIDs. Query `propertymappings/provider/scope/` to find them.
4. **Signing key for OIDC**: Must assign a signing key to OAuth2 providers or JWKS endpoint returns empty `{}`.
5. **Email verified claim**: Default email scope mapping sets `email_verified: False`. For Kubernetes OIDC, create a custom mapping that returns `True`.
6. **Token identifier uniqueness**: Token identifiers must be unique across the entire instance.

## Notes
- Authentik is classified as DEFCON Level 1 (Critical) — handle with care
- Changes to Authentik configuration (Helm chart, PgBouncer, etc.) must go through Terraform
- API-level changes (users, groups, applications) are fine to make directly via the API
- The embedded outpost auto-discovers providers assigned to it
- See also: `ingress-factory-migration` skill for protecting services
