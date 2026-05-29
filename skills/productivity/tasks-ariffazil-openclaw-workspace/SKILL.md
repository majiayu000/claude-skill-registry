---
name: tasks
description: Task & project management — GitHub Projects (native), Linear (API), Notion DB (API)
user-invocable: true
---

# Tasks & Projects Skill — arifOS_bot

Triggers: "task", "todo", "create task", "project", "kanban", "issue", "sprint",
          "what are my tasks", "add to backlog", "close task", "task status",
          "linear", "github project", "my tasks"

---

## Option Comparison

| Tool | Status | Best for | Cost |
|------|--------|----------|------|
| **GitHub Projects** | ✅ Ready (GH_TOKEN set) | Code-linked tasks, arifOS issues | Free |
| **Notion Database** | ⚠️ Need NOTION_API_KEY | Notes + tasks in one place | Free tier |
| **Linear** | ⚠️ Need LINEAR_API_KEY | Engineering sprints, roadmaps | You have it |

**Recommendation for Arif:** GitHub Projects for code work (zero new keys), Notion DB for life/PKM tasks (one integration token). Linear if you want structured sprints.

---

## GitHub Projects (Ready — No Setup Needed)

Uses `gh` CLI with existing `GITHUB_TOKEN`. GitHub Issues + Projects V2 board.

### Create an issue (= task)
```bash
gh issue create -R ariffazil/arifOS \
  --title "Task title" \
  --body "Description and acceptance criteria" \
  --label "enhancement" \
  --assignee ariffazil
```

### List my open tasks
```bash
gh issue list -R ariffazil/arifOS \
  --assignee ariffazil \
  --state open \
  --limit 20 \
  --json number,title,labels,createdAt \
  | python3 -c "
import sys, json
issues = json.load(sys.stdin)
for i in issues:
    labels = ','.join([l['name'] for l in i['labels']]) or '-'
    print(f\"#{i['number']:4} [{labels:20}] {i['title']}\")
"
```

### Update task status (via label)
```bash
gh issue edit 42 -R ariffazil/arifOS --add-label "in-progress"
gh issue edit 42 -R ariffazil/arifOS --remove-label "todo" --add-label "done"
gh issue close 42 -R ariffazil/arifOS --comment "Completed"
```

### View project board (GitHub Projects V2)
```bash
# List your projects
gh project list --owner ariffazil

# Add issue to project
gh project item-add PROJECT_NUMBER --owner ariffazil --url https://github.com/ariffazil/arifOS/issues/42

# List project items
gh project item-list PROJECT_NUMBER --owner ariffazil --format json \
  | python3 -c "import sys,json; [print(i.get('title','?'),'-',i.get('status','?')) for i in json.load(sys.stdin).get('items',[])]"
```

---

## Linear (GraphQL API)

### ⚙️ Setup (one-time)
```bash
# 1. Get API key: https://linear.app/settings/api → Personal API Keys
# 2. Add to VPS:
echo 'LINEAR_API_KEY=lin_api_YOUR_KEY_HERE' >> /srv/arifOS/.env
docker compose up -d --force-recreate openclaw
```

### My assigned issues
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: ${LINEAR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { viewer { assignedIssues(first: 20, filter: {state: {type: {nin: [\"completed\",\"cancelled\"]}}}) { nodes { id title priority state { name } team { name } dueDate } } } }"
  }' | python3 -c "
import sys, json
d = json.load(sys.stdin)
issues = d['data']['viewer']['assignedIssues']['nodes']
for i in issues:
    priority = ['', 'Urgent', 'High', 'Med', 'Low'][i.get('priority',0)] if i.get('priority') else '-'
    print(f\"[{priority:6}] [{i['state']['name']:15}] {i['title']}\")
"
```

### Create issue
```bash
# First get team ID
TEAM_ID=$(curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: ${LINEAR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { teams { nodes { id name } } }"}' \
  | python3 -c "import sys,json; teams=json.load(sys.stdin)['data']['teams']['nodes']; print(teams[0]['id'])")

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: ${LINEAR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"mutation CreateIssue(\$input: IssueCreateInput!) { issueCreate(input: \$input) { success issue { id title } } }\",
    \"variables\": {
      \"input\": {
        \"teamId\": \"${TEAM_ID}\",
        \"title\": \"Task title here\",
        \"description\": \"Details here\",
        \"priority\": 3
      }
    }
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Created:', d['data']['issueCreate']['issue']['title'])"
```

### Update issue state
```bash
ISSUE_ID="YOUR-ISSUE-ID"
# Get state IDs first
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: ${LINEAR_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { workflowStates { nodes { id name } } }"}' \
  | python3 -c "import sys,json; [print(s['name'],':',s['id']) for s in json.load(sys.stdin)['data']['workflowStates']['nodes']]"
```

---

## Notion as Task Manager

If you prefer Notion databases as your kanban board (uses `NOTION_API_KEY` from Notion skill):

```bash
# Requires: NOTION_API_KEY + a Notion DB with Status property
TASKS_DB_ID="YOUR-NOTION-TASKS-DB-ID"

# List Todo tasks
curl -s -X POST "https://api.notion.com/v1/databases/${TASKS_DB_ID}/query" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter":{"property":"Status","select":{"equals":"Todo"}},"page_size":20}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for row in d['results']:
    props = row['properties']
    for k, v in props.items():
        if v.get('type') == 'title':
            title = ''.join([t['plain_text'] for t in v['title']])
            print(f'  • {title}')
"

# Add task
curl -s -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"database_id\": \"${TASKS_DB_ID}\"},
    \"properties\": {
      \"Name\": {\"title\": [{\"text\": {\"content\": \"New task here\"}}]},
      \"Status\": {\"select\": {\"name\": \"Todo\"}}
    }
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Task created:', d.get('id'))"
```

---

## arifOS_bot Default Workflow

When Arif says "add task" or "create task" without specifying:
1. If code/infra-related → GitHub Issue on `ariffazil/arifOS`
2. If life/PKM-related → Notion database (if NOTION_API_KEY set)
3. If sprint/roadmap → Linear (if LINEAR_API_KEY set)

*arifOS_bot — Tasks via GitHub Projects (native) + Linear + Notion*
