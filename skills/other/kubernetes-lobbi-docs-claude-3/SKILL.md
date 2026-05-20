---
name: kubernetes
description: Kubernetes deployment, management, and troubleshooting. Activate for k8s, kubectl, pods, deployments, services, ingress, namespaces, and container orchestration tasks.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Kubernetes Skill

Provides comprehensive Kubernetes deployment and management capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Pod management and debugging
- Deployment configurations and rollouts
- Service and ingress setup
- Kubernetes resource templates
- Cluster troubleshooting
- Namespace management

## Quick Reference

### Common Commands
\`\`\`bash
# Pods
kubectl get pods -n agents
kubectl describe pod <name> -n agents
kubectl logs <pod> -n agents --tail=100 -f
kubectl exec -it <pod> -n agents -- /bin/sh

# Deployments
kubectl get deployments -n agents
kubectl rollout status deployment/<name> -n agents
kubectl rollout restart deployment/<name> -n agents
kubectl scale deployment/<name> -n agents --replicas=3

# Services
kubectl get svc -n agents
kubectl port-forward svc/<name> 8080:8080 -n agents

# Debugging
kubectl get events -n agents --sort-by='.lastTimestamp'
kubectl top pods -n agents
kubectl describe pod <name> -n agents | grep -A10 "Events:"
\`\`\`

## Resource Templates

### Deployment
\`\`\`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-deployment
  namespace: agents
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: agent
          image: golden-armada/agent:latest
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "500m"
              memory: "512Mi"
            requests:
              cpu: "100m"
              memory: "128Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
\`\`\`

### Service
\`\`\`yaml
apiVersion: v1
kind: Service
metadata:
  name: agent-service
  namespace: agents
spec:
  selector:
    app: agent
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
\`\`\`

### Ingress
\`\`\`yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: agent-ingress
  namespace: agents
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: agents.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: agent-service
                port:
                  number: 80
\`\`\`

## Troubleshooting Flow

1. Check pod status: `kubectl get pods`
2. Check events: `kubectl get events`
3. Check logs: `kubectl logs <pod>`
4. Check describe: `kubectl describe pod <pod>`
5. Check resources: `kubectl top pods`

## Golden Armada Specific

Default namespace: `agents`
Helm chart location: `deployment/helm/golden-armada`
