---
name: cc-agent-audit
description: "Claude Code 專案配置審計。觸發：review/優化 CLAUDE.md、skills、settings、定期清洗累積內容、新專案上線前檢查。"
version: 202604
context: fork
---

# Claude Code 專案配置審計

系統化 review 一個 Claude Code 專案或 agent 的配置品質，確保 prompt 精簡、結構清晰、資訊零損失。

## 核心原則：搬移而非刪除

優化配置時，一律採用「搬移」而非「刪除」：

| 操作 | 錯誤做法 | 正確做法 |
|------|---------|---------|
| 畢業一條 Lesson | 從 CLAUDE.md 刪除 | 搬到共用 rules 或 skill references/ |
| 精簡 description | 移除細節文字 | 先把細節移入 SKILL.md 正文，再縮短 description |
| 刪除一條使用者期待 | 直接刪除 | 搬到對應的 skill |
| 合併重複原則 | 刪較弱的那個 | 保留主版本，標記次版本為 @import 或 reference |

**審計保證**：優化後，所有資訊仍存在於系統的某處，品質不降級。

---

## 三層分離原則

解決「description 要豐富觸發 vs. token 要最小」的矛盾：

```
Layer 1: description（每輪注入 system-reminder）= 觸發條件 ONLY，≤2 句
Layer 2: SKILL.md 正文（按需載入）= 能力範圍、工作流程、品質標準
Layer 3: references/（深度載入）= 知識庫、案例、歷史教訓
```

每層的職責不互相跨越。詳見 `references/three-layer-principle.md`。

---

## 前置載入（按需）

| Skill | 何時需要 |
|-------|---------|
| `cc-prompt-craft` | 審查 CLAUDE.md 文本品質、cache 結構 |
| `cc-agent-design` | 審查工具配置、模型選擇、dispatch prompt |
| `cc-cost-engineering` | 審查 token 消耗、cache 效率、model 成本矩陣 |
| `cc-harness-patterns` | 審查 deferred loading、cache 穩定性 |
| `agentskill-expertise` | 審查 skill 設計哲學、Metadata-driven Triggering |

---

## 5 項檢查

依序執行，每項產出 `PASS / ISSUE(N)` 結論。

---

### Check 1：CLAUDE.md 文本品質

讀取 `CLAUDE.md`，逐項檢查：

| 檢查項 | PASS 條件 | 常見問題 |
|--------|----------|---------|
| 角色定義 | 寫人格不寫機制。一句話設定語氣基調 | 描述 AI 的技術機制而非個性特質 |
| 使用者期待 | 只放跟所有對話都相關的通用事項 | 任務特定指令（如寫作格式）坐在 CLAUDE.md 裡 |
| 核心原則 | 不與 `.claude/rules/` 的任何檔案重複 | 原則內容 rules 已有，出現在 CLAUDE.md 造成雙重定義 |
| 結構順序 | 穩定內容在前，Lessons Learned 在最後 | 易變的 Lessons 插在中間破壞 cache 穩定性 |
| Lessons | ≤10 條，無跟 rules 重複的 | 已被共用規則涵蓋的條目沒有畢業 |
| Skill 關鍵字表（若有）| 所有引用的 skill 名稱有對應的 SKILL.md 存在 | 引用已刪除或改名的 skill |

---

### Check 2：Skill Description 品質

列出所有 `.claude/skills/*/SKILL.md`，逐個檢查 frontmatter：

| 檢查項 | PASS 條件 | 常見問題 |
|--------|----------|---------|
| 有 frontmatter | `---` 包圍的 YAML block 存在 | 缺少 frontmatter，Claude Code 無法顯示於 system-reminder |
| description 長度 | ≤2 句話 | 觸發情境、更新時機、能力列表全塞進 description |
| 觸發條件 | 包含「觸發：」或「Use when:」 | 只寫功能描述，沒說什麼時候用 |
| 無冗餘內容 | 能力範圍、更新政策不在 description 裡 | 這些屬於 SKILL.md 正文，不該佔 system-reminder token |
| 格式統一 | 統一用一種觸發格式 | 有的中文「觸發時機」有的英文「Use when」混用 |

**估算 token 節省**：skill 數量 × 每個 skill 平均精簡 token 數 = 每輪節省量。

