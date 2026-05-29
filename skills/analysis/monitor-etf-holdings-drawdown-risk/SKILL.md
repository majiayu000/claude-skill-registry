---
name: monitor-etf-holdings-drawdown-risk
description: 偵測「商品價格上漲、但對應實物 ETF/信託持倉卻下滑」的背離現象，並用多指標交叉驗證，評估是否存在實物供給緊張/交割壓力風險。
---

<essential_principles>

<principle name="divergence_core">
**背離訊號核心邏輯**

背離事件定義：
- **價格上漲**：`price_return >= min_price_return_pct`（如 +15%）
- **庫存下滑**：`inventory_change <= -min_inventory_drawdown_pct`（如 -10%）
- **同時發生**：在相同視窗期（如 180 天）內同時滿足

當價格與庫存同向時（同漲同跌）為正常；**逆向時**（價漲庫跌）才需要警覺。
</principle>

<principle name="dual_hypothesis">
**雙重假設驗證**

不能直接把「庫存下降」解讀為「實物被搶」，需要交叉驗證：

| 假設 | 支持條件 | 反駁條件 |
|------|----------|----------|
| **實物緊張** | COMEX/LBMA 下降、backwardation、lease rates 上升、零售溢價擴大 | 其他庫存穩定、contango、溢價平穩 |
| **資金流/贖回** | ETF 流出但交易所庫存穩定、期貨結構不緊 | 多重庫存同步下降 |

**輸出兩種解釋，讓用戶判斷哪個更符合當前數據。**
</principle>

<principle name="data_access">
**資料取得方式**

本 skill 優先使用：
- **ETF 官網庫存**：Selenium 模擬人類瀏覽器行為抓取（避免 API 限制）
- **Yahoo Finance**：`yfinance` 套件取得現貨/期貨價格
- **交叉驗證**：COMEX 庫存、期貨結構等公開數據

腳本位於 `scripts/` 目錄，遵循 `references/data-sources.md` 的反偵測策略。
</principle>

<principle name="stress_scoring">
**壓力分數計算**

```
stress_score = 100 × min(1.0,
    0.6 × divergence_severity +      # 背離嚴重度
    0.2 × decade_low_bonus +         # 十年低點加成
    0.2 × ratio_extreme_bonus        # 比值極端加成
)
```

| 分數區間 | 解讀 |
|----------|------|
| 0-30     | 正常，無明顯背離 |
| 30-60    | 輕度背離，值得關注 |
| 60-80    | 中度背離，建議深入驗證 |
| 80-100   | 重度背離，高度警戒 |
</principle>

</essential_principles>

<objective>
監控實物型 ETF（如 SLV、PSLV、GLD）的持倉與商品價格背離現象：

1. **偵測背離**：價格上漲但 ETF 庫存下滑
2. **評估嚴重度**：計算背離程度、十年低點、比值極端
3. **交叉驗證**：使用 COMEX、期貨結構、零售溢價等指標
4. **產出洞察**：提供兩種對立假設，避免單一敘事偏誤

輸出：背離狀態、壓力分數、交叉驗證結果、下一步檢查建議。
</objective>

<quick_start>

**最快的方式：檢查 SLV 背離狀態**

```bash
cd skills/monitor-etf-holdings-drawdown-risk
pip install pandas numpy yfinance selenium webdriver-manager beautifulsoup4 matplotlib  # 首次使用
python scripts/divergence_detector.py --etf SLV --quick
```

輸出範例：
```json
{
  "asof": "2026-01-20",
  "divergence": false,
  "price_return_window": 1.92,
  "inventory_change_window": 0.15,
  "inventory_decade_low": false,
  "stress_score_0_100": 20.0,
  "interpretations": ["Physical Tightness", "ETF Flow Hypothesis"]
}
```

**完整分析 + 視覺化報告**：
```bash
# 1. 執行背離偵測
python scripts/divergence_detector.py \
  --etf SLV \
  --start 2010-01-01 \
  --end 2026-01-20 \
  --output result.json

# 2. 生成視覺化報告
python scripts/visualize_divergence.py \
  --result result.json \
  --output ../../../output/
```

**輸出**：
- JSON 分析結果：`result.json`
- 視覺化報告：`output/SLV_divergence_report_20260120.png`
- PDF 報告：`output/SLV_divergence_report_20260120.pdf`

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查** - 查看指定 ETF 目前的背離狀態與壓力分數
2. **完整分析** - 執行完整的歷史背離分析
3. **交叉驗證** - 使用多指標驗證背離訊號的真實性
4. **監控模式** - 設定持續監控與背離警報
5. **方法論學習** - 了解背離偵測與雙重假設邏輯

