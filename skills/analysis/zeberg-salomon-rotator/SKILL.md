---
name: zeberg-salomon-rotator
description: 用領先和同時指標建構景氣模型，並判讀兩種景氣階段：景氣擴張期 (Risk-On) 與景氣收縮期 (Risk-Off)，並根據理論給出 "撞冰山" 與 "下沉" 事件訊號。
---

<essential_principles>

<principle name="two_state_model">
**兩態切換模型核心**

Zeberg–Salomon 模型將市場簡化為兩種狀態：
- **RISK_ON**: 持有股票（SPY），景氣擴張期
- **RISK_OFF**: 持有長債（TLT），景氣收縮期

切換邏輯基於「領先指標先轉弱，同時指標後確認」的景氣循環規律。
</principle>

<principle name="leading_coincident">
**領先 vs 同時指標**

| 類型       | 作用 | 典型成分                     | 領先時間 |
|------------|------|------------------------------|----------|
| Leading    | 預警 | 殖利率曲線、新訂單、房市許可 | 6-12 月  |
| Coincident | 確認 | 就業、工業生產、實質收入     | 同步     |

**合成方式**：
1. 各序列做 transform（yoy/mom/diff）
2. 統一方向（direction +1/-1）
3. Rolling z-score 標準化
4. EMA 平滑
5. 加權合成
</principle>

<principle name="iceberg_sinking">
**冰山事件 vs 下沉事件**

```
Iceberg Event: LeadingIndex < iceberg_threshold
  → 預警：景氣開始轉弱
  → 搭配「領先指標下降」+ 可選「市場亢奮」濾鏡

Sinking Event: CoincidentIndex < sinking_threshold
  → 確認：實體經濟收縮
  → 通常在 Iceberg 之後數月發生
```

**狀態機邏輯**：
- RISK_ON → RISK_OFF：Iceberg 連續確認 + 斜率為負
- RISK_OFF → RISK_ON：領先指標回升超過 (threshold + hysteresis)
</principle>

<principle name="data_access">
**資料取得方式**

本 skill 使用**無需 API key** 的資料來源：
- **FRED CSV**: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}`
- **Yahoo Finance**: `yfinance` 套件抓取 SPY, TLT, VIX

腳本位於 `scripts/` 目錄，可直接執行。
</principle>

</essential_principles>

<objective>
實作 Zeberg–Salomon 兩態輪動策略：

1. **建構指標**：從 FRED 數據合成 LeadingIndex 與 CoincidentIndex
2. **偵測事件**：識別「冰山」（領先轉弱）與「下沉」（同時確認）
3. **切換訊號**：產生 RISK_ON ↔ RISK_OFF 切換事件
4. **回測績效**：計算累積報酬、MaxDD、CAGR、與 benchmark 比較

輸出：切換事件清單、指標時間序列、回測摘要、診斷資訊。
</objective>

<quick_start>

**最快的方式：執行預設回測**

```bash
cd skills/zeberg-salomon-rotator
pip install pandas numpy yfinance pandas-datareader  # 首次使用
python scripts/rotator.py --quick
```

輸出範例：
```json
{
  "state": "RISK_ON",
  "latest_indices": {"LeadingIndex": 0.41, "CoincidentIndex": 0.22},
  "iceberg_event": false,
  "sinking_event": false,
  "last_switch": {"date": "2023-06-30", "action": "EXIT_LONG_BOND_ENTER_EQUITY"}
}
```

**完整回測**：
```bash
python scripts/rotator.py --start 2000-01-01 --end 2026-01-01 --output result.json
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查** - 查看目前的景氣狀態與最新指標
2. **完整回測** - 執行完整的歷史回測與績效分析
3. **視覺化圖表** - 生成多面板回測結果圖表
4. **監控模式** - 設定持續監控與切換警報
5. **方法論學習** - 了解 Zeberg-Salomon 模型的邏輯

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                      | Action                                      |
|-------------------------------|---------------------------------------------|
| 1, "快速", "quick", "check"   | 執行 `python scripts/rotator.py --quick`    |
| 2, "回測", "backtest", "full" | 閱讀 `workflows/backtest.md` 並執行         |
| 3, "視覺化", "chart", "plot"  | 閱讀 `workflows/visualize.md` 並執行        |
| 4, "監控", "monitor", "alert" | 閱讀 `workflows/monitor.md` 並執行          |
| 5, "學習", "方法論", "why"    | 閱讀 `references/methodology.md`            |
| 提供參數 (如日期範圍)         | 閱讀 `workflows/backtest.md` 並使用參數執行 |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
zeberg-salomon-rotator/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── backtest.md                    # 完整回測工作流
│   ├── visualize.md                   # 視覺化工作流
│   ├── monitor.md                     # 持續監控工作流
│   └── analyze.md                     # 深度分析工作流
├── references/
│   ├── data-sources.md                # FRED 系列代碼與資料來源
│   ├── methodology.md                 # Zeberg-Salomon 方法論解析
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
└── scripts/
    ├── rotator.py                     # 主輪動腳本
    ├── visualize.py                   # 視覺化繪圖工具
    └── fetch_data.py                  # 數據抓取工具
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- Zeberg-Salomon 模型概念
- 冰山/下沉事件定義
- 兩態切換邏輯

