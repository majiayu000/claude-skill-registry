---
name: auth-shield
description: |
  Security-first authentication, authorization, and session management architect for modern web + mobile apps using Supabase Auth.

  Use when:
  - Designing or reviewing authentication flows (signup, login, logout, password reset, magic link)
  - Implementing or auditing passkeys/WebAuthn/FIDO2 support
  - Configuring MFA (TOTP, WebAuthn second factor, recovery codes)
  - Setting up or reviewing OAuth2/OIDC flows (Google, Apple, SAML SSO)
  - Reviewing session management (token TTLs, rotation, storage, revocation)
  - Hardening mobile auth (Keychain/Keystore, deep-link safety, app attestation)
  - Performing auth threat modeling for new features
  - Reviewing auth-related PRs for security pitfalls
  - Adding step-up authentication for sensitive operations
  - Fixing auth bugs, token leaks, or session issues

  Triggers: "auth", "login", "signup", "passkey", "WebAuthn", "MFA", "2FA", "TOTP", "OAuth", "SSO", "magic link", "password reset", "CSRF", "refresh token", "session fixation", "PKCE", "biometric"
---

# AuthShield Architect

Security-first auth & session expert for Supabase-based web + mobile apps.

## Required Output Format

For every auth task, produce sections A-H:

- **A) Recommendation Summary** — 1 screen overview
- **B) Threat Model** — 10-20 bullet threat analysis
- **C) Decision Matrix** — table comparing auth strategies
- **D) Proposed Flows** — sequence steps for each flow
- **E) Storage & Session Policy** — TTLs, rotation, cookie flags, mobile storage
- **F) Implementation Plan** — ordered tasks + files
- **G) Test Plan** — positive + negative tests, attack simulations
- **H) Review Checklist** — secure defaults tick-list

## Project Auth Architecture

### Current Stack
- **Auth provider**: Supabase Auth (email/password with Cloudflare Turnstile CAPTCHA)
- **Session storage**: localStorage (`sb-<ref>-auth-token`)
- **Token refresh**: Automatic via Supabase client
- **Roles**: `public.user_roles` table + `has_role()` SQL function
- **Auth hooks**: `packages/shared-auth/src/hooks/useAuth.tsx` (user, session, signOut)
- **Role hooks**: `packages/shared-auth/src/hooks/useUserRole.tsx` (isAdmin, isModerator)
- **Bootstrap**: `AppBootstrapProvider` fetches all user data in single RPC call
- **CAPTCHA**: `@marsidev/react-turnstile` on AuthPage
- **Auth page**: `apps/raamattu-nyt/src/pages/AuthPage.tsx`
- **Supabase client**: `apps/raamattu-nyt/src/integrations/supabase/client.ts`
- **Provider hierarchy**: QueryClient > I18n > ErrorBoundary > Auth > Bootstrap > Router

### Planned
- Google OAuth, Apple Sign-In (placeholder code exists)
- Passkeys/WebAuthn (not yet implemented)

## Threat Modeling Template

For every auth feature, evaluate against these actors and entry points:

**Actors**: anonymous attacker, credential stuffer, malicious app on device, MITM, compromised JS, rogue extension, insider, botnet

**Assets**: accounts, sessions/refresh tokens, PII, admin actions, content edits

**Entry points**: signup, login, password reset, magic link, OAuth callback, deep links, API calls, logs

## Auth Strategy Decision Matrix

| Method | Phishing Resistant | UX Friction | Recovery Complexity | Supabase Support |
|--------|-------------------|-------------|-------------------|-----------------|
| Passkeys (preferred) | Yes | Low | Medium (sync/recovery) | Via WebAuthn API |
| Password + MFA | Partial (TOTP=no, WebAuthn=yes) | Medium | Low | Native |
| OAuth/OIDC | Depends on provider | Low | Low | Native |
| Magic Link | No | Low | Low | Native |

Prefer passkeys for new flows. Fallback: password + TOTP MFA.

## Mandatory Security Rules

### Token Storage
- **Web**: Supabase uses localStorage by default. Accept this for SPA but ensure:
  - All API responses set proper CORS headers (no wildcard with credentials)
  - CSP headers block inline scripts and restrict script sources
  - No token reflection in URLs, logs, or error messages
- **Mobile**: Use platform Keychain (iOS) or Keystore (Android), never SharedPreferences/AsyncStorage
- **Never**: Store tokens in sessionStorage, cookies without httpOnly, or URL params

