---
name: analyze-high-unemployment-high-gdp-growth-fiscal-deficit-scenarios
description: 在「失業率走高／勞動市場轉弱」但「名目或實質 GDP 仍維持高位（或仍在成長）」的情境下，依據歷史關聯估算美國財政赤字占 GDP（Deficit/GDP）可能擴張的區間，並生成對長天期美債（長久期 UST）供給/利率風險的情境解讀。支援視覺化圖表輸出。
---

<essential_principles>

<principle name="labor_gdp_divergence">
**勞動-GDP 背離核心邏輯**

本技能聚焦於一個特殊的宏觀情境：**勞動市場明顯轉弱，但 GDP 仍處高位**。這種組合歷史上常伴隨：
- 財政赤字/GDP 的階躍式上升（自動穩定器 + 反週期支出）
- 長天期國債供給壓力增加
- 期限溢酬的潛在上升

關鍵洞察：「30 年歷史顯示，當 jobs 夠軟，赤字/GDP 會從 6–7% 跳到 12–17%」
</principle>

<principle name="slack_metric">
**勞動鬆緊度量 (Slack Metric)**

核心度量方式：
- **UJO** = Unemployed_Level / Job_Openings_Level（失業人數/職缺比）
  - 能捕捉「職缺掉很快、失業還沒上來」的早期轉弱階段
- **ΔUR** = Unemployment_Rate(t) - Unemployment_Rate(t-6M)（半年變化）
- **薩姆規則** = 3M_MA(UR) - min(UR over last 12M)（觸發式警報，≥0.5 為衰退警示）

這些指標用於定義「勞動轉弱事件」的觸發與分級（輕/中/重）。
</principle>

<principle name="elasticity_coefficients">
**彈性係數 (Elasticity Coefficients)**

基於 2000-2025 年歷史回歸分析的核心經濟彈性：

| 係數        | 數值      | 意涵                             |
|-------------|-----------|----------------------------------|
| **β_UR**    | **0.59**  | 失業率每↑1ppt → 赤字/GDP↑0.59ppt |
| **β_UJO**   | **0.69**  | UJO每↑1 → 赤字/GDP↑0.69ppt       |
| **β_JOLTS** | **-0.07** | 職缺每↑1M → 赤字/GDP↓0.07ppt     |
| **Lag**     | **4Q**    | 勞動指標領先赤字約4季            |

這些彈性係數用於：
- 情境投影的定量推演
- 驗證事件分組區間法的結果一致性
- 敏感度分析

詳細方法論見 `references/methodology.md`。
</principle>

<principle name="high_gdp_condition">
**高 GDP 條件定義**

「高 GDP」量化為：
- **GDP_level_percentile**：GDP 水平在回看期間的分位數（例如 > 70% 視為高位）
- **GDP_growth_regime**：成長仍為正、或僅小幅趨緩
- （進階）產出缺口/趨勢偏離

只有同時滿足「勞動轉弱」+「高 GDP」條件的樣本，才納入情境分析。
</principle>

<principle name="three_models">
**三種分析模型**

| 模型                    | 用途           | 輸出形式                           |
|-------------------------|----------------|------------------------------------|
| **event_study_banding** | 事件分組區間法 | 「12–17%」範圍型敘事，歷史事件清單 |
| **quantile_mapping**    | 分位數映射     | 「現在落在歷史哪個角落」的條件分布 |
| **robust_regression**   | 穩健迴歸推演   | 連續型情境路徑與區間               |

預設使用 `event_study_banding`，最貼近「歷史顯示…」的敘事方式。
</principle>

<principle name="visualization">
**三軸視覺化圖表**

本技能支援生成三軸圖表：
- **左軸**：失業人數（紅色）、職缺數（藍色）— 千人
- **右軸**：財政赤字/GDP（綠色）— 百分比
- **標註**：歷史 crossover 事件（失業 > 職缺）及對應的赤字跳升幅度
- **情境投影**：虛線顯示未來可能的路徑（mild/moderate/severe）

圖表基於 FRED 公開數據繪製，便於追蹤勞動-財政關聯的歷史演變。
</principle>

<principle name="data_access">
**資料取得方式**

