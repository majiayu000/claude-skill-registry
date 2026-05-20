---
name: error-handling-debugging
description: 当用户要求错误处理、异常链路、错误提示或调试技巧时使用。
---

# Error Handling & Debugging Skill

## 适用范围
- Rust 错误链路与上下文
- Tauri 命令错误转换
- 前端用户提示与错误恢复

## 关键规则（Critical Rules）
- Rust 侧用 `anyhow::Context` 补充错误信息
- Tauri 命令统一返回 `ApiResponse<T>`
- 前端错误必须 `message.error` 提示用户

## Rust 错误链示例
```rust
use anyhow::{Context, Result};
use std::path::Path;

pub fn load_config(path: &Path) -> Result<String> {
    std::fs::read_to_string(path)
        .with_context(|| format!("读取配置失败: {}", path.display()))
}
```

## Tauri 命令错误转换
```rust
#[tauri::command]
#[specta::specta]
pub async fn get_settings() -> Result<ApiResponse<SettingsData>, String> {
    match get_settings_data_service().await {
        Ok(settings_data) => Ok(ApiResponse::success(settings_data)),
        Err(e) => Ok(ApiResponse::error(format!("获取设置数据失败: {}", e))),
    }
}
```

## 前端错误提示
```ts
import { message } from 'antd';

export function showError(text: string) {
  message.error(text);
}
```

## 检查清单
- [ ] Rust 错误带上下文
- [ ] Tauri 命令返回 `ApiResponse`
- [ ] 前端使用 `message.error` 提示
