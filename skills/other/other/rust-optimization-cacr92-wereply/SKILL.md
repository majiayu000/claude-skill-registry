---
name: rust-optimization
description: 当用户要求"优化 Rust 代码"、"提高性能"、"减少内存使用"、"并行计算"、"缓存策略"、"HiGHS 求解器优化"、"数值计算优化"、"Moka 缓存"、"Rayon 并行"、"避免克隆"、"减少分配"、"SIMD 优化"、"工作窃取"、"异步性能"、"零成本抽象"、"内存优化"、"并发优化"，或者提到"性能优化"、"Rust优化"、"优化"、"配方计算性能"时使用此技能。用于优化 Rust 代码性能、内存管理、使用 Rayon 并行处理、实现 Moka 缓存策略或处理饲料配方优化系统中的数值计算和线性规划。
version: 3.0.0
---

# Rust Optimization Skill

Advanced Rust optimization techniques for high-performance feed formula calculation and linear programming.

## Performance Optimization Strategies

### 1. Caching Strategy (Moka)

Use `moka::future::Cache` for frequently accessed data:

```rust
use moka::future::Cache;
use std::time::Duration;

pub struct MaterialService {
    cache: Cache<String, Material>,
}

impl MaterialService {
    pub fn new() -> Self {
        Self {
            cache: Cache::builder()
                .max_capacity(1000)
                .time_to_live(Duration::from_secs(3600))
                .build(),
        }
    }

    pub async fn get_material(&self, code: &str) -> Result<Material> {
        self.cache
            .try_get_with(code.to_string(), async {
                self.repository.find_by_code(code).await
            })
            .await
    }
}
```

**When to cache:**
- Database query results that don't change often
- Computed nutrition values
- Expensive calculation results
- Reference data (materials, species standards)

### 2. Parallel Processing (Rayon)

Use `rayon` for CPU-intensive parallel computations:

```rust
use rayon::prelude::*;

pub fn calculate_nutrition_batch(
    materials: &[Material],
    proportions: &[f64],
) -> Vec<NutritionResult> {
    materials
        .par_iter()  // Parallel iterator
        .zip(proportions.par_iter())
        .map(|(material, proportion)| {
            calculate_material_nutrition(material, *proportion)
        })
        .collect()
}
```

**Best practices:**
- Use parallel iterators for embarrassingly parallel problems
- Benchmark to verify performance gains
- Avoid parallelizing small operations (overhead costs)
- Consider memory bandwidth limitations

### 3. Memory Optimization

#### Avoid Unnecessary Clones
```rust
// ❌ Bad - unnecessary clone
fn process(data: Vec<String>) -> Vec<String> {
    data.clone()
}

// ✅ Good - transfer ownership
fn process(data: Vec<String>) -> Vec<String> {
    data
}
```

#### Use References Where Possible
```rust
// ❌ Bad - takes ownership
fn calculate(materials: Vec<Material>) -> f64 {
    // ...
}

// ✅ Good - borrows data
fn calculate(materials: &[Material]) -> f64 {
    // ...
}
```

#### Use Cow for Conditional Cloning
```rust
use std::borrow::Cow;

fn maybe_transform(s: Cow<str>) -> Cow<str> {
    if needs_transform(s.as_ref()) {
        Cow::Owned(transform(s.into_owned()))
    } else {
        s
    }
}
```

### 4. Database Query Optimization

#### Avoid N+1 Queries
```rust
// ❌ Bad - N+1 problem
for formula in formulas {
    let materials = get_materials(formula.id).await?;
}

// ✅ Good - single query with JOIN
let results = sqlx::query!(
    "SELECT f.*, fm.* FROM formulas f
     LEFT JOIN formula_materials fm ON f.id = fm.formula_id"
)
.fetch_all(&pool)
.await?;
```

#### Use Batch Operations
```rust
// ✅ Batch insert
use sqlx::QueryBuilder;

pub async fn batch_insert(
    &self,
    items: Vec<Item>,
) -> Result<usize> {
    let mut query_builder = QueryBuilder::new(
        "INSERT INTO items (name, value) "
    );

    query_builder.push_values(items, |mut b, item| {
        b.push_bind(item.name)
         .push_bind(item.value);
    });

    let result = query_builder.build().execute(&self.pool).await?;
    Ok(result.rows_affected() as usize)
}
```

## Linear Programming Optimization

### HiGHS Solver Integration

