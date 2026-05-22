---
name: security-best-practices
description: "Expert security decisions for iOS/tvOS: when Keychain vs UserDefaults, certificate pinning trade-offs, API key protection strategies, and secure data lifecycle management. Use when storing sensitive data, implementing authentication, or hardening app security. Trigger keywords: Keychain, security, certificate pinning, encryption, API key, token storage, secure storage, biometric, jailbreak, data protection"
version: "3.0.0"
---

# Security Best Practices — Expert Decisions

Expert decision frameworks for iOS security choices. Claude knows Keychain APIs — this skill provides judgment calls for when security measures add value and implementation trade-offs.

---

## Decision Trees

### Storage Selection

```
What type of data?
├─ Credentials (passwords, tokens, secrets)
│  └─ Keychain (always)
│     kSecAttrAccessibleAfterFirstUnlock typical
│
├─ User preferences
│  └─ Is it sensitive? (e.g., PIN enabled)
│     ├─ YES → Keychain
│     └─ NO → UserDefaults is fine
│
├─ Large sensitive files
│  └─ File system + Data Protection
│     .completeFileProtection option
│
└─ Non-sensitive app state
   └─ UserDefaults or files
      No special protection needed
```

### Certificate Pinning Decision

```
What's your threat model?
├─ Consumer app, standard security
│  └─ Trust system CA validation
│     ATS (App Transport Security) is sufficient
│
├─ Financial/healthcare/enterprise
│  └─ Pin certificates
│     But plan for rotation!
│
├─ High-value target (banking, crypto)
│  └─ Pin public key (not certificate)
│     Survives cert renewal
│
└─ Internal enterprise app
   └─ May need custom CA trust
      ServerTrustManager with custom evaluator
```

**The trap**: Pinning without rotation plan. When cert expires, app stops working.

### API Key Protection Strategy

```
Who controls the server?
├─ You control backend
│  └─ Don't embed API keys in app
│     Authenticate users, server makes API calls
│
├─ Third-party API, user-specific
│  └─ OAuth flow
│     User authenticates, gets their own token
│
└─ Third-party API, app-level key
   └─ Is key truly needed client-side?
      ├─ NO → Proxy through your backend
      └─ YES → Obfuscate + attestation
         Accept risk of extraction
```

### Keychain Access Level

```
When does data need to be accessible?
├─ Only when device unlocked
│  └─ kSecAttrAccessibleWhenUnlocked
│     Most secure for user-facing data
│
├─ Background refresh needed
│  └─ kSecAttrAccessibleAfterFirstUnlock
│     Accessible after first unlock until reboot
│
├─ Shared across apps (same team)
│  └─ kSecAttrAccessGroup + appropriate access level
│
└─ Must survive device restore
   └─ kSecAttrSynchronizable = true
      Syncs via iCloud Keychain
```

---

## NEVER Do

### Storage Mistakes

**NEVER** store credentials in UserDefaults:
```swift
// ❌ UserDefaults is NOT encrypted
UserDefaults.standard.set(token, forKey: "authToken")
// Readable with device backup, jailbreak, or debugging

// ✅ Always use Keychain for credentials
try KeychainManager.save(key: "authToken", data: tokenData)
```

**NEVER** hardcode secrets in code:
```swift
// ❌ Compiled into binary — trivially extractable
let apiKey = "sk_live_abc123xyz789"

// ❌ Still in binary as string
let apiKey = String(format: "%@%@", "sk_live_", "abc123xyz789")

// ✅ Fetch from secure backend after authentication
let apiKey = try await secureConfigService.getAPIKey()

// Or at minimum, obfuscate + accept risk
let apiKey = Obfuscator.decode(encodedKey)
```

**NEVER** log sensitive data:
```swift
// ❌ Logs are accessible and persisted
print("User token: \(token)")
logger.debug("Password: \(password)")

// ✅ Never log credentials
logger.info("User authenticated successfully")

// If debugging, redact
#if DEBUG
logger.debug("Token: \(String(repeating: "*", count: token.count))")
#endif
```

### Keychain Mistakes

**NEVER** use kSecAttrAccessibleAlways:
```swift
// ❌ Accessible even before device unlocked — rarely needed
let query: [String: Any] = [
    kSecAttrAccessible as String: kSecAttrAccessibleAlways
]

// ✅ Use appropriate access level
let query: [String: Any] = [
    kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock
]
```

**NEVER** ignore Keychain errors:
```swift
// ❌ Silently fails — credential may not be saved
_ = SecItemAdd(query as CFDictionary, nil)

// ✅ Check status and handle errors
let status = SecItemAdd(query as CFDictionary, nil)
guard status == errSecSuccess else {
    throw KeychainError.saveFailed(status)
}
```

### Certificate Pinning Mistakes

**NEVER** pin without expiration handling:
```swift
// ❌ App breaks when certificate expires
let pinnedCert = loadBundledCertificate()
if serverCert != pinnedCert {
    completionHandler(.cancelAuthenticationChallenge, nil)
}

// ✅ Pin public key (survives renewal) or have rotation plan
let pinnedPublicKey = loadBundledPublicKey()
let serverPublicKey = extractPublicKey(from: serverCert)
if pinnedPublicKey != serverPublicKey {
    completionHandler(.cancelAuthenticationChallenge, nil)
}
```

