---
name: storage-sync
description: Synchronize memories between Turso (durable) and redb (cache) storage layers. Use when cache appears stale, after failures, or during periodic maintenance.
---

# Storage Sync

Synchronize memories between Turso (durable) and redb (cache) storage layers.

## When to Sync

1. **On startup** - After system initialization
2. **Periodic** - Scheduled background sync
3. **Cache staleness** - When redb appears outdated
4. **Recovery** - After storage failures
5. **Manual trigger** - When explicitly requested

## Sync Process

1. **Check connection health**:
   ```rust
   turso_client.ping().await?;
   redb_env.check_integrity()?;
   ```

2. **Fetch latest from Turso**:
   ```rust
   let episodes = turso_client
       .query("SELECT * FROM episodes ORDER BY timestamp DESC LIMIT ?")
       .bind(max_episodes_cache)
       .await?;
   ```

3. **Update redb cache**:
   ```rust
   tokio::task::spawn_blocking(move || {
       let write_txn = redb.begin_write()?;
       let mut table = write_txn.open_table(EPISODES_TABLE)?;
       for episode in episodes {
           table.insert(episode.id.as_bytes(), episode.to_bytes())?;
       }
       write_txn.commit()?;
   });
   ```

4. **Sync patterns and embeddings** if enabled

## Configuration

```rust
pub struct SyncConfig {
    pub max_episodes_cache: usize,  // Default: 1000
    pub batch_size: usize,          // Default: 100
    pub sync_patterns: bool,        // Default: true
    pub sync_embeddings: bool,      // Default: true
}
```

## Error Handling

| Error | Handling |
|-------|----------|
| Turso unavailable | Skip sync, log warning, retry later |
| redb corruption | Attempt repair, rebuild from Turso |
| Partial sync | Track progress, resume from last point |

## Performance Tips

- Batch small operations
- Incremental sync (only changes)
- Parallel fetch with Tokio
- Write-ahead preparation

## Validation

After sync, verify:
- Episode count matches
- Latest episodes present
- Pattern counts consistent
- No orphaned embeddings

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow syncs | Reduce cache size, increase batch |
| redb lock errors | Use dedicated write task |
| Memory pressure | Stream large results, smaller batches |
