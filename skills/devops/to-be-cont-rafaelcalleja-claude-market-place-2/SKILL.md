---
name: to-be-cont
description: "Comprehensive documentation review and analysis of to-be-continuous GitLab CI/CD templates and framework architecture"
allowed-tools:
  - glob
  - read
---

# To Be Continuous Documentation Research

A comprehensive workflow for exploring and understanding the to-be-continuous GitLab CI/CD framework through systematic documentation and template analysis.

## Prerequisites

- Access to the to-be-continuous documentation files in `docs/to-be-continuous-knowledge/templates/`
- Familiarity with GitLab CI/CD concepts
- Understanding of containerization and cloud infrastructure patterns

## Steps

### 1. Find Docker template files

Locate Docker YAML template files for GitLab CI/CD pipelines with support for Kaniko, Buildah, and DIND build tools

**Action:** glob
**Details:**
- glob_pattern: `docs/to-be-continuous-knowledge/templates/docker/*.yml`

**Reference:** [gitlab-ci-docker.yml](references/gitlab-ci-docker.yml)

### 2. Read Docker template files

Review GitLab CI/CD Docker templates including base configurations, build tools (kaniko/buildah/dind), security scanning (trivy), SBOM generation, and cloud provider authentication (AWS/GCP/Vault)

**Action:** read
**Details:**
- files:
  - `docs/to-be-continuous-knowledge/templates/docker/gitlab-ci-docker.yml`
  - `docs/to-be-continuous-knowledge/templates/docker/gitlab-ci-docker-vault.yml`
  - `docs/to-be-continuous-knowledge/templates/docker/gitlab-ci-docker-gcp.yml`
  - `docs/to-be-continuous-knowledge/templates/docker/gitlab-ci-docker-ecr.yml`

**References:**
- [gitlab-ci-docker-vault.yml](references/gitlab-ci-docker-vault.yml)
- [gitlab-ci-docker-gcp.yml](references/gitlab-ci-docker-gcp.yml)
- [gitlab-ci-docker-ecr.yml](references/gitlab-ci-docker-ecr.yml)

### 3. Read to-be-continuous documentation files

Review comprehensive to-be-continuous documentation covering introduction, usage patterns, architecture philosophy, advanced continuous delivery, community resources, and FAQs about GitLab CI/CD templates

**Action:** read
**Details:**
- files:
  - `docs/to-be-continuous-knowledge/templates/intro.md`
  - `docs/to-be-continuous-knowledge/templates/usage.md`
  - `docs/to-be-continuous-knowledge/templates/understand.md`
  - `docs/to-be-continuous-knowledge/templates/advanced-cd.md`
  - `docs/to-be-continuous-knowledge/templates/community.md`
  - `docs/to-be-continuous-knowledge/templates/faq.md`

**References:**
- [intro.md](references/intro.md)
- [usage.md](references/usage.md)
- [understand.md](references/understand.md)
- [advanced-cd.md](references/advanced-cd.md)
- [community.md](references/community.md)
- [faq.md](references/faq.md)

## References

This skill uses these reference materials:

- **gitlab-ci-docker.yml** ([references/gitlab-ci-docker.yml](references/gitlab-ci-docker.yml)) - Base GitLab CI/CD Docker template with support for Kaniko, Buildah, and DIND build tools, including stages for hadolint, trivy scanning, and SBOM generation

- **gitlab-ci-docker-vault.yml** ([references/gitlab-ci-docker-vault.yml](references/gitlab-ci-docker-vault.yml)) - Vault authentication variant for GitLab CI/CD Docker template using OIDC JWT tokens for secret management

- **gitlab-ci-docker-gcp.yml** ([references/gitlab-ci-docker-gcp.yml](references/gitlab-ci-docker-gcp.yml)) - GCP authentication variant with OIDC for Workload Identity Provider integration and service account impersonation

- **gitlab-ci-docker-ecr.yml** ([references/gitlab-ci-docker-ecr.yml](references/gitlab-ci-docker-ecr.yml)) - AWS ECR authentication variant with OIDC for IAM role assumption and ECR registry access

- **intro.md** ([references/intro.md](references/intro.md)) - Introduction to to-be-continuous framework with key features overview including modularity, security, git workflows, documentation, and implemented GitLab features

- **usage.md** ([references/usage.md](references/usage.md)) - Comprehensive usage guide covering template inclusion methods, configuration approaches, debugging, Docker image version strategies, secrets management, and advanced override techniques

- **understand.md** ([references/understand.md](references/understand.md)) - Architecture and philosophy documentation covering template types, generic pipeline stages, publish & release strategies, deployment environments, git branching models, and development workflows

- **advanced-cd.md** ([references/advanced-cd.md](references/advanced-cd.md)) - Advanced continuous delivery considerations including review apps, pull-based deployment and GitOps strategies, and deployment code organization patterns

- **community.md** ([references/community.md](references/community.md)) - Community resources including Discord channel, Stack Overflow support, contribution guidelines, GitLab code repository, and public presentations

- **faq.md** ([references/faq.md](references/faq.md)) - Frequently asked questions covering license (LGPL 3.0), development history at Orange, self-managed GitLab support, Auto DevOps comparison, template overrides, and tracking mechanisms

## Usage

To use this skill:

1. Start by reviewing the introduction documentation to understand the to-be-continuous framework philosophy and key features
2. Explore Docker templates to understand containerization approaches (Kaniko, Buildah, DIND)
3. Review cloud provider authentication variants (AWS ECR, GCP, Vault) for your deployment needs
4. Study the usage guide for template inclusion and configuration strategies
5. Understand the architecture and development workflows for your project type
6. Review advanced continuous delivery patterns for GitOps and pull-based deployment
7. Consult FAQs and community resources for specific implementation questions

## Notes

- The to-be-continuous framework is developed and maintained by Orange as an open-source project under LGPL 3.0 license
- Templates support modular composition for polyglot environments
- Adaptive pipeline strategy provides different behavior based on development stage (early development, MR, production branch)
- Supports multiple Git branching models: Feature-Branch (recommended) and Gitflow
- Extensive support for GitLab CI/CD features including caching, artifacts, code coverage, JUnit reports, and container scanning
- Community support available on Discord and Stack Overflow
- Each template is independently versioned using semantic versioning

---

*Generated by workflow-weaver on 2025-12-02*
*Original recording: to-be-cont, started 2025-12-02T00:00:00Z*
