---
name: analyze-copper-inventory-rebuild-signal
description: 用「庫存快速回補」作為短期警戒訊號，評估銅價是否接近短線高點，同時給出一個「長期是否偏便宜」的歷史分位數判讀。
---

<essential_principles>

<principle name="dual_signal_framework">
**雙層訊號框架（Dual Signal Framework）**

本技能將「肉眼看圖」轉換為可量化、可自動更新的雙層訊號系統：

| 層次 | 問題 | 核心指標 | 決策輸出 |
|------|------|----------|----------|
| **短線** | 是否「有點超前」？ | SHFE 回補速度 z-score + 庫存水位 | CAUTION / NEUTRAL / SUPPORTIVE |
| **長線** | 是否「仍偏便宜」？ | 銅價歷史分位數（10 年） | CHEAP / FAIR / RICH |

**關鍵洞察**：SHFE 庫存快速回補 + 水位偏高 → 常常貼近價格局部高點。
</principle>

<principle name="data_source">
**數據來源（三類數據）**

使用 Chrome CDP **全自動**抓取 Highcharts 圖表數據，共需三類數據：

| 數據 | 來源 | URL |
|------|------|-----|
| SHFE 銅庫存 | MacroMicro (CDP) | https://en.macromicro.me/series/8743/copper-shfe-warehouse-stock |
| COMEX 銅庫存 | MacroMicro (CDP) | https://www.macromicro.me/series/8742/copper-comex-warehouse-stock |
| 銅期貨價格 | Yahoo Finance | `HG=F`（COMEX 銅期貨連續近月） |

**口徑**：庫存為可交割銅庫存（噸）、價格為收盤價（USD/lb）
</principle>

<principle name="rebuild_speed_zscore">
**回補速度 Z-Score 計算**

將主觀「回補很快」轉化為客觀可比較的標準化指標：

```
rebuild_W = inv_t - inv_{t-W}  (W = 4 週)
z_score = (rebuild_W - μ) / σ   (μ, σ 為 3 年滾動)
```

- z-score > 1.5：回補速度「異常快」
- z-score > 2.0：回補速度「極端快」
- z-score < -1.5：去庫存速度「異常快」
</principle>

</essential_principles>

<objective>
分析銅庫存回補訊號與價格的歷史關係，輸出：
1. **短期訊號**：當前回補速度與庫存水位是否觸發「謹慎」訊號
2. **長期判讀**：銅價是否仍處於歷史偏便宜區間
3. **歷史驗證**：過去同類訊號對應價格高點的命中率
</objective>

<quick_start>

**全自動執行（無需手動操作 Chrome）**

**Step 1：安裝依賴**
```bash
pip install requests websocket-client pandas numpy yfinance matplotlib
```

**Step 2：一鍵抓取所有數據（SHFE + COMEX 庫存 + 銅價）**
```bash
cd skills/analyze-copper-inventory-rebuild-signal/scripts
python fetch_copper_data.py
```

腳本會自動：
- 啟動 Chrome 調試模式
- 依序抓取 SHFE 和 COMEX 庫存（~80 秒）
- 抓取銅期貨價格（Yahoo Finance）
- 儲存到 `cache/shfe_inventory.csv`、`cache/comex_inventory.csv`、`cache/copper_price.csv`
- 關閉 Chrome

**Step 3：執行庫存訊號分析**
```bash
python inventory_signal_analyzer.py
```

**Step 4：生成視覺化圖表**
```bash
python visualize_inventory_signal.py
```

**輸出**：`{專案根目錄}/output/copper_inventory_signal_YYYY-MM-DD.png`

</quick_start>

<intake>
需要進行什麼分析？

1. **快速檢查** - 查看當前 SHFE 庫存回補訊號狀態
2. **完整分析** - 執行回補訊號與價格高點的歷史驗證
3. **長期分位數** - 銅價歷史分位數判讀（10 年）
4. **視覺化** - 生成 Bloomberg 風格分析圖表

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response | Action |
|----------|--------|
| 1, "快速", "quick", "check", "狀態" | 執行 `python scripts/inventory_signal_analyzer.py --quick` |
| 2, "完整", "full", "驗證", "backtest" | 執行 `python scripts/inventory_signal_analyzer.py --full` |
| 3, "長期", "分位數", "percentile", "cheap" | 執行 `python scripts/inventory_signal_analyzer.py --long-term` |
| 4, "圖表", "chart", "視覺化", "visualize" | 執行 `python scripts/visualize_inventory_signal.py` |

