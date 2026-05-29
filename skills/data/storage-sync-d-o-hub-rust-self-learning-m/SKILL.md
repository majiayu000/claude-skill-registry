---
name: storage-sync
description: Synchronize memories between Turso (durable) and redb (cache) storage layers. Use when cache appears stale, after failures, or during periodic maintenance.
---

# Storage Sync

Synchronize memories between Turso (durable) and redb (cache) storage layers.

## Purpose
Ensure consistency between the durable Turso database and the hot redb cache by reconciling episodes, patterns, and embeddings.

## When to Sync

1. **On startup**: After system initialization
2. **Periodic maintenance**: Scheduled background sync
3. **Cache staleness**: When redb data appears outdated
4. **Recovery**: After Turso or redb failures
5. **Manual trigger**: When explicitly requested

## Sync Strategy

### Source of Truth
- **Turso**: Authoritative source for all data
- **redb**: Performance cache, can be rebuilt from Turso

### Sync Process

1. **Check connection health**:
   ```rust
   // Verify both connections are active
   turso_client.ping().await?;
   redb_env.check_integrity()?;
   ```

2. **Fetch latest from Turso**:
   ```rust
   // Query recent episodes, patterns, metadata
   let episodes = turso_client
       .query("SELECT * FROM episodes ORDER BY timestamp DESC LIMIT ?")
       .bind(max_episodes_cache)
       .await?;
   ```

3. **Update redb cache**:
   ```rust
   let write_txn = redb_env.begin_write()?;
   {
       let mut table = write_txn.open_table(EPISODES_TABLE)?;
       for episode in episodes {
           table.insert(episode.id, episode.to_bytes())?;
       }
   }
   write_txn.commit()?;
   ```

4. **Sync patterns and heuristics**:
   - Fetch updated patterns from Turso
   - Update redb pattern table
   - Rebuild pattern indexes if needed

5. **Sync embeddings**:
   - Check for new embeddings in Turso
   - Update redb embeddings table
   - Verify embedding metadata consistency

## Configuration

```rust
pub struct SyncConfig {
    pub max_episodes_cache: usize,  // Default: 1000
    pub batch_size: usize,           // Default: 100
    pub sync_patterns: bool,         // Default: true
    pub sync_embeddings: bool,       // Default: true
    pub validate_checksums: bool,    // Default: false
}
```

## Concurrency

- Use Tokio for Turso async operations
- Perform redb writes in dedicated task to avoid blocking
- Use semaphore to limit concurrent writes

```rust
let semaphore = Arc::new(Semaphore::new(10));
// Limit to 10 concurrent operations
```

## Error Handling

### Turso Unavailable
- Skip sync, use cached data
- Log warning, retry later
- Set staleness flag

### redb Corruption
- Attempt repair
- If failed, rebuild from Turso
- May require temp file and swap

### Partial Sync
- Track sync progress
- Resume from last successful point
- Use transaction boundaries

## Validation

After sync, verify:
1. Episode count matches (within cache limit)
2. Latest episodes are present in redb
3. Pattern counts are consistent
4. No orphaned embeddings

## Performance Tips

1. **Batch operations**: Group small writes
2. **Incremental sync**: Only sync changes since last sync
3. **Parallel fetch**: Use Tokio to parallelize Turso queries
4. **Write-ahead**: Prepare redb data before transaction

## Example

```rust
pub async fn sync_memories(&self, config: SyncConfig) -> Result<SyncReport> {
    let start = Instant::now();

    // 1. Fetch from Turso
    let episodes = self.turso
        .fetch_recent_episodes(config.max_episodes_cache)
        .await?;

    // 2. Update redb in dedicated task
    let redb = self.redb.clone();
    let sync_task = tokio::task::spawn_blocking(move || {
        let write_txn = redb.begin_write()?;
        {
            let mut table = write_txn.open_table(EPISODES_TABLE)?;
            for episode in episodes {
                table.insert(episode.id.as_bytes(), episode.to_bytes())?;
            }
        }
        write_txn.commit()?;
        Ok::<_, anyhow::Error>(())
    });

    sync_task.await??;

    // 3. Sync patterns if enabled
    if config.sync_patterns {
        self.sync_patterns_internal().await?;
    }

    // 4. Sync embeddings if enabled
    if config.sync_embeddings {
        self.sync_embeddings_internal().await?;
    }

    Ok(SyncReport {
        duration_ms: start.elapsed().as_millis() as u64,
        episodes_synced: episodes.len(),
        patterns_synced: /* ... */,
    })
}
```

## Monitoring

Track metrics:
- Sync duration
- Items synced (episodes, patterns, embeddings)
- Error rate
- Cache hit rate after sync
- Staleness warnings

## Troubleshooting

**Slow syncs**:
- Reduce `max_episodes_cache`
- Increase `batch_size`
- Check network latency to Turso

**redb lock errors**:
- Ensure no long-running read transactions
- Use dedicated write task
- Check for deadlocks

**Memory pressure**:
- Stream large result sets
- Use cursor-based pagination
- Process in smaller batches
