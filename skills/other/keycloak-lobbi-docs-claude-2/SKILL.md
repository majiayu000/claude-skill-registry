---
name: keycloak
description: Keycloak identity and access management including realms, clients, authentication flows, themes, and user federation. Activate for OAuth2, OIDC, SAML, SSO, identity providers, and authentication configuration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
---

# Keycloak Skill

Provides comprehensive Keycloak identity and access management capabilities for the Alpha Members Platform.

## When to Use This Skill

Activate this skill when working with:
- Keycloak realm configuration
- Client setup and management
- Authentication flows (MFA, OTP, WebAuthn)
- User federation (LDAP, Active Directory)
- Identity providers (SAML, OIDC, social login)
- Theme customization
- Role-based access control

## Quick Reference

### Common Commands
```bash
# Start Keycloak in dev mode
docker-compose up keycloak keycloak-db -d

# Export realm configuration
docker exec keycloak /opt/keycloak/bin/kc.sh export \
  --realm alpha-members \
  --dir /tmp/export \
  --users realm_file

# Import realm
docker exec keycloak /opt/keycloak/bin/kc.sh import \
  --dir /opt/keycloak/data/import

# Get admin token
curl -X POST "http://localhost:8080/realms/master/protocol/openid-connect/token" \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password"

# Health check
curl http://localhost:8080/health/ready
```

### Admin REST API
```bash
# Base URL
KEYCLOAK_URL="http://localhost:8080"
REALM="alpha-members"

# List users
curl -H "Authorization: Bearer $TOKEN" \
  "$KEYCLOAK_URL/admin/realms/$REALM/users"

# Create client
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "$KEYCLOAK_URL/admin/realms/$REALM/clients" \
  -d '{"clientId": "new-client", "enabled": true}'

# Get realm roles
curl -H "Authorization: Bearer $TOKEN" \
  "$KEYCLOAK_URL/admin/realms/$REALM/roles"
```

## Realm Configuration

### alpha-members Realm
```json
{
  "realm": "alpha-members",
  "enabled": true,
  "sslRequired": "external",
  "registrationAllowed": true,
  "registrationEmailAsUsername": true,
  "verifyEmail": true,
  "bruteForceProtected": true,
  "failureFactor": 5,
  "maxFailureWaitSeconds": 900
}
```

### Default Roles
- **admin** - Full administrative access
- **member** - Standard member access
- **guest** - Limited guest access

### Client Roles (member-api)
- members:read
- members:write
- members:delete
- members:admin

## Authentication Flows

### Browser Flow (Default)
1. Cookie (ALTERNATIVE)
2. Identity Provider Redirector (ALTERNATIVE)
3. Forms:
   - Username/Password (REQUIRED)
   - Conditional OTP (CONDITIONAL)

### Custom MFA Flow
```yaml
alpha-mfa-flow:
  - Username Password Form (REQUIRED)
  - Conditional OTP:
    - Condition: User Role (admin)
    - OTP Form (REQUIRED)
```

## Client Configuration

### member-api (Backend Service)
```json
{
  "clientId": "member-api",
  "enabled": true,
  "clientAuthenticatorType": "client-secret",
  "serviceAccountsEnabled": true,
  "directAccessGrantsEnabled": true,
  "publicClient": false,
  "protocol": "openid-connect"
}
```

### member-ui (Frontend SPA)
```json
{
  "clientId": "member-ui",
  "enabled": true,
  "publicClient": true,
  "standardFlowEnabled": true,
  "implicitFlowEnabled": false,
  "directAccessGrantsEnabled": false,
  "redirectUris": ["http://localhost:3000/*"],
  "webOrigins": ["+"],
  "protocol": "openid-connect",
  "attributes": {
    "pkce.code.challenge.method": "S256"
  }
}
```

## Token Configuration

```yaml
Access Token Lifespan: 1 hour (3600s)
Implicit Flow Lifespan: 15 minutes (900s)
SSO Session Idle: 30 minutes (1800s)
SSO Session Max: 10 hours (36000s)
Offline Session Idle: 30 days (2592000s)
```

## OIDC Endpoints

```yaml
Authorization: /realms/alpha-members/protocol/openid-connect/auth
Token: /realms/alpha-members/protocol/openid-connect/token
UserInfo: /realms/alpha-members/protocol/openid-connect/userinfo
Logout: /realms/alpha-members/protocol/openid-connect/logout
JWKS: /realms/alpha-members/protocol/openid-connect/certs
Discovery: /realms/alpha-members/.well-known/openid-configuration
```

## Theme Customization

### Theme Structure
```
keycloak/themes/alpha/
├── theme.properties
├── login/
│   ├── theme.properties
│   ├── resources/css/login.css
│   └── messages/messages_en.properties
├── account/
└── email/
```

### Theme Properties
```properties
parent=keycloak
import=common/keycloak
styles=css/login.css
locales=en
```

## User Federation

### LDAP Configuration
```yaml
Vendor: Active Directory
Connection URL: ldaps://ldap.corporate.com:636
Users DN: OU=Users,DC=corporate,DC=com
Username Attribute: sAMAccountName
Edit Mode: READ_ONLY
Sync Mode: IMPORT
```

## Security Best Practices

1. **Enable brute force protection**
2. **Require email verification**
3. **Use SSL/TLS in production** (sslRequired: all)
4. **Configure proper token lifetimes**
5. **Enable audit logging**
6. **Use PKCE for public clients**
7. **Implement MFA for admin roles**

## Project Files

- Realm Config: `keycloak/realm-config/alpha-realm.json`
- Docker: `docker/docker-compose.yml` (keycloak service)
- Themes: `keycloak/themes/alpha/`

## Related Agents

- **keycloak-realm-admin** - Realm and client management
- **keycloak-theme-developer** - Theme customization
- **keycloak-identity-specialist** - Federation and SSO
- **keycloak-auth-flow-designer** - Authentication flows
- **keycloak-security-auditor** - Security review

## Troubleshooting

```bash
# Check Keycloak logs
docker logs keycloak -f --tail=100

# Test OIDC configuration
curl http://localhost:8080/realms/alpha-members/.well-known/openid-configuration

# Validate token
curl -X POST "http://localhost:8080/realms/alpha-members/protocol/openid-connect/token/introspect" \
  -d "client_id=member-api" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "token=$ACCESS_TOKEN"
```
