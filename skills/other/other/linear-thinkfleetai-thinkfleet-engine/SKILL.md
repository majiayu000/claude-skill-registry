---
name: linear
description: "Manage Linear issues, projects, and cycles via the GraphQL API."
metadata: {"thinkfleetbot":{"emoji":"🔷","requires":{"bins":["curl","jq"],"env":["LINEAR_API_KEY"]}}}
---

# Linear

Manage Linear issues and projects via the GraphQL API.

## Environment Variables

- `LINEAR_API_KEY` - API key (generate at https://linear.app/settings/api)

## List issues

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"{ issues(first: 20) { nodes { id title state { name } assignee { name } priority } } }"}' | jq '.data.issues.nodes[] | {id, title, state: .state.name, assignee: .assignee.name, priority}'
```

## Create issue

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"mutation { issueCreate(input: { teamId: \"TEAM_ID\", title: \"Bug: Login broken\", description: \"Details here\", priority: 2 }) { success issue { id title url } } }"}' | jq '.data.issueCreate.issue'
```

## Update issue

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"mutation { issueUpdate(id: \"ISSUE_ID\", input: { stateId: \"STATE_ID\", priority: 1 }) { success issue { id title state { name } } } }"}' | jq '.data.issueUpdate.issue'
```

## List projects

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"{ projects(first: 20) { nodes { id name state } } }"}' | jq '.data.projects.nodes[] | {id, name, state}'
```

## List teams

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"{ teams { nodes { id name key } } }"}' | jq '.data.teams.nodes[] | {id, name, key}'
```

## Get issue

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"{ issue(id: \"ISSUE_ID\") { id title description state { name } assignee { name } priority labels { nodes { name } } } }"}' | jq '.data.issue'
```

## Add comment

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"mutation { commentCreate(input: { issueId: \"ISSUE_ID\", body: \"Comment text here\" }) { success comment { id body } } }"}' | jq '.data.commentCreate.comment'
```

## List cycles

```bash
curl -s -X POST -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.linear.app/graphql" \
  -d '{"query":"{ cycles(first: 10) { nodes { id name startsAt endsAt progress } } }"}' | jq '.data.cycles.nodes[] | {id, name, startsAt, endsAt, progress}'
```
