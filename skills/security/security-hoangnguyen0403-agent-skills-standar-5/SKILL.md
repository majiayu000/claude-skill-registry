---
name: Android Security
description: Standards for Data Encryption, Network Security, and Permissions
metadata:
  labels: [android, security, encryption]
  triggers:
    files: ['network_security_config.xml', 'AndroidManifest.xml']
    keywords:
      [
        'EncryptedSharedPreferences',
        'cleartextTrafficPermitted',
        'intent-filter',
      ]
---

# Android Security Standards

## **Priority: P0 (CRITICAL)**

## Implementation Guidelines

### Data Storage

- **Secrets**: NEVER store API keys in code. Use `EncryptedSharedPreferences` for sensitive local data (Tokens).
- **Keystore**: Use Android Keystore System for cryptographic keys.

### Network

- **HTTPS**: Enforce HTTPS via `network_security_config.xml` (`cleartextTrafficPermitted="false"`).
- **Pinning**: Consider Certificate Pinning for high-security apps.

### Component Export

- **Exported**: Explicitly set `android:exported="false"` for Activities/Receivers unless intended for external use.

## Anti-Patterns

- **No Sensitive Logs**: Strip logs in Release builds.
- **No Homebrew Root Detection**: Use Play Integrity API instead.
- **No Raw URL String Concatenation**: Use `Uri.Builder` or `HttpUrl` (OkHttp) to prevent parameter injection.

## References

- [Setup Examples](references/implementation.md)

## Related Topics

common/security-standards | architecture
