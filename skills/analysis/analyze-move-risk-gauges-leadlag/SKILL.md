---
name: analyze-move-risk-gauges-leadlag
description: 用公開市場數據檢查「利率波動率（MOVE）是否對利率事件（如 JGB 殖利率變動）不恐慌，並且是否領先帶動 VIX / 信用利差走低」。
---

<essential_principles>

<principle name="move_as_leading_indicator">
**MOVE 作為利率波動率領先指標**

MOVE Index（美林期權波動率指數）是衡量美國國債選擇權隱含波動率的指標：
- **MOVE 低/下降**：利率市場對未來波動預期降低，風險偏好上升
- **MOVE 高/上升**：利率市場恐慌，避險需求增加

MOVE 常被視為「債市的 VIX」，可作為其他風險指標的領先訊號。
</principle>

<principle name="leadlag_cross_correlation">
**交叉相關判斷領先落後**

使用 Cross-Correlation 判斷兩序列的領先/落後關係：
- 在 [-L, +L] 位移範圍內計算相關係數
- **最大相關出現在 lag > 0**：X 領先 Y
- **最大相關出現在 lag < 0**：X 落後 Y
- **最大相關出現在 lag ≈ 0**：同步移動

典型設定：L = 20（交易日），配合平滑處理降低噪音。
</principle>

<principle name="shock_event_reaction">
**事件窗檢定：是否被嚇到**

檢驗「利率事件（如 JGB 殖利率跳升）發生時，MOVE 是否恐慌」：
1. 定義衝擊事件：|ΔY[t-k:t]| ≥ threshold（如 15bp）
2. 檢查事件窗內 MOVE 變化
3. 若 MOVE 反應 < 歷史分布中位數 → "not spooked"

此邏輯可驗證「利率波動率對某事件不敏感」的敘事。
</principle>

<principle name="data_access">
**資料取得方式**

本 skill 使用 **Chrome CDP** 連接到 MacroMicro 抓取真實數據：
- **MOVE Index**: MacroMicro (CDP) - https://en.macromicro.me/charts/35584/us-treasury-move-index
- **JGB 10Y**: MacroMicro (CDP) - https://en.macromicro.me/charts/944/jp-10-year-goverment-bond-yield
- **VIX**: Yahoo Finance (yfinance)
- **Credit (IG OAS)**: FRED (BAMLC0A0CM)

**重要**：MOVE 和 JGB 需要透過 Chrome CDP 爬蟲取得，請參照 `<quick_start>` 的步驟啟動 Chrome。
</principle>

</essential_principles>

<objective>
實作利率波動率與風險指標的領先落後分析：

1. **數據抓取**：從公開來源取得 MOVE、VIX、信用利差、JGB 殖利率
2. **標準化處理**：Z 分數、平滑處理、頻率對齊
3. **領先落後分析**：交叉相關找出 MOVE vs VIX / 信用利差的 lead/lag
4. **事件窗檢定**：JGB 衝擊事件中 MOVE 是否「不恐慌」
5. **方向一致性**：MOVE 下行時，其他風險指標是否同步下行

輸出：領先落後判定、恐慌檢定結果、方向一致性比例、量化證據。
</objective>

<quick_start>

**執行分析前，必須先啟動 Chrome 調試模式**

**Step 1：關閉所有 Chrome 視窗**

**Step 2：用調試端口啟動 Chrome（Windows）**

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --remote-allow-origins=* ^
  --user-data-dir="%USERPROFILE%\.chrome-debug-profile" ^
  "https://en.macromicro.me/charts/35584/us-treasury-move-index"
```

**Step 3：在瀏覽器中開啟第二個分頁，載入 JGB 頁面**

```
https://en.macromicro.me/charts/944/jp-10-year-goverment-bond-yield
```

**Step 4：等待兩個頁面的圖表都完全載入（約 30-40 秒）**

**Step 5：執行分析**

```bash
cd .claude/skills/analyze-move-risk-gauges-leadlag/scripts
pip install pandas numpy yfinance requests websocket-client matplotlib  # 首次使用
python analyze.py --start 2024-01-01 --end 2026-01-31 --output-mode markdown
```

**Step 6（可選）：生成 Bloomberg 風格視覺化圖表**

```bash
# 方式一：分析時同時生成圖表
python analyze.py --start 2024-01-01 --end 2026-01-31 --output-mode markdown --chart

