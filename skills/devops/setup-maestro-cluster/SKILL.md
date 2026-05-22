---
name: setup-maestro-cluster
description: Sets up a long-running Maestro cluster environment using Azure ARO-HCP infrastructure with both service and management clusters
category: Infrastructure
tags: [azure, aks, maestro, deployment, cluster, aro-hcp]
---

# Setup Maestro Long-Running Cluster

Sets up a long-running Maestro cluster environment using Azure ARO-HCP infrastructure. This will deploy both service and management clusters.

**Prerequisites:**
- Azure CLI installed and logged in
- Access to "ARO Hosted Control Planes" Azure subscription
- Internet connectivity

**Environment variables set:**
- `USER=oasis` (if not already set)
- `PERSIST=true`
- `GITHUB_ACTIONS=true`
- `GOTOOLCHAIN=go1.24.4`

**Note:** This deployment typically takes 25-30 minutes to complete.

```bash
#!/bin/bash
# Execute the cluster setup script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/scripts/setup.sh" "$@"
```
