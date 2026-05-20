---
name: sf-integration
description: |
  Configure Salesforce integrations: Named Credentials, Connected Apps, External
  Services, Platform Events, CDC, and auth flows. Use when setting up integration
  infrastructure, metadata XML, or choosing architecture patterns. Activate on
  .namedCredential-meta.xml, .connectedApp-meta.xml, .platformEvent-meta.xml,
  mentions of "Named Credential", "Connected App", "Platform Event", "CDC",
  "External Service", or "OAuth flow".
license: Apache-2.0
metadata:
  author: clientell
  version: "1.0.0"
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Salesforce Integration Configuration & Architecture

You are a Salesforce integration architect. Configure integration infrastructure -- Named Credentials, Connected Apps, External Services, Platform Events, CDC, and auth flows. Focus on metadata setup, security configuration, and architecture decisions.

> **Scope boundary**: This skill covers integration *configuration and metadata*. For Apex callout code patterns (HttpRequest, @RestResource, SOAP, mocks), see [sf-apex integration patterns](../sf-apex/references/integration-patterns.md).

## 1. Named Credentials

Named Credentials abstract endpoint URLs and authentication from code. Two architectures exist.

### Legacy Named Credentials

Single metadata file combining endpoint + auth. Still supported but limited.

```xml
<!-- MyService.namedCredential-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<NamedCredential xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MyService</fullName>
    <label>My Service</label>
    <endpoint>https://api.example.com</endpoint>
    <principalType>NamedUser</principalType>
    <protocol>Password</protocol>
    <username>api_user</username>
    <!-- Password stored in org, not in metadata file -->
</NamedCredential>
```

Legacy `protocol` values: `Password`, `Oauth`, `Jwt`, `JwtExchange`, `AwsSv4`, `NoAuthentication`.

### Enhanced Named Credentials (Preferred)

Separates concerns into two metadata types:

| Component | Purpose | File suffix |
|-----------|---------|-------------|
| **External Credential** | Auth config (protocol, principal, identity) | `.externalCredential-meta.xml` |
| **Named Credential** | Endpoint URL, references an External Credential | `.namedCredential-meta.xml` |

Enhanced Named Credential referencing an External Credential:

```xml
<!-- MyService.namedCredential-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<NamedCredential xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MyService</fullName>
    <label>My Service</label>
    <endpoint>https://api.example.com</endpoint>
    <externalCredential>MyService_Auth</externalCredential>
    <generateAuthorizationHeader>true</generateAuthorizationHeader>
    <allowMergeFieldsInBody>false</allowMergeFieldsInBody>
    <allowMergeFieldsInHeader>true</allowMergeFieldsInHeader>
</NamedCredential>
```

External Credential with OAuth Client Credentials:

```xml
<!-- MyService_Auth.externalCredential-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<ExternalCredential xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MyService_Auth</fullName>
    <label>My Service Auth</label>
    <authenticationProtocol>Oauth</authenticationProtocol>
    <externalCredentialParameters>
        <parameterName>ClientId</parameterName>
        <parameterType>AuthProviderUrl</parameterType>
        <parameterValue>YOUR_CLIENT_ID</parameterValue>
    </externalCredentialParameters>
    <externalCredentialParameters>
        <parameterName>Scope</parameterName>
        <parameterType>AuthParameter</parameterType>
        <parameterValue>api read</parameterValue>
    </externalCredentialParameters>
    <principals>
        <principalName>MyServicePrincipal</principalName>
        <principalType>NamedPrincipal</principalType>
        <sequenceNumber>1</sequenceNumber>
    </principals>
</ExternalCredential>
```

### Permission Set Mapping for External Credentials

Users access External Credentials through Permission Set mappings. Without this, callouts fail with `NAMED_CREDENTIAL_NOT_FOUND`.

```xml
<!-- In a Permission Set -->
<externalCredentialPrincipalAccesses>
    <enabled>true</enabled>
    <externalCredentialPrincipal>MyService_Auth - MyServicePrincipal</externalCredentialPrincipal>
</externalCredentialPrincipalAccesses>
```

### When to Use Each

| Scenario | Recommendation |
|----------|---------------|
| New integration | Enhanced Named Credential + External Credential |
| Simple, single-user auth | Legacy Named Credential (acceptable) |
| Multiple endpoints, same auth | One External Credential, multiple Named Credentials |
| Per-user OAuth tokens | External Credential with Per-User principal |
| Migration from Remote Site Settings | Move to Named Credentials for auth management |

---

## 2. Connected Apps

