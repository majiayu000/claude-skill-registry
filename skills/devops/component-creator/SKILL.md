---
name: Component Creator
description: This skill should be used when the user wants to "create to-be-continuous component", "build TBC template", "extend existing component", "create variant", "contribute to to-be-continuous", "component structure", "how to create gitlab ci component", or needs guidance on component architecture, naming conventions, GitLab CI component syntax, input specifications, base job patterns, or to-be-continuous best practices and philosophy.
version: 0.1.0
---

# to-be-continuous Component Creation Guide

Guide users through creating production-ready to-be-continuous components that follow ecosystem conventions, architectural principles, and best practices.

## Overview

to-be-continuous components follow standardized patterns enabling composability, reusability, and maintainability across projects. Understanding component structure, naming conventions, and design principles is essential for creating components compatible with the ecosystem.

**Key concepts:**
- Single-responsibility principle per component
- Component-based architecture with `spec.inputs`
- Variant patterns for different authentication methods
- Base job inheritance for extensibility
- Convention over configuration
- Adaptive pipeline strategy

## Core Philosophy

### Single Responsibility & Modularity

Each component handles ONE specific pipeline stage (build, test, package, deploy, analyze). Components cooperate gracefully through:
- Shared artifact formats (Maven artifacts → Docker builds)
- Standardized dotenv variable exports
- Common stage naming conventions
- Reusable tool outputs (SonarQube reusing test reports)

### Adaptive Pipeline Strategy

"Prioritize speed in early development stages, gradually introduce Quality & Security tasks as you get closer to production."

**Implementation:**
- Development branches: Manual quality checks, allowed to fail
- Draft MRs: Auto-run quality checks, allowed to fail
- Ready MRs: Auto-run quality checks, must succeed
- Production/integration branches: All checks required

### Composability Over Integration

Components integrate through:
- Standardized stage sequence (11 stages)
- Dotenv artifact propagation
- Common variable naming patterns
- Shared authentication mechanisms

## Component Directory Structure

Every to-be-continuous component follows this organizational pattern:

```
component-name/
├── templates/
│   ├── gitlab-ci-component.yml        # Standard variant (required)
│   ├── gitlab-ci-component-vault.yml  # Vault variant (optional)
│   ├── gitlab-ci-component-oidc.yml   # OIDC variant (optional)
│   ├── gitlab-ci-component-gcp.yml    # GCP variant (optional)
│   ├── gitlab-ci-component-aws.yml    # AWS/EKS variant (optional)
│   └── gitlab-ci-component-ecr.yml    # ECR variant (optional)
├── README.md                          # Component documentation (required)
├── CHANGELOG.md                       # Version history (required)
├── .gitlab-ci.yml                     # Component's own CI/CD (required)
└── LICENSE                            # MIT license (recommended)
```

**Critical rules:**
1. **templates/ directory**: MUST contain all component YAML files
2. **Standard variant**: MUST exist (gitlab-ci-component.yml)
3. **Variant suffixes**: Use established patterns (-vault, -oidc, -gcp, -aws, -eks, -ecr)
4. **README.md**: MUST document inputs, examples, variants
5. **CHANGELOG.md**: MUST track version changes

## Component YAML Structure

### Required Sections

Every component YAML file MUST contain:

1. **spec**: Input/output specification
2. **Base job**: Hidden job (`.component-base`) extended by all jobs
3. **Jobs**: Concrete jobs that execute in pipeline stages
4. **Scripts**: Reusable bash functions (via YAML anchors)

### Standard Template Structure

