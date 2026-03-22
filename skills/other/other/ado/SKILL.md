---
name: ado
description: Generic Azure DevOps operations — edit tickets, query work items, add comments, change fields, move sprints, assign users, link items, and more. Triggers on "ado", "edit ticket", "update ticket", "move ticket", "assign ticket", "link ticket", "query ado", "search ado", "add comment to ticket", or ticket number mentions with edit/update intent.
model: sonnet
---

# ADO — Generic Azure DevOps Operations

Perform any Azure DevOps operation: edit fields, add comments, query/search work items, manage links, move sprints, assign users, etc.

> **Read `~/.claude/skills/_ado-shared.md`** for auth, env vars, fetch/update ticket patterns, and Windows/MSYS2 notes.

## Argument Parsing

The user's input may contain:
- **Ticket number**: `#12345`, `12345`, `ADO 12345`, `ticket 12345`
- **Field changes**: `set state to resolved`, `assign to user@email.com`, `change title to "..."`
- **Comments**: `add comment "..."`, `comment on ticket`
- **Queries**: `find tickets assigned to me`, `search for X`, `list bugs in current sprint`
- **Links**: `link 12345 to 12346`, `add parent 12300`

Extract the intent and parameters before executing.

---

## Defaults

- **Area Path**: Always use `BBNew\Core` unless the user explicitly specifies a different area path.

---

## Operations

### 1. Edit Fields

Fetch ticket first (to preserve existing values), then PATCH:

```bash
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
# Fetch current values
curl -s -H "Authorization: Basic $B64" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/<ID>?api-version=7.0"
```

Common fields and their API paths:

| Field | Path | Example Values |
|-------|------|----------------|
| Title | `/fields/System.Title` | Any string |
| State | `/fields/System.State` | `New`, `In Progress`, `Resolved`, `Closed` |
| Assigned To | `/fields/System.AssignedTo` | Email address |
| Area Path | `/fields/System.AreaPath` | **Default: `BBNew\Core`** |
| Iteration Path | `/fields/System.IterationPath` | `BBNew\Sprints 2026\Q1\Sprint 8.45` |
| Description | `/fields/System.Description` | HTML string |
| Tags | `/fields/System.Tags` | Semicolon-separated: `tag1; tag2` |
| Priority | `/fields/Microsoft.VSTS.Common.Priority` | `1`, `2`, `3`, `4` |
| Severity | `/fields/Microsoft.VSTS.Common.Severity` | `1 - Critical`, `2 - High`, `3 - Medium`, `4 - Low` |
| Test Notes | `/fields/BB.Testnotes` | HTML string |
| Repository | `/fields/Custom.Repository` | Semicolon-separated repo names |
| Resolution | `/fields/Microsoft.VSTS.Common.Resolution` | HTML string (usually PR link) |
| Effort | `/fields/Microsoft.VSTS.Scheduling.Effort` | Numeric (story points / effort hours) |
| Remaining Work | `/fields/Microsoft.VSTS.Scheduling.RemainingWork` | Numeric (hours) |

Use write-payload pattern from shared (node heredoc + cygpath + curl PATCH).

For HTML fields (Description, Test Notes): **always fetch existing value first and append/merge** — never blindly replace.

### 2. Add Comment

```bash
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
node << 'NS'
const fp = require('path').join(require('os').tmpdir(), 'ado-payload.json');
require('fs').writeFileSync(fp, JSON.stringify({ text: '<p>COMMENT_HTML</p>' }));
NS
WINPATH=$(cygpath -w "$LOCALAPPDATA/Temp/ado-payload.json")
curl -s -H "Authorization: Basic $B64" -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/<ID>/comments?api-version=7.0-preview.3" \
  -d @"$WINPATH"
```

### 3. Query Work Items (WIQL)

```bash
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
node << 'NS'
const fp = require('path').join(require('os').tmpdir(), 'ado-payload.json');
require('fs').writeFileSync(fp, JSON.stringify({
  query: "SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo] FROM workitems WHERE [System.TeamProject] = 'BBNew' AND <CONDITIONS> ORDER BY [System.Id] DESC"
}));
NS
WINPATH=$(cygpath -w "$LOCALAPPDATA/Temp/ado-payload.json")
curl -s -H "Authorization: Basic $B64" -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/wiql?api-version=7.0&\$top=50" \
  -d @"$WINPATH"
```

WIQL returns only IDs. Fetch details in batch:

