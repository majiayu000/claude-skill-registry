---
name: multi-cloud-kubernetes-operator
description: |
  Production-grade Kubernetes cluster provisioning and management on budget-friendly cloud providers (DigitalOcean DOKS, Hetzner K3s, Oracle OKE). Optimized for hackathon projects and learning environments where cost control is critical. Use when working with: (1) Deploying Kubernetes clusters on free/cheap cloud providers, (2) Budget-conscious hackathon deployments, (3) Multi-cloud Kubernetes portability, (4) Learning Kubernetes without expensive bills, (5) Rapid cluster spin-up and teardown, (6) Cost comparison between providers. Trigger keywords: "cheap kubernetes", "free kubernetes", "budget cloud", "hackathon deployment", "digitalocean kubernetes", "doks", "hetzner k3s", "oracle oke", "doctl", "oci cli", "tear down cluster", "kubernetes cost".
---

# Multi-Cloud Kubernetes Operator

Guide for provisioning and managing Kubernetes clusters on budget-friendly cloud providers, optimized for hackathon projects and learning environments.

## Supported Providers

| Provider | Min Cost/Month | Free Tier | Setup Time | Complexity | Best For |
|----------|----------------|-----------|------------|------------|----------|
| **OCI OKE** | $0 | Yes (Always Free) | 30-60 min | High | Zero-cost learning |
| **Hetzner K3s** | €4-8 ($4.50-9) | No | 5-10 min | Medium | Best price/performance |
| **DigitalOcean DOKS** | $12+ | $200 credit | 3-5 min | Low | Fastest setup |

## Quick Provider Selection

**Decision flowchart:**
```
Need truly free?
├─ Yes → Oracle OKE (but allow 1-2 hours for setup)
└─ No, can pay → ┐
                  ├─ Need fastest setup? → DigitalOcean DOKS
                  └─ Need cheapest paid? → Hetzner K3s
```

**Hackathon recommendations:**
- **24-48 hour hackathon:** DigitalOcean (speed > cost)
- **Week-long hackathon:** Hetzner (best value)
- **Multi-week project:** Oracle OKE (free but complex)
- **Team learning:** DigitalOcean (consistent experience)

## Provider-Specific Guides

Each provider has detailed documentation in the `references/` directory:

- **[DigitalOcean DOKS](references/digitalocean-doks.md)** - Easiest setup, $200 free credit
- **[Hetzner K3s](references/hetzner-k3s.md)** - Best price/performance, €4-8/month
- **[Oracle OKE](references/oracle-oke.md)** - Truly free tier, complex networking

## Universal Kubernetes Operations

These commands work identically across all providers once `kubectl` is configured:

### Context Management
```bash
# List available contexts
kubectl config get-contexts

# Switch context
kubectl config use-context <context-name>

# View current context
kubectl config current-context
```

### Basic Operations
```bash
# View cluster info
kubectl cluster-info
kubectl get nodes
kubectl get pods --all-namespaces

# Deploy application
kubectl create deployment nginx --image=nginx:latest
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Scale deployment
kubectl scale deployment nginx --replicas=3

# View logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs

# Delete resources
kubectl delete deployment nginx
kubectl delete service nginx
```

### Helm Package Management

**Commands verified via Context7 (/websites/helm_sh):**

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update repositories
helm repo update

# Search charts
helm search repo bitnami

# Install chart
helm install my-release bitnami/mysql

# List releases
helm list

# Uninstall release
helm uninstall my-release
```

## Cost Management Best Practices

### Pre-Deployment Checklist
- [ ] Estimated cluster runtime (hours/days)
- [ ] Calendar reminder set for deletion
- [ ] Team knows teardown procedure
- [ ] Backup/export strategy for data

### During Hackathon
```bash
# Monitor cluster resources
kubectl top nodes
kubectl top pods --all-namespaces

# Avoid expensive resources:
# - LoadBalancer services (use NodePort for dev)
# - Large persistent volumes
# - High replica counts
```

### Post-Hackathon Cleanup
**Critical:** Delete clusters immediately after hackathon ends.

```bash
# DigitalOcean
doctl kubernetes cluster delete <cluster-name> --force

# Hetzner (requires config file, protect_against_deletion: false)
hetzner-k3s delete --config cluster_config.yaml

# Oracle OKE
oci ce node-pool delete --node-pool-id <id> --force
oci ce cluster delete --cluster-id <id> --force
```

## Common Failures & Solutions

### Authentication Issues

**DigitalOcean:**
```bash
# Symptom: "invalid token"
# Solution:
doctl auth init  # Re-enter token
# Or regenerate at: https://cloud.digitalocean.com/account/api/tokens
```

**Hetzner:**
```bash
# Symptom: "API token invalid"
# Solution:
curl -H "Authorization: Bearer $HETZNER_TOKEN" \
  'https://api.hetzner.cloud/v1/server_types'
# If fails, regenerate token in Hetzner Console
```

**Oracle OCI:**
```bash
# Symptom: "NotAuthenticated"
# Solution:
oci setup config  # Reconfigure
oci iam region list  # Verify
```

### Connection Issues

**kubectl can't connect:**
```bash
# Refresh kubeconfig
# DigitalOcean:
doctl kubernetes cluster kubeconfig save <cluster-name>

