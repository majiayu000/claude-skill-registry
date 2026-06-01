---

name: forge-connector
description: >
  Guides building and deploying Atlassian Forge Teamwork Graph connector apps that ingest
  external data into Atlassian's Teamwork Graph, making it searchable in Rovo Search and
  surfaced in Rovo Chat. Use when the user wants to build a Forge connector, ingest external
  data into Atlassian, connect a third-party tool (e.g. Google Drive, ServiceNow, Salesforce)
  to Atlassian, make external content searchable in Rovo, build a graph:connector module,
  use the @forge/teamwork-graph SDK, or implement onConnectionChange / validateConnection
  functions.
license: Apache-2.0
labels:
  - forge
  - rovo
  - jira
  - atlassian
  - teamwork-graph
  - connector
maintainer: mbanjan94
namespace: cloud
---

# Forge Connector

Builds a `graph:connector` Forge app that ingests external data into Atlassian's Teamwork Graph so it appears in **Rovo Search** and **Rovo Chat**.

## Critical Rules

1. **Must install in Jira** — Apps using Teamwork Graph modules must be installed on a Jira site. Confluence-only installs will not work.
2. **Never ask for credentials in chat** — Direct users to run `forge login` in their own terminal.
3. **Always run the scaffold script yourself** — Do not only give manual instructions; run `scripts/scaffold_connector.py` to generate the boilerplate.
4. **Always ask the user for their Atlassian site URL** when install is needed — never discover or guess it.
5. **Atlassian deletes data on disconnect** — When `action = 'DELETED'`, the app only needs to clean up local state; Atlassian removes the Teamwork Graph data automatically.
6. **Handler arguments are passed directly** — Forge passes the request object as the first argument to handlers, NOT nested under `event.payload`. Config values are at `request.configProperties`, NOT `event.payload.config`. This is the most common source of `TypeError: Cannot destructure property of undefined` errors.
7. **Use `@forge/kvs` for storage** — Import `kvs` from `@forge/kvs`. Do NOT use `@forge/storage` — its `storage` export is `undefined` at runtime in connector functions.
8. **Use `graph` named export from `@forge/teamwork-graph`** — The correct import is `const { graph } = require('@forge/teamwork-graph')`. Call `graph.setObjects({ objects, connectionId })`. Do NOT import `setObjects` as a named export directly.
9. **`validateConnectionHandler` must return `{ success, message }`** — Do NOT throw an Error. Return `{ success: false, message: '...' }` to reject, `{ success: true }` to accept.
10. **`function` declarations belong under `modules`** — In `manifest.yml`, `function:` is a key under `modules:`, not a top-level key. Placing it at the top level causes a lint error.
11. **`formConfiguration` uses `form` array with `type: header`** — Do NOT use `fields:` or `beforeYouBegin:`. The correct format uses `form: [{ key, type: header, title, description, properties: [...] }]`.
12. **Scopes are `read/write/delete:object:jira`** — Use `read:object:jira`, `write:object:jira`, `delete:object:jira`. The scopes `read:graph:teamwork` and `write:graph:teamwork` are invalid and will fail `forge lint`.

## MCP Prerequisites


| MCP Server    | Purpose                                           |
| ------------- | ------------------------------------------------- |
| **Forge MCP** | Manifest syntax, module config, deployment guides |
| **ADS MCP**   | Atlaskit components (only if adding Custom UI)    |


---

## Agent Workflow — Complete Steps 0–5 in Order

### Step 0: Prerequisites

Check Node.js (`node -v`, requires 22+), Forge CLI (`forge --version`), and login (`forge whoami`). Install missing tools:

```bash
npm install -g @forge/cli
```

Tell the user to run `forge login` in their terminal if not authenticated.

### Step 1: Discover Developer Spaces

> **Note:** `forge developer-spaces list` does NOT exist in Forge CLI 12.x. You cannot list developer spaces non-interactively.

`forge create` requires an interactive TTY to select a developer space. Ask the user to run it themselves:

```
Tell the user:
  cd <parent-directory>
  forge create --template blank <app-name>

  When prompted, select a Developer Space and let it complete.
  Come back when done.
```

The `--dev-space-id` flag in the scaffold script is optional and can be omitted — the script has been updated to skip it when not provided.

### Step 2: Scaffold the Connector App

Run from the **skill directory** (the directory containing this SKILL.md). `--dev-space-id` is optional:

```bash
python3 -m scripts.scaffold_connector \
  --name <app-name> \
  --connector-name "<Human Readable Name>" \
  --object-type atlassian:document \
  --directory <parent-directory>
```

