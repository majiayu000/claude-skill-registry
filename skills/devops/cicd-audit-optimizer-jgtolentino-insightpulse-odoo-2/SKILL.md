---
name: cicd-audit-optimizer
description: Comprehensive CI/CD and automation audit skill. Catalogs all pipelines, assesses operational health, identifies gaps, and provides prioritized recommendations for optimization. Includes error cataloging and root cause analysis framework.
---

# Skill: CI/CD Audit & Optimization

Your role is to act as a **DevOps Audit Specialist** who systematically analyzes CI/CD pipelines, automation workflows, and deployment processes to identify inefficiencies, gaps, and opportunities for improvement.

## Objective

Conduct a full audit of the current CI/CD and automation landscape to:
1. Establish a complete inventory
2. Verify operational health
3. Identify critical gaps and optimization opportunities
4. Provide strategic recommendations to increase deployment velocity and reliability

## Phase 1: Full Inventory & Scope

Document all CI/CD pipelines and adjacent automations across all services and repositories.

For each item, capture:

### Pipeline Metadata
- **Service/Repo**: Which application or repository does it belong to?
- **Description**: What is its purpose? (e.g., "Builds and deploys frontend-web to staging.")
- **Tools Used**: (e.g., Jenkins, GitHub Actions, GitLab CI, Terraform, Ansible, custom scripts)
- **Triggers**: How is it activated? (e.g., on-commit to main, nightly schedule, manual trigger)
- **Artifacts**: What does it produce? (e.g., Docker image, .jar file, Terraform plan)

### Discovery Commands

```bash
# Find all CI/CD configuration files
find . -type f \( \
  -name ".gitlab-ci.yml" -o \
  -name ".github/workflows/*.yml" -o \
  -name "Jenkinsfile" -o \
  -name "azure-pipelines.yml" -o \
  -name ".circleci/config.yml" -o \
  -name "bitbucket-pipelines.yml" \
\)

# Find all automation scripts
find . -type f \( \
  -name "deploy*.sh" -o \
  -name "build*.sh" -o \
  -name "*pipeline*" -o \
  -name "Makefile" \
\)

# Find all IaC files
find . -type f \( \
  -name "*.tf" -o \
  -name "*.tfvars" -o \
  -name "*.yaml" -path "*/ansible/*" -o \
  -name "*.yml" -path "*/ansible/*" \
\)
```

## Phase 2: Operational Health Check

For each item identified in Phase 1, assess its current operational status.

### Health Metrics

1. **Current Status**: Is it fully operational, partially failing, or disabled?

2. **Key Metrics (last 30 days)**:
   - Success/Failure Rate (%)
   - Average Runtime
   - Failure patterns (time of day, specific steps)

3. **Monitoring & Alerting**: How are we alerted if this automation fails?
   - Slack alert
   - PagerDuty
   - Email
   - No monitoring (❌ HIGH RISK)

### GitHub Actions Health Check
```bash
# Get workflow runs for last 30 days
gh run list --limit 100 --json conclusion,name,startedAt,durationMs

# Get specific workflow details
gh workflow view <workflow-name>

# Get failed runs
gh run list --status failure --limit 20
```

### Health Status Report Template

```markdown
## Pipeline Health Report

### ✅ Healthy Pipelines (>95% success rate)
- [pipeline-name]: 99.2% success, avg 3m runtime
- ...

### ⚠️ At-Risk Pipelines (80-95% success rate)
- [pipeline-name]: 87% success, avg 12m runtime
  - Common failures: Flaky integration tests
  - Alert method: Slack #ci-failures

### ❌ Failing Pipelines (<80% success rate)
- [pipeline-name]: 45% success, avg 8m runtime
  - Common failures: Timeout on npm install
  - Alert method: None (CRITICAL)
  - Action required: Investigate dependency issues

### 🚫 Disabled/Abandoned Pipelines
- [pipeline-name]: Last run 3 months ago
  - Reason: Unknown
  - Action required: Archive or re-enable
```

## Phase 3: Gap Analysis & Future Automation

Identify all gaps and opportunities to improve the automation posture.

### 1. Manual Gaps

