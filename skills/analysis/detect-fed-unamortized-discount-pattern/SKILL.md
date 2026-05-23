---
name: detect-fed-unamortized-discount-pattern
description: 檢查聯準會持有證券的未攤銷折價（Unamortized Discounts）是否出現與特定歷史危機期間相似的走勢模板，並用多指標交叉驗證是否真的屬於「金融壓力升高」而非單純會計/利率效果。
---

<essential_principles>

<principle name="pattern_matching_not_prediction">
**形狀比對 ≠ 事件預測**

核心認知：把「肉眼類比」轉成可量化的「形狀比對」，但「像」不等於「會發生」：
- **相關係數 (corr)**：近期窗口 vs. 基準窗口的線性形狀相似
- **動態時間校正 (DTW)**：允許「快一點/慢一點」但形狀相似
- **形狀特徵 (shape_features)**：趨勢斜率、拐點結構、波動擴張

輸出「pattern_similarity_score」只回答「像不像」，不回答「會不會發生」。
</principle>

<principle name="cross_validation_stress">
**壓力驗證才能升級風險判斷**

把「形狀相似」與「壓力驗證」拆開：
1. **pattern_similarity_score**：只測量形狀相似度
2. **stress_confirmation_score**：測量交叉驗證指標是否同步惡化
3. **composite_risk_score**：加權合成，但必須附上「哪些指標支持/反對」

**反直覺檢查**：
- 若相似度很高，但交叉驗證指標沒有壓力訊號 → 可能只是利率/持有結構/會計攤銷造成的圖形相似
- 若相似度中等，但多數壓力指標同步惡化 → 反而要提高警覺
</principle>

<principle name="data_mechanism_understanding">
**理解指標背後機制**

**WUDSHO（Unamortized Discounts）成因**：
- 聯準會購買債券時，若買入價低於面值，差額計為「未攤銷折價」
- 利率上升期：市價下跌 → 購入債券折價增加 → WUDSHO 上升
- 利率下降期：市價上升 → 購入債券溢價增加 → WUDSHO 下降

**重要**：WUDSHO 變動可能反映：
1. 利率環境變化（最常見）
2. 持有債券久期結構
3. 會計攤銷時程
4. **真正的金融壓力**（需交叉驗證才能確認）
</principle>

<principle name="falsification_mindset">
**反證優先的分析框架**

社群常見的「圖形類比敘事」往往缺乏反證：
- ❌「這條線複製 COVID，60 天內黑天鵝」→ 只有類比，沒有驗證
- ✅ 本技能輸出：「形狀相似度 0.88，但信用利差中性、股市波動偏低 → 不支持系統性壓力假說」

必須輸出的反證項目：
1. 「形狀相似」的替代解釋（利率效果、會計效果）
2. 「壓力指標」的現況（支持/反對風險假說）
3. 「歷史後續」的條件分布（不是預測）
</principle>

<principle name="public_data_transparency">
**公開資料來源與限制**

本技能使用 FRED 公開週資料：
- **WUDSHO**: Fed 持有證券的未攤銷折價
- **交叉驗證指標**：信用利差、波動率、短端利差等

**必須揭露**：
- FRED 週資料可能有 T+1 ~ T+3 延遲
- 部分指標（如窗口工具用量）需要替代代理
- 形狀比對結果受 resample 頻率影響
</principle>

</essential_principles>

<objective>
偵測聯準會未攤銷折價走勢是否與歷史危機期間相似：

1. **取得目標序列**：從 FRED 取得 WUDSHO（或指定序列）的週資料
2. **窗口比對**：將近期窗口與歷史基準窗口（如 COVID 2020）做形狀比對
3. **相似度計算**：使用相關係數、DTW、形狀特徵等多種方法
4. **交叉驗證**：檢查信用利差、波動率、流動性指標是否同步惡化
5. **風險分數合成**：輸出可量化的風險分數與反證分析
6. **情境敘事**：描述歷史類比後續發展（非預測）

輸出：形狀相似度、壓力驗證分數、合成風險分數、反證分析、情境推演。
</objective>

