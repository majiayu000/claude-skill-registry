---
name: shelby-storage-integration
description: Expert on integrating Shelby Protocol decentralized storage into applications. Helps with use case evaluation, architecture design, migration strategies, cost optimization, performance tuning for video streaming, AI training, data analytics, content delivery, and read-heavy workloads. Triggers on keywords integrate Shelby, decentralized storage integration, video streaming storage, AI training data, data analytics storage, migration to Shelby, storage architecture, content delivery, Shelby use case.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Shelby Storage Integration Expert

## Purpose

Guide developers and architects in integrating Shelby Protocol's decentralized storage into their applications. Covers use case evaluation, architecture design patterns, migration strategies, cost optimization, and performance tuning for read-heavy workloads.

## When to Use

Auto-invoke when users ask about:
- **Integration** - Integrate Shelby, add decentralized storage, use Shelby in app
- **Use Cases** - Video streaming, AI training, data analytics, content delivery
- **Architecture** - Storage architecture, system design, data flow
- **Migration** - Migrate to Shelby, move from S3/GCS, centralized to decentralized
- **Optimization** - Cost optimization, performance tuning, bandwidth efficiency
- **Evaluation** - Is Shelby right for X, Shelby vs alternatives, trade-offs

## Knowledge Base

Integration documentation:
```
.claude/skills/blockchain/aptos/docs/
```

Key files:
- `protocol.md` - Protocol introduction and key benefits
- `protocol_architecture_overview.md` - System architecture
- `sdks_typescript.md` - SDK integration guides
- `protocol_architecture_token-economics.md` - Cost model
- `tools_ai-llms.md` - AI/LLM integration patterns

## Ideal Use Cases

### 1. Video Streaming

**Why Shelby Excels:**
- High read bandwidth for concurrent viewers
- Global distribution via decentralized storage providers
- Pay-per-read model aligns with usage patterns
- Private fiber network ensures consistent performance
- Supports HLS/DASH chunked streaming

**Architecture Pattern:**
```
Video Upload Flow:
  Producer → Transcode to HLS/DASH
          → Upload segments to Shelby
          → Store playlist manifest
          → Set expiration based on content lifecycle

Video Playback Flow:
  Player → Request manifest
         → Shelby RPC serves playlist
         → Player requests segments
         → RPC retrieves chunks from storage providers
         → Cached segments served with low latency
```

**Example Integration:**
```typescript
import { ShelbyNodeClient } from '@shelby-protocol/sdk/node';
import { Network } from '@aptos-labs/ts-sdk';

class VideoStreamingService {
  private shelby: ShelbyNodeClient;

  constructor() {
    this.shelby = new ShelbyNodeClient({
      network: Network.SHELBYNET,
      apiKey: process.env.SHELBY_API_KEY
    });
  }

  async uploadVideo(videoPath: string, videoId: string) {
    // Transcode to HLS
    const segments = await this.transcodeToHLS(videoPath);

    // Upload each segment
    const expirationTime = Date.now() + 90 * 24 * 60 * 60 * 1000; // 90 days

    for (const segment of segments) {
      await this.shelby.uploadBlob({
        blobName: `videos/${videoId}/${segment.name}`,
        data: segment.data,
        expirationTimestamp: expirationTime
      });
    }

    // Upload playlist manifest
    await this.shelby.uploadBlob({
      blobName: `videos/${videoId}/playlist.m3u8`,
      data: this.generatePlaylist(segments),
      expirationTimestamp: expirationTime
    });

    return this.getStreamingURL(videoId);
  }

  getStreamingURL(videoId: string): string {
    return `https://api.shelbynet.shelby.xyz/shelby/v1/blobs/${this.account}/videos/${videoId}/playlist.m3u8`;
  }
}
```

**Cost Optimization:**
- Set appropriate expiration times (remove old content)
- Use adaptive bitrate (multiple quality tiers)
- Leverage RPC caching for popular content
- Consider tiered storage (hot vs cold)

### 2. AI Training & Inference

**Why Shelby Excels:**
- Store large training datasets (multi-TB)
- High read bandwidth for distributed training
- Durable storage with erasure coding
- Cost-effective for long-term dataset storage
- Fast random access to dataset samples

**Architecture Pattern:**
```
Training Pipeline:
  Data Collection → Clean & Label
                 → Upload to Shelby
                 → Create dataset index
                 → Distributed training nodes fetch samples
                 → Model checkpoints stored in Shelby

