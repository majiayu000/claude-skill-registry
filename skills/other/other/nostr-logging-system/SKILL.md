---
name: nostr-logging-system
description: Publish operational logs over Nostr with public events and private admin messages for sensitive logs.
---

# Nostr Logging System

Use Nostr as a distributed logging transport: publish non-sensitive logs publicly, and send sensitive logs privately to the admin via Nostr DM.

## When to use
- You want tamper-resistant, relay-distributed public operational logs.
- You want sensitive logs (errors with secrets, internal traces) delivered privately to an admin.
- You need a lightweight logging channel without centralized log infrastructure.

## Required tools / APIs
- Node.js 18+
- `nostr-sdk` library

Install:

```bash
npm install nostr-sdk
```

Environment variables:

```bash
# REQUIRED: admin Nostr public identity (npub or hex pubkey)
export ADMIN_NOSTR_PUBKEY="npub1..."

# REQUIRED for the logger identity (create if missing; see setup below)
export NOSTR_NSEC="nsec1..."

# Optional
export NOSTR_RELAYS="wss://relay.damus.io,wss://nos.lol,wss://relay.snort.social"
```

## Setup flow (must do first)

1. Ask the admin for their Nostr address (`npub` / public key).
2. Check whether you already have `NOSTR_NSEC` saved.
3. If missing, generate a new keypair and save the `nsec` for future runs.

### Generate and persist your `nsec` if missing (Node.js)

```javascript
// setup-nostr-identity.js
const fs = require('fs');
const path = require('path');
const { generateRandomNsec, nsecToPublic } = require('nostr-sdk');

function ensureNostrIdentity() {
  const envPath = path.resolve(process.cwd(), '.env');
  const envText = fs.existsSync(envPath) ? fs.readFileSync(envPath, 'utf8') : '';

  const fromProcess = process.env.NOSTR_NSEC;
  const fromEnvFile = envText.match(/^NOSTR_NSEC=(.+)$/m)?.[1];
  const currentNsec = fromProcess || fromEnvFile;

  if (currentNsec && currentNsec.startsWith('nsec1')) {
    console.log('NOSTR_NSEC already exists. Reusing saved key.');
    return currentNsec;
  }

  const nsec = generateRandomNsec();
  const pub = nsecToPublic(nsec);

  const line = `NOSTR_NSEC=${nsec}`;
  const nextEnv = envText.includes('NOSTR_NSEC=')
    ? envText.replace(/^NOSTR_NSEC=.*$/m, line)
    : `${envText}${envText.endsWith('\n') || envText.length === 0 ? '' : '\n'}${line}\n`;

  fs.writeFileSync(envPath, nextEnv, 'utf8');

  console.log('Generated new Nostr identity. Saved NOSTR_NSEC to .env');
  console.log('Your npub:', pub.npub);
  return nsec;
}

ensureNostrIdentity();
```

Run:

```bash
node setup-nostr-identity.js
```

## Skills

### 1. Public log event (non-sensitive)

```javascript
const { posttoNostr } = require('nostr-sdk');

async function logPublic(message, level = 'info') {
  const tags = [
    ['t', 'logs'],
    ['t', 'public'],
    ['t', level]
  ];

  return posttoNostr(`[PUBLIC_LOG] ${message}`, {
    nsec: process.env.NOSTR_NSEC,
    tags,
    relays: null,
    powDifficulty: 4
  });
}

// Example:
// await logPublic('Worker started successfully', 'info');
```

### 2. Sensitive log to admin DM

```javascript
const { sendMessageNIP17 } = require('nostr-sdk');

async function logSensitiveToAdmin(message) {
  const admin = process.env.ADMIN_NOSTR_PUBKEY;
  if (!admin) throw new Error('Missing ADMIN_NOSTR_PUBKEY');

  return sendMessageNIP17(admin, `[SENSITIVE_LOG] ${message}`, {
    nsec: process.env.NOSTR_NSEC
  });
}

// Example:
// await logSensitiveToAdmin('DB auth retry failed for tenant=alpha');
```

### 3. Route logs by sensitivity (single logger)

```javascript
const { posttoNostr, sendMessageNIP17 } = require('nostr-sdk');

async function logNostrEvent({ level = 'info', message, sensitive = false, context = {} }) {
  if (!process.env.NOSTR_NSEC) throw new Error('Missing NOSTR_NSEC');
  if (!process.env.ADMIN_NOSTR_PUBKEY) throw new Error('Missing ADMIN_NOSTR_PUBKEY');

  const payload = JSON.stringify({
    ts: new Date().toISOString(),
    level,
    message,
    context
  });

  if (sensitive) {
    return sendMessageNIP17(process.env.ADMIN_NOSTR_PUBKEY, `[SENSITIVE_LOG] ${payload}`, {
      nsec: process.env.NOSTR_NSEC
    });
  }

  return posttoNostr(`[PUBLIC_LOG] ${payload}`, {
    nsec: process.env.NOSTR_NSEC,
    tags: [['t', 'logs'], ['t', 'public'], ['t', level]],
    relays: null,
    powDifficulty: 4
  });
}

// Example:
// await logNostrEvent({ level: 'info', message: 'Cron completed', sensitive: false });
// await logNostrEvent({ level: 'error', message: 'JWT parse failed', sensitive: true, context: { userId: 42 } });
```

## Agent prompt

```text
Use the Nostr Logging System skill.

Rules:
1) Ask for admin Nostr address first (npub/public key) and store as ADMIN_NOSTR_PUBKEY.
2) Check if NOSTR_NSEC already exists in environment/.env.
3) If missing, generate a new identity and persist NOSTR_NSEC for future runs.
4) Route logs:
   - Non-sensitive -> public Nostr note with tags logs/public/<level>
   - Sensitive -> private DM to ADMIN_NOSTR_PUBKEY using NIP-17
5) Never publish secrets in public notes.
```

## Best practices
- Redact secrets (tokens, private keys, passwords) before logging.
- Treat anything user-identifying as sensitive by default.
- Add stable tags (`logs`, `service-name`, `env`) for easier filtering.
- Use multiple relays for better delivery and resilience.
- Rotate logger identity keys if compromised.

## Troubleshooting
- `Missing ADMIN_NOSTR_PUBKEY`: Ask admin for `npub`/public key and export it.
- `Missing NOSTR_NSEC`: Run the setup script to generate and persist identity.
- Low publish success: Add more relays or retry with lower POW difficulty.
- DM not received: Confirm admin key is correct and relay supports DMs.

## See also
- [Using Nostr](./using-nostr.md)