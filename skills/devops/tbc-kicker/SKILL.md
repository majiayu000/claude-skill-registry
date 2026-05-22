---
name: TBC Kicker - GitLab CI/CD Generator
description: This skill should be used when the user asks to "generate gitlab-ci.yml", "create GitLab CI pipeline", "configure GitLab CI/CD", "use To-Be-Continuous templates", "setup TBC templates", "create CI/CD for Python/Node/Go/Java project", "configure Docker build in GitLab", "setup Kubernetes deployment in GitLab", "add SonarQube to GitLab CI", "configure Terraform with GitLab", or mentions "TBC", "To-Be-Continuous", "Kicker", or needs help selecting CI/CD templates for their project.
version: 1.1.0
---

# TBC Kicker - GitLab CI/CD Configuration Wizard

This skill guides users through generating `.gitlab-ci.yml` files using the To-Be-Continuous (TBC) framework, replicating the exact workflow of the Kicker web wizard.

## Overview

TBC Kicker is an interactive 8-step wizard that generates GitLab CI/CD configurations by combining 50 modular templates across 8 categories:

| Category | Count | Selection | Description |
|----------|-------|-----------|-------------|
| Build | 15 | Single | Programming language/framework |
| Code Analysis | 7 | Multiple | Security, linting, SAST |
| Packaging | 3 | Single | Container/package builds |
| Infrastructure | 1 | Single | Terraform IaC |
| Deployment | 11 | Single | Cloud/K8s deployment |
| Acceptance | 10 | Multiple | E2E/API testing |
| Other | 3 | Multiple | Misc utilities |

## Wizard Workflow

### Step 0: Configure Global Options

Before template selection, configure these options:

#### Configuration Mode
- **Basic**: Show only essential variables
- **Advanced**: Show all configuration variables including advanced ones

#### Include Mode
| Mode | Syntax | Use Case |
|------|--------|----------|
| `component` | `$CI_SERVER_FQDN/path/template@version` | GitLab 16.0+ (recommended) |
| `project` | `project: "path"` + `ref` + `file` | Self-hosted GitLab |
| `remote` | `https://host/path/-/raw/version/file` | External GitLab |

#### Version Mode
| Mode | Example | Updates | Stability |
|------|---------|---------|-----------|
| `major` | `@7` | Auto major | Least stable |
| `minor` | `@7.5` | Auto patch | Recommended |
| `full` | `@7.5.2` | None | Most stable |

#### Additional Options
- **With stages**: Include custom stages section
- **GitLab Host**: Custom host for remote mode

### Step 1: Build (Language)

Select ONE build template or "none":

| Template | Prefix | Description |
|----------|--------|-------------|
| Angular | `NG_` | Angular CLI projects |
| Bash | `BASH_` | Shell scripts with ShellCheck/Bats |
| DBT | `DBT_` | Data Build Tool |
| GitLab Package | `GLPKG_` | Generic package publishing |
| Go | `GO_` | Golang applications |
| Gradle | `GRADLE_` | Java/Kotlin with Gradle |
| GNU Make | `MAKE_` | Makefile-based builds |
| Maven | `MAVEN_` | Java with Maven |
| MkDocs | `MKD_` | Documentation sites |
| Node.js | `NODE_` | npm/yarn/pnpm projects |
| PHP | `PHP_` | PHP with Composer |
| pre-commit | `PRE_COMMIT_` | Pre-commit hooks |
| Python | `PYTHON_` | Python with pip/poetry |
| Scala/SBT | `SBT_` | Scala applications |
| Sphinx | `SPHINX_` | Sphinx documentation |

### Step 2: Code Analysis

Select MULTIPLE analysis templates:

| Template | Prefix | Description |
|----------|--------|-------------|
| DefectDojo | `DEFECTDOJO_` | Security report aggregation |
| Dependency Track | `DEPTRACK_` | SBOM & vulnerability tracking |
| Gitleaks | `GITLEAKS_` | Secret detection |
| MobSF | `MOBSF_` | Mobile security |
| SonarQube | `SONAR_` | Code quality & security |
| Spectral | `SPECTRAL_` | OpenAPI/AsyncAPI linting |
| SQLFluff | `SQLFLUFF_` | SQL linting |

### Step 3: Packaging

