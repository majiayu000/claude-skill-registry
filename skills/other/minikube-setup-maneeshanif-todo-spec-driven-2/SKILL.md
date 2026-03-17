---
name: minikube-setup
description: Setup and configure Minikube for local Kubernetes development
allowed-tools: Bash, Write, Read, Glob, Edit
---

# Minikube Setup Skill

## Quick Start

1. **Install Minikube** - Follow platform-specific instructions
2. **Start Minikube** - With adequate resources for 3 pods
3. **Enable Addons** - Ingress for external access
4. **Load Images** - Push local images to Minikube registry
5. **Deploy Application** - Apply Kubernetes manifests or Helm chart

## What is Minikube?

Minikube runs a single-node Kubernetes cluster locally for development:
- **Local testing** - Test K8s manifests without cloud costs
- **Fast iteration** - Build, deploy, test cycles locally
- **Full K8s API** - Supports most Kubernetes features
- **Cross-platform** - Linux, macOS, Windows

## System Requirements

| Resource | Minimum | Recommended |
|-----------|----------|-------------|
| CPUs | 2 | 4+ |
| Memory | 2GB | 8GB+ |
| Disk | 20GB | 50GB+ |
| Container Runtime | Docker or Podman | Docker |

## Installation

### Linux
```bash
# Download binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

### macOS
```bash
# Using Homebrew
brew install minikube

# Or download binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

### Windows
```bash
# Using Chocolatey
choco install minikube

# Or download installer from
# https://github.com/kubernetes/minikube/releases
```

## Starting Minikube

### Basic Start
```bash
# Start with defaults (2 CPU, 2GB RAM)
minikube start

# Start with more resources (recommended for this project)
minikube start --cpus=4 --memory=8192 --disk-size=50gb
```

### Driver Options

```bash
# Docker driver (default on most systems)
minikube start --driver=docker

# Podman driver
minikube start --driver=podman

# VirtualBox driver
minikube start --driver=virtualbox
```

### Start Options
```bash
# With all recommended options
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=50gb \
  --driver=docker \
  --container-runtime=docker
```

## Minikube Addons

### Enable Ingress
```bash
# Enable ingress controller
minikube addons enable ingress

# Verify
kubectl get pods -n ingress-nginx
```

### Enable Metrics Server
```bash
# Enable metrics for HPA
minikube addons enable metrics-server

# Verify
kubectl top pods
```

### List Available Addons
```bash
# See all available addons
minikube addons list

# Enable multiple
minikube addons enable ingress metrics-server registry
```

## Managing Minikube

### Status Check
```bash
# Check cluster status
minikube status

# Expected output:
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
```

### Stop and Start
```bash
# Stop cluster
minikube stop

# Start again (preserves state)
minikube start

# Delete and start fresh
minikube delete
minikube start
```

### Tunnel for External Access
```bash
# If NodePort doesn't work
minikube tunnel
# This runs in foreground - keep separate terminal
```

## Loading Images to Minikube

### Why Load Images?

Minikube cannot access local Docker images by default. You must:
1. Build image locally
2. Load image into Minikube
3. Deploy

### Load Commands
```bash
# Load single image
minikube image load todo-frontend:latest

# Load multiple images
minikube image load todo-frontend:latest todo-backend:latest todo-mcp-server:latest

# Load all images
docker images --format "{{.Repository}}:{{.Tag}}" | grep todo | xargs minikube image load
```

### Image Load Workflow
```bash
# Step 1: Build images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend
docker build -t todo-mcp-server:latest -f backend/Dockerfile.mcp ./backend

# Step 2: Start Minikube
minikube start

# Step 3: Load images
minikube image load todo-frontend:latest todo-backend:latest todo-mcp-server:latest

# Step 4: Verify
minikube image list
```

## Applying Kubernetes Manifests

### Using kubectl
```bash
# Apply all manifests
kubectl apply -f k8s/ -n todo-app

# Apply single file
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-configmap.yaml
kubectl apply -f k8s/02-secret.yaml

# Apply directory
kubectl apply -R -f k8s/
```

### Using Helm
```bash
# Install with values
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  -f helm/todo-app/values-dev.yaml

# Or use default values
helm install todo-app ./helm/todo-app --namespace todo-app
```

## Accessing Services

### Port Forwarding
```bash
# Forward service to local port
kubectl port-forward svc/frontend 8080:80 -n todo-app

# Access at http://localhost:8080
```

