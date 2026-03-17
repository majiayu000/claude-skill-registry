---
name: fswatch-duckdb
description: FileSystemWatcher over /tmp with DuckDB/DuckLake persistence. Auto-starts on Amp sessions for resilient file monitoring with temporal queries.
version: 1.0.0
---


# FileSystemWatcher + DuckDB Skill

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - coordination/observation)
**Principle**: Observe filesystem changes, persist to DuckDB, query temporally
**GF(3) Balanced Triad**:
- fswatch-duckdb (0) [Coordinator: Watch/observe]
- duckdb-temporal-versioning (+1) [Generator: Store events]
- clj-kondo-3color (-1) [Validator: Verify integrity]

---

## Overview

Resilient filesystem monitoring with:
1. **fswatch** or **watchman** for native file events
2. **DuckDB** for persistent event storage with time-travel
3. **DuckLake** patterns for partitioned, versioned storage
4. **Auto-start** on every Amp session

## Auto-Initialization (MANDATORY)

On every Amp session start, run:

```bash
# Initialize watcher database
duckdb ~/.agents/fswatch.duckdb <<'SQL'
CREATE TABLE IF NOT EXISTS fs_events (
  id INTEGER PRIMARY KEY,
  path VARCHAR NOT NULL,
  event_type VARCHAR NOT NULL,  -- 'created', 'modified', 'deleted', 'renamed'
  old_path VARCHAR,             -- for renames
  size BIGINT,
  mtime TIMESTAMP,
  checksum VARCHAR,             -- md5 for dedup
  session_id VARCHAR,           -- Amp thread ID
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  trit INTEGER DEFAULT 0        -- GF(3) color
);

CREATE INDEX IF NOT EXISTS idx_fs_events_path ON fs_events(path);
CREATE INDEX IF NOT EXISTS idx_fs_events_session ON fs_events(session_id);
CREATE INDEX IF NOT EXISTS idx_fs_events_time ON fs_events(created_at);
SQL
```

## Watch /tmp with fswatch

### Start Watcher (Background Daemon)

```bash
# Using fswatch (macOS/Linux)
fswatch -0 -r /tmp | while IFS= read -r -d '' path; do
  event_type="modified"
  if [ ! -e "$path" ]; then
    event_type="deleted"
  elif [ ! -s "$path.prev" 2>/dev/null ]; then
    event_type="created"
  fi
  
  size=$(stat -f%z "$path" 2>/dev/null || echo 0)
  mtime=$(stat -f%m "$path" 2>/dev/null || date +%s)
  checksum=$(md5 -q "$path" 2>/dev/null || echo "")
  
  duckdb ~/.agents/fswatch.duckdb \
    "INSERT INTO fs_events (path, event_type, size, mtime, checksum, session_id) 
     VALUES ('$path', '$event_type', $size, to_timestamp($mtime), '$checksum', '$AMP_THREAD_ID')"
done &
```

### Babashka Watcher (Recommended)

```clojure
#!/usr/bin/env bb
;; scripts/fswatch-daemon.bb

(require '[babashka.process :refer [shell process]]
         '[babashka.fs :as fs]
         '[clojure.java.io :as io])

(def db-path (str (System/getenv "HOME") "/.agents/fswatch.duckdb"))
(def watch-paths ["/tmp" "/var/tmp"])
(def session-id (or (System/getenv "AMP_THREAD_ID") (str (random-uuid))))

(defn record-event! [path event-type]
  (let [size (if (fs/exists? path) (fs/size path) 0)
        mtime (if (fs/exists? path) 
                (-> path fs/last-modified-time str) 
                "1970-01-01")
        checksum (when (and (fs/exists? path) (fs/regular-file? path))
                   (-> (shell {:out :string} "md5" "-q" path) :out str/trim))]
    (shell "duckdb" db-path
           (format "INSERT INTO fs_events (path, event_type, size, checksum, session_id) 
                    VALUES ('%s', '%s', %d, '%s', '%s')"
                   path event-type size (or checksum "") session-id))))

(defn watch-loop []
  (let [proc (process {:out :stream} 
                      "fswatch" "-0" "-r" (first watch-paths))]
    (with-open [rdr (io/reader (:out proc))]
      (loop []
        (when-let [line (.readLine rdr)]
          (let [path (str/trim line)
                event-type (cond
                             (not (fs/exists? path)) "deleted"
                             :else "modified")]
            (record-event! path event-type))
          (recur))))))

(println "🔍 Starting FileSystemWatcher for" watch-paths)
(println "📊 Persisting to" db-path)
(println "🧵 Session:" session-id)
(watch-loop)
```