```yaml
# Component: component-name
# Version: X.Y.Z
# Description: [What this component does]
# Documentation: https://to-be-continuous.gitlab.io/doc/ref/component-name

spec:
  inputs:
    # Required inputs (no default)
    required-input:
      description: "Description of required input"
      type: string

    # Optional inputs (with defaults)
    optional-input:
      description: "Description of optional input"
      type: string
      default: "default-value"

    # Boolean inputs
    feature-enabled:
      description: "Enable specific feature"
      type: boolean
      default: false

    # Enumerated inputs
    build-tool:
      description: "Tool to use for building"
      type: string
      options:
        - tool1
        - tool2
        - default
      default: "default"

# Reusable script library
.scripts: &component-scripts
  - |
    # Logging functions
    log_info() { echo -e "\033[1;34m[INFO]\033[0m $*"; }
    log_warn() { echo -e "\033[1;33m[WARN]\033[0m $*"; }
    log_error() { echo -e "\033[1;31m[ERROR]\033[0m $*"; }

    # Component-specific functions
    component_function() {
      # Function implementation
    }

# Hidden base job - extended by all component jobs
.component-base:
  image: appropriate/image:tag
  variables:
    # Map inputs to variables for backward compatibility
    COMPONENT_VAR: $[[ inputs.required-input ]]
    COMPONENT_FEATURE: $[[ inputs.feature-enabled ]]
  before_script:
    - *component-scripts
  rules:
    - !reference [.tbc-workflow-rules, skip-back-merge]
    - !reference [.tbc-workflow-rules, prefer-mr-pipeline]
    - !reference [.tbc-workflow-rules, extended-skip-ci]

# Concrete jobs
component-build:
  stage: build
  extends: .component-base
  script:
    - log_info "Building with $COMPONENT_VAR"
    - component_function
  artifacts:
    reports:
      dotenv: component.env
  rules:
    - when: on_success

component-test:
  stage: test
  extends: .component-base
  script:
    - log_info "Testing component"
  needs:
    - component-build
  rules:
    - !reference [.test-policy, rules]

component-publish:
  stage: publish
  extends: .component-base
  script:
    - log_info "Publishing component"
  needs:
    - component-build
    - component-test
  rules:
    - !reference [.delivery-policy, rules]
```

## Input Specification Best Practices

### Dual Syntax Support

Components MUST support BOTH input syntaxes for backward compatibility:

**Modern (Component Inputs):**
```yaml
include:
  - component: $CI_SERVER_FQDN/to-be-continuous/component/gitlab-ci-component@1.0.0
    inputs:
      build-tool: "maven"
      enable-tests: true
```

**Legacy (Variables):**
```yaml
include:
  - project: 'to-be-continuous/component'
    ref: '1.0.0'
    file: '/templates/gitlab-ci-component.yml'

variables:
  COMPONENT_BUILD_TOOL: "maven"
  COMPONENT_ENABLE_TESTS: "true"
```

**Implementation pattern:**
```yaml
spec:
  inputs:
    build-tool:
      type: string
      default: "default"

.component-base:
  variables:
    # Input maps to variable
    COMPONENT_BUILD_TOOL: $[[ inputs.build-tool ]]
```

### Naming Conventions

**Inputs (kebab-case):**
- `build-tool`, `snapshot-image`, `registry-mirror`
- Use hyphens to separate words
- All lowercase

**Variables (SCREAMING_SNAKE_CASE):**
- `COMPONENT_BUILD_TOOL`, `COMPONENT_SNAPSHOT_IMAGE`, `COMPONENT_REGISTRY_MIRROR`
- Use `COMPONENT_` prefix
- All uppercase with underscores

### Input Types

```yaml
spec:
  inputs:
    # String input
    string-input:
      type: string
      description: "Single value input"
      default: "default-value"

    # Number input
    number-input:
      type: number
      description: "Numeric value"
      default: 3

    # Boolean input
    boolean-input:
      type: boolean
      description: "True/false flag"
      default: false

    # Enumerated input
    choice-input:
      type: string
      description: "Select from options"
      options:
        - option1
        - option2
        - option3
      default: "option1"
```

### Required vs Optional Inputs

**Required inputs** (no default):
- Critical for component functionality
- Component fails if not provided
- Example: deployment target, required credentials

**Optional inputs** (with default):
- Customization and tuning
- Sensible defaults for common use cases
- Example: image versions, feature flags, timeouts

**Best practice:** Minimize required inputs. Provide defaults whenever possible.

## Base Job Patterns

### Hidden Base Job

**Purpose:** Centralize configuration affecting all component jobs

