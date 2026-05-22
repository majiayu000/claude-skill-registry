---
name: dojo-system
description: Create Dojo systems that implement game logic, modify model state, and handle player actions. Use when implementing game mechanics, player commands, or automated logic.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Dojo System Generation

Create Dojo systems (smart contracts) that implement your game's logic and modify model state.

## Essential Imports (Dojo 1.0+)

**Copy these imports for any Dojo system:**

```cairo
// Core Dojo imports - ALWAYS needed for systems
use dojo::model::{ModelStorage, ModelValueStorage};
use dojo::event::EventStorage;

// Starknet essentials
use starknet::{ContractAddress, get_caller_address, get_block_timestamp};
```

### Where does `self.world_default()` come from?

**`self.world_default()` is provided automatically by `#[dojo::contract]`** - no import needed!

```cairo
#[dojo::contract]  // <-- This macro provides world_default()
mod my_system {
    use dojo::model::{ModelStorage, ModelValueStorage};
    use dojo::event::EventStorage;

    #[abi(embed_v0)]
    impl MyImpl of IMySystem<ContractState> {
        fn my_function(ref self: ContractState) {
            // world_default() is available because of #[dojo::contract]
            let mut world = self.world_default();
            
            // Now use world for all operations...
        }
    }
}
```

### How to emit events

**Requires:** `use dojo::event::EventStorage;`

```cairo
// 1. Define the event (outside impl block)
#[derive(Copy, Drop, Serde)]
#[dojo::event]
struct PlayerMoved {
    #[key]
    player: ContractAddress,
    from_x: u32,
    from_y: u32,
    to_x: u32,
    to_y: u32,
}

// 2. Emit it (inside a function)
fn move_player(ref self: ContractState, direction: u8) {
    let mut world = self.world_default();
    
    // ... game logic ...
    
    // Emit event - note the @ for snapshot
    world.emit_event(@PlayerMoved {
        player: get_caller_address(),
        from_x: 0,
        from_y: 0, 
        to_x: 1,
        to_y: 1,
    });
}
```

### Quick reference: What imports what

| You want to use | Import this |
|----------------|-------------|
| `world.read_model()` | `use dojo::model::ModelStorage;` |
| `world.write_model()` | `use dojo::model::ModelStorage;` |
| `world.emit_event()` | `use dojo::event::EventStorage;` |
| `self.world_default()` | Nothing! Provided by `#[dojo::contract]` |
| `get_caller_address()` | `use starknet::get_caller_address;` |

## When to Use This Skill

- "Create a spawn system"
- "Add a move system that updates position"
- "Implement combat logic"
- "Generate a system for [game action]"

## What This Skill Does

Generates Cairo system contracts with:
- `#[dojo::contract]` attribute
- Interface definition with `#[starknet::interface]`
- System implementation
- World access (`world.read_model()`, `world.write_model()`)
- Event emissions with `#[dojo::event]`

## Quick Start

**Interactive mode:**
```
"Create a system for player movement"
```

I'll ask about:
- System name
- Functions and their parameters
- Models used
- Authorization requirements

**Direct mode:**
```
"Create a move system that updates Position based on Direction"
```

## System Structure

A Dojo contract consists of an interface trait and a contract module:

```cairo
use dojo_starter::models::{Direction, Position};

// Define the interface
#[starknet::interface]
trait IActions<T> {
    fn spawn(ref self: T);
    fn move(ref self: T, direction: Direction);
}

// Dojo contract
#[dojo::contract]
pub mod actions {
    use super::{IActions, Direction, Position};
    use starknet::{ContractAddress, get_caller_address};
    use dojo_starter::models::{Vec2, Moves};

    use dojo::model::{ModelStorage, ModelValueStorage};
    use dojo::event::EventStorage;

    // Define a custom event
    #[derive(Copy, Drop, Serde)]
    #[dojo::event]
    pub struct Moved {
        #[key]
        pub player: ContractAddress,
        pub direction: Direction,
    }

    #[abi(embed_v0)]
    impl ActionsImpl of IActions<ContractState> {
        fn spawn(ref self: ContractState) {
            let mut world = self.world_default();
            let player = get_caller_address();

            // Read current position (defaults to zero if not set)
            let position: Position = world.read_model(player);

            // Set initial position
            let new_position = Position {
                player,
                vec: Vec2 { x: position.vec.x + 10, y: position.vec.y + 10 }
            };
            world.write_model(@new_position);

            // Set initial moves
            let moves = Moves {
                player,
                remaining: 100,
                last_direction: Direction::None(()),
                can_move: true
            };
            world.write_model(@moves);
        }

        fn move(ref self: ContractState, direction: Direction) {
            let mut world = self.world_default();
            let player = get_caller_address();

            // Read current state
            let position: Position = world.read_model(player);
            let mut moves: Moves = world.read_model(player);

            // Update moves
            moves.remaining -= 1;
            moves.last_direction = direction;

            // Calculate next position
            let next = next_position(position, direction);

            // Write updated state
            world.write_model(@next);
            world.write_model(@moves);

            // Emit event
            world.emit_event(@Moved { player, direction });
        }
    }

    // Internal helper to get world with namespace
    #[generate_trait]
    impl InternalImpl of InternalTrait {
        fn world_default(self: @ContractState) -> dojo::world::WorldStorage {
            self.world(@"dojo_starter")
        }
    }
}

// Helper function outside the contract
fn next_position(mut position: Position, direction: Direction) -> Position {
    match direction {
        Direction::None => { return position; },
        Direction::Left => { position.vec.x -= 1; },
        Direction::Right => { position.vec.x += 1; },
        Direction::Up => { position.vec.y -= 1; },
        Direction::Down => { position.vec.y += 1; },
    };
    position
}
```

## Key Concepts

### World Access
Get the world storage using your namespace:
```cairo
let mut world = self.world(@"my_namespace");
```

Create a helper function to avoid repeating the namespace:
```cairo
#[generate_trait]
impl InternalImpl of InternalTrait {
    fn world_default(self: @ContractState) -> dojo::world::WorldStorage {
        self.world(@"my_namespace")
    }
}
```

### Reading Models
```cairo
let position: Position = world.read_model(player);
```

### Writing Models
```cairo
world.write_model(@Position { player, vec: Vec2 { x: 10, y: 20 } });
```

### Emitting Events
Define events with `#[dojo::event]`:
```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::event]
pub struct PlayerMoved {
    #[key]
    pub player: ContractAddress,
    pub from: Vec2,
    pub to: Vec2,
}

// Emit in your function
world.emit_event(@PlayerMoved { player, from: old_pos, to: new_pos });
```

### Getting Caller
```cairo
use starknet::get_caller_address;

let player = get_caller_address();
```

### Generating Unique IDs
```cairo
let entity_id = world.uuid();
```

## System Design

### Single Responsibility
Each system should have one clear purpose:
- `MovementSystem`: Handles player/entity movement
- `CombatSystem`: Manages battles and damage
- `InventorySystem`: Manages items

### Stateless Design
Systems should be stateless, reading state from models:
```cairo
fn attack(ref self: ContractState, target: ContractAddress) {
    let mut world = self.world_default();
    let attacker = get_caller_address();

    // Read current state
    let attacker_stats: Combat = world.read_model(attacker);
    let mut target_stats: Combat = world.read_model(target);

    // Apply logic
    target_stats.health -= attacker_stats.damage;

    // Write updated state
    world.write_model(@target_stats);
}
```

### Input Validation
Validate inputs before modifying state:
```cairo
fn move(ref self: ContractState, direction: Direction) {
    let mut world = self.world_default();
    let player = get_caller_address();

    let moves: Moves = world.read_model(player);
    assert(moves.remaining > 0, 'No moves remaining');
    assert(moves.can_move, 'Movement disabled');

    // Proceed with movement
}
```

## Permissions

Systems need writer permission to modify models.
Configure in `dojo_dev.toml`:
```toml
[writers]
"my_namespace" = ["my_namespace-actions"]
```

Or grant specific model access:
```toml
[writers]
"my_namespace-Position" = ["my_namespace-actions"]
"my_namespace-Moves" = ["my_namespace-actions"]
```

## Next Steps

After creating systems:
1. Use `dojo-test` skill to test system logic
2. Use `dojo-review` skill to check for issues
3. Use `dojo-deploy` skill to deploy your world
4. Use `dojo-client` skill to call systems from frontend

## Related Skills

- **dojo-model**: Define models used by systems
- **dojo-test**: Test system logic
- **dojo-review**: Review system implementation
- **dojo-deploy**: Deploy systems to network
