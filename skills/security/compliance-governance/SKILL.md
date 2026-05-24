---
name: compliance-governance
description: Provides compliance, governance, and supply chain security guidance for cloud-native systems. Covers OPA Rego policies, Kyverno cluster policies, SBOM generation, SLSA provenance, audit trail design, and regulatory framework mapping. Use when user mentions 'compliance', 'governance', 'OPA', 'kyverno', 'SBOM', 'SLSA', 'audit', 'policy-as-code', 'SOC2', 'HIPAA', 'PCI-DSS', 'artifact signing'.
---

# Compliance and Governance

Best practices for implementing policy-as-code, supply chain security, audit trails, and regulatory compliance in cloud-native environments. This skill covers the full lifecycle from policy authoring to continuous compliance monitoring and evidence generation.

## Regulatory Framework Comparison

Understanding which controls map to which framework prevents duplicate work and identifies gaps.

| Control Domain | SOC 2 (TSC) | HIPAA | PCI-DSS v4.0 | FedRAMP | ISO 27001 |
|----------------|-------------|-------|---------------|---------|-----------|
| Access Control | CC6.1-CC6.8 | 164.312(a) | Req 7, 8 | AC family | A.9 |
| Audit Logging | CC7.1-CC7.4 | 164.312(b) | Req 10 | AU family | A.12.4 |
| Encryption at Rest | CC6.1 | 164.312(a)(2)(iv) | Req 3 | SC-28 | A.10.1 |
| Encryption in Transit | CC6.7 | 164.312(e) | Req 4 | SC-8 | A.13.1 |
| Vulnerability Mgmt | CC7.1 | 164.308(a)(5)(ii) | Req 6, 11 | RA-5, SI-2 | A.12.6 |
| Incident Response | CC7.3-CC7.5 | 164.308(a)(6) | Req 12.10 | IR family | A.16 |
| Change Management | CC8.1 | 164.308(a)(5)(ii) | Req 6.5 | CM family | A.12.1 |
| Data Classification | CC6.5 | 164.312(d) | Req 3.2-3.4 | RA-2 | A.8.2 |
| Backup & Recovery | CC7.5, A1.2 | 164.308(a)(7) | Req 9.5 | CP family | A.12.3 |
| Vendor Management | CC9.2 | 164.308(b) | Req 12.8 | SA family | A.15 |

### Framework Selection Guidance

| Your Industry | Start With | Add When Needed |
|----------------|-----------|-----------------|
| SaaS B2B | SOC 2 Type II | ISO 27001 for international |
| Healthcare | HIPAA + SOC 2 | HITRUST for certification |
| E-commerce / Payments | PCI-DSS | SOC 2 for broader trust |
| Government / Defense | FedRAMP | NIST 800-171 for CUI |
| Finance | SOC 2 + PCI-DSS | SOX for public companies |

## Policy-as-Code with OPA

Open Policy Agent (OPA) evaluates policies written in Rego against structured data. Policies are version-controlled, tested, and deployed alongside application code.

### OPA Architecture

```
                    +------------------+
                    |  Policy Bundle   |
                    |  (Git repo)      |
                    +--------+---------+
                             |
                    +--------v---------+
  Request -------->|   OPA Server     |-------> Allow / Deny
  (JSON input)     |   (Rego engine)  |         + Reasons
                    +--------+---------+
                             |
                    +--------v---------+
                    |   Decision Log   |
                    |   (audit trail)  |
                    +------------------+
```

### OPA Rego Policy: Kubernetes Admission Control

```rego
package kubernetes.admission

import rego.v1

# Deny containers running as root
deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.containers
    not container.securityContext.runAsNonRoot
    msg := sprintf(
        "Container '%s' in Pod '%s' must set securityContext.runAsNonRoot=true",
        [container.name, input.request.object.metadata.name]
    )
}

# Deny images without digest pinning
deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.containers
    not contains(container.image, "@sha256:")
    not startswith(container.image, "registry.internal.company.com/")
    msg := sprintf(
        "Container '%s' uses unpinned image '%s'. Pin with @sha256: digest.",
        [container.name, container.image]
    )
}

# Require resource limits on all containers
deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.containers
    not container.resources.limits.memory
    msg := sprintf(
        "Container '%s' must define resources.limits.memory",
        [container.name]
    )
}

# Require labels for cost tracking
deny contains msg if {
    input.request.kind.kind in {"Deployment", "StatefulSet", "DaemonSet"}
    not input.request.object.metadata.labels["cost-center"]
    msg := sprintf(
        "%s '%s' must have label 'cost-center' for cost allocation",
        [input.request.kind.kind, input.request.object.metadata.name]
    )
}
```

