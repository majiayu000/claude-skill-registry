---
name: tauri-development
description: 当用户要求Tauri命令、Rust后端/前端联调、tauri-specta类型导出、bindings.ts调用或提到Tauri时使用。
---

# Tauri Development Skill

## 适用范围
- 新增/修改 Tauri 命令或 State 服务访问器
- Rust 后端与前端命令联调、类型导出
- 需要通过 `frontend/src/bindings.ts` 调用 Tauri 命令

## 关键规则（Critical Rules）
- 每个命令必须同时包含 `#[tauri::command]` 与 `#[specta::specta]`
- 命令入参/出参类型必须实现 `specta::Type`，必要时加 `#[specta(inline)]`
- 统一返回 `Result<ApiResponse<T>, String>`，使用 `api_ok` / `api_err` / `with_service`
- 前端只使用 `frontend/src/bindings.ts` 的 `commands`，禁止直接 `invoke`
- 数据库访问优先 `sqlx::query_as!` 且显式列名，写操作使用事务

## 快速模板
### 命令实现（基于现有服务）
```rust
use tauri::State;
use crate::tauri_app::TauriAppState;
use crate::utils::error::{ApiResponse, with_service};

#[tauri::command]
#[specta::specta]
pub async fn get_material_nutritions(
    state: State<'_, TauriAppState>,
    factory_code: String,
    material_code: String,
) -> Result<ApiResponse<Vec<crate::material::material_nutrition::MaterialNutrition>>, String> {
    let material_svc = state.get_material_service().await?;
    with_service(
        Ok(material_svc),
        |svc| async move {
            svc.get_material_nutritions(&material_code, &factory_code).await
        },
        "获取营养指标失败",
    )
    .await
}
```

### DTO 类型
```rust
#[derive(serde::Serialize, specta::Type, Clone)]
#[specta(inline)]
pub struct InitializationStatus {
    pub initialized: bool,
    pub message: String,
}
```

### 前端调用
```ts
import { commands } from '../bindings';
import { message } from 'antd';

export async function loadFactories(keyword: string | null) {
  const res = await commands.getAllFactories(keyword, null);
  if (res.status === 'error') {
    message.error(String(res.error));
    return [] as const;
  }
  const { success, data, error } = res.data;
  if (!success || !data) {
    message.error(error ?? '加载失败');
    return [] as const;
  }
  return data;
}
```

## 工作流程
1. 设计命令签名与 DTO（Rust/TS 字段一致）
2. 实现命令并返回 `ApiResponse`
3. 按项目既有流程更新 `frontend/src/bindings.ts`
4. 前端接入 `commands` 并补齐错误提示

## 检查清单
- [ ] 命令含 `#[tauri::command]` 与 `#[specta::specta]`
- [ ] 入参/出参实现 `specta::Type`
- [ ] 统一 `ApiResponse`，错误信息可直达用户
- [ ] 前端仅使用 `commands`