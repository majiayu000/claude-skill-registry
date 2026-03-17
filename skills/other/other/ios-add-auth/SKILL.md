---
name: ios-add-auth
description: Add authentication to an iOS app with Sign in with Apple, biometrics, and Keychain storage.
argument-hint: "[--providers apple,biometric] [--with-backend]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Add secure authentication to an existing iOS project using Apple-native approaches.

## Arguments
- `--providers <list>` — Comma-separated providers (default: `apple,biometric`)
  - `apple` — Sign in with Apple
  - `biometric` — Face ID / Touch ID
  - `credentials` — Email/password (requires backend)
- `--with-backend` — Include API client for backend auth

## What gets created

```
Services/
├── Auth/
│   ├── AuthService.swift           # Main auth service
│   ├── AuthState.swift             # Auth state enum
│   ├── KeychainManager.swift       # Secure token storage
│   ├── BiometricAuthManager.swift  # Face ID / Touch ID
│   └── SignInWithAppleManager.swift

Features/
├── Auth/
│   ├── SignInView.swift            # Sign-in screen
│   ├── SignInViewModel.swift
│   └── AuthenticatedContainer.swift # Wraps authenticated content

Models/
└── User.swift                      # User model
```

## Capabilities required

Add to Xcode project:
- **Sign in with Apple** capability (for `apple` provider)

Add to Info.plist:
- `NSFaceIDUsageDescription` — "Use Face ID to unlock the app"

## Keychain storage
- Access tokens stored in Keychain (not UserDefaults)
- Uses `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`
- Biometric-protected option available

## Auth flow
1. Check for existing session (Keychain)
2. If biometrics enabled, prompt for Face ID/Touch ID
3. If no session, show sign-in screen
4. On successful auth, store tokens in Keychain
5. Handle token refresh (if backend)

## Workflow
1. Add Sign in with Apple capability in Xcode
2. Create auth services and managers
3. Create sign-in UI
4. Create authenticated container wrapper
5. Integrate with DependencyContainer
6. Add Info.plist entries
7. Test on device (biometrics require device)

## Security requirements
- Never store tokens in UserDefaults
- Use Keychain with appropriate accessibility
- Validate Sign in with Apple tokens server-side
- Handle biometric fallback gracefully
- Clear Keychain on sign-out

## Output
Summarize: providers configured, capabilities needed, UI components, security setup.

## Reference
For implementation details and security patterns, see `reference/ios-add-auth-reference.md`
