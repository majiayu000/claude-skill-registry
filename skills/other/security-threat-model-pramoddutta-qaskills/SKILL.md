---
name: "Security Threat Modeling"
description: "Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations to produce actionable AppSec-grade threat models."
version: 1.0.0
author: openai
license: MIT
tags: [threat-model, security, appsec, trust-boundaries, abuse-paths]
testingTypes: [security]
frameworks: []
languages: [python, typescript, javascript, go, java]
domains: [web, api, backend, infrastructure]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Security Threat Modeling

Deliver an actionable AppSec-grade threat model specific to the repository, not a generic checklist. Anchor every architectural claim to evidence in the repo and keep assumptions explicit. Prioritize realistic attacker goals and concrete impacts.

## Workflow

### 1. Scope and Extract the System Model

- Identify primary components, data stores, and external integrations from the repo
- Identify how the system runs (server, CLI, library, worker) and its entrypoints
- Separate runtime behavior from CI/build/dev tooling and from tests/examples
- Map in-scope locations and exclude out-of-scope items explicitly
- Do not claim components, flows, or controls without evidence

### 2. Derive Boundaries, Assets, and Entry Points

- Enumerate trust boundaries as concrete edges between components
- Note protocol, auth, encryption, validation, and rate limiting at each boundary
- List assets that drive risk: data, credentials, models, config, compute resources, audit logs
- Identify entry points: endpoints, upload surfaces, parsers, job triggers, admin tooling

### 3. Calibrate Attacker Capabilities

- Describe realistic attacker capabilities based on exposure and intended usage
- List assets that drive risk: credentials, PII, integrity-critical state, availability
- Explicitly note non-capabilities to avoid inflated severity

### 4. Enumerate Threats as Abuse Paths

- Map attacker goals to assets and boundaries
- Focus on: exfiltration, privilege escalation, integrity compromise, denial of service
- Classify each threat and tie it to impacted assets
- Keep the number of threats small but high quality

### 5. Prioritize with Explicit Reasoning

- Use qualitative likelihood and impact (low/medium/high) with short justifications
- Set overall priority (critical/high/medium/low) using likelihood x impact
- State which assumptions most influence the ranking

### 6. Validate with the User

- Summarize key assumptions that affect threat ranking or scope
- Ask 1-3 targeted questions to resolve missing context
- Pause and wait for user feedback before producing the final report

### 7. Recommend Mitigations

- Distinguish existing mitigations (with evidence) from recommended mitigations
- Tie mitigations to concrete locations and control types
- Prefer specific implementation hints over generic advice

### 8. Quality Check

- Confirm all entrypoints are covered
- Confirm each trust boundary is represented in threats
- Confirm runtime vs CI/dev separation
- Write the final Markdown to `<repo-name>-threat-model.md`

## Risk Prioritization Guidance

- **High:** Pre-auth RCE, auth bypass, cross-tenant access, sensitive data exfiltration, key/token theft, sandbox escape
- **Medium:** Targeted DoS, partial data exposure, rate-limit bypass, log poisoning
- **Low:** Low-sensitivity info leaks, noisy DoS with easy mitigation, unlikely preconditions
