---
name: phenotype-lab-spec
description: |
  研究対象集団・アウトカムのフェノタイプ定義と検査値活用仕様を作成する。
  コンピューター実行可能なアルゴリズム形式で記述し、バリデーション計画を含める。
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - mcp__plugin_pubmed_PubMed__search_articles
context: normal
---

# Phenotype & Lab Specification Skill

## 目的
研究対象集団（曝露、アウトカム、共変量）をEHRデータから正確に同定するためのコンピューター実行可能なフェノタイプ定義と検査値活用仕様を作成する。

## 入力パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| PHENOTYPE_NAME | Yes | フェノタイプ名 | NDMM TIE patient |
| DRUG | Yes | 対象薬剤 | daratumumab |
| INDICATION | Yes | 対象疾患 | multiple myeloma |
| PHENOTYPE_TYPE | Yes | 種類 | population/exposure/outcome/covariate |
| REFERENCE_DEFINITION | No | 参照定義（ガイドライン等） | IMWG criteria |

## フェノタイプ定義フレームワーク

### 1. 対象集団フェノタイプ（Population Phenotype）

#### 構成要素
```
Population Phenotype =
  Disease Phenotype ∩
  Eligibility Criteria ∩
  Exclusion Criteria
```

#### 疾患フェノタイプ定義テンプレート
```yaml
disease_phenotype:
  name: "{INDICATION}"
  definition:
    primary:
      - type: diagnosis_code
        codes:
          - ICD10: ["C90.0", "C90.00", "C90.01", "C90.02"]
        timeframe: "any time before index"
        occurrence: ">= 1"
    supporting:
      - type: medication
        drug_class: "myeloma_agents"
        timeframe: "any time"
      - type: lab_value
        test: "M_protein"
        value: "> 0"
  validation:
    ppv_target: ">= 0.80"
    sensitivity_target: ">= 0.70"
```

### 2. 曝露フェノタイプ（Exposure Phenotype）

#### New User定義テンプレート
```yaml
exposure_phenotype:
  name: "{DRUG}_new_user"
  definition:
    exposure:
      - type: prescription
        drug: "{DRUG}"
        first_occurrence: true
    washout_period:
      duration: "365 days"
      no_prior: "{DRUG}"
    index_date: "first_prescription_date"
  regimen_identification:
    method: "concurrent_meds_window"
    window: "7 days"
    components:
      DRd: [daratumumab, lenalidomide, dexamethasone]
      DVd: [daratumumab, bortezomib, dexamethasone]
      VRd: [bortezomib, lenalidomide, dexamethasone]
```

### 3. アウトカムフェノタイプ（Outcome Phenotype）

#### イベントベース定義テンプレート
```yaml
outcome_phenotype:
  name: "progression_free_survival"
  definition:
    event:
      type: "composite"
      components:
        - name: "disease_progression"
          criteria:
            - lab_based:
                test: "M_protein"
                change: ">= 25% increase from nadir"
            - clinical:
                source: "progress_notes"
                keywords: ["PD", "progression", "増悪", "進行"]
        - name: "death"
          criteria:
            - type: "death_record"
    censoring:
      - "end_of_follow_up"
      - "treatment_switch"
      - "loss_to_follow_up"
```

### 4. 共変量フェノタイプ（Covariate Phenotype）

#### カテゴリ別定義テンプレート
```yaml
covariate_phenotypes:
  demographics:
    age:
      source: "patient_demographics"
      calc: "index_date - birth_date"
    sex:
      source: "patient_demographics"

  disease_characteristics:
    iss_stage:
      source: "lab_values + clinical_notes"
      definition:
        stage_I: "β2MG < 3.5 AND Alb >= 3.5"
        stage_II: "NOT stage_I AND NOT stage_III"
        stage_III: "β2MG >= 5.5"
      lab_window: "-30 to 0 days from index"

    cytogenetic_risk:
      source: "clinical_summary"
      extraction: "NLP"
      high_risk_markers: ["del(17p)", "t(4;14)", "t(14;16)", "gain1q"]

  comorbidities:
    renal_impairment:
      source: "lab_values"
      definition:
        severe: "eGFR < 30"
        moderate: "eGFR >= 30 AND eGFR < 60"
        mild: "eGFR >= 60 AND eGFR < 90"
        normal: "eGFR >= 90"
      lab_window: "-30 to 0 days from index"

  frailty:
    ecog_ps:
      source: "progress_notes"
      extraction: "NLP"
      keywords: ["PS", "ECOG", "パフォーマンスステータス"]
      values: [0, 1, 2, 3, 4]
```

## 検査値活用仕様

### 検査値マッピング
```yaml
lab_specifications:
  - standard_name: "hemoglobin"
    local_codes: ["HB", "Hb", "ヘモグロビン"]
    unit: "g/dL"
    normal_range: [12.0, 18.0]
    clinical_thresholds:
      severe_anemia: "< 8.0"
      moderate_anemia: "8.0 - 10.0"
      mild_anemia: "10.0 - 12.0"

  - standard_name: "eGFR"
    local_codes: ["eGFR", "推算GFR"]
    unit: "mL/min/1.73m2"
    calculation: "CKD-EPI or MDRD"
    clinical_thresholds:
      G5: "< 15"
      G4: "15 - 29"
      G3b: "30 - 44"
      G3a: "45 - 59"
      G2: "60 - 89"
      G1: ">= 90"

  - standard_name: "beta2_microglobulin"
    local_codes: ["β2MG", "β2-MG", "B2M"]
    unit: "mg/L"
    clinical_thresholds:
      elevated: "> 3.5"
      high: "> 5.5"
```

