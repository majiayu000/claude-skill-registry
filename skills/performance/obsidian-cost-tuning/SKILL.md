---
name: obsidian-cost-tuning
description: |
  Optimize Obsidian plugin resource usage and external service costs.
  Use when managing API quotas, reducing storage usage,
  or optimizing sync and external service consumption.
  Trigger with phrases like "obsidian resources", "obsidian quota",
  "optimize obsidian storage", "reduce obsidian costs".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Obsidian Cost Tuning

## Overview
Optimize resource consumption and external service costs for Obsidian plugins that use APIs, storage, or sync services.

## Prerequisites
- Plugin with external API integrations
- Understanding of API pricing models
- Access to usage metrics

## Resource Categories

### Cost Drivers
| Resource | Optimization Target | Impact |
|----------|-------------------|--------|
| API calls | Minimize requests | High |
| Data storage | Compress and dedupe | Medium |
| Sync bandwidth | Reduce transfer size | Medium |
| Compute | Cache results | Low |

## Instructions

### Step 1: API Request Optimization
```typescript
// src/services/api-optimizer.ts
import { requestUrl } from 'obsidian';

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  etag?: string;
}

export class OptimizedAPIClient {
  private cache = new Map<string, CacheEntry<any>>();
  private pendingRequests = new Map<string, Promise<any>>();
  private cacheTTL: number;

  constructor(cacheTTLMs: number = 5 * 60 * 1000) { // 5 min default
    this.cacheTTL = cacheTTLMs;
  }

  async get<T>(url: string, options: {
    bypassCache?: boolean;
    customTTL?: number;
  } = {}): Promise<T> {
    const cacheKey = url;

    // Check cache
    if (!options.bypassCache) {
      const cached = this.cache.get(cacheKey);
      const ttl = options.customTTL ?? this.cacheTTL;

      if (cached && Date.now() - cached.timestamp < ttl) {
        console.log(`[Cache] HIT: ${url}`);
        return cached.data as T;
      }
    }

    // Deduplicate concurrent requests
    const pending = this.pendingRequests.get(cacheKey);
    if (pending) {
      console.log(`[Request] DEDUPE: ${url}`);
      return pending as Promise<T>;
    }

    // Make request
    const requestPromise = this.makeRequest<T>(url, cacheKey);
    this.pendingRequests.set(cacheKey, requestPromise);

    try {
      return await requestPromise;
    } finally {
      this.pendingRequests.delete(cacheKey);
    }
  }

  private async makeRequest<T>(url: string, cacheKey: string): Promise<T> {
    const cached = this.cache.get(cacheKey);
    const headers: Record<string, string> = {};

    // Use ETags for conditional requests
    if (cached?.etag) {
      headers['If-None-Match'] = cached.etag;
    }

    const response = await requestUrl({
      url,
      headers,
      throw: false,
    });

    // Not modified - use cached data
    if (response.status === 304 && cached) {
      console.log(`[Request] NOT MODIFIED: ${url}`);
      this.cache.set(cacheKey, {
        ...cached,
        timestamp: Date.now(),
      });
      return cached.data as T;
    }

    // Store new data
    const etag = response.headers['etag'];
    this.cache.set(cacheKey, {
      data: response.json,
      timestamp: Date.now(),
      etag,
    });

    console.log(`[Request] FETCHED: ${url}`);
    return response.json as T;
  }

  clearCache(): void {
    this.cache.clear();
  }

  getCacheStats(): { size: number; entries: number } {
    let size = 0;
    for (const entry of this.cache.values()) {
      size += JSON.stringify(entry.data).length;
    }
    return { size, entries: this.cache.size };
  }
}
```

