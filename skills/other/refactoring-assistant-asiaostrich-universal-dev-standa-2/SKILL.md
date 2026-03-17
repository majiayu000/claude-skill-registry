---
name: refactor
scope: universal
description: "[UDS] Guide refactoring decisions and strategy selection"
allowed-tools: Read, Write, Grep, Glob, Bash(npm test:*), Bash(npx:*)
argument-hint: "[file or module | 檔案或模組]"
---

# Refactoring Assistant | 重構助手

Guide refactoring decisions, recommend strategies, and provide step-by-step execution workflows.

引導重構決策、推薦策略，並提供逐步執行工作流程。

## Usage | 使用方式

| Command | Purpose | 用途 |
|---------|---------|------|
| `/refactor` | Start interactive refactoring guide | 啟動互動式重構引導 |
| `/refactor decide` | Run refactor vs. rewrite decision tree | 執行重構 vs 重寫決策樹 |
| `/refactor tactical` | Suggest tactical (daily) strategies | 建議戰術性（日常）策略 |
| `/refactor strategic` | Guide strategic/architectural refactoring | 引導戰略性/架構重構 |
| `/refactor legacy` | Legacy code safety strategies | 遺留程式碼安全策略 |
| `/refactor debt` | Technical debt assessment | 技術債評估 |

## Strategy Quick Reference | 策略快速參考

### Tactical Strategies (Daily) | 戰術性策略

| Strategy | When to Use | 使用時機 |
|----------|-------------|---------|
| **Preparatory Refactoring** | Before adding a blocked feature | 新增被阻擋的功能之前 |
| **Boy Scout Rule** | During any maintenance work | 任何維護工作中 |
| **Red-Green-Refactor** | TDD development cycle | TDD 開發循環 |

### Strategic Strategies (Architectural) | 戰略性策略

| Strategy | When to Use | 使用時機 |
|----------|-------------|---------|
| **Strangler Fig** | Replacing entire system gradually | 逐步替換整個系統 |
| **Anti-Corruption Layer** | Integrating with legacy system | 與遺留系統整合 |
| **Branch by Abstraction** | Shared code refactoring on trunk | 在主幹上重構共享程式碼 |

### Safety Strategies (Legacy) | 安全防護策略

| Strategy | When to Use | 使用時機 |
|----------|-------------|---------|
| **Characterization Tests** | Before any legacy refactoring | 任何遺留程式碼重構之前 |
| **Scratch Refactoring** | Understanding black-box code | 理解黑盒程式碼 |
| **Finding Seams** | Injecting test doubles into legacy | 在遺留程式碼中注入測試替身 |

## Workflow | 工作流程

1. **Assess** - Identify code to refactor, evaluate test coverage
2. **Decide** - Run decision tree (refactor vs. rewrite) if needed
3. **Select strategy** - Choose appropriate strategy based on scope and risk
4. **Execute** - Follow step-by-step workflow with safety checks
5. **Verify** - Run tests to confirm behavior is preserved

## Usage Examples | 使用範例

```
User: /refactor src/legacy-auth/
AI: Analyzing src/legacy-auth/...
    Test coverage: 23% — recommending safety-first approach.
    Suggested strategy: Characterization Tests + Preparatory Refactoring
```

```
User: /refactor decide
AI: Let me help you decide whether to refactor or rewrite.
    Question 1: Is the code currently working in production? [Y/N]
```

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [refactoring-standards.md](../../core/refactoring-standards.md)
