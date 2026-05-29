---
name: google-trends-ath-detector
description: 專注於 Google Trends 數據擷取與分析，使用 Selenium 模擬真人瀏覽器行為抓取數據，自動判定搜尋趨勢是否創下歷史新高（ATH）或出現異常飆升，並提供訊號分型（季節性/事件驅動/結構性轉變）。
---

<essential_principles>
**Google Trends ATH Detector 核心原則**

**1. 模擬真人瀏覽器行為抓取 Google Trends**

本技能使用 Selenium 模擬真人瀏覽器：
- 移除 `navigator.webdriver` 自動化標記
- 隨機輪換 User-Agent（Chrome/Firefox/Safari）
- 請求間隨機延遲（0.5-2 秒）
- 先訪問首頁建立 session，再抓取數據

**2. 訊號分型（Signal Typing）**

搜尋趨勢飆升分為三種類型：

| 類型               | 特徵                 | 解讀                         |
|--------------------|----------------------|------------------------------|
| Seasonal spike     | 每年固定月份重複     | 制度性週期（投保季、報稅季） |
| Event-driven shock | 短期尖峰、z-score 高 | 新聞/政策/突發事件           |
| Regime shift       | 趨勢線上移、持續高位 | 結構性關注上升               |

**3. 分析公式**

```
ATH 判定：latest_value >= max(history) * 0.98
異常判定：zscore >= threshold (default: 2.5)
訊號分型：based on (is_ath, is_anomaly, trend_direction)
```

**4. 描述性分析優先**

本技能提供**客觀的數學分析結果**：
- 輸出訊號類型、異常分數等量化指標
- 提取 related queries 作為驅動因素參考
- 由用戶根據專業知識自行解讀
</essential_principles>

<intake>
**您想要執行什麼操作？**

1. **Detect** - 快速偵測是否創下 ATH 或出現異常
2. **Analyze** - 深度分析訊號類型與驅動因素
3. **Compare** - 比較多個主題的趨勢共振

**等待回應後再繼續。**
</intake>

<routing>
| Response                                  | Workflow             | Description         |
|-------------------------------------------|----------------------|---------------------|
| 1, "detect", "ath", "check", "是否創新高" | workflows/detect.md  | 快速偵測 ATH 與異常 |
| 2, "analyze", "deep", "分析", "訊號"      | workflows/analyze.md | 深度分析與訊號分型  |
| 3, "compare", "對照", "共振"              | workflows/compare.md | 多主題趨勢比較      |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<reference_index>
**參考文件** (`references/`)

| 文件                 | 內容                                       |
|----------------------|--------------------------------------------|
| input-schema.md      | 完整輸入參數定義與預設值                   |
| data-sources.md      | Google Trends 數據來源與 Selenium 爬取指南 |
| signal-types.md      | 訊號分型定義與判定邏輯                     |
| seasonality-guide.md | 季節性分解方法與解讀                       |
</reference_index>

<workflows_index>
| Workflow   | Purpose                      |
|------------|------------------------------|
| detect.md  | 快速偵測 ATH 與異常分數      |
| analyze.md | 深度分析、訊號分型、驅動詞彙 |
| compare.md | 多主題趨勢共振分析           |
</workflows_index>

<templates_index>
| Template           | Purpose              |
|--------------------|----------------------|
| output-schema.yaml | 標準輸出 JSON schema |
</templates_index>

<scripts_index>
| Script           | Purpose                           |
|------------------|-----------------------------------|
| trend_fetcher.py | 核心爬蟲與分析邏輯（Selenium 版） |
</scripts_index>

<examples_index>
**範例輸出** (`examples/`)

| 文件                        | 內容                          |
|-----------------------------|-------------------------------|
| health_insurance_ath.json   | Health Insurance ATH 偵測範例 |
| seasonal_vs_anomaly.json    | 季節性 vs 異常判定範例        |
| multi_topic_comparison.json | 多主題比較範例                |
</examples_index>

