---
name: harness-platform
description: Harness Platform administration including delegates, RBAC, connectors, secrets, templates, policy as code (OPA), user management, audit logs, and governance. Activate for Harness setup, administration, access control, and platform configuration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - harness-mcp
  - harness-cd
  - harness-ci
triggers:
  - harness delegate
  - harness rbac
  - harness connector
  - harness secret
  - harness template
  - harness policy
  - harness opa
  - harness user
  - harness admin
  - harness governance
  - harness audit
  - harness account
  - harness organization
  - harness project
---

# Harness Platform Administration Skill

Comprehensive Harness Platform administration for delegates, RBAC, connectors, secrets, templates, policy as code, and governance.

## When to Use This Skill

Activate this skill when:
- Deploying or troubleshooting Harness Delegates
- Configuring RBAC (roles, resource groups, user groups)
- Managing connectors (cloud, SCM, artifact registries)
- Setting up secrets management
- Creating and managing templates
- Implementing policy as code with OPA
- Auditing platform activity
- Managing accounts, organizations, and projects

## Platform Hierarchy

```
Account (Root)
├── Organization 1
│   ├── Project A
│   │   ├── Pipelines
│   │   ├── Services
│   │   ├── Environments
│   │   ├── Connectors (project-level)
│   │   └── Secrets (project-level)
│   ├── Project B
│   ├── Connectors (org-level)
│   └── Secrets (org-level)
├── Organization 2
├── Connectors (account-level)
├── Secrets (account-level)
├── Delegates
└── User Management
```

---

## Harness Delegates

### Overview

Delegates are lightweight agents that connect Harness to your infrastructure, executing tasks in your environments.

### Delegate Types

| Type | Use Case | Deployment Method |
|------|----------|-------------------|
| **Kubernetes** | K8s clusters, cloud-native | Helm, YAML |
| **Docker** | Single hosts, development | docker run |
| **Shell** | VMs, legacy systems | Shell script |
| **ECS** | AWS ECS environments | Task definition |

### Kubernetes Delegate (Helm)

```bash
# Add Harness Helm repo
helm repo add harness-delegate https://app.harness.io/storage/harness-download/delegate-helm-chart/
helm repo update

# Install delegate
helm install harness-delegate harness-delegate/harness-delegate-ng \
  --namespace harness-delegate \
  --create-namespace \
  --set accountId="${HARNESS_ACCOUNT_ID}" \
  --set delegateToken="${DELEGATE_TOKEN}" \
  --set delegateName="production-delegate" \
  --set managerEndpoint="https://app.harness.io" \
  --set delegateDockerImage="harness/delegate:latest" \
  --set replicas=2 \
  --set upgrader.enabled=true \
  --set k8sPermissionsType=CLUSTER_ADMIN
```

### Kubernetes Delegate (YAML)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: harness-delegate
---
apiVersion: v1
kind: Secret
metadata:
  name: harness-delegate-token
  namespace: harness-delegate
type: Opaque
data:
  token: <base64-encoded-token>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: harness-delegate
  namespace: harness-delegate
