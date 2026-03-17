---
name: eks-security
description: EKS security hardening and best practices. Use when configuring cluster security, implementing pod security, managing secrets, preparing for compliance audits, hardening infrastructure, scanning containers, or responding to security incidents.
---

# EKS Security

## Overview

Comprehensive security hardening guide for Amazon EKS clusters following 2025 best practices. This skill covers control plane security, workload isolation, secrets management, network policies, image scanning, runtime security, and compliance frameworks.

**Keywords**: EKS security, cluster hardening, IRSA, Pod Security Standards, network policies, secrets management, compliance, vulnerability scanning, runtime security, incident response

**Status**: Production-ready (2025 best practices)

## When to Use This Skill

- Hardening new EKS clusters for production
- Implementing security controls and policies
- Configuring RBAC and IAM access
- Setting up secrets management
- Preparing for compliance audits (CIS, NIST, SOC2)
- Responding to security incidents
- Scanning and remediating vulnerabilities
- Implementing zero-trust networking
- Setting up runtime security monitoring

## Security Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     EKS Security Layers                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Control Plane Security                           │
│  • Private API endpoint                                     │
│  • Audit logging enabled                                    │
│  • Secrets encryption with KMS                             │
│  • IP allowlisting                                          │
│                                                             │
│  Layer 2: Authentication & Authorization                    │
│  • IAM Roles for Service Accounts (IRSA)                   │
│  • RBAC with least privilege                               │
│  • Pod Identity for workloads                              │
│  • Service account isolation                               │
│                                                             │
│  Layer 3: Workload Security                                │
│  • Pod Security Standards (restricted)                      │
│  • Security contexts                                        │
│  • Read-only root filesystems                              │
│  • Non-root users                                           │
│  • Resource limits                                          │
│                                                             │
│  Layer 4: Network Security                                  │
│  • Network Policies (VPC CNI 1.14+)                        │
│  • Security Groups for Pods                                │
│  • Private subnets for nodes                               │
│  • VPC Flow Logs                                            │
│  • mTLS with service mesh                                  │
│                                                             │
│  Layer 5: Secrets & Data Protection                        │
│  • External Secrets Operator                               │
│  • AWS Secrets Manager integration                         │
│  • Encrypted etcd                                           │
│  • Automatic rotation                                       │
│                                                             │
│  Layer 6: Image & Runtime Security                         │
│  • Amazon Inspector scanning                               │
│  • Admission controllers (OPA/Gatekeeper)                  │
│  • Runtime monitoring (Falco, GuardDuty)                   │
│  • Image signing/verification                              │
│                                                             │
│  Layer 7: Compliance & Audit                               │
│  • CloudTrail logging                                       │
│  • GuardDuty for EKS                                       │
│  • Security Hub integration                                 │
│  • CIS/NIST compliance checks                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start: Essential Security Checklist

### Cluster Level (Day 0)
- [ ] Enable private API endpoint (or public + IP allowlist)
- [ ] Enable all control plane logging
- [ ] Configure secrets encryption with KMS
- [ ] Use latest Kubernetes version (within 2 versions)
- [ ] Enable audit logging
- [ ] Configure VPC with private subnets

### Node Level (Day 0)
- [ ] Use Amazon Linux 2023 or Bottlerocket AMI
- [ ] Enable IMDSv2 enforcement
- [ ] Minimal IAM permissions for node role
- [ ] Deploy nodes in private subnets only
- [ ] Enable SSM for remote access (disable SSH)
- [ ] Plan for regular node rotation (21 days max)

### Workload Level (Day 1)
- [ ] Implement Pod Security Standards (restricted level)
- [ ] Use IRSA for all AWS service access
- [ ] No privileged containers
- [ ] Configure security contexts (runAsNonRoot, readOnlyRootFilesystem)
- [ ] Set resource limits and requests
- [ ] Use dedicated service accounts per application

### Network Level (Day 1)
- [ ] Enable network policies (VPC CNI 1.14+ or Calico/Cilium)
- [ ] Configure default deny-all policies
- [ ] Use Security Groups for Pods for AWS resource access
- [ ] Enable VPC Flow Logs
- [ ] Restrict egress traffic
- [ ] Deploy private load balancers where possible

### Secrets Management (Day 1)
- [ ] Deploy External Secrets Operator
- [ ] Migrate secrets to AWS Secrets Manager
- [ ] Enable automatic secret rotation
- [ ] Remove hardcoded credentials
- [ ] Audit secret access via CloudTrail

### Image Security (Day 1-2)
- [ ] Enable Amazon Inspector for ECR repositories
- [ ] Configure automatic scanning on push
- [ ] Block deployment of critical vulnerabilities
- [ ] Implement image signing (Sigstore/Notary)
- [ ] Use minimal base images (distroless, Chainguard)
- [ ] ECR lifecycle policies for old images