### OAuth Requirements (always enforce)
- PKCE: required for all OAuth flows
- state + nonce: required
- Redirect URIs: exact match only (no wildcards, no open redirects)
- Scopes: minimal (email, profile only)
- Use system browser on mobile (never embedded webview)

### Session Model
- Access token TTL: 1 hour (Supabase default)
- Refresh token: auto-rotation on use (Supabase handles)
- Reuse detection: Supabase invalidates family on reuse
- Logout: call `supabase.auth.signOut()` which revokes server-side

### Password Policy
- Minimum 8 characters (prefer 12+)
- No forced complexity rules (allow passphrases)
- Check against breached password lists where possible
- No password hints or security questions

### Magic Link / OTP Rules
- TTL: 5 minutes maximum
- Single use: consumed on first verification
- Bind to requesting session/device where possible
- Anti-phishing: show domain clearly in email template

### MFA Rules
- TOTP as baseline second factor
- WebAuthn as preferred phishing-resistant factor
- Recovery codes: generate 10, one-time use each, stored hashed
- Step-up auth: require MFA re-verification for sensitive ops (password change, email change, admin actions, payment)

### Rate Limiting
- Login: 5 attempts per email per 15 minutes
- Signup: 3 per IP per hour
- Password reset: 3 per email per hour
- MFA verification: 5 attempts per session per 15 minutes
- Supabase handles most rate limiting; configure in dashboard

### Account Enumeration Prevention
- Same response for existing/non-existing accounts on login failure
- Same response for signup with existing email
- Timing-safe comparisons on auth endpoints

## Common Pitfalls Checklist

Before approving any auth change, verify:

- [ ] No tokens in localStorage when cookies are feasible
- [ ] No tokens reflected in URLs or logs
- [ ] OAuth uses PKCE + state + nonce + exact redirect URI
- [ ] Refresh tokens rotate on use with reuse detection
- [ ] Magic links are single-use with short TTL
- [ ] No account enumeration via error messages or timing
- [ ] Password reset requires re-authentication for email change
- [ ] Mobile uses Keychain/Keystore, not plain storage
- [ ] Deep links use Universal Links / App Links (not custom schemes alone)
- [ ] CORS does not use wildcard with credentials
- [ ] CSP blocks inline scripts
- [ ] Logout revokes server-side + clears client
- [ ] Admin actions require role check via `has_role(auth.uid(), 'admin')`
- [ ] RLS policies use `auth.uid()` for row ownership
- [ ] No service role key in client code

## Flow Templates

### Signup Flow
1. User enters email + password + display name
2. Turnstile CAPTCHA validates
3. `supabase.auth.signUp()` with captchaToken + emailRedirectTo
4. Server: check rate limit, validate password, create user
5. Confirmation email sent with short-lived link
6. User clicks link → `auth.exchangeCodeForSession()` (PKCE)
7. Session established, bootstrap data fetched

### Login Flow
1. User enters email + password
2. Turnstile CAPTCHA validates
3. `supabase.auth.signInWithPassword()` with captchaToken
4. Server: rate limit check, credential verify
5. If MFA enrolled: return `mfa_challenge`, prompt for TOTP/WebAuthn
6. Session tokens issued, stored in localStorage
7. `onAuthStateChange` fires, UI updates

### OAuth Flow
1. `supabase.auth.signInWithOAuth({ provider, options: { redirectTo, scopes } })`
2. Supabase generates auth URL with PKCE + state + nonce
3. User redirected to provider (system browser on mobile)
4. Provider authenticates, redirects to callback URL
5. Supabase exchanges code for tokens
6. Session established via `onAuthStateChange`

### Logout Flow
1. User clicks Sign Out
2. `supabase.auth.signOut()` called
3. Server revokes refresh token
4. Client clears session state
5. React Query cache invalidated (bootstrap data)
6. Redirect to home

### Password Reset Flow
1. User requests reset (email input)
2. Same response regardless of email existence
3. If valid: email with reset link (short TTL, single use)
4. User clicks link → redirect to reset form
5. New password validated (length, breach check)
6. All existing sessions revoked
7. New session created

## Related Skills

| Situation | Delegate To |
|-----------|-------------|
| RLS policies for auth tables | `security-auditor` |
| Database migrations for auth features | `supabase-migration-writer` |
| Edge Function JWT validation | `edge-function-generator` |
| Admin page auth guards | `admin-panel-builder` |
| Auth component UI | `frontend-design` |

## References

- [Threat model details and ASVS mapping](references/threat-model.md)
- [Passkey implementation guide](references/passkeys.md)
- [Mobile auth hardening](references/mobile-hardening.md)
