---
name: harness-expert
description: Expert-level Harness template types, runtime inputs, expression language, pipeline patterns (CI/CD, GitOps, Canary, Blue-Green), versioning, and step configurations
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch]
dependencies: [universal-templating]
triggers: [harness step, harness stage, harness pipeline, harness template, deployment pattern]
---

# Harness Expert Skill

Expert knowledge of Harness template types, expression language, pipeline patterns, and deployment strategies.

## Harness Template Types

### 1. Step Templates

**Purpose:** Reusable step configurations across pipelines

**Types:**
- **ShellScript** - Execute bash/PowerShell scripts
- **Run** - Container step with image/command
- **K8sDeploy** - Kubernetes deployments
- **Http** - HTTP calls/webhooks
- **Approval** - Manual approval gates
- **ServiceNow** - ServiceNow integration
- **Custom** - Custom step plugins

**Template Structure:**
```yaml
template:
  name: Deploy to Kubernetes
  type: Step
  spec:
    type: K8sDeploy
    spec:
      service: <+input>
      environment: <+input>
      kubernetesCluster: <+input>
      namespace: <+input>
      releaseName: <+input>
      timeout: <+input.deployment_timeout>
      skipDryRun: false
      allowNoFilesFound: false
      delegateSelectors:
        - <+input.delegate_selector>
```

**Runtime Inputs (Required):**
```yaml
templateInputs:
  spec:
    service:
      serviceRef: <+input.service_name>
    environment:
      environmentRef: <+input.environment_name>
    kubernetesCluster:
      clusterId: <+input.cluster_id>
    namespace: <+input.k8s_namespace>
    releaseName: <+input.release_name>
```

---

### 2. Stage Templates

**Purpose:** Reusable stage definitions with multiple steps

**Template Structure:**
```yaml
template:
  name: Deploy Stage Template
  type: Stage
  spec:
    type: Deployment
    spec:
      service:
        serviceRef: <+input.service_ref>
      infrastructure:
        infrastructureDefinition:
          type: <+input.infra_type>  # Kubernetes, AWS, GCP, etc.
          spec: <+input.infra_spec>
      execution:
        steps:
          - step:
              name: Deploy
              identifier: deploy
              type: K8sDeploy
              spec:
                service: <+input.service_ref>
                environment: <+input.environment_ref>
          - step:
              name: Verify
              identifier: verify
              type: ShellScript
              spec:
                script: <+input.verify_script>
```

---

### 3. Pipeline Templates

**Purpose:** Full pipeline definitions with approval gates, notifications, conditions

**Template Structure:**
```yaml
template:
  name: Complete CI/CD Pipeline
  type: Pipeline
  spec:
    stages:
      - stage:
          name: Build
          identifier: build
          type: CI
          spec:
            codebase:
              repoName: <+input.repo_name>
              branch: <+input.branch>
              build:
                type: Docker
                spec:
                  dockerfile: Dockerfile
                  registryConnector: <+input.registry_connector>

      - stage:
          name: Deploy Dev
          identifier: deploy_dev
          type: Deployment
          spec:
            service:
              serviceRef: <+input.service_ref>
            environment:
              environmentRef: dev
            infrastructure:
              infrastructureDefinition:
                type: Kubernetes
                spec:
                  clusterId: <+input.dev_cluster_id>

      - stage:
          name: Approval
          identifier: approval
          type: Approval
          spec:
            approvalStepType: ShellScript
            script: echo "Deploying to production..."

      - stage:
          name: Deploy Prod
          identifier: deploy_prod
          type: Deployment
          spec:
            service:
              serviceRef: <+input.service_ref>
            environment:
              environmentRef: prod
            infrastructure:
              infrastructureDefinition:
                type: Kubernetes
                spec:
                  clusterId: <+input.prod_cluster_id>
```

---

## Runtime Inputs (`<+input>`) Syntax

### Basic Input Declaration

```yaml
spec:
  service:
    serviceRef: <+input>                    # Required, user must provide
  timeout: <+input.deployment_timeout>      # Optional with variable name
  replicas: <+input | default(3)>           # With default value
```

### Input Types & Examples

