---
name: af-setup-process
description: Use when setting up new AgentFlow projects or installing modules after Discovery. Covers minimal setup (always the same), module installation (driven by Discovery's Tech Stack Agreement), brownfield setup, and project registry.

# AgentFlow documentation fields
title: Setup Process
created: 2025-10-29
updated: 2026-02-26
last_checked: 2026-02-26
tags: [skill, process, setup, infrastructure, bootstrap]
parent: ../README.md
---

# Setup Process

## Quick Reference

| Setup Type | Use Case | Command |
|------------|----------|---------|
| Minimal Setup | New project bootstrap (always the same) | `/af:setup` |
| Module Setup | Install modules after Discovery | Post-Discovery |
| Brownfield | Add AgentFlow to existing repo | `/brownfield:add` |

**Templates:** `.claude/templates/setup/`
**Detailed guide:** `docs/guides/setup-guide.md`

## When to Use

**✅ Use Setup Process for:**
- Creating new AgentFlow projects (greenfield)
- Adding AgentFlow to existing projects (brownfield)
- Bootstrapping BDD/TDD development environments

**❌ Don't use for:**
- Updating AgentFlow framework (use `/af:sync`)
- Fixing broken configurations (use troubleshooting)

## Prerequisites

**Required:**
- Node.js v20+
- Git installed
- 2GB+ free disk space
- Internet connectivity

**For GainInsight Infrastructure:**
- Access to gidev server
- `LINEAR_API_KEY` available in environment (provided automatically on gidev)

## Rules

### Critical Setup Rules

1. **Linear team creation is automatic** - Setup creates the team via GraphQL API
2. **Never skip validation phase** - Always verify setup completed correctly
3. **Use templates** - Reference `.claude/templates/setup/` for CLAUDE.md and handoff messages
4. **Add to project registry** - Use `project-registry` CLI for gidev projects
5. **Commit with --no-verify** - Initial commits skip git hooks (no code to lint yet)

### Setup State Rules

6. **State is tracked** - Setup maintains JSON state for resume capability
7. **Resume on failure** - Just re-run setup command to continue
8. **Validate before declaring success** - Run build and tests

## Workflows

### Workflow: Greenfield Setup (GainInsight)

**When:** Creating a new project from scratch on gidev infrastructure.

**Prerequisites:** LINEAR_API_KEY available in environment (provided automatically on gidev)

**Questions to ask:**
1. Project name? (for Linear team and GitHub repo)
2. Linear team key? (2-5 uppercase letters, unique in workspace)
3. Development model? (trunk, trunk+develop, or feature branch)
   - **Trunk**: Single branch (`main`), PRs merge directly to main → deploys to Live
   - **Trunk + develop**: Two branches (`develop` → Dev, `main` → Live), but trunk-based workflow (develop is the working branch, main is promotion-only)
   - **Feature branch**: Multiple environments, PRs to develop → Dev → Test → Live
4. GitHub repo exists? If no, what name? Org or personal?
5. Brief project description?
6. Zulip stream? (optional)

**Steps:**
1. Create Linear team (via GraphQL API - see `af-linear-api-expertise`)
   - Use `teamCreate` mutation with name, key, `cyclesEnabled: true`
   - Archive default workflow states
   - Create AgentFlow states based on development model
   - Create standard labels (Epic, BDD, UX, Docs, Debt)
2. Create GitHub repo if needed: `gh repo create GainInsightDev/{repo-name} --private`
3. Create Linear issue for setup (via GraphQL API)
4. Create Doppler project: `doppler projects create {project-name} --description "Secrets for {project-name}"`
   - Creates default configs (dev, stg, prd)
   - Module Installation will later populate with AWS credentials, API keys, etc.
5. Create bare repo on gidev: `add-repo git@github.com:Owner/repo.git`
6. Create stable worktree based on development model:
   - **Trunk**: `git worktree add /srv/worktrees/{repo}/main main`
   - **Trunk+develop**: Create `develop` branch, then `git worktree add /srv/worktrees/{repo}/develop develop` (main stays remote-only)
   - **Feature branch**: `git worktree add /srv/worktrees/{repo}/develop develop`
7. Sync AgentFlow: `npx ts-node .claude/scripts/sync/sync-from-agentflow.ts`
8. Create CLAUDE.md from template: `.claude/templates/setup/greenfield-claudemd.md`
9. Create security config: `mkdir -p .github && cp .claude/templates/github/dependabot.yml .github/`
10. Initial commit and push (use --no-verify)
11. Add to project registry via `project-registry` CLI (see "Project Registry Entry" workflow)
12. Create docs portal files: `docs/_category_.json`, `docs/README.md`
13. Update Linear issue to Done
14. Show handoff message: `.claude/templates/setup/greenfield-handoff.txt`

**Success criteria:**
- ✅ Linear team created with AgentFlow workflow states
- ✅ Doppler project created with default configs
- ✅ GitHub repo exists and has initial commit
- ✅ Stable worktree at `/srv/worktrees/{repo}/develop`
- ✅ Project in registry with docs config
- ✅ Linear issue created and marked Done
- ✅ Security config (dependabot.yml) in place

### Workflow: Linear Team Setup

**When:** Creating a new Linear team with AgentFlow workflow states (part of Greenfield setup).

**Prerequisites:** LINEAR_API_KEY available in environment (provided automatically on gidev)

**Inputs:**
- Project name (human-readable)
- Team key (2-5 uppercase letters, unique)
- Development model: `trunk`, `trunk+develop`, or `feature`

**Steps:**

1. **Create team:**
   ```bash
   curl -s -X POST https://api.linear.app/graphql \
     -H "Content-Type: application/json" \
     -H "Authorization: $LINEAR_API_KEY" \
     -d '{
       "query": "mutation { teamCreate(input: { name: \"PROJECT_NAME\", key: \"KEY\", cyclesEnabled: true }) { success team { id } } }"
     }'
   ```

2. **Get and archive default states:**
   ```bash
   # Get default states
   curl -s -X POST https://api.linear.app/graphql \
     -H "Content-Type: application/json" \
     -H "Authorization: $LINEAR_API_KEY" \
     -d '{"query": "{ team(id: \"TEAM_ID\") { states { nodes { id name } } } }"}'

   # Archive each default state
   curl -s -X POST https://api.linear.app/graphql \
     -H "Content-Type: application/json" \
     -H "Authorization: $LINEAR_API_KEY" \
     -d '{"query": "mutation { workflowStateArchive(id: \"STATE_ID\") { success } }"}'
   ```

3. **Create AgentFlow workflow states:**

   | State | Type | Color | Position | Trunk | Trunk+Develop | Feature |
   |-------|------|-------|----------|-------|---------------|---------|
   | Discovered | backlog | #bec2c8 | 0 | ✅ | ✅ | ✅ |
   | Refining | started | #5e6ad2 | 1 | ✅ | ✅ | ✅ |
   | Approved | unstarted | #bec2c8 | 2 | ✅ | ✅ | ✅ |
   | In Progress | started | #f2c94c | 3 | ✅ | ✅ | ✅ |
   | Waiting for Feedback | started | #eb5757 | 4 | ✅ | ✅ | ✅ |
   | In Review | started | #0f783c | 5 | ✅ | ✅ | ✅ |
   | Dev | completed | #f2c94c | 6 | — | ✅ | ✅ |
   | Test | completed | #26b5ce | 7 | — | — | ✅ |
   | Live | completed | #5e6ad2 | 8 | ✅ | ✅ | ✅ |
   | Canceled | canceled | #95a2b3 | 9 | ✅ | ✅ | ✅ |
   | Duplicate | canceled | #95a2b3 | 10 | ✅ | ✅ | ✅ |

   ```bash
   curl -s -X POST https://api.linear.app/graphql \
     -H "Content-Type: application/json" \
     -H "Authorization: $LINEAR_API_KEY" \
     -d '{
       "query": "mutation { workflowStateCreate(input: { teamId: \"TEAM_ID\", name: \"STATE_NAME\", type: \"TYPE\", color: \"COLOR\", position: POSITION }) { success } }"
     }'
   ```

4. **Create standard team labels:**

   | Label | Color | Purpose |
   |-------|-------|---------|
   | Epic | #f2994a | Epic grouping |
   | BDD | #26b5ce | BDD scenario work |
   | UX | #4cb782 | UX/design work |
   | Docs | #5e6ad2 | Documentation |
   | Debt | #f7c8c1 | Technical debt |

   **Workspace-scoped labels** (created once, apply to all teams):

   | Label | Color | Purpose |
   |-------|-------|---------|
   | approved:test | #26b5ce | Signal: deploy to test environment |
   | approved:live | #0f783c | Signal: deploy to production |

   ```bash
   curl -s -X POST https://api.linear.app/graphql \
     -H "Content-Type: application/json" \
     -H "Authorization: $LINEAR_API_KEY" \
     -d '{
       "query": "mutation { issueLabelCreate(input: { teamId: \"TEAM_ID\", name: \"LABEL_NAME\", color: \"COLOR\" }) { success } }"
     }'
   ```

**Success criteria:**
- ✅ Team created with correct key and cycles enabled
- ✅ Default states archived
- ✅ AgentFlow states created with correct colors
- ✅ Standard labels created

**Full script:** See `af-linear-api-expertise` skill for complete team setup script.

### Workflow: Module Setup (Post-Discovery)

**When:** After Discovery phase completes with a Tech Stack Agreement listing selected modules.

**Prerequisites:**
- Minimal setup (greenfield or brownfield) already completed
- Discovery phase complete with Tech Stack Agreement at `docs/architecture/tech-stack-agreement.md`
- Module registry available at `.claude/docs/reference/module-registry.yml`

**Process:**

1. **Read the Tech Stack Agreement**
   - Parse selected modules list
   - Identify applicable integration guides

2. **Resolve dependency order**
   - Load module registry
   - Topologically sort selected modules by `depends_on`
   - Example order: doppler → git → aws-infrastructure → amplify → auth → email → testing → ui-styling → cicd
   - Note: doppler and git are core modules (already installed), so Module Installation starts with aws-infrastructure

3. **For each module in dependency order:**
   a. **Load the module's skill** (e.g., `af-cognito-expertise` for auth)
   b. **Load applicable integration guides** (e.g., if both auth and email selected, load `cognito-ses.md`)
   c. **Execute setup steps** following the skill's installation workflow
   d. **Run validation tests** before proceeding to the next module
   e. **Record completion** in the Tech Stack Agreement

4. **Post-installation validation**
   - Run full validation suite
   - Verify all integration points
   - Update Linear with setup status

**Module installation order example (GainInsight Standard combination):**
```
1. aws-infrastructure  → af-environment-infrastructure skill
   Integration: none at this stage
2. amplify             → af-amplify-expertise skill
   Integration: amplify-esm.md (ESM configuration)
3. auth                → af-cognito-expertise skill
   Integration: cognito-ses.md (if email also selected)
4. email               → af-ses-expertise skill
   Integration: ses-per-account.md, auth-testing.md (if testing selected)
5. testing             → af-testing-expertise skill
   Integration: auth-testing.md (if auth selected)
6. ui-styling          → af-ux-design-expertise skill
7. cicd                → af-delivery-process skill
   Integration: cicd-amplify-polling.md (if amplify selected)
8. posthog             → af-posthog-expertise skill
9. security            → af-security-expertise skill
10. figma              → af-figma-design-expertise skill (optional, depends on ui-styling)
    Setup: Add MCP server URL, set up Code Connect, create Figma project structure
```

**Success criteria:**
- ✅ All selected modules installed in dependency order
- ✅ All applicable integration guides followed
- ✅ Validation tests pass for each module
- ✅ Tech Stack Agreement updated with completion status
- ✅ Ready for Refinement phase

### Workflow: Component Installation

**When:** Installing individual components during greenfield setup.

**Templates location:** `.claude/templates/setup/components/`
**Validation tests:** `.claude/templates/setup/validation/`

#### Install Testing Component

```bash
# 1. Create directories
mkdir -p tests/unit tests/e2e

# 2. Copy config files
cp .claude/templates/setup/components/testing/jest.config.js ./
cp .claude/templates/setup/components/testing/playwright.config.ts ./

# 3. Copy sample tests
cp .claude/templates/setup/components/testing/sample-unit.test.ts tests/unit/sample.test.ts
cp .claude/templates/setup/components/testing/sample-e2e.spec.ts tests/e2e/sample.spec.ts

# 4. Install dependencies
npm install --save-dev jest @types/jest ts-jest @playwright/test

# 5. Add scripts to package.json (merge manually or use jq)
# "test": "jest"
# "test:unit": "jest --selectProjects unit"
# "test:e2e": "playwright test"

# 6. Install Playwright browsers
npx playwright install chromium
```

**Validation:**
```bash
npm run test:unit  # Should pass with sample test
ls tests/unit tests/e2e  # Directories exist
```

#### Install CI/CD Component

```bash
# 1. Create directory
mkdir -p .github/workflows

# 2. Copy workflow based on stack
# For base/generic:
cp .claude/templates/setup/components/cicd/ci-base.yml .github/workflows/ci.yml

# For Directus:
cp .claude/templates/setup/components/cicd/ci-directus.yml .github/workflows/ci.yml

# 3. Optionally add Claude review
cp .claude/templates/setup/components/cicd/claude-review.yml .github/workflows/
```

**Validation:**
```bash
ls .github/workflows/ci.yml  # File exists
yq eval '.' .github/workflows/ci.yml  # Valid YAML
```

#### Install Security Component

```bash
# 1. Create directory
mkdir -p .github

# 2. Copy Dependabot config
cp .claude/templates/setup/components/security/dependabot.yml .github/
```

**Validation:**
```bash
ls .github/dependabot.yml  # File exists
yq eval '.version' .github/dependabot.yml  # Should return 2
```

#### Install Documentation Component

```bash
# 1. Create directories
mkdir -p docs/architecture/adr docs/guides

# 2. Copy templates
cp .claude/templates/setup/components/docs/_category_.json docs/
cp .claude/templates/setup/components/docs/docs-README.md docs/README.md

# 3. Replace {DATE} placeholders
sed -i "s/{DATE}/$(date +%Y-%m-%d)/g" docs/README.md
```

**Validation:**
```bash
ls docs/README.md docs/_category_.json  # Files exist
head -5 docs/README.md | grep -q "^---"  # Has frontmatter
```

#### Install AWS Infrastructure Component

**When:** Project will be hosted on AWS (Amplify, Lightsail, ECS, etc.)

**Template:** `.claude/templates/setup/components/aws-infrastructure/`

**Environment Models:**

| Model | Accounts | Use Case |
|-------|----------|----------|
| `simple` | prod only | Prototypes, small projects |
| `standard` | dev + prod | Most projects (recommended) |
| `full` | dev + test + prod | Enterprise, regulated |

**Prerequisites:** Doppler project already created (core module in Minimal Setup)

**Installation Steps:**

1. **Ask environment model** via AskUserQuestion
2. **Follow setup guide:** `.claude/templates/setup/components/aws-infrastructure/setup-guide.md`
3. **Key steps:**
   - Create AWS Organization Unit
   - Create AWS accounts (per model)
   - Add AWS credentials to existing Doppler project (dev/stg/prd configs)
   - Set up DNS delegation (optional)
   - Create git branches matching environments

**Validation:**
```bash
# AWS credentials stored in Doppler (project already exists from Minimal Setup)
doppler run --project {project-name} --config dev -- aws sts get-caller-identity
```

**After AWS Infrastructure, choose hosting component.**

#### Install Amplify Hosting Component

**When:** Next.js + GraphQL + DynamoDB stack

**Template:** `.claude/templates/setup/components/hosting-amplify/`

**Prerequisites:** AWS Infrastructure component completed

**Installation Steps:**

1. **Bootstrap CDK** in each account
2. **Create Amplify apps** per environment
3. **Configure service roles** for Gen 2 deployments
4. **Set platform** to WEB_COMPUTE for SSR
5. **Configure custom domains**
6. **Copy amplify backend template**
7. **Create amplify.yml build config**

**Files to copy:**
```bash
cp -r .claude/templates/setup/components/hosting-amplify/amplify/ ./
cp .claude/templates/setup/components/hosting-amplify/amplify.yml ./
```

**Validation:**
```bash
# CDK bootstrapped
doppler run --project {project-name} --config dev -- \
  aws cloudformation describe-stacks --stack-name CDKToolkit

# Amplify app exists
doppler run --project {project-name} --config dev -- \
  aws amplify get-app --app-id $(doppler secrets get AMPLIFY_APP_ID --plain)
```

**Full guide:** `.claude/templates/setup/components/hosting-amplify/setup-guide.md`

#### Install Lightsail Hosting Component

**When:** Docker/Directus + PostgreSQL stack

**Template:** `.claude/templates/setup/components/hosting-lightsail/`

**Prerequisites:** AWS Infrastructure component completed

**Installation Steps:**

1. **Create Lightsail instance(s)** per environment
2. **Configure firewall** (ports 22, 80, 443)
3. **Set up instance** with Docker
4. **Generate secrets** (Directus keys, Postgres password)
5. **Deploy Docker Compose**
6. **Configure SSL** with Caddy
7. **Configure DNS** A records

**Files to copy:**
```bash
cp .claude/templates/setup/components/hosting-lightsail/docker-compose.yml ./
```

**Validation:**
```bash
# Instance running
doppler run --project {project-name} --config prd -- \
  aws lightsail get-instance --instance-name {project-name}-prod

# Directus responding
curl -s https://{project-name}.gaininsight.global/server/health
```

**Full guide:** `.claude/templates/setup/components/hosting-lightsail/setup-guide.md`

### Workflow: Run Validation Suite

**When:** After component installation to verify everything works.

```bash
# Option 1: Run from AgentFlow templates
cd .claude/templates/setup/validation
npm install
PROJECT_ROOT=/path/to/new-project npm test

# Option 2: Copy validation to project and run
cp -r .claude/templates/setup/validation /path/to/new-project/
cd /path/to/new-project/validation
npm install
npm test
```

**Expected output:**
```
Running 4 projects...
  ✓ testing.spec.ts (5 tests)
  ✓ cicd.spec.ts (6 tests)
  ✓ security.spec.ts (5 tests)
  ✓ docs.spec.ts (5 tests)

21 passed
```

### Workflow: Brownfield Setup (GainInsight)

**When:** Adding AgentFlow to an existing repository.

**Prerequisites:**
- Bare repo exists at `/srv/repos/{repo}.git` (via `add-repo`)
- Running on gidev (LINEAR_API_KEY available via Doppler)

**Questions to ask:**
1. Repo name? (validate exists at /srv/repos/)
2. Linear team exists? If no:
   - Project name for Linear team?
   - Team key? (2-5 uppercase letters)
   - Development model? (trunk, trunk+develop, or feature)
3. If team exists: Linear team key? (validate exists, check for AgentFlow states)
4. Which branch for stable worktree?
5. Zulip stream? (optional)

**Steps:**
1. Validate bare repo exists: `ls /srv/repos/{repo}.git`
2. Check if Linear team exists (via GraphQL API)
   - If no: Create team with AgentFlow states (see "Linear Team Setup" workflow)
   - If yes: Verify AgentFlow states exist, add missing states if needed
3. Create Doppler project if not exists: `doppler projects create {project-name} --description "Secrets for {project-name}"`
4. Detect default branch from bare repo
5. Create or use stable worktree
6. Install dependencies: `npm install`
7. Sync AgentFlow framework
8. Create CLAUDE.md from template: `.claude/templates/setup/brownfield-claudemd.md`
9. Create security config if missing: `mkdir -p .github && cp .claude/templates/github/dependabot.yml .github/`
10. Commit and push (use --no-verify)
11. Add to project registry via `project-registry` CLI (see "Project Registry Entry" workflow)
12. Create docs portal files
13. Create Linear issue with next steps (docs retrofit, security audit)
14. Show handoff message: `.claude/templates/setup/brownfield-handoff.txt`

**Success criteria:**
- ✅ Linear team exists with AgentFlow workflow states
- ✅ Doppler project created with default configs
- ✅ AgentFlow framework synced to `.claude/`
- ✅ CLAUDE.md created with project context
- ✅ Project in registry with docs config
- ✅ Linear issue created with retrofit instructions

### Workflow: Project Registry Entry

**When:** Adding any project to gidev infrastructure.

**Registry:** `project-registry` CLI (backed by PostgreSQL/RDS — but always use the CLI, never raw SQL).

**Reading config:**
```bash
project-registry list                     # All project keys
project-registry <project>                # Full config (YAML format)
project-registry <project> <field>        # Single field (dot notation)
project-registry <project> linear.team_id # Example: get Linear team UUID
```

**Updating config:**
```bash
project-registry set <project> <field> <value>
# Examples:
project-registry set myproject agent_enabled true
project-registry set myproject branching_strategy trunk+develop
project-registry set myproject linear.team_key HLM
```

**Key fields:**

| Field | Purpose |
|-------|---------|
| `name` | Display name |
| `linear.team_key` / `linear.team_id` | Linear team mapping (use UUID for linearis CLI) |
| `zulip.stream` / `zulip.stream_id` | Zulip stream for agent notifications (legacy: `slack.channel_id`) |
| `github.repo` | GitHub repo (Org/repo) — always use `GainInsightDev/{repo}` |
| `repo_path` | Bare repo on server |
| `worktree_base` | Where worktrees live |
| `run_as` | Unix user for agent sessions |
| `port_base` | Base port for dev servers |
| `agent_enabled` | true to allow Agentflow to spawn agents |
| `branching_strategy` | `trunk`, `trunk+develop`, or `feature-branch` |
| `doppler.project` / `doppler.config` | Secrets management |

**Steps to add a new project:**

1. Find next port_base: `project-registry list` then check existing port_base values, add 10000
2. Create project entry with initial config:
   ```bash
   project-registry set {project-key} name "{Display Name}"
   project-registry set {project-key} linear.team_key "{TEAM_KEY}"
   project-registry set {project-key} linear.team_id "{team-uuid}"
   project-registry set {project-key} github.repo "GainInsightDev/{project-key}"
   project-registry set {project-key} repo_path "/srv/repos/{project-key}.git"
   project-registry set {project-key} worktree_base "/srv/worktrees/{project-key}"
   project-registry set {project-key} run_as "tmux-shared"
   project-registry set {project-key} port_base "{next-port-base}"
   project-registry set {project-key} agent_enabled true
   project-registry set {project-key} branching_strategy "feature-branch"
   project-registry set {project-key} doppler.project "{project-key}"
   project-registry set {project-key} doppler.config "dev"
   project-registry set {project-key} zulip.stream "{project-key}"
   ```
3. Verify: `project-registry {project-key}`

**Lookups:**
```bash
project-registry find-by-team HLM          # Find project by Linear team key
project-registry find-by-channel C0ACD7LK95J  # Find by channel (legacy Slack, migrating to Zulip)
project-registry find-by-repo myproject     # Find by repo name
project-registry teams                      # List all team→project mappings
project-registry channels                   # List all channel→project mappings
```

### Portal Integration

The project registry drives two portals on gidev:

| Portal | Registry Field | What It Does |
|--------|---------------|--------------|
| **Docs Portal** | docs config | Syncs documentation from repo to docs site |
| **Costs Portal** | AWS account IDs | Queries AWS Cost Explorer for project spend |

**Docs Portal:**
- Automatically syncs when registry entry exists
- Requires `docs/README.md` in the specified branch/subpath
- No manual refresh needed

**Costs Portal:**
- Requires AWS account IDs in project config
- Must run `sudo /usr/local/bin/collect-aws-costs` after adding accounts
- Runs automatically on schedule, but manual run picks up new projects immediately

### Workflow: Resume After Failure

**When:** Setup failed partway through.

**Steps:**
1. Setup detects incomplete state automatically
2. Prompts to resume or restart
3. Continues from last successful phase
4. Preserves completed work

**Just re-run the setup command** - resume is automatic.

## Decision Points

### Greenfield vs Brownfield?
- **New project from scratch** → Greenfield
- **Existing codebase** → Brownfield
- **Failed setup** → Resume (automatic)

### Which modules to install?
Module selection happens during Discovery, not during Setup:
- Discovery outputs a Tech Stack Agreement with selected modules
- Setup reads the agreement and installs modules in dependency order
- See `.claude/docs/reference/module-registry.yml` for available modules
- See `.claude/docs/guides/integrations/` for cross-module integration guides

## Common Pitfalls

1. **Linear team key already exists**
   - Team keys must be unique across the workspace
   - Check existing teams first: `curl ... '{"query": "{ teams { nodes { key } } }"}'`
   - Choose a different 2-5 character uppercase key

2. **Running in non-empty directory**
   - Greenfield needs empty directory
   - Prevents conflicts

3. **Skipping project registry**
   - Docs portal won't sync
   - Add entry via `project-registry` CLI

4. **Wrong port_base**
   - Check existing: `project-registry list` then inspect port_base values
   - Add 10000 to highest existing value
   - Prevents port collisions

5. **Missing docs portal files**
   - Create `docs/_category_.json` and `docs/README.md`
   - Required for docs portal sync

6. **Costs portal not showing new project**
   - Add `aws.accounts` to project registry
   - Run `sudo /usr/local/bin/collect-aws-costs` to refresh
   - Costs data appears after next collection run

## Zulip Notifications

**Optional** - requires Zulip bot credentials in Doppler.

**Steps:**
1. Identify the target Zulip stream from the project registry
2. Post message via Zulip API using bot credentials (`ZULIP_BOT_EMAIL`, `ZULIP_API_KEY`, `ZULIP_REALM`)

**If bot not subscribed to stream:**
- Subscribe bot to the stream, or tell user to do so
- Don't block setup completion

**Message template:**
```
:white_check_mark: AgentFlow setup complete for *{repo-name}*

:package: *{Project Name}*
:link: GitHub: https://github.com/{owner}/{repo}
:ticket: Linear: https://linear.app/gaininsight/issue/{ISSUE-ID}
:file_folder: Worktree: `/srv/worktrees/{repo}/{branch}`

Run `start-work {repo-name} {ISSUE-ID}` to begin development.
```

## Success Criteria

A successful setup means:
- ✅ All phases completed
- ✅ Build succeeds: `npm run build`
- ✅ Tests pass: `npm test`
- ✅ Git repository initialized
- ✅ Project in registry (gidev)

### Workflow: Pre-E2E Infrastructure Requirements

**When:** After Layer 1 (Infrastructure) but before E2E tests can pass.

**Problem:** E2E tests involving email (signup, password reset, invitations) will fail without proper infrastructure setup.

**Full guide:** See [Auth Setup Guide](../../docs/guides/gaininsight-standard/auth-setup.md) for comprehensive Cognito + SES workflows. Skills: `af-cognito-expertise`, `af-ses-expertise`.

**Checklist:**

| Requirement | Command to Check | Impact if Missing |
|-------------|------------------|-------------------|
| SES production access (per account) | `aws sesv2 get-account --query ProductionAccessEnabled` | Emails don't send in sandbox mode |
| Gmail testing credentials | `doppler secrets get GMAIL_TESTING_SERVICE_ACCOUNT` | Can't verify emails in tests |
| Domain DKIM verification | `aws sesv2 get-email-identity --email-identity domain` | Custom emails rejected by Gmail |
| Cognito attributes mutable | Check `amplify/auth/resource.ts` | Can't update user attributes |

**SES Production Access Request:**
```bash
# Request for each environment's AWS account
doppler run --project {project} --config {env} -- aws sesv2 put-account-details \
  --mail-type TRANSACTIONAL \
  --website-url "https://your-url.com" \
  --use-case-description "Transactional emails for authentication" \
  --production-access-enabled
```
Approval takes 24-48 hours per account.

**DKIM Setup for Custom Email Domain:**
```bash
# 1. Add domain identity
aws sesv2 create-email-identity --email-identity your-domain.com

# 2. Get DKIM tokens
aws sesv2 get-email-identity --email-identity your-domain.com \
  --query 'DkimAttributes.Tokens'

# 3. Add 3 CNAME records to DNS:
# {token1}._domainkey.your-domain.com → {token1}.dkim.amazonses.com
# {token2}._domainkey.your-domain.com → {token2}.dkim.amazonses.com
# {token3}._domainkey.your-domain.com → {token3}.dkim.amazonses.com

# 4. Verify DKIM is active (may take 72h)
aws sesv2 get-email-identity --email-identity your-domain.com \
  --query 'DkimAttributes.Status'  # Should be "SUCCESS"
```

**Note:** Without DKIM, custom emails (invitations, notifications) sent directly via SES client may be silently rejected by Gmail even though SES returns success. Cognito emails work because Cognito uses its own configured identity.

### Workflow: Cross-Account Resource Access

**When:** Test/prod accounts need access to shared dev resources (S3 report buckets, etc.)

**Problem:** Test reports fail to upload to S3 bucket in dev account from test/prod accounts.

**Solution:** Add cross-account bucket policy:
```json
{
  "Sid": "CrossAccountAccess",
  "Effect": "Allow",
  "Principal": {
    "AWS": [
      "arn:aws:iam::TEST_ACCOUNT_ID:user/deploy-user",
      "arn:aws:iam::PROD_ACCOUNT_ID:user/deploy-user"
    ]
  },
  "Action": ["s3:ListBucket", "s3:PutObject", "s3:GetObject"],
  "Resource": [
    "arn:aws:s3:::bucket-name",
    "arn:aws:s3:::bucket-name/*"
  ]
}
```

### Workflow: Doppler→GitHub Sync (CI/CD Credentials)

**When:** Configuring GitHub Actions to access Doppler secrets at runtime.

**Problem:** CI/CD workflows need credentials (AWS, Linear API, etc.). Manual copying of each secret to GitHub is error-prone and creates sync drift.

**Solution:** Use Doppler runtime fetch - create a single service token that workflows use to fetch all secrets at runtime.

**Prerequisites:**
- Doppler project exists with dev/stg/prd configs
- GitHub repo accessible via `gh` CLI
- Doppler CLI authenticated (`doppler login`)

**Steps:**

1. **Create Doppler service token for the environment:**
   ```bash
   # Create token for dev config (most common for CI)
   DOPPLER_TOKEN=$(doppler configs tokens create \
     --project {project-name} \
     --config dev \
     --name github-actions \
     --plain)
   ```

2. **Set token as GitHub secret:**
   ```bash
   gh secret set DOPPLER_TOKEN \
     --repo {owner}/{repo} \
     --body "$DOPPLER_TOKEN"
   ```

3. **Verify secret is set:**
   ```bash
   gh secret list --repo {owner}/{repo} | grep DOPPLER_TOKEN
   ```

**Workflow usage pattern:**

In GitHub Actions, use the Doppler action to inject secrets:

```yaml
steps:
  - name: Fetch secrets from Doppler
    uses: dopplerhq/secrets-fetch-action@v1.2.0
    with:
      doppler-token: ${{ secrets.DOPPLER_TOKEN }}
      inject-env-vars: true

  - name: Use secrets
    run: |
      # All Doppler secrets are now environment variables
      aws s3 ls  # Uses AWS_ACCESS_KEY_ID from Doppler
```

Or use `doppler run` directly:

```yaml
steps:
  - name: Run with Doppler
    env:
      DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
    run: doppler run -- npm run deploy
```

**Benefits:**
- Single secret to manage in GitHub
- Secrets stay in sync with Doppler automatically
- New secrets in Doppler immediately available to CI
- Audit trail in Doppler for secret access

**Multiple environments:**

For staging/prod deployments, create separate tokens:

```bash
# Create tokens for each environment
doppler configs tokens create --project {project} --config dev --name gha-dev --plain
doppler configs tokens create --project {project} --config stg --name gha-stg --plain
doppler configs tokens create --project {project} --config prd --name gha-prd --plain

# Set as separate GitHub secrets
gh secret set DOPPLER_TOKEN_DEV --body "$DEV_TOKEN"
gh secret set DOPPLER_TOKEN_STG --body "$STG_TOKEN"
gh secret set DOPPLER_TOKEN_PRD --body "$PRD_TOKEN"
```

**Validation:**
```bash
# Token works
DOPPLER_TOKEN=$DOPPLER_TOKEN doppler secrets --only-names

# GitHub secret exists
gh secret list | grep DOPPLER_TOKEN
```

---

### Workflow: Test Script Configuration (Doppler)

**When:** Configuring package.json test scripts for projects using Doppler for credentials.

**Problem:** Integration and E2E tests require AWS/cloud credentials. Without proper configuration, developers must remember to prefix commands with `doppler run ...`.

**Solution:** Create paired scripts - raw scripts for CI/CD, `:local` variants for local development.

**Required scripts in package.json:**
```json
{
  "scripts": {
    "test:unit": "jest --selectProjects unit",
    "test:integration": "jest --selectProjects integration",
    "test:integration:local": "doppler run --project {project} --config dev -- npm run test:integration",
    "test:coverage": "jest --coverage",
    "test:coverage:local": "doppler run --project {project} --config dev -- jest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:local": "doppler run --project {project} --config dev -- npm run test:e2e",
    "test:all": "npm run test:unit && npm run test:integration && npm run test:e2e",
    "test:all:local": "npm run test:unit && npm run test:integration:local && npm run test:e2e:local"
  }
}
```

**Replace `{project}` with the Doppler project name** (usually matches repo name).

**Script purposes:**

| Script | Credentials | Use Case |
|--------|-------------|----------|
| `test:unit` | None needed | Always works, no external deps |
| `test:integration` | Injected by CI/CD | GitHub Actions with Doppler |
| `test:integration:local` | Via Doppler CLI | Local development |
| `test:coverage` | Injected by CI/CD | CI coverage report |
| `test:coverage:local` | Via Doppler CLI | Local coverage (unit + integration) |
| `test:e2e` | Injected by CI/CD | GitHub Actions with Doppler |
| `test:e2e:local` | Via Doppler CLI | Local development |

**Why this pattern?**
- CI/CD environments inject credentials differently (GitHub Actions Doppler integration)
- Local developers get automatic credential injection
- Clear distinction between CI and local execution
- Unit tests work everywhere without configuration

**Validation:**
```bash
# Unit tests (no credentials needed)
npm run test:unit

# Integration tests (local with Doppler)
npm run test:integration:local

# E2E tests (local with Doppler)
npm run test:e2e:local
```

## Essential Reading

**Comprehensive guide:**
- [Setup Guide](../../docs/guides/setup-guide.md) - Full 1600+ line guide

**Templates:**
- `.claude/templates/setup/` - CLAUDE.md and handoff templates

**Related skills:**
- `af-discovery-process` - Next phase after setup
- `af-testing-expertise` - For E2E infrastructure requirements

**Module system:**
- [Module Registry](../../docs/reference/module-registry.yml) - Available modules and dependencies
- [Integration Guides](../../docs/guides/integrations/) - Cross-module integration knowledge

---

**Remember:**
1. Linear team must exist before setup
2. Use templates from `.claude/templates/setup/`
3. Add project to registry for docs sync
4. Resume is automatic on failure
5. Validate before declaring success
