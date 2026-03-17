---
name: dojo-review
description: Review Dojo code for best practices, common mistakes, security issues, and optimization opportunities. Use when auditing models, systems, tests, or preparing for deployment.
allowed-tools: Read, Grep, Glob
---

# Dojo Code Review

Review your Dojo code for common issues, security concerns, and optimization opportunities.

## When to Use This Skill

- "Review my Dojo code"
- "Check this system for issues"
- "Audit my models"
- "Review before deploying"

## What This Skill Does

Analyzes your code for:
- Model design patterns
- System implementation issues
- Security vulnerabilities
- Gas optimization opportunities
- Test coverage gaps
- Common mistakes

## Quick Start

**Interactive mode:**
```
"Review my Dojo project"
```

I'll ask about:
- What to review (models, systems, tests, all)
- Focus areas (security, performance)

**Direct mode:**
```
"Review the combat system for security issues"
"Check if my models follow ECS patterns"
```

## Review Categories

### Model Review

**Checks:**
- Required trait derivations (`Drop`, `Serde`)
- Key fields defined correctly (`#[key]`)
- Keys come before data fields
- Appropriate field types
- Small, focused models (ECS principle)

**Common issues:**
```cairo
// ❌ Missing required traits
#[dojo::model]
struct Position { ... }

// ✅ Required traits
#[derive(Drop, Serde)]
#[dojo::model]
struct Position { ... }

// ❌ Keys after data fields
struct Example {
    data: u32,
    #[key]
    id: u32,  // Must come first!
}

// ✅ Keys first
struct Example {
    #[key]
    id: u32,
    data: u32,
}
```

### System Review

**Checks:**
- Proper interface definition (`#[starknet::interface]`)
- Contract attribute (`#[dojo::contract]`)
- World access with namespace (`self.world(@"namespace")`)
- Input validation
- Event emissions
- Error messages

**Common issues:**
```cairo
// ❌ No input validation
fn set_health(ref self: ContractState, health: u8) {
    // Could be zero or invalid!
}

// ✅ Input validation
fn set_health(ref self: ContractState, health: u8) {
    assert(health > 0 && health <= 100, 'invalid health');
}

// ❌ No authorization check for sensitive function
fn admin_function(ref self: ContractState) {
    // Anyone can call!
}

// ✅ Authorization check
fn admin_function(ref self: ContractState) {
    let mut world = self.world_default();
    let caller = get_caller_address();
    assert(
        world.is_owner(selector_from_tag!("my_game"), caller),
        'not authorized'
    );
}
```

### Security Review

**Checks:**
- Authorization on sensitive functions
- Integer overflow/underflow
- Access control for model writes
- State consistency

**Common vulnerabilities:**
```cairo
// ❌ Integer underflow
health.current -= damage;  // Could underflow if damage > current!

// ✅ Safe subtraction
health.current = if health.current > damage {
    health.current - damage
} else {
    0
};

// ❌ Missing ownership check
fn transfer_nft(ref self: ContractState, token_id: u256, to: ContractAddress) {
    // Anyone can transfer anyone's NFT!
    let mut nft: NFT = world.read_model(token_id);
    nft.owner = to;
    world.write_model(@nft);
}

// ✅ Ownership check
fn transfer_nft(ref self: ContractState, token_id: u256, to: ContractAddress) {
    let mut world = self.world_default();
    let caller = get_caller_address();

    let mut nft: NFT = world.read_model(token_id);
    assert(nft.owner == caller, 'not owner');

    nft.owner = to;
    world.write_model(@nft);
}
```

### Gas Optimization

**Checks:**
- Minimal model reads/writes
- Efficient data types
- Unnecessary computations

**Optimization opportunities:**
```cairo
// ❌ Multiple reads of same model
let pos: Position = world.read_model(player);
let x = pos.x;
let pos2: Position = world.read_model(player);  // Duplicate!
let y = pos2.y;

// ✅ Single read
let pos: Position = world.read_model(player);
let x = pos.x;
let y = pos.y;

// ❌ Oversized types
struct Position {
    #[key]
    player: ContractAddress,
    x: u128,  // Overkill for coordinates
    y: u128,
}

// ✅ Appropriate types
struct Position {
    #[key]
    player: ContractAddress,
    x: u32,  // Sufficient for most games
    y: u32,
}
```

### Test Coverage

**Checks:**
- Unit tests for models
- Integration tests for systems
- Edge case coverage
- Failure case testing

**Coverage gaps:**
```cairo
// Missing tests:
// - Boundary values (max health, zero health)
// - Unauthorized access
// - Invalid inputs
// - Full workflow integration

// Add:
#[test]
fn test_health_bounds() { ... }

#[test]
#[should_panic(expected: ('not authorized',))]
fn test_unauthorized_access() { ... }

#[test]
fn test_spawn_move_attack_flow() { ... }
```

## Review Checklist

### Models
- [ ] All models derive `Drop` and `Serde`
- [ ] Key fields have `#[key]` attribute
- [ ] Keys come before data fields
- [ ] Models are small and focused
- [ ] Field types are appropriate size
- [ ] Custom types derive `Introspect`

### Systems
- [ ] Interface uses `#[starknet::interface]`
- [ ] Contract uses `#[dojo::contract]`
- [ ] World access uses correct namespace
- [ ] Input validation for all parameters
- [ ] Clear error messages
- [ ] Events emitted for important actions
- [ ] Caller identity verified when needed

### Security
- [ ] Sensitive functions check permissions
- [ ] Integer math handles over/underflow
- [ ] Ownership verified before transfers
- [ ] State changes are atomic

### Performance
- [ ] Minimal model reads per function
- [ ] Efficient data types used
- [ ] No unnecessary computations

### Tests
- [ ] Unit tests for models
- [ ] Integration tests for systems
- [ ] Edge cases tested
- [ ] Failure cases tested with `#[should_panic]`

## Common Anti-Patterns

### God Models
```cairo
// ❌ Everything in one model
#[dojo::model]
struct Player {
    #[key] player: ContractAddress,
    x: u32, y: u32,  // Position
    health: u8, mana: u8,  // Stats
    gold: u32, items: u8,  // Inventory
    level: u8, xp: u32,  // Progress
}

// ✅ Separate concerns (ECS pattern)
Position { player, x, y }
Stats { player, health, mana }
Inventory { player, gold, items }
Progress { player, level, xp }
```

### Missing world_default Helper
```cairo
// ❌ Repeating namespace everywhere
fn spawn(ref self: ContractState) {
    let mut world = self.world(@"my_game");
    // ...
}

fn move(ref self: ContractState, direction: u8) {
    let mut world = self.world(@"my_game");
    // ...
}

// ✅ Use internal helper
#[generate_trait]
impl InternalImpl of InternalTrait {
    fn world_default(self: @ContractState) -> dojo::world::WorldStorage {
        self.world(@"my_game")
    }
}

fn spawn(ref self: ContractState) {
    let mut world = self.world_default();
    // ...
}
```

### Not Emitting Events
```cairo
// ❌ No events
fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) {
    // Transfer logic but no event
}

// ✅ Emit events for indexing
fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) {
    // Transfer logic
    world.emit_event(@Transferred { from, to, amount });
}
```

## Next Steps

After code review:
1. Fix identified issues
2. Add missing tests
3. Re-run review to verify fixes
4. Use `dojo-test` skill to ensure tests pass
5. Use `dojo-deploy` skill when ready

## Related Skills

- **dojo-model**: Fix model issues
- **dojo-system**: Fix system issues
- **dojo-test**: Add missing tests
- **dojo-deploy**: Deploy after review
