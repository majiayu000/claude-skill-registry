---
name: analyze-investment-clock-rotation
description: 把「獲利成長 × 財務狀況（金融環境）」映射成「投資時鐘」，判斷目前落在哪個象限、近期是順時針還是逆時針旋轉、以及相對於上一輪循環的位置差異。
---

<essential_principles>

<principle name="quadrant_model">
**四象限模型核心**

投資時鐘將市場狀態簡化為四個象限：

```
          金融環境支持（寬鬆）
                ↑
       Q3      │      Q1
     修復過渡   │   理想象限
  ────────────┼────────────→ 獲利成長
       Q4      │      Q2
     最差象限   │   好壞混合
                │
          金融環境不支持（緊縮）
```

| 象限 | 獲利 | 金融環境 | 含義 | 配置建議 |
|------|------|----------|------|----------|
| Q1 理想象限 | ↑ | 支持↑ | 風險資產友善 | 偏多、順風配置 |
| Q2 好壞混合 | ↑ | 不支持↓ | 估值壓力、波動 | 波動管理、估值敏感 |
| Q3 修復過渡 | ↓ | 支持↑ | 寬鬆救市、基本面未回 | 勿誤判為全面牛市 |
| Q4 最差象限 | ↓ | 不支持↓ | 風險資產易受傷 | 風險控管、降槓桿 |
</principle>

<principle name="axis_convention">
**軸向約定（重要！）**

不同來源的投資時鐘圖可能有不同的軸向定義。本 skill 預設：

- **X 軸**：金融環境（Financial Conditions）
  - 左側 = 寬鬆（支持性高）
  - 右側 = 緊縮（支持性低）

- **Y 軸**：獲利成長（Earnings Growth）
  - 上方 = 正成長
  - 下方 = 負成長

**若你的圖表定義不同**，請在輸入參數中調整 `axis_mapping` 和 `clock_convention`。
</principle>

<principle name="clock_hour">
**時鐘點位計算**

透過 `atan2(y, x)` 計算角度，再轉換成 12 小時制：

- 12 點：正上方（獲利最高、金融環境中性）
- 3 點：右側（金融環境最緊）
- 6 點：正下方（獲利最低）
- 9 點：左側（金融環境最寬鬆）

**旋轉方向**：
- 順時針：典型景氣循環路徑（Q1 → Q2 → Q4 → Q3 → Q1）
- 逆時針：政策干預或非典型事件
</principle>

<principle name="data_access">
**資料取得方式**

本 skill 使用**無需 API key** 的資料來源：

- **FRED CSV**: `https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}`
  - 金融環境：NFCI（Chicago Fed）、STLFSI4（St. Louis Fed）
  - 獲利代理：CP（企業利潤）、GDP 相關指標

腳本位於 `scripts/` 目錄，可直接執行。
</principle>

</essential_principles>

<objective>
實作投資時鐘分析：

1. **建構座標**：從 FRED 數據計算獲利成長與金融環境 Z-score
2. **判定象限**：識別當前落在哪個象限
3. **計算點位**：轉換為 12 小時制時鐘點位
4. **分析旋轉**：判斷旋轉方向與幅度
5. **循環比較**：與前一輪循環比較（可選）

輸出：當前象限、時鐘點位、旋轉摘要、配置建議。
</objective>

<quick_start>

**最快的方式：執行預設分析**

```bash
cd skills/analyze-investment-clock-rotation
pip install pandas numpy requests  # 首次使用
python scripts/investment_clock.py --quick
```

輸出範例：
```json
{
  "as_of": "2026-01-15",
  "current_position": {
    "clock_hour": 10,
    "quadrant": "Q1_ideal",
    "earnings_growth": 0.052,
    "financial_conditions_zscore": -0.35
  },
  "interpretation": "理想象限，風險資產相對順風"
}
```

