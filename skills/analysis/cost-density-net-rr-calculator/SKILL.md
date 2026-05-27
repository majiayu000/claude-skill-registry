---
name: cost-density-net-rr-calculator
description: 計算交易成本對風險報酬比的非線性衰減影響。將固定佣金與點差整合為「成本密度」指標，揭示停損大小與策略效率的雙曲線關係，識別「獲利事件視界」閾值。
---

<essential_principles>
**成本密度模型核心原則**

**1. 核心公式**

所有計算基於以下關係：

```
Cost Density = (c/V + s)           # 成本密度（pips 等效）
x = Cost Density / P               # 負載係數
RR_net = (RR_g - x) / (1 + x)      # 淨風險報酬比
WR_min = (1 + x) / (1 + RR_g)      # 最低勝率
P_critical = CostDensity × (RR_g + 2) / RR_g  # 效率減半點
```

**2. 參數定義**

| 參數 | 定義                      | 單位         |
|------|---------------------------|--------------|
| RR_g | 毛風險報酬比（目標/停損） | 無單位       |
| P    | 停損大小                  | pips/points  |
| c    | 來回佣金（每手）          | 帳戶貨幣     |
| s    | 來回點差                  | pips/points  |
| V    | 每 pip 價值（每手）       | 帳戶貨幣/pip |
| R    | 固定風險（可選，會抵消）  | 帳戶貨幣     |

**3. 關鍵洞察**

- **雙曲線衰減**: P → 0 時，x → ∞，RR_net → -1
- **R 無關性**: RR_net 不依賴固定風險 R
- **剪刀效應**: 短時間框架同時增加成本負擔與降低訊號品質

**4. 單位一致性規則**

- P 和 s 必須使用相同基準（都是 pips 或都是 points）
- c 必須是 round-turn（來回）佣金
- V 必須是每 pip 每手的價值
</essential_principles>

<intake>
**您想要執行什麼操作？**

1. **Compute** - 計算單一參數組合的成本密度與效率指標
2. **Sweep** - 掃描停損範圍，生成 RR_net/WR_min 曲線表
3. **Analyze** - 解讀結果，提供策略建議

**等待回應後再繼續。**
</intake>

<routing>
| Response                             | Workflow             | Description          |
|--------------------------------------|----------------------|----------------------|
| 1, "compute", "calculate", "single"  | workflows/compute.md | 單次計算成本密度指標 |
| 2, "sweep", "grid", "curve", "range" | workflows/sweep.md   | 網格掃描與閾值搜尋   |
| 3, "analyze", "interpret", "explain" | workflows/analyze.md | 結果解讀與策略建議   |

**讀取工作流程後，請完全遵循其步驟。**
</routing>

<reference_index>
**參考文件** (`references/`)

| 文件        | 內容                     |
|-------------|--------------------------|
| formulas.md | 完整公式推導與數學證明   |
| theory.md   | 市場微結構理論背景與文獻 |
</reference_index>

<workflows_index>
| Workflow   | Purpose                    |
|------------|----------------------------|
| compute.md | 單次計算成本密度與效率指標 |
| sweep.md   | 網格掃描與閾值搜尋         |
| analyze.md | 結果解讀與策略建議         |
</workflows_index>

<templates_index>
| Template           | Purpose          |
|--------------------|------------------|
| output-schema.yaml | 輸出 JSON schema |
| input-schema.yaml  | 輸入參數 schema  |
</templates_index>

<scripts_index>
| Script          | Purpose             |
|-----------------|---------------------|
| cost_density.py | Python 計算實作     |
| cost_density.ts | TypeScript 計算實作 |
</scripts_index>

<quick_start>
**快速計算（XAU/USD 範例）：**

輸入：
```json
{
  "RR_g": 3.0,
  "c": 7.0,
  "s": 1.5,
  "V": 10.0,
  "P": 20
}
```

計算：
```python
cost_density = 7.0/10.0 + 1.5  # = 2.2 pips
x = 2.2 / 20                    # = 0.11
RR_net = (3.0 - 0.11) / (1 + 0.11)  # = 2.60
WR_min = (1 + 0.11) / (1 + 3.0)     # = 27.7%
P_critical = 2.2 * (3.0 + 2) / 3.0  # = 3.67 pips
```

輸出：
```json
{
  "cost_density": 2.2,
  "x": 0.11,
  "RR_net": 2.60,
  "WR_min": 0.277,
  "P_critical": 3.67,
  "Loss_RR": 0.133
}
```
</quick_start>

<success_criteria>
Skill 成功執行時：
- [ ] 輸入參數通過驗證（單位一致性）
- [ ] 正確計算 cost_density、x、RR_net、WR_min
- [ ] 識別是否處於高摩擦區（P < P_critical）
- [ ] 輸出符合 outputs_schema
- [ ] 提供 zh-TW 解釋說明
</success_criteria>
