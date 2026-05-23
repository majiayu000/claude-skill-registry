---
name: Ceres
description: Use when working with Ceres — a Rust semantic search engine for open data portals that harvests CKAN metadata and indexes it with vector embeddings (pgvector). Covers CLI commands (harvest, search, export, stats), REST API endpoints, portal configuration (portals.toml), embedding providers (Gemini, OpenAI), architecture, extending via traits, and contributing to the Ceres codebase.
---

# Ceres — Semantic Search Engine for Open Data Portals

Ceres harvests metadata from CKAN open data portals and indexes them with vector embeddings, enabling semantic search across fragmented data sources.

**Repository:** https://github.com/AndreaBozzo/Ceres
**License:** Apache-2.0 | **Rust edition:** 2024 | **MSRV:** 1.88+

## Pipeline

```
Metadata:  Portal URL → PortalClient (fetch) → DeltaDetector (content_hash) → DatasetStore (upsert, no embedding)
Embedding: DatasetStore (pending) → EmbeddingProvider (vector) → DatasetStore (update embedding)
Combined:  HarvestPipeline = HarvestService + EmbeddingService
```

Harvesting and embedding are decoupled: `HarvestService` handles metadata (no API key needed with `--metadata-only`), `EmbeddingService` handles vectors, and `HarvestPipeline` composes both. Each stage is a trait, so every component can be swapped or mocked independently.

## Crate Map

| Crate | Purpose | Key Exports |
|---|---|---|
| `ceres-core` | Business logic, traits, services | `HarvestService`, `EmbeddingService`, `HarvestPipeline`, `SearchService`, `ExportService`, `WorkerService`, `CircuitBreaker`, traits |
| `ceres-client` | CKAN API client, Gemini/OpenAI clients | `CkanClient`, `GeminiClient`, `OpenAIClient`, `PortalClientFactoryEnum`, `EmbeddingProviderEnum` |
| `ceres-db` | PostgreSQL + pgvector repository | `DatasetRepository`, `HarvestJobRepository` |
| `ceres-server` | Axum REST API with Swagger UI | Routes, DTOs, bearer auth, OpenAPI/Swagger |
| `ceres-cli` | Command-line interface | `harvest`, `embed`, `search`, `export`, `stats` subcommands |

## Core Traits (`ceres-core::traits`)

```rust
pub trait EmbeddingProvider: Send + Sync + Clone {
    fn name(&self) -> &'static str;
    fn dimension(&self) -> usize;
    fn generate(&self, text: &str) -> impl Future<Output = Result<Vec<f32>, AppError>> + Send;
    fn max_batch_size(&self) -> usize { 1 }
    fn generate_batch(&self, texts: &[String]) -> impl Future<Output = Result<Vec<Vec<f32>>, AppError>> + Send;
}

pub trait PortalClient: Send + Sync + Clone {
    type PortalData: Send;
    fn portal_type(&self) -> &'static str;
    fn base_url(&self) -> &str;
    fn list_dataset_ids(&self) -> impl Future<Output = Result<Vec<String>, AppError>> + Send;
    fn get_dataset(&self, id: &str) -> impl Future<Output = Result<Self::PortalData, AppError>> + Send;
    fn into_new_dataset(data: Self::PortalData, portal_url: &str, url_template: Option<&str>, language: &str) -> NewDataset;
    fn search_modified_since(&self, since: DateTime<Utc>) -> impl Future<Output = Result<Vec<Self::PortalData>, AppError>> + Send;
    fn search_all_datasets(&self) -> impl Future<Output = Result<Vec<Self::PortalData>, AppError>> + Send;
}

pub trait PortalClientFactory: Send + Sync + Clone {
    type Client: PortalClient;
    fn create(&self, portal_url: &str, portal_type: PortalType) -> Result<Self::Client, AppError>;
}

pub trait DatasetStore: Send + Sync + Clone {
    fn get_by_id(&self, id: Uuid) -> impl Future<Output = Result<Option<Dataset>, AppError>> + Send;
    fn get_hashes_for_portal(&self, portal_url: &str) -> impl Future<Output = Result<HashMap<String, Option<String>>, AppError>> + Send;
    fn upsert(&self, dataset: &NewDataset) -> impl Future<Output = Result<Uuid, AppError>> + Send;
    fn batch_upsert(&self, datasets: &[NewDataset]) -> impl Future<Output = Result<Vec<Uuid>, AppError>> + Send;
    fn search(&self, query_vector: Vec<f32>, limit: usize) -> impl Future<Output = Result<Vec<SearchResult>, AppError>> + Send;
    fn list_stream<'a>(&'a self, portal_filter: Option<&'a str>, limit: Option<usize>) -> BoxStream<'a, Result<Dataset, AppError>>;
    fn get_last_sync_time(&self, portal_url: &str) -> impl Future<Output = Result<Option<DateTime<Utc>>, AppError>> + Send;
    fn record_sync_status(&self, portal_url: &str, sync_time: DateTime<Utc>, sync_mode: &str, sync_status: &str, datasets_synced: i32) -> impl Future<Output = Result<(), AppError>> + Send;
    fn health_check(&self) -> impl Future<Output = Result<(), AppError>> + Send;
    // + update_timestamp_only, batch_update_timestamps, get_duplicate_titles
    // Stale detection
    fn mark_stale_datasets(&self, portal_url: &str, sync_start: DateTime<Utc>) -> impl Future<Output = Result<u64, AppError>> + Send;
    fn mark_stale_by_exclusion(&self, portal_url: &str, seen_ids: &[String]) -> impl Future<Output = Result<u64, AppError>> + Send;
    // Pending embeddings
    fn list_pending_embeddings(&self, portal_filter: Option<&str>, limit: usize) -> impl Future<Output = Result<Vec<Dataset>, AppError>> + Send;
}
```