spec:
  replicas: 2
  selector:
    matchLabels:
      app: harness-delegate
  template:
    metadata:
      labels:
        app: harness-delegate
    spec:
      serviceAccountName: harness-delegate
      terminationGracePeriodSeconds: 600
      containers:
        - name: delegate
          image: harness/delegate:latest
          imagePullPolicy: Always
          resources:
            requests:
              memory: "2Gi"
              cpu: "0.5"
            limits:
              memory: "4Gi"
              cpu: "2"
          ports:
            - containerPort: 8080
          env:
            - name: JAVA_OPTS
              value: "-Xms1g -Xmx2g"
            - name: ACCOUNT_ID
              value: "${HARNESS_ACCOUNT_ID}"
            - name: DELEGATE_TOKEN
              valueFrom:
                secretKeyRef:
                  name: harness-delegate-token
                  key: token
            - name: DELEGATE_NAME
              value: "production-delegate"
            - name: MANAGER_HOST_AND_PORT
              value: "https://app.harness.io"
            - name: DELEGATE_TYPE
              value: "KUBERNETES"
            - name: DELEGATE_TAGS
              value: "production,k8s,aws"
            - name: DELEGATE_DESCRIPTION
              value: "Production Kubernetes delegate"
            - name: NEXT_GEN
              value: "true"
            - name: WATCHER_STORAGE_URL
              value: "https://app.harness.io/public/prod/premium/watchers"
            - name: DELEGATE_STORAGE_URL
              value: "https://app.harness.io"
            - name: REMOTE_WATCHER_URL_CDN
              value: "https://app.harness.io/public/shared/watchers/builds"
            - name: INIT_SCRIPT
              value: |
                #!/bin/bash
                # Install additional tools
                apt-get update && apt-get install -y \
                  awscli \
                  kubectl \
                  helm \
                  terraform
          livenessProbe:
            httpGet:
              path: /api/health
              port: 8080
            initialDelaySeconds: 120
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /api/health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: harness-delegate
  namespace: harness-delegate
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: harness-delegate-cluster-admin
subjects:
  - kind: ServiceAccount
    name: harness-delegate
    namespace: harness-delegate
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

### Docker Delegate

```bash
docker run -d --name harness-delegate \
  --restart unless-stopped \
  -e ACCOUNT_ID="${HARNESS_ACCOUNT_ID}" \
  -e DELEGATE_TOKEN="${DELEGATE_TOKEN}" \
  -e DELEGATE_NAME="docker-delegate" \
  -e MANAGER_HOST_AND_PORT="https://app.harness.io" \
  -e DELEGATE_TYPE="DOCKER" \
  -e DELEGATE_TAGS="docker,dev" \
  -e NEXT_GEN="true" \
  -e INIT_SCRIPT="apt-get update && apt-get install -y awscli" \
  -m 2g \
  --cpus="1" \
  harness/delegate:latest
```

### Delegate Selectors

Use selectors to route tasks to specific delegates:

```yaml
# In pipeline steps
- step:
    name: Deploy to Production
    identifier: deploy_prod
    type: K8sRollingDeploy
    spec:
      delegateSelectors:
        - production
        - aws
        - k8s
```

### Delegate Profiles

```yaml
delegateProfile:
  name: Production Profile
  identifier: prod_profile
  description: "Profile for production delegates"
  startupScript: |
    #!/bin/bash
    # Install AWS CLI
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip && ./aws/install

    # Install kubectl
    curl -LO "https://dl.k8s.io/release/v1.28.0/bin/linux/amd64/kubectl"
    chmod +x kubectl && mv kubectl /usr/local/bin/

    # Install Helm
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

    # Install Terraform
    curl -LO "https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip"
    unzip terraform_1.5.7_linux_amd64.zip && mv terraform /usr/local/bin/
  selectors:
    - production
    - infra
```

### Delegate Troubleshooting

```bash
# Check delegate status (Kubernetes)
kubectl get pods -n harness-delegate
kubectl logs -n harness-delegate -l app=harness-delegate --tail=100

# Check delegate health
kubectl exec -n harness-delegate deployment/harness-delegate -- curl -s localhost:8080/api/health

# Restart delegate
kubectl rollout restart deployment/harness-delegate -n harness-delegate

# Check delegate connectivity
kubectl exec -n harness-delegate deployment/harness-delegate -- curl -s https://app.harness.io/api/version

# View delegate metrics
kubectl port-forward -n harness-delegate svc/harness-delegate 3460:3460
curl localhost:3460/api/metrics
```

---

## RBAC (Role-Based Access Control)

### Built-in Roles

| Role | Scope | Description |
|------|-------|-------------|
| **Account Admin** | Account | Full access to everything |
| **Account Viewer** | Account | Read-only access |
| **Organization Admin** | Org | Full access within org |
| **Project Admin** | Project | Full access within project |
| **Pipeline Executor** | Project | Execute pipelines |
| **Pipeline Viewer** | Project | View pipelines only |

### Custom Role Definition

