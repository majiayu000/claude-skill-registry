---
name: analyze-us-bank-credit-deposit-decoupling
description: 分析銀行貸款與存款之間的「信貸創造脫鉤」現象，追蹤存款的絕對收縮與回升軌跡，用以辨識聯準會緊縮政策在銀行體系內部的真實傳導效果。
---

<essential_principles>

<principle name="credit_deposit_accounting">
**信貸創造的基本會計邏輯**

傳統銀行體系下，貸款創造存款：
- 銀行發放貸款 → 借款人帳戶增加存款
- 理論上：新增貸款 ≈ 新增存款

當這個關係「脫鉤」時：
- 貸款持續擴張，但存款沒有等比例增加
- 代表有「力量」在抽走體系內的存款
- QT 環境下，資金流向貨幣市場基金、國債等
</principle>

<principle name="deposit_dynamics">
**存款動態的關鍵觀察**

2022-2023 年 QT 週期的關鍵特徵：

1. **存款絕對收縮期**（2022 Q2 - 2023 Q1）
   - 存款累積變化一度下探至 **-1.2 兆美元**
   - 代表存款總量比基期（2022年6月）還少 1.2 兆

2. **存款回升期**（2023 Q2 至今）
   - 存款逐步回升，但仍遠落後貸款增量
   - 當前存款累積變化約 +0.5 兆美元

3. **持續脫鉤**
   - 貸款累積增加約 +2.1 兆美元
   - 落差（Gap）約 1.6 兆美元
</principle>

<principle name="key_metrics">
**核心分析指標**

| 指標                   | 定義                                   | 意義                       |
|------------------------|----------------------------------------|----------------------------|
| 貸款累積變化           | loans(t) - loans(t0)                   | 銀行資產端擴張             |
| 存款累積變化           | deposits(t) - deposits(t0)             | 銀行負債端變化             |
| Decoupling Gap         | 貸款累積變化 - 存款累積變化            | 脫鉤程度                   |
| 存款最大回撤           | min(存款累積變化)                      | 存款收縮最嚴重的程度       |
| 存款回撤恢復比率       | (當前存款變化 - 最低點) / |最低點|     | 存款從低谷回升的程度       |
| Deposit Stress Ratio   | Gap / 貸款累積變化                     | 每單位新增貸款的存款缺口比 |
</principle>

<principle name="data_sources">
**數據來源（FRED 公開 CSV，無需 API Key）**

| 指標         | FRED Series ID   | 說明                                                  | 公開 URL                                              |
|--------------|------------------|-------------------------------------------------------|-------------------------------------------------------|
| 銀行貸款總量 | TOTLL            | Loans and Leases in Bank Credit, All Commercial Banks | https://fred.stlouisfed.org/graph/fredgraph.csv?id=TOTLL |
| 銀行存款總量 | DPSACBW027SBOG   | Deposits, All Commercial Banks                        | https://fred.stlouisfed.org/graph/fredgraph.csv?id=DPSACBW027SBOG |

資料頻率：Weekly（週頻）
對齊方式：以最新共同日期為準
</principle>

</essential_principles>

<objective>
分析銀行信貸與存款的脫鉤現象，追蹤存款的收縮與回升動態。

輸出三層訊號：
1. **Cumulative Changes**: 貸款與存款的累積變化量
2. **Deposit Dynamics**: 存款的最大回撤、回升程度、當前狀態
3. **Decoupling Assessment**: 脫鉤程度評估與宏觀解讀
</objective>

<quick_start>

**最快的方式：使用 FRED 公開 CSV（無需 API Key）**

**Step 1：安裝依賴**
```bash
pip install pandas numpy requests matplotlib
```

**Step 2：執行快速分析**
```bash
cd scripts
python decoupling_analyzer.py --quick
```

**Step 3：執行完整分析（含視覺化）**
```bash
python decoupling_analyzer.py \
  --start 2022-06-01 \
  --output ../../output/decoupling_$(date +%Y-%m-%d).json
```

**Step 4：生成視覺化圖表（Bloomberg 風格面積圖）**
```bash
python visualize_decoupling.py \
  --start 2022-06-01 \
  --output ../../output/credit_deposit_decoupling_$(date +%Y-%m-%d).png
```

**輸出範例**：
```json
{
  "period": "2022-06 to 2026-01",
  "cumulative_changes": {
    "loans_billion_usd": 2070.5,
    "deposits_billion_usd": 506.8,
    "gap_billion_usd": 1563.7
  },
  "deposit_dynamics": {
    "max_drawdown_billion_usd": -1200.0,
    "max_drawdown_date": "2023-04-12",
    "recovery_from_trough_billion_usd": 1706.8,
    "recovery_ratio": 1.42
  },
  "assessment": {
    "decoupling_status": "severe",
    "deposit_stress_ratio": 0.755,
    "phase": "recovery_but_lagging"
  }
}
```

