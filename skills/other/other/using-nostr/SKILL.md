---
name: using-nostr
description: Post notes, send encrypted messages, and interact with relays using the Nostr protocol.
---

# NOSTR Posting Skill
# Using nostr-sdk library
# Source: https://github.com/besoeasy/nostr-sdk

## Overview
Post messages, send encrypted DMs, and interact with the Nostr decentralized social protocol using minimal direct exports from the `nostr-sdk` module.

**Installation:**
```bash
npm install nostr-sdk
```

**Key Concepts:**
- **nsec**: Private key in bech32 format (starts with `nsec1`)
- **npub**: Public key in bech32 format (starts with `npub1`)
- **Relays**: WebSocket servers that propagate Nostr events
- **Events**: Signed JSON objects representing posts, DMs, etc.
- **POW**: Proof of Work (mining) to reduce spam

**Default Relays:**
- wss://relay.damus.io
- wss://nos.lol
- wss://relay.snort.social
- wss://nostr-pub.wellorder.net
- wss://nostr.oxtr.dev
- And 9+ more for maximum reach

---

## Skills

### post_public_note

Post a public text note to Nostr.

**Usage:**
```javascript
const { posttoNostr } = require("nostr-sdk");

const result = await posttoNostr("Hello Nostr! #introduction", {
  nsec: "nsec1...your-private-key",
  tags: [],
  relays: null,
  powDifficulty: 4
});
console.log(result);
```

**Parameters:**
- `message`: Text content to post
- `tags`: Optional array of tags (e.g., `[['t', 'topic']]`)
- `relays`: Optional custom relay list (uses defaults if null)
- `powDifficulty`: Proof of work difficulty (default: 4, 0 to disable)

**Auto-extracted Tags:**
- Hashtags: `#nostr` → `["t", "nostr"]`
- Mentions: `@npub1...` → `["p", <pubkey>]`
- Links: URLs automatically preserved
- Notes: `note1...` references → `["e", <event-id>]`

**Response:**
```javascript
{
  success: true,
  eventId: "abc123...",
  published: 12,      // Successfully published to 12 relays
  failed: 2,          // Failed on 2 relays
  totalRelays: 14,
  powDifficulty: 4,
  errors: []
}
```

**When to use:**
- User wants to post a public message
- Sharing content with hashtags
- Broadcasting announcements

---

### reply_to_post

Reply to an existing Nostr post.

**Usage:**
```javascript
const { replyToPost } = require("nostr-sdk");

const result = await replyToPost(
  "note1...event-id",           // Event ID (note or hex format)
  "Great post! @npub1...author", // Reply message
  "npub1...author-pubkey",      // Author's public key
  [],                           // Additional tags
  null,                         // Use default relays
  4                             // POW difficulty
);
```

**When to use:**
- Responding to a specific post
- Thread conversations
- Engaging with content

---

### send_encrypted_dm (NIP-4)

Send encrypted direct message using legacy NIP-4 standard.

**Usage:**
```javascript
const { sendmessage } = require("nostr-sdk");

const result = await sendmessage(
  "npub1...recipient",    // Recipient's public key
  "Secret message here",  // Message content
  { nsec: "nsec1...your-private-key" }
);
```

**When to use:**
- Compatibility with older Nostr clients
- Basic encrypted messaging
- Wide client support

**Limitations:**
- Sender/recipient metadata visible
- Older encryption (NIP-04)

---

### send_encrypted_dm_modern (NIP-17)

Send gift-wrapped encrypted message using NIP-17 (recommended).

**Usage:**
```javascript
const { sendMessageNIP17 } = require("nostr-sdk");

const result = await sendMessageNIP17(
  "npub1...recipient",    // Recipient's public key
  "Private message!",     // Message content
  { nsec: "nsec1...your-private-key" }
);
```

**Benefits:**
- Sealed sender (hides who sent the message)
- Better metadata protection
- Modern NIP-44 encryption
- Ephemeral keys for each message

**When to use:**
- Maximum privacy needed
- Modern applications
- Hiding sender identity

---

### receive_messages (NIP-4)

Listen for incoming direct messages.

**Usage:**
```javascript
const { getmessage } = require("nostr-sdk");

const unsubscribe = getmessage((message) => {
  console.log("From:", message.senderNpub);
  console.log("Message:", message.content);
  console.log("Time:", new Date(message.timestamp * 1000));
}, {
  nsec: "nsec1...your-private-key",
  since: Math.floor(Date.now() / 1000) - 3600  // Last hour
});

// Stop listening:
// unsubscribe();
```

**Message Object:**
```javascript
{
  id: "event-id",
  sender: "hex-pubkey",
  senderNpub: "npub1...",
  content: "decrypted message",
  timestamp: 1234567890,
  event: { /* full event */ }
}
```

**When to use:**
- Building a chat bot
- Receiving DMs
- Monitoring for messages

---

### receive_messages_modern (NIP-17)

Listen for incoming NIP-17 gift-wrapped messages.

**Usage:**
```javascript
const { getMessageNIP17 } = require("nostr-sdk");

const unsubscribe = getMessageNIP17((message) => {
  console.log("From:", message.senderNpub);
  console.log("Content:", message.content);
  console.log("Wrapped ID:", message.wrappedEventId);
}, {
  nsec: "nsec1...your-private-key",
  since: Math.floor(Date.now() / 1000) - 300  // Last 5 minutes
});

// Stop listening:
// unsubscribe();
```

