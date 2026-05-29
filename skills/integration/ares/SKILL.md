---
name: Ares
description: Use when working with the Ares web scraper — an LLM-powered Rust tool that extracts structured data from websites using JSON Schemas. Covers library usage, CLI commands, REST API, schema creation, adding custom fetchers/cleaners/extractors, deployment, and contributing to the Ares codebase.
---

# Ares — LLM-Powered Web Scraper

Ares is a Rust library, CLI, and HTTP server that extracts structured data from websites using LLMs and JSON Schemas.

**Repository:** https://github.com/AndreaBozzo/Ares
**License:** Apache-2.0 | **Rust edition:** 2024 | **MSRV:** 1.88+

## Pipeline

```
URL → Fetcher (HTML) → Cleaner (Markdown) → Extractor (LLM + JSON Schema) → Hash → Compare → Store
```

Each stage is a trait, so every component can be swapped or mocked independently.

## Crate Map

| Crate | Purpose | Key Exports |
|---|---|---|
| `ares-core` | Business logic, traits, pipeline | `ScrapeService`, `WorkerService`, `CircuitBreaker`, `ThrottledFetcher`, traits |
| `ares-client` | HTTP/browser fetchers, cleaner, LLM client | `ReqwestFetcher`, `BrowserFetcher`, `HtmdCleaner`, `OpenAiExtractor` |
| `ares-db` | PostgreSQL persistence | `Database`, `ExtractionRepository`, `ScrapeJobRepository` |
| `ares-api` | Axum REST API | Routes, DTOs, bearer auth, OpenAPI/Swagger |
| `ares-cli` | Command-line interface | `scrape`, `history`, `job`, `worker` subcommands |

## Core Traits (`ares-core::traits`)

```rust
pub trait Fetcher: Send + Sync + Clone {
    fn fetch(&self, url: &str) -> impl Future<Output = Result<String, AppError>> + Send;
}

pub trait Cleaner: Send + Sync + Clone {
    fn clean(&self, html: &str) -> Result<String, AppError>;
}

pub trait Extractor: Send + Sync + Clone {
    fn extract(&self, content: &str, schema: &serde_json::Value)
        -> impl Future<Output = Result<serde_json::Value, AppError>> + Send;
}

pub trait ExtractorFactory: Send + Sync + Clone {
    type Extractor: Extractor;
    fn create(&self, model: &str, base_url: &str) -> Result<Self::Extractor, AppError>;
}

pub trait ExtractionStore: Send + Sync + Clone {
    fn save(&self, extraction: &NewExtraction) -> impl Future<Output = Result<Uuid, AppError>> + Send;
    fn get_latest(&self, url: &str, schema_name: &str) -> impl Future<Output = Result<Option<Extraction>, AppError>> + Send;
    fn get_history(&self, url: &str, schema_name: &str, limit: usize, offset: usize) -> impl Future<Output = Result<Vec<Extraction>, AppError>> + Send;
}
```

`JobQueue` trait: see `ares-core::job_queue` — persistent queue with atomic claiming (`SELECT FOR UPDATE SKIP LOCKED`).

## Key Types

| Type | Module | Purpose |
|---|---|---|
| `Extraction` | `ares_core::models` | Completed extraction (id, url, schema_name, extracted_data, hashes, model, created_at) |
| `NewExtraction` | `ares_core::models` | Insert DTO (no id/timestamps) |
| `ScrapeResult` | `ares_core::models` | Pipeline output (extracted_data, hashes, changed flag, extraction_id) |
| `ScrapeJob` | `ares_core::job` | Queued job with status, retry info, LLM config |
| `JobStatus` | `ares_core::job` | Enum: Pending, Running, Completed, Failed, Cancelled |
| `RetryConfig` | `ares_core::job` | Exponential backoff: 1min → 5min → 30min → 60min (capped) |
| `WorkerConfig` | `ares_core::job` | Worker settings: poll_interval, retry_config, skip_unchanged |
| `AppError` | `ares_core::error` | Error enum with `is_retryable()` and `should_trip_circuit()` |
| `SchemaResolver` | `ares_core::schema` | CRUD for schemas: resolve, create, update, delete + registry management |
| `CircuitBreaker` | `ares_core::circuit_breaker` | Closed → Open → HalfOpen state machine |
| `ThrottledFetcher<F>` | `ares_core::throttle` | Per-domain delay with jitter |

## Quick Start (Library Usage)

```rust
use ares_client::{ReqwestFetcher, HtmdCleaner, OpenAiExtractor};
use ares_core::{ScrapeService, NullStore};

let fetcher = ReqwestFetcher::new()?;
let cleaner = HtmdCleaner::new();
let extractor = OpenAiExtractor::with_base_url(&api_key, "gpt-4o-mini", "https://api.openai.com/v1")?;

let service = ScrapeService::<_, _, _, NullStore>::new(fetcher, cleaner, extractor, "gpt-4o-mini".into());

let schema = serde_json::json!({
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"}
    },
    "required": ["title", "author"]
});

let result = service.scrape("https://example.com/blog", &schema, "blog").await?;
println!("{}", serde_json::to_string_pretty(&result.extracted_data)?);
```

With persistence, use `ScrapeService::with_store(fetcher, cleaner, extractor, store, model)`.

## Reference Guides

| Topic | File | When to Read |
|---|---|---|
| Architecture deep-dive | `references/architecture.md` | Understanding pipeline internals, crate dependencies, resilience patterns |
| JSON Schema system | `references/schemas.md` | Creating/managing schemas, registry, versioning |
| Extending Ares | `references/extending.md` | Implementing custom Fetcher/Cleaner/Extractor/Store/JobQueue |
| CLI & REST API | `references/cli-and-server.md` | Running CLI commands, calling API endpoints, deploying |
| Contributing | `references/contributing.md` | Dev setup, testing, CI, code style |

## Version Notes

- **Current version:** 0.1.0
- **crates.io release:** Scheduled for February 29, 2026
- Until then, use git dependency: `ares-core = { git = "https://github.com/AndreaBozzo/Ares" }`
- Works with any OpenAI-compatible API (OpenAI, Gemini, etc.)
- Browser support requires feature flag: `--features browser`