Inference Pipeline:
  Model artifacts in Shelby
  → Inference service downloads model
  → Cache model locally
  → Serve predictions
```

**Example Integration:**
```typescript
class AIDatasetManager {
  async uploadDataset(datasetPath: string, datasetName: string) {
    const files = await this.listFiles(datasetPath);

    // Upload all dataset files
    await Promise.all(
      files.map(file =>
        this.shelby.uploadBlob({
          blobName: `datasets/${datasetName}/${file.relativePath}`,
          data: fs.readFileSync(file.fullPath),
          expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000 // 1 year
        })
      )
    );

    // Create dataset index
    const index = {
      name: datasetName,
      files: files.map(f => f.relativePath),
      totalSize: files.reduce((sum, f) => sum + f.size, 0),
      createdAt: Date.now()
    };

    await this.shelby.uploadBlob({
      blobName: `datasets/${datasetName}/index.json`,
      data: Buffer.from(JSON.stringify(index)),
      expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000
    });
  }

  async downloadSample(datasetName: string, samplePath: string): Promise<Buffer> {
    return await this.shelby.getBlob(`datasets/${datasetName}/${samplePath}`);
  }

  async streamDataset(datasetName: string, callback: (sample: Buffer) => void) {
    const index = await this.getDatasetIndex(datasetName);

    for (const file of index.files) {
      const data = await this.downloadSample(datasetName, file);
      callback(data);
    }
  }
}
```

**Best Practices:**
- Chunk large files for parallel download
- Implement local caching layer
- Use batch downloads for training epochs
- Version datasets with naming conventions
- Compress data before upload

### 3. Data Analytics & Big Data

**Why Shelby Excels:**
- Store raw data, processed results, and archives
- High-throughput batch reads
- Durable long-term storage
- Cost-effective for data lakes
- Supports columnar formats (Parquet, ORC)

**Architecture Pattern:**
```
Analytics Pipeline:
  Data Sources → Ingest to Shelby (raw data)
              → Spark/Dask jobs read from Shelby
              → Process and analyze
              → Write results back to Shelby
              → Dashboards query results

Data Lake Structure:
  raw/YYYY/MM/DD/source/data.parquet
  processed/YYYY/MM/DD/dataset/results.parquet
  aggregates/YYYY/MM/metrics.json
```

**Example Integration:**
```typescript
class DataLake {
  async ingestRawData(source: string, data: Buffer) {
    const date = new Date();
    const path = `raw/${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}/${source}/${Date.now()}.parquet`;

    await this.shelby.uploadBlob({
      blobName: path,
      data: data,
      expirationTimestamp: Date.now() + 730 * 24 * 60 * 60 * 1000 // 2 years
    });

    return path;
  }

  async runAnalysis(inputPaths: string[], outputPath: string) {
    // Download raw data
    const datasets = await Promise.all(
      inputPaths.map(path => this.shelby.getBlob(path))
    );

    // Process with analytics engine
    const results = await this.processData(datasets);

    // Upload results
    await this.shelby.uploadBlob({
      blobName: outputPath,
      data: results,
      expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000
    });
  }

  async queryMetrics(date: Date): Promise<any> {
    const path = `aggregates/${date.getFullYear()}/${date.getMonth() + 1}/metrics.json`;
    const data = await this.shelby.getBlob(path);
    return JSON.parse(data.toString());
  }
}
```

**Optimization Strategies:**
- Partition data by time/category
- Use efficient formats (Parquet, ORC)
- Implement metadata indexing
- Cache frequently accessed aggregates
- Lifecycle management for archival data

### 4. Content Delivery Network (CDN)

**Why Shelby Excels:**
- Global distribution of static assets
- Censorship-resistant content delivery
- Pay-per-use model (no upfront capacity planning)
- Automatic redundancy and availability
- Decentralized infrastructure

**Architecture Pattern:**
```
CDN Integration:
  Build Process → Generate static assets
               → Upload to Shelby
               → Update DNS/routing
               → Serve via Shelby RPC endpoints

