---
name: dojo-migrate
description: Manage world migrations, handle breaking changes, and upgrade Dojo versions. Use when updating deployed worlds, migrating to new versions, or handling schema changes.
allowed-tools: Read, Bash, Grep, Glob
---

# Dojo Migration Management

Handle world migrations, upgrades, and breaking changes when updating deployed Dojo worlds.

## When to Use This Skill

- "Migrate my world changes"
- "Upgrade to new Dojo version"
- "Handle breaking changes"
- "Update deployed models"

## What This Skill Does

Manages migration workflows:
- Analyze migration diffs
- Plan migration strategies
- Execute migrations
- Handle breaking changes
- Upgrade Dojo versions

## Quick Start

**Update existing world:**
```
"Migrate my changes to the deployed world"
```

**Version upgrade:**
```
"Upgrade my project to Dojo v1.8.0"
```

## Migration Workflow

### 1. Inspect Changes

```bash
sozo inspect
```

Shows:
- New models
- Modified models
- New systems/contracts
- Modified systems
- Status of all resources

### 2. Build and Test

```bash
sozo build
sozo test
```

### 3. Execute Migration

```bash
# Deploy with default dev profile
sozo migrate

# Deploy with specific profile
sozo migrate --profile sepolia
```

## Migration Types

### Additive Migrations (Safe)

**Adding new model:**
```cairo
// New model - safe to add
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct NewFeature {
    #[key]
    pub player: ContractAddress,
    pub data: u32,
}
```

**Adding new system:**
```cairo
// New system - safe to add
#[dojo::contract]
pub mod new_system {
    // Implementation
}
```

**Adding model field:**
```cairo
// Adding field - existing data will have default (zero) value
struct Position {
    #[key] player: ContractAddress,
    x: u32,
    y: u32,
    z: u32,  // New field
}
```

### Breaking Migrations (Dangerous)

**Changing key fields:**
```cairo
// Old
struct Position {
    #[key] player: ContractAddress,
    x: u32, y: u32,
}

// New - BREAKING! Different key structure
struct Position {
    #[key] entity_id: u32,  // Changed key
    x: u32, y: u32,
}
```

**Removing fields:**
```cairo
// Old
struct Stats {
    #[key] player: ContractAddress,
    health: u8,
    mana: u8,
}

// New - BREAKING! Data loss
struct Stats {
    #[key] player: ContractAddress,
    health: u8,
    // mana removed
}
```

**Changing field types:**
```cairo
// Old
struct Position {
    #[key] player: ContractAddress,
    x: u32,
    y: u32,
}

// New - BREAKING! Type incompatible
struct Position {
    #[key] player: ContractAddress,
    x: u128,  // Changed type
    y: u128,
}
```

## Handling Breaking Changes

### Option 1: New World

Deploy fresh world with different seed:
```toml
# dojo_dev.toml
[world]
seed = "my_game_v2"  # Different seed = new world address
```

```bash
sozo build && sozo migrate
```

### Option 2: Parallel Models

Keep both old and new versions:
```cairo
// Keep old model
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct PositionV1 {
    #[key] player: ContractAddress,
    x: u32, y: u32,
}

// Add new model
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct PositionV2 {
    #[key] entity_id: u32,
    x: u32, y: u32, z: u32,
}
```

### Option 3: Data Migration System

Create a migration system to transform data:
```cairo
#[dojo::contract]
pub mod migrator {
    fn migrate_positions(ref self: ContractState, players: Array<ContractAddress>) {
        let mut world = self.world_default();

        for player in players {
            // Read old format
            let old_pos: PositionV1 = world.read_model(player);

            // Transform to new format
            let new_pos = PositionV2 {
                entity_id: world.uuid(),
                x: old_pos.x,
                y: old_pos.y,
                z: 0,
            };

            // Write new format
            world.write_model(@new_pos);
        }
    }
}
```

## Version Upgrades

### Update Dojo Version

1. Update `Scarb.toml`:
```toml
[dependencies]
dojo = "1.8.0"

[dev-dependencies]
dojo_cairo_test = "1.8.0"
```

2. Review changelog for breaking changes

3. Build and test:
```bash
sozo build
sozo test
```

4. Migrate:
```bash
sozo migrate
```

## Migration Checklist

### Pre-Migration
- [ ] Review changes with `sozo inspect`
- [ ] Test changes locally on Katana
- [ ] Identify breaking changes
- [ ] Plan data migration if needed
- [ ] Test migration on testnet first

### Migration
- [ ] Build succeeds (`sozo build`)
- [ ] Tests pass (`sozo test`)
- [ ] Migration executes (`sozo migrate`)
- [ ] Verify new models/systems work
- [ ] Check existing data integrity

### Post-Migration
- [ ] Test all systems still work
- [ ] Update Torii indexer if needed
- [ ] Regenerate client bindings
- [ ] Update client integration
- [ ] Monitor for issues

## Common Scenarios

### Adding a New Model

```bash
# 1. Add model to code
# 2. Build
sozo build

# 3. Migrate
sozo migrate

# 4. Verify
sozo inspect
```

### Updating System Logic

```bash
# 1. Update system code
# 2. Build and test
sozo build
sozo test

# 3. Migrate (redeploys system)
sozo migrate

# 4. Test updated system
sozo execute my_game-actions spawn
```

## Troubleshooting

### "Class hash not found"
- Run `sozo build` first
- Check Scarb.toml version compatibility
- Clear `target/` directory and rebuild

### "Model already exists"
- Models cannot be removed from world
- Use versioned model names if structure changes
- Consider deploying new world

### "Migration failed"
- Check account has funds for gas
- Verify profile configuration
- Review `sozo inspect` output

## Next Steps

After migration:
1. Test all functionality
2. Update client bindings (`sozo build --typescript`)
3. Update Torii if model changes (`dojo-indexer` skill)
4. Monitor world for issues

## Related Skills

- **dojo-deploy**: Initial deployment
- **dojo-config**: Update configuration
- **dojo-world**: Manage permissions after migration
- **dojo-indexer**: Update indexer for new schema
- **dojo-client**: Update client bindings
