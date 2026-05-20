---
name: tdd-workflow
description: Use when implementing any feature or bugfix, before writing implementation code - write the test first, watch it fail, write minimal code to pass; ensures tests actually verify behavior by requiring failure first. Enforces RED-GREEN-REFACTOR cycle with iron-law compliance.
metadata:
  short-description: TDD 测试驱动开发工作流
  keywords:
    - tdd-workflow
    - TDD
    - 测试驱动开发
    - Red-Green-Refactor
    - 测试先行
    - 单元测试
    - 测试覆盖率
    - test-first
    - test-driven
  category: 测试
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
  iron-law: |
    NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
---

# TDD Workflow - 测试驱动开发工作流

## 铁律

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**违反规则的信件就是违反规则的精神。**

**无例外**：
- 不保留为"参考"
- 写测试时"不调整"
- 不看它
- 删除=删除

---

## 常见合理化

| 借口 | 现实 |
|------|------|
| "太简单不需要测试" | 简单代码也会坏。测试只需 30 秒 |
| "我之后再测试" | 测试立即通过证明不了什么 |
| "测试后达到相同目的" | 测试后="代码做什么?"测试前="代码应该做什么?" |
| "已经手动测试了" | 临时≠系统化。无记录，无法重新运行 |
| "删除 X 小时工作是浪费" | 沉没成本谬误。保留未验证代码是技术债 |
| "保留参考，先写测试" | 你会调整它。那是测试后。删除=删除 |

---

## 红色标志 - 停止并重新开始

- 测试前有代码
- "已经手动测试了"
- "测试后达到相同目的"
- "是精神而非仪式"
- "只此一次"的合理化
- "保留为参考"
- 写测试时"不调整"

**所有这些意味着：删除代码。用 TDD 重新开始。**

---

## 核心理念

**测试驱动开发（Test-Driven Development, TDD）** 是一种先编写测试，再编写实现代码的开发方法。通过严格的 **Red-Green-Refactor** 循环，确保代码质量和可维护性。

### TDD 循环

```
┌─────────────────────────────────────────────────────────┐
│  1. RED    : 编写失败的测试                              │
│  2. GREEN  : 编写最简单的代码使测试通过                   │
│  3. REFACTOR: 在测试保护下重构代码                       │
│  4. 重复循环                                            │
└─────────────────────────────────────────────────────────┘
```

---

## 何时使用本技能

在以下场景时激活：

- 用户明确要求使用 **TDD** 或 **测试驱动开发**
- 需要编写新功能或修复 Bug
- 提到"测试"、"单元测试"、"测试覆盖率"
- 需要确保代码质量
- 重构现有代码（先补充测试）

---

## TDD 工作流程

### 步骤 1：理解需求

在开始编码前，明确：

- **功能需求**：这个功能要做什么？
- **验收标准**：如何判断功能正确？
- **边界条件**：有哪些特殊情况？
- **错误处理**：异常情况如何处理？

### 步骤 2：编写失败测试（RED）

**测试先行原则**：

1. **先写测试，不写实现**
2. **运行测试，确认失败**（证明测试有效）
3. **阅读错误信息，理解预期**

**测试命名规范**（AAA 模式）：

```python
# Should_预期行为_When_测试条件
def should_return_user_when_id_exists():
    # Arrange（准备）
    user_id = 123
    expected_user = User(id=123, name="Alice")

    # Act（执行）
    result = user_service.get_by_id(user_id)

    # Assert（断言）
    assert result.id == expected_user.id
    assert result.name == expected_user.name
```

### 步骤 3：最小化实现（GREEN）

**最简单的可工作代码**：

- **只写足够使测试通过的代码**
- **不追求完美，追求通过**
- **硬编码可以接受**（第一步）

```python
# 最初版本 - 硬编码也可以
def get_by_id(user_id):
    if user_id == 123:
        return User(id=123, name="Alice")
    return None
```

### 步骤 4：运行测试确认通过

```bash
# 运行测试
pytest tests/test_user_service.py -v

# 期望输出
✅ should_return_user_when_id_exists PASSED
```

### 步骤 5：重构代码（REFACTOR）

**在测试保护下优化**：

- **消除重复**
- **提取方法**
- **改善命名**
- **优化结构**

```python
# 重构后版本
def get_by_id(user_id):
    return _user_repository.find_by_id(user_id)
```

