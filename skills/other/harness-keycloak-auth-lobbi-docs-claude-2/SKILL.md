---
name: harness-keycloak-auth
description: Keycloak OIDC integration with Harness pipelines, EKS IRSA, service account authentication, and realm-as-code patterns
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
dependencies:
  - harness-eks-deployments
triggers:
  - keycloak
  - oidc
  - authentication
  - oauth
  - realm
  - client
  - keycloak eks
  - keycloak harness
---

# Harness Keycloak Auth Skill

Integrate Keycloak OIDC with Harness pipelines and EKS deployments.

## Use For
- Keycloak client management in pipelines, OIDC for EKS authentication
- Realm-as-code patterns, service account provisioning

## Keycloak Helm Values for EKS

```yaml
# charts/keycloak/values.yaml
keycloak:
  replicas: 2

  image:
    repository: quay.io/keycloak/keycloak
    tag: "24.0.1"

  command:
    - "/opt/keycloak/bin/kc.sh"
    - "start"
    - "--optimized"

  extraEnv: |
    - name: KC_HOSTNAME
      value: "keycloak.{{ .Values.global.domain }}"
    - name: KC_PROXY
      value: "edge"
    - name: KC_DB
      value: "postgres"
    - name: KC_DB_URL
      valueFrom:
        secretKeyRef:
          name: keycloak-db
          key: url
    - name: KC_DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: keycloak-db
          key: username
    - name: KC_DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: keycloak-db
          key: password
    - name: KEYCLOAK_ADMIN
      valueFrom:
        secretKeyRef:
          name: keycloak-admin
          key: username
    - name: KEYCLOAK_ADMIN_PASSWORD
      valueFrom:
        secretKeyRef:
          name: keycloak-admin
          key: password

  ingress:
    enabled: true
    ingressClassName: nginx
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
    rules:
      - host: keycloak.{{ .Values.global.domain }}
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: keycloak-tls
        hosts:
          - keycloak.{{ .Values.global.domain }}

  serviceAccount:
    create: true
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::{{ .Values.aws.accountId }}:role/keycloak-role
```

## Realm-as-Code Configuration

### Realm Export Template
```json
{
  "realm": "{{ .Values.keycloak.realm }}",
  "enabled": true,
  "sslRequired": "external",
  "registrationAllowed": false,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "resetPasswordAllowed": true,
  "editUsernameAllowed": false,
  "bruteForceProtected": true,
  "permanentLockout": false,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "waitIncrementSeconds": 60,
  "quickLoginCheckMilliSeconds": 1000,
  "maxDeltaTimeSeconds": 43200,
  "failureFactor": 5,
  "roles": {
    "realm": [
      { "name": "admin", "description": "Administrator" },
      { "name": "user", "description": "Standard user" }
    ]
  },
  "clients": [],
  "users": [],
  "browserSecurityHeaders": {
    "contentSecurityPolicyReportOnly": "",
    "xContentTypeOptions": "nosniff",
    "xRobotsTag": "none",
    "xFrameOptions": "SAMEORIGIN",
    "contentSecurityPolicy": "frame-src 'self'; frame-ancestors 'self'; object-src 'none';",
    "xXSSProtection": "1; mode=block",
    "strictTransportSecurity": "max-age=31536000; includeSubDomains"
  }
}
```

### Client Configuration Template
```json
{
  "clientId": "{{ .Values.service.name }}-client",
  "name": "{{ .Values.service.name }} Service",
  "enabled": true,
  "clientAuthenticatorType": "client-secret",
  "secret": "{{ .Values.keycloak.clientSecret }}",
  "redirectUris": [
    "https://{{ .Values.service.name }}.{{ .Values.global.domain }}/*"
  ],
  "webOrigins": [
    "https://{{ .Values.service.name }}.{{ .Values.global.domain }}"
  ],
  "standardFlowEnabled": true,
  "implicitFlowEnabled": false,
  "directAccessGrantsEnabled": true,
  "serviceAccountsEnabled": true,
  "publicClient": false,
  "protocol": "openid-connect",
  "attributes": {
    "pkce.code.challenge.method": "S256",
    "access.token.lifespan": "300",
    "client.session.idle.timeout": "1800"
  },
  "defaultClientScopes": [
    "web-origins",
    "profile",
    "roles",
    "email"
  ],
  "optionalClientScopes": [
    "address",
    "phone",
    "offline_access"
  ]
}
```

