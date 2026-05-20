---
name: deploy
description: Deploy Kaizen components with safety checks and validation
---
Deploy workflow for Kaizen infrastructure. Follow this sequence:

1. Pre-flight: Run `kubectl get nodes -o wide` to verify cluster health
2. Validate manifests: `kubectl apply --dry-run=client -f <manifest>`
3. Apply in order: base → storage → inference → monitoring → agents
4. Post-deploy: Verify pods running, check logs for errors

Arguments: $ARGUMENTS

Safety rules:
- Always dry-run first
- Never delete namespaces
- Check node readiness before deploying GPU workloads
- Verify NFS mount from VAULT before storage-dependent deploys
