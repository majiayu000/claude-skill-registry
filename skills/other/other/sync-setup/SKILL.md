---
description: Interactive sync setup wizard that configures GitHub, JIRA, and/or ADO integration in one guided flow. Use when saying "setup sync", "configure sync", "connect to jira", "connect to github", or "sync-setup".
---

# Sync Setup Wizard

Interactive skill that configures SpecWeave's external sync in one guided flow.

## Workflow

### Step 1: Provider Selection

Ask the user which providers to enable:

```
AskUserQuestion: "Which external platforms do you want to sync with?"
Options: GitHub, JIRA, Azure DevOps (multiSelect: true)
```

### Step 2: Credentials (per provider)

**GitHub**:
1. Check `gh auth status` — if authenticated, use existing token
2. If not, ask for GITHUB_TOKEN
3. Ask for owner/repo (or auto-detect from git remote)

**JIRA**:
1. Ask for JIRA domain (e.g., `company.atlassian.net`)
2. Ask for email
3. Ask for API token (from https://id.atlassian.com/manage/api-tokens)
4. Ask for project key
5. Validate: `curl -u email:token https://domain/rest/api/3/myself`

**Azure DevOps**:
1. Ask for organization name
2. Ask for project name
3. Ask for PAT (from https://dev.azure.com/org/_usersSettings/tokens)
4. Validate: `curl -u :PAT https://dev.azure.com/org/_apis/projects/project?api-version=7.1`

### Step 3: Permission Preset

```
AskUserQuestion: "What sync permissions do you want?"
Options:
- read-only: Only pull changes from external tools
- push-only: Only push SpecWeave changes to external tools
- bidirectional (Recommended): Both push and pull
- full-control: Everything including delete
```

### Step 4: Hierarchy Detection (JIRA/ADO only)

For JIRA and ADO, auto-detect the hierarchy:

```typescript
// Use the new SyncEngine to detect hierarchy
const engine = new SyncEngine({ permissions: resolvePermissions('read-only') });
engine.registerProvider(adapter);
const hierarchy = await engine.detectHierarchy(platform);
```

Show detected mapping and ask for confirmation:

```
AskUserQuestion: "Detected hierarchy pattern: [pattern]. Is this correct?"
Options: Yes, use detected mapping | No, let me customize | Use flat mapping
```

### Step 5: GitHub Projects v2 (GitHub only)

```
AskUserQuestion: "Do you want to sync with a GitHub Project board?"
Options: Yes, select a project | No, just Issues + Labels
```

If yes, list available projects and ask which one.

### Step 6: Write Config

Write the following:

1. **`.env`** — Add credentials (JIRA_API_TOKEN, JIRA_EMAIL, AZURE_DEVOPS_PAT, etc.)
2. **`.specweave/config.json`** — Update sync section:

```json
{
  "sync": {
    "enabled": true,
    "preset": "bidirectional",
    "github": { "enabled": true, "owner": "...", "repo": "..." },
    "jira": { "enabled": true, "domain": "...", "projectKey": "..." },
    "ado": { "enabled": true, "organization": "...", "project": "..." }
  }
}
```

### Step 7: Dry Run

Run a test sync (read-only) to verify configuration:

```bash
# Test each enabled provider
node -e "
  import { SyncEngine } from './src/sync/engine.js';
  import { GitHubAdapter } from './src/sync/providers/github.js';
  // ... test connection for each provider
"
```

Report results and confirm setup is complete.

## Key Principles

- **Never commit secrets**: Credentials go in `.env` only
- **Validate before saving**: Test API calls before writing config
- **Safe defaults**: Default to `bidirectional` preset (no delete)
- **User confirmation**: Always confirm detected hierarchy
