---
name: authentication-patterns
description: Comprehensive authentication implementation guidance including JWT best practices, OAuth 2.0/OIDC flows, Passkeys/FIDO2/WebAuthn, MFA patterns, and secure session management. Use when implementing login systems, token-based auth, SSO, passwordless authentication, or reviewing authentication security.
allowed-tools: Read, Glob, Grep, Task
---

# Authentication Patterns

Comprehensive guidance for implementing secure authentication systems, covering JWT, OAuth 2.0, OIDC, Passkeys, MFA, and session management.

## When to Use This Skill

Use this skill when:

- Implementing JWT-based authentication
- Setting up OAuth 2.0 or OpenID Connect flows
- Implementing passwordless authentication (Passkeys/FIDO2)
- Adding multi-factor authentication (MFA/2FA)
- Designing session management and secure cookies
- Implementing SSO (Single Sign-On)
- Reviewing authentication security
- Choosing between authentication approaches

## Authentication Method Selection

| Method | Best For | Security Level | UX |
|--------|----------|----------------|-----|
| Passkeys/WebAuthn | Primary auth, passwordless | ★★★★★ | Excellent |
| OAuth 2.0 + PKCE | Third-party login, SPAs | ★★★★☆ | Good |
| JWT + Refresh Tokens | APIs, microservices | ★★★★☆ | Good |
| Session Cookies | Traditional web apps | ★★★☆☆ | Excellent |
| Password + MFA | Legacy systems upgrade | ★★★★☆ | Moderate |

**Recommendation:** Prefer Passkeys for new applications. Use OAuth 2.0 + PKCE for SPAs. Always add MFA as a second factor.

## JWT Best Practices Quick Reference

### Algorithm Selection

| Algorithm | Use Case | Recommendation |
|-----------|----------|----------------|
| RS256 | Public key verification, distributed systems | ✅ Recommended |
| ES256 | Smaller tokens, ECDSA-based | ✅ Recommended |
| HS256 | Simple systems, same-party verification | ⚠️ Use carefully |
| None | Never use | ❌ Prohibited |

### Token Structure

```javascript
// Header
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-id-for-rotation"  // Key ID for key rotation
}

// Payload (Claims)
{
  "iss": "https://auth.example.com",  // Issuer
  "sub": "user-123",                   // Subject (user ID)
  "aud": "https://api.example.com",   // Audience
  "exp": 1735300000,                   // Expiration (short-lived)
  "iat": 1735296400,                   // Issued at
  "jti": "unique-token-id",            // JWT ID (for revocation)
  "scope": "read write"                // Permissions
}
```

### Token Lifetimes

| Token Type | Recommended Lifetime | Storage |
|------------|---------------------|---------|
| Access Token | 5-15 minutes | Memory only |
| Refresh Token | 7-30 days | Secure HttpOnly cookie or encrypted storage |
| ID Token | Match access token | Memory only |

**For detailed JWT security:** See [JWT Security Reference](references/jwt-security.md)

## OAuth 2.0 Flow Selection

| Flow | Use Case | PKCE Required |
|------|----------|---------------|
| Authorization Code + PKCE | SPAs, mobile apps, web apps | ✅ Yes |
| Client Credentials | Service-to-service | N/A |
| Device Authorization | Smart TVs, CLI tools | N/A |
| ~~Implicit~~ | Deprecated - don't use | N/A |
| ~~Resource Owner Password~~ | Deprecated - don't use | N/A |

### Authorization Code + PKCE Flow

```text
┌──────────┐                              ┌───────────────┐
│  Client  │                              │ Auth Server   │
└────┬─────┘                              └───────┬───────┘
     │                                            │
     │ 1. Generate code_verifier (random)         │
     │    code_challenge = SHA256(code_verifier)  │
     │                                            │
     │ 2. Authorization Request ─────────────────>│
     │    (response_type=code, code_challenge)    │
     │                                            │
     │ 3. User authenticates & consents           │
     │                                            │
     │ 4. <────────── Authorization Code ─────────│
     │                                            │
     │ 5. Token Request ─────────────────────────>│
     │    (code, code_verifier)                   │
     │                                            │
     │ 6. <────────── Access + Refresh Tokens ────│
     └────────────────────────────────────────────┘
```

**For detailed OAuth flows:** See [OAuth Flows Reference](references/oauth-flows.md)

## Passkeys/WebAuthn Quick Start

Passkeys provide phishing-resistant, passwordless authentication using public key cryptography.

### Registration Flow