Select ONE packaging template or "none":

| Template | Prefix | Description |
|----------|--------|-------------|
| Cloud Native Buildpacks | `CNB_` | Paketo buildpacks |
| Docker | `DOCKER_` | Dockerfile builds (kaniko/buildah/dind) |
| Source-to-Image | `S2I_` | OpenShift S2I |

### Step 4: Infrastructure

Select ONE infrastructure template or "none":

| Template | Prefix | Description |
|----------|--------|-------------|
| Terraform | `TF_` | Infrastructure as Code |

### Step 5: Deployment

Select ONE deployment template or "none":

| Template | Prefix | Description |
|----------|--------|-------------|
| Ansible | `ANSIBLE_` | Configuration management |
| AWS | `AWS_` | Amazon Web Services |
| Azure | `AZURE_` | Microsoft Azure |
| Cloud Foundry | `CF_` | Cloud Foundry PaaS |
| Docker Compose | `DCMP_` | Docker Compose/Stack |
| Google Cloud | `GCLOUD_` | Google Cloud Platform |
| Helm | `HELM_` | Kubernetes Helm charts |
| Helmfile | `HELMFILE_` | Helmfile deployments |
| Kubernetes | `K8S_` | kubectl deployments |
| OpenShift | `OS_` | OpenShift deployments |
| S3 | `S3_` | S3-compatible storage |

### Step 6: Acceptance Tests

Select MULTIPLE acceptance test templates:

| Template | Prefix | Description |
|----------|--------|-------------|
| Bruno | `BRUNO_` | API testing |
| Cypress | `CYPRESS_` | E2E web testing |
| Hurl | `HURL_` | HTTP testing |
| k6 | `K6_` | Load testing |
| Lighthouse | `LHCI_` | Performance testing |
| Playwright | `PLAYWRIGHT_` | E2E testing |
| Postman | `POSTMAN_` | API testing |
| Puppeteer | `PUPPETEER_` | Browser automation |
| Robot Framework | `ROBOT_` | Test automation |
| TestSSL | `TESTSSL_` | TLS/SSL testing |

### Step 7: Other Templates

Select MULTIPLE utility templates:

| Template | Prefix | Description |
|----------|--------|-------------|
| GitLab Butler | `BUTLER_` | Project cleanup |
| Renovate | `RENOVATE_` | Dependency updates |
| Semantic Release | `SEMREL_` | Version management |

### Step 8: Generate Configuration

Generate the `.gitlab-ci.yml` with selected templates.

## Template Configuration

### Variables

Each template has variables with these properties:

| Property | Description |
|----------|-------------|
| `name` | Variable name (e.g., `PYTHON_IMAGE`) |
| `default` | Default value |
| `type` | `text`, `url`, `boolean`, `enum`, `number` |
| `mandatory` | Required to use template |
| `secret` | Store in CI/CD settings, not in file |
| `advanced` | Only show in advanced mode |

### Features

Templates have toggleable features:

```yaml
# Feature enabled by default - disable with:
inputs:
  lint-disabled: true

# Feature disabled by default - enable with:
inputs:
  publish-enabled: true
```

### Variants

Templates may have variants for additional functionality:

| Variant | Available In | Purpose |
|---------|--------------|---------|
| **Vault** | Most templates | HashiCorp Vault secrets |
| **OIDC** | AWS, Azure, GCP | OpenID Connect auth |
| **Google Cloud** | Ansible, Python, Helm, K8s, Terraform | GCP authentication |
| **AWS** | Python, Terraform | AWS authentication |
| **GitLab Pages** | MkDocs, Sphinx, DBT | Publish to GitLab Pages |
| **Jib** | Maven | Build Docker images with Jib |

## YAML Output Format

### Component Mode (Recommended)

```yaml
include:
  # Python template
  - component: $CI_SERVER_FQDN/to-be-continuous/python/python@7
    inputs:
      image: "python:3.12-slim"
      build-system: "poetry"
      pytest-enabled: true
      bandit-enabled: true

  # Python template (Vault variant)
  - component: $CI_SERVER_FQDN/to-be-continuous/python/python-vault@7
    inputs:
      vault-base-url: "https://vault.example.com"

# secret variables
# (define the variables below in your GitLab group/project variables)
# VAULT_ROLE_ID: The AppRole RoleID
# VAULT_SECRET_ID: The AppRole SecretID
```

