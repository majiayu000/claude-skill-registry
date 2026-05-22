---
name: deploy-check
description: Validate deployment readiness — Docker, config, health, logging (Marcus Chen's workflow)
disable-model-invocation: true
---

Validate deployment readiness for the project.

Follow Marcus Chen's infrastructure standards:

## 1. Configuration Validation
- Read the config file — verify every setting uses the project's env prefix
- Read the env example file — verify every Settings field is documented
- Verify no hardcoded values in source (search for literal IPs, ports, device IDs)
- Verify no interactive prompts or raw print/console calls anywhere in the source root

## 2. Health Endpoint
- Read the system router — verify the health endpoint returns:
  - `status`: "ok" or "degraded"
  - Connection state of external resource
  - `version`: string
- Verify health bypasses authentication (uses the public DI dependency)
- Verify response uses a typed response model

## 3. Startup & Shutdown
- Read the app factory lifespan handler:
  - Fail-safe operation called on startup (if resource connected)
  - Fail-safe operation called on shutdown (if resource connected)
  - Resource `close()` called on shutdown
  - All events logged with appropriate levels (INFO/WARNING)
- Verify graceful degradation when resource is absent (catches exception, logs warning, continues)

## 4. Docker
- Read the Dockerfile — verify:
  - Multi-stage build (builder + runtime)
  - Non-root user in runtime stage
  - `HEALTHCHECK` instruction present
  - No secrets baked into image
  - `.dockerignore` excludes build artifacts (see stack concepts), .env, .git

## 5. Logging
- Verify structured log format
- Verify no `print()` statements in production code
- Verify no secrets (API keys) logged at any level
- Verify audit logger is used for state changes

## 6. Dependencies
- Read the dependency file (see project config) — verify all deps have minimum versions
- Check for known vulnerabilities with dependency audit command

## 7. Tests
Run the test command and the type-check command (see project config).
Both MUST pass clean.

## Output
Report as: **PASS** / **FAIL** / **WARN** for each section with specific findings.