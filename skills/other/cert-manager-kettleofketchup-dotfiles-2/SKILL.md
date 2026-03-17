---
name: cert-manager
description: Kubernetes certificate management debugging and configuration. This skill should be used when troubleshooting cert-manager issues, configuring private CA issuers (SelfSigned, CA, Vault), integrating with Traefik IngressRoute TLS, diagnosing Certificate/CertificateRequest/Issuer problems, or debugging webhook connectivity issues.
---

# cert-manager

Kubernetes-native TLS certificate lifecycle management. Automates issuance, renewal, and rotation from private CAs.

## Debugging Workflow

When certificates fail, debug the resource chain in order:

```
Certificate → CertificateRequest → Issuer/ClusterIssuer
```

**First commands to run:**
```bash
kubectl get certificate,certificaterequest,issuer,clusterissuer -A
kubectl describe certificate <name> -n <namespace>
```

For detailed debugging steps, see `references/troubleshooting-workflow.md`.

## Private CA Configuration

This skill focuses on self-hosted issuers (no Let's Encrypt):

| Issuer Type | Use Case |
|-------------|----------|
| SelfSigned | Bootstrap CA hierarchy, testing |
| CA | Sign with existing CA credentials in Secret |
| Vault | Sign via HashiCorp Vault PKI engine |

### Quick Bootstrap (SelfSigned → CA)

```yaml
# Creates self-signed root, then CA issuer for leaf certs
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: root-ca
  namespace: cert-manager
spec:
  isCA: true
  commonName: root-ca
  secretName: root-ca-secret
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: ca-issuer
spec:
  ca:
    secretName: root-ca-secret
```

For complete issuer configuration, see `references/private-ca-issuers.md`.

## Traefik Integration

Create Certificate resource, reference secret in IngressRoute:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: myapp-tls
spec:
  secretName: myapp-tls-secret
  dnsNames: ["myapp.example.com"]
  issuerRef:
    name: ca-issuer
    kind: ClusterIssuer
---
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
spec:
  entryPoints: [websecure]
  routes:
    - match: Host(`myapp.example.com`)
      kind: Rule
      services:
        - name: myapp-service
          port: 80
  tls:
    secretName: myapp-tls-secret
```

For wildcard certs and Ingress annotations, see `references/traefik-integration.md`.

## Common Issues

| Symptom | Likely Cause | Reference |
|---------|--------------|-----------|
| Certificate stuck Pending | Issuer not ready, CertificateRequest failed | troubleshooting-workflow.md |
| Webhook connection refused | Pod not running, network policy | webhook-issues.md |
| x509 unknown authority | CA bundle not injected | webhook-issues.md |
| Secret not created | Issuer configuration error | troubleshooting-workflow.md |
| Vault permission denied | Vault policy/role misconfigured | private-ca-issuers.md |

## References

- `references/troubleshooting-workflow.md` - Step-by-step debugging
- `references/private-ca-issuers.md` - SelfSigned, CA, Vault configuration
- `references/traefik-integration.md` - IngressRoute TLS setup
- `references/webhook-issues.md` - Webhook connectivity problems
