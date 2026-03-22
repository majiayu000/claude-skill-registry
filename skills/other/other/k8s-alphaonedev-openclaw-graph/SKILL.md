---
name: k8s
cluster: devops-sre
description: "Expertise in orchestrating and managing containerized applications at scale using Kubernetes."
tags: ["kubernetes","k8s","containers"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "kubernetes k8s containers orchestration pods services deployments"
---

# k8s

## Purpose
This skill enables the AI to orchestrate and manage containerized applications using Kubernetes, focusing on scaling, deployment, and maintenance of pods, services, and deployments in a cluster.

## When to Use
Use this skill for deploying multi-container apps, scaling workloads dynamically, managing resources in production environments, or troubleshooting cluster issues. Apply it when handling container orchestration beyond basic Docker, such as in CI/CD pipelines or microservices architectures.

## Key Capabilities
- Deploy and manage pods using YAML manifests or imperative commands.
- Scale applications with deployments and replicasets, e.g., autoscaling based on CPU metrics.
- Expose services via ClusterIP, NodePort, or LoadBalancer types.
- Handle storage with PersistentVolumes and PersistentVolumeClaims.
- Monitor and debug resources using built-in tools like kubectl logs and events.
- Integrate with networking plugins for service discovery and load balancing.
- Manage secrets and config maps for secure configuration.

## Usage Patterns
Always authenticate with a valid kubeconfig file, set via the $KUBECONFIG environment variable. For declarative setups, write YAML files and apply them; for imperative tasks, use kubectl directly. Pattern: Load context with `kubectl config use-context my-context`, then perform actions. Include error checks in scripts, e.g., verify command exit codes.

Example 1: Deploy a simple Nginx pod.
- Create a pod: `kubectl run nginx-pod --image=nginx --port=80`
- Expose it: `kubectl expose pod nginx-pod --type=NodePort --port=80`
- Verify: `kubectl get pods -l run=nginx-pod`

Example 2: Scale a deployment.
- Apply a deployment YAML: `kubectl apply -f deployment.yaml`
- Where deployment.yaml contains: `apiVersion: apps/v1 kind: Deployment metadata: name: my-app spec: replicas: 3 selector: matchLabels: app: my-app template: metadata: labels: app: my-app spec: containers: - name: my-container image: my-image`
- Scale it: `kubectl scale deployment my-app --replicas=5`
- Check status: `kubectl get deployments my-app`

## Common Commands/API
Use kubectl for CLI interactions; for API access, target the Kubernetes API server at endpoints like /api/v1/pods. Always specify namespaces with --namespace flag if needed.

- Get resources: `kubectl get pods --namespace=default -o wide` (flags: -o for output format, --namespace for scope)
- Create resources: `kubectl apply -f pod.yaml --record` (flags: -f for file, --record for history)
- Delete resources: `kubectl delete deployment my-app --cascade=foreground` (flags: --cascade for dependent cleanup)
- Update resources: `kubectl set image deployment/my-app my-container=my-image:new-tag`
- API endpoints: Use curl with authentication, e.g., `curl -k -H "Authorization: Bearer $KUBE_TOKEN" https://api.example.com/api/v1/namespaces/default/pods`
- Config formats: YAML for manifests, e.g., `apiVersion: v1 kind: Pod metadata: name: example spec: containers: - name: example image: nginx`
- Environment setup: Export $KUBECONFIG=/path/to/config for authentication.

## Integration Notes
Integrate Kubernetes with other tools via the Kubernetes API or operators. For authentication, use $KUBECONFIG for kubeconfig files or $KUBE_API_KEY for API tokens. Pattern: In scripts, check if $KUBECONFIG is set; if not, prompt or error out. For CI/CD, use tools like Argo CD or Jenkins plugins; example: Helm charts for packaging, installed via `helm install my-chart ./chart-dir`. Ensure compatibility with cloud providers like AWS EKS by setting provider-specific configs in kubeconfig.

## Error Handling
Always check kubectl exit codes; if non-zero, use `kubectl describe <resource>` for details. Common errors: "NotFound" for missing resources—handle by checking existence first with `kubectl get`; "Forbidden" for permissions—verify RBAC roles. In code, wrap commands in try-catch blocks, e.g., in Python: `import subprocess; try: subprocess.run(['kubectl', 'get', 'pods'], check=True) except subprocess.CalledProcessError as e: print(f"Error: {e}")`. For API calls, handle HTTP errors like 403 or 500 by retrying with exponential backoff. Log events with `kubectl get events --namespace=default` to diagnose issues.

## Graph Relationships
- Related to cluster: devops-sre (e.g., links to other devops skills like CI/CD tools).
- Connected via tags: kubernetes (e.g., relates to container management skills), k8s (synonym for kubernetes), containers (links to Docker or orchestration skills).
- Potential edges: This skill depends on networking and storage skills; it provides outputs for monitoring skills like Prometheus.
