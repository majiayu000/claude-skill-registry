---
name: modern-auth-2026
description: Modern authentication implementation for 2026 - passkeys (WebAuthn), OAuth (Google, Apple), magic links, and cross-device sync. Use for passwordless-first authentication, social login setup, Supabase Auth, Next.js auth flows, and multi-factor authentication. Activate on "passkeys", "WebAuthn", "Google Sign-In", "Apple Sign-In", "magic link", "passwordless", "authentication", "login", "OAuth", "social login". NOT for session management without auth (use standard JWT docs), authorization/RBAC (use security-auditor), or API key management (use api-architect).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - WebSearch
  - mcp__supabase__*
category: DevOps & Site Reliability
tags:
  - authentication
  - passkeys
  - webauthn
  - oauth
  - passwordless
  - supabase
  - mfa
  - social-login
---

# Modern Authentication Expert (2026)

Master passwordless-first authentication with passkeys, OAuth, magic links, and cross-device sync for modern web and mobile applications.

## When to Use

✅ **USE this skill for:**
- Implementing passkeys/WebAuthn authentication
- Google and Apple OAuth social login
- Supabase Auth configuration and troubleshooting
- Magic link/OTP passwordless flows
- Cross-device authentication sync
- MFA implementation (TOTP, passkeys as 2FA)
- Email/SMS recovery flows
- App Store compliance for social login

❌ **DO NOT use for:**
- Session management without auth context → use standard JWT patterns
- Authorization/RBAC policies → use `security-auditor` skill
- API key management → use `api-architect` skill
- Supabase RLS policies → use `supabase-admin` skill

---

## 2026 Authentication Landscape

### Industry Adoption Stats
- **Passkeys:** 87% of US/UK companies now use passkeys (FIDO Alliance)
- **Google:** 800+ million accounts use passkeys
- **Amazon:** 175 million users created passkeys in first year
- **Trend:** Passwordless is the security baseline, not a luxury

### Key Standards
| Standard | Purpose | Status |
|----------|---------|--------|
| WebAuthn L2 | Browser passkey API | Fully supported |
| FIDO2/CTAP2 | Cross-platform passkeys | Mature |
| OAuth 2.1 | Simplified OAuth | Replacing 2.0 |
| OAuth3 | Short-lived tokens | Emerging |
| Passkey Sync | iCloud/Google sync | Production |

---

## Architecture: Passwordless-First Design

### Recommended Auth Hierarchy (2026)

```
Primary Methods (Phishing-Resistant):
├── 1. Passkeys (WebAuthn) ← PREFERRED
│   ├── Platform authenticators (Face ID, Touch ID, Windows Hello)
│   └── Roaming authenticators (YubiKey, security keys)
├── 2. Social OAuth
│   ├── Google Sign-In (synced passkeys)
│   └── Apple Sign-In (privacy-focused)
│
Fallback Methods (Lower Security):
├── 3. Magic Links (email-based)
├── 4. Email OTP (time-limited codes)
└── 5. SMS OTP (deprecated - SIM swap risk)
    ⚠️ SMS should be last resort only

Legacy (Avoid):
└── 6. Password + Email ← DISCOURAGE
```

### Security Tier Comparison

| Method | Phishing-Resistant | Device-Bound | Sync-Capable | Friction |
|--------|-------------------|--------------|--------------|----------|
| Passkeys | ✅ Yes | ✅ Yes | ✅ Yes | Low |
| Hardware Key | ✅ Yes | ✅ Yes | ❌ No | Medium |
| Google OAuth | ⚠️ Partial | ❌ No | ✅ Yes | Low |
| Apple OAuth | ⚠️ Partial | ❌ No | ✅ Yes | Low |
| Magic Link | ❌ No | ❌ No | ✅ Yes | Medium |
| Email OTP | ❌ No | ❌ No | ✅ Yes | Medium |
| SMS OTP | ❌ No | ❌ No | ❌ No | Medium |
| Password | ❌ No | ❌ No | ✅ Yes | Low |

---

## Passkeys (WebAuthn) Implementation

### How Passkeys Work

