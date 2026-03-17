---
name: libsecret
description: >
  libsecret - Secret generation and environment utilities. generateSecret
  creates cryptographic random secrets. generateSecretB64 creates base64url
  secrets. createJwt signs HS256 JSON Web Tokens. getEnvVar and setEnvVar manage
  .env files. hashValues creates deterministic hashes. Use for credential
  management, JWT creation, and environment configuration.
---

# libsecret Skill

## When to Use

- Generating cryptographic secrets for APIs
- Creating and signing JWTs
- Managing .env file variables
- Creating deterministic hashes from values

## Key Concepts

**Secret generation**: Cryptographically secure random string generation for API
keys and tokens.

**JWT creation**: HS256-signed JSON Web Tokens for authentication.

**Environment management**: Read/write .env files programmatically.

## Usage Patterns

### Pattern 1: Generate secrets

```javascript
import { generateSecret, generateSecretB64 } from "@copilot-ld/libsecret";

const apiKey = generateSecret(); // hex string
const token = generateSecretB64(); // base64url string
```

### Pattern 2: Manage .env variables

```javascript
import { getEnvVar, setEnvVar } from "@copilot-ld/libsecret";

await setEnvVar(".env", "API_SECRET", secret);
const value = await getEnvVar(".env", "API_SECRET");
```

### Pattern 3: Create JWT

```javascript
import { createJwt } from "@copilot-ld/libsecret";

const jwt = createJwt({ userId: "123" }, secret, { expiresIn: "1h" });
```

## Integration

Used during setup scripts and initialization. Called by scripts/env-secrets.js.
