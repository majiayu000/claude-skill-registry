---
name: terraform-cicd
description: Automate Terraform with CI/CD pipelines, GitOps, Atlantis, and deployment workflows
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 07-terraform-cicd
bond_type: PRIMARY_BOND
---

# Terraform CI/CD Skill

Production CI/CD patterns for automated Terraform deployments.

## GitHub Actions

### PR Validation
```yaml
# .github/workflows/terraform-pr.yml
name: Terraform PR

on:
  pull_request:
    paths: ['terraform/**']

permissions:
  contents: read
  pull-requests: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3

      - name: Format Check
        run: terraform fmt -check -recursive

      - name: Init
        run: terraform init -backend=false

      - name: Validate
        run: terraform validate

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: aquasecurity/tfsec-action@v1.0.3

      - uses: bridgecrewio/checkov-action@v12
        with:
          directory: terraform/

  plan:
    needs: [validate, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - uses: hashicorp/setup-terraform@v3

      - run: terraform init
      - run: terraform plan -no-color | tee plan.txt

      - uses: actions/github-script@v7
        with:
          script: |
            const plan = require('fs').readFileSync('plan.txt', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '```\n' + plan.slice(0, 60000) + '\n```'
            });
```

### Deploy Workflow
```yaml
# .github/workflows/terraform-apply.yml
name: Terraform Apply

on:
  push:
    branches: [main]
    paths: ['terraform/**']

concurrency:
  group: terraform-${{ github.ref }}
  cancel-in-progress: false

jobs:
  apply:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - uses: hashicorp/setup-terraform@v3

      - run: terraform init
      - run: terraform apply -auto-approve
```

## Atlantis

### Configuration
```yaml
# atlantis.yaml
version: 3
automerge: false
parallel_plan: true
parallel_apply: false

projects:
  - name: dev
    dir: terraform/environments/dev
    autoplan:
      when_modified: ["*.tf", "*.tfvars"]
      enabled: true
    apply_requirements:
      - approved
      - mergeable

  - name: prod
    dir: terraform/environments/prod
    autoplan:
      enabled: true
    apply_requirements:
      - approved
      - mergeable
      - undiverged

workflows:
  default:
    plan:
      steps:
        - init
        - run: tflint
        - plan
```

## Terraform Cloud

```hcl
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      tags = ["app:myapp"]
    }
  }
}

resource "tfe_workspace" "app" {
  name         = "app-${var.environment}"
  organization = "my-org"
  auto_apply   = var.environment != "prod"

  vcs_repo {
    identifier     = "org/repo"
    branch         = "main"
    oauth_token_id = var.oauth_token_id
  }
}
```

## Drift Detection

```yaml
# .github/workflows/drift.yml
name: Drift Detection

on:
  schedule:
    - cron: '0 */6 * * *'

jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - run: terraform init
      - id: plan
        run: |
          terraform plan -detailed-exitcode || echo "drift=true" >> $GITHUB_OUTPUT

      - if: steps.plan.outputs.drift == 'true'
        uses: slackapi/slack-github-action@v1
        with:
          payload: '{"text": "Terraform drift detected!"}'
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| State lock timeout | Concurrent runs | Add concurrency control |
| Plan/Apply mismatch | Changes between steps | Cache plan file |
| Credentials error | OIDC not configured | Setup role trust |

## Usage

```python
Skill("terraform-cicd")
```

## Related

- **Agent**: 07-terraform-cicd (PRIMARY_BOND)
