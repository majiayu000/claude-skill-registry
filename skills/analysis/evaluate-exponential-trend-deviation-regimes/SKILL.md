---
name: evaluate-exponential-trend-deviation-regimes
description: 計算資產價格相對長期指數成長趨勢線的偏離度，衡量當前是否處於歷史極端區間，並可選擇性地進行宏觀因子分析以判斷行情體質。
---

<essential_principles>
**資產趨勢偏離度分析 核心原則**

<principle name="exponential_trend_fitting">
**指數趨勢線擬合**
多數資產在長期（數十年）尺度上遵循指數成長路徑。透過對數價格線性回歸（y = a + b*t where y = log(price)）擬合趨勢線，trend = exp(a + b*t)。偏離度 = (price / trend - 1) × 100%。
</principle>

<principle name="historical_context">
**歷史極端對照**
透過計算當前偏離度在歷史分布中的分位數，以及與歷史峰值/谷值的比較，提供市場位置的脈絡。使用者可指定特定日期作為參考點，或由系統自動識別歷史極端值。
</principle>

<principle name="regime_classification">
**行情體質判定（選用）**
針對特定資產（如黃金、股指），可結合宏觀因子進行行情體質分析。不同資產有不同的體質分類框架，使用者可自定義判定規則與因子權重。
</principle>

<principle name="universal_applicability">
**通用適用性**
本技能適用於任何具有長期指數成長特性的資產：商品（黃金、原油）、股票指數、加密貨幣、房地產等。核心邏輯不預設特定資產或歷史峰值。
</principle>
</essential_principles>

<intake>
**您想要執行什麼操作？**

1. **單資產偵測** - 計算單一資產的趨勢偏離度與歷史分位數
2. **歷史對照分析** - 將當前偏離度與使用者指定的歷史日期或自動識別的極端值進行比較
3. **宏觀因子分解** - 詳細拆解各宏觀代理指標對行情體質判定的貢獻（適用於支援的資產類別）

**等待回應後再繼續。**
</intake>

<routing>
| Response                           | Workflow              | Description |
|------------------------------------|-----------------------|-------------|
| 1, "detect", "single", "偵測"      | workflows/detect.md   | 單資產趨勢偏離度偵測與體質判定 |
| 2, "compare", "historical", "對照" | workflows/compare.md  | 歷史峰值詳細對照分析 |
| 3, "macro", "breakdown", "因子"    | workflows/macro.md    | 宏觀因子分解與貢獻度分析 |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<quick_start>
**快速開始**

```bash
# 安裝依賴
pip install pandas numpy yfinance pandas-datareader statsmodels

# 快速偵測（範例：黃金期貨）
cd skills/evaluate-exponential-trend-deviation-regimes
python scripts/trend_deviation.py --symbol GC=F --quick

# 分析其他資產（範例：S&P 500）
python scripts/trend_deviation.py --symbol ^GSPC --start 1950-01-01

# 完整分析（含宏觀因子，目前支援黃金）
python scripts/trend_deviation.py --symbol GC=F --start 1970-01-01 --include-macro

# 指定歷史參考日期
python scripts/trend_deviation.py --symbol GC=F --compare-peaks "2011-09-06,2020-08-07"

# 生成視覺化圖表（輸出 PNG + JSON）
python scripts/generate_chart.py --output ./output/
```
</quick_start>

<reference_index>
**參考文件** (`references/`)

| 文件 | 內容 |
|------|------|
| input-schema.md | 輸入參數詳細定義與驗證規則 |
| methodology.md | 指數趨勢擬合與偏離度計算方法論 |
| regime-rules.md | 1970s-like vs 2000s-like 體質判定規則 |
| data-sources.md | 數據來源與替代方案說明 |
</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| detect.md | 單資產趨勢偏離度偵測與體質判定 |
| compare.md | 歷史峰值詳細對照分析 |
| macro.md | 宏觀因子分解與貢獻度分析 |
</workflows_index>

<templates_index>
| Template | Purpose |
|----------|---------|
| output-json.md | JSON 輸出結構定義 |
| output-markdown.md | Markdown 報告輸出模板 |
</templates_index>

<scripts_index>
| Script | Purpose |
|--------|---------|
| trend_deviation.py | 主要分析腳本：趨勢擬合、偏離度計算、體質判定 |
| generate_chart.py | 視覺化圖表生成：偏離度歷史圖表與峰值標註 |
</scripts_index>

<examples_index>
**範例輸出** (`examples/`)

| 文件 | 內容 |
|------|------|
| gold-deviation-2026.json | 2026 年黃金趨勢偏離度分析範例 |
</examples_index>

<success_criteria>
Skill 成功執行時：
- [ ] 成功擬合黃金價格的指數趨勢線
- [ ] 計算出當前偏離度百分比與歷史分位數
- [ ] 與 2011/1980 峰值進行有效比較
- [ ] 綜合宏觀代理指標得出 regime 判定（1970s-like / 2000s-like）
- [ ] 輸出完整的 JSON 或 Markdown 報告
- [ ] （選用）生成視覺化圖表（PNG）標註歷史峰值與當前位置
</success_criteria>
