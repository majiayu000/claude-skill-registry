---
name: arch-guard
description: 進行代碼重構或新增模組時觸發。確保程式碼符合 Clean Architecture + DDD + CQRS 的層次關係，防止架構腐化。
---

# Architecture Guard Skill

## 觸發時機

- 進行代碼重構時
- 新增模組或類別時
- 修改現有程式碼的依賴關係時
- AI 生成新代碼前的架構審查

## 核心任務

確保程式碼放對位置，嚴格遵守領域驅動設計 (DDD) 與 Clean Architecture 的層次關係。

## 架構層次定義

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                  │
│         (Controllers, Views, DTOs)               │
├─────────────────────────────────────────────────┤
│              Application Layer                   │
│    (Use Cases, Application Services, Commands)   │
├─────────────────────────────────────────────────┤
│               Domain Layer                       │
│  (Entities, Value Objects, Domain Services,      │
│   Aggregates, Domain Events, Repositories IF)    │
├─────────────────────────────────────────────────┤
│            Infrastructure Layer                  │
│  (Repository Impl, External Services, DB, MQ)    │
└─────────────────────────────────────────────────┘
```

## 依賴規則 (Dependency Rule)

**核心原則：依賴只能向內指向，內層不能知道外層的存在**

### 允許的依賴方向

```
Presentation → Application → Domain ← Infrastructure
```

### 禁止的依賴

| 禁止情況 | 說明 | 違規範例 |
|---------|------|---------|
| Domain → Infrastructure | 領域層不能依賴基礎設施 | Domain Entity import JDBC |
| Domain → Application | 領域層不能依賴應用層 | Entity import UseCase |
| Domain → Presentation | 領域層不能依賴展示層 | Entity import Controller |
| Application → Presentation | 應用層不能依賴展示層 | UseCase import DTO |

## 違規檢測規則

### 🚫 嚴重違規 (必須立即修正)

1. **Domain 層引用資料庫驅動**
   ```java
   // ❌ 違規：Domain 層出現 JDBC/JPA 實作
   package com.example.domain.entity;
   import java.sql.Connection;  // 禁止！
   import javax.persistence.EntityManager;  // 禁止！
   ```

2. **Domain 層引用 Spring Framework**
   ```java
   // ❌ 違規：Domain 層出現 Spring 註解
   package com.example.domain.service;
   import org.springframework.stereotype.Service;  // 禁止！
   import org.springframework.beans.factory.annotation.Autowired;  // 禁止！
   ```

3. **Domain 層引用外部 HTTP 客戶端**
   ```java
   // ❌ 違規：Domain 層直接呼叫外部服務
   package com.example.domain.service;
   import org.springframework.web.client.RestTemplate;  // 禁止！
   ```

### ⚠️ 中度違規 (應該重構)

1. **Application 層包含業務邏輯**
   - Application Layer 應只負責編排 (Orchestration)
   - 複雜業務邏輯應下沉到 Domain Layer

2. **Repository 實作暴露在 Domain 層**
   - Domain 層只應定義 Repository 介面
   - 實作應在 Infrastructure 層

### 💡 建議改進

1. **使用 Port/Adapter 模式**
   - Domain 定義 Port (介面)
   - Infrastructure 提供 Adapter (實作)

## 標準目錄結構

```
src/main/java/com/example/
├── presentation/           # 展示層
│   ├── controller/
│   ├── dto/
│   │   ├── request/
│   │   └── response/
│   └── assembler/
│
├── application/            # 應用層
│   ├── command/           # CQRS Command
│   │   └── handler/
│   ├── query/             # CQRS Query
│   │   └── handler/
│   ├── service/           # Application Services
│   └── port/              # 輸出埠口定義
│       ├── inbound/
│       └── outbound/
│
├── domain/                 # 領域層 (純 POJO)
│   ├── model/
│   │   ├── aggregate/
│   │   ├── entity/
│   │   └── valueobject/
│   ├── service/           # Domain Services
│   ├── event/             # Domain Events
│   ├── repository/        # Repository 介面
│   └── exception/         # Domain Exceptions
│
└── infrastructure/         # 基礎設施層
    ├── persistence/
    │   ├── repository/    # Repository 實作
    │   └── entity/        # JPA/ORM Entities
    ├── messaging/
    ├── external/          # 外部服務整合
    └── config/            # 技術配置
```

## 審查檢查清單

### 新增類別時

- [ ] 類別放在正確的層次？
- [ ] import 語句是否違反依賴規則？
- [ ] Domain 層是否為純 POJO（無框架依賴）？
- [ ] Repository 介面與實作是否分離？

### 重構時

- [ ] 是否引入新的跨層依賴？
- [ ] 是否破壞現有的層次邊界？
- [ ] 是否需要透過介面解耦？

## 違規處理流程

1. **識別違規**：標記具體的類別和 import 語句
2. **分類嚴重度**：嚴重 / 中度 / 建議
3. **提供修正方案**：給出具體的重構建議
4. **阻止提交**：嚴重違規時應阻止代碼合併

## 範例：違規修正

### 修正前 (違規)

```java
// domain/service/OrderDomainService.java
package com.example.domain.service;

import org.springframework.stereotype.Service;  // ❌
import com.example.infrastructure.repository.JpaOrderRepository;  // ❌

@Service  // ❌
public class OrderDomainService {
    private final JpaOrderRepository repository;  // ❌
}
```

### 修正後 (正確)

```java
// domain/service/OrderDomainService.java
package com.example.domain.service;

import com.example.domain.repository.OrderRepository;  // ✅ 介面

public class OrderDomainService {
    private final OrderRepository repository;  // ✅ 依賴介面
}

// domain/repository/OrderRepository.java
package com.example.domain.repository;

public interface OrderRepository {  // ✅ 純介面
    Order findById(OrderId id);
    void save(Order order);
}

// infrastructure/persistence/repository/JpaOrderRepository.java
package com.example.infrastructure.persistence.repository;

import org.springframework.stereotype.Repository;  // ✅ 在 Infrastructure
import com.example.domain.repository.OrderRepository;

@Repository
public class JpaOrderRepository implements OrderRepository {
    // JPA 實作
}
```
