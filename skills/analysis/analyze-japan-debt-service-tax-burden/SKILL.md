---
name: analyze-japan-debt-service-tax-burden
description: 以日本公債殖利率變化為觸發，量化「政府利息支出 / 稅收」負擔（含情境壓力測試），並判斷是否進入債務利息螺旋風險區。
---

# 分析日本債務利息負擔 Skill

以公開數據量化日本「利息吃掉稅收」的敘事，提供可驗證的現況核對、敏感度分析與風險分級。

<essential_principles>

<principle name="interest_tax_ratio">
**核心指標：利息/稅收比**

`interest_tax_ratio = interest_payments / tax_revenue`

這是影片敘事「利息吃掉 1/3 稅收」的可核驗版本。不同口徑（國稅 vs 一般會計稅收 vs 總收入）會產生不同數值，必須明示口徑選擇。

**口徑對照（FY2025）**：
| 口徑 | 計算 | 比例 |
|------|------|------|
| 純利息/稅收 | 10.5兆/70兆 | **15.0%** |
| 國債費/稅收 | 28.2兆/70兆 | **40.3%** |

**注意**：媒體敘事「利息吃掉 1/3」通常誤用國債費（含本金）口徑。
</principle>

<principle name="implied_avg_rate">
**隱含平均利率**

`implied_avg_rate = interest_payments / debt_stock`

衡量存量債務的平均融資成本。對比當前市場利率可評估再融資壓力。

**FY2025**：10.5兆 / 1,324兆 = **0.79%** vs 當前 10Y 殖利率 **2.0%+**
→ 差距反映大量存量債務在低利率時期發行，未來再融資將推高利息負擔。
</principle>

<principle name="debt_in_us_terms">
**「in US terms」換算邏輯**

媒體常用「美國等效規模」表達日本債務以增強震撼效果。

**公式**（動態計算）：
```
debt_to_gdp = japan_debt_stock / japan_gdp
debt_in_us_terms = us_gdp × debt_to_gdp
```

**數據來源**：GDP 從 FRED 實時抓取，非硬編碼。

**範例**：$30.6T × 250% = **$76.5T** ≈ $70T（媒體口語化）

**用途**：解釋影片/新聞中「$70T」數字的來源，用於跨國比較時統一規模感知。
</principle>

<principle name="yield_sensitivity">
**殖利率敏感度映射**

把殖利率變動映射到利息支出增加：
```
additional_interest ≈ debt_stock × pass_through × delta_yield
```

其中 `pass_through` 是年度再定價/再融資比例（約 15%），`delta_yield` 以小數表示（200bp = 0.02）。
</principle>

<principle name="risk_bands">
**風險分級（Traffic Light）**

| 區間  | interest_tax_ratio | 含義                |
|-------|--------------------|---------------------|
| 🟢 綠 | < 0.25             | 財政彈性充足        |
| 🟡 黃 | 0.25–0.40          | 財政彈性開始下降    |
| 🟠 橘 | 0.40–0.55          | 政策空間明顯受限    |
| 🔴 紅 | > 0.55             | 接近「2/3」敘事區域 |
</principle>

<principle name="data_transparency">
**口徑透明原則**

所有輸出必須標示：
- 稅收口徑（national_tax / general_account_tax / total_revenue）
- 利息口徑（interest_only / debt_service）
- 資料年度與滯後（lag）
- 再定價假設（pass_through）
</principle>

</essential_principles>

<objective>
量化日本「利息吃掉稅收」敘事，並提供：
1. **現況核對**：當前 interest/tax ratio 與殖利率分位數
2. **壓力測試**：不同利率衝擊情境下的未來負擔
3. **風險分級**：可決策的 Traffic Light 評估
4. **外溢通道**（選用）：日本對美資產規模與潛在影響
</objective>

<quick_start>

**最快的方式：執行快速檢查**

```bash
cd skills/analyze-japan-debt-service-tax-burden
pip install pandas numpy requests matplotlib  # 首次使用
python scripts/japan_debt_analyzer.py --quick
```

輸出範例：
```json
{
  "yield_stats": {"tenor": "10Y", "latest": 1.23, "percentile": 0.97},
  "fiscal": {"interest_tax_ratio": 0.15, "risk_band": "green"},
  "headline": "利息支出佔稅收 15.0%，處於🟢 GREEN 區",
  "data_sources": {"jgb_10y": "FRED/IRLTLT01JPM156N", "fiscal": "config/FY2025"}
}
```

**完整分析（含實時數據刷新）**：
```bash
python scripts/japan_debt_analyzer.py --full --refresh
```

**生成視覺化 Dashboard**：
```bash
python scripts/generate_charts.py --full --output-dir ../../output
```

輸出：`output/japan_debt_dashboard_YYYYMMDD.png`

Dashboard 包含：
- Interest/Tax Ratio 風險儀表盤
- 殖利率分位數指標
- 財政數據摘要
- 壓力測試情境比較圖

