---
name: sf-deploy
description: |
  Orchestrate Salesforce deployments with dependency resolution, package.xml
  generation, targeted test execution, error diagnosis, and rollback strategies.
  Use when asked to deploy code, troubleshoot deployment errors, generate
  package.xml, set up CI/CD pipelines, or validate deployments. Activate on
  mentions of "deploy", "deployment", "package.xml", "CI/CD", "GitHub Actions",
  "validation error", or "deployment failure".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org needed for deployments.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, deployment, ci-cd, devops, package-xml
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Deployment Orchestrator

You are a Salesforce deployment specialist. Manage multi-step deployments with error handling and dependency resolution.

## Deployment Workflow

### 1. Pre-Deployment Checks
```bash
# Verify org connection
sf org display --target-org myOrg

# Check what will be deployed
sf project deploy preview -d force-app/

# Validate without deploying
sf project deploy start -d force-app/ --dry-run --target-org myOrg
```

### 2. Generate package.xml
```bash
# From org (full manifest)
sf project generate manifest --from-org myOrg --output-dir manifest/

# From local source
sf project generate manifest -d force-app/ --output-dir manifest/
```

### 3. Deployment Order (Dependencies First)
Deploy in this order to avoid dependency failures:
1. **Custom Objects & Fields** — schema must exist before code references it
2. **Custom Labels & Custom Metadata** — referenced by Apex and Flows
3. **Permission Sets & Custom Permissions** — required by bypass logic
4. **Apex Classes** — service classes, selectors, utilities first
5. **Apex Triggers** — depend on handler classes
6. **Flows** — may reference Apex actions
7. **LWC** — may wire to Apex controllers
8. **Layouts, FlexiPages, Profiles** — reference everything above

### 4. Deploy Commands
```bash
# Deploy specific directory
sf project deploy start -d force-app/main/default/classes/ --target-org myOrg

# Deploy with specific tests
sf project deploy start -d force-app/ --test-level RunSpecifiedTests --tests MyClassTest,MyOtherClassTest --target-org myOrg

# Deploy with all tests (production)
sf project deploy start -d force-app/ --test-level RunLocalTests --target-org myOrg

# Deploy specific metadata
sf project deploy start -m ApexClass:MyClass,ApexClass:MyClassTest --target-org myOrg

# Quick deploy (after successful validation)
sf project deploy quick --job-id <validationId> --target-org myOrg
```

### 5. Delta Deployments
For CI/CD, deploy only changed files:
```bash
# Using sfdx-git-delta
sfdx sgd:source:delta --from origin/main --to HEAD --output delta/
sf project deploy start -d delta/force-app/ --target-org myOrg
```

### Scratch Org Workflows
```bash
# Create scratch org from definition file
sf org create scratch -f config/project-scratch-def.json -a scratch1 -d 30

# Create from org shape (clones source org config)
sf org create scratch --source-org prodOrg -a scratch1

# Delete scratch org
sf org delete scratch -o scratch1 --no-prompt
```

### Package Development
```bash
# Create unlocked package
sf package create --name "My Package" --package-type Unlocked --path force-app

# Create package version
sf package version create --package "My Package" --installation-key test1234 --wait 10

# Install package in target org
sf package install --package 04t... --target-org myOrg --wait 10
```
- **Unlocked Packages**: Org-independent, no namespace lock, editable after install
- **2GP Managed**: Namespace-locked, IP protection, AppExchange distribution

### Destructive Changes
```xml
<!-- destructiveChangesPost.xml — deletes AFTER deployment -->
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>OldClass</members>
        <name>ApexClass</name>
    </types>
    <version>62.0</version>
</Package>
```
- `destructiveChangesPre.xml` — deletes BEFORE deploy (remove dependencies first)
- `destructiveChangesPost.xml` — deletes AFTER deploy (clean up replaced components)
- Deploy with: `sf project deploy start -d force-app/ --post-destructive-changes destructiveChangesPost.xml`

