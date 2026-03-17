---
name: iOS Security
description: Standards for Keychain, Biometrics, and Data Protection.
metadata:
  labels: [ios, security, keychain, encryption]
  triggers:
    files: ['**/*.swift']
    keywords:
      [SecItemAdd, kSecClassGenericPassword, LAContext, LocalAuthentication]
---

# iOS Security Standards

## **Priority: P0 (CRITICAL)**

## Implementation Guidelines

### Key Storage

- **Keychain**: Use for sensitive tokens, passwords, and identifiers (UUIDs). Never store in `UserDefaults`.
- **Valet**: Use high-level wrappers like SwiftKeychainWrapper or Valet to avoid raw Security.framework C-APIs.
- **Biometrics**: Use `LocalAuthentication` for FaceID/TouchID. Verify availability with `canEvaluatePolicy(_:error:)` before evaluation.

### Data Protection

- **File Encryption**: Use `Data.WritingOptions.completeFileProtection` when saving files to disk.
- **App Sandboxing**: Respect the sandbox; do not attempt to access files outside of your container.

### Network Security

- **ATS**: Don't disable App Transport Security (ATS) globally in `Info.plist`. Use exceptions only if strictly necessary.
- **SSL Pinning**: Use TrustKit or Alamofire pinning for backend-critical applications.

## Anti-Patterns

- **UserDefaults for Secrets**: `**No Secrets in UserDefaults**: Use Keychain.`
- **Ignoring LA Error Handles**: `**Handle LAError**: Check for userCancel, authenticationFailed, etc.`
- **Print Tokens**: `**No logging of PII/Tokens**: Ensure logs are stripped in Release builds.`

## References

- [Keychain & Biometrics Implementation](references/implementation.md)

## Related Topics

common/security-standards | architecture
