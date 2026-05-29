---
name: forecast-sector-relative-return-from-yield-spread
description: 用美債殖利率曲線利差（如 2Y-10Y）建立「領先關係」，推估未來一段時間內成長股（Nasdaq 100）相對防禦股（Healthcare/XLV）的相對績效方向與幅度。
---

<essential_principles>

<principle name="lead_lag_definition">
**領先落後關係定義**

殖利率利差（Yield Spread）作為領先指標：

```
spread_t = short_yield_t - long_yield_t
         = US02Y_t - US10Y_t
```

**spread 越高**：短端相對更高（曲線更倒掛/更緊）
**spread 越低**（或從負回到 0、轉正）：曲線「回正/變陡」

此 spread 被認為領先反映：
- 經濟週期預期（倒掛 → 衰退預期）
- 風險偏好轉換（曲線變陡 → 風險偏好回升）
</principle>

<principle name="relative_return_definition">
**相對報酬定義**

相對強弱比率（Ratio）：

```
ratio_t = risk_asset_t / defensive_asset_t
        = QQQ_t / XLV_t
```

**ratio 上升**：成長股（Nasdaq）相對更強
**ratio 下降**：防禦股（Healthcare）相對更強（XLV 跑贏）

預測目標為「未來 H 個月的對數相對報酬」：

```
future_rel_return = log(ratio(t+H) / ratio(t))
```

正值 → Nasdaq 跑贏，負值 → XLV 跑贏
</principle>

<principle name="advance_alignment">
**「2 Years in Advance」的真正含義**

圖表的時間對齊邏輯：
- 把 spread 往前平移 lead_months 個月
- 目標是檢查：**spread(t) 是否能解釋 ratio(t + H)**

工程化寫法：
```
X = spread(t)
Y = future_rel_return(t, H) = log(ratio(t+H) / ratio(t))
```

然後做相關性/迴歸/交叉相關掃描來找「最佳領先期」。

**避免直接用 ratio 水平做迴歸**（有趨勢/非平穩問題），改用對數報酬。
</principle>

<principle name="validation_framework">
**領先關係驗證框架**

需回答三件事：

1. **是否真的存在穩定領先關係？**
   - 掃描多個 lead（6, 12, 18, 24, 30 個月）
   - 看哪個 lead 下 corr(spread, future_rel_return) 最穩、顯著
   - 跨子樣本驗證（前半段 vs 後半段）

2. **目前情境對應的預測方向**
   - 最近 spread 水準、變化率
   - 模型預測 E[future_rel_return]
   - 分位數區間（如 80% 信心區間）

3. **把預測翻譯成直覺語句**
   - 由 future_rel_return 轉回百分比：`exp(future_rel_return) - 1`
   - 「未來 24 個月 XLV 相對 QQQ 勝率 X%、中位數報酬 Y%」
</principle>

<principle name="data_alignment">
**數據對齊原則**

- **頻率選擇**：週頻（weekly）降低雜訊，建議 1wk
- **平滑視窗**：可選 13 週或 26 週移動平均
- **回測長度**：至少涵蓋 1-2 次完整景氣循環（如 2007-present）

殖利率來源：FRED（DGS2, DGS10）
資產價格來源：Yahoo Finance（QQQ, XLV）
</principle>

</essential_principles>

<objective>
實作「殖利率利差 → 板塊相對報酬」領先關係分析：

1. **數據整合**：取得殖利率（FRED）與資產價格（yfinance）
2. **利差計算**：計算 spread = short_yield - long_yield
3. **相對報酬計算**：計算 future_rel_return = log(ratio(t+H) / ratio(t))
4. **領先關係驗證**：掃描多個 lead 找最佳相關性與穩定性
5. **情境預測**：基於當前 spread 產出未來相對報酬預測區間
6. **輸出報告**：驗證結論、預測方向、風險提示

輸出：領先關係驗證、當前預測、區間估計、歷史類比、風險提示。
</objective>

