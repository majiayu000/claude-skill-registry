---
source: skills/code-review-assistant/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2025-12-25
status: current
name: review
description: |
  系统化的程序码审查检查清单和提交前品质关卡。
  使用时机：审查 pull request、检查程序码品质、提交程序码前。
  关鍵字：review, PR, pull request, checklist, quality, commit, 审查, 检查, 簽入。
---

# 程序码审查助理

> **语言**: [English](../../../../skills/code-review-assistant/SKILL.md) | 简体中文

**版本**: 1.0.0
**最後更新**: 2025-12-24
**適用範圍**: Claude Code Skills

---

## 目的

此技能提供系统化的程序码审查和提交前验证检查清单。

## 快速參考

### 註解前綴

| 前綴 | 意義 | 需要採取的行动 |
|--------|---------|------------------|
| **❗ BLOCKING** | 合併前必須修正 | 🔴 必要 |
| **⚠️ IMPORTANT** | 应該修正，但不阻擋合併 | 🟡 建议 |
| **💡 SUGGESTION** | 可改进之处 | 🟢 选择性 |
| **❓ QUESTION** | 需要釐清 | 🔵 討論 |
| **📝 NOTE** | 信息性质，無需行动 | ⚪ 信息 |

### 审查检查清单类别

1. **功能性** - 是否正常运作？
2. **设计** - 架構是否正确？
3. **品质** - 程序码是否乾淨？
4. **可读性** - 是否容易理解？
5. **测试** - 涵蓋率是否足夠？
6. **安全性** - 是否有漏洞？
7. **效能** - 是否高效？
8. **错误处理** - 是否妥善处理？
9. **文件** - 是否更新？
10. **依賴项** - 是否必要？

### 提交前检查清单

- [ ] 建置成功（零错误、零警告）
- [ ] 所有测试通過
- [ ] 程序码符合项目标准
- [ ] 無安全漏洞
- [ ] 文件已更新
- [ ] 分支已与目標同步

## 详细指南

完整标准請參阅：
- [审查检查清单](./review-checklist.md)
- [提交前检查清单](./checkin-checklist.md)

## 审查註解範例

```markdown
❗ BLOCKING: 此处有潛在的 SQL injection 漏洞。
請使用參數化查詢而非字串串接。

⚠️ IMPORTANT: 此方法做太多事情了（120 行）。
考慮將验证邏辑提取到獨立方法。

💡 SUGGESTION: 考慮在此使用 Map 而非陣列以达到 O(1) 查找。

❓ QUESTION: 为什麼这里使用 setTimeout 而不是 async/await？

📝 NOTE: 这是个聰明的解决方案！很好地运用了 reduce。
```

## 核心原則

1. **保持尊重** - 审查程序码，而非审查人
2. **保持徹底** - 检查功能性，而非僅检查語法
3. **保持及时** - 在 24 小时內完成审查
4. **保持清晰** - 解釋「为什麼」，而非僅「是什麼」

---

## 配置偵测

此技能支援项目特定配置。

### 偵测順序

1. 检查 `CONTRIBUTING.md` 的「Disabled Skills」區段
   - 如果此技能被列出，則在此项目中停用
2. 检查 `CONTRIBUTING.md` 的「Code Review Language」區段
3. 若未找到，**预设使用英文**

### 首次设置

如果未找到配置且情境不明确：

1. 詢問使用者：「此项目尚未配置程序码审查语言。您想使用哪个选项？（English / 中文）」
2. 使用者选择後，建议在 `CONTRIBUTING.md` 中记录：

```markdown
## Code Review Language

This project uses **[chosen option]** for code review comments.
<!-- Options: English | 中文 -->
```

### 配置範例

在项目的 `CONTRIBUTING.md` 中：

```markdown
## Code Review Language

This project uses **English** for code review comments.
<!-- Options: English | 中文 -->

### Comment Prefixes
BLOCKING, IMPORTANT, SUGGESTION, QUESTION, NOTE
```

---

## 相关标准

- [Code Review Checklist](../../core/code-review-checklist.md)
- [Checkin Standards](../../core/checkin-standards.md)
- [Testing Standards](../../core/testing-standards.md)

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|---------|------|---------|
| 1.0.0 | 2025-12-24 | 新增：标准區段（目的、相关标准、版本历史、授权） |

---

## 授权

此技能依据 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权釋出。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
