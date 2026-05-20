---
name: gitlab-skill
description: The model must apply when tasks involve .gitlab-ci.yml configuration, GitLab Flavored Markdown (GLFM) syntax, gitlab-ci-local testing, CI/CD pipeline optimization, GitLab CI Steps composition, Docker-in-Docker workflows, or GitLab documentation creation. Triggers include modifying pipelines, writing GitLab README/Wiki content, debugging CI jobs locally, implementing caching strategies, or configuring release workflows.
---

# GitLab Skill

## Identity

GitLab CI/CD pipeline configuration, GitLab Flavored Markdown documentation, gitlab-ci-local testing expertise. Covers .gitlab-ci.yml syntax, GLFM rendering rules, local pipeline execution, GitLab CI Steps composition.

## Capability Domains

### Domain 1: CI/CD Pipeline Configuration

The model must apply for .gitlab-ci.yml creation, modification, optimization.

**TRIGGERS:**

- Task involves .gitlab-ci.yml file
- Pipeline performance optimization required
- Caching strategy implementation needed
- Conditional job execution configuration
- Secret/environment variable management
- Docker-in-Docker (dind) workflow setup
- Pipeline job failure troubleshooting
- GitLab CI Steps composition for reusable workflow units

**CONSTRAINTS:**

- The model must validate .gitlab-ci.yml syntax before committing
- The model must implement caching for dependencies to minimize build time
- The model must use masked variables for sensitive data
- The model must define timeout limits for all jobs
- The model must test pipelines locally with gitlab-ci-local before pushing
- The model must use .gitlab-ci.yml include feature for modular configurations
- The model must optimize job dependencies to prevent unnecessary execution
- The model must implement comprehensive testing at each pipeline stage

**REFERENCES:**

- [Pipeline Optimization Guide](./references/pipeline-optimization.md) - Caching strategies, job parallelization, Docker optimization patterns
- [Common Patterns](./references/common-patterns.md) - Reusable configuration examples
- [GitLab CI Steps Documentation](./references/ci-steps/index.md) - Steps feature overview, syntax, implementation details

### Domain 2: GitLab Flavored Markdown (GLFM)

The model must apply for GitLab documentation creation using GLFM syntax.

**TRIGGERS:**

- Writing README files for GitLab projects
- Creating GitLab Wiki pages
- API documentation with GitLab syntax highlighting
- User guides requiring collapsible sections
- Process flow diagrams with Mermaid
- Changelogs with GitLab issue/MR references

**GLFM_SYNTAX_FEATURES:**

- Alert blocks: `[!note]`, `[!tip]`, `[!important]`, `[!caution]`, `[!warning]`
- Collapsible sections: `<details><summary>` syntax
- Mermaid diagrams for visualizations
- Task lists with completion tracking
- GitLab references: #issue, !MR, @user
- Table of contents generation
- Math expressions support
- Color chips for design documentation

**CRITICAL_SYNTAX_RULES:**

The model must enforce these non-negotiable GLFM rendering requirements:

1. Alert types MUST be lowercase: `[!note]` not `[!Note]` or `[!NOTE]`
2. `<details><summary>` MUST be single line: `<details><summary>Text</summary>` not multi-line
3. No markdown syntax inside `<summary>` tags - use HTML equivalents (`<code>`, `<strong>`)
4. The model must validate rendering with validate-glfm.py script before finalizing

**REFERENCE:**

[GLFM Syntax Reference](./references/glfm-syntax.md) - Complete syntax guide, examples, common mistakes

### Domain 3: Local Pipeline Testing

The model must apply for local GitLab CI/CD pipeline execution with gitlab-ci-local.

**TRIGGERS:**

- Testing .gitlab-ci.yml changes before push
- Debugging pipeline job failures locally
- Validating release workflows without actual release creation
- Testing specific jobs/stages in isolation
- Verifying conditional job execution logic
- Checking artifact generation and dependencies

**SETUP_PROCEDURE:**

