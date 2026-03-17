---
name: input-normalizer
description: |
  3つの入力モード（薬剤起点/PICO起点/CQ起点）を統一フォーマットに変換し、
  後続のRWD研究企画スキルが利用できる構造化データを生成する。
allowed-tools:
  - Read
context: normal
---

# Input Normalizer Skill

## 目的
多様な入力形式（薬剤名、PICO、臨床的疑問）を受け付け、RWD研究企画に必要な統一フォーマットに変換する。

## 入力モード

### Mode 1: drug（薬剤起点）
製薬企業からの依頼や特定薬剤の調査に使用。

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| drug | Yes | 対象薬剤（一般名） | daratumumab |
| indication | Yes | 対象疾患/適応 | multiple myeloma |
| country | Yes | 対象国/地域 | Japan |
| sponsor | No | 依頼元企業 | Janssen |

### Mode 2: pico（PICO起点）
構造化されたリサーチクエスチョンがある場合に使用。

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| population | Yes | 対象集団 | 高齢frail NDMM患者（75歳以上、ECOG PS 2-3） |
| intervention | Yes | 介入/曝露 | DRd療法（daratumumab + lenalidomide + dexamethasone） |
| comparator | Yes | 比較対照 | VRd療法 または 標準治療 |
| outcome | Yes | 評価項目 | PFS, OS, 奏効率, Grade3以上有害事象 |
| country | Yes | 対象国 | Japan |
| timeframe | No | 追跡期間 | 24ヶ月 |

### Mode 3: clinical_question（CQ起点）
臨床現場からの素朴な疑問を構造化する場合に使用。

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| question | Yes | 自然言語の臨床的疑問 | 高齢者でダラツムマブは本当に有効？副作用は許容範囲？ |
| country | Yes | 対象国 | Japan |
| context | No | 追加コンテキスト | 外来化学療法、通院困難な患者が多い |

## 変換ロジック

### Mode: drug → 統一フォーマット

```
入力: drug=daratumumab, indication=NDMM, country=Japan

変換処理:
1. 薬剤情報から一般的な比較対照を推論
   - daratumumab → VRd, KRd, Rd などが比較対照候補
2. 適応から対象集団を詳細化
   - NDMM → 新規診断多発性骨髄腫患者
3. 一般的なアウトカムを設定
   - 有効性: PFS, OS, ORR, CR率
   - 安全性: 有害事象発生率、治療中止率
4. 代表的なRQを3-5個生成
```

### Mode: pico → 統一フォーマット

```
入力: population, intervention, comparator, outcome

変換処理:
1. intervention から薬剤名を抽出
   - "DRd療法" → drug=daratumumab
2. population から適応を推論
   - "NDMM患者" → indication=newly diagnosed multiple myeloma
3. 入力されたPICOをそのまま構造化
4. PICO要素からRQを文章化
```

### Mode: clinical_question → 統一フォーマット

```
入力: question="高齢者でダラツムマブは本当に有効？副作用は許容範囲？"

変換処理:
1. 固有名詞・薬剤名の抽出
   - ダラツムマブ → drug=daratumumab
2. 対象集団のキーワード抽出
   - 高齢者 → population要素
3. 疑問の種類を分類
   - 有効性 vs 安全性 vs 両方
4. PICO形式に分解
5. 複数の具体的RQに展開
```

## 出力フォーマット

