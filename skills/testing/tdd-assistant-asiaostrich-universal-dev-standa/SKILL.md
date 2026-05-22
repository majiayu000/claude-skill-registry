---
source: ../../../../skills/tdd-assistant/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2026-01-07
status: current
---

---
name: tdd
description: |
  Guide developers through Test-Driven Development workflow.
  Use when: writing tests first, practicing TDD, red-green-refactor cycle, BDD scenarios.
  Keywords: TDD, test first, red green refactor, FIRST, BDD, ATDD, 测试驅动开发, 紅綠重構.
---

# TDD 助手

> **语言**: [English](../../../../skills/tdd-assistant/SKILL.md) | 简体中文

**版本**: 1.0.0
**最後更新**: 2026-01-07
**適用範圍**: Claude Code Skills

---

## 目的

此技能引導开发者完成测试驅动开发工作流程，協助他們：
- 撰写有效的失败测试（紅色阶段）
- 实現最少程序码讓测试通過（綠色阶段）
- 在保持测试綠色的同时安全重構（重構阶段）
- 識别并避免常見的 TDD 反模式
- 集成 TDD 与 BDD 和 ATDD 方法
- 根据情境適當地应用 TDD

---

## 快速參考

### TDD 循環检查清单

```
┌─────────────────────────────────────────────────────────────────┐
│  🔴 紅色阶段                                                     │
│  □ 测试描述预期行为，而非实作                                     │
│  □ 测试名称清楚说明正在测试什麼                                   │
│  □ 测试遵循 AAA 模式（Arrange-Act-Assert）                       │
│  □ 测试因为「正确的原因」而失败                                   │
│  □ 失败消息清楚且可操作                                          │
├─────────────────────────────────────────────────────────────────┤
│  🟢 綠色阶段                                                     │
│  □ 撰写「最少」程序码讓测试通過                                   │
│  □ 「假裝」是可以接受的（如有需要可硬编码）                        │
│  □ 不要優化或過度设计                                            │
│  □ 测试現在通過                                                  │
│  □ 所有其他测试仍然通過                                          │
├─────────────────────────────────────────────────────────────────┤
│  🔵 重構阶段                                                     │
│  □ 消除重複（DRY）                                               │
│  □ 改善命名                                                      │
│  □ 如有需要提取方法                                              │
│  □ 「每次」变更後执行测试                                         │
│  □ 没有新增功能                                                  │
│  □ 所有测试仍然通過                                              │
└─────────────────────────────────────────────────────────────────┘
```

### FIRST 原則快速參考

| 原則 | 检查 | 常見違規 |
|------|------|---------|
| **F**ast（快速） | 每个单元测试 < 100ms | 数据庫呼叫、文件 I/O、网络 |
| **I**ndependent（獨立） | 無共享状态 | 静态变數、执行順序依賴 |
| **R**epeatable（可重複） | 結果總是相同 | DateTime.Now、Random、外部服务 |
| **S**elf-validating（自我验证） | 清楚的通過/失败 | 手动检查日誌、無斷言 |
| **T**imely（及时） | 程序码之前测试 | 实現後才写测试 |

### 反模式快速偵测

| 症状 | 可能的反模式 | 快速修復 |
|------|-------------|---------|
| 重構时测试失败 | 测试实作細节 | 只测试行为 |
| 测试通過但生产環境有 bug | 過度 mock | 新增集成测试 |
| 隨机测试失败 | 测试相依性 | 隔離测试状态 |
| 测试套件緩慢 | 集成测试太多 | 增加单元测试比例 |
| 团队回避写测试 | 测试设置複雜 | 用建構器簡化 |

---

## TDD vs BDD vs ATDD 快速參考

| 面向 | TDD | BDD | ATDD |
|------|-----|-----|------|
| **誰撰写** | 开发者 | 开发者 + BA + QA | 所有利益相关者 |
| **语言** | 程序码 | Gherkin（Given-When-Then） | 业务语言 |
| **层级** | 单元/元件 | 功能/場景 | 驗收 |
| **时机** | 编码期间 | 编码之前 | Sprint 之前 |

### 何时使用哪个

```
是技術实作細节嗎？
├─ 是 → TDD
└─ 否 → 有业务利益相关者嗎？
         ├─ 是 → 利益相关者需要阅读/验证测试嗎？
         │        ├─ 是 → ATDD → BDD → TDD
         │        └─ 否 → BDD → TDD
         └─ 否 → TDD
```

---

## 工作流協助

### 紅色阶段指導

撰写失败测试时，确保：

1. **清楚的意图**
   ```typescript
   // ❌ 模糊
   test('it works', () => { ... });

   // ✅ 清楚
   test('should calculate discount when order total exceeds threshold', () => { ... });
   ```

2. **单一行为**
   ```typescript
   // ❌ 多个行为
   test('should validate and save user', () => { ... });

   // ✅ 单一行为
   test('should reject invalid email format', () => { ... });
   test('should save user with valid data', () => { ... });
   ```