# 方式二：單獨生成圖表（自動使用快取數據）
python visualize.py --start 2024-01-01 --end 2026-01-31
```

圖表預設輸出路徑：`{專案根目錄}/output/move-leadlag-YYYY-MM-DD.png`

輸出範例：
```
## 結論

- 利率波動率（MOVE）對「JGB 殖利率衝擊」反應偏弱 / 未顯著升溫 → **not spooked**
- MOVE 的變化在統計上呈現 **領先 4-6 天** 的特徵
- MOVE 下行時，VIX / 信用利差同步走低的比例：VIX = 62%、Credit = 60%
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查** - 查看目前 MOVE 的領先落後狀態與恐慌程度
2. **完整分析** - 執行完整的領先落後與事件窗分析
3. **視覺化圖表** - 生成多面板分析結果圖表
4. **方法論學習** - 了解 Lead/Lag 分析與事件窗檢定的邏輯

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                     | Action                                                               |
|------------------------------|----------------------------------------------------------------------|
| 1, "快速", "quick", "check"  | 確認 Chrome CDP 已啟動，執行 `python scripts/analyze.py --quick`     |
| 2, "完整", "full", "analyze" | 閱讀 `workflows/analyze.md` 並執行                                   |
| 3, "視覺化", "chart", "plot" | 閱讀 `workflows/visualize.md` 並執行                                 |
| 4, "學習", "方法論", "why"   | 閱讀 `references/methodology.md`                                     |
| 提供參數 (如日期範圍)        | 閱讀 `workflows/analyze.md` 並使用參數執行                           |

**重要**：執行分析前必須確保 Chrome CDP 已啟動並載入 MOVE 和 JGB 頁面。
</routing>

<directory_structure>
```
analyze-move-risk-gauges-leadlag/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── cache/                             # 數據快取目錄
├── workflows/
│   ├── analyze.md                     # 完整分析工作流
│   └── visualize.md                   # 視覺化工作流
├── references/
│   ├── data-sources.md                # 資料來源與替代方案
│   ├── methodology.md                 # Lead/Lag 與事件窗方法論
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
└── scripts/
    ├── analyze.py                     # 主分析腳本
    ├── fetch_data.py                  # 數據抓取工具 (CDP + FRED + Yahoo)
    ├── visualize.py                   # Lead/Lag 綜合圖表繪圖工具
    └── visualize_rates_move.py        # 利率 vs MOVE 恐慌專題圖表（可帶入任何國家債券）
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- Lead/Lag 交叉相關分析
- Z 分數標準化
- 事件窗檢定邏輯

**資料來源**: references/data-sources.md
- MOVE Index: MacroMicro CDP
- JGB 10Y: MacroMicro CDP
- VIX: Yahoo Finance
- Credit (IG OAS): FRED
- 數據頻率與對齊

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow     | Purpose          | 使用時機           |
|--------------|------------------|--------------------|
| analyze.md   | 完整領先落後分析 | 需要詳細分析報告時 |
| visualize.md | 生成視覺化圖表   | 需要圖表展示時     |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script               | Command                                                              | Purpose                           |
|----------------------|----------------------------------------------------------------------|-----------------------------------|
| analyze.py           | `--quick`                                                            | 快速檢查當前狀態                  |
| analyze.py           | `--start DATE --end DATE`                                            | 完整分析                          |
| analyze.py           | `--start DATE --end DATE --chart`                                    | 分析並生成 Lead/Lag 綜合圖表      |
| analyze.py           | `--start DATE --end DATE --rates-chart`                              | 分析並生成利率 vs MOVE 專題圖表   |
| analyze.py           | `--rates-chart --rates-col BUND10Y --rates-name "Bund 10Y"`          | 指定其他國家債券分析              |
| fetch_data.py        | `--start DATE --end DATE`                                            | 單獨抓取數據                      |
| visualize.py         | `--start DATE --end DATE`                                            | 獨立生成 Lead/Lag 綜合圖表        |
| visualize_rates_move.py | `--start DATE --end DATE --rates-col JGB10Y --rates-name "JGB 10Y"` | 獨立生成利率 vs MOVE 恐慌專題圖表 |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數                 | 類型   | 預設值       | 說明                  |
|----------------------|--------|--------------|-----------------------|
| start_date           | string | -            | 起始日期 (YYYY-MM-DD) |
| end_date             | string | -            | 結束日期 (YYYY-MM-DD) |
| rates_vol_symbol     | string | MOVE         | 利率波動率指標        |
| equity_vol_symbol    | string | VIX          | 股市波動率指標        |
| credit_spread_symbol | string | CDX_IG_PROXY | 信用利差/風險指標     |
| jgb_yield_symbol     | string | JGB10Y       | 日本 10Y 殖利率       |

**分析參數**

| 參數                | 類型   | 預設值   | 說明                 |
|---------------------|--------|----------|----------------------|
| freq                | string | D        | 頻率（D=日 / W=週）  |
| smooth_window       | int    | 5        | 平滑移動平均窗       |
| zscore_window       | int    | 60       | Z 分數回看窗         |
| lead_lag_max_days   | int    | 20       | 交叉相關最大位移天數 |
| shock_window_days   | int    | 5        | 事件窗天數           |
| shock_threshold_bps | float  | 15       | JGB 衝擊門檻 (bps)   |
| output_mode         | string | markdown | 輸出格式             |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "analyze-move-risk-gauges-leadlag",
  "as_of": "2026-01-23",
  "status": "ok",
  "headline": "MOVE not spooked by JGB yield moves and appears to lead VIX/Credit lower.",
  "leadlag": {
    "MOVE_vs_VIX": {"best_lag_days": 6, "corr": 0.72},
    "MOVE_vs_CREDIT": {"best_lag_days": 4, "corr": 0.61}
  },
  "spooked_check": {
    "shock_definition": "abs(JGB10Y change over 5d) >= 15bp",
    "shock_count": 3,
    "mean_MOVE_reaction_on_shocks": 0.8,
    "MOVE_zscore_now": -0.4
  },
  "direction_alignment": {
    "MOVE_down_and_VIX_down_ratio": 0.58,
    "MOVE_down_and_CREDIT_down_ratio": 0.55
  }
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] MOVE vs VIX / Credit 的最佳領先天數與相關係數
- [ ] JGB 衝擊事件數量與 MOVE 平均反應
- [ ] MOVE 當前 Z 分數（恐慌程度）
- [ ] 方向一致性比例
- [ ] 一句話結論與量化證據
- [ ] 視覺化圖表（可選）
</success_criteria>

<chrome_cdp_reference>

## Chrome CDP 啟動指令

### Windows

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --remote-allow-origins=* ^
  --user-data-dir="%USERPROFILE%\.chrome-debug-profile" ^
  "https://en.macromicro.me/charts/35584/us-treasury-move-index"
```

