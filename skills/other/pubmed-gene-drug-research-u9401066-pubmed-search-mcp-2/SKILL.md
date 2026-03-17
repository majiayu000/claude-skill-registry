---
name: pubmed-gene-drug-research
description: Gene, drug compound, and disease research using NCBI Extended databases. Triggers: 基因, gene, 藥物, drug, compound, PubChem, ClinVar, 變異, variant, 臨床意義
---

# 基因與藥物研究

## 描述
使用 NCBI 擴展資料庫（Gene、PubChem、ClinVar）進行基因功能、藥物化合物、遺傳變異的跨資料庫研究。

## 觸發條件
- 「這個基因的功能是什麼？」
- 「這個藥物的結構/作用機制？」
- 「這個變異的臨床意義？」
- 提到基因名稱（如 BRCA1, TP53）
- 提到藥物化合物名稱
- 提到 ClinVar、遺傳變異

---

## 資料庫概覽

| 資料庫 | 內容 | 用途 |
|--------|------|------|
| **NCBI Gene** | 基因功能、位置、表現 | 基因研究 |
| **PubChem** | 化合物結構、藥理 | 藥物研究 |
| **ClinVar** | 遺傳變異臨床意義 | 遺傳診斷 |

---

## NCBI Gene 工具

### 搜尋基因

```python
search_ncbi_gene(query="BRCA1 breast cancer", limit=10)
```

### 回傳：

```json
{
  "genes": [
    {
      "gene_id": "672",
      "symbol": "BRCA1",
      "name": "BRCA1 DNA repair associated",
      "organism": "Homo sapiens",
      "chromosome": "17",
      "description": "This gene encodes a tumor suppressor...",
      "aliases": ["BRCC1", "FANCS", "RNF53"]
    }
  ]
}
```

### 取得基因詳情

```python
get_ncbi_gene_info(gene_id="672")
```

### 回傳：

```json
{
  "gene_id": "672",
  "symbol": "BRCA1",
  "full_name": "BRCA1 DNA repair associated",
  "chromosome": "17",
  "location": "17q21.31",
  "summary": "This gene encodes a tumor suppressor protein...",
  "function": "DNA double-strand break repair...",
  "pathways": ["Homologous recombination", "DNA damage response"],
  "diseases": ["Breast-ovarian cancer syndrome", "Fanconi anemia"],
  "expression": {
    "tissues": ["breast", "ovary", "testis"],
    "level": "ubiquitous"
  },
  "pubmed_references": ["12345678", "87654321"]
}
```

---

## PubChem 工具

### 搜尋化合物

```python
search_pubchem_compound(query="remimazolam", limit=5)
```

### 回傳：

```json
{
  "compounds": [
    {
      "cid": "11526795",
      "name": "Remimazolam",
      "formula": "C21H19BrN4O2",
      "molecular_weight": 439.3,
      "iupac_name": "methyl 3-[(4S)-8-bromo-1-methyl-6-(2-pyridinyl)...",
      "synonyms": ["CNS-7056", "ONO-2745"]
    }
  ]
}
```

### 取得化合物詳情

```python
get_pubchem_compound_info(cid="11526795")
```

### 回傳：

```json
{
  "cid": "11526795",
  "name": "Remimazolam",
  "formula": "C21H19BrN4O2",
  "molecular_weight": 439.3,
  "structure": {
    "canonical_smiles": "CN1C(=O)CN=C(C2=CC=CC=N2)...",
    "inchi": "InChI=1S/C21H19BrN4O2/..."
  },
  "pharmacology": {
    "mechanism": "GABA-A receptor positive allosteric modulator",
    "drug_class": "Benzodiazepine",
    "therapeutic_use": "Procedural sedation, general anesthesia"
  },
  "properties": {
    "logP": 2.5,
    "hydrogen_bond_donors": 0,
    "hydrogen_bond_acceptors": 4,
    "rotatable_bonds": 5
  },
  "related_pubmed": ["30217674", "28523456"]
}
```

---

## ClinVar 工具

### 搜尋變異

```python
search_clinvar(query="BRCA1 pathogenic", limit=20)
```

### 回傳：

```json
{
  "variants": [
    {
      "variation_id": "17661",
      "gene": "BRCA1",
      "variant_name": "NM_007294.4:c.5266dupC",
      "hgvs": "p.Gln1756Profs*74",
      "clinical_significance": "Pathogenic",
      "condition": "Hereditary breast and ovarian cancer syndrome",
      "review_status": "★★★★ (reviewed by expert panel)"
    }
  ]
}
```

### 取得變異詳情

```python
get_clinvar_variation(variation_id="17661")
```

### 回傳：