### OPA Policy Testing

```rego
package kubernetes.admission_test

import rego.v1

test_deny_root_container if {
    result := deny with input as {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "metadata": {"name": "test-pod"},
                "spec": {
                    "containers": [{
                        "name": "app",
                        "image": "nginx@sha256:abc123",
                        "securityContext": {},
                        "resources": {"limits": {"memory": "128Mi"}}
                    }]
                }
            }
        }
    }
    count(result) > 0
    some msg in result
    contains(msg, "runAsNonRoot")
}

test_allow_nonroot_container if {
    result := deny with input as {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "metadata": {"name": "test-pod"},
                "spec": {
                    "containers": [{
                        "name": "app",
                        "image": "nginx@sha256:abc123",
                        "securityContext": {"runAsNonRoot": true},
                        "resources": {"limits": {"memory": "128Mi"}}
                    }]
                }
            }
        }
    }
    count(result) == 0
}
```

## Policy-as-Code with Kyverno

Kyverno uses Kubernetes-native YAML for policies. No new language to learn.

### Kyverno ClusterPolicy: Image Registry Restriction

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
  annotations:
    policies.kyverno.io/title: Restrict Image Registries
    policies.kyverno.io/category: Supply Chain Security
    policies.kyverno.io/severity: high
    policies.kyverno.io/description: >-
      Only allow images from approved registries to prevent
      supply chain attacks via untrusted image sources.
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: validate-registries
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: >-
          Image '{{ images.containers.*.registry }}' is not from an
          approved registry. Allowed: ghcr.io/our-org, registry.internal.company.com
        pattern:
          spec:
            containers:
              - image: "ghcr.io/our-org/* | registry.internal.company.com/*"
            =(initContainers):
              - image: "ghcr.io/our-org/* | registry.internal.company.com/*"

    - name: require-digest
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Images must use digest (@sha256:) not tags for reproducibility."
        pattern:
          spec:
            containers:
              - image: "*@sha256:*"

    - name: add-image-pull-secret
      match:
        any:
          - resources:
              kinds:
                - Pod
      mutate:
        patchStrategicMerge:
          spec:
            imagePullSecrets:
              - name: registry-credentials
```

### OPA vs Kyverno Comparison

| Aspect | OPA / Gatekeeper | Kyverno |
|--------|-----------------|---------|
| Policy Language | Rego (purpose-built) | YAML (K8s-native) |
| Learning Curve | Steep (new language) | Gentle (familiar YAML) |
| Mutation Support | Limited | First-class |
| Generation Support | No | Yes (create resources) |
| Image Verification | Via external data | Built-in (cosign/notary) |
| Audit Reports | Custom | Built-in PolicyReport |
| Multi-cluster | Bundle server | Shared policies via Git |
| Best For | Complex logic, multi-system | K8s-only, team adoption |

## Supply Chain Security

### SBOM Generation with Syft

A Software Bill of Materials (SBOM) catalogs every component in your software. Required by executive orders and increasingly by enterprise customers.

```bash
# Generate SBOM from container image
syft ghcr.io/our-org/api:v1.2.3 -o spdx-json > sbom-api-v1.2.3.spdx.json

# Generate SBOM from source directory
syft dir:./src -o cyclonedx-json > sbom-source.cdx.json

# Generate SBOM from Dockerfile
syft docker:Dockerfile -o spdx-json > sbom-dockerfile.spdx.json

# Scan SBOM for vulnerabilities with Grype
grype sbom:./sbom-api-v1.2.3.spdx.json --fail-on high

# CI integration: generate + scan + attest in one pipeline
syft ghcr.io/our-org/api:v1.2.3 -o spdx-json | \
  tee sbom.spdx.json | \
  grype --fail-on critical
```

### SBOM Format Comparison

| Aspect | SPDX | CycloneDX |
|--------|------|-----------|
| Origin | Linux Foundation | OWASP |
| ISO Standard | ISO/IEC 5962:2021 | ECMA-424 |
| Primary Focus | Licensing + provenance | Security + dependencies |
| Gov. Requirement | US EO 14028 (preferred) | Widely accepted |
| Tooling | Broader ecosystem | Better vulnerability focus |
| Best For | License compliance | Security analysis |

### SLSA Provenance

Supply-chain Levels for Software Artifacts (SLSA) provides a framework for ensuring artifact integrity.

| SLSA Level | Requirements | Trust |
|------------|-------------|-------|
| Level 0 | No guarantees | None |
| Level 1 | Build process documented | Provenance exists |
| Level 2 | Hosted build, signed provenance | Tamper-resistant provenance |
| Level 3 | Hardened build platform | Tamper-proof provenance |

### SLSA Provenance with GitHub Actions

```yaml
name: Release with SLSA Provenance

