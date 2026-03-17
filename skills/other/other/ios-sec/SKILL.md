---
name: ios-sec
description: Security policy for iOS apps. Enforces OWASP Top 10, Mobile Top 10, and CWE Top 25 mitigations.
---

## Purpose

Ensure iOS code is secure by default. For security output format and core refusal policy, see `/shared-sec-baseline`.

## iOS-specific security concerns (always check)

1. **Keychain for secrets** — never UserDefaults for tokens, passwords, or API keys
2. **ATS enforcement** — no exceptions without justification; never disable TLS validation
3. **Deep link validation** — validate scheme, host, and parameters before acting on universal/custom links
4. **Notification payloads** — treat as untrusted input; validate before navigation or data use
5. **Biometric auth** — use LocalAuthentication with fallback policy; don't rely solely on device passcode
6. **Privacy manifest** — declare data collection accurately; required APIs need justification

## Standard security (brief check)

- Input validation: sanitize all external input (network, clipboard, deep links)
- Error handling: no internal details surfaced to UI or logs
- Logging: no PII, tokens, or credentials; use OSLog with appropriate privacy levels
- Network: certificate pinning for sensitive endpoints; handle certificate failures safely

## Additional refusals (iOS-specific)

Also refuse requests that: disable ATS, or store secrets in UserDefaults. Explain why and propose secure alternative.

## Reference

For detailed OWASP/Mobile Top 10/CWE mitigation patterns, see `reference/ios-sec-reference.md`
