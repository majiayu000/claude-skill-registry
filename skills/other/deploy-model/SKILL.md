---
name: deploy-model
description: Deploy or redeploy an inference model on the cluster. Use when asked to deploy, update, or restart a model.
disable-model-invocation: true
allowed-tools: Bash, Read, Edit
---

# Deploy Model

Deploy or manage inference models on Kaizen. Argument should be one of: `reasoning`, `embedding`, `heavy`, or a manifest path.

## Pre-flight Checks
1. Verify target node is Ready: `kubectl get nodes`
2. Check GPU availability: `kubectl describe node <node> | grep -A3 nvidia.com/gpu`
3. Check existing deployments: `kubectl get pods -n inference`

## Available Manifests
- `k8s/apps/inference/` — All inference deployments
- `k8s/apps/inference/sglang-core.yaml` — Heavy model (Qwen2.5-72B, TP=4, CORE)

## GPU Constraints
- INTERFACE: RTX 5090 (32GB) + RTX 4090 (24GB) — NO tensor parallelism
- CORE: 4x RTX 5070 Ti (16GB each) — TP=4 supported
- Deployment order determines GPU assignment on INTERFACE

## Deploy Steps
1. Read the manifest file
2. Validate: `kubectl apply --dry-run=client -f <manifest>`
3. Show the user what will be deployed (model, GPU, node, port)
4. **Ask for confirmation before applying**
5. Apply: `kubectl apply -f <manifest>`
6. Watch: `kubectl rollout status -n inference deploy/<name> --timeout=300s`
7. Test: `curl http://10.10.10.10:<port>/v1/models`

## Restart
```bash
kubectl rollout restart -n inference deploy/<name>
kubectl rollout status -n inference deploy/<name>
```