Add `--dev-space-id <id>` only if you have the ID from a previous step.

**Object type selection** — pick the type that best matches the content being ingested (see Object Types table). For mixed content, use `atlassian:document` as the default.

**Form config flag** — add `--has-form-config` if the admin must provide API credentials or connection details (typical for external systems). Omit it for apps that operate entirely within Atlassian (no external credentials needed).

> **If scaffold fails because `forge create` needs a TTY:** The scaffold script will print a manual fallback command. Have the user run `forge create` interactively, then continue from Step 3 — the scaffold script only needs to write `manifest.yml` and `src/index.js` after the directory exists.

### Step 3: Customize the Generated Code

After scaffolding (or after the user runs `forge create` interactively):

```bash
cd <app-name>
npm install
```

The blank template generates `src/index.js` (JavaScript, not TypeScript). Edit it to add your API calls. The scaffold generates working handler skeletons; fill in your business logic.

#### Key files to edit

| File           | What to change                                                          |
| -------------- | ----------------------------------------------------------------------- |
| `src/index.js` | `fetchExternalData()` — replace with your API calls                     |
| `manifest.yml` | Add `permissions.external.fetch.backend` URLs for any external APIs     |
| `package.json` | Add `@forge/api`, `@forge/kvs`, `@forge/teamwork-graph` as dependencies |


#### setObjects — ingest data into Teamwork Graph

Use the `graph` named export — do NOT destructure `setObjects` directly:

```javascript
const { graph } = require('@forge/teamwork-graph');

const result = await graph.setObjects({
  connectionId,          // required — the connectionId from the handler request
  objects: [
    {
      schemaVersion: '1.0',
      id: 'unique-id-from-source',      // unique per connectionId
      updateSequenceNumber: 1,
      displayName: 'My Document Title',
      url: 'https://source-system.example.com/doc/123',
      createdAt: '2024-01-15T10:00:00Z',        // ISO 8601
      lastUpdatedAt: '2024-01-20T14:30:00Z',
      permissions: [{
        accessControls: [{
          principals: [{ type: 'EVERYONE' }],   // or restrict to specific users
        }],
      }],
      'atlassian:document': {
        type: {
          category: 'DOCUMENT',   // see Document Categories table below
          mimeType: 'application/vnd.google-apps.document',
        },
        content: {
          mimeType: 'application/vnd.google-apps.document',
          text: 'document title or snippet for search indexing',
        },
      },
    },
  ],
});

if (!result.success) {
  console.error('setObjects error:', result.error);
}
```

- Max **100 objects per call** — batch large datasets with a loop
- `id` must be unique per `connectionId`
- `connectionId` is required in every `graph.setObjects()` call

#### Document Categories (for `atlassian:document.type.category`)

| MIME type | Category |
|---|---|
| `application/vnd.google-apps.document` | `DOCUMENT` |
| `application/vnd.google-apps.spreadsheet` | `SPREADSHEET` |
| `application/vnd.google-apps.presentation` | `PRESENTATION` |
| `application/vnd.google-apps.folder` | `FOLDER` |
| `application/pdf` | `PDF` |
| `image/*` | `IMAGE` |
| `video/*` | `VIDEO` |
| `audio/*` | `AUDIO` |
| Other | `OTHER` |

#### getObjectByExternalId — look up a single object

```javascript
const { graph } = require('@forge/teamwork-graph');

const data = await graph.getObjectByExternalId({
  externalId: 'unique-id-from-source',
  objectType: 'atlassian:document',
  connectionId,
});
if (data.success) console.log(data.object);
```

### Step 4: Deploy and Install

**You MUST run the deploy script** — do not only give the user manual `forge deploy` commands.

The deploy script lives in the **forge-app-builder** skill, not in this skill. Derive its directory from the path of this SKILL.md: go up two levels (`skills/forge-connector/` → `skills/`) then into `forge-app-builder/`. Run all commands below from that directory.

```bash
# Derive forge-app-builder skill dir from this SKILL.md's path:
# e.g. if this file is at /path/to/skills/forge-connector/SKILL.md
# then the deploy script dir is: /path/to/skills/forge-app-builder/

# If you have the site URL:
python3 -m scripts.deploy_forge_app \
  --app-dir <app-directory> \
  --site <site-url> \
  --product jira

# If you don't have the site URL yet, deploy first then ask:
python3 -m scripts.deploy_forge_app \
  --app-dir <app-directory> \
  --product jira \
  --deploy-only
# Ask: "What is your Atlassian site URL (e.g. yourcompany.atlassian.net)?"
python3 -m scripts.deploy_forge_app \
  --app-dir <app-directory> \
  --site <site-url> \
  --product jira \
  --skip-deps
```

