---
name: github-actions-workflows
description: GitHub Actions workflow patterns for CI/CD including matrix builds, reusable workflows, secrets management, and caching strategies. Use when setting up or optimizing GitHub Actions pipelines.
---

# GitHub Actions Workflows

Expert guidance for designing reliable, secure, and performant GitHub Actions CI/CD pipelines with patterns for matrix builds, reusable workflows, caching, and deployment automation.

## When to Use This Skill

- Setting up CI/CD pipelines with GitHub Actions from scratch
- Optimizing slow or expensive GitHub Actions workflows
- Implementing matrix builds for multi-environment testing
- Creating reusable workflows and composite actions for DRY pipelines
- Managing secrets securely across environments
- Configuring caching for dependency and build artifact reuse
- Setting up deployment workflows with staging and production gates
- Debugging failing or flaky workflow runs
- Implementing concurrency controls to prevent duplicate runs

## Quick Reference

| Task | Load reference |
| --- | --- |
| Matrix builds, reusable workflows, caching, deployment, concurrency | `skills/github-actions-workflows/references/workflow-patterns.md` |

## Core Principles

- **Structured jobs**: Break workflows into clear, distinct jobs with defined dependencies
- **DRY configuration**: Use reusable workflows and composite actions to avoid duplication
- **Security first**: Use GitHub secrets, OIDC, and minimum necessary permissions
- **Cache aggressively**: Cache dependencies, build outputs, and test fixtures
- **Trigger thoughtfully**: Configure event triggers to avoid unnecessary workflow runs
- **Document workflows**: Add comments explaining non-obvious YAML configuration

## Workflow

### 1. Design

Plan the pipeline structure before writing YAML.

- Identify trigger events (push, pull_request, schedule, workflow_dispatch)
- Map job dependencies and what can run in parallel
- Determine caching opportunities (dependencies, build outputs)
- Plan environment promotion (dev, staging, production)

### 2. Implementation

Build the pipeline incrementally.

- Start with a minimal workflow and add complexity
- Use matrix builds for multi-environment testing
- Extract reusable workflows for shared patterns
- Configure secrets management with environment protection

### 3. Optimization

Reduce runtime and cost.

- Profile workflow timing to identify bottlenecks
- Add caching for dependencies and build artifacts
- Use concurrency controls to cancel redundant runs
- Configure path filters to skip unaffected workflows

### 4. Maintenance

Keep workflows healthy over time.

- Pin action versions to specific SHAs for security
- Review and update actions regularly
- Monitor workflow runtime trends and costs
- Peer-review workflow changes before merging

## Common Mistakes

- Using `actions/checkout@main` instead of pinning to a SHA or version tag
- Not setting `permissions` block (defaults to overly broad read-write)
- Caching node_modules instead of the package manager cache directory
- Missing `concurrency` groups, leading to duplicate deploys
- Hardcoding secrets in workflow files instead of using GitHub Secrets
- Running the full test suite on every push instead of using path filters
- Not using `workflow_call` for shared CI logic across repositories
