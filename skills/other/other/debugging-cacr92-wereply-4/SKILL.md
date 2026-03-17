---
name: debugging
description: 当用户要求"调试这个"、"修复bug"、"排查问题"、"不工作"、"出错了"、"调查问题"、"性能问题"、"类型错误"、"Tauri 通信失败"、"断点调试"、"日志分析"、"性能分析"、"内存泄漏"、"死锁"，或者提到"调试"、"debugging"、"bug"、"问题"、"崩溃"、"错误"、"配方优化失败"、"HiGHS 求解器问题"时使用此技能。用于诊断和修复 Rust、React、数据库或 Tauri 集成代码中的问题。
version: 2.1.0
---

# Debugging Skill

Systematic debugging strategies for diagnosing and fixing issues in Tauri applications.

## Overview

This skill provides debugging guidance for:
- **Rust backend issues**: Panics, errors, async problems, database failures
- **React frontend issues**: Runtime errors, UI problems, state management issues
- **Integration problems**: Tauri command failures, type mismatches, serialization errors
- **Database issues**: Query failures, connection problems, migration errors
- **Performance issues**: Slow operations, memory leaks, blocking calls

## When This Skill Applies

This skill activates when:
- Application crashes or panics
- Functions return errors
- UI doesn't work as expected
- Tests are failing
- Performance is degraded
- Data is incorrect or corrupted
- Features don't work together properly

## Debugging Framework

### The Scientific Method

1. **Observe**: What exactly is happening?
2. **Formulate Hypothesis**: What could be causing this?
3. **Test Hypothesis**: How can we verify?
4. **Analyze Results**: Does this confirm or reject hypothesis?
5. **Iterate**: If not solved, form new hypothesis

### Systematic Debugging Process

```
┌─────────────────┐
│ 1. Define Issue │
│    What is the  │
│   symptom?      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Gather Info  │
│   Error msg?    │
│   Stack trace?  │
│   Logs?         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Reproduce    │
│   Can we make   │
│   it happen     │
│   consistently?│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Isolate      │
│   Narrow down   │
│   location      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Fix & Test   │
│   Apply fix     │
│   Verify it     │
│   works         │
└─────────────────┘
```

## Common Issues & Solutions

### Rust Backend Issues

#### Issue: "Function not found" for Tauri Command

**Symptom:**
```
Error: Failed to call command 'get_formula'
```

**Diagnosis Steps:**
1. Check if `#[tauri::command]` attribute is present
2. Check if command is registered in `main.rs`
3. Check if `#[specta::specta]` attribute is present
4. Regenerate types: `cargo run`

**Solution:**
```rust
// ✅ Ensure proper attributes
#[tauri::command]
#[specta::specta]
pub async fn get_formula(id: i64, state: State<'_, TauriAppState>) -> ApiResponse<Formula> {
    // ...
}

// In main.rs or lib.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_formula,
            // ... other commands
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

#### Issue: Database Lock Error

**Symptom:**
```
Error: database is locked
or
Error: database table is locked
```

**Diagnosis:**
```bash
# Check for long-running transactions
# Look for uncommitted transactions
# Verify WAL mode is enabled
```

**Solutions:**

**Enable WAL Mode:**
```rust
sqlx::query("PRAGMA journal_mode=WAL")
    .execute(&pool)
    .await?;

sqlx::query("PRAGMA busy_timeout=5000")
    .execute(&pool)
    .await?;
```

**Ensure Transaction Cleanup:**
```rust
// ✅ Always commit or rollback explicitly
let mut tx = pool.begin().await?;
match operation(&mut tx).await {
    Ok(result) => {
        tx.commit().await?;
        Ok(result)
    }
    Err(e) => {
        // Transaction auto-rolls back on drop
        Err(e)
    }
}
```

#### Issue: Async Runtime Panic

**Symptom:**
```
thread 'main' has overflowed its stack
or
panic: cannot drop in runtime context
```

**Diagnosis:**
- Look for blocking calls in async functions
- Check for deep recursion
- Find CPU-intensive operations without `.await`

**Solution:**
```rust
// ❌ Blocking in async
pub async fn bad() {
    std::thread::sleep(Duration::from_secs(1));  // Blocks!
    let result = expensive_cpu_calculation();     // No await
}

// ✅ Proper async
pub async fn good() {
    tokio::time::sleep(Duration::from_secs(1)).await;

    // Spawn blocking task for CPU work
    let result = tokio::task::spawn_blocking(|| {
        expensive_cpu_calculation()
    }).await?;
}
```

### React Frontend Issues

#### Issue: "Too many re-renders"

**Symptom:**
```
Warning: Too many re-renders. React limits the number of renders to prevent an infinite loop.
```

**Diagnosis Steps:**
1. Check for state updates in render body
2. Check for missing dependencies in `useEffect`
3. Check for callbacks created in render

**Solution:**
```typescript
// ❌ State update in render
export const BadComponent: React.FC = () => {
  const [count, setCount] = useState(0);

  setCount(count + 1);  // ❌ Updates on every render!

  return <div>{count}</div>;
};

