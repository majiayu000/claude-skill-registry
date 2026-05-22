---
name: mutation-testing
description: 在單元測試通過後觸發。透過引入人工錯誤（Mutants）來「測試你的測試」，確保測試案例具有足夠的錯誤偵測能力，建立對驗證機制的信任（Trust the Verification）。
---

# Mutation Testing Skill

## 觸發時機

- 單元測試覆蓋率達標（如 > 80%）但仍需確認測試品質時
- 核心演算法或高風險模組開發完成後
- CI/CD 流程中的品質閘門（Quality Gate）階段
- 使用者要求「驗證測試有效性」時

## 核心任務

執行變異測試（Mutation Testing），量化測試套件的品質，找出「倖存的變異體（Surviving Mutants）」，並據此強化測試案例。

---

## 為什麼需要變異測試？

單元測試覆蓋率（Line Check）只能告訴你「程式碼被執行到了」，但無法告訴你「測試是否驗證了正確的行為」。

> **"Coverage only checks if the code is executed, Mutation Testing checks if the code is verified."**

### 運作原理

1.  **變異 (Mutate)**：工具自動修改原始碼的一小部分（例如將 `a + b` 改為 `a - b`，或將 `return true` 改為 `return false`），產生一個「變異體 (Mutant)」。
2.  **測試 (Test)**：針對這個變異體執行現有的測試套件。
3.  **判定 (Verdict)**：
    *   **Killed (殺死)**：如果測試失敗（紅燈），表示測試成功偵測到了這個變異，這是**好事**。
    *   **Survived (倖存)**：如果測試仍然通過（綠燈），表示測試**無法偵測**這個錯誤，這是**壞事**。

---

## 工具選擇

### Java (主要支援)

使用 **PITest (PIT)**，這是目前 Java 生態系最成熟的變異測試工具。

```xml
<!-- pom.xml configuration example -->
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <dependencies>
        <dependency>
            <groupId>org.pitest</groupId>
            <artifactId>pitest-junit5-plugin</artifactId>
            <version>1.2.1</version>
        </dependency>
    </dependencies>
    <configuration>
        <targetClasses>
            <param>com.yourdomain.core.*</param>
        </targetClasses>
        <targetTests>
            <param>com.yourdomain.core.*Test</param>
        </targetTests>
        <mutators>
            <mutator>STRONGER</mutator> <!-- 使用更強的變異算子 -->
        </mutators>
    </configuration>
</plugin>
```

### 其他語言建議

- **JavaScript/TypeScript**: Stryker Mutator
- **Python**: Mutmut / Cosmic Ray
- **Go**: Gremlins

---

## 變異算子 (Mutators)

常見的變異類型包括：

1.  **Conditionals Boundary**：`i < 10` → `i <= 10`
2.  **Math**：`a + b` → `a - b`
3.  **Increments**：`i++` → `i--`
4.  **Invert Negatives**：`-i` → `i`
5.  **Return Values**：`return true` → `return false` / `return object` → `return null`
6.  **Void Method Calls**：移除對無回傳值方法的呼叫

---

## 分析流程

```
1. 執行單元測試 (必須全數通過)
       ↓
2. 執行變異測試 (mvn pitest:mutationCoverage)
       ↓
3. 產生報告 (target/pit-reports/index.html)
       ↓
4. 分析倖存變異體 (Analyze Surviving Mutants)
       ↓
5. 強化測試案例 (Add/Refine Test Cases)
       ↓
6. 重複直到 Mutation Score 達標
```

### 判定標準

| 指標 | 建議閾值 | 說明 |
|------|---------|------|
| **Line Coverage** | > 85% | 基礎要求 |
| **Mutation Score** | > 80% | 殺死的變異體 / 總變異體 |
| **Test Strength** | > 80% | 只計算有被覆蓋到的程式碼的變異分數 |

---

## 常見的倖存原因與對策

### 1. 缺乏斷言 (Missing Assertion)
測試執行了代碼，但沒有檢查結果。
*   **對策**：補上 `assertEquals` 或 `verify`。

### 2. 斷言過於寬鬆 (Weak Assertion)
只檢查了部分狀態（例如只檢查 List 不為空，沒檢查內容）。
*   **對策**：檢查具體的值和屬性。

### 3. 等價變異 (Equivalent Mutant)
變異後的代碼在邏輯上與原代碼等價（例如 `i < 10` 在迴圈中改成 `i != 10`）。
*   **對策**：這是工具限制，標記為 False Positive 或忽略。

---

## 交付產物

執行此 Skill 後，應產出：

1.  **Mutation Report Analysis**：分析主要倖存原因。
2.  **Improved Test Suite**：新增或修改的測試案例，能殺死之前的倖存者。
3.  **Confidence Assessment**：對該模組品質的信心評估。

> **注意**：變異測試極其耗時。建議只針對核心 Domain Logic (Entities, Value Objects, Domain Services) 執行，避免對整個專案執行。