```yaml
String Input:
  image: <+input>
  service: <+input.service_name>

Number Input:
  timeout: <+input.timeout_minutes>
  replicas: <+input | default(3)>

Boolean Input:
  skip_tests: <+input | default(false)>
  enable_monitoring: <+input>

List/Array Input:
  environments: <+input.env_list>
  delegate_selectors: <+input.selectors>

Object Input:
  infrastructure: <+input.infra_spec>
```

### Conditional Inputs

```yaml
# Only required if another input is true
{{#if use_custom_image}}
  image: <+input.custom_image>
{{/if}}

# Conditional with expression
<+if>
  conditions:
    - key: environment
      operator: equals
      value: production
  then: <+input.prod_cluster>
  else: <+input.dev_cluster>
</+if>
```

---

## Expression Language Syntax

### Pipeline-Level Expressions

```yaml
# Access pipeline metadata
<+pipeline.name>                    # Pipeline name
<+pipeline.identifier>              # Pipeline identifier
<+pipeline.executionId>            # Execution ID
<+pipeline.triggeredBy>            # Who triggered it
<+pipeline.startTs>                # Start timestamp
<+pipeline.sequenceNumber>         # Execution sequence
```

### Stage-Level Expressions

```yaml
# Access stage metadata
<+stage.name>                      # Stage name
<+stage.identifier>                # Stage identifier
<+stage.status>                    # Stage status (Success, Failed, etc.)
<+stage.type>                      # Stage type (CI, Deployment, etc.)

# Stage variables
<+stage.variables.VARIABLE_NAME>   # Stage variable
<+stageArtifacts.IMAGE_ID>        # Output artifacts
```

### Step-Level Expressions

```yaml
# Access step outputs
<+steps.STEP_ID.output.outputKey>  # Step output variable
<+steps.build_docker.output.image> # Docker image from build step
<+steps.deploy.status>             # Step execution status

# Example
<+steps.deploy.deploymentStatuses> # Deployment status details
```

### Environment Variables

```yaml
<+env.JIRA_URL>                    # Environment variable
<+env.DOCKER_REGISTRY>             # From infrastructure

# Example in script
- step:
    type: ShellScript
    spec:
      script: |
        echo "Registry: <+env.DOCKER_REGISTRY>"
        docker push <+env.DOCKER_REGISTRY>/myapp
```

### Secret References

```yaml
# Retrieve secrets
<+secrets.getValue("my_secret")>           # Simple secret
<+secrets.getValue("vault://prod/db_pwd")> # Vault path

# Example
- step:
    type: ShellScript
    spec:
      environmentVariables:
        DB_PASSWORD: <+secrets.getValue("database_password")>
```

### Artifact & Output Expressions

```yaml
# Artifacts from previous stages
<+artifact.image>                  # Primary artifact
<+artifact.imageTag>               # Image tag
<+artifacts.COLLECTOR.IMAGE_ID>    # Named artifact

# Example in deploy
- step:
    type: K8sDeploy
    spec:
      image: <+artifact.image>:<+artifact.imageTag>
      service: <+input.service_ref>
```

---

## Pipeline Patterns

### Pattern 1: CI/CD Standard

**Description:** Standard continuous integration and deployment

**Flow:** Build → Test → Deploy Dev → Approval → Deploy Prod

```yaml
template:
  name: Standard CI/CD
  type: Pipeline
  spec:
    stages:
      # Stage 1: Build
      - stage:
          name: Build
          identifier: build
          type: CI
          spec:
            codebase:
              repoName: <+input.repo_name>
              branch: <+input.branch>
            build:
              type: Docker
              spec:
                dockerfile: Dockerfile
                registryConnector: <+input.docker_connector>
                imageName: <+input.image_name>
                imageTag: <+artifact.imageTag>

      # Stage 2: Test
      - stage:
          name: Test
          identifier: test
          type: CI
          depends:
            on:
              - build
          spec:
            build:
              type: Container
              spec:
                image: <+steps.build.output.image>
                command: npm test -- --coverage

      # Stage 3: Deploy Dev
      - stage:
          name: Deploy Dev
          identifier: deploy_dev
          type: Deployment
          depends:
            on:
              - test
          spec:
            service:
              serviceRef: <+input.service_ref>
            environment:
              environmentRef: dev
            infrastructure:
              infrastructureDefinition:
                type: Kubernetes
                spec:
                  clusterId: <+input.dev_cluster>
            execution:
              steps:
                - step:
                    type: K8sDeploy
                    spec:
                      service: <+input.service_ref>
                      image: <+artifact.image>

      # Stage 4: Manual Approval
      - stage:
          name: Approval for Production
          identifier: approval
          type: Approval
          depends:
            on:
              - deploy_dev
          spec:
            approvalStepType: Manual
            approvers:
              - <+input.approver_group>

      # Stage 5: Deploy Production
      - stage:
          name: Deploy Production
          identifier: deploy_prod
          type: Deployment
          depends:
            on:
              - approval
          spec:
            service:
              serviceRef: <+input.service_ref>
            environment:
              environmentRef: prod
            infrastructure:
              infrastructureDefinition:
                type: Kubernetes
                spec:
                  clusterId: <+input.prod_cluster>
            execution:
              steps:
                - step:
                    type: K8sDeploy
                    spec:
                      service: <+input.service_ref>
                      image: <+artifact.image>
```

