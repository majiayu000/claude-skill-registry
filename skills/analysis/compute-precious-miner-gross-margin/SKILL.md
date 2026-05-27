---
name: compute-precious-miner-gross-margin
description: 以公開金屬價格 + 礦業成本指標（AISC/All-in cost/現金成本）計算「黃金/白銀礦業毛利率代理值」，並判斷當前是否處於歷史高/低檔區間。
---

<essential_principles>

<principle name="margin_proxy_definition">
**毛利率代理值定義**

礦業毛利率代理（Margin Proxy）使用簡化公式：

```
gross_margin_proxy = (metal_price - unit_cost) / metal_price
```

其中：
- **metal_price**：金屬現貨價或期貨近月價
- **unit_cost**：AISC (All-In Sustaining Cost)、現金成本(C1)或全成本

此指標**不等同會計報表的毛利率**，但能快速捕捉價格-成本關係的邊際變化。
</principle>

<principle name="cost_metric_hierarchy">
**成本指標口徑層次**

| 口徑              | 包含項目                        | 適用場景             |
|-------------------|---------------------------------|----------------------|
| Cash Cost (C1)    | 現場採掘 + 加工 + 場內行政      | 現金流壓力測試       |
| AISC              | C1 + 維持資本開支 + 勘探 + 行政 | 行業標準（WGC 定義） |
| All-In Cost (AIC) | AISC + 成長資本開支             | 完整經濟成本         |

建議優先使用 **AISC**，因其可比性最佳且資料可得性高。
</principle>

<principle name="aggregation_logic">
**籃子聚合邏輯**

| 方法                | 公式                             | 直覺                       |
|---------------------|----------------------------------|----------------------------|
| equal_weight        | Σ margin_i / N                   | 簡單平均，每家公司等權     |
| production_weighted | Σ (margin_i × prod_i) / Σ prod_i | 產量加權，反映「產業毛利」 |
| marketcap_weighted  | Σ (margin_i × mcap_i) / Σ mcap_i | 市值加權，反映「股權曝險」 |

建議使用 **production_weighted** 以更準確反映產業整體毛利結構。
</principle>

<principle name="data_frequency_alignment">
**數據頻率對齊**

- **金屬價格**：日頻或月均價
- **礦業成本**：季度（多數公司僅在季報揭露 AISC）
- **對齊方式**：
  - 將成本 forward-fill 至季度內各期
  - 或使用同季均價（更乾淨）

本 Skill 建議使用 **季度頻率** 作為基準，避免過度平滑。
</principle>

<principle name="data_sources">
**資料取得方式**

本 skill 使用**公開數據**：
- **金價**：LBMA Gold Price / COMEX 近月期貨
- **銀價**：LBMA Silver Price / COMEX 近月期貨
- **AISC**：公司 IR 投資人簡報 / 季報 MD&A / 新聞稿
- **產量**：同上，單位 oz / GEO / AgEq oz

腳本位於 `scripts/` 目錄，可直接執行。
</principle>

</essential_principles>

<objective>
實作「貴金屬礦業毛利率代理值」計算模型：

1. **數據整合**：抓取金屬價格序列與礦業成本/產量數據
2. **計算毛利率代理**：單一公司層級 + 籃子聚合
3. **歷史分位數**：判斷當前水位在歷史區間的位置
4. **驅動拆解**：區分價格驅動 vs 成本驅動
5. **訊號生成**：極端高/低檔區間標記

輸出：毛利率時序、歷史分位、驅動拆解、交易/研究連結。
</objective>

<quick_start>

**最快的方式：執行預設情境分析**

```bash
cd skills/compute-precious-miner-gross-margin
pip install pandas numpy requests yfinance beautifulsoup4 lxml  # 首次使用
python scripts/margin_calculator.py --quick --metal gold
```

輸出範例：
```json
{
  "skill": "compute_precious_miner_margin_proxy",
  "metal": "gold",
  "frequency": "quarterly",
  "cost_metric": "AISC",
  "basket": {
    "miners": ["NEM", "GOLD", "AEM"],
    "aggregation": "production_weighted"
  },
  "latest": {
    "date": "2025-Q4",
    "metal_price_usd_oz": 2650.0,
    "unit_cost_proxy_usd_oz": 1320.0,
    "gross_margin_proxy": 0.502,
    "history_percentile": 0.78,
    "regime_label": "high_margin"
  }
}
```

