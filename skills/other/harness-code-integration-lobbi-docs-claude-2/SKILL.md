---
name: harness-code-integration
description: Harness Code repository workflows, triggers, PR pipelines, branch protection, and GitOps integration for AWS EKS deployments
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
triggers:
  - harness code
  - harness repo
  - harness git
  - pr pipeline
  - branch protection
  - code trigger
  - gitops
---

# Harness Code Integration Skill

Manage Harness Code repositories, triggers, PR pipelines, and GitOps workflows.

## Use For
- Repository setup, branch protection, PR validation pipelines
- Triggers (push, PR, tag), GitOps workflows, code policies

## Repository Structure for EKS Deployments

```
my-app/                          # Harness Code repository
├── src/                         # Application source
├── charts/
│   └── my-service/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-staging.yaml
│       ├── values-prod.yaml
│       └── templates/
├── .harness/
│   ├── pipelines/
│   │   ├── build.yaml
│   │   ├── deploy-dev.yaml
│   │   ├── deploy-staging.yaml
│   │   └── deploy-prod.yaml
│   └── inputsets/
│       ├── dev-inputs.yaml
│       └── prod-inputs.yaml
└── keycloak/
    └── realm-export.json
```

## Harness Code Connector

```yaml
connector:
  name: Harness Code
  identifier: harness_code
  type: HarnessCode
  spec:
    authentication:
      type: Http
      spec:
        type: UsernameToken
        spec:
          username: <+secrets.getValue("harness_code_user")>
          tokenRef: harness_code_token
```

## Triggers

### Push Trigger (Main Branch)
```yaml
trigger:
  name: Main Branch Push
  identifier: main_push
  enabled: true
  encryptedWebhookSecretIdentifier: ""
  description: "Deploy on push to main"
  source:
    type: Webhook
    spec:
      type: HarnessCode
      spec:
        repoName: my-app
        events:
          - Push
        actions: []
        payloadConditions:
          - key: targetBranch
            operator: Equals
            value: main
  pipelineIdentifier: deploy_pipeline
  inputSetRefs:
    - main_inputs
  stagesToExecute: []
```

### Pull Request Trigger
```yaml
trigger:
  name: PR Validation
  identifier: pr_validation
  enabled: true
  source:
    type: Webhook
    spec:
      type: HarnessCode
      spec:
        repoName: my-app
        events:
          - PullRequest
        actions:
          - Open
          - Reopen
          - Edit
          - Synchronize
        payloadConditions:
          - key: targetBranch
            operator: In
            value: main, develop
  pipelineIdentifier: pr_validation_pipeline
```

### Tag Trigger (Release)
```yaml
trigger:
  name: Release Tag
  identifier: release_tag
  enabled: true
  source:
    type: Webhook
    spec:
      type: HarnessCode
      spec:
        repoName: my-app
        events:
          - Push
        payloadConditions:
          - key: ref
            operator: StartsWith
            value: refs/tags/v
  pipelineIdentifier: release_pipeline
  inputYaml: |
    pipeline:
      identifier: release_pipeline
      variables:
        - name: version
          type: String
          value: <+trigger.payload.ref>.replace("refs/tags/", "")
```

## PR Validation Pipeline

```yaml
pipeline:
  name: PR Validation
  identifier: pr_validation_pipeline
  stages:
    - stage:
        name: Validate
        type: CI
        spec:
          cloneCodebase: true
          infrastructure:
            type: KubernetesDirect
            spec:
              connectorRef: eks_connector
              namespace: ci-runners
          execution:
            steps:
              - step:
                  type: Run
                  name: Lint Helm Chart
                  spec:
                    shell: Bash
                    command: |
                      helm lint charts/my-service
                      helm template charts/my-service --debug
              - step:
                  type: Run
                  name: Security Scan
                  spec:
                    shell: Bash
                    command: |
                      trivy config charts/my-service
                      checkov -d charts/my-service
              - step:
                  type: Run
                  name: Unit Tests
                  spec:
                    shell: Bash
                    command: npm test
              - step:
                  type: Plugin
                  name: PR Comment
                  spec:
                    connectorRef: harness_code
                    image: plugins/github-comment
                    settings:
                      message: "✅ All checks passed!"
```

## Branch Protection Rules

Configure via Harness Code UI or API:

