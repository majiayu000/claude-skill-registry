---
name: cicd-master
description: |
  CI/CD pipeline advisor for GitHub Actions workflows, deployment scripts, and server task scheduling.
  Use when: (1) editing or reviewing .github/workflows/*.yml files, (2) working on deployment scripts
  in bin/, (3) questions about cron jobs or systemd services on local servers, (4) Docker image
  build/push pipelines, (5) security hardening for CI/CD (secrets, permissions, attestations).
  This skill provides advice and reviews - it does not execute server commands.
---

# CI/CD Master

Advisory guidance for robust and secure CI/CD pipelines in the SAPPHIRE project.

**Role:** Review, advise, and suggest improvements. Does not execute server commands directly or indirectly.

## Project CI/CD Architecture

```
Developer → GitHub Actions → Docker Hub → AWS Server → Local Hydromet Servers
              │
              ├── build_test.yml (on push/PR)
              │   └── Test builds, unit tests
              │
              └── deploy_main.yml (on merge to main)
                  └── Build, sign, push images with attestations
```

## GitHub Actions Security Checklist

When reviewing or editing workflow files, verify:

- [ ] Pinned action versions (`@v4` not `@main`)
- [ ] Minimal `permissions:` scope (prefer `read` over `write`)
- [ ] Secrets via `${{ secrets.* }}` never hardcoded
- [ ] No command injection via `${{ github.event.* }}` in `run:`
- [ ] Timeout set for long-running jobs (`timeout-minutes:`)
- [ ] Concurrency controls for expensive jobs

## Current Security Features

| Feature | Status | Purpose |
|---------|--------|---------|
| SLSA Provenance | Enabled | Supply chain attestation |
| SBOM Generation | Enabled | Software Bill of Materials |
| Cosign Signing | Enabled | Image signature verification |
| Non-root User | In images | Container security |
| Pinned Actions | Yes | Reproducible builds |

## Workflow Best Practices

### Job Dependencies
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
  build:
    needs: test  # Only runs if test passes
```

### Disk Space for Large Builds
ML image builds (~4GB) need disk cleanup:
```yaml
- name: Free disk space
  run: |
    sudo rm -rf /usr/share/dotnet
    sudo rm -rf /opt/ghc
    sudo rm -rf /usr/local/share/boost
    sudo rm -rf /usr/local/lib/android
```

### Supply Chain Security
```yaml
- uses: docker/build-push-action@v6
  with:
    provenance: true
    sbom: true
```

## Deployment Script Review (bin/)

When reviewing scripts in `bin/`, check for:

- Proper error handling (`set -e` or equivalent)
- No hardcoded credentials (use environment variables)
- Logging for debugging
- Idempotency (safe to run multiple times)
- Clear documentation of prerequisites

## Task Scheduling Guidance

### Cron Syntax Reference
```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *

# Examples
0 6 * * *    # Daily at 6:00 AM
0 */6 * * *  # Every 6 hours
0 6 1 * *    # First day of month at 6:00 AM
```

### Systemd Timers (recommended over cron)
- More reliable with `Persistent=true` (runs missed jobs)
- Better logging via `journalctl`
- Dependency management with other services

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Build timeout | Add `timeout-minutes: 60` |
| ML build fails | Add disk cleanup step |
| Docker rate limits | Use authenticated pulls |
| Workflow not triggering | Check `on:` triggers and branch rules |