```javascript
// 1. Get challenge from server
const options = await fetch('/api/webauthn/register/options').then(r => r.json());

// 2. Create credential
const credential = await navigator.credentials.create({
  publicKey: {
    challenge: base64ToBuffer(options.challenge),
    rp: { name: "Example App", id: "example.com" },
    user: {
      id: base64ToBuffer(options.userId),
      name: options.username,
      displayName: options.displayName
    },
    pubKeyCredParams: [
      { type: "public-key", alg: -7 },   // ES256
      { type: "public-key", alg: -257 }  // RS256
    ],
    authenticatorSelection: {
      authenticatorAttachment: "platform",  // or "cross-platform"
      residentKey: "required",              // Discoverable credential
      userVerification: "required"          // Biometric/PIN required
    },
    timeout: 60000
  }
});

// 3. Send credential to server for storage
await fetch('/api/webauthn/register/verify', {
  method: 'POST',
  body: JSON.stringify({
    id: credential.id,
    rawId: bufferToBase64(credential.rawId),
    response: {
      clientDataJSON: bufferToBase64(credential.response.clientDataJSON),
      attestationObject: bufferToBase64(credential.response.attestationObject)
    }
  })
});
```

**For complete Passkeys implementation:** See [Passkeys Implementation Guide](references/passkeys-implementation.md)

## MFA Implementation Patterns

### MFA Methods (by Security)

| Method | Phishing Resistant | Security | UX |
|--------|-------------------|----------|-----|
| Passkeys/Security Keys | ✅ Yes | ★★★★★ | Good |
| Authenticator App (TOTP) | ❌ No | ★★★★☆ | Good |
| Push Notification | ⚠️ Partial | ★★★★☆ | Excellent |
| SMS OTP | ❌ No | ★★☆☆☆ | Moderate |
| Email OTP | ❌ No | ★★☆☆☆ | Moderate |

### TOTP Implementation

```csharp
using System.Security.Cryptography;
using OtpNet;  // Install: Otp.NET package

/// <summary>
/// TOTP (Time-based One-Time Password) service for MFA.
/// </summary>
public sealed class TotpService
{
    private const int SecretLength = 20;  // 160 bits

    /// <summary>
    /// Generate a new TOTP secret for user enrollment.
    /// </summary>
    public static string GenerateSecret()
    {
        var secretBytes = RandomNumberGenerator.GetBytes(SecretLength);
        return Base32Encoding.ToString(secretBytes);
    }

    /// <summary>
    /// Generate provisioning URI for authenticator apps (Google Authenticator, etc.)
    /// </summary>
    public static string GetProvisioningUri(string secret, string email, string issuer)
    {
        return $"otpauth://totp/{Uri.EscapeDataString(issuer)}:{Uri.EscapeDataString(email)}" +
               $"?secret={secret}&issuer={Uri.EscapeDataString(issuer)}&algorithm=SHA1&digits=6&period=30";
    }

    /// <summary>
    /// Verify TOTP code during login. Allows 1-step time drift.
    /// </summary>
    public static bool VerifyTotp(string secret, string otp)
    {
        var secretBytes = Base32Encoding.ToBytes(secret);
        var totp = new Totp(secretBytes, step: 30, totpSize: 6);

        // VerificationWindow allows for clock drift (1 step = 30 seconds each direction)
        return totp.VerifyTotp(otp, out _, VerificationWindow.RfcSpecifiedNetworkDelay);
    }
}
```

## Session Management

### Secure Cookie Configuration

```csharp
// ASP.NET Core cookie configuration
app.UseCookiePolicy(new CookiePolicyOptions
{
    HttpOnly = HttpOnlyPolicy.Always,        // Prevent JavaScript access (XSS protection)
    Secure = CookieSecurePolicy.Always,      // HTTPS only
    MinimumSameSitePolicy = SameSiteMode.Lax // CSRF protection (or Strict for more security)
});

// Per-cookie configuration
Response.Cookies.Append("session_id", sessionId, new CookieOptions
{
    HttpOnly = true,             // Prevent JavaScript access
    Secure = true,               // HTTPS only
    SameSite = SameSiteMode.Lax, // CSRF protection
    MaxAge = TimeSpan.FromHours(1),
    Domain = ".example.com",
    Path = "/",
    IsEssential = true           // Required for GDPR essential cookies
});
```

### Session Security Checklist

- [ ] Generate cryptographically random session IDs (128+ bits)
- [ ] Regenerate session ID after authentication
- [ ] Set HttpOnly flag on session cookies
- [ ] Set Secure flag (HTTPS only)
- [ ] Set SameSite attribute (Lax or Strict)
- [ ] Implement session timeout (idle and absolute)
- [ ] Invalidate session on logout (server-side)
- [ ] Bind session to user fingerprint (optional, consider privacy)

