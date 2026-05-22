---
name: json-to-java-record
description: 將 JSON 資料片段轉換為 Java Record 類別。適用於需要從 API 回應或 JSON 資料建立強型別 Java 類別的情境。
---

# JSON 轉 Java Record Skill

這個 Skill 幫助將原始 JSON 資料或 API 回應轉換為結構化、強型別的 Java Record 類別。

## 目標

將 JSON 資料自動轉換為符合 Java 21+ 標準的 Record 類別，並加上適當的 Jackson 註解。

## 指示說明

1. **分析輸入**：查看使用者提供的 JSON 物件。

2. **推斷型別**：
   - `string` → `String`
   - `number`（整數）→ `Integer` 或 `Long`
   - `number`（小數）→ `Double` 或 `BigDecimal`
   - `boolean` → `Boolean`
   - `array` → `List<Type>`
   - `null` → 使用 `@Nullable` 或 `Optional<Type>`
   - 巢狀物件 → 建立個別的子類別 Record

3. **遵循範例**：查看 `examples/` 資料夾了解如何結構化輸出程式碼。
   - 輸入：`examples/input_data.json`
   - 輸出：`examples/UserRecord.java`

   注意巢狀字典（如 `preferences`）如何被抽取為獨立的 Record 類別。

## 風格指南

- 使用 `PascalCase` 命名 Record 類別
- 使用 `camelCase` 命名欄位
- 使用 `@JsonProperty` 處理 JSON 欄位名稱與 Java 命名不一致的情況
- 如果欄位可能為 null，使用 `@Nullable` 註解
- 日期時間字串使用 `LocalDateTime` 或 `Instant`
- 加上 `@JsonIgnoreProperties(ignoreUnknown = true)` 忽略未知欄位

## 必要的 Import

```java
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.time.Instant;
```

## 注意事項

- Record 類別是不可變的（immutable）
- 所有欄位都是 final
- 自動產生 `equals()`、`hashCode()` 和 `toString()`