```rust
use highs::*;

pub struct FormulaOptimizer {
    solver: HighsModel,
}

impl FormulaOptimizer {
    pub fn optimize(&mut self) -> Result<OptimizationResult> {
        // Set objective function
        self.solver.setObjectiveSense(ObjectiveSense::Minimize);

        // Add constraints efficiently
        for (nutrient, constraint) in &self.nutrient_constraints {
            let cols: Vec<Col> = self.material_indices.values().copied().collect();
            let values: Vec<f64> = self.materials
                .iter()
                .map(|m| m.nutrients.get(nutrient).copied().unwrap_or(0.0))
                .collect();

            self.solver.addRow(
                &cols,
                &values,
                constraint.min_value,
                constraint.max_value,
            )?;
        }

        // Solve
        self.solver.solve()?;
        Ok(self.extract_result())
    }
}
```

### Numerical Stability Tips

1. **Scale similar magnitudes**: Normalize data to similar ranges
2. **Avoid extreme values**: Use reasonable bounds (e.g., 0-100% for proportions)
3. **Use appropriate tolerance**: Don't over-constrain the solver
4. **Handle zero values**: Add small epsilon if needed for numerical stability

## Async Runtime Optimization

### Proper Async/Await Usage

```rust
// ❌ Bad - blocks runtime
pub async fn bad_blocking() {
    let result = expensive_sync_function(); // Blocks!
}

// ✅ Good - async-friendly
pub async fn good_async() {
    let result = tokio::task::spawn_blocking(|| {
        expensive_sync_function()
    }).await?;
}
```

### Concurrent Operations

```rust
// ✅ Run multiple independent operations concurrently
let (materials, species, factories) = tokio::try_join!(
    get_materials(),
    get_species(),
    get_factories()
)?;
```

## Profiling and Benchmarking

### Criterion Benchmarking

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn benchmark_formula_calculation(c: &mut Criterion) {
    c.bench_function("formula_calc", |b| {
        b.iter(|| {
            calculate_formula(black_box(test_data()))
        })
    });
}

criterion_group!(benches, benchmark_formula_calculation);
criterion_main!(benches);
```

### Flame Graph Profiling

```bash
# Install flamegraph
cargo install flamegraph

# Generate flamegraph
cargo flamegraph --bin cacrfeedformula

# View the generated flamegraph.svg
```

## Memory Leak Prevention

### Common Memory Leak Patterns

1. **Cyclic references in Rc/RefCell**: Use `Weak` references
2. **Unbounded caches**: Set max_capacity on Moka caches
3. **Tokio spawn without handles**: Keep task JoinHandles
4. **Event listener leaks**: Ensure cleanup on drop

### Memory Leak Detection

```bash
# Use valgrind for memory leak detection
cargo build --release
valgrind --leak-check=full --show-leak-kinds=all ./target/release/cacrfeedformula

# Use heaptrack for profiling
heaptrack ./target/release/cacrfeedformula
```

## Compiler Optimizations

### Release Profile Configuration

```toml
[profile.release]
opt-level = 3          # Maximum optimization
lto = true             # Link-time optimization
codegen-units = 1      # Better optimization at cost of compile time
panic = "abort"        # Smaller binary
strip = true           # Remove debug symbols
```

### Profile-Guided Optimization (PGO)

```bash
# Step 1: Build with profiling instrumentation
cargo build --release --profile profiling

# Step 2: Run typical workloads to generate profiling data
./target/profiling/cacrfeedformula --workload

# Step 3: Build optimized using profiling data
cargo build --release
```

## Common Performance Anti-Patterns

### ❌ Over-Using Arc
```rust
// Unnecessary Arc for single-threaded code
fn process(data: Arc<Vec<String>>) {
    // No concurrency needed
}
```

### ✅ Proper Arc Usage
```rust
// Arc is needed for sharing across threads
pub struct AppState {
    pub db: Arc<SqlitePool>,  // ✓ Shared across async tasks
}
```

### ❌ String Concatenation in Loops
```rust
let mut result = String::new();
for item in items {
    result += &item.to_string();  // ✗ Reallocation each iteration
}
```

### ✅ Efficient String Building
```rust
let mut result = String::with_capacity(items.len() * 10);
for item in items {
    result.push_str(&item.to_string());  // ✓ Pre-allocated
}
```

## When to Use This Skill

Activate this skill when:
- Optimizing formula calculation performance
- Reducing memory usage
- Implementing caching strategies
- Using parallel processing
- Working with linear programming solver
- Debugging performance bottlenecks
- Writing benchmarking code
- Analyzing memory usage
