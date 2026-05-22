---
name: security-risk
description: "Combine security scanning and threat modeling for changes involving data handling, API interception, sync, storage, authentication, or encryption."
license: MIT
tags:
  - security
  - privacy
  - threat-modeling
allowed-tools:
  - bash
  - git
  - markdown
metadata:
  author: laurenceputra
  version: 1.0.0
---

# Security Risk

Identify security and privacy risks and propose mitigations.

## Workflow
1. Review data flows and trust boundaries.
2. Scan for injection, logging, and auth risks.
3. Summarize risks and mitigations.

## Output Format
- Risks identified
- Mitigations
- Residual risk

## References
- [Threat modeling worksheet](references/threat-model.md)
