---
name: detect-atr-squeeze-regime
description: 以 14 日指數平滑 ATR 偵測市場是否從秩序型趨勢轉為波動主導的擠壓（squeeze）行情，並輸出對技術位、停損、交易持有期的可行性評估。
---

<essential_principles>

<principle name="atr_percent_normalization">
**ATR% 標準化核心**

傳統 ATR 是絕對值（價格單位），不同價位資產無法比較。
將 ATR 轉換為百分比（ATR / Close * 100）後：
- 可跨資產比較波動強度
- 能建立「常態基準」（3 年移動均值）
- 用「倍率」判定是否進入異常波動區

```
ATR% = (14-day EMA of True Range) / Close * 100
Ratio = Current ATR% / 3-year Rolling Mean ATR%
```
</principle>

<principle name="three_regime_classification">
**三行情分類**

| 行情                           | ATR% 條件   | Ratio 條件 | 市場特徵                           |
|--------------------------------|-------------|------------|------------------------------------|
| `orderly_market`               | 常態區間    | < 1.2      | 技術位有效、停損精準、趨勢追蹤可靠 |
| `elevated_volatility_trend`    | 偏高        | 1.2 - 2.0  | 技術位減效、需放寬停損、仍有方向性 |
| `volatility_dominated_squeeze` | >= 高波門檻 | >= 2.0     | 技術位失靈、停損頻被掃、反身性主導 |

**擠壓行情**的判定需要**同時**滿足：
1. ATR% >= `high_vol_threshold_pct`（預設 6%）
2. Ratio >= `spike_threshold_x`（預設 2.0）
</principle>

<principle name="reflexivity_mechanics">
**反身性機制解讀**

當進入 `volatility_dominated_squeeze` 行情：

**價格運動被「被迫流」主導**：
- 保證金調整 / 槓桿去化
- 期權 Delta/Gamma 避險
- 空頭回補
- 被動風險平價再平衡

**技術位可靠度下降**：
- 突破/跌破更常是流動性與風控觸發的結果
- 不代表基本面改變或趨勢確認

**停損脆弱性**：
- 同一口波動可掃過多層 stops
- 低時間尺度的 conviction trading「結構性受損」
- 宏觀看對也難撐：短期雜訊大到足以讓方向正確的部位先被洗掉
</principle>

<principle name="actionable_adjustments">
**可操作的調整建議**

當偵測到擠壓行情時：

| 調整項目   | 秩序市場    | 擠壓行情       |
|------------|-------------|----------------|
| 停損倍數   | 1.0-1.5 ATR | 2.0-3.0 ATR    |
| 倉位縮放   | 正常        | 降至 1/ATR%    |
| 時間框架   | 日內/短線   | 切換到較長週期 |
| 工具選擇   | 裸倉位      | 期權/價差結構  |
| 技術位信任 | 高          | 低（視為雜訊） |
</principle>

</essential_principles>

<objective>
偵測資產是否進入「波動主導的擠壓行情」：

1. **計算 ATR%**：14 日 EMA 平滑的真實波幅百分比
2. **建立基準**：3 年滾動均值作為「常態」參照
3. **判定行情**：比較當前值與基準的倍率
4. **輸出建議**：停損調整、倉位縮放、技術位信任度

輸出：行情判定、ATR% 數值、倍率、可操作的風控建議。
</objective>

<quick_start>

**最快的方式：偵測白銀（SI=F）**

```bash
cd skills/detect-atr-squeeze-regime
pip install pandas numpy yfinance pandas_ta  # 首次使用
python scripts/atr_squeeze.py --symbol SI=F --quick
```

輸出範例：
```json
{
  "symbol": "SI=F",
  "as_of": "2026-01-14",
  "regime": "volatility_dominated_squeeze",
  "atr_pct": 7.23,
  "atr_ratio_to_baseline": 2.41,
  "tech_level_reliability": "low",
  "tech_level_reliability_score": 28,
  "suggested_stop_atr_mult": 2.5,
  "position_scale": 0.41
}
```

**完整分析**：
```bash
python scripts/atr_squeeze.py --symbol XAGUSD --start 2020-01-01 --end 2026-01-01 --output result.json
```

**生成視覺化儀表盤**：
```bash
pip install matplotlib  # 首次使用
python scripts/plot_atr_squeeze.py --symbol SI=F --output output/
```

儀表盤包含：
- 價格走勢圖
- ATR% 波動率時間序列
- ATR 倍率儀表盤
- 當前狀態與風控建議面板

</quick_start>

<intake>
需要進行什麼操作？

1. **快速偵測** - 檢查單一資產的當前行情狀態
2. **多資產掃描** - 掃描多個資產尋找擠壓行情
3. **歷史回測** - 回溯識別過去的擠壓期間
4. **持續監控** - 設定警報當行情切換時通知
5. **方法論學習** - 了解 ATR 擠壓行情的理論基礎

