---
name: dojo-integration-test
description: Use this skill when the user asks to "test dojo contracts", "run integration tests", "start dojo stack", "test with torii", "verify contract behavior", mentions integration testing for Dojo/Cairo contracts, or needs to set up local katana/torii infrastructure.
version: 1.0.0
---

# Dojo Integration Test Skill

This skill sets up a complete local Dojo development stack and enables integration testing of smart contracts.

## Required Input

Before running this skill, you MUST know the contract location on local disk:
- **Contract Path**: Absolute or relative path to the Dojo project directory (e.g., `./worlds/dojo-starter`)

This path should contain:
- `Scarb.toml` - Cairo project configuration
- `src/` - Cairo source files
- `dojo_dev.toml` - Dojo development configuration

## Prerequisites Check

Before starting, verify the following:

1. **Required asdf plugins**: sozo, katana, torii, scarb
   ```bash
   asdf current sozo && asdf current katana && asdf current torii && asdf current scarb
   ```

2. **Project files**:
   - `.tool-versions` - defines tool versions
   - `Scarb.toml` - Cairo project configuration
   - `dojo_dev.toml` - Dojo development configuration

3. **Available ports**:
   - 5050 (Katana RPC)
   - 8080 (Torii HTTP)
   - 50051 (Torii gRPC)

   Check with: `lsof -i :5050 -i :8080 -i :50051`

## Contract Information Extraction

Extract contract information from manifest and config files:

```bash
# Get world address (after migration)
jq -r '.world.address' manifest_dev.json

# List all contracts
jq -r '.contracts[].tag' manifest_dev.json

# List all models
jq -r '.models[].tag' manifest_dev.json

# Get RPC URL from dojo_dev.toml
grep rpc_url dojo_dev.toml
```

## Infrastructure Startup Sequence

### Step 1: Start Katana

```bash
katana --dev --dev.no-fee &
```

Wait for: `curl -s localhost:5050 | jq .`

### Step 2: Build and Migrate Contracts

```bash
sozo build && sozo migrate
```

Extract world address after migration:
```bash
WORLD_ADDRESS=$(jq -r '.world.address' manifest_dev.json)
echo "World address: $WORLD_ADDRESS"
```

### Step 3: Start Torii

**Default mode (asdf-installed torii):**
```bash
torii --world $WORLD_ADDRESS --http.cors_origins "*" &
```

**From source mode** (when user requests "build from source", "use source", or "compile torii"):

Ask the user for the torii source directory path, then run:
```bash
cd <TORII_SOURCE_PATH> && cargo run --release --bin torii -- --world $WORLD_ADDRESS --http.cors_origins "*" &
```

Wait for health check: `curl -s localhost:8080/health`

## Contract Interaction Commands

### Execute Contract Functions

Before executing contract functions, you need to discover available contracts, their functions, and understand the calldata format.

#### Step 1: Discover Available Contracts

```bash
# List all deployed contracts
jq -r '.contracts[].tag' manifest_dev.json

# Get detailed contract info including systems/functions
jq '.contracts[] | {tag, systems}' manifest_dev.json
```

#### Step 2: Find Available Functions

```bash
# List all functions for a specific contract
jq '.contracts[] | select(.tag == "dojo_starter-actions") | .systems' manifest_dev.json
```

#### Step 3: Read Cairo Source for Function Signatures

To understand function parameters, read the Cairo source files:

```bash
# Find system implementations
ls src/systems/

# Read the actions contract to see function signatures
cat src/systems/actions.cairo
```

Example: In `actions.cairo`, you might find:
```cairo
fn spawn(ref self: ContractState) { ... }
fn move(ref self: ContractState, direction: Direction) { ... }
```

#### Step 4: Find Enum/Type Definitions for Calldata

For enum types like `Direction`, check the models file:

```bash
# Read model definitions
cat src/models.cairo
```

Example Direction enum:
```cairo
#[derive(Copy, Drop, Serde, PartialEq, Introspect)]
pub enum Direction {
    None,   // 0
    Left,   // 1
    Right,  // 2
    Up,     // 3
    Down,   // 4
}
```

#### Step 5: Execute Functions

```bash
# Format: sozo execute <namespace>-<contract> <function> [calldata...]

# No arguments
sozo execute dojo_starter-actions spawn

# With enum argument (use numeric value)
sozo execute dojo_starter-actions move -c 1  # Direction::Left
sozo execute dojo_starter-actions move -c 3  # Direction::Up

# With multiple arguments
sozo execute dojo_starter-actions some_func -c 0x123,42,1
```

### Inspect World State

```bash
sozo inspect
```

### Query via GraphQL (Torii)

```bash
curl -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ dojoStarterMovesModels { edges { node { player remaining } } } }"}'
```

### Subscribe to Entities (gRPC)

```bash
grpcurl -plaintext \
  -d '{"clause":{"keys":{"keys":[],"pattern_matching":1,"models":["dojo_starter-Position"]}}}' \
  localhost:50051 world.World/SubscribeEntities
```

## Verification Patterns

### Health Checks

| Service | Command | Expected |
|---------|---------|----------|
| Katana | `curl -s localhost:5050` | JSON-RPC response |
| Torii HTTP | `curl -s localhost:8080/health` | 200 OK |
| Torii gRPC | `grpcurl -plaintext localhost:50051 list` | Service list |

### Verify Entity State

After executing a contract function, verify state changes:

```bash
# Execute spawn
sozo execute dojo_starter-actions spawn

# Check Position model via GraphQL
curl -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ dojoStarterPositionModels { edges { node { player vec { x y } } } } }"}'
```

## Cleanup

### Kill Background Processes

```bash
# Kill katana
pkill -f "katana"

# Kill torii
pkill -f "torii"
```

### Clean Database Files (optional)

```bash
rm -rf torii.db* katana.db*
```

## Quick Start Workflow

Complete workflow for testing:

```bash
# 1. Check prerequisites
asdf current sozo katana torii scarb

# 2. Start katana
katana --dev --dev.no-fee &
sleep 2

# 3. Build and migrate
sozo build && sozo migrate

# 4. Extract world address
WORLD_ADDRESS=$(jq -r '.world.address' manifest_dev.json)

# 5. Start torii
torii --world $WORLD_ADDRESS --http.cors_origins "*" &
sleep 3

# 6. Verify services
curl -s localhost:5050 > /dev/null && echo "Katana: OK"
curl -s localhost:8080/health > /dev/null && echo "Torii: OK"

# 7. Execute test transaction
sozo execute dojo_starter-actions spawn

# 8. Verify state change
curl -s -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ dojoStarterPositionModels { edges { node { player vec { x y } } } } }"}'
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :5050
lsof -i :8080

# Kill by PID
kill -9 <PID>
```

### Migration Fails

```bash
# Clean build artifacts
sozo clean
sozo build
sozo migrate
```

### Torii Not Indexing

Ensure world address matches:
```bash
# Verify world address in manifest
jq -r '.world.address' manifest_dev.json

# Restart torii with correct address
pkill -f torii
torii --world $(jq -r '.world.address' manifest_dev.json) --http.cors_origins "*" &
```
