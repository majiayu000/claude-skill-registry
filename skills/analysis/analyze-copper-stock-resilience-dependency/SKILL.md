---
name: analyze-copper-stock-resilience-dependency
description: 用跨資產訊號（全球股市韌性 + 中國利率環境）評估銅價能否突破關卡或進入「回補/回踩」到支撐的機率與路徑。
---

<essential_principles>

<principle name="cross_asset_dependency">
**跨資產依賴核心邏輯**

銅價的關卡突破與回補，並非單純由銅本身決定，而是高度依賴股市韌性：

```
銅價走勢 = f(技術面關卡狀態) × f(股市韌性) × f(中國利率環境)
```

關鍵洞察：
- **股市韌性高**時：銅突破關卡後「續航」機率更高
- **股市韌性低**時：銅更容易出現「back-and-fill」回補到支撐區
- **中國10Y殖利率**：作為風險壓力/政策寬鬆的雙面訊號
</principle>

<principle name="round_levels">
**心理關卡與趨勢狀態**

銅價的重要心理整數位（如 10,000 / 13,000 USD/ton）是判斷突破與回補的關鍵：

| 狀態      | 條件                       | 含義     |
|-----------|----------------------------|----------|
| **up**    | close > SMA(60) 且斜率為正 | 上升趨勢 |
| **down**  | close < SMA(60) 且斜率為負 | 下降趨勢 |
| **range** | 其他                       | 區間整理 |

關卡判定：
- `near_resistance`: 接近上方關卡
- `near_support`: 接近下方支撐
</principle>

<principle name="equity_resilience_score">
**股市韌性評分（0-100）**

將「股市韌性」量化為可計算的分數：

| 因子       | 權重 | 計算方式                           |
|------------|------|------------------------------------|
| 12個月動能 | 40%  | 12m 報酬分位數（vs 歷史）          |
| 均線位置   | 40%  | 是否站上 12 月均線（是=100，否=0） |
| 近期回撤   | 20%  | 近 3m 回撤越小越好（反向計分）     |

評分解讀：
- **70-100**：高韌性，銅突破關卡後續航機率較高
- **30-70**：中性，需觀察其他因子
- **0-30**：低韌性，回補風險顯著上升
</principle>

<principle name="rolling_beta">
**滾動迴歸：量化依賴強度**

計算銅價對股市與中國殖利率的滾動貝塔係數：

```
Δcopper ~ β1 × Δequity + β2 × Δchina_yield + ε
```

- **β1（股市貝塔）越大越正**：銅越像風險資產，越依賴股市
- **β1 高分位**：市場正在把銅當風險資產一起交易
- **β1 < 0（負相關）**：銅與股市脫鉤，展現獨立邏輯（避險/供給/能源轉型敘事）
- **β2（殖利率貝塔）**：正 = 殖利率上升利好銅（通膨敘事），負 = 反之
</principle>

<principle name="data_access">
**資料取得方式**

本 skill 使用以下公開數據來源：