```yaml
role:
  name: Deployment Manager
  identifier: deployment_manager
  description: "Can manage and execute deployments"
  tags:
    department: platform
  allowedScopeLevels:
    - project
  permissions:
    # Pipeline permissions
    - resourceType: PIPELINE
      actions:
        - core_pipeline_view
        - core_pipeline_execute
    # Service permissions
    - resourceType: SERVICE
      actions:
        - core_service_view
        - core_service_access
    # Environment permissions
    - resourceType: ENVIRONMENT
      actions:
        - core_environment_view
        - core_environment_access
    # Connector permissions
    - resourceType: CONNECTOR
      actions:
        - core_connector_view
    # Secret permissions
    - resourceType: SECRET
      actions:
        - core_secret_view
```

### Resource Groups

```yaml
resourceGroup:
  name: Production Resources
  identifier: prod_resources
  description: "All production environment resources"
  allowedScopeLevels:
    - project
  includedScopes:
    - filter: ByResourceType
      resourceType: ENVIRONMENT
      attributeFilter:
        attributeName: type
        attributeValues:
          - Production
    - filter: ByResourceType
      resourceType: SERVICE
    - filter: ByResourceType
      resourceType: PIPELINE
      attributeFilter:
        attributeName: identifier
        attributeValues:
          - "deploy_*"
```

### User Groups

```yaml
userGroup:
  name: Platform Engineers
  identifier: platform_engineers
  description: "Platform engineering team"
  users:
    - user1@company.com
    - user2@company.com
    - user3@company.com
  externallyManaged: false
  harnessManaged: false
  ssoLinked: false
  notificationConfigs:
    - type: SLACK
      slackWebhookUrl: <+secrets.getValue("slack_webhook")>
    - type: EMAIL
      groupEmail: platform-team@company.com
```

### Role Binding

```yaml
roleBinding:
  name: Platform Team Prod Access
  identifier: platform_prod_access
  roleIdentifier: deployment_manager
  resourceGroupIdentifier: prod_resources
  principals:
    - type: USER_GROUP
      identifier: platform_engineers
  managed: false
```

### Service Accounts

```yaml
serviceAccount:
  name: CI Pipeline Account
  identifier: ci_pipeline_sa
  description: "Service account for CI automation"
  tags:
    purpose: automation
  accountIdentifier: "${HARNESS_ACCOUNT_ID}"
---
# Create API key for service account
apiKey:
  name: CI API Key
  identifier: ci_api_key
  serviceAccountIdentifier: ci_pipeline_sa
  apiKeyType: SERVICE_ACCOUNT
  defaultTimeToExpireToken: 90  # days
```

---

## Connectors

### Cloud Connectors

#### AWS Connector

```yaml
connector:
  name: AWS Production
  identifier: aws_prod
  type: Aws
  spec:
    credential:
      type: ManualConfig
      spec:
        accessKeyRef: aws_access_key
        secretKeyRef: aws_secret_key
      region: us-east-1
    delegateSelectors:
      - aws-delegate
    executeOnDelegate: true
```

#### AWS with IRSA (Recommended for EKS)

```yaml
connector:
  name: AWS EKS IRSA
  identifier: aws_irsa
  type: Aws
  spec:
    credential:
      type: Irsa
      spec:
        awsAssumeRole:
          roleArn: "arn:aws:iam::123456789012:role/harness-role"
    delegateSelectors:
      - eks-delegate
```

#### GCP Connector

```yaml
connector:
  name: GCP Production
  identifier: gcp_prod
  type: Gcp
  spec:
    credential:
      type: ManualConfig
      spec:
        secretKeyRef: gcp_service_account_key
    delegateSelectors:
      - gcp-delegate
```

#### Azure Connector

```yaml
connector:
  name: Azure Production
  identifier: azure_prod
  type: Azure
  spec:
    credential:
      type: ManualConfig
      spec:
        applicationId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        tenantId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        secretRef: azure_client_secret
    azureEnvironmentType: AZURE
    delegateSelectors:
      - azure-delegate
```

### Kubernetes Connectors