### Step 2: Request Batching
```typescript
// src/services/batch-requester.ts
export class BatchRequester<T, R> {
  private queue: Array<{ input: T; resolve: (r: R) => void; reject: (e: Error) => void }> = [];
  private batchTimeout: NodeJS.Timeout | null = null;
  private batchProcessor: (inputs: T[]) => Promise<R[]>;
  private maxBatchSize: number;
  private batchDelayMs: number;

  constructor(
    batchProcessor: (inputs: T[]) => Promise<R[]>,
    options: { maxBatchSize?: number; batchDelayMs?: number } = {}
  ) {
    this.batchProcessor = batchProcessor;
    this.maxBatchSize = options.maxBatchSize ?? 20;
    this.batchDelayMs = options.batchDelayMs ?? 50;
  }

  async request(input: T): Promise<R> {
    return new Promise((resolve, reject) => {
      this.queue.push({ input, resolve, reject });

      if (this.queue.length >= this.maxBatchSize) {
        this.processBatch();
      } else if (!this.batchTimeout) {
        this.batchTimeout = setTimeout(() => this.processBatch(), this.batchDelayMs);
      }
    });
  }

  private async processBatch(): Promise<void> {
    if (this.batchTimeout) {
      clearTimeout(this.batchTimeout);
      this.batchTimeout = null;
    }

    const batch = this.queue.splice(0, this.maxBatchSize);
    if (batch.length === 0) return;

    try {
      const inputs = batch.map(item => item.input);
      const results = await this.batchProcessor(inputs);

      batch.forEach((item, index) => {
        item.resolve(results[index]);
      });
    } catch (error) {
      batch.forEach(item => {
        item.reject(error as Error);
      });
    }
  }
}

// Usage: Batch multiple API lookups into single request
const batcher = new BatchRequester<string, NoteMetadata>(
  async (noteIds: string[]) => {
    // Single API call for multiple items
    const response = await api.getNotes(noteIds);
    return response.notes;
  }
);

// Individual calls are automatically batched
const note1 = await batcher.request('note-1');
const note2 = await batcher.request('note-2');
```

### Step 3: Storage Optimization
```typescript
// src/services/storage-optimizer.ts
export class StorageOptimizer {
  // Compress data before storing
  static compress(data: any): string {
    const json = JSON.stringify(data);

    // Simple compression: remove whitespace and use shorter keys
    // For production, use actual compression library
    return json
      .replace(/\s+/g, '')
      .replace(/"([^"]+)":/g, (_, key) => {
        // Use single-char keys for common fields
        const shortKeys: Record<string, string> = {
          'path': 'p',
          'name': 'n',
          'content': 'c',
          'modified': 'm',
          'created': 'r',
          'tags': 't',
        };
        return `"${shortKeys[key] || key}":`;
      });
  }

  // Decompress stored data
  static decompress(compressed: string): any {
    const longKeys: Record<string, string> = {
      'p': 'path',
      'n': 'name',
      'c': 'content',
      'm': 'modified',
      'r': 'created',
      't': 'tags',
    };

    const expanded = compressed.replace(/"([pncmrt])":/g, (_, key) => {
      return `"${longKeys[key]}":`;
    });

    return JSON.parse(expanded);
  }

  // Deduplicate repeated strings
  static deduplicateStrings<T extends object>(data: T[]): { data: T[]; dictionary: string[] } {
    const dictionary: string[] = [];
    const stringIndex = new Map<string, number>();

    const indexedData = data.map(item => {
      const indexed: any = {};
      for (const [key, value] of Object.entries(item)) {
        if (typeof value === 'string' && value.length > 10) {
          let index = stringIndex.get(value);
          if (index === undefined) {
            index = dictionary.length;
            dictionary.push(value);
            stringIndex.set(value, index);
          }
          indexed[key] = `$${index}`;
        } else {
          indexed[key] = value;
        }
      }
      return indexed;
    });

    return { data: indexedData, dictionary };
  }

  // Calculate storage savings
  static calculateSavings(original: any, optimized: any): {
    originalSize: number;
    optimizedSize: number;
    savingsPercent: number;
  } {
    const originalSize = JSON.stringify(original).length;
    const optimizedSize = JSON.stringify(optimized).length;
    const savingsPercent = ((originalSize - optimizedSize) / originalSize) * 100;

    return { originalSize, optimizedSize, savingsPercent };
  }
}
```