## DuckLake Partitioning

For high-volume /tmp monitoring, partition by hour:

```sql
-- Create partitioned view
CREATE VIEW fs_events_hourly AS
SELECT 
  date_trunc('hour', created_at) as hour_bucket,
  path,
  event_type,
  size,
  checksum,
  session_id
FROM fs_events;

-- Export to DuckLake-style Parquet partitions
COPY (
  SELECT * FROM fs_events 
  WHERE created_at >= CURRENT_DATE
) TO '/tmp/ducklake/fs_events' 
(FORMAT PARQUET, PARTITION_BY (date_trunc('day', created_at)));
```

### DuckLake Catalog Integration

```sql
-- Attach DuckLake catalog (if available)
ATTACH 'ducklake:fswatch' AS lake (DATA_PATH '/tmp/ducklake/data');

-- Sync local events to lake
INSERT INTO lake.fs_events 
SELECT * FROM fs_events 
WHERE session_id = current_session();
```

## Queries for Resilience

### Recent Events (Last Hour)

```sql
SELECT path, event_type, size, created_at
FROM fs_events
WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '1 hour'
ORDER BY created_at DESC
LIMIT 50;
```

### Events by Session (Cross-Amp Thread)

```sql
SELECT session_id, COUNT(*) as event_count, 
       MIN(created_at) as first_event,
       MAX(created_at) as last_event
FROM fs_events
GROUP BY session_id
ORDER BY first_event DESC;
```

### Find Duplicates by Checksum

```sql
SELECT checksum, COUNT(*) as copies, 
       array_agg(path) as paths
FROM fs_events
WHERE checksum IS NOT NULL AND checksum != ''
GROUP BY checksum
HAVING COUNT(*) > 1;
```

### Time-Travel Query

```sql
-- What was in /tmp at a specific time?
SELECT * FROM fs_events
WHERE created_at <= '2025-12-24 10:00:00'
  AND path LIKE '/tmp/%'
  AND event_type != 'deleted'
ORDER BY created_at DESC;
```

## Session Persistence

### Save Session State on Exit

```bash
# Add to ~/.zshrc or shell profile
fswatch_save_session() {
  if [ -n "$AMP_THREAD_ID" ]; then
    duckdb ~/.agents/fswatch.duckdb \
      "UPDATE fs_events SET trit = 1 WHERE session_id = '$AMP_THREAD_ID'"
  fi
}
trap fswatch_save_session EXIT
```

### Restore Previous Session Context

```sql
-- Get context from previous session
SELECT DISTINCT path, event_type, MAX(created_at) as last_event
FROM fs_events
WHERE session_id = (
  SELECT session_id FROM fs_events 
  WHERE session_id != current_setting('amp.session_id')
  ORDER BY created_at DESC LIMIT 1
)
GROUP BY path, event_type;
```

## GF(3) Trifurcated Monitoring

For Copy-on-Interact resilience, spawn 3 watchers:

```clojure
;; Trifurcated watcher pattern
(defn trifurcated-watch [paths]
  (let [minus  (future (watch-with-trit paths -1))   ; Validate/filter
        ergodic (future (watch-with-trit paths 0))   ; Coordinate/aggregate
        plus   (future (watch-with-trit paths +1))]  ; Generate/store
    ;; GF(3) sum: -1 + 0 + 1 = 0 ✓
    {:validators @minus
     :coordinators @ergodic
     :generators @plus}))
```

## Integration with Amp

### Auto-Start on Thread Creation

Add to `~/.agents/AGENTS.md`:

