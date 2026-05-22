---
name: feature-implement
description: Systematic approach to implementing new features in Rust memory systems
audience: developers
workflow: feature-development
---
# Feature Implementation

Systematic approach to implementing new features in the Rust memory system.

## Purpose
Add new functionality following project conventions, maintaining code quality and test coverage.

## Implementation Process

### Phase 1: Planning

#### 1. Understand Requirements
- What is the feature?
- Why is it needed?
- Who will use it?
- What are the acceptance criteria?

#### 2. Design Approach
- How does it fit into existing architecture?
- What modules need changes?
- What new modules are needed?
- What are the data structures?
- What are the API signatures?

#### 3. Check Constraints
- File size limit: ≤ 500 LOC per file
- Async/Tokio patterns for I/O
- Error handling with `anyhow::Result`
- Storage: Turso (durable) + redb (cache)

### Phase 2: Implementation

#### 1. Create Module Structure

```bash
# For new module
touch src/new_feature/mod.rs
touch src/new_feature/core.rs
touch src/new_feature/storage.rs

# Update src/lib.rs
# pub mod new_feature;
```

Example structure:
```
src/
├── new_feature/
│   ├── mod.rs          # Public API exports
│   ├── core.rs         # Core logic (<500 LOC)
│   ├── storage.rs      # Storage operations (<500 LOC)
│   └── types.rs        # Data structures (<500 LOC)
```

#### 2. Define Types

```rust
// src/new_feature/types.rs
use serde::{Deserialize, Serialize};

/// Feature data structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FeatureData {
    pub id: String,
    pub created_at: i64,
    pub data: serde_json::Value,
}

/// Configuration for feature
#[derive(Debug, Clone)]
pub struct FeatureConfig {
    pub enabled: bool,
    pub max_items: usize,
}
```

#### 3. Implement Core Logic

```rust
// src/new_feature/core.rs
use anyhow::Result;

/// Main feature implementation
pub struct Feature {
    config: FeatureConfig,
}

impl Feature {
    /// Create new feature instance
    pub fn new(config: FeatureConfig) -> Self {
        Self { config }
    }

    /// Core feature operation
    pub async fn process(&self, input: FeatureData) -> Result<FeatureData> {
        // Validate input
        self.validate(&input)?;

        // Process
        let processed = self.process_internal(input).await?;

        // Store result
        self.store(&processed).await?;

        Ok(processed)
    }

    fn validate(&self, data: &FeatureData) -> Result<()> {
        // Validation logic
        Ok(())
    }

    async fn process_internal(&self, data: FeatureData) -> Result<FeatureData> {
        // Processing logic
        Ok(data)
    }

    async fn store(&self, data: &FeatureData) -> Result<()> {
        // Storage logic
        Ok(())
    }
}
```

#### 4. Add Storage Layer

```rust
// src/new_feature/storage.rs
use super::types::FeatureData;
use anyhow::Result;

/// Turso storage for feature
pub struct FeatureStorage {
    turso: TursoClient,
}

impl FeatureStorage {
    pub async fn save(&self, data: &FeatureData) -> Result<()> {
        let sql = "INSERT OR REPLACE INTO feature_table (id, data, created_at) VALUES (?, ?, ?)";
        self.turso
            .execute(sql)
            .bind(&data.id)
            .bind(serde_json::to_string(&data.data)?)
            .bind(data.created_at)
            .await?;
        Ok(())
    }

    pub async fn get(&self, id: &str) -> Result<Option<FeatureData>> {
        let sql = "SELECT id, data, created_at FROM feature_table WHERE id = ?";
        let row = self.turso.query(sql).bind(id).await?;

        // Parse and return
        Ok(None) // Placeholder
    }
}
```

#### 5. Implement Public API

```rust
// src/new_feature/mod.rs
mod core;
mod storage;
mod types;

pub use types::{FeatureConfig, FeatureData};
pub use core::Feature;

/// Convenience function for common use case
pub async fn quick_process(data: FeatureData) -> anyhow::Result<FeatureData> {
    let feature = Feature::new(FeatureConfig::default());
    feature.process(data).await
}
```

