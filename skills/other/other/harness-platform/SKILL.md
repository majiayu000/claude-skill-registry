---
name: harness-platform
description: Harness Platform administration including delegates, RBAC, connectors, secrets, templates, policy as code (OPA), user management, audit logs, and governance
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch]
dependencies: [harness-mcp, harness-cd, harness-ci]
triggers: [harness delegate, harness rbac, harness connector, harness secret, harness template, harness policy, harness opa, harness user, harness admin]
---

# Harness Platform Administration Skill

Comprehensive Harness Platform administration for delegates, RBAC, connectors, secrets, templates, OPA policies, and governance.

## Platform Hierarchy

```
Account (Root)
├── Organization
│   ├── Project
│   │   ├── Pipelines, Services, Environments
│   │   ├── Connectors (project-level)
│   │   └── Secrets (project-level)
│   ├── Connectors (org-level)
│   └── Secrets (org-level)
├── Delegates
├── Secrets (account-level)
└── User Management
```

## Harness Delegates

**Types:** Kubernetes (Helm, YAML), Docker, Shell, ECS

**Kubernetes Helm Install:**
```bash
helm repo add harness-delegate https://app.harness.io/storage/harness-download/delegate-helm-chart/
helm install harness-delegate harness-delegate/harness-delegate-ng \
  --namespace harness-delegate --create-namespace \
  --set accountId="${HARNESS_ACCOUNT_ID}" \
  --set delegateToken="${DELEGATE_TOKEN}" \
  --set delegateName="prod-delegate" \
  --set replicas=2
```

**Delegate Selectors:** Route tasks to specific delegates with labels (e.g., production, aws, k8s)

**Troubleshooting:**
```bash
kubectl get pods -n harness-delegate
kubectl logs -n harness-delegate -l app=harness-delegate --tail=100
kubectl exec deployment/harness-delegate -n harness-delegate -- curl -s localhost:8080/api/health
```

## RBAC (Role-Based Access Control)

**Built-in Roles:**
- Account Admin (full access)
- Account Viewer (read-only)
- Organization Admin (org-level)
- Project Admin (project-level)
- Pipeline Executor (execute only)
- Pipeline Viewer (view only)

**Resource Types:** PIPELINE, SERVICE, ENVIRONMENT, CONNECTOR, SECRET, INFRASTRUCTURE

**Custom Role Example:**
```yaml
role:
  name: Deployment Manager
  permissions:
    - resourceType: PIPELINE
      actions: [core_pipeline_view, core_pipeline_execute]
    - resourceType: SERVICE
      actions: [core_service_view, core_service_access]
    - resourceType: ENVIRONMENT
      actions: [core_environment_view, core_environment_access]
```

**User Groups & Role Binding:**
- Create groups by team/function
- Bind roles to groups with resource groups
- Support SAML/SSO integration
- Service accounts for automation with API keys (90-day default expiry)

## Connectors

**Cloud Connectors:**
- **AWS:** ManualConfig (access/secret key) or IRSA (recommended for EKS)
- **GCP:** Service account key
- **Azure:** App ID, Tenant ID, Client Secret

**Kubernetes:**
- Manual: Master URL + Service Account token
- In-cluster: InheritFromDelegate (simplest)

**Container Registries:** Docker Hub, ECR, GCR, ACR

**Test Connector:**
```bash
curl -X POST "https://app.harness.io/gateway/ng/api/connectors/testConnection/${CONNECTOR_ID}" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -d '{"accountIdentifier":"...", "orgIdentifier":"...", "projectIdentifier":"..."}'
```

## Secrets Management

**Secret Managers:** Harness Built-in (Google KMS), HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault

**Vault Connector:**
```yaml
connector:
  type: Vault
  spec:
    vaultUrl: https://vault.company.com
    basePath: harness
    authToken: <+secrets.getValue("vault_root_token")>
    renewalIntervalMinutes: 60
    secretEngineVersion: 2
```

**Secret References:**
- Harness: `<+secrets.getValue("my_secret")>`
- Vault: `<+secrets.getValue("vault://secret/data/myapp#api_key")>`
- AWS SM: `<+secrets.getValue("awsSecretsManager://prod/database")>`