```
Registration Flow:
┌──────────┐      ┌──────────┐      ┌──────────┐
│  User    │─────▶│  Browser │─────▶│  Server  │
│          │      │ WebAuthn │      │          │
└──────────┘      └──────────┘      └──────────┘
     │                  │                  │
     │  1. User clicks  │                  │
     │     "Register"   │                  │
     │                  │  2. Server sends │
     │                  │◀─ challenge +    │
     │                  │   user info      │
     │  3. Device shows │                  │
     │◀─ biometric      │                  │
     │                  │                  │
     │  4. User         │                  │
     │─▶ authenticates  │                  │
     │                  │  5. Send public  │
     │                  │─▶ key + signed   │
     │                  │   challenge      │
     │                  │                  │
     │                  │  6. Server stores│
     │                  │◀─ public key     │
     └──────────────────┴──────────────────┘

Key Points:
- Private key NEVER leaves device
- Server only stores public key
- Biometric data stays local
- Credential bound to domain (anti-phishing)
```

### Library Recommendations

**Frontend:**
```json
{
  "@simplewebauthn/browser": "^10.0.0",
  "next-passkey-webauthn": "^2.0.0"
}
```

**Backend:**
```json
{
  "@simplewebauthn/server": "^10.0.0"
}
```

### Next.js Passkey Implementation

**1. Database Schema (Supabase):**
```sql
-- Store passkey credentials
CREATE TABLE passkey_credentials (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  credential_id text UNIQUE NOT NULL,
  public_key bytea NOT NULL,
  counter integer DEFAULT 0,
  transports text[], -- e.g., ['internal', 'hybrid']
  device_type text, -- 'platform' or 'cross-platform'
  backed_up boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  last_used_at timestamptz
);

CREATE INDEX idx_passkey_user_id ON passkey_credentials(user_id);
CREATE INDEX idx_passkey_credential_id ON passkey_credentials(credential_id);

-- RLS policies
ALTER TABLE passkey_credentials ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own credentials" ON passkey_credentials
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own credentials" ON passkey_credentials
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own credentials" ON passkey_credentials
  FOR DELETE USING (auth.uid() = user_id);
```

**2. Registration API Route (app/api/passkeys/register/route.ts):**
```typescript
import { generateRegistrationOptions, verifyRegistrationResponse } from '@simplewebauthn/server';
import { createClient } from '@/lib/supabase/server';

const RP_NAME = 'Your App Name';
const RP_ID = process.env.NODE_ENV === 'production'
  ? 'yourapp.com'
  : 'localhost';

export async function POST(request: Request) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { step, credential } = await request.json();

  if (step === 'options') {
    // Get existing credentials to exclude
    const { data: existingCreds } = await supabase
      .from('passkey_credentials')
      .select('credential_id')
      .eq('user_id', user.id);

    const options = await generateRegistrationOptions({
      rpName: RP_NAME,
      rpID: RP_ID,
      userID: user.id,
      userName: user.email!,
      userDisplayName: user.user_metadata?.display_name || user.email!,
      attestationType: 'none', // For privacy
      excludeCredentials: existingCreds?.map(c => ({
        id: Buffer.from(c.credential_id, 'base64url'),
        type: 'public-key',
      })) || [],
      authenticatorSelection: {
        residentKey: 'preferred', // Discoverable credentials
        userVerification: 'preferred', // Biometric when available
        authenticatorAttachment: 'platform', // Device-bound (not roaming keys)
      },
    });

    // Store challenge in session (or use signed JWT)
    await supabase.from('auth_challenges').upsert({
      user_id: user.id,
      challenge: options.challenge,
      expires_at: new Date(Date.now() + 5 * 60 * 1000), // 5 min
    });

    return Response.json(options);
  }

  if (step === 'verify') {
    // Get stored challenge
    const { data: challengeData } = await supabase
      .from('auth_challenges')
      .select('challenge')
      .eq('user_id', user.id)
      .single();

    const verification = await verifyRegistrationResponse({
      response: credential,
      expectedChallenge: challengeData!.challenge,
      expectedOrigin: process.env.NEXT_PUBLIC_APP_URL!,
      expectedRPID: RP_ID,
    });

    if (verification.verified && verification.registrationInfo) {
      const { credentialID, credentialPublicKey, counter } = verification.registrationInfo;

      await supabase.from('passkey_credentials').insert({
        user_id: user.id,
        credential_id: Buffer.from(credentialID).toString('base64url'),
        public_key: Buffer.from(credentialPublicKey),
        counter,
        transports: credential.response.transports,
        device_type: verification.registrationInfo.credentialDeviceType,
        backed_up: verification.registrationInfo.credentialBackedUp,
      });

      return Response.json({ success: true });
    }

    return Response.json({ error: 'Verification failed' }, { status: 400 });
  }
}
```

