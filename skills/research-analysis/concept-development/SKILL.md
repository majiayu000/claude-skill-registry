---
name: concept-development
description: 發展研究概念並驗證創新性。觸發：concept、發展概念、研究概念、novelty、創新點、補充概念、幫我補充、擴展概念、加強、驗證失敗、novelty不夠、怎麼改。
---

# 研究概念發展技能

## ⚠️ 核心哲學：像頂尖 Reviewer 一樣犀利！

```
❌ 錯誤：「您的 concept 很好喔～可以考慮補充一下～」（討好式）
✅ 正確：「您聲稱『首次』，但沒有 PubMed 搜尋證據。Reviewer 會問：『你怎麼知道沒人做過？』」
```

**犀利回饋原則**：
1. **直指問題核心** - 不繞彎、不糖衣
2. **用證據說話** - 「你說 X，但文獻顯示 Y」
3. **提出 Reviewer 會問的問題** - 讓作者無法反駁
4. **給具體修復方案** - 不是「可以考慮」，而是「加入這句話」

---

## 黃金法則

1. **永遠先問用戶** - 不要自動修改 NOVELTY/SELLING_POINTS
2. **給犀利但建設性的回饋** - 像嚴格的導師，不是敵人
3. **用戶說「直接寫」就開始** - 尊重用戶決定
4. **反覆修改 = 危險信號** - 如果改了兩次還沒改善，停下來討論

---

## 核心工具

| 工具 | 用途 |
|------|------|
| `read_draft` / `write_draft` | 讀寫 concept.md |
| `validate_for_section` | ⭐ 針對特定 section 驗證（推薦）|
| `validate_concept` | 完整驗證（給出犀利回饋）|
| `list_saved_references` | 檢視已收集文獻 |
| `save_reference_mcp` | 儲存新文獻（**永遠優先**）|
| `sync_references` | 同步 wikilinks 到 References |
| `mcp_cgu_deep_think` | CGU 深度分析概念弱點 |

---

## 🚀 完整流程：從主題到 Concept

### Phase 1: 文獻搜尋（使用 pubmed-search MCP）

```
1. mcp_pubmed-search_search_literature(query="your topic")
   → 搜尋相關文獻，取得 PMIDs

2. mcp_pubmed-search_fetch_article_details(pmids="12345,67890")
   → 取得文章詳細資料（標題、摘要、作者）

3. 分析 Research Gap
   → 向用戶說明：「現有研究做了 X，但缺少 Y」
   → 用證據支持：「搜尋 'A AND B' 結果為 0 篇」
```

### Phase 2: 專案建立（使用 mdpaper MCP）

```
4. mcp_mdpaper_create_project(
     name="my-research-project",
     paper_type="original-research"
   )
   → 建立專案資料夾結構

5. mcp_mdpaper_save_reference_mcp(pmid="12345678")
   → ⚠️ 永遠用 save_reference_mcp，不要用 save_reference
   → 儲存關鍵參考文獻，取得 citation_key
```

### Phase 3: 概念撰寫

```
6. 使用 concept.md template 撰寫：

   ## Research Question
   明確的研究問題（PICO 格式）

   ## 🔒 NOVELTY STATEMENT
   本研究的創新點（必須有搜尋證據支持！）
   ⚠️ 後續撰寫不可弱化！

   ## 🔒 KEY SELLING POINTS
   - 賣點 1
   - 賣點 2
   - 賣點 3
   ⚠️ 必須全部保留！

   ## Gap Analysis
   現有研究的不足（引用文獻說明）

   ## Proposed Approach
   預計使用的方法

7. mcp_mdpaper_write_draft(
     filename="concept.md",
     content="...",
     project="my-research-project"
   )
   → 儲存 concept
```

### Phase 4: 驗證與迭代

```
8. mcp_mdpaper_validate_concept(project="my-research-project")
   → 取得犀利回饋

9. 根據回饋決定：
   - ✅ 直接寫 → 開始 Introduction
   - 🔧 修正 → 一次只改一點
   - 🤖 CGU → 從 reviewer 角度分析
```

---

## 🔒 Protected Content 規則

| 標記 | 內容 | 規則 |
|------|------|------|
| 🔒 NOVELTY STATEMENT | 創新點聲明 | **不可刪除、不可弱化** |
| 🔒 KEY SELLING POINTS | 賣點清單 | **必須全部保留** |

**在後續撰寫中**：
- Introduction 必須呼應 NOVELTY STATEMENT
- Discussion 必須強調 KEY SELLING POINTS
- Agent 修改前必須問用戶確認

---

## 流程 A：從零建立（快速版）

```
1. get_current_project() → 確認專案
2. list_saved_references() → 回顧文獻
3. 定義 PICO + 撰寫 NOVELTY + SELLING_POINTS
4. write_draft(filename="concept.md", content="...")
5. validate_for_section(section="Introduction") → 檢查能否開始寫
```

## 流程 B：補充現有 Concept（用戶主動要求時）

**觸發**：「幫我補充」「加強 concept」「擴展」

```
1. read_draft("concept.md") → 了解現狀
2. 🗣️ 詢問用戶：「想補充哪個方向？」
   - 文獻支持？
   - 創新點細化？
   - 方法說明？
3. 一次只做一件事
4. 讓用戶確認後再繼續
```

---

## 🔔 Novelty Score 低的處理流程（犀利回饋模式）

**觸發**：validate_concept 回傳 score < 75

### ⚠️ 絕對不要做的事

```
❌ 自動開始修改 NOVELTY STATEMENT
❌ 連續多次修改嘗試「提高分數」
❌ 用討好的語氣說「您的 concept 很好」
```

### ✅ 正確流程：犀利但給選項