### Minikube Service Command
```bash
# Open service in browser
minikube service frontend -n todo-app

# Get URL without opening
minikube service frontend -n todo-app --url
```

### Minikube IP
```bash
# Get Minikube IP
minikube ip

# Access NodePort services
# http://$(minikube ip):<nodeport>
```

## Dashboard

```bash
# Start dashboard
minikube dashboard

# Access at: http://127.0.0.1:5xxxx

# Open in browser with URL
minikube dashboard --url
```

## Troubleshooting Minikube

### Issue: Minikube won't start
```bash
# Check prerequisites
minikube check

# Common fixes:
# 1. Update minikube
# 2. Restart Docker Desktop
# 3. Delete .minikube directory: rm -rf ~/.minikube
# 4. Try different driver
```

### Issue: Images not found
```bash
# Verify image is loaded
minikube image list

# If not loaded, re-run load command
minikube image load todo-frontend:latest
```

### Issue: Pods in Pending state
```bash
# Check resources
kubectl top nodes

# Check events
kubectl describe pod <pod-name> -n todo-app

# May need to increase Minikube resources
minikube stop
minikube start --cpus=4 --memory=8192
```

### Issue: CrashLoopBackOff
```bash
# View logs
kubectl logs <pod-name> -n todo-app

# View previous logs
kubectl logs <pod-name> -n todo-app --previous

# Describe pod for events
kubectl describe pod <pod-name> -n todo-app
```

### Issue: Ingress not working
```bash
# Verify ingress addon
minikube addons list | grep ingress

# Enable if missing
minikube addons enable ingress

# Add host entry (for todo.local)
echo "$(minikube ip) todo.local" | sudo tee -a /etc/hosts
```

## Integration with Project

### Todo Project Minikube Workflow

```bash
# 1. Start Minikube with adequate resources
minikube start --cpus=4 --memory=8192 --disk-size=50gb

# 2. Enable required addons
minikube addons enable ingress metrics-server

# 3. Build Docker images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend
docker build -t todo-mcp-server:latest -f backend/Dockerfile.mcp ./backend

# 4. Load images into Minikube
minikube image load todo-frontend:latest todo-backend:latest todo-mcp-server:latest

# 5. Create namespace
kubectl create namespace todo-app

# 6. Create secrets
kubectl create secret generic backend-secrets \
  --from-literal=GEMINI_API_KEY=${GEMINI_API_KEY} \
  --from-literal=BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET} \
  -n todo-app

# 7. Apply manifests
kubectl apply -f k8s/ -n todo-app

# 8. Verify deployment
kubectl get pods -n todo-app
kubectl get svc -n todo-app

# 9. Access application
minikube service frontend -n todo-app
```

## Cleanup

```bash
# Stop Minikube
minikube stop

# Delete cluster
minikube delete

# Clear all data
rm -rf ~/.minikube

# Delete namespace
kubectl delete namespace todo-app
```

## Verification Checklist

After Minikube setup:
- [ ] Minikube is running (`minikube status`)
- [ ] kubectl is configured
- [ ] Ingress addon is enabled
- [ ] All images are loaded (`minikube image list`)
- [ ] Namespace `todo-app` exists
- [ ] Secrets are created
- [ ] All pods are Running
- [ ] All services have endpoints
- [ ] Application is accessible in browser
- [ ] Frontend can connect to backend
- [ ] Backend can connect to MCP server

## Common Commands Reference

```bash
# Daily workflow
minikube start                              # Start cluster
kubectl get pods -n todo-app                # Check status
minikube dashboard                          # Open dashboard
minikube service frontend -n todo-app     # Access app

# Debugging
kubectl logs -f deployment/backend -n todo-app  # View logs
kubectl describe pod <pod-name> -n todo-app       # Debug pod
kubectl exec -it <pod-name> -n todo-app -- sh  # Shell in pod

# Cleanup
minikube stop                              # Stop cluster
minikube delete                            # Delete cluster
```

## Next Steps

After successful Minikube deployment:
1. Test all application features
2. Verify AI chatbot works end-to-end
3. Prepare for cloud deployment (Phase 5)
4. Review Helm charts for production use

## References

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Minikube GitHub](https://github.com/kubernetes/minikube)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl-ai Integration](../aiops-gordon/SKILL.md)
- [Phase 4 Constitution](../../../prompts/constitution-prompt-phase-4.md)
- [Phase 4 Plan](../../../prompts/plan-prompt-phase-4.md)