```yaml
connector:
  name: Production K8s
  identifier: prod_k8s
  type: K8sCluster
  spec:
    credential:
      type: ManualConfig
      spec:
        masterUrl: "https://k8s-api.company.com"
        auth:
          type: ServiceAccount
          spec:
            serviceAccountTokenRef: k8s_token
            caCertRef: k8s_ca_cert
    delegateSelectors:
      - k8s-delegate
```

#### K8s with Delegate Credentials

```yaml
connector:
  name: In-Cluster K8s
  identifier: in_cluster_k8s
  type: K8sCluster
  spec:
    credential:
      type: InheritFromDelegate
    delegateSelectors:
      - production
```

### Container Registry Connectors

#### Docker Hub

```yaml
connector:
  name: Docker Hub
  identifier: docker_hub
  type: DockerRegistry
  spec:
    dockerRegistryUrl: https://index.docker.io/v2/
    providerType: DockerHub
    auth:
      type: UsernamePassword
      spec:
        username: myuser
        passwordRef: docker_password
```

#### AWS ECR

```yaml
connector:
  name: ECR Registry
  identifier: ecr_registry
  type: Aws
  spec:
    credential:
      type: ManualConfig
      spec:
        accessKeyRef: aws_access_key
        secretKeyRef: aws_secret_key
    region: us-east-1
```

#### GCR

```yaml
connector:
  name: GCR Registry
  identifier: gcr_registry
  type: Gcp
  spec:
    credential:
      type: ManualConfig
      spec:
        secretKeyRef: gcp_key
```

### Harness Code Connector

```yaml
connector:
  name: Harness Code
  identifier: harness_code
  type: Harness
  spec:
    apiUrl: https://app.harness.io/code
    apiKeyRef: harness_api_key
    delegateSelectors:
      - code-delegate
```

### Test Connector

```bash
# Test connector via API
curl -X POST "https://app.harness.io/gateway/ng/api/connectors/testConnection/${CONNECTOR_ID}" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "accountIdentifier": "${HARNESS_ACCOUNT_ID}",
    "orgIdentifier": "${ORG_ID}",
    "projectIdentifier": "${PROJECT_ID}"
  }'
```

---

## Secrets Management

### Secret Managers

| Type | Description | Use Case |
|------|-------------|----------|
| **Harness Built-in** | Google KMS encrypted | Default, simple |
| **HashiCorp Vault** | Enterprise secrets | Production |
| **AWS Secrets Manager** | AWS native | AWS workloads |
| **GCP Secret Manager** | GCP native | GCP workloads |
| **Azure Key Vault** | Azure native | Azure workloads |

### Vault Connector

```yaml
connector:
  name: HashiCorp Vault
  identifier: vault
  type: Vault
  spec:
    vaultUrl: https://vault.company.com
    basePath: harness
    authToken: <+secrets.getValue("vault_root_token")>
    renewalIntervalMinutes: 60
    secretEngineManuallyConfigured: true
    secretEngineName: secret
    secretEngineVersion: 2
    readOnly: false
    delegateSelectors:
      - vault-delegate
```

### AWS Secrets Manager

```yaml
connector:
  name: AWS Secrets Manager
  identifier: aws_sm
  type: AwsSecretManager
  spec:
    credential:
      type: ManualConfig
      spec:
        accessKeyRef: aws_access_key
        secretKeyRef: aws_secret_key
    region: us-east-1
    secretNamePrefix: harness/
    delegateSelectors:
      - aws-delegate
```

### Secret References

```yaml
# Harness secret
<+secrets.getValue("my_secret")>

# Vault secret
<+secrets.getValue("vault://secret/data/myapp#api_key")>

# AWS Secrets Manager
<+secrets.getValue("awsSecretsManager://prod/database")>

# GCP Secret Manager
<+secrets.getValue("gcpSecretManager://projects/my-project/secrets/my-secret/versions/latest")>

# Azure Key Vault
<+secrets.getValue("azureVault://my-vault/secrets/my-secret")>
```

### Create Secret via API

```bash
curl -X POST "https://app.harness.io/gateway/ng/api/v2/secrets" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "secret": {
      "name": "my-api-key",
      "identifier": "my_api_key",
      "type": "SecretText",
      "spec": {
        "secretManagerIdentifier": "harnessSecretManager",
        "valueType": "Inline",
        "value": "supersecretvalue"
      }
    }
  }'
```