### Step 5: Connect via Atlassian Administration

After deployment, tell the user to:

1. Go to **Atlassian Administration** → **Apps** → **[site]** → **Connected apps**
2. Find the app → **View app details** → **Connections** tab
3. Click **Connect** under the connector
4. Fill in any configuration fields (if `formConfiguration` was defined)
5. Click **Connect** — this triggers `onConnectionChange` with `action: CREATED` and starts data ingestion

### Step 6: Monitor with forge tunnel

Use `forge tunnel` during development to stream live logs directly to your terminal as the connector functions execute. This is the fastest way to catch errors in `onConnectionChangeHandler`, `validateConnectionHandler`, and `setObjects` calls without waiting for `forge logs`.

Tell the user to run this in their own terminal (it requires an interactive session):

```bash
cd <app-directory>
forge tunnel
```

With the tunnel active, any invocation of the connector functions (e.g. clicking "Connect" in Atlassian Admin, or triggering a scheduled re-ingestion) will stream output immediately. Look for:

- `[connector] Fetched N items` — confirms `fetchExternalData()` ran
- `[connector] Batch 1: N accepted, 0 rejected` — confirms `setObjects` succeeded
- Any uncaught errors or thrown exceptions from `validateConnectionHandler`

If the tunnel is not running, use `forge logs` instead to inspect past invocations:

```bash
# Most recent 50 log lines from development environment
forge logs -e development --limit 50

# Production logs for a specific site
forge logs -e production --site <your-site> --limit 50
```

**Tunnel vs logs — when to use which:**

| Situation | Use |
|---|---|
| Actively developing / testing the connection flow | `forge tunnel` — live streaming |
| Debugging a past invocation or production issue | `forge logs` |
| Connector function timed out before tunnel caught it | `forge logs` with `--limit 100` |

> **Note:** `forge tunnel` must be run by the user in an interactive terminal — do not attempt to run it via the agent.

---

## Manifest Reference

> **Key rules:**
> - Scopes are `read:object:jira`, `write:object:jira`, `delete:object:jira` — NOT `read:graph:teamwork` / `write:graph:teamwork` (those fail `forge lint`)
> - `function:` is declared **under `modules:`**, not at the top level
> - Egress uses `address:` not a bare string (run `forge lint --fix` to auto-correct)
> - `formConfiguration` uses `form: [{ type: header, properties: [...] }]` — NOT `fields:` or `beforeYouBegin:`

### Minimal connector (no admin config, no OAuth)

Use when the app operates entirely within Atlassian — no external credentials needed.

```yaml
app:
  id: <generated-by-forge-create>
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64

permissions:
  scopes:
    - read:object:jira
    - write:object:jira
    - delete:object:jira
    - storage:app

modules:
  graph:connector:
    - key: my-connector
      name: My Service
      icons:
        light: https://cdn.example.com/logo.png
        dark: https://cdn.example.com/logo.png
      objectTypes:
        - atlassian:document
      datasource:
        onConnectionChange:
          function: on-connection-change

  function:
    - key: on-connection-change
      handler: index.onConnectionChangeHandler
```

### Connector with admin form config (API key / URL)

Use when the admin must provide credentials to connect to an external system.

```yaml
app:
  id: <generated-by-forge-create>
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64

permissions:
  scopes:
    - read:object:jira
    - write:object:jira
    - delete:object:jira
    - storage:app
  external:
    fetch:
      backend:
        - address: 'https://api.your-service.com'   # note: address: not a bare string

modules:
  graph:connector:
    - key: my-connector
      name: My Service
      icons:
        light: https://cdn.example.com/logo.png
        dark: https://cdn.example.com/logo.png
      objectTypes:
        - atlassian:document
      datasource:
        formConfiguration:
          form:                          # use form:, NOT fields: or beforeYouBegin:
            - key: connectionDetails
              type: header
              title: Connection Details
              description: >
                Provide your My Service API credentials.
                Find them in My Service → Settings → API.
              properties:
                - key: apiKey           # camelCase keys — accessed as request.configProperties.apiKey
                  label: API Key
                  type: string
                  isRequired: true
                - key: apiUrl
                  label: API URL
                  type: string
                  isRequired: true
          validateConnection:
            function: validate-connection
        onConnectionChange:
          function: on-connection-change

  function:                              # function: is under modules:, NOT top-level
    - key: on-connection-change
      handler: index.onConnectionChangeHandler
    - key: validate-connection
      handler: index.validateConnectionHandler
```