# Hetzner:
export KUBECONFIG=$(pwd)/kubeconfig

# Oracle:
oci ce cluster create-kubeconfig --cluster-id <id> --file ~/.kube/config

# Verify context
kubectl config current-context
kubectl get nodes -v=6  # Verbose debugging
```

### Provisioning Stuck

**Cluster stuck "provisioning":**
1. Wait 10-15 minutes (normal for OKE, DOKS)
2. Check provider console/dashboard
3. If stuck >15 minutes, delete and recreate
4. For OCI: Check Always Free quota limits

**Nodes not joining:**
```bash
# Check node status
kubectl get nodes
kubectl describe node <node-name>

# Provider-specific debugging:
# - DigitalOcean: Check droplet status in console
# - Hetzner: SSH into node, check `systemctl status k3s`
# - Oracle: Check compute instance status, security lists
```

### Resource Limits

**Quota exceeded:**
- DigitalOcean: Contact support or upgrade account
- Hetzner: No limits on standard instances
- Oracle: Always Free has strict limits, try different region

## Multi-Cloud Portability Patterns

### Application Deployment (provider-agnostic)
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: webapp
spec:
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer  # Works on all providers
```

**Deploy:**
```bash
kubectl apply -f deployment.yaml
# Same command works on DOKS, K3s, OKE
```

### Storage Considerations

Each provider has different storage classes:
```bash
# List available storage classes
kubectl get storageclass

# DigitalOcean: digitalocean-block-storage
# Hetzner: hcloud-volumes
# Oracle: oci, oci-bv

# Use default for portability:
kubectl get storageclass | grep default
```

### Load Balancer Costs

**Cost implications:**
- DigitalOcean: $12/month per LoadBalancer
- Hetzner: €5.39/month per LoadBalancer
- Oracle: 1 free 10Mbps LB, then paid

**Cost-saving alternative (dev/test):**
```bash
# Use NodePort instead of LoadBalancer
kubectl expose deployment webapp --port=80 --type=NodePort

# Access via node IP:port
kubectl get nodes -o wide
kubectl get svc webapp  # Check NodePort (e.g., 30080)
# Access: http://<node-ip>:<node-port>
```

## Provider-Specific Notes

### DigitalOcean DOKS
✅ **Pros:** Managed control plane, automatic upgrades, easy setup
⚠️ **Cons:** Higher cost, minimum $12/month
📖 **Full guide:** [references/digitalocean-doks.md](references/digitalocean-doks.md)

### Hetzner K3s
✅ **Pros:** Lowest cost, fast provisioning, K3s simplicity
⚠️ **Cons:** DIY management, requires config file, European regions only
📖 **Full guide:** [references/hetzner-k3s.md](references/hetzner-k3s.md)

### Oracle OKE
✅ **Pros:** Truly free tier, managed Kubernetes
⚠️ **Cons:** High setup complexity, networking prerequisites, capacity issues
📖 **Full guide:** [references/oracle-oke.md](references/oracle-oke.md)

## Documentation Grounding

All CLI commands in this skill are verified via Context7 MCP server documentation:
- **doctl:** `/digitalocean/doctl` (Context7)
- **hetzner-k3s:** `/vitobotta/hetzner-k3s` (Context7)
- **oci-cli:** `/oracle/oci-cli` (Context7)
- **helm:** `/websites/helm_sh` (Context7)
- **kubectl:** K3s documentation (Context7)

Commands marked "⚠️ UNVERIFIED" require checking official documentation:
- [OCI OKE Documentation](https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm)

## Safety Warnings

**⚠️ ALWAYS:**
- Set calendar reminders to delete clusters
- Verify deletion in provider console
- Check for orphaned resources (load balancers, volumes)
- Monitor costs daily during multi-day hackathons

**⚠️ NEVER:**
- Hardcode credentials in config files
- Commit API tokens to version control
- Leave clusters running after hackathon
- Use production credentials for testing

## Quick Reference Commands

**Provider CLI verification:**
```bash
# Check installed CLIs
doctl version
hetzner-k3s version
oci --version
kubectl version --client
helm version

# Check authentication
doctl account get
curl -H "Authorization: Bearer $HETZNER_TOKEN" https://api.hetzner.cloud/v1/server_types
oci iam region list
```

**Universal cleanup:**
```bash
# List all clusters
doctl kubernetes cluster list
# (Hetzner: check Hetzner Console)
oci ce cluster list --compartment-id <id>

# Delete pattern
<provider-delete-command> <cluster-name> --force
```

## Additional Resources

**Official Documentation:**
- [DigitalOcean DOKS](https://docs.digitalocean.com/products/kubernetes/)
- [Hetzner K3s Tool](https://github.com/vitobotta/hetzner-k3s)
- [Oracle OKE](https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)

**Cost Calculators:**
- [DigitalOcean Pricing](https://www.digitalocean.com/pricing/kubernetes)
- [Hetzner Cloud Pricing](https://www.hetzner.com/cloud)
- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
