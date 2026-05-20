---
name: ios-nfr
description: Non-functional requirements checklist for iOS features
---

## Purpose

Ensure iOS stories address NFRs. Complement security policies and stack conventions.

## iOS-specific concerns (always consider)

1. **App Store readiness** — permission purpose strings, entitlement/capability changes documented
2. **Battery** — no high-frequency polling; efficient image handling
3. **Offline correctness** — local persistence as source of truth; migration plan for schema changes; bounded storage growth
4. **Accessibility** — accessible labels on controls; dynamic type doesn't break layouts; adequate tap targets
5. **Performance** — no main-thread blocking; smooth scrolling; network calls don't block UI

For standard concerns, output format, and flexibility rules, see `/shared-nfr`.

### iOS-specific standard concern additions

- Reliability: failure states handled gracefully
- Security: appropriate storage for sensitive values (keychain when needed)
- Observability: critical transitions logged with stable identifiers
