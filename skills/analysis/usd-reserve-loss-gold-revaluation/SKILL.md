---
name: usd-reserve-loss-gold-revaluation
description: 在「美元／某貨幣失去儲備地位、黃金成為唯一錨」的假設下，用央行貨幣負債 ÷ 黃金儲備，推演「資產負債表可承受的隱含金價」，並輸出各國/各貨幣的槓桿程度、缺口與排名。
---

<essential_principles>

<principle name="gold_anchor_hypothesis">
**黃金錨定假說**

本模型基於極端情境假設：若法定貨幣體系瓦解、黃金成為唯一錨定資產，則：
- **隱含金價** = 貨幣負債 ÷ 黃金儲備
- 這不是「預測」，而是「壓力測試」：資產負債表要撐得住需要多高的金價

典型論述來源：VanEck「$39k gold」分析（M0 + FX turnover 加權）
</principle>

<principle name="two_aggregates">
**兩種貨幣口徑差異**

| 口徑 | 定義 | 隱含金價 | 解讀 |
|------|------|----------|------|
| M0 (Monetary Base) | 央行直接負債（通貨 + 準備金） | ~$39k | 央行資產負債表壓力 |
| M2 (Broad Money) | 含銀行體系信用擴張 | ~$184k | 全體信用體系壓力 |

**關鍵洞察**：兩者差距反映「信用乘數」的槓桿效應。
</principle>

<principle name="weighting_logic">
**加權方法的直覺**

| 方法 | 數據來源 | 直覺 |
|------|----------|------|
| fx_turnover | BIS 三年調查 | 外匯交易份額 ≈ 國際結算/儲備使用強度 |
| reserve_share | IMF COFER | 官方外匯儲備幣別佔比 |
| equal | - | 不考慮貨幣重要性差異 |
| custom | 用戶自訂 | 可配合特定情境分析 |

加權的直覺：份額越高的貨幣，在「重新錨定」時需吸收的負債壓力越大。
</principle>

<principle name="backing_ratio">
**黃金支撐率 (Backing Ratio)**

```
backing_ratio = (gold_oz × gold_spot) / money_base
```

解讀：
- backing_ratio ≈ 3% → 黃金僅支撐 3% 的貨幣負債（高槓桿）
- backing_ratio ≈ 60% → 黃金接近完全支撐（低槓桿）

貼文中「日本黃金只支撐約 3% 的 M0」即此概念。
</principle>

<principle name="data_access">
**資料取得方式**

本 skill 使用**公開數據**：
- **黃金儲備**：World Gold Council / IMF IFS（tonnes）
- **貨幣量**：各國央行 / FRED / IMF IFS（M0/M2）
- **FX Turnover**：BIS Triennial Survey（每三年更新）
- **金價**：Yahoo Finance / FRED（XAU/USD）

腳本位於 `scripts/` 目錄，可直接執行。
</principle>

</essential_principles>

<objective>
實作「美元失去儲備地位下的黃金重估」壓力測試模型：

1. **數據整合**：抓取各國 M0/M2、黃金儲備、匯率、FX turnover 權重
2. **計算隱含金價**：未加權與加權版本
3. **計算黃金支撐率**：衡量各國槓桿程度
4. **計算缺口**：需要再買多少黃金才能達到目標支撐率
5. **排名輸出**：誰最槓桿、誰最穩健

輸出：隱含金價、支撐率排名、缺口分析、敘事洞察。
</objective>

<quick_start>

**最快的方式：執行預設情境分析**

```bash
cd skills/usd-reserve-loss-gold-revaluation
pip install pandas numpy requests yfinance  # 首次使用
python scripts/gold_revaluation.py --quick
```

輸出範例：
```json
{
  "headline": {
    "implied_gold_price_m0_weighted": 39210.0,
    "implied_gold_price_m2_weighted": 184500.0,
    "interpretation": "壓力測試數字，非價格預測"
  },
  "ranking": [
    {"entity": "JPY", "backing_ratio": 0.03, "lever_multiple": 41.0},
    {"entity": "USD", "backing_ratio": 0.08, "lever_multiple": 12.5},
    {"entity": "ZAR", "backing_ratio": 0.60, "lever_multiple": 0.16}
  ]
}
```

