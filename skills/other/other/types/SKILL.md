---
name: types
description: Reference for Splitrail's core data types. Use when working with ConversationMessage, Stats, DailyStats, or other type definitions.
---

# Key Types

Read `src/types.rs` for full definitions.

## Core Types

- **ConversationMessage** - Normalized message format across all analyzers. Contains application source, timestamp, hashes for deduplication, model info, token/cost stats, and role.

- **Stats** - Comprehensive usage metrics for a single message including token counts, costs, file operations, todo tracking, and composition stats by file type.

- **DailyStats** - Pre-aggregated stats per date with message counts, conversation counts, model breakdown, and embedded Stats.

- **Application** - Enum identifying which AI coding tool a message came from.

- **MessageRole** - User or Assistant.

## Hashing Strategy

- `local_hash`: Deduplication within a single analyzer
- `global_hash`: Deduplication on upload to Splitrail Cloud

## Aggregation

Use `crate::utils::aggregate_by_date()` to group messages into daily stats. See `src/utils.rs`.