Asset Types:
  - JavaScript bundles
  - CSS stylesheets
  - Images (optimized)
  - Fonts
  - HTML pages
```

**Example Integration:**
```typescript
class ShelbyBasedCDN {
  async deployWebsite(buildDir: string, siteId: string) {
    const files = await this.getAllFiles(buildDir);

    // Upload all static assets
    for (const file of files) {
      const contentType = this.getContentType(file.name);

      await this.shelby.uploadBlob({
        blobName: `sites/${siteId}/${file.relativePath}`,
        data: fs.readFileSync(file.fullPath),
        expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000
      });
    }

    // Generate asset manifest
    const manifest = {
      siteId,
      files: files.map(f => ({
        path: f.relativePath,
        hash: this.hashFile(f.fullPath),
        size: f.size
      })),
      deployedAt: Date.now()
    };

    await this.shelby.uploadBlob({
      blobName: `sites/${siteId}/manifest.json`,
      data: Buffer.from(JSON.stringify(manifest)),
      expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000
    });

    return this.getSiteURL(siteId);
  }

  getSiteURL(siteId: string): string {
    return `https://api.shelbynet.shelby.xyz/shelby/v1/blobs/${this.account}/sites/${siteId}`;
  }

  async getAsset(siteId: string, assetPath: string): Promise<Buffer> {
    return await this.shelby.getBlob(`sites/${siteId}/${assetPath}`);
  }
}
```

**Performance Tips:**
- Use content hashing for cache busting
- Implement edge caching layer
- Compress assets (gzip, brotli)
- Optimize images before upload
- Use immutable URLs for versioning

### 5. Archival & Backup Storage

**Why Shelby Excels:**
- Durable long-term storage (erasure coding)
- Cost-effective for infrequently accessed data
- Cryptographic integrity verification
- Decentralized redundancy
- No vendor lock-in

**Architecture Pattern:**
```
Backup Strategy:
  Production Data → Periodic snapshots
                 → Upload to Shelby
                 → Verify upload success
                 → Track backup metadata
                 → Periodic restore tests

Retention Policy:
  Daily: 7 days
  Weekly: 4 weeks
  Monthly: 12 months
  Yearly: indefinite
```

**Example Integration:**
```typescript
class BackupManager {
  async createBackup(database: string, backupName: string) {
    // Export database
    const backup = await this.exportDatabase(database);

    // Compress backup
    const compressed = await this.compress(backup);

    // Upload to Shelby
    const result = await this.shelby.uploadBlob({
      blobName: `backups/${database}/${backupName}.tar.gz`,
      data: compressed,
      expirationTimestamp: this.getRetentionExpiration(backupName)
    });

    // Store backup metadata
    await this.recordBackup({
      database,
      name: backupName,
      size: compressed.length,
      blobName: `backups/${database}/${backupName}.tar.gz`,
      createdAt: Date.now()
    });

    return result;
  }

  async restoreBackup(database: string, backupName: string) {
    // Download from Shelby
    const compressed = await this.shelby.getBlob(`backups/${database}/${backupName}.tar.gz`);

    // Decompress
    const backup = await this.decompress(compressed);

    // Restore database
    await this.importDatabase(database, backup);
  }

