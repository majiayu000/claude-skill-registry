---
name: cfn-transparency-middleware
description: "Agent interaction capture, logging, and analysis with memory tracking and security (Rust implementation). Use when you need to capture and analyze agent interactions, track tool usage and performance metrics, query execution history, or export audit trails for compliance."
version: 1.0.0
tags: [middleware, logging, security, transparency, memory, rust]
status: production
---

## Transparency Middleware (Rust Implementation)

### Overview
The Transparency Middleware is a critical component of our agent orchestration system, designed to capture, log, and analyze agent interactions with comprehensive memory tracking and security features. This implementation uses Rust for high performance and memory safety.

### Architecture

#### Core Components

1. **Memory Schema** (`src/memory_schema.rs`)
   - Defines data structures for agent interactions
   - Event types: AgentExecution, ToolUsage, Error, Edit, Bash
   - Query builder for flexible filtering

2. **Memory Repository** (`src/memory_repository.rs`)
   - SQLite backend for persistent storage
   - Async operations for performance
   - Automatic table creation and indexing

3. **Memory Query** (`src/memory_query.rs`)
   - Builder pattern for constructing queries
   - Filtering by agent, task, time, event type
   - Pagination and sorting support

4. **Main Library** (`src/lib.rs`)
   - Core middleware implementation
   - Configuration management
   - Data sanitization and security filtering

### Usage

#### Initialize Middleware

```rust
use transparency_middleware::{TransparencyMiddleware, TransparencyConfig};

// Load configuration
let config = TransparencyConfig::load_config("config.json")?;

// Create middleware instance
let mut middleware = TransparencyMiddleware::new(config);

// Initialize database connection
middleware.initialize().await?;

// Set agent ID for tracking
middleware.set_agent_id("my-agent-id".to_string());
```

#### Capture Agent Interactions

```rust
// Capture agent execution
middleware.capture_agent_execution(
    "backend-dev",
    "Agent output and results...",
    "task-123"
).await?;

// Get performance metrics
let metrics = middleware.get_metrics().await?;
println!("Total entries: {}", metrics.total_entries);
```

#### Query Stored Data

```rust
use transparency_middleware::{MemoryQuery, QueryBuilder};

let query = QueryBuilder::new()
    .agent_id("my-agent-id")
    .event_type(EventType::ToolUsage)
    .limit(100)
    .build();

let entries = middleware.query(query).await?;
for entry in entries {
    println!("{}: {}", entry.timestamp, entry.event_type);
}
```

#### Export Data

```rust
use transparency_middleware::ExportFormat;

// Export to JSON
middleware.export_data(ExportFormat::Json, "export.json").await?;

// Export to CSV
middleware.export_data(ExportFormat::Csv, "export.csv").await?;
```

### Shell Scripts

The skill includes shell scripts for common operations:

#### invoke-transparency-init.sh
Initialize a new transparency tracking session.

```bash
./invoke-transparency-init.sh \
  --level detailed \
  --performance-monitoring yes \
  --context-filtering yes \
  --max-overhead 5 \
  --task-id my-task-123
```

#### invoke-transparency-observe.sh
Observe agent interactions in real-time.

```bash
./invoke-transparency-observe.sh \
  --agent-id my-agent \
  --real-time yes \
  --format json
```

#### invoke-transparency-filter.sh
Filter and analyze captured interactions.

```bash
./invoke-transparency-filter.sh \
  --agent-id my-agent \
  --start-time "2024-01-01T00:00:00Z" \
  --end-time "2024-01-02T00:00:00Z" \
  --event-type tool_usage
```

#### invoke-transparency-metrics.sh
Get performance and usage metrics.

```bash
./invoke-transparency-metrics.sh \
  --agent-id my-agent \
  --output json
```

#### invoke-transparency-stop.sh
Stop tracking and cleanup.

```bash
./invoke-transparency-stop.sh \
  --agent-id my-agent \
  --task-id my-task-123 \
  --cleanup yes
```

## Testing

### Unit Tests
Run the comprehensive unit test suite:

```bash
cd .claude/skills/cfn-transparency-middleware
cargo test
```

