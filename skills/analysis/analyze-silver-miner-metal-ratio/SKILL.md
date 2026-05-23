---
name: analyze-silver-miner-metal-ratio
description: 以「銀礦股價格 ÷ 白銀價格」的相對比率衡量礦業股板塊相對於金屬本體的估值區間（偏貴/偏便宜），並用歷史分位數與類比區間推導「底部/頂部」訊號與情境推演。
---

<essential_principles>

<principle name="ratio_definition">
**比率定義與意義**

礦業股/金屬比率（Miner-to-Metal Ratio）：

```
ratio_t = miner_price_t / metal_price_t
```

其中：
- **miner_price**：銀礦股代表（ETF 如 SIL/SILJ，或自建礦業股指數）
- **metal_price**：白銀價格（期貨 SI=F、現貨 XAGUSD、ETF SLV）

此比率衡量「礦業股相對於金屬本體」的估值水位：
- **比率高**：礦業股相對白銀偏貴（可能過度樂觀、槓桿溢價高）
- **比率低**：礦業股相對白銀偏便宜（可能被低估、或反映成本/股權稀釋風險）
</principle>

<principle name="quantile_interpretation">
**分位數解讀邏輯**

使用歷史分位數（Percentile Rank）判斷當前比率位置：

| 分位數區間 | 標籤           | 直覺                       |
|------------|----------------|----------------------------|
| ≤ 20%      | bottom (底部)  | 礦業股相對白銀歷史上很便宜 |
| 20-40%     | low (偏低)     | 礦業股相對估值偏低         |
| 40-60%     | neutral (中性) | 歷史中位區間               |
| 60-80%     | high (偏高)    | 礦業股相對估值偏高         |
| ≥ 80%      | top (頂部)     | 礦業股相對白銀歷史上很貴   |

**底部區間不等於白銀必漲**：可能是礦業股因成本/稀釋被合理定價。
</principle>

<principle name="divergence_signal">
**背離訊號的意義**

當出現「比率低 + 白銀高」的組合：

- **比率處於底部區**：礦業股相對白銀偏便宜
- **白銀處於高位**：金屬價格已在歷史高檔

此「背離」意味著：
1. 礦業股可能有追趕空間（均值回歸邏輯）
2. 或礦業股正確反映了結構性問題（成本、稀釋、地緣風險）

需結合基本面交叉驗證，而非盲目視為買入訊號。
</principle>

<principle name="scenario_math">
**情境推演計算**

目標：若比率要回到歷史頂部（或中位），需要什麼條件？

假設當前比率 = 1.14，目標比率（頂部門檻）= 2.45：

**情境 A：白銀不變，礦業股需漲多少？**
```
miner_multiplier = target_ratio / current_ratio
                 = 2.45 / 1.14 = 2.15x (需漲 115%)
```

**情境 B：礦業股不變，白銀需跌多少？**
```
metal_multiplier = current_ratio / target_ratio
                 = 1.14 / 2.45 = 0.46 (需跌 54%)
```

此推演提供「極端情境」的量化參考，非預測。
</principle>

<principle name="data_alignment">
**數據對齊原則**

- **頻率選擇**：長週期訊號建議使用週頻（1wk）或月頻（1mo）
- **平滑視窗**：可選 4 週或 3 個月移動平均降低雜訊
- **事件去重**：類比事件間隔需 ≥ min_separation_days（如 180 天）

本 skill 使用 yfinance 取得 ETF/期貨數據，預設週頻對齊。
</principle>

</essential_principles>

<objective>
實作「銀礦股價 / 銀價比率」分析模型：

1. **數據整合**：取得礦業股代理與白銀價格序列
2. **比率計算**：計算相對比率並可選平滑
3. **分位數判斷**：當前比率在歷史的位置
4. **類比事件**：歷史底部區間的事件識別
5. **前瞻驗證**：底部事件後白銀的 1/2/3 年表現
6. **情境推演**：礦業股需漲多少 / 白銀需跌多少才回到頂部

輸出：當前狀態、歷史類比、情境推演、風險提示。
</objective>

<quick_start>

**最快的方式：執行預設情境分析**

