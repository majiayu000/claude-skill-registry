---
name: backsolve-miner-vs-metal-ratio-with-fundamentals
description: 從網路自動抓取礦業公司財務報表與營運揭露（產量、成本、資本支出），回算「礦業股/金屬本體比率」的基本面解釋與區間門檻（如 1.2/1.7），並輸出可重現的估值拆解（成本因子 / 槓桿因子 / 倍數因子 / 稀釋因子）。
---

<essential_principles>

<principle name="ratio_decomposition">
**比率拆解核心公式**

礦業股/金屬價格比率可分解為四大基本面因子：

```
R_t ≈ K × M_t × (1-L_t) × C_t × D_t
```

其中：
- **K**: 校準常數（由觀測值估計）
- **M_t**: 倍數因子（EV/EBITDA）
- **(1-L_t)**: 槓桿因子（1 - NetDebt/EV）
- **C_t**: 成本因子（1 - AISC/S_t）
- **D_t**: 稀釋因子（Shares_base / Shares_t）

此拆解讓「比率變動」有可歸因的量化解釋。
</principle>

<principle name="aisc_extraction">
**AISC 抽取優先順序**

全維持成本（AISC）是礦業股估值的核心驅動：

| 優先級 | 來源            | 方法                                        |
|--------|-----------------|---------------------------------------------|
| 1      | MD&A / 財報附註 | 關鍵字抽取：「AISC」「all-in sustaining」   |
| 2      | 年報簡報 PDF    | 解析表格：$/oz 或 $/ounce                   |
| 3      | Proxy 回算      | (OpCost + SustCapex + G&A - Byproduct) / Oz |

當直接揭露不可得時，以 proxy 回算補缺；記錄 `aisc_method` 以標註來源。
</principle>

<principle name="backsolve_logic">
**反推邏輯（Backsolve）**

目標：給定目標比率 R*（如歷史頂部 1.7），反推需要哪些因子條件。

**單因子反推**：假設其他因子不變，只調整單一因子

```
M* = M_now × (R*/R_now)         # 需要的倍數
(1-L*) = (1-L_now) × (R*/R_now) # 需要的去槓桿
C* = C_now × (R*/R_now)         # 需要的成本改善 → 反推 AISC*
D* = D_now × (R*/R_now)         # 需要的稀釋折扣
```

**雙因子組合**：以網格列舉可行組合（如倍數 +20% + 白銀 -15%）。
</principle>

<principle name="event_study">
**事件研究方法**

識別「比率落入底部分位」的歷史事件，回看事件當期的四大因子狀態：

1. **AISC 是否上升**：成本壓力
2. **NetDebt/EV 是否惡化**：槓桿壓力
3. **EV/EBITDA 是否壓縮**：倍數壓力
4. **Shares 是否上升**：稀釋壓力

排名「哪個因子貢獻最大」，識別驅動底部的主因。
</principle>

<principle name="data_priority">
**數據來源優先順序**

遵循「結構化優先」原則：

1. **SEC XBRL (10-K/10-Q)**：直接取欄位（債務、現金、股數、CFO、Capex）
2. **SEDAR+ (加拿大)**：銀礦公司常在加拿大上市
3. **公司 IR 年報/MD&A**：補齊 AISC、產量等非標準欄位
4. **ETF Holdings**：官方 CSV 或 SEC N-PORT

抓取時使用 Selenium 模擬人類行為，避免被封鎖。
</principle>

</essential_principles>

<objective>
實作「礦業股/金屬價格比率」基本面回算系統：

1. **數據整合**：抓取價格、ETF 持股、財務報表、營運揭露
2. **因子計算**：計算 AISC、槓桿、倍數、稀釋四大因子
3. **比率拆解**：建立 R_t ≈ K × M × (1-L) × C × D 近似式
4. **門檻反推**：給定目標比率，反推需要的因子組合
5. **事件研究**：歷史底部事件的因子驅動分析
6. **輸出報告**：結構化 JSON 與可讀 Markdown

目標用戶：看到 SIL/白銀比率極端時，想用「真實財報」驗證驅動因素。
</objective>

<quick_start>

**最快的方式：使用預設參數分析**

```bash
cd skills/backsolve-miner-vs-metal-ratio-with-fundamentals
pip install pandas numpy yfinance matplotlib  # 首次使用
python scripts/fundamental_analyzer.py --quick
```

**完整分析（含財報抓取）**

```bash
python scripts/fundamental_analyzer.py \
  --metal-symbol SI=F \
  --miner-universe etf:SIL \
  --region-profile us_sec \
  --start-date 2015-01-01 \
  --output result.json
```

**生成視覺化儀表板**

```bash
python scripts/visualize_factors.py --quick --output output/
# 輸出: output/sil_silver_factor_analysis_YYYY-MM-DD.png
```

視覺化儀表板包含四個面板：
1. **比率時間序列**：歷史走勢 + 分位數區間（底部/頂部）
2. **因子雷達圖**：四大因子健康度一覽
3. **因子評分長條圖**：成本、槓桿、倍數、稀釋各項評分
4. **情境熱力圖**：倍數擴張 × 白銀變動的組合分析

