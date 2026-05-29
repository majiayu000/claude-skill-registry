---
name: duck-time-travel
description: SKILL: Duck Time Travel
source: local
license: UNLICENSED
---

# SKILL: Duck Time Travel

**Version**: 1.0.0
**Created**: 2025-12-21
**Trit**: 0 (ERGODIC - Coordinator)
**Color**: `#26D826` (Green)
**Lineage**: Traced from 745+ threads across November-December 2025

## Canonical Triads

```
clj-kondo-3color (-1) ⊗ duck-time-travel (0) ⊗ rama-gay-clojure (+1) = 0 ✓
acsets (-1) ⊗ duck-time-travel (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Purpose

DuckDB/DuckLake time-travel queries with interaction color tracking. Every thread interaction gets a deterministic color via Gay.jl SplitMix64.

## Thread Lineage Analysis

### Most Expensive Threads (Message Count)

| Thread ID | Title | Messages | Color (seed-derived) |
|-----------|-------|----------|---------------------|
| T-019b24be-1daa | Thread search results for gay and color | 419 | `#a93ec0` |
| T-019b3165-0082 | Prevent Gay.jl regression with subagent branch tracking | 344 | `#7a1036` |
| T-09d1dee8-9a4f | Docker compose dev profile configuration error | 303 | `#babe58` |
| T-7289adbd-f227 | Terminal image protocols and color rendering | 298 | `#6ffe80` |
| T-6b865d09-bfa7 | Count AMP threads using CLI | 246 | `#555f06` |
| T-64c86783-b888 | Investigating vers cli output anomalies | 244 | `#281993` |
| T-c02b8551-348d | Install Vercel CLI without Homebrew | 228 | `#d115c6` |
| T-28328d85-4673 | Connect to Vers VM and check status | 212 | `#8ce2a6` |
| T-b8114b83-2244 | Generate comprehensive color palette | 203 | `#5df760` |
| T-019b381f-8fd5 | Babashka Gemini MCP server with DuckDB extraction | 199 | `#c9f233` |

### Root Thread Lineage (Most Connected)

```
T-019b2211-1dc0 (Root: Gay.jl parallel)
    └─ T-019b2247-cf0d (Fork: Gay.jl parallel #1)
    └─ T-019b2247-c147 (Fork: Gay.jl parallel #2)
    └─ T-019b2247-a952 (Fork: Gay.jl parallel #3)
    └─ T-019b2247-5802 (Fork: Gay.jl concepts)
    └─ T-019b2247-4717 (Fork: Gay.jl patterns)
        └─ T-019b2248-4511 (Interleave forked Gay.jl)
            └─ T-019b2272-7c9b
                └─ T-019b2289-ff42
                    └─ T-019b22ab-3fa4 (Color mining + incentives)
                        └─ T-019b2302-47d2
                            └─ T-019b2364-2e63 (CT-Zulip + GAY)
                                └─ T-019b2374-f1be (DuckDB + Hatchery)
```

## DuckLake Time Travel Syntax

### Query at Specific Snapshot Version
```sql
-- Query table at snapshot version 3
SELECT * FROM tbl AT (VERSION => 3);
```

### Query at Specific Timestamp
```sql
-- Query table as of last week
SELECT * FROM tbl AT (TIMESTAMP => now() - INTERVAL '1 week');

-- Query for November 2025 specifically
SELECT * FROM tbl AT (TIMESTAMP => '2025-11-15 00:00:00');
```

### Attach Database at Historic Point
```sql
-- Attach at specific snapshot version
ATTACH 'ducklake:file.db' (SNAPSHOT_VERSION 3);

-- Attach at specific time
ATTACH 'ducklake:file.db' (SNAPSHOT_TIME '2025-11-30 00:00:00');
```

### List Available Snapshots
```sql
-- Get all snapshots for the database
SELECT * FROM ducklake_snapshot ORDER BY snapshot_id DESC;
```

## Bi-Temporal Schema Pattern

From the Frobenius thread (T-019b3656-55e1):