<quick_start>

**最快的方式：執行完整分析**

```bash
cd skills/detect-fed-unamortized-discount-pattern
pip install pandas numpy requests scipy matplotlib  # 首次使用
python scripts/pattern_detector.py --quick
```

輸出：
- `output/pattern_analysis_YYYY-MM-DD.json` - JSON 結果

**完整分析（指定參數）**：
```bash
python scripts/pattern_detector.py \
  --target_series WUDSHO \
  --baseline_windows "COVID_2020:2020-01-01:2020-06-30" \
  --recent_window_days 120 \
  --output result.json
```

**Bloomberg 風格視覺化**（輸出至專案根目錄 output/）：
```bash
python scripts/visualize_pattern.py
```

使用現有分析結果生成圖表：
```bash
python scripts/visualize_pattern.py --json output/pattern_analysis_YYYY-MM-DD.json
```

輸出圖表：
- `output/fed_unamortized_discount_pattern_YYYY-MM-DD.png` - 形狀比對與壓力儀表板
- `output/fed_unamortized_discount_history_YYYY-MM-DD.png` - 歷史走勢總覽

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查（推薦）** - 查看目前的形狀相似度與壓力分數
2. **完整分析** - 執行完整的形狀比對與交叉驗證
3. **視覺化分析** - 生成形狀比對圖表
4. **歷史事件對照** - 深入了解歷史基準窗口的後續發展
5. **方法論學習** - 了解形狀比對與交叉驗證的邏輯
6. **自訂參數** - 指定序列、窗口、門檻等參數

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                      | Action                                               |
|-------------------------------|------------------------------------------------------|
| 1, "快速", "quick", "check"   | 執行 `python scripts/pattern_detector.py --quick`    |
| 2, "完整", "full", "analysis" | 閱讀 `workflows/execute-analysis.md` 並執行          |
| 3, "視覺化", "chart", "圖表"  | 執行 `python scripts/visualize_pattern.py -o output` |
| 4, "歷史", "事件", "episodes" | 閱讀 `workflows/historical-episodes.md` 並執行       |
| 5, "學習", "方法論", "why"    | 閱讀 `references/methodology.md`                     |
| 6, "自訂", "custom", 提供參數 | 閱讀 `workflows/execute-analysis.md` 並使用參數執行  |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
detect-fed-unamortized-discount-pattern/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── execute-analysis.md            # 完整分析工作流
│   ├── visualize-analysis.md          # 視覺化分析工作流
│   └── historical-episodes.md         # 歷史事件對照工作流
├── references/
│   ├── methodology.md                 # 形狀比對與交叉驗證方法論
│   ├── data-sources.md                # 資料來源與 FRED 系列代碼
│   ├── wudsho-mechanism.md            # WUDSHO 指標機制說明
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── pattern_detector.py            # 主分析腳本
│   ├── visualize_pattern.py           # 視覺化腳本
│   └── fetch_data.py                  # 資料抓取工具
└── examples/
    └── sample_output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 形狀比對方法（相關係數、DTW、形狀特徵）
- 正規化與窗口對齊
- 相似度分數計算
- 交叉驗證邏輯

**資料來源**: references/data-sources.md
- FRED 系列代碼清單
- 資料頻率與延遲
- 公開替代資料說明

**指標機制**: references/wudsho-mechanism.md
- WUDSHO 的成因與解讀
- 利率效果 vs. 壓力效果
- 常見誤讀與反證

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow               | Purpose          | 使用時機               |
|------------------------|------------------|------------------------|
| execute-analysis.md    | 完整形狀比對分析 | 需要完整報告時         |
| visualize-analysis.md  | 視覺化分析       | 需要圖表時             |
| historical-episodes.md | 歷史事件深度分析 | 理解歷史類比與後續發展 |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script               | Command              | Purpose                              |
|----------------------|----------------------|--------------------------------------|
| pattern_detector.py  | `--quick`            | 快速檢查當前狀態                     |
| pattern_detector.py  | `--output FILE`      | 完整分析                             |
| visualize_pattern.py | （無參數）           | Bloomberg 風格視覺化（輸出至專案根目錄 output/） |
| visualize_pattern.py | `--json FILE`        | 使用現有 JSON 結果生成圖表           |
| fetch_data.py        | `--series WUDSHO`    | 抓取 FRED 資料                       |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數               | 類型          | 預設值  | 說明               |
|--------------------|---------------|---------|--------------------|
| target_series      | string        | WUDSHO  | 目標 FRED 系列代碼 |
| baseline_windows   | array[object] | [COVID] | 歷史參考事件窗口   |
| recent_window_days | int           | 120     | 近期比對窗口長度   |
| resample_freq      | string        | W       | 資料頻率           |
| normalize_method   | string        | zscore  | 正規化方法         |