## Password Security (When Required)

### Password Hashing

```csharp
using System.Security.Cryptography;
using Konscious.Security.Cryptography;  // Install: Konscious.Security.Cryptography.Argon2

/// <summary>
/// Argon2id password hashing service (recommended by OWASP).
/// </summary>
public sealed class PasswordHasher
{
    private const int SaltSize = 16;
    private const int HashSize = 32;
    private const int Iterations = 3;      // time_cost
    private const int MemorySize = 65536;  // 64 MB
    private const int Parallelism = 4;     // threads

    /// <summary>
    /// Hash a password using Argon2id.
    /// </summary>
    public static string HashPassword(string password)
    {
        var salt = RandomNumberGenerator.GetBytes(SaltSize);

        using var argon2 = new Argon2id(System.Text.Encoding.UTF8.GetBytes(password))
        {
            Salt = salt,
            DegreeOfParallelism = Parallelism,
            MemorySize = MemorySize,
            Iterations = Iterations
        };

        var hash = argon2.GetBytes(HashSize);

        // Combine salt + hash for storage
        var combined = new byte[SaltSize + HashSize];
        Buffer.BlockCopy(salt, 0, combined, 0, SaltSize);
        Buffer.BlockCopy(hash, 0, combined, SaltSize, HashSize);

        return Convert.ToBase64String(combined);
    }

    /// <summary>
    /// Verify a password against stored hash.
    /// </summary>
    public static bool VerifyPassword(string password, string storedHash)
    {
        var combined = Convert.FromBase64String(storedHash);
        if (combined.Length != SaltSize + HashSize) return false;

        var salt = combined[..SaltSize];
        var expectedHash = combined[SaltSize..];

        using var argon2 = new Argon2id(System.Text.Encoding.UTF8.GetBytes(password))
        {
            Salt = salt,
            DegreeOfParallelism = Parallelism,
            MemorySize = MemorySize,
            Iterations = Iterations
        };

        var actualHash = argon2.GetBytes(HashSize);

        // Timing-safe comparison
        return CryptographicOperations.FixedTimeEquals(actualHash, expectedHash);
    }
}
```

### Password Policy

| Requirement | Recommendation |
|-------------|----------------|
| Minimum length | 12+ characters |
| Maximum length | 128+ characters (prevent DoS) |
| Complexity | No arbitrary rules (allow all characters) |
| Breach check | Check against known breached passwords |
| Rate limiting | 5 attempts, then exponential backoff |
| Account lockout | Temporary lockout (15-30 min) after failures |

## Quick Decision Tree

**What authentication are you implementing?**

1. **New web/mobile app** → Passkeys + OAuth 2.0 fallback
2. **SPA with API backend** → OAuth 2.0 + PKCE with JWT access tokens
3. **Service-to-service** → Client Credentials flow or mTLS
4. **Adding MFA to existing** → TOTP authenticator app (minimum), Passkeys (ideal)
5. **Traditional web app** → Session cookies + CSRF tokens
6. **CLI/device with no browser** → Device Authorization flow

## Security Checklist

### Token Security

- [ ] Short-lived access tokens (5-15 minutes)
- [ ] Secure refresh token storage
- [ ] Token revocation mechanism
- [ ] Proper token validation (signature, claims, expiry)

### OAuth/OIDC Security

- [ ] Use PKCE for all public clients
- [ ] Validate redirect URIs strictly
- [ ] Validate state parameter
- [ ] Validate nonce for OIDC
- [ ] Use exact redirect URI matching

### Session Security

- [ ] HttpOnly, Secure, SameSite cookies
- [ ] Session regeneration after auth
- [ ] Proper session invalidation
- [ ] Idle and absolute timeouts

### MFA Security

- [ ] MFA on all accounts (enforce or encourage)
- [ ] Secure recovery codes
- [ ] Rate limit MFA attempts
- [ ] Prefer phishing-resistant methods

## References

- [JWT Security Deep Dive](references/jwt-security.md) - Complete JWT implementation guide
- [OAuth 2.0 Flows](references/oauth-flows.md) - OAuth/OIDC flow diagrams and implementation
- [Passkeys Implementation](references/passkeys-implementation.md) - WebAuthn/FIDO2 complete guide

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `authorization-models` | After authentication, apply authorization (RBAC, ABAC) |
| `cryptography` | Underlying crypto for tokens and passwords |
| `api-security` | Securing API endpoints with authentication |
| `secure-coding` | General security patterns |

## Version History

- v1.0.0 (2025-12-26): Initial release with JWT, OAuth 2.0, Passkeys, MFA, sessions

---

**Last Updated:** 2025-12-26
