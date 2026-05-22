---
name: building-with-tbc
description: This skill should be used when the user asks to "generate gitlab-ci.yml",
  "create GitLab CI pipeline", "configure GitLab CI/CD", "use To-Be-Continuous templates",
  "setup TBC templates", "create CI/CD for Python/Node/Go/Java project", "configure
  Docker build in GitLab", "setup Kubernetes deployment in GitLab", "add SonarQube
  to GitLab CI", "configure Terraform with GitLab", or mentions "TBC", "To-Be-Continuous",
  "Kicker".
version: 1.0.0
---

# Building with To-Be-Continuous (TBC)

Knowledge base for generating GitLab CI/CD configurations using the To-Be-Continuous framework.

## CRITICAL: Framework-First Principle

**NEVER assume a solution. ALWAYS evaluate the framework first.**

Before generating any configuration, **invoke the `component-research` skill** using the Skill tool:

```
Skill: component-research
```

This triggers the Deep Research process to determine:
- Which TBC components fit the use case
- Whether variants are needed
- If custom steps are truly required (rare)

**Mandatory Workflow:**
1. **Invoke `component-research` skill** (Skill tool) to evaluate fit
2. Wait for decision output with Priority 1-6 recommendation
3. Only proceed to generate configuration after decision is documented
4. If Priority 6 (custom step), document WHY TBC doesn't fit

**The user may request something and be incorrect about the approach.** The `component-research` skill disciplines correct framework usage before any generation happens.

## Overview

To-Be-Continuous (TBC) is a framework of 62 modular templates organized into 8 categories for building GitLab CI/CD pipelines.

### Template Categories

| Category | Count | Selection |
|----------|-------|-----------|
| Build | 15 | Single |
| Code Analysis | 7 | Multiple |
| Packaging | 3 | Single |
| Infrastructure | 1 | Single |
| Deployment | 11 | Single |
| Acceptance | 10 | Multiple |
| Other | 3 | Multiple |

**Selection Rules:**
- Build, Packaging, Infrastructure, Deployment: SELECT ONE or NONE
- Code Analysis, Acceptance, Other: SELECT MULTIPLE (including none)

## Configuration Modes

| Mode | GitLab Version | Syntax |
|------|----------------|--------|
| component | 16.0+ (recommended) | `$CI_SERVER_FQDN/path/template@version` |
| project | Self-hosted | `project: "path"` + `ref` + `file` |
| remote | External | HTTPS URL to template |

## Version Modes

| Mode | Syntax | Updates |
|------|--------|---------|
| major | `@7` | Auto major (less stable) |
| minor | `@7.5` | Auto patch (recommended) |
| full | `@7.5.2` | None (most stable) |

## Generating Configurations

When generating a TBC configuration, read and follow `references/create-component.md`.

## Evaluating Component Fit

Before generating, **invoke the `component-research` skill** using the Skill tool. That skill executes the complete decision process with flowcharts and Deep Research protocol.

## Reference Files

| Need | Reference |
|------|-----------|
| Decide if component fits | Invoke `component-research` skill (Skill tool) |
| Complete template catalog | `references/templates-catalog.md` |
| Build templates (15) | `references/build-templates.md` |
| Deployment templates (11) | `references/deployment-templates.md` |
| Analysis templates (7) | `references/analysis-templates.md` |
| Variants (Vault, OIDC) | `references/variantes.md` |
| Common presets | `references/presets.md` |
| Best practices | `references/best-practices.md` |
| Configuration formats | `references/configuration-formats.md` |

## Schemas

All templates have JSON schemas in `schemas/`. Read schema to get valid inputs, components, and versions:

```
schemas/{template-name}.json
```

## Example Configurations

Working examples in `examples/`:
- `python-docker-k8s.yml`
- `node-sonar-docker.yml`
- `terraform-aws.yml`
- `java-maven-cf.yml`

## Validation

Use SlashCommand tool with `tbc:validate`.

## Key Principles

1. Read schemas first - templates have specific variables, don't hallucinate
2. Transform names for component mode - lowercase with hyphens
3. Validate before presenting - use `tbc:validate`
4. Respect selection rules - single vs multiple per category
5. Document secret variables - they go in GitLab CI/CD settings
6. Use `$CI_SERVER_FQDN` for component mode
