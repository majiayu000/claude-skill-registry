---
name: helm
description: Kubernetes package manager for installing, upgrading, and managing applications.
---

# Helm

```ps1

helm template helm-app .  --values values.yaml -n helm-demo

helm template helm-demo
helm package helm-demo
helm install helm-demo --generate-name -n helm-demo --debug
helm list -n helm-demo
helm upgrade helm-demo-1757482975 helm-demo -n helm-demo --debug
helm uninstall helm-demo-1757482975 helm-demo -n helm-demo --debug
```