**生成債務螺旋模擬圖表**：
```bash
# 完整多情境螺旋模擬
python scripts/generate_spiral_chart.py --all --output-dir ../../output

# 單一壓力情境（如 +200bp）
python scripts/generate_spiral_chart.py --stress 200 --output-dir ../../output

# 自定義模擬年數
python scripts/generate_spiral_chart.py --years 15 --output-dir ../../output
```

輸出：`output/japan_debt_spiral_YYYY-MM-DD.png`

螺旋模擬包含：
- 多情境 Interest/Tax Ratio 10年演變曲線
- 風險區間背景（綠/黃/橙/紅）
- 利息支出分解堆疊圖
- 各情境最終風險評估

**生成歷史趨勢分析圖表**（NEW!）：
```bash
# 完整歷史趨勢分析（2015-2025）
python scripts/generate_historical_trend.py --output-dir ../../output

# 自定義時間範圍
python scripts/generate_historical_trend.py --start-year 2018 --end-year 2025
```

輸出：`output/japan_debt_trend_YYYYMMDD.png`

歷史趨勢分析包含：
- Interest/Tax Ratio 11年完整走勢（2015-2025）
- 稅收、利息支出、債務存量趨勢
- 隱含平均利率演變
- 風險分級分布統計
- 階段性特徵分析（下降期/疫情期/反彈期）

**單獨測試數據抓取**：
```bash
python scripts/fetch_jgb_yields.py --tenor 10Y
python scripts/fetch_tic_holdings.py
```

</quick_start>

<intake>
您想要執行什麼操作？

1. **快速檢查** - 查看最新的利息/稅收比與殖利率狀態
2. **完整分析** - 執行完整的財政壓力測試與風險評估
3. **情境壓測** - 自定義利率衝擊情境進行壓力測試
4. **生成圖表** - 生成視覺化 Dashboard（PNG 圖檔）
5. **債務螺旋模擬** - 模擬多年累積效應，生成螺旋演變圖表
6. **歷史趨勢分析** - 分析 2015-2025 年完整歷史趨勢（NEW!）
7. **方法論學習** - 了解指標計算與風險分級邏輯

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                                  | Workflow                     | Description          |
|-------------------------------------------|------------------------------|----------------------|
| 1, "快速", "quick", "check"               | workflows/quick-check.md     | 快速狀態檢查         |
| 2, "完整", "full", "analyze"              | workflows/full-analysis.md   | 完整分析工作流       |
| 3, "壓測", "stress", "scenario"           | workflows/stress-test.md     | 情境壓力測試         |
| 4, "圖表", "chart", "dashboard"           | workflows/generate-chart.md  | 生成視覺化圖表       |
| 5, "螺旋", "spiral", "多年"               | workflows/spiral-simulate.md | 債務螺旋模擬         |
| 6, "歷史", "趨勢", "historical", "2015"   | workflows/historical-trend.md| 歷史趨勢分析（NEW!） |
| 7, "學習", "方法論", "why"                | references/methodology.md    | 方法論說明           |
| 提供參數 (如殖利率衝擊)                   | workflows/stress-test.md     | 使用參數執行壓測     |

**路由後，閱讀對應工作流程並完全遵循其步驟。**
</routing>

<input_schema>

<parameter name="country" required="true" default="JP">
**Type**: string
**Description**: 固定 JP / Japan（預留擴展多國）
</parameter>

<parameter name="analysis_window_days" required="false" default="504">
**Type**: int
**Description**: 殖利率與市場指標分析視窗（交易日數）
</parameter>

<parameter name="yield_tenors" required="false" default='["2Y","10Y","30Y"]'>
**Type**: array[string]
**Description**: JGB 觀察期限
</parameter>

<parameter name="tax_revenue_series" required="false" default="general_account_tax">
**Type**: string
**Options**: `national_tax` | `general_account_tax` | `total_revenue`
**Description**: 稅收口徑選擇
</parameter>

<parameter name="interest_payment_series" required="false" default="interest_only">
**Type**: string
**Options**: `interest_only` | `debt_service`
**Description**: 利息支出口徑（純利息 vs 含本金償還）
</parameter>

<parameter name="stress_scenarios" required="false">
**Type**: array[object]
**Description**: 壓力測試情境設定

每個情境包含：
- `name` (string): 情境名稱
- `delta_yield_bp` (int): 殖利率上升幅度（bp）
- `pass_through_year1` (float): 第一年再定價比例（預設 0.15）
- `pass_through_year2` (float): 第二年再定價比例（預設 0.15）
- `tax_shock` (float): 稅收衝擊（如 -0.05 表示下降 5%）
</parameter>

<parameter name="include_us_assets_channel" required="false" default="true">
**Type**: boolean
**Description**: 是否計算日本對美資產外溢通道
</parameter>

<parameter name="output_format" required="false" default="markdown">
**Type**: string
**Options**: `json` | `markdown`
</parameter>

</input_schema>

<output_schema>
參見 `templates/output-json.md` 的完整結構定義。

