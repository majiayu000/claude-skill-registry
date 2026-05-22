---
name: n8n-syntax-credentials
description: >
  Use when creating custom credentials, implementing authentication, configuring
  OAuth2, or testing credential connections. Prevents incorrect authenticate
  injection methods and OAuth2 misconfiguration. Covers ICredentialType
  interface, credential properties, authenticate property with 4 injection
  methods (query, header, body, basic auth), OAuth2 configuration, API key
  patterns, credential testing via ICredentialTestRequest, and
  genericCredentialRequest.
  Keywords: n8n, credentials, ICredentialType, authenticate, OAuth2, API key,
  credential testing, ICredentialTestRequest, genericCredentialRequest.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n-syntax-credentials

## Quick Reference

### ICredentialType Interface

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | `string` | YES | Internal identifier (e.g., `'myServiceApi'`) |
| `displayName` | `string` | YES | GUI label shown to users |
| `documentationUrl` | `string` | NO | Link to credentials setup docs |
| `properties` | `INodeProperties[]` | YES | Array of credential input fields |
| `authenticate` | `IAuthenticate` | NO | How credentials inject into requests |
| `test` | `ICredentialTestRequest` | NO | Endpoint for credential validation |
| `extends` | `string[]` | NO | Inherit from other credential types |
| `icon` | `Icon` | NO | Credential icon in GUI |
| `iconUrl` | `string` | NO | URL-based icon |

### Credential Property Types

| Type | Use Case | Example |
|------|----------|---------|
| `'string'` | API keys, tokens, URLs | `{ type: 'string', typeOptions: { password: true } }` |
| `'number'` | Port numbers, numeric IDs | `{ type: 'number', default: 443 }` |
| `'boolean'` | Feature toggles | `{ type: 'boolean', default: false }` |
| `'options'` | Region selectors, auth method | `{ type: 'options', options: [...] }` |
| `'hidden'` | Internal values, computed tokens | `{ type: 'hidden', typeOptions: { expirable: true } }` |

### authenticate: 4 Injection Methods

| Method | Target | Key in `properties` |
|--------|--------|---------------------|
| Query string | URL parameters | `qs` |
| Header | HTTP headers | `headers` |
| Request body | POST body | `body` |
| Basic auth | Authorization header | `auth` |

ALL methods require `type: 'generic'` as the authenticate type.

### Credential Expression Syntax

Access credential values inside `authenticate` using: `={{$credentials.fieldName}}`

For header values with prefixes: `'=Bearer {{$credentials.apiKey}}'`

### Critical Warnings

**ALWAYS** set `typeOptions: { password: true }` on sensitive fields (API keys, tokens, passwords) -- n8n masks these in the GUI and encrypts them at rest.

**ALWAYS** register credentials in `package.json` under the `n8n.credentials` array pointing to compiled `.js` files in `dist/`.

**ALWAYS** use `type: 'generic'` in the authenticate property -- no other type value is supported for the generic authenticate pattern.

**ALWAYS** provide a `test` property with a lightweight API endpoint to validate credentials during setup.

**NEVER** store credentials in plain text or workflow JSON -- n8n encrypts all credential data using an encryption key.

**NEVER** hardcode credential values in node code -- ALWAYS read them via `this.getCredentials('credentialTypeName')` in the node's execute method.

**NEVER** use `authenticate` AND manually inject credentials in the node's `execute()` method for the same credential -- pick one approach.

**NEVER** forget the `=` prefix in authenticate expressions -- `'={{$credentials.key}}'` is correct, `'{{$credentials.key}}'` silently passes a literal string.

---

## Decision Tree: Which Authentication Pattern?

```
Need authentication?
├── API key in URL parameter?
│   └── Use authenticate.properties.qs
├── API key or token in header?
│   └── Use authenticate.properties.headers
├── Username + password (Basic Auth)?
│   └── Use authenticate.properties.auth
├── Credentials in request body?
│   └── Use authenticate.properties.body
├── OAuth2 flow?
│   └── Extend 'oAuth2Api' base credential
└── Complex/custom auth logic?
    └── Skip authenticate, handle in node execute() via this.getCredentials()
```

---

## Essential Patterns

### Pattern 1: API Key Credential (Header Injection)

```typescript
import type { ICredentialType, INodeProperties, IAuthenticate } from 'n8n-workflow';

export class ExampleApi implements ICredentialType {
  name = 'exampleApi';
  displayName = 'Example API';
  documentationUrl = 'https://docs.example.com/auth';
  properties: INodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: { password: true },
      default: '',
    },
  ];
  authenticate: IAuthenticate = {
    type: 'generic',
    properties: {
      headers: {
        Authorization: '=Bearer {{$credentials.apiKey}}',
      },
    },
  };
  test: ICredentialTestRequest = {
    request: {
      baseURL: 'https://api.example.com',
      url: '/me',
    },
  };
}
```

### Pattern 2: Query String Authentication

```typescript
authenticate: IAuthenticate = {
  type: 'generic',
  properties: {
    qs: {
      api_key: '={{$credentials.apiKey}}',
    },
  },
};
```

### Pattern 3: Basic Auth