**完整情境分析**：
```bash
python scripts/margin_calculator.py \
  --metal silver \
  --miners CDE,HL,AG \
  --start-date 2015-01-01 \
  --frequency quarterly \
  --cost-metric AISC \
  --aggregation production_weighted \
  --output result.json
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速計算** - 使用預設參數計算主要礦業籃子的毛利率代理
2. **完整分析** - 自訂參數進行情境分析（可選擇金屬、礦業、成本口徑）
3. **數據研究** - 了解如何獲取 AISC / 成本數據（爬蟲設計）
4. **訊號生成** - 將毛利率轉為交易/研究訊號
5. **方法論學習** - 了解計算邏輯與數據來源

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                    | Action                                             |
|-----------------------------|----------------------------------------------------|
| 1, "快速", "quick", "計算"  | 執行 `python scripts/margin_calculator.py --quick` |
| 2, "完整", "full", "分析"   | 閱讀 `workflows/analyze.md` 並執行                 |
| 3, "數據", "data", "爬蟲"   | 閱讀 `workflows/data-research.md`                  |
| 4, "訊號", "signal", "交易" | 閱讀 `workflows/signal-generation.md` 並執行       |
| 5, "學習", "方法論", "why"  | 閱讀 `references/methodology.md`                   |
| 提供參數 (如礦業清單)       | 閱讀 `workflows/analyze.md` 並使用參數執行         |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
compute-precious-miner-gross-margin/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整情境分析工作流
│   ├── data-research.md               # 數據源研究與爬蟲設計
│   └── signal-generation.md           # 訊號生成工作流
├── references/
│   ├── data-sources.md                # 數據來源與獲取方式
│   ├── methodology.md                 # 方法論與計算邏輯
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   └── margin_calculator.py           # 主計算腳本
└── examples/
    └── sample-output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 毛利率代理值定義
- 成本口徑層次解析
- 聚合方法與直覺
- 歷史分位數計算

**資料來源**: references/data-sources.md
- 金銀價格數據來源
- AISC / 現金成本數據來源
- 產量數據來源
- 爬蟲設計指引

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍
- 預設礦業籃子

</reference_index>

<workflows_index>
| Workflow             | Purpose      | 使用時機                  |
|----------------------|--------------|---------------------------|
| analyze.md           | 完整情境分析 | 需要自訂參數計算毛利率    |
| data-research.md     | 數據源研究   | 了解如何獲取成本數據      |
| signal-generation.md | 訊號生成     | 將毛利率轉為交易/研究訊號 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script               | Command                      | Purpose          |
|----------------------|------------------------------|------------------|
| margin_calculator.py | `--quick --metal gold`       | 快速計算黃金礦業 |
| margin_calculator.py | `--quick --metal silver`     | 快速計算白銀礦業 |
| margin_calculator.py | `--miners NEM,GOLD --freq Q` | 自訂礦業與頻率   |
| margin_calculator.py | `--decompose`                | 驅動拆解分析     |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數        | 類型   | 預設值              | 說明                                   |
|-------------|--------|---------------------|----------------------------------------|
| metal       | string | gold                | 目標金屬（gold/silver）                |
| miners      | array  | 預設籃子            | 礦業代號清單                           |
| start_date  | string | 10 年前             | 計算起始日（YYYY-MM-DD）               |
| end_date    | string | today               | 計算結束日                             |
| frequency   | string | quarterly           | 頻率（daily/weekly/monthly/quarterly） |
| cost_metric | string | AISC                | 成本口徑                               |
| aggregation | string | production_weighted | 聚合方式                               |

**進階參數**

| 參數                 | 類型   | 預設值         | 說明           |
|----------------------|--------|----------------|----------------|
| price_series         | string | spot           | 價格口徑       |
| fx_mode              | string | none           | 匯率處理       |
| outlier_rule         | string | winsorize_1_99 | 離群處理       |
| history_window_years | int    | 20             | 歷史分位數視窗 |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "compute_precious_miner_margin_proxy",
  "metal": "silver",
  "frequency": "quarterly",
  "cost_metric": "AISC",
  "basket": {
    "miners": ["CDE", "HL", "AG"],
    "aggregation": "production_weighted"
  },
  "latest": {
    "date": "2025-Q4",
    "metal_price_usd_oz": 31.50,
    "unit_cost_proxy_usd_oz": 6.30,
    "gross_margin_proxy": 0.80,
    "history_percentile": 0.94,
    "regime_label": "extreme_high_margin"
  },
  "decomposition": {
    "last_3m_price_change_pct": 0.12,
    "last_3m_cost_change_pct": -0.03,
    "driver": "mostly_price_up"
  },
  "notes": [
    "gross_margin_proxy 使用 (price - AISC)/price 作為近似；不等同會計報表的毛利率口徑。",
    "若成本為季度資料，已以季度內 forward-fill/同季均價對齊。"
  ],
  "recommended_next_checks": [
    "用同一套 margin proxy 對照 SIL/SILJ 或個股的 3/6/12 個月前瞻報酬（事件研究）",
    "檢查是否出現資本開支/併購升溫、或成本再通膨（柴油/工資/試劑）導致毛利回落"
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 毛利率代理值時序數據
- [ ] 各礦業的單位成本與毛利率
- [ ] 籃子聚合毛利率
- [ ] 歷史分位數與區間標記（extreme_high/high/neutral/low/extreme_low）
- [ ] 驅動拆解（價格驅動 vs 成本驅動）
- [ ] 結果輸出為指定格式（JSON 或 Markdown）
- [ ] 後續研究建議
</success_criteria>