```bash
cd skills/analyze-silver-miner-metal-ratio
pip install pandas numpy yfinance matplotlib  # 首次使用
python scripts/ratio_analyzer.py --quick
```

**生成視覺化圖表（基本版）**

```bash
python scripts/ratio_plotter.py --quick --output-dir ../../output
```

**生成完整版圖表（含底部事件、前瞻報酬統計）**

```bash
python scripts/ratio_plotter.py --comprehensive --start-date 2010-01-01 --output-dir ../../output
```

圖表輸出路徑：
- 基本版：`output/sil_silver_ratio_YYYY-MM-DD.png`
- 完整版：`output/sil_silver_ratio_comprehensive_YYYY-MM-DD.png`

輸出範例：
```json
{
  "skill": "analyze_silver_miner_metal_ratio",
  "current": {
    "ratio": 1.14,
    "ratio_percentile": 18.7,
    "zone": "bottom",
    "bottom_threshold": 1.16,
    "top_threshold": 2.45
  },
  "history_analogs": {
    "bottom_event_dates": ["2010-08-06", "2016-01-29", "2020-03-20"],
    "forward_metal_returns": {
      "252": {"count": 3, "median": 0.42, "win_rate": 1.0}
    }
  },
  "scenarios": {
    "target": "return_to_top",
    "miner_multiplier_if_metal_flat": 2.15,
    "metal_drop_pct_if_miner_flat": 0.54
  }
}
```

