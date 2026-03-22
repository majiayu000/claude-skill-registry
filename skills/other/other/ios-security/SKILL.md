---
name: ios-security
description: "Secure iOS apps with Keychain Services, CryptoKit encryption, biometric authentication (Face ID, Touch ID), Secure Enclave key storage, LAContext, App Transport Security (ATS), certificate pinning, data protection classes, and secure coding patterns. Use when implementing app security features, auditing privacy manifests, configuring App Transport Security, securing keychain access, adding biometric authentication, or encrypting sensitive data with CryptoKit."
---

# iOS Security

Guidance for handling sensitive data, authenticating users, encrypting
correctly, and following Apple's security best practices on iOS.

## Contents

- [Keychain Services](#keychain-services)
- [Data Protection](#data-protection)
- [CryptoKit](#cryptokit)
- [Secure Enclave](#secure-enclave)
- [Biometric Authentication](#biometric-authentication)
- [App Transport Security (ATS)](#app-transport-security-ats)
- [Certificate Pinning](#certificate-pinning)
- [Secure Coding Patterns](#secure-coding-patterns)
- [Privacy Manifests](#privacy-manifests)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Keychain Services

The Keychain is the ONLY correct place to store sensitive data. Never store
passwords, tokens, API keys, or secrets in UserDefaults, files, or Core Data.

### Storing Credentials

```swift
func saveToKeychain(account: String, data: Data, service: String) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service,
        kSecValueData as String: data,
        kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
    ]

    let status = SecItemAdd(query as CFDictionary, nil)

    if status == errSecDuplicateItem {
        let updateQuery: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: account,
            kSecAttrService as String: service
        ]
        let updates: [String: Any] = [kSecValueData as String: data]
        let updateStatus = SecItemUpdate(updateQuery as CFDictionary, updates as CFDictionary)
        guard updateStatus == errSecSuccess else {
            throw KeychainError.updateFailed(updateStatus)
        }
    } else if status != errSecSuccess {
        throw KeychainError.saveFailed(status)
    }
}
```

### Reading Credentials

```swift
func readFromKeychain(account: String, service: String) throws -> Data {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service,
        kSecReturnData as String: true,
        kSecMatchLimit as String: kSecMatchLimitOne
    ]

    var result: AnyObject?
    let status = SecItemCopyMatching(query as CFDictionary, &result)

    guard status == errSecSuccess, let data = result as? Data else {
        throw KeychainError.readFailed(status)
    }
    return data
}
```

### Deleting Credentials

```swift
func deleteFromKeychain(account: String, service: String) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: account,
        kSecAttrService as String: service
    ]

    let status = SecItemDelete(query as CFDictionary)
    guard status == errSecSuccess || status == errSecItemNotFound else {
        throw KeychainError.deleteFailed(status)
    }
}
```

### kSecAttrAccessible Values

| Value | When Available | Device-Only | Use For |
|---|---|---|---|
| `kSecAttrAccessibleWhenUnlocked` | Device unlocked | No | General credentials |
| `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` | Device unlocked | Yes | Sensitive credentials |
| `kSecAttrAccessibleAfterFirstUnlock` | After first unlock | No | Background-accessible tokens |
| `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` | After first unlock | Yes | Background tokens, no backup |
| `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` | Passcode set + unlocked | Yes | Highest security |

Rules:
- Use `ThisDeviceOnly` variants for sensitive data. Prevents backup/restore to other devices.
- Use `AfterFirstUnlock` for tokens needed by background operations.
- Use `WhenPasscodeSetThisDeviceOnly` for most sensitive data. Item is deleted if passcode is removed.
- NEVER use `kSecAttrAccessibleAlways` (deprecated and insecure).

### Keychain Access Groups

Share keychain items across apps from the same team:

```swift
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "shared-token",
    kSecAttrAccessGroup as String: "TEAMID.com.company.shared"
]
```

### @AppStorage vs Keychain

| Storage | Use For | Security |
|---------|---------|----------|
| `@AppStorage` / `UserDefaults` | Non-sensitive preferences (theme, onboarding state, feature flags) | Not encrypted at rest |
| Keychain | Passwords, tokens, API keys, secrets | Hardware-encrypted, access-controlled |

**Rule:** If the data would be embarrassing or dangerous if exposed, it goes in Keychain. Everything else can use `@AppStorage`.

```swift
// Non-sensitive preference -- @AppStorage is fine
@AppStorage("hasCompletedOnboarding") private var hasOnboarded = false

// Sensitive credential -- MUST use Keychain
// WRONG: @AppStorage("authToken") private var token = ""
// CORRECT: Use saveToKeychain(account:data:service:)
```

## Data Protection

iOS encrypts files based on their protection class:

| Class | When Available | Use For |
|---|---|---|
| `.complete` | Only when unlocked | Sensitive user data |
| `.completeUnlessOpen` | Open handles survive lock | Active downloads, recordings |
| `.completeUntilFirstUserAuthentication` | After first unlock (default) | Most app data |
| `.none` | Always | Non-sensitive, system-needed data |

```swift
// Set file protection
try data.write(to: url, options: .completeFileProtection)

// Check protection level
let attributes = try FileManager.default.attributesOfItem(atPath: path)
let protection = attributes[.protectionKey] as? FileProtectionType
```

Use `.complete` for any file containing user-sensitive data. The default
`.completeUntilFirstUserAuthentication` is acceptable for general app data.

## CryptoKit

Use CryptoKit for all cryptographic operations. Do not use CommonCrypto or the
raw Security framework for new code.

### Symmetric Encryption (AES-GCM)

```swift
import CryptoKit

let key = SymmetricKey(size: .bits256)

func encrypt(_ data: Data, using key: SymmetricKey) throws -> Data {
    let sealed = try AES.GCM.seal(data, using: key)
    guard let combined = sealed.combined else {
        throw CryptoError.sealFailed
    }
    return combined
}

func decrypt(_ data: Data, using key: SymmetricKey) throws -> Data {
    let box = try AES.GCM.SealedBox(combined: data)
    return try AES.GCM.open(box, using: key)
}
```

### Hashing

```swift
let hash = SHA256.hash(data: data)
let hashString = hash.compactMap { String(format: "%02x", $0) }.joined()

// Also available: SHA384, SHA512
```

### HMAC (Message Authentication)

```swift
let key = SymmetricKey(size: .bits256)

// Sign
let signature = HMAC<SHA256>.authenticationCode(for: data, using: key)

// Verify
let isValid = HMAC<SHA256>.isValidAuthenticationCode(signature, authenticating: data, using: key)
```

For digital signatures (P256/ECDSA), key agreement (Curve25519), ChaChaPoly,
and HKDF key derivation, see `references/cryptokit-advanced.md`.

## Secure Enclave

For the highest security, store keys in the Secure Enclave. Keys never leave
the hardware. Only P256 is supported.

```swift
guard SecureEnclave.isAvailable else { return }

let accessControl = SecAccessControlCreateWithFlags(
    nil, kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    [.privateKeyUsage, .biometryCurrentSet], nil
)!
let privateKey = try SecureEnclave.P256.Signing.PrivateKey(accessControl: accessControl)

let signature = try privateKey.signature(for: data)  // May trigger biometric prompt
let isValid = privateKey.publicKey.isValidSignature(signature, for: data)

// Persist: store dataRepresentation in Keychain, restore with:
let restored = try SecureEnclave.P256.Signing.PrivateKey(
    dataRepresentation: privateKey.dataRepresentation
)
```

## Biometric Authentication

This section covers biometric protection for Keychain items and data
access. For user-facing biometric sign-in flows (`LAContext.evaluatePolicy`
as a login mechanism), see the `authentication` skill.

### LocalAuthentication (Face ID / Touch ID)

```swift
import LocalAuthentication

func authenticateWithBiometrics() async throws -> Bool {
    let context = LAContext()
    var error: NSError?

    guard context.canEvaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics, error: &error
    ) else {
        // Biometrics not available -- fall back to passcode
        if context.canEvaluatePolicy(.deviceOwnerAuthentication, error: &error) {
            return try await context.evaluatePolicy(
                .deviceOwnerAuthentication,
                localizedReason: "Authenticate to access your account"
            )
        }
        throw AuthError.biometricsUnavailable
    }

    return try await context.evaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics,
        localizedReason: "Authenticate to access your account"
    )
}
```

### Info.plist Requirement

You MUST include `NSFaceIDUsageDescription` in Info.plist:

```xml
<key>NSFaceIDUsageDescription</key>
<string>Authenticate to access your secure data</string>
```

Missing this key causes a crash on Face ID devices.

### LAContext Configuration

```swift
let context = LAContext()
context.localizedFallbackTitle = "Use Passcode"
context.touchIDAuthenticationAllowableReuseDuration = 30
let currentState = context.evaluatedPolicyDomainState // Compare to detect enrollment changes
```

### Biometric + Keychain

Protect keychain items with biometric access:

```swift
let access = SecAccessControlCreateWithFlags(
    nil,
    kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    .biometryCurrentSet,
    nil
)!

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "auth-token",
    kSecValueData as String: tokenData,
    kSecAttrAccessControl as String: access,
    kSecUseAuthenticationContext as String: LAContext()
]
```

SecAccessControl flags:
- `.biometryCurrentSet` -- Requires biometry, invalidated if enrollment changes. Most secure.
- `.biometryAny` -- Requires biometry, survives enrollment changes.
- `.userPresence` -- Biometry or passcode. Most flexible.

## App Transport Security (ATS)

ATS enforces HTTPS by default. Do NOT disable it.

### What ATS Requires

- TLS 1.2 or later
- Forward secrecy cipher suites
- SHA-256 or better certificates
- 2048-bit or greater RSA keys (or 256-bit ECC)

### Exception Domains (Last Resort)

```xml
<!-- Only for legacy servers you cannot upgrade -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSExceptionDomains</key>
    <dict>
        <key>legacy-api.example.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
            <key>NSExceptionMinimumTLSVersion</key>
            <string>TLSv1.2</string>
        </dict>
    </dict>
</dict>
```

Rules:
- NEVER set `NSAllowsArbitraryLoads` to true. Apple will reject the app.
- Exception domains require justification in App Review notes.
- Use exception domains only for third-party servers you cannot control.

## Certificate Pinning

Pin certificates for sensitive API connections to prevent MITM attacks.

### URLSession Delegate Pinning

```swift
import CryptoKit

class PinnedSessionDelegate: NSObject, URLSessionDelegate {
    // SHA-256 hash of the certificate's Subject Public Key Info
    private let pinnedHashes: Set<String> = [
        "base64EncodedSHA256HashOfSPKI=="
    ]

    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge
    ) async -> (URLSession.AuthChallengeDisposition, URLCredential?) {
        guard let trust = challenge.protectionSpace.serverTrust,
              let chain = SecTrustCopyCertificateChain(trust) as? [SecCertificate],
              let certificate = chain.first else {
            return (.cancelAuthenticationChallenge, nil)
        }

        guard let publicKey = SecCertificateCopyKey(certificate),
              let publicKeyData = SecKeyCopyExternalRepresentation(
                  publicKey, nil
              ) as Data? else {
            return (.cancelAuthenticationChallenge, nil)
        }

        let hash = SHA256.hash(data: publicKeyData)
        let hashString = Data(hash).base64EncodedString()

        if pinnedHashes.contains(hashString) {
            return (.useCredential, URLCredential(trust: trust))
        }

        return (.cancelAuthenticationChallenge, nil)
    }
}
```

Rules:
- Pin the public key hash, not the certificate. Certificates rotate; public keys are more stable.
- Always include at least one backup pin.
- Have a rotation plan. If all pinned keys expire, the app cannot connect.
- Consider a kill switch (remote config to disable pinning in emergency).

## Secure Coding Patterns

### Never Log Sensitive Data

```swift
// WRONG
logger.debug("User logged in with token: \(token)")

// CORRECT
logger.debug("User logged in successfully")
```

### Clear Sensitive Data From Memory

```swift
var sensitiveData = Data(/* ... */)
defer {
    sensitiveData.resetBytes(in: 0..<sensitiveData.count)
}
```

### Validate All Input

```swift
guard let url = URL(string: input),
      ["https"].contains(url.scheme?.lowercased()) else {
    throw SecurityError.invalidURL
}
let resolved = url.standardized.path
guard resolved.hasPrefix(allowedDirectory.path) else {
    throw SecurityError.pathTraversal
}
```

### API Key Placeholder Pattern

Use `#error` to prevent accidental commits of placeholder API keys:

```swift
// Forces a build error until the real key is configured
#error("Add your API key to Secrets.plist -- see README for setup")
private let apiKey = Secrets.value(for: "API_KEY")
```

### Jailbreak Detection

Check for known jailbreak file paths (`/Applications/Cydia.app`, `/usr/sbin/sshd`, etc.) and sandbox escape. Jailbreak detection is not foolproof -- use it as one layer, not the only layer. See `references/cryptokit-advanced.md` for full implementation.

## Privacy Manifests

Apps and SDKs must declare data access in `PrivacyInfo.xcprivacy`. See
`references/privacy-manifest.md` for required-reason API declarations and
security-related data collection details. For submission requirements and
compliance checklists, see `references/app-review-guidelines.md`.

## Common Mistakes

1. **Storing secrets in UserDefaults.** Tokens, passwords, API keys must go in Keychain.
2. **Hardcoded secrets in source.** No API keys or credentials in Swift files.
3. **Disabling ATS globally.** `NSAllowsArbitraryLoads = true` is a rejection risk.
4. **Logging sensitive data.** Never log tokens, passwords, or API keys.
5. **Missing PrivacyInfo.xcprivacy.** Required for all apps using required-reason APIs.
6. **Using CommonCrypto instead of CryptoKit.** CryptoKit is safer and modern.
7. **Missing NSFaceIDUsageDescription.** Crashes on Face ID devices.
8. **Using `.biometryAny` when `.biometryCurrentSet` is needed.** The former survives enrollment changes, which may be undesirable for high-security items.
9. **Path traversal vulnerabilities.** Always resolve and validate paths.
10. **Missing concurrency annotations.** Ensure Keychain wrapper types are Sendable; isolate UI-facing security prompts to `@MainActor`.

## Review Checklist

- [ ] Secrets in Keychain, not UserDefaults or files; no hardcoded credentials
- [ ] Correct `kSecAttrAccessible` value; `ThisDeviceOnly` for non-backup data
- [ ] File protection class set for sensitive files (`.complete`)
- [ ] CryptoKit for encryption (not CommonCrypto); 256-bit symmetric keys
- [ ] Keys stored in Keychain or Secure Enclave
- [ ] Biometric auth with fallback; `NSFaceIDUsageDescription` in Info.plist
- [ ] Correct `SecAccessControl` flags; `LAContext` configured
- [ ] HTTPS enforced; no `NSAllowsArbitraryLoads`; cert pinning for sensitive APIs
- [ ] PrivacyInfo.xcprivacy present; all required-reason APIs declared
- [ ] No sensitive data in logs; Data cleared after use; URLs/paths validated

## References

- CryptoKit advanced patterns: `references/cryptokit-advanced.md`
- Privacy manifest guide: `references/privacy-manifest.md`
- App Review security guidelines: `references/app-review-guidelines.md`
- File storage directory guide and protection: `references/file-storage-patterns.md`

