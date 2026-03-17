# TDD 工作流 Skill

## 核心原则

**强制要求**：所有新功能、Bug 修复、重构必须达到 **80% 以上测试覆盖率**。

---

## RED-GREEN-REFACTOR 循环

### 1. RED（写测试，测试失败）
先写测试，验证测试会失败（因为功能尚未实现）。

### 2. GREEN（实现代码，测试通过）
编写最小代码使测试通过。

### 3. REFACTOR（重构代码，保持测试通过）
优化代码，保持所有测试通过。

---

## 工作流程

### 步骤 1：编写用户故事
描述期望的行为：

```
作为用户，我希望能够创建新的饲料配方，
以便我可以保存和管理不同的配方方案。

验收标准：
- 配方名称必填，长度 2-50 个字符
- 品种代码必填，必须是有效的品种
- 创建成功后返回配方 ID
- 创建失败时显示错误消息
```

### 步骤 2：生成测试用例
覆盖正常路径和边界情况：

**Rust 测试用例**：
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_create_formula_success() {
        // 正常创建配方
    }

    #[tokio::test]
    async fn test_create_formula_empty_name() {
        // 配方名称为空
    }

    #[tokio::test]
    async fn test_create_formula_name_too_long() {
        // 配方名称过长
    }

    #[tokio::test]
    async fn test_create_formula_invalid_species() {
        // 品种代码无效
    }

    #[tokio::test]
    async fn test_create_formula_database_error() {
        // 数据库连接失败
    }
}
```

**TypeScript 测试用例**：
```typescript
describe('FormulaForm', () => {
  it('should create formula successfully', async () => {
    // 正常创建
  });

  it('should show error when name is empty', async () => {
    // 名称为空
  });

  it('should show error when name is too long', async () => {
    // 名称过长
  });

  it('should show error when species is invalid', async () => {
    // 品种无效
  });
});
```

### 步骤 3：运行测试（RED）
```bash
# Rust
cargo test