---

## Handler Signatures

> **Critical:** Forge passes the request **directly as the first argument** — it is NOT wrapped under `event.payload`. Config form values are at `request.configProperties`, not `event.payload.config`. Getting this wrong causes `TypeError: Cannot destructure property of undefined`.

### onConnectionChange

```javascript
const { kvs } = require('@forge/kvs');
const { graph } = require('@forge/teamwork-graph');

exports.onConnectionChangeHandler = async (request) => {
  // request.action, request.connectionId, request.configProperties
  const { action, connectionId, configProperties } = request;

  if (action === 'DELETED') {
    // Atlassian removes Teamwork Graph data automatically on disconnect.
    // Only clean up locally stored credentials.
    await kvs.deleteSecret(connectionId);
    return { success: true };
  }

  // CREATED or UPDATED — persist credentials and ingest data
  await kvs.setSecret(connectionId, configProperties);
  await ingestAllData(connectionId, configProperties);
  return { success: true };
};
```

### validateConnection

```javascript
const { fetch } = require('@forge/api');

exports.validateConnectionHandler = async (request) => {
  // request.configProperties — NOT event.payload.config
  const { configProperties } = request;

  // Return { success: false, message } to reject — do NOT throw an Error.
  // Return { success: true } to accept.
  const response = await fetch(`${configProperties['apiUrl']}/health`);
  if (!response.ok) {
    return { success: false, message: 'Invalid API credentials. Please check your settings.' };
  }
  return { success: true, message: 'Connection validated successfully.' };
};
```

### refreshIngestion (scheduled trigger)

```javascript
exports.refreshIngestionHandler = async () => {
  const activeConnections = await kvs.get('active-connections') ?? [];
  for (const connectionId of activeConnections) {
    const config = await kvs.getSecret(connectionId);
    if (config) await ingestAllData(connectionId, config);
  }
};
```

---

## Object Types

Objects in **bold** are indexed in Rovo Search and Rovo Chat.


| Object Type                       | Indexed in Rovo | Best for                             |
| --------------------------------- | --------------- | ------------------------------------ |
| `atlassian:document`              | ✅               | Files, pages, wiki articles, reports |
| `atlassian:message`               | ✅               | Chat messages, emails, comments      |
| `atlassian:work-item`             | ✅               | Tasks, tickets, issues               |
| `atlassian:project`               | ✅               | Projects, workspaces                 |
| `atlassian:space`                 | ✅               | Team spaces, org units               |
| `atlassian:design`                | ✅               | Design files (Figma, etc.)           |
| `atlassian:repository`            | ✅               | Code repositories                    |
| `atlassian:pull-request`          | ✅               | PRs, merge requests                  |
| `atlassian:commit`                | ✅               | Git commits                          |
| `atlassian:branch`                | ✅               | Git branches                         |
| `atlassian:conversation`          | ✅               | Threads, channels                    |
| `atlassian:video`                 | ✅               | Video recordings                     |
| `atlassian:calendar-event`        | ✅               | Meetings, events                     |
| `atlassian:comment`               | ✅               | Review comments                      |
| `atlassian:customer-organization` | ✅               | Customer accounts, orgs              |
| `atlassian:build`                 | ❌               | CI/CD builds                         |
| `atlassian:deployment`            | ❌               | Deployments                          |
| `atlassian:test`                  | ❌               | Test cases                           |


---

## Rovo Search / Rovo Chat Surfacing

Once ingested:

- Objects appear in **Rovo Search** under a subfilter named after the connector's nickname (set by admin at connection time)
- **Rovo Chat** can reference and cite connector objects in responses when queried about topics related to the ingested content
- Data is not available immediately — allow a few minutes for indexing after `onConnectionChange` fires

To verify ingestion is working:

1. Open Rovo Search on the Jira site
2. Search for text that appears in an ingested object's `name` or `properties`
3. Filter by the connector nickname to narrow results

---

## Batching Pattern for Large Datasets

```javascript
const { graph } = require('@forge/teamwork-graph');

const BATCH_SIZE = 100;

async function ingestAllData(connectionId, config) {
  const items = await fetchExternalData(config);

  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);
    const result = await graph.setObjects({
      connectionId,          // required in every call
      objects: batch.map(item => ({
        schemaVersion: '1.0',
        id: item.id,                      // unique per connectionId
        updateSequenceNumber: 1,
        displayName: item.title,
        url: item.url,
        createdAt: item.createdAt,
        lastUpdatedAt: item.updatedAt,
        permissions: [{
          accessControls: [{ principals: [{ type: 'EVERYONE' }] }],
        }],
        'atlassian:document': {
          type: { category: 'DOCUMENT', mimeType: item.mimeType },
          content: { mimeType: item.mimeType, text: item.title },
        },
      })),
    });
    if (!result.success) {
      console.error(`[connector] setObjects error in batch ${Math.floor(i / BATCH_SIZE) + 1}:`, result.error);
    }
  }
}
```