// ✅ Use useEffect for side effects
export const GoodComponent: React.FC = () => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(1);  // Only runs once
  }, []);

  return <div>{count}</div>;
};
```

#### Issue: State Not Updating

**Symptom:**
```typescript
setState(newValue);
console.log(state);  // Still shows old value
```

**Diagnosis:**
- State updates are asynchronous
- React batches updates

**Solution:**
```typescript
// ❌ Trying to read immediately after set
setState(newValue);
console.log(state);  // Old value

// ✅ Use useEffect to read updated state
setState(newValue);
useEffect(() => {
  console.log(state);  // New value
}, [state]);

// ✅ Or use functional updates if new state depends on old
setState(prev => prev + 1);
```

#### Issue: Hooks Called in Wrong Order

**Symptom:**
```
Error: Invalid hook call. Hooks can only be called inside of the body of a function component.
```

**Diagnosis:**
- Hooks in conditions
- Hooks in loops
- Hooks in nested functions

**Solution:**
```typescript
// ❌ Hook in condition
if (condition) {
  const [value, setValue] = useState(0);
}

// ✅ Hooks at top level
const [value, setValue] = useState(0);
if (condition) {
  // Use value here
}
```

### Tauri Integration Issues

#### Issue: Type Mismatch Error

**Symptom:**
```
Error: Type 'string' is not assignable to type 'number'
```

**Diagnosis Steps:**
1. Check Rust DTO field types
2. Check `bindings.ts` generated types
3. Check for `#[serde(alias)]` if needed
4. Verify `#[specta(inline)]` is present

**Solution:**
```rust
// Rust DTO
#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct CreateFormulaDto {
    #[serde(alias = "formulaName")]  // Accept both name/formulaName
    pub name: String,

    #[serde(alias = "formulaId")]
    pub id: i64,
}
```

```typescript
// TypeScript
const result = await commands.createFormula({
  name: "Test",      // ✅ or formulaName: "Test"
  id: 123,           // ✅ or formulaId: 123
});
```

#### Issue: Command Returns Success but Data is Null

**Symptom:**
```typescript
const result = await commands.getFormula(123);
console.log(result); // { success: true, data: null }
```

**Diagnosis:**
- Check if `ApiResponse<T>` wrapping is correct
- Verify `api_ok()` is used correctly

**Solution:**
```rust
// ❌ Forgetting to wrap data
#[tauri::command]
pub async fn get_formula(id: i64) -> Formula {
    // Returns Formula directly, not wrapped
}

// ✅ Proper ApiResponse wrapping
#[tauri::command]
pub async fn get_formula(id: i64) -> ApiResponse<Formula> {
    match formula_service.get(id).await {
        Ok(formula) => api_ok(formula),
        Err(e) => api_err(format!("获取失败: {}", e)),
    }
}
```

### Database Issues

#### Issue: "No such table" Error

**Symptom:**
```
Error: no such table: formulas
```

**Diagnosis Steps:**
```bash
# Check if migrations ran
sqlite3 feed_formula.db ".schema formulas"

# Check migrations folder
ls -la migrations/
```

**Solution:**
```bash
# Run migrations
sqlx migrate run --database-url sqlite:feed_formula.db

# Or in code
sqlx::migrate!("./migrations")
    .run(&pool)
    .await
    .expect("Failed to run migrations");
```

#### Issue: Query Returns Empty Results

**Symptom:**
```rust
let result = sqlx::query_as!(Material, "SELECT * FROM materials")
    .fetch_all(&pool)
    .await?;
// result is empty Vec, but data exists
```

**Diagnosis:**
```bash
# Verify data exists
sqlite3 feed_formula.db "SELECT COUNT(*) FROM materials"

# Check exact query
sqlite3 feed_formula.db "SELECT * FROM materials LIMIT 5"
```

**Common Causes:**
- Different database file (check path)
- Uncommitted transaction
- Wrong WHERE clause

**Solution:**
```rust
// Check database path
let db_path = std::path::Path::new("feed_formula.db");
println!("Using database: {:?}", db_path.canonicalize());

// Ensure queries are committed
let mut tx = pool.begin().await?;
// ... do work ...
tx.commit().await?;  // Don't forget this!
```

## Debugging Tools & Techniques

### 1. Logging Strategy

**Rust (using tracing):**
```rust
use tracing::{info, warn, error, debug, instrument};

#[instrument(skip(self))]
pub async fn optimize_formula(&self, formula_id: i64) -> Result<Formula> {
    info!(formula_id, "Starting optimization");

    let formula = self.get_formula(formula_id).await
        .context("Failed to load formula")?;
    debug!(material_count = formula.materials.len(), "Formula loaded");

    let result = self.run_optimization(&formula).await?;
    info!(cost = result.total_cost, "Optimization complete");

    Ok(result)
}
```