```sql
CREATE TABLE github_events (
    id VARCHAR PRIMARY KEY,
    type VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL,  -- Business time (when event occurred)
    recorded_at TIMESTAMP NOT NULL DEFAULT current_timestamp,  -- System time
    -- Bi-temporal columns for full history
    valid_from TIMESTAMP NOT NULL DEFAULT current_timestamp,
    valid_to TIMESTAMP DEFAULT 'infinity'::TIMESTAMP
);

-- Time-travel view
CREATE VIEW events_at_time AS
SELECT * FROM github_events
WHERE valid_from <= current_timestamp 
  AND valid_to > current_timestamp;

-- Query state at specific time
CREATE MACRO events_as_of(query_time) AS TABLE
SELECT * FROM github_events
WHERE valid_from <= query_time AND valid_to > query_time;
```

## Interaction Color Tracking

Every DuckDB interaction gets a deterministic color:

```sql
-- Color-tracked interactions table
CREATE TABLE interaction_colors (
    interaction_id VARCHAR PRIMARY KEY,
    thread_id VARCHAR NOT NULL,
    query_text TEXT,
    query_fingerprint BIGINT,  -- FNV-1a hash
    color_seed BIGINT,  -- SplitMix64 seed
    color_hex VARCHAR(7),  -- e.g., '#a93ec0'
    color_trit INTEGER CHECK (color_trit IN (-1, 0, 1)),  -- GF(3)
    executed_at TIMESTAMP DEFAULT current_timestamp
);

-- Function to compute color from seed
-- Uses Gay.jl SplitMix64 algorithm
CREATE MACRO seed_to_hex(seed) AS (
    '#' || printf('%06x', (seed * 0x9e3779b97f4a7c15) % 16777216)
);

-- Track every query
INSERT INTO interaction_colors (interaction_id, thread_id, query_text, query_fingerprint, color_seed, color_hex, color_trit)
VALUES (
    gen_random_uuid(),
    'T-019b43b8-...',
    'SELECT * FROM tbl AT (VERSION => 3)',
    fnv_hash('SELECT * FROM tbl AT (VERSION => 3)'),
    sm64_next(fnv_hash('SELECT * FROM tbl AT (VERSION => 3)')),
    seed_to_hex(sm64_next(fnv_hash(...))),
    sm64_next(...) % 3 - 1  -- GF(3): -1, 0, +1
);
```

## Just Recipes

```just
# Time travel to specific snapshot
duck-at-version db version:
    duckdb {{db}} -c "SELECT * FROM main AT (VERSION => {{version}})"

# Time travel to specific date
duck-at-date db date:
    duckdb {{db}} -c "ATTACH 'ducklake:{{db}}' (SNAPSHOT_TIME '{{date}}')"

# List all snapshots
duck-snapshots db:
    duckdb {{db}} -c "SELECT snapshot_id, snapshot_time FROM ducklake_snapshot ORDER BY snapshot_id DESC"

# November 2025 time travel
duck-nov2025 db:
    duckdb -c "ATTACH 'ducklake:{{db}}' (SNAPSHOT_TIME '2025-11-30 23:59:59'); SELECT * FROM main LIMIT 10"

# Track interaction colors
duck-color-track db query:
    duckdb {{db}} -c "INSERT INTO interaction_colors ..."
```

## GF(3) Conservation

All interactions are tracked with ternary phase:

| Phase | Trit | Description | Color Range |
|-------|------|-------------|-------------|
| MINUS | -1 | Contraction queries (DELETE, DROP) | Cold (180°-300°) |
| ERGODIC | 0 | Read queries (SELECT) | Neutral (60°-180°) |
| PLUS | +1 | Expansion queries (INSERT, CREATE) | Warm (300°-60°) |

**Invariant**: Sum of trits across any triplet of interactions = 0 mod 3

## Files

- [db/migrations/001_crdt_memoization.sql](file:///Users/bob/ies/music-topos/db/migrations/001_crdt_memoization.sql) - CRDT time-travel schema
- [db/thread_operad_schema.sql](file:///Users/bob/ies/music-topos/db/thread_operad_schema.sql) - Thread operad with color streams
- [lib/gay.hy](file:///Users/bob/ies/music-topos/lib/gay.hy) - Hy implementation of SPI colors

## Related Skills

- `discohy-streams` - DisCoPy categorical color streams
- `gay-mcp` - Gay.jl MCP server integration
- `acsets-algebraic-databases` - ACSets for DuckDB schemas