**請選擇或直接提供資產代碼開始分析。**
</intake>

<routing>
| Response                         | Action                                       |
|----------------------------------|----------------------------------------------|
| 1, "快速", "quick", "check"      | 執行 `python scripts/atr_squeeze.py --quick` |
| 2, "掃描", "scan", "multiple"    | 閱讀 `workflows/monitor.md` 並執行           |
| 3, "回測", "backtest", "history" | 閱讀 `workflows/backtest.md` 並執行          |
| 4, "監控", "monitor", "alert"    | 閱讀 `workflows/monitor.md` 並執行           |
| 5, "學習", "方法論", "why"       | 閱讀 `references/methodology.md`             |
| 提供 symbol (如 SI=F, GC=F)      | 閱讀 `workflows/detect.md` 並使用參數執行    |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
detect-atr-squeeze-regime/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── detect.md                      # 單資產偵測工作流
│   ├── monitor.md                     # 多資產監控工作流
│   └── backtest.md                    # 歷史回測工作流
├── references/
│   ├── methodology.md                 # ATR 擠壓行情方法論
│   ├── input-schema.md                # 完整輸入參數定義
│   └── data-sources.md                # 資料來源說明
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── atr_squeeze.py                 # 主偵測腳本
│   └── plot_atr_squeeze.py            # 視覺化儀表盤腳本
└── examples/
    └── xagusd-squeeze-2024.json       # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- ATR% 標準化原理
- 三行情分類邏輯
- 反身性機制解讀
- Ole Hansen 白銀擠壓案例

**資料來源**: references/data-sources.md
- Yahoo Finance 期貨代碼
- Stooq 替代來源
- 數據頻率與對齊

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow    | Purpose    | 使用時機         |
|-------------|------------|------------------|
| detect.md   | 單資產偵測 | 需要檢查特定資產 |
| monitor.md  | 多資產監控 | 日常掃描或警報   |
| backtest.md | 歷史回測   | 驗證識別準確性   |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script              | Command                          | Purpose          |
|---------------------|----------------------------------|------------------|
| atr_squeeze.py      | `--symbol SI=F --quick`          | 快速檢查當前狀態 |
| atr_squeeze.py      | `--symbol SI=F --start DATE`     | 完整歷史分析     |
| atr_squeeze.py      | `--scan SI=F,GC=F,CL=F`          | 多資產掃描       |
| plot_atr_squeeze.py | `--symbol SI=F --output output/` | 生成視覺化儀表盤 |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數       | 類型   | 預設值     | 說明       |
|------------|--------|------------|------------|
| symbol     | string | (required) | 資產代碼   |
| start_date | string | today-5y   | 取樣開始日 |
| end_date   | string | today      | 取樣結束日 |
| timeframe  | string | 1d         | 價格頻率   |

**ATR 參數**

| 參數            | 類型   | 預設值 | 說明                 |
|-----------------|--------|--------|----------------------|
| atr_period      | int    | 14     | ATR 週期             |
| atr_smoothing   | string | ema    | 平滑法（ema/wilder） |
| use_percent_atr | bool   | true   | 是否轉為百分比       |

**行情判定參數**

| 參數                   | 類型   | 預設值 | 說明                    |
|------------------------|--------|--------|-------------------------|
| baseline_window_days   | int    | 756    | 長期基準窗口（約 3 年） |
| spike_threshold_x      | number | 2.0    | 倍率門檻                |
| high_vol_threshold_pct | number | 6.0    | 絕對 ATR% 高波動門檻    |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "detect-atr-squeeze-regime",
  "symbol": "SI=F",
  "as_of": "2026-01-14",
  "regime": "volatility_dominated_squeeze",
  "atr_pct": 7.23,
  "atr_ratio_to_baseline": 2.41,
  "baseline_atr_pct": 3.0,
  "tech_level_reliability": "low",
  "tech_level_reliability_score": 28,
  "risk_adjustments": {
    "suggested_stop_atr_mult": 2.5,
    "position_scale": 0.41,
    "recommended_timeframe": "weekly",
    "instrument_suggestion": "options_or_spreads"
  },
  "interpretation": {
    "regime_explanation": "...",
    "tactics": ["...", "..."]
  }
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前行情判定（orderly / elevated / squeeze）
- [ ] ATR% 數值與對基準的倍率
- [ ] 技術位可靠度評分（0-100）
- [ ] 建議停損倍數
- [ ] 建議倉位縮放係數
- [ ] 行情解釋與戰術建議
- [ ] 時間序列資料（可選，用於視覺化）
- [ ] 視覺化儀表盤 PNG（可選，使用 plot_atr_squeeze.py）
</success_criteria>