## Templates

**Types:** Step, Stage, Pipeline, StepGroup (reusable across pipelines)

**Step Template Example:**
```yaml
template:
  name: Notify Slack
  type: Step
  spec:
    type: ShellScript
    spec:
      shell: Bash
      script: |
        curl -X POST $SLACK_WEBHOOK \
          -H 'Content-Type: application/json' \
          -d '{"text":"<+input>"}'
```

**Using Templates in Pipeline:**
```yaml
template:
  templateRef: standard_k8s_deploy
  versionLabel: "1.0.0"
  templateInputs:
    spec:
      service:
        serviceRef: my_service
      environment:
        environmentRef: production
```

## Policy as Code (OPA)

**Policy Structure (Rego):**
```rego
package pipeline

# Deny production deploys without approval
deny[msg] {
    some stage in input.pipeline.stages
    stage.stage.spec.environment.environmentRef == "production"
    not has_approval_step(input.pipeline)
    msg := "Production requires approval step"
}

# Require delegate selectors
deny[msg] {
    some stage in input.pipeline.stages
    stage.stage.spec.environment.environmentRef == "production"
    not stage.stage.spec.infrastructure.spec.delegateSelectors
    msg := "Production must specify delegate selectors"
}
```

**Policy Set Configuration:**
```yaml
policySet:
  name: Production Governance
  policySetType: Pipeline
  policies:
    - policyRef: require_approval
      severity: error
    - policyRef: require_delegate_selectors
      severity: error
  entitySelector:
    - type: PIPELINE
      filter:
        - key: projectIdentifier
          value: production_project
```

**Evaluation Points:** On Save, On Run

## Audit Logs

**Query Logs:**
```bash
curl -X POST "https://app.harness.io/gateway/ng/api/audits/list" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -d '{"accountIdentifier":"...", "pageIndex":0, "pageSize":20}'
```

**Event Types:** CREATE, UPDATE, DELETE, LOGIN, PIPELINE_START, PIPELINE_END

## API Reference

**Authentication:**
```bash
# API Key
curl -H "x-api-key: ${HARNESS_API_KEY}"

# Bearer Token
curl -H "Authorization: Bearer ${TOKEN}"
```

**Common Endpoints:**
- Users: `GET /ng/api/user/users`
- User Groups: `GET /ng/api/user-groups`
- Roles: `GET /ng/api/roles`
- Resource Groups: `GET /ng/api/resourcegroup`
- Connectors: `GET /ng/api/connectors`
- Secrets: `GET /ng/api/v2/secrets`
- Delegates: `GET /ng/api/delegate-token-ng`
- Templates: `GET /template/api/templates`
- Audit Logs: `POST /ng/api/audits/list`

**Create Project:**
```bash
curl -X POST "https://app.harness.io/gateway/ng/api/projects" \
  -H "x-api-key: ${HARNESS_API_KEY}" \
  -d '{"project":{"name":"My Project","identifier":"my_project","orgIdentifier":"default"}}'
```

## Best Practices

**Delegate Management:**
1. Deploy 2+ replicas for HA
2. Resource sizing: 2GB RAM, 0.5 CPU minimum
3. Use meaningful tags for routing
4. Enable auto-upgrade
5. Monitor and export metrics

**Security:**
1. Least privilege RBAC
2. Use external secret managers with rotation
3. Service accounts for automation
4. Regular audit log review
5. OPA for governance enforcement

**Organization:**
1. Logical org/project hierarchy
2. Consistent naming conventions
3. Reuse templates across projects
4. Document all resources

## Related Documentation

- [Harness Docs](https://developer.harness.io/docs/platform)
- [Delegate Guide](https://developer.harness.io/docs/platform/delegates)
- [RBAC Guide](https://developer.harness.io/docs/platform/role-based-access-control)
- [Connectors](https://developer.harness.io/docs/platform/connectors)
- [Secrets](https://developer.harness.io/docs/platform/secrets)
- [Templates](https://developer.harness.io/docs/platform/templates)
- [Governance](https://developer.harness.io/docs/platform/governance)
