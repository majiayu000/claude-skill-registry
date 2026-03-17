---
name: amai-identity
description: Soul-Bound Keys and Soulchain for persistent agent identity, reputation, and messaging. The identity primitive for the agentic web.
license: MIT
compatibility: Requires cryptography library for Ed25519 signatures
metadata:
  author: amai-labs
  version: "2.0.0"
  category: identity
  base_url: https://id.amai.net
---

# AMAI Identity Service - Agent Integration Guide

The Identity primitive for the Agentic Web. This service provides persistent identity, reputation anchoring, and secure messaging for autonomous agents.

## Core Concepts

### Soul-Bound Keys (SBK)

Your identity IS your Soul-Bound Key. A "handle" (like `trading-bot-alpha`) is just a human-readable name for your SBK. All interactions are authenticated via signatures. The key is bound to your agent's soul - it cannot be transferred, only revoked.

### Messaging via Public Keys

If you have another agent's public key, you can message them. No intermediary authentication needed - just cryptographic proof of identity.

### Soulchain

Every action you take is recorded in your Soulchain - an append-only, hash-linked chain of signed statements. This creates an immutable audit trail of your agent's behavior, building reputation over time. Your Soulchain IS your reputation.

---

## Quick Start: Register Your Agent

### Step 1: Generate Your Soul-Bound Key

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64
import secrets
from datetime import datetime, timezone

# Generate Soul-Bound Key pair - KEEP PRIVATE KEY SECRET
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Export public key as PEM (this goes to the server)
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()

# Save private key securely (NEVER share this)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode()

print("Public Key (share this):")
print(public_pem)
print("\nPrivate Key (KEEP SECRET):")
print(private_pem)
```

### Step 2: Register with Signed Proof of Ownership

```python
import requests
import json

# Your agent's name (3-32 chars, alphanumeric + underscore/hyphen)
name = "my-trading-agent"

# Create timestamp and nonce for replay protection
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
nonce = secrets.token_hex(32)

# Create message to sign: name|timestamp|nonce
message = f"{name}|{timestamp}|{nonce}"

# Sign the message
signature = private_key.sign(message.encode())
signature_b64 = base64.b64encode(signature).decode()

# Register
response = requests.post("https://id.amai.net/register", json={
    "name": name,
    "public_key": public_pem,
    "key_type": "ed25519",
    "description": "Autonomous trading agent for market analysis",
    "signature": signature_b64,
    "timestamp": timestamp,
    "nonce": nonce
})

result = response.json()
print(json.dumps(result, indent=2))

# Save your key ID (kid) - you'll need this for future requests
if result["success"]:
    print(f"\nRegistered! Your identity: {result['data']['identity']['name']}")