**Pattern:**
```yaml
.component-base:
  image: $[[ inputs.image ]]
  tags:
    - docker
  variables:
    VAR1: $[[ inputs.var1 ]]
    VAR2: "default-value"
  before_script:
    - *component-scripts
    - setup_function
  rules:
    - !reference [.tbc-workflow-rules, skip-back-merge]
    - !reference [.tbc-workflow-rules, prefer-mr-pipeline]
    - !reference [.tbc-workflow-rules, extended-skip-ci]
```

**Users can override:**
```yaml
.component-base:
  tags:
    - kubernetes
  variables:
    http_proxy: "http://proxy:8080"
```

### Tool-Specific Base Jobs

For components supporting multiple tools:

```yaml
.component-base:
  # Common configuration

.component-tool1-base:
  extends: .component-base
  image: tool1/image:latest
  variables:
    TOOL: "tool1"

.component-tool2-base:
  extends: .component-base
  image: tool2/image:latest
  variables:
    TOOL: "tool2"

component-build-tool1:
  extends: .component-tool1-base
  script:
    - tool1 build

component-build-tool2:
  extends: .component-tool2-base
  script:
    - tool2 build
```

## Job Naming Conventions

### Format

`[component]-[action]` or `[component]-[tool]-[action]`

**Examples:**
- `docker-build`, `docker-publish`, `docker-trivy`
- `maven-compile`, `maven-test`, `maven-deploy`
- `k8s-review`, `k8s-staging`, `k8s-production`

### Action Verbs

Use consistent verbs:
- **build**: Compile, assemble artifacts
- **test**: Unit tests, integration tests
- **scan**: Security scanning, vulnerability analysis
- **lint**: Code linting, static analysis
- **package**: Create distributable format
- **publish**: Upload to registry
- **deploy**: Deploy to environment
- **cleanup**: Remove resources

### Environment Jobs

For deployment components:
- `component-review` (ephemeral review environments)
- `component-integration` (integration testing environment)
- `component-staging` (pre-production environment)
- `component-production` (production environment)

## Pipeline Stages

### Standard 11-Stage Sequence

```yaml
stages:
  - .pre
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
  - .post
```

**Stage assignments:**
- **build**: Compile code, run unit tests
- **test**: Additional testing (integration, contract)
- **package-build**: Build containers, packages
- **package-test**: Test packages (security scans, healthchecks)
- **infra**: Provision non-prod infrastructure
- **deploy**: Deploy to non-prod environments
- **acceptance**: Functional, performance, security tests
- **publish**: Promote artifacts to release registries
- **infra-prod**: Provision production infrastructure
- **production**: Deploy to production

**Custom stages:** Can be inserted (e.g., `code-analysis` between `test` and `package-build`)

## Variant Patterns

### Common Variants

| Variant | Suffix | Authentication | Use Case | Components |
|---------|--------|----------------|----------|------------|
| **Standard** | (none) | CI/CD variables | Simple deployments | All (62) |
| **Vault** | `-vault` | HashiCorp Vault JWT/AppRole | Enterprise secrets management | ~20 |
| **OIDC** | `-oidc` | OpenID Connect | Temporary cloud credentials | AWS, Azure, GCloud |
| **GCP** | `-gcp` | Workload Identity Federation | GKE deployments, Artifact Registry | Docker, K8s, Helm, S3, Terraform |
| **AWS/EKS** | `-aws`/`-eks` | OIDC with IAM roles | EKS deployments, ECR registry | K8s, Docker |
| **ECR** | `-ecr` | OIDC with IAM | ECR-specific registry auth | Docker |

Consult `../template-discovery/references/variantes.md` for complete catalog (70+ variants documented).

### When to Create a Variant

Create a variant when:
- **Authentication method differs**: Vault vs static credentials
- **Platform integration required**: GCP Workload Identity, AWS OIDC
- **Security requirements change**: OIDC temporary credentials vs long-lived tokens
- **Deployment strategy differs**: Different cloud provider SDKs

**Don't create variant for:**
- Configuration differences (use inputs/variables)
- Optional features (use boolean inputs)
- Minor behavior changes (use conditional logic)

### Variant Implementation Pattern

**Step 1: Copy standard variant**
```bash
cp gitlab-ci-component.yml gitlab-ci-component-vault.yml
```

