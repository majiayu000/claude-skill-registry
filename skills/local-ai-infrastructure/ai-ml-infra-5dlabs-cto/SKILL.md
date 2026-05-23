---
name: ai-ml-infra
description: KubeAI, GPU operators, and model serving patterns for AI/ML infrastructure on Kubernetes.
agents: [bolt]
triggers: [kubeai, gpu, model, inference, vllm, ollama, llm, ai, ml]
---

# AI/ML Infrastructure

Model serving with KubeAI, GPU scheduling, and inference patterns.

## Model Deployment Options

| Feature | KubeAI | Ollama Operator | LlamaStack |
|---------|--------|-----------------|------------|
| Backend | vLLM (GPU optimized) | Ollama (easy) | Multi-backend |
| Scale from zero | Yes | No | No |
| OpenAI API | Native | Compatible | Compatible |
| Best for | Production GPU | CPU/mixed | Full AI stack |

## KubeAI Setup

### Model CRD

```yaml
apiVersion: kubeai.org/v1
kind: Model
metadata:
  name: llama-3-8b
  namespace: kubeai
spec:
  features: [TextGeneration]
  url: "ollama://llama3.1:8b"
  engine: OLlama
  resourceProfile: nvidia-gpu-l4:1
  minReplicas: 0      # Scale to zero
  maxReplicas: 3
  targetRequests: 10  # Scale up threshold
```

### Resource Profiles

| Profile | GPUs | VRAM | Use Case |
|---------|------|------|----------|
| `cpu` | 0 | - | Embeddings, small models |
| `nvidia-gpu-l4:1` | 1x L4 | 24GB | 8B models |
| `nvidia-gpu-h100:1` | 1x H100 | 80GB | 70B models |
| `nvidia-gpu-h100:2` | 2x H100 | 160GB | Large models |

### Custom Resource Profile

```yaml
resourceProfiles:
  nvidia-gpu-l4:
    nodeSelector:
      nvidia.com/gpu.product: "NVIDIA-L4"
    requests:
      cpu: "4"
      memory: "16Gi"
    limits:
      nvidia.com/gpu: "1"
      cpu: "8"
      memory: "32Gi"
```

## Accessing Models

### OpenAI-Compatible API

```bash
# Port-forward
kubectl port-forward svc/kubeai -n kubeai 8000:80

# List models
curl http://localhost:8000/openai/v1/models

# Chat completion
curl http://localhost:8000/openai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3-8b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### In-Cluster Access

```yaml
env:
  - name: OPENAI_API_BASE
    value: "http://kubeai.kubeai.svc/openai/v1"
  - name: OPENAI_API_KEY
    value: "not-needed"  # KubeAI doesn't require auth
```

### SDK Usage

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://kubeai.kubeai.svc/openai/v1",
  apiKey: "not-needed",
});

const response = await client.chat.completions.create({
  model: "llama-3-8b",
  messages: [{ role: "user", content: "Hello!" }],
});
```

## GPU Operator

NVIDIA GPU Operator manages GPU drivers and device plugins.

### Verify GPU Nodes

```bash
# Check GPU nodes
kubectl get nodes -l nvidia.com/gpu.product

# Check GPU allocations
kubectl describe node <gpu-node> | grep nvidia.com/gpu

# Check device plugin
kubectl get pods -n gpu-operator -l app=nvidia-device-plugin-daemonset
```

### GPU Pod Scheduling

```yaml
spec:
  containers:
    - name: gpu-app
      resources:
        limits:
          nvidia.com/gpu: 1
  nodeSelector:
    nvidia.com/gpu.product: "NVIDIA-L4"
```

## Model Selection Guide

| Model | Size | GPU Req | Best For |
|-------|------|---------|----------|
| `llama3.1:8b` | 8B | L4 x1 | General, coding |
| `llama3.1:70b` | 70B | H100 x2 | Complex reasoning |
| `qwen2.5-coder` | 7B | L4 x1 | Code generation |
| `nomic-embed-text` | 137M | CPU | Embeddings |
| `deepseek-r1` | 1.5B | CPU | Light reasoning |

## Ollama Operator (Alternative)

Simpler setup for Ollama models:

```yaml
apiVersion: ollama.ayaka.io/v1
kind: Model
metadata:
  name: phi4
  namespace: ollama-operator-system
spec:
  image: phi4
  resources:
    limits:
      nvidia.com/gpu: "1"
```

Access:
```bash
kubectl port-forward svc/ollama-model-phi4 -n ollama-operator-system 11434:11434
ollama run phi4
```

## Validation Commands

```bash
# Check KubeAI models
kubectl get models -n kubeai
kubectl describe model <name> -n kubeai

# Check model pods
kubectl get pods -n kubeai -l app.kubernetes.io/name=kubeai

# Check GPU utilization
kubectl exec -n kubeai <pod> -- nvidia-smi

# Test API
curl http://kubeai.kubeai.svc/openai/v1/models
```

## Troubleshooting

### Model not starting

```bash
# Check model status
kubectl describe model <name> -n kubeai

# Check pod events
kubectl get events -n kubeai --sort-by='.lastTimestamp'

# Check logs
kubectl logs -n kubeai -l model=<name>
```

### Out of memory (OOM)

Reduce model parameters:
```yaml
spec:
  args:
    - --max-model-len=4096      # Reduce from 8192
    - --gpu-memory-utilization=0.8  # Reduce from 0.9
```

### Slow first response

Set minReplicas to keep model warm:
```yaml
spec:
  minReplicas: 1  # Always keep one running
```

## Best Practices

1. **Use scale-from-zero** - Set `minReplicas: 0` to save resources
2. **Right-size GPU profiles** - Don't over-allocate expensive GPUs
3. **Use vLLM for production** - Better throughput than Ollama
4. **Monitor GPU memory** - Set appropriate `gpu-memory-utilization`
5. **Keep frequently-used models warm** - `minReplicas: 1`
6. **Use OpenAI-compatible API** - Easy integration with existing code