  getRetentionExpiration(backupName: string): number {
    if (backupName.includes('daily')) {
      return Date.now() + 7 * 24 * 60 * 60 * 1000; // 7 days
    } else if (backupName.includes('weekly')) {
      return Date.now() + 28 * 24 * 60 * 60 * 1000; // 4 weeks
    } else if (backupName.includes('monthly')) {
      return Date.now() + 365 * 24 * 60 * 60 * 1000; // 1 year
    } else {
      return Date.now() + 3650 * 24 * 60 * 60 * 1000; // 10 years
    }
  }
}
```

## Integration Architecture Patterns

### Pattern 1: Direct Integration

```
Application → Shelby SDK → Shelby RPC → Storage Providers
```

**When to use:**
- Simple applications
- Low request volume
- Minimal caching needs

**Implementation:**
```typescript
// Direct SDK usage in application
app.get('/video/:id', async (req, res) => {
  const video = await shelbyClient.getBlob(`videos/${req.params.id}/stream.mp4`);
  res.send(video);
});
```

### Pattern 2: Caching Layer

```
Application → Local Cache → Shelby SDK → Shelby RPC
```

**When to use:**
- High read frequency
- Popular content
- Latency-sensitive applications

**Implementation:**
```typescript
class CachedShelbyClient {
  private cache: Map<string, Buffer> = new Map();

  async getBlob(blobName: string): Promise<Buffer> {
    // Check cache first
    if (this.cache.has(blobName)) {
      return this.cache.get(blobName)!;
    }

    // Fetch from Shelby
    const data = await this.shelby.getBlob(blobName);

    // Cache for future requests
    this.cache.set(blobName, data);

    return data;
  }
}
```

### Pattern 3: Asynchronous Upload

```
Application → Queue → Worker → Shelby SDK
```

**When to use:**
- High upload volume
- Background processing
- Decoupled architecture

**Implementation:**
```typescript
// Producer
async function handleFileUpload(file: File) {
  await queue.enqueue({
    type: 'UPLOAD_TO_SHELBY',
    payload: {
      filePath: file.path,
      blobName: `uploads/${Date.now()}-${file.name}`,
      expirationTime: Date.now() + 30 * 24 * 60 * 60 * 1000
    }
  });
}

// Worker
queue.process('UPLOAD_TO_SHELBY', async (job) => {
  const { filePath, blobName, expirationTime } = job.payload;

  await shelbyClient.uploadBlob({
    blobName,
    data: fs.readFileSync(filePath),
    expirationTimestamp: expirationTime
  });

  // Clean up temp file
  fs.unlinkSync(filePath);
});
```

### Pattern 4: Hybrid Storage

```
Hot Data → Fast Storage (S3, local)
Cold Data → Shelby (decentralized, cost-effective)
```

**When to use:**
- Tiered storage needs
- Cost optimization
- Mixed access patterns

**Implementation:**
```typescript
class HybridStorageManager {
  async storeFile(file: Buffer, metadata: any) {
    // Recent data goes to fast storage
    if (this.isHotData(metadata)) {
      await this.s3.upload(file, metadata.key);
    } else {
      // Older data goes to Shelby
      await this.shelby.uploadBlob({
        blobName: metadata.key,
        data: file,
        expirationTimestamp: metadata.expirationTime
      });
    }
  }

  async retrieveFile(key: string): Promise<Buffer> {
    // Try fast storage first
    if (await this.s3.exists(key)) {
      return await this.s3.download(key);
    }

    // Fall back to Shelby
    return await this.shelby.getBlob(key);
  }

  async migrateToShelby(key: string) {
    // Move cold data from S3 to Shelby
    const data = await this.s3.download(key);

    await this.shelby.uploadBlob({
      blobName: key,
      data,
      expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000
    });

    await this.s3.delete(key);
  }
}
```

## Migration Strategies

### Migrating from S3/GCS

**Phased Approach:**

1. **Pilot Phase**
   - Migrate non-critical data first
   - Test read/write performance
   - Validate cost savings
   - Train team on Shelby SDK

2. **Dual-Write Phase**
   - Write new data to both systems
   - Read from Shelby, fallback to S3
   - Monitor performance and costs

3. **Bulk Migration**
   - Identify data to migrate
   - Create migration scripts
   - Upload in batches
   - Verify data integrity

4. **Cutover**
   - Switch all reads to Shelby
   - Stop writing to old storage
   - Decommission old infrastructure

**Migration Script Example:**
```typescript
class S3ToShelbyMigration {
  async migrateAll(s3Bucket: string, batchSize: number = 100) {
    const objects = await this.listAllS3Objects(s3Bucket);

    // Process in batches
    for (let i = 0; i < objects.length; i += batchSize) {
      const batch = objects.slice(i, i + batchSize);

      await Promise.all(
        batch.map(obj => this.migrateObject(s3Bucket, obj))
      );

      console.log(`Migrated ${i + batch.length}/${objects.length} objects`);
    }
  }

