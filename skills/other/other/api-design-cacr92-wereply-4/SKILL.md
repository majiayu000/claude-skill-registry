---
name: api-design
description: 当用户要求"设计API"、"创建DTO"、"定义数据结构"、"API文档"、"请求响应格式"，或者提到"API设计"、"数据传输对象"、"契约"、"接口"时使用此技能。用于 API 设计模式、数据建模、类型安全或后端 API 结构设计。
version: 2.0.0
---

# API Design Skill

Expert guidance for designing robust, type-safe APIs and data structures in Tauri applications.

## Overview

This skill provides guidance for:
- Designing Tauri command APIs
- Creating type-safe DTOs (Data Transfer Objects)
- API documentation and contracts
- Request/response patterns
- Error handling in APIs
- API versioning and evolution

## When This Skill Applies

This skill activates when:
- Creating new Tauri commands
- Designing request/response DTOs
- Planning API structure
- Documenting API contracts
- Refactoring existing APIs
- Handling API versioning

## API Design Principles

### 1. Type Safety First

**✓ Good: Explicit, typed structures**

```rust
use serde::{Deserialize, Serialize};
use specta::Type;

#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct CreateFormulaDto {
    /// Formula name (2-100 characters)
    #[serde(alias = "formulaName")]
    pub name: String,

    /// Species code (e.g., "pig", "chicken")
    #[serde(alias = "speciesCode")]
    pub species_code: String,

    /// Optional description
    pub description: Option<String>,

    /// Formula materials
    pub materials: Vec<FormulaMaterialDto>,
}

#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct FormulaMaterialDto {
    /// Material code
    #[serde(alias = "materialCode")]
    pub material_code: String,

    /// Proportion in percentage (0-100)
    pub proportion: f64,
}
```

**✗ Bad: Untyped or generic structures**

```rust
// ✗ Avoid generic maps
pub type RequestData = HashMap<String, serde_json::Value>;

// ✗ Avoid raw JSON
pub fn create_formula(data: serde_json::Value) -> Result<Formula>;
```

### 2. Consistent Naming Conventions

**Rust → TypeScript Mapping:**

| Rust | TypeScript | Notes |
|------|-------------|-------|
| `snake_case` | `camelCase` | Auto-converted by specta |
| `formula_id` | `formulaId` | Use `#[serde(alias)]` for compatibility |
| `species_code` | `speciesCode` | Keep consistent |

```rust
#[derive(Serialize, Deserialize, Type)]
pub struct ApiResponse {
    pub formula_id: i64,       // TypeScript: formulaId
    pub species_code: String,   // TypeScript: speciesCode
    pub total_cost: f64,        // TypeScript: totalCost
}
```

### 3. Validation at API Boundaries

```rust
use validators::Validators;

#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct CreateFormulaDto {
    pub name: String,
    pub species_code: String,
    pub materials: Vec<FormulaMaterialDto>,
}

impl CreateFormulaDto {
    pub fn validate(&self) -> Result<(), ValidationError> {
        // Validate name
        if self.name.is_empty() {
            return Err(ValidationError {
                field: "name".to_string(),
                message: "名称不能为空".to_string(),
            });
        }

        if self.name.len() > 100 {
            return Err(ValidationError {
                field: "name".to_string(),
                message: "名称不能超过100个字符".to_string(),
            });
        }

        // Validate materials
        if self.materials.is_empty() {
            return Err(ValidationError {
                field: "materials".to_string(),
                message: "至少需要一种原料".to_string(),
            });
        }

        let total_proportion: f64 = self.materials
            .iter()
            .map(|m| m.proportion)
            .sum();

        if (total_proportion - 100.0).abs() > 0.01 {
            return Err(ValidationError {
                field: "materials".to_string(),
                message: format!("原料总比例必须为100%，当前为{}", total_proportion),
            });
        }

        Ok(())
    }
}

#[tauri::command]
#[specta::specta]
pub async fn create_formula(
    dto: CreateFormulaDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<Formula> {
    // Validate before processing
    if let Err(e) = dto.validate() {
        return api_err(format!("参数验证失败: {}", e.message));
    }

    // Proceed with creation
    with_service(state, |ctx| async move {
        ctx.formula_service.create_validated(dto).await
    })
    .await
}
```

## Request/Response Patterns