Connected Apps define OAuth client configuration for external applications accessing Salesforce, or for Salesforce-to-Salesforce auth.

### Connected App Metadata

```xml
<!-- MyConnectedApp.connectedApp-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<ConnectedApp xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MyConnectedApp</fullName>
    <label>My Connected App</label>
    <contactEmail>admin@example.com</contactEmail>
    <oauthConfig>
        <callbackUrl>https://myapp.example.com/callback</callbackUrl>
        <certificate>MyCertificateName</certificate>
        <consumerKey>WILL_BE_GENERATED</consumerKey>
        <isAdminApproved>true</isAdminApproved>
        <isConsumerSecretOptional>false</isConsumerSecretOptional>
        <scopes>Api</scopes>
        <scopes>RefreshToken</scopes>
        <scopes>OfflineAccess</scopes>
    </oauthConfig>
    <oauthPolicy>
        <ipRelaxation>ENFORCE</ipRelaxation>
        <refreshTokenPolicy>SPECIFIC_LIFETIME</refreshTokenPolicy>
        <refreshTokenValidityPeriod>720</refreshTokenValidityPeriod>
        <refreshTokenValidityUnits>HOURS</refreshTokenValidityUnits>
    </oauthPolicy>
</ConnectedApp>
```

### OAuth Scopes Reference

| Scope value | Meaning |
|-------------|---------|
| `Api` | Access REST/SOAP APIs |
| `Web` | Access via browser (web scope) |
| `Full` | Full access (avoid in production) |
| `RefreshToken` | Enable refresh tokens (offline_access) |
| `OfflineAccess` | Same as RefreshToken |
| `Chatter` | Chatter REST API |
| `CustomPermissions` | Custom permission access |
| `OpenID` | OpenID Connect identity |
| `Profile` | User profile info |
| `Email` | User email |

### JWT Bearer Flow Setup

For server-to-server with no interactive login:

1. Generate X.509 certificate and upload to Connected App
2. Pre-authorize the Connected App for the integration user's profile
3. Set `isAdminApproved` to `true`
4. Consumer sends JWT signed with private key to token endpoint
5. Token endpoint: `https://login.salesforce.com/services/oauth2/token`

Grant type: `urn:ietf:params:oauth:grant-type:jwt-bearer`

### Web Server Flow Setup

For user-facing applications:

1. Configure callback URL (must be HTTPS, exact match)
2. Set appropriate scopes (avoid `Full`)
3. Set IP relaxation policy based on security requirements
4. Configure refresh token lifetime

### IP Relaxation Options

| Value | Behavior |
|-------|----------|
| `ENFORCE` | Enforce IP restrictions from Connected App |
| `BYPASS` | Bypass org IP restrictions |
| `BYPASS_WITH_VALID_BROWSER_SESSION` | Bypass only if active browser session |

---

## 3. External Services

External Services let you register an OpenAPI spec and auto-generate invocable actions usable in Flow, Einstein Bots, and Apex.

### Registration Steps

1. Create a Named Credential for the external API endpoint
2. Navigate to Setup > External Services
3. Provide the OpenAPI (Swagger) spec -- URL or paste JSON/YAML
4. Salesforce parses operations and generates invocable actions

### Requirements and Constraints

- OpenAPI **3.0** only (2.0/Swagger not supported for new registrations)
- Spec size limit: 100 KB
- Max 50 operations per registration
- All operations use the Named Credential for auth
- Generated actions appear as Flow External Service actions
- Supported HTTP methods: GET, POST, PUT, PATCH, DELETE

### Using External Service in Flow

After registration, each operation becomes an invocable action:

1. In Flow Builder, add an Action element
2. Filter by category "External Services"
3. Select the operation (e.g., `createOrder`, `getCustomer`)
4. Map Flow variables to input/output parameters
5. The Named Credential handles authentication automatically

### External Service Metadata

```xml
<!-- MyExternalService.externalServiceRegistration-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<ExternalServiceRegistration xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>MyExternalService</fullName>
    <label>My External Service</label>
    <namedCredential>MyService</namedCredential>
    <schema>--- OpenAPI JSON spec inlined or referenced ---</schema>
    <schemaType>OpenApi3</schemaType>
    <serviceBinding>
        <fieldName>operationName</fieldName>
        <value>createOrder</value>
    </serviceBinding>
    <status>Complete</status>
</ExternalServiceRegistration>
```

---

## 4. Platform Events

Custom event bus for decoupled, event-driven integration within Salesforce and with external systems.

### Event Definition

