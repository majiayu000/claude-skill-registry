---
name: lithium-supply-demand-gap-radar
description: 將鋰產業鏈（礦端 → 精煉化學品 → 電池與終端需求），整合為一套可運算的替代指標；再把這些指標映射到鋰主題 ETF（如 LIT）的成分暴露與長期價格走勢，形成可供決策的依據。 
---

<essential_principles>
**鋰產業鏈供需雷達 核心原則**

<principle name="supply_chain_layers">
**供應鏈分層（Supply Chain Layers）**

鋰產業鏈必須分層分析，不可混為一談：

```
Mining → Processing → Battery
(礦端)   (化學品)    (終端需求)
```

| 層級                 | 代表數據                 | 典型延遲  |
|----------------------|--------------------------|-----------|
| Upstream (礦端)      | 鋰礦產量、出口量         | 年度/季度 |
| Midstream (化學品)   | 碳酸鋰/氫氧化鋰價格      | 週度/日度 |
| Downstream (電池/EV) | EV 銷量、電池裝機量(GWh) | 月度      |

**強制規則**：
- 供給分析需指定層級（礦端 vs 精煉端）
- 需求 proxy 需明確轉換假設（kWh → kg Li）
- 價格分析需區分碳酸鋰 vs 氫氧化鋰
</principle>

<principle name="data_level_fallback">
**數據等級與備援策略（Data Level Fallback）**

根據 `data_level` 參數自動選擇數據源：

| data_level     | 價格數據             | 供需數據           | 可靠度 |
|----------------|----------------------|--------------------|--------|
| `free_nolimit` | CME 期貨/Proxy 指數  | USGS/IEA/澳洲政府  | 中     |
| `free_limit`   | SMM/Fastmarkets 頁面 | + 公司財報         | 中高   |
| `paid_low`     | SMM 完整序列         | + Benchmark 基本   | 高     |
| `paid_high`    | Fastmarkets API      | + S&P/BNEF/WoodMac | 最高   |

**強制規則**：
- 價格數據不足時，使用 CME 合約或相關股籃子作為 proxy
- 需在輸出中標註實際使用的數據等級
</principle>

<principle name="li_content_conversion">
**鋰含量轉換（Li Content Conversion）**

電池需求到鋰需求的轉換必須明確假設：

| 假設場景 | kg Li / kWh | 備註                |
|----------|-------------|---------------------|
| 保守估計 | 0.12        | 含 LFP 佔比上升假設 |
| 中性估計 | 0.15        | 混合 NMC/LFP        |
| 積極估計 | 0.18        | 高鎳 NMC 主導       |

```python
li_demand_kt = battery_gwh * kg_per_kwh * 1000  # 單位: kt LCE
```

**強制規則**：
- 需求估計必須輸出三個情境（保守/中性/積極）
- 輸出需包含 `kg_per_kwh_assumption` 欄位
</principle>

<principle name="regime_classification">
**價格型態分類（Price Regime Classification）**

鋰價週期分為四個階段：

| Regime      | 特徵                         | 交易含義           |
|-------------|------------------------------|--------------------|
| `downtrend` | 12-26 週動能 < 0, 斜率 < 0   | 空頭主導，避免做多 |
| `bottoming` | 動能收斂，波動下降，均值回歸 | 觀望，等待確認     |
| `uptrend`   | 動能 > 0, 斜率 > 0           | 做多視窗開啟       |
| `overheat`  | 動能極端正值，波動放大       | 獲利了結風險       |

**指標組合**：
- 12 週 / 26 週動能（ROC）
- 趨勢斜率（線性回歸）
- 波動率（ATR / 標準差）
- 均值回歸強度（距 MA 偏離度）
</principle>

<principle name="etf_transmission">
**ETF 傳導敏感度（ETF Transmission）**

ETF 對鋰價的敏感度受持股結構影響：

| 持股類型          | 對鋰價 Beta | 波動特性            |
|-------------------|-------------|---------------------|
| Upstream (礦業)   | 1.5 - 2.5   | 高槓桿、高波動      |
| Midstream (精煉)  | 0.8 - 1.2   | 跟隨但有加工費緩衝  |
| Downstream (電池) | 0.3 - 0.8   | 受競爭/技術路線影響 |

