---
name: detect-palladium-lead-silver-turns
description: 以鈀金的先行轉向作為確認條件，檢驗白銀短期漲跌是否獲得工業景氣與風險情緒的同步支持，並標記缺乏鈀金參與度的失敗走勢。
---

<essential_principles>

<principle name="cross_metal_confirmation">
**跨金屬確認核心**

「鈀金領先白銀」的假說需要可量化驗證：
- 以 cross-correlation 估計最佳領先滯後（lead-lag）
- 當銀出現拐點時，檢查鈀金是否在確認窗口內先行或同步出現同向拐點
- 未被確認的拐點視為「失敗推動」的候選

```
Lead-Lag = argmax(cross_correlation(pd_ret[t-k:t], ag_ret[t:t+k]))
Confirmed = pd_turn exists within [ag_turn.ts - window, ag_turn.ts + window]
```
</principle>

<principle name="turning_point_detection">
**拐點偵測三法**

| 方法           | 原理                          | 適用場景       |
|----------------|-------------------------------|----------------|
| `pivot`        | 左右 N 根K棒內的局部極值      | 結構明確的趨勢 |
| `peaks`        | scipy find_peaks + prominence | 自動化密度控制 |
| `slope_change` | 趨勢斜率由正轉負或反之        | 平滑趨勢追蹤   |

建議從 `pivot` 開始，左右各 3-5 根K棒，再依需求調整。
</principle>

<principle name="participation_judgment">
**參與度判定**

鈀金是否「參與」銀的走勢，有多種衡量方式：

| 指標               | 定義               | 門檻建議          |
|--------------------|--------------------|-------------------|
| `returns_corr`     | 報酬率滾動相關係數 | > 0.5             |
| `direction_agree`  | 同向漲跌的比例     | > 60%             |
| `vol_expansion`    | 兩者波動同步擴張   | σ_pd / σ_ag > 0.8 |
| `breakout_confirm` | 銀突破時鈀金也突破 | 同向突破          |

未達門檻時，銀的動作可能是「流動性噪音」而非趨勢確認。
</principle>

<principle name="failure_move_detection">
**失敗走勢判定**

將「無鈀金參與的銀動作」落地為可回測的規則：

| 規則                         | 定義                            | 後果               |
|------------------------------|---------------------------------|--------------------|
| `no_confirm_then_revert`     | 無確認 + 銀在 N 根K內回撤過起點 | 標記為 failed_move |
| `no_confirm_then_break_fail` | 無確認 + 銀突破後回落跌破突破點 | 假突破             |

歷史統計：未確認事件的失敗率 vs 已確認事件的成功率。
</principle>

</essential_principles>

<objective>
偵測「鈀金領先、白銀跟隨」的跨金屬拐點：

1. **數據取得**：白銀與鈀金的 OHLCV（yfinance: SI=F, PA=F）
2. **拐點偵測**：識別兩者的局部高低點（pivot / peaks / slope_change）
3. **領先滯後估計**：cross-correlation 找最佳 lag
4. **跨金屬確認**：銀的拐點是否在窗口內被鈀金同向拐點確認
5. **失敗走勢判定**：未確認的銀拐點是否符合失敗規則

輸出：確認率、失敗率、每個事件的詳細判定、風控建議。
</objective>

<quick_start>

**最快的方式：偵測白銀近期拐點是否被鈀金確認**

```bash
cd skills/detect-palladium-lead-silver-turns
pip install pandas numpy yfinance scipy statsmodels  # 首次使用
python scripts/palladium_lead_silver.py --silver SI=F --palladium PA=F --quick
```

輸出範例：
```json
{
  "symbol_pair": {"silver": "SI=F", "palladium": "PA=F"},
  "as_of": "2026-01-14",
  "timeframe": "1h",
  "estimated_pd_leads_by_bars": 6,
  "lead_lag_corr": 0.42,
  "confirmation_rate": 0.71,
  "unconfirmed_failure_rate": 0.64,
  "latest_event": {
    "ts": "2026-01-15T14:00:00Z",
    "turn": "top",
    "confirmed": false,
    "participation_ok": false,
    "failed_move": true
  }
}
```

**完整分析**：
```bash
python scripts/palladium_lead_silver.py --silver SI=F --palladium PA=F --timeframe 1h --lookback 1000 --output result.json
```

**生成 Bloomberg 風格視覺化圖表**（推薦）：
```bash
pip install matplotlib yfinance  # 首次使用
python scripts/plot_bloomberg_style.py --input result.json --output output/palladium_silver_2026-01-26.png
```

圖表特色：
- **Bloomberg 專業配色**：深色背景、橙紅色白銀線、橙黃色鈀金線
- **背景色帶標記**：綠色背景 = 已確認拐點區域，紅色背景 = 未確認拐點區域（不擋住走勢線）
- **最新事件標註**：醒目標示最新拐點的確認狀態與價格
- **Pd/Ag 價格比率圖**：顯示鈀金對白銀的相對價格變化，含 20 期均線
- **滾動確認率**：動態顯示確認邏輯的有效性趨勢
- **統計面板**：確認率、失敗率、總拐點數等關鍵指標
- **行情解讀**：當前狀態評估與可操作建議

**傳統三合一圖表**（技術分析向）：
```bash
python scripts/plot_palladium_silver.py --silver SI=F --palladium PA=F --output output/
```

包含：
- 銀/鈀價格疊加與拐點標記
- 確認/未確認事件分布
- 滾動相關係數時間序列
- 失敗走勢統計

</quick_start>

<intake>
需要進行什麼操作？