on:
  push:
    tags: ['v*']

permissions:
  contents: write
  packages: write
  id-token: write       # OIDC for keyless signing
  attestations: write   # GitHub artifact attestations

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        id: build
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Attest SBOM
        uses: actions/attest-sbom@v2
        with:
          subject-name: ghcr.io/${{ github.repository }}
          subject-digest: ${{ steps.build.outputs.digest }}
          sbom-path: sbom.spdx.json

      - name: Attest build provenance
        uses: actions/attest-build-provenance@v2
        with:
          subject-name: ghcr.io/${{ github.repository }}
          subject-digest: ${{ steps.build.outputs.digest }}
```

### Artifact Signing with Cosign

```bash
# Install cosign
go install github.com/sigstore/cosign/v2/cmd/cosign@latest

# Keyless signing (recommended -- uses OIDC identity)
cosign sign ghcr.io/our-org/api@sha256:abc123def456

# Verify signature
cosign verify ghcr.io/our-org/api@sha256:abc123def456 \
  --certificate-identity=https://github.com/our-org/api/.github/workflows/release.yml@refs/tags/v1.2.3 \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com

# Sign with key pair (for air-gapped environments)
cosign generate-key-pair
cosign sign --key cosign.key ghcr.io/our-org/api@sha256:abc123def456
cosign verify --key cosign.pub ghcr.io/our-org/api@sha256:abc123def456

# Attach SBOM as attestation
cosign attest --predicate sbom.spdx.json \
  --type spdxjson \
  ghcr.io/our-org/api@sha256:abc123def456
```

## Audit Trail Architecture

Every compliance framework requires audit logging. Design for immutability and completeness.

### Audit Event Schema

```json
{
  "event_id": "uuid-v7",
  "timestamp": "2025-03-15T14:30:00.000Z",
  "actor": {
    "type": "user|service|system",
    "id": "user-123",
    "ip": "10.0.1.50",
    "session_id": "sess-abc"
  },
  "action": {
    "type": "create|read|update|delete|login|export|approve",
    "resource": "patient-record",
    "resource_id": "rec-456"
  },
  "context": {
    "service": "api-gateway",
    "environment": "production",
    "request_id": "req-789",
    "correlation_id": "corr-012"
  },
  "outcome": {
    "status": "success|failure|denied",
    "reason": "insufficient_permissions",
    "policy_violated": "rbac-admin-only"
  },
  "changes": {
    "before": {"status": "active"},
    "after": {"status": "suspended"}
  },
  "metadata": {
    "compliance_scope": ["hipaa", "soc2"],
    "data_classification": "pii",
    "retention_days": 2555
  }
}
```

### Audit Trail Pipeline

```
Application --> Structured Log --> Log Aggregator --> Immutable Store
    |                                    |                   |
    v                                    v                   v
  stdout/          Fluentd/Vector    S3 (WORM) +
  event bus        with schema       CloudTrail
                   validation        Lake
                                         |
                                         v
                                   SIEM / Query
                                   (Athena, Splunk,
                                    Elastic)
```

### Retention Requirements by Framework

| Framework | Minimum Retention | Recommended | Notes |
|-----------|------------------|-------------|-------|
| SOC 2 | 1 year | 3 years | Auditor needs rolling 12 months |
| HIPAA | 6 years | 7 years | From date of creation or last effective date |
| PCI-DSS | 1 year | 3 years | Immediate access to 3 months |
| FedRAMP | 3 years | 6 years | May vary by data classification |
| GDPR | No minimum | Case-by-case | Must justify retention period |

## RBAC and Access Control

### Kubernetes RBAC Policy

```yaml
# Principle: least privilege, namespace-scoped, no wildcard verbs
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-developer
  namespace: team-alpha
rules:
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["pods", "pods/log", "services", "configmaps"]
    verbs: ["get", "list", "watch"]
  # Explicitly NO access to: secrets, persistent volumes, cluster roles
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-developer-binding
  namespace: team-alpha
subjects:
  - kind: Group
    name: team-alpha-devs
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: app-developer
  apiGroup: rbac.authorization.k8s.io
