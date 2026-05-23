---
name: checkpoint-resume
description: Exactly-once processing semantics with distributed coordination for file-based data pipelines. Atomic file claiming, status tracking, and automatic retry with in-memory fallback.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: data-access
  time: 4h
  source: drift-masterguide
---

# Checkpoint & Resume Processing

Exactly-once processing semantics with distributed coordination for file-based data pipelines.

## When to Use This Skill

- Processing large file batches across multiple workers
- Need to resume after worker crashes
- Preventing duplicate processing of the same file
- Tracking processing progress and statistics

## Core Concepts

The pattern provides:
- Atomic file claiming (only one worker processes each file)
- Status tracking (pending, processing, completed, failed)
- Automatic retry with configurable limits
- In-memory fallback for development/testing

```
┌──────────┐     ┌─────────────────┐     ┌──────────┐
│ Worker 1 │────▶│  Checkpoint DB  │◀────│ Worker 2 │
└──────────┘     └─────────────────┘     └──────────┘
     │                   │                    │
     ▼                   ▼                    ▼
  claim_file()     atomic claims        claim_file()
  process()        status tracking      process()
  complete()       retry logic          complete()
```

## Implementation

### Database Schema (PostgreSQL/Supabase)

```sql
CREATE TABLE file_checkpoints (
  file_url TEXT PRIMARY KEY,
  file_type TEXT NOT NULL,
  file_timestamp TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  records_total INTEGER DEFAULT 0,
  records_filtered INTEGER DEFAULT 0,
  records_persisted INTEGER DEFAULT 0,
  processing_time_ms INTEGER DEFAULT 0,
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  processed_by TEXT,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_checkpoints_status ON file_checkpoints(status);

-- Atomic claim function
CREATE OR REPLACE FUNCTION claim_file(
  p_file_url TEXT,
  p_file_type TEXT,
  p_file_timestamp TIMESTAMPTZ,
  p_worker_id TEXT
) RETURNS BOOLEAN AS $$
DECLARE
  v_claimed BOOLEAN := FALSE;
BEGIN
  -- Try to insert new record
  INSERT INTO file_checkpoints (file_url, file_type, file_timestamp, status, processed_by, started_at)
  VALUES (p_file_url, p_file_type, p_file_timestamp, 'processing', p_worker_id, NOW())
  ON CONFLICT (file_url) DO NOTHING;
  
  IF FOUND THEN
    v_claimed := TRUE;
  ELSE
    -- Check if we can retry a failed file
    UPDATE file_checkpoints
    SET status = 'processing', processed_by = p_worker_id, started_at = NOW(), retry_count = retry_count + 1
    WHERE file_url = p_file_url AND status = 'failed' AND retry_count < 3;
    
    v_claimed := FOUND;
  END IF;
  
  RETURN v_claimed;
END;
$$ LANGUAGE plpgsql;
```

### TypeScript

