---
name: dojo-test
description: Write tests for Dojo models and systems using spawn_test_world, cheat codes, and assertions. Use when testing game logic, verifying state changes, or ensuring system correctness.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Dojo Test Generation

Write comprehensive tests for your Dojo models and systems using Cairo's test framework and Dojo's test utilities.

## When to Use This Skill

- "Write tests for the move system"
- "Test the Position model"
- "Add unit tests for combat logic"
- "Create integration tests"

## What This Skill Does

Generates test files with:
- `spawn_test_world()` setup
- Model and system registration
- Test functions with assertions
- Cheat code usage for manipulating execution context
- State verification

## Quick Start

**Interactive mode:**
```
"Write tests for the spawn system"
```

I'll ask about:
- What to test (models, systems, or both)
- Test scenarios (happy path, edge cases)
- State assertions needed

**Direct mode:**
```
"Test that the move system correctly updates Position"
```

## Running Tests

```bash
# Run all tests
sozo test

# Run specific test
sozo test test_spawn
```

## Test Structure

### Unit Tests (in model files)

Place unit tests in the same file as the model:

```cairo
// models.cairo

#[derive(Copy, Drop, Serde)]
#[dojo::model]
struct Position {
    #[key]
    player: ContractAddress,
    vec: Vec2,
}

#[cfg(test)]
mod tests {
    use super::{Position, Vec2, Vec2Trait};

    #[test]
    fn test_vec_is_zero() {
        assert!(Vec2Trait::is_zero(Vec2 { x: 0, y: 0 }), "not zero");
    }

    #[test]
    fn test_vec_is_equal() {
        let position = Vec2 { x: 420, y: 0 };
        assert!(position.is_equal(Vec2 { x: 420, y: 0 }), "not equal");
    }
}
```

### Integration Tests

Create a `tests` directory for system integration tests:

```cairo
// tests/test_move.cairo

#[cfg(test)]
mod tests {
    use dojo::model::{ModelStorage, ModelValueStorage, ModelStorageTest};
    use dojo::world::WorldStorageTrait;
    use dojo_cairo_test::{spawn_test_world, NamespaceDef, TestResource, ContractDefTrait};

    use dojo_starter::systems::actions::{actions, IActionsDispatcher, IActionsDispatcherTrait};
    use dojo_starter::models::{Position, m_Position, Moves, m_Moves, Direction};

    fn namespace_def() -> NamespaceDef {
        NamespaceDef {
            namespace: "dojo_starter",
            resources: [
                TestResource::Model(m_Position::TEST_CLASS_HASH),
                TestResource::Model(m_Moves::TEST_CLASS_HASH),
                TestResource::Event(actions::e_Moved::TEST_CLASS_HASH),
                TestResource::Contract(actions::TEST_CLASS_HASH)
            ].span()
        }
    }

    fn contract_defs() -> Span<ContractDef> {
        [
            ContractDefTrait::new(@"dojo_starter", @"actions")
                .with_writer_of([dojo::utils::bytearray_hash(@"dojo_starter")].span())
        ].span()
    }

    #[test]
    fn test_move() {
        let caller = starknet::contract_address_const::<0x0>();

        let ndef = namespace_def();
        let mut world = spawn_test_world([ndef].span());

        // Sync permissions and initializations
        world.sync_perms_and_inits(contract_defs());

        // Get contract address from DNS
        let (contract_address, _) = world.dns(@"actions").unwrap();
        let actions_system = IActionsDispatcher { contract_address };

        // Spawn player
        actions_system.spawn();

        // Read initial state
        let initial_moves: Moves = world.read_model(caller);
        let initial_position: Position = world.read_model(caller);

        assert(
            initial_position.vec.x == 10 && initial_position.vec.y == 10,
            "wrong initial position"
        );

        // Move right
        actions_system.move(Direction::Right(()));

        // Verify state changes
        let moves: Moves = world.read_model(caller);
        assert(moves.remaining == initial_moves.remaining - 1, "moves is wrong");

        let new_position: Position = world.read_model(caller);
        assert(new_position.vec.x == initial_position.vec.x + 1, "position x is wrong");
        assert(new_position.vec.y == initial_position.vec.y, "position y is wrong");
    }
}
```

