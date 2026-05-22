---
name: ack-resources
description: AWS Controllers for Kubernetes (ACK) for Kubernetes-native AWS resource management. Use when managing AWS resources via kubectl, implementing GitOps for infrastructure, creating self-service developer platforms, integrating AWS services with EKS workloads, or adopting existing AWS resources into Kubernetes.
---

# AWS Controllers for Kubernetes (ACK)

Manage AWS services directly from Kubernetes using custom resource definitions (CRDs) and controllers. ACK extends the Kubernetes API to create, update, and delete AWS resources using familiar kubectl commands and GitOps workflows.

## Overview

**AWS Controllers for Kubernetes (ACK)** enables you to:
- Define AWS resources as Kubernetes manifests (S3 buckets, RDS databases, SQS queues, etc.)
- Use kubectl to manage AWS infrastructure
- Implement end-to-end GitOps for applications and infrastructure
- Leverage Kubernetes RBAC for AWS resource access control
- Automatically reconcile drift between desired and actual AWS state
- Adopt existing AWS resources without recreation

**Architecture Pattern:**
```
Git (manifests) → ArgoCD/Flux → Kubernetes (ACK CRDs) → AWS APIs → AWS Resources
                                      ↓
                              Continuous Reconciliation
```

**Key Characteristics:**
- **Kubernetes Native**: Uses standard CRDs and the operator pattern
- **Direct API Integration**: Calls AWS APIs directly (not CloudFormation)
- **Modular**: Install only the service controllers you need
- **GitOps-First**: Designed for declarative infrastructure management
- **Multi-Account**: Supports cross-account resource management (CARM)

## When to Use ACK

### Perfect For

✅ **EKS Workloads Needing AWS Services**
- Applications requiring RDS databases, S3 buckets, SQS queues
- Unified control plane for apps and their infrastructure dependencies
- Tight coupling between Kubernetes workloads and AWS resources

✅ **GitOps Infrastructure Workflows**
- Version-controlled AWS infrastructure in Git
- PR-based review process for infrastructure changes
- ArgoCD/Flux automated synchronization

✅ **Self-Service Developer Platforms**
- Developers provision AWS resources via kubectl
- Namespace-based RBAC controls access
- Platform teams define policies and quotas

✅ **Multi-Account/Multi-Tenant Environments**
- Different teams/namespaces map to different AWS accounts
- Centralized control plane with isolated AWS resources
- Cost allocation per namespace/account

### Not Ideal For

❌ **Multi-Cloud Infrastructure**
- ACK is AWS-only (use Crossplane for multi-cloud)

❌ **Comprehensive AWS Coverage Required**
- Limited to 14+ GA controllers (use Terraform for broader coverage)

❌ **Non-Kubernetes Environments**
- Requires Kubernetes cluster (use Terraform/CDK for AWS-only infrastructure)

❌ **Stable Production APIs Only**
- Many controllers still in alpha (v1alpha1)

## Supported AWS Services (2025)

### Generally Available Controllers

| Service | Controller | Common Use Cases |
|---------|-----------|------------------|
| **Amazon S3** | s3-controller | Application data storage, static assets |
| **Amazon RDS** | rds-controller | PostgreSQL, MySQL, Oracle databases |
| **Amazon DynamoDB** | dynamodb-controller | NoSQL tables for applications |
| **Amazon SQS** | sqs-controller | Message queues for async processing |
| **Amazon SNS** | sns-controller | Notifications and pub/sub messaging |
| **AWS Lambda** | lambda-controller | Serverless functions |
| **Amazon ECR** | ecr-controller | Container image repositories |
| **Amazon EKS** | eks-controller | Additional EKS clusters |
| **Amazon EC2** | ec2-controller | VPCs, subnets, security groups |
| **AWS IAM** | iam-controller | Roles, policies for applications |
| **Amazon EFS** | efs-controller | Shared file systems |
| **Amazon ElastiCache** | elasticache-controller | Redis/Memcached clusters |
| **Amazon MSK** | msk-controller | Managed Kafka clusters |
| **API Gateway V2** | apigatewayv2-controller | HTTP/WebSocket APIs |
| **Amazon SageMaker** | sagemaker-controller | ML model endpoints |
| **Amazon Athena** | athena-controller | SQL queries on S3 data |

