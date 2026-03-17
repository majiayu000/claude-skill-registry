---
name: api-design
description: 当用户要求API/接口/DTO设计、请求响应结构、分页、命名规范或校验规则时使用。
---

# API Design Skill

## 适用范围
- 设计或调整 Tauri 命令接口
- 设计 DTO/响应结构
- 统一命名与校验策略

## 关键规则（Critical Rules）
- 外层响应统一 `ApiResponse<T>`
- DTO 使用 `serde` + `specta::Type`，字段 camelCase 与前端一致
- 校验在命令边界完成，业务层返回 `anyhow::Result` 并补充上下文
- 错误信息面向用户，简洁明确

## 标准响应
```rust
#[derive(serde::Serialize, specta::Type)]
#[specta(inline)]
pub struct ApiResponse<T: specta::Type> {
    pub success: bool,
    pub data: Option<T>,
    pub error: Option<String>,
}
```

## DTO 规范（示例）
```rust
#[derive(Debug, Clone, Serialize, Deserialize, specta::Type)]
#[serde(rename_all = "camelCase")]
pub struct CreateFactoryDto {
    pub factory_code: Code,
    pub factory_name: Name,
    pub description: Description,
    pub address: Option<String>,
    pub contact: Option<String>,
    pub phone: Option<String>,
    pub is_active: Boolean,
}
```

## 命名与契约
- 命令：动词 + 名词（`get`/`create`/`update`/`delete`）
- DTO：`CreateXDto` / `UpdateXDto` / `XDto`
- 前后端字段统一 camelCase，Rust 侧使用 `#[serde(rename_all = "camelCase")]`

## 分页与列表
- 优先复用现有类型：`crate::material::material_service::MaterialsPage` / `MaterialsPaginatedResult`
- 返回列表时保持字段可直接渲染，避免二次拼装

## 校验建议
- 对 `String` 长度、`Option` 必填进行检查
- SQLx 之前完成基本校验，避免 DB 错误直接暴露

## 检查清单
- [ ] 响应使用 `ApiResponse<T>`
- [ ] DTO 实现 `specta::Type` 且字段 camelCase
- [ ] 校验在命令边界完成
- [ ] 命名与既有命令风格一致
