---
name: af-setup-gaininsight-stack
description: Set up the GainInsight Standard 4-layer stack with Amplify, Next.js, shadcn/ui, and auth. Use when bootstrapping new projects, configuring the opinionated infrastructure, or onboarding to the standard.

title: GainInsight Standard Skill
created: 2025-12-15
updated: 2026-02-18
last_checked: 2026-01-06
tags: [skill, gaininsight, infrastructure, aws, amplify, doppler]
parent: ../README.md
related:
  - ../../docs/guides/gaininsight-standard/README.md
---

# GainInsight Standard Skill

Directive knowledge for when and why to use the GainInsight Standard stack.

## What is GainInsight Standard?

GainInsight Standard is a **bundle** of components that together provide a complete production stack:

```
GainInsight Standard = AWS Infrastructure + Amplify Hosting + Testing + CI/CD + Security
                       └── Components ──────────────────────────────────────────────────┘
```

**Component breakdown:**

| Component | Source | What It Provides |
|-----------|--------|------------------|
| AWS Infrastructure | `.claude/templates/setup/components/aws-infrastructure/` | AWS Org, accounts, Doppler, DNS |
| Amplify Hosting | `.claude/templates/setup/components/hosting-amplify/` | CDK, Amplify apps, domains, builds |
| Testing | `.claude/templates/setup/components/testing/` | Jest, Playwright, sample tests |
| CI/CD | `.claude/templates/setup/components/cicd/` | GitHub Actions workflows |
| Security | `.claude/templates/setup/components/security/` | Dependabot configuration |

**Layers extend the base components:**

| Layer | What It Adds |
|-------|--------------|
| Layer 1 | AWS Infrastructure + Amplify Hosting + Hello World app |
| Layer 2 | Enhanced testing: selector contracts, reports, coverage |
| Layer 3 | shadcn/ui, Storybook, RTL component tests |
| Layer 4 | CI/CD with Amplify polling, Claude Code review |

**Alternative stacks using the same components:**

- **Directus Stack**: AWS Infrastructure + Lightsail Hosting + Testing + CI/CD
- **Minimal Stack**: Testing + CI/CD + Security (no AWS)

> **Note:** GainInsight Standard is now defined as a named combination in the [Module Registry](../../docs/reference/module-registry.yml). During Discovery, projects select individual modules rather than choosing "GainInsight Standard" as a monolithic path. The layer guides below remain the authoritative source for step-by-step setup of each module, and the [integration guides](../../docs/guides/integrations/) document how modules connect.

## When to Use This Skill

Use this skill when you need to:
- Set up a new project with the GainInsight Standard infrastructure
- Progress from one layer to the next in an existing project
- Validate layer completion with BDD tests
- Make decisions about layer configuration
- Tear down resources safely

## Skills Referenced

- **`af-provision-infrastructure`** - For credential access, DNS operations, Route53, CloudFront setup
- **`af-configure-cognito-auth`** - For Cognito User Pool setup, custom attributes, auth triggers
- **`af-configure-ses-email`** - For SES domain verification, sandbox/production, DKIM
- **`af-configure-test-frameworks`** - For test framework configuration (Layer 2)
- **`af-enforce-doc-standards`** - For documentation requirements

## Quick Reference

| Layer | Name | What It Provides | Time |
|-------|------|------------------|------|
| **1** | Infrastructure | AWS accounts, Doppler, Amplify, DNS, Hello World app | ~45 min |
| **2** | Testing | Jest, Playwright, test reports, selector contracts | ~20 min |
| **3** | UI & Styling | shadcn/ui components, Storybook, RTL tests, theming | ~30 min |
| **4** | CI/CD | GitHub Actions, Claude Code review, Storybook hosting | ~20 min |

**Test framework:**
- **E2E:** Playwright (complete user journeys)
- **Integration:** Jest + AWS SDK (backend behaviour)
- **Component:** RTL (React Testing Library - UI behaviour)
- **Unit:** Jest (pure logic)

