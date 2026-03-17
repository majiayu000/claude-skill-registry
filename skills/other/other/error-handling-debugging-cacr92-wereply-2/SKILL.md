---
name: error-handling-debugging
description: 当用户要求"处理错误"、"错误处理"、"捕获异常"、"错误恢复"，或者提到"错误处理"、"error handling"、"异常"时使用此技能。用于处理 Rust 或 TypeScript 中的错误、调试问题、排查 Tauri 命令失败、修复数据库错误或实现错误恢复策略。
version: 2.0.0
---

# Error Handling & Debugging Skill

Comprehensive error handling and debugging strategies for Tauri + Rust + React applications.

## Rust Error Handling

### Error Chain with anyhow

```rust
use anyhow::{Context, Result, anyhow, bail};

pub async fn complex_operation(&self) -> Result<Output> {
    let data = self.fetch_data()
        .await
        .context("获取数据失败")?;

    if data.is_empty() {
        bail!("数据为空，无法继续处理");
    }

    let processed = self.process_data(&data)
        .context("处理数据失败")?;

    Ok(processed)
}
```

### ApiResponse Conversion Pattern

```rust
use crate::utils::error::{api_err, api_ok, ApiResponse};

#[tauri::command]
#[specta::specta]
pub async fn handle_formula_request(
    dto: FormulaDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<Formula> {
    // Using with_service helper for automatic error conversion
    with_service(state, |ctx| async move {
        ctx.formula_service.create_formula(dto).await
    })
    .await
}

// Manual conversion
#[tauri::command]
#[specta::specta]
pub async fn manual_error_handling() -> ApiResponse<Data> {
    match perform_operation().await {
        Ok(data) => api_ok(data),
        Err(e) => {
            // Log error internally
            error!("Operation failed: {:?}", e);
            // Return user-friendly message
            api_err(format!("操作失败，请检查输入后重试"))
        }
    }
}
```

