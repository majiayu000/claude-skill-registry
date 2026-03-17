---
name: deploy
description: Deploy CDK stacks and content to AWS environments
---

# Deploy

How to deploy CDK infrastructure and application content to AWS.

## Environments

| Environment | Hostnames | AWS Account |
|-------------|-----------|-------------|
| sandbox | `sandbox.jaypie.net`, `garden-api.sandbox.jaypie.net`, `garden.sandbox.jaypie.net` | Finlayson Studio Sandbox (562880556342) |
| development | `development.jaypie.net`, `garden-api.development.jaypie.net`, `garden.development.jaypie.net` | Finlayson Studio Development (211125635435) |
| production | `jaypie.net`, `garden-api.jaypie.net`, `garden.jaypie.net` | Finlayson Studio Development (211125635435) |

## Stacks

| Stack ID | Description |
|----------|-------------|
| `JaypieDocumentation` | Documentation site (S3 + CloudFront) |
| `JaypieGardenData` | Shared DynamoDB table |
| `JaypieGardenApi` | Garden streaming API (Express Lambda) |
| `JaypieGardenNextjs` | Garden Next.js frontend |

## Remote Deploy (Preferred)

Deployments trigger automatically via GitHub Actions. Push or tag to trigger.

### Branch Triggers

| Branch Pattern | Deploys To | Lint/Test Required |
|---------------|------------|-------------------|
| `feat/*`, `fix/*`, `branch/*`, `claude/*`, `sandbox/*` | sandbox | No |
| `main`, `development/*` | development | Yes |
| _(no branch trigger)_ | production | _(tag only)_ |

Path filter: Only triggers when `workspaces/**`, `.github/actions/**`, or `.github/workflows/deploy-*.yml` change.

### Tag Triggers

| Tag Pattern | Deploys To | Lint/Test Required |
|-------------|------------|-------------------|
| `sandbox-*` | sandbox | No |
| `development-*` | development | Yes |
| `production-*`, `v0.*`, `v1.*` | production | Yes |
| `stack-documentation-*` | documentation only | No |

### Manual Trigger

Use the **Deploy Stacks (Manual)** workflow via GitHub Actions UI or CLI:

```bash
# Deploy all stacks to sandbox
gh workflow run deploy-stacks.yml -f environment=sandbox -f stacks=all

# Deploy specific stack(s)
gh workflow run deploy-stacks.yml -f environment=sandbox -f stacks="JaypieGardenData"
gh workflow run deploy-stacks.yml -f environment=sandbox -f stacks="JaypieGardenData JaypieGardenApi JaypieGardenNextjs"

# Deploy to production
gh workflow run deploy-stacks.yml -f environment=production -f stacks=all
```

### Quick Deploy via Tags

```bash
# Deploy to sandbox now
git tag sandbox-$(date +%s) && git push origin sandbox-$(date +%s)

# Deploy to development
git tag development-$(date +%s) && git push origin development-$(date +%s)

# Deploy to production
git tag production-$(date +%s) && git push origin production-$(date +%s)
```

## Local Deploy

Local deploys go to **sandbox only**. Requires AWS SSO login and `.env` configuration.

### Prerequisites

1. **AWS SSO Login** (ask user before running — correct browser must be in foreground):
   ```bash
   aws sso login --profile Developer-562880556342
   ```

2. **`.env` file** at repo root with at minimum:
   ```
   AWS_PROFILE=Developer-562880556342
   ```

### Local Deploy Scripts

```bash
# Deploy individual stacks (sandbox only)
npm run deploy:documentation:sandbox
npm run deploy:garden-api:sandbox
npm run deploy:garden-nextjs:sandbox
```

### Manual CDK Deploy

For stacks without scripts (e.g., `JaypieGardenData`) or custom scenarios:

```bash
# Set environment
export AWS_PROFILE=Developer-562880556342
export AWS_REGION=us-east-1
export CDK_DEFAULT_ACCOUNT=$(aws sts get-caller-identity --profile $AWS_PROFILE --query 'Account' --output text)
export CDK_DEFAULT_REGION=$AWS_REGION
export CDK_ENV_HOSTED_ZONE=jaypie.net
export PROJECT_ENV=sandbox
export PROJECT_KEY=jaypie
export PROJECT_NONCE=local
export PROJECT_SPONSOR=finlaysonstudio
export PROJECT_VERSION=$(node -p "require('./package.json').version")

# Build and deploy
npm run build
cd workspaces/cdk
npx cdk deploy JaypieGardenData --profile $AWS_PROFILE --require-approval never -c stacks=JaypieGardenData
```

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_PROFILE` | _(required)_ | AWS SSO profile name |
| `AWS_REGION` | `us-east-1` | AWS region |
| `CDK_DEFAULT_ACCOUNT` | _(from STS)_ | AWS account ID |
| `CDK_DEFAULT_REGION` | `us-east-1` | CDK target region |
| `CDK_ENV_HOSTED_ZONE` | `jaypie.net` | Route53 hosted zone |
| `PROJECT_ENV` | `sandbox` | Environment identifier |
| `PROJECT_KEY` | `jaypie` | Project identifier |
| `PROJECT_NONCE` | `local` | Unique resource suffix |
| `PROJECT_SPONSOR` | `finlaysonstudio` | Organization name |

## Monitoring Deployments

### Check Workflow Status

```bash
# List recent workflow runs
gh run list --limit 5

# Watch a running workflow
gh run watch

# View a specific run
gh run view <run-id>

# View failed run logs
gh run view <run-id> --log-failed
```

### Check Deployed Stacks in AWS

Use `mcp__jaypie__aws` with the appropriate profile:

```
aws("cloudformation_describe_stack", { stackName: "JaypieGardenData", profile: "Developer-562880556342" })
aws("dynamodb_describe_table", { tableName: "<table-name>", profile: "Developer-562880556342" })
aws("lambda_list_functions", { functionNamePrefix: "garden", profile: "Developer-562880556342" })
```

### CloudFormation Stack Naming

Deployed stacks follow this pattern:
```
cdk-${PROJECT_SPONSOR}-${PROJECT_KEY}-${PROJECT_ENV}-${PROJECT_NONCE}-${resource}
```
Example: `cdk-finlaysonstudio-jaypie-sandbox-local-garden-data`

## After Deploying

1. **Monitor the workflow** — use `gh run watch` or check GitHub Actions
2. **On failure** — delegate the failing run to a subagent to parse logs:
   ```
   gh run view <run-id> --log-failed
   ```
3. **Fix errors** — even those that seem unrelated (lint, test, typecheck). Push fixes and re-monitor
4. **Iterate** — repeat until the workflow succeeds
5. **Verify** — check that stacks exist in AWS and resources are healthy

## Troubleshooting

### SSO Session Expired
```bash
aws sso login --profile Developer-562880556342
```
Ask the user first — they need the Finlayson Studio browser in the foreground.

### Stack Deploys to Wrong Hostname
`PROJECT_ENV` is not set correctly. Ensure the GitHub environment has the right `PROJECT_ENV` value.

### "Stack does not exist" in CloudFormation
The stack hasn't been deployed yet. Deploy it via GitHub Actions or locally.

### "undefined" in Stack Name
A required environment variable is missing. Check all `PROJECT_*` and `CDK_*` variables.

### Cross-Stack Dependencies
`JaypieGardenData` must be deployed before `JaypieGardenApi` or `JaypieGardenNextjs` if they consume the shared table. Deploy data stack first, then consumer stacks.
