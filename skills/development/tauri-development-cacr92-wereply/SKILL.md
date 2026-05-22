---
name: tauri-development
description: 当用户要求"创建 Tauri 命令"、"添加后端命令"、"集成 Rust 和 React"、"设置 specta 类型"、"从前端调用 Tauri"、"优化 Tauri 性能"、"处理 Tauri 错误"、"前后端类型不一致"、"更新 bindings.ts"、"specta 类型问题"、"跨平台桌面开发"、"窗口管理"、"文件系统访问"、"系统托盘"，或者提到"Tauri"、"桌面应用"、"命令通信"、"类型绑定"、"桌面 UI"时使用此技能。用于饲料配方系统的 Tauri 特定模式、Rust 后端集成、前后端通信、类型安全保障或使用 Tauri 2.0 开发跨平台桌面应用。
version: 4.0.0
---

# Tauri Development Skill

Expert guidance for Tauri 2.0 desktop application development with Rust backend and React TypeScript frontend.

## Overview

This skill provides comprehensive guidance for:
- Creating Tauri commands with proper specta type binding
- Integrating Rust backend with React TypeScript frontend
- Handling desktop-specific patterns and constraints
- Optimizing frontend-backend communication
- Following Tauri 2.0 best practices

## When This Skill Applies

This skill activates when:
- Creating or modifying Tauri commands
- Setting up specta type bindings
- Debugging frontend-backend communication issues
- Implementing desktop-specific features
- Optimizing Tauri application performance
- Handling Tauri-specific error cases

## Core Tauri Principles

### Command Definition Pattern
All Tauri commands must follow this pattern:

```rust
use serde::{Deserialize, Serialize};
use specta::Type;

#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct MyDto {
    pub field: String,
}

#[tauri::command]
#[specta::specta]
pub async fn my_command(
    dto: MyDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<ResultType> {
    // Implementation
}
```

**Key Requirements:**
- `#[tauri::command]` - Required for all commands
- `#[specta::specta]` - Required for TypeScript type generation
- `#[specta(inline)]` - Required on DTOs for proper type export
- `ApiResponse<T>` - Unified return type for error handling

### Frontend Command Usage
**✓ Correct:**
```typescript
import { commands } from '../bindings';

const result = await commands.myCommand({ field: "value" });
if (!result.success) {
    message.error(result.message);
    return;
}
const data = result.data;
```

**✗ Incorrect:**
```typescript
// ✗ Don't use raw invoke
import { invoke } from '@tauri-apps/api/core';
const result = await invoke('my_command', { dto });
```

## Common Patterns

### State Management
Use dependency injection for services:

```rust
pub struct TauriAppState {
    pub db: Arc<SqlitePool>,
    pub material_service: Arc<MaterialService>,
}

pub async fn get_state() -> TauriAppState {
    TauriAppState {
        db: Arc::new(pool),
        material_service: Arc::new(MaterialService::new(pool)),
    }
}
```

### Error Handling
Always use ApiResponse for top-level commands:

```rust
use crate::utils::error::{api_err, api_ok, ApiResponse};

#[tauri::command]
#[specta::specta]
pub async fn some_command() -> ApiResponse<Data> {
    match inner_logic().await {
        Ok(data) => api_ok(data),
        Err(e) => api_err(format!("操作失败: {}", e)),
    }
}
```

### Async/Await Best Practices
- Use `async` for external-facing commands
- Use sync functions for pure computations
- Never block the async runtime with `std::thread::sleep`
- Use `tokio::time::sleep` instead

## Tauri-Specific Considerations

### Desktop Application Constraints
1. **No console.log** - Use Ant Design message components
2. **File paths** - Use `path.resolve` for cross-platform compatibility
3. **Native dialogs** - Use Tauri APIs for file dialogs
4. **System integration** - Leverage native OS features

### Performance Optimization
- Use `moka::future::Cache` for frequently accessed data
- Implement proper connection pooling for SQLite
- Use `rayon` for CPU-intensive parallel computations
- Minimize bridge calls between frontend and backend

### Security Considerations
- Validate all user input on both frontend and backend
- Use SQL parameter binding (never string concatenation)
- Sanitize file paths to prevent directory traversal
- Implement proper error handling without exposing sensitive info

## Common Pitfalls

### ❌ Blocking Async Runtime
```rust
// ✗ Blocks entire runtime
pub async fn bad() {
    std::thread::sleep(Duration::from_secs(1));
}
```

### ✅ Proper Async Sleep
```rust
// ✓ Async-friendly
pub async fn good() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}
```

### ❌ SELECT * in Queries
```rust
// ✗ Inefficient, unclear
sqlx::query_as!("SELECT * FROM materials WHERE code = ?", code)
```

### ✅ Explicit Column Selection
```rust
// ✓ Clear intent, optimized
sqlx::query_as!(
    Material,
    "SELECT code, name, price FROM materials WHERE code = ?",
    code
)
```

## Type Generation Workflow

1. Define Rust types with `#[specta::specta]` and `#[specta(inline)]`
2. Run `npm run tauri build` or development server
3. Types are automatically generated in `frontend/src/bindings.ts`
4. Import and use types in TypeScript code

## Testing Guidelines

### Backend Testing
- Unit tests for pure functions
- Integration tests for database operations
- Use test database fixtures

### Frontend Testing
- Test command success/error paths
- Mock Tauri commands in tests
- Verify type safety across the bridge

## When to Use This Skill

Activate this skill when:
- Creating or modifying Tauri commands
- Debugging frontend-backend communication
- Optimizing Tauri application performance
- Handling Tauri-specific error cases
- Planning new features with Tauri constraints

## Quick Reference

### Essential Tauri Command Template

```rust
#[tauri::command]
#[specta::specta]
pub async fn command_name(
    dto: RequestDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<ResponseData> {
    with_service(state, |ctx| async move {
        ctx.service.do_work(dto).await
    })
    .await
}
```

### Frontend Command Call Template

```typescript
import { commands } from '../bindings';

const result = await commands.commandName({ field: "value" });
if (!result.success) {
    message.error(result.message);
    return;
}
const data = result.data;
```

### Required Attributes Checklist

- [ ] `#[tauri::command]` on all commands
- [ ] `#[specta::specta]` on all commands
- [ ] `#[specta(inline)]` on all DTOs
- [ ] Return type `ApiResponse<T>`
- [ ] Use `commands` from bindings (not `invoke`)
- [ ] Handle errors with message component
- [ ] No console.log in desktop app

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Types not generated | Run dev server or rebuild |
| Command not found | Check `#[tauri::command]` attribute |
| Type mismatch | Verify `#[specta(inline)]` on DTOs |
| Runtime blocking | Use async/await, not blocking calls |
| Console logs in app | Use `message` component instead |

### Frontmatter Fields Summary

| Field | Value | Purpose |
|-------|-------|---------|
| `#[tauri::command]` | - | Exposes function to frontend |
| `#[specta::specta]` | - | Enables type generation |
| `#[specta(inline)]` | - | Inlines type in bindings.ts |
| `ApiResponse<T>` | - | Unified error handling |

## Additional Resources

### Project References
- [Rust Backend Standards](../../rules/02-rust-backend-standards.md)
- [React Frontend Standards](../../rules/03-react-frontend-standards.md)

### Official Documentation
- [Tauri 2.0 Documentation](https://tauri.app/v1/guids/)
- [specta Documentation](https://specta.quatri.dev/)
- [Claude Code Tauri Guide](https://docs.anthropic.com/en/docs/build-with-claude/claude-code)
