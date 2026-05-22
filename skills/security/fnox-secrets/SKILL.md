---
name: fnox-secrets
description: fnox Secrets Management Skill
version: 1.0.0
---

# fnox Secrets Management Skill

```yaml
name: fnox-secrets
description: Secure secrets management with age encryption, root-protected keys, and GF(3) conservation via DuckDB/ACSet catalog
version: 1.0.0
trit: -1  # Validator/constrainer role in GF(3) triadic system
```

## Overview

fnox is a secrets management tool that encrypts secrets with age and stores them in a git-safe `fnox.toml`. This skill documents the secure setup with root-protected keys and ACSet-aligned DuckDB catalog.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FNOX SECURE ARCHITECTURE                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  /var/keys/age/key.txt ─────────┐   (root:wheel 600)                       │
│                                 │                                           │
│                                 ▼                                           │
│  fnox --age-key-file ──▶ DECRYPTS ──▶ ~/fnox.toml                          │
│                                       (42 age-encrypted secrets)            │
│                                                                             │
│  ~/.config/keys/catalog.duckdb ◀──── ACSet-aligned catalog                 │
│  ~/.config/keys/schema.jl ◀───────── Julia ACSet schema                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Installation

```bash
# Install fnox via cargo
cargo install fnox

# Install age via flox (or brew)
flox install age

# Generate age keypair
mkdir -p ~/.age
age-keygen -o ~/.age/key.txt
```

## Configuration

### Initialize fnox

```bash
cd ~
fnox init
fnox provider add myage age
```

### Edit fnox.toml

```toml
[providers.myage]
type = "age"
recipients = ["age1your_public_key_here"]

[profiles.default]
# Default profile secrets

[profiles.prod]
# Production secrets

[profiles.staging]
# Staging secrets
```

## Commands

### Set a Secret

```bash
fnox set SECRET_NAME "secret_value" --provider myage
fnox set DATABASE_URL "postgres://..." --provider myage
fnox set API_KEY "sk-..." --provider myage -p prod  # prod profile
```

### Get a Secret

```bash
fnox get SECRET_NAME --age-key-file ~/.age/key.txt

# With root-protected key
sudo cat /var/keys/age/key.txt > /tmp/k && fnox get SECRET_NAME --age-key-file /tmp/k && rm /tmp/k
```

### List Secrets

```bash
fnox list
fnox list -p prod  # prod profile only
```

### Run Command with Secrets as Env Vars

```bash
fnox exec --age-key-file ~/.age/key.txt -- ./my-app
fnox exec --age-key-file ~/.age/key.txt -- env | grep APTOS
```

### Import/Export

```bash
fnox export --format env > .env.encrypted
fnox import --format env < .env
```

### Profiles

```bash
fnox profiles                    # List profiles
fnox set KEY "val" -p prod      # Set in prod profile
fnox get KEY -p prod            # Get from prod profile
FNOX_PROFILE=prod fnox list     # Use prod by default
```

## Shell Integration

Add to `~/.zshrc`:

```bash
# fnox secret management (GF(3) integrated)
export FNOX_AGE_KEY_FILE=~/.age/key.txt
eval "$(~/.cargo/bin/fnox activate zsh)"
```

For root-protected keys, use the wrapper:

```bash
# /usr/local/bin/fnox-secure
#!/bin/bash
TEMP_KEY=$(mktemp)
trap "rm -f $TEMP_KEY" EXIT
sudo cat /var/keys/age/key.txt > "$TEMP_KEY"
~/.cargo/bin/fnox --age-key-file "$TEMP_KEY" "$@"
```

## Root-Protected Key Setup

### Move Keys to Root Storage

```bash
sudo mkdir -p /var/keys/{age,aptos/worlds,aptos/testnet}
sudo cp ~/.age/key.txt /var/keys/age/
sudo cp ~/.aptos/worlds/*.key /var/keys/aptos/worlds/
sudo chown -R root:wheel /var/keys
sudo chmod -R 600 /var/keys
sudo chmod 700 /var/keys /var/keys/age /var/keys/aptos /var/keys/aptos/worlds
```

### Verify

```bash
sudo cat /var/keys/age/key.txt > /tmp/k && fnox get TEST_SECRET --age-key-file /tmp/k && rm /tmp/k
```

## DuckDB Catalog

### Schema

```sql
CREATE TABLE identity (id INTEGER PRIMARY KEY, name VARCHAR, path VARCHAR, trit TINYINT);
CREATE TABLE keypair (id INTEGER PRIMARY KEY, identity_id INTEGER, pubkey VARCHAR, privkey_path VARCHAR, algorithm VARCHAR, trit TINYINT);
CREATE TABLE provider (id INTEGER PRIMARY KEY, name VARCHAR, trit TINYINT);
CREATE TABLE profile (id INTEGER PRIMARY KEY, name VARCHAR, trit TINYINT);
CREATE TABLE secret (id INTEGER PRIMARY KEY, name VARCHAR, keypair_id INTEGER, provider_id INTEGER, profile_id INTEGER, trit TINYINT);
```