**Step 2: Modify authentication mechanism**
```yaml
# Standard variant uses CI/CD variables
variables:
  REGISTRY_TOKEN: $[[ inputs.registry-token ]]

# Vault variant fetches from Vault
variables:
  REGISTRY_TOKEN: '@url@http://vault-secrets-provider/api/secrets/registry?field=token'
```

**Step 3: Add variant-specific inputs**
```yaml
spec:
  inputs:
    vault-addr:
      description: "Vault server address"
      type: string
    vault-role:
      description: "Vault role for authentication"
      type: string
      default: "gitlab-ci"
```

**Step 4: Update README with variant documentation**

**Step 5: Add to variantes.md catalog**

## Variable Conventions

### Variable Scoping

Three levels of variables:

**1. Global Component Variables**
```yaml
variables:
  COMPONENT_VERSION: "1.0.0"
  COMPONENT_DEFAULT_IMAGE: "alpine:latest"
```

**2. Job-Level Variables**
```yaml
.component-base:
  variables:
    BASE_VAR: "value"

component-build:
  variables:
    BUILD_SPECIFIC_VAR: "value"
```

**3. Scoped Variables** (conditional)
```yaml
variables:
  S3_BUCKET: "nonprod-bucket"
  scoped__S3_BUCKET__if__CI_ENVIRONMENT_NAME__equals__production: "prod-bucket"
```

### Secret Handling

**Standard secrets** (CI/CD variables):
```yaml
variables:
  SECRET_VAR: $SECRET_FROM_CICD_VARS
```

**Unmaskable secrets** (Base64 encoding):
```yaml
variables:
  SECRET_WITH_SPECIAL_CHARS: '@b64@eyJvcGVuIjoiJOKCrDVAbWUifQ=='
```

**External secrets** (Vault, URL):
```yaml
variables:
  VAULT_SECRET: '@url@http://vault-secrets-provider/api/secrets/path?field=name'
```

**Secret evaluation** (in scripts):
```bash
eval_secret() {
  local var_name="$1"
  local var_value="${!var_name}"

  # Decode @b64@ prefix
  if [[ "$var_value" =~ ^@b64@(.+)$ ]]; then
    echo "${BASH_REMATCH[1]}" | base64 -d
    return
  fi

  # Fetch @url@ prefix
  if [[ "$var_value" =~ ^@url@(.+)$ ]]; then
    curl -sSf "${BASH_REMATCH[1]}"
    return
  fi

  # Return as-is
  echo "$var_value"
}
```

## Artifact Export Patterns

### DotEnv Artifacts

Export variables for downstream jobs:

```yaml
component-build:
  script:
    - build_command
    - |
      {
        echo "component_version=${VERSION}"
        echo "component_artifact=${ARTIFACT_PATH}"
        echo "component_digest=$(sha256sum artifact | cut -d' ' -f1)"
      } > component.env
  artifacts:
    reports:
      dotenv: component.env
```

**Downstream consumption:**
```yaml
component-deploy:
  needs:
    - component-build
  script:
    - echo "Deploying version ${component_version}"
    - echo "Artifact digest: ${component_digest}"
```

### Standard Output Variables

**Naming convention:** `component_attribute`

Examples:
- `docker_image`, `docker_tag`, `docker_digest`
- `maven_artifact`, `maven_version`
- `k8s_namespace`, `k8s_service_url`

**Benefits:**
- Declarative deployment pipelines
- Version propagation across stages
- Artifact traceability

## Rules and Conditions

### Standard Rule References

Components MUST include standard workflow rules:

```yaml
.component-base:
  rules:
    - !reference [.tbc-workflow-rules, skip-back-merge]
    - !reference [.tbc-workflow-rules, prefer-mr-pipeline]
    - !reference [.tbc-workflow-rules, extended-skip-ci]
```

**Explanation:**
- **skip-back-merge**: Prevent pipelines on automated back-merges
- **prefer-mr-pipeline**: Use MR pipelines over branch pipelines when both exist
- **extended-skip-ci**: Support `[skip ci on tag]`, `[skip ci on mr]`, etc.

### Adaptive Pipeline Policies

**Test jobs** (quality/security):
```yaml
component-test:
  rules:
    - !reference [.test-policy, rules]
```

