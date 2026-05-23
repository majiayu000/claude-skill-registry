---
name: duroxide-orchestrations
description: Writing durable workflows using Duroxide in Rust. Use when creating orchestrations, activities, workflows, or when the user mentions duroxide, durable functions, or workflow orchestration.
---

# Duroxide Durable Workflow Development

## Overview

Skills for developing durable workflows using Duroxide in Rust. Duroxide provides deterministic, replayable orchestrations with automatic failure recovery.

## Core Concepts

- **Activities**: Idempotent operations that perform actual work (K8s calls, DB queries, HTTP requests)
- **Orchestrations**: Deterministic workflow logic that coordinates activities
- **Continue-as-new**: Pattern for long-running orchestrations to prevent unbounded history
- **Sub-orchestrations**: Reusable workflow compositions
- **Detached orchestrations**: Background workflows that run independently

## Directory Structure

```
toygres-orchestrations/src/
├── orchestrations/          # Workflow definitions
│   └── my_orchestration.rs
├── activities/              # Atomic operations
│   ├── my_activity.rs
│   └── cms/                 # Grouped by domain
│       └── my_cms_activity.rs
├── registry.rs              # Central registration
├── types.rs                 # Orchestration I/O types
├── activity_types.rs        # Activity I/O types
└── names.rs                 # Naming constants
```

## Naming Convention

Follow the hierarchical namespace pattern in `names.rs`:

```rust
// Format: {crate}::{type}::{name}
pub mod orchestrations {
    pub const MY_WORKFLOW: &str = "toygres-orchestrations::orchestration::my-workflow";
}

pub mod activities {
    pub const MY_ACTIVITY: &str = "toygres-orchestrations::activity::my-activity";
}
```

## Creating Activities

Activities must be **idempotent** - safe to retry without side effects.

```rust
// toygres-orchestrations/src/activities/my_activity.rs
use duroxide::ActivityContext;
use crate::activity_types::{MyInput, MyOutput};

/// Activity name for registration and scheduling
pub const NAME: &str = "toygres-orchestrations::activity::my-activity";

pub async fn activity(
    ctx: ActivityContext,
    input: MyInput,
) -> Result<MyOutput, String> {
    ctx.trace_info(format!("Starting activity: {}", input.name));

    // CRITICAL: Check idempotency first - has this already been done?
    let already_done = check_if_done(&input).await?;
    if already_done {
        ctx.trace_info("Already completed, returning cached result");
        return Ok(MyOutput { ... });
    }

    // Perform actual work
    let result = do_work(&input).await
        .map_err(|e| format!("Failed: {}", e))?;

    ctx.trace_info("Activity completed successfully");
    Ok(result)
}
```

### Activity Registration

Add to `registry.rs`:

```rust
pub fn create_activity_registry() -> ActivityRegistry {
    ActivityRegistry::builder()
        .register_typed(
            activities::my_activity::NAME,
            activities::my_activity::activity,
        )
        .build()
}
```

## Creating Orchestrations

Orchestrations coordinate activities with deterministic logic.

```rust
// toygres-orchestrations/src/orchestrations/my_orchestration.rs
use duroxide::{OrchestrationContext, RetryPolicy, BackoffStrategy};
use std::time::Duration;

pub async fn my_orchestration(
    ctx: OrchestrationContext,
    input: MyInput,
) -> Result<MyOutput, String> {
    ctx.trace_info(format!("Starting orchestration: {}", input.id));

    // Schedule an activity (basic)
    let result = ctx
        .schedule_activity_typed::<ActivityInput, ActivityOutput>(
            activities::my_activity::NAME,
            &activity_input,
        )
        .into_activity_typed::<ActivityOutput>()
        .await?;

    Ok(MyOutput { ... })
}
```

### Orchestration Registration

```rust
pub fn create_orchestration_registry() -> OrchestrationRegistry {
    OrchestrationRegistry::builder()
        .register_typed(
            orchestrations::MY_WORKFLOW,
            crate::orchestrations::my_orchestration::my_orchestration,
        )
        .build()
}
```

## Scheduling Patterns

### Basic Activity Scheduling

```rust
let result = ctx
    .schedule_activity_typed::<Input, Output>(NAME, &input)
    .into_activity_typed::<Output>()
    .await?;
```

### Activity with Retry and Backoff

```rust
let result = ctx
    .schedule_activity_with_retry_typed::<Input, Output>(
        NAME,
        &input,
        RetryPolicy::new(5)  // Max 5 retries
            .with_backoff(BackoffStrategy::Exponential {
                base: Duration::from_secs(2),
                multiplier: 2.0,
                max: Duration::from_secs(30),
            })
            .with_timeout(Duration::from_secs(60)),
    )
    .await?;
```

### Backoff Strategies