**Reference implementation:** Juncan (`/data/worktrees/juncan/develop`)

---

## Module Registry Reference

GainInsight Standard maps to the following modules in the registry:

| Module | Registry Name | Integration Guides |
|--------|--------------|-------------------|
| AWS Infrastructure | `aws-infrastructure` | — |
| Amplify Hosting | `amplify` | [ESM Config](../../docs/guides/integrations/amplify-esm.md), [CI/CD Polling](../../docs/guides/integrations/cicd-amplify-polling.md) |
| Auth (Cognito) | `auth` | [Cognito+SES](../../docs/guides/integrations/cognito-ses.md), [Auth+Testing](../../docs/guides/integrations/auth-testing.md) |
| Email (SES) | `email` | [SES Per-Account](../../docs/guides/integrations/ses-per-account.md) |
| Testing | `testing` | — |
| UI & Styling | `ui-styling` | — |
| CI/CD | `cicd` | [CI/CD+Amplify](../../docs/guides/integrations/cicd-amplify-polling.md) |
| PostHog | `posthog` | — |
| Security | `security` | — |

When setting up a project that matches this combination, the setup process resolves dependencies from the registry and loads integration guides automatically. The layer guides remain the step-by-step reference for each module's setup.

---

## Rules

### Critical Rules (MUST)

1. **MUST complete layers in order.** Layer 2 depends on Layer 1, etc. Never skip layers.

2. **MUST run validation tests before proceeding to next layer.** Each layer has validation tests that verify completion. Do not proceed until tests pass.

3. **MUST use Doppler for ALL secrets.** No `.env` files, no hardcoded credentials, no exceptions.

4. **MUST never commit secrets or credentials.** Check `.gitignore` includes `amplify_outputs.json`, `.env*`, credentials files.

5. **MUST create test specifications BEFORE implementation.** Install layer tests in RED phase first, then implement until GREEN.

6. **MUST configure ALL THREE environments.** Dev, test, and prod. Do not stop after dev only.

7. **MUST include `amplify/package.json` with `"type": "module"`.** Without this, sandbox deployment fails with module resolution errors.

### Process Rules (SHOULD)

8. **SHOULD use `{project-name}` placeholder pattern** in all configs and documentation. Replace on installation.

9. **SHOULD follow branch-to-environment mapping:** develop -> dev, staging -> stg, main -> prd.

10. **SHOULD create Amplify apps in each AWS account** (not three branches in one app). Each environment is isolated.

11. **SHOULD run `cdk bootstrap` in each account** before first Amplify deployment.

12. **SHOULD store AMPLIFY_APP_ID in Doppler** after creating each Amplify app.

13. **SHOULD use port 3001 by default** (not 3000) to avoid conflicts with Metabase and other services.

14. **SHOULD configure paired test scripts** for credential-dependent tests:
    - `test:integration` - raw script for CI/CD (credentials injected by GitHub Actions)
    - `test:integration:local` - wrapped with `doppler run` for local development
    - `test:e2e` / `test:e2e:local` - same pattern
    - See `af-setup-project` skill for full script configuration

### Quality Rules (MAY)

15. **MAY stop after any layer.** Each layer produces a complete, useful setup. Layer 1 alone is deployable.

16. **MAY use Juncan as reference** for working patterns. It's the most recent complete implementation.

17. **MAY run sandbox workflow tests** to validate full developer experience (requires GI server).

---

## Workflows

### Starting a New Project

1. Ask: "Is greenfield setup complete?" (GitHub repo, Linear team, `.claude/` synced)
2. If no -> Complete greenfield setup first
3. If yes -> Begin Layer 1 from [Infrastructure Guide](../../docs/guides/gaininsight-standard/layer-1-infrastructure.md)
4. Ask: "What project name will you use?" (used throughout as `{project-name}`)

### Progressing to Next Layer

