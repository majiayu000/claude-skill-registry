---
name: analyze-jgb-insurer-superlong-flow
description: 從日本保險公司對超長期（10年以上）JGB 的淨買賣時間序列，自動產出「本月是否創紀錄淨賣出、連續淨賣出月數、期間累積淨賣出」等結論。
---

# 分析日本保險公司超長期 JGB 淨買賣流量 Skill

以 JSDA 公開數據驗證「保險公司創紀錄賣超長端國債」等敘事，提供可複製的摘要（含 streak / record / 累積值）。

<essential_principles>

<principle name="jsda_data_source">
**核心數據來源：JSDA 公社債店頭売買高（Trading Volume of OTC Bonds）**

日本證券業協會（JSDA）自 2018/05 起將投資人別交易統計整併進「Trading Volume of OTC Bonds」資料集。

**數據位置**：
- 當前財年：https://www.jsda.or.jp/shiryoshitsu/toukei/tentoubaibai/koushasai.xlsx
- 歷史財年：https://www.jsda.or.jp/shiryoshitsu/toukei/tentoubaibai/koushasai{YYYY}.xlsx

**關鍵 Sheet**：
- `(Ｊ)合計差引` - 淨買賣額（Sell - Purchase）

**數據特徵**：
- 頻率：月度
- 分類：投資人類型 × 債券類型 × 天期桶
- 單位：億日圓（100 million yen）
- 延遲：約 T+1 個月

**注意**：2018/05 前的舊版「Trends in Bond Transactions (by investor type)」已停止更新。
</principle>

<principle name="sign_convention">
**符號慣例（重要！）**

JSDA 使用「賣出 - 買入」作為差引計算方式：

```
net_sale = 賣出金額 - 買入金額
```

- **正值 = 淨賣出**（賣出 > 買入，需求減少）
- **負值 = 淨買入**（買入 > 賣出，需求增加）

這與部分新聞報導的符號相反，需特別注意。
</principle>

<principle name="maturity_bucket_mapping">
**天期桶口徑對齊**

JSDA Excel 欄位結構（第 4 列）：

| JSDA 欄位 | 英文 | 說明 |
|-----------|------|------|
| 超長期 | Interest-bearing Long-term (over 10-year) | 10 年以上利付債 |
| 利付長期 | Interest-bearing Long-term | 5-10 年利付債 |
| 利付中期 | Interest-bearing Medium-term | 2-5 年利付債 |
| 割引 | Zero-Coupon | 零息債 |
| 国庫短期証券等 | Treasury Discount Bills | 短期國庫券 |

**本 Skill 使用**：`超長期`（對應新聞常見的「10+ years」或「super-long」口徑）
</principle>

<principle name="investor_mapping">
**投資人分類**

| JSDA 分類 | 英文 | 說明 |
|-----------|------|------|
| 生保・損保 | Life & Non-Life Insurance Companies | 壽險 + 產險合計 |
| 都市銀行 | City Banks | 大型商業銀行 |
| 地方銀行 | Regional Banks | 區域性銀行 |
| 信託銀行 | Trust Banks | 含年金管理 |
| 外国人 | Foreigners | 海外投資者 |

**本 Skill 使用**：`生保・損保`（保險公司合計）
</principle>

<principle name="record_detection">
**歷史極值判斷邏輯**

```python
record_high = max(series)  # 最大淨賣出（正值最大）
is_record_sale = (latest == record_high) AND (latest > 0)
```

**注意事項**：
- 數據起點會影響「歷史紀錄」的判定，輸出必須說明樣本期間
- 若僅為近期極值，需標註「近 N 個月新高」
</principle>

</essential_principles>

<objective>
驗證「日本保險公司創紀錄賣超長端 JGB」等敘事，並提供：
1. **本月淨賣出/買入**：最新月份數值（億日圓）
2. **是否創紀錄**：判斷是否為樣本最大淨賣出（正值最大）
3. **連續淨賣出月數**：streak_len
4. **本輪累積淨賣出**：cum_over_streak
5. **Z-score 與分位數**：相對歷史的極端程度
</objective>

<quick_start>

**最快的方式：執行快速分析**

```bash
cd .claude/skills/analyze-jgb-insurer-superlong-flow
pip install pandas numpy openpyxl  # 首次使用
python scripts/jsda_flow_analyzer.py --quick
```

**輸出範例**（2025/12 實測結果）：

```markdown
## 日本保險公司超長期 JGB 淨買賣驗證報告

**分析期間**：2022-04 ~ 2025-12（45 個月）

### 核心結論

| 指標 | 數值 | 說明 |
|------|------|------|
| 本月（2025-12）| **8,224 億日圓** | 淨賣出 |
| 是否創歷史紀錄 | **✓ 是** | 全樣本 (45 個月) |
| 連續淨賣出月數 | **5 個月** | 自 2025-08 起 |
| 本輪累積淨賣出 | **13,959 億日圓** | 1.40 兆日圓 |

### Headline Takeaways

1. ✓ 驗證屬實：日本保險公司在 2025/12 創下歷史最大單月淨賣出
2. 已連續 5 個月淨賣出超長期國債，累積 1.40 兆日圓
3. 當前淨賣出規模處於歷史極端區間（Z-score: 2.71）
```

**完整分析（含歷史比較）**：
```bash
python scripts/jsda_flow_analyzer.py --full --format json
```

**強制重新下載數據**：
```bash
python scripts/jsda_flow_analyzer.py --quick --refresh
```

</quick_start>

<intake>
您想要執行什麼操作？