## Harness Pipeline Steps for Keycloak

### Create/Update Keycloak Client
```yaml
- step:
    type: Run
    name: Configure Keycloak Client
    identifier: configure_keycloak
    spec:
      shell: Bash
      command: |
        # Get admin token
        TOKEN=$(curl -s -X POST \
          "${KEYCLOAK_URL}/realms/master/protocol/openid-connect/token" \
          -H "Content-Type: application/x-www-form-urlencoded" \
          -d "username=${KEYCLOAK_ADMIN}" \
          -d "password=${KEYCLOAK_ADMIN_PASSWORD}" \
          -d "grant_type=password" \
          -d "client_id=admin-cli" | jq -r '.access_token')

        # Check if client exists
        CLIENT_ID="<+service.name>-client"
        EXISTING=$(curl -s -X GET \
          "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/clients?clientId=${CLIENT_ID}" \
          -H "Authorization: Bearer ${TOKEN}" | jq -r '.[0].id // empty')

        # Prepare client config
        cat > /tmp/client.json << 'EOF'
        {
          "clientId": "<+service.name>-client",
          "name": "<+service.name>",
          "enabled": true,
          "clientAuthenticatorType": "client-secret",
          "redirectUris": ["https://<+service.name>.<+pipeline.variables.domain>/*"],
          "webOrigins": ["https://<+service.name>.<+pipeline.variables.domain>"],
          "standardFlowEnabled": true,
          "serviceAccountsEnabled": true,
          "publicClient": false,
          "protocol": "openid-connect"
        }
        EOF

        if [ -n "$EXISTING" ]; then
          # Update existing client
          curl -s -X PUT \
            "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/clients/${EXISTING}" \
            -H "Authorization: Bearer ${TOKEN}" \
            -H "Content-Type: application/json" \
            -d @/tmp/client.json
          echo "Updated client: ${CLIENT_ID}"
        else
          # Create new client
          curl -s -X POST \
            "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/clients" \
            -H "Authorization: Bearer ${TOKEN}" \
            -H "Content-Type: application/json" \
            -d @/tmp/client.json
          echo "Created client: ${CLIENT_ID}"
        fi

        # Get client secret
        CLIENT_UUID=$(curl -s -X GET \
          "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/clients?clientId=${CLIENT_ID}" \
          -H "Authorization: Bearer ${TOKEN}" | jq -r '.[0].id')

        SECRET=$(curl -s -X GET \
          "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/clients/${CLIENT_UUID}/client-secret" \
          -H "Authorization: Bearer ${TOKEN}" | jq -r '.value')

        # Store in AWS Secrets Manager
        aws secretsmanager put-secret-value \
          --secret-id "<+service.name>/keycloak-client-secret" \
          --secret-string "${SECRET}"
      envVariables:
        KEYCLOAK_URL: <+pipeline.variables.keycloak_url>
        KEYCLOAK_REALM: <+pipeline.variables.keycloak_realm>
        KEYCLOAK_ADMIN: <+secrets.getValue("keycloak_admin_user")>
        KEYCLOAK_ADMIN_PASSWORD: <+secrets.getValue("keycloak_admin_password")>
```

### Realm Import Step
```yaml
- step:
    type: Run
    name: Import Keycloak Realm
    identifier: import_realm
    spec:
      shell: Bash
      command: |
        # Get admin token
        TOKEN=$(curl -s -X POST \
          "${KEYCLOAK_URL}/realms/master/protocol/openid-connect/token" \
          -H "Content-Type: application/x-www-form-urlencoded" \
          -d "username=${KEYCLOAK_ADMIN}" \
          -d "password=${KEYCLOAK_ADMIN_PASSWORD}" \
          -d "grant_type=password" \
          -d "client_id=admin-cli" | jq -r '.access_token')

        # Import realm from repo
        curl -s -X POST \
          "${KEYCLOAK_URL}/admin/realms" \
          -H "Authorization: Bearer ${TOKEN}" \
          -H "Content-Type: application/json" \
          -d @keycloak/realm-export.json

        echo "Realm imported successfully"
```