**Additional controllers available in preview/beta.** See references for complete list.

## Quick Start Workflow

### 1. Understand Your Objective

**What are you trying to accomplish?**

- **Setup**: Install ACK controllers in your EKS cluster → See [Controller Setup](#2-setup-install-ack-controller)
- **Create Resources**: Define AWS resources as Kubernetes manifests → See [Create AWS Resources](#3-create-aws-resources)
- **Adopt Existing**: Import existing AWS resources into ACK → See [Adopt Existing Resources](#5-adopt-existing-aws-resources)
- **GitOps**: Integrate with ArgoCD/Flux → See [GitOps Integration](#6-gitops-integration)
- **Multi-Account**: Manage resources across AWS accounts → See [Cross-Account Management](#7-cross-account-management-carm)
- **Troubleshoot**: Debug ACK resource issues → See [Troubleshooting](#8-troubleshooting)

### 2. Setup: Install ACK Controller

**Prerequisites:**
- EKS cluster (Kubernetes 1.16+)
- kubectl configured
- Helm 3.8+
- AWS CLI

**Installation Steps:**

#### Step 1: Create OIDC Provider (IRSA)

```bash
# Enable IRSA for your EKS cluster
eksctl utils associate-iam-oidc-provider \
  --cluster=my-cluster \
  --region=us-east-1 \
  --approve
```

#### Step 2: Create IAM Policy for Controller

Example for S3 controller:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:ListBucket",
        "s3:GetBucket*",
        "s3:PutBucket*",
        "s3:DeleteBucket*"
      ],
      "Resource": "*"
    }
  ]
}
```

```bash
# Create the IAM policy
aws iam create-policy \
  --policy-name ACK-S3-Controller-Policy \
  --policy-document file://s3-policy.json
```

#### Step 3: Create IAM Role with IRSA

```bash
# Create service account with IAM role
eksctl create iamserviceaccount \
  --name ack-s3-controller \
  --namespace ack-system \
  --cluster my-cluster \
  --attach-policy-arn arn:aws:iam::123456789012:policy/ACK-S3-Controller-Policy \
  --approve \
  --override-existing-serviceaccounts
```

#### Step 4: Install Controller via Helm

```bash
export HELM_EXPERIMENTAL_OCI=1

# Install S3 controller
helm install ack-s3-controller \
  oci://public.ecr.aws/aws-controllers-k8s/s3-chart \
  --version=v0.1.7 \
  --namespace ack-system \
  --create-namespace \
  --set=aws.region=us-east-1 \
  --set=serviceAccount.create=false \
  --set=serviceAccount.name=ack-s3-controller
```

#### Step 5: Verify Installation

```bash
# Check controller is running
kubectl get pods -n ack-system

# List installed CRDs
kubectl get crds | grep s3.services.k8s.aws
```

**See reference:** `references/controller-setup.md` for detailed installation guides for all controllers.

### 3. Create AWS Resources

Define AWS resources using Kubernetes manifests:

#### Example: S3 Bucket

```yaml
apiVersion: s3.services.k8s.aws/v1alpha1
kind: Bucket
metadata:
  name: my-app-bucket
  namespace: production
spec:
  name: my-app-bucket-unique-12345
  versioning:
    status: Enabled
```

```bash
kubectl apply -f s3-bucket.yaml

# Check status
kubectl get buckets.s3.services.k8s.aws -n production
kubectl describe bucket my-app-bucket -n production
```

#### Example: RDS PostgreSQL Instance

```yaml
apiVersion: rds.services.k8s.aws/v1alpha1
kind: DBInstance
metadata:
  name: myapp-db
  namespace: production
spec:
  dbInstanceIdentifier: myapp-db
  dbInstanceClass: db.t3.medium
  engine: postgres
  engineVersion: "15.4"
  allocatedStorage: 20
  storageType: gp3
  storageEncrypted: true
  masterUsername: postgres
  masterUserPassword:
    name: db-credentials  # Kubernetes secret
    key: password
  backupRetentionPeriod: 7
  multiAZ: true
  publiclyAccessible: false
  dbSubnetGroupName: my-subnet-group
  vpcSecurityGroupIDs:
    - sg-0123456789abcdef0
```

#### Example: SQS Queue

```yaml
apiVersion: sqs.services.k8s.aws/v1alpha1
kind: Queue
metadata:
  name: orders-queue
  namespace: production
spec:
  queueName: orders-queue
  visibilityTimeout: 30
  messageRetentionPeriod: 345600  # 4 days
  receiveMessageWaitTimeSeconds: 20  # Long polling
```

**See reference:** `references/resource-definitions.md` for comprehensive examples of all supported AWS services.

### 4. Reference and Export Resource Values

ACK resources automatically populate status fields with AWS resource details. Use these in two ways:

#### Pattern 1: Resource References (Cross-Resource)

Reference one ACK resource from another using `*Ref` fields:

```yaml
# Create API Gateway API
apiVersion: apigatewayv2.services.k8s.aws/v1alpha1
kind: API
metadata:
  name: my-api
  namespace: default
spec:
  name: my-api
  protocolType: HTTP
---
# Create Integration referencing the API
apiVersion: apigatewayv2.services.k8s.aws/v1alpha1
kind: Integration
metadata:
  name: my-integration
  namespace: default
spec:
  apiRef:
    from:
      name: my-api  # References API by name
  integrationType: AWS_PROXY
  integrationURI: arn:aws:lambda:us-east-1:123456789012:function:my-function
```

#### Pattern 2: Field Exports (to ConfigMap/Secret)

Export ACK resource values for use by Kubernetes workloads:

```yaml
# Export S3 bucket ARN to ConfigMap
apiVersion: services.k8s.aws/v1alpha1
kind: FieldExport
metadata:
  name: export-bucket-arn
  namespace: production
spec:
  from:
    resource:
      group: s3.services.k8s.aws
      kind: Bucket
      name: my-app-bucket
    path: ".status.arn"
  to:
    kind: configmap
    name: app-config
    key: S3_BUCKET_ARN
```

Use exported value in pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  namespace: production
spec:
  containers:
  - name: app
    image: my-app:latest
    envFrom:
    - configMapRef:
        name: app-config  # Contains S3_BUCKET_ARN
```

### 5. Adopt Existing AWS Resources

Import existing AWS resources (created outside ACK) without recreation:

```yaml
apiVersion: services.k8s.aws/v1alpha1
kind: AdoptedResource
metadata:
  name: adopt-prod-bucket
  namespace: production
spec:
  aws:
    nameOrID: existing-prod-bucket-name  # Existing AWS resource
  kubernetes:
    group: s3.services.k8s.aws
    kind: Bucket
    metadata:
      name: prod-bucket  # Name in Kubernetes
      namespace: production
```

**Process:**
1. Apply AdoptedResource manifest
2. ACK describes the existing AWS resource
3. Creates corresponding Kubernetes resource with full spec/status
4. Future changes managed via the ACK resource

**Benefits:**
- No resource recreation (zero downtime)
- Gradual migration to ACK
- Preserve existing configurations

### 6. GitOps Integration

Manage ACK resources through Git with ArgoCD or Flux:

#### ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: aws-infrastructure
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/infrastructure
    path: ack-resources/production
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: false  # Safety: don't auto-delete AWS resources
      selfHeal: true  # Auto-correct drift
    syncOptions:
    - CreateNamespace=true
```

#### Flux Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: aws-infrastructure
  namespace: flux-system
spec:
  interval: 10m
  path: ./ack-resources/production
  prune: false  # Safety: don't auto-delete
  sourceRef:
    kind: GitRepository
    name: infrastructure
  targetNamespace: production
```

**Workflow:**
1. Developers create/modify ACK resources in Git
2. Submit PR for review
3. Merge to main triggers ArgoCD/Flux sync
4. ACK controllers create/update AWS resources
5. Continuous reconciliation ensures consistency

**See reference:** `references/gitops-patterns.md` for comprehensive GitOps workflows and best practices.

### 7. Cross-Account Management (CARM)

Manage AWS resources in multiple accounts from a single Kubernetes cluster:

#### Step 1: Create ConfigMap with Account Role Mappings

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ack-role-account-map
  namespace: ack-system
data:
  "111122223333": "arn:aws:iam::111122223333:role/ack-controller-role"
  "444455556666": "arn:aws:iam::444455556666:role/ack-controller-role"
```

#### Step 2: Annotate Namespace with Account ID

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
  annotations:
    services.k8s.aws/owner-account-id: "111122223333"
```

#### Step 3: Deploy Resources (Uses Namespace Account)

```yaml
apiVersion: s3.services.k8s.aws/v1alpha1
kind: Bucket
metadata:
  name: team-a-bucket
  namespace: team-a  # Uses account 111122223333
spec:
  name: team-a-bucket-unique
```

**Benefits:**
- Multi-tenancy with separate billing
- RBAC-based access control
- Security boundaries per team/account

### 8. Troubleshooting

#### Check Resource Status

```bash
# View resource status
kubectl get buckets.s3.services.k8s.aws -n production
kubectl describe bucket my-bucket -n production

# Check status conditions
kubectl get bucket my-bucket -n production -o jsonpath='{.status.conditions}'
```

**Status Conditions:**
- `ACK.ResourceSynced: True` - Resource matches AWS state
- `ACK.Terminal: True` - Resource in error state
- `ACK.Recovering: True` - Resource recovering from error

#### Check Controller Logs

```bash
# View controller logs
kubectl logs -n ack-system deployment/ack-s3-controller -f

# Filter for specific resource
kubectl logs -n ack-system deployment/ack-s3-controller | grep my-bucket
```

#### Common Issues

**Issue: Resource stuck in pending state**

```bash
# Check events
kubectl describe bucket my-bucket -n production

# Common causes:
# - IAM permissions missing
# - AWS API throttling
# - Invalid resource configuration
```

**Issue: Drift reconciliation not working**

```bash
# Verify controller is running
kubectl get pods -n ack-system

# Check reconciliation interval (default ~10 minutes)
# Force reconciliation by annotating resource
kubectl annotate bucket my-bucket -n production force-sync="$(date +%s)"
```

**Issue: Cross-account resources failing**

```bash
# Verify namespace annotation
kubectl get namespace team-a -o yaml | grep owner-account-id

# Verify ConfigMap has role mapping
kubectl get configmap ack-role-account-map -n ack-system -o yaml

# Check controller has assume role permissions
```

## Production Best Practices

### 1. Deletion Policies

Protect critical resources from accidental deletion:

```yaml
apiVersion: rds.services.k8s.aws/v1alpha1
kind: DBInstance
metadata:
  name: production-db
  namespace: production
  annotations:
    services.k8s.aws/deletion-policy: retain  # Keep AWS resource on delete
spec:
  dbInstanceIdentifier: production-db
  # ... spec
```

**Policy hierarchy:**
1. Resource annotation (highest priority)
2. Namespace annotation
3. Controller flag (lowest priority)

**Policy values:**
- `delete` (default): Delete AWS resource when K8s resource deleted
- `retain`: Keep AWS resource when K8s resource deleted

### 2. Secrets Management

Never store passwords in plain text:

```yaml
# Create secret
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: production
type: Opaque
stringData:
  password: "SecurePassword123!"
---
# Reference in RDS instance
apiVersion: rds.services.k8s.aws/v1alpha1
kind: DBInstance
metadata:
  name: mydb
spec:
  masterUserPassword:
    name: db-credentials
    key: password
```

**Better: Use External Secrets Operator** with AWS Secrets Manager for secret rotation.

### 3. IAM Least Privilege

Grant minimum required permissions per controller:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:GetBucket*",
        "s3:PutBucket*"
      ],
      "Resource": "arn:aws:s3:::prefix-*"  // Limit to specific prefix
    }
  ]
}
```

### 4. Resource Quotas

Limit resource creation per namespace:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: aws-resource-quota
  namespace: production
spec:
  hard:
    count/buckets.s3.services.k8s.aws: "10"
    count/dbinstances.rds.services.k8s.aws: "5"
    count/queues.sqs.services.k8s.aws: "20"
```

