---
name: coding-standards
description: 代碼實作階段觸發。強制執行統一的編碼規範，支援 Java、TypeScript、Go 多語言。包含 Input/Output 模式、依賴注入、不可變物件等規範，確保代碼風格一致性。
---

# Coding Standards Skill

## 觸發時機

- 編寫新代碼時
- 代碼審查階段
- 生成 Application Service / Use Case 時
- 被 Sub-agent (command/query/reactor) 呼叫時

## 核心任務

強制執行統一的編碼規範，確保 AI 生成的代碼風格高度一致，降低人類審閱成本。

## 多語言支援

根據專案語言選擇對應的規範：

| 語言 | 參考文件 | 說明 |
|-----|---------|------|
| Java | 本文件 | Spring Boot / Jakarta EE |
| Java | [references/JAVA_CLEAN_ARCH.md](references/JAVA_CLEAN_ARCH.md) | Clean Architecture 詳細結構 |
| TypeScript | [references/TYPESCRIPT.md](references/TYPESCRIPT.md) | Node.js / Deno / Bun |
| Go | [references/GOLANG.md](references/GOLANG.md) | Standard Go Project Layout |
| Rust | [references/RUST.md](references/RUST.md) | Cargo / Tokio async runtime |

## Claude Code Sub-agent 整合

當被其他 Sub-agent 呼叫時，本 Skill 提供語言特定的編碼規範：

```
command-sub-agent 呼叫 → 提供 Use Case / Command Handler 的編碼規範
query-sub-agent 呼叫 → 提供 Query Handler / Read Model 的編碼規範
reactor-sub-agent 呼叫 → 提供 Event Handler 的編碼規範
```

---

## 規範 1：Input/Output Inner Class 模式

### 目的
- 明確定義方法的輸入輸出契約
- 提高代碼可讀性和可維護性
- 便於單元測試

### 標準模式

```java
public class CreateOrderUseCase {
    
    // ✅ Input 定義為靜態內部類別
    public static class Input {
        private final CustomerId customerId;
        private final List<OrderItemRequest> items;
        private final ShippingAddress address;
        
        public Input(CustomerId customerId, 
                     List<OrderItemRequest> items,
                     ShippingAddress address) {
            // 可在此進行基本驗證
            Objects.requireNonNull(customerId, "customerId must not be null");
            Objects.requireNonNull(items, "items must not be null");
            if (items.isEmpty()) {
                throw new IllegalArgumentException("items must not be empty");
            }
            this.customerId = customerId;
            this.items = List.copyOf(items);
            this.address = address;
        }
        
        // Getters
        public CustomerId getCustomerId() { return customerId; }
        public List<OrderItemRequest> getItems() { return items; }
        public ShippingAddress getAddress() { return address; }
    }
    
    // ✅ Output 定義為靜態內部類別
    public static class Output {
        private final OrderId orderId;
        private final OrderStatus status;
        private final LocalDateTime createdAt;
        
        public Output(OrderId orderId, OrderStatus status, LocalDateTime createdAt) {
            this.orderId = orderId;
            this.status = status;
            this.createdAt = createdAt;
        }
        
        // Getters
        public OrderId getOrderId() { return orderId; }
        public OrderStatus getStatus() { return status; }
        public LocalDateTime getCreatedAt() { return createdAt; }
    }
    
    // ✅ 主要執行方法，接收 Input，回傳 Output
    public Output execute(Input input) {
        // 業務邏輯
    }
}
```

### 禁止模式

```java
// ❌ 禁止：直接使用多個參數
public OrderResult createOrder(String customerId, List<Item> items, String address) {
    // 這樣做會讓介面難以維護
}

// ❌ 禁止：使用 Map 作為輸入輸出
public Map<String, Object> createOrder(Map<String, Object> params) {
    // 這樣做會失去型別安全
}
```

## 規範 2：@Bean not @Component

### 目的
- 集中管理依賴注入配置
- 明確的依賴關係可視化
- 便於測試時替換實作

### 標準模式