## EKS OIDC Integration with Keycloak

### IRSA for Keycloak-Authenticated Pods
```yaml
# ServiceAccount with Keycloak token injection
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ .Values.service.name }}
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::{{ .Values.aws.accountId }}:role/{{ .Values.service.name }}-role
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.service.name }}
spec:
  template:
    spec:
      serviceAccountName: {{ .Values.service.name }}
      containers:
        - name: app
          env:
            - name: KEYCLOAK_URL
              value: "https://keycloak.{{ .Values.global.domain }}"
            - name: KEYCLOAK_REALM
              value: "{{ .Values.keycloak.realm }}"
            - name: KEYCLOAK_CLIENT_ID
              value: "{{ .Values.service.name }}-client"
            - name: KEYCLOAK_CLIENT_SECRET
              valueFrom:
                secretKeyRef:
                  name: {{ .Values.service.name }}-keycloak
                  key: client-secret
```

### External Secrets for Keycloak Credentials
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ .Values.service.name }}-keycloak
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: {{ .Values.service.name }}-keycloak
    creationPolicy: Owner
  data:
    - secretKey: client-secret
      remoteRef:
        key: {{ .Values.service.name }}/keycloak-client-secret
```

## Helm Values for Keycloak-Enabled Service

```yaml
# values.yaml for a service with Keycloak auth
service:
  name: api-gateway

keycloak:
  enabled: true
  realm: production
  clientId: api-gateway-client
  # Client secret fetched from AWS Secrets Manager
  clientSecretRef:
    name: api-gateway-keycloak
    key: client-secret

  # OIDC configuration
  oidc:
    issuerUri: https://keycloak.example.com/realms/production
    jwksUri: https://keycloak.example.com/realms/production/protocol/openid-connect/certs
    tokenEndpoint: https://keycloak.example.com/realms/production/protocol/openid-connect/token
    authorizationEndpoint: https://keycloak.example.com/realms/production/protocol/openid-connect/auth
    userInfoEndpoint: https://keycloak.example.com/realms/production/protocol/openid-connect/userinfo

  # Role mappings
  roles:
    admin: ROLE_ADMIN
    user: ROLE_USER
```

## Pipeline Variables for Keycloak

```yaml
pipeline:
  variables:
    - name: keycloak_url
      type: String
      default: "https://keycloak.example.com"
      description: "Keycloak server URL"
    - name: keycloak_realm
      type: String
      default: "production"
      description: "Keycloak realm name"
    - name: domain
      type: String
      default: "example.com"
      description: "Base domain for services"
```

## Verification Steps

```yaml
- step:
    type: Run
    name: Verify Keycloak Integration
    identifier: verify_keycloak
    spec:
      shell: Bash
      command: |
        # Test token endpoint
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
          "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/.well-known/openid-configuration")

        if [ "$RESPONSE" != "200" ]; then
          echo "Keycloak realm not accessible"
          exit 1
        fi

        # Test client authentication
        TOKEN_RESPONSE=$(curl -s -X POST \
          "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" \
          -H "Content-Type: application/x-www-form-urlencoded" \
          -d "client_id=${CLIENT_ID}" \
          -d "client_secret=${CLIENT_SECRET}" \
          -d "grant_type=client_credentials")

        if echo "$TOKEN_RESPONSE" | jq -e '.access_token' > /dev/null; then
          echo "Keycloak client authentication successful"
        else
          echo "Keycloak client authentication failed"
          exit 1
        fi
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Token endpoint unreachable | Check Keycloak ingress, verify realm exists |
| Invalid client credentials | Regenerate client secret, update secrets |
| CORS errors | Configure web origins in client settings |
| Token validation failed | Check JWKS endpoint, verify issuer URI |
| Realm import failed | Validate JSON syntax, check for conflicts |

## References
- [Keycloak Admin REST API](https://www.keycloak.org/docs-api/latest/rest-api/)
- [EKS OIDC Provider](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)