### Integration Tests
Test middleware with CFN Loop orchestrator:

```bash
./.claude/skills/cfn-transparency-middleware/test-e2e.sh
```

### End-to-End Tests
Full lifecycle test with sample agent:

```bash
./.claude/skills/cfn-transparency-middleware/test-e2e.sh
```

### Performance Benchmarks
Measure performance impact:

```bash
./.claude/skills/cfn-transparency-middleware/performance-benchmark.sh
```

## Configuration

### Transparency Levels

1. **Minimal**: Only critical events (errors, task completion)
2. **Detailed**: All tool usage and state changes
3. **Verbose**: Includes raw inputs/outputs
4. **Debug**: Full execution trace with timing

### Security Settings

- **Message Filtering**: Redacts sensitive data patterns
- **Context Filtering**: Filters based on operation context
- **Performance Limits**: Enforces maximum overhead percentage
- **Size Limits**: Caps payload sizes to prevent bloat

### Performance Settings

- **Queue Size**: Buffer size for async operations (default: 1000)
- **Flush Interval**: How often to write to disk (default: 5000ms)
- **Max Overhead**: Maximum performance impact (default: 5%)

## Security Considerations

### Data Redaction
The middleware automatically redacts sensitive information using configurable patterns:
- Passwords, tokens, secrets
- API keys and private keys
- Custom patterns can be added

### Access Control
- Database files should have restricted permissions (600)
- Export files inherit standard file permissions
- In-memory data is cleared on cleanup

### Auditing
- All configuration changes are logged
- Data access through queries is tracked
- Export operations are recorded

## Performance

### Benchmarks
- **Throughput**: 10,000+ events/second
- **Latency**: < 1ms average overhead
- **Memory**: < 50MB baseline
- **Storage**: Efficient SQLite with indexes

### Optimization Tips
1. Use `async_logging` for high-throughput scenarios
2. Adjust `queue_size` based on load
3. Set appropriate `flush_interval_ms` for your use case
4. Enable `compression_enabled` for large datasets

## Troubleshooting

### Database Issues
```bash
# Check database file permissions
ls -la transparency-middleware.db

# Rebuild corrupted database
rm transparency-middleware.db
# Initialize again with invoke-transparency-init.sh
```

### Performance Issues
```bash
# Check metrics for bottlenecks
./invoke-transparency-metrics.sh --agent-id my-agent --output json

# Adjust configuration if overhead > 5%
# Increase flush_interval_ms or enable async_logging
```

### Missing Events
1. Verify transparency level is appropriate
2. Check exclude_patterns aren't too broad
3. Ensure agent_id matches exactly
4. Review message filtering configuration

## Integration with CFN Loops

### CLI Integration
The middleware can be integrated into CFN Loop execution:

```bash
# Wrap agent execution with transparency
./invoke-transparency-init.sh --task-id $TASK_ID
# ... run agent commands ...
./invoke-transparency-stop.sh --task-id $TASK_ID
```

### Memory Repository Access
Agents can query the transparency log:

```rust
let query = QueryBuilder::new()
    .task_id("current-task")
    .build();

let history = middleware.query(query).await?;
```

## File Structure

```
.claude/skills/cfn-transparency-middleware/
├── src/
│   ├── lib.rs              # Main middleware implementation
│   ├── main.rs             # CLI binary
│   ├── memory_schema.rs    # Data structures
│   ├── memory_repository.rs # Database operations
│   └── memory_query.rs     # Query builder
├── Cargo.toml              # Rust dependencies
├── config.json             # Default configuration
├── invoke-*.sh             # Shell scripts
├── README.md               # User documentation
├── SKILL.md                # This file
└── test-e2e.sh             # End-to-end tests
```

## Dependencies

### Runtime Dependencies
- `sqlx`: Async SQLite database access
- `tokio`: Async runtime
- `serde`: JSON serialization
- `chrono`: Date/time handling
- `tracing`: Structured logging
- `anyhow`: Error handling

### Development Dependencies
- `tempfile`: Test temporary files
- `mockall`: Mocking for tests

## License

MIT License - see LICENSE file for details.