---

## Templates

### Template Types

| Type | Description | Scope |
|------|-------------|-------|
| **Step** | Reusable step | Any pipeline |
| **Stage** | Complete stage | Any pipeline |
| **Pipeline** | Full pipeline | Create instances |
| **StepGroup** | Group of steps | Any pipeline |

### Step Template

```yaml
template:
  name: Notify Slack
  identifier: notify_slack
  versionLabel: "1.0.0"
  type: Step
  orgIdentifier: default
  projectIdentifier: my_project
  spec:
    type: ShellScript
    timeout: 1m
    spec:
      shell: Bash
      onDelegate: true
      source:
        type: Inline
        spec:
          script: |
            curl -X POST $SLACK_WEBHOOK \
              -H 'Content-Type: application/json' \
              -d '{
                "text": "<+input>",
                "channel": "<+input>.default(\"#general\")"
              }'
      environmentVariables:
        - name: SLACK_WEBHOOK
          type: Secret
          value: <+input>
```

### Stage Template

```yaml
template:
  name: Standard K8s Deploy
  identifier: standard_k8s_deploy
  versionLabel: "1.0.0"
  type: Stage
  spec:
    type: Deployment
    spec:
      deploymentType: Kubernetes
      service:
        serviceRef: <+input>
      environment:
        environmentRef: <+input>
        deployToAll: false
        infrastructureDefinitions:
          - identifier: <+input>
      execution:
        steps:
          - step:
              name: Rollout Deployment
              identifier: rolloutDeployment
              type: K8sRollingDeploy
              timeout: 10m
              spec:
                skipDryRun: false
        rollbackSteps:
          - step:
              name: Rollback
              identifier: rollback
              type: K8sRollingRollback
              timeout: 10m
              spec: {}
      failureStrategies:
        - onFailure:
            errors:
              - AllErrors
            action:
              type: StageRollback
```

### Using Templates

```yaml
pipeline:
  name: My Pipeline
  stages:
    - stage:
        name: Deploy
        identifier: deploy
        template:
          templateRef: standard_k8s_deploy
          versionLabel: "1.0.0"
          templateInputs:
            type: Deployment
            spec:
              service:
                serviceRef: my_service
              environment:
                environmentRef: production
                infrastructureDefinitions:
                  - identifier: prod_k8s
```

---

## Policy as Code (OPA)

### Overview

Harness uses Open Policy Agent (OPA) Rego policies for governance enforcement.

### Policy Structure

```rego
package pipeline

import future.keywords.in

# Deny pipelines without approval for production
deny[msg] {
    some stage in input.pipeline.stages
    stage.stage.spec.environment.environmentRef == "production"
    not has_approval_step(input.pipeline)
    msg := "Production deployments require an approval step"
}

has_approval_step(pipeline) {
    some stage in pipeline.stages
    some step in stage.stage.spec.execution.steps
    step.step.type == "HarnessApproval"
}

# Require delegate selectors for production
deny[msg] {
    some stage in input.pipeline.stages
    stage.stage.spec.environment.environmentRef == "production"
    not stage.stage.spec.infrastructure.spec.delegateSelectors
    msg := "Production stages must specify delegate selectors"
}

# Enforce naming conventions
deny[msg] {
    not startswith(input.pipeline.identifier, "deploy_")
    not startswith(input.pipeline.identifier, "build_")
    msg := "Pipeline identifier must start with 'deploy_' or 'build_'"
}

# Require test stage before deploy
deny[msg] {
    has_deploy_stage(input.pipeline)
    not has_test_stage(input.pipeline)
    msg := "Pipelines with deployment must include a test stage"
}

has_deploy_stage(pipeline) {
    some stage in pipeline.stages
    stage.stage.type == "Deployment"
}

has_test_stage(pipeline) {
    some stage in pipeline.stages
    stage.stage.type == "CI"
    contains(lower(stage.stage.identifier), "test")
}

# Warn on high parallel concurrency
warn[msg] {
    input.pipeline.allowStageExecutions == true
    count(input.pipeline.stages) > 5
    msg := "High parallelism detected. Consider limiting concurrent stages."
}
```

