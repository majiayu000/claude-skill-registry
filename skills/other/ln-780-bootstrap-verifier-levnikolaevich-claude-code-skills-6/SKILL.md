---
name: ln-780-bootstrap-verifier
description: Orchestrates final verification - build, test, and container health checks
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-780-bootstrap-verifier

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

---

## Purpose

Orchestrates the final bootstrap verification pipeline by delegating to specialized workers and aggregating results into a comprehensive report.

**Scope:**
- Coordinates build, test, and container verification
- Aggregates results from all workers
- Generates final verification report

**Out of Scope:**
- Direct execution of builds/tests/containers (delegated to workers)
- Project structure creation (handled by earlier phases)

---

## When to Use

| Scenario | Use This Skill |
|----------|---------------|
| After ln-700 completes project setup | Yes |
| Standalone build verification | No, use ln-781 directly |
| Manual testing only | No, use ln-782 directly |
| Container-only launch | No, use ln-783 directly |

---

## Workflow

### Phase 1: Pre-flight Checks

Verify environment readiness before starting verification pipeline.

| Check | Detection Method | Failure Action |
|-------|-----------------|----------------|
| Docker installed | Check docker command availability | Report error, skip container phase |
| Docker Compose | Check docker compose version | Report error, skip container phase |
| Project structure | Scan for package.json, *.csproj, docker-compose.yml | Adapt workflow to detected components |
| Port availability | Check if required ports are free | Warn user, suggest alternatives |

### Phase 2: Build Verification

Delegate to **ln-781-build-verifier**.

- Pass detected project types
- Collect build results (status, duration, output paths)
- On failure: collect error logs, proceed to report (skip test/container phases)

### Phase 3: Test Verification

Delegate to **ln-782-test-runner**.

- Pass build results for context
- Collect test results (total, passed, failed, duration)
- On failure: collect failure details, optionally continue to container phase

### Phase 4: Container Launch

Delegate to **ln-783-container-launcher**.

- Pass project configuration
- Collect container status and health check results
- On failure: collect container logs

### Phase 5: Report Generation

Aggregate all results into final verification report.

**Report Sections:**
| Section | Content |
|---------|---------|
| Build Results | Status, duration, output paths per project |
| Test Results | Total, passed, failed counts per suite |
| Container Status | Name, status, port, health per container |
| Health Checks | URL, status code, response time per endpoint |
| Next Steps | Actionable items for user |

---

## Worker Invocation

Use Skill tool to delegate work:

| Worker | Invocation | Data Passed |
|--------|------------|-------------|
| ln-781-build-verifier | `Skill: ln-781-build-verifier` | Detected project types |
| ln-782-test-runner | `Skill: ln-782-test-runner` | Build status, skip flag |
| ln-783-container-launcher | `Skill: ln-783-container-launcher` | Compose file path |

**Sequential execution required:** Build -> Test -> Container

---

## Critical Rules

1. **Never execute builds/tests/containers directly** - always delegate to workers
2. **Fail-fast on build errors** - skip test and container phases
3. **Always generate report** - even on failure, include collected data
4. **Pre-flight checks first** - detect environment issues before starting

---

## Options

| Option | Default | Description |
|--------|---------|-------------|
| runTests | true | Execute test phase |
| skipTestsOnFailure | false | Continue to container phase if tests fail |
| startContainers | true | Execute container phase |
| keepContainersRunning | true | Leave containers running after verification |
| healthCheckTimeout | 120 | Max seconds to wait for healthy containers |

---

## Definition of Done

- [ ] All detected project types built successfully
- [ ] All test suites executed (if enabled)
- [ ] All containers healthy (if enabled)
- [ ] Verification report generated and displayed to user
- [ ] Next steps provided

---

## Reference Files

- Worker: `../ln-781-build-verifier/SKILL.md`
- Worker: `../ln-782-test-runner/SKILL.md`
- Worker: `../ln-783-container-launcher/SKILL.md`

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