### Standard Response Format

```rust
use serde::{Deserialize, Serialize};
use specta::Type;

/// Standard API response wrapper
#[derive(Serialize, Deserialize, Type)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub message: Option<String>,
    pub code: Option<String>,
}

impl<T> ApiResponse<T> {
    pub fn ok(data: T) -> Self {
        Self {
            success: true,
            data: Some(data),
            message: None,
            code: None,
        }
    }

    pub fn err(message: String) -> Self {
        Self {
            success: false,
            data: None,
            message: Some(message),
            code: Some("ERROR".to_string()),
        }
    }

    pub fn with_code(mut self, code: &str) -> Self {
        self.code = Some(code.to_string());
        self
    }
}
```

### Paginated Response

```rust
#[derive(Serialize, Deserialize, Type)]
#[specta(inline)]
pub struct PaginatedResponse<T> {
    pub data: Vec<T>,
    pub total: usize,
    pub page: usize,
    pub page_size: usize,
    pub total_pages: usize,
}

#[derive(Serialize, Deserialize, Type)]
#[specta(inline)]
pub struct PaginationParams {
    pub page: Option<usize>,
    pub page_size: Option<usize>,
    pub sort_by: Option<String>,
    pub sort_order: Option<SortOrder>,
}

#[tauri::command]
#[specta::specta]
pub async fn list_materials(
    params: PaginationParams,
    state: State<'_, TauriAppState>,
) -> ApiResponse<PaginatedResponse<Material>> {
    let page = params.page.unwrap_or(1);
    let page_size = params.page_size.unwrap_or(20);

    with_service(state, |ctx| async move {
        let result = ctx.material_service
            .paginate(page, page_size)
            .await?;
        api_ok(result)
    })
    .await
}
```

## Error Handling Patterns

### Structured Error Types

```rust
use thiserror::Error;

#[derive(Error, Debug, Serialize, Deserialize, Type)]
pub enum ApiError {
    #[error("Validation failed: {field} - {message}")]
    Validation { field: String, message: String },

    #[error("Resource not found: {resource} with id {id}")]
    NotFound { resource: String, id: i64 },

    #[error("Permission denied: {action}")]
    Permission { action: String },

    #[error("Conflict: {resource} already exists")]
    Conflict { resource: String },

    #[error("Internal server error: {0}")]
    Internal(String),
}

impl From<ApiError> for ApiResponse<()> {
    fn from(err: ApiError) -> Self {
        let (code, message) = match &err {
            ApiError::Validation { .. } => ("VALIDATION_ERROR", err.to_string()),
            ApiError::NotFound { .. } => ("NOT_FOUND", err.to_string()),
            ApiError::Permission { .. } => ("PERMISSION_DENIED", err.to_string()),
            ApiError::Conflict { .. } => ("CONFLICT", err.to_string()),
            ApiError::Internal(_) => ("INTERNAL_ERROR", "服务器内部错误".to_string()),
        };

        ApiResponse {
            success: false,
            data: None,
            message: Some(message),
            code: Some(code.to_string()),
        }
    }
}
```

## API Documentation

### Inline Documentation