**路由後，執行對應命令。**
</routing>

<directory_structure>
```
analyze-copper-inventory-rebuild-signal/
├── SKILL.md                              # 本文件（路由器）
├── manifest.json                         # 技能元資料
├── skill.yaml                            # 前端展示元數據
├── scripts/
│   ├── fetch_copper_data.py              # 全自動 CDP 數據爬蟲（SHFE + COMEX + 價格）
│   ├── fetch_shfe_inventory.py           # SHFE 專用爬蟲（向下相容）
│   ├── inventory_signal_analyzer.py      # 核心分析邏輯
│   └── visualize_inventory_signal.py     # Bloomberg 風格視覺化
├── references/
│   ├── data-sources.md                   # 數據來源說明
│   ├── methodology.md                    # 方法論說明
│   └── historical-episodes.md            # 歷史事件對照
├── templates/
│   ├── output-json.md                    # JSON 輸出格式
│   └── output-markdown.md                # Markdown 輸出格式
├── workflows/
│   ├── quick-check.md                    # 快速檢查流程
│   ├── full-analysis.md                  # 完整分析流程
│   └── visualize.md                      # 視覺化流程
├── cache/
│   ├── shfe_inventory.csv                # SHFE 庫存快取
│   ├── comex_inventory.csv               # COMEX 庫存快取
│   └── copper_price.csv                  # 銅價快取
└── examples/
    └── sample_output.json                # 範例輸出

# 視覺化輸出位置（專案根目錄）
{專案根目錄}/output/
└── copper_inventory_signal_YYYY-MM-DD.png  # 輸出圖表（含日期）
```
</directory_structure>

<scripts_index>
| Script | Command | Purpose |
|--------|---------|---------|
| fetch_copper_data.py | `python fetch_copper_data.py` | 全自動抓取所有數據（SHFE + COMEX + 價格） |
| fetch_copper_data.py | `--force-refresh` | 強制重新抓取（忽略快取） |
| fetch_copper_data.py | `--source shfe` | 只抓取 SHFE 庫存 |
| fetch_copper_data.py | `--source comex` | 只抓取 COMEX 庫存 |
| fetch_copper_data.py | `--source price` | 只抓取銅價 |
| inventory_signal_analyzer.py | `--quick` | 快速檢查當前訊號狀態 |
| inventory_signal_analyzer.py | `--full` | 完整歷史驗證分析 |
| inventory_signal_analyzer.py | `--long-term` | 長期價格分位數分析 |
| visualize_inventory_signal.py | 無參數 | 生成 Bloomberg 風格圖表（輸出到專案根目錄 output/） |
| visualize_inventory_signal.py | `-o path.png` | 指定輸出路徑 |
</scripts_index>

<input_parameters>

**分析參數**

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `start_date` | string | 2015-01-01 | 回測起始日 |
| `end_date` | string | today | 回測結束日 |
| `price_ticker` | string | HG=F | 銅期貨代碼（Yahoo Finance） |
| `price_freq` | string | weekly | 價格頻率（daily/weekly） |
| `fast_rebuild_window_weeks` | int | 4 | 「快速回補」觀察窗（週） |
| `fast_rebuild_z` | float | 1.5 | 回補速度 z-score 門檻 |
| `high_inventory_mode` | string | percentile | 庫存偏高判定模式（absolute/percentile） |
| `high_inventory_percentile` | float | 0.85 | 庫存偏高分位數門檻 |
| `peak_match_window_weeks` | int | 2 | 訊號對應價格高點的容許窗口（±N 週） |
| `long_term_window_years` | int | 10 | 長期分位數計算窗口（年） |
| `cheap_percentile` | float | 0.35 | 「長期偏便宜」門檻 |

</input_parameters>

<visualization>

**視覺化輸出：Bloomberg 風格銅庫存回補訊號儀表板**

遵循 `thoughts/shared/guide/bloomberg-style-chart-guide.md` 規範設計。

包含三個區塊（上中下排列）：

1. **銅價 + 總庫存對照**（雙軸圖）
   - R1 右軸：銅價（橙紅色線）
   - L2 左軸：總庫存面積圖（SHFE + COMEX 疊加）
   - 標記 CAUTION 訊號觸發點
   - 最新價格標註

2. **回補速度 z-score**（時序圖）
   - SHFE z-score：面積填充（紅/青色區分回補/去庫存）
   - COMEX z-score：虛線疊加
   - 門檻線（z=1.5, z=2.0, z=-1.5）