### Phase 3: Testing

#### 1. Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_feature_creation() {
        let config = FeatureConfig {
            enabled: true,
            max_items: 100,
        };
        let feature = Feature::new(config);
        assert!(feature.config.enabled);
    }

    #[test]
    fn test_validation() {
        let feature = Feature::new(FeatureConfig::default());
        let data = FeatureData {
            id: "test".to_string(),
            created_at: 0,
            data: serde_json::json!({}),
        };
        assert!(feature.validate(&data).is_ok());
    }

    #[tokio::test]
    async fn test_process() {
        let feature = Feature::new(FeatureConfig::default());
        let input = create_test_data();
        let result = feature.process(input).await;
        assert!(result.is_ok());
    }
}
```

#### 2. Integration Tests

```rust
// tests/integration/feature_test.rs
use memory_core::new_feature::*;

#[tokio::test]
async fn test_end_to_end_feature() {
    // Setup
    let memory = create_test_memory().await;

    // Execute feature
    let data = FeatureData { /* ... */ };
    let result = memory.feature_operation(data).await;

    // Verify
    assert!(result.is_ok());

    // Check storage
    let stored = memory.get_feature_data("id").await.unwrap();
    assert_eq!(stored.id, "id");
}
```

### Phase 4: Integration

#### 1. Wire into Main API

```rust
// src/lib.rs
pub mod new_feature;

use new_feature::Feature;

pub struct SelfLearningMemory {
    // Existing fields...
    feature: Feature,
}