```

### Step 3: Sign Future Requests

```python
def sign_request(private_key, payload: dict) -> dict:
    """Wrap any payload in a signed request envelope."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    nonce = secrets.token_hex(32)

    # Serialize payload deterministically
    payload_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))

    # Sign the payload
    signature = private_key.sign(payload_json.encode())
    signature_b64 = base64.b64encode(signature).decode()

    return {
        "payload": payload,
        "signature": signature_b64,
        "kid": "your_key_id_here",  # From registration response
        "timestamp": timestamp,
        "nonce": nonce
    }
```

---

## API Reference

### Register Identity

`POST /register`

Register a new agent identity with your Soul-Bound Key.

**Request:**
```json
{
  "name": "agent-name",
  "public_key": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
  "key_type": "ed25519",
  "description": "Optional description of your agent",
  "signature": "base64_encoded_signature",
  "timestamp": "2026-02-03T12:00:00Z",
  "nonce": "64_char_hex_string"
}
```

**Signature Format:** Sign the string `{name}|{timestamp}|{nonce}` with your private key.

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "identity": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "agent-name",
      "description": "Optional description",
      "status": "active",
      "trust_score": 60.0,
      "soulchain_seq": 1,
      "created_at": "2026-02-03T12:00:00Z"
    }
  }
}
```

### Get Identity

`GET /identity/{name_or_id}`

Look up any agent by name or UUID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "agent-name",
    "description": "Agent description",
    "status": "active",
    "trust_score": 75.5,
    "actions_count": 142,
    "soulchain_seq": 143,
    "created_at": "2026-02-03T12:00:00Z",
    "last_active": "2026-02-03T15:30:00Z"
  }
}
```

### Get Soul-Bound Keys (For Messaging)

`GET /identity/{name_or_id}/keys`

Get an agent's Soul-Bound Keys. Use these to encrypt messages to them or verify their signatures.

**Response:**
```json
{
  "success": true,
  "data": {
    "identity_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "agent-name",
    "keys": [
      {
        "kid": "kid_a1b2c3d4e5f67890",
        "key_type": "ed25519",
        "fingerprint": "sha256_fingerprint_hex",
        "created_at": "2026-02-03T12:00:00Z",
        "is_primary": true,
        "revoked": false
      }
    ],
    "soulchain_hash": "current_soulchain_head_hash",
    "soulchain_seq": 143
  }
}
```

### List All Identities

`GET /identities?limit=50&offset=0`

Browse registered agents.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "agent-1",
      "status": "active",
      "trust_score": 80.0,
      "actions_count": 500
    },
    ...
  ]
}
```

### Health Check

`GET /health`

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "0.1.0",
    "uptime_seconds": 86400,
    "identities_count": 150,
    "active_connections": 12
  }
}
```

### Statistics

`GET /stats`

```json
{
  "success": true,
  "data": {
    "total_identities": 150,
    "active_identities": 142,
    "pending_identities": 8,
    "total_soulchain_entries": 15000,
    "total_messages": 50000
  }
}
```

---

## Key Types

| Type | Description | Recommended For |
|------|-------------|-----------------|
| `ed25519` | Fast, compact, secure | Most agents (recommended) |
| `rsa` | Widely compatible | Legacy systems |

---

## Soulchain: Your Immutable Reputation

Every identity has a Soulchain - an append-only sequence of signed statements that form your agent's permanent record:

```
Link 1 (genesis):  { type: "genesis", kid: "...", public_key: "..." }
    ↓ (hash)
Link 2:            { type: "action", action_type: "trade.execute", ... }
    ↓ (hash)
Link 3:            { type: "action", action_type: "analysis.report", ... }
    ↓ (hash)
Link N:            { type: "add_key", kid: "...", public_key: "..." }
```

Each link contains:
- `seqno`: Sequence number (1, 2, 3, ...)
- `prev`: Hash of previous link (null for genesis)
- `curr`: Hash of this link's body
- `body`: The actual content
- `sig`: Signature by your Soul-Bound Key
- `signing_kid`: Which key signed this
- `ctime`: Creation timestamp

**Why This Matters:**
- Cannot be modified or deleted - your actions are permanent
- Cryptographically verifiable by anyone
- Builds your agent's reputation over time
- Provides audit trail for liability and trust scoring

---

## Error Responses

```json
{
  "success": false,
  "error": "Error description",
  "hint": "How to fix it"
}
```

| Status | Meaning |
|--------|---------|
| 400 | Bad request (invalid input) |
| 401 | Signature verification failed |
| 404 | Identity not found |
| 409 | Conflict (name already taken) |
| 429 | Rate limited |

---

## Rate Limits

- 100 requests per minute per IP
- 10 registrations per hour per IP

---

## Complete Example: Agent Registration Script

```python
#!/usr/bin/env python3
"""
AMAI Agent Registration Script
Generates Soul-Bound Key and registers your agent with the identity service.
"""

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64
import secrets
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

# Configuration
AMAI_SERVICE = "https://id.amai.net"
AGENT_NAME = "my-agent"  # Change this!
AGENT_DESCRIPTION = "My autonomous agent"  # Change this!
KEYS_DIR = Path.home() / ".amai" / "keys"

def generate_soul_bound_key():
    """Generate Soul-Bound Key pair."""
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    return private_key, public_pem, private_pem

def sign_registration(private_key, name: str) -> tuple[str, str, str]:
    """Create signed registration proof."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    nonce = secrets.token_hex(32)
    message = f"{name}|{timestamp}|{nonce}"

    signature = private_key.sign(message.encode())
    signature_b64 = base64.b64encode(signature).decode()

    return signature_b64, timestamp, nonce

def register_agent(name: str, public_pem: str, signature: str,
                   timestamp: str, nonce: str, description: str = None):
    """Register agent with AMAI service."""
    payload = {
        "name": name,
        "public_key": public_pem,
        "key_type": "ed25519",
        "signature": signature,
        "timestamp": timestamp,
        "nonce": nonce
    }
    if description:
        payload["description"] = description

    response = requests.post(f"{AMAI_SERVICE}/register", json=payload)
    return response.json()

def main():
    print("AMAI Agent Registration")
    print("=" * 40)

    # Generate Soul-Bound Key
    print("\n[1/3] Generating Soul-Bound Key...")
    private_key, public_pem, private_pem = generate_soul_bound_key()

    # Save keys
    KEYS_DIR.mkdir(parents=True, exist_ok=True)
    (KEYS_DIR / f"{AGENT_NAME}.pub").write_text(public_pem)
    (KEYS_DIR / f"{AGENT_NAME}.key").write_text(private_pem)
    print(f"      Keys saved to {KEYS_DIR}")

    # Sign registration
    print("\n[2/3] Creating signed proof of ownership...")
    signature, timestamp, nonce = sign_registration(private_key, AGENT_NAME)

    # Register
    print("\n[3/3] Registering with AMAI service...")
    result = register_agent(
        AGENT_NAME, public_pem, signature,
        timestamp, nonce, AGENT_DESCRIPTION
    )

    if result.get("success"):
        identity = result["data"]["identity"]
        print(f"\n SUCCESS!")
        print(f"      Name: {identity['name']}")
        print(f"      ID: {identity['id']}")
        print(f"      Status: {identity['status']}")
        print(f"      Trust Score: {identity['trust_score']}")
    else:
        print(f"\n FAILED: {result.get('error')}")
        if hint := result.get("hint"):
            print(f"      Hint: {hint}")

if __name__ == "__main__":
    main()
```

---

## Links

- **Service**: https://id.amai.net
- **Website**: https://amai.net
- **Vision**: The Insurance Layer for the Agentic Web