---

### Pattern 2: GitOps with ArgoCD

**Description:** GitOps pattern using Argo CD for deployments

**Flow:** Build → Push Manifest → Trigger ArgoCD → Verify

```yaml
template:
  name: GitOps CI/CD Pipeline
  type: Pipeline
  spec:
    stages:
      # Stage 1: Build Docker Image
      - stage:
          name: Build
          identifier: build
          type: CI
          spec:
            codebase:
              repoName: <+input.repo_name>
              branch: <+input.branch>
            build:
              type: Docker
              spec:
                dockerfile: Dockerfile
                registryConnector: <+input.docker_connector>
                imageName: <+input.image_name>

      # Stage 2: Update Manifest Repository
      - stage:
          name: Update Manifests
          identifier: update_manifests
          type: CI
          depends:
            on:
              - build
          spec:
            steps:
              - step:
                  type: Run
                  spec:
                    container:
                      image: ubuntu:22.04
                      shell: Bash
                    script: |
                      git clone <+input.manifest_repo> manifests
                      cd manifests
                      sed -i "s|IMAGE_TAG|<+artifact.imageTag>|g" k8s/deployment.yaml
                      git add k8s/deployment.yaml
                      git commit -m "Update image to <+artifact.imageTag>"
                      git push origin main

      # Stage 3: Trigger ArgoCD Sync
      - stage:
          name: Deploy via ArgoCD
          identifier: deploy_argocd
          type: Deployment
          depends:
            on:
              - update_manifests
          spec:
            steps:
              - step:
                  type: Http
                  spec:
                    url: <+input.argocd_api_url>/api/v1/applications/<+input.app_name>/sync
                    method: Post
                    headers:
                      Authorization: Bearer <+secrets.getValue("argocd_token")>
                    requestBody: |
                      {
                        "syncPolicy": {
                          "syncStrategy": {
                            "argo": {}
                          }
                        }
                      }

      # Stage 4: Verify Deployment
      - stage:
          name: Verify
          identifier: verify
          type: Deployment
          depends:
            on:
              - deploy_argocd
          spec:
            steps:
              - step:
                  type: ShellScript
                  spec:
                    script: |
                      kubectl rollout status deployment/<+input.app_name> \
                        -n <+input.namespace> \
                        --timeout=5m
```

---

### Pattern 3: Canary Deployment

**Description:** Gradual traffic shift with automated verification

**Flow:** Deploy Canary (5%) → Verify → Increment Traffic (25%) → Verify → Full Deploy