### Compliance & Monitoring (Day 2-3)
- [ ] Enable GuardDuty for EKS
- [ ] Configure Security Hub
- [ ] Run kube-bench for CIS compliance
- [ ] Deploy runtime security (Falco)
- [ ] Set up CloudWatch alarms for security events
- [ ] Configure SIEM integration

## Security Workflow

### Phase 1: Foundation (Control Plane)
1. Review control plane endpoint configuration
2. Enable comprehensive logging
3. Configure KMS encryption for secrets
4. Set up IAM authentication
5. Implement API access controls

**See**: [references/cluster-security.md](references/cluster-security.md)

### Phase 2: Workload Hardening
1. Implement Pod Security Standards
2. Configure security contexts
3. Set up IRSA for service accounts
4. Deploy RBAC policies
5. Enable admission controllers

**See**: [references/workload-security.md](references/workload-security.md)

### Phase 3: Secrets & Data Protection
1. Deploy External Secrets Operator
2. Migrate secrets to AWS Secrets Manager
3. Configure automatic rotation
4. Set up CSI Secrets Store Driver (if needed)
5. Audit and monitor secret access

**See**: [references/secrets-management.md](references/secrets-management.md)

### Phase 4: Network Security
1. Enable network policies
2. Configure default deny rules
3. Set up Security Groups for Pods
4. Implement service mesh with mTLS (optional)
5. Enable VPC Flow Logs

### Phase 5: Runtime Security
1. Deploy image scanning
2. Configure admission controllers
3. Set up runtime monitoring (Falco)
4. Enable GuardDuty for EKS
5. Configure incident response

### Phase 6: Compliance & Audit
1. Run security benchmarks
2. Configure continuous compliance
3. Set up security dashboards
4. Document security controls
5. Conduct regular security reviews

## Critical Security Controls

### 1. IAM Roles for Service Accounts (IRSA)

**Why**: Provides pod-level AWS permissions without node-level credentials

**Quick Implementation**:
```yaml
# Service Account with IRSA
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/my-app-role
```

**Best Practices**:
- One service account per application
- Explicit trust policies with namespace and SA name
- Least privilege IAM policies
- Regular audit of role usage

