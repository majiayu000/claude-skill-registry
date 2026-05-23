---
name: roadmap-updater
description: 更新 ROADMAP.md 狀態。觸發：roadmap、路線、規劃、里程碑。
---

# ROADMAP 更新技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 更新 roadmap、規劃 | ✅ |
| 完成里程碑 | ✅ |
| 被 git-precommit 調用 | ✅ 自動觸發 |

---

## 可用工具

此技能使用標準檔案操作：

| 操作 | 工具 |
|------|------|
| 讀取 | `read_file("ROADMAP.md")` |
| 更新 | `replace_string_in_file()` |
| 搜尋 | `grep_search()` |

---

## 狀態標記

```
📋 計劃中 → 🚧 進行中 → ✅ 已完成
```

---

## 標準工作流程

```python
# 1. 讀取 ROADMAP
read_file("ROADMAP.md")

# 2. 分析完成的功能（從 commit message 或用戶說明）

# 3. 更新狀態
replace_string_in_file(
    filePath="ROADMAP.md",
    oldString="- [ ] 用戶認證",
    newString="- [x] 用戶認證 ✅ (2025-12-22)"
)
```

---

## 格式範例

```markdown
# ROADMAP

## Phase 1: MVP (Q1 2025)

### 已完成 ✅
- [x] 基礎架構設置
- [x] 用戶認證模組

### 進行中 🚧
- [ ] API 文檔

### 計劃中 📋
- [ ] 前端介面

## Phase 2: 擴展 (Q2 2025)
- [ ] 多語言支援
- [ ] 效能優化
```

---

## 輸出範例

```
🗺️ ROADMAP 更新

匹配到的項目：
  ✅ 用戶認證 → 標記為已完成
  🚧 API 文檔 → 保持進行中

建議新增：
  - 新增「密碼重設」到已完成
```

---

## 相關技能

- `git-precommit` - 提交前自動調用
- `changelog-updater` - 同步版本記錄