```markdown
## FileSystemWatcher Auto-Start

On every session, run:
```bash
bb ~/.agents/skills/fswatch-duckdb/scripts/fswatch-daemon.bb &
```

Query recent activity:
```bash
duckdb ~/.agents/fswatch.duckdb "SELECT * FROM fs_events ORDER BY created_at DESC LIMIT 20"
```
```

### Justfile Commands

```just
# Start filesystem watcher daemon
fswatch-start:
  bb ~/.agents/skills/fswatch-duckdb/scripts/fswatch-daemon.bb &

# Stop all watchers
fswatch-stop:
  pkill -f fswatch-daemon

# Query recent events
fswatch-recent count="20":
  duckdb ~/.agents/fswatch.duckdb \
    "SELECT path, event_type, size, created_at FROM fs_events ORDER BY created_at DESC LIMIT {{count}}"

# Export to DuckLake
fswatch-export:
  duckdb ~/.agents/fswatch.duckdb \
    "COPY fs_events TO '/tmp/ducklake/fs_events.parquet' (FORMAT PARQUET)"

# Database stats
fswatch-stats:
  duckdb ~/.agents/fswatch.duckdb \
    "SELECT COUNT(*) as total_events, COUNT(DISTINCT path) as unique_paths, COUNT(DISTINCT session_id) as sessions FROM fs_events"
```

## Surrounding File Context

When interacting with files, query related events:

```sql
-- Find all events for files in same directory
SELECT * FROM fs_events
WHERE path LIKE (
  SELECT dirname(path) || '%' 
  FROM fs_events 
  WHERE path = '/tmp/myfile.txt'
)
ORDER BY created_at DESC;
```

## Cleanup & Maintenance

```sql
-- Archive old events (older than 7 days)
COPY (
  SELECT * FROM fs_events 
  WHERE created_at < CURRENT_DATE - INTERVAL '7 days'
) TO '/tmp/ducklake/archive/fs_events_archive.parquet';

-- Delete archived events
DELETE FROM fs_events 
WHERE created_at < CURRENT_DATE - INTERVAL '7 days';

-- Vacuum database
VACUUM;
```

## QuickTime Recording Auto-Processor

Automatically processes screen recordings with triadic skill interleaving:

```bash
# Process single recording
bb ~/.agents/skills/fswatch-duckdb/scripts/quicktime-processor.bb ~/Desktop/recording.mov

# Watch mode (auto-process new recordings)
bb ~/.agents/skills/fswatch-duckdb/scripts/quicktime-processor.bb &
```

### Triadic Processing Pipeline

| Stream | Trit | Skill | Voice Persona |
|--------|------|-------|---------------|
| MINUS | -1 | Frame extraction | Anna (Emmy Noether) |
| ERGODIC | 0 | Thumbnail generation | Amélie (Sophie Germain) |
| PLUS | +1 | Audio extraction | Ava (Premium) |

### DuckLake Integration

Outputs stored in `/tmp/ducklake/`:
- `frames/` - Extracted video frames
- `recordings/` - Thumbnails
- `audio/` - Extracted audio tracks

### Interaction Entropy Coloring

Each recording gets a deterministic color based on its path entropy:
```clojure
(def entropy (interaction-entropy path))
(def color (gen-color entropy 0))
;; color includes {:L :C :H :trit :seed}
```

### Query Processed Recordings

```sql
-- Recent recordings
SELECT * FROM recording_processing ORDER BY processed_at DESC LIMIT 10;

-- Skill interleaving log
SELECT * FROM skill_interleave WHERE triplet_id = 0;

-- By trit color
SELECT input_path, trit, frame_count FROM recording_processing WHERE trit = -1;
```

---

**Skill Name**: fswatch-duckdb
**Type**: FileSystem Observer with Temporal Storage + Video Processing
**Trit**: 0 (ERGODIC - coordination)
**GF(3)**: Balanced with duckdb-temporal-versioning (+1) + clj-kondo-3color (-1)
**Auto-Start**: Yes - runs daemon on every Amp session
**Watch Paths**: /tmp, ~/Desktop, ~/Movies (configurable)
**DuckLake**: /tmp/ducklake/



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Dataframes
- **polars** [○] via bicomodule

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

## Forward Reference

- unified-reafference (real-time session monitoring)
