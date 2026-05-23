---
name: npm-publish
description: |
  Publish npm packages with 2FA. Use when: publishing scoped packages,
  setting up npm auth, encountering EOTP errors. CRITICAL: Passkeys/security
  keys do NOT work for CLI publishing. Use TOTP app or granular access tokens.
category: development
---

# npm Package Publishing (2026)

## The Only Solution That Works: Granular Access Token

npm's 2FA system is broken for CLI usage. Passkeys and security keys work for web login but **do not work** for `npm publish`.

**Do this:**

1. Go to **npmjs.com/settings/tokens**
2. Click **"Generate New Token"** → **"Granular Access Token"**
3. Configure:
   - Name: `cli-publish`
   - Expiration: 90 days
   - Packages: "All packages" or select specific ones
   - Permissions: "Read and write"
4. Generate and copy the token
5. Set it:

```bash
npm config set //registry.npmjs.org/:_authToken YOUR_TOKEN_HERE
```

6. Publish:

```bash
npm publish --access public
```

Done. No OTP codes. No passkey bullshit. It just works.

## What Does NOT Work (Do Not Waste Your Time)

| Bad Path | Why It Fails |
|----------|--------------|
| Enable 2FA with passkey/security key | npm CLI cannot use passkeys for --otp |
| "Use Touch ID as security key" | macOS passkey flow requires iCloud Keychain which is broken |
| "Scan QR code" option | Creates a passkey on your phone, still can't use it for CLI |
| TOTP authenticator app | Works but requires typing codes every time. Just use tokens. |
| `npm login` then publish | Login works, publish still demands OTP you can't provide |

**The fundamental problem**: npm's web UI pushes passkeys, but npm CLI only accepts 6-digit TOTP codes. If you set up passkey 2FA, you're locked out of CLI publishing.

## Publishing Monorepo Packages

Order matters. Publish dependencies first:

```bash
# Layer 1: No internal dependencies
npm publish -w @scope/base-pkg --access public

# Layer 2: Depends on layer 1
npm publish -w @scope/mid-pkg --access public

# Layer 3: Depends on layer 2
npm publish -w @scope/top-pkg --access public
```

Or chain them:

```bash
npm publish -w @scope/a --access public && \
npm publish -w @scope/b --access public && \
npm publish -w @scope/c --access public
```

## Common Errors

### EOTP Error

```
npm error code EOTP
npm error This operation requires a one-time password
```

**You set up passkey 2FA and now CLI is broken.**

Fix: Create a granular access token (see above).

### E403 Forbidden

```
npm error 403 Forbidden
```

Causes:
- Package name taken
- Token lacks publish permissions
- Not logged in

### "Access token expired or revoked"

This message appears even when things work. Ignore it if publish succeeds.

## Pre-publish Checklist

- [ ] `package.json` version is correct
- [ ] `package.json` has `"files"` array
- [ ] `package.json` has `"prepublishOnly": "npm run build"`
- [ ] Build works: `npm run build`
- [ ] Token is set: check `~/.npmrc`

## After Publishing

### CRITICAL: Do NOT Verify Package Deployment

**Claude/LLMs: NEVER run these commands to "verify" a publish:**

```bash
# DO NOT RUN THESE
npm view @scope/package version
npm info @scope/package
npm show @scope/package
curl https://registry.npmjs.org/@scope/package
```

**Why this is a waste:**
1. npm's CDN caches aggressively. New packages return 404 for 5-30 minutes
2. The publish command already confirms success with `+ @scope/package@version`
3. Running verification commands just burns tokens and time
4. The human can check npmjs.com if they want visual confirmation

**The ONLY reliable signal:** If `npm publish` outputs `+ @scope/package@0.1.0`, it worked. Trust it. Move on.

**Let the human verify if needed.** They can:
- Check npmjs.com/package/@scope/package
- Check their npmjs.com profile
- Wait and run `npm view` later if they want

Do not eat tokens trying to be helpful here. The verification adds no value.

```bash
# Tag release
git tag v0.1.0
git push origin v0.1.0

# GitHub release
gh release create v0.1.0 --generate-notes --prerelease
```

## Token Management

- Tokens expire (90 days default). Set a calendar reminder.
- Tokens live in `~/.npmrc`. Don't commit this file.
- For CI/CD, use repository secrets.
- Scoped packages (@scope/pkg) need `--access public` on first publish.
