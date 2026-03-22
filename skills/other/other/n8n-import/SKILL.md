---
name: n8n-import
description: Import n8n workflows from infrastructure/n8n/workflows/ into the running GKE pod in fenrir-marketing namespace. Use when the user says '/n8n-import', 'import n8n workflows', 'push workflows to n8n', 'deploy n8n workflow', or 'install workflow on n8n'.
argument-hint: "[workflow-file.json]"
allowed-tools: Bash, Read, Glob
---

# n8n Workflow Import

Import n8n workflow JSON files from the local repository into the running n8n pod on GKE.

This is the inverse of `/n8n-commit` (which exports from the pod to git).

## Workflow

When invoked, follow these steps exactly:

### 1. Find the n8n pod

```bash
N8N_POD=$(kubectl get pods -n fenrir-marketing -l app.kubernetes.io/name=n8n,app.kubernetes.io/component=main -o jsonpath='{.items[0].metadata.name}')
echo "n8n pod: $N8N_POD"
```

If no pod is found or the command fails, stop immediately and report that the n8n pod is not running in the `fenrir-marketing` namespace. Suggest checking cluster connectivity with `kubectl cluster-info`.

### 2. Determine which workflows to import

- If `$ARGUMENTS` specifies a filename (e.g., `gmail-reddit-monitor.json`), import only that file from `infrastructure/n8n/workflows/`.
- If no argument is provided, import ALL `.json` files from `infrastructure/n8n/workflows/`.
- Validate that each file exists locally before proceeding. If a specified file does not exist, stop and report the missing file. List available workflow files to help the user.

### 3. Create temp directory on pod

```bash
kubectl exec -n fenrir-marketing "$N8N_POD" -- mkdir -p /tmp/n8n-import
```

### 4. Copy workflow files to the pod

For each workflow file:

```bash
kubectl cp "infrastructure/n8n/workflows/<file>.json" "fenrir-marketing/$N8N_POD:/tmp/n8n-import/<file>.json"
```

### 5. Import workflows using n8n CLI

For a single file:

```bash
kubectl exec -n fenrir-marketing "$N8N_POD" -- n8n import:workflow --input=/tmp/n8n-import/<file>.json
```

For all files (directory mode):

```bash
kubectl exec -n fenrir-marketing "$N8N_POD" -- n8n import:workflow --input=/tmp/n8n-import/
```

### 6. Clean up temp files on pod

```bash
kubectl exec -n fenrir-marketing "$N8N_POD" -- rm -rf /tmp/n8n-import
```

### 7. Report results

After completing all steps, provide a summary in this format:

```
## n8n Workflow Import Complete

- **Pod:** <N8N_POD name>
- **Namespace:** fenrir-marketing
- **Workflows imported:** <list of filenames>
- **Source:** infrastructure/n8n/workflows/

Workflows are now available in the n8n UI. You may need to activate them manually.
```

If any import failed, list the failures separately with error details.

## Notes

- **Namespace:** `fenrir-marketing`
- **Requires:** kubectl configured for the GKE cluster
- **Upsert behavior:** If a workflow with the same ID already exists in n8n, it will be updated (overwritten). This is n8n's default import behavior.
- **New workflows:** Workflows with no matching ID in n8n are created as new entries.
- **Inactive by default:** Imported workflows are created as inactive. The user must activate them manually in the n8n UI.
- **Always use absolute paths** when referencing files in bash commands, since agent threads reset cwd between bash calls.
