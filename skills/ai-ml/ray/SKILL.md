---
name: ray
description: Ray distributed computing framework. Use for scaling ML.
---

# Ray

Ray is the compute layer for AI. It powers ChatGPT training and massive scale workloads. v3.0 (2025) improves **efficiency** and adds an **MCP Server** for agents.

## When to Use

- **Distributed Training**: Scaling PyTorch across 100 GPUs.
- **Ray Serve**: Serving LLMs with high throughput (vLLM integration).
- **Hyperparameter Tuning**: Ray Tune is the industry standard.

## Core Concepts

### Actors & Tasks

- **Task**: Stateless function (like Lambda).
- **Actor**: Stateful class (like a microservice).

### Object Store

Shared memory across the cluster means zero-copy data sharing.

## Best Practices (2025)

**Do**:

- **Use `ray.data`**: For streaming massive datasets into trainers.
- **Use KubeRay**: The Kubernetes operator for managing Ray clusters.
- **Use Ray Serve**: It supports "Model Composition" (chaining models).

**Don't**:

- **Don't use for simple scripts**: The overhead of starting a Ray cluster is 5-10s.

## References

- [Ray Documentation](https://docs.ray.io/)
