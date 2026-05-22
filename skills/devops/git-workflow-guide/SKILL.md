---
source: /skills/claude-code/git-workflow-guide/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2025-12-25
status: current
name: git-workflow-guide
description: |
  指導 Git 分支策略、分支命名与合併操作。
  使用时机：建立分支、合併、Pull Request、Git 工作流程問題。
  关鍵字：branch, merge, PR, pull request, GitFlow, GitHub Flow, 分支, 合併, 工作流程。
---

# Git 工作流程指南

> **语言**: [English](../../../../../skills/claude-code/git-workflow-guide/SKILL.md) | 简体中文

**版本**: 1.0.0
**最後更新**: 2025-12-24
**適用範圍**: Claude Code Skills

---

## 目的

本技能提供 Git 分支策略、分支命名慣例与合併操作的指導。

## 快速參考

### 工作流程策略选择

| 部署頻率 | 建议策略 |
|---------|---------|
| 每日多次 | Trunk-Based Development |
| 每周至雙周 | GitHub Flow |
| 每月或更長 | GitFlow |

### 分支命名慣例

```
<type>/<short-description>
```

| 类型 | 用途 | 範例 |
|------|------|------|
| `feature/` | 新功能 | `feature/oauth-login` |
| `fix/` 或 `bugfix/` | 错误修復 | `fix/memory-leak` |
| `hotfix/` | 緊急生产環境修復 | `hotfix/security-patch` |
| `refactor/` | 程序码重構 | `refactor/extract-service` |
| `docs/` | 僅文件变更 | `docs/api-reference` |
| `test/` | 测试新增 | `test/integration-tests` |
| `chore/` | 維護任务 | `chore/update-dependencies` |
| `release/` | 發布准备 | `release/v1.2.0` |

### 命名規則

1. **使用小写**
2. **使用連字号分隔单字**
3. **描述性但簡潔**

## 详细指南

完整标准請參阅：
- [Git 工作流程策略](./git-workflow.md)
- [分支命名參考](./branch-naming.md)

## 建立分支前检查清单

建立新分支前：

1. **检查未合併的分支**
   ```bash
   git branch --no-merged main
   ```

2. **同步最新程序码**
   ```bash
   git checkout main
   git pull origin main
   ```

3. **验证测试通過**
   ```bash
   npm test  # 或您项目的测试指令
   ```

4. **使用正确命名建立分支**
   ```bash
   git checkout -b feature/description
   ```

## 合併策略快速指南

| 策略 | 使用时机 |
|------|---------|
| **Merge Commit** (`--no-ff`) | 長期功能、GitFlow 發布 |
| **Squash Merge** | 功能分支、乾淨历史 |
| **Rebase + FF** | Trunk-Based、短期分支 |

## 範例

### 建立功能分支

```bash
# 良好範例
git checkout -b feature/user-authentication
git checkout -b fix/null-pointer-in-payment
git checkout -b hotfix/critical-data-loss

# 不良範例
git checkout -b 123              # 缺乏描述性
git checkout -b Fix-Bug          # 非小写
git checkout -b myFeature        # 缺少类型前綴
```

### 合併工作流程 (GitHub Flow)

```bash
# 1. 從 main 建立分支
git checkout main
git pull origin main
git checkout -b feature/user-profile

# 2. 进行变更并提交
git add .
git commit -m "feat(profile): add avatar upload"
git push -u origin feature/user-profile

# 3. 透過 GitHub/GitLab UI 建立 PR 并合併

# 4. 合併後刪除分支
git checkout main
git pull origin main
git branch -d feature/user-profile
```

### 处理合併衝突

```bash
# 1. 使用 main 更新您的分支
git checkout feature/my-feature
git fetch origin
git merge origin/main

# 2. 在文件中解决衝突
# <<<<<<< HEAD
# 您的变更
# =======
# 传入的变更
# >>>>>>> origin/main

# 3. 暫存已解决的文件
git add resolved-file.js

# 4. 完成合併
git commit -m "chore: resolve merge conflicts with main"

# 5. 测试并推送
npm test
git push origin feature/my-feature
```

---

## 組態偵测

本技能支援项目特定的工作流程組態。

### 偵测順序

1. 检查 `CONTRIBUTING.md` 是否有「Git Workflow」或「Branching Strategy」章节
2. 若找到，使用指定的策略（GitFlow / GitHub Flow / Trunk-Based）
3. 若未找到，**预设使用 GitHub Flow** 以保持簡单

### 首次设置

若未找到組態：

1. 詢問使用者：「本项目尚未设置 Git 工作流程策略。您偏好哪一种？（GitFlow / GitHub Flow / Trunk-Based）」
2. 选择後，建议在 `CONTRIBUTING.md` 中记录：

```markdown
## Git 工作流程

### 分支策略
本项目使用 **[所選选项]**。

### 分支命名
格式：`<type>/<description>`
範例：`feature/oauth-login`、`fix/memory-leak`

### 合併策略
- 功能分支：**[Squash / Merge commit / Rebase]**
```

---

## 相关标准

- [Git 工作流程](../../core/git-workflow.md)
- [提交消息指南](../../core/commit-message-guide.md)
- [簽入标准](../../core/checkin-standards.md)

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2025-12-24 | 新增：标准章节（目的、相关标准、版本历史、授权） |

---

## 授权

本技能採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权發布。

**來源**：[universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