<quick_start>
**快速開始：安裝依賴**

```bash
pip install selenium webdriver-manager beautifulsoup4 lxml loguru
```

**Python API：**

```python
from scripts.trend_fetcher import fetch_trends, analyze_ath

# 抓取數據（使用 Selenium 模擬瀏覽器）
data = fetch_trends(
    topic="Health Insurance",
    geo="US",
    timeframe="2004-01-01 2025-12-31"
)

# ATH 分析
result = analyze_ath(data, threshold=2.5)

print(f"Is ATH: {result['analysis']['is_all_time_high']}")
print(f"Signal Type: {result['analysis']['signal_type']}")
print(f"Z-Score: {result['analysis']['zscore']}")
```

**CLI 快速開始：**

```bash
# 基本分析
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --geo US \
  --output ./output/health_insurance.json

# 比較多個主題
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --compare "Unemployment,Inflation" \
  --geo US \
  --output ./output/comparison.json

# 跳過 related queries（更快、更少請求）
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --no-related \
  --output ./output/health_insurance.json

# Debug 模式（顯示瀏覽器、保存 HTML）
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --debug \
  --no-headless

# 登入模式（預設等待 120 秒供 2FA 驗證）
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --output ./output/health_insurance.json

# 跳過登入等待（不需要登入時）
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --login-wait 0 \
  --output ./output/health_insurance.json

# 從已下載的 CSV 檔案分析（跳過瀏覽器抓取）
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --csv ./downloads/multiTimeline.csv \
  --output ./output/health_insurance.json

# 自動從 Downloads 目錄找最新 CSV
python scripts/trend_fetcher.py \
  --topic "Health Insurance" \
  --csv auto \
  --output ./output/health_insurance.json
```

**CLI 參數說明：**

| 參數            | 說明                           | 預設值                |
|-----------------|--------------------------------|-----------------------|
| `--topic`       | 搜尋主題（必要）               | -                     |
| `--geo`         | 地區代碼                       | US                    |
| `--timeframe`   | 時間範圍                       | 2004-01-01 2025-12-31 |
| `--threshold`   | 異常 z-score 門檻              | 2.5                   |
| `--compare`     | 比較主題（逗號分隔）           | -                     |
| `--no-related`  | 跳過 related queries           | false                 |
| `--no-headless` | 顯示瀏覽器視窗                 | false                 |
| `--login`       | 強制啟用登入模式               | false                 |
| `--login-wait`  | 登入等待秒數（0=互動式 Enter） | 120                   |
| `--csv`         | CSV 檔案路徑或 'auto' 自動尋找 | -                     |
| `--debug`       | 啟用調試模式                   | false                 |
| `--output`      | 輸出 JSON 檔案路徑             | -                     |
</quick_start>

<success_criteria>
Skill 成功執行時：
- [ ] Selenium 成功啟動並模擬瀏覽器
- [ ] 正確抓取 Google Trends 時間序列
- [ ] 判定 ATH 狀態與異常分數
- [ ] 識別訊號類型（seasonal/event/regime）
- [ ] 提取 related queries 驅動詞彙（若啟用）
- [ ] 輸出結構化 JSON 結果
</success_criteria>

<anti_detection_strategy>
**防偵測策略摘要**

本技能實現以下防偵測措施（基於 design-human-like-crawler.md）：

| 策略                       | 效果               | 優先級  |
|----------------------------|--------------------|---------|
| 移除 `navigator.webdriver` | 核心，防止 JS 偵測 | 🔴 必要 |
| 隨機 User-Agent            | 避免固定 UA 被識別 | 🔴 必要 |
| 請求前隨機延遲             | 模擬人類行為       | 🔴 必要 |
| 禁用自動化擴展             | 移除 Chrome 痕跡   | 🟡 建議 |
| 先訪問首頁再 API           | 建立正常 session   | 🟡 建議 |

**Chrome 選項配置：**

```python
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
```
</anti_detection_strategy>