**完整分析**：
```bash
python scripts/investment_clock.py \
  --start 2022-01-01 \
  --end 2026-01-19 \
  --compare-cycle 2020-01-01 2022-12-31 \
  --output result.json
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查** - 查看目前的投資時鐘位置與象限
2. **完整分析** - 分析時間區間內的旋轉路徑與方向
3. **循環比較** - 與前一輪循環比較旋轉特徵
4. **視覺化圖表** - 生成投資時鐘視覺化圖表
5. **方法論學習** - 了解投資時鐘模型的邏輯

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                       | Action                                             |
|--------------------------------|----------------------------------------------------|
| 1, "快速", "quick", "check"    | 執行 `python scripts/investment_clock.py --quick`  |
| 2, "完整", "分析", "full"      | 閱讀 `workflows/analyze.md` 並執行                 |
| 3, "比較", "循環", "compare"   | 閱讀 `workflows/compare-cycle.md` 並執行           |
| 4, "視覺化", "chart", "plot"   | 閱讀 `workflows/visualize.md` 並執行               |
| 5, "學習", "方法論", "why"     | 閱讀 `references/methodology.md`                   |
| 提供參數 (如日期範圍)          | 閱讀 `workflows/analyze.md` 並使用參數執行         |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
analyze-investment-clock-rotation/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元數據
├── workflows/
│   ├── analyze.md                     # 完整分析工作流
│   ├── compare-cycle.md               # 循環比較工作流
│   └── visualize.md                   # 視覺化工作流
├── references/
│   ├── methodology.md                 # 投資時鐘方法論
│   ├── data-sources.md                # FRED 系列代碼與資料來源
│   └── input-schema.md                # 完整輸入參數定義
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
└── scripts/
    ├── investment_clock.py            # 主分析腳本
    ├── fetch_data.py                  # 數據抓取工具
    └── visualize.py                   # 視覺化繪圖工具
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- 投資時鐘概念與歷史
- 四象限定義與配置含義
- 旋轉方向解讀

**資料來源**: references/data-sources.md
- FRED 系列代碼（金融環境/獲利代理）
- 數據頻率與對齊方法

**輸入參數**: references/input-schema.md
- 完整參數定義
- 預設值與建議範圍

</reference_index>

<workflows_index>
| Workflow          | Purpose              | 使用時機               |
|-------------------|----------------------|------------------------|
| analyze.md        | 完整分析             | 需要詳細象限與旋轉分析 |
| compare-cycle.md  | 循環比較             | 比較不同循環的特徵     |
| visualize.md      | 生成視覺化圖表       | 需要圖表展示           |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告模板 |
</templates_index>

<scripts_index>
| Script               | Command                          | Purpose              |
|----------------------|----------------------------------|----------------------|
| investment_clock.py  | `--quick`                        | 快速檢查當前位置     |
| investment_clock.py  | `--start DATE --end DATE`        | 完整分析             |
| investment_clock.py  | `--compare-cycle START END`      | 循環比較             |
| fetch_data.py        | `--series NFCI,CP`               | 抓取 FRED 資料       |
| visualize.py         | `-i result.json -o chart.png`    | 生成視覺化圖表       |
</scripts_index>

<input_schema_summary>

**核心參數**

| 參數                    | 類型   | 預設值           | 說明               |
|-------------------------|--------|------------------|--------------------|
| market                  | string | US_EQUITY        | 分析標的           |
| start_date              | string | 2022-01-01       | 分析起點           |
| end_date                | string | today            | 分析終點           |
| freq                    | string | weekly           | 頻率（weekly/monthly） |

**資料來源參數**

| 參數                    | 類型   | 說明                      |
|-------------------------|--------|---------------------------|
| earnings_series.source  | string | fred / api / csv / manual |
| earnings_series.series_id | string | FRED 序列 ID（如 CP）     |
| earnings_series.growth_method | string | yoy / qoq_annualized  |
| financial_conditions_series.source | string | fred / api / csv |
| financial_conditions_series.series_id | string | NFCI / STLFSI4 |
| financial_conditions_series.transform | string | level / zscore / inverse |

**軸向參數**

| 參數                       | 類型   | 預設值              | 說明                 |
|----------------------------|--------|---------------------|----------------------|
| axis_mapping.x             | string | financial_conditions | X 軸定義            |
| axis_mapping.y             | string | earnings_growth      | Y 軸定義            |
| clock_convention.financial_loose_is_left | bool | true | 寬鬆在左側 |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "analyze-investment-clock-rotation",
  "as_of": "2026-01-19",
  "market": "US_EQUITY",
  "current_state": {
    "clock_hour": 10,
    "quadrant": "Q1_ideal",
    "quadrant_name": "理想象限",
    "x_value": -0.35,
    "y_value": 0.052
  },
  "rotation_summary": {
    "from_hour": 2,
    "to_hour": 10,
    "direction": "clockwise",
    "magnitude_degrees": 240
  },
  "interpretation": "獲利成長為正，金融環境偏支持，屬於風險資產相對順風的象限"
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 當前象限（Q1/Q2/Q3/Q4）
- [ ] 時鐘點位（1-12 點）
- [ ] 獲利成長值與金融環境 Z-score
- [ ] 旋轉方向（順時針/逆時針）
- [ ] 旋轉幅度（度數）
- [ ] 配置建議（依象限）
- [ ] 循環比較摘要（若有啟用）
- [ ] 視覺化圖表（可選，輸出至 `output/` 目錄）
</success_criteria>
