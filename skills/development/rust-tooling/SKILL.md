---
name: rust-tooling
description: Rust development tools including PyO3 bindings, sqlx database access, AGiXT SDK, and Rust-Python interop
icon: 🦀
category: development
tools:
  - cargo
  - rustc
  - rust-analyzer
  - rustfmt
  - clippy
  - maturin
  - pyo3
  - sqlx-cli
  - agixt_sdk
---

# Rust Tooling Skills

## Overview

This skill provides expertise in Rust development tools for building high-performance components, Python bindings, and type-safe database access.

## PyO3 - Rust-Python Bindings

PyO3 enables writing Python extensions in Rust for performance-critical ROS2 components.

### Project Setup

```bash
# Install maturin (build tool for PyO3)
pixi add maturin

# Create new PyO3 project
maturin new my_rust_module --bindings pyo3
cd my_rust_module
```

### Cargo.toml

```toml
[package]
name = "my_rust_module"
version = "0.1.0"
edition = "2021"

[lib]
name = "my_rust_module"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.20", features = ["extension-module"] }
numpy = "0.20"  # For NumPy array support
```

### Basic Example

```rust
use pyo3::prelude::*;

/// A fast point cloud processor
#[pyclass]
struct PointCloudProcessor {
    #[pyo3(get, set)]
    voxel_size: f64,
}

#[pymethods]
impl PointCloudProcessor {
    #[new]
    fn new(voxel_size: f64) -> Self {
        PointCloudProcessor { voxel_size }
    }

    /// Downsample point cloud using voxel grid
    fn downsample(&self, points: Vec<[f64; 3]>) -> Vec<[f64; 3]> {
        // High-performance Rust implementation
        points.into_iter()
            .filter(|p| p[0] % self.voxel_size < 0.5)
            .collect()
    }
}

/// Process sensor data with SIMD optimization
#[pyfunction]
fn fast_transform(data: Vec<f64>, scale: f64) -> Vec<f64> {
    data.iter().map(|x| x * scale).collect()
}

/// Python module
#[pymodule]
fn my_rust_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PointCloudProcessor>()?;
    m.add_function(wrap_pyfunction!(fast_transform, m)?)?;
    Ok(())
}
```

### NumPy Integration

```rust
use numpy::{PyArray1, PyArray2, PyReadonlyArray2};
use pyo3::prelude::*;

#[pyfunction]
fn process_lidar_scan<'py>(
    py: Python<'py>,
    points: PyReadonlyArray2<'py, f64>,
) -> &'py PyArray1<f64> {
    let points = points.as_array();
    let distances: Vec<f64> = points
        .rows()
        .into_iter()
        .map(|row| (row[0].powi(2) + row[1].powi(2) + row[2].powi(2)).sqrt())
        .collect();

    PyArray1::from_vec(py, distances)
}
```

### Build and Install

```bash
# Development build
maturin develop

# Release build
maturin build --release

# Install in current environment
pip install target/wheels/*.whl

# Build for multiple Python versions
maturin build --release --interpreter python3.10 python3.11
```

### ROS2 Integration

```python
# In your ROS2 node
import my_rust_module
from sensor_msgs.msg import PointCloud2
import numpy as np

class FastLidarNode(Node):
    def __init__(self):
        super().__init__('fast_lidar')
        self.processor = my_rust_module.PointCloudProcessor(0.1)

    def process_callback(self, msg: PointCloud2):
        # Convert to numpy array
        points = np.array(list(pc2.read_points(msg)))

        # Fast Rust processing
        result = my_rust_module.process_lidar_scan(points)
```

## sqlx - Type-Safe Database Access

sqlx provides compile-time checked SQL queries for robotics data persistence.

### Installation

```bash
# Install sqlx CLI
cargo install sqlx-cli

# Or via Nix
nix profile install nixpkgs#sqlx-cli
```

### Cargo.toml

```toml
[dependencies]
sqlx = { version = "0.7", features = [
    "runtime-tokio",
    "postgres",
    "sqlite",
    "chrono",
    "uuid"
]}
tokio = { version = "1", features = ["full"] }
```

### Database Setup

```bash
# Create database
sqlx database create

# Run migrations
sqlx migrate run

# Prepare offline mode (for CI)
cargo sqlx prepare
```

### Migration Example

```sql
-- migrations/001_create_robots.sql
CREATE TABLE robots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'idle',
    position_x DOUBLE PRECISION,
    position_y DOUBLE PRECISION,
    battery_level DOUBLE PRECISION,
    last_seen TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE telemetry (
    id BIGSERIAL PRIMARY KEY,
    robot_id UUID REFERENCES robots(id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_telemetry_robot_time ON telemetry(robot_id, timestamp);
```

### Rust Code

