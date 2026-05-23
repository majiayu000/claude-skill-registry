---
name: twelve-factor-app
description: The Twelve-Factor App methodology for building scalable, maintainable cloud-native applications. Use when designing backend services, APIs, microservices, or any software-as-a-service application. Triggers on deployment patterns, configuration management, process architecture, logging, and infrastructure decisions.
---

# Community Cloud-Native Applications Best Practices

Comprehensive methodology for building modern software-as-a-service applications that are portable, scalable, and maintainable. Contains 51 rules across 12 categories, covering the entire application lifecycle from codebase management to production operations.

## When to Apply

Reference these guidelines when:
- Designing new backend services or APIs
- Containerizing applications for Kubernetes or Docker
- Setting up CI/CD pipelines
- Managing configuration across environments
- Implementing logging and monitoring
- Planning application scaling strategy
- Debugging deployment or environment issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Codebase & Version Control | CRITICAL | `code-` |
| 2 | Dependencies | CRITICAL | `dep-` |
| 3 | Configuration | CRITICAL | `config-` |
| 4 | Backing Services | HIGH | `svc-` |
| 5 | Build, Release, Run | HIGH | `build-` |
| 6 | Processes & State | HIGH | `proc-` |
| 7 | Concurrency & Scaling | HIGH | `scale-` |
| 8 | Disposability | HIGH | `disp-` |
| 9 | Port Binding | MEDIUM | `port-` |
| 10 | Dev/Prod Parity | MEDIUM | `parity-` |
| 11 | Logging | MEDIUM | `log-` |
| 12 | Admin Processes | MEDIUM | `admin-` |

## Quick Reference

### 1. Codebase & Version Control (CRITICAL)

- [`code-single-codebase`](references/code-single-codebase.md) - Maintain one codebase per application in version control
- [`code-one-app-one-repo`](references/code-one-app-one-repo.md) - Enforce one-to-one correlation between codebase and application
- [`code-deploys-not-branches`](references/code-deploys-not-branches.md) - Use deploys not branches to represent environments
- [`code-shared-as-libraries`](references/code-shared-as-libraries.md) - Factor shared code into libraries managed by dependency manager

### 2. Dependencies (CRITICAL)

- [`dep-explicit-declaration`](references/dep-explicit-declaration.md) - Declare all dependencies explicitly in a manifest file
- [`dep-isolate-execution`](references/dep-isolate-execution.md) - Isolate dependencies to prevent system package leakage
- [`dep-no-system-tools`](references/dep-no-system-tools.md) - Never rely on implicit system tools being available
- [`dep-deterministic-builds`](references/dep-deterministic-builds.md) - Use lockfiles for deterministic dependency resolution

### 3. Configuration (CRITICAL)

- [`config-separate-from-code`](references/config-separate-from-code.md) - Strictly separate configuration from code
- [`config-use-env-vars`](references/config-use-env-vars.md) - Store configuration in environment variables
- [`config-no-env-groups`](references/config-no-env-groups.md) - Treat environment variables as granular controls not grouped environments
- [`config-validate-on-startup`](references/config-validate-on-startup.md) - Validate required configuration at application startup
- [`config-never-commit-secrets`](references/config-never-commit-secrets.md) - Never commit secrets or credentials to version control

### 4. Backing Services (HIGH)

- [`svc-as-attached-resources`](references/svc-as-attached-resources.md) - Treat backing services as attached resources
- [`svc-connection-strings`](references/svc-connection-strings.md) - Reference all backing services via connection URLs in config
- [`svc-no-local-vs-remote`](references/svc-no-local-vs-remote.md) - Make no distinction between local and third-party services
- [`svc-detach-attach-without-code`](references/svc-detach-attach-without-code.md) - Design services to be detachable and attachable without code changes

### 5. Build, Release, Run (HIGH)