```xml
<!-- Order_Event__e.object-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Order_Event__e</fullName>
    <label>Order Event</label>
    <pluralLabel>Order Events</pluralLabel>
    <publishBehavior>PublishAfterCommit</publishBehavior>
    <fields>
        <fullName>Order_Id__c</fullName>
        <label>Order Id</label>
        <type>Text</type>
        <length>18</length>
    </fields>
    <fields>
        <fullName>Action__c</fullName>
        <label>Action</label>
        <type>Text</type>
        <length>50</length>
    </fields>
    <fields>
        <fullName>Payload__c</fullName>
        <label>Payload</label>
        <type>LongTextArea</type>
        <length>131072</length>
        <visibleLines>5</visibleLines>
    </fields>
</CustomObject>
```

### Publish Behavior

| Behavior | When event publishes | Use when |
|----------|---------------------|----------|
| `PublishAfterCommit` | After transaction commits successfully | Default. Event should reflect committed data |
| `PublishImmediately` | Immediately, even if transaction rolls back | Logging, auditing, fire-and-forget notifications |

**Key rule**: `PublishAfterCommit` events do not fire if the transaction rolls back. `PublishImmediately` events fire regardless -- use cautiously.

### Subscriber Patterns

- **Apex Trigger**: `trigger OrderEventTrigger on Order_Event__e (after insert)` -- runs in its own execution context
- **Flow**: Use a Platform Event-Triggered Flow (Record-Triggered flows cannot subscribe)
- **External**: CometD or Pub/Sub API (gRPC) for external system subscribers

### Replay and Retention

- **Standard Platform Events**: retained 24 hours, replayable via Replay ID
- **High-Volume Platform Events**: retained 72 hours, higher throughput (150K/hour)
- Use `ReplayId` in CometD or Pub/Sub API to resume from a specific point after subscriber failure
- Subscribers can set replay position: `-1` (tip), `-2` (all retained events), or a specific Replay ID

---

## 5. Change Data Capture (CDC)

Streams record changes (create, update, delete, undelete) as events on the event bus.

### Enabling CDC

1. Setup > Change Data Capture
2. Select objects to track (standard or custom)
3. Changes publish to channels: `/data/<ObjectName>ChangeEvent` (e.g., `/data/AccountChangeEvent`)

For custom objects: `/data/<CustomObject__c>ChangeEvent` becomes `/data/Custom_Object__ChangeEvent`

### ChangeEventHeader Fields

Every CDC event includes a header with change metadata:

| Field | Description |
|-------|-------------|
| `entityName` | SObject API name |
| `changeType` | `CREATE`, `UPDATE`, `DELETE`, `UNDELETE` |
| `changedFields` | List of fields that changed (UPDATE only) |
| `commitTimestamp` | When the change was committed |
| `transactionKey` | Groups changes from the same transaction |
| `sequenceNumber` | Order within a transaction |
| `recordIds` | IDs of changed records |
| `commitUser` | User who made the change |
| `commitNumber` | Monotonically increasing commit sequence |

### CDC Subscriber Trigger

```apex
trigger AccountChangeEventTrigger on AccountChangeEvent (after insert) {
    for (AccountChangeEvent event : Trigger.new) {
        EventBus.ChangeEventHeader header = event.ChangeEventHeader;
        String changeType = header.getChangeType();
        List<String> changedFields = header.getChangedFields();

        if (changeType == 'UPDATE' && changedFields.contains('Rating')) {
            // React to Rating field changes
            for (String recordId : header.getRecordIds()) {
                // Queue processing for each changed record
            }
        }
    }
}
```

### CDC vs Platform Events

| Aspect | CDC | Platform Events |
|--------|-----|-----------------|
| Trigger | Automatic on record DML | Explicit publish via code/flow |
| Schema | Mirrors SObject fields | Custom-defined fields |
| Use case | React to data changes | Decouple business processes |
| Retention | 72 hours | 24h (standard) / 72h (high-volume) |
| External subscribe | Pub/Sub API, CometD | Pub/Sub API, CometD |

---

## 6. Outbound Messaging (Legacy)

SOAP-based outbound notifications triggered by Workflow Rules. Legacy pattern -- prefer Platform Events for new work.

- Fires from Workflow Rules only (not Process Builder or Flow)
- SOAP format, automatic retry with exponential backoff for 24 hours
- Endpoint must respond with Ack ID; retries until acknowledged or 24h timeout
- Max 100 fields per message
- **Migrate to**: Platform Events (decoupled pub/sub), Flow + HTTP Callout (declarative), or Apex Callout (complex request/response)

---

