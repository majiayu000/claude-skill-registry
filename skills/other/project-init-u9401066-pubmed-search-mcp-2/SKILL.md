---
name: project-init
description: Initialize new projects using this template. Triggers: init, new, 新專案, 初始化, create project, 建立專案, bootstrap, scaffold project.
---

# 專案初始化技能

## 描述
將此專案作為模板，快速初始化新專案。

## 觸發條件
- 「初始化新專案」
- 「從模板建立專案」
- 「create new project」

## 功能

### 1. 模板複製
複製此專案的架構到新目錄：

```
「用這個模板建立 my-new-project」

執行：
1. 複製目錄結構
2. 重置 Git 歷史
3. 更新專案名稱
4. 清空 Memory Bank
5. 重置 CHANGELOG
```

### 2. 複製內容

| 檔案/目錄 | 動作 |
|-----------|------|
| CONSTITUTION.md | 複製 |
| .github/bylaws/ | 複製 |
| .claude/skills/ | 複製 |
| .github/workflows/ | 複製 |
| .github/ISSUE_TEMPLATE/ | 複製 |
| memory-bank/ | 複製結構，清空內容 |
| README.md | 重置為模板 |
| CHANGELOG.md | 重置為初始版本 |
| .git/ | 重新初始化 |

### 3. 互動式設定

詢問用戶：
- 專案名稱
- 專案描述
- 授權類型 (MIT/Apache/GPL)
- 主要程式語言
- 是否需要 Docker 支援

## 輸出格式

```
🚀 專案初始化

專案名稱: my-new-project
位置: ~/projects/my-new-project

✅ 目錄結構已建立
✅ 憲法與子法已複製
✅ Skills 已複製
✅ CI/CD 已設定
✅ Git 已初始化

下一步：
  cd ~/projects/my-new-project
  code .
```