### 5. Monitoring

Enable Prometheus metrics for ACK controllers:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ack-s3-controller
  namespace: ack-system
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: ack-s3-controller
  endpoints:
  - port: metrics
    interval: 30s
```

**Key metrics:**
- `ack_resource_reconcile_duration_seconds`: Reconciliation latency
- `ack_resource_reconcile_errors_total`: Error count
- `ack_resource_synced`: Resource sync status

### 6. High Availability

Run multiple controller replicas with leader election:

```yaml
# Helm values
replicaCount: 3
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app.kubernetes.io/name: ack-s3-controller
      topologyKey: kubernetes.io/hostname
```

## ACK vs Alternatives

### ACK vs Terraform

| Aspect | ACK | Terraform |
|--------|-----|-----------|
| **Cloud Support** | AWS only | Multi-cloud (AWS, Azure, GCP, 300+ providers) |
| **Paradigm** | Kubernetes-native, continuous reconciliation | State-based, apply-driven |
| **Maturity** | Newer, many alpha APIs | Mature, stable, widely adopted |
| **Service Coverage** | 14+ GA, 12+ preview | 1000+ AWS resources |
| **Drift Handling** | Automatic continuous reconciliation | Detect on plan/apply, manual fix |
| **Best For** | EKS workloads, GitOps, K8s-centric teams | Multi-cloud, comprehensive coverage |

**Selective Approach:** Use ACK for application-tied resources (RDS, SQS, S3 for apps) and Terraform for foundational infrastructure (VPCs, IAM, networking).

### ACK vs Crossplane

| Aspect | ACK | Crossplane |
|--------|-----|-----------|
| **Scope** | AWS only | Multi-cloud |
| **Abstraction** | None (1:1 AWS API) | Compositions (custom abstractions) |
| **Maturity** | AWS-sponsored | CNCF project |
| **Best For** | AWS-only, simple use cases | Multi-cloud, platform engineering |

**Note:** Crossplane provider-aws uses ACK code generation under the hood.

### ACK vs AWS CDK

| Aspect | ACK | AWS CDK |
|--------|-----|---------|
| **Language** | YAML (K8s manifests) | TypeScript, Python, Java, C#, Go |
| **Output** | Direct AWS API calls | CloudFormation templates |
| **Execution** | Continuous (K8s reconciliation) | On-demand (CDK deploy) |
| **Best For** | K8s-native workflows, GitOps | Application developers, reusable patterns |

## Common Patterns

### Pattern 1: Application Stack

Define entire application stack in one manifest:

```yaml
# database.yaml
apiVersion: rds.services.k8s.aws/v1alpha1
kind: DBInstance
metadata:
  name: app-db
  namespace: production
