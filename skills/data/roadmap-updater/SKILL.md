---
name: roadmap-updater
description: Auto-update ROADMAP.md status based on completed features. Triggers: RM, roadmap, 路線, 規劃, 完成功能, milestone, 里程碑, 路線圖, 計畫, plan, planning, 進度, progress, 功能完成, feature done, 待辦, todo, backlog.
version: 2.2.0
category: documentation
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies: []
allowed-tools:
  - read_file
  - write_file
  - replace_string_in_file
  - get_changed_files
---

# ROADMAP 更新技能

## 描述

根據完成的功能自動更新 ROADMAP.md，保持專案路線圖與實際進度同步。

## 觸發條件

- 「更新 roadmap」「RM」「路線圖」
- 被 `git-precommit` 編排器調用
- 完成規劃中的功能後

---

## 📁 ROADMAP.md 標準格式

```markdown
# Roadmap

> Last updated: 2026-01-15

## ✅ 已完成 (Completed)

- [x] **功能名稱** - 簡短描述 `(2026-01-15)`
- [x] **另一功能** - 描述 `(2026-01-10)`

## 🚧 進行中 (In Progress)

- [ ] **功能名稱** - 描述 `(預計 2026-Q1)`
- [ ] **另一功能** - 描述

## 📋 計劃中 (Planned)

### Phase 1: 基礎建設 (2026-Q1)
- [ ] 計劃項目 1
- [ ] 計劃項目 2

### Phase 2: 功能擴展 (2026-Q2)
- [ ] 計劃項目 3
- [ ] 計劃項目 4

## 🔮 未來考慮 (Future)

- 可能的功能 1
- 可能的功能 2
```

---

## 🔧 操作步驟

### Step 1: 讀取現有 ROADMAP

```
read_file("ROADMAP.md")
```

### Step 2: 取得最近變更（選用）

如果從 `git-precommit` 調用，可取得變更資訊：

```
get_changed_files()
```

分析變更內容以判斷完成了什麼功能。

### Step 3: 匹配 ROADMAP 項目

根據完成的工作，在 ROADMAP 中尋找匹配項目：

**匹配策略**：
1. 精確匹配功能名稱
2. 關鍵字匹配（如 "認證" 匹配 "用戶認證系統"）
3. 檔案路徑推斷（如 `src/auth/` 變更可能對應認證功能）

### Step 4: 執行狀態更新

使用 `replace_string_in_file` 更新狀態：

**計劃中 → 進行中**：
```
oldString: "## 📋 計劃中 (Planned)\n\n- [ ] **用戶認證**"
newString: "## 📋 計劃中 (Planned)\n\n"

oldString: "## 🚧 進行中 (In Progress)\n\n"
newString: "## 🚧 進行中 (In Progress)\n\n- [ ] **用戶認證** - 開發中"
```

**進行中 → 已完成**：
```
oldString: "- [ ] **用戶認證** - 開發中"
newString: ""  (從進行中移除)

oldString: "## ✅ 已完成 (Completed)\n\n"
newString: "## ✅ 已完成 (Completed)\n\n- [x] **用戶認證** - 完成登入/註冊功能 `(2026-01-15)`\n"
```

### Step 5: 更新最後修改日期

```
oldString: "> Last updated: 2026-01-10"
newString: "> Last updated: 2026-01-15"
```

---

## 📊 狀態轉換圖

```
📋 計劃中 (Planned)
    │
    ▼ [開始開發]
🚧 進行中 (In Progress)
    │
    ▼ [完成]
✅ 已完成 (Completed)
```

---

## ⚡ 更新原則

### 1. 保留歷史

```markdown
✅ 正確：
- [x] **功能 A** - 描述 `(2026-01-15)`
- [x] **功能 B** - 描述 `(2026-01-10)`

❌ 錯誤：移除已完成的項目
```

### 2. 時間標記

```markdown
✅ 正確：`(2026-01-15)` 或 `(預計 2026-Q1)`
❌ 錯誤：沒有日期標記
```

### 3. 新功能處理

如果完成了 ROADMAP 未列出的功能：

```markdown
📝 建議新增：
在「✅ 已完成」區塊新增：
- [x] **密碼重設功能** - 實作忘記密碼流程 `(2026-01-15)`
```

---

## 🔄 與其他 Skills 整合

| Skill | 整合方式 |
| ----- | -------- |
| `git-precommit` | 自動調用，傳入變更資訊 |
| `changelog-updater` | 完成的功能同步到 CHANGELOG |
| `memory-updater` | progress.md 的 Done 可參考 |
| `release` | 發布時確認 ROADMAP 狀態 |

---

## 📝 輸出格式

執行完成後回報：

```
🗺️ ROADMAP 更新報告

狀態變更：
- ✅ 用戶認證 - 📋→✅ (標記為已完成)
- 🚧 API 文檔 - 維持進行中

建議新增：
- 💡「密碼重設」功能已完成，建議加入 ROADMAP

已更新：
- ROADMAP.md (Last updated: 2026-01-15)
```

---

## ⚠️ 注意事項

1. **不要刪除計劃項目**：即使決定不做，也應標註而非刪除
2. **Phase 調整需確認**：Phase 的調整通常需要與使用者確認
3. **版本對應**：已完成功能應對應到具體版本或日期