```yaml
branchProtection:
  pattern: main
  rules:
    - requirePullRequest: true
    - requireReviews:
        count: 1
        dismissStaleReviews: true
        requireCodeOwners: true
    - requireStatusChecks:
        strict: true
        contexts:
          - "pr_validation_pipeline"
    - requireSignedCommits: false
    - restrictPushes:
        allowedUsers: []
        allowedTeams:
          - platform-team
    - restrictDeletions: true
    - requireLinearHistory: false
```

## GitOps Integration (ArgoCD via Harness)

### Update Release Repo
```yaml
- step:
    type: GitOpsUpdateReleaseRepo
    name: Update GitOps Repo
    identifier: update_gitops
    spec:
      connectorRef: harness_code
      repoName: gitops-config
      filePath: apps/<+service.name>/<+env.name>/values.yaml
      fileContent: |
        image:
          repository: <+artifact.image>
          tag: <+artifact.tag>
        keycloak:
          clientId: <+service.name>-client
```

### GitOps Sync
```yaml
- step:
    type: GitOpsSync
    name: Sync Application
    identifier: gitops_sync
    spec:
      applicationIdentifier: <+service.name>-<+env.name>
      prune: true
      dryRun: false
```

## Manifest Sources from Harness Code

### Helm Chart from Repo
```yaml
manifests:
  - manifest:
      identifier: main_chart
      type: HelmChart
      spec:
        store:
          type: HarnessCode
          spec:
            repoName: my-app
            branch: <+pipeline.variables.branch>
            folderPath: charts/my-service
        chartName: my-service
        helmVersion: V3
```

### Values Override
```yaml
manifests:
  - manifest:
      identifier: values_override
      type: Values
      spec:
        store:
          type: HarnessCode
          spec:
            repoName: my-app
            branch: main
            paths:
              - charts/my-service/values-<+env.name>.yaml
```

### Kustomize from Repo
```yaml
manifests:
  - manifest:
      identifier: kustomize
      type: Kustomize
      spec:
        store:
          type: HarnessCode
          spec:
            repoName: my-app
            branch: main
            folderPath: k8s/overlays/<+env.name>
```

## Code Quality Gates

```yaml
- step:
    type: Run
    name: Quality Gate
    spec:
      shell: Bash
      command: |
        # Helm lint
        helm lint charts/my-service --strict

        # Security scan
        trivy config charts/my-service --severity HIGH,CRITICAL --exit-code 1

        # Keycloak realm validation
        if [ -f keycloak/realm-export.json ]; then
          jq -e '.realm' keycloak/realm-export.json > /dev/null
        fi
      envVariables:
        TRIVY_SEVERITY: HIGH,CRITICAL
```

## Expressions for Harness Code

| Expression | Purpose |
|------------|---------|
| `<+trigger.payload.repository.name>` | Repository name |
| `<+trigger.payload.ref>` | Git reference (branch/tag) |
| `<+trigger.payload.pullRequest.number>` | PR number |
| `<+trigger.payload.pullRequest.sourceBranch>` | PR source branch |
| `<+trigger.payload.pullRequest.targetBranch>` | PR target branch |
| `<+trigger.payload.sender.login>` | User who triggered |
| `<+codebase.commitSha>` | Full commit SHA |
| `<+codebase.shortCommitSha>` | Short commit SHA |
| `<+codebase.branch>` | Branch name |
| `<+codebase.tag>` | Tag name (if tagged) |

## Webhook Payload Examples

### Push Event
```json
{
  "ref": "refs/heads/main",
  "before": "abc123",
  "after": "def456",
  "repository": {
    "name": "my-app",
    "full_name": "org/my-app"
  },
  "commits": [
    {
      "id": "def456",
      "message": "feat: add new endpoint",
      "author": { "name": "Developer" }
    }
  ]
}
```

### Pull Request Event
```json
{
  "action": "opened",
  "number": 42,
  "pullRequest": {
    "title": "Add Keycloak integration",
    "sourceBranch": "feature/keycloak",
    "targetBranch": "main",
    "state": "open"
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Trigger not firing | Check webhook configuration, verify event type |
| Clone failed | Verify connector credentials, check repo access |
| Branch not found | Confirm branch exists, check payload conditions |
| PR comment failed | Verify connector has write permissions |
| GitOps sync timeout | Check ArgoCD health, verify manifest validity |

## References
- [Harness Code Triggers](https://developer.harness.io/docs/platform/triggers/triggering-pipelines/)
- [GitOps with Harness](https://developer.harness.io/docs/continuous-delivery/gitops/)