### Custom Error Types

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum FormulaError {
    #[error("配方不存在: {id}")]
    FormulaNotFound { id: i64 },

    #[error("营养约束冲突: {nutrient}")]
    NutritionConflict { nutrient: String },

    #[error("优化失败: {reason}")]
    OptimizationFailed { reason: String },

    #[error("数据库错误: {0}")]
    Database(#[from] sqlx::Error),

    #[error("IO错误: {0}")]
    Io(#[from] std::io::Error),
}

impl From<FormulaError> for ApiResponse<()> {
    fn from(err: FormulaError) -> Self {
        match err {
            FormulaError::FormulaNotFound { id } => {
                api_err(format!("配方 ID {} 不存在", id))
            }
            FormulaError::NutritionConflict { nutrient } => {
                api_err(format!("营养约束 {nutrient} 冲突，请调整约束范围"))
            }
            FormulaError::OptimizationFailed { reason } => {
                api_err(format!("配方优化失败: {}", reason))
            }
            _ => api_err(format!("操作失败: {}", err)),
        }
    }
}
```

## TypeScript Error Handling

### Try-Catch with User Feedback

```typescript
import { message } from 'antd';
import { commands } from '../bindings';

export async function safeExecute<T>(
  operation: () => Promise<ApiResponse<T>>,
  errorMessage: string = '操作失败'
): Promise<T | null> {
  try {
    const result = await operation();
    if (!result.success) {
      message.error(result.message || errorMessage);
      return null;
    }
    return result.data;
  } catch (error) {
    message.error(`${errorMessage}: ${error instanceof Error ? error.message : String(error)}`);
    return null;
  }
}

// Usage
const formula = await safeExecute(
  () => commands.getFormula(id),
  '加载配方失败'
);
```

### Error Boundaries

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Result, Button } from 'antd';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Result
          status="error"
          title="发生错误"
          subTitle={this.state.error?.message}
          extra={
            <Button type="primary" onClick={() => window.location.reload()}>
              刷新页面
            </Button>
          }
        />
      );
    }

    return this.props.children;
  }
}
```

## Debugging Techniques

### Rust Debugging

#### Tracing Instrumentation

```rust
use tracing::{info, debug, error, instrument};
use tracing_subscriber;

pub fn init_logging() {
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::DEBUG)
        .init();
}

#[instrument(skip(self))]
pub async fn optimize_formula(&self, formula_id: i64) -> Result<Formula> {
    info!(formula_id, "开始优化配方");

    let formula = self.get_formula(formula_id).await?;
    debug!(material_count = formula.materials.len(), "加载配方原料");

    let result = self.run_optimization(&formula).await?;
    info!(cost = result.total_cost, "优化完成");

    Ok(result)
}
```

#### Structured Debugging

```rust
#[derive(Debug)]
pub struct OptimizationContext {
    pub formula_id: i64,
    pub material_count: usize,
    pub constraint_count: usize,
    pub start_time: std::time::Instant,
}

impl OptimizationContext {
    pub fn log_summary(&self) {
        debug!(
            formula_id = self.formula_id,
            material_count = self.material_count,
            constraint_count = self.constraint_count,
            elapsed_ms = self.start_time.elapsed().as_millis(),
            "优化上下文信息"
        );
    }
}
```

### TypeScript Debugging

#### Debug Component (No console.log!)

```typescript
import { Alert } from 'antd';

interface DebugInfoProps {
  data: unknown;
  title?: string;
}

export const DebugInfo: React.FC<DebugInfoProps> = ({ data, title }) => {
  if (process.env.NODE_ENV === 'production') {
    return null;
  }

  return (
    <Alert
      type="info"
      message={title || 'Debug Info'}
      description={
        <pre style={{ maxHeight: 200, overflow: 'auto' }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      }
      closable
    />
  );
};
```

## Common Error Patterns & Solutions

### Database Errors

#### Connection Pool Exhausted

```rust
// Error: Pool exhausted
// Solution: Increase pool size or reduce concurrent operations

let pool = SqlitePoolOptions::new()
    .max_connections(10)  // Increase from 5
    .acquire_timeout(Duration::from_secs(60))  // Increase timeout
    .connect(&database_url)
    .await?;
```

#### Lock Timeout

```rust
// Error: Database is locked
// Solution: Enable WAL mode and reduce transaction time

sqlx::query("PRAGMA journal_mode=WAL")
    .execute(&pool)
    .await?;

sqlx::query("PRAGMA busy_timeout=5000")  // 5 second timeout
    .execute(&pool)
    .await?;
```

### Tauri Command Errors

#### Type Mismatch

```rust
// Error: Failed to deserialize
// Solution: Ensure types match between Rust and TypeScript

// Rust
#[derive(Serialize, Deserialize, Type)]
#[serde(rename_all = "camelCase")]  // Match TypeScript naming
pub struct CreateFormulaDto {
    pub formula_name: String,  // camelCase
    pub species_code: String,
}

// TypeScript
interface CreateFormulaDto {
  formulaName: string;  // camelCase
  speciesCode: string;
}
```

#### Missing specta Attributes

```rust
// Error: Type not exported
// Solution: Add #[specta::specta] and #[specta(inline)]

#[derive(Serialize, Deserialize, Type)]
#[specta(inline)]  // Required for inline export
pub struct MaterialDto {
    pub code: String,
    pub name: String,
}

#[tauri::command]
#[specta::specta]  // Required for command
pub async fn create_material(dto: MaterialDto) -> ApiResponse<Material> {
    // ...
}
```

### React Errors

#### Hook Dependency Warning

```typescript
// Warning: React Hook dependency missing
// Solution: Include all dependencies

// ❌ Bad
useEffect(() => {
  fetchData(userId, category);
}, [userId]);  // Missing 'category'

// ✅ Good
useEffect(() => {
  fetchData(userId, category);
}, [userId, category]);  // All dependencies
```

#### Memory Leaks

```typescript
// Warning: Can't perform a React state update on an unmounted component
// Solution: Cleanup effects

useEffect(() => {
  let isMounted = true;

  const fetchData = async () => {
    const result = await commands.getData();
    if (isMounted) {
      setData(result);
    }
  };

  fetchData();

  return () => {
    isMounted = false;  // Cleanup
  };
}, []);
```

## Error Recovery Strategies

### Retry Logic

```rust
use tokio::time::{sleep, Duration};
use backoff::{ExponentialBackoff, future::retry};

pub async fn retry_operation<T, E, Fn, Fut>(mut operation: Fn) -> Result<T, E>
where
    Fn: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, E>>,
    E: std::fmt::Debug,
{
    let mut attempts = 0;
    let max_attempts = 3;

    loop {
        match operation().await {
            Ok(result) => return Ok(result),
            Err(e) => {
                attempts += 1;
                if attempts >= max_attempts {
                    error!("操作失败，已重试 {} 次", max_attempts);
                    return Err(e);
                }
                warn!("操作失败，第 {} 次重试", attempts);
                sleep(Duration::from_millis(1000 * attempts as u64)).await;
            }
        }
    }
}
```

### Graceful Degradation

```typescript
export function useFormulaData(formulaId: number) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['formula', formulaId],
    queryFn: async () => {
      const result = await commands.getFormula(formulaId);
      if (!result.success) throw new Error(result.message);
      return result.data;
    },
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });

  // Graceful degradation
  if (error) {
    return {
      data: null,
      isLoading: false,
      error,
      // Provide fallback data
      fallbackData: {
        id: formulaId,
        name: '加载失败',
        materials: [],
      },
    };
  }

  return { data, isLoading, error: null };
}
```

## Logging Strategy

### Rust Logging Levels

```rust
use tracing::{error, warn, info, debug, trace};

// ERROR: Application errors requiring immediate attention
error!(
    error = ?e,
    formula_id = id,
    "配方优化失败"
);

// WARN: Warning messages, potentially harmful situations
warn!(
    formula_id = id,
    "配方未满足所有营养约束"
);

// INFO: Important informational messages
info!(
    formula_id = id,
    cost = result.total_cost,
    "配方优化成功"
);

// DEBUG: Detailed diagnostic information
debug!(
    material_count = materials.len(),
    constraint_count = constraints.len(),
    "开始优化"
);

// TRACE: Very detailed diagnostic information
trace!("详细追踪信息");
```

### Desktop Application Logging (No console!)

```typescript
// ❌ Bad - Console logging
console.log('Data loaded', data);
console.error('Error', error);

// ✅ Good - User-facing messages
import { message } from 'antd';

// For debugging: use debug component or send to backend
message.success('数据加载成功');
message.error('加载失败');

// Optional: implement debug logger that sends to Rust backend
export async function debugLog(level: 'info' | 'warn' | 'error', message: string) {
  if (process.env.NODE_ENV === 'development') {
    await commands.debugLog({ level, message });
  }
}
```

## Testing Error Scenarios

### Rust Error Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_formula_not_found() {
        let result = FormulaService::new(pool)
            .get_formula(99999)
            .await;

        assert!(result.is_err());
        match result {
            Err(FormulaError::FormulaNotFound { id }) => {
                assert_eq!(id, 99999);
            }
            _ => panic!("Expected FormulaNotFound error"),
        }
    }
}
```

### TypeScript Error Tests

```typescript
describe('Error Handling', () => {
  it('should handle API errors gracefully', async () => {
    const mockCommands = {
      getFormula: vi.fn().mockResolvedValue({
        success: false,
        message: '配方不存在',
      }),
    };

    const { result } = renderHook(() => useFormula(1, { commands: mockCommands }));

    await waitFor(() => {
      expect(result.current.error).toBeTruthy();
      expect(result.current.data).toBeNull();
    });
  });
});
```

## When to Use This Skill

Activate this skill when:
- Implementing error handling in Rust or TypeScript
- Debugging application issues
- Investigating Tauri command failures
- Handling database errors
- Implementing retry logic
- Writing logging code
- Creating error recovery strategies
- Testing error scenarios
- Troubleshooting type errors
- Fixing memory leaks
- Resolving performance issues