1. **快速偵測** - 檢查最近白銀拐點是否被鈀金確認
2. **歷史回測** - 回溯分析跨金屬確認的有效性
3. **持續監控** - 設定警報當出現新拐點時通知
4. **參數調校** - 找出最佳的確認窗口與參與度門檻
5. **方法論學習** - 了解跨金屬領先滯後的理論基礎

**請選擇或直接提供分析參數開始。**
</intake>

<routing>
| Response                           | Action                                                 |
|------------------------------------|--------------------------------------------------------|
| 1, "快速", "quick", "check"        | 執行 `python scripts/palladium_lead_silver.py --quick` |
| 2, "回測", "backtest", "history"   | 閱讀 `workflows/backtest.md` 並執行                    |
| 3, "監控", "monitor", "alert"      | 閱讀 `workflows/monitor.md` 並執行                     |
| 4, "調校", "optimize", "tune"      | 閱讀 `workflows/detect.md` 的參數調校部分              |
| 5, "學習", "方法論", "why"         | 閱讀 `references/methodology.md`                       |
| 提供參數（如 timeframe, lookback） | 閱讀 `workflows/detect.md` 並使用參數執行              |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
detect-palladium-lead-silver-turns/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── detect.md                      # 單次偵測工作流
│   ├── backtest.md                    # 歷史回測工作流
│   └── monitor.md                     # 持續監控工作流
├── references/
│   ├── methodology.md                 # 跨金屬領先滯後方法論
│   ├── input-schema.md                # 完整輸入參數定義
│   └── data-sources.md                # 資料來源說明
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── palladium_lead_silver.py       # 主偵測腳本
│   ├── plot_bloomberg_style.py        # Bloomberg 風格視覺化（推薦）
│   └── plot_palladium_silver.py       # 傳統三合一圖表
└── examples/
    └── silver-palladium-2024.json     # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 跨金屬領先滯後原理
- 拐點偵測三法詳解
- 參與度與確認邏輯
- 失敗走勢的市場含義

**資料來源**: references/data-sources.md
- Yahoo Finance 期貨代碼
- 宏觀濾鏡數據來源
- 數據頻率與對齊

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow    | Purpose  | 使用時機           |
|-------------|----------|--------------------|
| detect.md   | 單次偵測 | 檢查特定時間範圍   |
| backtest.md | 歷史回測 | 驗證確認邏輯有效性 |
| monitor.md  | 持續監控 | 日常追蹤或警報     |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script                   | Command                                          | Purpose          |
|--------------------------|--------------------------------------------------|------------------|
| palladium_lead_silver.py | `--silver SI=F --palladium PA=F --quick`         | 快速檢查當前狀態 |
| palladium_lead_silver.py | `--silver SI=F --palladium PA=F --lookback 1000` | 完整歷史分析     |
| plot_bloomberg_style.py  | `--input result.json --output output/chart.png`  | Bloomberg 風格圖表（推薦） |
| plot_palladium_silver.py | `--silver SI=F --palladium PA=F --output dir/`   | 傳統三合一圖表   |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數             | 類型   | 預設值     | 說明         |
|------------------|--------|------------|--------------|
| silver_symbol    | string | (required) | 白銀標的代碼 |
| palladium_symbol | string | (required) | 鈀金標的代碼 |
| timeframe        | string | 1h         | 分析時間尺度 |
| lookback_bars    | int    | 1000       | 回溯K棒數    |

**拐點偵測參數**

| 參數                | 類型   | 預設值 | 說明                |
|---------------------|--------|--------|---------------------|
| turn_method         | string | pivot  | 拐點偵測方法        |
| pivot_left          | int    | 3      | pivot 左側確認K數   |
| pivot_right         | int    | 3      | pivot 右側確認K數   |
| confirm_window_bars | int    | 6      | 跨金屬確認窗口      |
| lead_lag_max_bars   | int    | 24     | 領先滯後最大滯後K數 |

**參與度參數**

| 參數                    | 類型   | 預設值                 | 說明           |
|-------------------------|--------|------------------------|----------------|
| participation_metric    | string | direction_agree        | 參與度衡量方式 |
| participation_threshold | float  | 0.6                    | 參與度門檻     |
| failure_rule            | string | no_confirm_then_revert | 失敗走勢規則   |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "detect-palladium-lead-silver-turns",
  "symbol_pair": {"silver": "SI=F", "palladium": "PA=F"},
  "as_of": "2026-01-14",
  "timeframe": "1h",
  "lookback_bars": 1200,
  "summary": {
    "estimated_pd_leads_by_bars": 6,
    "lead_lag_corr": 0.42,
    "confirmation_rate": 0.71,
    "unconfirmed_failure_rate": 0.64,
    "total_ag_turns": 24,
    "confirmed_turns": 17,
    "failed_moves": 5
  },
  "events": [
    {
      "ts": "2026-01-08T10:00:00Z",
      "turn": "bottom",
      "confirmed": true,
      "confirmation_lag_bars": -3,
      "participation_ok": true,
      "failed_move": false
    }
  ],
  "interpretation": {
    "regime_assessment": "...",
    "tactics": ["...", "..."]
  }
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 鈀金對白銀的最佳領先滯後估計（bars）
- [ ] 領先滯後的相關係數
- [ ] 白銀拐點被鈀金確認的確認率
- [ ] 未確認事件的失敗走勢比例
- [ ] 每個白銀拐點的詳細判定（confirmed, participation, failed）
- [ ] 行情解讀與戰術建議
- [ ] 時間序列資料（可選，用於視覺化）
- [ ] 視覺化圖表 PNG（可選，使用 plot_palladium_silver.py）
</success_criteria>
