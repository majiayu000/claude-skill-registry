---
name: openmetadata-ops
description: Administer OpenMetadata platform including users, teams, bots, roles, policies, and security. Use when managing access control, configuring SSO, creating service accounts, setting up team hierarchies, or troubleshooting authentication issues.
---

# OpenMetadata Operations

Guide for administering OpenMetadata platform: users, teams, bots, roles, policies, security configuration, and operational tasks.

## When to Use This Skill

- Managing users and team hierarchies
- Creating and configuring bots (service accounts)
- Setting up roles and policies (RBAC/ABAC)
- Configuring SSO and authentication providers
- Managing JWT tokens and API access
- Troubleshooting authentication and authorization issues

## This Skill Does NOT Cover

- Building OpenMetadata SDKs (see `openmetadata-sdk-dev`)
- Using SDKs/APIs to build integrations (see `openmetadata-dev`)
- Deploying OpenMetadata infrastructure (Kubernetes, Docker)
- Database administration for OpenMetadata backend

---

## Team Hierarchy

### Team Types

OpenMetadata uses a hierarchical team structure:

```
Organization (root)
├── Business Unit
│   ├── Division
│   │   ├── Department
│   │   │   └── Group ← Only Groups can own Data Assets
│   │   └── Group
│   └── Department
│       └── Group
└── Business Unit
    └── Group
```

| Level | Purpose | Can Own Assets |
|-------|---------|----------------|
| **Organization** | Company root, auto-created | No |
| **Business Unit** | Top-tier organizational unit | No |
| **Division** | Mid-tier under Business Unit | No |
| **Department** | Team under Division | No |
| **Group** | Lowest level, contains users | **Yes** |

### Create Team

**Via UI:**
1. Navigate to **Settings → Teams**
2. Click **Add Team**
3. Select team type (BusinessUnit, Division, Department, Group)
4. Set parent team
5. Add team name, display name, description

**Via API:**
```bash
curl -X PUT "http://localhost:8585/api/v1/teams" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-engineering",
    "displayName": "Data Engineering",
    "description": "Data platform team",
    "teamType": "Group",
    "parents": [{"id": "parent-team-uuid", "type": "team"}]
  }'
```

### Team Policies

Assign policies to teams for inherited permissions:

```bash
curl -X PATCH "http://localhost:8585/api/v1/teams/${TEAM_ID}" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json-patch+json" \
  -d '[
    {
      "op": "add",
      "path": "/policies/-",
      "value": {"id": "policy-uuid", "type": "policy"}
    }
  ]'
```

---

## User Management

### Add User

**Via UI:**
1. Navigate to **Settings → Users**
2. Click **Add User**
3. Enter email, name, select teams
4. Assign roles

**Via API:**
```bash
curl -X PUT "http://localhost:8585/api/v1/users" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john.doe",
    "email": "john.doe@company.com",
    "displayName": "John Doe",
    "teams": [{"id": "team-uuid", "type": "team"}],
    "roles": [{"id": "role-uuid", "type": "role"}]
  }'
```

### Assign Role to User

```bash
curl -X PATCH "http://localhost:8585/api/v1/users/${USER_ID}" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json-patch+json" \
  -d '[
    {
      "op": "add",
      "path": "/roles/-",
      "value": {"id": "data-steward-role-uuid", "type": "role"}
    }
  ]'
```

### Generate User Access Token

Users can generate personal access tokens:

1. Go to **Profile → Access Token**
2. Click **Generate New Token**
3. Set expiration (optional)
4. Copy token immediately (shown only once)

---

## Bots (Service Accounts)

### What Are Bots?

Bots are service accounts for automated processes:
- Ingestion pipelines
- External integrations
- Scheduled jobs
- CI/CD automation

### Built-in Bots

| Bot | Purpose | Default Role |
|-----|---------|--------------|
| `ingestion-bot` | Metadata ingestion pipelines | Ingestion Bot Role |
| `automator-bot` | Automation workflows | Automator Role |

### Create Custom Bot

**Via UI:**
1. Navigate to **Settings → Integrations → Bots**
2. Click **Add Bot**
3. Enter bot name and description
4. Select or create role
5. Copy generated JWT token

**Via API:**
```bash
# Create bot
curl -X PUT "http://localhost:8585/api/v1/bots" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ci-cd-bot",
    "displayName": "CI/CD Bot",
    "description": "Bot for CI/CD pipeline metadata updates",
    "botUser": {
      "name": "ci-cd-bot",
      "email": "ci-cd-bot@openmetadata.org",
      "isBot": true
    }
  }'
```

### Get Bot JWT Token

**Via UI:**
1. Navigate to **Settings → Integrations → Bots**
2. Select the bot
3. Click **Revoke & Regenerate Token** or view existing token

**Via API:**
```bash
# Get bot details including auth mechanism
curl "http://localhost:8585/api/v1/bots/name/ingestion-bot?fields=botUser" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"
```