## Key Types

| Type | Module | Purpose |
|---|---|---|
| `Dataset` | `ceres_core::models` | Complete dataset row (id, original_id, source_portal, url, title, description, embedding, metadata, timestamps, content_hash, is_stale) |
| `NewDataset` | `ceres_core::models` | Insert/update DTO. Has `compute_content_hash()` for delta detection |
| `SearchResult` | `ceres_core::models` | Dataset + similarity_score (0.0-1.0) |
| `DatabaseStats` | `ceres_core::models` | total_datasets, datasets_with_embeddings, stale_datasets, total_portals, last_update |
| `HarvestJob` | `ceres_core::job` | Queued harvest job with status, retry info, portal config |
| `JobStatus` | `ceres_core::job` | Enum: Pending, Running, Completed, Failed, Cancelled |
| `SyncStats` | `ceres_core::sync` | created, updated, unchanged, failed, skipped counts |
| `SyncOutcome` | `ceres_core::sync` | Per-dataset outcome: Created, Updated, Unchanged, Failed, Skipped |
| `BatchHarvestSummary` | `ceres_core::sync` | Aggregated results from batch harvesting multiple portals |
| `PortalEntry` | `ceres_core::config` | Portal config: name, url, type, enabled, url_template, language |
| `AppError` | `ceres_core::error` | Error enum with `is_retryable()` and `should_trip_circuit()` |
| `EmbeddingStats` | `ceres_core::embedding` | embedded, failed, skipped, total counts from an embedding run |
| `HarvestPipeline` | `ceres_core::pipeline` | Composes HarvestService + EmbeddingService for combined harvest-then-embed |
| `CircuitBreaker` | `ceres_core::circuit_breaker` | Closed -> Open -> HalfOpen state machine |

## Quick Start

```bash
# Install
cargo install ceres-search

# Start PostgreSQL + pgvector
docker compose up db -d

# Configure
cp .env.example .env  # Edit with your Gemini/OpenAI API key

# Run migrations
make migrate

# Harvest a portal
ceres harvest https://dati.comune.milano.it

# Harvest all configured portals
ceres harvest

# Search
ceres search "trasporto pubblico" --limit 5

# Export
ceres export --format jsonl > datasets.jsonl

# Stats
ceres stats
```

## Reference Guides

| Topic | File | When to Read |
|---|---|---|
| Architecture deep-dive | `references/architecture.md` | Understanding crate graph, services, error handling, database schema |
| CLI & REST API | `references/cli-and-server.md` | Running CLI commands, calling API endpoints, env vars, deployment |
| Harvesting system | `references/harvesting.md` | Two-tier optimization, delta detection, streaming, circuit breaker |
| Extending Ceres | `references/extending.md` | Implementing custom EmbeddingProvider, PortalClient, or DatasetStore |
| Contributing | `references/contributing.md` | Dev setup, testing, CI, code style |

## Version Notes

- **Current version:** 0.3.1
- **crates.io package:** `ceres-search`
- Harvesting and embedding are decoupled: `--metadata-only` harvests without API key, `embed` command generates embeddings separately
- Stale dataset detection: datasets removed from portals are soft-marked (`is_stale`) during full syncs
- Supports Gemini (768d, `gemini-embedding-001`) and OpenAI (1536d/3072d, `text-embedding-3-small`/`large`) embeddings
- 25+ pre-configured CKAN portals (354k+ datasets)
- HuggingFace dataset: `AndreaBozzo/ceres-open-data-index`