# TypeScript
npm test
```

**预期结果**：测试失败（因为功能尚未实现）。

### 步骤 4：实现代码（GREEN）
编写最小代码使测试通过：

**Rust 实现**：
```rust
pub async fn create_formula(
    &self,
    dto: CreateFormulaDto,
) -> Result<i64> {
    // 验证输入
    if dto.name.is_empty() {
        return Err(anyhow!("配方名称不能为空"));
    }

    if dto.name.len() > 50 {
        return Err(anyhow!("配方名称过长"));
    }

    // 验证品种代码
    self.validate_species_code(&dto.species_code).await?;

    // 插入数据库
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

**TypeScript 实现**：
```typescript
export const FormulaForm: React.FC = () => {
  const [form] = Form.useForm();

  const handleSubmit = async (values: any) => {
    try {
      const result = await commands.createFormula(values);
      if (result.success) {
        message.success('创建成功');
      } else {
        message.error(result.message);
      }
    } catch (error) {
      message.error(`创建失败: ${error}`);
    }
  };

  return (
    <Form form={form} onFinish={handleSubmit}>
      <Form.Item
        name="name"
        rules={[
          { required: true, message: '请输入配方名称' },
          { min: 2, max: 50, message: '名称长度为 2-50 个字符' }
        ]}
      >
        <Input />
      </Form.Item>
      {/* 其他字段 */}
    </Form>
  );
};
```

### 步骤 5：再次运行测试
```bash
cargo test
npm test
```

**预期结果**：所有测试通过。

### 步骤 6：重构（REFACTOR）
优化代码，保持测试通过：

```rust
// 提取验证逻辑
fn validate_formula_name(name: &str) -> Result<()> {
    if name.is_empty() {
        return Err(anyhow!("配方名称不能为空"));
    }

    if name.len() > 50 {
        return Err(anyhow!("配方名称过长"));
    }

    Ok(())
}

pub async fn create_formula(
    &self,
    dto: CreateFormulaDto,
) -> Result<i64> {
    // 使用提取的验证函数
    validate_formula_name(&dto.name)?;
    self.validate_species_code(&dto.species_code).await?;

    // 插入数据��
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

### 步骤 7：验证覆盖率
```bash
# Rust
cargo tarpaulin --out Html

# TypeScript
npm run test:coverage
```

**要求**：覆盖率 >= 80%。

---

## 测试类型

### 1. 单元测试（Unit Tests）
测试独立函数和组件：

**Rust**：
```rust
#[test]
fn test_validate_formula_name() {
    assert!(validate_formula_name("测试配方").is_ok());
    assert!(validate_formula_name("").is_err());
    assert!(validate_formula_name(&"a".repeat(100)).is_err());
}

#[test]
fn test_calculate_nutrition() {
    let material = Material {
        protein: 18.0,
        energy: 3200.0,
        ..Default::default()
    };

    let result = calculate_nutrition(&material);
    assert_eq!(result.protein, 18.0);
}
```

**TypeScript**：
```typescript
describe('formatCurrency', () => {
  it('should format number as currency', () => {
    expect(formatCurrency(1234.56)).toBe('¥1,234.56');
  });
});
```

### 2. 集成测试（Integration Tests）
测试 API 端点和数据库操作：

**Rust**：
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

### 3. 手动测试
对于关键用户流程，进行手动测试：
- 配方优化完整流程
- 预混料设计流程
- 报告生成流程

---

## 最佳实践

### 1. 测试用户行为而非实现
✓ 正确：测试"点击提交按钮后显示成功消息"
✗ 错误：测试"调用 setState 设置 success 为 true"

### 2. 保持测试快速
单元测试应 < 100ms。

### 3. Mock 外部依赖
Mock 数据库、API、文件系统等。

### 4. 测试隔离
每个测试独立运行，互不影响。

### 5. 测试错误路径
不仅测试正常情况，也要测试错误情况。

### 6. 使用描述性的测试名称
```rust
#[test]
fn test_validate_formula_name_rejects_empty_string() { }

#[test]
fn test_validate_formula_name_accepts_valid_chinese_name() { }
```

---

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
    message: '创建成功',
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

    mock_repo
        .expect_create()
        .returning(|_| Ok(1));

    let service = FormulaService::new(Arc::new(mock_repo));
    let result = service.create_formula(dto).await;

    assert!(result.is_ok());
}
```

---

## 覆盖率验证

### Rust
```bash
# 安装 tarpaulin
cargo install cargo-tarpaulin

# 生成覆盖率报告
cargo tarpaulin --out Html --output-dir coverage

# 查看报告
open coverage/index.html
```

### TypeScript
```bash
# 运行测试并生成覆盖率
npm run test:coverage

# 查看报告
open coverage/index.html
```

---

## 何时使用此 Skill

- ✅ 添加新功能前
- ✅ 修复 Bug 前
- ✅ 重构代码前
- ✅ 用户明确要求测试时
- ✅ 代码审查时发现缺少测试

---

## 与其他 Skill 的配合

- 与 `testing-strategy` skill 配合使用
- 与 `code-review` skill 配合进行测试审查
- 与 `refactoring` skill 配合确保重构安全

---

## 提交前检查清单

- [ ] 所有测试通过
- [ ] 覆盖率 >= 80%
- [ ] 无跳过的测试
- [ ] 测试命名清晰
- [ ] 边界情况已测试
- [ ] 错误路径已测试
- [ ] Mock 使用合理
- [ ] 测试独立运行

---

## 常见陷阱

### 1. 测试实现细节
✗ 错误：测试组件的内部状态
✓ 正确：测试用户可见的行为

### 2. 测试之间有依赖
✗ 错误：test2 依赖 test1 的数据
✓ 正确：每个测试独立设置数据

### 3. 过度 Mock
✗ 错误：Mock 所有依赖
✓ 正确：只 Mock 外部依赖

### 4. 忽略异步问题
✗ 错误：忘记 `await`
✓ 正确：正确处理所有异步操作

---

## 参考资源

- [Rust Testing Guide](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- 项目规范：`.claude/rules/07-testing-standards.md`