### Project Mode

```yaml
include:
  # Python template
  - project: "to-be-continuous/python"
    ref: "7.5"
    file: "templates/gitlab-ci-python.yml"

# secret variables
# SONAR_TOKEN: SonarQube authentication token

variables:
  PYTHON_IMAGE: "python:3.12-slim"
  PYTHON_BUILD_SYSTEM: "poetry"
  PYTEST_ENABLED: "true"
```

### Remote Mode

```yaml
include:
  # Python template
  - remote: "https://gitlab.com/to-be-continuous/python/-/raw/7.5/templates/gitlab-ci-python.yml"

variables:
  PYTHON_IMAGE: "python:3.12-slim"
```

### Input Name Transformation

For component mode, transform variable names:

1. Strip prefix: `PYTHON_IMAGE` → `IMAGE`
2. Lowercase: `IMAGE` → `image`
3. Hyphens for underscores: `BUILD_SYSTEM` → `build-system`

Examples:
- `PYTHON_IMAGE` → `image`
- `PYTHON_BUILD_SYSTEM` → `build-system`
- `PYTEST_ENABLED` → `pytest-enabled`
- `GO_CI_LINT_DISABLED` → `ci-lint-disabled`

### Stages (Optional)

```yaml
stages:
  - build
  - test
  - package-build
  - package-test
  - infra
  - deploy
  - acceptance
  - publish
  - infra-prod
  - production
```

## Environment Configuration

Deployment templates support 4 environments:

| Environment | Variable Prefix | Branch | Purpose |
|-------------|-----------------|--------|---------|
| review | `{PREFIX}_REVIEW_` | Feature | Dynamic review apps |
| integration | `{PREFIX}_INTEG_` | develop | CI environment |
| staging | `{PREFIX}_STAGING_` | main | Pre-production |
| production | `{PREFIX}_PROD_` | main | Production |

## Presets

Pre-configured variable sets for common services:

| Preset | Variables Set |
|--------|--------------|
| **SonarCloud** | `SONAR_HOST_URL: https://sonarcloud.io` |
| **OpenShift Sandbox** | `OS_URL`, `K8S_URL` for RedHat sandbox |

## Additional Resources

### Reference Files

For detailed template configurations:
- **`references/build-templates.md`** - All 15 build templates with full variables
- **`references/deployment-templates.md`** - 12 templates (1 infrastructure + 11 hosting) with variants
- **`references/analysis-templates.md`** - 23 templates (7 analysis + 3 packaging + 10 acceptance + 3 misc/publish)
- **`references/presets.md`** - Pre-configured settings for SonarCloud, OpenShift Sandbox

### Example Files

Working configurations in `examples/`:
- **`python-docker-k8s.yml`** - Python + Docker + Helm
- **`node-sonar-docker.yml`** - Node.js + SonarQube + Docker
- **`terraform-aws.yml`** - Terraform + AWS with OIDC
- **`java-maven-cf.yml`** - Maven + Cloud Foundry

### Official Resources

- **Kicker Wizard**: https://to-be-continuous.gitlab.io/kicker
- **Documentation**: https://to-be-continuous.gitlab.io/doc
- **Templates**: https://gitlab.com/to-be-continuous
- **Samples**: https://gitlab.com/to-be-continuous/samples

## Workflow Guidelines

### For New Projects

1. Ask about project type, language, and deployment target
2. Configure global options (recommend component mode, minor version)
3. Select templates for each category
4. Read `schemas/{template}.json` to get valid inputs, components, and versions
5. Configure variables (focus on mandatory and image versions)
6. Enable relevant features and variants
7. Generate the configuration

### For Existing Projects

1. Review current `.gitlab-ci.yml`
2. Identify opportunities to use TBC templates
3. Read `schemas/{template}.json` to get valid inputs, components, and versions
4. Suggest equivalent TBC templates
5. Provide migration guidance

### Best Practices

- Use `component` mode for GitLab 16.0+
- Use `minor` version for balance of updates and stability
- Enable only needed features
- Store secrets in CI/CD variables
- Document non-default configurations
- Use variants for cloud authentication (Vault, OIDC)