**Behavior:**
- **Tag/protected branches**: Auto-run, must succeed
- **Dev branch (no MR)**: Manual, allowed to fail
- **Draft MR**: Auto-run, allowed to fail
- **Ready MR**: Auto-run, must succeed

**Delivery jobs** (publish/production):
```yaml
component-publish:
  rules:
    - !reference [.delivery-policy, rules]
```

**Behavior:**
- Execute on release tags (SemVer)
- Execute on production/integration branches
- Skip elsewhere

### Custom Rules

```yaml
component-manual-job:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
      when: never
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
    - when: never
```

## Script Best Practices

### Logging Functions

```bash
.scripts: &component-scripts
  - |
    # ANSI color codes
    log_info() { echo -e "\033[1;34m[INFO]\033[0m $*"; }
    log_warn() { echo -e "\033[1;33m[WARN]\033[0m $*"; }
    log_error() { echo -e "\033[1;31m[ERROR]\033[0m $*"; }
    log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $*"; }
```

### Tool Installation Helpers

```bash
maybe_install_tool() {
  if ! command -v tool &> /dev/null; then
    log_info "Installing tool..."
    # Installation logic
  fi
}
```

### Multi-Distro Compatibility

```bash
detect_package_manager() {
  if command -v apt-get &> /dev/null; then
    echo "apt-get"
  elif command -v yum &> /dev/null; then
    echo "yum"
  elif command -v apk &> /dev/null; then
    echo "apk"
  else
    log_error "No supported package manager found"
    return 1
  fi
}
```

### Error Handling

```bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Function with error handling
safe_operation() {
  if ! risky_command; then
    log_error "Command failed"
    return 1
  fi
  log_success "Command succeeded"
}
```

## Component Naming

### Component Names

- **kebab-case**: `docker`, `semantic-release`, `kubernetes`, `cloud-native-buildpacks`
- **Descriptive**: Clearly indicate technology/purpose
- **Match technology**: `maven` for Maven, `terraform` for Terraform
- **No abbreviations**: `kubernetes` not `k8s` (exception: widely known like `s3`)

### Template Files

Pattern: `gitlab-ci-[component][-variant].yml`

Examples:
- `gitlab-ci-docker.yml` (standard)
- `gitlab-ci-docker-vault.yml` (Vault variant)
- `gitlab-ci-docker-gcp.yml` (GCP variant)
- `gitlab-ci-kubernetes-aws.yml` (AWS variant)

## Documentation Requirements

### README.md Structure

```markdown
# Component Name

Brief description of what component does.

## Inputs

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `input-name` | string | `default` | Description |

## Variants

- **Standard**: Description
- **Vault**: Description
- **OIDC**: Description

## Example

\`\`\`yaml
include:
  - component: $CI_SERVER_FQDN/to-be-continuous/component/gitlab-ci-component@1.0.0
    inputs:
      example-input: "value"
\`\`\`

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPONENT_VAR` | Description | `value` |

## Jobs

- **component-build**: Description
- **component-test**: Description

## Integration

How component integrates with other components.

## License

MIT
```

### CHANGELOG.md

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

## [1.1.0] - 2024-01-15
### Added
- New input for feature X
- Support for variant Y

### Changed
- Updated default image to v2.0

### Fixed
- Bug in authentication flow

## [1.0.0] - 2023-12-01
### Added
- Initial release
```

## Versioning Strategy

### Semantic Versioning