**請選擇或直接提供分析參數（如 ETF 代碼）。**
</intake>

<routing>
| Response                        | Action                                        |
|---------------------------------|-----------------------------------------------|
| 1, "快速", "quick", "check"     | 執行 `scripts/divergence_detector.py --quick` |
| 2, "分析", "analyze", "full"    | 閱讀 `workflows/analyze.md` 並執行            |
| 3, "驗證", "validate", "cross"  | 閱讀 `workflows/cross-validate.md` 並執行     |
| 4, "監控", "monitor", "alert"   | 閱讀 `workflows/monitor.md` 並執行            |
| 5, "學習", "方法論", "why"      | 閱讀 `references/methodology.md`              |
| 提供 ETF 代碼 (如 SLV, GLD)     | 閱讀 `workflows/analyze.md` 並使用參數執行    |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
monitor-etf-holdings-drawdown-risk/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整背離分析工作流
│   ├── monitor.md                     # 持續監控工作流
│   └── cross-validate.md              # 交叉驗證工作流
├── references/
│   ├── data-sources.md                # ETF 庫存與價格資料來源
│   ├── methodology.md                 # 背離偵測方法論
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
└── scripts/
    ├── divergence_detector.py         # 主偵測腳本
    ├── fetch_etf_holdings.py          # ETF 庫存抓取（Selenium）
    └── fetch_prices.py                # 價格數據抓取
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 背離偵測邏輯
- 雙重假設驗證框架
- 壓力分數計算

**資料來源**: references/data-sources.md
- ETF 官網庫存抓取（Selenium）
- Yahoo Finance 價格數據
- 交叉驗證數據源（COMEX、LBMA）

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow          | Purpose          | 使用時機               |
|-------------------|------------------|------------------------|
| analyze.md        | 完整背離分析     | 需要完整歷史分析時     |
| monitor.md        | 持續監控狀態     | 日常監控或警報         |
| cross-validate.md | 交叉驗證背離訊號 | 確認背離真實性時       |
</workflows_index>

<templates_index>
| Template           | Purpose             |
|--------------------|---------------------|
| output-json.md     | JSON 輸出結構定義   |
| output-markdown.md | Markdown 報告模板   |
</templates_index>

<scripts_index>
| Script                  | Command                                 | Purpose              |
|-------------------------|-----------------------------------------|----------------------|
| divergence_detector.py  | `--etf SLV --quick`                     | 快速檢查背離狀態     |
| divergence_detector.py  | `--start DATE --end DATE --output FILE` | 完整歷史分析         |
| visualize_divergence.py | `--result result.json --output DIR`     | 生成視覺化報告       |
| fetch_etf_holdings.py   | `--etf SLV --output holdings.csv`       | 抓取 ETF 庫存        |
| fetch_prices.py         | `--symbol SI=F --output prices.csv`     | 抓取商品價格         |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數                   | 類型   | 預設值     | 說明                       |
|------------------------|--------|------------|----------------------------|
| etf_ticker             | string | (必填)     | ETF/信託代碼（如 SLV）     |
| commodity_price_symbol | string | (必填)     | 商品價格代碼（如 XAGUSD）  |
| start_date             | string | 10Y 前     | 分析起始日                 |
| end_date               | string | today      | 分析結束日                 |

**背離參數**

| 參數                       | 類型  | 預設值 | 說明                   |
|----------------------------|-------|--------|------------------------|
| divergence_window_days     | int   | 180    | 背離計算視窗（天）     |
| decade_low_window_days     | int   | 3650   | 十年低點視窗（天）     |
| min_price_return_pct       | float | 0.15   | 價格上漲門檻           |
| min_inventory_drawdown_pct | float | 0.10   | 庫存下滑門檻           |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "monitor-etf-holdings-drawdown-risk",
  "asof": "2026-01-16",
  "inputs": {
    "etf_ticker": "SLV",
    "commodity_price_symbol": "XAGUSD"
  },
  "result": {
    "divergence": true,
    "price_return_window": 0.32,
    "inventory_change_window": -0.18,
    "inventory_decade_low": true,
    "inventory_to_price_ratio_z": -2.4,
    "stress_score_0_100": 78.5
  },
  "interpretations": [...],
  "next_checks": [...]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 背離狀態判定（divergence: true/false）
- [ ] 價格變化與庫存變化數值
- [ ] 十年低點判定
- [ ] 庫存/價格比值 Z 分數
- [ ] 壓力分數（0-100）
- [ ] 兩種對立假設解釋
- [ ] 下一步驗證建議清單
</success_criteria>
