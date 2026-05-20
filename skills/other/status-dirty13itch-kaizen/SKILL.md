---
name: status
description: Check Kaizen system health across all nodes and services
---
Run comprehensive health check. Report on each section:

**Cluster**: `kubectl get nodes -o wide && kubectl get pods -A`
**GPUs**: `kubectl exec` into GPU pods and run `nvidia-smi` or check node labels
**Inference**: `curl -s http://10.10.10.12:30000/health` and port 30001
**Storage**: `df -h /mnt/disk9/models` on VAULT, check NFS PV status
**Monitoring**: Check Prometheus/Grafana pods in kaizen-monitoring namespace

Format as a status dashboard. Flag anything not healthy.