本技能使用**無需 API key** 的公開資料來源：
- **FRED CSV**: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}`
  - 勞動：UNRATE, UNEMPLOY, JTSJOL, ICSA
  - 宏觀：GDP, GDPC1
  - 財政：FYFSGDA188S（聯邦盈餘/赤字占 GDP）
- **BEA**: 備用的 GDP/財政數據源

腳本位於 `scripts/` 目錄，可直接執行。
</principle>

</essential_principles>

<objective>
實作「高失業 + 高 GDP」情境下的財政赤字推估：

1. **建構勞動鬆緊指標**：從 FRED 數據計算 UJO、薩姆規則 等
2. **定義背離事件**：識別「勞動轉弱 + GDP 高位」的歷史樣本
3. **推估赤字區間**：使用三種模型估算 Deficit/GDP 的可能跳升區間
4. **生成情境解讀**：產出對長天期 UST 的供給/利率風險解讀
5. **視覺化輸出**：生成三軸圖表與情境投影

輸出：診斷資訊、赤字區間投影、歷史事件樣本、UST 風險解讀、視覺化圖表。
</objective>

<quick_start>

**最快的方式：執行預設情境分析**

```bash
cd skills/analyze-high-unemployment-high-gdp-growth-fiscal-deficit-scenarios
pip install pandas numpy requests matplotlib  # 首次使用
python scripts/analyzer.py --quick
```

**生成視覺化圖表（推薦）**：
```bash
python scripts/analyzer.py --visualize --scenario-type moderate
```

**或直接使用視覺化腳本**：
```bash
python scripts/visualizer.py --scenario moderate --years 25
```

輸出範例：
```json
{
  "skill": "analyze_high_unemployment_fiscal_deficit_scenarios",
  "as_of": "2026-01-21",
  "diagnostics": {
    "current_slack_percentile": 0.28,
    "high_gdp_condition": true,
    "triggered_labor_softening": false
  },
  "deficit_gdp_projection": {
    "baseline_deficit_gdp": 0.062,
    "conditional_range_next_8q": {
      "p25": 0.11, "p50": 0.135, "p75": 0.16
    },
    "n_episodes": 3
  }
}
```

**完整情境分析 + 圖表**：
```bash
python scripts/analyzer.py --lookback 30 --horizon 8 --model event_study_banding --visualize --scenario-type severe --output result.json --chart-output chart.png
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速診斷** - 查看目前的勞動/GDP 狀態與赤字風險判定
2. **完整情境分析** - 執行完整的歷史事件研究與赤字區間推估
3. **視覺化圖表** - 生成三軸圖表與情境投影
4. **自訂情境推演** - 輸入自訂的失業衝擊情境進行推演
5. **方法論學習** - 了解勞動-財政連結的邏輯與模型
6. **UST 風險解讀** - 生成長天期美債的供給/利率風險報告

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                     | Action                                     |
|------------------------------|--------------------------------------------|
| 1, "快速", "quick", "診斷"   | 執行 `python scripts/analyzer.py --quick`  |
| 2, "完整", "full", "情境"    | 閱讀 `workflows/analyze.md` 並執行         |
| 3, "視覺化", "圖表", "chart" | 閱讀 `workflows/visualize.md` 並執行       |
| 4, "自訂", "custom", "推演"  | 閱讀 `workflows/scenario.md` 並執行        |
| 5, "學習", "方法論", "why"   | 閱讀 `references/methodology.md`           |
| 6, "UST", "美債", "利率"     | 閱讀 `workflows/ust-risk.md` 並執行        |
| 提供參數 (如 lookback_years) | 閱讀 `workflows/analyze.md` 並使用參數執行 |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
analyze-high-unemployment-high-gdp-growth-fiscal-deficit-scenarios/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整情境分析工作流
│   ├── visualize.md                   # 視覺化圖表工作流
│   ├── scenario.md                    # 自訂情境推演工作流
│   └── ust-risk.md                    # UST 風險解讀工作流
├── references/
│   ├── data-sources.md                # FRED 系列代碼與資料來源
│   ├── methodology.md                 # 勞動-財政連結方法論
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── analyzer.py                    # 主分析腳本（含視覺化整合）
│   ├── visualizer.py                  # 視覺化專用腳本
│   └── fetch_data.py                  # 數據抓取工具
└── output/                            # 圖表輸出目錄
    └── (generated charts)
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 勞動-財政連結邏輯
- 三種分析模型詳解
- 事件分組與門檻定義

