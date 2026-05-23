---
name: detect-us-equity-valuation-percentile-extreme
description: 把多個股票估值指標統一轉成在過去百年歷史中的分位數，再合成一個總分，判斷目前是否處於歷史極端高估區間，並用歷史類比（如 1929、1965、1999）給出風險解讀。
---

<essential_principles>

<principle name="percentile_normalization">
**分位數標準化核心**

將不同單位的估值指標（PE、PB、CAPE 等）統一成「0-100 的歷史分位數」：
- **分位數 = 100 × (歷史中 ≤ 當前值的樣本數 / 總樣本數)**
- 例：CAPE 位於歷史第 98 分位 → 過去 130 年只有 2% 的時間比現在更貴
- 統一單位後，可跨指標合成「綜合估值分位數」
</principle>

<principle name="composite_aggregation">
**多指標合成邏輯**

合成公式：`composite_percentile = 加權平均(各指標分位數)`

支援三種合成方式：
| 方式 | 公式 | 適用場景 |
|------|------|----------|
| mean | 算術平均 | 各指標同等重要 |
| median | 中位數 | 抵抗單一指標異常拉升 |
| trimmed_mean | 去極端平均 | 穩健估計 |

**重要**：各指標可能有不同歷史長度，預設使用「各自歷史」計算分位數再合成。
</principle>

<principle name="extreme_detection">
**極端高估偵測邏輯**

```
if composite_percentile >= extreme_threshold (預設 95):
    → 判定「歷史極端高估」
    → 觸發風險解讀流程
```

歷史類比事件識別：
1. 找出合成分位數超過門檻的峰值
2. 用 `episode_min_gap_days` 去重（預設 10 年內只保留最高點）
3. 輸出：1929、1965、1999、2021、當前...
</principle>

<principle name="risk_interpretation">
**風險解讀框架**

「估值極端高」≠「明天崩盤」，但歷史特徵是：
- **風險分布不對稱**：下跌尾巴變厚
- **未來中期報酬壓縮**：估值均值回歸壓低長期報酬上限
- **波動先升後跌**：事件後 6-12 月波動率通常上升

輸出事後統計：
- 未來 180/365/1095 天報酬分布
- 最大回撤中位數與尾部風險
- 波動率變化機率
</principle>

<principle name="data_transparency">
**資料來源與限制揭露**

本 skill 使用**公開替代資料**，非彭博原始數據：
- **Shiller CAPE**: Robert Shiller 公開資料集（可回溯至 1871 年）
- **市值/GDP**: FRED 公開數據（可回溯至 1950 年代）
- **PE/PB/PS**: 公開金融資料（歷史較短，約 30-50 年）

**必須揭露**：
- 各指標可得期間不同
- 合成分位數為「近似重建」，非精確複製
</principle>

</essential_principles>

<objective>
偵測美股估值是否處於歷史極端區間：

1. **收集估值指標**：從公開數據源取得 PE、CAPE、PB、PS、市值/GDP 等
2. **計算分位數**：將各指標轉換為歷史分位數（0-100）
3. **合成總分**：加權平均（或中位數）得到綜合估值分位數
4. **判定極端**：若總分 ≥ 門檻（預設 95），觸發極端高估警報
5. **歷史類比**：找出歷史上的類似事件（1929、1965、1999 等）
6. **事後統計**：計算這些事件後的報酬、回撤、波動變化

輸出：當前狀態、各指標分位數、歷史類比事件、風險解讀。
</objective>

<quick_start>

**最快的方式：執行視覺化分析**

```bash
cd skills/detect-us-equity-valuation-percentile-extreme
pip install pandas numpy yfinance requests matplotlib openpyxl xlrd  # 首次使用
python scripts/visualize_valuation.py -o output
```

輸出：
- `output/us_valuation_percentile_YYYY-MM-DD.png` - 歷史走勢圖（類似 @ekwufinance 風格）
- `output/us_valuation_breakdown_YYYY-MM-DD.png` - 各指標分位數分解圖
- `output/us_valuation_analysis_YYYY-MM-DD.json` - JSON 結果

**圖表特色**：
- 多指標合成分位數的**歷史走勢**（非單一時間點）
- **歷史峰值標記**：1929、1965、1999、2021
- S&P 500 指數疊加（對數刻度）
- 當前「新高」標註

**快速檢查（純 JSON）**：
```bash
python scripts/valuation_percentile.py --quick
```

**完整分析**：
```bash
python scripts/valuation_percentile.py \
  --as_of_date 2026-01-21 \
  --universe "^GSPC" \
  --metrics "cape,mktcap_to_gdp,trailing_pe,pb" \
  --output result.json
```

</quick_start>

<intake>
需要進行什麼操作？