**Details**: [references/cluster-security.md#irsa](references/cluster-security.md)

### 2. Pod Security Standards

**Why**: Prevents privilege escalation and enforces security best practices

**Quick Implementation**:
```yaml
# Restricted namespace
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Levels**:
- **privileged**: No restrictions (avoid in production)
- **baseline**: Minimal restrictions (development)
- **restricted**: Comprehensive restrictions (REQUIRED for production)

**Details**: [references/workload-security.md#pod-security-standards](references/workload-security.md)

### 3. Network Policies

**Why**: Implement microsegmentation and zero-trust networking

**Quick Implementation**:
```yaml
# Default deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

**Capabilities**:
- Pod-to-pod traffic control
- Namespace isolation
- External service access control
- Defense in depth with Security Groups for Pods

**Details**: [references/workload-security.md#network-policies](references/workload-security.md)

### 4. External Secrets Operator

**Why**: Centralized secret management with automatic rotation

**Quick Implementation**:
```yaml
# ExternalSecret resource
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: app-secrets-k8s
  data:
  - secretKey: db-password
    remoteRef:
      key: prod/db/password
```

**Benefits**:
- Automatic synchronization
- Works with Fargate (unlike CSI driver)
- Multiple backend support
- Audit trail via CloudTrail

**Details**: [references/secrets-management.md#external-secrets-operator](references/secrets-management.md)

### 5. Container Image Scanning

**Why**: Identify and remediate vulnerabilities before deployment

**Amazon Inspector 2025 Features**:
- Container image mapping (shows running containers)
- Extended coverage (distroless, scratch, Chainguard)
- Continuous monitoring with automatic rescans
- Prioritization based on actively running images

**Quick Setup**:
```bash
# Enable enhanced scanning
aws ecr put-registry-scanning-configuration \
  --scan-type ENHANCED \
  --rules '[{"repositoryFilters":[{"filter":"*","filterType":"WILDCARD"}],"scanFrequency":"CONTINUOUS_SCAN"}]'
```

**Details**: [references/workload-security.md#image-scanning](references/workload-security.md)

### 6. Runtime Security Monitoring

**Why**: Detect and respond to threats in real-time

**Tools**:
- **Amazon GuardDuty for EKS**: Managed threat detection
- **Falco**: Open-source runtime security
- **OPA/Gatekeeper**: Policy enforcement

**GuardDuty for EKS Capabilities**:
- Suspicious API calls
- Privilege escalation attempts
- Cryptocurrency mining detection
- Anomalous network activity
- Container escape attempts

**Details**: [references/workload-security.md#runtime-security](references/workload-security.md)

## Security Patterns

### Pattern 1: Zero-Trust Cluster (Maximum Security)

**Configuration**:
- Private API endpoint only
- All nodes in private subnets
- Network policies enabled (default deny)
- Pod Security Standards (restricted)
- mTLS service mesh (Istio)
- No public load balancers
- VPN/Direct Connect for access

**Use Case**: Healthcare, finance, regulated industries

### Pattern 2: Defense-in-Depth Production Cluster

**Configuration**:
- Public + private API endpoints
- IP allowlist on public endpoint
- Nodes in private subnets
- Network policies + Security Groups for Pods
- Pod Security Standards (restricted)
- External Secrets Operator
- GuardDuty + Inspector enabled

**Use Case**: Standard production workloads

### Pattern 3: Multi-Tenant Cluster

**Configuration**:
- Namespace isolation with RBAC
- ResourceQuotas per namespace
- Network policies per namespace
- Dedicated node groups with taints/tolerations
- Pod Security Standards per namespace
- Audit logging of all API calls

**Use Case**: Platform teams, SaaS applications

## Compliance Frameworks

### CIS Kubernetes Benchmark

**Tool**: kube-bench
```bash
# Run CIS benchmark
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job-eks.yaml

# View results
kubectl logs -n kube-bench job/kube-bench
```

**Key Controls**:
- Control plane security
- Worker node configuration
- Pod security policies
- Network policies
- Authentication/authorization

### NIST 800-190 (Container Security)

**Five Areas**:
1. Image security and integrity
2. Registry security
3. Orchestrator security
4. Container runtime security
5. Host OS security

**Implementation**: See detailed mapping in [references/cluster-security.md#compliance](references/cluster-security.md)

### SOC2 / HIPAA / PCI-DSS

**Common Requirements**:
- Encryption at rest and in transit
- Audit logging and monitoring
- Access controls (RBAC + IRSA)
- Vulnerability scanning
- Incident response procedures
- Regular security assessments

## Security Incident Response

### Detection Sources
1. GuardDuty alerts
2. CloudWatch alarms
3. Falco runtime alerts
4. Audit log anomalies
5. Network traffic analysis
6. Container image scan results

### Response Workflow
1. **Identify**: Determine scope and severity
2. **Contain**: Isolate affected workloads
3. **Eradicate**: Remove malicious components
4. **Recover**: Restore from known-good state
5. **Review**: Post-incident analysis

### Common Scenarios

**Compromised Pod**:
```bash
# Immediate isolation
kubectl label pod <pod-name> security=isolated
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: isolate-compromised-pod
spec:
  podSelector:
    matchLabels:
      security: isolated
  policyTypes:
  - Ingress
  - Egress
EOF

# Collect forensics
kubectl logs <pod-name> > pod-logs.txt
kubectl exec <pod-name> -- ps aux > processes.txt

# Delete pod
kubectl delete pod <pod-name>
```

**Details**: [references/workload-security.md#incident-response](references/workload-security.md)

## Detailed Documentation

For comprehensive security configurations and advanced topics:

- **Cluster-Level Security**: [references/cluster-security.md](references/cluster-security.md)
  - Control plane hardening
  - API endpoint configuration
  - Audit logging setup
  - IRSA detailed configuration
  - RBAC best practices
  - Compliance frameworks

- **Workload Security**: [references/workload-security.md](references/workload-security.md)
  - Pod Security Standards implementation
  - Security contexts configuration
  - Network policies patterns
  - Image scanning and verification
  - Runtime security (Falco, GuardDuty)
  - Admission controllers (OPA/Gatekeeper)
  - Incident response procedures

- **Secrets Management**: [references/secrets-management.md](references/secrets-management.md)
  - External Secrets Operator setup
  - AWS Secrets Manager integration
  - CSI Secrets Store Driver
  - Secret rotation strategies
  - Encryption configuration
  - Audit and monitoring

## Security Assessment Tools

### Scanning and Assessment
- **kube-bench**: CIS Kubernetes benchmark
- **kube-hunter**: Active vulnerability scanning
- **Polaris**: Configuration validation
- **Trivy**: Vulnerability and misconfiguration scanning
- **Checkov**: IaC security scanning

### Runtime Security
- **Falco**: Runtime threat detection
- **GuardDuty for EKS**: AWS-managed threat detection
- **Sysdig**: Container security platform

### Policy Enforcement
- **OPA/Gatekeeper**: Policy as code
- **Kyverno**: Kubernetes-native policy engine
- **Pod Security Admission**: Built-in PSS enforcement

## Common Security Anti-Patterns to Avoid

| Anti-Pattern | Risk | Solution |
|--------------|------|----------|
| Using default service accounts | Overly permissive | Create dedicated service accounts per app |
| Privileged containers | Host access, container escape | Use specific capabilities, PSS restricted |
| Hardcoded secrets in manifests | Credential exposure | Use External Secrets Operator |
| No network policies | Lateral movement | Implement default-deny policies |
| Running as root | Privilege escalation | Set runAsNonRoot: true |
| Public API endpoint without restrictions | Unauthorized access | Use private endpoint or IP allowlist |
| No image scanning | Vulnerability deployment | Enable Amazon Inspector |
| Shared node IAM roles | Excessive permissions | Use IRSA for pod-level permissions |
| No resource limits | Resource exhaustion | Set requests and limits |
| Missing audit logs | No forensic capability | Enable all control plane logs |

## Automated Security Hardening

### Terraform Module (Recommended)
```hcl
module "eks_security" {
  source = "./modules/eks-security"

  cluster_name = "production-cluster"

  # Control plane
  enable_private_endpoint = true
  enable_public_endpoint  = false
  enable_audit_logging    = true
  kms_key_arn            = aws_kms_key.eks.arn

  # Workload security
  pod_security_standard = "restricted"
  enable_network_policies = true

  # Secrets
  deploy_external_secrets = true
  secrets_manager_role_arn = aws_iam_role.secrets.arn

  # Monitoring
  enable_guardduty = true
  enable_inspector = true

  # Compliance
  cis_compliance_mode = true
}
```

**See full examples**: [references/cluster-security.md#terraform](references/cluster-security.md)

## Security Roadmap

### Week 1: Foundation
- [ ] Review and harden control plane
- [ ] Configure audit logging
- [ ] Set up IRSA for critical workloads
- [ ] Enable Pod Security Standards

### Week 2: Network & Secrets
- [ ] Deploy network policies
- [ ] Implement External Secrets Operator
- [ ] Configure Security Groups for Pods
- [ ] Enable VPC Flow Logs

### Week 3: Scanning & Runtime
- [ ] Enable Amazon Inspector
- [ ] Deploy GuardDuty for EKS
- [ ] Configure Falco (optional)
- [ ] Set up admission controllers

### Week 4: Compliance & Operations
- [ ] Run CIS benchmark
- [ ] Configure Security Hub
- [ ] Document security controls
- [ ] Train team on incident response
- [ ] Schedule regular security reviews

## Quick Reference Commands

### Security Audit
```bash
# Check Pod Security Standards
kubectl get namespaces -o custom-columns=NAME:.metadata.name,PSS:.metadata.labels.pod-security\.kubernetes\.io/enforce

# List service accounts with IRSA
kubectl get sa -A -o jsonpath='{range .items[?(@.metadata.annotations.eks\.amazonaws\.com/role-arn)]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.metadata.annotations.eks\.amazonaws\.com/role-arn}{"\n"}{end}'

# Check for privileged pods
kubectl get pods -A -o jsonpath='{range .items[?(@.spec.containers[*].securityContext.privileged==true)]}{.metadata.namespace}{"\t"}{.metadata.name}{"\n"}{end}'

# List pods running as root
kubectl get pods -A -o jsonpath='{range .items[?(@.spec.securityContext.runAsNonRoot!=true)]}{.metadata.namespace}{"\t"}{.metadata.name}{"\n"}{end}'

# Check network policies
kubectl get networkpolicies -A

# View audit logs
aws logs tail /aws/eks/production-cluster/cluster --follow --filter-pattern '{ $.verb != "get" && $.verb != "list" && $.verb != "watch" }'
```

### Security Monitoring
```bash
# GuardDuty findings
aws guardduty list-findings --detector-id <detector-id> --finding-criteria '{"Criterion":{"resource.resourceType":{"Eq":["EKS"]}}}'

# Inspector scan results
aws inspector2 list-findings --filter-criteria '{"ecrImageRepositoryName":[{"comparison":"EQUALS","value":"my-repo"}]}'

# CloudWatch Container Insights
aws cloudwatch get-metric-statistics \
  --namespace ContainerInsights \
  --metric-name pod_cpu_utilization \
  --dimensions Name=ClusterName,Value=production-cluster
```

---

**Last Updated**: November 2025
**Kubernetes Version**: 1.33
**Security Standards**: CIS Kubernetes Benchmark 1.8, NIST 800-190, AWS Well-Architected
**Status**: Production-ready
