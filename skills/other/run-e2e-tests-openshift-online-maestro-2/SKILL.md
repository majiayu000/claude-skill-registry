---
name: run-e2e-tests
description: Runs end-to-end or upgrade tests on existing long-running Maestro clusters deployed in Azure AKS
category: Testing
tags: [azure, aks, maestro, e2e, testing, upgrade, kubernetes]
---

# Run E2E Tests on Long-Running Cluster

Runs end-to-end or upgrade tests on existing long-running Maestro clusters deployed in Azure AKS.

**Prerequisites:**
- Azure CLI, kubectl, kubelogin, jq must be installed
- Logged into Azure with cluster access
- Long-running clusters must be already deployed
- Required environment variables:
  - `SVC_RESOURCE_GROUP`: Resource group for service cluster
  - `SVC_CLUSTER_NAME`: Name of service cluster
  - `MGMT_RESOURCE_GROUP`: Resource group for management cluster
  - `MGMT_CLUSTER_NAME`: Name of management cluster

**Usage:**
```bash
/run-e2e-tests [test-type]
```

Where `test-type` can be:
- `upgrade`: Run upgrade tests (default)
- `e2e`: Run standard E2E tests with Istio
- `all`: Run both upgrade and e2e tests

**Example:**
```bash
export SVC_RESOURCE_GROUP="hcp-underlay-<cluster-id>-svc"
export SVC_CLUSTER_NAME="<cluster-id>-svc"
export MGMT_RESOURCE_GROUP="hcp-underlay-<cluster-id>-mgmt-1"
export MGMT_CLUSTER_NAME="<cluster-id>-mgmt-1"

/run-e2e-tests upgrade
```

```bash
#!/bin/bash
# Execute the E2E test script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/scripts/run-tests.sh" "$@"
```
