---
name: nickel-concentration-risk-analyzer
description: 以全球鎳供給結構為核心，量化各國的主導程度（例如印尼）、主要礦區供給量、以及政策配額/減產情境對全球供需平衡與價格非對稱的影響。
---

<essential_principles>
**鎳供給集中度分析 核心原則**

<principle name="unit_enforcement">
**口徑先行（Unit Enforcement）**

所有分析必須先確定口徑，不同口徑會導致數量級差異：

| 口徑            | 說明                        | 典型數值差異 |
|-----------------|-----------------------------|--------------|
| `t_Ni_content`  | 鎳金屬含量（本 Skill 預設） | 基準值       |
| `t_ore_wet`     | 礦石濕噸                    | 可達 50-100x |
| `t_NPI_product` | NPI 產品噸                  | 約 10-15% Ni |
| `t_matte`       | 鎳鋶噸                      | 約 75% Ni    |

**強制規則**：
- 若輸入數據口徑不明確，必須標記為 `model_estimate`
- 同一分析中不得混用不同口徑數據
- 輸出必須包含 `unit` 欄位
</principle>

<principle name="supply_type_clarity">
**供給類型區分（Supply Type Clarity）**

鎳供給鏈各階段必須分開計算：

```
Mine Production (mined) → Intermediate (NPI/Matte/MHP) → Refined (class1/class2)
```

- **mined**: 礦場產量（鎳金屬含量）
- **refined**: 精煉產量（含冶煉）
- 「印尼 60% 市佔」通常指 **mined nickel content**
</principle>

<principle name="data_tiering">
**數據分層策略（Data Tiering）**

| Tier | 特性                 | 來源           | 用途               |
|------|----------------------|----------------|--------------------|
| 0    | 免費、穩定、口徑一致 | USGS MCS, INSG | Baseline 主幹      |
| 1    | 免費但分散、需整合   | 公司年報、財報 | Mine-level 錨點    |
| 2    | 付費、更即時完整     | S&P Global MI  | 精度驗證、對齊口徑 |
| 3    | 政策/配額近期訊息    | 新聞、官方公告 | 情境輸入           |

**優先順序**：Tier 0 建立 baseline → Tier 1 補充 mine-level → Tier 2 驗證精度
</principle>

<principle name="execution_probability">
**政策執行機率（Execution Probability）**

政策減產不需 100% 執行即可造成衝擊。預設模型：

```python
expected_cut = cut_value * execution_prob  # 預設 execution_prob = 0.5
```

三層輸出：
- **Hard cut**: 政策完全落地
- **Half success**: 執行 50%（或指定值）
- **Soft landing**: 只延遲投產/只砍新增產能
</principle>

<principle name="concentration_metrics">
**集中度指標定義**

| 指標            | 公式                         | 解讀                     |
|-----------------|------------------------------|--------------------------|
| Country Share   | `country_prod / global_prod` | 單國佔比                 |
| CR_n            | `Σ top_n_share`              | 前 N 國/礦集中度         |
| HHI             | `Σ share²`                   | 市場集中度（0-10000）    |
| Policy Leverage | `cut_amount / global_prod`   | 政策可撬動的全球供給比例 |

HHI 判讀：< 1500 低集中、1500-2500 中等、> 2500 高集中
</principle>
</essential_principles>

<intake>
**您想要執行什麼操作？**

1. **Analyze** - 分析全球鎳供給結構與集中度指標（CR_n, HHI, country share）
2. **Scenario** - 模擬政策/減產情境對供給的衝擊（RKAB配額、出口限制等）
3. **Validate** - 驗證市場說法的數據口徑與來源可靠度
4. **Ingest** - 從各數據源擷取並標準化鎳供給數據

**等待回應後再繼續。**
</intake>

<routing>
| Response                                                | Workflow                      | Description          |
|---------------------------------------------------------|-------------------------------|----------------------|
| 1, "analyze", "concentration", "share", "hhi", "集中度" | workflows/analyze.md          | 供給結構與集中度分析 |
| 2, "scenario", "policy", "cut", "減產", "情境", "RKAB"  | workflows/scenario-engine.md  | 政策情境衝擊模擬     |
| 3, "validate", "verify", "check", "驗證", "來源"        | workflows/validate-sources.md | 數據來源與口徑驗證   |
| 4, "ingest", "fetch", "data", "抓取", "擷取"            | workflows/ingest.md           | 數據擷取與標準化     |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<reference_index>
**參考文件** (`references/`)

| 文件                          | 內容                       |
|-------------------------------|----------------------------|
| data-sources.md               | 所有數據來源詳細說明與 URL |
| unit-conversion.md            | 單位轉換規則與假設         |
| concentration-metrics.md      | 集中度指標詳細計算方法     |
| indonesia-supply-structure.md | 印尼鎳供給結構與關鍵園區   |
| mine-level-anchors.md         | 主要礦區/園區產量錨點      |
| failure-modes.md              | 失敗模式與緩解策略         |
</reference_index>