```bash
# 1. Install gitlab-ci-local globally
npm install -g gitlab-ci-local

# 2. Configure authentication tokens
# Edit $HOME/.gitlab-ci-local/variables.yml

# 3. Set project-specific variables
# Create .gitlab-ci-local-variables.yml in project root

# 4. Execute job locally
gitlab-ci-local <job-name>
```

**COMMON_OPERATIONS:**

```bash
gitlab-ci-local --list                    # List all jobs
gitlab-ci-local --preview                 # Preview parsed configuration
gitlab-ci-local --stage test              # Run specific stage
gitlab-ci-local --needs release           # Run with dependencies
gitlab-ci-local --timestamps job-name     # Debug with timestamps
```

**REFERENCE:**

[GitLab CI Local Guide](./references/gitlab-ci-local-guide.md) - Setup, authentication, troubleshooting, examples

### Domain 4: GitLab CLI (glab)

The model must apply for GitLab repository and pipeline operations via the `glab` CLI.

**TRIGGERS:**

- Monitoring pipeline status from terminal
- Linting CI configuration before push
- Listing or inspecting pipelines and jobs
- Non-interactive CI/CD operations in scripts or automation

**CRITICAL: AVOID INTERACTIVE COMMANDS**

The `glab ci view` command launches an interactive TUI. Use non-interactive alternatives:

```bash
# INTERACTIVE (avoid in automation):
glab ci view                    # Opens interactive TUI

# NON-INTERACTIVE alternatives:
glab ci status --compact        # Quick pass/fail status
glab ci get                     # Pipeline details as text
glab ci list --per-page 5       # Recent pipelines table
```

**LINTING CI CONFIGURATION:**

```bash
# Validate .gitlab-ci.yml syntax via GitLab API
glab ci lint

# Include job list in output
glab ci lint --include-jobs

# Simulate pipeline creation (dry run)
glab ci lint --dry-run --ref main
```

The lint command sends the local `.gitlab-ci.yml` to GitLab API for validation. This resolves `include:` directives from the remote repository, so included files must be committed and pushed for accurate validation.

**PIPELINE MONITORING:**

```bash
# List recent pipelines with status
glab ci list --per-page 5

# Get current branch pipeline details
glab ci get

# Quick status check (exits non-zero on failure)
glab ci status --compact
```

**Output from `glab ci get`:**

```text
# Pipeline:
id:       1254276
status:   success
source:   push
ref:      main
sha:      c3f955e...
yaml Errors:

# Jobs:
job_name:  success
```

**Output from `glab ci list`:**

```text
State            IID        Ref     Created
(success)    #1254276   (#4)   main    (1 minute ago)
(failed)     #1254271   (#3)   main    (15 minutes ago)
```

**COMMON WORKFLOW:**

```bash
# 1. Validate before commit
glab ci lint

# 2. Commit and push
git add . && git commit -m "message" && git push

# 3. Monitor pipeline
glab ci list --per-page 3
glab ci status --compact

# 4. On failure, get details
glab ci get
```

**REFERENCE:**

Run `glab ci --help` for full subcommand list. Each subcommand supports `--help` for detailed options.

## Validation Checklist

### CI/CD Pipeline Validation

The model must verify before committing .gitlab-ci.yml:

- [ ] Syntax validated against GitLab CI schema
- [ ] Jobs and stages use descriptive names, logical organization
- [ ] Caching configured for dependencies
- [ ] Secrets masked, environment variables secured
- [ ] Conditional execution prevents unnecessary resource consumption
- [ ] Artifacts configured with appropriate expiration
- [ ] Timeout limits defined per job
- [ ] Pipeline tested locally with gitlab-ci-local
- [ ] Pipeline architecture documented

### GLFM Documentation Validation

The model must verify before committing GLFM files:

