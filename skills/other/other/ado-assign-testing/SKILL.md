---
name: ado-assign-testing
description: Distribute reviewed work items to team members for testing
model: sonnet
---

# Testing Assignment Skill

Assign reviewed ADO work items to team members for testing. Distributes items evenly while respecting the rule: never assign to the person who resolved or reviewed the item.

## Arguments

- `--users "email1,email2,..."` - Comma-separated list of team member emails to receive assignments

## Process

### 1. Fetch Reviewed Items

```bash
curl -s http://localhost:3010/api/sprint/reviewed-items
```

Returns JSON with `sprintName` and `items[]` containing:
- `id`, `title`, `state`, `type`, `url`
- `assignedTo` - current assignee (skip if already set)
- `resolvedBy` - display name of resolver
- `reviewedBy` - display name of reviewer

### 2. Get Credentials from .env

Read `C:\dev\ai\orch\.env` for:
- `ADO_ORG` - Azure DevOps organization
- `ADO_PAT` - Personal access token
- `ADO_PROJECT` - Project name (e.g., BBNew)

### 3. Name-to-Email Mapping (Blue Billywig)

```javascript
const nameToEmail = {
  'Guido Hultink': 'g.hultink@bluebillywig.com',
  'Martijn Bots': 'm.bots@bluebillywig.com',
  'Janroel Koppen': 'j.koppen@bluebillywig.com',
  'Vincent van Laar': 'v.vanlaar@bluebillywig.com',
  'Jan ten Haaf': 'j.tenhaaf@bluebillywig.com',
  'Max Mulder': 'm.mulder@bluebillywig.com',
  'Simon Smulders': 's.smulders@bluebillywig.com',
  'Peter van der Spek': 'p.vanderspek@bluebillywig.com',
  'Olaf Timme': 'o.timme@bluebillywig.com'
};
```

### 4. Distribution Algorithm

Write a Node.js script in scratchpad:

```javascript
// Track assignments per user
const userCounts = {};
users.forEach(u => userCounts[u] = 0);

const assignments = [];
const skipped = [];

items.forEach(item => {
  // Skip items already assigned
  if (item.assignedTo) {
    skipped.push({id: item.id, reason: 'Already assigned to ' + item.assignedTo});
    return;
  }

  const resolverEmail = nameToEmail[item.resolvedBy] || '';
  const reviewerEmail = nameToEmail[item.reviewedBy] || '';

  // Filter eligible users (not resolver, not reviewer)
  const eligible = users.filter(u => u !== resolverEmail && u !== reviewerEmail);

  if (eligible.length === 0) {
    skipped.push({id: item.id, reason: 'No eligible users'});
    return;
  }

  // Pick user with fewest assignments
  eligible.sort((a, b) => userCounts[a] - userCounts[b]);
  const assignee = eligible[0];
  userCounts[assignee]++;

  assignments.push({id: item.id, assignee});
});
```

### 5. Execute Assignments

ADO API to update AssignedTo:

```javascript
async function assignItem(id, assignee) {
  const url = `https://dev.azure.com/${ADO_ORG}/${PROJECT}/_apis/wit/workitems/${id}?api-version=7.1`;
  const auth = Buffer.from(':' + ADO_PAT).toString('base64');

  const body = [{ op: 'replace', path: '/fields/System.AssignedTo', value: assignee }];

  const response = await fetch(url, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json-patch+json',
      'Authorization': `Basic ${auth}`
    },
    body: JSON.stringify(body)
  });

  return response.ok;
}
```

### 6. Report Results

Output markdown table:

```markdown
## Testing Assignment Complete

**Sprint:** [Sprint Name]
**Total Items:** N assigned
**Skipped:** N
**Users:** N

### Assignments by User
| User | Items | Work Item IDs |
|------|-------|---------------|
| user@example.com | 5 | #123, #456, ... |
```

## Rules

1. **Never assign to resolver** - The person in `resolvedBy` should not test their own work
2. **Never assign to reviewer** - The person in `reviewedBy` already reviewed it
3. **Even distribution** - Balance items across all eligible users
4. **Skip already assigned** - Items with `assignedTo` set are skipped
5. **Skip if impossible** - If all selected users are ineligible, skip the item

## Known Issues

- `reviewedBy` field requires `ADO_REVIEWED_BY_FIELD=Microsoft.VSTS.Common.ReviewedBy` in .env (NOT Custom.ReviewedBy)
- Server must be restarted after .env changes

## Example

```
/ado-assign-testing --users "g.hultink@bluebillywig.com,m.bots@bluebillywig.com,j.koppen@bluebillywig.com"
```