### Bot Token Validation

Validate bot tokens at [jwt.io](https://jwt.io) or programmatically:

```python
import jwt

def validate_bot_token(token: str, public_key: str) -> dict:
    """Validate and decode bot JWT token."""
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer="open-metadata.org",
        )
        assert payload.get("isBot") == True
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired - regenerate in UI")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")
```

### Bot Token Rotation

Rotate bot tokens periodically:

1. Navigate to **Settings → Integrations → Bots**
2. Select the bot
3. Click **Revoke & Regenerate Token**
4. Update all systems using the old token
5. Verify ingestion pipelines are working

---

## Roles and Policies

### Access Control Model

OpenMetadata uses hybrid RBAC + ABAC:

```
Authorization Decision = f(User, Resource, Operation)

Where:
- User    = Identity + Roles + Teams
- Resource = Entity Type + Attributes (owner, domain, tags)
- Operation = Create, Edit, Delete, ViewAll, EditOwner, etc.
```

### Built-in Roles

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| **Admin** | Full platform access | All operations on all resources |
| **Data Consumer** | Read-only access | ViewBasic on most entities |
| **Data Steward** | Governance operations | Edit descriptions, tags, glossary |
| **Ingestion Bot Role** | Pipeline operations | Create/edit services and entities |

### Create Custom Role

**Via UI:**
1. Navigate to **Settings → Roles**
2. Click **Add Role**
3. Enter name and description
4. Add policies to the role

**Via API:**
```bash
curl -X PUT "http://localhost:8585/api/v1/roles" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DataEngineer",
    "displayName": "Data Engineer",
    "description": "Role for data engineering team",
    "policies": [
      {"id": "policy-uuid-1", "type": "policy"},
      {"id": "policy-uuid-2", "type": "policy"}
    ]
  }'
```

### Policy Structure

Policies contain rules that define permissions:

```json
{
  "name": "TableEditPolicy",
  "rules": [
    {
      "name": "AllowEditTables",
      "resources": ["table"],
      "operations": ["Create", "Edit", "Delete"],
      "effect": "allow",
      "condition": "isOwner()"
    }
  ]
}
```

### Common Policy Rules

| Rule | Effect | Description |
|------|--------|-------------|
| `isOwner()` | Condition | User/team owns the resource |
| `inTeam('team-name')` | Condition | User belongs to team |
| `hasDomain('domain')` | Condition | Resource is in domain |
| `hasTag('tag-fqn')` | Condition | Resource has specific tag |

### Create Policy

```bash
curl -X PUT "http://localhost:8585/api/v1/policies" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TeamOwnershipPolicy",
    "displayName": "Team Ownership Policy",
    "description": "Allow team members to edit owned resources",
    "rules": [
      {
        "name": "EditOwnedResources",
        "resources": ["table", "dashboard", "pipeline"],
        "operations": ["Edit", "EditDescription", "EditTags"],
        "effect": "allow",
        "condition": "isOwner()"
      }
    ]
  }'
```

### Operations Reference

| Operation | Description |
|-----------|-------------|
| `Create` | Create new entities |
| `Delete` | Delete entities |
| `ViewAll` | View all entity fields including sensitive data |
| `ViewBasic` | View basic fields (name, description, tags) |
| `Edit` | Edit entity properties |
| `EditDescription` | Edit description only |
| `EditTags` | Edit tags and classifications |
| `EditOwner` | Change entity owner |
| `EditLineage` | Modify lineage edges |
| `EditCustomFields` | Modify custom properties |

---

## Authentication Configuration

### Supported Providers

| Provider | Type | Notes |
|----------|------|-------|
| OpenMetadata (built-in) | JWT | Development only |
| Google | OIDC | Google Workspace SSO |
| Okta | OIDC | Okta SSO |
| Azure AD | OIDC | Microsoft Entra ID |
| Auth0 | OIDC | Auth0 SSO |
| AWS Cognito | OIDC | AWS Cognito User Pools |
| OneLogin | OIDC | OneLogin SSO |
| Keycloak | OIDC | Self-hosted OIDC |
| Custom OIDC | OIDC | Any OIDC-compliant provider |

> **Note**: OpenMetadata does not support multiple auth providers simultaneously.

### Configure SSO (Example: Okta)

**1. Create Okta Application:**
- Sign in to Okta Admin Console
- Navigate to **Applications → Create App Integration**
- Select **OIDC - OpenID Connect** and **Web Application**
- Set redirect URI: `http://localhost:8585/callback`

**2. Configure OpenMetadata:**

```yaml
# openmetadata.yaml
authenticationConfiguration:
  provider: okta
  publicKeyUrls:
    - https://your-domain.okta.com/oauth2/default/v1/keys
  authority: https://your-domain.okta.com/oauth2/default
  clientId: <your-client-id>
  callbackUrl: http://localhost:8585/callback
```

**3. Configure Frontend:**

```yaml
# openmetadata.yaml (continued)
authorizerConfiguration:
  className: org.openmetadata.service.security.DefaultAuthorizer
  containerRequestFilter: org.openmetadata.service.security.JwtFilter
  adminPrincipals:
    - admin@company.com
  principalDomain: company.com
```

### LDAP/Active Directory

For LDAP integration, use an OIDC proxy like Keycloak:

1. Deploy Keycloak
2. Configure LDAP User Federation in Keycloak
3. Configure OpenMetadata to use Keycloak as OIDC provider

---

## Custom Properties Administration

### Create Custom Property Type

**Via UI:**
1. Navigate to **Settings → Custom Properties**
2. Select entity type (Table, Dashboard, etc.)
3. Click **Add Property**
4. Configure name, type, description

**Via API:**
```bash
curl -X PUT "http://localhost:8585/api/v1/metadata/types/name/table/customProperties" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dataClassification",
    "description": "Data classification level",
    "propertyType": {
      "id": "enum-type-uuid",
      "type": "type"
    },
    "customPropertyConfig": {
      "config": {
        "values": ["Public", "Internal", "Confidential", "Restricted"]
      }
    }
  }'
```

### List Custom Properties

```bash
curl "http://localhost:8585/api/v1/metadata/types/name/table?fields=customProperties" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"
```

---

## Troubleshooting

### Authentication Issues

**Problem: 401 Unauthorized**

1. Check JWT token validity:
   ```bash
   # Decode token at jwt.io or:
   echo $JWT_TOKEN | cut -d. -f2 | base64 -d | jq .
   ```

2. Verify token expiration (`exp` claim)

3. Check issuer matches configuration

**Problem: Bot ingestion failing**

1. Verify bot has `Ingestion Bot Role`:
   ```bash
   curl "http://localhost:8585/api/v1/bots/name/ingestion-bot?fields=botUser" \
     -H "Authorization: Bearer ${ADMIN_TOKEN}"
   ```

2. Check role policies weren't modified

3. Regenerate bot token if expired

### Authorization Issues

**Problem: 403 Forbidden**

1. Check user's roles:
   ```bash
   curl "http://localhost:8585/api/v1/users/name/john.doe?fields=roles,teams" \
     -H "Authorization: Bearer ${ADMIN_TOKEN}"
   ```

2. Verify role has required policy

3. Check policy conditions (isOwner, inTeam, etc.)

**Problem: User can't see entities**

1. Verify `ViewBasic` or `ViewAll` permission
2. Check team hierarchy - user must be in a Group
3. Verify entity isn't soft-deleted

### Common Fixes

| Issue | Solution |
|-------|----------|
| Token expired | Regenerate token in UI |
| Missing permissions | Add policy to role |
| User not in team | Add user to Group-type team |
| Bot not working | Check role assignment, regenerate token |
| SSO login failing | Verify redirect URI, check OIDC config |

---

## Operational Tasks

### Backup Considerations

Critical data to back up:
- Database (MySQL/PostgreSQL)
- Elasticsearch indices
- JWT signing keys
- Configuration files

### Audit Logging

OpenMetadata tracks changes via:
- Entity version history
- Change events in Elasticsearch
- API audit logs

Query audit events:
```bash
curl "http://localhost:8585/api/v1/events?entityType=table&timestamp=1704067200000" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"
```

### Health Checks

```bash
# API health
curl "http://localhost:8585/api/v1/system/health"

# Elasticsearch health
curl "http://localhost:8585/api/v1/search/health"
```

---

## Best Practices

### Security

1. **Never use built-in auth in production** - always configure SSO
2. **Rotate bot tokens** periodically (every 90 days recommended)
3. **Use least-privilege roles** - create specific policies per team
4. **Audit admin access** regularly

### Team Structure

1. **Use Groups for ownership** - only Groups can own assets
2. **Mirror org structure** - Business Unit → Division → Department → Group
3. **Assign domain owners** - use domains for cross-team governance

### Bot Management

1. **Create purpose-specific bots** - don't reuse ingestion-bot
2. **Document bot purposes** in descriptions
3. **Monitor bot token usage** in audit logs
4. **Disable unused bots** rather than deleting

---

## References

- [OpenMetadata Security Guide](https://docs.open-metadata.org/latest/deployment/security)
- [Roles and Policies](https://docs.open-metadata.org/latest/how-to-guides/admin-guide-roles-policies)
- [Team Management](https://docs.open-metadata.org/latest/how-to-guides/admin-guide/teams-and-users)
- [SSO Configuration](https://docs.open-metadata.org/latest/deployment/security)
- `openmetadata-dev` - Using SDKs/APIs for integrations
- `openmetadata-sdk-dev` - Implementing SDKs for new languages