### macOS

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$HOME/.chrome-debug-profile" \
  "https://en.macromicro.me/charts/35584/us-treasury-move-index"
```

### 驗證連線

```bash
curl -s http://127.0.0.1:9222/json
```

### 需要開啟的頁面

1. **MOVE Index**: https://en.macromicro.me/charts/35584/us-treasury-move-index
2. **JGB 10Y**: https://en.macromicro.me/charts/944/jp-10-year-goverment-bond-yield

</chrome_cdp_reference>

<visualization_reference>

## Bloomberg 風格視覺化圖表

本 skill 生成的圖表遵循 `thoughts/shared/guide/bloomberg-style-chart-guide.md` 規範。

### 圖表結構（2x3 佈局）

```
┌──────────────┬─────────────────────────────────┐
│ 交叉相關分析  │ 波動率指標時間序列               │
│   (1,1)      │      (1,2) + (1,3)              │
├──────────────┼─────────────────────────────────┤
│ 事件反應分布  │ 標準化序列（Z 分數）            │
│   (2,1)      │      (2,2) + (2,3)              │
└──────────────┴─────────────────────────────────┘
```

| 位置          | 面板名稱           | 內容                                   |
|---------------|--------------------|----------------------------------------|
| 左上 (1,1)    | 交叉相關分析       | MOVE vs VIX/Credit 的 lead/lag 曲線    |
| 左下 (2,1)    | 事件反應分布       | JGB 衝擊時 MOVE 變化直方圖 + 判定結果  |
| 右上 (跨2格)  | 波動率時間序列     | MOVE Index + VIX（雙軸）+ 衝擊事件標記 |
| 右下 (跨2格)  | 標準化序列         | MOVE/VIX/Credit Z 分數 + 當前 MOVE 標記|

### 配色方案

```python
COLORS = {
    "background": "#1a1a2e",   # 深藍黑色背景
    "primary": "#ff6b35",       # 橙紅色（MOVE）
    "secondary": "#ffaa00",     # 橙黃色（VIX）
    "tertiary": "#ffff00",      # 黃色（Credit）
    "jgb": "#00ff88",           # 綠色（JGB/未恐慌）
    "shock_line": "#ff4444",    # 紅色（衝擊/恐慌）
}
```

### 圖表輸出

- **預設路徑**: `{專案根目錄}/output/move-leadlag-YYYY-MM-DD.png`
- **解析度**: 150 DPI
- **尺寸**: 18x10 英寸
- **格式**: PNG

### CLI 參數

```bash
# 分析時自動生成 Lead/Lag 綜合圖表
python analyze.py --start 2024-01-01 --end 2026-01-31 --chart