- [`build-separate-stages`](references/build-separate-stages.md) - Strictly separate build, release, and run stages
- [`build-immutable-releases`](references/build-immutable-releases.md) - Create immutable releases with unique identifiers
- [`build-no-runtime-changes`](references/build-no-runtime-changes.md) - Never modify code at runtime - changes require new release
- [`build-complexity-in-build`](references/build-complexity-in-build.md) - Push complexity into build stage keep run stage minimal
- [`build-artifact-per-commit`](references/build-artifact-per-commit.md) - Generate one build artifact per commit deploy same artifact everywhere

### 6. Processes & State (HIGH)

- [`proc-stateless-processes`](references/proc-stateless-processes.md) - Execute the application as stateless processes
- [`proc-no-sticky-sessions`](references/proc-no-sticky-sessions.md) - Never use sticky sessions - store session data in backing services
- [`proc-no-local-filesystem`](references/proc-no-local-filesystem.md) - Never assume local filesystem persists between requests
- [`proc-compile-at-build`](references/proc-compile-at-build.md) - Perform asset compilation and bundling at build time not runtime
- [`proc-share-nothing`](references/proc-share-nothing.md) - Design processes to share nothing with each other

### 7. Concurrency & Scaling (HIGH)

- [`scale-process-model`](references/scale-process-model.md) - Scale out via the process model with multiple process types
- [`scale-process-types`](references/scale-process-types.md) - Assign workloads to appropriate process types
- [`scale-no-daemonize`](references/scale-no-daemonize.md) - Never daemonize or write PID files let process manager handle it
- [`scale-horizontal-not-vertical`](references/scale-horizontal-not-vertical.md) - Design for horizontal scaling over vertical scaling
- [`scale-process-formation`](references/scale-process-formation.md) - Define process formation as declarative configuration

### 8. Disposability (HIGH)

- [`disp-disposable-processes`](references/disp-disposable-processes.md) - Design processes to be disposable started or stopped at any moment
- [`disp-fast-startup`](references/disp-fast-startup.md) - Minimize startup time to enable rapid scaling and recovery
- [`disp-graceful-shutdown`](references/disp-graceful-shutdown.md) - Implement graceful shutdown on SIGTERM
- [`disp-crash-only`](references/disp-crash-only.md) - Design for crash-only software that recovers from sudden death
- [`disp-idempotent-operations`](references/disp-idempotent-operations.md) - Make operations idempotent to safely retry after failures

### 9. Port Binding (MEDIUM)

- [`port-self-contained`](references/port-self-contained.md) - Make the application completely self-contained with embedded server
- [`port-export-via-binding`](references/port-export-via-binding.md) - Export services via port binding using PORT environment variable
- [`port-any-protocol`](references/port-any-protocol.md) - Use port binding to export any protocol not just HTTP

### 10. Dev/Prod Parity (MEDIUM)

- [`parity-minimize-gaps`](references/parity-minimize-gaps.md) - Minimize gaps between development and production environments
- [`parity-same-backing-services`](references/parity-same-backing-services.md) - Use the same type and version of backing services in all environments
- [`parity-deploy-frequently`](references/parity-deploy-frequently.md) - Deploy frequently to minimize the time gap
- [`parity-developers-deploy`](references/parity-developers-deploy.md) - Involve developers in deployment to minimize personnel gap

### 11. Logging (MEDIUM)

- [`log-event-streams`](references/log-event-streams.md) - Treat logs as event streams not files
- [`log-no-routing`](references/log-no-routing.md) - Never route or store logs from within the application
- [`log-structured-format`](references/log-structured-format.md) - Use structured logging for machine-readable event streams
- [`log-unbuffered-stdout`](references/log-unbuffered-stdout.md) - Write logs unbuffered to stdout for real-time streaming

### 12. Admin Processes (MEDIUM)

- [`admin-one-off-processes`](references/admin-one-off-processes.md) - Run admin tasks as one-off processes not special scripts
- [`admin-same-environment`](references/admin-same-environment.md) - Run admin processes against a release with same codebase and config
- [`admin-repl-access`](references/admin-repl-access.md) - Provide REPL access for debugging and data inspection

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
