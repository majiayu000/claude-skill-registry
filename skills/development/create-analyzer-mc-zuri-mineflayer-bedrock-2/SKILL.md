---
name: create-analyzer
description: Create a new packet analyzer for Minecraft Bedrock logs. Generates template code, provides documentation links, and guides testing workflow.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Create Minecraft Bedrock Packet Analyzer

Generate a new domain-specific packet analyzer for analyzing captured Bedrock packets.

## Quick Start

1. **Identify the domain**: inventory, movement, entities, chat, blocks, etc.
2. **Find relevant packets**: Search `protocol.d.ts` for packet types
3. **Generate analyzer file** using template below
4. **Export from index.ts**
5. **Test with captured logs**

## Analyzer Template

Create file at: `packages/minecraft-logs-analyzers/src/analyzers/{domain}.ts`

```typescript
import { BaseAnalyzer } from "../base-analyzer.ts";
import type { Direction, LogEntry, AnalyzerConfig } from "../types.ts";

const PACKETS_TO_LOG = [
  // Add packet names from protocol.d.ts
];

/**
 * Analyzer for {domain}-related packets.
 */
export class {Domain}Analyzer extends BaseAnalyzer {
  readonly config: AnalyzerConfig = {
    name: "{domain}",
    packets: PACKETS_TO_LOG,
  };

  constructor(basePath: string, registry?: any) {
    super(basePath);
    if (registry) this.registry = registry;
    this.init();
  }

  protected extractFields(
    direction: Direction,
    name: string,
    packet: any
  ): LogEntry | null {
    const base = this.createBaseEntry(direction, name);

    switch (name) {
      // Add case for each packet type
      // case "packet_name":
      //   return { ...base, field: packet.field };

      default:
        return null;
    }
  }
}
```

## Registration

Add export to `packages/minecraft-logs-analyzers/src/index.ts`:

```typescript
export { {Domain}Analyzer } from "./analyzers/{domain}.ts";
```

## Documentation Locations

| Resource | Location |
|----------|----------|
| Protocol types | `packages/mineflayer-bedrock/src/protocol.d.ts` |
| Existing analyzers | `packages/minecraft-logs-analyzers/src/analyzers/` |
| Base class | `packages/minecraft-logs-analyzers/src/base-analyzer.ts` |
| Types | `packages/minecraft-logs-analyzers/src/types.ts` |
| Bedrock plugins | `packages/mineflayer/lib/bedrockPlugins/` |

## Finding Relevant Packets

```bash
# Search protocol.d.ts for packet types
grep -n "packet_" packages/mineflayer-bedrock/src/protocol.d.ts | head -50

# Find packets used by a specific plugin
grep -n "client.on" packages/mineflayer/lib/bedrockPlugins/*.mts

# Search for specific packet handling
grep -rn "move_player" packages/mineflayer/lib/bedrockPlugins/
```

## Common Packet Domains

| Domain | Key Packets |
|--------|-------------|
| Inventory | `inventory_slot`, `inventory_content`, `inventory_transaction`, `item_stack_request`, `item_stack_response`, `mob_equipment` |
| Movement | `player_auth_input`, `move_player`, `set_actor_motion`, `move_actor_absolute`, `move_actor_delta` |
| Entities | `add_entity`, `remove_entity`, `set_entity_data`, `set_entity_motion`, `add_player` |
| Chat | `text`, `command_request`, `command_output` |
| Blocks | `update_block`, `block_event`, `level_event`, `update_sub_chunk_blocks` |
| Combat | `actor_event`, `hurt_armor`, `entity_fall`, `animate` |
| World | `level_chunk`, `sub_chunk`, `network_chunk_publisher_update` |

## Testing Workflow

### 1. Capture Packets from Real Client

**Critical**: Always capture from the real Minecraft client first to understand the exact packet format.

```bash
# Start capture proxy
npm run start --workspace=minecraft-logs-recorder -- -o ./test-logs

# Connect Minecraft Bedrock to localhost:19150
# Perform the exact action you want to implement (crafting, chest interaction, etc.)
# Disconnect to save logs
```

The `.jsonl` file contains processed packets, `.bin` contains raw data for replay.