```json
{
  "variation_id": "17661",
  "gene": "BRCA1",
  "variant": {
    "hgvs_c": "NM_007294.4:c.5266dupC",
    "hgvs_p": "p.Gln1756Profs*74",
    "variant_type": "frameshift",
    "consequence": "loss of function"
  },
  "clinical": {
    "significance": "Pathogenic",
    "review_status": "reviewed by expert panel",
    "last_evaluated": "2023-06-15"
  },
  "conditions": [
    {
      "name": "Hereditary breast and ovarian cancer syndrome",
      "medgen_id": "C0677776",
      "inheritance": "Autosomal dominant"
    }
  ],
  "population_frequency": {
    "gnomAD": 0.00001,
    "note": "Rare variant"
  },
  "evidence": {
    "pubmed_references": ["12345678", "23456789"],
    "functional_studies": "Loss of BRCT domain function"
  }
}
```

---

## 跨資料庫研究流程

### 情境：研究 BRCA1 基因與藥物標靶

```python
# Step 1: 基因資訊
gene_info = get_ncbi_gene_info(gene_id="672")  # BRCA1

# Step 2: 相關文獻
search_literature(
    query=f'"{gene_info["symbol"]}"[Gene] AND drug target',
    limit=20
)

# Step 3: 相關化合物（靶向藥物）
search_pubchem_compound(query="BRCA1 inhibitor", limit=10)

# Step 4: 臨床相關變異
search_clinvar(query="BRCA1 pathogenic", limit=50)
```

---

## 藥物研究流程

### 情境：研究新藥的作用機制和相關研究

```python
# Step 1: 化合物資訊
compound = get_pubchem_compound_info(cid="11526795")  # remimazolam

# Step 2: 相關基因（藥物標靶）
search_ncbi_gene(query="GABA receptor", limit=10)

# Step 3: 臨床文獻
search_literature(
    query=f'"{compound["name"]}" mechanism action',
    limit=30
)

# Step 4: 藥物比較
search_literature(
    query=f'"{compound["name"]}" versus midazolam',
    limit=20
)
```

---

## 遺傳變異研究流程

### 情境：評估某個變異的臨床意義

```python
# Step 1: 搜尋變異
variants = search_clinvar(query="NM_007294.4:c.5266dupC")

# Step 2: 取得詳細資訊
variant_details = get_clinvar_variation(variation_id="17661")

# Step 3: 相關基因功能
gene_info = get_ncbi_gene_info(gene_id="672")

# Step 4: 相關文獻
search_literature(
    query=f'BRCA1 c.5266dupC pathogenic',
    limit=20
)

# Step 5: 類似變異
search_clinvar(query="BRCA1 frameshift pathogenic", limit=30)
```

---

## 藥物基因組學研究

### 情境：研究藥物與基因變異的關係

```python
# Step 1: 藥物資訊
drug = search_pubchem_compound(query="warfarin")

# Step 2: 相關代謝基因
cyp_genes = search_ncbi_gene(query="CYP2C9 warfarin metabolism")

# Step 3: 影響藥效的變異
variants = search_clinvar(query="CYP2C9 drug response")

# Step 4: 藥物基因組學文獻
search_literature(
    query="warfarin CYP2C9 pharmacogenomics",
    limit=30
)
```

---

## 整合報告範例

### 基因報告

```markdown
## BRCA1 基因報告

### 基本資訊
- **基因符號**: BRCA1
- **位置**: 17q21.31
- **功能**: DNA 雙股斷裂修復

### 相關疾病
- 遺傳性乳癌卵巢癌症候群
- Fanconi 貧血

### 關鍵變異 (ClinVar)
| 變異 | 臨床意義 | 審查狀態 |
|------|----------|----------|
| c.5266dupC | Pathogenic | ★★★★ |
| c.68_69del | Pathogenic | ★★★★ |

### 相關文獻
- PMID: 12345678 - "BRCA1 and DNA repair..."
- PMID: 87654321 - "Hereditary breast cancer..."
```

### 藥物報告

```markdown
## Remimazolam 藥物報告

### 基本資訊
- **CID**: 11526795
- **分子式**: C21H19BrN4O2
- **分子量**: 439.3 g/mol

### 藥理學
- **機轉**: GABA-A 受體正向異位調節劑
- **藥物分類**: 苯二氮平類
- **適應症**: 程序性鎮靜、全身麻醉

### 相關文獻
- PMID: 30217674 - "Phase 3 RCT..."
- PMID: 35678901 - "Real-world experience..."
```

---

## 小技巧

### 1. 基因搜尋技巧

```python
# 使用官方基因符號
search_ncbi_gene(query="TP53")  # ✅
search_ncbi_gene(query="p53 protein")  # ⚠️ 可能找到多個

# 加入物種限制
search_ncbi_gene(query="BRCA1 human")
```

### 2. 化合物搜尋技巧

```python
# 使用 CID 最準確
get_pubchem_compound_info(cid="11526795")

# 商品名搜尋
search_pubchem_compound(query="Lipitor")  # atorvastatin
```

### 3. 變異命名法

```python
# HGVS 標準命名
search_clinvar(query="NM_007294.4:c.5266dupC")

# 蛋白質變異
search_clinvar(query="BRCA1 p.Gln1756Profs")

# 基因 + 臨床意義
search_clinvar(query="BRCA1 pathogenic")
```
