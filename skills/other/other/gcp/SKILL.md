---
name: gcp
description: Google Cloud Platform with Cloud Run, GKE, and BigQuery. Use for GCP infrastructure.
---

# Google Cloud Platform (GCP)

GCP is known for its data analytics (BigQuery) and being the home of Kubernetes. 2025 highlights **Vertex AI** for rapid model deployment and **Cloud Run** for serverless everywhere.

## When to Use

- **Big Data**: BigQuery is arguably the best data warehouse for speed and ease of use.
- **Kubernetes**: GKE (Google Kubernetes Engine) often leads in features and stability (Autopilot).
- **AI**: TPU access and Vertex AI for training large models.

## Core Concepts

### Projects

The primary unit of isolation. Resources belong to a Project. Projects belong to Folders/Organization.

### Global VPC

Unlike AWS/Azure, GCP VPCs are global. Subnets are regional. A single VPC can span the world.

### IAM

Permissions are granted to Members (Users/Service Accounts) on Resources via Roles.

## Best Practices (2025)

**Do**:

- **Use Cloud Run**: The default computed choice for stateless containers. Scales to zero, fast startup.
- **Use Workload Identity**: Let GKE workloads impersonate Service Accounts securely.
- **Shared VPC**: For orgs, use a Shared VPC in a Host Project to centralize networking.

**Don't**:

- **Don't use `owner` role**: It's too broad. Use precise roles (`storage.objectViewer`).

## References

- [Google Cloud Documentation](https://cloud.google.com/docs)
