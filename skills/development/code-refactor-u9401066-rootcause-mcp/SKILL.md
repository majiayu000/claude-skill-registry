---
name: code-refactor
description: Proactively detect and execute code refactoring to maintain DDD architecture and code quality. Triggers: RF, refactor, 重構, 拆分, split, 模組化, modularize, 太長, cleanup, 整理, clean, 優化, optimize, extract, 提取, simplify, 簡化, 複雜度, complexity, 重組, reorganize, 改善, improve.
version: 2.1.0
category: quality
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies:
  - ddd-architect
  - test-generator
  - memory-updater
allowed-tools:
  - read_file
  - write_file
  - replace_string_in_file
  - list_dir
  - grep_search
  - semantic_search
  - get_errors
---

# 程式碼重構技能

## 描述
主動偵測並執行程式碼重構，維持 DDD 架構和程式碼品質。

## 觸發條件
- 「重構這段程式碼」、「refactor」
- 「這個檔案太長了」
- 「模組化」、「拆分」
- **主動觸發**：偵測到程式碼超過閾值時

---

## 核心原則

> 📜 依據憲法第 7.3 條「主動重構原則」

```
重構不是改天換地，而是持續的小步快跑
每次提交都應該比上次更乾淨
```

---

## 閾值設定

### 📏 長度閾值

| 類型 | 警告 | 強制重構 |
|------|------|----------|
| 檔案 | > 200 行 | > 400 行 |
| 類別 | > 150 行 | > 300 行 |
| 函數 | > 30 行 | > 50 行 |
| 目錄檔案數 | > 10 個 | > 15 個 |

### 🔄 複雜度閾值

| 指標 | 警告 | 強制重構 |
|------|------|----------|
| 圈複雜度 | > 10 | > 15 |
| 巢狀深度 | > 3 層 | > 4 層 |
| 參數數量 | > 4 個 | > 6 個 |
| 依賴數量 | > 5 個 | > 8 個 |

---

## 重構模式庫

### 1️⃣ Extract Method（提取方法）

**觸發條件**：函數過長、重複邏輯

```python
# Before
def process_order(order):
    # 驗證訂單 (10 行)
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
    # ... 更多驗證
    
    # 計算價格 (15 行)
    subtotal = sum(item.price * item.qty for item in order.items)
    tax = subtotal * 0.05
    total = subtotal + tax
    # ... 更多計算
    
    # 儲存訂單 (10 行)
    # ...

# After
def process_order(order):
    self._validate_order(order)
    total = self._calculate_total(order)
    self._save_order(order, total)

def _validate_order(self, order):
    """驗證訂單有效性"""
    if not order.items:
        raise ValueError("Empty order")
    # ...

def _calculate_total(self, order) -> Decimal:
    """計算訂單總金額（含稅）"""
    subtotal = sum(item.price * item.qty for item in order.items)
    return subtotal * Decimal("1.05")
```

### 2️⃣ Extract Class（提取類別）

**觸發條件**：類別職責過多、超過 150 行

```python
# Before: User 類別包含太多職責
class User:
    def __init__(self, name, email, ...):
        self.name = name
        self.email = email
        self.address_line1 = ...
        self.address_line2 = ...
        self.city = ...
        self.postal_code = ...
    
    def validate_email(self): ...
    def format_address(self): ...
    def calculate_shipping(self): ...

# After: 提取 Address 值物件
@dataclass(frozen=True)
class Address:
    """地址值物件"""
    line1: str
    line2: str | None
    city: str
    postal_code: str
    
    def format(self) -> str:
        return f"{self.line1}\n{self.city} {self.postal_code}"

class User:
    def __init__(self, name: str, email: Email, address: Address):
        self.name = name
        self.email = email
        self.address = address
```

### 3️⃣ Replace Conditional with Polymorphism（多態取代條件）

**觸發條件**：大量 if-elif-else 或 switch

```python
# Before: 條件地獄
def calculate_shipping(order):
    if order.shipping_type == "standard":
        return order.weight * 10
    elif order.shipping_type == "express":
        return order.weight * 25 + 50
    elif order.shipping_type == "overnight":
        return order.weight * 50 + 100
    elif order.shipping_type == "international":
        # 複雜計算...
        pass

# After: 策略模式
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, order) -> Decimal: ...

class StandardShipping(ShippingStrategy):
    def calculate(self, order) -> Decimal:
        return order.weight * 10

class ExpressShipping(ShippingStrategy):
    def calculate(self, order) -> Decimal:
        return order.weight * 25 + 50

# 使用
shipping_strategies = {
    "standard": StandardShipping(),
    "express": ExpressShipping(),
    # ...
}
cost = shipping_strategies[order.shipping_type].calculate(order)
```

