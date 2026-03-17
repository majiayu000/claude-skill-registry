---
name: shared-sec-baseline
description: Security output format, core refusal policy, and purpose statement shared across all platforms.
---

## Purpose

Ensure code is secure by default. Refuse insecure implementations and propose alternatives. Platform security skills reference this for output format and refusal policy, then add platform-specific concerns.

## Output

For security-relevant changes, include brief **security notes**:

- Which concerns were addressed
- Items marked "n/a" with one-line reason
- Residual risks and mitigations if any

## Refusals

Refuse requests that:

- Bypass TLS validation
- Add backdoors or secret access mechanisms
- Log credentials, tokens, or secrets
- Disable authorization checks
- Weaken existing security controls

Explain why and propose a secure alternative.

Platform security skills may add platform-specific refusals (e.g., disabling ATS, storing secrets in UserDefaults).
