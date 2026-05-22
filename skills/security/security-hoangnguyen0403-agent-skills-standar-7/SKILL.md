---
name: Flutter Security
description: Security standards for Flutter applications based on OWASP Mobile.
metadata:
  labels: [security, owasp, pii, encryption]
  triggers:
    files: ['lib/infrastructure/**', 'pubspec.yaml']
    keywords: [secure_storage, obfuscate, jailbreak, pinning, PII, OWASP]
---

# Mobile Security

## **Priority: P0 (CRITICAL)**

Standards for basic mobile security and PII protection.

## Implementation Guidelines

- **Secure Storage**: Use `flutter_secure_storage` for tokens/PII. Never use `shared_preferences`.
- **Hardcoding**: Never store API keys or secrets in Dart code. Use `--dart-define` or `.env`.
- **Obfuscation**: Always release with `--obfuscate` and `--split-debug-info`. Note: This is a deterrent, not cryptographic protection. For sensitive logic, move to backend.
- **SSL Pinning**: For high-security apps, use `dio_certificate_pinning`.
- **Root Detection**: Use `flutter_jailbreak_detection` for financial/sensitive applications.
- **PII Masking**: Mask sensitive data (email, phone) in logs and analytics.

## Reference & Examples

For SSL Pinning and Secure Storage implementation details:
See [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

common/security-standards | layer-based-clean-architecture | performance