impl SelfLearningMemory {
    pub async fn feature_operation(&self, data: FeatureData) -> Result<FeatureData> {
        self.feature.process(data).await
    }
}
```

#### 2. Update Database Schema

```sql
-- migrations/003_add_feature_table.sql
CREATE TABLE IF NOT EXISTS feature_table (
    id TEXT PRIMARY KEY,
    data TEXT NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE INDEX idx_feature_created ON feature_table(created_at DESC);
```

#### 3. Add Configuration

```rust
// src/config.rs
pub struct Config {
    // Existing config...
    pub feature_config: FeatureConfig,
}
```

### Phase 5: Documentation

#### 1. Code Documentation

```rust
/// Process feature data through the memory system.
///
/// This function takes raw feature data, validates it, processes it according
/// to learned patterns, and stores the result in both Turso and redb.
///
/// # Arguments
///
/// * `data` - The feature data to process
///
/// # Returns
///
/// Processed feature data with enriched information
///
/// # Errors
///
/// Returns error if:
/// - Data validation fails
/// - Storage operations fail
/// - Processing encounters unrecoverable error
///
/// # Example
///
/// ```no_run
/// use memory_core::new_feature::*;
///
/// #[tokio::main]
/// async fn main() -> anyhow::Result<()> {
///     let data = FeatureData {
///         id: "example".to_string(),
///         created_at: 1234567890,
///         data: serde_json::json!({"key": "value"}),
///     };
///
///     let result = quick_process(data).await?;
///     println!("Processed: {:?}", result);
///     Ok(())
/// }
/// ```
pub async fn feature_operation(&self, data: FeatureData) -> Result<FeatureData>
```

#### 2. Update README

Add feature to main README.md:
```markdown
## Features

- Episodic memory storage
- Pattern extraction and learning
- Context retrieval
- **NEW: Feature name** - Brief description
```

### Phase 6: Quality Checks

```bash
# Format
cargo fmt

# Lint
cargo clippy --all -- -D warnings

# Build
cargo build --all

# Test
cargo test --all

# Documentation
cargo doc --no-deps
```

### Phase 7: Commit

```bash
# Stage changes
git add src/new_feature/ tests/integration/feature_test.rs

# Commit with clear message
git commit -m "[feature] add new_feature module

- Implemented core Feature struct with process logic
- Added Turso storage layer with save/get operations
- Created comprehensive unit and integration tests
- Updated main API to expose feature_operation
- Added database migration for feature_table

Closes: #123
"
```

## Best Practices

### Code Organization
- One feature per module
- Split large modules (< 500 LOC per file)
- Clear separation: types, core logic, storage, API

### Error Handling
```rust
// Good: Propagate errors
pub async fn operation(&self) -> Result<Data> {
    let data = self.fetch().await?;
    self.process(data).await?;
    Ok(data)
}

// Bad: Swallow errors
pub async fn operation(&self) -> Option<Data> {
    let data = self.fetch().await.ok()?;  // Error info lost
    Some(data)
}
```

### Async Patterns
```rust
// Good: Concurrent operations
let (result1, result2) = tokio::join!(
    operation1(),
    operation2(),
);

// Bad: Sequential when could be concurrent
let result1 = operation1().await;
let result2 = operation2().await;
```

### Testing
- Unit tests for each function
- Integration tests for workflows
- Test error cases
- Test edge cases (empty, max, invalid)

### Documentation
- Public APIs must be documented
- Include examples for complex APIs
- Document errors and edge cases
- Keep docs up to date with code

## Feature Checklist

- [ ] Requirements understood
- [ ] Design reviewed
- [ ] Module structure created
- [ ] Types defined
- [ ] Core logic implemented
- [ ] Storage layer added
- [ ] Public API exposed
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests added
- [ ] Documentation written
- [ ] Code formatted (`cargo fmt`)
- [ ] Lints pass (`cargo clippy`)
- [ ] All tests pass (`cargo test --all`)
- [ ] Build succeeds (`cargo build --release`)
- [ ] Committed with clear message
- [ ] PR created (if applicable)

## Common Pitfalls

### 1. Forgetting `.await`
```rust
// Wrong
let data = async_function();  // Returns Future, not Data

// Right
let data = async_function().await?;
```

### 2. Blocking in Async Context
```rust
// Wrong
async fn process() {
    std::thread::sleep(Duration::from_secs(1));  // Blocks executor!
}

// Right
async fn process() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}
```

### 3. Not Testing Error Cases
```rust
#[tokio::test]
async fn test_error_handling() {
    let result = operation_with_invalid_input().await;
    assert!(result.is_err());
    assert!(matches!(result.unwrap_err(), Error::InvalidInput(_)));
}
```

### 4. Ignoring Performance
```rust
// Consider batch operations
for item in items {
    storage.save(item).await?;  // N database calls
}

// Better
storage.save_batch(items).await?;  // 1 database call
```

## Integration with GitHub Release Best Practices

This skill integrates with the GitHub release best practices workflow for feature development and release management:

### Release Preparation Integration
When implementing features for release:
1. **Version Impact Assessment**: Consult github-release-best-practices skill for semantic versioning implications
2. **Changelog Planning**: Consider Keep a Changelog format for feature documentation
3. **Quality Gates**: Ensure implementation meets release standards (>90% coverage, zero warnings)
4. **Breaking Changes**: Identify and document any breaking changes for migration guides

### Coordination Workflows
- **Pre-Implementation**: Use github-release-best-practices for version planning
- **Implementation**: Follow feature-implement patterns while considering release requirements  
- **Testing**: Coordinate with testing-qa for release validation
- **Release Creation**: Leverage github-release-best-practices agent for final release orchestration

### Example Integration Pattern
```markdown
## Feature Implementation → Release Workflow

1. **Assessment Phase**
   - github-release-best-practices: Analyze feature scope and version impact
   - feature-implement: Plan implementation with release considerations

2. **Implementation Phase**
   - feature-implement: Execute feature development
   - testing-qa: Ensure quality gates met
   - code-reviewer: Validate implementation standards

3. **Release Phase**
   - github-release-best-practices: Update changelog, create release notes
   - goap-agent: Coordinate final release creation
```

This integration ensures features are implemented with release readiness in mind, following 2025 GitHub release best practices for Rust workspaces.