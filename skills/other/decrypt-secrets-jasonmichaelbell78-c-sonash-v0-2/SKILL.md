---
name: decrypt-secrets
description: Decrypt MCP tokens for remote sessions
---

# Decrypt Secrets

Decrypt your encrypted MCP tokens at the start of a remote session.

## When to Use

- At the start of a remote/web session when MCP servers need tokens
- When you see "Encrypted secrets found but not decrypted" in session startup
- When MCP servers fail due to missing authentication

## How It Works

1. Your tokens are stored encrypted in `.env.local.encrypted` (safe to commit)
2. Running this decrypts them to `.env.local` (gitignored)
3. MCP servers then use the tokens automatically

## Instructions

Run the decryption script and enter your passphrase:

```bash
node scripts/secrets/decrypt-secrets.js
```

You'll be prompted for the passphrase you set when encrypting.

## First-Time Setup

If you haven't encrypted your secrets yet:

1. Add your tokens to `.env.local`:

   ```
   GITHUB_TOKEN=ghp_your_token
   SONAR_TOKEN=sqp_your_token
   CONTEXT7_API_KEY=your_key
   ```

2. Encrypt them:

   ```bash
   node scripts/secrets/encrypt-secrets.js
   ```

3. Commit `.env.local.encrypted` to your repo

4. In future sessions, just run the decrypt script

## Security Notes

- `.env.local` is gitignored - your actual tokens are never committed
- `.env.local.encrypted` uses AES-256-GCM encryption
- Choose a strong passphrase (8+ characters)
- Your passphrase is never stored anywhere