- [ ] Alert blocks use lowercase syntax: `[!note]`, `[!tip]`, `[!important]`, `[!caution]`, `[!warning]`
- [ ] Collapsible sections use single-line `<details><summary>` format
- [ ] No markdown syntax in `<summary>` tags
- [ ] Mermaid diagrams used for process flows
- [ ] Table of contents present for documents >100 lines
- [ ] GitLab references used: #issue, !MR, @user
- [ ] Code blocks have language specifiers
- [ ] Heading hierarchy consistent (no skipped levels)
- [ ] Rendered output validated with validate-glfm.py

### Local Testing Validation

The model must verify local test environment:

- [ ] gitlab-ci-local installed and accessible
- [ ] Authentication tokens configured in $HOME/.gitlab-ci-local/variables.yml
- [ ] Project variables defined in .gitlab-ci-local-variables.yml
- [ ] Jobs execute locally without errors
- [ ] Artifacts present in .gitlab-ci-local/artifacts/
- [ ] Configuration validated with `--preview` flag

## Utility Scripts

### validate-glfm.py

Python script validates GLFM rendering via GitLab Markdown API.

**Usage:**

```bash
# Validate markdown file
uv run --with requests ./scripts/validate-glfm.py --file README.md

# Validate inline markdown
uv run --with requests ./scripts/validate-glfm.py --markdown "> [!note]\n> Test alert"

# Save rendered HTML to file
uv run --with requests ./scripts/validate-glfm.py --file test.md --output rendered.html
```

**Capabilities:**

- Automatic GITLAB_TOKEN environment variable loading
- File or inline markdown input
- HTML output to stdout or file
- Verbose debugging mode (`--verbose`)
- Error handling with retry logic

## Reference Documentation

**CI/CD Pipeline References:**

- [pipeline-optimization.md](./references/pipeline-optimization.md) - Performance optimization, caching strategies, job parallelization, Docker patterns
- [common-patterns.md](./references/common-patterns.md) - Reusable .gitlab-ci.yml configuration patterns

**GLFM References:**

- [glfm-syntax.md](./references/glfm-syntax.md) - Complete syntax guide, examples, anti-patterns

**gitlab-ci-local References:**

- [gitlab-ci-local-guide.md](./references/gitlab-ci-local-guide.md) - Setup, authentication, troubleshooting, real-world examples

**GitLab CI Steps References:**

- [ci-steps/index.md](./references/ci-steps/index.md) - Overview, navigation hub
- [ci-steps/steps-overview.md](./references/ci-steps/steps-overview.md) - Technical reference, syntax, specification, capabilities
- [ci-steps/examples.md](./references/ci-steps/examples.md) - Real-world usage patterns, implementation examples
- [ci-steps/step-runner-architecture.md](./references/ci-steps/step-runner-architecture.md) - Implementation details, architecture, step-runner execution engine internals

## Execution Protocol

The model must follow this sequence when gitlab-skill applies:

1. **Update documentation reference** (first step on skill activation):

   ```bash
   uv run scripts/sync-gitlab-docs.py --working-dir .
   ```

   - Updates GitLab CI documentation from official repository
   - Respects 3-day cooldown (successful runs only)
   - Use `--force` flag to bypass cooldown if needed
   - Creates/updates Documentation Index in this SKILL.md file
   - Lock file: `.sync-gitlab-docs.lock` (gitignored)

2. Identify domain: CI/CD configuration, GLFM documentation, or local testing
3. Load domain-specific reference files for technical specifications
4. Apply domain constraints and validation rules
5. Execute domain-specific validation checklist
6. Validate output using appropriate tooling (gitlab-ci-local or validate-glfm.py)

## Quick Start Paths

**IF task involves CI/CD pipeline:**

1. Load [pipeline-optimization.md](./references/pipeline-optimization.md)
2. Review [common-patterns.md](./references/common-patterns.md) for reusable configurations
3. Test locally with gitlab-ci-local before pushing

**IF task involves GLFM documentation:**

1. Load [glfm-syntax.md](./references/glfm-syntax.md)
2. Apply CRITICAL_SYNTAX_RULES during writing
3. Validate rendering with validate-glfm.py script

**IF task involves local pipeline testing:**