```yaml
template:
  name: Canary Deployment Pattern
  type: Pipeline
  spec:
    stages:
      # Stage 1: Deploy Canary (5% traffic)
      - stage:
          name: Deploy Canary
          identifier: deploy_canary
          type: Deployment
          spec:
            service:
              serviceRef: <+input.service_ref>
            environment:
              environmentRef: prod
            infrastructure:
              infrastructureDefinition:
                type: Kubernetes
                spec:
                  clusterId: <+input.prod_cluster>
            execution:
              steps:
                - step:
                    type: K8sDeploy
                    spec:
                      canaryStrategy:
                        enabled: true
                        canaryPercentage: 5
                      service: <+input.service_ref>
                      image: <+artifact.image>

      # Stage 2: Verify Canary Metrics
      - stage:
          name: Verify Canary
          identifier: verify_canary
          type: Deployment
          depends:
            on:
              - deploy_canary
          spec:
            steps:
              - step:
                  type: ShellScript
                  spec:
                    script: |
                      # Check error rate, latency, etc.
                      kubectl logs -l version=canary -n <+input.namespace> \
                        --since=10m | grep ERROR | wc -l > /tmp/errors
                      ERRORS=$(cat /tmp/errors)
                      if [ $ERRORS -gt <+input.error_threshold> ]; then
                        exit 1
                      fi

      # Stage 3: Increment Traffic (25%)
      - stage:
          name: Increment Traffic
          identifier: increment_traffic
          type: Deployment
          depends:
            on:
              - verify_canary
          spec:
            steps:
              - step:
                  type: ShellScript
                  spec:
                    script: |
                      kubectl patch vs <+input.service_ref> -n <+input.namespace> \
                        -p '{"spec":{"hosts":[{"name":"*","http":[{"match":[{"uri":{"regex":".*"}}],"route":[{"destination":{"host":"<+input.service_ref>","subset":"canary"},"weight":25}]}]}]}}'

      # Stage 4: Verify Again
      - stage:
          name: Verify Increment
          identifier: verify_increment
          type: Deployment
          depends:
            on:
              - increment_traffic
          spec:
            steps:
              - step:
                  type: ShellScript
                  spec:
                    script: |
                      sleep 300  # Wait 5 minutes
                      # Same verification logic

      # Stage 5: Full Deployment
      - stage:
          name: Deploy Full
          identifier: deploy_full
          type: Deployment
          depends:
            on:
              - verify_increment
          spec:
            steps:
              - step:
                  type: K8sDeploy
                  spec:
                    service: <+input.service_ref>
                    image: <+artifact.image>
                    canaryStrategy:
                      enabled: true
                      canaryPercentage: 100
```

---

### Pattern 4: Blue-Green Deployment

**Description:** Two identical production environments with instant switching

**Flow:** Build → Deploy to Green (inactive) → Verify → Switch Traffic → Cleanup Blue

```yaml
template:
  name: Blue-Green Deployment Pattern
  type: Pipeline
  spec:
    variables:
      - name: active_color
        type: String
        default: blue
      - name: inactive_color
        type: String
        default: green

    stages:
      # Stage 1: Deploy to Inactive Environment
      - stage:
          name: Deploy to Inactive
          identifier: deploy_inactive
          type: Deployment
          spec:
            service:
              serviceRef: <+input.service_ref>
            environment:
              environmentRef: <+pipeline.variables.inactive_color>
            infrastructure:
              infrastructureDefinition:
                type: Kubernetes
                spec:
                  clusterId: <+input.prod_cluster>
            execution:
              steps:
                - step:
                    type: K8sDeploy
                    spec:
                      service: <+input.service_ref>
                      image: <+artifact.image>

      # Stage 2: Run Smoke Tests
      - stage:
          name: Smoke Tests
          identifier: smoke_tests
          type: CI
          depends:
            on:
              - deploy_inactive
          spec:
            steps:
              - step:
                  type: Run
                  spec:
                    container:
                      image: postman/newman
                      shell: Bash
                    script: |
                      newman run tests/smoke-collection.json \
                        --environment env-<+pipeline.variables.inactive_color>.json \
                        --reporters cli,json

      # Stage 3: Manual Approval for Switch
      - stage:
          name: Approve Traffic Switch
          identifier: approve_switch
          type: Approval
          depends:
            on:
              - smoke_tests
          spec:
            approvalStepType: Manual
            approvers:
              - <+input.approver_group>

      # Stage 4: Switch Traffic
      - stage:
          name: Switch Traffic
          identifier: switch_traffic
          type: Deployment
          depends:
            on:
              - approve_switch
          spec:
            steps:
              - step:
                  type: ShellScript
                  spec:
                    script: |
                      # Switch load balancer/service to point to inactive environment
                      kubectl patch service <+input.service_ref> \
                        -n production \
                        -p '{"spec":{"selector":{"version":"<+pipeline.variables.inactive_color>"}}}'

      # Stage 5: Verify Active Environment
      - stage:
          name: Verify Active
          identifier: verify_active
          type: Deployment
          depends:
            on:
              - switch_traffic
          spec:
            steps:
              - step:
                  type: ShellScript
                  spec:
                    script: |
                      for i in {1..30}; do
                        STATUS=$(curl -s -o /dev/null -w "%{http_code}" <+input.prod_url>/health)
                        if [ $STATUS -eq 200 ]; then
                          echo "Health check passed"
                          exit 0
                        fi
                        sleep 10
                      done
                      exit 1

      # Stage 6: Cleanup Old Environment
      - stage:
          name: Cleanup
          identifier: cleanup
          type: Deployment
          depends:
            on:
              - verify_active
          spec:
            steps:
              - step:
                  type: ShellScript
                  spec:
                    script: |
                      kubectl scale deployment <+input.service_ref>-<+pipeline.variables.active_color> \
                        -n production \
                        --replicas=0
```