Components MUST follow [SemVer](https://semver.org/):

- **MAJOR**: Breaking changes (incompatible inputs, removed jobs)
- **MINOR**: New features (new inputs, new jobs, backward compatible)
- **PATCH**: Bug fixes (no new functionality)

### Version Tags

Create Git tags for releases:
```bash
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```

### Version Aliases

GitLab automatically creates aliases:
- `1` → latest 1.x.x
- `1.2` → latest 1.2.x
- `1.2.3` → exact version

**Users can pin:**
```yaml
# Always get latest patches
component: .../component@1.2

# Pin exact version
component: .../component@1.2.3
```

## Testing Components

### Sample Project

Create sample project demonstrating component usage:

```
samples/component-sample/
├── .gitlab-ci.yml          # Uses component
├── README.md               # Explains sample
├── src/                    # Sample source code
└── tests/                  # Sample tests
```

**Sample .gitlab-ci.yml:**
```yaml
include:
  - component: $CI_SERVER_FQDN/to-be-continuous/component/gitlab-ci-component@1.0.0
    inputs:
      build-tool: "maven"
      enable-tests: true
```

### Validation Checklist

Before releasing component:

- [ ] All variants tested
- [ ] README documentation complete
- [ ] CHANGELOG updated
- [ ] Input specifications validated
- [ ] Sample project created
- [ ] Semantic versioning applied
- [ ] Security scan passed
- [ ] Component CI/CD passes

## Reference Files

For detailed component patterns and examples:

- **`../template-discovery/references/catalog.md`**: 62 existing components to study
- **`../template-discovery/references/variantes.md`**: 70+ variant implementations across components
- **`../template-discovery/references/usage-guide.md`**: Component syntax, scoped variables, secrets management
- **`../template-discovery/references/best-practices.md`**: Architectural patterns (Review Apps, GitOps, repo structure)

## Common Patterns

### Minimal Component

Single job, single stage:

```yaml
spec:
  inputs:
    target:
      type: string

.component-base:
  image: alpine:latest
  rules:
    - !reference [.tbc-workflow-rules, skip-back-merge]
    - !reference [.tbc-workflow-rules, prefer-mr-pipeline]

component-job:
  stage: deploy
  extends: .component-base
  script:
    - echo "Deploying to $[[ inputs.target ]]"
```

### Multi-Tool Component

Support multiple build tools:

```yaml
spec:
  inputs:
    build-tool:
      type: string
      options: [tool1, tool2, default]
      default: "default"

.component-base:
  variables:
    TOOL: $[[ inputs.build-tool ]]

component-build-tool1:
  extends: .component-base
  rules:
    - if: '$TOOL == "tool1"'
  script:
    - tool1 build

component-build-tool2:
  extends: .component-base
  rules:
    - if: '$TOOL == "tool2"'
  script:
    - tool2 build
```

### Environment Deployment Component

Deploy to multiple environments:

```yaml
.component-base:
  image: kubectl:latest
  script:
    - kubectl apply -f manifests/

component-review:
  extends: .component-base
  stage: deploy
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    on_stop: component-review-cleanup

component-staging:
  extends: .component-base
  stage: deploy
  environment:
    name: staging

component-production:
  extends: .component-base
  stage: production
  environment:
    name: production
  rules:
    - !reference [.delivery-policy, rules]
```

## Contributing Components

### Workflow

1. **Discuss on Discord**: Post message with topic `New template: component-name`
2. **Core team creates project**: From template skeleton repository
3. **Fork and branch**: Work from `initial-component` branch
4. **Implement component**: Follow patterns in this guide
5. **Create MR**: Mark as Draft until ready
6. **Review**: At least 2 core team approvals required
7. **Merge**: Automatic release on merge

### Commit Standards

- **Atomic commits**: One logical change per commit
- **Semantic commits**: Follow Conventional Commits
- **Signed-off**: Include `Signed-off-by:` line (DCO)

Examples:
```
feat: add OIDC authentication variant
fix: correct environment variable mapping
docs: update README with new inputs
```

### Review Criteria

- Follows naming conventions
- Includes all required files
- Documentation complete
- Sample project provided
- All variants tested
- Follows to-be-continuous philosophy

## Summary: Key Behaviors

**STRUCTURED**:
- Follow standard directory layout
- Use established naming conventions
- Include all required files (README, CHANGELOG)

**COMPATIBLE**:
- Support dual syntax (inputs + variables)
- Use standard workflow rules
- Export dotenv artifacts for downstream jobs
- Follow 11-stage pipeline sequence

**MODULAR**:
- Single responsibility per component
- Hidden base job for extensibility
- Variant pattern for authentication methods
- Composable with other components

**DOCUMENTED**:
- Clear input specifications
- Usage examples in README
- Variant documentation
- Version changelog

**TESTED**:
- Sample project demonstrating usage
- All variants validated
- Component CI/CD passing
- Security scanning enabled

**Remember**: Study existing components in catalog.md and variantes.md for proven patterns. When in doubt, reference similar existing components for guidance.