**React (no console.log):**
```typescript
import { message } from 'antd';

// ✅ User-facing debug info
message.info(`Loaded ${data.length} items`);

// ✅ Conditional debug component
{process.env.NODE_ENV === 'development' && (
  <Alert
    type="info"
    message="Debug Info"
    description={<pre>{JSON.stringify(data, null, 2)}</pre>}
  />
)}
```

### 2. Debug Assertions

**Rust:**
```rust
// Debug-only checks
debug_assert!(price >= 0.0, "Price cannot be negative");

// Runtime checks
assert!(
    materials.len() <= 100,
    "Too many materials: {}", materials.len()
);
```

**TypeScript:**
```typescript
// Type guards
function isFormula(data: unknown): data is Formula {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'name' in data
  );
}

// Usage
if (isFormula(result)) {
  // TypeScript knows it's a Formula now
  console.log(result.name);
}
```

### 3. Breakpoints & Inspection

**Rust (using debugger):**
```bash
# Install rust-tools
rustup component add rust-src

# Run with debugger
rust-lldb -- target/debug/cacrfeedformula

# In debugger
(lldb) breakpoint set --file src/formula/service.rs --line 42
(lldb) run
(lldb) print formula_id
(lldb) continue
```

**React:**
```typescript
// Add debugger statement
useEffect(() => {
  debugger;  // Pauses execution in browser dev tools
  const data = await fetchData();
  setState(data);
}, []);
```

### 4. Binary Search Debugging

**Narrow down problematic code:**

```rust
// Comment out half the code
// If error disappears, bug is in commented half
// Otherwise, bug is in active half

#[tauri::command]
pub async fn complex_operation(dto: Dto) -> ApiResponse<Result> {
    // First half
    let result1 = step1(&dto).await?;

    // Comment out second half to isolate
    // let result2 = step2(&result1).await?;
    // let result3 = step3(&result2).await?;

    api_ok(result1)
}
```

## Performance Debugging

### Identifying Slow Operations

**Rust:**
```rust
use std::time::Instant;

pub async fn slow_function() -> Result<()> {
    let start = Instant::now();

    // Operation 1
    let data = fetch_data().await?;
    println!("fetch_data: {:?}", start.elapsed());

    // Operation 2
    let result = process_data(&data)?;
    println!("process_data: {:?}", start.elapsed());

    Ok(())
}
```

**Flamegraphs:**
```bash
# Install flamegraph
cargo install flamegraph

# Generate flamegraph
cargo flamegraph --bin cacrfeedformula

# View output
open flamegraph.svg
```

**React Profiler:**
```typescript
import { Profiler } from 'react';

<Profiler id="FormulaList" onRender={(id, phase, actualDuration) => {
  if (process.env.NODE_ENV === 'development') {
    console.log(`${id} (${phase}) took ${actualDuration}ms`);
  }
}}>
  <FormulaList />
</Profiler>
```

## Debugging Checklist

### Initial Assessment
- [ ] What exactly is the error/symptom?
- [ ] When does it happen? (Consistently? Intermittently?)
- [ ] What was the last change that worked?
- [ ] Error message and stack trace captured?

### Information Gathering
- [ ] Backend logs checked (Rust tracing)
- [ ] Frontend checked (React DevTools)
- [ ] Database state verified
- [ ] Network requests inspected (if applicable)

### Hypothesis & Test
- [ ] Root cause hypothesis formed
- [ ] Created minimal reproduction case
- [ ] Test applied to verify hypothesis
- [ ] Confirmed or rejected hypothesis

### Fix & Verify
- [ ] Fix implemented
- [ ] Tests pass (including new tests for bug)
- [ ] Edge cases considered
- [ ] No regressions introduced

## Quick Reference

### Common Debug Commands

```bash
# Rust
cargo test                    # Run tests
cargo test -- --nocapture    # Show test output
RUST_LOG=debug cargo run     # Enable debug logging
rust-lldb target/debug/binary   # Debug with lldb

# Database
sqlite3 feed_formula.db "SELECT * FROM formulas LIMIT 5"
sqlite3 feed_formula.db ".schema"

# Frontend
npm run dev                  # Start dev server
npm run lint                 # Check for issues
npm run type-check           # Type checking
```

### Error Message Keywords

| Keyword | Likely Cause | Action |
|---------|--------------|--------|
| `unwrap()` | Panic on None/Err | Use proper error handling |
| `borrow` | Borrow checker issue | Check lifetimes, use references |
| `async` | Runtime/blocking mismatch | Use `await` or `spawn_blocking` |
| `cannot find` | Import/name issue | Check imports and spelling |
| `type mismatch` | Type error | Check types, add conversions |
| `expected` | Syntax error | Fix syntax near error location |

## When to Use This Skill

Activate this skill when:
- Diagnosing errors or crashes
- Investigating unexpected behavior
- Fixing failing tests
- Tracking down bugs
- Analyzing performance issues
- Troubleshooting integration problems
- Learning from past issues