1. Run current layer validation tests
2. If tests fail -> Debug and fix until passing
3. If tests pass -> Ask user: "Layer N is complete. Continue to Layer N+1 or stop here?"
4. If continue -> Load next layer guide
5. Install next layer's test specifications (RED phase)
6. Implement layer steps until tests pass (GREEN phase)

### Validating Layer Completion

For each layer, run the appropriate test command:

| Layer | Test Command |
|-------|--------------|
| 1 | `doppler run --project {project} --config dev -- npm run test:layer-1` |
| 2 | `doppler run --project {project} --config dev -- npm run test:layer-2` |
| 3 | `doppler run --project {project} --config dev -- npm run test:layer-3` |
| 4 | `doppler run --project {project} --config dev -- npm run test:layer-4` |

### Deciding on Teardown Scope

1. Ask: "What needs to be removed?"
   - Full project decommission -> Full teardown (T.1-T.14)
   - Reset infrastructure only -> Partial (T.3-T.8, keep GitHub/Linear)
   - Remove CI/CD only -> Layer 4 teardown (T.2)
2. Confirm: "This will permanently delete [scope]. Type project name to confirm."
3. Proceed only after explicit confirmation
4. Follow [Teardown Guide](../../docs/guides/gaininsight-standard/teardown.md)

---

## Examples

### Good: Complete Layer Validation

```
User: Layer 1 setup is done
Agent: Let me run the Layer 1 validation tests.
       [Runs: doppler run --project juncan --config dev -- npm run test:layer-1]
       All 12 scenarios passed. Layer 1 is verified complete.
       Would you like to continue to Layer 2 (Testing Framework)?
```

### Bad: Skipping Validation

```
User: Layer 1 setup is done
Agent: Great! Let's move to Layer 2.
       [Starts Layer 2 without running tests]
```
**Why bad:** Layer 1 may have incomplete configuration. Tests catch issues like missing AMPLIFY_APP_ID, failed CDK bootstrap, or incorrect DNS delegation.

### Good: ESM Configuration

```bash
# amplify/package.json
{
  "type": "module"
}

# Root tsconfig.json excludes amplify
"exclude": ["node_modules", ".amplify", "amplify", "tests"]
```

### Bad: Missing ESM Configuration

```bash
# No amplify/package.json
# Result: npx ampx sandbox fails with:
# Cannot find module '.../amplify/data/resource'
```
**Why bad:** Amplify Gen 2 uses ESM. Without the module type declaration, Node.js can't resolve ES module imports.

### Good: Environment Isolation

```
Dev account:  juncan-dev   -> develop branch  -> dev.juncan.gaininsight.global
Test account: juncan-test  -> staging branch  -> test.juncan.gaininsight.global
Prod account: juncan-prod  -> main branch     -> juncan.gaininsight.global
```

### Bad: Shared Account

```
Single account with three Amplify apps pointing to different branches
```
**Why bad:** No blast radius isolation. A misconfiguration in dev can affect prod data.

---

## Common Pitfalls

### 1. Sandbox Deployment Fails with Module Error

**Problem:** `Cannot find module '.../amplify/data/resource'`

**Solution:** Create `amplify/package.json` with `{"type": "module"}`. Add `"amplify"` to root tsconfig.json excludes.

### 2. Amplify Build Fails with Bootstrap Error

**Problem:** `BootstrapDetectionError` or CDK-related failure

**Solution:** Run `npx cdk bootstrap aws://ACCOUNT_ID/eu-west-2` in each AWS account before first Amplify deployment.

### 3. Domain Shows "Available" but SSL Fails

**Problem:** Custom domain status is AVAILABLE but HTTPS connections fail

**Solution:** Verify branch mapping. Check `aws amplify get-domain-association` returns non-empty `subDomains` array. If empty, run `update-domain-association` with correct branch mapping.

### 4. Tests Can't Find Doppler Credentials

**Problem:** Tests fail with "Doppler project not found" or AWS auth errors

**Solution:** Ensure `doppler run --project {project} --config dev --` prefix on all test commands. Verify project exists with `doppler projects list`.