```rust
/// Creates a new formula with the specified materials.
///
/// # Arguments
///
/// * `dto` - Formula creation data
///   - `name`: Formula name (2-100 characters)
///   - `species_code`: Target species code
///   - `materials`: List of materials with proportions
///
/// # Returns
///
/// Created formula with assigned ID
///
/// # Errors
///
/// - `VALIDATION_ERROR`: Invalid input data
/// - `CONFLICT`: Formula name already exists
///
/// # Example
///
/// ```typescript
/// const result = await commands.createFormula({
///   name: "Growing Pig Formula",
///   speciesCode: "pig",
///   materials: [
///     { materialCode: "corn", proportion: 50.0 },
///     { materialCode: "soybean", proportion: 50.0 }
///   ]
/// });
/// ```
#[tauri::command]
#[specta::specta]
pub async fn create_formula(
    dto: CreateFormulaDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<Formula> {
    // Implementation
}
```

### TypeScript Usage Documentation

Create corresponding TypeScript documentation:

```typescript
/**
 * Creates a new formula
 *
 * @param dto - Formula creation data
 * @param dto.name - Formula name (2-100 characters)
 * @param dto.speciesCode - Target species code (e.g., "pig", "chicken")
 * @param dto.materials - Array of materials with proportions
 * @returns Promise with created formula
 * @throws ValidationError if input data is invalid
 * @throws ConflictError if formula name already exists
 *
 * @example
 * ```typescript
 * const result = await commands.createFormula({
 *   name: "Growing Pig Formula",
 *   speciesCode: "pig",
 *   materials: [
 *     { materialCode: "corn", proportion: 50.0 },
 *     { materialCode: "soybean", proportion: 50.0 }
 *   ]
 * });
 *
 * if (!result.success) {
 *   message.error(result.message);
 *   return;
 * }
 *
 * const formula = result.data;
 * console.log(`Created formula with ID: ${formula.id}`);
 * ```
 */
```

## API Versioning

### Versioning Strategy

```rust
// Current version (v1)
#[tauri::command]
#[specta::specta)]
pub async fn create_formula_v1(dto: CreateFormulaDtoV1) -> ApiResponse<Formula> {
    // Implementation
}

// New version with additional fields
#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct CreateFormulaDtoV2 {
    // Inherit v1 fields
    #[serde(flatten)]
    pub v1_fields: CreateFormulaDtoV1,

    // New fields
    pub formula_type: FormulaType,
    pub tags: Vec<String>,
}

#[tauri::command]
#[specta::specta]
pub async fn create_formula(dto: CreateFormulaDtoV2) -> ApiResponse<Formula> {
    // Use latest version as default
}
```

## Best Practices Checklist

### DTO Design ✅

- [ ] All fields have explicit types
- [ ] Validation rules are documented
- [ ] Field names are consistent with TypeScript conventions
- [ ] Optional fields use `Option<T>`
- [ ] Collections have appropriate bounds
- [ ] Documentation includes examples

### API Contract ✅

- [ ] Request DTOs are validated
- [ ] Response format is consistent
- [ ] Error codes are standardized
- [ ] Error messages are user-friendly
- [ ] Success/error responses are clear
- [ ] API is documented with examples

### Type Safety ✅

- [ ] `#[specta::specta]` on all commands
- [ ] `#[specta(inline)]` on all DTOs
- [ ] Types are generated in `bindings.ts`
- [ ] Frontend uses generated types
- [ ] No `as any` type assertions
- [ ] Error handling is type-safe

## Quick Reference

### Command Template

```rust
#[tauri::command]
#[specta::specta]
pub async fn command_name(
    dto: RequestDto,
    state: State<'_, TauriAppState>,
) -> ApiResponse<ResponseData> {
    // 1. Validate input
    dto.validate()?;

    // 2. Process with service
    with_service(state, |ctx| async move {
        ctx.service.do_work(dto).await
    })
    .await
}
```

### DTO Template

```rust
#[derive(Serialize, Deserialize, Type, Clone)]
#[specta(inline)]
pub struct RequestDto {
    #[serde(alias = "fieldName")]
    pub field_name: String,
    pub optional_field: Option<String>,
}
```

### Response Template

```typescript
const result = await commands.commandName({ fieldName: "value" });
if (!result.success) {
    message.error(result.message);
    return;
}
const data = result.data;
```

## Common API Patterns

### CRUD Operations

```rust
// Create
#[tauri::command]
#[specta::specta]
pub async fn create_formula(dto: CreateFormulaDto, state: State<'_>)
    -> ApiResponse<Formula>;

// Read
#[tauri::command]
#[specta::specta]
pub async fn get_formula(id: i64, state: State<'_>)
    -> ApiResponse<Formula>;

// Update
#[tauri::command]
#[specta::specta]
pub async fn update_formula(id: i64, dto: UpdateFormulaDto, state: State<'_>)
    -> ApiResponse<Formula>;

// Delete
#[tauri::command]
#[specta::specta]
pub async fn delete_formula(id: i64, state: State<'_>)
    -> ApiResponse<()>;

// List
#[tauri::command]
#[specta::specta]
pub async fn list_formulas(params: ListParams, state: State<'_>)
    -> ApiResponse<PaginatedResponse<Formula>>;
```

## When to Use This Skill

Activate this skill when:
- Designing new Tauri commands
- Creating request/response DTOs
- Planning API structure
- Documenting APIs
- Validating API design
- Handling API errors
- Versioning APIs