### 4️⃣ Introduce Parameter Object（參數物件）

**觸發條件**：參數超過 4 個

```python
# Before: 參數過多
def create_user(
    name: str,
    email: str,
    phone: str,
    address_line1: str,
    address_line2: str,
    city: str,
    postal_code: str,
    country: str,
):
    ...

# After: 使用參數物件
@dataclass
class CreateUserCommand:
    name: str
    email: str
    phone: str
    address: Address

def create_user(command: CreateUserCommand):
    ...
```

### 5️⃣ Split Module（拆分模組）

**觸發條件**：目錄超過 10 個檔案

```
# Before
src/Domain/
├── User.py
├── Order.py
├── Product.py
├── Payment.py
├── Shipping.py
├── Review.py
├── Coupon.py
├── Notification.py
├── ...  # 太多了！

# After: 按子領域拆分
src/Domain/
├── Identity/
│   └── User.py
├── Ordering/
│   ├── Order.py
│   └── Payment.py
├── Catalog/
│   ├── Product.py
│   └── Review.py
├── Promotion/
│   └── Coupon.py
└── Communication/
    └── Notification.py
```

---

## DDD 架構守護

重構時必須檢查是否違反 DDD 原則：

### ❌ 常見違規

```python
# 違規 1: Domain 層依賴 Infrastructure
# Domain/Services/OrderService.py
from infrastructure.database import db  # ❌ 禁止！

# 違規 2: Presentation 直接存取 Domain
# Presentation/API/routes.py
from domain.repositories import UserRepository  # ❌ 應透過 Application

# 違規 3: Entity 包含持久化邏輯
class User:
    def save(self):  # ❌ 應在 Repository
        db.session.add(self)
```

### ✅ 正確依賴方向

```
Presentation → Application → Domain
                    ↓
              Infrastructure
```

---

## 重構流程

### 1️⃣ 偵測階段
```markdown
🔍 偵測到重構需求：
- 檔案：`src/domain/services/order_service.py`
- 問題：檔案長度 342 行（超過 200 行警告閾值）
- 複雜度：圈複雜度 12（超過 10 警告閾值）
```

### 2️⃣ 分析階段
```markdown
📊 分析結果：
- `process_order()` 函數 85 行，建議拆分
- 發現 3 處重複邏輯，建議提取
- 識別出 2 個隱藏的 Value Object
```

### 3️⃣ 規劃階段
```markdown
📋 重構計畫：
1. 提取 `OrderValidator` 類別
2. 提取 `PricingCalculator` 服務
3. 建立 `OrderStatus` Value Object
4. 更新測試確保覆蓋
```

### 4️⃣ 執行階段
```markdown
🔧 執行重構：
- [x] 建立 `OrderValidator` 類別
- [x] 遷移驗證邏輯
- [x] 更新測試
- [x] 確認測試通過
- [ ] 提取 `PricingCalculator`
- [ ] ...
```

### 5️⃣ 驗證階段
```markdown
✅ 重構完成：
- 測試：全部通過（42/42）
- 覆蓋率：85%（+3%）
- 複雜度：8（-4）
- 架構：符合 DDD ✓
```

---

## 主動建議範本

當偵測到需要重構時，AI 應主動建議：

```markdown
💡 **重構建議**

偵測到 `order_service.py` 已達 250 行，建議進行模組化：

### 建議拆分方案

| 新檔案 | 內容 | 行數 |
|--------|------|------|
| `order_validator.py` | 訂單驗證邏輯 | ~50 行 |
| `pricing_calculator.py` | 價格計算邏輯 | ~60 行 |
| `order_service.py` | 服務編排 | ~80 行 |

### 預期效益
- ✅ 單一職責原則
- ✅ 更易測試
- ✅ 降低認知負荷

是否要我執行這個重構？
```

---

## 與其他 Skills 整合

| Skill | 整合方式 |
|-------|----------|
| `code-reviewer` | 審查時觸發重構建議 |
| `test-generator` | 重構前先生成測試 |
| `ddd-architect` | 確保重構符合 DDD |
| `memory-updater` | 記錄重構決策 |