### 5. Layer Tests Fail After Setup "Complete"

**Problem:** User says setup is done but validation tests fail

**Solution:** Never trust "done" without running tests. Always run `npm run test:layer-N` before proceeding. Fix failures before moving to next layer.

### 6. Multiple Package Lock Files

**Problem:** Amplify build fails with "Multiple package lock files found"

**Solution:** Use only npm (not pnpm/yarn) for GainInsight Standard projects. Commit only `package-lock.json`. Remove any `pnpm-lock.yaml` or `yarn.lock`.

### 7. Cognito Custom Attributes Set to Immutable

**Problem:** Custom attributes like `custom:tenant_id` can't be updated after user creation.

**Root cause:** Setting `mutable: false` on custom attributes blocks ALL updates, including `AdminUpdateUserAttributes` called by Lambda functions with IAM permissions. This is enforced at the Cognito service level.

**Impact:**
- Super admin grant/revoke breaks (`custom:platform_role`)
- User removal from orgs breaks (`custom:tenant_id`, `custom:user_type`)
- Post-confirmation Lambda attribute updates break

**Solution:** Set ALL custom attributes to `mutable: true`. Enforce security at the application/API level instead.

**Note:** Changing attribute mutability requires User Pool recreation (deletes all users). Plan attributes carefully before first deployment.

### 8. Integration Tests Fail with "Auth flow not enabled"

**Problem:** `InvalidParameterException: Auth flow not enabled for this client`

**Root cause:** Amplify Gen 2 creates User Pool Clients with limited auth flows. Integration tests using `AdminInitiateAuthCommand` need `ALLOW_ADMIN_USER_PASSWORD_AUTH`.

**Solution:** Add CDK escape hatch in `amplify/backend.ts`:
```typescript
const cfnUserPoolClient = backend.auth.resources.cfnResources.cfnUserPoolClient;
cfnUserPoolClient.explicitAuthFlows = [
  "ALLOW_CUSTOM_AUTH",
  "ALLOW_REFRESH_TOKEN_AUTH",
  "ALLOW_USER_SRP_AUTH",
  "ALLOW_ADMIN_USER_PASSWORD_AUTH", // Required for integration tests
];
```

### 9. SES Emails Not Sending in Test Environment

**Problem:** E2E tests timeout waiting for emails that never arrive.

**Root cause:** SES is per-AWS-account, not per-Amplify-app. Each account (dev, test, prod) needs:
1. Production access requested (24-48h approval)
2. Sending domain verified with DKIM

**Architecture:**
```
juncan-dev account  → SES config (shared by all sandboxes)
juncan-test account → SES config (separate)
juncan-prod account → SES config (separate)
```

**Solution:** Request SES production access for each account:
```bash
doppler run --project {project} --config stg -- aws sesv2 put-account-details \
  --mail-type TRANSACTIONAL \
  --website-url "https://your-url.com" \
  --use-case-description "Transactional emails for authentication" \
  --production-access-enabled
```

**Cognito SES Configuration:** Cognito defaults to sending via its own domain (50 emails/day limit). For higher volume, configure Cognito to use your verified SES identity. Without this, E2E tests creating multiple users will hit `LimitExceededException`. See `emailConfiguration` in Cognito User Pool settings.

### 10. Custom Emails (Not Cognito) Need DKIM

**Problem:** Cognito verification emails work but custom emails (invitations, notifications) don't arrive.

**Root cause:** Cognito sends via its configured identity with DKIM. Custom emails sent directly via SES client may lack DKIM, causing Gmail to reject them.

**Solution:** For custom email sending:
1. Send from a domain with DKIM configured (not just a verified email address)
2. Or use a domain like `noreply@{project}.gaininsight.global` which already has DKIM

Check DKIM status:
```bash
aws sesv2 get-email-identity --email-identity "your-domain.com" \
  --query 'DkimAttributes.{Status:Status,SigningEnabled:SigningEnabled}'
```

### 11. CI/CD: `create-deployment` API Doesn't Work

