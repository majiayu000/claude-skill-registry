---
name: secure-deployment
version: "2.0.0"
description: Security best practices for deploying AI/ML models to production environments
sasmp_version: "1.3.0"
bonded_agent: 06-api-security-tester
bond_type: SECONDARY_BOND
# Schema Definitions
input_schema:
  type: object
  required: [deployment_stage]
  properties:
    deployment_stage:
      type: string
      enum: [pre_deployment, deployment, runtime, all]
    environment:
      type: string
      enum: [development, staging, production]
output_schema:
  type: object
  properties:
    security_score:
      type: number
    checks_passed:
      type: integer
    checks_failed:
      type: integer
    recommendations:
      type: array
# Framework Mappings
owasp_llm_2025: [LLM03, LLM06]
nist_ai_rmf: [Govern, Manage]
---

# Secure AI Deployment

Deploy **AI/ML models securely** with defense-in-depth strategies and zero-trust architecture.

## Quick Reference

```yaml
Skill:       secure-deployment
Agent:       06-api-security-tester
OWASP:       LLM03 (Supply Chain), LLM06 (Excessive Agency)
NIST:        Govern, Manage
Use Case:    Secure production deployment
```

## Deployment Pipeline

```
Model Training → [Security Scan] → [Signing] → [Encrypted Storage]
                                                      ↓
[Canary Deploy] ← [Staged Rollout] ← [Integrity Check] ← [Pull]
       ↓
[Production] → [Continuous Monitoring]
```

## Security Stages

### 1. Pre-Deployment Checks

```yaml
Security Scans:
  - model_vulnerability_scan
  - dependency_audit
  - bias_evaluation
  - adversarial_robustness_test
  - pii_leak_detection
  - license_compliance
  - secrets_detection
```

```python
class PreDeploymentChecker:
    def run_all_checks(self, model_path):
        results = []

        # Dependency audit
        results.append(self.audit_dependencies(model_path))

        # Secrets detection
        results.append(self.scan_for_secrets(model_path))

        # PII leak detection
        results.append(self.detect_pii_leakage(model_path))

        # Adversarial robustness
        results.append(self.test_robustness(model_path))

        # Bias evaluation
        results.append(self.evaluate_bias(model_path))

        return results

    def audit_dependencies(self, path):
        """Check for vulnerable dependencies"""
        vulns = self.dependency_scanner.scan(path)
        critical = [v for v in vulns if v.severity == 'CRITICAL']
        if critical:
            return CheckResult("dependencies", "FAIL", critical)
        return CheckResult("dependencies", "PASS")

    def scan_for_secrets(self, path):
        """Detect hardcoded secrets"""
        secrets = self.secret_scanner.scan(path)
        if secrets:
            return CheckResult("secrets", "FAIL", secrets)
        return CheckResult("secrets", "PASS")
```

### 2. Deployment Configuration

```yaml
Container Security:
  base_image: distroless/python3
  user: nonroot (UID 65532)
  filesystem: read-only
  capabilities: drop ALL
  seccomp: runtime/default

Network Security:
  ingress: API gateway only
  egress: allowlist only
  mtls: required
  network_policy: strict

Secrets Management:
  provider: HashiCorp Vault
  injection: sidecar
  rotation: 24 hours
  never_in_env: true

Model Storage:
  encryption: AES-256-GCM
  signing: RSA-4096
  integrity: SHA-256 hash
  access: RBAC enforced
```

```python
# Kubernetes deployment security
SECURE_DEPLOYMENT = """
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 65532
        fsGroup: 65532
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: model-server
        image: distroless/python3:nonroot
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop: ["ALL"]
        resources:
          limits:
            cpu: "4"
            memory: "16Gi"
            nvidia.com/gpu: "1"
          requests:
            cpu: "2"
            memory: "8Gi"
        volumeMounts:
        - name: model
          mountPath: /model
          readOnly: true
        - name: tmp
          mountPath: /tmp
"""
```

### 3. Runtime Protection

```yaml
Isolation:
  runtime: gvisor
  network: namespace isolated
  process: pid namespace

Monitoring:
  logging: structured JSON
  metrics: Prometheus
  tracing: OpenTelemetry
  alerts: PagerDuty

Resource Protection:
  cpu_limit: enforced
  memory_limit: enforced
  gpu_memory: enforced
  timeout: 30 seconds
```

```python
class RuntimeProtection:
    def __init__(self):
        self.timeout = 30  # seconds
        self.max_memory = 16 * 1024**3  # 16GB
        self.rate_limiter = RateLimiter()

    def protected_inference(self, model, input_data, user_id):
        # Rate limiting
        if not self.rate_limiter.allow(user_id):
            raise RateLimitError()

        # Timeout protection
        with timeout(self.timeout):
            # Memory monitoring
            with memory_limit(self.max_memory):
                result = model.infer(input_data)

        # Log the request
        self.log_inference(user_id, input_data, result)

        return result
```

### 4. Staged Rollout

```yaml
Rollout Strategy:
  canary:
    initial_percentage: 5%
    increment: 10%
    interval: 1 hour
    success_criteria:
      - error_rate < 0.1%
      - latency_p99 < 5s
      - no_security_alerts

  rollback:
    automatic: true
    triggers:
      - error_rate > 1%
      - security_alert
      - latency_p99 > 10s
```

## Security Checklist

```yaml
Pre-Deployment:
  - [ ] Dependencies scanned and patched
  - [ ] Secrets removed from codebase
  - [ ] PII leak testing passed
  - [ ] Adversarial robustness validated
  - [ ] Model signed and verified
  - [ ] Access controls configured

Deployment:
  - [ ] Non-root container
  - [ ] Read-only filesystem
  - [ ] Resource limits set
  - [ ] Network policies applied
  - [ ] Secrets via vault
  - [ ] TLS/mTLS enabled

Runtime:
  - [ ] Monitoring enabled
  - [ ] Alerting configured
  - [ ] Logging comprehensive
  - [ ] Rate limiting active
  - [ ] Rollback tested
```

## CI/CD Security Gates

```yaml
# .github/workflows/secure-deploy.yml
name: Secure Deployment

jobs:
  security-scan:
    steps:
      - name: Dependency Audit
        run: pip-audit --strict

      - name: Secret Scan
        run: gitleaks detect

      - name: Container Scan
        run: trivy image $IMAGE

      - name: SBOM Generation
        run: syft $IMAGE -o spdx-json

  deploy:
    needs: security-scan
    steps:
      - name: Sign Image
        run: cosign sign $IMAGE

      - name: Verify Signature
        run: cosign verify $IMAGE

      - name: Deploy Canary
        run: kubectl apply -f canary.yaml
```

## Severity Classification

```yaml
CRITICAL:
  - Secrets in codebase
  - Critical vulnerabilities
  - No authentication

HIGH:
  - Root container
  - Missing encryption
  - No rate limiting

MEDIUM:
  - Missing resource limits
  - Incomplete logging
  - Outdated dependencies

LOW:
  - Non-optimal configs
  - Missing SBOM
```

## Troubleshooting

```yaml
Issue: Deployment failing security scan
Solution: Update dependencies, remove secrets, fix configs

Issue: Container won't start (read-only FS)
Solution: Use tmpfs for temp files, volume for model

Issue: High latency after security layers
Solution: Optimize validation, use caching, async logging
```

## Integration Points

| Component | Purpose |
|-----------|---------|
| Agent 06 | Security testing |
| Agent 08 | CI/CD automation |
| /test api | Pre-deploy testing |
| ArgoCD | GitOps deployment |

---

**Deploy AI models securely with defense-in-depth practices.**
