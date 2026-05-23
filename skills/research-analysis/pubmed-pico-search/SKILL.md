---
name: pubmed-pico-search
description: PICO-based clinical question search. Triggers: PICO, 臨床問題, A比B好嗎, treatment comparison, clinical question, 療效比較
---

# PICO 臨床問題搜尋

## 描述
針對 PICO 格式的臨床問題進行結構化搜尋，自動解析 Population, Intervention, Comparison, Outcome 元素。

## 觸發條件
- 「A 比 B 好嗎？」、「哪個治療效果更好？」
- 「在...病人中...的效果」
- 「...相比...」、「療效比較」
- 提到 PICO、臨床實證、治療指引

---

## PICO 元素說明

| 元素 | 英文 | 說明 | 範例 |
|------|------|------|------|
| **P** | Population | 什麼病人？ | ICU 病人、糖尿病患者 |
| **I** | Intervention | 什麼治療？ | remimazolam、SGLT2 抑制劑 |
| **C** | Comparison | 比較什麼？ | propofol、傳統療法 |
| **O** | Outcome | 什麼結果？ | 譫妄發生率、死亡率 |

---

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: parse_pico(description)                            │
│  → 自動解析臨床問題為 P, I, C, O 元素                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Step 2: generate_search_queries() × 4 (並行)               │
│  → 每個 PICO 元素分別取得 MeSH + 同義詞                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Step 3: 組合 Boolean Query                                 │
│  → (P) AND (I) AND (C) AND (O) + filter                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  Step 4: search_literature() + merge                        │
│  → 執行搜尋並合併結果                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: 解析 PICO

### 自然語言問題：

```python
parse_pico(description="remimazolam 在 ICU 鎮靜比 propofol 好嗎？會減少 delirium 嗎？")
```

### 回傳：

```json
{
  "pico": {
    "P": "ICU patients",
    "I": "remimazolam",
    "C": "propofol",
    "O": "delirium, sedation outcome"
  },
  "question_type": "therapy",
  "suggested_filter": "therapy[filter]",
  "next_steps": [
    "For each PICO element, call generate_search_queries()",
    "Combine with AND logic",
    "Add therapy[filter] for high evidence"
  ]
}
```

### 或者直接提供結構化 PICO：

```python
parse_pico(
    description="",
    p="ICU patients",
    i="remimazolam",
    c="propofol",
    o="delirium"
)
```

---

## Step 2: 擴展每個 PICO 元素（並行！）

```python
# 四個並行呼叫
generate_search_queries(topic="ICU patients")         # → P 材料
generate_search_queries(topic="remimazolam")          # → I 材料
generate_search_queries(topic="propofol")             # → C 材料
generate_search_queries(topic="delirium")             # → O 材料
```

### 回傳範例（I 元素）：

```json
{
  "mesh_terms": [{"preferred": "remimazolam [Supplementary Concept]", "synonyms": ["CNS 7056"]}],
  "all_synonyms": ["CNS 7056", "ONO 2745"]
}
```

---

## Step 3: 組合 Boolean Query

### 高精確度（AND 所有元素）：

```
("Intensive Care Units"[MeSH] OR ICU[tiab])           # P
AND (remimazolam OR "CNS 7056")                        # I
AND (propofol OR Diprivan)                             # C
AND ("Delirium"[MeSH] OR delirium[tiab])              # O
AND therapy[filter]                                    # Evidence filter
```

### 高召回率（放寬 I/C）：

```
(ICU[tiab])                                            # P
AND (remimazolam OR propofol OR "CNS 7056")           # I OR C
AND (delirium[tiab])                                   # O
```

---

## Step 4: 執行搜尋

```python
# 高精確度查詢
search_literature(
    query='("Intensive Care Units"[MeSH] OR ICU[tiab]) AND (remimazolam) AND (propofol) AND (delirium) AND therapy[filter]',
    limit=50
)

# 高召回率查詢
search_literature(
    query='ICU[tiab] AND (remimazolam OR propofol) AND delirium[tiab]',
    limit=50
)

# 合併結果
merge_search_results(results_json='[[...], [...]]')
```

---

## Clinical Query Filters

根據 `question_type` 自動建議篩選器：

| 問題類型 | Filter | 適用情境 |
|----------|--------|----------|
| **therapy** | `therapy[filter]` | 治療效果比較、介入性研究 |
| **diagnosis** | `diagnosis[filter]` | 診斷工具、篩檢準確度 |
| **prognosis** | `prognosis[filter]` | 預後因子、存活率預測 |
| **etiology** | `etiology[filter]` | 危險因子、病因探討 |

這些是 PubMed 內建的 Clinical Query Filters，可大幅提升證據品質！

---

## 完整範例：SGLT2 抑制劑與心衰竭

### 臨床問題：
「在第二型糖尿病合併心衰竭的病人中，SGLT2 抑制劑相比傳統治療，能否減少住院率？」

```python
# Step 1: 解析
pico = parse_pico(
    description="在第二型糖尿病合併心衰竭的病人中，SGLT2 抑制劑相比傳統治療，能否減少住院率？"
)
# P = Type 2 diabetes with heart failure
# I = SGLT2 inhibitors
# C = Traditional therapy
# O = Hospitalization rate

# Step 2: 並行取得各元素的 MeSH
p_materials = generate_search_queries("Type 2 diabetes heart failure")
i_materials = generate_search_queries("SGLT2 inhibitors")
o_materials = generate_search_queries("hospitalization")

# Step 3: 組合查詢
query = '''
("Diabetes Mellitus, Type 2"[MeSH] AND "Heart Failure"[MeSH])
AND ("Sodium-Glucose Transporter 2 Inhibitors"[MeSH] 
     OR empagliflozin OR dapagliflozin OR canagliflozin)
AND ("Hospitalization"[MeSH] OR hospitalization[tiab] OR rehospitalization)
AND therapy[filter]
'''

# Step 4: 搜尋
search_literature(query=query, limit=100, min_year=2018)
```

---

## 小技巧

### 1. 問題類型判斷：

```python
# 治療比較 → therapy
"A 藥比 B 藥好嗎？"

# 診斷準確度 → diagnosis  
"CT 診斷肺癌的敏感度？"

# 預後評估 → prognosis
"這個指數能預測死亡率嗎？"

# 病因研究 → etiology
"抽菸會增加...的風險嗎？"
```

### 2. 沒有 Comparison？

有些問題沒有明確的 C 元素，這很正常：

```python
parse_pico(description="COVID-19 病人使用 remdesivir 的效果")
# P = COVID-19 patients
# I = remdesivir
# C = (empty or placebo)
# O = efficacy/outcomes
```

### 3. 結果太少？

- 移除 C 元素（只搜 P + I + O）
- 移除 filter（但會降低證據品質）
- 使用 `expansion_type="broader"`
