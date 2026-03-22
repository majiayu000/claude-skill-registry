---
name: ado-investigate
description: Use when investigating an ADO ticket to identify which GitHub repos are relevant, populate the Repository field, and append AI analysis to the description. Triggers on "investigate ticket", "analyze ticket", "find repos for ticket", or "enrich ticket".
model: sonnet
---

# Investigate ADO Ticket

Fetch ADO ticket → score bluebillywig GitHub repos → update `Custom.Repository` field → append AI analysis to description.

> **Read `~/.claude/skills/_ado-shared.md`** for auth, env vars, fetch ticket, write-payload, and Windows/MSYS2 patterns.

## Workflow

1. Fetch ticket + current field values
2. Fetch non-archived repos from bluebillywig org
3. Score repos against ticket content
4. Read READMEs for uncertain top candidates
5. Update ticket: Repository field + description appendix

---

## Step 1: Fetch Ticket

Use fetch with `$expand=all` (see shared). Extract and note:
- `System.Title`
- `System.Description` (HTML — strip tags for keyword analysis)
- `System.WorkItemType`, `System.AreaPath`
- `Custom.Repository` — **preserve existing values** when updating
- `Microsoft.VSTS.Common.AcceptanceCriteria` if set

---

## Step 2: Fetch GitHub Repos

**Skip this step** — `docs/bluebillywig-repos.md` already has all active repos. Only fetch live if you suspect the list is stale (>2 weeks old):

```bash
gh repo list bluebillywig --limit 100 --json name,description,repositoryTopics,isArchived \
  > /tmp/repos-raw.json
node << 'NS'
const raw = require('fs').readFileSync(require('os').tmpdir() + '/repos-raw.json', 'utf8');
const filtered = JSON.parse(raw).filter(r => !r.isArchived);
console.log(JSON.stringify(filtered, null, 2));
NS
```

---

## Step 3: Score Repos

**First**: read `C:\dev\ai\orch\docs\bluebillywig-repos.md` — describes every active repo with keyword→repo scoring guide.

Extract keywords from ticket (title + stripped description + area path):

| Signal | Points |
|--------|--------|
| Repo name word in title | +40 |
| Repo name word in description | +20 |
| Topic matches ticket keyword | +20 each |
| Description word overlap | +5 per keyword |
| Area path segment matches repo name | +15 |

Include repos scoring >30 pts, max 3. If top candidates <60 pts, fetch README:

```bash
gh repo view bluebillywig/<repo> --json readme --jq '.readme.text' | head -c 3000
```

---

## Step 4: Update Repository Field

`Custom.Repository` is semicolon-separated. Merge with existing — never overwrite blindly.

```bash
node << 'NS'
const fp = require('path').join(require('os').tmpdir(), 'ado-payload.json');
const existing = 'EXISTING_VALUE_OR_EMPTY';   // from Step 1
const toAdd = ['repo-a', 'repo-b'];
const merged = [...new Set([...existing.split(';').filter(Boolean), ...toAdd])].join(';');
require('fs').writeFileSync(fp, JSON.stringify([
  { op: 'replace', path: '/fields/Custom.Repository', value: merged }
]));
NS
```

Then PATCH via shared write-payload pattern.

---

## Step 5: Append Analysis to Description

Append to `System.Description` — never replace the full existing content.

```html
<hr>
<p><strong>[AI Investigation – YYYY-MM-DD]</strong></p>
<p><strong>Relevant repos:</strong></p>
<ul>
  <li><strong>repo-name</strong> — reason (e.g. "name matches 'player', has 'video' topic")</li>
</ul>
<p><strong>Suggested approach:</strong> 1–2 sentence implementation hint.</p>
```

Then PATCH via shared write-payload pattern (append to existing description HTML).

---

## Output to User

```
## Investigation: ADO #<ID> — <title>

**Repos identified:**
- repo-a (85% — "player" in name + video topics)
- repo-b (60% — area path "Core" matches)

**Ticket updated:**
- ✅ Custom.Repository: repo-a;repo-b
- ✅ Description: AI analysis section appended

**Suggested approach:** <1–2 sentences>
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Overwriting existing repos | Read `Custom.Repository` first, merge with new values |
| Replacing full description | Fetch current `System.Description`, append only |
| Including archived repos | Filter `isArchived == false` from `gh repo list` |
| Guessing repo names | Names from `gh repo list` are the exact picklist values — use as-is |
| `topics` field in `gh repo list` | Wrong field name — use `repositoryTopics` |
| `--order` flag in `gh repo list` | Flag doesn't exist — omit it |