3. **訊號狀態儀表板**
   - 短期訊號區塊（CAUTION/NEUTRAL/SUPPORTIVE）
   - 長期判斷區塊（CHEAP/FAIR/RICH）
   - SHFE/COMEX z-score 即時數值

**配色**：Bloomberg 深色主題（依據 bloomberg-style-chart-guide.md）
- 背景: `#1a1a2e`（深藍黑色）
- 網格: `#2d2d44`（暗灰紫）
- 銅價（primary）: `#ff6b35`（橙紅色）
- SHFE 庫存（secondary）: `#ffaa00`（橙黃色）
- COMEX 庫存（tertiary）: `#ffff00`（黃色）
- CAUTION 訊號: `#ff4444`（紅色）
- SUPPORTIVE: `#00ff88`（綠色）
- 中性: `#888888`（灰色）

**快速繪圖**：
```bash
cd scripts
python visualize_inventory_signal.py
```

**輸出路徑**：`{專案根目錄}/output/copper_inventory_signal_YYYY-MM-DD.png`

圖表會自動輸出到專案根目錄的 `output/` 資料夾，檔名包含當天日期。

</visualization>

<output_example>

**Markdown 輸出範例**

```markdown
# 銅：庫存回補訊號（SHFE / COMEX）

## 最新狀態
- 數據日期：2026-01-26
- SHFE 庫存：235,000 噸
- SHFE 4 週回補速度 z-score：+1.9（異常快）
- COMEX 庫存：18,500 噸
- COMEX 4 週回補速度 z-score：+0.5（正常）
- 總庫存（SHFE + COMEX）：253,500 噸
- 銅期貨價格：4.52 USD/lb

## 短期判斷（是否「有點超前」）
- 訊號：**⚠️ CAUTION**
- 原因：SHFE 庫存「水位偏高」且「回補速度異常快」
- 歷史驗證：過去同類訊號在 ±2 週內對應局部高點的命中率約 **62%**
- 解讀：短線更容易出現「漲勢喘口氣 / 回檔」而不是一路順風

## 長期判斷（是否仍「偏便宜」）
- 銅價 10 年歷史分位數：0.32（低於 0.35）
- 結論：**💚 長期偏便宜**（但不代表短線不會先整理）

---
### 數據來源
- SHFE 庫存：MacroMicro (CDP)
- COMEX 庫存：MacroMicro (CDP)
- 銅價：Yahoo Finance (HG=F)
```

**JSON 輸出範例**

```json
{
  "asof": "2026-01-26",
  "near_term_signal": "CAUTION",
  "long_term_view": "CHEAP",
  "latest": {
    "shfe_inventory_tonnes": 235000,
    "shfe_rebuild_z": 1.9,
    "comex_inventory_tonnes": 18500,
    "comex_rebuild_z": 0.5,
    "total_inventory_tonnes": 253500,
    "copper_price": 4.52,
    "price_percentile": 0.32
  },
  "backtest": {
    "peak_match_window_weeks": 2,
    "signal_to_local_peak_hit_rate": 0.62,
    "signal_count": 21
  }
}
```

</output_example>

<success_criteria>
分析成功時應產出：

- [x] SHFE 和 COMEX 庫存數據已從 MacroMicro **全自動**抓取並快取
- [x] 銅期貨價格數據已從 Yahoo Finance 抓取
- [x] SHFE 和 COMEX 當前回補速度 z-score 與庫存分位數
- [x] 短期訊號（CAUTION / NEUTRAL / SUPPORTIVE）
- [x] 歷史訊號命中率回測結果
- [x] 長期價格分位數與判讀（CHEAP / FAIR / RICH）
- [x] **Bloomberg 風格視覺化圖表**
- [x] 明確標註數據來源與計算方法
</success_criteria>

<references_index>
| 文件 | 內容 |
|------|------|
| references/data-sources.md | SHFE 庫存與銅價數據來源、CDP 抓取說明 |
| references/methodology.md | 回補速度 z-score、分位數計算方法論 |
| references/historical-episodes.md | 歷史訊號觸發事件對照 |
</references_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| workflows/quick-check.md | 快速檢查當前訊號狀態 |
| workflows/full-analysis.md | 完整歷史驗證分析 |
| workflows/visualize.md | 視覺化圖表生成 |
</workflows_index>

<templates_index>
| Template | Purpose |
|----------|---------|
| templates/output-json.md | JSON 輸出格式規範 |
| templates/output-markdown.md | Markdown 輸出格式規範 |
</templates_index>