```java
// ✅ 正確：使用 @Configuration + @Bean
@Configuration
public class UseCaseConfiguration {
    
    @Bean
    public CreateOrderUseCase createOrderUseCase(
            OrderRepository orderRepository,
            InventoryService inventoryService,
            EventPublisher eventPublisher) {
        return new CreateOrderUseCase(
            orderRepository, 
            inventoryService, 
            eventPublisher
        );
    }
    
    @Bean
    public CancelOrderUseCase cancelOrderUseCase(
            OrderRepository orderRepository,
            PaymentGateway paymentGateway) {
        return new CancelOrderUseCase(orderRepository, paymentGateway);
    }
}

// ✅ Use Case 類別保持純淨，無 Spring 註解
public class CreateOrderUseCase {
    private final OrderRepository orderRepository;
    private final InventoryService inventoryService;
    private final EventPublisher eventPublisher;
    
    // 建構子注入
    public CreateOrderUseCase(
            OrderRepository orderRepository,
            InventoryService inventoryService,
            EventPublisher eventPublisher) {
        this.orderRepository = orderRepository;
        this.inventoryService = inventoryService;
        this.eventPublisher = eventPublisher;
    }
}
```

### 禁止模式

```java
// ❌ 禁止：在 Use Case 上使用 @Component/@Service
@Service  // ❌ 不要這樣做
public class CreateOrderUseCase {
    
    @Autowired  // ❌ 不要這樣做
    private OrderRepository orderRepository;
}
```

### 例外情況

以下情況可使用 @Component 系列註解：

| 類型 | 允許使用 | 說明 |
|------|---------|------|
| Controller | @RestController | 展示層入口點 |
| Repository 實作 | @Repository | Infrastructure 層 |
| Event Listener | @Component | 技術性元件 |
| Scheduled Task | @Component | 技術性元件 |

## 規範 3：命名規範

### Use Case / Command Handler 命名

```java
// ✅ 動詞 + 名詞 + UseCase
CreateOrderUseCase
CancelOrderUseCase
UpdateCustomerProfileUseCase

// ✅ CQRS Command Handler
CreateOrderCommandHandler
CancelOrderCommandHandler

// ✅ CQRS Query Handler
GetOrderByIdQueryHandler
ListOrdersByCustomerQueryHandler
```

### 方法命名

```java
// ✅ Use Case 統一使用 execute()
public Output execute(Input input)

// ✅ Command Handler 統一使用 handle()
public void handle(CreateOrderCommand command)

// ✅ Query Handler 統一使用 handle()
public OrderDto handle(GetOrderByIdQuery query)
```

## 規範 4：不可變物件 (Immutable Objects)

### Input/Output 必須是不可變的

```java
public static class Input {
    private final CustomerId customerId;  // ✅ final
    private final List<OrderItemRequest> items;
    
    public Input(CustomerId customerId, List<OrderItemRequest> items) {
        this.customerId = customerId;
        this.items = List.copyOf(items);  // ✅ 防禦性複製
    }
    
    // ✅ 只有 Getter，沒有 Setter
    public CustomerId getCustomerId() { return customerId; }
    public List<OrderItemRequest> getItems() { 
        return items;  // 已經是不可變的
    }
}
```

## 規範 5：例外處理模式

### 使用 Domain Exception

```java
// ✅ 定義領域特定例外
public class OrderNotFoundException extends DomainException {
    public OrderNotFoundException(OrderId orderId) {
        super("Order not found: " + orderId.getValue());
    }
}

public class InsufficientInventoryException extends DomainException {
    public InsufficientInventoryException(ProductId productId, int requested, int available) {
        super(String.format(
            "Insufficient inventory for product %s: requested %d, available %d",
            productId.getValue(), requested, available
        ));
    }
}
```

## 檢查清單

### 新增 Use Case 時

- [ ] 是否定義了 Input 內部類別？
- [ ] 是否定義了 Output 內部類別？
- [ ] Input/Output 是否為不可變？
- [ ] 是否使用 @Bean 而非 @Component？
- [ ] 命名是否遵循規範？

### 代碼審查時

- [ ] 有無 @Autowired 欄位注入？（應改用建構子注入）
- [ ] Use Case 類別是否有框架依賴？
- [ ] 例外是否使用 Domain Exception？

## 自動檢查規則 (供 Linter 使用)

```yaml
rules:
  - id: no-component-on-usecase
    pattern: "@(Component|Service).*class.*UseCase"
    message: "Use @Bean configuration instead of @Component on UseCase classes"
    severity: error
    
  - id: no-autowired-field
    pattern: "@Autowired\\s+private"
    message: "Use constructor injection instead of field injection"
    severity: error
    
  - id: require-input-output-class
    pattern: "class.*UseCase.*execute\\((?!Input)"
    message: "UseCase.execute() should accept Input inner class"
    severity: warning
```
