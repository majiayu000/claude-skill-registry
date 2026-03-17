---
name: helm
cluster: devops-sre
description: "Helm is a package manager for Kubernetes that allows defining, installing, and upgrading applications via charts."
tags: ["helm","kubernetes","package-manager"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "helm kubernetes package manager charts deployment"
---

# helm

## Purpose
Helm is a package manager for Kubernetes, enabling users to define, install, and upgrade applications using charts. It simplifies managing Kubernetes resources by packaging them into reusable templates.

## When to Use
Use Helm for deploying and managing applications on Kubernetes clusters, especially when handling multiple environments, versioning dependencies, or automating deployments. Ideal for DevOps workflows involving microservices, where consistent application packaging is needed, such as in CI/CD pipelines for scalable apps.

## Key Capabilities
- Package applications as charts, which are directories containing YAML manifests and templates.
- Support for chart repositories, allowing versioned storage and retrieval.
- Templating engine to customize deployments with values files (e.g., YAML format for overriding parameters).
- Rollback and upgrade features for managing release lifecycles.
- Integration with Kubernetes RBAC for secure operations.

## Usage Patterns
To use Helm, first ensure Kubernetes access via `kubectl` or set the `KUBECONFIG` environment variable (e.g., `export KUBECONFIG=~/.kube/config`). Initialize Helm with `helm init` if needed, then add repositories and install charts. For custom deployments, create a chart with `helm create mychart`, edit values.yaml, and install. Always specify the namespace with `--namespace` flag for multi-tenant clusters.

## Common Commands/API
Helm operates via CLI commands; no direct REST API exists, but it interacts with Kubernetes API server.
- Install a chart: `helm install myrelease stable/nginx --set service.type=LoadBalancer --namespace dev`
  - Flags: `--set` for inline overrides, `--values` for external YAML file (e.g., `helm install --values values.yaml`).
- Upgrade a release: `helm upgrade myrelease stable/nginx --set replicas=3`
  - Use `--atomic` for rollback on failure.
- List releases: `helm list --all-namespaces`
- Delete a release: `helm uninstall myrelease --namespace dev`
- Search repositories: `helm search repo nginx`
Code snippet for a basic values.yaml file:
```
replicaCount: 2
image:
  repository: nginx
  tag: latest
```
To add a repository: `helm repo add stable https://charts.helm.sh/stable`, then update with `helm repo update`.

## Integration Notes
Helm integrates with Kubernetes tools; ensure your cluster is accessible via the Kubernetes API. For authentication, use `$KUBECONFIG` for client certificates or tokens. In CI/CD (e.g., GitHub Actions), run Helm in a container with `kubectl` installed: set env var like `export HELM_REPOSITORY_CONFIG=repo.yaml`. For Terraform integration, use Helm provider: define in HCL as `resource "helm_release" "nginx" { name = "myrelease" chart = "stable/nginx" set { name = "service.type" value = "LoadBalancer" } }`. Avoid conflicts by using Helm's `--wait` flag with Kubernetes operators.

## Error Handling
Common errors include "chart not found" (fix by running `helm repo update`), permission issues (ensure RBAC via `kubectl create clusterrolebinding`), or failed hooks (check with `helm status`). For deployment failures, use `helm history release-name` to review revisions, then rollback with `helm rollback release-name 0`. If a chart install errors due to invalid values, validate YAML first with a linter like `yamllint values.yaml`. Always check Kubernetes events with `kubectl get events --namespace dev` for root causes.

## Concrete Usage Examples
1. **Install a WordPress chart**: Add the repo with `helm repo add bitnami https://charts.bitnami.com/bitnami`, then install: `helm install mywordpress bitnami/wordpress --set wordpressUsername=admin --set wordpressPassword=$WP_PASSWORD --namespace web`. This deploys WordPress with custom credentials; ensure `$WP_PASSWORD` is set as an env var for security.
2. **Upgrade an existing MongoDB release**: First, install with `helm install mymongo bitnami/mongodb --set auth.enabled=true`, then upgrade: `helm upgrade mymongo bitnami/mongodb --set resources.requests.memory=512Mi --namespace db`. This scales resources; monitor with `helm status mymongo` to verify.

## Graph Relationships
- Related to: kubernetes (core dependency for deployments)
- Co-located in: devops-sre cluster (shared with tools like kubectl, terraform)
- Tagged with: helm, kubernetes, package-manager (links to similar skills in the cluster)