spec:
  dbInstanceIdentifier: app-db
  # ... database config
---
# queue.yaml
apiVersion: sqs.services.k8s.aws/v1alpha1
kind: Queue
metadata:
  name: app-queue
  namespace: production
spec:
  queueName: app-queue
---
# Export values for app
apiVersion: services.k8s.aws/v1alpha1
kind: FieldExport
metadata:
  name: export-db-endpoint
spec:
  from:
    resource:
      group: rds.services.k8s.aws
      kind: DBInstance
      name: app-db
    path: ".status.endpoint.address"
  to:
    kind: secret
    name: app-config
    key: DB_HOST
```

### Pattern 2: Multi-Region Setup

Deploy same resources across regions:

```yaml
# us-east-1-bucket.yaml
apiVersion: s3.services.k8s.aws/v1alpha1
kind: Bucket
metadata:
  name: multi-region-bucket-east
  namespace: production
  annotations:
    services.k8s.aws/region: us-east-1
spec:
  name: my-bucket-us-east-1-unique
---
# us-west-2-bucket.yaml
apiVersion: s3.services.k8s.aws/v1alpha1
kind: Bucket
metadata:
  name: multi-region-bucket-west
  namespace: production
  annotations:
    services.k8s.aws/region: us-west-2
spec:
  name: my-bucket-us-west-2-unique
