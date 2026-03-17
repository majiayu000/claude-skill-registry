---
name: keycloak-expert
description: "This skill should be used when the user asks to 'configure Keycloak', 'set up ABAC', 'create Keycloak realm', 'integrate Azure AD with Keycloak', 'implement authorization services', 'configure OIDC client', 'create Keycloak policies', 'set up UMA/RPT tokens', 'deploy Keycloak on OpenShift', 'integrate Spring Security with Keycloak', 'configure NextAuth.js with Keycloak', 'create protocol mappers', 'map Azure groups to roles', or needs guidance on Keycloak realm/client configuration, ABAC policies and permissions, identity provider federation, or Configuration as Code patterns."
---

# Keycloak Expert Skill

Expert guidance for Keycloak identity and access management with deep focus on ABAC implementation.

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [ABAC Implementation](#abac-implementation)
3. [Configuration as Code](#configuration-as-code)
4. [Integration Patterns](#integration-patterns)
5. [Security](#security)
6. [OpenShift Deployment](#openshift-deployment)

## Core Concepts

### Realm Architecture
- **Realm**: Isolated tenant with own users, roles, clients, and identity providers
- **Client**: Application registered for authentication (public, confidential, bearer-only)
- **Roles**: Realm-level or client-scoped permissions
- **Groups**: Organizational units for role assignment
- **Identity Provider**: External authentication source (Azure AD, Google, SAML)

### Token Types
- **ID Token**: User identity for frontends (short-lived)
- **Access Token**: API authorization (5-30 min)
- **Refresh Token**: Obtain new tokens without re-login (hours-days)
- **RPT (Requesting Party Token)**: ABAC authorization response containing permissions

## ABAC Implementation

ABAC moves authorization logic from application code to Keycloak's centralized policy engine.

### ABAC Building Blocks
```
Resources → What is protected (API endpoints, data, features)
Scopes → Actions on resources (view, edit, delete, admin)
Policies → Rules for access (role-based, time-based, JS-based, aggregate)
Permissions → Connect policies to resources/scopes
```

### Resource Definition
```java
// Protected resource representing an API endpoint or feature
.createResource("user-profiles")
    .withDisplayName("User Profile Data")
    .withType("urn:app:resources:profile")
    .withUris("/api/users/profile/*")
    .withScopes("view", "edit", "delete")
    .and()
```

### Policy Types
1. **Role Policy**: Access based on realm/client roles
2. **Group Policy**: Access based on group membership
3. **User Policy**: Access for specific users
4. **Time Policy**: Time-window restrictions
5. **JavaScript Policy**: Custom logic with `$evaluation` context
6. **Aggregate Policy**: Combine multiple policies with decision strategy

### Permission Creation
```java
.createPermission("admin-profile-management")
    .onResource("user-profiles")
    .withScopes("edit", "delete")
    .withPolicies("admin-role-policy", "business-hours-policy")
    .withDecisionStrategy(DecisionStrategy.UNANIMOUS)
    .and()
```

### UMA Token Exchange (RPT Flow)
Backend validates permissions by exchanging access token for RPT:
```bash
curl -X POST "${KEYCLOAK_URL}/realms/${REALM}/protocol/openid-connect/token" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:uma-ticket" \
  -d "audience=${CLIENT_ID}" \
  -d "permission=${RESOURCE}#${SCOPE}"
```

**Response Codes:**
- `200 + access_token`: Permission granted
- `403`: Permission denied by policy
- `400`: Invalid request or resource

## Configuration as Code

For detailed fluent builder patterns, see: **[references/fluent-builders.md](references/fluent-builders.md)**

### Key Builders
- `FluentRealmBuilder`: Realm settings, token lifespans, security
- `FluentClientBuilder`: OAuth clients, redirect URIs, flows
- `FluentRoleBuilder`: Roles, composites, default roles
- `FluentAzureIdpBuilder`: Azure AD federation with group mapping
- `FluentAbacBuilder`: Complete ABAC configuration

### Example: Complete Realm Setup
```java
// 1. Create realm
FluentRealmBuilder.create()
    .with(keycloakClient)
    .createRealm("toolbox")
    .accessTokenLifespan(1200)  // 20 min
    .ssoSessionIdleTimeout(1800)
    .bruteForceProtected(true)
    .and().apply();

// 2. Configure roles
FluentRoleBuilder.forRealm("toolbox")
    .with(keycloakClient)
    .createRole("admin").withDescription("Administrator").and()
    .createCompositeRole("default-roles-toolbox")
        .addRealmRole("offline_access")
        .addClientRole("account", "view-profile")
        .and()
    .setDefaultRole("default-roles-toolbox")
    .apply();

// 3. Configure client with authorization
FluentClientBuilder.forRealm("toolbox")
    .with(keycloakClient)
    .createClient("toolbox-webui")
        .confidentialClient()
        .enableStandardFlow()
        .enableServiceAccounts()
        .enableAuthorizationServices()
        .addRedirectUri("https://app.example.com/callback")
        .and()
    .apply();

// 4. Configure ABAC
FluentAbacBuilder.forClient("toolbox", "toolbox-webui")
    .with(abacConfiguration)
    .enableAuthorization(PolicyEnforcementMode.ENFORCING)
    .createResource("mailtemplate")
        .withType("urn:toolbox:resources:mailtemplate")
        .withScopes("view")
        .and()
    .createPolicy("admin-policy")
        .requireRoles("admin")
        .and()
    .createPermission("view-mailtemplate")
        .onScopes("view")
        .withPolicies("admin-policy")
        .and()
    .apply();
```

## Integration Patterns

For complete integration examples, see: **[references/integrations.md](references/integrations.md)**

### Spring Boot Backend (ABAC)
```java
@AbacPolicy(resource = "mailtemplate", action = "view")
@GetMapping("/mail/templates")
public List<MailTemplate> getMailTemplates() {
    return mailService.getAllTemplates();
}
```

The `@AbacPolicy` annotation triggers AOP-based policy evaluation via UMA:
1. Extract JWT from request
2. Call Keycloak token endpoint with UMA ticket grant
3. If RPT returned → proceed; if 403 → AccessDeniedException

### NextAuth.js Frontend
```typescript
// auth.config.ts
export const authOptions = {
  providers: [
    KeycloakProvider({
      clientId: process.env.AUTH_KEYCLOAK_ID,
      clientSecret: process.env.AUTH_KEYCLOAK_SECRET,
      issuer: process.env.AUTH_KEYCLOAK_ISSUER,
    }),
  ],
  callbacks: {
    jwt: async ({ token, account }) => {
      if (account) {
        token.accessToken = account.access_token;
        token.refreshToken = account.refresh_token;
        token.expiresAt = account.expires_at;
      }
      return token;
    },
  },
};
```

### Azure AD Federation
```java
FluentAzureIdpBuilder.forRealm("toolbox")
    .with(keycloakClient)
    .configureAzureAD(clientId, clientSecret, tenantId)
        .withAlias("azuread")
        .withDisplayName("Azure AD")
        .withDefaultScopes("openid", "profile", "email")
        .trustEmails()
        .and()
    .createMapper("azure-admin-group-mapper")
        .claimToRole()
        .mapClaim("groups")
        .withClaimValue(adminGroupId)
        .toRole("admin")
        .and()
    .apply();
```

## Security

For detailed security guidance, see: **[references/security.md](references/security.md)**

### PKCE (Required for All Clients)
Per OAuth 2.0 Security BCP, enable PKCE even for confidential clients:
```java
.createClient("my-app")
    .confidentialClient()
    .enableStandardFlow()
    .enablePKCE()
    .withPkceMethod("S256")
    .and()
```

### Security Hardening Checklist
- [ ] Admin console on separate hostname with network restrictions
- [ ] TLS enabled, HTTP disabled in production
- [ ] Brute force protection enabled
- [ ] Rate limiting configured (`KC_HTTP_MAX_QUEUED_REQUESTS`)
- [ ] Event logging enabled for auditing
- [ ] Credential rotation procedures documented

### Token Revocation
```java
// Revoke refresh token
String revokeEndpoint = authServerUrl + "/realms/" + realm + "/protocol/openid-connect/revoke";
form.add("token", refreshToken);
form.add("token_type_hint", "refresh_token");
```

### Monitoring
Enable metrics endpoint:
```bash
KC_METRICS_ENABLED=true
KC_HEALTH_ENABLED=true
```

Key alerts: login failures >10/min, token latency p99 >2s, error rate >1%

## OpenShift Deployment

For OpenShift/Kubernetes specifics, see: **[references/deployment.md](references/deployment.md)**

### Red Hat Keycloak Operator (k8s.keycloak.org/v2alpha1)
```yaml
apiVersion: k8s.keycloak.org/v2alpha1
kind: Keycloak
metadata:
  name: keycloak
spec:
  instances: 1
  db:
    vendor: mysql
    host: mysql.mraas.svc.cluster.local
    usernameSecret:
      name: mysql-db-keycloak-secret
      key: username
    passwordSecret:
      name: mysql-db-keycloak-secret
      key: password
  http:
    httpEnabled: true
    tlsSecret: keycloak-tls
  proxy:
    headers: xforwarded
  hostname:
    hostname: https://keycloak.example.com
    admin: https://admin-keycloak.example.com
    strict: false
  image: custom-keycloak-image:tag
  imagePullSecrets:
    - name: registry-pull-secret
  startOptimized: true
  unsupported:
    podTemplate:
      spec:
        containers:
          - name: keycloak
            env:
              - name: CUSTOM_DB_URL
                valueFrom:
                  secretKeyRef:
                    name: custom-db-secret
                    key: url
```

### Key Configuration Points
- `startOptimized: true` for production (uses pre-built image)
- `proxy.headers: xforwarded` for reverse proxy behind ingress
- `hostname.strict: false` allows multiple hostnames
- Environment variables injected via `unsupported.podTemplate`

## Reference Files

- **[references/fluent-builders.md](references/fluent-builders.md)**: Complete fluent builder API documentation
- **[references/integrations.md](references/integrations.md)**: Spring Security, NextAuth.js, and API integration patterns
- **[references/deployment.md](references/deployment.md)**: OpenShift operator, Docker Compose, environment variables
- **[references/abac-patterns.md](references/abac-patterns.md)**: Advanced ABAC patterns, policy strategies, UMA protocol details
- **[references/security.md](references/security.md)**: PKCE, hardening, token revocation, monitoring

## Quick Reference

### Common Environment Variables
| Variable | Description |
|----------|-------------|
| `KEYCLOAK_ADMIN` | Admin username |
| `KEYCLOAK_ADMIN_PASSWORD` | Admin password |
| `KC_DB` | Database type (mysql, postgres) |
| `KC_DB_URL` | JDBC connection string |
| `AZURE_CLIENT_ID` | Azure AD app client ID |
| `AZURE_CLIENT_SECRET` | Azure AD app secret |
| `AZURE_TENANT_ID` | Azure AD tenant |

### Keycloak Admin API Endpoints
| Endpoint | Purpose |
|----------|---------|
| `/admin/realms/{realm}` | Realm management |
| `/admin/realms/{realm}/clients` | Client management |
| `/admin/realms/{realm}/clients/{id}/authz` | Authorization services |
| `/realms/{realm}/protocol/openid-connect/token` | Token endpoint |
| `/realms/{realm}/protocol/openid-connect/certs` | JWKS endpoint |

### Decision Strategies
| Strategy | Behavior |
|----------|----------|
| `UNANIMOUS` | All policies must permit |
| `AFFIRMATIVE` | At least one policy must permit |
| `CONSENSUS` | Majority of policies must permit |