---

### Check 3：Settings 配置

讀取 `settings.local.json` 或 `settings.json`，檢查：

| 檢查項 | PASS 條件 | 常見問題 |
|--------|----------|---------|
| 工具最小化 | allow list 只有這個 agent 真的需要的工具 | 一次性加了全套工具，實際用不到 |
| 無冗餘權限 | wildcard（`*`）存在時無個別條目 | `mcp__tool__*` 同時列了 7 條個別權限 |
| deny rules | 執行 bash 的 agent 有 deny rules | 無 deny 導致 agent 可執行危險指令 |
| model 適配 | model 匹配任務複雜度（見 cc-cost-engineering 矩陣） | 簡單反思任務用 opus，浪費費用 |
| MCP server 數量 | `.mcp.json` 的 server 數量合理，無不使用的 server | MCP server 的工具 schema 每輪注入 prompt，多餘 server 增加 token + cache break 風險 |

---

### Check 4：Rules 對齊

確認 `.claude/rules/` 的內容與 `CLAUDE.md` 無矛盾：

| 檢查項 | PASS 條件 |
|--------|----------|
| 無相互矛盾 | rules 與 CLAUDE.md 的指令方向一致 |
| 無跨檔重複 | 同一條指令不同時出現在 rules 和 CLAUDE.md |
| @import 有效 | 若使用 @import，被引用的檔案存在 |

---

### Check 5：跨檔一致性

若有 persona/soul.md，檢查與 CLAUDE.md 的一致性：

| 檢查項 | PASS 條件 | 常見問題 |
|--------|----------|---------|
| 角色定義對齊 | CLAUDE.md 角色定義 ⊆ soul.md Who I Am | CLAUDE.md 寫「AI 助手」但 soul.md 寫有個性的角色名 |
| 原則不矛盾 | CLAUDE.md 核心原則不與 soul.md Work Principles 衝突 | 同一條原則兩邊措辭或方向不同 |
| 使用者期待不重複 | CLAUDE.md 使用者期待不與 soul.md Quirks/How I Sound 重複 | 「emoji 節制」同時出現在兩處 |

若無 persona/soul.md，此 check 標記 N/A。

---

## 執行模式

| 模式 | 觸發方式 | 行為 |
|------|---------|------|
| review | "review X 的配置" / "audit this project" | 唯讀，產出報告，不改任何檔案 |
| fix | "整理 X 的配置" / "optimize this project" | 產出報告 + 列出所有預計改動，等確認後才執行 |
| batch | "review 所有 agent" | 逐個 agent/專案產出獨立報告 |

---

## 輸出格式

```
# 配置審計報告：{project/agent name}

## Summary
- CLAUDE.md: PASS / ISSUE(N)
- Skills: PASS / ISSUE(N)
- Settings: PASS / ISSUE(N)
- Rules: PASS / ISSUE(N)
- Consistency: PASS / ISSUE(N) / N/A

## Issues

### [ISSUE-1] {檢查項}
- Current: ...
- Problem: ...
- Suggested fix: ... （含具體 before/after）
- Migration: 被移除的內容搬到哪裡

### [ISSUE-2] ...

## Token Impact
- Skill descriptions: ~{N} tokens/turn saved
- CLAUDE.md: ~{N} tokens saved
- Rules consolidation: {N} fewer system-reminder injections
```

---

## 安全規範

- **review 模式是嚴格唯讀**，不寫入任何檔案
- **fix 模式**必須先列出所有計畫變更（diff 格式），等待使用者確認後才執行
- **Lessons 永不自動刪除**——只標記為「畢業候選」，由使用者決定
- **Description 精簡**必須先確認細節已移入 SKILL.md 正文，才縮短 description

---

## 依賴的知識來源

- `cc-prompt-craft`：prompt 結構、cache 優化、17 種設計模式
- `cc-agent-design`：工具最小化、模型選擇、dispatch prompt
- `cc-cost-engineering`：token 成本、cache 中斷原因、model 成本矩陣
- `cc-harness-patterns`：deferred loading、cache 穩定性
- `agentskill-expertise`：skill 設計哲學（Metadata-driven、Description-Driven Triggering）