### 步骤 6：重复循环

每个功能点重复上述步骤，直到功能完整。

---

## 测试质量标准

### 必须遵守的规则

- ✅ **测试覆盖率 ≥ 80%**
- ✅ **每个测试用例独立**（不依赖其他测试）
- ✅ **测试可重复**（多次运行结果一致）
- ✅ **测试命名清晰**（描述意图）
- ✅ **遵循 AAA 模式**（Arrange-Act-Assert）

### 禁止的反模式

- ❌ **伪测试**：测试代码没有断言
- ❌ **万能测试**：一个测试验证太多东西
- ❌ **测试内部实现**：应该测试行为，不是实现细节
- ❌ **脆弱测试**：依赖外部状态（时间、随机数等）

---

## TDD 最佳实践

### 1. 小步前进

- **一次只写一个测试**
- **一次只实现一个功能点**
- **频繁运行测试**（每 1-2 分钟）

### 2. 测试隔离

```python
# 好的示例 - 使用 fixtures
@pytest.fixture
def clean_database():
    db.reset()
    yield
    db.cleanup()

def test_create_user(clean_database):
    user = user_service.create("Alice")
    assert user.name == "Alice"
```

### 3. 测试边界条件

```python
def test_get_by_id():
    # 正常情况
    assert get_user(1) is not None

    # 边界条件
    assert get_user(0) is None
    assert get_user(-1) is None
    assert get_user(999999) is None
```

### 4. 测试异常情况

```python
def test_create_user_with_duplicate_email():
    with pytest.raises(DuplicateEmailError):
        user_service.create("alice@example.com")
        user_service.create("alice@example.com")
```

---

## 不同语言的 TDD 示例

### Python (pytest)

```python
# 测试
def should_calculate_total_price():
    cart = ShoppingCart()
    cart.add_item(Item(name="Book", price=10))
    cart.add_item(Item(name="Pen", price=5))

    assert cart.total_price() == 15

# 实现
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def total_price(self):
        return sum(item.price for item in self.items)
```

### JavaScript (Jest)

```javascript
// 测试
test('should calculate total price', () => {
  const cart = new ShoppingCart();
  cart.addItem({ name: 'Book', price: 10 });
  cart.addItem({ name: 'Pen', price: 5 });

  expect(cart.totalPrice()).toBe(15);
});

// 实现
class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(item) {
    this.items.push(item);
  }

  totalPrice() {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

### TypeScript (Jest)

```typescript
// 测试
test('should calculate total price', () => {
  const cart = new ShoppingCart();
  cart.addItem({ name: 'Book', price: 10 });
  cart.addItem({ name: 'Pen', price: 5 });

  expect(cart.totalPrice()).toBe(15);
});

// 实现
interface Item {
  name: string;
  price: number;
}

class ShoppingCart {
  private items: Item[] = [];

  addItem(item: Item): void {
    this.items.push(item);
  }

  totalPrice(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

---

## 常见问题

### Q1: 是否需要 100% 测试覆盖率？

**A**: 不一定。80-90% 是合理目标。以下情况可以例外：
- UI 组件（优先用 E2E 测试）
- 简单的 getter/setter
- 第三方库的封装

### Q2: 如何测试私有方法？

**A**: 不要直接测试私有方法。应该通过公共接口测试其行为。如果私有方法太复杂，考虑提取到独立的类。

### Q3: TDD 会降低开发速度吗？

**A**: 短期可能稍慢，但长期来看：
- 减少调试时间
- 减少回归 Bug
- 提高代码可维护性
- **整体效率提升 30-50%**

### Q4: 什么时候不适合 TDD？

**A**:
- 探索性原型（POC）
- UI 设计探索
- 紧急热修复（但仍应事后补充测试）

---

## 验证清单

完成 TDD 开发后，检查：

- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥ 80%
- [ ] 每个测试用例独立且可重复
- [ ] 测试命名清晰（Should_ExpectedBehavior_When_StateUnderTest）
- [ ] 遵循 AAA 模式
- [ ] 无伪测试（所有测试都有断言）
- [ ] 边界条件已测试
- [ ] 异常情况已测试

---

## 相关参考

- [TDD 最佳实践](../references/tdd-best-practices.md)
- [测试覆盖率配置](../config.yaml#tdd)
