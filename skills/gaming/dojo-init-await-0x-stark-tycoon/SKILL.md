---
name: dojo-init
description: Initialize new Dojo projects with proper directory structure, configuration files, and dependencies. Use when starting a new Dojo game project or setting up the initial project structure.
allowed-tools: Read, Write, Bash, Glob
---

# Dojo Project Initialization

Initialize new Dojo projects with the complete directory structure, configuration files, and dependencies.

## When to Use This Skill

- "Create a new Dojo project"
- "Initialize a Dojo game called [name]"
- "Set up a new Dojo application"
- "Start a new provable game project"

## What This Skill Does

Creates a complete Dojo project with:
- `Scarb.toml` with Dojo dependencies
- `dojo_dev.toml` for local development
- Source directory structure
- Example models and systems
- Test files

## Quick Start

**Using sozo init:**
```bash
sozo init my-game
```

This creates a new Dojo project from the [dojo-starter template](https://github.com/dojoengine/dojo-starter).

**Interactive mode:**
```
"Create a new Dojo project called my-game"
```

## Project Structure

After initialization:

```
my-game/
├── Scarb.toml              # Package manifest and dependencies
├── dojo_dev.toml           # Local development profile
├── dojo_release.toml       # Production deployment profile
└── src/
    ├── lib.cairo           # Module exports
    ├── models.cairo        # Game state models
    ├── systems/
    │   └── actions.cairo   # Game logic systems
    └── tests/
        └── test_world.cairo # Integration tests
```

## Configuration Files

### Scarb.toml

Package manifest with Dojo dependencies:

```toml
[package]
cairo-version = "2.12.2"
name = "my_game"
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

### dojo_dev.toml

Local development configuration:

```toml
[world]
name = "My Game"
seed = "my_game"

[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."

[namespace]
default = "my_game"

[writers]
"my_game" = ["my_game-actions"]
```

## Starter Template Contents

The starter template includes:

### Models (`src/models.cairo`)
- `Position` model with player key and Vec2 coordinates
- `Moves` model tracking remaining moves and direction
- `Direction` enum

### Systems (`src/systems/actions.cairo`)
- `spawn` function to initialize player state
- `move` function to update player position
- Example event emission

### Tests (`src/tests/test_world.cairo`)
- Test world setup with `spawn_test_world`
- Integration tests for spawn and move

## Development Workflow

1. **Initialize project:**
   ```bash
   sozo init my-game
   cd my-game
   ```

2. **Start Katana:**
   ```bash
   katana --dev --dev.no-fee
   ```

3. **Build and deploy:**
   ```bash
   sozo build && sozo migrate
   ```

4. **Test your system:**
   ```bash
   sozo execute my_game-actions spawn
   ```

5. **Run tests:**
   ```bash
   sozo test
   ```

## Customization

After initialization, customize your project:

1. **Add models:** Create new model structs in `src/models.cairo` or separate files
2. **Add systems:** Create new contract modules in `src/systems/`
3. **Update permissions:** Edit `[writers]` in `dojo_dev.toml`
4. **Add dependencies:** Edit `[dependencies]` in `Scarb.toml`

## Next Steps

After initialization:
1. Use `dojo-model` skill to add game state models
2. Use `dojo-system` skill to implement game logic
3. Use `dojo-test` skill to write tests
4. Use `dojo-deploy` skill to deploy your world

## Related Skills

- **dojo-model**: Add models to your project
- **dojo-system**: Add systems to your project
- **dojo-config**: Modify configuration
- **dojo-deploy**: Deploy your project