```typescript
interface FileCheckpoint {
  fileUrl: string;
  fileType: string;
  fileTimestamp: Date;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  recordsTotal: number;
  recordsFiltered: number;
  recordsPersisted: number;
  processingTimeMs: number;
  errorMessage?: string;
  retryCount: number;
  processedBy?: string;
}

interface ProcessingStats {
  totalRows: number;
  filteredRows: number;
  persistedRows: number;
  durationMs: number;
}

class CheckpointManager {
  private workerId: string;
  private inMemory = new Map<string, FileCheckpoint>();
  private useInMemory = false;

  constructor(
    private getClient: () => DatabaseClient | null,
    workerId?: string
  ) {
    this.workerId = workerId || 
      `worker_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  }

  async claimFile(
    fileUrl: string, 
    fileType: string, 
    fileTimestamp: Date
  ): Promise<boolean> {
    const client = this.getClient();
    
    if (client) {
      try {
        const result = await client.rpc('claim_file', {
          p_file_url: fileUrl,
          p_file_type: fileType,
          p_file_timestamp: fileTimestamp.toISOString(),
          p_worker_id: this.workerId,
        });
        
        if (!result.error) return result.data === true;
      } catch (e) {
        console.warn('Database unavailable, using in-memory');
      }
    }

    // Fallback to in-memory (single-worker mode)
    this.useInMemory = true;
    
    if (this.inMemory.has(fileUrl)) {
      const existing = this.inMemory.get(fileUrl)!;
      if (existing.status !== 'failed' || existing.retryCount >= 3) {
        return false;
      }
    }

    this.inMemory.set(fileUrl, {
      fileUrl,
      fileType,
      fileTimestamp,
      status: 'processing',
      recordsTotal: 0,
      recordsFiltered: 0,
      recordsPersisted: 0,
      processingTimeMs: 0,
      retryCount: 0,
      processedBy: this.workerId,
    });

    return true;
  }

  async completeFile(fileUrl: string, stats: ProcessingStats): Promise<void> {
    const client = this.getClient();
    
    if (client && !this.useInMemory) {
      await client.rpc('complete_file', {
        p_file_url: fileUrl,
        p_records_total: stats.totalRows,
        p_records_filtered: stats.filteredRows,
        p_records_persisted: stats.persistedRows,
        p_processing_time_ms: stats.durationMs,
      });
      return;
    }

    const checkpoint = this.inMemory.get(fileUrl);
    if (checkpoint) {
      checkpoint.status = 'completed';
      checkpoint.recordsTotal = stats.totalRows;
      checkpoint.recordsFiltered = stats.filteredRows;
      checkpoint.recordsPersisted = stats.persistedRows;
      checkpoint.processingTimeMs = stats.durationMs;
    }
  }

  async failFile(fileUrl: string, errorMessage: string): Promise<void> {
    const client = this.getClient();
    
    if (client && !this.useInMemory) {
      await client
        .from('file_checkpoints')
        .update({ status: 'failed', error_message: errorMessage })
        .eq('file_url', fileUrl);
      return;
    }

    const checkpoint = this.inMemory.get(fileUrl);
    if (checkpoint) {
      checkpoint.status = 'failed';
      checkpoint.errorMessage = errorMessage;
      checkpoint.retryCount++;
    }
  }

  async isProcessed(fileUrl: string): Promise<boolean> {
    const client = this.getClient();
    
    if (client && !this.useInMemory) {
      const { data } = await client
        .from('file_checkpoints')
        .select('status')
        .eq('file_url', fileUrl)
        .single();
      
      return data?.status === 'completed';
    }

    return this.inMemory.get(fileUrl)?.status === 'completed';
  }

  getWorkerId(): string {
    return this.workerId;
  }
}
```

## Usage Examples

### Processing Files

```typescript
const checkpoint = new CheckpointManager(getDbClient);

async function processFiles(fileUrls: string[]) {
  for (const url of fileUrls) {
    // Try to claim
    const claimed = await checkpoint.claimFile(url, 'events', new Date());
    if (!claimed) {
      console.log(`Skipping ${url} - already claimed`);
      continue;
    }

    const startTime = Date.now();
    
    try {
      const result = await processFile(url);
      
      await checkpoint.completeFile(url, {
        totalRows: result.total,
        filteredRows: result.filtered,
        persistedRows: result.persisted,
        durationMs: Date.now() - startTime,
      });
      
    } catch (error) {
      await checkpoint.failFile(url, error.message);
    }
  }
}
```

## Best Practices

1. Use database functions for atomic claims - prevents race conditions
2. Always have in-memory fallback for dev/testing
3. Track retry count to prevent infinite loops (max 3 retries)
4. Include processing stats for observability
5. Generate unique worker IDs to track which worker processed what

## Common Mistakes

- Not using atomic operations for claiming (race conditions)
- No retry limit (infinite retry loops)
- Forgetting in-memory fallback (breaks local development)
- Not tracking processing statistics (can't debug issues)
- Using file path instead of URL as key (path changes between environments)

## Related Patterns

- batch-processing - Batch database operations
- dead-letter-queue - Handle permanently failed files
- distributed-lock - Coordinate between workers
