---
name: authentication
description: "Implement iOS authentication patterns including Sign in with Apple (ASAuthorizationAppleIDProvider, ASAuthorizationController, ASAuthorizationAppleIDCredential), credential state checking, identity token validation, ASWebAuthenticationSession for OAuth and third-party auth flows, ASAuthorizationPasswordProvider for AutoFill credential suggestions, and biometric authentication with LAContext. Use when implementing Sign in with Apple, handling Apple ID credentials, building OAuth login flows, integrating Password AutoFill, checking credential revocation state, or validating identity tokens server-side."
---

# Authentication

Implement authentication flows on iOS using the AuthenticationServices
framework, including Sign in with Apple, OAuth/third-party web auth,
Password AutoFill, and biometric authentication.

## Contents

- [Sign in with Apple](#sign-in-with-apple)
- [Credential Handling](#credential-handling)
- [Credential State Checking](#credential-state-checking)
- [Token Validation](#token-validation)
- [Existing Account Setup Flows](#existing-account-setup-flows)
- [ASWebAuthenticationSession (OAuth)](#aswebauthenticationsession-oauth)
- [Password AutoFill Credentials](#password-autofill-credentials)
- [Biometric Authentication](#biometric-authentication)
- [SwiftUI SignInWithAppleButton](#swiftui-signinwithapplebutton)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Sign in with Apple

Add the "Sign in with Apple" capability in Xcode before using these APIs.

### UIKit: ASAuthorizationController Setup

```swift
import AuthenticationServices

final class LoginViewController: UIViewController {
    func startSignInWithApple() {
        let provider = ASAuthorizationAppleIDProvider()
        let request = provider.createRequest()
        request.requestedScopes = [.fullName, .email]

        let controller = ASAuthorizationController(authorizationRequests: [request])
        controller.delegate = self
        controller.presentationContextProvider = self
        controller.performRequests()
    }
}

extension LoginViewController: ASAuthorizationControllerPresentationContextProviding {
    func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {
        view.window!
    }
}
```

### Delegate: Handling Success and Failure

```swift
extension LoginViewController: ASAuthorizationControllerDelegate {
    func authorizationController(
        controller: ASAuthorizationController,
        didCompleteWithAuthorization authorization: ASAuthorization
    ) {
        guard let credential = authorization.credential
            as? ASAuthorizationAppleIDCredential else { return }

        let userID = credential.user  // Stable, unique, per-team identifier
        let email = credential.email  // nil after first authorization
        let fullName = credential.fullName  // nil after first authorization
        let identityToken = credential.identityToken  // JWT for server validation
        let authCode = credential.authorizationCode  // Short-lived code for server exchange

        // Save userID to Keychain for credential state checks
        // See references/keychain-biometric.md for Keychain patterns
        saveUserID(userID)

        // Send identityToken and authCode to your server
        authenticateWithServer(identityToken: identityToken, authCode: authCode)
    }

    func authorizationController(
        controller: ASAuthorizationController,
        didCompleteWithError error: any Error
    ) {
        let authError = error as? ASAuthorizationError
        switch authError?.code {
        case .canceled:
            break  // User dismissed
        case .failed:
            showError("Authorization failed")
        case .invalidResponse:
            showError("Invalid response")
        case .notHandled:
            showError("Not handled")
        case .notInteractive:
            break  // Non-interactive request failed -- expected for silent checks
        default:
            showError("Unknown error")
        }
    }
}
```

## Credential Handling

`ASAuthorizationAppleIDCredential` properties and their behavior:

| Property | Type | First Auth | Subsequent Auth |
|---|---|---|---|
| `user` | `String` | Always | Always |
| `email` | `String?` | Provided if requested | `nil` |
| `fullName` | `PersonNameComponents?` | Provided if requested | `nil` |
| `identityToken` | `Data?` | JWT (Base64) | JWT (Base64) |
| `authorizationCode` | `Data?` | Short-lived code | Short-lived code |
| `realUserStatus` | `ASUserDetectionStatus` | `.likelyReal` / `.unknown` | `.unknown` |

**Critical:** `email` and `fullName` are provided ONLY on the first
authorization. Cache them immediately during the initial sign-up flow. If the
user later deletes and re-adds the app, these values will not be returned.

```swift
func handleCredential(_ credential: ASAuthorizationAppleIDCredential) {
    // Always persist the user identifier
    let userID = credential.user

    // Cache name and email IMMEDIATELY -- only available on first auth
    if let fullName = credential.fullName {
        let name = PersonNameComponentsFormatter().string(from: fullName)
        UserProfile.saveName(name)  // Persist to your backend
    }
    if let email = credential.email {
        UserProfile.saveEmail(email)  // Persist to your backend
    }
}
```

## Credential State Checking

Check credential state on every app launch. The user may revoke access at
any time via Settings > Apple Account > Sign-In & Security.

```swift
func checkCredentialState() async {
    let provider = ASAuthorizationAppleIDProvider()
    guard let userID = loadSavedUserID() else {
        showLoginScreen()
        return
    }

    do {
        let state = try await provider.credentialState(forUserID: userID)
        switch state {
        case .authorized:
            proceedToMainApp()
        case .revoked:
            // User revoked -- sign out and clear local data
            signOut()
            showLoginScreen()
        case .notFound:
            showLoginScreen()
        case .transferred:
            // App transferred to new team -- migrate user identifier
            migrateUser()
        @unknown default:
            showLoginScreen()
        }
    } catch {
        // Network error -- allow offline access or retry
        proceedToMainApp()
    }
}
```

### Credential Revocation Notification

```swift
NotificationCenter.default.addObserver(
    forName: ASAuthorizationAppleIDProvider.credentialRevokedNotification,
    object: nil,
    queue: .main
) { _ in
    // Sign out immediately
    AuthManager.shared.signOut()
}
```

## Token Validation

The `identityToken` is a JWT. Send it to your server for validation --
never trust it client-side alone.

```swift
func sendTokenToServer(credential: ASAuthorizationAppleIDCredential) async throws {
    guard let tokenData = credential.identityToken,
          let token = String(data: tokenData, encoding: .utf8),
          let authCodeData = credential.authorizationCode,
          let authCode = String(data: authCodeData, encoding: .utf8) else {
        throw AuthError.missingToken
    }

    var request = URLRequest(url: URL(string: "https://api.example.com/auth/apple")!)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONEncoder().encode(
        ["identityToken": token, "authorizationCode": authCode]
    )

    let (data, response) = try await URLSession.shared.data(for: request)
    guard (response as? HTTPURLResponse)?.statusCode == 200 else {
        throw AuthError.serverValidationFailed
    }
    let session = try JSONDecoder().decode(SessionResponse.self, from: data)
    // Store session token in Keychain -- see references/keychain-biometric.md
    try KeychainHelper.save(session.accessToken, forKey: "accessToken")
}
```

Server-side, validate the JWT against Apple's public keys at
`https://appleid.apple.com/auth/keys` (JWKS). Verify: `iss` is
`https://appleid.apple.com`, `aud` matches your bundle ID, `exp` not passed.

## Existing Account Setup Flows

On launch, silently check for existing Sign in with Apple and password
credentials before showing a login screen:

```swift
func performExistingAccountSetupFlows() {
    let appleIDRequest = ASAuthorizationAppleIDProvider().createRequest()
    let passwordRequest = ASAuthorizationPasswordProvider().createRequest()

    let controller = ASAuthorizationController(
        authorizationRequests: [appleIDRequest, passwordRequest]
    )
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests(
        options: .preferImmediatelyAvailableCredentials
    )
}
```

Call this in `viewDidAppear` or on app launch. If no existing credentials
are found, the delegate receives a `.notInteractive` error -- handle it
silently and show your normal login UI.

## ASWebAuthenticationSession (OAuth)

Use `ASWebAuthenticationSession` for OAuth and third-party authentication
(Google, GitHub, etc.). Never use `WKWebView` for auth flows.

```swift
import AuthenticationServices

final class OAuthController: NSObject, ASWebAuthenticationPresentationContextProviding {
    func startOAuthFlow() {
        let authURL = URL(string:
            "https://provider.com/oauth/authorize?client_id=YOUR_ID&redirect_uri=myapp://callback&response_type=code"
        )!
        let session = ASWebAuthenticationSession(
            url: authURL, callback: .customScheme("myapp")
        ) { callbackURL, error in
            guard let callbackURL, error == nil,
                  let code = URLComponents(url: callbackURL, resolvingAgainstBaseURL: false)?
                      .queryItems?.first(where: { $0.name == "code" })?.value else { return }
            Task { await self.exchangeCodeForTokens(code) }
        }
        session.presentationContextProvider = self
        session.prefersEphemeralWebBrowserSession = true  // No shared cookies
        session.start()
    }

    func presentationAnchor(for session: ASWebAuthenticationSession) -> ASPresentationAnchor {
        ASPresentationAnchor()
    }
}
```

### SwiftUI WebAuthenticationSession

```swift
struct OAuthLoginView: View {
    @Environment(\.webAuthenticationSession) private var webAuthSession

    var body: some View {
        Button("Sign in with Provider") {
            Task {
                let url = URL(string: "https://provider.com/oauth/authorize?client_id=YOUR_ID")!
                let callbackURL = try await webAuthSession.authenticate(
                    using: url, callback: .customScheme("myapp")
                )
                // Extract authorization code from callbackURL
            }
        }
    }
}
```

Callback types: `.customScheme("myapp")` for URL scheme redirects;
`.https(host:path:)` for universal link redirects (preferred).

## Password AutoFill Credentials

Use `ASAuthorizationPasswordProvider` to offer saved keychain credentials
alongside Sign in with Apple:

```swift
func performSignIn() {
    let appleIDRequest = ASAuthorizationAppleIDProvider().createRequest()
    appleIDRequest.requestedScopes = [.fullName, .email]

    let passwordRequest = ASAuthorizationPasswordProvider().createRequest()

    let controller = ASAuthorizationController(
        authorizationRequests: [appleIDRequest, passwordRequest]
    )
    controller.delegate = self
    controller.presentationContextProvider = self
    controller.performRequests()
}

// In delegate:
func authorizationController(
    controller: ASAuthorizationController,
    didCompleteWithAuthorization authorization: ASAuthorization
) {
    switch authorization.credential {
    case let appleIDCredential as ASAuthorizationAppleIDCredential:
        handleAppleIDLogin(appleIDCredential)
    case let passwordCredential as ASPasswordCredential:
        // User selected a saved password from keychain
        signInWithPassword(
            username: passwordCredential.user,
            password: passwordCredential.password
        )
    default:
        break
    }
}
```

Set `textContentType` on text fields for AutoFill to work:

```swift
usernameField.textContentType = .username
passwordField.textContentType = .password
```

## Biometric Authentication

Use `LAContext` from LocalAuthentication for Face ID / Touch ID as a
sign-in or re-authentication mechanism. For protecting Keychain items
with biometric access control (`SecAccessControl`, `.biometryCurrentSet`),
see the `ios-security` skill.

```swift
import LocalAuthentication

func authenticateWithBiometrics() async throws -> Bool {
    let context = LAContext()
    var error: NSError?

    guard context.canEvaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics, error: &error
    ) else {
        throw AuthError.biometricsUnavailable
    }

    return try await context.evaluatePolicy(
        .deviceOwnerAuthenticationWithBiometrics,
        localizedReason: "Sign in to your account"
    )
}
```

**Required:** Add `NSFaceIDUsageDescription` to Info.plist. Missing this
key crashes on Face ID devices.

## SwiftUI SignInWithAppleButton

```swift
import AuthenticationServices

struct AppleSignInView: View {
    @Environment(\.colorScheme) var colorScheme

    var body: some View {
        SignInWithAppleButton(.signIn) { request in
            request.requestedScopes = [.fullName, .email]
        } onCompletion: { result in
            switch result {
            case .success(let authorization):
                guard let credential = authorization.credential
                    as? ASAuthorizationAppleIDCredential else { return }
                handleCredential(credential)
            case .failure(let error):
                handleError(error)
            }
        }
        .signInWithAppleButtonStyle(
            colorScheme == .dark ? .white : .black
        )
        .frame(height: 50)
    }
}
```

## Common Mistakes

### 1. Not checking credential state on app launch

```swift
// DON'T: Assume the user is still authorized
func appDidLaunch() {
    if UserDefaults.standard.bool(forKey: "isLoggedIn") {
        showMainApp()  // User may have revoked access!
    }
}

// DO: Check credential state every launch
func appDidLaunch() async {
    await checkCredentialState()  // See "Credential State Checking" above
}
```

### 2. Not performing existing account setup flows

```swift
// DON'T: Always show a full login screen on launch
// DO: Call performExistingAccountSetupFlows() first;
//     show login UI only if .notInteractive error received
```

### 3. Assuming email/name are always provided

```swift
// DON'T: Force-unwrap email or fullName
let email = credential.email!  // Crashes on subsequent logins

// DO: Handle nil gracefully -- only available on first authorization
if let email = credential.email {
    saveEmail(email)  // Persist immediately
}
```

### 4. Not implementing ASAuthorizationControllerPresentationContextProviding

```swift
// DON'T: Skip the presentation context provider
controller.delegate = self
controller.performRequests()  // May not display UI correctly

// DO: Always set the presentation context provider
controller.delegate = self
controller.presentationContextProvider = self  // Required for proper UI
controller.performRequests()
```

### 5. Storing identityToken in UserDefaults

```swift
// DON'T: Store tokens in UserDefaults
UserDefaults.standard.set(tokenString, forKey: "identityToken")

// DO: Store in Keychain
// See references/keychain-biometric.md for Keychain patterns
try KeychainHelper.save(tokenData, forKey: "identityToken")
```

## Review Checklist

- [ ] "Sign in with Apple" capability added in Xcode project
- [ ] `ASAuthorizationControllerPresentationContextProviding` implemented
- [ ] Credential state checked on every app launch (`credentialState(forUserID:)`)
- [ ] `credentialRevokedNotification` observer registered; sign-out handled
- [ ] `email` and `fullName` cached on first authorization (not assumed available later)
- [ ] `identityToken` sent to server for validation, not trusted client-side only
- [ ] Tokens stored in Keychain, not UserDefaults or files
- [ ] `performExistingAccountSetupFlows` called before showing login UI
- [ ] Error cases handled: `.canceled`, `.failed`, `.notInteractive`
- [ ] `NSFaceIDUsageDescription` in Info.plist for biometric auth
- [ ] `ASWebAuthenticationSession` used for OAuth (not `WKWebView`)
- [ ] `prefersEphemeralWebBrowserSession` set for OAuth when appropriate
- [ ] `textContentType` set on username/password fields for AutoFill

## References

- Keychain & biometric patterns: `references/keychain-biometric.md`
- [AuthenticationServices](https://sosumi.ai/documentation/authenticationservices)
- [ASAuthorizationAppleIDProvider](https://sosumi.ai/documentation/authenticationservices/asauthorizationappleidprovider)
- [ASAuthorizationAppleIDCredential](https://sosumi.ai/documentation/authenticationservices/asauthorizationappleidcredential)
- [ASAuthorizationController](https://sosumi.ai/documentation/authenticationservices/asauthorizationcontroller)
- [ASWebAuthenticationSession](https://sosumi.ai/documentation/authenticationservices/aswebauthenticationsession)
- [ASAuthorizationPasswordProvider](https://sosumi.ai/documentation/authenticationservices/asauthorizationpasswordprovider)
- [SignInWithAppleButton](https://sosumi.ai/documentation/authenticationservices/signinwithapplebutton)
- [Implementing User Authentication with Sign in with Apple](https://sosumi.ai/documentation/authenticationservices/implementing-user-authentication-with-sign-in-with-apple)