```rust
// Fixed delay between retries
BackoffStrategy::Fixed {
    delay: Duration::from_secs(5)
}

// Linear increase: 2s, 4s, 6s, 8s, max 10s
BackoffStrategy::Linear {
    base: Duration::from_secs(2),
    max: Duration::from_secs(10)
}

// Exponential: 2s, 4s, 8s, 16s, max 30s
BackoffStrategy::Exponential {
    base: Duration::from_secs(2),
    multiplier: 2.0,
    max: Duration::from_secs(30)
}
```

### Sub-Orchestration (Reusable Workflow)

```rust
let result = ctx
    .schedule_sub_orchestration_typed::<Input, Output>(
        orchestrations::CHILD_WORKFLOW,
        &input,
    )
    .into_sub_orchestration_typed::<Output>()
    .await?;
```

### Detached Orchestration (Background/Fire-and-Forget)

```rust
// Start orchestration without waiting for completion
let input_json = serde_json::to_string(&input)?;
ctx.schedule_orchestration(
    orchestrations::BACKGROUND_WORKFLOW,
    &orchestration_id,  // Unique ID for this instance
    input_json,
);
// Continues immediately - orchestration runs independently
```

## Deterministic Timing

**NEVER use `tokio::time::sleep()` - it breaks determinism!**

```rust
// Deterministic timer - safe for replay
ctx.schedule_timer(Duration::from_secs(30)).into_timer().await;

// Get current time deterministically
let now = ctx.utcnow().await?;
```

## Signal Handling with select2

Wait for either a timer or an external signal:

```rust
// Wait for 30 seconds OR deletion signal (whichever comes first)
let timer = ctx.schedule_timer(Duration::from_secs(30));
let deletion_signal = ctx.schedule_wait("InstanceDeleted");

let (winner_index, _) = ctx.select2(timer, deletion_signal).await;

if winner_index == 1 {
    // Signal received
    ctx.trace_info("Received signal, exiting gracefully");
    return Ok(());
}
// Timer fired, continue
```

## Continue-as-New Pattern

For long-running orchestrations, prevent unbounded history growth:

```rust
pub async fn long_running_orchestration(
    ctx: OrchestrationContext,
    input: MyInput,
) -> Result<MyOutput, String> {
    // Do one iteration of work
    let result = do_work(&ctx, &input).await?;

    // Wait before next iteration
    ctx.schedule_timer(Duration::from_secs(60)).into_timer().await;

    // Continue as new: restarts with fresh execution history
    let next_input = MyInput {
        iteration: input.iteration + 1,
        ..input
    };
    let input_json = serde_json::to_string(&next_input)?;
    ctx.continue_as_new(input_json).await?;

    Ok(result)
}
```

## Error Handling Patterns

### Propagate Critical Errors

```rust
// Fail orchestration if activity fails
let result = ctx
    .schedule_activity_typed::<I, O>(NAME, &input)
    .into_activity_typed::<O>()
    .await?;  // ? propagates error
```

### Best-Effort Operations (Log and Continue)

```rust
// Don't fail orchestration for non-critical operations
if let Err(err) = ctx
    .schedule_activity_typed::<I, O>(NAME, &input)
    .into_activity_typed::<O>()
    .await
{
    ctx.trace_warn(format!("Non-critical operation failed: {}", err));
    // Continue despite error
}
```

## Versioning Strategy

**CRITICAL: Never modify existing orchestration code. Always create new versions.**

Running orchestrations replay their history - changing code breaks replay.

### Adding a New Version (Recommended Pattern)

When adding a new version, follow this workflow for cleaner git diffs:

1. **Copy the current latest version** to a new function with the OLD version number
2. **Make your changes** in the existing function name and bump its version
3. Register both in the registry

**Why?** This preserves history per version and makes git diffs show only the actual changes,
rather than showing the new version as entirely new code.

```rust
// STEP 1: Copy current implementation to preserve v1.0.1
pub async fn my_orchestration_1_0_1(ctx: OrchestrationContext, input: Input) -> Result<Output, String> {
    ctx.trace_info("[v1.0.1] Original logic");
    // Exact copy of previous implementation - DO NOT MODIFY
}

// STEP 2: Update the main function with new version
// This is now v1.0.2 - git diff will clearly show what changed
pub async fn my_orchestration_1_0_2(ctx: OrchestrationContext, input: Input) -> Result<Output, String> {
    ctx.trace_info("[v1.0.2] Updated logic");
    // Your new changes here - git diff shows only the delta
}
```

Register all versions:

```rust
OrchestrationRegistry::builder()
    .register_typed(NAME, my_orchestration)  // v1.0.0 (original)
    .register_versioned_typed(NAME, "1.0.1", my_orchestration_1_0_1)
    .register_versioned_typed(NAME, "1.0.2", my_orchestration_1_0_2)  // Latest
    .build()
```

## Logging

Use context logging methods for durability:

```rust
ctx.trace_info(format!("Processing: {}", id));
ctx.trace_warn(format!("Warning: {}", message));
ctx.trace_error(format!("Error: {}", error));
```

## Type Definitions

All I/O types must implement Serialize/Deserialize:

```rust
// activity_types.rs
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct MyInput {
    pub name: String,
    pub count: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct MyOutput {
    pub result: String,
    pub success: bool,
}
```

Add serialization tests:

```rust
#[test]
fn test_my_input_serialization() {
    let input = MyInput { name: "test".into(), count: 5 };
    let json = serde_json::to_string(&input).unwrap();
    let parsed: MyInput = serde_json::from_str(&json).unwrap();
    assert_eq!(input, parsed);
}
```

## Complete Example: Multi-Step Orchestration

```rust
pub async fn create_resource_orchestration(
    ctx: OrchestrationContext,
    input: CreateResourceInput,
) -> Result<CreateResourceOutput, String> {
    ctx.trace_info(format!("Creating resource: {}", input.name));

    // Step 1: Reserve in database
    ctx.schedule_activity_typed::<ReserveInput, ReserveOutput>(
        activities::reserve_resource::NAME,
        &ReserveInput { name: input.name.clone() },
    )
    .into_activity_typed::<ReserveOutput>()
    .await?;

    // Step 2: Create with retry (external service may be flaky)
    match create_with_retry(&ctx, &input).await {
        Ok(output) => {
            // Step 3: Update status to ready
            update_status(&ctx, &input.name, "ready").await;
            Ok(output)
        }
        Err(e) => {
            ctx.trace_error(format!("Creation failed: {}", e));
            // Step 4: Cleanup on failure via sub-orchestration
            cleanup_on_failure(&ctx, &input.name).await;
            Err(e)
        }
    }
}

async fn create_with_retry(
    ctx: &OrchestrationContext,
    input: &CreateResourceInput,
) -> Result<CreateResourceOutput, String> {
    ctx
        .schedule_activity_with_retry_typed::<CreateInput, CreateOutput>(
            activities::create_resource::NAME,
            &CreateInput { ... },
            RetryPolicy::new(3)
                .with_backoff(BackoffStrategy::Exponential {
                    base: Duration::from_secs(2),
                    multiplier: 2.0,
                    max: Duration::from_secs(30),
                }),
        )
        .await
}

async fn cleanup_on_failure(ctx: &OrchestrationContext, name: &str) -> Result<(), String> {
    ctx
        .schedule_sub_orchestration_typed::<DeleteInput, DeleteOutput>(
            orchestrations::DELETE_RESOURCE,
            &DeleteInput { name: name.to_string() },
        )
        .into_sub_orchestration_typed::<DeleteOutput>()
        .await?;
    Ok(())
}

async fn update_status(ctx: &OrchestrationContext, name: &str, status: &str) {
    if let Err(e) = ctx
        .schedule_activity_typed::<UpdateInput, UpdateOutput>(
            activities::update_status::NAME,
            &UpdateInput { name: name.to_string(), status: status.to_string() },
        )
        .into_activity_typed::<UpdateOutput>()
        .await
    {
        ctx.trace_warn(format!("Failed to update status: {}", e));
    }
}
```

## Best Practices Summary

1. **Naming**: Use `{crate}::{type}::{name}` format in `names.rs`
2. **Idempotency**: Activities must be safe to retry
3. **Determinism**: Only use `ctx.schedule_timer()`, never `tokio::time::sleep()`
4. **Versioning**: Never modify existing orchestrations - create new versions
5. **Error Handling**: Propagate critical errors, log non-critical ones
6. **Long-Running**: Use continue-as-new to prevent history bloat
7. **Testing**: Add serialization round-trip tests for all types
8. **Logging**: Use `ctx.trace_*()` methods, not `println!`
9. **Composition**: Use sub-orchestrations for reusable workflows
10. **Background Tasks**: Use detached orchestrations for fire-and-forget

## Client API

```rust
// Start orchestration (uses latest registered version - PREFERRED)
client.start_orchestration(instance_id, orchestration_name, input).await?;

// Start specific version (only when you need to pin to older version)
client.start_orchestration_versioned(instance_id, orchestration_name, "1.0.1", input).await?;

// Cancel orchestration
client.cancel_instance(instance_id, "reason").await?;

// Send signal
client.send_signal(instance_id, "SignalName", payload).await?;

// Get status
let info = client.get_instance_info(instance_id).await?;
```

### Version Selection

**Default behavior:** `start_orchestration` automatically uses the latest registered version.

**Use `start_orchestration_versioned` only when:**
- You need to pin to a specific older version for compatibility
- Testing a specific version in isolation

**Version numbering convention:**
- `1.0.0` - Initial version
- `1.0.1` - Bug fixes, minor improvements
- `1.0.2` - Additional bug fixes, new optional features
- Major version changes for breaking input/output changes
