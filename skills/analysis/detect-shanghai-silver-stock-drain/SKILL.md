---
name: detect-shanghai-silver-stock-drain
description: 以公開交易所庫存資料為核心，量化上海白銀庫存耗盡的方向、速度與加速度，並將其轉成可交易的供給緊縮訊號。
---

<essential_principles>

<principle name="drain_metrics_core">
**庫存耗盡三維度量化**

庫存分析的三維框架：
- **方向（Direction）**：庫存是上升還是下降
- **速度（Speed）**：每週流出量 `drain_rate(t) = -Δ1(t)`
- **加速度（Acceleration）**：流出速度的變化 `Δ2(t) = drain_rate(t) - drain_rate(t-1)`

當 `drain_rate > 0` 且 `Δ2 > 0` 時，表示「庫存正在流出，且流出速度在加快」——這是晚期供給訊號的核心特徵。
</principle>

<principle name="z_score_standardization">
**Z 分數標準化判斷**

使用歷史視窗（建議 3~5 年）計算 Z 分數：
- `z_drain(t) = (drain_rate(t) - mean) / std`
- `z_accel(t) = (Δ2(t) - mean) / std`

門檻判定：
| 指標             | 門檻   | 意義                 |
|------------------|--------|----------------------|
| z_drain          | ≤ -1.5 | 流出速度顯著大於常態 |
| z_accel          | ≥ +1.0 | 流出正在加速         |
| level_percentile | ≤ 0.20 | 庫存處於歷史低檔     |
</principle>

<principle name="three_stage_signal">
**三段式晚期訊號判定**

把推文敘事轉為可執行規則：

| 條件            | 描述                    | 單獨成立 | 組合效果     |
|-----------------|-------------------------|----------|--------------|
| A. Level        | 庫存水位 < 20% 歷史分位 | WATCH    | -            |
| B. Speed        | z_drain ≤ -1.5          | WATCH    | B+C → MEDIUM |
| C. Acceleration | z_accel ≥ +1.0          | WATCH    | A+B+C → HIGH |

**訊號分級**：
- `HIGH_LATE_STAGE_SUPPLY_SIGNAL`：A+B+C 同時成立
- `MEDIUM_SUPPLY_TIGHTENING`：(B+C) 或 (A+B) 成立
- `WATCH`：任一條件成立
- `NO_SIGNAL`：無異常
</principle>

<principle name="data_sources">
**資料來源與口徑**

主要數據來源：
- **CEIC Data**：上海期貨交易所白銀倉單數據
  - URL: `https://www.ceicdata.com/zh-hans/china/shanghai-futures-exchange-commodity-futures-stock/cn-warehouse-stock-shanghai-future-exchange-silver`
  - 數據範圍：2012-07-02 至今（約 3,300+ 觀測值）
  - 更新頻率：每日
  - 歷史最高：3,091 噸 (2021-01-12)

**重要提醒**：
- 這是「交易所可交割/倉單」口徑，不等於全中國社會庫存
- 單週跳動可能反映倉儲規則變動或搬倉，需平滑處理
- 使用 Selenium 模擬人類瀏覽器抓取 SVG 圖表，遵循反偵測策略
</principle>

</essential_principles>

<objective>
監控上海白銀庫存（SGE + SHFE）的耗盡狀態：

1. **數據採集**：抓取 SGE/SHFE 週報庫存數據
2. **三維量化**：計算方向、速度、加速度
3. **標準化判斷**：使用 Z 分數判定異常
4. **訊號生成**：輸出晚期供給訊號分級
5. **市場交叉驗證**（選配）：COMEX、ETF、現貨溢價

輸出：庫存水位、耗盡速度、加速度、Z 分數、訊號分級、敘事解讀。
</objective>

<quick_start>

**最快的方式：檢查上海白銀庫存耗盡狀態**

```bash
cd skills/detect-shanghai-silver-stock-drain

# 首次使用：安裝依賴
pip install pandas numpy selenium webdriver-manager matplotlib

# 1. 抓取最新數據（5 年歷史，約 200+ 週）
python scripts/fetch_shfe_stock.py --force-update

# 2. 執行快速檢查
python scripts/drain_detector.py --quick
```

輸出範例：
```json
{
  "as_of": "2026-01-16",
  "signal": "MEDIUM_SUPPLY_TIGHTENING",
  "latest_combined_stock_tonnes": 1133.3,
  "level_percentile": 0.12,
  "z_drain_rate": -2.1,
  "z_acceleration": 1.4
}
```