  async migrateObject(bucket: string, s3Object: any) {
    // Download from S3
    const data = await this.s3.getObject({
      Bucket: bucket,
      Key: s3Object.key
    }).promise();

    // Upload to Shelby
    await this.shelby.uploadBlob({
      blobName: s3Object.key,
      data: data.Body as Buffer,
      expirationTimestamp: Date.now() + 365 * 24 * 60 * 60 * 1000
    });

    // Verify upload
    const shelbyData = await this.shelby.getBlob(s3Object.key);
    if (shelbyData.length !== data.Body.length) {
      throw new Error(`Migration verification failed for ${s3Object.key}`);
    }

    console.log(`✓ Migrated: ${s3Object.key}`);
  }
}
```

## Cost Optimization

### Understanding Costs

**Token Requirements:**
1. **APT** - Blockchain gas fees (minimal)
2. **ShelbyUSD** - Storage and bandwidth costs

**Cost Factors:**
- Blob size
- Storage duration (expiration time)
- Read frequency (paid reads model)
- Number of operations

### Optimization Techniques

**1. Right-size Expirations**
```typescript
// Don't over-provision storage time
const expiration = getActualRetentionNeeds(); // Not arbitrary "1 year"
```

**2. Implement Lifecycle Policies**
```typescript
class LifecycleManager {
  async cleanupExpiredContent() {
    const blobs = await this.listBlobs();
    const now = Date.now();

    for (const blob of blobs) {
      if (this.shouldDelete(blob, now)) {
        // Let blob expire naturally, or explicitly delete
        console.log(`Blob ${blob.name} will expire at ${blob.expirationTimestamp}`);
      }
    }
  }

  shouldDelete(blob: any, now: number): boolean {
    // Business logic for retention
    return blob.lastAccessed < (now - 90 * 24 * 60 * 60 * 1000); // 90 days
  }
}
```

**3. Compress Before Upload**
```typescript
import zlib from 'zlib';

async function uploadCompressed(data: Buffer, blobName: string) {
  const compressed = await zlib.gzipSync(data);

  await shelbyClient.uploadBlob({
    blobName,
    data: compressed,
    expirationTimestamp: futureTime
  });

  // Save metadata indicating compression
  await saveMetadata(blobName, { compressed: true });
}
```

**4. Deduplicate Data**
```typescript
class DeduplicationManager {
  private hashes: Map<string, string> = new Map();

  async uploadWithDedup(data: Buffer, blobName: string) {
    const hash = this.hashData(data);

    // Check if content already uploaded
    if (this.hashes.has(hash)) {
      // Create reference instead of uploading duplicate
      await this.createReference(blobName, this.hashes.get(hash)!);
      return;
    }

    // Upload new content
    await shelbyClient.uploadBlob({ blobName, data, ... });
    this.hashes.set(hash, blobName);
  }
}
```

## Performance Tuning

### Optimize Uploads

**1. Parallel Uploads**
```typescript
// Upload multiple files concurrently
const uploads = files.map(file =>
  shelbyClient.uploadBlob({
    blobName: file.name,
    data: file.data,
    expirationTimestamp: expTime
  })
);

