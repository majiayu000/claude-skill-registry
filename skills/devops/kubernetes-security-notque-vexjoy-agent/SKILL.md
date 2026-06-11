---
name: kubernetes-security
description: "Kubernetes security: RBAC, PodSecurity, network policies."
user-invocable: false
context: fork
agent: kubernetes-helm-engineer
routing:
  triggers:
    - "kubernetes security"
    - "k8s RBAC"
    - "RBAC setup"
    - "pod security policy"
    - "network policy"
  category: kubernetes
  pairs_with:
    - kubernetes-debugging
    - cobalt-core
---

# Kubernetes Security Skill

Harden Kubernetes clusters and workloads through RBAC, pod security, network isolation, secret management, and supply chain controls.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| RBAC, Role, RoleBinding, ClusterRole, ServiceAccount, least-privilege, access control, permissions | `references/rbac-patterns.md` | ~60 lines |
| PodSecurity, SecurityContext, runAsNonRoot, readOnlyRootFilesystem, restricted, baseline, image hardening, distroless, Dockerfile | `references/pod-security.md` | ~90 lines |
| NetworkPolicy, default-deny, allow-list, egress, ingress, DNS, lateral movement, namespace isolation | `references/network-policies.md` | ~70 lines |
| cosign, Kyverno, OPA, admission controller, Sealed Secrets, External Secrets, supply chain, misconfiguration, privileged | `references/supply-chain.md` | ~120 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.

---

## Phase 1: IDENTIFY

Determine which security domain the user is asking about.

| Domain | Reference |
|--------|-----------|
| Access control, permissions, roles | `references/rbac-patterns.md` |
| Pod hardening, container security | `references/pod-security.md` |
| Network isolation, traffic rules | `references/network-policies.md` |
| Image signing, secrets, admission control | `references/supply-chain.md` |

If the question spans multiple domains, load all relevant references. Most production hardening tasks touch at least RBAC + pod security.

**Gate**: Domain identified. Reference(s) loaded. Proceed to Phase 2.

---

## Phase 2: RESPOND

Use loaded reference knowledge to answer with concrete YAML manifests and specific configurations. The references contain complete, copy-paste-ready examples for each security domain.

For general Kubernetes debugging, pair with the `kubernetes-debugging` skill.

**Gate**: Question answered with reference-backed manifests, not generic advice.

---

## Phase 3: VERIFY

Validate the security posture against the misconfiguration table in `references/supply-chain.md`. Flag any of the 8 common misconfigurations if present in the user's manifests.

---

## References

- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [External Secrets Operator](https://external-secrets.io/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- [Cosign](https://docs.sigstore.dev/cosign/overview/)
- [Kyverno](https://kyverno.io/)