1. **快速檢查** - 查看最新月份的淨買賣與連續淨賣出狀態
2. **完整分析** - 執行完整的歷史比較與極值判斷
3. **驗證新聞** - 輸入新聞的數字，對比 JSDA 原始數據
4. **JSON 輸出** - 輸出結構化 JSON 供後續處理

**請選擇或直接執行分析。**
</intake>

<routing>
| Response                        | Action                              |
|---------------------------------|-------------------------------------|
| 1, "快速", "quick", "check"     | `python scripts/jsda_flow_analyzer.py --quick` |
| 2, "完整", "full", "analyze"    | `python scripts/jsda_flow_analyzer.py --full`  |
| 3, "驗證", "verify", "新聞"     | 讀取 workflows/verify-claim.md      |
| 4, "json", "JSON"               | `python scripts/jsda_flow_analyzer.py --format json` |
</routing>

<input_schema>

<parameter name="--quick" required="false">
**Type**: flag
**Description**: 快速檢查模式（使用快取數據）
</parameter>

<parameter name="--full" required="false">
**Type**: flag
**Description**: 完整分析模式
</parameter>

<parameter name="--start-year" required="false" default="2018">
**Type**: int
**Description**: 起始財年（日本財年 4 月開始）
</parameter>

<parameter name="--lookback" required="false">
**Type**: int
**Description**: 回溯月數（預設全樣本）
</parameter>

<parameter name="--format" required="false" default="markdown">
**Type**: string
**Options**: `json` | `markdown`
**Description**: 輸出格式
</parameter>

<parameter name="--refresh" required="false">
**Type**: flag
**Description**: 強制重新下載數據
</parameter>

<parameter name="--output" required="false">
**Type**: string
**Description**: 輸出檔案路徑
</parameter>

</input_schema>

<output_schema>

**JSON 輸出結構**：
```json
{
  "skill": "analyze_jgb_insurer_superlong_flow",
  "version": "1.0.0",
  "as_of": "2026-01-26",
  "data_source": {
    "name": "JSDA Trading Volume of OTC Bonds (公社債店頭売買高)",
    "url": "https://www.jsda.or.jp/shiryoshitsu/toukei/tentoubaibai/",
    "sheet": "(Ｊ)合計差引"
  },
  "parameters": {
    "investor_group": "life_and_nonlife_insurance",
    "investor_label": "生保・損保 (Life & Non-Life Insurance Companies)",
    "maturity_bucket": "super_long",
    "maturity_label": "超長期 (Interest-bearing Long-term over 10-year)",
    "sign_convention": "正值=淨賣出 (Sell-Purchase), 負值=淨買入",
    "unit": "100 million yen (億円)"
  },
  "analysis_period": {
    "start": "2022-04",
    "end": "2025-12",
    "months": 45
  },
  "latest_month": {
    "date": "2025-12",
    "net_sale_100m_yen": 8224,
    "net_sale_trillion_yen": 0.8224,
    "interpretation": "淨賣出"
  },
  "record_analysis": {
    "is_record_sale": true,
    "record_sale_100m_yen": 8224,
    "record_sale_date": "2025-12",
    "record_purchase_100m_yen": -8889,
    "record_purchase_date": "2023-03",
    "lookback_period": "全樣本 (45 個月)"
  },
  "streak_analysis": {
    "consecutive_net_sale_months": 5,
    "streak_start": "2025-08",
    "cumulative_net_sale_100m_yen": 13959,
    "cumulative_net_sale_trillion_yen": 1.3959
  },
  "historical_stats": {
    "mean_100m_yen": -2025,
    "std_100m_yen": 3785,
    "latest_zscore": 2.71,
    "latest_percentile": 0.9778
  },
  "headline_takeaways": [
    "✓ 驗證屬實：日本保險公司在 2025/12 創下歷史最大單月淨賣出（8,224 億日圓）",
    "已連續 5 個月淨賣出超長期國債，累積金額 13,959 億日圓（1.40 兆日圓）",
    "當前淨賣出規模處於歷史極端區間（Z-score: 2.71，超過 2 個標準差）"
  ]
}
```
</output_schema>

<reference_index>
**參考文件** (`references/`)

| 文件              | 內容                                     |
|-------------------|------------------------------------------|
| data-sources.md   | JSDA 數據來源與 XLS 下載說明             |
| methodology.md    | 計算方法論（streak、record、cumulative） |
</reference_index>

<scripts_index>
| Script                 | Command       | Purpose            |
|------------------------|---------------|--------------------|
| jsda_flow_analyzer.py  | `--quick`     | 快速檢查           |
| jsda_flow_analyzer.py  | `--full`      | 完整分析           |
| jsda_flow_analyzer.py  | `--refresh`   | 強制重新下載數據   |
</scripts_index>

<success_criteria>
Skill 成功執行時：

- [x] 輸出最新月份淨賣出/買入數值
- [x] 判斷是否為歷史極值（含回溯期間說明）
- [x] 計算連續淨賣出月數與累積金額
- [x] 明確標示天期桶與投資人口徑
- [x] 提供 Z-score 與分位數
- [x] 可操作的 headline takeaways
</success_criteria>

<directory_structure>
```
analyze-jgb-insurer-superlong-flow/
├── SKILL.md                           # 本文件（主入口）
├── skill.yaml                         # 前端展示元數據
├── workflows/
│   ├── quick-check.md                 # 快速檢查工作流
│   ├── full-analysis.md               # 完整分析工作流
│   └── verify-claim.md                # 驗證新聞工作流
├── references/
│   ├── data-sources.md                # 資料來源說明
│   └── methodology.md                 # 方法論與公式
├── scripts/
│   └── jsda_flow_analyzer.py          # 主分析腳本（含數據下載）
└── data/
    └── cache/                         # 自動緩存目錄（.gitignore）
```
</directory_structure>