3. **正确的斷言**
   ```typescript
   // ❌ 無斷言
   test('should process order', () => {
     orderService.process(order);
     // 缺少斷言！
   });

   // ✅ 清楚的斷言
   test('should mark order as processed', () => {
     const result = orderService.process(order);
     expect(result.status).toBe('processed');
   });
   ```

### 綠色阶段指導

讓测试通過时，记住：

1. **最少实現**
   ```typescript
   // 测试：should return "FizzBuzz" for numbers divisible by both 3 and 5

   // ❌ 過度设计的第一次实現
   function fizzBuzz(n: number): string {
     const divisibleBy3 = n % 3 === 0;
     const divisibleBy5 = n % 5 === 0;
     if (divisibleBy3 && divisibleBy5) return 'FizzBuzz';
     if (divisibleBy3) return 'Fizz';
     if (divisibleBy5) return 'Buzz';
     return n.toString();
   }

   // ✅ 當前测试的最少实現（假裝！）
   function fizzBuzz(n: number): string {
     return 'FizzBuzz'; // 剛好足夠通過「这个」测试
   }
   ```

2. **漸进式泛化**
   - 第一个测试：硬编码答案
   - 第二个测试：新增簡单条件
   - 第三个测试：泛化模式

### 重構阶段指導

安全重構检查清单：

```
之前：
□ 所有测试都是綠色
□ 理解程序码在做什麼

期间（一次一个）：
□ 提取方法 → 执行测试
□ 重新命名 → 执行测试
□ 消除重複 → 执行测试
□ 簡化条件 → 执行测试

之後：
□ 所有测试仍然綠色
□ 程序码更乾淨
□ 没有新功能
```

---

## 与 SDD 集成

使用規格驅动开发时：

### Spec → 测试映射

| Spec 區段 | 测试类型 |
|----------|---------|
| 驗收标准 | 驗收测试（ATDD/BDD） |
| 业务規則 | 单元测试（TDD） |
| 邊界情况 | 单元测试（TDD） |
| 集成点 | 集成测试 |

### 工作流程

```
1. 阅读 Spec (SPEC-XXX)
   ↓
2. 識别驗收标准
   ↓
3. 撰写 BDD 場景（如適用）
   ↓
4. 对每个場景：
   ├─ TDD：紅 → 綠 → 重構
   └─ 標记 AC 为已实現
   ↓
5. 所有 AC 已实現？
   ├─ 是 → 標记 Spec 为完成
   └─ 否 → 返回步骤 4
```

### 测试文件參考

```typescript
/**
 * SPEC-001：使用者验证 的测试
 *
 * 驗收标准：
 * - AC-1：使用者可以用有效憑证登入
 * - AC-2：無效密码顯示错误
 * - AC-3：3 次失败嘗試後帳号鎖定
 */
describe('使用者验证 (SPEC-001)', () => {
  // 依 AC 組織测试
});
```

---

## 配置偵测

此技能支援项目特定配置。

### 偵测順序

1. 检查 `CONTRIBUTING.md` 的「Disabled Skills」區段
   - 如果此技能在列表中，則对此项目停用
2. 检查 `CONTRIBUTING.md` 的「TDD Standards」區段
3. 检查程序码庫中現有的测试模式
4. 如果未找到，**预设使用标准 TDD 实踐**

### 首次设置

如果未找到配置且情境不明确：

1. 詢問：「此项目尚未配置 TDD 偏好。您偏好哪种方法？」
   - 純 TDD（紅-綠-重構）
   - BDD 風格 TDD（Given-When-Then）
   - ATDD 搭配 BDD 和 TDD

2. 选择後，建议在 `CONTRIBUTING.md` 中文件化：

```markdown
## TDD 标准

### 偏好方法
- 主要：TDD（紅-綠-重構）
- 对於有业务利益相关者的功能：BDD

### 测试命名慣例
- 模式：`should_[行为]_when_[条件]`
- 範例：`should_return_error_when_email_invalid`

### 覆蓋率目標
- 单元：80%
- 集成：60%
```

---

## 详细指南

完整标准請參阅：
- [TDD 核心标准](../../../../core/test-driven-development.md)
- [TDD 工作流程指南](./tdd-workflow.md)
- [语言範例](./language-examples.md)

相关测试标准：
- [测试标准](../../../../core/testing-standards.md)
- [测试完整性維度](../../../../core/test-completeness-dimensions.md)

---

## 相关标准

- [测试驅动开发](../../../../core/test-driven-development.md) - TDD 核心标准
- [测试标准](../../../../core/testing-standards.md) - 测试框架
- [测试完整性維度](../../../../core/test-completeness-dimensions.md) - 7 維度
- [規格驅动开发](../../../../core/spec-driven-development.md) - SDD 集成
- [测试指南技能](../testing-guide/SKILL.md) - 测试指南
- [测试覆蓋率助手](../test-coverage-assistant/SKILL.md) - 覆蓋率協助

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-01-07 | 初始版本 |

---

## 授权

此技能依据 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权釋出。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