**相似度參數**

| 參數               | 類型          | 預設值                      | 說明         |
|--------------------|---------------|-----------------------------|--------------|
| similarity_metrics | array[string] | [corr, dtw, shape_features] | 相似度指標   |
| alert_thresholds   | object        | {corr_min: 0.7, ...}        | 觸發警報門檻 |

**交叉驗證參數**

| 參數                    | 類型          | 預設值        | 說明               |
|-------------------------|---------------|---------------|--------------------|
| confirmatory_indicators | array[object] | [信用利差...] | 交叉驗證指標清單   |
| lookahead_days          | int           | 60            | 前瞻期（情境敘事） |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "detect-fed-unamortized-discount-pattern",
  "as_of_date": "2026-01-26",
  "target_series": "WUDSHO",
  "best_match": {
    "baseline": "COVID_2020",
    "segment_start": "2020-01-08",
    "segment_end": "2020-06-17",
    "corr": 0.91,
    "dtw": 0.38,
    "feature_sim": 0.82,
    "pattern_similarity_score": 0.88
  },
  "stress_confirmation": {
    "score": 0.22,
    "details": [
      {"name": "credit_spread", "signal": "neutral", "z": 0.4},
      {"name": "equity_vol", "signal": "mild_risk_on", "z": -0.2},
      {"name": "funding_stress_proxy", "signal": "neutral", "z": 0.1}
    ]
  },
  "composite_risk_score": 0.49,
  "interpretation": {
    "summary": "走勢形狀與 COVID 早期片段相似度高，但壓力驗證指標偏中性...",
    "what_to_watch_next_60d": ["..."],
    "rebuttal_to_claim": ["..."]
  },
  "caveats": [
    "形狀相似不代表因果相同；該序列可能強烈受利率、持有期限結構與會計攤銷影響。",
    "若缺乏壓力指標同步惡化，不應把圖形類比直接升級成『黑天鵝預言』。"
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 形狀相似度分數（pattern_similarity_score）
- [ ] 最佳匹配的歷史片段（baseline、segment_start/end）
- [ ] 多維度相似度（corr、dtw、feature_sim）
- [ ] 壓力驗證分數（stress_confirmation_score）
- [ ] 各驗證指標詳情（名稱、訊號、z-score）
- [ ] 合成風險分數（composite_risk_score）
- [ ] 解讀框架（summary、what_to_watch、rebuttal）
- [ ] 資料品質說明與風險警語（caveats）

**視覺化輸出**（使用 visualize_pattern.py，Bloomberg 風格）：

- [ ] 形狀比對與壓力儀表板圖（`fed_unamortized_discount_pattern_YYYY-MM-DD.png`）
  - 上左：近期 vs. 歷史基準窗口的正規化形狀比對
  - 上右：相似度分數面板（corr、DTW、feature_sim、綜合風險）
  - 下左：壓力驗證指標水平條圖（Z-Score）
  - 下右：解讀說明（訊號統計、結論）
- [ ] 歷史走勢總覽圖（`fed_unamortized_discount_history_YYYY-MM-DD.png`）
  - 完整 WUDSHO 歷史走勢
  - 歷史基準窗口標記（COVID_2020、GFC_2008、TAPER_2013、RATE_HIKE_2022）
  - 近期窗口與最佳匹配片段高亮
  - 最新值標註
</success_criteria>