**共同上漲情境模擬**

```bash
python scripts/scenario_path_simulator.py --quick --output output/
# 輸出: output/scenario_path_YYYY-MM-DD.png + return_heatmap_YYYY-MM-DD.png
```

核心公式：**礦業股漲幅 = (1 + 銀價漲幅) × (R₁/R₀) - 1**

自訂參數：
```bash
python scripts/scenario_path_simulator.py \
  --silver-monthly 5 \      # 銀價每月漲幅 5%
  --ratio-start 1.10 \      # 比率起點
  --ratio-end 1.20 \        # 比率終點
  --months 6 \              # 模擬 6 個月
  --heatmap                 # 同時生成熱力圖
```

**輸出範例**：

```json
{
  "now": {
    "metal_price": 94.4,
    "miner_price": 103.4,
    "ratio": 1.13,
    "ratio_percentile": 0.111
  },
  "thresholds": {
    "bottom_ratio": 1.20,
    "top_ratio": 1.70,
    "median_ratio": 1.51
  },
  "fundamentals_weighted": {
    "aisc_usd_per_oz": 28.0,
    "net_debt_to_ev": 0.25,
    "ev_to_ebitda": 6.4,
    "shares_yoy_change": 0.12
  },
  "factors_now": {
    "cost_factor_C": 0.7034,
    "leverage_factor_1_minus_L": 0.75,
    "multiple_M": 6.4,
    "dilution_discount_D": 0.89
  },
  "backsolve_to_top": {
    "multiple_only_need": 9.1,
    "deleverage_only_need_1_minus_L": 1.12,
    "cost_only_implied_aisc": 15.6,
    "dilution_only_need_D": 1.26
  }
}
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速分析** - 使用預設參數（SIL / SI=F）計算當前因子狀態
2. **完整分析** - 抓取財報、計算因子、反推門檻
3. **因子拆解** - 深入了解四大因子的計算邏輯
4. **門檻反推** - 給定目標比率，計算需要的因子組合
5. **事件研究** - 歷史底部事件的因子驅動排名
6. **方法論學習** - 了解回算邏輯與數據來源
7. **視覺化** - 生成四面板儀表板圖表
8. **共同上漲情境** - 模擬銀價與礦業股同漲時的比例關係與路徑

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                       | Action                                                         |
|--------------------------------|----------------------------------------------------------------|
| 1, "快速", "quick", "分析"     | 執行 `python scripts/fundamental_analyzer.py --quick`          |
| 2, "完整", "full", "財報"      | 閱讀 `workflows/analyze.md` 並執行                             |
| 3, "因子", "factor", "拆解"    | 閱讀 `references/fundamental-factors.md`                       |
| 4, "反推", "backsolve", "門檻" | 閱讀 `references/backsolve-math.md` 並執行反推分析             |
| 5, "事件", "event", "底部"     | 閱讀 `workflows/analyze.md` 並聚焦事件研究                     |
| 6, "學習", "方法論", "why"     | 閱讀 `references/fundamental-factors.md` + `backsolve-math.md` |
| 7, "視覺化", "圖", "chart"     | 執行 `python scripts/visualize_factors.py --quick`             |
| 8, "共同上漲", "情境", "路徑"  | 執行 `python scripts/scenario_path_simulator.py --quick`       |
| "比例關係", "漲幅", "要漲多少" | 執行 `python scripts/scenario_path_simulator.py --quick`       |
| 提供參數 (如 ETF/金屬代理)     | 閱讀 `workflows/analyze.md` 並使用參數執行                     |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
backsolve-miner-vs-metal-ratio-with-fundamentals/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整分析工作流
│   └── data-fetch.md                  # 數據抓取工作流
├── references/
│   ├── input-schema.md                # 完整輸入參數定義
│   ├── data-sources.md                # 數據來源說明
│   ├── fundamental-factors.md         # 四大因子計算邏輯
│   └── backsolve-math.md              # 反推數學公式
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── fundamental_analyzer.py        # 主計算腳本
│   ├── visualize_factors.py           # 視覺化儀表板腳本
│   └── scenario_path_simulator.py     # 共同上漲情境模擬器
└── examples/
    └── sample-output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍
- 各方法選項說明

**數據來源**: references/data-sources.md
- 價格數據（yfinance / stooq / alphavantage）
- 財報數據（SEC EDGAR / SEDAR+ / 公司 IR）
- ETF 持股（官方 CSV / N-PORT / 手動 URL）

**因子計算**: references/fundamental-factors.md
- AISC 成本因子
- 槓桿因子
- 倍數因子
- 稀釋因子

**反推數學**: references/backsolve-math.md
- 單因子反推公式
- 雙因子組合網格
- 校準常數估計

</reference_index>

<workflows_index>
| Workflow      | Purpose  | 使用時機                    |
|---------------|----------|-----------------------------|
| analyze.md    | 完整分析 | 需要抓取財報並計算因子      |
| data-fetch.md | 數據抓取 | 了解如何抓取 ETF 持股與財報 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script                     | Command                              | Purpose                    |
|----------------------------|--------------------------------------|----------------------------|
| fundamental_analyzer.py    | `--quick`                            | 快速分析 SIL/SI=F          |
| fundamental_analyzer.py    | `--miner-universe etf:SILJ`          | 自訂礦業股 ETF             |
| fundamental_analyzer.py    | `--backsolve-target 1.7`             | 指定反推目標比率           |
| fundamental_analyzer.py    | `--event-study --min-separation 180` | 執行事件研究               |
| visualize_factors.py       | `--quick --output output/`           | 生成四面板視覺化儀表板     |
| visualize_factors.py       | `--input result.json`                | 從 JSON 結果生成圖表       |
| scenario_path_simulator.py | `--quick`                            | 共同上漲情境路徑模擬       |
| scenario_path_simulator.py | `--silver-monthly 5 --months 6`      | 自訂銀價月漲幅與模擬月數   |
| scenario_path_simulator.py | `--ratio-start 1.10 --ratio-end 1.20`| 自訂比率起終點             |
| scenario_path_simulator.py | `--heatmap`                          | 同時生成收益率熱力圖       |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數                 | 類型   | 預設值  | 說明                                    |
|----------------------|--------|---------|-----------------------------------------|
| metal_symbol         | string | SI=F    | 金屬價格代碼（SI=F 白銀、GC=F 黃金）    |
| miner_universe       | object | etf:SIL | 礦業股/ETF 定義                         |
| region_profile       | string | us_sec  | 監管與揭露來源（us_sec / canada_sedar） |
| time_range.start     | string | 5 年前  | 分析起點（YYYY-MM-DD）                  |
| time_range.end       | string | today   | 分析終點                                |
| time_range.frequency | string | weekly  | 取樣頻率（daily/weekly/monthly）        |

**因子方法選擇**

| 參數                         | 類型   | 預設值              | 說明          |
|------------------------------|--------|---------------------|---------------|
| fundamental_methods.aisc     | string | hybrid              | AISC 抽取方法 |
| fundamental_methods.leverage | string | net_debt_to_ev      | 槓桿計算方法  |
| fundamental_methods.multiple | string | ev_to_ebitda        | 倍數計算方法  |
| fundamental_methods.dilution | string | weighted_avg_shares | 稀釋計算方法  |

**分位門檻**

| 參數                    | 類型  | 預設值 | 說明           |
|-------------------------|-------|--------|----------------|
| ratio_thresholds.bottom | float | 0.20   | 底部分位數門檻 |
| ratio_thresholds.top    | float | 0.80   | 頂部分位數門檻 |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "backsolve_miner_vs_metal_ratio_with_fundamentals",
  "inputs": {
    "metal_symbol": "SI=F",
    "miner_universe": {"type": "etf_holdings", "etf_ticker": "SIL"},
    "region_profile": "us_sec"
  },
  "now": {
    "metal_price": 94.4,
    "miner_price": 103.4,
    "ratio": 1.13,
    "ratio_percentile": 0.111
  },
  "thresholds": {
    "bottom_ratio": 1.20,
    "top_ratio": 1.70,
    "median_ratio": 1.51
  },
  "fundamentals_weighted": {
    "aisc_usd_per_oz": 28.0,
    "net_debt_to_ev": 0.25,
    "ev_to_ebitda": 6.4,
    "shares_yoy_change": 0.12
  },
  "factors_now": {
    "cost_factor_C": 0.7034,
    "leverage_factor_1_minus_L": 0.75,
    "multiple_M": 6.4,
    "dilution_discount_D": 0.89
  },
  "backsolve_to_top": {
    "multiple_only_need": 9.1,
    "deleverage_only_need_1_minus_L": 1.12,
    "cost_only_implied_aisc": 15.6,
    "dilution_only_need_D": 1.26,
    "two_factor_grid_examples": [
      {"multiple_up": 1.20, "metal_down": -0.15, "hits_top": true},
      {"deleverage": -0.10, "multiple_up": 1.15, "hits_top": true}
    ]
  },
  "event_study": {
    "bottom_events": [
      {
        "date": "2026-01-02",
        "ratio": 1.13,
        "aisc": 29.1,
        "net_debt_to_ev": 0.27,
        "ev_to_ebitda": 5.8,
        "shares_yoy": 0.14,
        "dominant_driver": "multiple_compression"
      }
    ]
  },
  "summary": "比率處於歷史底部，主要驅動為倍數壓縮...",
  "notes": [
    "AISC 使用 hybrid 方法回算，部分公司為 proxy 值",
    "建議交叉驗證：COT 持倉、ETF 流量、美元/實質利率"
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前比率與歷史分位數
- [ ] 四大基本面因子（AISC、槓桿、倍數、稀釋）
- [ ] 權重加總後的組合因子
- [ ] 門檻反推結果（單因子 + 雙因子組合）
- [ ] 歷史底部事件的因子驅動排名
- [ ] 結果輸出為指定格式（JSON 或 Markdown）
- [ ] 數據來源與方法標註（aisc_method 等）
- [ ] 風險提示與後續研究建議
- [ ] 視覺化儀表板（PNG 格式，檔名含日期）
</success_criteria>