<quick_start>

**最快的方式：執行預設情境分析**

```bash
cd skills/forecast-sector-relative-return-from-yield-spread
pip install pandas numpy yfinance matplotlib statsmodels requests  # 首次使用
python scripts/spread_forecaster.py --quick
```

**完整分析（含領先掃描與穩定性驗證）**

```bash
python scripts/spread_forecaster.py \
  --risk-ticker QQQ \
  --defensive-ticker XLV \
  --lead-months 24 \
  --lookback-years 12 \
  --output result.json
```

**生成視覺化圖表**

```bash
python scripts/spread_plotter.py --quick --output-dir ../../output
```

輸出範例：
```json
{
  "skill": "forecast_sector_relative_return_from_yield_spread",
  "signal_name": "US02Y_minus_US10Y_leads_QQQ_over_XLV",
  "lead_months": 24,
  "current_spread": -0.35,
  "model": {
    "type": "lagged_regression",
    "alpha": 0.02,
    "beta": -0.45,
    "corr_x_y": -0.32
  },
  "forecast": {
    "future_24m_relative_return_pct": -0.077,
    "interval_pct_80": [-0.22, 0.04],
    "interpretation": "若此關係維持，未來24個月QQQ相對XLV期望報酬為-7.7%，XLV較可能跑贏。"
  }
}
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速分析** - 使用預設參數（QQQ/XLV, 24 個月領先）計算當前預測
2. **完整分析** - 自訂參數進行領先關係驗證與情境預測
3. **領先掃描** - 掃描多個領先期（6-30 個月）找最佳相關性
4. **視覺化圖表** - 生成利差與相對報酬對齊圖
5. **穩定性驗證** - 檢查領先關係在不同子樣本的一致性
6. **方法論學習** - 了解領先關係邏輯與計算方式

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                       | Action                                                              |
|--------------------------------|---------------------------------------------------------------------|
| 1, "快速", "quick", "分析"     | 執行 `python scripts/spread_forecaster.py --quick`                  |
| 2, "完整", "full", "自訂"      | 閱讀 `workflows/analyze.md` 並執行                                  |
| 3, "掃描", "scan", "領先"      | 閱讀 `workflows/analyze.md` 並聚焦 lead_scan                        |
| 4, "圖表", "chart", "視覺化"   | 執行 `python scripts/spread_plotter.py --quick --output-dir output/`|
| 5, "驗證", "穩定", "stability" | 閱讀 `workflows/analyze.md` 並聚焦穩定性驗證                        |
| 6, "學習", "方法論", "why"     | 閱讀 `references/methodology.md`                                    |
| 提供參數 (如 ticker, lead)     | 閱讀 `workflows/analyze.md` 並使用參數執行                          |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
forecast-sector-relative-return-from-yield-spread/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整分析工作流
│   └── data-research.md               # 數據源研究與替代方案
├── references/
│   ├── methodology.md                 # 方法論與計算邏輯
│   ├── input-schema.md                # 完整輸入參數定義
│   └── data-sources.md                # 數據來源與獲取方式
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── spread_forecaster.py           # 主計算腳本
│   └── spread_plotter.py              # 視覺化圖表腳本
└── examples/
    └── sample-output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 領先落後關係定義
- 相對報酬計算
- 迴歸模型設定
- 區間估計方法
- 穩定性驗證

**資料來源**: references/data-sources.md
- 殖利率代理（FRED DGS2/DGS10）
- 資產價格代理（QQQ/XLV）
- 數據對齊原則

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow         | Purpose        | 使用時機                            |
|------------------|----------------|-------------------------------------|
| analyze.md       | 完整情境分析   | 需要自訂參數驗證領先關係與預測      |
| data-research.md | 數據源研究     | 了解如何獲取或替代殖利率/資產數據   |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script               | Command                                     | Purpose                          |
|----------------------|---------------------------------------------|----------------------------------|
| spread_forecaster.py | `--quick`                                   | 快速分析 QQQ/XLV, 24m lead       |
| spread_forecaster.py | `--lead-months 12 --lookback-years 15`     | 自訂領先期與回測長度             |
| spread_forecaster.py | `--lead-scan --scan-range 6,12,18,24,30`   | 領先期掃描                       |
| spread_plotter.py    | `--quick --output-dir ../../output`        | 快速生成基本版圖表               |
| spread_plotter.py    | `--comprehensive --start-date 2007-01-01`  | 完整版圖表（含領先對齊）         |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數              | 類型   | 預設值 | 說明                              |
|-------------------|--------|--------|-----------------------------------|
| risk_ticker       | string | QQQ    | 代表成長股的標的                  |
| defensive_ticker  | string | XLV    | 代表防禦股的標的                  |
| short_tenor       | string | 2Y     | 短端殖利率期限                    |
| long_tenor        | string | 10Y    | 長端殖利率期限                    |
| lead_months       | int    | 24     | 領先期（月）                      |
| lookback_years    | int    | 12     | 回測/估計歷史年數                 |

**進階參數**

| 參數                 | 類型   | 預設值            | 說明                           |
|----------------------|--------|-------------------|--------------------------------|
| freq                 | string | weekly            | 資料頻率（daily/weekly/monthly）|
| smoothing_window     | int    | 13                | 平滑視窗（週數）               |
| return_horizon_months| int    | 24                | 預測的相對報酬視窗             |
| model_type           | string | lagged_regression | 模型類型                       |
| confidence_level     | float  | 0.80              | 區間估計信心水準               |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "forecast_sector_relative_return_from_yield_spread",
  "inputs": {
    "risk_ticker": "QQQ",
    "defensive_ticker": "XLV",
    "lead_months": 24,
    "lookback_years": 12
  },
  "signal_name": "US02Y_minus_US10Y_leads_QQQ_over_XLV",
  "lead_months": 24,
  "current_spread": -0.35,
  "model": {
    "type": "lagged_regression",
    "alpha": 0.02,
    "beta": -0.45,
    "fit_quality": {
      "corr_x_y": -0.32,
      "r_squared": 0.10,
      "notes": "負 beta 意味歷史上倒掛/緊縮的 spread 對應未來 QQQ 相對走弱"
    }
  },
  "forecast": {
    "future_24m_relative_return_log": -0.08,
    "future_24m_relative_return_pct": -0.077,
    "interval_pct_80": [-0.22, 0.04],
    "interpretation": "若此關係維持，未來24個月QQQ相對XLV期望報酬為-7.7%，XLV較可能跑贏；但區間仍含正值，需搭配其他條件確認。"
  },
  "diagnostics": {
    "lead_scan": {
      "best_lead_months": 24,
      "correlation_by_lead": {"6": -0.15, "12": -0.22, "18": -0.28, "24": -0.32, "30": -0.30}
    },
    "stability_checks": {
      "first_half_corr": -0.30,
      "second_half_corr": -0.34,
      "consistency": "medium-high"
    }
  },
  "summary": "殖利率利差（2Y-10Y）對 QQQ/XLV 相對報酬有約 24 個月的領先性...",
  "notes": [
    "領先關係反映的是『歷史統計規律』，不保證未來成立。",
    "當前 spread 水準與變化率皆需考慮。",
    "建議搭配：景氣指標、估值分位、資金流向做交叉驗證。"
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前殖利率利差水準
- [ ] 領先關係相關性與迴歸係數
- [ ] 未來相對報酬預測（點估計與區間）
- [ ] 領先期掃描結果（若執行）
- [ ] 穩定性驗證（子樣本一致性）
- [ ] 結果輸出為指定格式（JSON 或 Markdown）
- [ ] 視覺化圖表輸出（若需要）
- [ ] 風險提示與後續研究建議
</success_criteria>