**Problem:** `BadRequestException: Operation not supported. App is already connected a repository`

**Root cause:** The `aws amplify create-deployment` API only works for apps NOT connected to GitHub. GainInsight apps are git-connected.

**Solution:** Use hybrid architecture:
- **Amplify auto-build** handles deployment (triggered by git push)
- **GitHub Actions** polls for completion, then runs E2E tests

See CI/CD workflow templates at `.claude/templates/gaininsight-standard/cicd/`.

### 12. CI/CD Polling Finds Wrong Amplify Job

**Problem:** E2E tests run against old deployment because polling grabbed the wrong job.

**Root cause:** Using "get latest job" can grab a job from a previous push if multiple pushes happen quickly.

**Solution:** Poll for job matching the specific commit SHA:
```bash
JOB_ID=$(aws amplify list-jobs --app-id $APP_ID --branch-name $BRANCH \
  --query "jobSummaries[?commitId=='$COMMIT_SHA'].jobId" --output text | head -1)
```

---

## Essential Reading

### Procedural Guides (HOW)

| Guide | Purpose |
|-------|---------|
| [Layer 1: Infrastructure](../../docs/guides/gaininsight-standard/layer-1-infrastructure.md) | AWS accounts, Doppler, Amplify, DNS setup |
| [Layer 2: Testing](../../docs/guides/gaininsight-standard/layer-2-testing.md) | Jest, Playwright, selector contracts |
| [Layer 3: UI & Styling](../../docs/guides/gaininsight-standard/layer-3-ui-styling.md) | shadcn/ui components, Storybook, RTL tests |
| [Layer 4: CI/CD](../../docs/guides/gaininsight-standard/layer-4-cicd.md) | GitHub Actions, Claude Code review |
| [Teardown](../../docs/guides/gaininsight-standard/teardown.md) | Safe destruction procedures |

### Related Documentation

| Resource | Purpose |
|----------|---------|
| [AWS Amplify Guide](../../docs/guides/aws-amplify-guide.md) | DynamoDB modeling, GraphQL, authentication patterns |
| [Testing Guide](../../docs/guides/testing-guide.md) | Test pyramid, coverage targets, Playwright patterns |
| BDD Guide | AgentFlow uses Playwright directly (not Cucumber) - see BDD Guide above |

### Reference Implementation

**Juncan** (`/data/worktrees/juncan/develop`) is the most recent complete GainInsight Standard implementation. Reference it for:
- Selector contracts in `tests/selectors/`
- ESM configuration in `amplify/package.json`
- Test organization: `tests/e2e/`, `tests/integration/`, colocated RTL tests
- Storybook stories in `stories/`
- GitHub Actions workflows

### Templates

Templates are available at `.claude/templates/gaininsight-standard/`:
- `hello-world-app/` - Complete Next.js + Amplify Gen 2 + shadcn/ui starter
- `tests/gaininsight-stack/` - Layer validation BDD tests
- `docs/` - Project documentation templates
- `cicd/` - GitHub Actions workflows for Amplify hybrid CI/CD:
  - `lint-and-test.yml.tpl` - PR validation
  - `deploy-simple.yml.tpl` - Dev/prod deployment monitoring
  - `deploy-with-e2e.yml.tpl` - Staging deployment with E2E tests
- `.github/workflows/claude-code-review.yml.template` - Automated PR review with Claude Code

#### Claude Code Review Workflow

The `claude-code-review.yml.template` provides automated PR reviews using Claude Code. Features:
- Uses OIDC authentication (requires `id-token: write` permission)
- Reads project's CLAUDE.md for style/convention guidance
- Optional Linear integration to create issues from significant findings

**Required secrets:** `CLAUDE_CODE_OAUTH_TOKEN`
**Optional secrets:** `LINEAR_API_KEY`, `LINEAR_TEAM_ID`

See [Layer 4: CI/CD guide](../../docs/guides/gaininsight-standard/layer-4-cicd.md) for installation.