```

### Access Control Comparison

| Model | When to Use | Complexity | Example |
|-------|------------|------------|---------|
| RBAC | Standard team structures | Low | Developer, Admin, Viewer roles |
| ABAC | Dynamic, attribute-driven | Medium | "Allow if department=engineering AND env=staging" |
| ReBAC | Relationship-heavy domains | High | "Allow if user is owner of parent folder" |
| PBAC | Compliance-driven | Medium | OPA/Cedar policies |

## Policy-as-Code Workflow

```
Author Policy --> Unit Test --> Review PR --> Merge --> Deploy to OPA/Kyverno
    |                |              |            |              |
    v                v              v            v              v
  Rego/YAML      opa test      Peer +        Main           Gatekeeper
  in Git         conftest      Security      branch         admission
                                review                      controller
                                                               |
                                                               v
                                                         Audit + Alert
                                                         on violations
```

### CI Pipeline for Policy Testing

```yaml
name: Policy CI

on:
  pull_request:
    paths:
      - 'policies/**'

jobs:
  test-opa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install OPA
        run: |
          curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
          chmod +x opa && sudo mv opa /usr/local/bin/

      - name: Run policy unit tests
        run: opa test policies/ -v

      - name: Check policy formatting
        run: opa fmt --diff policies/

      - name: Validate against sample resources
        run: |
          for fixture in test-fixtures/*.json; do
            echo "Testing: $fixture"
            opa eval -i "$fixture" -d policies/ "data.kubernetes.admission.deny" \
              --format pretty
          done

  test-kyverno:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Kyverno CLI
        run: |
          curl -LO https://github.com/kyverno/kyverno/releases/latest/download/kyverno-cli_linux_x86_64.tar.gz
          tar xzf kyverno-cli_linux_x86_64.tar.gz
          sudo mv kyverno /usr/local/bin/

      - name: Test Kyverno policies
        run: kyverno test policies/kyverno/tests/
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Manual compliance checks | Inconsistent, unscalable, audit failures | Automate with OPA/Kyverno in admission control |
| Policies in wikis, not code | Drift between docs and enforcement | Policy-as-code in Git with CI testing |
| `ClusterRole` with wildcard verbs | Grants full cluster access, violates least privilege | Namespace-scoped Roles with explicit verb lists |
| SBOM generated once, never updated | Stale dependency data, missed CVEs | Generate SBOM on every build, scan continuously |
| Audit logs in application database | Mutable, deletable, single point of failure | Write-once storage (S3 Object Lock, immutable volumes) |
| Tag-based image references | Mutable tags allow supply chain attacks | Pin images by `@sha256:` digest |
| Unsigned artifacts in production | No provenance, no tamper detection | Sign with cosign, verify in admission control |
| "We'll add compliance later" | Retrofit is 10x more expensive | Build compliance controls into CI from day one |
| Single compliance framework mapping | Duplicate control implementations | Map controls across frameworks (unified control matrix) |
| No policy dry-run before enforce | Policies break production workloads | Use `Audit` mode first, review PolicyReport, then `Enforce` |
| Shared service accounts across teams | No accountability, impossible to audit | Per-team service accounts with scoped permissions |
| Storing secrets in ConfigMaps | ConfigMaps are not encrypted at rest | Use Secrets with encryption, or external secret managers |
| No evidence collection automation | Scramble before audits, missing proof | Automate evidence gathering with scheduled jobs |

## Compliance Automation Checklist

- [ ] Policy-as-code repository established with CI/CD pipeline
- [ ] OPA or Kyverno deployed as admission controller in all clusters
- [ ] Policies run in audit mode before enforcement
- [ ] SBOM generated on every container build
- [ ] SBOM scanned for vulnerabilities with severity thresholds
- [ ] Artifacts signed with cosign (keyless via OIDC preferred)
- [ ] Signature verification enforced in admission control
- [ ] Audit logs written to immutable storage (WORM/Object Lock)
- [ ] Audit log retention meets framework requirements
- [ ] RBAC follows least privilege (no wildcard verbs, namespace-scoped)
- [ ] Service accounts scoped per team/application
- [ ] Regulatory control matrix maintained mapping controls across frameworks
- [ ] Evidence collection automated for audit preparation
- [ ] SLSA Level 2+ achieved for production artifacts
- [ ] Policy test coverage tracked (aim for >90%)
- [ ] Compliance dashboard with real-time violation metrics
- [ ] Incident response runbook includes compliance notification procedures
- [ ] Third-party dependencies reviewed for license compliance
- [ ] Data classification labels applied to all storage resources
- [ ] Access reviews scheduled quarterly with automated reports
