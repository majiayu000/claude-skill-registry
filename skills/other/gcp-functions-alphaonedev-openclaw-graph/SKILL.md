---
name: gcp-functions
cluster: cloud-gcp
description: "Deploy and manage serverless functions on Google Cloud Platform using Cloud Functions for event-driven applications."
tags: ["gcp","serverless","functions"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "gcp cloud functions serverless deployment triggers events"
---

# gcp-functions

## Google Cloud Integration

This skill delegates all GCP provisioning and operations to the official Google Cloud Python client libraries.

```bash
# Core GCP client library
pip install google-cloud-python

# Vertex AI + Agent Engine (AI/ML workloads)
pip install google-cloud-aiplatform

# Specific service clients (install only what you need)
pip install google-cloud-bigquery      # BigQuery
pip install google-cloud-storage       # Cloud Storage
pip install google-cloud-pubsub        # Pub/Sub
pip install google-cloud-run           # Cloud Run
```

**SDK Docs:** https://github.com/googleapis/google-cloud-python
**Vertex AI SDK:** https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk

Use the Google Cloud Python SDK for all GCP provisioning and operational actions. This skill provides architecture guidance, cost modeling, and pre-flight requirements — the SDK handles execution.

## Architecture Guidance

Consult this skill for:
- GCP service selection and trade-off analysis
- Cost estimation and optimization (committed use discounts, sustained use)
- Pre-flight IAM / Workload Identity Federation requirements
- IaC approach (Terraform AzureRM vs Deployment Manager vs Config Connector)
- Integration patterns with Google Workspace and other GCP services
- Vertex AI Agent Engine for multi-agent workflow design

## Agent & AI Capabilities

| Capability | Tool |
|---|---|
| LLM agents | Vertex AI Agent Engine |
| Model serving | Vertex AI Model Garden |
| RAG | Vertex AI Search + Embeddings API |
| Multi-agent | Agent Development Kit (google/adk-python) |
| MCP | Vertex AI Extensions (MCP-compatible) |

## Reference

- [Google Cloud Python Client](https://github.com/googleapis/google-cloud-python)
- [Vertex AI Python SDK](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk)
- [Google ADK](https://github.com/google/adk-python)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
- [IAM Best Practices](https://cloud.google.com/iam/docs/best-practices-for-using-and-securing-service-accounts)
- [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
