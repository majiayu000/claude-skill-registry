---
name: memory-updater
description: 更新 Memory Bank 檔案。觸發：memory、記憶、進度、存檔、sync、做到哪。
---

# Memory Bank 更新技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 更新 memory、記錄進度 | ✅ |
| 存檔、sync、做到哪 | ✅ |
| 工作階段結束時 | ✅ 自動觸發 |

---

## 可用工具

### Memory Bank MCP Tools

| 工具 | 用途 |
|------|------|
| `memory_bank_update_progress` | 更新 progress.md (done/doing/next) |
| `memory_bank_update_context` | 更新 activeContext.md |
| `memory_bank_log_decision` | 記錄重大決策到 decisionLog.md |
| `memory_bank_show_memory` | 顯示特定記憶檔案內容 |
| `memory_bank_switch_mode` | 切換工作模式 (architect/code/ask/debug) |

---

## 檔案對應

| 檔案 | 內容 | 更新時機 |
|------|------|----------|
| `activeContext.md` | 當前工作焦點 | 每次切換任務 |
| `progress.md` | 進度追蹤 (Done/Doing/Next) | 完成任務時 |
| `decisionLog.md` | 重大決策記錄 | 做出架構/技術決策時 |
| `productContext.md` | 產品上下文 | 專案設定變更時 |
| `systemPatterns.md` | 系統模式 | 發現新模式時 |

---

## 標準工作流程

### 流程 A：更新進度

```python
# 完成任務
memory_bank_update_progress(
    done=["完成用戶認證模組"],
    doing=["撰寫測試"],
    next=["部署到 staging"]
)
```

### 流程 B：記錄決策

```python
# 做出重大決策後
memory_bank_log_decision(
    decision="使用 JWT 進行認證",
    rationale="比 session 更適合 API 服務",
    alternatives=["Session-based", "OAuth2"]
)
```

### 流程 C：更新上下文

```python
# 切換工作焦點
memory_bank_update_context(
    current_task="實作密碼重設功能",
    related_files=["src/auth/reset.py", "templates/reset_email.html"]
)
```

---

## 更新原則

1. **增量更新** - 只新增/修改相關內容
2. **保持簡潔** - 避免冗餘描述
3. **時間標記** - 重要項目加上日期
4. **關聯性** - 標記相關檔案和決策

---

## 相關技能

- `memory-checkpoint` - 大量更新時的檢查點
- `git-precommit` - 提交前自動同步