```typescript
export class MyBasicAuthApi implements ICredentialType {
  name = 'myBasicAuthApi';
  displayName = 'My Basic Auth API';
  properties: INodeProperties[] = [
    {
      displayName: 'Username',
      name: 'username',
      type: 'string',
      default: '',
    },
    {
      displayName: 'Password',
      name: 'password',
      type: 'string',
      typeOptions: { password: true },
      default: '',
    },
  ];
  authenticate: IAuthenticate = {
    type: 'generic',
    properties: {
      auth: {
        username: '={{$credentials.username}}',
        password: '={{$credentials.password}}',
      },
    },
  };
}
```

### Pattern 4: Body Injection

```typescript
authenticate: IAuthenticate = {
  type: 'generic',
  properties: {
    body: {
      username: '={{$credentials.username}}',
      password: '={{$credentials.password}}',
    },
  },
};
```

### Pattern 5: OAuth2 Credential

```typescript
import type { ICredentialType, INodeProperties } from 'n8n-workflow';

export class MyServiceOAuth2Api implements ICredentialType {
  name = 'myServiceOAuth2Api';
  displayName = 'My Service OAuth2 API';
  extends = ['oAuth2Api'];
  documentationUrl = 'https://docs.myservice.com/oauth';
  properties: INodeProperties[] = [
    {
      displayName: 'Grant Type',
      name: 'grantType',
      type: 'hidden',
      default: 'authorizationCode',
    },
    {
      displayName: 'Authorization URL',
      name: 'authUrl',
      type: 'hidden',
      default: 'https://myservice.com/oauth/authorize',
    },
    {
      displayName: 'Access Token URL',
      name: 'accessTokenUrl',
      type: 'hidden',
      default: 'https://myservice.com/oauth/token',
    },
    {
      displayName: 'Scope',
      name: 'scope',
      type: 'hidden',
      default: 'read write',
    },
    {
      displayName: 'Auth URI Query Parameters',
      name: 'authQueryParameters',
      type: 'hidden',
      default: '',
    },
    {
      displayName: 'Authentication',
      name: 'authentication',
      type: 'hidden',
      default: 'body',
    },
  ];
}
```

### Pattern 6: Credential Testing

```typescript
test: ICredentialTestRequest = {
  request: {
    baseURL: '={{$credentials?.baseUrl}}',
    url: '/api/v1/verify',
    method: 'GET',
    skipSslCertificateValidation:
      '={{$credentials?.allowUnauthorizedCerts}}' as unknown as boolean,
  },
};
```

n8n calls this endpoint when users click "Test" in the credentials dialog. A 2xx response validates the credentials.

### Pattern 7: Credential Registration (package.json)

```json
{
  "name": "n8n-nodes-myservice",
  "n8n": {
    "n8nNodesApiVersion": 1,
    "credentials": [
      "dist/credentials/MyServiceApi.credentials.js",
      "dist/credentials/MyServiceOAuth2Api.credentials.js"
    ],
    "nodes": [
      "dist/nodes/MyService/MyService.node.js"
    ]
  }
}
```

**Rule**: The `n8n.credentials` array MUST point to compiled `.js` files in `dist/`, NEVER to `.ts` source files.

### Pattern 8: Credential Inheritance (extends)

```typescript
export class MyServiceApi implements ICredentialType {
  name = 'myServiceApi';
  displayName = 'My Service API';
  extends = ['oAuth2Api'];  // Inherits all OAuth2 properties
  properties: INodeProperties[] = [
    // Only define ADDITIONAL properties here
    // Base OAuth2 properties (clientId, clientSecret, etc.) are inherited
    {
      displayName: 'Region',
      name: 'region',
      type: 'options',
      options: [
        { name: 'US', value: 'us' },
        { name: 'EU', value: 'eu' },
      ],
      default: 'us',
    },
  ];
}
```

### Pattern 9: Using Credentials in Node execute()

```typescript
async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
  const credentials = await this.getCredentials('exampleApi');
  // credentials.apiKey, credentials.baseUrl, etc.

  const response = await this.helpers.httpRequestWithAuthentication.call(
    this, 'exampleApi', {
      method: 'GET',
      url: `${credentials.baseUrl}/api/data`,
    }
  );

  return [this.helpers.returnJsonArray(response as IDataObject[])];
}
```

**Rule**: When using `authenticate` on the credential, use `httpRequestWithAuthentication` -- it automatically applies the authenticate configuration. When NOT using `authenticate`, manually inject credentials into request options.

---

## Credential Node Binding

Link credentials to nodes via the `credentials` array in `INodeTypeDescription`:

```typescript
credentials: [
  {
    name: 'myServiceApi',
    required: true,
  },
  {
    name: 'myServiceOAuth2Api',
    required: true,
    displayOptions: {
      show: { authentication: ['oAuth2'] },
    },
  },
],
```

Use `displayOptions` to conditionally show credentials based on an authentication method selector.

---

## Reference Links

- [references/methods.md](references/methods.md) -- ICredentialType interface, IAuthenticate, ICredentialTestRequest, property types
- [references/examples.md](references/examples.md) -- API key credential, OAuth2 credential, basic auth, credential test
- [references/anti-patterns.md](references/anti-patterns.md) -- Credential configuration mistakes

### Official Sources

- https://docs.n8n.io/integrations/creating-nodes/build/reference/credentials-files/
- https://docs.n8n.io/integrations/creating-nodes/build/reference/ui-elements/
- https://github.com/n8n-io/n8n/tree/master/packages/workflow/src
- https://github.com/n8n-io/n8n-nodes-starter