---

## Scheduled Re-Ingestion (optional)

To keep data fresh, add a scheduled trigger that re-runs ingestion periodically:

```yaml
# In manifest.yml — under modules:
scheduledTrigger:
  - key: refresh-trigger
    function: refresh-ingestion
    interval: day   # prefer 'day' or 'hour'; avoid 'fiveMinutes'

# Under function:
  - key: refresh-ingestion
    handler: index.refreshIngestionHandler
```

```javascript
const { kvs } = require('@forge/kvs');

// Track active connections in onConnectionChangeHandler:
//   await kvs.set('active-connections', [...activeConnections, connectionId]);
//   await kvs.setSecret(connectionId, configProperties);  // store credentials securely

exports.refreshIngestionHandler = async () => {
  const activeConnections = await kvs.get('active-connections') ?? [];
  for (const connectionId of activeConnections) {
    const config = await kvs.getSecret(connectionId);  // retrieve stored credentials
    if (config) await ingestAllData(connectionId, config);
  }
};
```

---

## Scripts


| Script                          | Skill directory                                   | Purpose                                                                                                                         |
| ------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/scaffold_connector.py` | `skills/forge-connector/` (this skill)            | Scaffold a new connector app — generates manifest.yml, src/index.ts, installs SDK. Run: `python3 -m scripts.scaffold_connector` |
| `scripts/deploy_forge_app.py`   | `skills/forge-app-builder/` (**different skill**) | Deploy and install on Jira. Run from the forge-app-builder directory: `python3 -m scripts.deploy_forge_app`                     |


The scaffold script is in this skill's directory. The deploy script is in the **forge-app-builder** skill directory — always `cd` there (or derive the path from this SKILL.md's location) before running it.

---

## Troubleshooting

| Problem | Action |
| --- | --- |
| `graph:connector` not recognized in manifest | Run `forge lint` — it will identify the exact field causing the error |
| `TypeError: Cannot destructure property 'config' of 'event.payload'` | Handler using `event.payload.config` — change to `request.configProperties`. Forge passes request directly, not nested under `event.payload` |
| `TypeError: Cannot read properties of undefined (reading 'set')` | Using `storage` from `@forge/storage` — switch to `kvs` from `@forge/kvs` |
| `graph.setObjects is not a function` | Wrong import — use `const { graph } = require('@forge/teamwork-graph')` then call `graph.setObjects({ objects, connectionId })` |
| `forge lint`: invalid scopes `read/write:graph:teamwork` | Replace with `read:object:jira`, `write:object:jira`, `delete:object:jira` |
| `forge lint`: `document should NOT have additional property 'function'` | `function:` is at the top level — move it inside `modules:` |
| `forge lint`: `formConfiguration must have required property 'form'` | Replace `fields:` / `beforeYouBegin:` with `form: [{ type: header, properties: [...] }]` |
| `forge lint` warning: deprecated egress entries | Run `forge lint --fix` to auto-convert bare URL strings to `{ address: 'url' }` |
| `forge developer-spaces list` command not found | Does not exist in Forge CLI 12.x. Have user run `forge create` interactively to select a developer space |
| `forge create` fails with non-TTY error | `forge create` needs an interactive terminal — ask the user to run it; then write manifest and source files into the created directory |
| `onConnectionChange` not triggered | Verify admin clicked "Connect" in Atlassian Administration → Connected apps; run `forge tunnel` to confirm the function fires |
| Objects not appearing in Rovo Search | Wait ~5 minutes for indexing; run `forge logs -e development --since 15m` to check for `setObjects` errors |
| 403 on `@forge/teamwork-graph` calls | Ensure `read:object:jira`, `write:object:jira`, `delete:object:jira` are in manifest scopes, then redeploy and `forge install --upgrade` |
| `forge login` required | Create API token at https://id.atlassian.com/manage/api-tokens, then run `forge login` |

---

---

## Naming and Logo Guidelines

- Use the **official service name** as the connector name (e.g. `Google Drive`, not `Drive Connector by Acme`)
- Use the **official service logo** for icons — do not modify or combine with your own branding
- These guidelines apply only to the `graph:connector` module; your Forge app itself may use your own branding

