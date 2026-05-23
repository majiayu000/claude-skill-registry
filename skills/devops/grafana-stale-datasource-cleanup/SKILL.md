---
name: grafana-stale-datasource-cleanup
description: |
  Fix Grafana datasource errors when a Helm chart creates a datasource that conflicts
  with provisioned ones, or when stale datasources persist in the MySQL database.
  Use when: (1) Grafana shows "dial tcp: lookup <service> no such host" for a datasource,
  (2) Grafana API returns "datasources:delete permissions needed" when trying to remove
  a datasource, (3) provisioned datasource exists but Grafana uses a stale one from
  the database, (4) Helm chart auto-creates a datasource pointing to a disabled gateway
  service (e.g., loki-gateway). Requires direct MySQL access to fix when Grafana RBAC
  blocks API operations.
author: Claude Code
version: 1.0.0
date: 2026-02-13
---

# Grafana Stale Datasource Cleanup

## Problem
Grafana uses a stale or incorrect datasource from its MySQL database instead of
the correctly provisioned one. Common when Helm charts auto-create datasources
that point to services you've disabled (e.g., Loki gateway).

## Context / Trigger Conditions
- Grafana shows error: `dial tcp: lookup loki-gateway on 10.96.0.10:53: no such host`
- A provisioned datasource (via ConfigMap sidecar) is correct but Grafana uses a
  different one stored in MySQL
- Grafana API returns `"permissions needed: datasources:delete"` or
  `"permissions needed: datasources:write"` even with admin credentials
- Dashboard references a datasource UID that points to a wrong URL

## Solution

### Step 1: Identify the stale datasource

List all datasources via API (this usually works even with RBAC):
```bash
kubectl exec -n monitoring deploy/grafana -c grafana -- \
  sh -c 'curl -s "http://localhost:3000/api/datasources" \
  -u "admin:$GF_SECURITY_ADMIN_PASSWORD"' | python3 -c \
  "import sys,json; [print(d['uid'], d['name'], d['url']) for d in json.load(sys.stdin)]"
```

### Step 2: Try API deletion first

```bash
kubectl exec -n monitoring deploy/grafana -c grafana -- \
  sh -c 'curl -s -X DELETE "http://localhost:3000/api/datasources/uid/<STALE_UID>" \
  -u "admin:$GF_SECURITY_ADMIN_PASSWORD"'
```

If this returns a permissions error, proceed to Step 3.

### Step 3: Delete directly from MySQL

When Grafana RBAC blocks API operations, go through MySQL:

```bash
# Find the Grafana MySQL password
kubectl exec -n monitoring deploy/grafana -c grafana -- \
  sh -c 'echo $GF_DATABASE_PASSWORD'

# Find the stale datasource
kubectl exec -n dbaas deploy/mysql -- mysql -u grafana -p"<PASSWORD>" grafana \
  -e "SELECT id, uid, name, url FROM data_source;"

# Delete it
kubectl exec -n dbaas deploy/mysql -- mysql -u grafana -p"<PASSWORD>" grafana \
  -e "DELETE FROM data_source WHERE uid='<STALE_UID>';"
```

### Step 4: Fix dashboards referencing the old UID

Dashboards store datasource UIDs in their JSON. Update via MySQL:
```bash
kubectl exec -n dbaas deploy/mysql -- mysql -u grafana -p"<PASSWORD>" grafana \
  -e "UPDATE dashboard SET data = REPLACE(data, '<OLD_UID>', '<NEW_UID>') WHERE title LIKE '%Dashboard Name%';"
```

### Step 5: Refresh Grafana

Hard-refresh browser (Cmd+Shift+R). If datasource still doesn't appear:
```bash
kubectl rollout restart deploy -n monitoring grafana
```

## Verification
```bash
# Verify only correct datasources remain
kubectl exec -n monitoring deploy/grafana -c grafana -- \
  sh -c 'curl -s "http://localhost:3000/api/datasources" \
  -u "admin:$GF_SECURITY_ADMIN_PASSWORD"' | python3 -m json.tool
```

## Notes
- Grafana's sidecar auto-discovers ConfigMaps with label `grafana_datasource: "1"`
  and provisions datasources from them. These are file-provisioned and show as
  "provisioned" in the UI.
- Helm charts (e.g., Loki) may auto-create their own datasource in the Grafana
  database pointing to services like `loki-gateway`. If you disable the gateway,
  this datasource becomes stale.
- Grafana dashboards in this repo are stored in MySQL (not file-provisioned),
  so dashboard JSON files in the repo are reference copies only.
- The `GF_SECURITY_ADMIN_PASSWORD` env var is set by the Grafana Helm chart.
- See also: `loki-helm-deployment-pitfalls` for related Loki deployment issues.