**資料來源**: references/data-sources.md
- FRED 系列代碼（勞動/GDP/財政）
- 數據頻率與對齊方法

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow     | Purpose      | 使用時機           |
|--------------|--------------|--------------------|
| analyze.md   | 完整情境分析 | 需要歷史事件研究時 |
| visualize.md | 視覺化圖表   | 需要生成圖表時     |
| scenario.md  | 自訂情境推演 | 輸入自訂失業衝擊時 |
| ust-risk.md  | UST 風險解讀 | 需要債市風險報告時 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script        | Command                                | Purpose            |
|---------------|----------------------------------------|--------------------|
| analyzer.py   | `--quick`                              | 快速診斷當前狀態   |
| analyzer.py   | `--lookback 30 --horizon 8`            | 完整情境分析       |
| analyzer.py   | `--visualize --scenario-type moderate` | 分析 + 視覺化圖表  |
| visualizer.py | `--scenario moderate --years 25`       | 單獨生成視覺化圖表 |
| visualizer.py | `--scenario severe --output chart.png` | 指定輸出路徑       |
| fetch_data.py | `--series UNRATE,JTSJOL,GDP`           | 抓取 FRED 資料     |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數             | 類型   | 預設值              | 說明       |
|------------------|--------|---------------------|------------|
| country          | string | US                  | 國家代碼   |
| lookback_years   | int    | 30                  | 回看年數   |
| frequency        | string | quarterly           | 資料頻率   |
| horizon_quarters | int    | 8                   | 推演季度數 |
| model            | string | event_study_banding | 分析模型   |
| output_format    | string | json                | 輸出格式   |

**勞動指標設定**

| 參數             | 類型   | 預設值                           | 說明          |
|------------------|--------|----------------------------------|---------------|
| use_jolts        | bool   | true                             | 使用 JOLTS    |
| use_unemployment | bool   | true                             | 使用失業率    |
| use_sahm_rule    | bool   | true                             | 計算 薩姆規則 |
| slack_metric     | string | unemployed_to_job_openings_ratio | 鬆緊度量      |

**視覺化參數**

| 參數          | 類型   | 預設值   | 說明                            |
|---------------|--------|----------|---------------------------------|
| visualize     | bool   | false    | 是否生成視覺化圖表              |
| scenario_type | string | moderate | 情境類型 (mild/moderate/severe) |
| chart_output  | string | auto     | 圖表輸出路徑                    |
| no_show       | bool   | false    | 不顯示圖表（僅保存）            |

**情境假設**

| 參數               | 類型   | 預設值              | 說明         |
|--------------------|--------|---------------------|--------------|
| gdp_path           | string | high_gdp_sticky     | GDP 路徑假設 |
| unemployment_shock | object | {type, size, speed} | 失業衝擊設定 |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "analyze_high_unemployment_fiscal_deficit_scenarios",
  "inputs": {
    "country": "US",
    "lookback_years": 30,
    "slack_metric": "unemployed_to_job_openings_ratio",
    "model": "event_study_banding"
  },
  "diagnostics": {
    "current_slack_percentile": 0.28,
    "high_gdp_condition": true,
    "triggered_labor_softening": false
  },
  "elasticity_model": {
    "parameters": {
      "beta_ur": 0.59,
      "beta_ujo": 0.69,
      "beta_jolts": -0.07,
      "lag_quarters": 4
    },
    "interpretation": {
      "ur_effect": "每 1ppt 失業率上升 → 赤字/GDP 上升 0.59 ppt",
      "ujo_effect": "UJO 每上升 1 → 赤字/GDP 上升 0.69 ppt",
      "lag_effect": "勞動指標領先赤字約 4 季"
    },
    "conditional_means": {
      "deficit_when_loose": 5.6,
      "deficit_when_tight": 5.2
    }
  },
  "deficit_gdp_projection": {
    "baseline_deficit_gdp": 0.062,
    "conditional_range_next_8q": {
      "p25": 0.11, "p50": 0.135, "p75": 0.16, "min": 0.095, "max": 0.175
    },
    "n_episodes": 3,
    "episode_years": ["2001-2003", "2008-2010", "2020-2021"]
  },
  "interpretation": {
    "macro_story": "...",
    "ust_duration_implications": [...],
    "watchlist_switch_indicators": [...]
  },
  "visualization": {
    "chart_path": "output/fiscal_deficit_scenario_20260121.png",
    "scenario_type": "moderate",
    "projected_deficit_jump_bps": 600
  }
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

**數據分析**
- [ ] 當前勞動鬆緊狀態（分位數、是否觸發轉弱）
- [ ] 高 GDP 條件判定結果
- [ ] Deficit/GDP 的條件分布區間（p25/p50/p75）
- [ ] 歷史樣本事件清單（年份、指標數值）
- [ ] UST 供給壓力通道解讀
- [ ] 風險偏好通道解讀（避險 vs 供給兩股力量）
- [ ] 監控切換指標清單
- [ ] 診斷資訊（當前指標數值）

**視覺化（若啟用）**
- [ ] 三軸圖表（職缺/失業/赤字GDP）
- [ ] 歷史 crossover 事件標註
- [ ] 情境投影虛線（mild/moderate/severe）
- [ ] 衰退期灰色陰影
- [ ] JSON 摘要檔案
</success_criteria>
