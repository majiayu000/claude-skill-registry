---
source: skills/claude-code/commit-standards/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2025-12-25
status: current
name: commit-standards
description: |
  遵循約定式提交标准格式化提交消息。
  使用时机：撰写提交消息、git commit、檢视提交历史。
  关鍵字：commit、git、message、conventional、feat、fix、refactor。
---

# 提交消息标准

> **语言**: [English](../../../../../skills/claude-code/commit-standards/SKILL.md) | 简体中文

**版本**: 1.0.0
**最後更新**: 2025-12-24
**適用範圍**: Claude Code Skills

---

## 目的

此技能确保遵循約定式提交标准，撰写一致且有意義的提交消息。

## 快速參考

### 基本格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型

| English | 使用时机 |
|---------|----------|
| `feat` | 新功能 |
| `fix` | 错误修正 |
| `refactor` | 程序码重構（無功能变更） |
| `docs` | 僅文件变更 |
| `style` | 格式調整（無程序码邏辑变更） |
| `test` | 新增或更新测试 |
| `perf` | 效能改善 |
| `build` | 建置系统或依賴项目 |
| `ci` | CI/CD 流程变更 |
| `chore` | 維護任务 |
| `revert` | 还原先前的提交 |
| `security` | 安全漏洞修正 |

### 主旨行規則

1. **長度**: ≤72 字元（50 为理想）
2. **时態**: 祈使語氣（使用 "Add feature" 而非 "Added feature"）
3. **大小写**: 首字母大写
4. **無句点**: 結尾不加句点

## 详细指南

完整标准請參考：
- [約定式提交指南](./conventional-commits.md)
- [语言选项](./language-options.md)

## 範例

### ✅ 良好範例

```
feat(auth): Add OAuth2 Google login support
fix(api): Resolve memory leak in user session cache
refactor(database): Extract query builder to separate class
docs(readme): Update installation instructions for Node 20
```

### ❌ 不良範例

```
fixed bug                    # 太模糊，無範圍
feat(auth): added google login  # 過去式
Update stuff.                # 有句点，模糊
WIP                          # 不具描述性
```

## 主体内容指南

使用主体内容说明变更的**原因（WHY）**：

```
fix(api): Resolve race condition in concurrent user updates

Why this occurred:
- Two simultaneous PUT requests could overwrite each other
- No optimistic locking implemented

What this fix does:
- Add version field to User model
- Return 409 Conflict if version mismatch

Fixes #789
```

## 破壞性变更

务必在页腳记录破壞性变更：

```
feat(api): Change user endpoint response format

BREAKING CHANGE: User API response format changed

Migration guide:
1. Update API clients to remove .data wrapper
2. Use created_at instead of createdAt
```

## 議題參照

```
Closes #123    # 自动关閉議題
Fixes #456     # 自动关閉議題
Refs #789      # 連結但不关閉
```

---

## 配置檢测

此技能支援项目特定的语言配置。

### 檢测順序

1. 检查 `CONTRIBUTING.md` 中的「Commit Message Language」區段
2. 若找到，使用指定的选项（English / 简体中文 / Bilingual）
3. 若未找到，**预设使用 English** 以獲得最大工具相容性

### 首次设置

若未找到配置且情境不明确：

1. 詢問使用者：「此项目尚未配置提交消息语言偏好。您想使用哪个选项？（English / 中文 / Bilingual）」
2. 使用者选择後，建议记录於 `CONTRIBUTING.md`：

```markdown
## Commit Message Language

This project uses **[chosen option]** commit types.
<!-- Options: English | 简体中文 | Bilingual -->
```

### 配置範例

在项目的 `CONTRIBUTING.md` 中：

```markdown
## Commit Message Language

This project uses **English** commit types.

### Allowed Types
feat, fix, refactor, docs, style, test, perf, build, ci, chore, revert, security
```

---

## 相关标准

- [提交消息指南](../../../../../core/commit-message-guide.md)
- [Git 工作流程](../../../../../core/git-workflow.md)
- [变更日誌标准](../../../../../core/changelog-standards.md)

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | 2025-12-24 | 新增：标准區段（目的、相关标准、版本历史、授权） |

---

## 授权

此技能以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 釋出。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
