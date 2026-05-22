---
name: tdd-workflow
description: 当用户要求TDD、测试驱动开发、先写测试或提到红绿重构时使用。
---

# TDD 工作流 Skill

## 核心原则
**强制要求**：所有新功能、Bug 修复、重构必须达到 **80% 以上测试覆盖率**。

## RED-GREEN-REFACTOR 循环

### 1. RED（写测试，测试失败）
先写测试，验证测试会失败（因为功能尚未实现）。

### 2. GREEN（实现代码，测试通过）
编写最小代码使测试通过。

### 3. REFACTOR（重构代码，保持测试通过）
优化代码，保持所有测试通过。

## 工作流程

### 步骤 1：编写用户故事
```
作为用户，我希望能够创建新的饲料配方。

验收标准：
- 配方名称必填，长度 2-50 个字符
- 品种代码必填，必须是有效的品种
- 创建成功后返回配方 ID
```

### 步骤 2：生成测试用例

**Rust 测试**：
```rust
#[tokio::test]
async fn test_create_formula_success() { }

#[tokio::test]
async fn test_create_formula_empty_name() { }

#[tokio::test]
async fn test_create_formula_name_too_long() { }

#[tokio::test]
async fn test_create_formula_invalid_species() { }
```

**TypeScript 测试**：
```typescript
describe('FormulaForm', () => {
  it('should create formula successfully', async () => { });
  it('should show error when name is empty', async () => { });
  it('should show error when name is too long', async () => { });
});
```

### 步骤 3：运行测试（RED）
```bash
cargo test    # Rust
npm test      # TypeScript
```
**预期结果**：测试失败。

### 步骤 4：实现代码（GREEN）
```rust
pub async fn create_formula(&self, dto: CreateFormulaDto) -> Result<i64> {
    if dto.name.is_empty() {
        return Err(anyhow!("配方名称不能为空"));
    }

    let formula_id = sqlx::query!(
        "INSERT INTO formulas (name, species_code) VALUES (?, ?)",
        dto.name, dto.species_code
    )
    .execute(&self.pool)
    .await?
    .last_insert_rowid();

    Ok(formula_id)
}
```

### 步骤 5：再次运行测试
```bash
cargo test
npm test
```
**预期结果**：所有测试通过。

### 步骤 6：重构（REFACTOR）
```rust
// 提取验证逻辑
fn validate_formula_name(name: &str) -> Result<()> {
    if name.is_empty() {
        return Err(anyhow!("配方名称不能为空"));
    }
    Ok(())
}

pub async fn create_formula(&self, dto: CreateFormulaDto) -> Result<i64> {
    validate_formula_name(&dto.name)?;
    // ...
}
```

### 步骤 7：验证覆盖率
```bash
cargo tarpaulin --out Html       # Rust
npm run test:coverage            # TypeScript
```
**要求**：覆盖率 >= 80%。

## 测试类型

### 1. 单元测试
```rust
#[test]
fn test_validate_formula_name() {
    assert!(validate_formula_name("测试配方").is_ok());
    assert!(validate_formula_name("").is_err());
}
```

### 2. 集成测试
```rust
#[tokio::test]
async fn test_create_formula_integration() {
    let pool = setup_test_db().await;
    let repo = FormulaRepository::new(Arc::new(pool));

    let dto = CreateFormulaDto {
        name: "测试配方".to_string(),
        species_code: "PIG".to_string(),
    };

    let result = repo.create(dto).await;
    assert!(result.is_ok());

    cleanup_test_db().await;
}
```

## Mock 示例

### Mock Tauri 命令（TypeScript）
```typescript
import { vi } from 'vitest';

vi.mock('../bindings', () => ({
  commands: {
    createFormula: vi.fn(),
  },
}));

it('should create formula', async () => {
  vi.mocked(commands.createFormula).mockResolvedValue({
    success: true,
    data: { id: 1 },
  });

  const result = await createFormula(dto);
  expect(result.success).toBe(true);
});
```

### Mock 数据库（Rust）
```rust
use mockall::mock;

mock! {
    pub FormulaRepository {
        async fn create(&self, dto: CreateFormulaDto) -> Result<i64>;
    }
}

#[tokio::test]
async fn test_with_mock() {
    let mut mock_repo = MockFormulaRepository::new();
    mock_repo.expect_create().returning(|_| Ok(1));

    let service = FormulaService::new(Arc::new(mock_repo));
    let result = service.create_formula(dto).await;

    assert!(result.is_ok());
}
```

## 最佳实践

1. **测试用户行为而非实现** → 测试"点击提交后显示成功消息"
2. **保持测试快速** → 单元测试 < 100ms
3. **Mock 外部依赖** → Mock 数据库、API、文件系统
4. **测试隔离** → 每个测试独立运行
5. **测试错误路径** → 测试正常和错误情况
6. **描述性测试名称** → `test_validate_formula_name_rejects_empty_string`

## 提交前检查清单

- [ ] 所有测试通过
- [ ] 覆盖率 >= 80%
- [ ] 无跳过的测试
- [ ] 测试命名清晰
- [ ] 边界情况已测试
- [ ] 错误路径已测试
- [ ] Mock 使用合理
- [ ] 测试独立运行

## 常见陷阱

1. **测试实现细节** → 应测试用户可见的行为
2. **测试之间有依赖** → 每个测试独立设置数据
3. **过度 Mock** → 只 Mock 外部依赖
4. **忽略异步问题** → 正确处理所有异步操作