**完整情境分析**：
```bash
python scripts/gold_revaluation.py \
  --date 2026-01-07 \
  --entities USD,CNY,JPY,EUR,GBP \
  --aggregate M0 \
  --weighting fx_turnover \
  --output result.json
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速計算** - 使用預設參數計算主要貨幣的隱含金價
2. **完整分析** - 自訂參數進行情境分析（可選擇口徑、權重、實體）
3. **比較分析** - 同時比較 M0 vs M2、不同加權方法的差異
4. **監控模式** - 追蹤黃金支撐率的變化趨勢
5. **方法論學習** - 了解計算邏輯與數據來源
6. **視覺化圖表** - 生成分析結果的視覺化圖表

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                        | Action                                        |
|---------------------------------|-----------------------------------------------|
| 1, "快速", "quick", "計算"      | 執行 `python scripts/gold_revaluation.py --quick` |
| 2, "完整", "full", "分析"       | 閱讀 `workflows/analyze.md` 並執行            |
| 3, "比較", "compare", "對比"    | 閱讀 `workflows/compare.md` 並執行            |
| 4, "監控", "monitor", "追蹤"    | 閱讀 `workflows/monitor.md` 並執行            |
| 5, "學習", "方法論", "why"      | 閱讀 `references/methodology.md`              |
| 6, "圖表", "畫圖", "視覺化"     | 執行 `python scripts/visualize_revaluation.py` |
| 提供參數 (如實體清單)            | 閱讀 `workflows/analyze.md` 並使用參數執行    |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
usd-reserve-loss-gold-revaluation/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整情境分析工作流
│   ├── compare.md                     # M0/M2 比較分析工作流
│   └── monitor.md                     # 持續監控工作流
├── references/
│   ├── data-sources.md                # 數據來源與獲取方式
│   ├── methodology.md                 # 方法論與計算邏輯
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
└── scripts/
    ├── gold_revaluation.py            # 主計算腳本
    └── visualize_revaluation.py       # 視覺化腳本
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 黃金錨定假說解析
- 隱含金價計算公式
- 支撐率與槓桿解讀

**資料來源**: references/data-sources.md
- 黃金儲備數據來源
- 貨幣量 M0/M2 數據來源
- BIS FX Turnover 數據
- 匯率與金價來源

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow    | Purpose          | 使用時機                   |
|-------------|------------------|---------------------------|
| analyze.md  | 完整情境分析     | 需要自訂參數進行壓力測試   |
| compare.md  | M0/M2 比較分析   | 比較不同口徑的隱含金價差異 |
| monitor.md  | 持續監控         | 追蹤支撐率變化趨勢         |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script                    | Command                         | Purpose                |
|---------------------------|---------------------------------|------------------------|
| gold_revaluation.py       | `--quick`                       | 快速計算主要貨幣       |
| gold_revaluation.py       | `--entities USD,CNY --agg M0`   | 自訂實體與口徑         |
| gold_revaluation.py       | `--compare-aggregates`          | M0 vs M2 比較          |
| visualize_revaluation.py  | `--mode usd`                    | 美元單一視覺化圖表     |
| visualize_revaluation.py  | `--mode multi`                  | 多貨幣比較視覺化圖表   |
| visualize_revaluation.py  | `--mode all --output-dir DIR`   | 生成所有圖表至指定目錄 |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數               | 類型   | 預設值       | 說明                       |
|--------------------|--------|--------------|---------------------------|
| scenario_date      | string | today        | 情境估算基準日期           |
| entities           | array  | 主要貨幣     | 分析對象（國家/貨幣代碼）  |
| monetary_aggregate | string | M0           | 貨幣口徑（M0/M2/MB/M1/M3） |
| weighting_method   | string | fx_turnover  | 加權方式                   |
| fx_base            | string | USD          | 計價幣別基準               |

**進階參數**

| 參數             | 類型   | 預設值     | 說明                   |
|------------------|--------|------------|------------------------|
| liability_scope  | string | broad_money | 負債口徑               |
| gold_reserve_unit| string | troy_oz    | 黃金單位（oz/tonnes）  |
| gold_price_spot  | float  | auto       | 基準日金價（可自動抓取）|
| fx_rates         | object | auto       | 匯率（可自動抓取）     |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "usd-reserve-loss-gold-revaluation",
  "scenario_date": "2026-01-07",
  "assumptions": {
    "monetary_aggregate": "M0",
    "weighting_method": "fx_turnover",
    "fx_base": "USD",
    "gold_spot_usd_per_oz": 2050.0
  },
  "headline": {
    "implied_gold_price_weighted_usd_per_oz": 39210.0,
    "interpretation": "資產負債表壓力測算（非價格預測）"
  },
  "table": [...],
  "insights": [...]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 隱含金價（未加權與加權版本）
- [ ] 各實體的黃金支撐率（backing_ratio）
- [ ] 槓桿倍數排名（lever_multiple_vs_spot）
- [ ] 黃金缺口分析（additional_gold_oz_needed）
- [ ] 敘事洞察（M0 vs M2 差異、槓桿解讀）
- [ ] 結果輸出為指定格式（JSON 或 Markdown）
- [ ] 視覺化圖表（可選，包含金價比較、支撐率、信用乘數等 6 個面板）
</success_criteria>
