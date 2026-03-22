---
name: sync-ado-repos
description: Sync GitHub repos from bluebillywig org to an ADO "Repository" picklist field on all work item types
model: sonnet
---

# Sync GitHub Repos to ADO Picklist

Fetches all repos from `github.com/bluebillywig` and creates/updates a `Custom.Repository` picklist field on all work item types across all inherited processes in Azure DevOps.

## Process

Write and execute a Node.js script (temp file, delete after). Use built-in `fetch` (Node 18+).

**Auth headers:**
- GitHub: `Authorization: Bearer {GITHUB_TOKEN}`
- ADO: `Authorization: Basic {base64(':' + ADO_PAT)}`

**ADO API version:** `7.1` for all calls except field creation (`4.1-preview.1`) and project properties (`7.1-preview.1`).

### 1. Read credentials from `.env`

Parse `C:\dev\ai\orch\.env` for `ADO_ORG`, `ADO_PAT`, `GITHUB_TOKEN`. Use `fs.readFileSync` with line parsing (split on `=`, trim, strip quotes). Last value wins for duplicate keys.

### 2. Fetch all repos from `github.com/bluebillywig`

```
GET https://api.github.com/orgs/bluebillywig/repos?per_page=100&page=N
```

Paginate until empty page. Extract `.name`, sort alphabetically, log count.

### 3. Find or create/update picklist

First check if `Custom.Repository` field exists and read its `picklistId`:
```
GET https://dev.azure.com/{org}/_apis/wit/fields/Custom.Repository?api-version=7.1
```

If no picklist ID from field, search all picklists for one named "Repository":
```
GET https://dev.azure.com/{org}/_apis/work/processes/lists?api-version=7.1
```

**Create** (if not found -- include `name`!):
```
POST .../lists?api-version=7.1
Body: { "name": "Repository", "type": "String", "items": [...repos], "isSuggested": true }
```

**Update** (if found):
```
PUT .../lists/{listId}?api-version=7.1
Body: { "id": "{listId}", "items": [...repos], "isSuggested": true }
```

### 4. Get all inherited processes and their WITs

```
GET https://dev.azure.com/{org}/_apis/work/processes?$expand=projects&api-version=7.1
```

Filter to `customizationType === 'inherited'`. The `$expand=projects` parameter includes which projects use each process. For EACH inherited process, fetch WITs:

```
GET https://dev.azure.com/{org}/_apis/work/processes/{processId}/workitemtypes?api-version=7.1
```

### 5. Create field if it doesn't exist

If step 3's field check returned 404, create the field. Use the older `processdefinitions` API with `type: "string"` (NOT `"picklistString"`):
```
POST https://dev.azure.com/{org}/_apis/work/processdefinitions/{processId}/fields?api-version=4.1-preview.1
Body: { "name": "Repository", "type": "string", "pickList": { "id": "{picklistId}" } }
```

The `type` must be `"string"` — the picklist binding is what makes it a picklist field. Using `"picklistString"` causes `FieldTypeInvalid`.

### 6. Add field to all work item types

For each WIT, check `wit.customization`:

**If `customization !== 'system'`** (already derived/custom): add field directly:
```
POST .../processes/{processId}/workItemTypes/{witRefName}/fields?api-version=7.1
Body: { "referenceName": "Custom.Repository" }
```

**If `customization === 'system'`** (not yet derived): skip — the REST API cannot derive a WIT with the same name as the system parent. These require manual derivation via the ADO UI.

- Ignore **409** (field already added)
- Skip Test Case/Test Plan/Test Suite — system-only types that don't accept custom fields

### 7. Add control to form layout (CRITICAL)

**Adding a field to a WIT does NOT make it visible on the form.** You must also add a control to the WIT's layout.

For each WIT where the field was added:

1. Get the layout:
```
GET .../processes/{processId}/workItemTypes/{witRefName}/layout?api-version=7.1
```

2. Check if `Custom.Repository` control already exists (scan all pages/sections/groups/controls for `ctrl.id === 'Custom.Repository'`).

3. Find a suitable group on the "Details" page. Prefer groups labeled "Details" or "Classification". **Avoid groups that already contain an `HtmlFieldControl`** — ADO allows only one HTML control per group (error VS403105).

4. If the first group fails with 500 (HTML control conflict), find another group without HTML controls.

5. If an existing plain control exists, remove it first:
```
DELETE .../processes/{processId}/workItemTypes/{witRefName}/layout/groups/{groupId}/controls/Custom.Repository?api-version=7.1
```

6. Add the control as a **multivalue contribution** (same pattern as `Custom.BusinessUnit` / "Business Unit(s)"). This uses the already-installed `ms-devlabs.vsts-extensions-multivalue-control` extension:
```
POST .../processes/{processId}/workItemTypes/{witRefName}/layout/groups/{groupId}/controls?api-version=7.1
Body: {
  "id": "Custom.Repository",
  "label": "Repository",
  "visible": true,
  "readOnly": false,
  "isContribution": true,
  "contribution": {
    "contributionId": "ms-devlabs.vsts-extensions-multivalue-control.multivalue-form-control",
    "inputs": { "FieldName": "Custom.Repository" }
  }
}
```

### 8. Report

Output markdown summary: repos synced, picklist created vs updated, processes and WITs updated vs skipped, controls added to layout. Include reminder to install [Multivalue control extension](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.vsts-extensions-multivalue-control) for multi-select.

## Known Limitations

- **System WITs** (`customization: system`): cannot add fields or layout controls via API. Open ADO UI > Process > click the WIT to auto-derive, then re-run.
- **Test Case/Plan/Suite**: locked system types across all processes, skip these.
- **Field type**: must use `"string"` (not `"picklistString"`) in the `processdefinitions` API.
- **HTML control conflict**: each layout group allows only one HTML control. If a group already has one, pick a different group.
- **Picklist creation**: must include `name` field in POST body or API returns 400.
- **Multivalue extension**: `ms-devlabs.vsts-extensions-multivalue-control` is already installed in the org. The field type is identical to a regular picklist string — multi-select is purely a layout control concern (use `isContribution: true` with the extension's `contributionId`).
- **isSuggested must be true**: The multivalue control stores values as semicolons-separated (e.g., `foo;bar`). If `isSuggested: false`, ADO validates the combined string against individual picklist items and rejects it. Use `isSuggested: true` so values are suggestions, not enforced.

## Important Notes

- Handle errors gracefully -- if one WIT rejects the field, log and continue
- Run with `node.exe` directly to avoid Git Bash shell issues
- Delete temp script after execution

## Verification

1. ADO > Project Settings > Process > Work item type -- verify "Repository" field exists
2. Open a work item -- confirm repo dropdown shows all bluebillywig repos
3. If multi-select needed: install Multivalue control extension