# 生成利率 vs MOVE 恐慌專題圖表（預設 JGB 10Y）
python analyze.py --start 2024-01-01 --end 2026-01-31 --rates-chart

# 指定其他國家債券（如 Bund 10Y）
python analyze.py --start 2024-01-01 --end 2026-01-31 --rates-chart \
  --rates-col BUND10Y --rates-name "Bund 10Y"

# 同時生成兩種圖表
python analyze.py --start 2024-01-01 --end 2026-01-31 --chart --rates-chart

# 單獨生成圖表
python visualize.py --start 2024-01-01 --end 2026-01-31
python visualize_rates_move.py --start 2024-01-01 --end 2026-01-31 --rates-col JGB10Y --rates-name "JGB 10Y"
```

</visualization_reference>

<rates_move_chart_reference>

## 利率 vs MOVE 恐慌專題圖表

通用的利率波動率恐慌分析圖表，**可帶入任何國家/地區的債券殖利率**。

專注於回答：「MOVE 是否對 [指定債券] 殖利率變動感到恐慌？」

### 支援的債券（需在數據中存在）

| 參數值 (--rates-col) | 顯示名稱 (--rates-name) | 說明 |
|---------------------|------------------------|------|
| JGB10Y | "JGB 10Y" | 日本 10 年期公債（預設） |
| UST10Y | "UST 10Y" | 美國 10 年期公債 |
| BUND10Y | "Bund 10Y" | 德國 10 年期公債 |
| GILT10Y | "Gilt 10Y" | 英國 10 年期公債 |
| （自訂） | （自訂） | 任何在數據中存在的利率欄位 |

### 使用範例

```bash
# 分析 JGB 10Y vs MOVE（預設）
python analyze.py --start 2024-01-01 --end 2026-01-31 --rates-chart

# 分析 Bund 10Y vs MOVE
python analyze.py --start 2024-01-01 --end 2026-01-31 --rates-chart \
  --rates-col BUND10Y --rates-name "Bund 10Y"

# 獨立生成圖表
python visualize_rates_move.py --start 2024-01-01 --end 2026-01-31 \
  --rates-col JGB10Y --rates-name "JGB 10Y"
```

### 圖表結構

```
┌─────────────────────────────────────────────────┐
│           [利率名稱] vs MOVE 時序圖              │
│           （雙軸對比 + 衝擊事件標記）            │
├───────────────────────┬─────────────────────────┤
│   利率變化 vs MOVE    │     恐慌判定儀表板       │
│   反應散點圖 + 回歸線  │   （統計數據 + 結論）    │
└───────────────────────┴─────────────────────────┘
```

| 位置 | 面板名稱 | 內容 |
|------|----------|------|
| 上方 | 時序對比 | 指定利率（綠）+ MOVE（橙）雙軸圖，黃色虛線標記衝擊事件 |
| 左下 | 散點分析 | 利率變化(bps) vs MOVE 變化，含回歸線與相關係數 |
| 右下 | 判定儀表板 | 恐慌/未恐慌判定結果、統計數據、解讀說明 |

### 配色方案

```python
COLORS = {
    "move": "#ff6b35",          # 橙紅色（MOVE）
    "rates": "#00ff88",         # 綠色（利率）
    "spooked": "#ff4444",       # 紅色（恐慌判定）
    "not_spooked": "#00ff88",   # 綠色（未恐慌判定）
    "shock_marker": "#ffff00",  # 黃色（衝擊事件標記）
}
```

### 輸出路徑

- **預設路徑**: `{專案根目錄}/output/{rates-name}-move-panic-YYYY-MM-DD.png`
- 範例：`output/jgb-10y-move-panic-2026-01-23.png`

</rates_move_chart_reference>