**NEVER** disable ATS for convenience:
```swift
// ❌ Disables all transport security
// Info.plist
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>  <!-- NEVER in production -->
</dict>

// ✅ Only exception if absolutely needed, with justification
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
```

### Memory Safety

**NEVER** keep credentials in memory longer than needed:
```swift
// ❌ Password stays in memory
class LoginManager {
    var currentPassword: String?  // May persist in memory
}

// ✅ Clear sensitive data immediately after use
func authenticate(password: String) async throws {
    defer {
        // Can't truly clear String, but can clear Data
        // For true secure handling, use Data and zero it
    }
    let result = try await authService.login(password: password)
}
```

---

## Essential Patterns

### Keychain Manager

```swift
final class KeychainManager {
    enum KeychainError: Error {
        case itemNotFound
        case duplicateItem
        case unexpectedStatus(OSStatus)
    }

    static func save(key: String, data: Data, accessibility: CFString = kSecAttrAccessibleAfterFirstUnlock) throws {
        // Delete existing item first (upsert pattern)
        try? delete(key: key)

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: accessibility
        ]

        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.unexpectedStatus(status)
        }
    }

    static func load(key: String) throws -> Data {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status != errSecItemNotFound else {
            throw KeychainError.itemNotFound
        }
        guard status == errSecSuccess, let data = result as? Data else {
            throw KeychainError.unexpectedStatus(status)
        }
        return data
    }

    static func delete(key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]

        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unexpectedStatus(status)
        }
    }
}
```

### Public Key Pinning

```swift
final class PublicKeyPinningDelegate: NSObject, URLSessionDelegate {
    private let pinnedPublicKeys: [SecKey]

    init(publicKeyHashes: [String]) {
        // Load pinned public keys from bundle
        self.pinnedPublicKeys = publicKeyHashes.compactMap { hash in
            // Convert hash to SecKey
            loadPublicKey(hash: hash)
        }
    }

    func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge, completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Evaluate trust
        guard SecTrustEvaluateWithError(serverTrust, nil) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Extract server's public key
        guard let serverCertificate = SecTrustGetCertificateAtIndex(serverTrust, 0),
              let serverPublicKey = SecCertificateCopyKey(serverCertificate) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Check if server's public key matches any pinned key
        let matched = pinnedPublicKeys.contains { pinnedKey in
            serverPublicKey == pinnedKey
        }

        if matched {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
```

### Secure Configuration

```swift
enum SecureConfig {
    // Environment-specific (via xcconfig, not hardcoded)
    static var apiBaseURL: String {
        guard let url = Bundle.main.object(forInfoDictionaryKey: "API_BASE_URL") as? String else {
            fatalError("API_BASE_URL not configured")
        }
        return url
    }

    // Fetched from backend after authentication
    static func fetchSecrets() async throws -> AppSecrets {
        // User must be authenticated first
        guard let authToken = try? KeychainManager.load(key: "authToken") else {
            throw ConfigError.notAuthenticated
        }

        // Fetch from secure endpoint
        var request = URLRequest(url: URL(string: "\(apiBaseURL)/config/secrets")!)
        request.setValue("Bearer \(String(data: authToken, encoding: .utf8)!)", forHTTPHeaderField: "Authorization")

        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(AppSecrets.self, from: data)
    }
}
```

---

## Quick Reference

### Storage Selection Matrix

| Data Type | Storage | Protection Level |
|-----------|---------|------------------|
| Auth tokens | Keychain | AfterFirstUnlock |
| Passwords | Keychain | WhenUnlocked |
| Biometric secret | Keychain | WhenPasscodeSetThisDeviceOnly |
| User preferences | UserDefaults | None needed |
| Sensitive files | Files | .completeFileProtection |
| Cache | Files/Cache | None needed |

### Keychain Access Levels

| Level | When Accessible | Use Case |
|-------|-----------------|----------|
| WhenUnlocked | Device unlocked | User-facing credentials |
| AfterFirstUnlock | After first unlock | Background operations |
| WhenPasscodeSetThisDeviceOnly | With passcode, this device | Biometric-protected |
| Always | Always | Almost never use |

### Security Audit Checklist

- [ ] Credentials in Keychain, not UserDefaults
- [ ] No hardcoded secrets in code
- [ ] No sensitive data in logs
- [ ] HTTPS only (ATS enabled)
- [ ] Certificate/public key pinning (if high-value)
- [ ] Appropriate Keychain access levels
- [ ] Files use Data Protection
- [ ] Clear sensitive data from memory

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Token in UserDefaults | Not encrypted | Keychain |
| API key in source | Easily extracted | Backend proxy or obfuscate |
| NSAllowsArbitraryLoads = true | No transport security | Proper ATS config |
| kSecAttrAccessibleAlways | Over-permissive | Appropriate access level |
| Ignoring SecItem status | Silent failures | Check and handle errors |
| Pinning certificate, not public key | Breaks on renewal | Pin public key |
| Sensitive data in logs | Exposure risk | Never log credentials |