## 7. Remote Site Settings vs Named Credentials

### Migration Path

Remote Site Settings only whitelist an endpoint URL. Named Credentials add auth management on top.

| Feature | Remote Site Setting | Named Credential |
|---------|-------------------|-----------------|
| URL whitelisting | Yes | Yes (implicit) |
| Auth management | No (manual in code) | Yes (automatic) |
| Credential storage | Developer responsibility | Platform-managed |
| Per-environment config | Manual | Built-in |
| Merge fields | No | Yes (headers, body, URL) |
| Deployable | Yes | Yes |

**Migration steps**:
1. Create Named Credential with the Remote Site URL as endpoint
2. Configure auth protocol (OAuth, Password, JWT, etc.)
3. Update Apex code: replace hardcoded endpoint with `callout:NamedCredentialName`
4. Remove auth header construction from code
5. Delete the Remote Site Setting
6. Test in sandbox before production

---

## 8. Auth Flow Decision Guide

| Flow | Use case | Client type | User interaction |
|------|----------|-------------|-----------------|
| **JWT Bearer** | Server-to-server, CI/CD, backend automation | Confidential | None (pre-authorized) |
| **Web Server (Auth Code)** | Web apps with user login | Confidential | Browser redirect |
| **Auth Code + PKCE** | SPAs, mobile apps, public clients | Public | Browser redirect |
| **Client Credentials** | M2M, service accounts (no user context) | Confidential | None |
| **Device Flow** | CLI tools, headless devices, IoT | Public or confidential | Out-of-band user auth |
| **Refresh Token** | Maintain sessions without re-auth | Either | None (silent) |

### Decision Rules

1. **No user context needed?** Use Client Credentials (if available) or JWT Bearer
2. **Backend service?** JWT Bearer with X.509 certificate
3. **User-facing web app?** Web Server flow
4. **Public client (SPA/mobile)?** Auth Code + PKCE (mandatory)
5. **No browser?** Device Flow
6. **Long-lived access?** Add `RefreshToken` / `OfflineAccess` scope

---

## 9. Gotchas

### Named Credentials
- Max **100 callouts** per synchronous transaction (shared with all HTTP requests)
- Enhanced Named Credentials require Permission Set mapping or callout silently fails
- External Credential parameter names are case-sensitive
- `generateAuthorizationHeader` must be `true` for automatic OAuth header injection

### Platform Events
- **150,000 events/hour** publish limit (high-volume); 50,000 for standard
- `PublishAfterCommit` events lost if transaction rolls back -- no retry
- At-least-once delivery: subscribers must be idempotent
- Subscriber trigger failures cause automatic retry (up to 8 retries with backoff)
- `EventBus.publish()` does not throw exceptions -- check `SaveResult` for errors

### Change Data Capture
- **72-hour replay window** -- events older than 72h are lost
- CDC events do not fire for bulk API operations by default (must enable)
- Large transaction changes may be split across multiple events (check `sequenceNumber`)
- Not available for all standard objects -- check Salesforce documentation

### External Services
- **OpenAPI 3.0 only** -- Swagger 2.0 specs must be converted
- 100 KB spec size limit
- Max 50 operations per registration
- Complex nested schemas may not parse correctly -- flatten where possible

### Connected Apps
- Consumer key/secret generated on creation -- cannot be set via metadata
- **Admin approval required** for JWT Bearer and Client Credentials flows
- Certificate expiry causes silent auth failures -- monitor and rotate
- IP relaxation policy applies to the Connected App, not the user's IP restrictions
- Changes to Connected App take up to 10 minutes to propagate

### General
- Cannot mix synchronous callouts and DML in the same transaction without careful ordering (callout before DML, or use `@future`/Queueable)
- Callout timeout max: 120 seconds per request, 120 seconds total per transaction

---

## Workflow

1. Identify the integration pattern using the decision guides above
2. Use Glob and Grep to find existing integration metadata in the project
3. Generate or update Named Credential / External Credential / Connected App metadata
4. Configure Platform Events or CDC if event-driven
5. Set up External Services if spec-driven
6. Verify Permission Set mappings for External Credentials
7. Suggest deployment: `sf project deploy start -d force-app/main/default/namedCredentials/`

## References

- [Integration Reference](references/integration-reference.md) -- metadata XML templates, auth flow details, architecture decision guides
- [Apex Integration Patterns](../sf-apex/references/integration-patterns.md) -- callout code, @RestResource, SOAP, mocks (separate skill)
- [Governor Limits](../../references/governor-limits.md) -- per-transaction limits