### Testing Model Read/Write

```cairo
#[test]
fn test_world_test_set() {
    let caller = starknet::contract_address_const::<0x0>();
    let ndef = namespace_def();
    let mut world = spawn_test_world([ndef].span());

    // Test initial position (default zero)
    let mut position: Position = world.read_model(caller);
    assert(position.vec.x == 0 && position.vec.y == 0, "initial position wrong");

    // Test write_model_test (bypasses permissions)
    position.vec.x = 122;
    position.vec.y = 88;
    world.write_model_test(@position);

    let mut position: Position = world.read_model(caller);
    assert(position.vec.y == 88, "write_model_test failed");

    // Test model deletion
    world.erase_model(@position);
    let position: Position = world.read_model(caller);
    assert(position.vec.x == 0 && position.vec.y == 0, "erase_model failed");
}
```

## Cheat Codes

Use starknet's built-in testing cheat codes to manipulate execution context:

### Set Caller Address
```cairo
use starknet::{testing, contract_address_const};

#[test]
fn test_as_different_caller() {
    let player1 = contract_address_const::<'player1'>();
    testing::set_caller_address(player1);
    // Now get_caller_address() returns player1
}
```

### Set Contract Address
```cairo
use starknet::{testing, contract_address_const};

#[test]
fn test_with_contract_address() {
    let contract = contract_address_const::<'contract'>();
    testing::set_contract_address(contract);
    // Now get_contract_address() returns contract
}
```

### Set Block Timestamp
```cairo
use starknet::testing;

#[test]
fn test_with_timestamp() {
    testing::set_block_timestamp(123456);
    // Now get_block_timestamp() returns 123456
}
```

### Set Block Number
```cairo
use starknet::testing;

#[test]
fn test_with_block_number() {
    testing::set_block_number(1234567);
    // Now get_block_number() returns 1234567
}
```

## Test Patterns

### Test Expected Panic
```cairo
#[test]
#[should_panic(expected: ('No moves remaining',))]
fn test_no_moves_remaining() {
    // Setup with zero moves
    // ...
    actions_system.move(Direction::Right(())); // Should panic
}
```

### Test Multiple Players
```cairo
#[test]
fn test_two_players() {
    let player1 = contract_address_const::<0x111>();
    let player2 = contract_address_const::<0x222>();

    // Player 1 actions
    testing::set_contract_address(player1);
    actions_system.spawn();

    // Player 2 actions
    testing::set_contract_address(player2);
    actions_system.spawn();

    // Verify both have independent state
    let pos1: Position = world.read_model(player1);
    let pos2: Position = world.read_model(player2);
}
```

### Test State Transitions
```cairo
#[test]
fn test_spawn_then_move() {
    // Initial state
    actions_system.spawn();
    let initial: Position = world.read_model(caller);

    // Transition
    actions_system.move(Direction::Right(()));

    // Verify
    let after: Position = world.read_model(caller);
    assert(after.vec.x == initial.vec.x + 1, "did not move right");
}
```

## Key Test Utilities

| Function | Purpose |
|----------|---------|
| `spawn_test_world([ndef].span())` | Create test world with models |
| `world.sync_perms_and_inits(contract_defs())` | Sync permissions |
| `world.dns(@"contract_name")` | Get contract address by name |
| `world.read_model(keys)` | Read model state |
| `world.write_model_test(@model)` | Write model (bypass permissions) |
| `world.erase_model(@model)` | Delete model |

## Test Organization

```
src/
├── models.cairo         # Include unit tests in #[cfg(test)] mod
├── systems/
│   └── actions.cairo    # Include unit tests in #[cfg(test)] mod
└── tests/
    └── test_world.cairo # Integration tests
```

## Next Steps

After writing tests:
1. Run `sozo test` to execute
2. Use `dojo-review` skill to verify test coverage
3. Run tests before deploying with `dojo-deploy`

## Related Skills

- **dojo-model**: Create models to test
- **dojo-system**: Create systems to test
- **dojo-review**: Review test coverage
- **dojo-deploy**: Deploy after tests pass
