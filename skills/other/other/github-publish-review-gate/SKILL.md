---
name: "github-publish-review-gate"
description: "How to gate a public GitHub README and repo handoff without misrepresenting build or runtime requirements"
domain: "testing"
confidence: "medium"
source: "hicks-github-publish-gate"
---

## Context

Use this when a local product repo is being prepared for a public GitHub push and the slice includes a new root README, packaging/install guidance, or a first-time public handoff.

## Pattern

1. **Start with the public truth surface**
   - Require a root `README.md`.
   - Check that the README describes the actual product shape, supported platforms, and core workflows already implemented in the repo.

2. **Split contributor prerequisites from runtime prerequisites**
   - Contributor setup covers SDKs, package managers, and optional packaging tools.
   - End-user runtime covers only what is needed to launch/install the shipped app.
   - Framework-dependent desktop installers need this separation explicitly or the README will overstate or understate what users need.

3. **Make the handoff discoverable**
   - A first-time visitor should be able to find what the app is, how to build/test it, and where the install/release path lives.
   - Require an explicit license posture and a discoverable public destination or release story.

4. **Do a publish-blocker sweep**
   - Check for accidental editor junk, local agent state, generated output, and test scratch files.
   - Treat missing README, missing license posture, or missing public destination as blockers until resolved or consciously scoped.

## Anti-Patterns

- Approving because the PRD or internal docs are accurate while the public README is still absent or vague
- Claiming installer simplicity without naming framework-dependent runtime requirements
- Telling end users to install contributor tools like Node.js or WiX just to run the app
- Publishing a repo publicly with no license stance and no clear release/install entry point