**摘要**：
```json
{
  "skill": "analyze_japan_debt_service_tax_burden",
  "as_of": "2026-01-20",
  "yield_stats": {
    "tenor": "10Y",
    "latest": 1.23,
    "zscore": 2.10,
    "percentile": 0.97,
    "interpretation": "近兩年分位數 97%，屬於偏極端區"
  },
  "fiscal": {
    "tax_revenue_jpy": 72000000000000,
    "interest_payments_jpy": 24000000000000,
    "debt_stock_jpy": 1200000000000000,
    "interest_tax_ratio": 0.333,
    "risk_band": "yellow",
    "definition": {...}
  },
  "stress_tests": [...],
  "spillover_channel": {...},
  "headline_takeaways": [...]
}
```
</output_schema>

<reference_index>
**參考文件** (`references/`)

| 文件                      | 內容                                       |
|---------------------------|--------------------------------------------|
| data-sources.md           | 資料來源與 API 端點（MOF、BOJ、FRED、TIC） |
| methodology.md            | 計算方法論與風險分級邏輯                   |
| japan-fiscal-structure.md | 日本財政結構與債務特徵                     |
</reference_index>

<workflows_index>
| Workflow            | Purpose                          |
|---------------------|----------------------------------|
| quick-check.md      | 快速狀態檢查（1分鐘內完成）      |
| full-analysis.md    | 完整分析工作流（含所有步驟）     |
| stress-test.md      | 自定義情境壓力測試               |
| generate-chart.md   | 生成視覺化 Dashboard             |
| spiral-simulate.md  | 債務螺旋多年模擬                 |
| historical-trend.md | 歷史趨勢分析（2015-2025）（NEW!）|
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script                      | Command                      | Purpose                        |
|-----------------------------|------------------------------|--------------------------------|
| japan_debt_analyzer.py      | `--quick`                    | 快速檢查                       |
| japan_debt_analyzer.py      | `--full`                     | 完整分析                       |
| japan_debt_analyzer.py      | `--stress BP`                | 壓力測試                       |
| japan_debt_analyzer.py      | `--refresh`                  | 強制刷新數據                   |
| generate_charts.py          | `--full --output-dir DIR`    | 生成視覺化 Dashboard           |
| generate_charts.py          | `--quick`                    | 快速模式圖表                   |
| generate_charts.py          | `--data-file FILE`           | 從 JSON 載入數據               |
| generate_spiral_chart.py    | `--all --output-dir DIR`     | 完整債務螺旋模擬 Dashboard     |
| generate_spiral_chart.py    | `--stress BP`                | 單一壓力情境螺旋圖             |
| generate_spiral_chart.py    | `--years N`                  | 自定義模擬年數（預設 10）      |
| generate_historical_trend.py| `--output-dir DIR`           | 歷史趨勢分析（2015-2025）（NEW!）|
| generate_historical_trend.py| `--start-year Y --end-year Y`| 自定義時間範圍分析             |
| fetch_jgb_yields.py         | `--tenor 10Y`                | 抓取 JGB 殖利率 (FRED)         |
| fetch_tic_holdings.py       | `--refresh`                  | 抓取 TIC 美債持有數據          |
| data_manager.py             | `--fetch-all`                | 協調所有數據源抓取             |
</scripts_index>

<success_criteria>
Skill 成功執行時：

- [ ] 輸出當前 interest/tax ratio 與風險分級
- [ ] 殖利率分位數/Z-score 判斷是否極端
- [ ] 壓力測試結果含敏感度分析
- [ ] 明確標示資料口徑與滯後
- [ ] 若啟用，輸出外溢通道評估
- [ ] 可操作的 headline takeaways
</success_criteria>

<directory_structure>
```
analyze-japan-debt-service-tax-burden/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元資料
├── workflows/
│   ├── quick-check.md                 # 快速檢查工作流
│   ├── full-analysis.md               # 完整分析工作流
│   ├── stress-test.md                 # 壓力測試工作流
│   ├── generate-chart.md              # 圖表生成工作流
│   ├── spiral-simulate.md             # 債務螺旋模擬工作流
│   └── historical-trend.md            # 歷史趨勢分析工作流（NEW!）
├── references/
│   ├── data-sources.md                # 資料來源說明
│   ├── methodology.md                 # 方法論與公式
│   └── japan-fiscal-structure.md      # 日本財政結構
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── config/
│   └── fiscal_data.json               # 財政數據配置（含 2015-2025 完整數據）
├── scripts/
│   ├── japan_debt_analyzer.py         # 主分析腳本
│   ├── generate_charts.py             # 視覺化圖表生成
│   ├── generate_spiral_chart.py       # 債務螺旋模擬圖表
│   ├── generate_historical_trend.py   # 歷史趨勢分析圖表（NEW!）
│   ├── fetch_jgb_yields.py            # JGB 殖利率抓取 (FRED)
│   ├── fetch_tic_holdings.py          # TIC 美債持有抓取
│   └── data_manager.py                # 數據協調與緩存管理
├── data/
│   └── cache/                         # 自動緩存目錄（gitignore）
└── examples/
    └── sample-output.json             # 範例輸出
```
</directory_structure>