**計算公式**：
```python
ETF_beta_li = Σ(weight_i * beta_i_to_lithium)
```

**強制規則**：
- 需計算 rolling beta（建議 52 週滾動）
- 傳導斷裂判斷：beta < 0.3 且持續 > 8 週
</principle>
</essential_principles>

<intake>
**您想要執行什麼操作？**

1. **Full Analysis** - 完整供需×價格×傳導整合分析（生成完整報告）
2. **Balance Nowcast** - 僅計算供需平衡即時估計（缺口擴大/縮小）
3. **Price Regime** - 僅分析價格型態與週期位置
4. **ETF Exposure** - 僅分析 ETF 持股結構與鋰價敏感度
5. **Ingest Data** - 從各數據源擷取並標準化數據

**等待回應後再繼續。**
</intake>

<routing>
| Response                                          | Workflow                     | Description                |
|---------------------------------------------------|------------------------------|----------------------------|
| 1, "full", "analyze", "完整", "報告", "LIT"       | workflows/full-analysis.md   | 完整供需×價格×傳導整合分析 |
| 2, "balance", "nowcast", "供需", "缺口", "gap"    | workflows/balance-nowcast.md | 供需平衡即時估計           |
| 3, "price", "regime", "價格", "週期", "型態"      | workflows/price-regime.md    | 價格型態與週期分析         |
| 4, "etf", "exposure", "holding", "傳導", "敏感度" | workflows/etf-exposure.md    | ETF 暴露與傳導分析         |
| 5, "ingest", "data", "fetch", "抓取", "擷取"      | workflows/ingest.md          | 數據擷取與標準化           |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<reference_index>
**參考文件** (`references/`)

| 文件                      | 內容                               |
|---------------------------|------------------------------------|
| data-sources.md           | 所有數據來源詳細說明與 URL         |
| unit-conversion.md        | 單位轉換規則（LCE/Li/GWh）         |
| price-methodology.md      | 價格數據方法學（Fastmarkets/SMM）  |
| etf-holdings-structure.md | LIT 持股結構與產業鏈分段           |
| supply-chain-mapping.md   | 鋰供應鏈完整映射（礦→化學品→電池） |
| failure-modes.md          | 失敗模式與緩解策略                 |
</reference_index>

<workflows_index>
| Workflow           | Purpose                    |
|--------------------|----------------------------|
| full-analysis.md   | 完整供需×價格×傳導整合分析 |
| balance-nowcast.md | 供需平衡即時估計           |
| price-regime.md    | 價格型態與週期分析         |
| etf-exposure.md    | ETF 持股暴露與傳導分析     |
| ingest.md          | 數據擷取與標準化           |
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
| Script                    | Purpose                  |
|---------------------------|--------------------------|
| lithium_pipeline.py       | 核心數據管線             |
| ingest_sources.py         | 數據來源擷取             |
| compute_balance.py        | 供需平衡計算             |
| classify_regime.py        | 價格型態分類             |
| compute_etf_beta.py       | ETF 傳導敏感度計算       |
| visualize_analysis.py     | 分析結果綜合視覺化       |
| inflection_point_chart.py | **拐點分析專用視覺化** ⭐ |
</scripts_index>

<quick_start>
**CLI 快速開始：**

```bash
# 完整分析 LIT ETF（預設 10 年回看、週度頻率）
python scripts/lithium_pipeline.py analyze --ticker=LIT --lookback=10 --freq=weekly

# 僅計算供需平衡 Nowcast
python scripts/lithium_pipeline.py balance --asof=2026-01-16

# 分析價格型態（碳酸鋰 + 氫氧化鋰）
python scripts/lithium_pipeline.py regime --chem=both

# 計算 ETF 對鋰價的傳導敏感度
python scripts/lithium_pipeline.py etf-beta --ticker=LIT --window=52

# ✨ 生成視覺化圖表（完整儀表板）
python scripts/visualize_analysis.py
# 輸出：output/lithium_analysis_YYYY-MM-DD.png
```