**3. Authentication API Route (app/api/passkeys/authenticate/route.ts):**
```typescript
import { generateAuthenticationOptions, verifyAuthenticationResponse } from '@simplewebauthn/server';
import { createClient } from '@/lib/supabase/server';

export async function POST(request: Request) {
  const supabase = createClient();
  const { step, credential, email } = await request.json();

  if (step === 'options') {
    // For discoverable credentials, email is optional
    let userCredentials = [];

    if (email) {
      const { data: user } = await supabase
        .from('profiles')
        .select('id')
        .eq('email', email)
        .single();

      if (user) {
        const { data: creds } = await supabase
          .from('passkey_credentials')
          .select('credential_id, transports')
          .eq('user_id', user.id);

        userCredentials = creds || [];
      }
    }

    const options = await generateAuthenticationOptions({
      rpID: RP_ID,
      userVerification: 'preferred',
      allowCredentials: userCredentials.length ? userCredentials.map(c => ({
        id: Buffer.from(c.credential_id, 'base64url'),
        type: 'public-key',
        transports: c.transports,
      })) : undefined, // Empty = discoverable credential flow
    });

    // Store challenge
    await supabase.from('auth_challenges').upsert({
      challenge_id: options.challenge,
      challenge: options.challenge,
      expires_at: new Date(Date.now() + 5 * 60 * 1000),
    });

    return Response.json(options);
  }

  if (step === 'verify') {
    // Find credential
    const credentialId = Buffer.from(credential.id, 'base64url').toString('base64url');

    const { data: storedCred } = await supabase
      .from('passkey_credentials')
      .select('*, profiles!inner(email)')
      .eq('credential_id', credentialId)
      .single();

    if (!storedCred) {
      return Response.json({ error: 'Credential not found' }, { status: 401 });
    }

    // Get challenge
    const { data: challengeData } = await supabase
      .from('auth_challenges')
      .select('challenge')
      .eq('challenge_id', credential.response.clientDataJSON.challenge)
      .single();

    const verification = await verifyAuthenticationResponse({
      response: credential,
      expectedChallenge: challengeData!.challenge,
      expectedOrigin: process.env.NEXT_PUBLIC_APP_URL!,
      expectedRPID: RP_ID,
      authenticator: {
        credentialID: Buffer.from(storedCred.credential_id, 'base64url'),
        credentialPublicKey: storedCred.public_key,
        counter: storedCred.counter,
      },
    });

    if (verification.verified) {
      // Update counter
      await supabase
        .from('passkey_credentials')
        .update({
          counter: verification.authenticationInfo.newCounter,
          last_used_at: new Date(),
        })
        .eq('id', storedCred.id);

      // Create Supabase session
      const { data: session } = await supabase.auth.admin.generateLink({
        type: 'magiclink',
        email: storedCred.profiles.email,
      });

      return Response.json({
        success: true,
        session: session.properties?.hashed_token
      });
    }

    return Response.json({ error: 'Verification failed' }, { status: 401 });
  }
}
```

**4. Frontend Hook (hooks/usePasskey.ts):**
```typescript
import { startRegistration, startAuthentication } from '@simplewebauthn/browser';
import { useState } from 'react';

export function usePasskey() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registerPasskey = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Get options from server
      const optionsRes = await fetch('/api/passkeys/register', {
        method: 'POST',
        body: JSON.stringify({ step: 'options' }),
      });
      const options = await optionsRes.json();

      // Start WebAuthn registration
      const credential = await startRegistration(options);

      // Verify with server
      const verifyRes = await fetch('/api/passkeys/register', {
        method: 'POST',
        body: JSON.stringify({ step: 'verify', credential }),
      });

      if (!verifyRes.ok) {
        throw new Error('Verification failed');
      }

      return true;
    } catch (err: any) {
      // Handle user cancellation gracefully
      if (err.name === 'NotAllowedError') {
        setError('Passkey registration cancelled');
      } else {
        setError(err.message);
      }
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const authenticateWithPasskey = async (email?: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const optionsRes = await fetch('/api/passkeys/authenticate', {
        method: 'POST',
        body: JSON.stringify({ step: 'options', email }),
      });
      const options = await optionsRes.json();

      const credential = await startAuthentication(options);

      const verifyRes = await fetch('/api/passkeys/authenticate', {
        method: 'POST',
        body: JSON.stringify({ step: 'verify', credential }),
      });

      if (!verifyRes.ok) {
        throw new Error('Authentication failed');
      }

      const { session } = await verifyRes.json();
      // Exchange for Supabase session
      // ...
      return true;
    } catch (err: any) {
      if (err.name === 'NotAllowedError') {
        setError('Passkey authentication cancelled');
      } else {
        setError(err.message);
      }
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const isSupported = typeof window !== 'undefined' &&
    window.PublicKeyCredential !== undefined;

  return {
    registerPasskey,
    authenticateWithPasskey,
    isSupported,
    isLoading,
    error,
  };
}
```

