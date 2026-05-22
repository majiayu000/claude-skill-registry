---
name: bluesky-jetstream
description: Bluesky Jetstream Firehose Skill
version: 1.0.0
---

# Bluesky Jetstream Firehose Skill

**GF(3) Trit**: -1 (MINUS - validator/filter on incoming data stream)
**Role**: Constrain and validate Bluesky firehose events before processing

## Overview

Jetstream is Bluesky's simplified JSON firehose - a WebSocket streaming API that provides real-time access to all public activity on the Bluesky network. Unlike the full atproto firehose (which uses CBOR/CAR binary encoding), Jetstream delivers plain JSON, making it accessible for rapid prototyping.

**Endpoints**:
- Primary: `wss://jetstream2.us-east.bsky.network/subscribe`
- Backup: `wss://jetstream1.us-west.bsky.network/subscribe`

**Source**: [github.com/bluesky-social/jetstream](https://github.com/bluesky-social/jetstream)

## Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `wantedCollections` | string[] | Filter by NSID (repeatable) |
| `wantedDids` | string[] | Filter by specific DIDs (repeatable) |
| `compress` | boolean | Enable zstd compression |
| `cursor` | integer | Resume from timestamp (microseconds since epoch) |

Example URL:
```
wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post&wantedCollections=app.bsky.feed.like
```

## Message Types

### commit
Repository commit events (most common):
```json
{
  "did": "did:plc:abc123...",
  "time_us": 1703123456789012,
  "kind": "commit",
  "commit": {
    "rev": "3k...",
    "operation": "create",
    "collection": "app.bsky.feed.post",
    "rkey": "3k...",
    "record": {
      "$type": "app.bsky.feed.post",
      "text": "Hello world!",
      "createdAt": "2024-12-21T10:00:00.000Z"
    },
    "cid": "bafyrei..."
  }
}
```

### identity
Identity updates:
```json
{
  "did": "did:plc:abc123...",
  "time_us": 1703123456789012,
  "kind": "identity",
  "identity": {
    "did": "did:plc:abc123...",
    "handle": "alice.bsky.social",
    "seq": 12345
  }
}
```

### account
Account status changes:
```json
{
  "did": "did:plc:abc123...",
  "time_us": 1703123456789012,
  "kind": "account",
  "account": {
    "active": true,
    "did": "did:plc:abc123...",
    "seq": 12345
  }
}
```

## Collection NSIDs

| NSID | Description |
|------|-------------|
| `app.bsky.feed.post` | Posts/skeets |
| `app.bsky.feed.like` | Likes |
| `app.bsky.feed.repost` | Reposts |
| `app.bsky.graph.follow` | Follows |
| `app.bsky.graph.block` | Blocks |
| `app.bsky.graph.list` | Lists |
| `app.bsky.graph.listitem` | List memberships |
| `app.bsky.actor.profile` | Profile updates |
| `app.bsky.feed.threadgate` | Thread gates |
| `app.bsky.feed.postgate` | Post gates |

## JavaScript Example

```javascript
const ws = new WebSocket(
  'wss://jetstream2.us-east.bsky.network/subscribe?' +
  'wantedCollections=app.bsky.feed.post'
);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.kind === 'commit' && data.commit.operation === 'create') {
    console.log(`[${data.did}]: ${data.commit.record.text}`);
  }
};
```

## Babashka/Clojure Example

```clojure
(ns bluesky.jetstream
  (:require [clojure.data.json :as json]
            [org.httpkit.client :as http]))

(def GAMMA 0x9E3779B9)

(defn splitmix32 [x]
  (let [z (bit-and (+ x GAMMA) 0xFFFFFFFF)
        z (bit-and (* (bit-xor z (unsigned-bit-shift-right z 15)) 0x85EBCA6B) 0xFFFFFFFF)
        z (bit-and (* (bit-xor z (unsigned-bit-shift-right z 13)) 0xC2B2AE35) 0xFFFFFFFF)]
    (bit-xor z (unsigned-bit-shift-right z 16))))

(defn cid->trit [cid]
  (let [hash (reduce #(bit-xor (unchecked-multiply %1 31) (int %2)) 0 cid)
        hue (mod (splitmix32 hash) 360)]
    (cond
      (or (< hue 60) (>= hue 300)) +1   ; PLUS (warm)
      (< hue 180) 0                      ; ERGODIC (neutral)
      :else -1)))                        ; MINUS (cold)

(defn process-event [event]
  (when (and (= (:kind event) "commit")
             (= (get-in event [:commit :operation]) "create"))
    (let [cid (get-in event [:commit :cid])
          text (get-in event [:commit :record :text])
          trit (cid->trit cid)]
      {:did (:did event)
       :text text
       :cid cid
       :trit trit
       :trit-label (case trit 1 "PLUS" 0 "ERGODIC" -1 "MINUS")})))
```

## Integration with Agent-o-rama

### Memory Substrate Connection

```clojure
;; Feed Jetstream events into memory substrate
(defn ingest-to-substrate [event memory-client]
  (when-let [processed (process-event event)]
    ;; Compress into control artifact
    (compress-trace memory-client
      [{:role :user 
        :content (format "Bluesky post from %s: %s" 
                         (:did processed) (:text processed))}]
      {:tags ["bluesky" (:trit-label processed)]
       :source "jetstream"
       :cid (:cid processed)})))
```

### Decay Tracking

Posts from Jetstream get the same decay epistemology:
- **Half-life**: 10 hours (HALF_LIFE_MS = 36000000)
- **Renewal**: User engagement (likes, replies) renews the artifact
- **Expiration**: Unrenewed posts decay to trit=0 (neutral)

### GF(3) Conservation

Each ingested post gets a trit assignment based on CID hash:
```
Σ(post trits) ≡ 0 (mod 3)
```

Over large samples, the distribution naturally balances due to SplitMix64's uniform properties.

## Rate Limits & Best Practices

1. **Use cursor for resumption**: Store `time_us` to resume after disconnect
2. **Exponential backoff**: 1s → 2s → 4s → ... → 60s max on reconnect
3. **Filter collections**: Request only what you need
4. **Handle compression**: Use zstd for bandwidth savings at scale
5. **Monitor lag**: Compare `time_us` to wall clock for lag detection

## DuckDB Schema

```sql
CREATE TABLE IF NOT EXISTS bluesky_firehose (
  seq_id BIGINT PRIMARY KEY,
  did VARCHAR NOT NULL,
  collection VARCHAR NOT NULL,
  rkey VARCHAR,
  cid VARCHAR,
  operation VARCHAR,  -- create | update | delete
  record_json JSON,
  text VARCHAR,
  created_at TIMESTAMP,
  trit INTEGER,       -- -1, 0, +1
  color_hex VARCHAR,  -- Gay.jl deterministic color
  cursor_us BIGINT,   -- For resumption
  ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_did (did),
  INDEX idx_collection (collection),
  INDEX idx_trit (trit),
  INDEX idx_cursor (cursor_us)
);

-- View for GF(3) balance check
CREATE VIEW bluesky_gf3_balance AS
SELECT 
  DATE_TRUNC('hour', ingested_at) as hour,
  SUM(trit) as trit_sum,
  MOD(SUM(trit), 3) as gf3_remainder,
  COUNT(*) as event_count
FROM bluesky_firehose
GROUP BY 1
ORDER BY 1 DESC;
```

## Savitch Connection

The triadic processing of Jetstream events mirrors Savitch's reachability algorithm:

```
NSPACE(S(n)) ⊆ DSPACE(S(n)²)

Firehose Event Processing:
├── MINUS (-1): Validate/filter incoming event
├── ERGODIC (0): Route to appropriate handler  
└── PLUS (+1): Generate processed artifact

Each branch: O(S(n)) space
Recursion depth: O(log n) for branching decisions
Total: O(S(n)²) deterministic space simulating nondeterministic choices
```

## Commands

```bash
# Start Babashka consumer
bb scripts/bluesky_jetstream.clj --collections app.bsky.feed.post --limit 1000

# Open HTML viewer
open scripts/bluesky_viewer.html

# Query stored events
duckdb ~/.topos/ducklake.duckdb "SELECT * FROM bluesky_firehose ORDER BY cursor_us DESC LIMIT 10"

# Check GF(3) balance
duckdb ~/.topos/ducklake.duckdb "SELECT * FROM bluesky_gf3_balance LIMIT 24"
```

## Related Skills

- `duckdb-temporal-versioning` (+1): Store firehose with time-travel
- `gay-mcp` (+1): Deterministic coloring for CIDs
- `memory-substrate` (0): Ingest into Agent-o-rama memory

## References

- [Jetstream Documentation](https://docs.bsky.app/blog/jetstream)
- [Jetstream Source Code](https://github.com/bluesky-social/jetstream)
- [ATProto Specification](https://atproto.com/specs/atp)
- [Jazco Blog: Jetstream Design](https://jazco.dev/2024/09/24/jetstream/)

---

**Skill Name**: bluesky-jetstream
**Type**: Real-time data stream consumer
**Trit**: -1 (MINUS - validator/filter)
**GF(3) Triad**: bluesky-jetstream (-1) ⊗ duckdb-temporal (0) ⊗ gay-mcp (+1) = 0 ✓



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.