---
name: external-dns
description: >-
  ExternalDNS for automatic DNS record management in Kubernetes. Use when the
  user needs to synchronize Kubernetes Ingress and Service resources with DNS
  providers like Route 53, CloudDNS, or Cloudflare automatically.
license: Apache-2.0
compatibility: 'linux, macos'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - external-dns
    - dns
    - kubernetes
    - route53
    - cloudflare
---

# ExternalDNS

ExternalDNS synchronizes Kubernetes Services and Ingresses with DNS providers, automatically creating and updating DNS records.

## Installation with Helm

```bash
# Install ExternalDNS via Helm
helm repo add external-dns https://kubernetes-sigs.github.io/external-dns/
helm repo update

helm install external-dns external-dns/external-dns \
  --namespace external-dns \
  --create-namespace \
  --values values.yaml
```

## AWS Route 53 Configuration

```yaml
# values-aws.yaml — Helm values for AWS Route 53 provider
provider:
  name: aws

env:
  - name: AWS_DEFAULT_REGION
    value: us-east-1

extraArgs:
  - --source=service
  - --source=ingress
  - --domain-filter=example.com
  - --aws-zone-type=public
  - --policy=upsert-only
  - --registry=txt
  - --txt-owner-id=my-cluster

serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/external-dns
```

```json
// iam-policy.json — IAM policy for ExternalDNS Route 53 access
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["route53:ChangeResourceRecordSets"],
      "Resource": ["arn:aws:route53:::hostedzone/Z1234567890"]
    },
    {
      "Effect": "Allow",
      "Action": ["route53:ListHostedZones", "route53:ListResourceRecordSets", "route53:ListTagsForResource"],
      "Resource": ["*"]
    }
  ]
}
```

## Google Cloud DNS Configuration

```yaml
# values-gcp.yaml — Helm values for Google Cloud DNS provider
provider:
  name: google

extraArgs:
  - --source=service
  - --source=ingress
  - --domain-filter=example.com
  - --google-project=my-gcp-project
  - --google-zone-visibility=public
  - --policy=sync
  - --registry=txt
  - --txt-owner-id=my-cluster
```

## Cloudflare Configuration

```yaml
# values-cloudflare.yaml — Helm values for Cloudflare provider
provider:
  name: cloudflare

env:
  - name: CF_API_TOKEN
    valueFrom:
      secretKeyRef:
        name: cloudflare-api-token
        key: api-token

extraArgs:
  - --source=service
  - --source=ingress
  - --domain-filter=example.com
  - --cloudflare-proxied
  - --policy=sync
```

```yaml
# cloudflare-secret.yaml — Cloudflare API token secret
apiVersion: v1
kind: Secret
metadata:
  name: cloudflare-api-token
  namespace: external-dns
type: Opaque
stringData:
  api-token: "your-cloudflare-api-token"
```

## Service Annotations

```yaml
# service-lb.yaml — LoadBalancer service with DNS annotations
apiVersion: v1
kind: Service
metadata:
  name: web-app
  annotations:
    external-dns.alpha.kubernetes.io/hostname: app.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
    - port: 80
      targetPort: 8080
```

```yaml
# service-multi.yaml — Service with multiple DNS hostnames
apiVersion: v1
kind: Service
metadata:
  name: api-service
  annotations:
    external-dns.alpha.kubernetes.io/hostname: "api.example.com,api-v2.example.com"
    external-dns.alpha.kubernetes.io/ttl: "60"
    external-dns.alpha.kubernetes.io/cloudflare-proxied: "true"
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
    - port: 443
      targetPort: 8443
```

## Ingress Annotations

```yaml
# ingress-dns.yaml — Ingress with ExternalDNS auto-registration
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app
  annotations:
    external-dns.alpha.kubernetes.io/ttl: "120"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-app
                port:
                  number: 80
```

## Istio Gateway Source

```yaml
# values-istio.yaml — ExternalDNS with Istio Gateway source
extraArgs:
  - --source=istio-gateway
  - --source=istio-virtualservice
  - --domain-filter=example.com
  - --policy=sync
```

## Full Deployment Manifest

```yaml
# external-dns-deploy.yaml — ExternalDNS deployment without Helm
apiVersion: apps/v1
kind: Deployment
metadata:
  name: external-dns
  namespace: external-dns
spec:
  replicas: 1
  selector:
    matchLabels:
      app: external-dns
  template:
    metadata:
      labels:
        app: external-dns
    spec:
      serviceAccountName: external-dns
      containers:
        - name: external-dns
          image: registry.k8s.io/external-dns/external-dns:v0.14.0
          args:
            - --source=service
            - --source=ingress
            - --domain-filter=example.com
            - --provider=aws
            - --policy=sync
            - --registry=txt
            - --txt-owner-id=my-cluster
            - --interval=1m
            - --log-level=info
          env:
            - name: AWS_DEFAULT_REGION
              value: us-east-1
```

## Common Commands

```bash
# Check ExternalDNS logs
kubectl logs -n external-dns deploy/external-dns -f

# Verify DNS records were created
dig app.example.com
nslookup app.example.com

# Check TXT ownership records
dig TXT app.example.com

# Dry-run mode (add to args)
# --dry-run  — logs changes without applying
```
