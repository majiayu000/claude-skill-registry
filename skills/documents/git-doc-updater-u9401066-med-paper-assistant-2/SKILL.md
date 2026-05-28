---
name: git-doc-updater
description: Git 提交前文檔同步。觸發：docs、文檔、sync docs、發布。
---

# Git 文檔自動更新技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 更新文檔、sync docs | ✅ |
| 準備發布 | ✅ |
| 被 git-precommit 調用 | ✅ 自動觸發 |

---

## 可用工具

| 操作 | 工具 |
|------|------|
| 讀取檔案 | `read_file()` |
| 更新檔案 | `replace_string_in_file()` |
| Git 變更 | `get_changed_files()` |
| Memory Bank | `memory_bank_update_progress()` |

---

## 自動更新的文檔

| 文檔 | 更新條件 | 調用的 Skill |
|------|----------|--------------|
| README.md | 新功能/依賴變更 | `readme-updater` |
| CHANGELOG.md | 任何代碼變更 | `changelog-updater` |
| ROADMAP.md | 完成里程碑 | `roadmap-updater` |
| memory-bank/ | 每次提交 | `memory-updater` |

---

## 標準工作流程

```python
# 1. 分析變更
get_changed_files()

# 2. 判斷需要更新哪些文檔
# - 新檔案在 src/ → README 功能列表
# - pyproject.toml 變更 → README 安裝說明
# - 任何變更 → CHANGELOG
# - 完成 ROADMAP 項目 → ROADMAP

# 3. 依序呼叫對應 Skills（參見流程圖）

# 4. 同步 Memory Bank
memory_bank_update_progress(done=["..."], doing=[], next=["..."])
```

---

## 執行流程圖

```
Git Commit 請求
     │
     ▼
分析變更檔案
     │
     ├──> README 需要更新? ──> readme-updater
     │
     ├──> CHANGELOG 需要更新? ──> changelog-updater
     │
     ├──> ROADMAP 需要更新? ──> roadmap-updater
     │
     └──> memory-updater（必要）
```

---

## 輸出範例

```
📝 文檔更新檢查

✅ README.md - 無需更新
✅ CHANGELOG.md - 已添加 v1.2.0 條目
✅ ROADMAP.md - 已標記「用戶認證」為完成
✅ memory-bank/progress.md - 已更新進度

準備提交 4 個文檔變更...
```

---

## 相關技能

- `git-precommit` - 調用此技能
- `readme-updater` - README 更新
- `changelog-updater` - CHANGELOG 更新
- `memory-updater` - Memory Bank 更新
