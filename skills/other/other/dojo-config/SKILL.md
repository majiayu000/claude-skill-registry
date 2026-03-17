---
name: dojo-config
description: Configure Scarb.toml, dojo profiles, world settings, and dependencies. Use when setting up project configuration, managing dependencies, or configuring deployment environments.
allowed-tools: Read, Write, Edit, Glob
---

# Dojo Configuration Management

Manage Dojo project configuration including Scarb.toml, deployment profiles, and world settings.

## When to Use This Skill

- "Configure Dojo for my project"
- "Update Scarb.toml dependencies"
- "Set up deployment profiles"
- "Configure world settings"

## What This Skill Does

Manages configuration files:
- `Scarb.toml` - Package manifest and dependencies
- `dojo_dev.toml` - Local development profile
- `dojo_<profile>.toml` - Other environment profiles
- World configuration, namespaces, and permissions

## Quick Start

**Interactive mode:**
```
"Update my Dojo configuration"
```

I'll ask about:
- What to configure (dependencies, profiles, world)
- Environment (dev, testnet, mainnet)
- Specific settings

**Direct mode:**
```
"Add the Origami library to my dependencies"
"Configure production deployment for Sepolia"
```

## Configuration Files

Dojo projects use two types of configuration files:

### `Scarb.toml` - Project Manifest

Defines project dependencies and build settings:

```toml
[package]
cairo-version = "2.12.2"
name = "my-dojo-game"
version = "1.0.0"
edition = "2024_07"

[[target.starknet-contract]]
sierra = true
build-external-contracts = ["dojo::world::world_contract::world"]

[dependencies]
starknet = "2.12.2"
dojo = "1.7.1"

[dev-dependencies]
cairo_test = "2.12.2"
dojo_cairo_test = "1.7.1"

[tool.scarb]
allow-prebuilt-plugins = ["dojo_cairo_macros"]
```

### `dojo_<profile>.toml` - Profile Configuration

Profile-specific deployment settings.
Dojo looks for `dojo_dev.toml` by default.

```toml
[world]
name = "My Game"
description = "An awesome on-chain game"
seed = "my-unique-seed"
cover_uri = "file://assets/cover.png"
icon_uri = "file://assets/icon.png"

[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."

[namespace]
default = "my_game"

[writers]
"my_game" = ["my_game-actions"]

[owners]
"my_game" = ["my_game-admin"]
```

## Profile System

Dojo uses profiles to manage different environments:

```bash
# Use default 'dev' profile (dojo_dev.toml)
sozo build
sozo migrate

# Use specific profile (dojo_mainnet.toml)
sozo build --profile mainnet
sozo migrate --profile mainnet
```

**Profile file naming:** `dojo_<profile>.toml`
- `dojo_dev.toml` - Development (default)
- `dojo_staging.toml` - Staging
- `dojo_mainnet.toml` - Production

## World Configuration

```toml
[world]
name = "My Game"                    # Human-readable name
description = "A provable game"     # Description
seed = "my-unique-seed"             # Unique seed for address generation
cover_uri = "ipfs://Qm..."          # Cover image (ipfs:// or file://)
icon_uri = "ipfs://Qm..."           # Icon image

[world.socials]
x = "https://x.com/mygame"
discord = "https://discord.gg/mygame"
```

## Environment Settings

```toml
[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."
# Or use keystore for production:
# keystore_path = "/path/to/keystore"
world_address = "0x077c0..."        # Set after first deployment
```

## Namespace Configuration

Namespaces organize your resources:

```toml
[namespace]
default = "my_game"                 # Default namespace for all resources

# Optional: Map specific resources to namespaces
mappings = { "weapons" = ["Sword", "Bow"], "characters" = ["Player", "Enemy"] }
```

Resources get tagged as `<namespace>-<resource_name>`.

## Permission Configuration

Set up initial permissions at deployment time:

```toml
[writers]
# Namespace-level: actions can write to all resources in my_game
"my_game" = ["my_game-actions"]
# Resource-specific: movement can only write to Position
"my_game-Position" = ["my_game-movement"]

[owners]
# Namespace ownership
"my_game" = ["my_game-admin"]
```

## Dependencies

### Add Dojo Dependencies

```toml
[dependencies]
starknet = "2.12.2"
dojo = "1.7.1"

[dev-dependencies]
cairo_test = "2.12.2"
dojo_cairo_test = "1.7.1"
```

### Add External Libraries

**Origami (game utilities):**
```toml
[dependencies]
origami_token = { git = "https://github.com/dojoengine/origami", tag = "v1.0.0" }
```

**Alexandria (math utilities):**
```toml
[dependencies]
alexandria_math = { git = "https://github.com/keep-starknet-strange/alexandria" }
```

### External Contracts

When using external libraries with models:

```toml
[[target.starknet-contract]]
build-external-contracts = [
    "dojo::world::world_contract::world",
    "armory::models::m_Flatbow",        # Format: <crate>::<path>::m_<ModelName>
]
```

## Environment Examples

### Development (dojo_dev.toml)

```toml
[world]
name = "My Game (Dev)"
seed = "dev-my-game"

[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."

[namespace]
default = "dev"

[writers]
"dev" = ["dev-actions"]
```

### Production (dojo_mainnet.toml)

```toml
[world]
name = "My Game"
seed = "prod-my-game"
description = "Production deployment"
cover_uri = "ipfs://YourCoverHash"
icon_uri = "ipfs://YourIconHash"

[env]
rpc_url = "https://api.cartridge.gg/x/starknet/mainnet"
account_address = "0x..."
keystore_path = "~/.starknet_accounts/mainnet.json"

[namespace]
default = "game"

[writers]
"game" = ["game-actions"]

[owners]
"game" = ["game-admin"]
```

## Security

### Protecting Secrets

**Never commit private keys.** Use `.gitignore`:

```
# Ignore sensitive configs
dojo_mainnet.toml
dojo_*_secrets.toml

# Keep development config
!dojo_dev.toml
```

**Use keystore for production:**
```toml
[env]
keystore_path = "~/.starknet_accounts/mainnet.json"
# Instead of: private_key = "0x..."
```

## Troubleshooting

**"Profile not found":**
- Ensure `dojo_<profile>.toml` exists in project root
- Check spelling matches the `--profile` flag

**"World not found":**
- Set `world_address` in `[env]` after first deployment
- Verify RPC URL is correct

**"Account not found":**
- Ensure account is deployed on target network
- Check account_address format (should start with 0x)

## Next Steps

After configuration:
1. Use `dojo-deploy` skill to deploy with your config
2. Use `dojo-migrate` skill when updating deployments
3. Use `dojo-world` skill to manage runtime permissions

## Related Skills

- **dojo-init**: Initialize new project with config
- **dojo-deploy**: Deploy using configuration
- **dojo-migrate**: Update deployed worlds
- **dojo-world**: Manage world permissions