**When to use:**
- Receiving modern private messages
- Maximum privacy for incoming DMs
- Supporting NIP-17 protocol

---

### get_global_feed

Fetch recent posts from the global Nostr feed.

**Usage:**
```javascript
const { getGlobalFeed } = require("nostr-sdk");

const events = await getGlobalFeed({
  limit: 50,                                    // Max 50 posts
  since: Math.floor(Date.now() / 1000) - 3600, // Last hour
  until: null,                                  // Up to now
  kinds: [1],                                   // Text notes only
  authors: null,                                // All authors
  relays: null                                  // Use defaults
});

events.forEach(event => {
  console.log("Author:", event.authorNpub);
  console.log("Content:", event.content);
  console.log("Note ID:", event.noteId);
  console.log("Posted:", event.createdAtDate);
});
```

**When to use:**
- Building a feed reader
- Monitoring public posts
- Trending content analysis

---

### generate_keys

Generate new Nostr key pair.

**Usage:**
```javascript
const { generateNewKey } = require("nostr-sdk");

const keys = generateNewKey();
console.log(keys);
// {
//   privateKey: "hex-private-key",
//   publicKey: "hex-public-key",
//   nsec: "nsec1...",
//   npub: "npub1..."
// }
```

**Quick Generate:**
```javascript
const { generateRandomNsec } = require("nostr-sdk");
const nsec = generateRandomNsec();
console.log(nsec); // nsec1...
```

---

### convert_keys

Convert between key formats.

**Usage:**
```javascript
const { nsecToPublic } = require("nostr-sdk");

const publicInfo = nsecToPublic("nsec1...your-key");
console.log(publicInfo);
// {
//   publicKey: "hex-public-key",
//   npub: "npub1..."
// }
```

---

## Quick Start Examples

### Example 1: Post a Message
```javascript
const { posttoNostr } = require("nostr-sdk");

async function postHello() {
  const result = await posttoNostr("Hello from my bot! #nostr #automation", {
    nsec: "nsec1...your-private-key"
  });
  
  console.log("Posted:", result.eventId);
}

postHello();
```

### Example 2: Send Private DM
```javascript
const { sendMessageNIP17 } = require("nostr-sdk");

async function sendPrivateMessage() {
  const result = await sendMessageNIP17(
    "npub1...recipient",
    "This is a secret message!",
    { nsec: "nsec1...your-private-key" }
  );
  
  console.log("Sent:", result.success ? "Yes" : "No");
}

sendPrivateMessage();
```

### Example 3: Listen for DMs
```javascript
const { getMessageNIP17 } = require("nostr-sdk");

console.log("Listening for messages...");

const unsubscribe = getMessageNIP17((msg) => {
  console.log(`Message from ${msg.senderNpub}: ${msg.content}`);
}, {
  nsec: "nsec1...your-private-key"
});

// Keep running or call unsubscribe() to stop
```

### Example 4: Quick Post (No Setup)
```javascript
const { posttoNostr } = require("nostr-sdk");

// Auto-generates keys if not provided
const result = await posttoNostr("Quick post!", {
  nsec: "nsec1...your-key"  // Optional - generates new if omitted
});
```

---

## Decision Tree

```
User wants to post to Nostr?
├─ Is it a public post?
│  ├─ Is it a reply to another post?
│  │  ├─ YES → Use replyToPost()
│  │  └─ NO → Use posttoNostr()
│  └─ Need spam protection?
│     ├─ YES → Set powDifficulty to 4+
│     └─ NO → Set powDifficulty to 0
│
├─ Is it a private message?
│  ├─ Maximum privacy needed?
│  │  ├─ YES → Use sendMessageNIP17()
│  │  └─ NO → Use sendmessage()
│  │
│  └─ Need to receive messages?
│     ├─ Use NIP-17 → getMessageNIP17()
│     └─ Use NIP-4 (legacy) → getmessage()
│
└─ Need to read posts?
   └─ Use getGlobalFeed()
```

---

## Key Management

**Security Best Practices:**
- Never commit nsec keys to git
- Store keys in environment variables or secure vaults
- Generate new keys for testing
- Use different keys for different purposes

**Environment Variables:**
```bash
export NOSTR_NSEC="nsec1...your-private-key"
```

```javascript
const { posttoNostr } = require("nostr-sdk");

await posttoNostr("Health check log", {
  nsec: process.env.NOSTR_NSEC
});
```

---

## Error Handling

**Common Errors:**
- `Private key not set` → Provide nsec or generate keys
- `Invalid nsec format` → Check bech32 encoding
- `Failed to post to Nostr` → Check relay connections
- `Failed to decrypt message` → Wrong private key for recipient

**Best Practice:**
```javascript
const { posttoNostr } = require("nostr-sdk");

try {
  const result = await posttoNostr("Hello", {
    nsec: process.env.NOSTR_NSEC
  });
  if (!result.success) {
    console.error("Failed to publish:", result.errors);
  }
} catch (error) {
  console.error("Error:", error.message);
}
```

---

## Cleanup

Direct-export functions do not require a class instance, so there is no client cleanup step.

---

## Resources

- **Library**: https://github.com/besoeasy/nostr-sdk
- **Nostr Protocol**: https://nostr.com
- **NIPs (Nostr Implementation Possibilities)**: https://github.com/nostr-protocol/nips
- **Key Tools**:
  - https://nostrcheck.me (key converter)
  - https://snort.social (web client)
  - https://damus.io (iOS client)