---

## Template Versioning Best Practices

### Version Format

```
MAJOR.MINOR.PATCH

- MAJOR: Breaking changes (input names change, outputs change)
- MINOR: New optional inputs or non-breaking changes
- PATCH: Bug fixes, documentation updates
```

### Version Declaration

```yaml
template:
  name: Deploy Service
  identifier: deploy_service
  versionLabel: "2.1.0"
  spec:
    # Template specification
```

### Using Versioned Templates

```yaml
# Always use specific version in production
stages:
  - stage:
      template:
        templateRef: deploy_service
        versionLabel: "2.1.0"  # Explicit version
        templateInputs:
          spec:
            service: <+input.service_ref>
```

### Changelog Maintenance

```markdown
## Version 2.1.0 (2024-01-15)
- Added: Support for custom health checks
- Added: Optional monitoring setup
- Improved: Error messages for common issues
- Fixed: Timeout handling in K8s deployments

## Version 2.0.0 (2024-01-01) - BREAKING
- Changed: Input name from 'cluster' to 'clusterId'
- Changed: Stage type from 'Deploy' to 'Deployment'
- Removed: Legacy inline script support

## Version 1.0.0 (2023-12-01)
- Initial release
```

---

## Common Step Configurations

### K8s Deployment Step

```yaml
- step:
    name: Deploy to Kubernetes
    identifier: k8s_deploy
    type: K8sDeploy
    spec:
      service: <+input.service_ref>
      environment: <+input.environment_ref>
      kubernetesCluster:
        clusterId: <+input.cluster_id>
      namespace: <+input.namespace>
      releaseName: <+input.release_name>
      timeout: 10m
      skipDryRun: false
      allowNoFilesFound: false
      delegateSelectors:
        - <+input.delegate_selector>
```

### Container Step (Docker/Podman)

```yaml
- step:
    name: Run Docker Step
    identifier: docker_step
    type: Run
    spec:
      container:
        image: <+input.image>
        shell: Bash
        runAsUser: <+input.user>
      script: |
        #!/bin/bash
        set -e
        echo "Running test suite..."
        npm test -- --coverage
        echo "Test passed!"
      envVariables:
        TEST_ENV: <+input.environment>
        API_URL: <+env.API_URL>
      outputVariables:
        - name: test_result
          value: $(cat test-results.json)
```

### HTTP Step

```yaml
- step:
    name: Notify Slack
    identifier: notify_slack
    type: Http
    spec:
      url: <+input.slack_webhook>
      method: Post
      headers:
        Content-Type: application/json
      requestBody: |
        {
          "text": "Deployment to <+input.environment> completed!",
          "attachments": [
            {
              "text": "Version: <+artifact.imageTag>"
            }
          ]
        }
```

### Approval Step

```yaml
- step:
    name: Manual Approval
    identifier: approval
    type: Approval
    spec:
      approvalMessage: Deploy to production?
      approvers:
        - <+input.approver_group>
      approvalTimeout: 1d
      autoRejectIfNoActivity: true
      isAutoRejectAfterOverride: true
```

---

## Related Documentation

- [Harness Docs](https://developer.harness.io/docs)
- [Pipeline Templates](https://developer.harness.io/docs/platform/templates)
- [Expression Language](https://developer.harness.io/docs/platform/variables-and-expressions/harness-variables)
- [Deployment Strategies](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/kubernetes-executions)
