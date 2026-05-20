---
name: device-integrity
description: "Verify device legitimacy and app integrity using DeviceCheck (DCDevice per-device bits) and App Attest (DCAppAttestService key generation, attestation, and assertion flows). Use when implementing fraud prevention, detecting compromised devices, validating app authenticity with Apple's servers, protecting sensitive API endpoints with attested requests, or adding device verification to your backend architecture."
---

# Device Integrity

Verify that requests to your server come from a genuine Apple device running
your unmodified app. DeviceCheck provides per-device bits for simple flags
(e.g., "claimed promo offer"). App Attest uses Secure Enclave keys and Apple
attestation to cryptographically prove app legitimacy on each request.

## Contents

- [DCDevice (DeviceCheck Tokens)](#dcdevice-devicecheck-tokens)
- [DCAppAttestService (App Attest)](#dcappattestservice-app-attest)
- [App Attest Key Generation](#app-attest-key-generation)
- [App Attest Attestation Flow](#app-attest-attestation-flow)
- [App Attest Assertion Flow](#app-attest-assertion-flow)
- [Server Verification Guidance](#server-verification-guidance)
- [Error Handling](#error-handling)
- [Common Patterns](#common-patterns)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)

## DCDevice (DeviceCheck Tokens)

[`DCDevice`](https://sosumi.ai/documentation/devicecheck/dcdevice) generates a
unique, ephemeral token that identifies a device. The token is sent to your
server, which then communicates with Apple's servers to read or set two
per-device bits. Available on iOS 11+.

### Token Generation

```swift
import DeviceCheck

func generateDeviceToken() async throws -> Data {
    guard DCDevice.current.isSupported else {
        throw DeviceIntegrityError.deviceCheckUnsupported
    }

    return try await DCDevice.current.generateToken()
}
```

### Sending the Token to Your Server

```swift
func sendTokenToServer(_ token: Data) async throws {
    let tokenString = token.base64EncodedString()

    var request = URLRequest(url: serverURL.appending(path: "verify-device"))
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONEncoder().encode(["device_token": tokenString])

    let (_, response) = try await URLSession.shared.data(for: request)
    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw DeviceIntegrityError.serverVerificationFailed
    }
}
```

### Server-Side Overview

Your server uses the device token to call Apple's DeviceCheck API endpoints:

| Endpoint | Purpose |
|----------|---------|
| `https://api.devicecheck.apple.com/v1/query_two_bits` | Read the two bits for a device |
| `https://api.devicecheck.apple.com/v1/update_two_bits` | Set the two bits for a device |
| `https://api.devicecheck.apple.com/v1/validate_device_token` | Validate a device token without reading bits |

The server authenticates with a DeviceCheck private key from the Apple Developer
portal, creating a signed JWT for each request.

### What the Two Bits Are For

Apple stores two Boolean values per device per developer team. You decide what
they mean. Common uses:

- **Bit 0:** Device has claimed a promotional offer.
- **Bit 1:** Device has been flagged for fraud.

Bits persist across app reinstall; device reset does not clear them. You control
when to reset them via the server API.

## DCAppAttestService (App Attest)

[`DCAppAttestService`](https://sosumi.ai/documentation/devicecheck/dcappattestservice)
validates that a specific instance of your app on a specific device is
legitimate. It uses a hardware-backed key in the Secure Enclave to create
cryptographic attestations and assertions. Available on iOS 14+.

The flow has three phases:
1. **Key generation** -- create a key pair in the Secure Enclave.
2. **Attestation** -- Apple certifies the key belongs to a genuine Apple device running your app.
3. **Assertion** -- sign server requests with the attested key to prove ongoing legitimacy.

### Checking Support

```swift
import DeviceCheck

let attestService = DCAppAttestService.shared

guard attestService.isSupported else {
    // Fall back to DCDevice token or other risk assessment.
    // App Attest is not available on simulators or all device models.
    return
}
```

## App Attest Key Generation

Generate a cryptographic key pair stored in the Secure Enclave. The returned
`keyId` is a string identifier you persist (e.g., in Keychain) for later
attestation and assertion calls.

```swift
import DeviceCheck

actor AppAttestManager {
    private let service = DCAppAttestService.shared
    private var keyId: String?

    /// Generate and persist a key pair for App Attest.
    func generateKeyIfNeeded() async throws -> String {
        if let existingKeyId = loadKeyIdFromKeychain() {
            self.keyId = existingKeyId
            return existingKeyId
        }

        let newKeyId = try await service.generateKey()
        saveKeyIdToKeychain(newKeyId)
        self.keyId = newKeyId
        return newKeyId
    }

    // MARK: - Keychain helpers (simplified)

    private func saveKeyIdToKeychain(_ keyId: String) {
        let data = Data(keyId.utf8)
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: "app-attest-key-id",
            kSecAttrService as String: Bundle.main.bundleIdentifier ?? "",
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
        ]
        SecItemDelete(query as CFDictionary) // Remove old if exists
        SecItemAdd(query as CFDictionary, nil)
    }

    private func loadKeyIdFromKeychain() -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: "app-attest-key-id",
            kSecAttrService as String: Bundle.main.bundleIdentifier ?? "",
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess, let data = result as? Data else { return nil }
        return String(data: data, encoding: .utf8)
    }
}
```

**Important:** Generate the key once and persist the `keyId`. Generating a new
key invalidates any previous attestation.

## App Attest Attestation Flow

Attestation proves that the key was generated on a genuine Apple device running
your unmodified app. You perform attestation once per key, then store the
attestation object on your server.

### Client-Side Attestation

```swift
import DeviceCheck
import CryptoKit

extension AppAttestManager {
    /// Attest the key with Apple. Send the attestation object to your server.
    func attestKey() async throws -> Data {
        guard let keyId else {
            throw DeviceIntegrityError.keyNotGenerated
        }

        // 1. Request a one-time challenge from your server
        let challenge = try await fetchServerChallenge()

        // 2. Hash the challenge (Apple requires a SHA-256 hash)
        let challengeHash = Data(SHA256.hash(data: challenge))

        // 3. Ask Apple to attest the key
        let attestation = try await service.attestKey(keyId, clientDataHash: challengeHash)

        // 4. Send the attestation object to your server for verification
        try await sendAttestationToServer(
            keyId: keyId,
            attestation: attestation,
            challenge: challenge
        )

        return attestation
    }

    private func fetchServerChallenge() async throws -> Data {
        let url = serverURL.appending(path: "attest/challenge")
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }

    private func sendAttestationToServer(
        keyId: String,
        attestation: Data,
        challenge: Data
    ) async throws {
        var request = URLRequest(url: serverURL.appending(path: "attest/verify"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let payload: [String: String] = [
            "key_id": keyId,
            "attestation": attestation.base64EncodedString(),
            "challenge": challenge.base64EncodedString()
        ]
        request.httpBody = try JSONEncoder().encode(payload)

        let (_, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw DeviceIntegrityError.attestationVerificationFailed
        }
    }
}
```

### Server-Side Attestation Verification

Your server must:
1. Verify the attestation object is a valid CBOR-encoded structure.
2. Extract the certificate chain and validate it against Apple's App Attest root CA.
3. Verify the `nonce` in the attestation matches `SHA256(challenge)`.
4. Extract and store the public key and receipt for future assertion verification.

See [Validating apps that connect to your server](https://sosumi.ai/documentation/devicecheck/validating-apps-that-connect-to-your-server) for the full server verification algorithm.

## App Attest Assertion Flow

After attestation, use assertions to sign individual requests. Each assertion
proves the request came from the attested app instance.

### Client-Side Assertion

```swift
import DeviceCheck
import CryptoKit

extension AppAttestManager {
    /// Generate an assertion to accompany a server request.
    /// - Parameter requestData: The request payload to sign (e.g., JSON body).
    /// - Returns: The assertion data to include with the request.
    func generateAssertion(for requestData: Data) async throws -> Data {
        guard let keyId else {
            throw DeviceIntegrityError.keyNotGenerated
        }

        // Hash the request data -- the server will verify this matches
        let clientDataHash = Data(SHA256.hash(data: requestData))

        return try await service.generateAssertion(keyId, clientDataHash: clientDataHash)
    }
}
```

### Using Assertions in Network Requests

```swift
extension AppAttestManager {
    /// Perform an attested API request.
    func makeAttestedRequest(
        to url: URL,
        method: String = "POST",
        body: Data
    ) async throws -> (Data, URLResponse) {
        let assertion = try await generateAssertion(for: body)

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue(assertion.base64EncodedString(), forHTTPHeaderField: "X-App-Assertion")
        request.httpBody = body

        return try await URLSession.shared.data(for: request)
    }
}
```

### Server-Side Assertion Verification

Your server must:
1. Decode the assertion (CBOR).
2. Verify the authenticator data, including the counter (must be greater than the stored counter).
3. Verify the signature using the stored public key from attestation.
4. Confirm the `clientDataHash` matches the SHA-256 of the received request body.
5. Update the stored counter to prevent replay attacks.

## Server Verification Guidance

### Attestation vs. Assertion

| Phase | When | What It Proves | Frequency |
|-------|------|---------------|-----------|
| **Attestation** | After key generation | The key lives on a genuine Apple device running your unmodified app | Once per key |
| **Assertion** | With each sensitive request | The request came from the attested app instance | Per request |

### Recommended Server Architecture

1. **Challenge endpoint** -- generate a random nonce, store it server-side with a short TTL (e.g., 5 minutes).
2. **Attestation verification endpoint** -- validate the attestation object, store the public key and receipt keyed by `keyId`.
3. **Assertion verification middleware** -- verify assertions on sensitive endpoints (purchases, account changes).

### Risk Assessment

Combine App Attest with [fraud risk assessment](https://sosumi.ai/documentation/devicecheck/assessing-fraud-risk) for defense in depth. App Attest alone does not guarantee the user is not abusing the app -- it confirms the app is genuine.

## Error Handling

### DCError Codes

```swift
import DeviceCheck

func handleAttestError(_ error: Error) {
    if let dcError = error as? DCError {
        switch dcError.code {
        case .unknownSystemFailure:
            // Transient system error -- retry with exponential backoff
            break
        case .featureUnsupported:
            // Device or OS does not support this feature
            // Fall back to alternative verification
            break
        case .invalidKey:
            // Key is corrupted or was invalidated
            // Generate a new key and re-attest
            break
        case .invalidInput:
            // The clientDataHash or keyId was malformed
            break
        case .serverUnavailable:
            // Apple's attestation server is unreachable -- retry later
            break
        @unknown default:
            break
        }
    }
}
```

### Retry Strategy

```swift
extension AppAttestManager {
    func attestKeyWithRetry(maxAttempts: Int = 3) async throws -> Data {
        var lastError: Error?

        for attempt in 0..<maxAttempts {
            do {
                return try await attestKey()
            } catch let error as DCError where error.code == .serverUnavailable {
                lastError = error
                let delay = UInt64(pow(2.0, Double(attempt))) * 1_000_000_000
                try await Task.sleep(nanoseconds: delay)
            } catch {
                throw error // Non-retryable errors propagate immediately
            }
        }

        throw lastError ?? DeviceIntegrityError.attestationFailed
    }
}
```

### Handling Invalidated Keys

If `attestKey` returns `DCError.invalidKey`, the Secure Enclave key has been
invalidated (e.g., OS update, Secure Enclave reset). Delete the stored `keyId`
from Keychain and generate a new key:

```swift
extension AppAttestManager {
    func handleInvalidKey() async throws -> String {
        deleteKeyIdFromKeychain()
        keyId = nil
        return try await generateKeyIfNeeded()
    }

    private func deleteKeyIdFromKeychain() {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: "app-attest-key-id",
            kSecAttrService as String: Bundle.main.bundleIdentifier ?? ""
        ]
        SecItemDelete(query as CFDictionary)
    }
}
```

## Common Patterns

### Full Integration Manager

Combine the patterns above into a single `actor` that manages the full lifecycle:
1. Check `isSupported` and fall back to `DCDevice` tokens on unsupported devices.
2. Call `generateKeyIfNeeded()` on launch to create or load the persisted key.
3. Call `attestKeyWithRetry()` once after key generation.
4. Use `generateAssertion(for:)` on each sensitive server request.
5. Handle `DCError.invalidKey` by regenerating and re-attesting.

### Gradual Rollout

Apple recommends a gradual rollout. Gate App Attest behind a remote feature
flag and fall back to `DCDevice` tokens on unsupported devices.

### Environment Entitlement

Set the App Attest environment in your entitlements file. Use `development`
during testing and `production` for App Store builds:

```xml
<key>com.apple.developer.devicecheck.appattest-environment</key>
<string>production</string>
```

When the entitlement is missing, the system uses `development` in debug builds
and `production` for App Store and TestFlight builds.

### Error Type

```swift
enum DeviceIntegrityError: Error {
    case deviceCheckUnsupported
    case keyNotGenerated
    case attestationFailed
    case attestationVerificationFailed
    case assertionFailed
    case serverVerificationFailed
}
```

## Common Mistakes

1. **Generating a new key on every launch.** Generate once, persist the `keyId` in Keychain.
2. **Skipping the fallback for unsupported devices.** Not all devices support App Attest. Use `DCDevice` tokens as fallback.
3. **Trusting attestation client-side.** All verification must happen on your server.
4. **Not implementing replay protection.** The server must track and increment the assertion counter.
5. **Missing the environment entitlement.** Without it, debug builds use `development` and App Store uses `production`. Mismatches cause attestation failures.
6. **Not handling `DCError.invalidKey`.** Keys can be invalidated by OS updates. Detect and regenerate.

## Review Checklist

- [ ] `DCAppAttestService.isSupported` checked before use; fallback to `DCDevice` when unsupported
- [ ] Key generated once and `keyId` persisted in Keychain
- [ ] Attestation performed once per key; attestation object sent to server
- [ ] Server validates attestation against Apple's App Attest root CA
- [ ] Assertions generated for each sensitive request; server verifies signature and counter
- [ ] `DCError` cases handled: `.serverUnavailable` with retry, `.invalidKey` with key regeneration
- [ ] App Attest environment entitlement set correctly for debug vs. production
- [ ] Gradual rollout considered; feature flag in place for enabling/disabling
