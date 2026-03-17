---
name: requirement
scope: universal
description: "[UDS] Write user stories and requirements following INVEST criteria"
allowed-tools: Read, Write, Grep
argument-hint: "[feature description | 功能描述]"
---

# Requirement Assistant | 需求助手

Write well-structured user stories and requirements following INVEST criteria.

撰寫結構良好的使用者故事和需求文件，遵循 INVEST 準則。

## Workflow | 工作流程

1. **Understand context** - Gather feature information | 蒐集功能資訊
2. **Identify stakeholders** - Who benefits from this feature? | 誰受益？
3. **Write user story** - Follow the standard format | 遵循標準格式
4. **Define acceptance criteria** - Specific, testable conditions | 定義可測試條件
5. **Validate with INVEST** - Check quality criteria | 用 INVEST 驗證品質

## User Story Format | 使用者故事格式

```markdown
As a [role],
I want [feature],
So that [benefit].

### Acceptance Criteria

- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]
```

## INVEST Criteria | INVEST 準則

| Criterion | Description | 說明 |
|-----------|-------------|------|
| **I**ndependent | Can be developed separately | 可獨立開發 |
| **N**egotiable | Details can be discussed | 可協商細節 |
| **V**aluable | Delivers value to user | 提供使用者價值 |
| **E**stimable | Can estimate effort | 可估算工作量 |
| **S**mall | Fits in one sprint | 適合單一迭代 |
| **T**estable | Has clear test criteria | 有明確測試標準 |

## Quality Checklist | 品質檢查清單

- [ ] User story follows "As a / I want / So that" format
- [ ] At least 2 acceptance criteria defined
- [ ] All 6 INVEST criteria satisfied
- [ ] Edge cases and error scenarios considered
- [ ] Out of scope items documented

## Usage | 使用方式

```
/requirement                         - Interactive requirement wizard | 互動式需求精靈
/requirement user login              - Write requirement for feature | 為功能撰寫需求
/requirement "users can export data" - Based on description | 根據描述撰寫
```

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [requirement-engineering.md](../../core/requirement-engineering.md)
