---
name: dojo-world
description: Manage world permissions, namespaces, resource registration, and access control. Use when configuring world ownership, setting up authorization policies, or managing resource permissions.
allowed-tools: Read, Write, Bash, Grep
---

# Dojo World Management

Manage your Dojo world's permissions, namespaces, resource registration, and access control policies.

## When to Use This Skill

- "Configure world permissions"
- "Set up namespace access"
- "Grant writer permissions"
- "Manage resource ownership"

## What This Skill Does

Handles world management:
- Namespace configuration
- Writer permissions (can write data)
- Owner permissions (can write data + manage permissions)
- Permission hierarchy management

## Quick Start

**Configure permissions:**
```
"Grant writer permission to my system"
```

**Check permissions:**
```
"List permissions for my world"
```

## Permission Concepts

### Permission Types

**Owner Permission:**
- Write data to the resource
- Grant and revoke permissions to others
- Upgrade the resource
- Set resource metadata

**Writer Permission:**
- Write data to the resource
- Cannot grant permissions to others
- Cannot upgrade the resource

**Reading is always permissionless.**

### Permission Hierarchy

```
World Owner (highest)
    └── Namespace Owner
        └── Resource Owner / Writer (lowest)
```

- **World Owner**: Can do anything in the world
- **Namespace Owner**: Can manage all resources in their namespace
- **Resource Owner**: Can manage a specific resource (model/contract/event)
- **Writer**: Can only write data to a resource

## Configuration-Based Permissions

Set permissions during deployment in `dojo_<profile>.toml`:

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

**Format:** `"<TARGET_TAG>" = ["<GRANTEE_TAG>"]`

## CLI Permission Management

### Grant Permissions

```bash
# Grant writer permission
sozo auth grant writer my_game-Position,my_game-actions

# Grant owner permission
sozo auth grant owner my_game,my_game-admin
```

### Revoke Permissions

```bash
# Revoke writer permission
sozo auth revoke writer my_game-Position,my_game-actions

# Revoke owner permission
sozo auth revoke owner my_game,my_game-admin
```

### List Permissions

```bash
# List all permissions
sozo auth list
```

## Runtime Permission Management (Cairo)

### Grant Permissions

```cairo
use dojo::world::WorldStorage;

// Grant writer permission to a contract
world.grant_writer(
    selector_from_tag!("my_game-Position"),
    movement_system_address
);

// Grant owner permission
world.grant_owner(
    selector_from_tag!("my_game-GameState"),
    new_owner_address
);
```

### Revoke Permissions

```cairo
// Revoke writer permission
world.revoke_writer(
    selector_from_tag!("my_game-Position"),
    old_system_address
);

// Revoke owner permission
world.revoke_owner(
    selector_from_tag!("my_game-GameState"),
    old_owner_address
);
```

### Check Permissions

```cairo
// Check if address is owner
let is_owner = world.is_owner(resource_selector, address);

// Check if address is writer
let can_write = world.is_writer(resource_selector, address);
```

## Permission Patterns

### Principle of Least Privilege

```cairo
// Good: Specific permissions for specific functions
world.grant_writer(selector_from_tag!("my_game-Position"), movement_contract);
world.grant_writer(selector_from_tag!("my_game-Health"), combat_contract);

// Bad: Overly broad permissions
world.grant_owner(selector_from_tag!("my_game"), movement_contract);
```

### Multi-System Architecture

```cairo
// Different systems handle different aspects
world.grant_writer(selector_from_tag!("my_game-Position"), movement_system);
world.grant_writer(selector_from_tag!("my_game-Health"), combat_system);
world.grant_writer(selector_from_tag!("my_game-Inventory"), inventory_system);

// Trading system needs access to Inventory too
world.grant_writer(selector_from_tag!("my_game-Inventory"), trading_system);
```

### Namespace-Level Permissions

Grant access to all resources in a namespace:

```cairo
// This system can write to ANY resource in "my_game" namespace
world.grant_writer(
    selector_from_tag!("my_game"),
    system_contract
);
```

### Admin System

```cairo
// Admin has owner permission on namespace
world.grant_owner(selector_from_tag!("my_game"), game_admin);

// Admin has owner permission on critical resources
world.grant_owner(selector_from_tag!("my_game-GameConfig"), game_admin);
```

## Authorization in Systems

### Public Functions

Anyone can call:
```cairo
fn spawn(ref self: ContractState) {
    let mut world = self.world_default();
    let player = get_caller_address();

    // No permission check - anyone can spawn
    world.write_model(@Position { player, vec: Vec2 { x: 0, y: 0 } });
}
```

### Checking Permissions

```cairo
fn admin_function(ref self: ContractState) {
    let mut world = self.world_default();
    let caller = get_caller_address();

    // Check caller is owner of the namespace
    assert(
        world.is_owner(selector_from_tag!("my_game"), caller),
        'not authorized'
    );

    // Proceed with admin logic
}
```

## Permission Events

The World contract emits events when permissions change:

```cairo
#[derive(Drop, starknet::Event)]
pub struct OwnerUpdated {
    #[key]
    pub resource: felt252,
    #[key]
    pub contract: ContractAddress,
    pub value: bool,
}

#[derive(Drop, starknet::Event)]
pub struct WriterUpdated {
    #[key]
    pub resource: felt252,
    #[key]
    pub contract: ContractAddress,
    pub value: bool,
}
```

## Common Scenarios

### Initial Setup (via config)

```toml
# dojo_dev.toml
[namespace]
default = "my_game"

[writers]
# All resources in my_game can be written by actions
"my_game" = ["my_game-actions"]

[owners]
# Admin system owns the namespace
"my_game" = ["my_game-admin"]
```

### Adding New System (runtime)

```cairo
fn add_new_system(ref self: ContractState, new_system_address: ContractAddress) {
    let mut world = self.world_default();

    // Must be namespace owner to grant permissions
    world.grant_writer(
        selector_from_tag!("my_game-Position"),
        new_system_address
    );
}
```

### Transfer Namespace Ownership

```cairo
fn transfer_ownership(ref self: ContractState, new_owner: ContractAddress) {
    let mut world = self.world_default();

    // Grant owner to new address
    world.grant_owner(selector_from_tag!("my_game"), new_owner);

    // Revoke from current owner
    world.revoke_owner(selector_from_tag!("my_game"), get_caller_address());
}
```

## Troubleshooting

### "Not authorized" errors
- Check writer permissions are granted
- Verify the system address is correct
- Check if permission is at namespace or resource level

### "Permission denied"
- Check you have owner permission to grant/revoke
- Verify you're calling from the correct account

### Debugging Permissions

```cairo
fn debug_permissions(world: @WorldStorage, resource: felt252, address: ContractAddress) {
    let is_owner = world.is_owner(resource, address);
    let is_writer = world.is_writer(resource, address);

    // Log or print these values for debugging
}
```

## Next Steps

After permission setup:
1. Test all permission checks work correctly
2. Document the permission structure
3. Set up monitoring for permission changes
4. Consider using a multi-sig for production owner accounts

## Related Skills

- **dojo-deploy**: Deploy world first
- **dojo-system**: Add authorization to systems
- **dojo-config**: Configure permissions in profile
- **dojo-review**: Audit permission setup
