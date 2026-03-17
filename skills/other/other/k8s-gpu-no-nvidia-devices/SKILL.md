---
name: k8s-gpu-no-nvidia-devices
description: |
  Fix for Kubernetes GPU pods showing "CUDA not supported" or no /dev/nvidia* devices
  despite nvidia.com/gpu resource allocation. Use when: (1) container runs but torch.cuda.is_available()
  returns False, (2) ls /dev/nvidia* shows "no matches found", (3) nvidia-smi fails inside pod
  but works on host, (4) PyTorch/TensorFlow falls back to CPU despite GPU allocation.
  Covers NVIDIA device plugin, time-slicing, and container runtime issues.
author: Claude Code
version: 1.0.0
date: 2026-01-27
---

# Kubernetes GPU Pod - No NVIDIA Devices Found

## Problem

A Kubernetes pod requests GPU resources (`nvidia.com/gpu: 1`) and schedules on a GPU node,
but inside the container there are no NVIDIA devices visible. The application falls back
to CPU with messages like "CUDA not supported by the Torch installed!" despite running
in a CUDA-enabled container image.

## Context / Trigger Conditions

- Pod shows `Running` status and is on a node with `gpu=true` label
- `kubectl describe pod` shows GPU limit/request is satisfied
- Inside container: `ls /dev/nvidia*` returns "no matches found"
- Inside container: `nvidia-smi` fails or command not found
- Application logs show: "CUDA not supported", "Switching to CPU", "torch.cuda.is_available() = False"
- On the host node: `nvidia-smi` works fine

## Solution

### Step 1: Verify GPU Availability

Check if other pods are consuming the GPU:

```bash
# List all pods using GPU resources
kubectl get pods -A -o json | jq -r '.items[] | select(.spec.containers[].resources.limits."nvidia.com/gpu" != null) | "\(.metadata.namespace)/\(.metadata.name)"'

# Check NVIDIA device plugin pods
kubectl get pods -n nvidia -l app=nvidia-device-plugin
kubectl logs -n nvidia -l app=nvidia-device-plugin --tail=50
```

### Step 2: Free GPU Resources

If another workload is using the GPU, unload it:

```bash
# For Ollama specifically
kubectl exec -n ollama deployment/ollama -- ollama stop <model_name>

# Or scale down the conflicting deployment
kubectl scale deployment/<name> -n <namespace> --replicas=0
```

### Step 3: Restart the Affected Pod

After freeing GPU resources, restart the pod to get fresh device allocation:

```bash
kubectl rollout restart deployment/<name> -n <namespace>

# Or delete the pod directly
kubectl delete pod <pod-name> -n <namespace>
```

### Step 4: Verify GPU Access

```bash
# Check devices are now visible
kubectl exec -n <namespace> deployment/<name> -- ls -la /dev/nvidia*

# Test nvidia-smi
kubectl exec -n <namespace> deployment/<name> -- nvidia-smi

# Test PyTorch CUDA
kubectl exec -n <namespace> deployment/<name> -- python3 -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

## Verification

After restart, you should see:

```
/dev/nvidia0
/dev/nvidiactl
/dev/nvidia-uvm
/dev/nvidia-uvm-tools
```

And `nvidia-smi` should show the GPU with your container process.

## Example

```bash
# Problem: ebook2audiobook shows "CUDA not supported"
$ kubectl exec -n ebook2audiobook deployment/ebook2audiobook -- ls /dev/nvidia*
zsh:1: no matches found: /dev/nvidia*

# Solution: Unload Ollama model holding the GPU
$ kubectl exec -n ollama deployment/ollama -- ollama ps
NAME           SIZE     PROCESSOR
qwen2.5:14b    10 GB    33%/67% CPU/GPU

$ kubectl exec -n ollama deployment/ollama -- ollama stop qwen2.5:14b

# Restart the affected pod
$ kubectl rollout restart deployment/ebook2audiobook -n ebook2audiobook

# Verify
$ kubectl exec -n ebook2audiobook deployment/ebook2audiobook -- nvidia-smi
# Should now show the Tesla T4 GPU
```

## Notes

- **GPU Time-Slicing**: If using NVIDIA GPU time-slicing (configured in GPU Operator),
  multiple pods can share a GPU. However, device injection still requires proper timing.

- **Pod Scheduling Order**: Pods that start while GPU is fully allocated may not get
  devices injected even after GPU becomes available - a restart is required.

- **Container Runtime**: The NVIDIA Container Toolkit must be properly configured.
  Issues can arise from:
  - cgroup driver mismatch (systemd vs cgroupfs)
  - Container updates causing device loss
  - SELinux blocking device access

- **Image Compatibility**: The container image must have CUDA libraries matching the
  driver version. Check with `nvidia-smi` on host for driver version.

- **This Cluster**: Uses NVIDIA GPU Operator with time-slicing (20 replicas per GPU).
  GPU node is `k8s-node1` with Tesla T4.

## See Also

- Check GPU Operator status: `kubectl get pods -n nvidia`
- View time-slicing config: `kubectl get configmap -n nvidia time-slicing-config -o yaml`

## References

- [NVIDIA Container Toolkit Troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/troubleshooting.html)
- [Kubernetes GPU Device Plugin](https://github.com/NVIDIA/k8s-device-plugin)
- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/overview.html)
