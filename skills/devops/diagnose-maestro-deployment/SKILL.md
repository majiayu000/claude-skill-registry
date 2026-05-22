---
name: diagnose-maestro-deployment
description: Diagnoses failed Maestro cluster deployments by analyzing Helm releases, pod status, and resource conflicts
category: Troubleshooting
tags: [azure, aks, maestro, troubleshooting, debugging, helm, kubernetes]
---

# Diagnose Maestro Deployment

Automatically diagnoses failed Maestro cluster deployments by:
- Analyzing deployment output to identify resource groups and cluster names
- Checking Helm release status in both service and management clusters
- Inspecting pod states and error conditions
- Identifying resource conflicts and timing issues
- Generating a detailed analysis report with root cause and recommendations

**Prerequisites:**
- Azure CLI installed and logged in
- kubectl and kubelogin installed
- Access to the failed deployment output or cluster information

**Usage:**
```bash
# Diagnose using deployment output file
diagnose-maestro-deployment /path/to/deployment.output

# Diagnose using cluster names directly
diagnose-maestro-deployment --svc-rg <resource-group> --svc-cluster <cluster-name> --mgmt-rg <resource-group> --mgmt-cluster <cluster-name>
```

```bash
#!/bin/bash
# Execute the diagnostic script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/scripts/diagnose.sh" "$@"
```
