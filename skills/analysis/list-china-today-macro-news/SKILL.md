---
name: list-china-today-macro-news
description: 彙整今日中國宏觀經濟新聞消息，從華爾街日報、36氪等來源抓取並篩選宏觀相關新聞，輸出雜誌風格的新聞摘要。適用於交易/研究開盤前快速掌握中國宏觀動態。
based_on: news-aggregator-skill
---

# 今日中國宏觀新聞 Skill

> 🔗 Based on [news-aggregator-skill](../../../vendor/news-aggregator-skill) | 專注於中國宏觀經濟新聞的垂直擴展

從多個中文財經新聞源抓取並篩選中國宏觀經濟相關新聞，提供 AI 深度解讀。

## Tools

### fetch_china_macro_news.py

**Usage:**

```bash
### 基本用法：抓取華爾街日報的中國宏觀新聞
python scripts/fetch_china_macro_news.py --source wallstreetcn --limit 15

### 多源掃描：華爾街日報 + 36氪
python scripts/fetch_china_macro_news.py --source wallstreetcn,36kr --limit 10

### 深度抓取（下載文章內容）
python scripts/fetch_china_macro_news.py --source wallstreetcn --limit 10 --deep
```

### 智慧關鍵字擴展 (Smart Keyword Expansion)
**CRITICAL**: 當用戶給出簡單關鍵字時，自動擴展覆蓋相關領域：
*   用戶: "利率" -> Agent 使用: `--keyword "利率,LPR,MLF,降息,加息,PBOC,央行"`
*   用戶: "通膨" -> Agent 使用: `--keyword "通膨,CPI,PPI,物價,通縮"`
*   用戶: "貿易" -> Agent 使用: `--keyword "貿易,進出口,順差,關稅,海關"`

```bash
# Example: User asked for "央行新聞" (Note the expanded keywords)
python scripts/fetch_china_macro_news.py --source wallstreetcn --limit 20 --keyword "央行,PBOC,利率,LPR,MLF,降息,降準" --deep
```

**Arguments:**

- `--source`: One of `wallstreetcn`, `36kr`, `all` (default: wallstreetcn).
- `--limit`: Max items per source (default 15).
- `--keyword`: Comma-separated filters (default: 宏觀相關關鍵字).
- `--deep`: **[NEW]** Enable deep fetching. Downloads and extracts the main text content of the articles.

**Output:**
JSON array. If `--deep` is used, items will contain a `content` field associated with the article text.

## 預設宏觀關鍵字

腳本預設使用以下關鍵字篩選中國宏觀新聞：

```
央行,PBOC,利率,LPR,MLF,降息,降準,
GDP,PMI,CPI,PPI,通膨,通縮,
經濟,宏觀,財政,貨幣政策,
貿易,進出口,順差,逆差,
就業,失業,消費,零售,
房地產,樓市,投資,基建,
人民幣,匯率,外匯,
債券,國債,信貸,社融,M2
```

## Interactive Menu

When the user says **"今日中國宏觀新聞"** (or similar "menu/help" triggers):
1.  **READ** the content of `templates.md` in the skill directory.
2.  **DISPLAY** the list of available commands to the user exactly as they appear in the file.
3.  **GUIDE** the user to select a number or copy the command to execute.

## Smart Time Filtering & Reporting (CRITICAL)

If the user requests a specific time window (e.g., "過去 X 小時") and the results are sparse (< 5 items):
1.  **Prioritize User Window**: First, list all items that strictly fall within the user's requested time (Time < X).
2.  **Smart Fill**: If the list is short, you MUST include high-value/high-heat items from a wider range (e.g. past 24h) to ensure the report provides at least 5 meaningful insights.
3.  **Annotation**: Clearly mark these older items (e.g., "⚠️ 18h 前", "🔥 24h 熱點") so the user knows they are supplementary.
4.  **High Value**: Always prioritize "重大政策", "央行動態", or "關鍵數據" items even if they slightly exceed the time window.

## Response Guidelines (CRITICAL)

**Format & Style:**
- **Language**: 繁體中文 (zh-TW).
- **Style**: Magazine/Newsletter style (e.g., "財訊" or "華爾街日報" vibe). Professional, concise, yet engaging.
- **Structure**:
    - **🔥 頭條焦點**: Top 3-5 most critical macro stories.
    - **💰 央行與貨幣政策**: 利率、流動性相關.
    - **📊 經濟數據**: GDP、PMI、CPI 等數據解讀.
    - **💱 匯率與市場**: 人民幣、債券、股市相關.
- **Item Format**:
    - **Title**: **MUST be a Markdown Link** to the original URL.
        - ✅ Correct: `### 1. [央行宣布降準 0.5 個百分點](https://...)`
        - ❌ Incorrect: `### 1. 央行宣布降準 0.5 個百分點`
    - **Metadata Line**: Must include Source, **Time/Date**, and Heat/Score.
    - **1-Liner Summary**: A punchy, "so what?" summary.
    - **Deep Interpretation (Bulleted)**: 2-3 bullet points explaining *why* this matters, technical details, or context. (Required for "Deep Scan").

**Output Artifact:**
- Always save the full report to `reports/` directory with a timestamped filename (e.g., `reports/china_macro_YYYYMMDD_HHMM.md`).
- Present the full report content to the user in the chat.
- **CRITICAL**: Report footer MUST include attribution line.

## 數據源說明

| 來源           | 說明                                    | 適用場景                     |
|----------------|-----------------------------------------|------------------------------|
| **華爾街日報** | 中國頂級財經媒體，宏觀/市場新聞即時性強 | 央行政策、市場動態、數據解讀 |
| **36氪**       | 科技財經媒體，涵蓋宏觀經濟快訊          | 經濟政策、產業動態           |

## 範例輸出

```markdown
# 今日中國宏觀新聞摘要（2026-01-20）

> 掃描時間：11:30 | 來源：華爾街日報、36氪 | 共 12 條相關新聞

---

## 🔥 頭條焦點

### 1. [央行今日開展 5000 億 MLF 操作，利率持平](https://wallstreetcn.com/...)
📍 華爾街日報 | 🕐 09:45 | 🔥 高關注

央行維持 MLF 利率不變，符合市場預期。

- **核心要點**：本月 MLF 到期量 4500 億，淨投放 500 億
- **市場影響**：短期流動性維持寬鬆，LPR 大概率持平
- **後續觀察**：關注月末資金面與下月降準窗口

### 2. [12 月 PMI 回升至 50.1，製造業重返擴張區間](https://wallstreetcn.com/...)
📍 華爾街日報 | 🕐 10:00 | 🔥 重要數據

官方製造業 PMI 小幅回升，結束連續兩個月收縮。

- **數據亮點**：新訂單指數回升 0.3 個百分點
- **結構分化**：大型企業穩健，中小企業仍承壓
- **政策含義**：穩增長政策效果初顯，但基礎尚不穩固

---

## 💰 央行與貨幣政策

### 3. [1 月 LPR 報價出爐：1 年期 3.10%、5 年期 3.60% 均持平](https://...)
...

---

*報告由 list-china-today-macro-news skill 自動生成*
*🔗 Powered by [news-aggregator-skill](https://github.com/anthropics/news-aggregator-skill)*
```

## Attribution

This skill is built upon and extends the architecture of **news-aggregator-skill**.
- Core fetching patterns derived from `news-aggregator-skill/scripts/fetch_news.py`
- Report formatting follows the news-aggregator-skill Response Guidelines
- Smart Time Filtering logic adapted from news-aggregator-skill

---
*🔗 Based on [news-aggregator-skill](../../../vendor/news-aggregator-skill) by Anthropic*