### 2. Analyze Captured Logs

```bash
# View first 20 packets
head -20 test-logs/*.jsonl

# Count packets by type
grep -o '"p":"[^"]*"' test-logs/*.jsonl | sort | uniq -c | sort -rn

# Find specific packets
grep '"p":"move_player"' test-logs/*.jsonl | head -5
```

### 3. Test Your Analyzer

```typescript
import { {Domain}Analyzer } from 'minecraft-logs-analyzers';
import { createReplayClient } from 'minecraft-logs-recorder/replay';

// Attach analyzer to replay client
const analyzer = new {Domain}Analyzer('test-output/replay');
const client = createReplayClient('test-logs/1.21.130-*.bin');

// Analyzer will log packets to test-output/replay-{domain}.jsonl
analyzer.attachToBot(client);

// Check output
// cat test-output/replay-{domain}.jsonl
```

### 4. Verify Output Format

```bash
# View analyzer output
cat test-output/replay-{domain}.jsonl | head -10

# Validate JSON
cat test-output/replay-{domain}.jsonl | jq -c '.' | head -10
```

## BaseAnalyzer Methods

| Method | Description |
|--------|-------------|
| `createBaseEntry(direction, name)` | Create log entry with t, tick, d, p fields |
| `updateTick(packet)` | Extract tick from packet.tick |
| `itemName(item)` | Resolve item name from network_id |
| `writeEntry(entry)` | Write entry to JSONL file |
| `message(msg, data?)` | Log custom debug message |

## Override Points

| Method | When to Override |
|--------|------------------|
| `shouldLog(name, packet)` | Custom filtering (e.g., only log non-empty actions) |
| `extractFields(direction, name, packet)` | Required - extract relevant fields |

## IMPORTANT: Start with Full Packets

**Always log full packet data initially**, not filtered/summarized data. This was critical for solving crafting implementation:

```typescript
// BAD: Filtering too early loses critical details
protected shouldLog(name: string, packet: unknown): boolean {
  // Only log if it has crafting containers...  ❌
  return hasCraftingContainer;
}

// GOOD: Log everything first, filter later
protected shouldLog(name: string, packet: unknown): boolean {
  return true;  // ✅ See all packets first
}

// GOOD: Return full packet data in extractFields
return {
  ...base,
  responses: p.responses,  // ✅ Full data, not summarized
};
```

Real client packet captures revealed crucial details that were being filtered out:
- `craft_recipe_auto` uses `hotbar_and_inventory` container, not `crafting_input`
- `results_deprecated` action requires `result_items` array with full item data
- Stack IDs use negative request_id for chained actions
- `place` goes directly to inventory, not through cursor

**Only add filtering after you fully understand the protocol.**

## Example: Movement Analyzer

```typescript
import { BaseAnalyzer } from "../base-analyzer.ts";
import type { Direction, LogEntry, AnalyzerConfig } from "../types.ts";

const PACKETS_TO_LOG = [
  "player_auth_input",
  "move_player",
  "set_actor_motion",
];

export class MovementAnalyzer extends BaseAnalyzer {
  readonly config: AnalyzerConfig = {
    name: "movement",
    packets: PACKETS_TO_LOG,
  };

  constructor(basePath: string) {
    super(basePath);
    this.init();
  }

  protected extractFields(
    direction: Direction,
    name: string,
    packet: any
  ): LogEntry | null {
    const base = this.createBaseEntry(direction, name);

    switch (name) {
      case "player_auth_input":
        this.updateTick(packet);
        return {
          ...base,
          tick: packet.tick,
          pos: [packet.position?.x, packet.position?.y, packet.position?.z],
          yaw: packet.yaw,
          pitch: packet.pitch,
        };

      case "move_player":
        return {
          ...base,
          pos: [packet.position?.x, packet.position?.y, packet.position?.z],
          mode: packet.mode,
          onGround: packet.on_ground,
        };

      case "set_actor_motion":
        return {
          ...base,
          entityId: packet.runtime_entity_id,
          velocity: [packet.velocity?.x, packet.velocity?.y, packet.velocity?.z],
        };

      default:
        return null;
    }
  }
}
```