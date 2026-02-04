---
name: k8s-expert
description: This skill should be used when the user asks to "deploy to kubernetes", "debug pod issues", "configure ingress", "set up helm chart", "argocd sync", "kubectl commands", "service not working", "pod crashloopbackoff", "external-secrets setup", "cert-manager config", "troubleshoot k8s", "pvc pending", "metallb config", "external-dns setup", "cloudflared tunnel", or mentions k8s, kubernetes, kubectl, helm, argocd, k3s, homelab cluster. Provides comprehensive Kubernetes guidance including GitOps patterns from this dotfiles repo.
---

# Kubernetes Expert

Full-stack Kubernetes guidance: kubectl, Helm, ArgoCD GitOps, networking, secrets, debugging. Includes patterns from this repo's `k8s/` homelab setup.

## Quick Reference

### kubectl Essentials

```bash
# Pod debugging
kubectl get pods -A                           # all namespaces
kubectl describe pod <name> -n <ns>           # events, status
kubectl logs <pod> -n <ns> --previous         # crashed container logs
kubectl logs <pod> -c <container> -f          # follow specific container
kubectl exec -it <pod> -n <ns> -- /bin/sh     # shell into pod

# Resource inspection
kubectl get events -n <ns> --sort-by='.lastTimestamp'
kubectl top pods -n <ns>                      # resource usage
kubectl get all -n <ns>                       # everything in namespace

# Quick edits
kubectl edit deployment <name> -n <ns>
kubectl rollout restart deployment <name> -n <ns>
kubectl rollout status deployment <name> -n <ns>
kubectl rollout undo deployment <name> -n <ns>

# Ephemeral containers (debug without restart)
kubectl debug <pod> -it --image=busybox --target=<container>  # attach to running pod
kubectl debug <pod> -it --copy-to=debug-pod --image=nicolaka/netshoot  # copy pod for debug
kubectl debug node/<node> -it --image=busybox  # debug node issues
```

### Helm Commands

```bash
# Chart management
helm repo add <name> <url>
helm repo update
helm search repo <chart>

# Install/upgrade
helm install <release> <chart> -n <ns> --create-namespace -f values.yaml
helm upgrade <release> <chart> -n <ns> -f values.yaml
helm upgrade --install <release> <chart> -n <ns>  # install or upgrade

# Debugging
helm list -A                                  # all releases
helm status <release> -n <ns>
helm history <release> -n <ns>
helm get values <release> -n <ns>             # current values
helm get manifest <release> -n <ns>           # rendered templates
helm template <chart> -f values.yaml          # dry-run render

# Rollback
helm rollback <release> <revision> -n <ns>
```

### ArgoCD Operations

```bash
# CLI setup
argocd login <server> --grpc-web

# App management
argocd app list
argocd app get <app>
argocd app sync <app>
argocd app sync <app> --prune                 # remove orphaned resources
argocd app diff <app>                         # preview changes

# Troubleshooting
argocd app logs <app>
argocd app history <app>
argocd app rollback <app> <id>
```

## Homelab Patterns (from k8s/)

This repo uses **app-of-apps pattern** with ArgoCD:

```
k8s/
├── argocd/
│   ├── app-of-apps.yaml      # root app pointing to apps/
│   ├── apps/                 # ArgoCD Application manifests
│   │   ├── cert-manager.yaml
│   │   ├── external-secrets.yaml
│   │   └── ...
│   ├── cluster-issuer/       # cert-manager ClusterIssuers
│   ├── external-secrets/     # ExternalSecret definitions
│   └── <app-name>/           # per-app configs (values.yaml, etc)
└── terraform/
    ├── main.tf               # base infra
    ├── argocd/               # ArgoCD bootstrap
    └── metallb-config/       # load balancer
```

### Adding New App to Homelab

1. Create ArgoCD Application in `k8s/argocd/apps/<app>.yaml`:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/peterstorm/.dotfiles.git
    targetRevision: HEAD
    path: k8s/argocd/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

2. Create app directory with manifests: `k8s/argocd/my-app/`
3. Push to git - ArgoCD auto-syncs

## Debugging Workflows

### Pod Not Starting

```bash
# 1. Check pod status
kubectl get pod <pod> -n <ns> -o wide

# 2. Check events
kubectl describe pod <pod> -n <ns> | grep -A 20 Events

# 3. Common issues:
# - ImagePullBackOff: wrong image/tag, missing imagePullSecrets
# - Pending: insufficient resources, node selector mismatch
# - CrashLoopBackOff: check logs
# - CreateContainerConfigError: missing configmap/secret
```

### Service Not Reachable

```bash
# 1. Verify endpoints exist
kubectl get endpoints <svc> -n <ns>

# 2. Check service selector matches pod labels
kubectl get svc <svc> -n <ns> -o yaml | grep -A5 selector
kubectl get pods -n <ns> --show-labels

# 3. Test from within cluster
kubectl run debug --rm -it --image=busybox -- wget -qO- http://<svc>.<ns>.svc.cluster.local
```

### Ingress Issues

```bash
# 1. Check ingress status
kubectl get ingress -n <ns>
kubectl describe ingress <name> -n <ns>

# 2. Verify TLS secret exists
kubectl get secret <tls-secret> -n <ns>

# 3. Check cert-manager certificate
kubectl get certificate -n <ns>
kubectl describe certificate <name> -n <ns>

# 4. Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
```

## Secrets Management

### External Secrets (homelab pattern)

ClusterSecretStore connects to secret backend:
```yaml
# k8s/argocd/external-secrets/cluster-secret-store.yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "external-secrets"
```

ExternalSecret pulls specific secrets:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: my-secret
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: vault-backend
  target:
    name: my-secret
  data:
    - secretKey: password
      remoteRef:
        key: apps/myapp
        property: password
```

**Security best practices for ESO:**
- Use namespaced SecretStore instead of ClusterSecretStore when possible
- Apply RBAC to limit which namespaces can access which secrets
- Add NetworkPolicy to restrict ESO controller egress
- Set `refreshInterval` appropriately (not too frequent)

### Cert-Manager (homelab pattern)

**Staging-first workflow** (avoid rate limits):
```bash
# 1. Deploy with staging issuer first (untrusted cert, no rate limits)
cert-manager.io/cluster-issuer: letsencrypt-staging

# 2. Verify certificate issued successfully
kubectl get certificate -n <ns>
kubectl describe certificate <name> -n <ns>

# 3. Switch to production
cert-manager.io/cluster-issuer: letsencrypt-prod

# 4. Delete old secret to trigger re-issue
kubectl delete secret <tls-secret> -n <ns>
```

ClusterIssuers (staging + prod):
```yaml
# k8s/argocd/cluster-issuer/letsencrypt-staging.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: your@email.com
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
      - dns01:
          cloudflare:
            apiTokenSecretRef:
              name: cloudflare-api-token
              key: api-token
---
# k8s/argocd/cluster-issuer/letsencrypt-prod.yaml (same but prod server)
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    # ... same config
```

Ingress with auto-TLS:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod  # or staging for testing
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
```

## Additional Resources

### Reference Files

For detailed patterns and troubleshooting:
- **`references/troubleshooting.md`** - Extended debugging workflows
- **`references/helm-patterns.md`** - Helm chart best practices
- **`references/homelab-components.md`** - MetalLB, external-dns, cloudflared, k9s

### Homelab Context

Examine actual configs in this repo:
- `k8s/argocd/app-of-apps.yaml` - Root ArgoCD app
- `k8s/argocd/apps/` - All managed applications
- `k8s/terraform/` - Infrastructure as code
