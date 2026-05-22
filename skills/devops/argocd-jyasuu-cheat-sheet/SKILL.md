---
name: argocd
description: GitOps continuous delivery tool for Kubernetes with repository management and application synchronization.
---

# ArgoCD

```ps1

$version = (Invoke-RestMethod https://api.github.com/repos/argoproj/argo-cd/releases/latest).tag_name
$url = "https://github.com/argoproj/argo-cd/releases/download/" + $version + "/argocd-windows-amd64.exe"
$output = "argocd.exe"
Invoke-WebRequest -Uri $url -OutFile $output
argocd login argocd.example.com --sso


argocd repo add https://github.com/jyasuu/helm-demo.git `
 --username ? `
 --password ?

argocd app create helm-app `
  --repo https://github.com/jyasuu/helm-demo.git `
  --path . `
  --revision main `
  --dest-server https://kubernetes.default.svc `
  --dest-namespace helm-demo `
  --sync-policy automated `
  --values values-lab.yaml `
  --project helm-app

argocd app list
argocd app sync helm-app
argocd app delete helm-app
argocd app history helm-app
argocd app manifests helm-app
```