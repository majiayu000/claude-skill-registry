---
name: keychain-secure
description: macOS Keychain credential management with GF(3) balanced operations
version: 1.0.0
---


# Keychain Secure Skill: GF(3) Balanced Credential Management

**Status**: ✅ Production Ready
**Trit**: -1 (MINUS - validator/security)
**Color**: #2626D8 (Blue)
**Principle**: Store(+1) + Retrieve(0) + Validate(-1) = 0
**Frame**: Never env vars, always Keychain

---

## Overview

**Keychain Secure** provides secure credential storage on macOS with GF(3) conservation. Every credential lifecycle is balanced:

```
Create (+1) → Transport (0) → Consume/Verify (-1) = 0 ✓
```

## GF(3) Triads

```
keychain-secure (-1) ⊗ mdm-cobordism (0) ⊗ gay-mcp (+1) = 0 ✓  [Credential Chain]
keychain-secure (-1) ⊗ unworld (0) ⊗ oapply-colimit (+1) = 0 ✓  [Derivation]
keychain-secure (-1) ⊗ acsets (0) ⊗ koopman-generator (+1) = 0 ✓  [Pattern]
```

## Why Not Environment Variables?

| Storage | Security | Problem |
|---------|----------|---------|
| `export API_KEY=...` | ❌ None | Visible in `ps`, logs, shell history |
| `.env` file | ❌ Minimal | Readable, often committed to git |
| Keychain | ✅ Encrypted | Hardware-backed, ACL-protected |

**Rule**: Secrets belong in Keychain, never in environment.

## Commands

### Store Credential (+1 Generator)

```bash
# Interactive (prompts for password)
security add-generic-password \
    -s "service-name" \
    -a "$USER" \
    -w

# Non-interactive (⚠️ visible in process list briefly)
security add-generic-password \
    -s "service-name" \
    -a "$USER" \
    -w "secret-value" \
    -U  # Update if exists
```

### Retrieve Credential (0 Coordinator)

```bash
# Get password value
security find-generic-password \
    -s "service-name" \
    -a "$USER" \
    -w

# Use in command substitution
export API_KEY=$(security find-generic-password -s "openai" -a "$USER" -w)
```

### Delete Credential (-1 Validator)

```bash
security delete-generic-password \
    -s "service-name" \
    -a "$USER"
```

### Verify Credential (-1 Validator)

```bash
# Check if credential exists and is retrievable
security find-generic-password -s "service-name" -a "$USER" -w >/dev/null 2>&1 \
    && echo "valid" || echo "invalid"
```

## GF(3) Balanced Operations

### Pattern 1: Store-Retrieve-Validate

```bash
# +1: Store
security add-generic-password -s "test" -a "$USER" -w "secret123" -U

# 0: Retrieve  
RETRIEVED=$(security find-generic-password -s "test" -a "$USER" -w)

# -1: Validate
[ "$RETRIEVED" = "secret123" ] && echo "GF(3) = 0 ✓"
```

### Pattern 2: Create-Use-Rotate

```bash
# +1: Create new credential
security add-generic-password -s "api-key-v2" -a "$USER" -w "$NEW_KEY"

# 0: Use credential (transport)
curl -H "Authorization: Bearer $(security find-generic-password -s 'api-key-v2' -a '$USER' -w)" ...

# -1: Delete old credential
security delete-generic-password -s "api-key-v1" -a "$USER"
```

## Python API

```python
from mdm_mcp_server import Keychain, Trit, verify_gf3

# Store (+1)
ok, trit = Keychain.store("openai", "api-key", "sk-...")
assert trit == Trit.PLUS

# Retrieve (0)
secret, trit = Keychain.retrieve("openai", "api-key")
assert trit == Trit.ERGODIC

# Delete (-1)
ok, trit = Keychain.delete("openai", "api-key")
assert trit == Trit.MINUS

# GF(3) balanced operation
ok, trits = Keychain.store_then_verify("service", "account", "secret")
assert verify_gf3(trits)  # [+1, 0, -1] = 0 ✓
```

## Ruby API

```ruby
require 'keychain_secure'

# Store with GF(3) tracking
KeychainSecure.store(
  service: 'openai',
  account: ENV['USER'],
  secret: 'sk-...',
  trit: :plus  # +1
)

# Balanced lifecycle
KeychainSecure.balanced_lifecycle(
  service: 'api-key',
  account: ENV['USER']
) do |secret|
  # Use secret here (trit: 0)
  make_api_call(secret)
end
# Automatic validation on block exit (trit: -1)
```

## Access Control

### Restrict to Specific Apps

```bash
security add-generic-password \
    -s "my-service" \
    -a "$USER" \
    -w "secret" \
    -T "/usr/bin/security" \
    -T "/Applications/MyApp.app"
```

### Require User Confirmation

```bash
# Set ACL to require confirmation
security set-generic-password-partition-list \
    -s "my-service" \
    -a "$USER" \
    -S "apple:"
```

## Integration with MDM

```python
# MDM enrollment with Keychain-backed credentials
from mdm_mcp_server import W1_GENERATE_KEY, Keychain

# Store MDM push certificate
Keychain.store("mdm-push-cert", "apns", push_cert_pem)

# Retrieve for APNS connection
push_cert, _ = Keychain.retrieve("mdm-push-cert", "apns")
```

## Common Services

| Service | Account | Description |
|---------|---------|-------------|
| `openai` | `api-key` | OpenAI API key |
| `anthropic` | `api-key` | Claude API key |
| `github` | `pat` | Personal access token |
| `mdm-push-cert` | `apns` | MDM push certificate |
| `scep-challenge` | `enrollment` | SCEP challenge password |

## Security Best Practices

1. **Use Access Groups** for app-to-app sharing
2. **Set ACLs** to require user presence for sensitive items
3. **Rotate credentials** periodically (create new, delete old)
4. **Never log secrets** — even to debug logs
5. **Verify GF(3)** — ensures complete credential lifecycle

## Anti-Patterns

```bash
# ❌ BAD: Secret in command line (visible in ps)
curl -H "Authorization: Bearer sk-abc123" ...

# ✅ GOOD: Secret from Keychain
curl -H "Authorization: Bearer $(security find-generic-password -s 'openai' -a '$USER' -w)" ...

# ❌ BAD: Secret in environment
export OPENAI_API_KEY="sk-abc123"

# ✅ GOOD: Retrieve when needed
OPENAI_API_KEY=$(security find-generic-password -s 'openai' -a "$USER" -w)
```

---

**Skill Name**: keychain-secure
**Type**: Credential Management / Security
**Trit**: -1 (MINUS)
**Color**: #2626D8 (Blue)
**GF(3)**: Store(+1) + Retrieve(0) + Validate(-1) = 0
**Env Vars**: Never for secrets



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ◁
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.