<workflows_index>
| Workflow            | Purpose                                  |
|---------------------|------------------------------------------|
| analyze.md          | 供給結構與集中度分析（CR_n, HHI, share） |
| scenario-engine.md  | 政策情境衝擊模擬                         |
| validate-sources.md | 數據來源與口徑驗證                       |
| ingest.md           | 數據擷取與標準化                         |
</workflows_index>

<templates_index>
| Template           | Purpose           |
|--------------------|-------------------|
| output-json.md     | JSON 輸出結構模板 |
| output-markdown.md | Markdown 報告模板 |
| config.yaml        | 分析參數配置模板  |
| data-schema.yaml   | 數據 Schema 定義  |
</templates_index>

<scripts_index>
| Script                   | Purpose                |
|--------------------------|------------------------|
| nickel_pipeline.py       | 核心數據管線           |
| ingest_sources.py        | 數據來源擷取           |
| compute_concentration.py | 集中度指標計算         |
| scenario_impact.py       | 情境衝擊模擬           |
| visualize_concentration.py | 集中度分析視覺化圖表 |
| visualize_scenario.py    | 情境衝擊視覺化圖表     |
</scripts_index>

<quick_start>
**CLI 快速開始：**

```bash
# 分析當前全球鎳供給集中度
python scripts/nickel_pipeline.py analyze --asof=2026-01-16 --scope=mined

# 生成集中度視覺化圖表（輸出到 output/ 目錄，檔名包含日期）
python scripts/visualize_concentration.py

# 模擬印尼減產 20% 的情境衝擊
python scripts/nickel_pipeline.py scenario --cut=20 --target=Indonesia --exec-prob=0.5

# 生成情境衝擊視覺化圖表
python scripts/visualize_scenario.py

# 驗證「印尼 60% 市佔」的數據來源
python scripts/nickel_pipeline.py validate --claim="Indonesia 60% share"
```

**Library 快速開始：**

```python
from nickel_pipeline import NickelConcentrationAnalyzer

analyzer = NickelConcentrationAnalyzer(
    asof_date="2026-01-16",
    scope={"supply_type": "mined", "unit": "t_Ni_content"},
    data_level="free_nolimit"
)

# 計算集中度指標
result = analyzer.compute_concentration()
print(f"Indonesia share: {result['indonesia_share_2024']:.1%}")
print(f"HHI: {result['hhi_2024']:.0f}")
```
</quick_start>

<success_criteria>
Skill 成功執行時：
- [ ] 正確識別數據口徑（mined/refined/nickel content）
- [ ] 輸出包含 unit 欄位標註
- [ ] 集中度指標計算正確（share, CR_n, HHI）
- [ ] 情境分析輸出三層結果（hard/half/soft）
- [ ] 數據來源可追溯（source_id, confidence）
- [ ] 單位警告正確觸發（ore vs content）
</success_criteria>

<input_schema>
**輸入參數定義**

```yaml
# 必要參數
asof_date: string (ISO)  # 分析基準日
horizon:
  history_start_year: int
  history_end_year: int
  forecast_end_year: int

# 範圍參數
scope:
  supply_type: string  # mined | refined | nickel_content (必填)
  product_group: string  # class1 | class2 | NPI | matte | MHP | mixed (選填)
  countries: array[string]  # 預設: Indonesia, Philippines, Russia, Canada, Australia, Other

# 情境參數 (scenario workflow 專用)
policy_scenarios:
  - name: string
    target_country: string  # 預設: Indonesia
    policy_variable: string  # ore_quota_RKAB | mine_permit | export_rule | smelter_capacity
    cut_type: string  # pct_global | pct_country | absolute
    cut_value: number
    start_year: int
    end_year: int
    execution_prob: number  # 0-1, 預設 0.5

# 數據等級
data_level: string  # free_nolimit | free_limit | paid_low | paid_high
```
</input_schema>

<data_pipeline_architecture>
**數據流水線架構**

```
[Data Sources]
     |
     v
+-------------------+
|   ingest_sources  |  --> Tier 0: USGS, INSG
+-------------------+      Tier 1: Company reports
     |                     Tier 2: S&P Global (optional)
     v
+-------------------+
|   normalize       |  --> 統一 schema + 單位標註
+-------------------+      (year, country, supply_type, value, unit, source_id)
     |
     v
+-------------------+
| compute_concentration | --> share, CR_n, HHI
+-------------------+
     |
     v
+-------------------+
|   scenario_impact |  --> expected_cut, global_hit_pct
+-------------------+
     |
     v
+-------------------+
|   generate_output |  --> JSON + Markdown
+-------------------+
     |
     v
[Analysis Result]
```

**標準化欄位 Schema：**

| 欄位          | 類型   | 說明                                     |
|---------------|--------|------------------------------------------|
| year          | int    | 年度                                     |
| country       | string | 國家                                     |
| supply_type   | string | mined/refined                            |
| product_group | string | NPI/matte/MHP/class1...                  |
| value         | float  | 數值                                     |
| unit          | string | t_Ni_content / t_ore_wet / t_NPI_product |
| source_id     | string | USGS/INSG/S&P/Company/Other              |
| confidence    | float  | 來源品質評分 (0-1)                       |
</data_pipeline_architecture>