### Policy Set Configuration

```yaml
policySet:
  name: Production Governance
  identifier: prod_governance
  description: "Governance policies for production deployments"
  policySetType: Pipeline
  policies:
    - policyRef: require_approval
      severity: error
    - policyRef: require_delegate_selectors
      severity: error
    - policyRef: naming_conventions
      severity: warning
  entitySelector:
    - type: PIPELINE
      filter:
        - key: projectIdentifier
          value: production_project
```

### Policy Evaluation Points

| Point | Description |
|-------|-------------|
| **On Save** | When pipeline is saved |
| **On Run** | Before pipeline execution |

---

## Audit Logs

### Query Audit Logs

```bash
# Get audit logs
curl -X POST "https://app.harness.io/gateway/ng/api/audits/list" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "accountIdentifier": "${HARNESS_ACCOUNT_ID}",
    "pageIndex": 0,
    "pageSize": 20,
    "filterType": "AUDIT",
    "startTime": 1704067200000,
    "endTime": 1704153600000
  }'
```

### Audit Event Types

| Event | Description |
|-------|-------------|
| `CREATE` | Resource created |
| `UPDATE` | Resource modified |
| `DELETE` | Resource deleted |
| `LOGIN` | User login |
| `PIPELINE_START` | Pipeline execution started |
| `PIPELINE_END` | Pipeline execution completed |

---

## API Reference

### Authentication

```bash
# API Key
curl -X GET "https://app.harness.io/gateway/ng/api/..." \
  -H "x-api-key: ${HARNESS_API_KEY}"

# Bearer Token
curl -X GET "https://app.harness.io/gateway/ng/api/..." \
  -H "Authorization: Bearer ${TOKEN}"
```

### Common Endpoints

| Resource | Endpoint |
|----------|----------|
| Users | `GET /ng/api/user/users` |
| User Groups | `GET /ng/api/user-groups` |
| Roles | `GET /ng/api/roles` |
| Resource Groups | `GET /ng/api/resourcegroup` |
| Connectors | `GET /ng/api/connectors` |
| Secrets | `GET /ng/api/v2/secrets` |
| Delegates | `GET /ng/api/delegate-token-ng` |
| Templates | `GET /template/api/templates` |
| Audit Logs | `POST /ng/api/audits/list` |

### Create Resources

```bash
# Create project
curl -X POST "https://app.harness.io/gateway/ng/api/projects" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "project": {
      "name": "My Project",
      "identifier": "my_project",
      "orgIdentifier": "default",
      "description": "My new project"
    }
  }'
```

---

## Best Practices

### Delegate Management

1. **High Availability**: Deploy 2+ replicas
2. **Resource Sizing**: 2GB RAM, 0.5 CPU minimum
3. **Tagging**: Use meaningful tags for routing
4. **Updates**: Enable auto-upgrade
5. **Monitoring**: Export metrics to Prometheus

### Security

1. **Least Privilege**: Minimal RBAC permissions
2. **Secret Rotation**: Use external secret managers
3. **Service Accounts**: Use for automation
4. **Audit Logging**: Review regularly
5. **Policy Enforcement**: OPA for governance

### Organization

1. **Hierarchy**: Logical org/project structure
2. **Naming**: Consistent identifiers
3. **Templates**: Reuse across projects
4. **Documentation**: Describe all resources

---

## Related Documentation

- [Harness Platform Docs](https://developer.harness.io/docs/platform)
- [Delegate Guide](https://developer.harness.io/docs/platform/delegates)
- [RBAC Guide](https://developer.harness.io/docs/platform/role-based-access-control)
- [Connectors Guide](https://developer.harness.io/docs/platform/connectors)
- [Secrets Management](https://developer.harness.io/docs/platform/secrets)
- [Templates](https://developer.harness.io/docs/platform/templates)
- [Governance](https://developer.harness.io/docs/platform/governance)
- [Harness Knowledge Base](../docs/HARNESS-KNOWLEDGE-BASE.md)