```

### Pattern 3: Environment Promotion

Use Kustomize overlays for environment-specific configurations:

```
ack-resources/
├── base/
│   ├── kustomization.yaml
│   ├── rds-instance.yaml
│   └── s3-bucket.yaml
├── overlays/
│   ├── dev/
│   │   └── kustomization.yaml  # db.t3.small, single-AZ
│   ├── staging/
│   │   └── kustomization.yaml  # db.t3.medium, multi-AZ
│   └── production/
│       └── kustomization.yaml  # db.r5.large, multi-AZ, encrypted
```

## Next Steps

### For Installation & Configuration
→ See `references/controller-setup.md`:
- Detailed installation for all 14+ controllers
- IAM policy templates per service
- IRSA configuration examples
- Controller configuration options
- Multi-controller setup
- Upgrade procedures

### For Resource Definitions & Examples
→ See `references/resource-definitions.md`:
- Comprehensive examples for all AWS services
- S3, RDS, DynamoDB, SQS, SNS, Lambda, ECR, IAM, EC2, EKS
- Production configurations with encryption, backups, HA
- Cross-resource references
- Field exports to ConfigMaps/Secrets
- Adopting existing AWS resources

### For GitOps Integration
→ See `references/gitops-patterns.md`:
- ArgoCD integration patterns
- Flux CD integration patterns
- Multi-cluster GitOps
- Environment promotion strategies
- Drift detection and reconciliation
- Disaster recovery procedures
- Secrets management with External Secrets Operator

## Resources

**Official Documentation:**
- ACK Community: https://aws-controllers-k8s.github.io/community/
- GitHub: https://github.com/aws-controllers-k8s
- Service List: https://aws-controllers-k8s.github.io/community/docs/community/services/

**Container Images:**
- ECR Public Gallery: https://gallery.ecr.aws/aws-controllers-k8s

**Learning:**
- EKS Workshop: https://www.eksworkshop.com/docs/automation/controlplanes/ack/
- AWS Blog (ACK): https://aws.amazon.com/blogs/containers/ (filter: ACK)

**Common Commands:**
```bash
# List all ACK resources in namespace
kubectl get services.k8s.aws -n <namespace>

# Describe ACK resource with events
kubectl describe bucket.s3.services.k8s.aws <name> -n <namespace>

# View controller logs
kubectl logs -n ack-system deployment/ack-s3-controller -f

# Export resource to YAML
kubectl get bucket.s3.services.k8s.aws <name> -n <namespace> -o yaml

# Validate resource (dry-run)
kubectl apply --dry-run=server -f bucket.yaml
```

## Summary

ACK brings AWS resource management into the Kubernetes ecosystem, enabling true infrastructure-as-code with GitOps workflows. It's ideal for teams running EKS workloads that need tight integration between applications and AWS services, with the flexibility to use familiar Kubernetes tools and processes.

**Best practice:** Use ACK selectively for application-tied resources (databases, queues, storage for apps) while using Terraform for foundational infrastructure (VPCs, IAM roles, networking). This hybrid approach combines the strengths of both tools.