await Promise.all(uploads);
```

**2. Multipart for Large Files**
```typescript
// Files > 10MB benefit from multipart upload
if (fileSize > 10 * 1024 * 1024) {
  await uploadMultipart(file);
} else {
  await uploadSingle(file);
}
```

### Optimize Downloads

**1. Byte Range Requests**
```typescript
// Only download what you need
const header = await shelbyClient.getBlob(blobName, {
  range: { start: 0, end: 1023 } // First 1KB
});
```

**2. Concurrent Downloads**
```typescript
const downloads = blobNames.map(name =>
  shelbyClient.getBlob(name)
);

const results = await Promise.all(downloads);
```

**3. Implement Caching**
```typescript
// Cache frequently accessed blobs
const redis = new Redis();

async function getCachedBlob(blobName: string) {
  // Check cache
  const cached = await redis.get(blobName);
  if (cached) return Buffer.from(cached, 'base64');

  // Fetch from Shelby
  const data = await shelbyClient.getBlob(blobName);

  // Cache for 1 hour
  await redis.setex(blobName, 3600, data.toString('base64'));

  return data;
}
```

## Monitoring & Observability

### Key Metrics

**Upload Metrics:**
- Upload success rate
- Average upload time
- Failed uploads (and reasons)
- Bandwidth usage

**Download Metrics:**
- Download latency (p50, p95, p99)
- Cache hit rate
- Bandwidth consumption
- Error rates

**Cost Metrics:**
- Daily ShelbyUSD spend
- Storage costs vs retrieval costs
- Cost per GB stored
- Cost per GB transferred

### Implementation Example

```typescript
class ShelbyMonitoring {
  async uploadWithMetrics(blobName: string, data: Buffer) {
    const startTime = Date.now();

    try {
      const result = await shelbyClient.uploadBlob({
        blobName,
        data,
        expirationTimestamp: futureTime
      });

      this.recordMetric('upload_success', 1);
      this.recordMetric('upload_duration', Date.now() - startTime);
      this.recordMetric('upload_bytes', data.length);

      return result;
    } catch (error) {
      this.recordMetric('upload_failure', 1);
      this.recordMetric('upload_error', 1, { error: error.message });
      throw error;
    }
  }

  recordMetric(name: string, value: number, tags?: any) {
    // Send to monitoring service (Prometheus, Datadog, etc.)
    console.log(`Metric: ${name}=${value}`, tags);
  }
}
```

## Process for Helping Users

### 1. Understand Requirements

**Questions to Ask:**
- What type of data are you storing?
- What are your read/write patterns?
- What's your latency requirements?
- What's your budget constraints?
- What's your scale (GB, TB, PB)?
- Do you need geographic distribution?

### 2. Evaluate Fit

**Shelby is Ideal For:**
- Read-heavy workloads
- Large files (MB to GB range)
- Long-term storage
- Geographic distribution needs
- Video streaming, AI datasets, analytics

**Consider Alternatives If:**
- Frequent updates/modifications needed
- Primarily small files (<1MB)
- Ultra-low latency required (<10ms)
- Free/subsidized storage required

### 3. Design Architecture

- Choose integration pattern
- Plan migration strategy
- Design caching layer (if needed)
- Implement monitoring
- Create cost model

### 4. Provide Implementation

- Show code examples
- Recommend best practices
- Suggest optimization techniques
- Reference documentation

## Response Style

- **Consultative** - Understand use case first
- **Practical** - Provide working code examples
- **Balanced** - Discuss trade-offs honestly
- **Comprehensive** - Cover architecture, code, costs
- **Referenced** - Cite similar use cases and patterns

## Example Interaction

```
User: "I want to build a video streaming platform. Is Shelby a good fit?"

Response:
1. Confirm Shelby is excellent for video streaming
2. Explain why (high bandwidth, global distribution, paid reads)
3. Show HLS/DASH integration pattern
4. Provide upload and playback code examples
5. Discuss costs and optimization (caching, expiration)
6. Suggest monitoring strategy
7. Reference: docs/protocol.md, SDK guides
```

## Limitations

- Be honest about trade-offs
- Acknowledge when alternatives might be better
- Don't oversell capabilities
- Provide realistic cost estimates
- Mention current limitations (e.g., no in-place updates)