**Step 1: 給出犀利回饋**

```
「**Score:** 65/100

**⚠️ Critical Issues (Reviewer 會質疑):**

❌ **您聲稱『首次』，但沒有提供文獻搜尋證據**
- 🎯 Reviewer 會問：『你怎麼知道沒人做過？搜尋策略是什麼？』
- 🔧 加入：『PubMed 搜尋 "X AND Y" (2024-12-17) 結果為 0 篇』

❌ **使用模糊用語『更好』但沒有量化**
- 🎯 Reviewer 會問：『好多少？有統計學意義嗎？』
- 🔧 改為：『減少 50%』或『OR 0.3 (95% CI 0.1-0.5)』

**您的選擇：**
1. ✅ 直接寫 → 我立即開始
2. 🔧 修正問題 → 告訴我要改哪個
3. 🤖 用 CGU 想 → 從 reviewer 角度找更多弱點」
```

**Step 2: 根據用戶回應**

| 用戶說 | Agent 行為 |
|--------|------------|
| 「直接寫」 | ✅ 立即開始寫 Introduction |
| 「幫我加搜尋證據」 | 🔧 只改那一點，不改其他 |
| 「用 CGU 想想」 | 🤖 呼叫 CGU 從 reviewer 角度分析 |

---

## 🤖 CGU 創意工具使用指南

**何時建議使用 CGU？**
- 用戶卡關，不知道怎麼強化
- Score < 60，需要從對手角度思考
- 用戶主動說「幫我想想」

### 工具選擇

| 情境 | CGU 工具 | 用法 |
|------|----------|------|
| 找出弱點在哪 | `deep_think` | `deep_think(topic="從 reviewer 角度，這個研究最容易被攻擊的點是什麼？", depth="medium")` |
| 找強化論點 | `spark_collision` | `spark_collision(concept_a="現有研究的限制", concept_b="我的方法優勢")` |
| 廣泛發想 | `generate_ideas` | `generate_ideas(topic="如何讓這個研究的 novelty 無可辯駁", count=5)` |

### CGU 使用流程

```
1. 用戶說「用 CGU 想想」
2. 呼叫 CGU 工具
3. 整理輸出，列出 2-3 個具體建議
4. 問用戶：「這些方向哪個最適合？」
5. 用戶選擇後，只修改那一個方向
```

---

## 犀利回饋範本

### Pattern 1: 聲稱「首次」但沒證據

```
❌ **問題**：您聲稱『首次』，但沒有提供文獻搜尋證據
🎯 **Reviewer 會問**：『你怎麼知道沒人做過？你的搜尋策略是什麼？』
🔧 **具體修復**：加入 `PubMed 搜尋 "term1 AND term2" (日期) 結果為 0 篇`
```

### Pattern 2: 模糊量化

```
❌ **問題**：使用『更好』『改善』但沒有數字
🎯 **Reviewer 會問**：『好多少？臨床上有意義嗎？』
🔧 **具體修復**：改為 `OR 0.3 (95% CI 0.1-0.5)` 或 `減少 50%`
```

### Pattern 3: 有引用但沒說限制

```
❌ **問題**：引用了 [[author2024]] 但沒說它的限制
🎯 **Reviewer 會問**：『既然有人做過，你的貢獻在哪？』
🔧 **具體修復**：加入 `[[author2024]] 比較了 A vs B，但【未納入 C / 未評估 X】`
```

---

## 🚨 危險信號：何時必須停下來

| 信號 | 行動 |
|------|------|
| 已經改了 2 次，分數沒改善 | **停！** 問用戶要不要換方向 |
| 改完分數反而變低 | **停！** 恢復原版，討論其他方案 |
| 發現要大幅修改研究方向 | **停！** 這是用戶的決定 |
| 用戶沒回應就繼續改 | **停！** 永遠等用戶確認 |

---

## 分層驗證（快速參考）

| Paper Type | Core Required | Intro | Methods |
|------------|---------------|-------|---------|
| original-research | NOVELTY, SELLING_POINTS | background, gap | ⚠️ recommended |
| systematic-review | + search_strategy | same | same |
| case-report | same | same | minimal |
| letter | NOVELTY only | minimal | - |

**Section-Specific 驗證**：
```
validate_for_section(section="Introduction")
# → can_write_section=True 就能開始寫，Methods 缺少不 blocking
```

---

## Wikilink 格式

| 格式 | 範例 | 狀態 |
|------|------|------|
| ✅ 正確 | `[[ruetzler2024_38497992]]` | 標準 |
| ❌ 錯誤 | `[[38497992]]` | 缺 author_year |

**取得 citation_key**：
```
save_reference_mcp(pmid="38497992")
# 回傳：💡 Use [[ruetzler2024_38497992]]
```

---

## 好的 Novelty Statement 範例

✅ 「PubMed 搜尋 "X AND Y" 結果為 0 篇。本研究首次在**台灣 ICU** 比較 **remimazolam 和 propofol**」
✅ 「[[author2024]] 比較了 A vs B，但未納入 C。本研究首次加入 C」
❌ 「我們研究了 X」（太模糊）
❌ 「這是首次...」（沒有搜尋證據）

---

## 決策點

| 時機 | 問題 | 選項 |
|------|------|------|
| 驗證顯示 score < 75 | 怎麼辦？ | **先問用戶**：直接寫 / 修正問題 / 用 CGU |
| 用戶選「修正」 | 改哪個？ | 只改用戶指定的那一點 |
| 用戶選「CGU」 | 用哪個？ | deep_think（找弱點）/ spark_collision（找論點）|

---

## 相關技能

- `literature-review` - 前置步驟
- `parallel-search` - 補充文獻搜尋
