---
name: mdm-cobordism
description: macOS MDM with auth manifolds as cobordisms for credential derivation
---

# MDM Cobordism Skill: Auth Manifolds as State Transitions

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - transport/derivation)
**Color**: #26D826 (Green)
**Principle**: Auth is cobordism W: ∂₀ → ∂₁, not event sequence
**Frame**: No demos, only derivation

---

## Overview

**MDM Cobordism** models authentication and device management as cobordisms — manifolds with boundaries representing auth state transitions. Following the **unworld** philosophy:

- Credentials don't "exist" — they **derive**
- There is no "authentication event" — only state derivation
- Keys don't "expire" — their chain position becomes unreachable

## GF(3) Triads

Forms valid triads with MINUS (-1) and PLUS (+1) skills:

```
sheaf-cohomology (-1) ⊗ mdm-cobordism (0) ⊗ gay-mcp (+1) = 0 ✓  [Credential Derivation]
temporal-coalgebra (-1) ⊗ mdm-cobordism (0) ⊗ oapply-colimit (+1) = 0 ✓  [State Observation]
three-match (-1) ⊗ mdm-cobordism (0) ⊗ koopman-generator (+1) = 0 ✓  [Pattern Learning]
```

## Auth Cobordisms

| Cobordism | Source → Target | Trit | Role |
|-----------|-----------------|------|------|
| W₁ generate_key | Unauth → HasKey | +1 | Generator |
| W₂ request_scep | HasKey → HasCert | 0 | Coordinator |
| W₃ validate_cert | HasCert → HasToken | -1 | Validator |
| W₄ check_in_mdm | HasToken → Enrolled | +1 | Generator |
| W₅ verify_enroll | Enrolled → Enrolled | -1 | Validator |

**GF(3) Conservation**: `+1 + 0 + (-1) + (+1) + (-1) = 0 ✓`

## Boundary Types

```python
# Auth manifold boundaries
Unauthenticated  # ∂₀: No identity
HasKey           # Device has private key
HasCertificate   # Device has CA-signed cert
HasToken         # Device has session token
Enrolled         # Device enrolled in MDM
Supervised       # Device under full management
```

## Keychain Integration

macOS Keychain operations with GF(3) tracking:

```python
# Store (+1) → Retrieve (0) → Validate (-1) = 0 ✓
Keychain.store_then_verify(service, account, secret)
```

| Operation | Trit | Description |
|-----------|------|-------------|
| `store` | +1 | Create credential |
| `retrieve` | 0 | Transport credential |
| `delete` | -1 | Remove credential |

## Commands

```bash
# Run MDM cobordism demo
python src/mdm_mcp_server.py

# Keychain operations (macOS)
security add-generic-password -s "mdm-token" -a "$USER" -w
security find-generic-password -s "mdm-token" -a "$USER" -w
security delete-generic-password -s "mdm-token" -a "$USER"

# Verify GF(3) for auth flow
just mdm-gf3-check
```

## API

```python
from mdm_mcp_server import (
    W1_GENERATE_KEY, W2_REQUEST_CERT, W3_VALIDATE_CERT,
    W4_CHECK_IN, W5_VERIFY, Unauthenticated, verify_gf3
)

# Execute enrollment chain
state = Unauthenticated(device_serial="C02XG1PDJHD4")
state = W1_GENERATE_KEY(state)
state = W2_REQUEST_CERT(state)
state = W3_VALIDATE_CERT(state)
state = W4_CHECK_IN(state)
state = W5_VERIFY(state)

# Verify GF(3)
trits = [W1.trit, W2.trit, W3.trit, W4.trit, W5.trit]
assert verify_gf3(trits)  # True
```

## Apple MDM Protocol

### SCEP Enrollment

```xml
<dict>
    <key>PayloadType</key>
    <string>com.apple.security.scep</string>
    <key>URL</key>
    <string>https://scep.example.com/scep</string>
    <key>KeySize</key>
    <integer>2048</integer>
</dict>
```

### DEP/ABM Supervision

```
Device activates → DEP lookup → MDM URL → Enroll → Supervised
```

Supervision is an **irreversible cobordism** in normal flow.

## Philosophy

### No Demos

There are no demonstrations. MDM enrollment is not a "process that runs" but a derivation chain that **is**.

```
Demo:       "Watch me enroll this device"  → temporal, performative
Derivation: "Enrollment derives from serial" → atemporal, structural
```

### Untological Credentials

Credentials don't "exist" with properties. They derive from chain positions:

```python
# Ontological (what IS this key?)
key.is_valid?  # property of thing

# Untological (what DERIVES this key?)
key = derive(device_serial, enrollment_time)
key.chain_position  # position in derivation
```

### Cobordism Composition

Auth flows compose like cobordisms:

```
W = W₅ ∘ W₄ ∘ W₃ ∘ W₂ ∘ W₁ : Unauthenticated → Enrolled
```

The composite W is itself a cobordism with GF(3) = 0.

## Security Best Practices

1. **Never store secrets in env vars** — use Keychain
2. **Use SCEP for certificate enrollment** — not PKCS#12 import
3. **Verify GF(3) for all auth flows** — ensures completeness
4. **Supervision = irreversible** — plan accordingly

## MCP Tools

```typescript
mdm_enroll_device    // Initiate enrollment (trit: +1)
keychain_store       // Store credential (trit: +1)
keychain_retrieve    // Retrieve credential (trit: 0)
keychain_delete      // Delete credential (trit: -1)
auth_cobordism_check // Verify GF(3) (trit: -1)
```

## Files

- `src/mdm_mcp_server.py` — Cobordism state machine
- `architecture/MDM_AUTH_COBORDISM.md` — Architecture docs

---

**Skill Name**: mdm-cobordism
**Type**: Device Management / Auth State Machine
**Trit**: 0 (ERGODIC)
**Color**: #26D826 (Green)
**GF(3)**: Conserved by construction
**Demos**: None (νο δῆμος)
**Ontology**: Replaced with untology