**完整情境分析**：
```bash
python scripts/ratio_analyzer.py \
  --miner-proxy SIL \
  --metal-proxy SI=F \
  --start-date 2008-01-01 \
  --freq 1wk \
  --smoothing-window 4 \
  --bottom-quantile 0.20 \
  --top-quantile 0.80 \
  --output result.json
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速分析** - 使用預設參數（SIL / SI=F）計算當前比率狀態
2. **完整分析** - 自訂參數進行情境分析（可選擇礦業股/金屬代理、分位門檻）
3. **視覺化圖表** - 生成比率走勢圖，標記當前位置與分位數區間
4. **歷史驗證** - 查看底部區間事件的前瞻報酬統計
5. **情境推演** - 計算「回到頂部」需要的礦業股漲幅或白銀跌幅
6. **方法論學習** - 了解比率邏輯與分位數解讀

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                      | Action                                                              |
|-------------------------------|---------------------------------------------------------------------|
| 1, "快速", "quick", "分析"    | 執行 `python scripts/ratio_analyzer.py --quick`                     |
| 2, "完整", "full", "自訂"     | 閱讀 `workflows/analyze.md` 並執行                                  |
| 3, "圖表", "chart", "視覺化"  | 執行 `python scripts/ratio_plotter.py --quick --output-dir output/` |
| 4, "歷史", "驗證", "backtest" | 閱讀 `workflows/analyze.md` 並聚焦歷史類比                          |
| 5, "情境", "scenario", "推演" | 閱讀 `workflows/analyze.md` 並聚焦情境推演                          |
| 6, "學習", "方法論", "why"    | 閱讀 `references/methodology.md`                                    |
| 提供參數 (如礦業股/金屬代理)  | 閱讀 `workflows/analyze.md` 並使用參數執行                          |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
analyze-silver-miner-metal-ratio/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整情境分析工作流
│   └── data-research.md               # 數據源研究與替代方案
├── references/
│   ├── methodology.md                 # 方法論與計算邏輯
│   ├── input-schema.md                # 完整輸入參數定義
│   └── data-sources.md                # 數據來源與獲取方式
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── ratio_analyzer.py              # 主計算腳本
│   └── ratio_plotter.py               # 視覺化圖表腳本
└── examples/
    └── sample-output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 比率定義與直覺
- 分位數解讀邏輯
- 背離訊號的意義
- 情境推演數學
- 歷史驗證方法

**資料來源**: references/data-sources.md
- 礦業股代理（ETF/指數）
- 白銀價格代理
- 數據對齊原則

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow         | Purpose      | 使用時機                          |
|------------------|--------------|-----------------------------------|
| analyze.md       | 完整情境分析 | 需要自訂參數計算比率與情境        |
| data-research.md | 數據源研究   | 了解如何獲取或替代礦業股/金屬數據 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script            | Command                                                    | Purpose                                |
|-------------------|------------------------------------------------------------|----------------------------------------|
| ratio_analyzer.py | `--quick`                                                  | 快速分析 SIL/SI=F                      |
| ratio_analyzer.py | `--miner-proxy SILJ --freq 1mo`                            | 自訂礦業股與頻率                       |
| ratio_analyzer.py | `--scenario-target return_to_median`                       | 回到中位數情境                         |
| ratio_plotter.py  | `--quick --output-dir ../../output`                        | 快速生成基本版圖表                     |
| ratio_plotter.py  | `--comprehensive --start-date 2010-01-01 --output-dir ...` | 完整版圖表（含底部事件、前瞻報酬統計） |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數        | 類型   | 預設值  | 說明                          |
|-------------|--------|---------|-------------------------------|
| miner_proxy | string | SIL     | 銀礦股代表（ETF/指數代號）    |
| metal_proxy | string | SI=F    | 白銀價格代表（期貨/現貨/ETF） |
| start_date  | string | 10 年前 | 歷史回溯起點（YYYY-MM-DD）    |
| end_date    | string | today   | 分析終點                      |
| freq        | string | 1wk     | 取樣頻率（1d/1wk/1mo）        |

**進階參數**

| 參數                | 類型   | 預設值         | 說明                             |
|---------------------|--------|----------------|----------------------------------|
| smoothing_window    | int    | 4              | 比率平滑視窗（週數/月數）        |
| bottom_quantile     | float  | 0.20           | 底部估值區分位數門檻             |
| top_quantile        | float  | 0.80           | 頂部估值區分位數門檻             |
| min_separation_days | int    | 180            | 類比事件去重間隔                 |
| forward_horizons    | list   | [52, 104, 156] | 前瞻期（週數，對應 1/2/3 年）    |
| scenario_target     | string | return_to_top  | 情境目標（return_to_top/median） |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "analyze_silver_miner_metal_ratio",
  "inputs": {
    "miner_proxy": "SIL",
    "metal_proxy": "SI=F",
    "start_date": "2010-01-01",
    "freq": "1wk"
  },
  "current": {
    "ratio": 1.14,
    "ratio_percentile": 18.7,
    "zone": "bottom",
    "bottom_threshold": 1.16,
    "top_threshold": 2.45
  },
  "history_analogs": {
    "bottom_event_dates": ["2010-08-06", "2016-01-29", "2020-03-20"],
    "forward_metal_returns": {
      "252": {"count": 3, "median": 0.42, "mean": 0.39, "win_rate": 1.0, "worst": 0.18},
      "504": {"count": 3, "median": 0.71, "mean": 0.66, "win_rate": 1.0, "worst": 0.31}
    }
  },
  "scenarios": {
    "target": "return_to_top",
    "target_ratio": 2.45,
    "miner_multiplier_if_metal_flat": 2.15,
    "metal_multiplier_if_miner_flat": 0.46,
    "metal_drop_pct_if_miner_flat": 0.54
  },
  "summary": "銀礦股價 / 銀價比率落在歷史低分位，顯示礦業股相對白銀偏便宜...",
  "notes": [
    "比率訊號衡量的是『相對估值』，不是單邊價格保證。",
    "礦業股與金屬可能同漲，但礦業股也可能因成本上升、地緣/政策風險、增發稀釋而落後。",
    "建議搭配：礦業股獲利率(成本曲線)、白銀實質利率/美元、投機部位(COT)、ETF 流量等做交叉驗證。"
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前比率與歷史分位數
- [ ] 估值區間判定（bottom/low/neutral/high/top）
- [ ] 歷史底部事件列表與去重
- [ ] 底部事件後的前瞻報酬統計（平均/中位/勝率/最差）
- [ ] 情境推演（礦業股需漲多少 / 白銀需跌多少）
- [ ] 結果輸出為指定格式（JSON 或 Markdown）
- [ ] 視覺化圖表輸出（若需要）
- [ ] 風險提示與後續研究建議
</success_criteria>