**完整分析 + 視覺化報告**：
```bash
# 1. 執行完整分析
python scripts/drain_detector.py \
  --start 2020-01-01 \
  --end 2026-01-16 \
  --output result.json

# 2. 生成視覺化報告
python scripts/visualize_drain.py \
  --result result.json \
  --output ../../../output/
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查** - 查看目前上海白銀庫存耗盡狀態與訊號
2. **完整分析** - 執行完整的歷史庫存分析與趨勢計算
3. **數據更新** - 抓取最新的 SGE/SHFE 庫存數據
4. **交叉驗證** - 使用 COMEX、ETF 等指標交叉驗證
5. **方法論學習** - 了解三維度量化與訊號判定邏輯

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                       | Action                                     |
|--------------------------------|--------------------------------------------|
| 1, "快速", "quick", "check"    | 執行 `scripts/drain_detector.py --quick`   |
| 2, "分析", "analyze", "full"   | 閱讀 `workflows/analyze.md` 並執行         |
| 3, "更新", "fetch", "data"     | 閱讀 `workflows/fetch-data.md` 並執行      |
| 4, "驗證", "validate", "cross" | 閱讀 `workflows/cross-validate.md` 並執行  |
| 5, "學習", "方法論", "why"     | 閱讀 `references/methodology.md`           |
| 提供日期參數                   | 閱讀 `workflows/analyze.md` 並使用參數執行 |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
detect-shanghai-silver-stock-drain/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整庫存分析工作流
│   ├── fetch-data.md                  # 數據抓取工作流
│   └── cross-validate.md              # 交叉驗證工作流
├── references/
│   ├── data-sources.md                # SGE/SHFE 資料來源說明
│   ├── methodology.md                 # 三維度量化方法論
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
└── scripts/
    ├── drain_detector.py              # 主偵測腳本
    ├── fetch_sge_stock.py             # SGE 庫存抓取（PDF）
    ├── fetch_shfe_stock.py            # SHFE 庫存抓取
    └── visualize_drain.py             # 視覺化報告生成
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 三維度量化邏輯（方向、速度、加速度）
- Z 分數標準化
- 三段式訊號判定

**資料來源**: references/data-sources.md
- SGE 行情周報 PDF 抓取
- SHFE 倉單/庫存周報抓取
- Selenium 反偵測策略

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow          | Purpose      | 使用時機                 |
|-------------------|--------------|--------------------------|
| analyze.md        | 完整庫存分析 | 需要完整歷史分析時       |
| fetch-data.md     | 數據抓取     | 更新 SGE/SHFE 庫存數據   |
| cross-validate.md | 交叉驗證訊號 | 確認供給緊縮訊號真實性時 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script              | Command                                 | Purpose          |
|---------------------|-----------------------------------------|------------------|
| drain_detector.py   | `--quick`                               | 快速檢查耗盡狀態 |
| drain_detector.py   | `--start DATE --end DATE --output FILE` | 完整歷史分析     |
| fetch_sge_stock.py  | `--output sge_stock.csv`                | 抓取 SGE 庫存    |
| fetch_shfe_stock.py | `--output shfe_stock.csv`               | 抓取 SHFE 庫存   |
| visualize_drain.py  | `--result result.json --output DIR`     | 生成視覺化報告   |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數            | 類型   | 預設值         | 說明                     |
|-----------------|--------|----------------|--------------------------|
| start_date      | string | 3Y 前          | 分析起始日 (YYYY-MM-DD)  |
| end_date        | string | today          | 分析結束日 (YYYY-MM-DD)  |
| frequency       | string | weekly         | 數據頻率 (weekly/daily)  |
| include_sources | array  | ["SGE","SHFE"] | 納入的庫存來源           |
| unit            | string | tonnes         | 單位 (tonnes/kg/troy_oz) |

**分析參數**

| 參數                   | 類型  | 預設值 | 說明                 |
|------------------------|-------|--------|----------------------|
| smoothing_window_weeks | int   | 4      | 平滑視窗（週）       |
| drain_threshold_z      | float | -1.5   | 異常耗盡 Z 分數門檻  |
| accel_threshold_z      | float | +1.0   | 耗盡加速 Z 分數門檻  |
| confirm_with_markets   | bool  | true   | 是否做市場側交叉驗證 |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "detect_shanghai_silver_stock_drain",
  "as_of": "2026-01-16",
  "unit": "tonnes",
  "sources": ["SGE", "SHFE"],
  "latest_combined_stock": 1133.3,
  "level_percentile": 0.12,
  "recent_4w_avg_drawdown": 58.4,
  "drawdown_acceleration": 9.7,
  "z_scores": {
    "z_drain_rate": -2.1,
    "z_acceleration": 1.4
  },
  "signal": "HIGH_LATE_STAGE_SUPPLY_SIGNAL",
  "narrative": [...],
  "caveats": [...]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 上海合併庫存水位（SGE + SHFE）
- [ ] 庫存水位歷史分位數
- [ ] 近 N 週平均流出速度
- [ ] 流出加速度
- [ ] z_drain_rate 與 z_acceleration
- [ ] 訊號分級（HIGH/MEDIUM/WATCH/NO_SIGNAL）
- [ ] 敘事解讀（中文）
- [ ] 數據口徑與限制說明
</success_criteria>
