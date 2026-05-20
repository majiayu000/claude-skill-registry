---
name: jwt
description: JSON Web Tokens for secure transmission. Use for authentication.
---

# JSON Web Token (JWT)

JWT is a compact, URL-safe means of representing claims to be transferred between two parties. The claims are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) or JSON Web Encryption (JWE).

## When to Use

- **Stateless Authentication**: API doesn't need to check a database session for every request.
- **Information Exchange**: Securely transmitting information (like User ID + Roles) between microservices.

## Quick Start (Structure)

`Header.Payload.Signature`

```json
// Header
{
  "alg": "RS256",
  "typ": "JWT"
}

// Payload (Claims)
{
  "sub": "1234567890", // Subject (User ID)
  "name": "John Doe",
  "iat": 1516239022,    // Issued At
  "exp": 1516242622,    // Expiration
  "role": "admin"
}

// Signature
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

## Core Concepts

### Signing Algorithms

- **HS256** (HMAC): Shared secret. Fast, simple. Good for internal microservices.
- **RS256 / ES256** (RSA/ECDSA): Public/Private key pair. The ID Provider signs with Private; APIs verify with Public. **Preferred for 2025**.

### Claims

- **Registered**: `iss` (issuer), `exp` (expiration), `sub` (subject), `aud` (audience).
- **Public/Private**: Custom data (`role`, `tenant_id`).

## Best Practices (2025)

**Do**:

- **Short Expiration**: 5-15 minutes max. Use Refresh Tokens for long-lived sessions.
- **Algorithm Verification**: Hardcode the expected algorithm (e.g., `algorithms=['RS256']`) in your verifier to prevent `None` alg attacks.
- **Use RS256/ES256**: Avoid sharing secrets if possible.

**Don't**:

- **No PII**: Don't put GDPR/PII data (email, address) in the JWT unless encrypted (JWE). It can be decoded by anyone.
- **No Sensitive Data**: Don't put "password" or "credit card" in claims.
- **Don't store in LocalStorage**: Susceptible to XSS. Use **HttpOnly / Secure Cookies**.

## Troubleshooting

| Error               | Cause                            | Solution                                     |
| :------------------ | :------------------------------- | :------------------------------------------- |
| `TokenExpiredError` | `exp` time passed.               | Refresh the token using a Refresh Token.     |
| `JsonWebTokenError` | Malformed or Signature mismatch. | Check secret/public key and token integrity. |

## References

- [jwt.io](https://jwt.io/)
- [RFC 7519](https://tools.ietf.org/html/rfc7519)
