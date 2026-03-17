---
name: testing
description: Comprehensive testing strategies for Guts including unit tests, integration tests, property-based testing, and fuzzing
---

# Testing Skill for Guts

You are writing tests for a distributed system that requires high reliability.

## Testing Pyramid

```
        /\
       /  \      E2E Tests (few)
      /    \     Integration Tests (some)
     /      \    Unit Tests (many)
    /________\   Property Tests (extensive)
```

## Unit Testing

### Structure

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    // Group related tests
    mod repository_tests {
        use super::*;

        #[test]
        fn create_repository_success() {
            let repo = Repository::new("test-repo");
            assert_eq!(repo.name(), "test-repo");
        }

        #[test]
        fn create_repository_invalid_name() {
            let result = Repository::new("");
            assert!(matches!(result, Err(RepositoryError::InvalidName(_))));
        }
    }
}
```

### Async Tests

```rust
#[tokio::test]
async fn async_operation_completes() {
    let service = TestService::new().await;

    let result = tokio::time::timeout(
        Duration::from_secs(5),
        service.long_running_operation(),
    )
    .await;

    assert!(result.is_ok());
}
```

## Integration Testing

### Test Fixtures

```rust
// tests/common/mod.rs
pub struct TestNode {
    pub node: Node,
    pub temp_dir: TempDir,
}

impl TestNode {
    pub async fn new() -> Self {
        let temp_dir = TempDir::new().unwrap();
        let config = Config::test_default(temp_dir.path());
        let node = Node::new(config).await.unwrap();

        Self { node, temp_dir }
    }
}

// tests/integration/repository_tests.rs
#[tokio::test]
async fn can_create_and_clone_repository() {
    let node = TestNode::new().await;

    // Create repository
    let repo_id = node.create_repository("test").await.unwrap();

    // Clone should succeed
    let cloned = node.clone_repository(repo_id).await;
    assert!(cloned.is_ok());
}
```

### Multi-Node Tests

```rust
#[tokio::test]
async fn nodes_sync_repository() {
    // Start 3 nodes
    let nodes: Vec<_> = futures::future::join_all(
        (0..3).map(|_| TestNode::new())
    ).await;

    // Connect nodes
    for i in 1..nodes.len() {
        nodes[i].connect_to(&nodes[0]).await.unwrap();
    }

    // Create repo on node 0
    let repo_id = nodes[0].create_repository("sync-test").await.unwrap();

    // Wait for sync
    tokio::time::sleep(Duration::from_secs(2)).await;

    // Verify all nodes have the repo
    for node in &nodes {
        assert!(node.has_repository(repo_id).await);
    }
}
```

## Property-Based Testing

Using `proptest`:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn repository_name_roundtrip(name in "[a-z][a-z0-9-]{0,63}") {
        let repo = Repository::new(&name).unwrap();
        prop_assert_eq!(repo.name(), name);
    }

    #[test]
    fn signature_verification(data in any::<Vec<u8>>()) {
        let identity = Identity::new();
        let signature = identity.sign(&data);
        prop_assert!(identity.verify(&data, &signature).is_ok());
    }
}
```

## Fuzzing

Using `cargo-fuzz`:

```rust
// fuzz/fuzz_targets/parse_message.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use guts_protocol::Message;

fuzz_target!(|data: &[u8]| {
    // Parsing should never panic
    let _ = Message::parse(data);
});
```

## Test Commands

```bash
# Run all tests
cargo test --workspace

# Run with coverage
cargo llvm-cov --workspace --html

# Run specific test
cargo test repository_tests::create_repository

# Run integration tests only
cargo test --test '*' --workspace

# Run benchmarks
cargo bench --workspace

# Run fuzzer
cargo +nightly fuzz run parse_message
```

## CI Test Matrix

```yaml
test:
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest]
      rust: [stable, beta, nightly]
  steps:
    - uses: actions/checkout@v4
    - uses: dtolnay/rust-toolchain@master
      with:
        toolchain: ${{ matrix.rust }}
    - run: cargo test --workspace --all-features
```

## Mocking Dependencies

```rust
use mockall::automock;

#[automock]
pub trait Storage {
    async fn get(&self, key: &[u8]) -> Result<Vec<u8>>;
    async fn put(&self, key: &[u8], value: &[u8]) -> Result<()>;
}

#[tokio::test]
async fn service_uses_storage() {
    let mut mock = MockStorage::new();
    mock.expect_get()
        .returning(|_| Ok(vec![1, 2, 3]));

    let service = Service::new(Box::new(mock));
    let result = service.fetch_data(b"key").await;

    assert_eq!(result.unwrap(), vec![1, 2, 3]);
}
```