```rust
use sqlx::{postgres::PgPoolOptions, FromRow, Pool, Postgres};
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, FromRow)]
struct Robot {
    id: Uuid,
    name: String,
    status: String,
    position_x: Option<f64>,
    position_y: Option<f64>,
    battery_level: Option<f64>,
    last_seen: DateTime<Utc>,
}

struct RobotRepository {
    pool: Pool<Postgres>,
}

impl RobotRepository {
    async fn new(database_url: &str) -> Result<Self, sqlx::Error> {
        let pool = PgPoolOptions::new()
            .max_connections(5)
            .connect(database_url)
            .await?;
        Ok(Self { pool })
    }

    // Compile-time verified query
    async fn get_robot(&self, id: Uuid) -> Result<Robot, sqlx::Error> {
        sqlx::query_as!(
            Robot,
            r#"
            SELECT id, name, status, position_x, position_y,
                   battery_level, last_seen
            FROM robots
            WHERE id = $1
            "#,
            id
        )
        .fetch_one(&self.pool)
        .await
    }

    async fn update_position(
        &self,
        id: Uuid,
        x: f64,
        y: f64
    ) -> Result<(), sqlx::Error> {
        sqlx::query!(
            r#"
            UPDATE robots
            SET position_x = $2, position_y = $3, last_seen = NOW()
            WHERE id = $1
            "#,
            id, x, y
        )
        .execute(&self.pool)
        .await?;
        Ok(())
    }

    async fn record_telemetry(
        &self,
        robot_id: Uuid,
        metric: &str,
        value: f64,
    ) -> Result<(), sqlx::Error> {
        sqlx::query!(
            r#"
            INSERT INTO telemetry (robot_id, metric_name, metric_value)
            VALUES ($1, $2, $3)
            "#,
            robot_id, metric, value
        )
        .execute(&self.pool)
        .await?;
        Ok(())
    }
}
```

### SQLite for Embedded

```rust
use sqlx::sqlite::{SqlitePool, SqlitePoolOptions};

async fn setup_local_db() -> Result<SqlitePool, sqlx::Error> {
    let pool = SqlitePoolOptions::new()
        .max_connections(1)
        .connect("sqlite:robot_local.db?mode=rwc")
        .await?;

    // Run embedded migrations
    sqlx::migrate!("./migrations")
        .run(&pool)
        .await?;

    Ok(pool)
}
```

## Nix Integration

### flake.nix Addition

```nix
{
  devShells.default = pkgs.mkShell {
    packages = with pkgs; [
      # Rust toolchain
      rustc
      cargo
      rust-analyzer

      # PyO3 tools
      maturin

      # sqlx
      sqlx-cli

      # Database clients
      postgresql
      sqlite
    ];

    shellHook = ''
      export DATABASE_URL="postgres://user:pass@localhost/robotics"
      export SQLX_OFFLINE=true  # Use prepared queries in CI
    '';
  };
}
```

## Best Practices

### PyO3
1. **Use `#[pyclass]`** for stateful objects
2. **Prefer `Vec<T>`** over `PyList` for performance
3. **Use `numpy`** crate for array operations
4. **Release GIL** for CPU-bound operations: `py.allow_threads(|| ...)`

### sqlx
1. **Use migrations** for schema changes
2. **Enable offline mode** for CI builds
3. **Use connection pooling** in production
4. **Prefer compile-time checked queries** (`query!` macro)

## AGiXT Rust SDK

The AGiXT Rust SDK enables Rust applications to communicate with AGiXT for AI-powered robotics.

### Project Structure

```
rust/
├── Cargo.toml                    # Workspace root
└── agixt-bridge/
    ├── Cargo.toml                # AGiXT bridge crate
    ├── src/
    │   ├── main.rs               # CLI entry point
    │   ├── lib.rs                # Library exports
    │   ├── client.rs             # AGiXT client wrapper
    │   ├── commands.rs           # Robot command types
    │   └── config.rs             # Configuration
    └── examples/
        ├── basic_chat.rs         # Basic AGiXT chat
        └── robot_commands.rs     # Robot command processing
```

### Cargo.toml

```toml
[dependencies]
agixt_sdk = "0.1"
tokio = { version = "1.0", features = ["full"] }
reqwest = { version = "0.11", features = ["json"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
```

### Basic Usage

```rust
use agixt_sdk::AGiXTSDK;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let client = AGiXTSDK::new(
        Some("http://localhost:7437".to_string()),
        Some("agixt-dev-key".to_string()),
        false,
    );

    // Get available providers
    let providers = client.get_providers().await?;
    println!("Providers: {:?}", providers);

    // Create conversation
    let conv = client.new_conversation("ros2-agent", None, None).await?;
    println!("Conversation: {:?}", conv);

    Ok(())
}
```

### Build and Run

```bash
# Build the bridge
cd rust/agixt-bridge
cargo build

# Run example
cargo run --example basic_chat

# Run with release optimizations
cargo build --release
```

### ROS2 Integration Pattern

```rust
use agixt_sdk::AGiXTSDK;
use std::sync::Arc;

pub struct AGiXTROS2Bridge {
    client: Arc<AGiXTSDK>,
    agent_name: String,
}

impl AGiXTROS2Bridge {
    pub fn new(url: &str, api_key: &str, agent: &str) -> Self {
        let client = AGiXTSDK::new(
            Some(url.to_string()),
            Some(api_key.to_string()),
            false,
        );
        Self {
            client: Arc::new(client),
            agent_name: agent.to_string(),
        }
    }

    pub async fn process_command(&self, command: &str) -> anyhow::Result<String> {
        // Send command to AGiXT for AI processing
        // Return structured response for ROS2 action
        todo!("Implement based on your robot's action interface")
    }
}
```

### Configuration

Environment variables:
- `AGIXT_URL` - AGiXT API URL (default: `http://localhost:7437`)
- `AGIXT_API_KEY` - API key (default: `agixt-dev-key`)
- `LOCALAI_URL` - LocalAI URL (default: `http://localhost:8080`)
- `AGIXT_AGENT` - Default agent name (default: `ros2-agent`)

See `rust/agixt-bridge/src/config.rs` for configuration details.

## Related Skills

- [ROS2 Development](../ros2-development/SKILL.md) - ROS2 integration
- [Nix Environment](../nix-environment/SKILL.md) - Package management
- [AI Assistants](../ai-assistants/SKILL.md) - LocalAI, AGiXT, aichat, aider
- [Distributed Systems](../distributed-systems/SKILL.md) - NATS messaging for multi-robot
