---
name: wrike
description: Manage projects, tasks, and workflows via Wrike API. Create tasks, update statuses, and track work.
metadata: {"clawdbot":{"emoji":"📊","requires":{"env":["WRIKE_ACCESS_TOKEN"]}}}
---
# Wrike
Project management platform.
## Environment
```bash
export WRIKE_ACCESS_TOKEN="xxxxxxxxxx"
```
## List Folders
```bash
curl "https://www.wrike.com/api/v4/folders" -H "Authorization: Bearer $WRIKE_ACCESS_TOKEN"
```
## Create Task
```bash
curl -X POST "https://www.wrike.com/api/v4/folders/{folderId}/tasks" \
  -H "Authorization: Bearer $WRIKE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "status": "Active"}'
```
## List Tasks
```bash
curl "https://www.wrike.com/api/v4/tasks" -H "Authorization: Bearer $WRIKE_ACCESS_TOKEN"
```
## Links
- Docs: https://developers.wrike.com