**資料來源**: references/data-sources.md
- FRED 系列代碼（領先/同時）
- Yahoo Finance 資產代碼
- 數據頻率與對齊

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow     | Purpose        | 使用時機         |
|--------------|----------------|------------------|
| backtest.md  | 完整歷史回測   | 需要績效分析時   |
| visualize.md | 生成視覺化圖表 | 需要圖表展示時   |
| monitor.md   | 持續監控狀態   | 日常監控或警報   |
| analyze.md   | 深度指標分析   | 理解當前市場狀態 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script        | Command                       | Purpose          |
|---------------|-------------------------------|------------------|
| rotator.py    | `--quick`                     | 快速檢查當前狀態 |
| rotator.py    | `--start DATE --end DATE`     | 完整回測         |
| visualize.py  | `-i result.json -o chart.png` | 生成視覺化圖表   |
| fetch_data.py | `--series T10Y3M,PAYEMS`      | 抓取 FRED 資料   |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數         | 類型   | 預設值     | 說明         |
|--------------|--------|------------|--------------|
| start_date   | string | 2000-01-01 | 回測起始日   |
| end_date     | string | today      | 回測結束日   |
| freq         | string | M          | 頻率（M=月） |
| equity_proxy | string | SPY        | 風險資產代理 |
| bond_proxy   | string | TLT        | 長債代理     |

**門檻參數**

| 參數              | 類型   | 預設值 | 說明         |
|-------------------|--------|--------|--------------|
| iceberg_threshold | number | -0.3   | 領先指標門檻 |
| sinking_threshold | number | -0.5   | 同時指標門檻 |
| confirm_periods   | int    | 2      | 連續確認期數 |
| hysteresis        | number | 0.15   | 進出場間距   |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "zeberg-salomon-rotator",
  "as_of": "2026-01-14",
  "state": "RISK_ON",
  "latest_indices": {
    "LeadingIndex": 0.41,
    "CoincidentIndex": 0.22,
    "iceberg_event": false,
    "sinking_event": false
  },
  "switch_events": [...],
  "backtest_summary": {
    "cagr": 0.123,
    "max_drawdown": -0.27,
    "turnovers": 10
  }
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前狀態（RISK_ON 或 RISK_OFF）
- [ ] LeadingIndex 與 CoincidentIndex 數值
- [ ] 冰山/下沉事件判定
- [ ] 切換事件清單（含日期、原因）
- [ ] 回測績效摘要（CAGR, MaxDD, 換手次數）
- [ ] 與 benchmark 比較（買入持有、60/40）
- [ ] 診斷資訊（各指標貢獻）
- [ ] 視覺化圖表（可選，輸出至 `output/` 目錄）
</success_criteria>
