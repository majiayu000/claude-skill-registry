---
name: "Deterministic Simulation Testing (Tokio/Rust)"
description: "Test distributed systems with reproducible deterministic simulation using turmoil"
approved: Yes
created: 2026-01-19
license: "MIT"
metadata:
  author: "Main Agent"
  version: "2.1-approved"
  last_updated: "2026-01-28"
tags:
  - rust
  - tokio
  - testing
  - distributed-systems
  - simulation
  - determinism
tools:
  - turmoil
  - madsim
  - proptest
files:
  - examples/basic-dst-setup.md: Working example of DST test setup with turmoil
  - examples/basic-dst-setup.rs: Complete DST test example code
assets:
  - docs/dst-rust-guide.md: Comprehensive DST guide for Rust developers
  - docs/dst-internals-guide.md: Deep dive into DST implementation details
  - docs/README.md: DST documentation overview
---

# Deterministic Simulation Testing (Rust)

## When to Use This Skill

Read this when testing distributed systems that need:
- Reproducible failure scenarios
- Network partition testing
- Consensus protocol verification
- Fast simulation of time-dependent behavior
- Reproducing intermittent bugs

**Key insight:** Control all non-determinism (time, randomness, network, I/O) with a seed = identical behavior every run.

---

## The Four Pillars of Determinism

| Pillar | Problem | Solution |
|--------|---------|----------|
| **Execution** | Thread scheduling is non-deterministic | Single-threaded async executor |
| **Entropy** | RNGs use system entropy | Seeded PRNG throughout |
| **Time** | Real clocks advance unpredictably | Simulated clock, manual advancement |
| **I/O** | Network has variable latency/loss | In-memory simulated network |

---

## Key Libraries

| Library | Purpose | Use When |
|---------|---------|----------|
| **turmoil** | Network simulation for Tokio | Standard TCP/UDP patterns |
| **madsim** | Full libc interception | Need to catch all entropy/time sources |
| **proptest** | Property-based input generation | Generating test scenarios |

---

## Quick Start

### 1. Add Dependencies

```toml
[features]
default = []
simulation = ["turmoil"]

[dependencies]
tokio = { version = "1", features = ["full"] }
rand = "0.8"

[dev-dependencies]
turmoil = "0.6"
```

### 2. Basic Turmoil Test

```rust
use turmoil::Builder;
use std::time::Duration;

#[test]
fn test_echo_server() {
    let mut sim = Builder::new()
        .simulation_duration(Duration::from_secs(60))
        .build();

    // Server
    sim.host("server", || async {
        let listener = turmoil::net::TcpListener::bind("0.0.0.0:8080").await?;
        let (mut socket, _) = listener.accept().await?;

        let mut buf = [0u8; 1024];
        loop {
            let n = socket.read(&mut buf).await?;
            if n == 0 { break; }
            socket.write_all(&buf[..n]).await?;
        }
        Ok(())
    });

    // Client
    sim.client("client", async {
        let mut socket = turmoil::net::TcpStream::connect("server:8080").await?;
        socket.write_all(b"hello").await?;

        let mut buf = [0u8; 1024];
        let n = socket.read(&mut buf).await?;
        assert_eq!(&buf[..n], b"hello");
        Ok(())
    });

    sim.run().unwrap();
}
```

### 3. Seed Management

```rust
fn run_with_seed<F>(test_fn: F)
where
    F: FnOnce(u64) + std::panic::UnwindSafe
{
    let seed: u64 = std::env::var("TEST_SEED")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or_else(|| rand::random());

    println!("TEST_SEED={}", seed);

    let result = std::panic::catch_unwind(|| test_fn(seed));

    if result.is_err() {
        eprintln!("Reproduce with: TEST_SEED={} cargo test", seed);
        std::panic::resume_unwind(result.unwrap_err());
    }
}
```

---

## Common Patterns

### Pattern 1: Deterministic HashMap

```rust
use std::collections::HashMap;
use std::hash::{BuildHasher, Hasher};

#[derive(Clone, Default)]
pub struct DeterministicHasher {
    state: u64,
}

impl Hasher for DeterministicHasher {
    fn finish(&self) -> u64 {
        self.state
    }

    fn write(&mut self, bytes: &[u8]) {
        const FNV_PRIME: u64 = 1099511628211;
        for &byte in bytes {
            self.state ^= byte as u64;
            self.state = self.state.wrapping_mul(FNV_PRIME);
        }
    }
}

#[derive(Clone, Default)]
pub struct DeterministicBuildHasher;

impl BuildHasher for DeterministicBuildHasher {
    type Hasher = DeterministicHasher;
    fn build_hasher(&self) -> Self::Hasher {
        DeterministicHasher { state: 14695981039346656037 }
    }
}

type DetHashMap<K, V> = HashMap<K, V, DeterministicBuildHasher>;
```

### Pattern 2: Simulated Time (Tokio-only)