---

## OAuth: Google Sign-In

### Setup Requirements

1. **Google Cloud Console:**
   - Create OAuth 2.0 Client ID (Web application)
   - Add authorized JavaScript origins: `https://yourapp.com`
   - Add authorized redirect URIs: `https://yourapp.supabase.co/auth/v1/callback`

2. **Supabase Dashboard:**
   - Authentication → Providers → Google
   - Add Client ID and Client Secret
   - Enable "Sign in with Google"

### Implementation

**Supabase Client (Next.js):**
```typescript
import { createClient } from '@/lib/supabase/client';

async function signInWithGoogle() {
  const supabase = createClient();

  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`,
      queryParams: {
        access_type: 'offline', // For refresh tokens
        prompt: 'consent', // Force consent screen
      },
    },
  });

  if (error) {
    console.error('Google sign-in error:', error);
  }
}
```

**Native Mobile (React Native/Expo):**
```typescript
import * as Google from 'expo-auth-session/providers/google';
import { createClient } from '@supabase/supabase-js';

export function useGoogleAuth() {
  const [request, response, promptAsync] = Google.useIdTokenAuthRequest({
    clientId: process.env.EXPO_PUBLIC_GOOGLE_CLIENT_ID,
    iosClientId: process.env.EXPO_PUBLIC_GOOGLE_IOS_CLIENT_ID,
    androidClientId: process.env.EXPO_PUBLIC_GOOGLE_ANDROID_CLIENT_ID,
  });

  useEffect(() => {
    if (response?.type === 'success') {
      const { id_token } = response.params;

      supabase.auth.signInWithIdToken({
        provider: 'google',
        token: id_token,
      });
    }
  }, [response]);

  return { signIn: () => promptAsync(), isLoading: !request };
}
```

---

## OAuth: Apple Sign-In

### App Store Requirements (2024+)

⚠️ **Critical Compliance Rule:**

> Apps that use third-party login (Google, Facebook, etc.) must also offer an **equivalent privacy-focused option**. Sign in with Apple satisfies this requirement.

**Required if you offer:** Google, Facebook, Twitter, Amazon, WeChat login
**Exception:** Enterprise/education apps with existing SSO

### Setup Requirements

1. **Apple Developer Portal:**
   - Enable "Sign in with Apple" capability
   - Create Service ID for web
   - Create Key (.p8 file) for token generation
   - ⚠️ **Key expires every 6 months** - set calendar reminder!

2. **Supabase Dashboard:**
   - Authentication → Providers → Apple
   - Add Service ID, Team ID, Key ID
   - Upload .p8 key file

### Implementation

**Web (Supabase):**
```typescript
async function signInWithApple() {
  const supabase = createClient();

  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'apple',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`,
    },
  });

  if (error) {
    console.error('Apple sign-in error:', error);
  }
}
```

**Native iOS (Swift):**
```swift
import AuthenticationServices

func handleAppleSignIn() async throws {
    let appleIDProvider = ASAuthorizationAppleIDProvider()
    let request = appleIDProvider.createRequest()
    request.requestedScopes = [.fullName, .email]

    let result = try await performSignIn(request)

    // Extract ID token
    guard let identityToken = result.credential.identityToken,
          let tokenString = String(data: identityToken, encoding: .utf8) else {
        throw AuthError.missingToken
    }

    // Sign in to Supabase
    try await supabase.auth.signInWithIdToken(
        credentials: .init(
            provider: .apple,
            idToken: tokenString
        )
    )
}
```

---

## Magic Links (Email Passwordless)

### Best Practices

```typescript
// ✅ Good: Short TTL, single-use
const { error } = await supabase.auth.signInWithOtp({
  email: user.email,
  options: {
    emailRedirectTo: `${origin}/auth/callback`,
    shouldCreateUser: true, // Auto-create on first login
  },
});

// Configure in Supabase Dashboard:
// - Magic Link expiry: 5-10 minutes (shorter is safer)
// - Rate limit: 3 per hour per email
```

### Email Template Customization

```html
<!-- Supabase Dashboard → Auth → Email Templates → Magic Link -->
<h2>Sign in to {{ .SiteURL }}</h2>
<p>Click the link below to sign in. This link expires in 10 minutes.</p>
<p><a href="{{ .ConfirmationURL }}">Sign in to Your Account</a></p>
<p>If you didn't request this, you can safely ignore this email.</p>
```

---

## Recovery Flows

### Email Recovery (Password Reset)

```typescript
// Request reset
await supabase.auth.resetPasswordForEmail(email, {
  redirectTo: `${origin}/auth/update-password`,
});

// Update password (on /auth/update-password page)
await supabase.auth.updateUser({ password: newPassword });
```

### Account Recovery Hierarchy

```
Recovery Options (in order of security):
1. Backup Passkey (stored on different device)
2. Trusted Recovery Contact (delegated access)
3. Email verification + Security questions
4. Email-only recovery (last resort)
5. SMS recovery ⚠️ (vulnerable to SIM swap)
```

### Implementing Backup Passkeys

```typescript
// Prompt user to register backup device after primary
function PromptBackupPasskey() {
  const [hasBackup, setHasBackup] = useState(false);
  const { data: credentials } = usePasskeyCredentials();

  useEffect(() => {
    // Check if user has only one passkey
    if (credentials?.length === 1) {
      setHasBackup(false);
    }
  }, [credentials]);

  if (hasBackup) return null;

  return (
    <div className="bg-amber-50 border border-amber-200 p-4 rounded-lg">
      <h3>Add a Backup Passkey</h3>
      <p>Register a passkey on another device to ensure account recovery.</p>
      <Button onClick={registerPasskey}>Add Backup Device</Button>
    </div>
  );
}
```

---

## Cross-Device Sync

### How Passkey Sync Works

```
Device A (iPhone)              iCloud Keychain              Device B (Mac)
┌─────────────────┐           ┌─────────────┐           ┌─────────────────┐
│ Create Passkey  │──────────▶│ E2E Encrypt │──────────▶│ Passkey Ready   │
│ for example.com │           │ & Sync      │           │ to use          │
└─────────────────┘           └─────────────┘           └─────────────────┘

Google Password Manager:
- Android devices synced
- Chrome browser synced
- Windows via Chrome

Apple iCloud Keychain:
- All Apple devices synced
- Safari on all platforms
- Shared with Family Sharing (optional)
```

### Cross-Platform Authentication (QR Code)

When user wants to sign in on a device without their passkey:

```typescript
// Device A shows QR code
// User scans with phone (Device B) that has passkey
// Phone authenticates via Bluetooth proximity

// This is handled automatically by the browser's WebAuthn implementation
// No additional code needed - just allow hybrid transports:

const options = await generateAuthenticationOptions({
  rpID: RP_ID,
  authenticatorSelection: {
    // Allow cross-device (QR code) authentication
    authenticatorAttachment: undefined, // Don't restrict
  },
});
```

---

## Supabase Auth Configuration Checklist

### Dashboard Settings

1. **Authentication → Settings:**
   - [ ] Site URL: `https://yourapp.com`
   - [ ] Redirect URLs: Add all valid callbacks
   - [ ] JWT Expiry: 3600 (1 hour)
   - [ ] Enable email confirmations: Yes

2. **Authentication → Providers → Email:**
   - [ ] Enable Email: Yes
   - [ ] Confirm email: Yes (recommended)
   - [ ] Secure email change: Yes
   - [ ] Double confirm email: No (reduces friction)

3. **Authentication → Email Templates:**
   - [ ] Customize all templates
   - [ ] Test email delivery
   - [ ] Set appropriate expiry times

4. **Authentication → Rate Limiting:**
   - [ ] Email: 3 per hour
   - [ ] SMS: 3 per hour
   - [ ] Magic links: 3 per 5 minutes

### Environment Variables

```env
# Required
NEXT_PUBLIC_SUPABASE_URL=https://yourproject.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Apple OAuth
APPLE_SERVICE_ID=your-service-id
APPLE_TEAM_ID=your-team-id
APPLE_KEY_ID=your-key-id
APPLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."

# Passkeys
PASSKEY_RP_ID=yourapp.com
PASSKEY_RP_NAME="Your App Name"
```

---

## Common Issues & Solutions

### Issue: Sign-up says "Check email" but no email arrives

**Cause:** Email confirmation not configured in Supabase Dashboard

**Solution:**
1. Go to Supabase Dashboard → Authentication → Providers → Email
2. Verify "Confirm email" is enabled
3. Check email templates are configured
4. Verify SMTP settings (or use Supabase's built-in email)
5. Check spam folder

### Issue: Apple Sign-In suddenly stops working

**Cause:** Apple .p8 key expired (6-month limit)

**Solution:**
1. Generate new key in Apple Developer Portal
2. Update key in Supabase Dashboard
3. Set calendar reminder for next expiry

### Issue: Google OAuth redirect error

**Cause:** Redirect URI mismatch

**Solution:**
1. Verify redirect URI in Google Cloud Console matches exactly:
   - `https://yourproject.supabase.co/auth/v1/callback`
2. Check for trailing slashes
3. Ensure HTTP vs HTTPS matches

### Issue: Passkey not syncing between devices

**Cause:** Credential created with wrong attachment type

**Solution:**
```typescript
// Use 'platform' for synced credentials
authenticatorAttachment: 'platform', // NOT 'cross-platform'

// 'cross-platform' = hardware security keys (no sync)
// 'platform' = device biometrics (sync via iCloud/Google)
```

---

## Security Best Practices

### Token Management

```typescript
// ✅ Good: Short-lived access tokens + refresh
const session = await supabase.auth.getSession();
// Access token: 1 hour
// Refresh token: 7 days (rotate on use)

// ✅ Good: Secure token storage
// Browser: HttpOnly cookies (Supabase handles this)
// Mobile: Secure Keychain/Keystore

// ❌ Bad: Long-lived tokens in localStorage
localStorage.setItem('token', longLivedToken); // DON'T
```

### Rate Limiting

```typescript
// Implement rate limiting on auth endpoints
const rateLimit = {
  signIn: { max: 5, windowMs: 15 * 60 * 1000 }, // 5 per 15 min
  signUp: { max: 3, windowMs: 60 * 60 * 1000 }, // 3 per hour
  passwordReset: { max: 3, windowMs: 60 * 60 * 1000 },
  passkey: { max: 10, windowMs: 15 * 60 * 1000 },
};
```

### Secure Defaults

```typescript
// Always verify email on signup
const { error } = await supabase.auth.signUp({
  email,
  password,
  options: {
    emailRedirectTo: `${origin}/auth/callback`,
    // Supabase will only create confirmed user after email click
  },
});

// Require email verification for sensitive actions
async function sensitiveAction(userId: string) {
  const { data: user } = await supabase.auth.getUser();

  if (!user?.email_confirmed_at) {
    throw new Error('Please verify your email first');
  }

  // Proceed with action...
}
```

---

## References

### Official Documentation
- [Google Passkeys Developer Guide](https://developers.google.com/identity/passkeys/developer-guides)
- [Apple Sign in with Apple](https://developer.apple.com/sign-in-with-apple/)
- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [WebAuthn Spec](https://www.w3.org/TR/webauthn-2/)

### Libraries
- [SimpleWebAuthn](https://simplewebauthn.dev/) - Recommended WebAuthn library
- [Corbado](https://www.corbado.com/blog/supabase-passkeys) - Passkey-as-a-service option
- [Hanko](https://www.hanko.io/) - Open-source passkey server

### Research (2026)
- [Authentication Trends in 2026](https://www.c-sharpcorner.com/article/authentication-trends-in-2026-passkeys-oauth3-and-webauthn/)
- [Passwordless & MFA in 2026](https://securityboulevard.com/2025/12/passwordless-mfa-in-2026-passkeys-push-mfa-device-trust/)
- [FIDO Alliance Passkey Index](https://fidoalliance.org/)
