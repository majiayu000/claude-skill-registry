---
name: pulumi-k8s-generator
type: standard
depth: extended
description: >-
  Generates production-ready Pulumi K8s TypeScript resources following deploy.ts
  patterns. Use when creating new Deployments, Services, Ingress, Gateway API,
  HPA, ConfigMaps, Secrets, PVCs, DaemonSets, NetworkPolicies, PDBs,
  ValidatingAdmissionPolicies, or ComponentResources in infrastructure code. NOT
  for validating existing Pulumi code (use pulumi-k8s-validator).
---

# [H1][PULUMI-K8S-GENERATOR]
>**Dictum:** *Infrastructure code follows deploy.ts canonical patterns.*

<br>

Generate Pulumi K8s resources in TypeScript: `_CONFIG` + `_Ops` + dispatch table.

**Provider:** current stable `@pulumi/kubernetes` (Server-Side Apply default) | **K8s:** 1.32-1.35 | **Canonical:** `infrastructure/src/deploy.ts` (207 LOC)

| Use this skill                       | Use OTHER skill                                |
| ------------------------------------ | ---------------------------------------------- |
| Create/generate Pulumi K8s resources | `pulumi-k8s-validator`: Validate existing code |
| Build ComponentResource compositions | `k8s-debug`: Debug deployed resources          |
| Define multi-resource stacks         | `observability-stack`: Observability infra     |

**Tasks:**
1. Gather requirements (table below)
2. Lookup API docs via `context7-tools` for `@pulumi/kubernetes` target kind; fallback: WebSearch `"@pulumi/kubernetes" "<kind>" TypeScript API 2025`
3. Read `references/pulumi_k8s_patterns.md` -- naming, labels, security, mode dispatch
4. Read `references/resource_templates.md` -- templates, factories, ComponentResource, advanced patterns
5. Read `infrastructure/src/deploy.ts` -- canonical implementation
6. Generate resources per architecture and standards below
7. Invoke `pulumi-k8s-validator` skill
8. Deliver summary table with `pulumi preview` / `pulumi up` next steps

---
## [1][REQUIREMENTS]
>**Dictum:** *Gather all inputs before generation.*

<br>

| Field              | Required | Default                                         | deploy.ts Reference            |
| ------------------ | -------- | ----------------------------------------------- | ------------------------------ |
| Deployment mode    | YES      | --                                              | `_Ops.mode()` (line 64)        |
| Resource kind(s)   | YES      | --                                              | --                             |
| Container image    | YES      | --                                              | `input.api.image` (line 163)   |
| Port               | YES      | `4000`                                          | `_CONFIG.ports.api` (line 22)  |
| Health paths       | YES      | `/api/health/liveness`, `/api/health/readiness` | `_CONFIG.k8s.probes` (line 19) |
| CPU/memory         | NO       | `small` preset                                  | `input.api.cpu` (line 168)     |
| HPA min/max/target | NO       | env-driven                                      | `input.hpa.*` (line 174)       |
| PVC size           | NO       | `10Gi`                                          | `_k8sObserve` (line 120)       |
| Namespace          | NO       | `parametric`                                    | `_CONFIG.k8s.namespace`        |

Mode: `cloud` (K8s+AWS) or `selfhosted` (Docker). Kind: Deployment, Service, Ingress, Gateway, HTTPRoute, GRPCRoute, HPA, ConfigMap, Secret, PVC, DaemonSet, NetworkPolicy, PDB, ValidatingAdmissionPolicy, ComponentResource.

---
## [2][ARCHITECTURE]
>**Dictum:** *deploy.ts layers structure all generated code.*

<br>

| Layer         | Purpose                                                      | Lines   |
| ------------- | ------------------------------------------------------------ | ------- |
| `_CONFIG`     | Immutable `as const` -- ports, labels, probes, images        | 11-24   |
| `_Ops`        | Pure factories -- `meta()`, `k8sUrl()`, `secret()`, `fail()` | 28-119  |
| `_k8sObserve` | Array-driven factory: PVC+ConfigMap+Deployment+Service       | 120-126 |
| `_DEPLOY`     | Dispatch table `{ cloud, selfhosted } as const`              | 130-195 |
| `deploy`      | Entry point: resolves mode, delegates to dispatch            | 199-202 |

**Guidance:**
- `Mode dispatch` - Cloud uses ClusterIP + nginx ingress. Selfhosted uses `@pulumi/docker` exclusively.
- `Output tracking` - Use `namespace.metadata.name` (Output) for implicit dependency ordering.
- `Secrets` - `pulumi.secret()` wraps sensitive values; `pulumi.interpolate` for `Output<T>` strings.
- `Factories` - Array-driven `_k8sObserve` pattern for repetitive resource groups.

**Best-Practices:**
- Resources require `requests` + `limits` (env-driven, deploy.ts:168). Guaranteed QoS when `limits == requests`.
- All workloads require liveness + readiness + startup probes (deploy.ts:19).
- New workloads require `_SECURITY` pod/container contexts (see resource_templates.md).
- `terminationGracePeriodSeconds: 30` on all pod specs (deploy.ts:171).
- `as const satisfies` for config objects; `pulumi.interpolate` only when mixing `Output<T>`.
- PodDisruptionBudget required for `replicas >= 2`. NetworkPolicy required for production namespaces.
- `topologySpreadConstraints` for zone distribution; pod anti-affinity for node distribution.

---
## [3][MODE_RULES]
>**Dictum:** *Mode dispatch prevents cross-concern resource creation.*

<br>

| Concern | `cloud` (K8s + AWS)                       | `selfhosted` (Docker)                |
| ------- | ----------------------------------------- | ------------------------------------ |
| Compute | Deployment + Service (ClusterIP)          | `docker.Container` + Traefik labels  |
| Ingress | Ingress (nginx class) or Gateway API      | Traefik reverse proxy                |
| Scaling | HPA (CPU + memory targets)                | None                                 |
| Config  | ConfigMap + Secret                        | `docker.Container.envs`              |
| Data    | AWS RDS + ElastiCache + S3                | Docker containers (pg, redis, minio) |
| TLS     | Ingress TLS + ssl-redirect annotation     | Let's Encrypt via Traefik            |
| Observe | DaemonSet (Alloy) + `_k8sObserve` factory | Docker containers with uploads       |

[CRITICAL] Cloud: ClusterIP + nginx ingress (NOT LoadBalancer + ALB). Selfhosted: `@pulumi/docker` only (NOT Kubernetes).

---
## [4][TROUBLESHOOTING]
>**Dictum:** *Common failures have deterministic fixes.*

<br>

| Issue                        | Cause                             | Fix                                                           |
| ---------------------------- | --------------------------------- | ------------------------------------------------------------- |
| Type errors on k8s resources | API shape changed in provider     | Verify against current stable API via context7                |
| Preview fails on namespace   | Namespace not yet created         | Use `namespace.metadata.name` Output for implicit dep         |
| Cross-stack reference errors | Wrong format or different backend | Format: `<org>/<project>/<stack>`, same backend required      |
| Selfhosted creating k8s      | Mode violation                    | Selfhosted uses `@pulumi/docker` only                         |
| `already exists` in preview  | Resource in cluster not in state  | `pulumi import <type> <name> <id>`                            |
| Replace instead of update    | Immutable field changed           | See `pulumi-k8s-validator/references/common_issues.md`        |
| Server-Side Apply conflicts  | Field manager ownership conflict  | `pulumi refresh` or set field manager explicitly              |
| Gateway API not found        | CRDs not installed                | Install gateway controller before Gateway/HTTPRoute/GRPCRoute |