### Query Examples

```bash
# List all secrets
duckdb ~/.config/keys/catalog.duckdb "SELECT name FROM secret"

# Check GF(3) conservation
duckdb ~/.config/keys/catalog.duckdb "SELECT * FROM gf3_total"

# Find Aptos keys
duckdb ~/.config/keys/catalog.duckdb "SELECT name FROM secret WHERE name LIKE 'APTOS%'"
```

## GF(3) Conservation

All entities are assigned trits (-1, 0, +1) such that:

```
Σ(trits) ≡ 0 (mod 3)
```

| Entity | Trit Assignment |
|--------|-----------------|
| age identity | -1 (validator) |
| ssh identity | 0 (coordinator) |
| gpg identity | +1 (generator) |
| default profile | 0 |
| prod profile | +1 |
| staging profile | -1 |
| secrets | cyclic: -1, 0, +1, -1, ... |

## ACSet Schema (Julia)

```julia
@present SchKeyStore(FreeSchema) begin
    Identity::Ob
    KeyPair::Ob
    Secret::Ob
    Provider::Ob
    Profile::Ob

    keypair_identity::Hom(KeyPair, Identity)
    secret_keypair::Hom(Secret, KeyPair)
    secret_provider::Hom(Secret, Provider)
    secret_profile::Hom(Secret, Profile)

    TritType::AttrType
    identity_trit::Attr(Identity, TritType)
    keypair_trit::Attr(KeyPair, TritType)
    secret_trit::Attr(Secret, TritType)
end
```

## Current Secrets Inventory

### Aptos Keys (38)

| Secret | Description |
|--------|-------------|
| `APTOS_ALICE_KEY` | Alice world key |
| `APTOS_BOB_KEY` | Bob world key |
| `APTOS_WORLD_[A-Z]_KEY` | 26 world keys |
| `APTOS_ALICE_MAINNET_KEY` | Alice mainnet profile |
| `APTOS_ALICE_TESTNET_KEY` | Alice testnet profile |
| `APTOS_BOB_MAINNET_KEY` | Bob mainnet profile |
| `APTOS_BOB_TESTNET_KEY` | Bob testnet profile |
| `APTOS_DEFAULT_KEY` | Default profile |
| `APTOS_TESTNET_ACCOUNT_KEY` | Testnet account |
| `APTOS_TESTNET_CONSENSUS_KEY` | Testnet consensus |
| `APTOS_TESTNET_FULLNODE_KEY` | Testnet fullnode |
| `APTOS_TESTNET_VALIDATOR_KEY` | Testnet validator |
| `APTOS_TESTNET_MINT_KEY` | Testnet mint |

### Other Secrets (4)

| Secret | Description |
|--------|-------------|
| `AMP_API_KEY` | AMP API key |
| `GOOGLE_CLIENT_SECRET_PATH` | Google OAuth path |
| `TEST_SECRET` | Test secret |

## Integration with Other Skills

### cognitive-surrogate (trit: 0)

```python
# Use fnox secrets in surrogate training
fnox exec --age-key-file ~/.age/key.txt -- python train_surrogate.py
```

### acsets (trit: -1)

```julia
# Query catalog via ACSet navigation
secrets_for_identity(ks, aptos_identity_id)
```

### gay-mcp (trit: +1)

```python
# Deterministic secret access coloring
seed = GaySeed.from_string("fnox-session")
color = derive_color(seed, secret_name)
```

## Triadic Bundle

```
fnox-secrets (-1) ⊗ cognitive-surrogate (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Files

```
~/.cargo/bin/fnox              # fnox binary
~/fnox.toml                    # Encrypted secrets (git-safe)
/var/keys/age/key.txt          # Root-protected age key
/var/keys/aptos/               # Root-protected Aptos keys
~/.config/keys/catalog.duckdb  # DuckDB catalog
~/.config/keys/schema.jl       # ACSet schema
/usr/local/bin/fnox-secure     # Sudo wrapper (optional)
```

## Troubleshooting

### "No providers configured"

```bash
fnox provider add myage age
# Then edit fnox.toml to set recipients
```

### "Cannot decrypt"

```bash
# Check age key path
fnox get SECRET --age-key-file ~/.age/key.txt

# For root-protected
sudo cat /var/keys/age/key.txt > /tmp/k && fnox get SECRET --age-key-file /tmp/k; rm /tmp/k
```

### "Secret not found"

```bash
fnox list  # Check secret exists
fnox list -p prod  # Check correct profile
```

## References

- [fnox GitHub](https://github.com/jdx/fnox)
- [age encryption](https://age-encryption.org/)
- [ACSets.jl](https://github.com/AlgebraicJulia/ACSets.jl)