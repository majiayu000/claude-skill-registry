---
name: argocd
description: "Manage Argo CD applications and sync operations via the REST API."
metadata: {"thinkfleetbot":{"emoji":"🐙","requires":{"bins":["curl","jq"],"env":["ARGOCD_SERVER","ARGOCD_TOKEN"]}}}
---

# Argo CD

Manage Argo CD applications, sync operations, and clusters via the REST API.

## Environment Variables

- `ARGOCD_SERVER` - Argo CD server URL (e.g. `https://argocd.example.com`)
- `ARGOCD_TOKEN` - Bearer token (generate via `argocd account generate-token` or API)

## List applications

```bash
curl -sk -H "Authorization: Bearer $ARGOCD_TOKEN" \
  "$ARGOCD_SERVER/api/v1/applications" | jq '.items[] | {name: .metadata.name, status: .status.sync.status, health: .status.health.status, repo: .spec.source.repoURL}'
```

## Get application details

```bash
curl -sk -H "Authorization: Bearer $ARGOCD_TOKEN" \
  "$ARGOCD_SERVER/api/v1/applications/my-app" | jq '{name: .metadata.name, sync: .status.sync, health: .status.health, source: .spec.source}'
```

## Sync application

```bash
curl -sk -X POST -H "Authorization: Bearer $ARGOCD_TOKEN" \
  -H "Content-Type: application/json" \
  "$ARGOCD_SERVER/api/v1/applications/my-app/sync" \
  -d '{}' | jq '{phase: .status.phase}'
```

## Sync with specific revision

```bash
curl -sk -X POST -H "Authorization: Bearer $ARGOCD_TOKEN" \
  -H "Content-Type: application/json" \
  "$ARGOCD_SERVER/api/v1/applications/my-app/sync" \
  -d '{"revision": "HEAD", "prune": true}' | jq '{phase: .status.phase}'
```

## Get application resource tree

```bash
curl -sk -H "Authorization: Bearer $ARGOCD_TOKEN" \
  "$ARGOCD_SERVER/api/v1/applications/my-app/resource-tree" | jq '.nodes[] | {kind: .kind, name: .name, health: .health.status}'
```

## List clusters

```bash
curl -sk -H "Authorization: Bearer $ARGOCD_TOKEN" \
  "$ARGOCD_SERVER/api/v1/clusters" | jq '.items[] | {name: .name, server: .server, status: .connectionState.status}'
```

## List repositories

```bash
curl -sk -H "Authorization: Bearer $ARGOCD_TOKEN" \
  "$ARGOCD_SERVER/api/v1/repositories" | jq '.items[] | {repo: .repo, connectionState: .connectionState.status}'
```

## Application diff (managed resources)

```bash
curl -sk -H "Authorization: Bearer $ARGOCD_TOKEN" \
  "$ARGOCD_SERVER/api/v1/applications/my-app/managed-resources" | jq '.items[] | {kind, name: .name, status: .status}'
```

## Notes

- Use `-k` flag if Argo CD uses self-signed certificates.
- Sync operations are async; poll application status to track progress.
- Always confirm before syncing, especially with `prune: true`.