**視覺化輸出**：
- 📊 6合1 專業儀表板（18" × 12"，300 DPI）
- 📁 自動保存至 `output/` 目錄
- 📅 檔名包含當天日期
- 🎨 完整中文支持

**Library 快速開始：**

```python
from lithium_pipeline import LithiumSupplyDemandRadar

radar = LithiumSupplyDemandRadar(
    etf_ticker="LIT",
    lookback_years=10,
    price_freq="weekly",
    chem_focus="both",
    data_level="free_nolimit"
)

# 完整分析
result = radar.full_analysis()
print(f"Balance Index: {result['balance_index']:.2f}")
print(f"Price Regime: {result['price_regime']}")
print(f"ETF Beta to Li: {result['etf_beta_li']:.2f}")
print(f"Thesis: {result['thesis']}")
```
</quick_start>

<success_criteria>
Skill 成功執行時：
- [ ] 正確識別數據等級並使用對應來源
- [ ] 供需平衡指數計算正確（含三情境）
- [ ] 價格型態分類明確（downtrend/bottoming/uptrend/overheat）
- [ ] ETF 傳導敏感度計算正確（rolling beta）
- [ ] 輸出包含完整的失效條件（invalidation）
- [ ] 數據來源可追溯（source_id, data_level）
- [ ] 單位轉換假設明確標註
- [ ] **視覺化圖表已生成且符合規格**（300 DPI, PNG, 檔名含日期）
- [ ] **報告與圖表在 output/ 目錄下一起輸出**
</success_criteria>

<input_schema>
**輸入參數定義**

```yaml
# 必要參數
etf_ticker: string      # 目標 ETF（預設 LIT）
lookback_years: int     # 回看年限（建議 10-15）
price_freq: string      # weekly | daily（建議 weekly）

# 範圍參數
region_focus:           # 供應/需求重點區（選填）
  - China
  - Australia
  - Chile
  - Argentina
  - US
  - EU

chem_focus: string      # carbonate | hydroxide | both（預設 both）

# 數據等級
data_level: string      # free_nolimit | free_limit | paid_low | paid_high

# 數據源開關
sources:
  usgs: boolean
  iea_ev_outlook: boolean
  australia_req: boolean
  abs_exports: boolean
  fastmarkets: boolean
  smm: boolean
  etf_holdings: boolean

# 輸出格式
output_format: string   # markdown | json（預設 markdown）
```
</input_schema>

<data_pipeline_architecture>
**數據流水線架構**

```
[Data Sources]
     |
     v
+--------------------+
|   ingest_sources   |  --> USGS, IEA, Australia REQ/ABS
+--------------------+      Fastmarkets/SMM (方法學/價格)
     |                      Global X LIT factsheet
     v
+--------------------+
|   normalize        |  --> 統一 schema + 單位標註
+--------------------+
     |
     +-------------------+-------------------+
     |                   |                   |
     v                   v                   v
+-----------+    +-----------+    +-----------+
| supply_   |    | price_    |    | etf_      |
| demand    |    | series    |    | holdings  |
+-----------+    +-----------+    +-----------+
     |                   |                   |
     v                   v                   v
+-----------+    +-----------+    +-----------+
| balance_  |    | classify_ |    | compute_  |
| nowcast   |    | regime    |    | etf_beta  |
+-----------+    +-----------+    +-----------+
     |                   |                   |
     +-------------------+-------------------+
                         |
                         v
              +--------------------+
              |   generate_insight |  --> Thesis + Targets + Invalidation
              +--------------------+
                         |
                         v
              +--------------------+
              |   format_output    |  --> JSON + Markdown
              +--------------------+
```

**標準化欄位 Schema：**

| 欄位        | 類型   | 說明                         |
|-------------|--------|------------------------------|
| date        | date   | 數據日期                     |
| metric_type | string | supply/demand/price/etf      |
| metric_name | string | 具體指標名稱                 |
| value       | float  | 數值                         |
| unit        | string | kt_LCE/USD_per_kg/GWh/pct    |
| region      | string | 國家/區域                    |
| source_id   | string | USGS/IEA/SMM/Fastmarkets/etc |
| data_level  | string | 數據等級                     |
| confidence  | float  | 來源品質評分 (0-1)           |
</data_pipeline_architecture>
