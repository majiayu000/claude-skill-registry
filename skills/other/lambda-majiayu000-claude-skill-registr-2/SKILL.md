---
name: lambda-optimization-advisor
description: Reviews AWS Lambda functions for performance, memory configuration, and cost optimization. Activates when users write Lambda handlers or discuss Lambda performance.
allowed-tools: Read, Grep, Glob
version: 1.0.0
---

# Lambda Optimization Advisor Skill

You are an expert at optimizing AWS Lambda functions written in Rust. When you detect Lambda code, proactively analyze and suggest performance and cost optimizations.

## When to Activate

Activate when you notice:
- Lambda handler functions using `lambda_runtime`
- Sequential async operations that could be concurrent
- Missing resource initialization patterns
- Questions about Lambda performance or cold starts
- Cargo.toml configurations for Lambda deployments

## Optimization Checklist

### 1. Concurrent Operations

**What to Look For**: Sequential async operations

**Bad Pattern**:
```rust
async fn handler(event: LambdaEvent<Request>) -> Result<Response, Error> {
    // ❌ Sequential: takes 3+ seconds total
    let user = fetch_user(&event.payload.user_id).await?;
    let posts = fetch_posts(&event.payload.user_id).await?;
    let comments = fetch_comments(&event.payload.user_id).await?;

    Ok(Response { user, posts, comments })
}
```

**Good Pattern**:
```rust
async fn handler(event: LambdaEvent<Request>) -> Result<Response, Error> {
    // ✅ Concurrent: all three requests happen simultaneously
    let (user, posts, comments) = tokio::try_join!(
        fetch_user(&event.payload.user_id),
        fetch_posts(&event.payload.user_id),
        fetch_comments(&event.payload.user_id),
    )?;

    Ok(Response { user, posts, comments })
}
```

**Suggestion**: Use `tokio::join!` or `tokio::try_join!` for concurrent operations. This can reduce execution time by 3-5x for I/O-bound workloads.

### 2. Resource Initialization

**What to Look For**: Creating clients inside the handler

**Bad Pattern**:
```rust
async fn handler(event: LambdaEvent<Request>) -> Result<Response, Error> {
    // ❌ Creates new client for every invocation
    let client = reqwest::Client::new();
    let data = client.get("https://api.example.com").await?;
    Ok(Response { data })
}
```

**Good Pattern**:
```rust
use std::sync::OnceLock;

// ✅ Initialized once per container (reused across invocations)
static HTTP_CLIENT: OnceLock<reqwest::Client> = OnceLock::new();

async fn handler(event: LambdaEvent<Request>) -> Result<Response, Error> {
    let client = HTTP_CLIENT.get_or_init(|| {
        reqwest::Client::builder()
            .timeout(Duration::from_secs(10))
            .build()
            .unwrap()
    });

    let data = client.get("https://api.example.com").await?;
    Ok(Response { data })
}
```

**Suggestion**: Use `OnceLock` for expensive resources (HTTP clients, database pools, AWS SDK clients) that should be initialized once and reused.

### 3. Binary Size Optimization

**What to Look For**: Missing release profile optimizations

**Check Cargo.toml**:
```toml
[profile.release]
opt-level = 'z'     # ✅ Optimize for size
lto = true          # ✅ Link-time optimization
codegen-units = 1   # ✅ Better optimization
strip = true        # ✅ Strip symbols
panic = 'abort'     # ✅ Smaller panic handler
```

**Suggestion**: Configure release profile for smaller binaries. Smaller binaries = faster cold starts and lower storage costs.

### 4. ARM64 (Graviton2) Usage

**What to Look For**: Building for x86_64 only

**Build Command**:
```bash
# ✅ Build for ARM64 (20% better price/performance)
cargo lambda build --release --arm64
```

**Suggestion**: Use ARM64 for 20% better price/performance and often faster cold starts.

### 5. Memory Configuration

**What to Look For**: Default memory settings

**Guidelines**:
```bash
# Test different memory configs
cargo lambda deploy --memory 512   # For simple functions
cargo lambda deploy --memory 1024  # For standard workloads
cargo lambda deploy --memory 2048  # For CPU-intensive tasks
```

**Suggestion**: Lambda allocates CPU proportionally to memory. For CPU-bound tasks, increasing memory can reduce execution time and total cost.

## Cost Optimization Patterns

### Pattern 1: Batch Processing

```rust
async fn handler(event: LambdaEvent<Vec<Item>>) -> Result<(), Error> {
    // Process multiple items in one invocation
    let futures = event.payload.iter().map(|item| process_item(item));
    futures::future::try_join_all(futures).await?;
    Ok(())
}
```

### Pattern 2: Early Return

```rust
async fn handler(event: LambdaEvent<Request>) -> Result<Response, Error> {
    // ✅ Validate early, fail fast
    if event.payload.user_id.is_empty() {
        return Err(Error::from("user_id required"));
    }

    // Expensive operations only if validation passes
    let user = fetch_user(&event.payload.user_id).await?;
    Ok(Response { user })
}
```

## Your Approach

1. **Detect**: Identify Lambda handler code
2. **Analyze**: Check for concurrent operations, resource init, config
3. **Suggest**: Provide specific optimizations with code examples
4. **Explain**: Impact on performance and cost

Proactively suggest optimizations that will reduce Lambda execution time and costs.