What processes in the software delivery lifecycle (from commit to production) are still partially or fully manual?

**Common Manual Processes to Check:**
- [ ] Manual QA testing
- [ ] Manual approval gates (where automation could pre-screen)
- [ ] Running database migrations by hand
- [ ] Creating hotfixes
- [ ] Rolling back changes
- [ ] Environment provisioning
- [ ] SSL certificate renewal
- [ ] DNS updates
- [ ] Secret rotation
- [ ] Dependency updates

### 2. Pipeline Bottlenecks

**Performance Analysis:**
```bash
# Analyze GitHub Actions timing
gh run list --json durationMs,name,steps \
  | jq -r '.[] | "\(.name),\(.durationMs)"' \
  | sort -t, -k2 -rn \
  | head -20
```

**Common Bottlenecks:**
- Slow test suites (can they be parallelized?)
- Large Docker image builds (can layers be cached?)
- Sequential jobs that could run in parallel
- External API calls without timeout/retry logic

### 3. Missing Automations

**Security & Compliance:**
- [ ] Automated dependency vulnerability scanning (Dependabot, Snyk)
- [ ] SAST (Static Application Security Testing)
- [ ] DAST (Dynamic Application Security Testing)
- [ ] Secret scanning (GitGuardian, TruffleHog)
- [ ] License compliance checking

**Quality Gates:**
- [ ] Code coverage enforcement
- [ ] Performance regression testing
- [ ] Load testing
- [ ] Accessibility testing (WCAG compliance)
- [ ] Browser compatibility testing

**Operations:**
- [ ] Auto-generated release notes
- [ ] Automated rollback on failed health checks
- [ ] Automatic scaling based on load
- [ ] Cost optimization (shutdown dev/staging at night)
- [ ] Infrastructure drift detection

**Observability:**
- [ ] Automatic SLO monitoring
- [ ] Error rate alerts
- [ ] Performance monitoring (APM integration)
- [ ] Log aggregation and alerting

## Phase 4: Error Cataloging & Root Cause Analysis

### The Failure Catalog

Create a structured log of all CI/CD failures with these fields:

```json
{
  "incident_id": "INC-2025-001",
  "timestamp": "2025-11-09T14:32:00Z",
  "system_agent": "deploy-production-workflow",
  "symptom": "Deployment to production failed with 500 error",
  "full_logs": "https://github.com/org/repo/actions/runs/12345",
  "initial_triage": "Infrastructure",
  "root_cause": "ECS task definition had incorrect environment variables",
  "category": "Configuration Error",
  "fix_applied": "Updated terraform to use correct secret ARN",
  "prevention": "Added validation step to check env vars before deploy"
}
```

### Root Cause Analysis Framework

#### Step 1: Can you reproduce the failure exactly?

**NO → Intermittent failure (Infrastructure/Tools issue)**
- Look for: Resource spikes (CPU/memory), network timeouts, rate limiting, race conditions
- Tools: Check CloudWatch metrics, application logs, network traces

**YES → Consistent failure (Skill/Capability or Tools issue)**
- Proceed to Step 2

#### Step 2: Can you reproduce the failure manually?

Bypass automation. Run the exact command manually with the same permissions.

**YES, still fails → Tools/Technology problem**
- The code/config is invalid
- External API is down
- Tool version has a bug
- Fix: Address the underlying tool/code issue

**NO, works manually → Automation Skill or Infrastructure problem**
- The automation is doing something (or not doing something) differently
- Proceed to Step 3

#### Step 3: Do logs show a clear infrastructure error?

**YES → Infrastructure problem**
- Error 503: Service Unavailable
- OOMKilled (Out of Memory)
- Permission Denied / 403 Forbidden
- Connection Timeout
- Fix: Address infrastructure capacity, permissions, networking

**NO → Skill/Capability problem**
- Tool misuse (wrong parameters)
- Hallucination (invented parameters)
- Specification issue (ambiguous instructions)
- Error handling failure
- Fix: Improve automation logic, error handling, or documentation

### The 5 Whys Method

Use this for drilling down to root cause:

```
Symptom: Deploy-to-production workflow failed

Why? The terraform apply command failed
Why? Command returned 403 Forbidden from AWS
Why? IAM role credentials lacked permissions
Why? ECS task execution role was missing ec2:CreateInstance policy
Why? New "Create Instance" policy was never attached to service account

ROOT CAUSE: Missing IAM policy attachment
FIX: Attach policy to service account
PREVENTION: Add IAM policy validation step to terraform CI/CD
```

### Categorization Framework

Classify each failure into one of these categories:

**1. Skills & Capabilities (The "Brain")**
- Vague automation instructions
- Poor error handling logic
- Automation passes wrong parameters
- Missing context or dependencies

**2. Infrastructure (The "Body")**
- OOM (Out of Memory) errors
- Network timeouts
- IAM/permission issues
- Disk space exhausted
- Resource limits reached

**3. Tools & Technology (The "Tools")**
- Bug in tool version
- Flaky tests
- Inconsistent build environment
- External API downtime
- Dependency conflicts

**4. Process & People (The "Human")**
- Manual intervention caused drift
- Bad code merged to main
- Outdated documentation
- Missing code review

## Deliverable Format

### Executive Summary
- Total pipelines/automations inventoried
- Overall health score (% healthy, at-risk, failing)
- Top 3 critical gaps
- Top 3 quick wins

### Detailed Inventory
- Complete list of all CI/CD pipelines with metadata
- Health metrics for each

### Gap Analysis
Prioritized list of recommendations with:
- **Impact**: High/Medium/Low
- **Complexity**: High/Medium/Low
- **Estimated effort**: Hours/Days/Weeks
- **Priority score**: Impact × Urgency / Complexity

### Example Recommendation

```markdown
### Recommendation #1: Implement Automated Dependency Updates

**Impact**: HIGH
- Reduces security vulnerabilities
- Eliminates weekly manual dependency review meeting
- Prevents production incidents from outdated packages

**Complexity**: LOW
- Enable Dependabot in GitHub (1 config file)
- Configure auto-merge for patch versions

**Estimated Effort**: 2 hours

**Priority Score**: 9/10

**Implementation Plan**:
1. Create `.github/dependabot.yml` config
2. Enable auto-merge for patch/minor versions with passing tests
3. Configure Slack notifications for major version updates
4. Set up weekly dependency dashboard review
```

## DORA Metrics Baseline

As part of the audit, establish baseline DORA metrics:

```bash
# Deployment Frequency
gh api graphql -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      deployments(last: 100, environments: ["production"]) {
        nodes {
          createdAt
        }
      }
    }
  }
' -f owner=ORG -f repo=REPO

# Lead Time for Changes
# (Calculate time from commit to production deployment)

# Change Failure Rate
# (% of deployments that required hotfix/rollback)

# Mean Time to Recovery
# (Average time from incident detection to resolution)
```

## Tools and Commands Reference

### GitHub CLI (gh)
```bash
# List all workflows
gh workflow list

# View workflow runs
gh run list --workflow=deploy.yml --limit 50

# View failed runs
gh run list --status=failure --json conclusion,name,startedAt

# Download workflow logs
gh run view <run-id> --log
```

### GitLab CI
```bash
# Get pipeline status
curl --header "PRIVATE-TOKEN: <token>" \
  "https://gitlab.com/api/v4/projects/<id>/pipelines"

# Get failed jobs
curl --header "PRIVATE-TOKEN: <token>" \
  "https://gitlab.com/api/v4/projects/<id>/pipelines/<id>/jobs?scope=failed"
```

### Jenkins
```bash
# Get build status via API
curl -s "http://jenkins/job/<job-name>/lastBuild/api/json" \
  | jq '.result'

# Get failed builds
curl -s "http://jenkins/job/<job-name>/api/json" \
  | jq '.builds[] | select(.result == "FAILURE")'
```

## Success Criteria

This audit is complete when:
- [ ] 100% of CI/CD pipelines are documented
- [ ] Health metrics available for all active pipelines
- [ ] All failures from last 30 days are cataloged
- [ ] Root cause identified for top 10 most frequent failures
- [ ] Prioritized recommendations list created
- [ ] DORA baseline metrics established
- [ ] Executive summary delivered
