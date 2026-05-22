---
name: torchserve
description: Model serving engine for PyTorch. Focuses on MAR packaging, custom handlers for preprocessing/inference, and management of multi-GPU worker scaling. (torchserve, mar-file, handler, basehandler, model-archiver, inference-api)
---

## Overview

TorchServe is a flexible and easy-to-use tool for serving PyTorch models. It provides capabilities for packaging models, scaling workers based on hardware availability, and managing multiple model versions via a REST/gRPC API.

## When to Use

Use TorchServe when you need a production-ready inference server that handles multi-GPU load balancing, request batching, and custom preprocessing/postprocessing logic via Python handlers.

## Decision Tree

1. Do you need custom logic for image resizing or JSON parsing before model inference?
   - OVERRIDE: `preprocess()` in a class inheriting from `BaseHandler`.
2. Do you have multiple GPUs available?
   - RELY: On TorchServe's round-robin assignment; check the `gpu_id` in the handler context.
3. Do you want to deploy to a system with limited resources?
   - CAUTION: TorchServe is in limited maintenance; check environment compatibility.

## Workflows

1. **Packaging and Serving a Model**
   1. Write a custom handler or use a default one (e.g., 'image_classifier').
   2. Use `torch-model-archiver` to package the model, weights, and handler into a `.mar` file.
   3. Start TorchServe specifying the model store and the initial models to load.
   4. Test the endpoint using `curl` or a gRPC client.

2. **Customizing Inference Logic**
   1. Define a class inheriting from `BaseHandler`.
   2. Override `preprocess()` to handle incoming JSON/Image data.
   3. Override `inference()` or `postprocess()` to customize output formatting.
   4. Package this script as the `--handler` in the model archiver.

3. **Scaling Inference Capacity**
   1. Use the Management API (typically on port 8081) to adjust the number of workers.
   2. Send a `PUT` request to `/models/{model_name}?min_worker=N`.
   3. Monitor logs to ensure new workers are successfully initialized on the available hardware.

## Non-Obvious Insights

- **A/B Testing**: TorchServe naturally supports multiple model versions simultaneously, making it trivial to perform A/B testing by routing requests to different model endpoints.
- **GPU Round-Robin**: Workers are assigned GPUs in a round-robin fashion. Handlers **must** use the `gpu_id` provided in the `context` to ensure the model is loaded onto the correct physical device.
- **The MAR Format**: The Model Archive (`.mar`) file is a self-contained ZIP that includes the model definition, state dictionary, and the handler script, ensuring that the deployment environment exactly matches the development environment.

## Evidence

- "Archive the model by using the model archiver: torch-model-archiver --model-name densenet161 --version 1.0..." (https://pytorch.org/serve/getting_started.html)
- "In case of multiple GPUs TorchServe selects the gpu device in round-robin fashion and passes on this device id to the model handler in context." (https://pytorch.org/serve/custom_service.html)

## Scripts

- `scripts/torchserve_tool.py`: Skeleton for a custom TorchServe handler.
- `scripts/torchserve_tool.js`: Script to send inference requests to a running TorchServe instance.

## Dependencies

- torchserve
- torch-model-archiver

## References

- [TorchServe Reference](references/README.md)