```bash
# Extract IDs and fetch batch (max 200)
curl -s -H "Authorization: Basic $B64" -X POST \
  -H "Content-Type: application/json" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitemsbatch?api-version=7.0" \
  -d @"$WINPATH"
```

Batch payload: `{ "ids": [1,2,3], "fields": ["System.Id","System.Title","System.State","System.AssignedTo"] }`

Common WIQL conditions:

| Intent | WIQL Condition |
|--------|---------------|
| Assigned to me | `[System.AssignedTo] = @Me` |
| Assigned to user | `[System.AssignedTo] = 'email@example.com'` |
| Current sprint | `[System.IterationPath] = @CurrentIteration` |
| State filter | `[System.State] = 'In Progress'` |
| Bugs only | `[System.WorkItemType] = 'Bug'` |
| Title contains | `[System.Title] CONTAINS 'search term'` |
| Tag filter | `[System.Tags] CONTAINS 'tag-name'` |
| Area path | `[System.AreaPath] UNDER 'BBNew\Core'` |
| Created recently | `[System.CreatedDate] >= @Today - 7` |

### 4. Add/Remove Links

Link types:
- `System.LinkTypes.Hierarchy-Forward` — Parent → Child
- `System.LinkTypes.Hierarchy-Reverse` — Child → Parent
- `System.LinkTypes.Related` — Related

```bash
node << 'NS'
const fp = require('path').join(require('os').tmpdir(), 'ado-payload.json');
require('fs').writeFileSync(fp, JSON.stringify([
  {
    op: 'add',
    path: '/relations/-',
    value: {
      rel: 'System.LinkTypes.Related',
      url: 'https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/TARGET_ID'
    }
  }
]));
NS
WINPATH=$(cygpath -w "$LOCALAPPDATA/Temp/ado-payload.json")
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
curl -s -H "Authorization: Basic $B64" -X PATCH \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/<ID>?api-version=7.0" \
  -d @"$WINPATH"
```

To remove a link: fetch ticket with `$expand=relations`, find the relation index, then:
```json
[{ "op": "remove", "path": "/relations/<INDEX>" }]
```

### 5. Move to Sprint

Fetch current sprint path first if needed (see shared), then update Iteration Path:

```json
[{ "op": "replace", "path": "/fields/System.IterationPath", "value": "BBNew\\Sprints 2026\\Q1\\Sprint 8.45" }]
```

### 6. Create New Work Item

```bash
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
node << 'NS'
const fp = require('path').join(require('os').tmpdir(), 'ado-payload.json');
require('fs').writeFileSync(fp, JSON.stringify([
  { op: 'add', path: '/fields/System.Title', value: 'TITLE' },
  { op: 'add', path: '/fields/System.AreaPath', value: 'BBNew\\Core' },  // ALWAYS default to BBNew\Core
  { op: 'add', path: '/fields/System.Description', value: '<p>DESCRIPTION</p>' }
]));
NS
WINPATH=$(cygpath -w "$LOCALAPPDATA/Temp/ado-payload.json")
curl -s -H "Authorization: Basic $B64" -X POST \
  -H "Content-Type: application/json-patch+json" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/\$Task?api-version=7.0" \
  -d @"$WINPATH"
```

Replace `$Task` with: `$Bug`, `$User%20Story`, `$Feature`, `$Epic`, etc.

### 7. Bulk Operations

For updating multiple tickets, loop through IDs:

```bash
for ID in 12345 12346 12347; do
  # ... PATCH each
done
```

---

## Output Format

After any operation, report concisely:

```
## ADO #<ID> — <title>

**Action:** <what was done>
- ✅ <field>: <old value> → <new value>
- ✅ Comment added
- ✅ Linked to #<other>

[View ticket](https://dev.azure.com/bluebillywig/BBNew/_workitems/edit/<ID>)
```

For queries:

```
## ADO Query Results

| # | Title | State | Assigned To |
|---|-------|-------|-------------|
| 12345 | Fix the thing | In Progress | user@email.com |
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Replacing HTML fields blindly | Always fetch existing value first, append/merge |
| Using `curl -u` | Use manual base64 auth header (see shared) |
| Inline `-d` with HTML | Write to temp file via node heredoc |
| Wrong `op` on create vs update | `add` for POST (new), `replace` for PATCH (existing) |
| Forgetting `$expand=all` | Add when you need relations/comments |
| WIQL `@Me` not working | Only works with authenticated user; use explicit email for curl |
| Escaping `$` in work item type URL | Use `\$Task` in bash to prevent variable expansion |
| Setting AreaPath to `BBNew` | Always use `BBNew\Core` (not root `BBNew`) |