```json
{
  "input_mode": "drug | pico | clinical_question",
  "normalized": {
    "drug": {
      "generic_name": "daratumumab",
      "brand_name": "ダラザレックス",
      "class": "抗CD38モノクローナル抗体",
      "sponsor": "Janssen"
    },
    "indication": {
      "name": "newly diagnosed multiple myeloma",
      "name_ja": "新規診断多発性骨髄腫",
      "icd10": "C90.0",
      "subtype": null
    },
    "country": "Japan",
    "pico": {
      "population": {
        "description": "新規診断多発性骨髄腫患者",
        "inclusion_criteria": [
          "NDMM診断確定",
          "初回治療",
          "年齢18歳以上"
        ],
        "exclusion_criteria": [
          "他の悪性腫瘍合併",
          "重篤な臓器障害"
        ],
        "subgroups": [
          "高齢者（75歳以上）",
          "移植非適応",
          "frail患者"
        ]
      },
      "intervention": {
        "name": "DRd療法",
        "components": ["daratumumab", "lenalidomide", "dexamethasone"],
        "regimen": "標準用量"
      },
      "comparator": {
        "primary": "VRd療法",
        "alternatives": ["Rd療法", "実臨床での標準治療"]
      },
      "outcome": {
        "primary": ["PFS"],
        "secondary": ["OS", "ORR", "CR率", "MRD陰性率"],
        "safety": ["Grade3以上有害事象", "治療中止率", "感染症"]
      }
    },
    "research_questions": [
      {
        "id": "RQ1",
        "type": "comparative_effectiveness",
        "question": "NDMM患者において、DRd療法はVRd療法と比較してPFSを延長するか？",
        "priority": "high"
      },
      {
        "id": "RQ2",
        "type": "safety",
        "question": "日本人NDMM患者におけるDRd療法の安全性プロファイルは？",
        "priority": "high"
      },
      {
        "id": "RQ3",
        "type": "subgroup",
        "question": "高齢frail患者（75歳以上）でDRd療法の有効性・安全性は維持されるか？",
        "priority": "medium"
      }
    ],
    "study_type_suggestions": [
      {
        "type": "comparative_cohort",
        "description": "DRd vs VRd の比較コホート研究",
        "feasibility": "high"
      },
      {
        "type": "descriptive",
        "description": "DRd実臨床での使用実態・アウトカム記述研究",
        "feasibility": "high"
      },
      {
        "type": "subgroup_analysis",
        "description": "高齢・frail患者でのサブグループ解析",
        "feasibility": "medium"
      }
    ],
    "ehr_rwd_relevance": {
      "lab_values_needed": ["M蛋白", "遊離軽鎖", "血清クレアチニン", "ヘモグロビン"],
      "narrative_extraction": ["効果判定", "有害事象", "治療変更理由"],
      "jmdc_mdv_gap": "検査値による奏効評価、経過記録からの詳細AE情報はクレームDBでは不可"
    }
  },
  "metadata": {
    "normalized_at": "2025-01-18T12:00:00Z",
    "confidence": {
      "drug_extraction": 1.0,
      "pico_inference": 0.85,
      "rq_relevance": 0.9
    }
  }
}
```

## 変換例

### 例1: drug モード

**入力:**
```
mode: drug
drug: pembrolizumab
indication: NSCLC
country: Japan
```

**出力（抜粋）:**
```json
{
  "normalized": {
    "drug": {"generic_name": "pembrolizumab"},
    "indication": {"name": "non-small cell lung cancer"},
    "pico": {
      "population": {"description": "進行・再発NSCLC患者"},
      "intervention": {"name": "pembrolizumab単剤または併用"},
      "comparator": {"primary": "化学療法"},
      "outcome": {"primary": ["PFS", "OS"]}
    },
    "research_questions": [
      {"question": "PD-L1高発現NSCLCにおけるpembrolizumab単剤の実臨床での有効性は？"},
      {"question": "日本人NSCLCにおけるirAEの発生頻度と管理状況は？"}
    ]
  }
}
```

### 例2: clinical_question モード

**入力:**
```
mode: clinical_question
question: "透析患者にレンバチニブは使えるのか？減量基準は？"
country: Japan
```

**出力（抜粋）:**
```json
{
  "normalized": {
    "drug": {"generic_name": "lenvatinib"},
    "indication": {"name": "hepatocellular carcinoma / thyroid cancer"},
    "pico": {
      "population": {"description": "透析患者（腎機能障害）を有する肝細胞癌/甲状腺癌患者"},
      "intervention": {"name": "lenvatinib"},
      "comparator": {"primary": "未治療 or 他のTKI"},
      "outcome": {"primary": ["治療継続率", "用量調整パターン", "有害事象"]}
    },
    "research_questions": [
      {"question": "透析患者におけるlenvatinibの至適開始用量は？"},
      {"question": "腎機能障害患者でのlenvatinib減量・中止率は？"},
      {"question": "透析患者でのlenvatinib投与例における有効性は維持されるか？"}
    ]
  }
}
```

## 注意事項

1. **薬剤名の正規化**: 商品名→一般名への変換、略称の展開を行う
2. **適応の確認**: 承認適応外の組み合わせの場合は警告を出力
3. **曖昧性の明示**: 推論に不確実性がある場合はconfidenceスコアを下げる
4. **多言語対応**: 日本語入力も適切に処理
5. **後続スキルへの連携**: 出力JSONは全ての後続スキルで参照可能

## エラーハンドリング

| エラー | 対処 |
|--------|------|
| 薬剤名が特定できない | ユーザーに確認を求める |
| 適応が曖昧 | 候補リストを提示して選択を求める |
| PICOが不完全 | 欠損要素を推論で補完し、confidence低下を明示 |
| 矛盾する入力 | 警告を出力し、優先ルールに従って処理 |
