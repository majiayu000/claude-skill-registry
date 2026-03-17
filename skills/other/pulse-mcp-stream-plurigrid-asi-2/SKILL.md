---
name: pulse-mcp-stream
description: "Layer 1 Real-Time Social Stream Monitoring via MCP with DuckDB persistence"
---

# pulse-mcp-stream

> Layer 1: Real-Time Social Stream Monitoring via MCP

**Version**: 1.1.0 (music-topos enhanced)
**Trit**: +1 (Generator - produces live data)
**Bundle**: acquisition

## Overview

Pulse-MCP-stream provides real-time monitoring of social interactions, enabling the cognitive surrogate system to stay updated with the latest patterns. It streams mentions, engagement changes, and trending topics.

## Enhanced Integration: MCP + DuckDB

### MCP Server (TypeScript)

```typescript
// pulse-mcp-server/src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server";
import { Firehose } from "@atproto/sync";
import * as duckdb from "duckdb";

const server = new Server({
  name: "pulse-mcp-stream",
  version: "1.0.0"
});

// Connect to DuckDB for persistence
const db = new duckdb.Database("pulse_stream.duckdb");

server.setRequestHandler("subscribe", async (params) => {
  const { actor, filters } = params;
  
  const firehose = new Firehose({
    service: "wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos"
  });
  
  firehose.on("create", async (event) => {
    if (event.author === actor) {
      // Store in DuckDB
      await db.run(`
        INSERT INTO pulse_events (event_id, event_type, actor_did, text, created_at)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
      `, [event.uri, event.type, event.author, event.record?.text]);
    }
  });
  
  await firehose.start();
  return { status: "subscribed", actor };
});
```

### DuckDB Schema

```sql
CREATE TABLE pulse_events (
    event_id VARCHAR PRIMARY KEY,
    event_type VARCHAR,  -- 'post', 'reply', 'like', 'repost', 'mention'
    actor_did VARCHAR,
    actor_handle VARCHAR,
    subject_uri VARCHAR,
    text TEXT,
    created_at TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    gay_color VARCHAR  -- Deterministic color via SPI seed
);

CREATE TABLE engagement_deltas (
    delta_id VARCHAR PRIMARY KEY,
    post_uri VARCHAR,
    likes_delta INT,
    reposts_delta INT,
    replies_delta INT,
    velocity FLOAT,  -- engagements per minute
    measured_at TIMESTAMP
);

-- Real-time velocity tracking
CREATE VIEW v_post_velocity AS
SELECT 
    post_uri,
    COUNT(*) FILTER (WHERE event_type = 'like') as likes,
    COUNT(*) FILTER (WHERE event_type = 'repost') as reposts,
    COUNT(*) / (EXTRACT(EPOCH FROM (MAX(created_at) - MIN(created_at))) / 60.0) as velocity_per_min
FROM pulse_events
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY post_uri;
```

### Python Client

```python
# pulse_client.py
import asyncio
import duckdb
from dataclasses import dataclass
from typing import AsyncIterator

@dataclass
class PulseEvent:
    event_id: str
    event_type: str
    actor: str
    text: str
    created_at: str

class PulseClient:
    def __init__(self, db_path: str = "pulse_stream.duckdb", seed: int = 0xf061ebbc2ca74d78):
        self.db = duckdb.connect(db_path)
        self.seed = seed
    
    async def subscribe_actor(self, actor: str) -> AsyncIterator[PulseEvent]:
        """Subscribe to real-time updates for a user."""
        # Poll DuckDB for new events
        last_id = ""
        while True:
            result = self.db.execute("""
                SELECT * FROM pulse_events 
                WHERE actor_handle = ? AND event_id > ?
                ORDER BY created_at
                LIMIT 10
            """, [actor, last_id]).fetchall()
            
            for row in result:
                last_id = row[0]
                yield PulseEvent(*row[:5])
            
            await asyncio.sleep(1)
    
    async def detect_trends(self, center_user: str, window_minutes: int = 60):
        """Detect trending topics in user's network."""
        return self.db.execute("""
            WITH word_counts AS (
                SELECT 
                    UNNEST(STRING_SPLIT(LOWER(text), ' ')) as word,
                    COUNT(*) as mentions
                FROM pulse_events
                WHERE created_at > NOW() - INTERVAL ? MINUTE
                GROUP BY word
            )
            SELECT word, mentions
            FROM word_counts
            WHERE LENGTH(word) > 3
            ORDER BY mentions DESC
            LIMIT 10
        """, [window_minutes]).fetchall()
```

### Ruby Integration

```ruby
# lib/pulse_stream.rb
require 'duckdb'

module PulseStream
  def self.connect(db_path: "pulse_stream.duckdb")
    @db = DuckDB::Database.open(db_path)
    @conn = @db.connect
  end
  
  def self.latest_events(actor:, limit: 10)
    @conn.query(<<~SQL, actor, limit)
      SELECT event_id, event_type, text, created_at
      FROM pulse_events
      WHERE actor_handle = ?
      ORDER BY created_at DESC
      LIMIT ?
    SQL
  end
  
  def self.velocity(post_uri:)
    result = @conn.query(<<~SQL, post_uri)
      SELECT velocity_per_min FROM v_post_velocity WHERE post_uri = ?
    SQL
    result.first&.first || 0.0
  end
  
  def self.viral?(post_uri:, threshold: 5.0)
    velocity(post_uri: post_uri) > threshold
  end
end
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | influence-propagation | Validates network patterns |
| 0 | bisimulation-game | Coordinates equivalence |
| +1 | **pulse-mcp-stream** | Generates live data |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## MCP Configuration

```json
{
  "mcpServers": {
    "pulse": {
      "command": "node",
      "args": ["pulse-mcp-server/dist/index.js"],
      "env": {
        "DUCKDB_PATH": "pulse_stream.duckdb",
        "GAY_SEED": "0xf061ebbc2ca74d78"
      }
    }
  }
}
```

## Justfile Recipes

```makefile
# Start pulse stream
pulse-start actor="barton.bsky.social":
    python3 -c "import asyncio; from pulse_client import PulseClient; asyncio.run(PulseClient().subscribe_actor('{{actor}}'))"

# Check velocity
pulse-velocity uri:
    ruby -I lib -r pulse_stream -e "PulseStream.connect; puts PulseStream.velocity(post_uri: '{{uri}}')"

# Detect trends
pulse-trends window="60":
    duckdb pulse_stream.duckdb -c "SELECT * FROM v_post_velocity WHERE velocity_per_min > 1.0 LIMIT 10"
```

## Related Skills

- `atproto-ingest` (Layer 1) - Batch data collection
- `influence-propagation` (Layer 7) - Network analysis
- `cognitive-surrogate` (Layer 6) - Pattern consumption
- `duckdb-temporal-versioning` - Time-travel queries
