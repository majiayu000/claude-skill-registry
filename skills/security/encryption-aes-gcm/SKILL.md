---
name: encryption-aes-gcm
description: AES-256-GCM encryption for sensitive credentials (BYOD/BYOK). Node crypto, IV + authTag storage, multi-field colon-separated IVs. Triggers on "encryption", "decrypt", "AES-256-GCM", "BYOD", "BYOK", "credentials".
---

# AES-256-GCM Encryption

Project uses AES-256-GCM for encrypting user credentials (BYOD Convex keys, BYOK API keys). Node crypto module, requires `"use node"` directive.

## Core Pattern

```typescript
// From convex/lib/encryption.ts
"use node";

import { createCipheriv, createDecipheriv, randomBytes } from "node:crypto";

const ALGORITHM = "aes-256-gcm";
```

All encryption functions in files with `"use node"` at top (Convex Node runtime required).

## Environment Key

```typescript
// From convex/lib/encryption.ts
function getEncryptionKey(): Buffer {
  const key = process.env.BYOD_ENCRYPTION_KEY;
  if (!key) {
    throw new Error("BYOD_ENCRYPTION_KEY environment variable not set");
  }
  // 32 bytes (64 hex chars) - use directly
  if (key.length === 64) {
    return Buffer.from(key, "hex");
  }
  // Otherwise hash to 32 bytes
  const crypto = require("node:crypto");
  return crypto.createHash("sha256").update(key).digest();
}
```

**Key requirement**: `BYOD_ENCRYPTION_KEY` in Convex environment. Accepts 64 hex chars or any string (hashed).

## Encryption Function

```typescript
// From convex/lib/encryption.ts
export async function encryptCredential(
  plaintext: string,
): Promise<{ encrypted: string; iv: string; authTag: string }> {
  const key = getEncryptionKey();
  const iv = randomBytes(16);

  const cipher = createCipheriv(ALGORITHM, key, iv);
  let encrypted = cipher.update(plaintext, "utf8", "hex");
  encrypted += cipher.final("hex");

  const authTag = cipher.getAuthTag();

  return {
    encrypted,
    iv: iv.toString("hex"),
    authTag: authTag.toString("hex"),
  };
}
```

**Returns three parts**: encrypted data, IV (16 bytes), authTag (for GCM authentication).

**Always generate new IV** per encryption (never reuse).

## Decryption Function

```typescript
// From convex/lib/encryption.ts
export async function decryptCredential(
  encrypted: string,
  iv: string,
  authTag: string,
): Promise<string> {
  const key = getEncryptionKey();

  const decipher = createDecipheriv(ALGORITHM, key, Buffer.from(iv, "hex"));
  decipher.setAuthTag(Buffer.from(authTag, "hex"));

  let decrypted = decipher.update(encrypted, "hex", "utf8");
  decrypted += decipher.final("utf8");

  return decrypted;
}
```

**Must set authTag before decrypting** - validates data integrity. Throws if tampered.

## Multi-Field Storage (BYOK Pattern)

Store multiple encrypted keys with shared IV/authTag arrays:

```typescript
// From convex/byok/saveCredentials.ts
const FIELD_MAP = {
  vercelGateway: "encryptedVercelKey",
  openRouter: "encryptedOpenRouterKey",
  groq: "encryptedGroqKey",
  deepgram: "encryptedDeepgramKey",
};

const KEY_INDEX = {
  vercelGateway: 0,
  openRouter: 1,
  groq: 2,
  deepgram: 3,
};

// Parse colon-separated string: "iv1:iv2:iv3:iv4"
function parseParts(str: string | undefined): string[] {
  if (!str) return ["", "", "", ""];
  const parts = str.split(":");
  while (parts.length < 4) parts.push("");
  return parts;
}
```

**Encryption storage**:

```typescript
// From convex/byok/saveCredentials.ts (saveApiKey action)
const encrypted = await encryptCredential(args.apiKey);

// Get existing IVs/authTags
const existing = await ctx.runQuery(internal.byok.credentials.getConfigInternal, {
  userId: user._id,
});

const ivParts = parseParts(existing?.encryptionIVs);
const authTagParts = parseParts(existing?.authTags);

// Update specific index
const idx = KEY_INDEX[args.keyType];
ivParts[idx] = encrypted.iv;
authTagParts[idx] = encrypted.authTag;

// Store as colon-separated
await ctx.runMutation(internal.byok.credentials.upsertConfig, {
  userId: user._id,
  [FIELD_MAP[args.keyType]]: encrypted.encrypted,
  encryptionIVs: ivParts.join(":"), // "v_iv:or_iv:groq_iv:dg_iv"
  authTags: authTagParts.join(":"),
});
```

**Decryption retrieval**:

```typescript
// From convex/byok/saveCredentials.ts (revalidateKey action)
const existing = await ctx.runQuery(internal.byok.credentials.getConfigInternal, {
  userId: user._id,
});

const encryptedKey = existing[FIELD_MAP[args.keyType]];
const ivParts = parseParts(existing.encryptionIVs);
const authTagParts = parseParts(existing.authTags);

const idx = KEY_INDEX[args.keyType];
const iv = ivParts[idx];
const authTag = authTagParts[idx];

if (!iv || !authTag) {
  throw new ConvexError("Unable to decrypt key. Please re-add it.");
}

const apiKey = await decryptCredential(encryptedKey, iv, authTag);
```

## Database Schema

```typescript
// userApiKeys table (BYOK)
{
  userId: v.id("users"),
  encryptedVercelKey: v.optional(v.string()),
  encryptedOpenRouterKey: v.optional(v.string()),
  encryptedGroqKey: v.optional(v.string()),
  encryptedDeepgramKey: v.optional(v.string()),
  encryptionIVs: v.string(),  // "iv1:iv2:iv3:iv4"
  authTags: v.string(),        // "tag1:tag2:tag3:tag4"
  lastValidated: v.optional(v.object({...})),
}

// userDatabaseConfig table (BYOD)
{
  userId: v.id("users"),
  encryptedDeploymentUrl: v.string(),
  encryptedDeployKey: v.string(),
  encryptionIV: v.string(),    // Single IV: "urlIV:keyIV"
  authTags: v.string(),         // Single authTags: "urlTag:keyTag"
}
```

**BYOK**: 4 keys → 4 indexes → colon-separated IVs/authTags
**BYOD**: 2 fields → colon-separated `urlIV:keyIV` and `urlTag:keyTag`

## Security Rules

1. **Never log plaintext** - only log key types, not values:
   ```typescript
   logger.warn("Failed to validate API key", {
     tag: "BYOK",
     keyType,  // ✅ Log type
     error: String(error),
   });
   // ❌ DON'T: apiKey: apiKey
   ```

2. **Never return encrypted credentials to client**:
   ```typescript
   // From convex/byod/credentials.ts (getConfig query)
   // Never return encrypted credentials to client
   return {
     _id: config._id,
     connectionStatus: config.connectionStatus,
     lastConnectionTest: config.lastConnectionTest,
     // ❌ DON'T include: encryptedDeploymentUrl, encryptedDeployKey
   };
   ```

3. **Use internal queries for encrypted data**:
   ```typescript
   // From convex/byod/credentials.ts
   export const getConfigInternal = internalQuery({
     args: { userId: v.id("users") },
     handler: async (ctx, args): Promise<Doc<"userDatabaseConfig"> | null> => {
       return await ctx.db
         .query("userDatabaseConfig")
         .withIndex("by_user", (q) => q.eq("userId", args.userId))
         .first();
     },
   });
   ```

4. **Always verify authTag** - `decipher.final()` throws if tampered.

5. **Fail secure on validation errors**:
   ```typescript
   // From convex/byok/saveCredentials.ts
   try {
     encrypted = await encryptCredential(args.apiKey);
   } catch (error) {
     logger.error("BYOK encryption failed", { tag: "BYOK", error: String(error) });
     throw new ConvexError(
       "BYOK is not available right now. Please contact support.",
     );
   }
   ```

## Use Cases

**BYOK (Bring Your Own Key)**: User-provided API keys for Vercel Gateway, OpenRouter, Groq, Deepgram
- File: `convex/byok/saveCredentials.ts`
- Actions: `saveApiKey`, `removeApiKey`, `revalidateKey`
- Table: `userApiKeys`

**BYOD (Bring Your Own Database)**: User Convex deployment credentials
- File: `convex/byod/credentials.ts`
- Table: `userDatabaseConfig`
- Fields: `encryptedDeploymentUrl`, `encryptedDeployKey`

## Error Handling

```typescript
// Encryption failure (missing env key)
throw new ConvexError("BYOK is not available right now. Please contact support.");

// Decryption failure (missing IV/authTag)
throw new ConvexError("Unable to decrypt key. Please re-add it.");

// Validation failure (invalid API key)
throw new ConvexError("Invalid API key. Please check the key is correct.");
```

## Key Files

- `convex/lib/encryption.ts` - Core encrypt/decrypt functions
- `convex/byok/saveCredentials.ts` - Multi-key BYOK pattern
- `convex/byok/credentials.ts` - BYOK queries/mutations
- `convex/byod/credentials.ts` - BYOD config management
- `convex/byok/constants.ts` - Field mappings, key indexes

## Avoid

- ❌ Reusing IVs (always generate new with `randomBytes(16)`)
- ❌ Storing plaintext anywhere (logs, DB, client responses)
- ❌ Using algorithms other than `aes-256-gcm` (project standard)
- ❌ Forgetting `"use node"` directive (encryption requires Node runtime)
- ❌ Missing authTag validation (set before decrypt, verify on final)
- ❌ Hardcoding encryption keys in code (use env vars)