### Step 4: Rate Limiting with Quotas
```typescript
// src/services/quota-manager.ts
interface QuotaConfig {
  dailyLimit: number;
  monthlyLimit: number;
  perMinuteLimit: number;
}

export class QuotaManager {
  private config: QuotaConfig;
  private usage: {
    daily: { count: number; date: string };
    monthly: { count: number; month: string };
    perMinute: number[];
  };
  private storageKey: string;

  constructor(plugin: Plugin, config: QuotaConfig) {
    this.config = config;
    this.storageKey = 'api-quota-usage';
    this.usage = this.loadUsage(plugin);
  }

  private loadUsage(plugin: Plugin): typeof this.usage {
    const saved = plugin.loadData()?.[this.storageKey];
    const today = new Date().toISOString().split('T')[0];
    const month = today.substring(0, 7);

    return {
      daily: saved?.daily?.date === today
        ? saved.daily
        : { count: 0, date: today },
      monthly: saved?.monthly?.month === month
        ? saved.monthly
        : { count: 0, month },
      perMinute: [],
    };
  }

  async canMakeRequest(): Promise<{ allowed: boolean; reason?: string; waitMs?: number }> {
    const now = Date.now();

    // Check per-minute limit
    this.usage.perMinute = this.usage.perMinute.filter(t => now - t < 60000);
    if (this.usage.perMinute.length >= this.config.perMinuteLimit) {
      const oldestRequest = this.usage.perMinute[0];
      const waitMs = 60000 - (now - oldestRequest);
      return {
        allowed: false,
        reason: `Rate limit: ${this.config.perMinuteLimit} requests/minute`,
        waitMs,
      };
    }

    // Check daily limit
    if (this.usage.daily.count >= this.config.dailyLimit) {
      return {
        allowed: false,
        reason: `Daily limit reached: ${this.config.dailyLimit} requests`,
      };
    }

    // Check monthly limit
    if (this.usage.monthly.count >= this.config.monthlyLimit) {
      return {
        allowed: false,
        reason: `Monthly limit reached: ${this.config.monthlyLimit} requests`,
      };
    }

    return { allowed: true };
  }

  recordRequest(): void {
    const now = Date.now();
    this.usage.perMinute.push(now);
    this.usage.daily.count++;
    this.usage.monthly.count++;
  }

  getUsageStats(): {
    daily: { used: number; limit: number; percent: number };
    monthly: { used: number; limit: number; percent: number };
  } {
    return {
      daily: {
        used: this.usage.daily.count,
        limit: this.config.dailyLimit,
        percent: (this.usage.daily.count / this.config.dailyLimit) * 100,
      },
      monthly: {
        used: this.usage.monthly.count,
        limit: this.config.monthlyLimit,
        percent: (this.usage.monthly.count / this.config.monthlyLimit) * 100,
      },
    };
  }
}
```

### Step 5: Intelligent Sync Optimization
```typescript
// src/services/sync-optimizer.ts
export class SyncOptimizer {
  private lastSyncHashes = new Map<string, string>();

  // Only sync changed content
  async getChangedFiles(
    files: TFile[],
    vault: Vault
  ): Promise<TFile[]> {
    const changed: TFile[] = [];

    for (const file of files) {
      const content = await vault.cachedRead(file);
      const hash = await this.hashContent(content);
      const lastHash = this.lastSyncHashes.get(file.path);

      if (hash !== lastHash) {
        changed.push(file);
        this.lastSyncHashes.set(file.path, hash);
      }
    }

    console.log(`[Sync] ${changed.length}/${files.length} files changed`);
    return changed;
  }

  private async hashContent(content: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(content);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('').substring(0, 16);
  }

  // Compress sync payload
  static prepareForSync(data: any): { payload: string; originalSize: number; compressedSize: number } {
    const original = JSON.stringify(data);
    const compressed = StorageOptimizer.compress(data);

    return {
      payload: compressed,
      originalSize: original.length,
      compressedSize: compressed.length,
    };
  }
}
```

## Output
- API request caching and deduplication
- Request batching for efficiency
- Storage compression and optimization
- Quota management with usage tracking
- Intelligent sync with change detection

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Quota exceeded | Too many requests | Implement rate limiting |
| High storage costs | Uncompressed data | Apply compression |
| Slow sync | Full sync every time | Use delta sync |
| API costs high | No caching | Add request caching |

## Examples

### Usage Dashboard Component
```typescript
class UsageDashboard {
  displayUsage(quotaManager: QuotaManager): HTMLElement {
    const container = document.createElement('div');
    const stats = quotaManager.getUsageStats();

    container.innerHTML = `
      <h4>API Usage</h4>
      <div class="usage-bar">
        <div class="usage-fill" style="width: ${stats.daily.percent}%"></div>
        <span>Daily: ${stats.daily.used}/${stats.daily.limit}</span>
      </div>
      <div class="usage-bar">
        <div class="usage-fill" style="width: ${stats.monthly.percent}%"></div>
        <span>Monthly: ${stats.monthly.used}/${stats.monthly.limit}</span>
      </div>
    `;

    return container;
  }
}
```

## Resources
- [API Rate Limiting Best Practices](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)
- [Data Compression Techniques](https://developer.mozilla.org/en-US/docs/Web/API/Compression_Streams_API)

## Next Steps
For architecture patterns, see `obsidian-reference-architecture`.
