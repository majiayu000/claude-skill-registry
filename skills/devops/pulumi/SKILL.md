---
name: pulumi
description: Pulumi infrastructure as code performance and reliability guidelines. This skill should be used when writing, reviewing, or refactoring Pulumi code to ensure optimal deployment performance and infrastructure reliability. Triggers on tasks involving Pulumi stacks, components, state management, secrets configuration, resource lifecycle options, or CI/CD automation.
---

# Pulumi Best Practices

Comprehensive performance and reliability guide for Pulumi infrastructure as code, designed for AI agents and LLMs. Contains 46 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Pulumi infrastructure code
- Designing component abstractions for reuse
- Configuring secrets and sensitive values
- Organizing stacks and cross-stack references
- Setting up CI/CD pipelines for infrastructure

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | State Management and Backend | CRITICAL | `pstate-` |
| 2 | Resource Graph Optimization | CRITICAL | `graph-` |
| 3 | Component Design | HIGH | `pcomp-` |
| 4 | Secrets and Configuration | HIGH | `secrets-` |
| 5 | Stack Organization | MEDIUM-HIGH | `stack-` |
| 6 | Resource Options and Lifecycle | MEDIUM | `lifecycle-` |
| 7 | Testing and Validation | MEDIUM | `test-` |
| 8 | Automation and CI/CD | LOW-MEDIUM | `auto-` |

## Quick Reference

### 1. State Management and Backend (CRITICAL)

- `pstate-backend-selection` - Use managed backend for production stacks
- `pstate-checkpoint-skipping` - Enable checkpoint skipping for large stacks
- `pstate-stack-size` - Keep stacks under 500 resources
- `pstate-refresh-targeting` - Use targeted refresh instead of full stack
- `pstate-export-import` - Use state export/import for migrations
- `pstate-import-existing` - Import existing resources before managing

### 2. Resource Graph Optimization (CRITICAL)

- `graph-parallel-resources` - Structure resources for maximum parallelism
- `graph-output-dependencies` - Use outputs to express true dependencies
- `graph-explicit-depends` - Use dependsOn only for external dependencies
- `graph-avoid-apply-side-effects` - Avoid side effects in apply functions
- `graph-conditional-resources` - Use conditional logic at resource level
- `graph-stack-references-minimal` - Minimize stack reference depth

### 3. Component Design (HIGH)

- `pcomp-component-resources` - Use ComponentResource for reusable abstractions
- `pcomp-parent-child` - Pass parent option to child resources
- `pcomp-unique-naming` - Use name prefix pattern for unique resource names
- `pcomp-register-outputs` - Register component outputs explicitly
- `pcomp-multi-language` - Design components for multi-language consumption
- `pcomp-transformations` - Use transformations for cross-cutting concerns

### 4. Secrets and Configuration (HIGH)

- `secrets-use-secret-config` - Use secret config for sensitive values
- `secrets-avoid-state-exposure` - Prevent secret leakage in state
- `secrets-external-providers` - Use external secret managers for production
- `secrets-generate-random` - Generate secrets with random provider
- `secrets-provider-rotation` - Rotate secrets provider when team members leave
- `secrets-environment-isolation` - Isolate secrets by environment

### 5. Stack Organization (MEDIUM-HIGH)

- `stack-separation-by-lifecycle` - Separate stacks by deployment lifecycle
- `stack-references-parameterized` - Parameterize stack references
- `stack-output-minimal` - Export only required outputs
- `stack-naming-conventions` - Use consistent stack naming convention

### 6. Resource Options and Lifecycle (MEDIUM)

- `lifecycle-protect-stateful` - Protect stateful resources
- `lifecycle-delete-before-replace` - Use deleteBeforeReplace for unique constraints
- `lifecycle-retain-on-delete` - Use retainOnDelete for shared resources
- `lifecycle-ignore-changes` - Use ignoreChanges for externally managed properties
- `lifecycle-replace-on-changes` - Use replaceOnChanges for immutable dependencies
- `lifecycle-aliases` - Use aliases for safe resource renaming
- `lifecycle-custom-timeouts` - Set custom timeouts for long-running resources

### 7. Testing and Validation (MEDIUM)

- `test-unit-mocking` - Use mocks for fast unit tests
- `test-property-policies` - Use policy as code for property testing
- `test-integration-ephemeral` - Use ephemeral stacks for integration tests
- `test-preview-assertions` - Assert on preview results before deployment
- `test-stack-reference-mocking` - Mock stack references in unit tests

### 8. Automation and CI/CD (LOW-MEDIUM)

- `auto-automation-api-workflows` - Use Automation API for complex workflows
- `auto-inline-programs` - Use inline programs for dynamic infrastructure
- `auto-ci-cd-preview` - Run preview in PR checks
- `auto-deployments-api` - Use Pulumi Deployments for GitOps
- `auto-review-stacks` - Use review stacks for PR environments
- `auto-drift-detection` - Enable drift detection for production

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
