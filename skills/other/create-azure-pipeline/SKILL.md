---
name: create-azure-pipeline
description: Generate Azure Pipelines YAML with 4 stages
user-invocable: true
---

Generate azure-pipelines.yml for: . Include: Build+Test, AI Code Quality, Staging Deploy (60s health), Production Deploy (120s health + approval).