```rust
#[tokio::test(flavor = "current_thread", start_paused = true)]
async fn test_timeout() {
    let start = tokio::time::Instant::now();

    // This doesn't actually wait - time is simulated
    tokio::time::sleep(Duration::from_secs(3600)).await;

    // But an hour has "passed"
    assert_eq!(start.elapsed(), Duration::from_secs(3600));
}
```

### Pattern 3: Abstract I/O Layer

```rust
#[cfg(not(feature = "simulation"))]
pub use tokio::net::{TcpListener, TcpStream};

#[cfg(feature = "simulation")]
pub use turmoil::net::{TcpListener, TcpStream};
```

### Pattern 4: Fault Injection

```rust
let mut sim = Builder::new()
    .min_message_latency(Duration::from_millis(100))
    .max_message_latency(Duration::from_millis(500))
    .build();

// Network partition
sim.partition("node-a", "node-b");

// Run during partition
sim.run_until(Duration::from_secs(30));

// Heal partition
sim.repair("node-a", "node-b");

sim.run().unwrap();
```

---

## Pitfalls to Avoid

### Pitfall 1: Using std::time

```rust
// BAD ❌ - Bypasses simulated time
std::time::Instant::now()
std::thread::sleep(duration)

// GOOD ✅ - Uses simulated time
tokio::time::Instant::now()
tokio::time::sleep(duration).await
```

### Pitfall 2: HashMap Iteration Order

```rust
// BAD ❌ - Order is non-deterministic
for (k, v) in hashmap.iter() {
    process_in_order(k, v); // Order affects result!
}

// GOOD ✅ - Use BTreeMap or sort first
let mut items: Vec<_> = hashmap.iter().collect();
items.sort_by_key(|(k, _)| *k);
```

### Pitfall 3: Third-Party Crate Entropy

```rust
// BAD ❌ - uuid uses system entropy
let id = uuid::Uuid::new_v4();

// GOOD ✅ - Generate from seeded RNG
let id = uuid::Uuid::from_u128(rng.gen());
```

---

## Examples

### Network Partition Test

```rust
#[test]
fn test_survives_partition() {
    let seed = 42u64;
    let mut rng = StdRng::seed_from_u64(seed);

    let mut sim = Builder::new()
        .simulation_duration(Duration::from_secs(120))
        .build();

    // Create 3-node cluster
    for i in 0..3 {
        let node_name = format!("node-{}", i);
        sim.host(&node_name, || async move {
            // Consensus participant logic
            Ok(())
        });
    }

    // Run normally
    sim.run_until(Duration::from_secs(10));

    // Random partition
    let victim = rng.gen_range(0..3);
    sim.partition(
        &format!("node-{}", victim),
        &format!("node-{}", (victim + 1) % 3)
    );

    // Run during partition
    sim.run_until(Duration::from_secs(30));

    // Heal
    sim.repair(
        &format!("node-{}", victim),
        &format!("node-{}", (victim + 1) % 3)
    );

    // Verify recovery
    sim.run().unwrap();
}
```

### Determinism Verification

```rust
#[test]
fn verify_determinism() {
    let seed = 12345u64;

    let result1 = run_and_capture(seed);
    let result2 = run_and_capture(seed);

    assert_eq!(result1, result2,
        "Non-determinism detected! Check for unseeded RNG or real time.");
}

fn run_and_capture(seed: u64) -> Vec<Event> {
    // Run simulation, capture events
    // Return events for comparison
}
```

---

## Running Simulation Tests

```bash
# With random seed
cargo test --features simulation

# With specific seed for reproduction
TEST_SEED=12345 cargo test --features simulation

# Run specific test
TEST_SEED=42 cargo test test_survives_partition --features simulation
```

---

## References

- [TigerBeetle Blog: A Descent Into the Vortex](https://tigerbeetle.com/blog)
- [S2.dev: Deterministic simulation testing for async Rust](https://s2.dev/blog)
- [turmoil GitHub](https://github.com/tokio-rs/turmoil)
- [madsim GitHub](https://github.com/madsim-rs/madsim)
- [FoundationDB Testing Talk](https://www.youtube.com/watch?v=4fFDFbi3toc)

## Examples

See `examples/` directory for working code:

- `basic-dst-setup.md` - Working DST test setup guide
- `basic-dst-setup.rs` - Complete DST test example code

See `docs/` directory for comprehensive guides:

- `dst-rust-guide.md` - Complete DST concepts and turmoil/madsim usage
- `dst-internals-guide.md` - Deep dive into DST implementation details
- `README.md` - DST documentation overview

## Related Skills

- [Rust with Async Code](../rust-with-async-code/skill.md) - For async patterns in production code
- [Rust Testing Excellence](../rust-testing-excellence/skill.md) - For general testing patterns

---

*Last Updated: 2026-01-28*
*Version: 2.1-approved*