| 數據          | 代碼/來源                                                                         | 取得方式              |
|---------------|-----------------------------------------------------------------------------------|----------------------|
| 銅期貨價格    | COMEX Copper (HG=F)                                                               | Yahoo Finance        |
| 全球股市市值  | VT (Vanguard Total World Stock ETF)                                               | Yahoo Finance        |
| 中國10Y殖利率 | [MacroMicro](https://en.macromicro.me/charts/133362/China-10Year-Government-Bond-Yield) | Selenium + Highcharts |

**單位換算**：
- HG=F 為 $/lb，自動乘以 2204.62262 轉換為 $/ton
- VT ETF 價格乘以係數轉換為全球市值估計（兆美元）
- 中國10Y 為百分比（%）
</principle>

</essential_principles>

<objective>
實作銅價股市韌性依賴分析：

1. **資料擷取**：抓取銅價、全球股市、中國10Y殖利率
2. **趨勢與關卡判定**：計算 SMA、趨勢狀態、接近哪個關卡
3. **股市韌性評分**：計算 equity_resilience_score
4. **依賴關係量化**：滾動迴歸計算 β 係數
5. **回補機率估計**：歷史統計回補頻率（高韌性 vs 低韌性）
6. **情境判讀**：輸出當前是「續航」還是「回補」情境

輸出：當前狀態、依賴強度、回補機率、可執行警報旗標。
</objective>

<quick_start>

**最快的方式：執行預設分析**

```bash
cd skills/analyze-copper-stock-resilience-dependency
pip install pandas numpy yfinance scipy statsmodels matplotlib  # 首次使用
python scripts/copper_stock_analyzer.py --quick
```

輸出範例：
```json
{
  "as_of": "2026-01-22",
  "latest_state": {
    "copper_price_usd_per_ton": 12727,
    "copper_trend": "up",
    "equity_resilience_score": 83,
    "rolling_beta_equity_24m": -0.80
  },
  "diagnosis": {
    "narrative": "銅價上升趨勢中，接近 13,000 關卡，股市韌性高檔。"
  }
}
```

**生成 Bloomberg 風格圖表**：
```bash
python scripts/visualize.py \
  --start 2015-01-01 \
  -o output/copper_resilience_2026-01-22.png
```

圖表包含：
- 銅價月線 + SMA60（右軸，橙紅/黃色）
- 全球股市市值（左軸，橙色面積圖）
- 中國 10Y 殖利率（左軸，黃線）
- 關卡線（10,000 / 13,000）

**生成依賴度分析圖表**（三面板綜合圖）：
```bash
python scripts/plot_dependency_analysis.py \
  --start 2015-01-01 \
  -o ../../output/copper-dependency-analysis-2026-01-22.png
```

圖表包含三個面板：
1. **銅價面板**：銅價 + SMA60 + 趨勢背景色（綠=上升，紅=下降）+ 關卡線
2. **β係數面板**：滾動 β 時間序列 + ±1σ 區間 + 當前分位數 + 負值警示
3. **韌性面板**：股市韌性評分 + 高/低閾值線

**完整分析**：
```bash
python scripts/copper_stock_analyzer.py \
  --start 2015-01-01 \
  --end 2026-01-22 \
  --copper HG=F \
  --equity ACWI \
  --output result.json
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查** - 查看目前銅價、股市韌性、關卡狀態
2. **完整分析** - 分析時間區間內的依賴關係與回補機率
3. **視覺化圖表** - 生成銅價與依賴因子的視覺化圖表
4. **依賴度分析圖** - 生成三面板依賴度分析圖表（銅價+β係數+韌性）
5. **方法論學習** - 了解跨資產依賴模型的邏輯

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                     | Action                                                 |
|------------------------------|--------------------------------------------------------|
| 1, "快速", "quick", "check"  | 執行 `python scripts/copper_stock_analyzer.py --quick` |
| 2, "完整", "分析", "full"    | 閱讀 `workflows/analyze.md` 並執行                     |
| 3, "視覺化", "chart", "plot" | 閱讀 `workflows/visualize.md` 並執行                   |
| 4, "依賴度", "dependency"    | 執行 `python scripts/plot_dependency_analysis.py`      |
| 5, "學習", "方法論", "why"   | 閱讀 `references/methodology.md`                       |
| 提供參數 (如日期範圍)        | 閱讀 `workflows/analyze.md` 並使用參數執行             |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
analyze-copper-stock-resilience-dependency/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整分析工作流
│   ├── quick-check.md                 # 快速檢查工作流
│   └── visualize.md                   # 視覺化工作流
├── references/
│   ├── methodology.md                 # 跨資產依賴方法論
│   ├── data-sources.md                # 數據來源與爬蟲說明
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── copper_stock_analyzer.py       # 主分析腳本
│   ├── fetch_data.py                  # 數據抓取工具
│   ├── visualize.py                   # Bloomberg 風格圖表
│   └── plot_dependency_analysis.py    # 三面板依賴度分析圖表
├── data/
│   └── cache/                         # 數據快取目錄
└── examples/
    └── sample-output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 跨資產依賴概念與研究報告對照
- 股市韌性評分設計
- 滾動迴歸與貝塔解讀
- Back-and-fill 回補判定邏輯

**資料來源**: references/data-sources.md
- Yahoo Finance (yfinance) 使用說明
- 中國10Y殖利率爬蟲設計
- 數據頻率與對齊方法

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow       | Purpose        | 使用時機                   |
|----------------|----------------|----------------------------|
| analyze.md     | 完整分析       | 需要詳細依賴關係與回補分析 |
| quick-check.md | 快速檢查       | 只想看當前狀態             |
| visualize.md   | 生成視覺化圖表 | 需要圖表展示               |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script                      | Command                                    | Purpose                      |
|-----------------------------|--------------------------------------------|------------------------------|
| copper_stock_analyzer.py    | `--quick`                                  | 快速檢查當前狀態             |
| copper_stock_analyzer.py    | `--start DATE --end DATE`                  | 完整分析                     |
| fetch_data.py               | `--series HG=F,ACWI`                       | 抓取市場數據                 |
| visualize.py                | `--start 2015-01-01 -o output/chart.png`   | 生成 Bloomberg 風格圖表      |
| plot_dependency_analysis.py | `--start 2015-01-01 -o output/chart.png`   | 生成三面板依賴度分析圖表     |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數                   | 類型   | 預設值     | 說明          |
|------------------------|--------|------------|---------------|
| start_date             | string | 2020-01-01 | 分析起點      |
| end_date               | string | today      | 分析終點      |
| freq                   | string | 1mo        | 頻率（月）    |
| copper_series          | string | HG=F       | 銅價序列代碼  |
| equity_proxy_series    | string | ACWI       | 股市代理序列  |
| china_10y_yield_series | string | 爬取       | 中國10Y殖利率 |

**模型參數**

| 參數                  | 類型  | 預設值         | 說明               |
|-----------------------|-------|----------------|--------------------|
| ma_window             | int   | 60             | 移動平均視窗       |
| rolling_window        | int   | 24             | 滾動迴歸視窗（月） |
| round_levels          | list  | [10000, 13000] | 關卡位置           |
| backfill_max_drawdown | float | 0.25           | 回補幅度上限       |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "analyze-copper-stock-resilience-dependency",
  "as_of": "2026-01-22",
  "inputs": {
    "copper_series": "HG=F (converted to USD/ton)",
    "equity_proxy_series": "ACWI",
    "ma_window": 60,
    "rolling_window": 24
  },
  "latest_state": {
    "copper_price_usd_per_ton": 12727,
    "copper_sma_60": 9355,
    "copper_trend": "up",
    "near_resistance_levels": [13000],
    "near_support_levels": [],
    "equity_resilience_score": 91,
    "rolling_beta_equity_24m": -0.80,
    "rolling_beta_yield_24m": -0.05
  },
  "diagnosis": {
    "narrative": "銅價上升趨勢中，接近 13,000 關卡，股市韌性高檔。",
    "scenario": "續航機率較高",
    "dependency_status": "滾動 β 為負值 (-0.80)，銅與股市呈反向關係，脫離傳統風險資產模式"
  },
  "actionable_flags": [
    {
      "flag": "APPROACHING_RESISTANCE",
      "meaning": "接近重要阻力位，關注能否突破"
    },
    {
      "flag": "NEGATIVE_BETA_REGIME",
      "meaning": "銅與股市呈反向關係，脫離傳統風險資產模式"
    },
    {
      "flag": "LOW_BETA_ANOMALY",
      "meaning": "β 處於歷史極端低位，銅正展現獨立於股市的上漲邏輯"
    }
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前銅價與趨勢狀態（up/down/range）
- [ ] 接近的關卡位置（resistance/support）
- [ ] 股市韌性評分（0-100）
- [ ] 滾動貝塔係數（β_equity, β_yield）
- [ ] 回補機率估計（overall / high_resilience / low_resilience）
- [ ] 情境判讀敘述
- [ ] 可執行警報旗標
- [ ] 視覺化圖表（可選，輸出至 `output/` 目錄）
</success_criteria>
