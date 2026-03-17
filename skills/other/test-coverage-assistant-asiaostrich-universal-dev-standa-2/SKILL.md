---
name: coverage
scope: partial
description: "[UDS] Analyze test coverage and provide recommendations"
allowed-tools: Read, Grep, Glob, Bash(npm test:*)
argument-hint: "[file or module | 檔案或模組]"
---

# Test Coverage Assistant | 測試覆蓋率助手

Analyze test coverage across multiple dimensions and provide actionable recommendations.

多維度分析測試覆蓋率並提供可執行的建議。

## Coverage Dimensions | 覆蓋率維度

| Dimension | What it Measures | 測量內容 |
|-----------|------------------|----------|
| **Line** | Lines of code executed | 執行的程式碼行數 |
| **Branch** | Decision paths taken | 決策路徑覆蓋 |
| **Function** | Functions called | 呼叫的函數 |
| **Statement** | Statements executed | 執行的陳述式 |

## 8-Dimension Framework | 八維度框架

1. **Code Coverage** - Lines, branches, functions
2. **Requirement Coverage** - All requirements have tests
3. **Risk Coverage** - High-risk areas prioritized
4. **Integration Coverage** - Component interaction paths
5. **Edge Case Coverage** - Boundary conditions tested
6. **Error Coverage** - Error handling paths verified
7. **Permission Coverage** - Access control scenarios
8. **AI Generation Quality** - AI-generated test effectiveness

## Coverage Targets | 覆蓋率目標

| Level | Coverage | Use Case | 適用場景 |
|-------|----------|----------|----------|
| Minimum | 60% | Legacy code | 遺留程式碼 |
| Standard | 80% | Most projects | 大多數專案 |
| High | 90% | Critical systems | 關鍵系統 |
| Critical | 95%+ | Safety-critical | 安全關鍵 |

## Workflow | 工作流程

1. **Run coverage tool** - Generate coverage report | 產生覆蓋率報告
2. **Analyze gaps** - Identify untested areas | 識別未測試區域
3. **Prioritize** - Rank by risk and importance | 依風險排序
4. **Recommend tests** - Suggest specific tests to add | 建議新增測試
5. **Track progress** - Monitor coverage over time | 追蹤進度

## Usage | 使用方式

```
/coverage                   - Run full coverage analysis | 執行完整覆蓋率分析
/coverage src/auth          - Analyze specific module | 分析特定模組
/coverage --recommend       - Get test recommendations | 取得測試建議
```

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [test-completeness-dimensions.md](../../core/test-completeness-dimensions.md)