</quick_start>

<intake>
需要進行什麼分析？

1. **快速檢查** - 查看最新的信貸-存款脫鉤狀態
2. **完整分析** - 執行完整分析並生成視覺化圖表
3. **方法論學習** - 了解信貸創造脫鉤的會計邏輯與宏觀意義

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                     | Action                                               |
|------------------------------|------------------------------------------------------|
| 1, "快速", "quick", "check"  | 執行 `python scripts/decoupling_analyzer.py --quick` |
| 2, "完整", "full", "analyze" | 執行完整分析並生成圖表                               |
| 3, "學習", "方法論", "why"   | 閱讀 `references/methodology.md`                     |
| 提供參數 (如日期範圍)        | 使用指定參數執行分析                                 |

**路由後，執行對應腳本並生成視覺化圖表。**
</routing>

<visualization>

**視覺化輸出：信貸-存款脫鉤面積圖**

採用 **Bloomberg Intelligence 風格**，參考 FRED 原生圖表設計：

**圖表特徵**：
1. **面積圖（Area Chart）**：清楚顯示累積變化的體量
2. **藍色面積**：貸款累積變化（Loans & Leases）
3. **紅色面積**：存款累積變化（Deposits）
4. **0 軸線**：清楚標示基準線
5. **數值標註**：最新數值標示在圖表右側

**配色方案（遵循 Bloomberg 規範）**：
- 背景：`#1a1a2e`（深藍黑）
- 貸款面積：`#4a90d9`（藍色）
- 存款面積：`#d94a4a`（紅色）
- 文字：`#ffffff`（白色）
- 網格：`#2d2d44`（暗灰）

**快速繪圖**：
```bash
cd scripts
python visualize_decoupling.py \
  --start 2022-06-01 \
  --output ../../output/credit_deposit_decoupling_YYYY-MM-DD.png
```

**輸出路徑**：`output/credit_deposit_decoupling_YYYY-MM-DD.png`

**圖表解讀**：
- 藍色面積持續擴大 → 銀行持續放貸
- 紅色面積一度為負 → 存款絕對收縮（2022-2023）
- 紅色面積回升但落後藍色 → 脫鉤持續

</visualization>

<input_schema>

<parameter name="start_date" required="true">
**Type**: string (ISO YYYY-MM-DD)
**Description**: 分析起始日期
**Default**: "2022-06-01"
**Example**: "2022-06-01"
</parameter>

<parameter name="end_date" required="false">
**Type**: string (ISO YYYY-MM-DD)
**Description**: 分析結束日期
**Default**: 今天
</parameter>

</input_schema>

<output_schema>
**完整輸出結構**：
```json
{
  "skill": "analyze_bank_credit_deposit_decoupling",
  "version": "2.0.0",
  "status": "success",
  "analysis_period": {
    "start": "2022-06-01",
    "end": "2026-01-07"
  },
  "data_sources": {
    "loans": {
      "series_id": "TOTLL",
      "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=TOTLL"
    },
    "deposits": {
      "series_id": "DPSACBW027SBOG",
      "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DPSACBW027SBOG"
    }
  },
  "cumulative_changes": {
    "loans_billion_usd": 2070.5,
    "deposits_billion_usd": 506.8,
    "gap_billion_usd": 1563.7,
    "gap_trillion_usd": 1.56
  },
  "deposit_dynamics": {
    "max_drawdown_billion_usd": -1200.0,
    "max_drawdown_date": "2023-04-12",
    "current_vs_trough_billion_usd": 1706.8,
    "recovery_ratio": 1.42,
    "phase": "recovery_but_lagging"
  },
  "assessment": {
    "decoupling_status": "severe",
    "deposit_stress_ratio": 0.755,
    "interpretation": "每新增 $1 貸款，僅有 $0.24 形成存款"
  },
  "macro_implication": "銀行信貸與存款出現嚴重脫鉤..."
}
```
</output_schema>

<success_criteria>
分析成功時應產出：

- [ ] 銀行貸款、存款兩個指標的時序數據
- [ ] 累積變化量計算（從基期開始）
- [ ] 存款最大回撤（Maximum Drawdown）及日期
- [ ] 存款回升程度（Recovery Ratio）
- [ ] Decoupling Gap 與 Deposit Stress Ratio
- [ ] **Bloomberg 風格面積圖**（output/credit_deposit_decoupling_YYYY-MM-DD.png）
- [ ] 可操作的宏觀解讀
</success_criteria>

<scripts_index>
| Script                  | Command                   | Purpose                    |
|-------------------------|---------------------------|----------------------------|
| decoupling_analyzer.py  | `--quick`                 | 快速檢查最新訊號           |
| decoupling_analyzer.py  | `--start DATE`            | 完整分析                   |
| visualize_decoupling.py | `--start DATE --output`   | 生成 Bloomberg 風格面積圖  |
</scripts_index>
