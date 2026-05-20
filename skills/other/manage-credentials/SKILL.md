---
name: manage-credentials
description: Set up and manage package and connection credentials securely in Datagrok
---

# Manage Credentials

Help the user store, retrieve, and manage security credentials for packages and database connections.

## Usage
```
/manage-credentials [package-name] [--connection <connection-name>]
```

## Instructions

### 1. Read package credentials in code

```typescript
const creds = await _package.getCredentials();
if (creds === null) {
  grok.shell.info('Credentials are not set.');
  return;
}
const login = creds.parameters['login'];
const password = creds.parameters['password'];
```

Read a single parameter:
```typescript
const creds = await _package.getCredentials();
const apiKey = creds.parameters['apiKey'];
```

### 2. Set package credentials via API

Send a POST request to the credentials endpoint:

```typescript
const grokHost = 'https://your-instance.datagrok.ai';
const packageName = 'MyPackage';
const url = `${grokHost}/api/credentials/for/${packageName}`;

const headers = {
  'Authorization': apiKey,
  'Content-Type': 'application/json'
};

const credentials = {login: 'myLogin', password: 'myPassword'};
await fetch(url, {method: 'POST', headers, body: JSON.stringify(credentials)});
```

### 3. Set package credentials via UI

1. Go to **Manage | Packages**
2. Right-click the package > **Credentials...**
3. Add key-value pairs
4. Set **Credentials owner** (a user or group — only members can read)

### 4. Connection credentials in JSON

Define credentials in the connection JSON file using environment variable substitution:

```json
{
  "#type": "DataConnection",
  "name": "MyDb",
  "parameters": {
    "server": "db.example.com",
    "port": 5432,
    "db": "mydb"
  },
  "credentials": {
    "parameters": {
      "login": "${DB_LOGIN}",
      "password": "${DB_PASSWORD}"
    }
  },
  "dataSource": "Postgres"
}
```

### 5. Set connection credentials via API

For connections that belong to a package, use a dotted name:

```
POST ${GROK_HOST}/api/credentials/for/${PACKAGE_NAME}.${CONNECTION_NAME}
Headers: { Authorization: <API_KEY>, Content-Type: application/json }
Body: { "login": "...", "password": "..." }
```

### 6. Service users

For automated credential management, create a service user:

1. Go to **Manage | Users | Actions | Add Service User**
2. Specify a login and generate an API key
3. Use the service user's API key for programmatic credential setup

## Behavior

- Never commit credentials or secrets in JSON files to the repository.
- Always use environment variable substitution (`${VAR_NAME}`) in connection files for sensitive values.
- When the user needs to store API keys or tokens, guide them to package credentials (`_package.getCredentials()`).
- When the user needs database login/password, guide them to connection credentials.
- Remind users about the **Credentials owner** field — it controls who can read the credentials.
- For examples, refer to the NLP package and `packages/ApiSamples/scripts/misc/package-credentials`.