1. **視覺化分析（推薦）** - 生成歷史走勢圖表，標記歷史峰值
2. **快速檢查** - 查看目前的估值分位數與極端狀態
3. **完整分析** - 執行完整的歷史分位數分析與風險解讀
4. **歷史類比** - 深入分析歷史極端高估事件與事後表現
5. **方法論學習** - 了解估值分位數模型的邏輯
6. **自訂參數** - 指定估值指標、門檻、合成方式等

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                         | Action                                       |
|----------------------------------|----------------------------------------------|
| 1, "視覺化", "圖表", "chart"     | 執行 `python scripts/visualize_valuation.py -o output` |
| 2, "快速", "quick", "check"      | 執行 `python scripts/valuation_percentile.py --quick` |
| 3, "完整", "full", "analysis"    | 閱讀 `workflows/execute-analysis.md` 並執行 |
| 4, "歷史", "類比", "episodes"    | 閱讀 `workflows/historical-episodes.md` 並執行 |
| 5, "學習", "方法論", "why"       | 閱讀 `references/methodology.md`             |
| 6, "自訂", "custom", 提供參數    | 閱讀 `workflows/execute-analysis.md` 並使用參數執行 |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
detect-us-equity-valuation-percentile-extreme/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── execute-analysis.md            # 完整分析工作流
│   ├── visualize-analysis.md          # 視覺化分析工作流
│   └── historical-episodes.md         # 歷史類比分析工作流
├── references/
│   ├── methodology.md                 # 估值分位數方法論
│   ├── data-sources.md                # 資料來源與代碼
│   ├── valuation-metrics.md           # 估值指標定義
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── valuation_percentile.py        # 主分析腳本
│   ├── visualize_valuation.py         # 視覺化腳本（歷史走勢圖）
│   └── fetch_valuation_data.py        # 資料抓取工具
└── examples/
    └── sample_output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 分位數標準化原理
- 多指標合成邏輯
- 極端偵測與歷史類比

**資料來源**: references/data-sources.md
- Shiller CAPE 資料集
- FRED 系列代碼
- 公開替代資料說明

**估值指標**: references/valuation-metrics.md
- PE、Forward PE、CAPE 定義
- PB、PS、EV/EBITDA 定義
- Q Ratio、市值/GDP 定義

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow                | Purpose          | 使用時機               |
|-------------------------|------------------|------------------------|
| execute-analysis.md     | 完整估值分析     | 需要完整報告時         |
| historical-episodes.md  | 歷史事件深度分析 | 理解歷史類比與事後統計 |
</workflows_index>

<templates_index>
| Template           | Purpose              |
|--------------------|----------------------|
| output-json.md     | JSON 輸出結構定義    |
| output-markdown.md | Markdown 報告模板    |
</templates_index>

<scripts_index>
| Script                    | Command                           | Purpose              |
|---------------------------|-----------------------------------|----------------------|
| visualize_valuation.py    | `-o output`                       | **視覺化分析（推薦）** |
| valuation_percentile.py   | `--quick`                         | 快速檢查當前狀態     |
| valuation_percentile.py   | `--as_of_date DATE --output FILE` | 完整分析             |
| fetch_valuation_data.py   | `--metrics cape,pe`               | 抓取估值資料         |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數           | 類型   | 預設值       | 說明             |
|----------------|--------|--------------|------------------|
| as_of_date     | string | today        | 評估日期         |
| universe       | string | ^GSPC        | 市場代碼         |
| history_start  | string | 1900-01-01   | 歷史起算日       |
| metrics        | array  | [cape, ...]  | 估值指標清單     |
| aggregation    | string | mean         | 合成方法         |

**門檻參數**

| 參數                  | 類型   | 預設值 | 說明                   |
|-----------------------|--------|--------|------------------------|
| extreme_threshold     | number | 95     | 極端高估門檻（分位數） |
| episode_min_gap_days  | int    | 3650   | 歷史事件去重間隔       |
| forward_windows_days  | array  | [180, 365, 1095] | 事後統計視窗     |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "detect-us-equity-valuation-percentile-extreme",
  "as_of_date": "2026-01-21",
  "universe": "^GSPC",
  "composite_percentile": 97.3,
  "extreme_threshold": 95,
  "is_extreme": true,
  "metric_percentiles": {
    "cape": 98.2,
    "mktcap_to_gdp": 96.5,
    "trailing_pe": 94.1
  },
  "historical_episodes": [
    {"date": "1929-09-01", "composite_percentile": 97.8},
    {"date": "1999-12-01", "composite_percentile": 98.5}
  ],
  "forward_stats": {
    "365d_forward_return": {"median": -8.2, "p25": -22.1, "p10": -38.5},
    "1095d_max_drawdown": {"median": -28.4, "p75": -42.1}
  },
  "data_quality_notes": [
    "CAPE 資料可回溯至 1871 年",
    "市值/GDP 資料可回溯至 1950 年代",
    "合成分位數使用各指標自身歷史分布"
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前綜合估值分位數（0-100）
- [ ] 各指標個別分位數
- [ ] 極端高估判定（是/否）
- [ ] 歷史類比事件清單（日期、分位數）
- [ ] 事後統計（報酬、回撤、波動）
- [ ] 資料品質說明（各指標可得期間）
- [ ] 風險解讀框架（可選，輸出至 Markdown）

**視覺化輸出**（使用 visualize_valuation.py）：

- [ ] 歷史走勢圖（`us_valuation_percentile_YYYY-MM-DD.png`）
  - 多指標合成分位數時間序列
  - 歷史峰值標記（1929、1965、1999、2021）
  - S&P 500 指數疊加（對數刻度）
  - 當前位置標註
- [ ] 指標分解圖（`us_valuation_breakdown_YYYY-MM-DD.png`）
  - 各指標分位數橫向條形圖
  - 極端門檻參考線
- [ ] JSON 結果檔（`us_valuation_analysis_YYYY-MM-DD.json`）
</success_criteria>
