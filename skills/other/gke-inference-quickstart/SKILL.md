---
name: gke-inference-quickstart
description: Deploy optimized AI/ML inference workloads on GKE using Google's Inference Quickstart (GIQ). Covers model discovery, manifest generation, and deployment using native MCP tools and CLI.
---

# GKE Inference Quickstart (GIQ)

## Purpose

This skill guides the deployment of AI/ML inference workloads on GKE using GIQ. It leverages `gcloud container ai profiles manifests create` to create optimized Kubernetes manifests based on Google's best practices and benchmarks.

## When to Use

- **Goal:** Deploy an AI model (e.g., Llama, Gemma, Mistral) to GKE.
- **Goal:** Generate a Kubernetes manifest for inference.
- **Context:** User asks about "GIQ", "Inference Quickstart", or "AI benchmarks" on GKE.

## Prerequisites

- A GKE cluster (preferably with GPU/TPU node pools, though GIQ can help identify requirements).
- `gcloud` CLI installed and authenticated (for discovery commands).

## Workflow

### 1. Discovery: Find Models and Hardware

Before generating a manifest, you often need to pick a valid combination of Model, Model Server, and Accelerator.

**List all supported models:**

```bash
gcloud container ai profiles models list
```

**Find valid accelerators and servers for a specific model:**

```bash
# Replace <MODEL_NAME> with a model from the list above (e.g., 'gemma-2-9b-it')
gcloud container ai profiles list --model=<MODEL_NAME>
```

**View benchmarks/profiles (optional):**
To see costs and latency targets:

```bash
gcloud container ai profiles list --model=<MODEL_NAME>
```

### 2. Generate Manifest

Use the `gcloud container ai profiles manifests create` command. This ensures you are using the latest supported flags and options directly from the CLI.

**Parameters:**

- `--model`: The model ID (e.g., `gemma-2-9b-it`).
- `--model-server`: The inference server (e.g., `vllm`, `tgi`, `triton`, `tensorrt-llm`).
- `--accelerator-type`: The accelerator type (e.g., `nvidia-l4`, `nvidia-tesla-a100`).
- `--target-ntpot-milliseconds`: (Optional) Target Normalized Time Per Output Token in ms.

**Example Command:**

```bash
gcloud container ai profiles manifests create \
  --model=gemma-2-9b-it \
  --model-server=vllm \
  --accelerator-type=nvidia-l4 \
  --target-ntpot-milliseconds=50 > inference-workload.yaml
```

### 3. Review and Deploy

1. **Save:** The example command above saves output to `inference-workload.yaml`. Ensure you have this file.
2. **Review:** Check for any placeholders or specific requirements (like PVCs or secrets).
   - _Note: Some models require Hugging Face tokens. Ensure query instructions for secrets are followed._
3. **Deploy:**
   ```bash
   kubectl apply -f inference-workload.yaml
   ```

## Troubleshooting

- **Invalid Combination:** If the manifest creation fails with an invalid combination error, re-run the discovery commands in Step 1 to verify the tuple (model, server, accelerator).
- **Quota Issues:** Ensure the target region has sufficient quota for the requested accelerator (e.g., `NVIDIA_L4_GPUS`).

## Reference

- **Docs:** [GKE Inference Quickstart Documentation](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/machine-learning/inference/inference-quickstart)
