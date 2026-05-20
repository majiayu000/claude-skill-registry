---
name: shared-nfr
description: Standard NFR concerns, output format, and flexibility rules shared across all platforms.
---

## Purpose

Define the common NFR evaluation framework. Platform NFR skills reference this for standard concerns, output format, and flexibility — then add platform-specific concerns.

## Standard concerns (brief check)

- Performance: response time and payload size targets
- Reliability: error handling strategy and user-facing failure modes
- Security/privacy: align with security policy; no PII in logs
- Observability: key events logged, metrics for latency/errors
- Accessibility: keyboard nav, semantic markup, color contrast (UI changes)
- **Testability:** TDD is mandatory — see `/shared-tdd`

## Output

Include an **NFR notes** section with:

- Decisions for relevant concerns (1-2 sentences each)
- Items marked "n/a" with brief reason
- If an NFR significantly changes scope, propose minimal-now + hardening-later

## Flexibility

- "Prototype" requests may relax targets if tradeoffs documented
- Don't invent elaborate SLOs unless user specifies stricter requirements
