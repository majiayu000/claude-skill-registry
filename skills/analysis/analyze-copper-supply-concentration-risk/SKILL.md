---
name: analyze-copper-supply-concentration-risk
description: 用公開資料量化「銅供應是否過度集中、主要產地是否結構性衰退、替代增量是否依賴少數國家」，並輸出可行的中期供應風險結論與情境推演。
---

<essential_principles>

<principle name="narrative_to_metrics">
**敘事轉指標（Narrative to Metrics）**

市場敘事必須可量化驗證。三大命題對應三組指標：

| 命題 | 核心問題 | 量化指標 |
|------|----------|----------|
| A. 集中度 | 供應是否過度集中？ | CR4, CR5, 份額排名 |
| B. 結構衰退 | 智利是否結構性衰退？ | 峰值年份、峰值回撤 |
| C. 替代依賴 | 是否依賴秘魯/DRC？ | 秘魯+DRC 合計份額 vs 智利份額 |

**注意**：由於 MacroMicro 只提供 5 個國家的細分數據，HHI 指標不適用於本分析。
</principle>

<principle name="data_source">
**數據來源：MacroMicro (WBMS)**

唯一主要來源，使用 Chrome CDP **全自動**抓取 Highcharts 圖表數據。

- URL: https://en.macromicro.me/charts/91500/wbms-copper-mine-production-total-world
- 口徑: mined copper content（礦場產量的銅金屬含量）
- 可用序列: World, Chile, Peru, DRC, China, US
</principle>

</essential_principles>

<objective>
分析全球銅供應的國家集中度與結構性風險。

輸出兩層分析：
1. **Concentration**: 國家份額排名、CR4/CR5
2. **Chile vs Replacers**: 智利 vs 新興替代國（Peru + DRC）份額對比
</objective>

<quick_start>

**全自動執行（無需手動操作 Chrome）**

**Step 1：安裝依賴**
```bash
pip install requests websocket-client pandas numpy matplotlib
```

**Step 2：一鍵抓取數據（自動啟動/關閉 Chrome）**
```bash
cd scripts
python fetch_copper_production.py
```

腳本會自動：
- 啟動 Chrome 調試模式
- 等待頁面載入（~40 秒）
- 提取 Highcharts 數據
- 儲存到 `cache/copper_production.csv`
- 關閉 Chrome

**Step 3：生成 Bloomberg 風格視覺化圖表**
```bash
python visualize_copper_concentration.py
```

**輸出**：`output/copper_concentration.png`

</quick_start>

<intake>
需要進行什麼分析？

1. **快速圖表** - 直接生成 Bloomberg 風格集中度圖表
2. **完整分析** - 1970 年至今的集中度趨勢分析（含數據表）
3. **智利趨勢** - 智利產量份額與峰值回撤分析
4. **替代評估** - 秘魯+DRC 替代依賴度分析

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response | Action |
|----------|--------|
| 1, "快速", "圖表", "chart" | `python scripts/fetch_copper_production.py && python scripts/visualize_copper_concentration.py` |
| 2, "完整", "trend", "1970" | 抓取數據後輸出完整年度數據表 |
| 3, "智利", "chile" | 分析智利份額趨勢與峰值 |
| 4, "替代", "replacement", "秘魯", "drc" | 分析 Peru+DRC 是否已超越智利 |

**路由後，執行對應命令。**
</routing>

<directory_structure>
```
analyze-copper-supply-concentration-risk/
├── SKILL.md                              # 本文件（路由器）
├── skill.yaml                            # 前端展示元數據
├── scripts/
│   ├── fetch_copper_production.py        # 全自動 CDP 數據爬蟲
│   └── visualize_copper_concentration.py # Bloomberg 風格視覺化
├── cache/
│   ├── copper_production.csv             # 數據快取
│   └── copper_production_cache.json      # 原始 JSON 快取
└── output/
    └── copper_concentration.png          # 輸出圖表
```
</directory_structure>

<scripts_index>
| Script | Command | Purpose |
|--------|---------|---------|
| fetch_copper_production.py | `python fetch_copper_production.py` | 全自動 CDP 抓取（自動啟動/關閉 Chrome） |
| fetch_copper_production.py | `--force-refresh` | 強制重新抓取（忽略快取） |
| fetch_copper_production.py | `--start-year 1970` | 指定起始年份 |
| visualize_copper_concentration.py | `python visualize_copper_concentration.py` | 生成 Bloomberg 風格圖表 |
| visualize_copper_concentration.py | `--output path/to/output.png` | 指定輸出路徑 |
</scripts_index>

<visualization>

**視覺化輸出：Bloomberg 風格銅供應集中度儀表板**

包含兩張圖（上下排列）：
1. **國家份額堆疊面積圖**：Chile, Peru, DRC, China, US, Others
2. **智利 vs 新興替代國**：Chile vs Peru+DRC 份額對比，標記交叉點

**配色**：Bloomberg 深色主題
- 背景: `#1a1a2e`
- Chile: `#ff6b35` (橙紅)
- Peru: `#00bfff` (天藍)
- DRC: `#00ff88` (綠)
- Peru+DRC: `#00d4aa` (青綠)

**快速繪圖**：
```bash
cd scripts
python visualize_copper_concentration.py
```

**輸出路徑**：`output/copper_concentration.png`

</visualization>

<output_example>
**2023 年關鍵指標**：

| 國家 | 份額 |
|------|------|
| Chile | 23.5% |
| Peru + DRC | 25.2% |
| China | 7.5% |
| US | 5.0% |

**關鍵發現**：
- 智利份額峰值：37.2% (2004)
- 智利當前份額：23.5% (2023)
- 峰值回撤：13.7pp
- **2023 年 Peru+DRC 首次超越智利**（份額逆轉）
</output_example>

<success_criteria>
分析成功時應產出：

- [x] 數據已從 MacroMicro **全自動**抓取並快取
- [x] 國家份額排名（Chile, Peru, DRC, China, US, Others）
- [x] 智利峰值年份與回撤分析
- [x] 秘魯+DRC 替代趨勢
- [x] **Bloomberg 風格視覺化圖表**
- [x] 明確標註數據來源
</success_criteria>