### 時系列検査値の処理
```yaml
lab_time_series:
  baseline_value:
    window: "-30 to 0 days from index"
    selection: "closest to index"
    missing_handling: "extend window to -60 days"

  longitudinal_values:
    frequency: "all available"
    time_points: "relative to index date"
    aggregation:
      - method: "last value carried forward"
      - method: "time-weighted average"

  derived_measures:
    nadir:
      definition: "minimum value during treatment"
    change_from_baseline:
      definition: "(current - baseline) / baseline * 100"
    time_to_event:
      definition: "first time threshold crossed"
```

## 出力フォーマット

```markdown
# Phenotype Specification: {PHENOTYPE_NAME}

## 1. メタデータ

| 項目 | 値 |
|------|-----|
| フェノタイプ名 | {PHENOTYPE_NAME} |
| 種類 | {PHENOTYPE_TYPE} |
| バージョン | v1.0 |
| 作成日 | YYYY-MM-DD |
| 参照定義 | {REFERENCE_DEFINITION} |

## 2. コンピューター実行可能定義

### 2.1 対象集団定義
```yaml
[YAML形式のフェノタイプ定義]
```

### 2.2 曝露定義
```yaml
[YAML形式の曝露定義]
```

### 2.3 アウトカム定義
```yaml
[YAML形式のアウトカム定義]
```

### 2.4 共変量定義
```yaml
[YAML形式の共変量定義]
```

## 3. 検査値仕様

### 3.1 使用検査項目一覧
| 検査項目 | ローカルコード | 単位 | 用途 |
|----------|---------------|------|------|
| ... | ... | ... | ... |

### 3.2 検査値閾値
| 検査項目 | 閾値 | 臨床的意義 |
|----------|------|-----------|
| ... | ... | ... |

### 3.3 時系列処理仕様
```yaml
[YAML形式の時系列処理仕様]
```

## 4. NLP/テキスト抽出仕様

### 4.1 経過記録からの抽出
| 抽出情報 | キーワード/パターン | バリデーション方法 |
|----------|-------------------|------------------|
| ECOG PS | "PS[0-4]", "ECOG", "パフォーマンス" | 手動レビュー100例 |
| 奏効評価 | "CR", "VGPR", "PR", "SD", "PD" | 検査値との照合 |

### 4.2 サマリーからの抽出
| 抽出情報 | 抽出元セクション | 抽出方法 |
|----------|-----------------|---------|
| ISS病期 | 診断名/検査所見 | 正規表現 + 検査値計算 |
| 細胞遺伝学 | 検査所見 | 正規表現 |

## 5. バリデーション計画

### 5.1 内部バリデーション
| 方法 | サンプル数 | 目標指標 |
|------|-----------|---------|
| Chart review | 100 | PPV >= 0.80, Sens >= 0.70 |
| Lab値照合 | 全例 | 一致率 >= 0.95 |

### 5.2 外部バリデーション
| 方法 | 比較対象 | 期待結果 |
|------|---------|---------|
| 先行研究比較 | [PMID] | 患者特性一致 |

## 6. 欠測データ対応

| 変数 | 想定欠測率 | 対応方法 |
|------|-----------|---------|
| eGFR | < 10% | ウィンドウ拡大、多重代入 |
| ECOG PS | 30-50% | 感度分析（完全ケース/代入） |
| 細胞遺伝学 | 20-40% | 「不明」カテゴリ作成 |

## 7. 感度分析用代替定義

| 定義 | 変更点 | 目的 |
|------|--------|------|
| 厳格定義 | [変更内容] | 特異度向上確認 |
| 広義定義 | [変更内容] | 感度向上確認 |

## 8. 参考文献・根拠
- [定義の根拠となるガイドライン・文献]
- PMID/DOI: ...
```

## クレームDB差別化ポイント

### 本仕様でのみ可能な定義
| フェノタイプ | クレームDB | EHR-RWD | 差別化 |
|-------------|-----------|---------|--------|
| ISS病期 | 不可（検査値なし） | 検査値から算出可 | ○ |
| 細胞遺伝学リスク | 不可 | サマリーから抽出可 | ○ |
| ECOG PS | 不可 | 経過記録から抽出可 | ○ |
| 血清学的奏効 | 不可 | M蛋白/FLC推移から判定可 | ○ |
| AE Grade | 不可 | 経過記録から抽出可 | ○ |

## 注意事項

1. **定義の明確性**: 曖昧さのない実行可能な定義を作成
2. **バリデーションの必須化**: 全フェノタイプにバリデーション計画を含める
3. **欠測への対応**: 欠測率と対応策を事前に計画
4. **バージョン管理**: 定義変更時はバージョン更新と変更履歴記録
5. **臨床的妥当性**: 定義が臨床的に意味のある集団を捉えているか確認
