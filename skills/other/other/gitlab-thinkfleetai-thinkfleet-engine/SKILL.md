---
name: gitlab
description: "Manage GitLab projects, merge requests, pipelines, and issues via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🦊","requires":{"bins":["curl","jq"],"env":["GITLAB_URL","GITLAB_TOKEN"]}}}
---

# GitLab

Manage GitLab projects, merge requests, pipelines, and issues via the REST API.

## Environment Variables

- `GITLAB_URL` - GitLab instance URL (e.g. `https://gitlab.com` or self-hosted)
- `GITLAB_TOKEN` - Personal access token or project token

## List projects

```bash
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects?membership=true&per_page=20&order_by=last_activity_at" | jq '.[] | {id, name: .path_with_namespace, default_branch}'
```

## Get project details

```bash
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/123" | jq '{id, name: .path_with_namespace, default_branch, web_url}'
```

## List merge requests

```bash
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/123/merge_requests?state=opened&per_page=10" | jq '.[] | {iid, title, author: .author.username, source_branch, target_branch}'
```

## Create merge request

```bash
curl -s -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/123/merge_requests" \
  -d '{
    "source_branch": "feature-branch",
    "target_branch": "main",
    "title": "Add new feature",
    "description": "Description here"
  }' | jq '{iid, web_url}'
```

## List pipelines

```bash
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/123/pipelines?per_page=10" | jq '.[] | {id, status, ref, created_at}'
```

## Trigger pipeline

```bash
curl -s -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/123/pipeline" \
  -d '{"ref": "main"}' | jq '{id, status, web_url}'
```

## Get pipeline jobs

```bash
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/123/pipelines/456/jobs" | jq '.[] | {id, name, stage, status, duration}'
```

## List issues

```bash
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/123/issues?state=opened&per_page=10" | jq '.[] | {iid, title, state, assignee: .assignee.username}'
```

## Create issue

```bash
curl -s -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/123/issues" \
  -d '{"title": "Bug report", "description": "Details here", "labels": "bug"}' | jq '{iid, web_url}'
```

## Get job log

```bash
curl -s -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/123/jobs/789/trace" | tail -50
```

## Notes

- Project ID can be numeric or URL-encoded path (e.g. `mygroup%2Fmyproject`).
- Use `per_page` and `page` query params for pagination.
- Rate limits: 300 requests/min for authenticated requests on gitlab.com.
- Always confirm before creating MRs, triggering pipelines, or modifying issues.