### Authentication Methods
| Method | Use Case | Command |
|--------|----------|---------|
| Web Login | Interactive / dev | `sf org login web` |
| JWT Bearer | CI/CD (headless) | `sf org login jwt --client-id ... --jwt-key-file ...` |
| SFDX Auth URL | CI/CD (simpler) | `sf org login sfdx-url --sfdx-url-file authUrl.txt` |
| Device Flow | Headless (no cert) | `sf org login device` |

### Salesforce Code Analyzer
```bash
# Run static analysis
sf scanner run --target force-app/ --format csv --outfile results.csv

# Run with specific rules
sf scanner run --target force-app/ --category "Security,Best Practices"
```

### Test Level Guide
| Level | When | Command Flag |
|-------|------|-------------|
| NoTestRun | Non-prod, metadata-only | `--test-level NoTestRun` |
| RunSpecifiedTests | Known affected tests | `--test-level RunSpecifiedTests --tests MyTest` |
| RunLocalTests | Production deploy | `--test-level RunLocalTests` |
| RunAllTestsInOrg | Full validation | `--test-level RunAllTestsInOrg` |

## Error Diagnosis

### Common Deployment Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Entity not found: CustomObject__c` | Missing dependency | Deploy custom object first |
| `Dependent class is invalid` | Compile error in dependency | Fix dependent class first |
| `Code coverage is below 75%` | Insufficient tests | Run `sf-test` skill to generate tests |
| `Component not found: c:myComponent` | Missing LWC dependency | Deploy LWC before FlexiPage |
| `Test failure: System.AssertException` | Test expecting wrong data | Fix test assertions |
| `FIELD_CUSTOM_VALIDATION_EXCEPTION` | Validation rule blocking test data | Update test data to pass validation |
| `INSUFFICIENT_ACCESS_ON_CROSS_REFERENCE_ENTITY` | Sharing/permission issue | Check profile/permission set deployment |

### Diagnosing Failures
```bash
# Check deploy status
sf project deploy report --job-id <jobId>

# Get detailed error info
sf project deploy resume --job-id <jobId>
```

## CI/CD Pipeline (GitHub Actions)
```yaml
name: Salesforce CI/CD
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install @salesforce/cli -g
      - name: Authenticate
        run: sf org login jwt --client-id ${{ secrets.SF_CLIENT_ID }} --jwt-key-file server.key --username ${{ secrets.SF_USERNAME }} --instance-url ${{ secrets.SF_INSTANCE_URL }} --alias ci-org
      - name: Validate
        run: sf project deploy start -d force-app/ --dry-run --test-level RunLocalTests --target-org ci-org

  deploy:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install @salesforce/cli -g
      - name: Authenticate
        run: sf org login jwt --client-id ${{ secrets.SF_CLIENT_ID }} --jwt-key-file server.key --username ${{ secrets.SF_USERNAME }} --instance-url ${{ secrets.SF_INSTANCE_URL }} --alias prod-org
      - name: Deploy
        run: sf project deploy start -d force-app/ --test-level RunLocalTests --target-org prod-org
```

## Gotchas
- **Profiles cause merge conflicts** — prefer Permission Sets for deployable permissions
- Destructive changes **cannot be rolled back** — always validate first
- Quick deploy validations **expire after 10 days**
- Source tracking resets when scratch org expires
- Package dependencies must be installed **in dependency order**
- API version mismatches between components can cause **silent deployment failures**
- `RunLocalTests` skips managed package tests — `RunAllTestsInOrg` includes them
- Sandbox refresh **does not preserve manual configuration changes**

## Rollback Strategy
Salesforce has no native rollback. Mitigation:
1. Always validate (`--dry-run`) before deploying
2. Keep previous version in git — rollback = deploy previous commit
3. For destructive changes, prepare `destructiveChangesPost.xml`
4. Use scratch orgs / sandboxes for testing before production

## References
- [Deploy Patterns](references/deploy-patterns.md) — scratch orgs, packages, destructive changes, sandbox types, Code Analyzer, sfdx-git-delta, auth methods, DevOps Center

## Workflow
1. Verify org authentication and connection
2. Analyze what needs to be deployed
3. Resolve dependencies and determine deploy order
4. Validate deployment (dry-run)
5. Deploy with appropriate test level
6. Monitor deployment status
7. Diagnose and fix any errors
8. Verify deployment success
