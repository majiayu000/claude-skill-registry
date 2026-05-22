---
name: observability-instrument-with-otel
description: |
  Adds OpenTelemetry instrumentation to service methods by applying @traced decorators, structured logging,
  and trace/span ID propagation for distributed tracing. Use when adding new service methods, debugging
  complex flows, investigating performance issues, or need distributed tracing across application layers.
  Triggers on "add tracing", "instrument this method", "add observability", "debug with traces", or
  "track execution flow".
allowed-tools:
  - Read
  - Grep
  - Edit
  - Bash
---

# Instrument with OpenTelemetry

## Purpose
Add OpenTelemetry (OTEL) instrumentation to service methods for distributed tracing, structured logging, and observability across Clean Architecture layers.

## When to Use

Use this skill when:
- Adding new service methods that need observability
- Debugging complex execution flows across layers
- Investigating performance issues or bottlenecks
- Need distributed tracing for multi-service operations
- Adding structured logging with trace correlation
- Instrumenting Application, Infrastructure, or Interface layers
- Replacing print() statements with proper logging
- Tracking operations across method boundaries

## Table of Contents

### Core Sections

- [Quick Start](#quick-start)
  - Simple example to get started immediately
- [Instructions](#instructions)
  - [Step 1: Import OTEL Components](#step-1-import-otel-components)
  - [Step 2: Get Logger Instance](#step-2-get-logger-instance)
  - [Step 3: Apply @traced Decorator](#step-3-apply-traced-decorator)
  - [Step 4: Add Structured Logging](#step-4-add-structured-logging)
  - [Step 5: Add Manual Spans for Complex Operations (Optional)](#step-5-add-manual-spans-for-complex-operations-optional)
  - [Step 6: Add Correlation Context for Request Tracking (Optional)](#step-6-add-correlation-context-for-request-tracking-optional)
  - [Step 7: Verify Instrumentation](#step-7-verify-instrumentation)
- [Examples](#examples)
  - [Example 1: Add Tracing to Command Handler](#example-1-add-tracing-to-command-handler)
  - [Example 2: Add Tracing to Infrastructure Service](#example-2-add-tracing-to-infrastructure-service)
  - [Example 3: Add Manual Spans for Performance Tracking](#example-3-add-manual-spans-for-performance-tracking)
  - [Example 4: Add Correlation Context for Multi-File Operations](#example-4-add-correlation-context-for-multi-file-operations)

### Advanced Topics

- [Common Patterns](#common-patterns)
  - [Pattern 1: Service Method Instrumentation](#pattern-1-service-method-instrumentation)
  - [Pattern 2: Error Logging with Trace Context](#pattern-2-error-logging-with-trace-context)
  - [Pattern 3: Multi-Step Operation Tracking](#pattern-3-multi-step-operation-tracking)
- [Observability Best Practices](#observability-best-practices)
  - Guidelines for effective instrumentation
- [Troubleshooting](#troubleshooting)
  - [Logs Missing Trace IDs](#logs-missing-trace-ids)
  - [@traced Not Working on Async Methods](#traced-not-working-on-async-methods)
  - [Span Attributes Not Appearing](#span-attributes-not-appearing)
- [Requirements](#requirements)
  - Dependencies and prerequisites

### Supporting Resources

- [references/reference.md](./references/reference.md) - Advanced OTEL configuration
- [ARCHITECTURE.md](/Users/dawiddutoit/projects/play/project-watch-mcp/ARCHITECTURE.md) - Clean Architecture layers
- Core monitoring module: `src/project_watch_mcp/core/monitoring/`

### Utility Scripts

- [scripts/add_tracing.py](./scripts/add_tracing.py) - Auto-add OpenTelemetry instrumentation to service files
- [scripts/analyze_traces.py](./scripts/analyze_traces.py) - Analyze trace coverage in Python service files
- [scripts/validate_instrumentation.py](./scripts/validate_instrumentation.py) - Validate OTEL instrumentation patterns

## Quick Start
Add OTEL tracing to a service method:
```python
from project_watch_mcp.core.monitoring import get_logger, traced

logger = get_logger(__name__)

class MyService:
    @traced
    async def my_method(self, param: str) -> ServiceResult[Data]:
        logger.info(f"Processing {param}")
        # Method implementation
        return ServiceResult.ok(result)
```

## Instructions

### Step 1: Import OTEL Components
Add imports at the top of your file (fail-fast principle):
```python
from project_watch_mcp.core.monitoring import get_logger, traced
```

For advanced instrumentation (context management, correlation IDs):
```python
from project_watch_mcp.core.monitoring import (
    get_logger,
    traced,
    trace_span,
    correlation_context,
    add_context,
)
```

### Step 2: Get Logger Instance
Replace any existing logger initialization with OTEL logger:
```python
logger = get_logger(__name__)
```

**Why:** OTEL logger automatically includes trace_id, span_id, and correlation IDs in all log messages.

### Step 3: Apply @traced Decorator
Add `@traced` decorator to methods you want to trace:

**For Application Layer (Commands/Queries):**
```python
class IndexFileHandler(CommandHandler[IndexFileCommand]):
    @traced
    async def handle(self, command: IndexFileCommand) -> ServiceResult[None]:
        logger.info(f"Indexing file: {command.file_path}")
        # Implementation
```

**For Infrastructure Services:**
```python
class EmbeddingService:
    @traced
    async def generate_embeddings(self, texts: list[str]) -> ServiceResult[list[float]]:
        logger.info(f"Generating embeddings for {len(texts)} texts")
        # Implementation
```

**For MCP Tools (Interface Layer):**
```python
@traced
async def search_code(query: str, search_type: str = "semantic") -> dict:
    logger.info(f"Search request: query='{query}', type={search_type}")
    # Implementation
```

### Step 4: Add Structured Logging
Use logger with contextual information (avoid magic numbers, use clear descriptions):

**Good Examples:**
```python
logger.info(f"Processing file: {file_path}")
logger.debug(f"Query execution time: {elapsed_ms}ms")
logger.warning(f"Retry attempt {attempt}/{max_retries} failed")
logger.error(f"Failed to connect to Neo4j: {str(e)}")
```

**What @traced Automatically Adds:**
- `trace_id`: Distributed tracing ID (propagated across services)
- `span_id`: Current operation ID (unique per method call)
- Function name as span name (e.g., `IndexFileHandler.handle`)
- Function arguments as span attributes (primitives only)

### Step 5: Add Manual Spans for Complex Operations (Optional)
For fine-grained tracing within a method:
```python
@traced
async def complex_operation(self, data: Data) -> ServiceResult[Result]:
    logger.info("Starting complex operation")

    # Manual span for specific sub-operation
    with trace_span("validate_data", data_size=len(data)) as span:
        logger.info("Validating data")
        validation_result = await self._validate(data)
        span.set_attribute("validation_passed", validation_result.success)

    # Another manual span
    with trace_span("process_chunks", chunk_count=10) as span:
        logger.info("Processing chunks")
        results = await self._process_chunks(data)
        span.set_attribute("chunks_processed", len(results))

    return ServiceResult.ok(results)
```

### Step 6: Add Correlation Context for Request Tracking (Optional)
For tracking operations across multiple method calls:
```python
async def index_repository(self, repo_path: str) -> ServiceResult[None]:
    with correlation_context() as cid:
        logger.info(f"Starting repository indexing: {repo_path}")

        # All subsequent logs will include this correlation_id
        for file_path in files:
            await self.index_file(file_path)  # Logs include same correlation_id

        logger.info("Repository indexing complete")
```

### Step 7: Verify Instrumentation
Run tests to ensure tracing works:
```bash
uv run pytest tests/path/to/test.py -v
```

Check logs for trace/span IDs:
```bash
tail -f logs/project-watch-mcp.log | grep "trace:"
```

Expected log format:
```
2025-10-18 14:30:45 - [trace:a1b2c3d4 | span:e5f6g7h8] - module.name - INFO - Processing file
```

## Examples

### Example 1: Add Tracing to Command Handler
**Before:**
```python
class IndexFileHandler(CommandHandler[IndexFileCommand]):
    async def handle(self, command: IndexFileCommand) -> ServiceResult[None]:
        print(f"Indexing {command.file_path}")
        return await self._index(command)
```

**After:**
```python
from project_watch_mcp.core.monitoring import get_logger, traced

logger = get_logger(__name__)

class IndexFileHandler(CommandHandler[IndexFileCommand]):
    @traced
    async def handle(self, command: IndexFileCommand) -> ServiceResult[None]:
        logger.info(f"Indexing file: {command.file_path}")
        return await self._index(command)
```

### Example 2: Add Tracing to Infrastructure Service
**Before:**
```python
class Neo4jCodeRepository:
    async def save_file(self, file: File) -> bool:
        logging.info("Saving file")
        # Implementation
```

**After:**
```python
from project_watch_mcp.core.monitoring import get_logger, traced

logger = get_logger(__name__)

class Neo4jCodeRepository:
    @traced
    async def save_file(self, file: File) -> ServiceResult[None]:
        logger.info(f"Saving file to Neo4j: {file.path}")
        # Implementation
        return ServiceResult.ok(None)
```

### Example 3: Add Manual Spans for Performance Tracking
```python
from project_watch_mcp.core.monitoring import get_logger, traced, trace_span

logger = get_logger(__name__)

class EmbeddingService:
    @traced
    async def batch_generate(self, texts: list[str]) -> ServiceResult[list[Embedding]]:
        logger.info(f"Batch generating embeddings for {len(texts)} texts")

        # Track API call performance
        with trace_span("voyage_api_call", text_count=len(texts)) as span:
            logger.debug("Calling Voyage AI API")
            embeddings = await self.client.embed(texts)
            span.set_attribute("embeddings_generated", len(embeddings))

        # Track storage performance
        with trace_span("store_embeddings", embedding_count=len(embeddings)) as span:
            logger.debug("Storing embeddings in Neo4j")
            await self.repository.save_embeddings(embeddings)
            span.set_attribute("storage_success", True)

        return ServiceResult.ok(embeddings)
```

### Example 4: Add Correlation Context for Multi-File Operations
```python
from project_watch_mcp.core.monitoring import get_logger, traced, correlation_context

logger = get_logger(__name__)

class RepositoryIndexer:
    @traced
    async def index_repository(self, repo_path: str) -> ServiceResult[None]:
        # Generate correlation ID for this indexing operation
        with correlation_context() as cid:
            logger.info(f"Starting repository indexing: {repo_path} (correlation_id: {cid})")

            files = await self.discover_files(repo_path)
            logger.info(f"Discovered {len(files)} files to index")

            for file_path in files:
                # All logs from index_file will include same correlation_id
                await self.index_file_handler.handle(IndexFileCommand(file_path))

            logger.info(f"Repository indexing complete: {len(files)} files processed")

        return ServiceResult.ok(None)
```

## Requirements
- OpenTelemetry initialized (handled by `initialize_otel_logger()` in core/monitoring)
- Python 3.11+ (for modern type hints)
- Async/await support for async methods
- ServiceResult pattern used for return types
- Access to `project_watch_mcp.core.monitoring` module

## Common Patterns

### Pattern 1: Service Method Instrumentation
```python
from project_watch_mcp.core.monitoring import get_logger, traced

logger = get_logger(__name__)

class MyService:
    @traced
    async def operation(self, param: str) -> ServiceResult[Data]:
        logger.info(f"Starting operation with param: {param}")
        result = await self._execute(param)
        logger.info(f"Operation completed successfully")
        return ServiceResult.ok(result)
```

### Pattern 2: Error Logging with Trace Context
```python
@traced
async def risky_operation(self) -> ServiceResult[Data]:
    try:
        logger.info("Attempting risky operation")
        result = await self._risky_call()
        return ServiceResult.ok(result)
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}")
        return ServiceResult.fail(f"Operation failed: {str(e)}")
```

### Pattern 3: Multi-Step Operation Tracking
```python
@traced
async def multi_step_process(self, data: Data) -> ServiceResult[Result]:
    with trace_span("step_1_validation") as span:
        logger.info("Step 1: Validating input")
        validation = await self._validate(data)
        span.set_attribute("valid", validation.success)

    with trace_span("step_2_processing") as span:
        logger.info("Step 2: Processing data")
        processed = await self._process(data)
        span.set_attribute("items_processed", len(processed))

    with trace_span("step_3_storage") as span:
        logger.info("Step 3: Storing results")
        await self._store(processed)
        span.set_attribute("items_stored", len(processed))

    return ServiceResult.ok(processed)
```

## Observability Best Practices
1. **Always use @traced on public methods** - Commands, Queries, Services
2. **Never use print() statements** - Use logger instead (fail-fast principle)
3. **Add context to logs** - Include relevant parameters, counts, durations
4. **Use trace_span for expensive operations** - API calls, database queries, file I/O
5. **Use correlation_context for request tracking** - Multi-file operations, batch processing
6. **Log at appropriate levels** - DEBUG (detailed), INFO (milestones), WARNING (degraded), ERROR (failures)
7. **Avoid logging sensitive data** - API keys, passwords, PII
8. **Set span attributes for metrics** - Counts, durations, success/failure indicators

## Troubleshooting

### Logs Missing Trace IDs
**Issue:** Logs don't show `[trace:... | span:...]`

**Solution:** Ensure OTEL is initialized before any logging:
```python
from project_watch_mcp.core.monitoring import initialize_otel_logger

initialize_otel_logger()  # Call once at application startup
```

### @traced Not Working on Async Methods
**Issue:** Decorator doesn't capture spans for async methods

**Solution:** The `@traced` decorator handles both sync and async automatically. Ensure you're using `async def`:
```python
@traced
async def my_method(self):  # ✅ Works
    pass

@traced
def my_method(self):  # ✅ Also works for sync
    pass
```

### Span Attributes Not Appearing
**Issue:** Custom attributes not visible in traces

**Solution:** Use `span.set_attribute()` within the span context:
```python
with trace_span("operation") as span:
    span.set_attribute("key", "value")  # ✅ Correct
```

## See Also
- [references/reference.md](./references/reference.md) - Advanced OTEL configuration
- [ARCHITECTURE.md](/Users/dawiddutoit/projects/play/project-watch-mcp/ARCHITECTURE.md) - Clean Architecture layers
- Core monitoring module: `src/project_watch_mcp/core/monitoring/`