1. Load [gitlab-ci-local-guide.md](./references/gitlab-ci-local-guide.md)
2. Verify authentication configuration in $HOME/.gitlab-ci-local/
3. Execute pipeline locally, verify artifacts in .gitlab-ci-local/artifacts/

## Documentation Index

```text
ci/
  ├── [Get started with GitLab CI/CD](./references/ci/_index.md)
      Build and test your application.
  ├── [Debugging CI/CD pipelines](./references/ci/debugging.md)
      Configuration validation, warnings, errors, and troubleshooting.
  ├── caching/
    ├── [Caching in GitLab CI/CD](./references/ci/caching/_index.md)
    ├── [CI/CD caching examples](./references/ci/caching/examples.md)
  ├── chatops/
    ├── [GitLab ChatOps](./references/ci/chatops/_index.md)
  ├── ci_cd_for_external_repos/
    ├── [GitLab CI/CD for external repositories](./references/ci/ci_cd_for_external_repos/_index.md)
        GitHub, Bitbucket, external sources, mirroring, and cross-platform.
    ├── [Using GitLab CI/CD with a Bitbucket Cloud repository](./references/ci/ci_cd_for_external_repos/bitbucket_integration.md)
        Connect your Bitbucket Cloud repository to GitLab CI/CD.
    ├── [External commit statuses](./references/ci/ci_cd_for_external_repos/external_commit_statuses.md)
        How external CI/CD systems integrate with GitLab pipelines using commit statuses.
    ├── [Using GitLab CI/CD with a GitHub repository](./references/ci/ci_cd_for_external_repos/github_integration.md)
        Connect your GitHub repository to GitLab CI/CD.
  ├── cloud_deployment/
    ├── [Deploy to AWS from GitLab CI/CD](./references/ci/cloud_deployment/_index.md)
        Deploy applications from GitLab CI/CD to AWS, including ECS and EC2, by using GitLab-provided Docker images and CloudFormation templates.
    ├── [Use GitLab CI/CD to deploy to Heroku](./references/ci/cloud_deployment/heroku.md)
        Deploy a GitLab project to Heroku by using GitLab CI/CD.
    ├── ecs/
      ├── [Deploy to Amazon Elastic Container Service](./references/ci/cloud_deployment/ecs/deploy_to_aws_ecs.md)
          Deploy a GitLab project to Amazon ECS. Containerize the application and set up continuous deployment, review apps, and security testing.
  ├── cloud_services/
    ├── [Connect to cloud services](./references/ci/cloud_services/_index.md)
    ├── aws/
      ├── [Configure OpenID Connect in AWS to retrieve temporary credentials](./references/ci/cloud_services/aws/_index.md)
    ├── azure/
      ├── [Configure OpenID Connect in Azure to retrieve temporary credentials](./references/ci/cloud_services/azure/_index.md)
    ├── google_cloud/
      ├── [Configure OpenID Connect with GCP Workload Identity Federation](./references/ci/cloud_services/google_cloud/_index.md)
  ├── components/
    ├── [CI/CD components](./references/ci/components/_index.md)
        Reusable, versioned CI/CD components for pipelines.
    ├── [CI/CD component examples](./references/ci/components/examples.md)
  ├── docker/
    ├── [Docker integration](./references/ci/docker/_index.md)
    ├── [Authenticate with registry in Docker-in-Docker](./references/ci/docker/authenticate_registry.md)
    ├── [Use Buildah to build multi-platform images](./references/ci/docker/buildah_rootless_multi_arch.md)
    ├── [Tutorial: Use Buildah in a rootless container with GitLab Runner Operator on OpenShift](./references/ci/docker/buildah_rootless_tutorial.md)
    ├── [Troubleshooting Docker Build](./references/ci/docker/docker_build_troubleshooting.md)
    ├── [Make Docker-in-Docker builds faster with Docker layer caching](./references/ci/docker/docker_layer_caching.md)
    ├── [Build Docker images with BuildKit](./references/ci/docker/using_buildkit.md)
    ├── [Use Docker to build Docker images](./references/ci/docker/using_docker_build.md)
    ├── [Run your CI/CD jobs in Docker containers](./references/ci/docker/using_docker_images.md)
        Learn how to run your CI/CD jobs in Docker containers hosted on dedicated CI/CD build servers or your local machine.
    ├── [Use kaniko to build Docker images (removed)](./references/ci/docker/using_kaniko.md)
  ├── environments/
    ├── [Environments](./references/ci/environments/_index.md)
        Environments, variables, dashboards, and review apps.
    ├── [Configure Kubernetes deployments (deprecated)](./references/ci/environments/configure_kubernetes_deployments.md)
    ├── [Deployment approvals](./references/ci/environments/deployment_approvals.md)
        Require approvals prior to deploying to a Protected Environment
    ├── [Deployment safety](./references/ci/environments/deployment_safety.md)
    ├── [Deployments](./references/ci/environments/deployments.md)
        Deployments, rollbacks, safety, and approvals.
    ├── [Environments Dashboard](./references/ci/environments/environments_dashboard.md)
        Monitor environments across multiple projects, including latest commits, pipeline status, and deployment times.
    ├── [Track deployments of an external deployment tool](./references/ci/environments/external_deployment_tools.md)
    ├── [Incremental rollouts with GitLab CI/CD](./references/ci/environments/incremental_rollouts.md)
        Kubernetes, CI/CD, risk mitigation, and deployment.
    ├── [Dashboard for Kubernetes](./references/ci/environments/kubernetes_dashboard.md)
    ├── [Protected environments](./references/ci/environments/protected_environments.md)
  ├── examples/
    ├── [GitLab CI/CD examples](./references/ci/examples/_index.md)
    ├── [Testing PHP projects](./references/ci/examples/php.md)
    ├── [Publish npm packages to the GitLab package registry using semantic-release](./references/ci/examples/semantic-release.md)
    ├── deployment/
      ├── [Using Dpl as a deployment tool](./references/ci/examples/deployment/_index.md)
      ├── [Running Composer and npm scripts with deployment via SCP in GitLab CI/CD](./references/ci/examples/deployment/composer-npm-deploy.md)
  ├── gitlab_google_cloud_integration/
    ├── [GitLab and Google Cloud integration](./references/ci/gitlab_google_cloud_integration/_index.md)
        Cloud services and Kubernetes deployments.
  ├── inputs/
    ├── [CI/CD inputs](./references/ci/inputs/_index.md)
    ├── [CI/CD input examples](./references/ci/inputs/examples.md)
  ├── interactive_web_terminal/
    ├── [Interactive web terminals](./references/ci/interactive_web_terminal/_index.md)
  ├── jobs/
    ├── [CI/CD Jobs](./references/ci/jobs/_index.md)
        Configuration, rules, caching, artifacts, and logs.
    ├── [GitLab CI/CD job token](./references/ci/jobs/ci_job_token.md)
    ├── [Fine-grained permissions for CI/CD job tokens](./references/ci/jobs/fine_grained_permissions.md)
    ├── [Job artifacts](./references/ci/jobs/job_artifacts.md)
    ├── [Troubleshooting job artifacts](./references/ci/jobs/job_artifacts_troubleshooting.md)
    ├── [Control how jobs run](./references/ci/jobs/job_control.md)
    ├── [Job execution flow](./references/ci/jobs/job_execution.md)
        Job execution steps.
    ├── [CI/CD job logs](./references/ci/jobs/job_logs.md)
    ├── [Specify when jobs run with `rules`](./references/ci/jobs/job_rules.md)
    ├── [Troubleshooting jobs](./references/ci/jobs/job_troubleshooting.md)
    ├── [Using SSH keys with GitLab CI/CD](./references/ci/jobs/ssh_keys.md)
  ├── migration/
    ├── [Migrate from Bamboo](./references/ci/migration/bamboo.md)
    ├── [Migrate from CircleCI](./references/ci/migration/circleci.md)
    ├── [Migrate from GitHub Actions](./references/ci/migration/github_actions.md)
    ├── [Migrate from Jenkins](./references/ci/migration/jenkins.md)
    ├── [Plan a migration from another tool to GitLab CI/CD](./references/ci/migration/plan_a_migration.md)
        Migrate from Jenkins, GitHub Actions, and others.
    ├── [Migrate from TeamCity](./references/ci/migration/teamcity.md)
    ├── examples/
      ├── [Migrate a Maven build from Jenkins to GitLab CI/CD](./references/ci/migration/examples/jenkins-maven.md)
  ├── mobile_devops/
    ├── [Mobile DevOps](./references/ci/mobile_devops/_index.md)
    ├── [Tutorial: Build Android apps with GitLab Mobile DevOps](./references/ci/mobile_devops/mobile_devops_tutorial_android.md)
    ├── [Tutorial: Build iOS apps with GitLab Mobile DevOps](./references/ci/mobile_devops/mobile_devops_tutorial_ios.md)
  ├── pipeline_editor/
    ├── [Pipeline editor](./references/ci/pipeline_editor/_index.md)
  ├── pipeline_security/
    ├── [Pipeline security](./references/ci/pipeline_security/_index.md)
        Secrets management, job tokens, secure files, and cloud security.
    ├── slsa/
      ├── [GitLab SLSA](./references/ci/pipeline_security/slsa/_index.md)
      ├── [SLSA provenance specification](./references/ci/pipeline_security/slsa/provenance_v1.md)
  ├── pipelines/
    ├── [CI/CD pipelines](./references/ci/pipelines/_index.md)
        Configuration, automation, stages, schedules, and efficiency.
    ├── [Compute minutes](./references/ci/pipelines/compute_minutes.md)
        Calculations, quotas, purchase information.
    ├── [Compute usage for GitLab-hosted runners on GitLab Dedicated](./references/ci/pipelines/dedicated_hosted_runner_compute_minutes.md)
        Compute minutes, usage tracking, quota management for GitLab-hosted runners on GitLab Dedicated.
    ├── [Downstream pipelines](./references/ci/pipelines/downstream_pipelines.md)
    ├── [Troubleshooting downstream pipelines](./references/ci/pipelines/downstream_pipelines_troubleshooting.md)
    ├── [Compute usage for instance runners](./references/ci/pipelines/instance_runner_compute_minutes.md)
        Compute minutes, purchasing, usage tracking, quota management for instance runners on GitLab.com and GitLab Self-Managed.
    ├── [Merge request pipelines](./references/ci/pipelines/merge_request_pipelines.md)
        Learn how to use merge request pipelines in GitLab CI/CD to test changes efficiently, run targeted jobs, and improve code quality before merging.
    ├── [Merge trains](./references/ci/pipelines/merge_trains.md)
        Use merge trains to queue merge requests and prevent branch conflicts in GitLab CI/CD.
    ├── [Merged results pipelines](./references/ci/pipelines/merged_results_pipelines.md)
    ├── [Troubleshooting merge request pipelines](./references/ci/pipelines/mr_pipeline_troubleshooting.md)
    ├── [Pipeline architecture](./references/ci/pipelines/pipeline_architectures.md)
    ├── [Pipeline efficiency](./references/ci/pipelines/pipeline_efficiency.md)
    ├── [Types of pipelines](./references/ci/pipelines/pipeline_types.md)
    ├── [Scheduled pipelines](./references/ci/pipelines/schedules.md)
    ├── [Customize pipeline configuration](./references/ci/pipelines/settings.md)
  ├── quick_start/
    ├── [Tutorial: Create and run your first GitLab CI/CD pipeline](./references/ci/quick_start/_index.md)
    ├── [Tutorial: Create a complex pipeline](./references/ci/quick_start/tutorial.md)
  ├── resource_groups/
    ├── [Resource group](./references/ci/resource_groups/_index.md)
        Control the job concurrency in GitLab CI/CD
  ├── review_apps/
    ├── [Review apps](./references/ci/review_apps/_index.md)
        Set up and use review apps to create temporary environments for testing changes before merging.
  ├── runners/
    ├── [Runners](./references/ci/runners/_index.md)
        Configuration and job execution.
    ├── [Configuring runners](./references/ci/runners/configure_runners.md)
        Set timeouts, protect sensitive information, control behavior with tags and variables, and configure artifact and cache settings of your GitLab Runner.
    ├── [Using Git submodules with GitLab CI/CD](./references/ci/runners/git_submodules.md)
    ├── [Long polling](./references/ci/runners/long_polling.md)
    ├── [Migrating to the new runner registration workflow](./references/ci/runners/new_creation_workflow.md)
    ├── [Provision runners in Google Cloud Compute Engine](./references/ci/runners/provision_runners_google_cloud.md)
    ├── [Runner fleet dashboard for administrators](./references/ci/runners/runner_fleet_dashboard.md)
    ├── [Runner fleet dashboard for groups](./references/ci/runners/runner_fleet_dashboard_groups.md)
    ├── [Manage runners](./references/ci/runners/runners_scope.md)
        Learn about the types of runners, their availability, and how to manage them.
    ├── hosted_runners/
      ├── [GitLab-hosted runners](./references/ci/runners/hosted_runners/_index.md)
      ├── [GPU-enabled hosted runners](./references/ci/runners/hosted_runners/gpu_enabled.md)
      ├── [Hosted runners on Linux](./references/ci/runners/hosted_runners/linux.md)
      ├── [Hosted runners on macOS](./references/ci/runners/hosted_runners/macos.md)
      ├── [Hosted runners on Windows](./references/ci/runners/hosted_runners/windows.md)
  ├── secrets/
    ├── [Use external secrets in CI/CD](./references/ci/secrets/_index.md)
    ├── [Use AWS Secrets Manager secrets in GitLab CI/CD](./references/ci/secrets/aws_secrets_manager.md)
    ├── [Use Azure Key Vault secrets in GitLab CI/CD](./references/ci/secrets/azure_key_vault.md)
    ├── [Tutorial: Update HashiCorp Vault configuration to use ID Tokens](./references/ci/secrets/convert-to-id-tokens.md)
    ├── [Tutorial: Use Fortanix Data Security Manager (DSM) with GitLab](./references/ci/secrets/fortanix_dsm_integration.md)
    ├── [Use GCP Secret Manager secrets in GitLab CI/CD](./references/ci/secrets/gcp_secret_manager.md)
    ├── [Use HashiCorp Vault secrets in GitLab CI/CD](./references/ci/secrets/hashicorp_vault.md)
    ├── [Tutorial: Authenticating and reading secrets with HashiCorp Vault](./references/ci/secrets/hashicorp_vault_tutorial.md)
    ├── [OpenID Connect (OIDC) Authentication Using ID Tokens](./references/ci/secrets/id_token_authentication.md)
    ├── secrets_manager/
      ├── [GitLab Secrets Manager](./references/ci/secrets/secrets_manager/_index.md)
  ├── secure_files/
    ├── [Project-level secure files](./references/ci/secure_files/_index.md)
  ├── services/
    ├── [Services](./references/ci/services/_index.md)
    ├── [Use GitLab as a microservice](./references/ci/services/gitlab.md)
    ├── [Using MySQL](./references/ci/services/mysql.md)
    ├── [Using PostgreSQL](./references/ci/services/postgres.md)
    ├── [Using Redis](./references/ci/services/redis.md)
  ├── steps/
    ├── [CI/CD steps](./references/ci/steps/_index.md)
  ├── test_cases/
    ├── [Test cases](./references/ci/test_cases/_index.md)
        Test cases in GitLab can help your teams create testing scenarios in their existing development platform.
  ├── testing/
    ├── [Test with GitLab CI/CD](./references/ci/testing/_index.md)
        Generate test reports, code quality analysis, and security scans that display in merge requests.
    ├── [Accessibility testing](./references/ci/testing/accessibility_testing.md)
    ├── [Browser Performance Testing](./references/ci/testing/browser_performance_testing.md)
    ├── [Code Quality](./references/ci/testing/code_quality.md)
    ├── [Configure CodeClimate-based Code Quality scanning (deprecated)](./references/ci/testing/code_quality_codeclimate_scanning.md)
    ├── [Troubleshooting Code Quality](./references/ci/testing/code_quality_troubleshooting.md)
    ├── [Fail Fast Testing](./references/ci/testing/fail_fast_testing.md)
        Run only relevant RSpec tests using the fail-fast template to get faster feedback on code changes.
    ├── [Load Performance Testing](./references/ci/testing/load_performance_testing.md)
        Measure how code changes affect application performance using k6 load tests to assess response times and throughput under load.
    ├── [Metrics reports](./references/ci/testing/metrics_reports.md)
        Track and compare performance, memory, and custom metrics.
    ├── [Unit test report examples](./references/ci/testing/unit_test_report_examples.md)
    ├── [Unit test reports](./references/ci/testing/unit_test_reports.md)
        View and debug unit test results without searching through job logs.
    ├── code_coverage/
      ├── [Code coverage](./references/ci/testing/code_coverage/_index.md)
      ├── [Cobertura coverage report](./references/ci/testing/code_coverage/cobertura.md)
      ├── [JaCoCo coverage report](./references/ci/testing/code_coverage/jacoco.md)
  ├── triggers/
    ├── [Trigger pipelines with the API](./references/ci/triggers/_index.md)
  ├── variables/
    ├── [GitLab CI/CD variables](./references/ci/variables/_index.md)
        Configuration, usage, and security.
    ├── [Use CI/CD variables in job scripts](./references/ci/variables/job_scripts.md)
        Configuration, usage, and security.
    ├── [Predefined CI/CD variables reference](./references/ci/variables/predefined_variables.md)
    ├── [Troubleshooting CI/CD variables](./references/ci/variables/variables_troubleshooting.md)
    ├── [Where variables can be used](./references/ci/variables/where_variables_can_be_used.md)
        GitLab CI/CD variable usage and expansion across different environments.
  ├── yaml/
    ├── [CI/CD YAML syntax reference](./references/ci/yaml/_index.md)
        Pipeline configuration keywords, syntax, examples, and inputs.
    ├── [GitLab CI/CD artifacts reports types](./references/ci/yaml/artifacts_reports.md)
        Artifact report types for test results, security scans, code quality checks, and performance metrics.
    ├── [Deprecated keywords](./references/ci/yaml/deprecated_keywords.md)
    ├── [CI/CD expressions](./references/ci/yaml/expressions.md)
    ├── [Use CI/CD configuration from other files](./references/ci/yaml/includes.md)
        Use the `include` keyword to extend your CI/CD configuration with content from other YAML files.
    ├── [Validate GitLab CI/CD configuration](./references/ci/yaml/lint.md)
        Use the GitLab CI Lint tool to validate CI/CD configuration and simulate pipelines to find errors before jobs run.
    ├── [Matrix expressions in GitLab CI/CD](./references/ci/yaml/matrix_expressions.md)
    ├── [Make jobs start earlier with `needs`](./references/ci/yaml/needs.md)
    ├── [Scripts and job logs](./references/ci/yaml/script.md)
    ├── [Troubleshooting scripts and job logs](./references/ci/yaml/script_troubleshooting.md)
    ├── [Use Sigstore for keyless signing and verification](./references/ci/yaml/signing_examples.md)
    ├── [GitLab CI/CD `workflow` keyword](./references/ci/yaml/workflow.md)
    ├── [Optimize GitLab CI/CD configuration files](./references/ci/yaml/yaml_optimization.md)
        Use YAML anchors, !reference tags, and the `extends` keyword to reduce CI/CD configuration file complexity.
```

