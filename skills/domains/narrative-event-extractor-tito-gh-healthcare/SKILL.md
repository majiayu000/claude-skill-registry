---
name: narrative-event-extractor
description: |
  経過記録・臨床サマリー等のナラティブテキストから臨床イベント（有害事象、効果判定、
  症状変化等）を抽出する仕様を設計する。NLP/正規表現パターンと品質管理計画を含む。
allowed-tools:
  - Read
  - Grep
  - Glob
context: normal
---

# Narrative Event Extractor Skill

## 目的
EHR内の非構造化テキスト（経過記録、臨床サマリー、看護記録等）から研究に必要な臨床イベント・情報を抽出するための仕様を設計する。

## 当社EHRで利用可能なテキストデータ

| データ種類 | 内容 | 構造化度 | 情報密度 |
|-----------|------|---------|---------|
| **経過記録** | 日々の診療記録、医師所見 | 低 | 高 |
| **臨床サマリー** | 退院サマリー、紹介状 | 中 | 高 |
| **看護記録** | 患者状態、バイタル、観察 | 低〜中 | 中 |

※画像データ・部門システムデータは利用不可

## 入力パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| EVENT_TYPE | Yes | 抽出対象イベント種類 | adverse_event / response / symptom |
| DRUG | Yes | 対象薬剤 | daratumumab |
| INDICATION | Yes | 対象疾患 | multiple myeloma |
| SPECIFIC_EVENTS | No | 具体的イベント名 | neutropenia, infection, IRR |
| TEXT_SOURCE | No | テキストソース指定 | progress_notes / summary / all |

## イベント抽出フレームワーク

### 1. 有害事象（Adverse Events）抽出

#### 共通有害事象パターン
```yaml
adverse_event_extraction:
  infusion_related_reaction:
    keywords_ja: ["注入反応", "IRR", "輸注反応", "インフュージョンリアクション"]
    keywords_en: ["infusion reaction", "IRR"]
    context_clues: ["投与中", "投与後", "初回投与"]
    severity_markers:
      grade_1_2: ["軽度", "中等度", "対症療法で改善"]
      grade_3_4: ["重度", "投与中止", "入院", "ステロイド投与"]

  neutropenia:
    keywords_ja: ["好中球減少", "顆粒球減少", "neutropenia"]
    lab_confirmation: "ANC < 1500/μL"
    severity_markers:
      grade_1: "ANC 1500-2000"
      grade_2: "ANC 1000-1500"
      grade_3: "ANC 500-1000"
      grade_4: "ANC < 500"

  infection:
    keywords_ja: ["感染", "肺炎", "発熱", "敗血症", "帯状疱疹"]
    keywords_en: ["infection", "pneumonia", "sepsis", "herpes zoster"]
    pathogen_markers: ["細菌", "ウイルス", "真菌", "COVID"]
    severity_markers:
      mild: ["外来治療", "経口抗菌薬"]
      severe: ["入院", "IV抗菌薬", "ICU"]

  thrombocytopenia:
    keywords_ja: ["血小板減少", "thrombocytopenia"]
    lab_confirmation: "Plt < 100,000/μL"

  peripheral_neuropathy:
    keywords_ja: ["末梢神経障害", "しびれ", "感覚異常", "neuropathy"]
    severity_markers:
      grade_1: ["軽度", "日常生活支障なし"]
      grade_2: ["中等度", "器具的ADL制限"]
      grade_3_4: ["重度", "セルフケアADL制限"]
```

#### 有害事象メタ情報抽出
```yaml
ae_metadata:
  onset_date:
    patterns: ["[0-9]{4}/[0-9]{2}/[0-9]{2}", "○月○日", "Day[0-9]+"]
    relative_markers: ["投与後○日", "○クール目", "前回より"]

  outcome:
    resolved: ["改善", "回復", "軽快", "消失"]
    ongoing: ["持続", "継続", "残存"]
    fatal: ["死亡", "永眠"]

  action_taken:
    dose_reduced: ["減量", "dose reduction"]
    dose_delayed: ["延期", "スキップ", "休薬"]
    discontinued: ["中止", "終了", "off"]

  causality:
    related: ["関連あり", "因果関係あり", "薬剤性"]
    possible: ["可能性あり", "否定できず"]
    unlikely: ["関連なし", "因果関係なし"]
```

### 2. 効果判定（Response Assessment）抽出

#### 骨髄腫特異的奏効評価
```yaml
response_extraction:
  imwg_response:
    stringent_cr:
      keywords: ["sCR", "stringent CR", "厳格完全奏効"]
      criteria: "免疫固定法陰性 + FLC比正常 + 骨髄形質細胞<5%"

    complete_response:
      keywords: ["CR", "完全奏効", "complete response"]
      criteria: "免疫固定法陰性"

    very_good_partial:
      keywords: ["VGPR", "非常に良好な部分奏効"]
      criteria: "M蛋白90%以上減少"

    partial_response:
      keywords: ["PR", "部分奏効", "partial response"]
      criteria: "M蛋白50%以上減少"

    stable_disease:
      keywords: ["SD", "安定", "stable disease"]

    progressive_disease:
      keywords: ["PD", "進行", "増悪", "progression"]
      criteria: "M蛋白25%以上増加"

  response_context:
    assessment_timing: ["○クール後", "○ヶ月時点", "best response"]
    assessment_method: ["IMWG基準", "効果判定", "PET-CT"]
```

### 3. 症状・状態（Symptoms/Status）抽出

#### Performance Status
```yaml
status_extraction:
  ecog_ps:
    pattern: "(?:PS|ECOG|パフォーマンスステータス)[：:\s]*([0-4])"
    keywords:
      ps_0: ["日常生活制限なし", "通常の活動", "無症状"]
      ps_1: ["軽度の症状", "軽作業可", "歩行可能"]
      ps_2: ["歩行可能", "自分の身の回り可", "日中50%以上起床"]
      ps_3: ["限られた自分の身の回り", "日中50%以上臥床"]
      ps_4: ["全く動けない", "完全に臥床", "セルフケア不能"]

  symptoms:
    pain:
      keywords: ["疼痛", "痛み", "骨痛", "腰痛", "NRS"]
      scale_pattern: "NRS[：:\s]*([0-9]|10)"

    fatigue:
      keywords: ["倦怠感", "疲労", "だるさ", "疲れ"]
      severity: ["軽度", "中等度", "重度"]

    appetite:
      keywords: ["食欲", "食事摂取", "経口摂取"]
      status: ["良好", "低下", "不振", "不良"]
```

### 4. 治療関連情報抽出

```yaml
treatment_extraction:
  dose_modification:
    reduction:
      keywords: ["減量", "dose reduction", "○mg→○mg"]
      pattern: "([0-9]+)mg.*(?:から|→).*([0-9]+)mg"

    delay:
      keywords: ["延期", "スキップ", "休薬", "○日遅れ"]

  discontinuation:
    keywords: ["中止", "終了", "off treatment"]
    reasons:
      progression: ["PD", "進行", "増悪"]
      toxicity: ["副作用", "毒性", "有害事象"]
      patient_choice: ["患者希望", "本人希望"]
      death: ["死亡", "永眠"]
      other: ["その他", "転院"]

  line_of_therapy:
    pattern: "([0-9]+)(?:次治療|ライン|line)"
    keywords: ["初回治療", "二次治療", "三次治療", "salvage"]
```

## 出力フォーマット

```markdown
# Narrative Event Extraction Specification: {EVENT_TYPE}

## 1. 概要

| 項目 | 値 |
|------|-----|
| 抽出対象イベント | {EVENT_TYPE} |
| 対象薬剤 | {DRUG} |
| 対象疾患 | {INDICATION} |
| テキストソース | {TEXT_SOURCE} |

## 2. 抽出仕様

### 2.1 対象イベント一覧
| イベント | カテゴリ | 優先度 |
|----------|---------|--------|
| ... | ... | High/Medium/Low |

### 2.2 抽出パターン定義

#### イベント1: [イベント名]
```yaml
event_name: "[イベント名]"
keywords:
  japanese: [...]
  english: [...]
regex_patterns:
  - pattern: "..."
    capture_groups: [...]
context_requirements:
  - "[文脈条件1]"
  - "[文脈条件2]"
negation_patterns:
  - "否定形パターン"
severity_classification:
  mild: [...]
  moderate: [...]
  severe: [...]
```

#### イベント2: [イベント名]
...

### 2.3 メタ情報抽出
```yaml
metadata_extraction:
  date:
    patterns: [...]
  severity:
    patterns: [...]
  outcome:
    patterns: [...]
  causality:
    patterns: [...]
```

## 3. NLP処理パイプライン

### 3.1 前処理
```
1. テキスト正規化（全角→半角、表記揺れ統一）
2. 文分割
3. 否定表現検出
4. 時制検出（過去/現在/予定）
```

### 3.2 抽出処理
```
1. キーワードマッチング
2. 正規表現パターンマッチ
3. 文脈確認（否定、時制、主語）
4. 重複除去・統合
```

### 3.3 後処理
```
1. 信頼度スコア付与
2. 構造化データへの変換
3. バリデーションフラグ付与
```

## 4. 品質管理計画

### 4.1 バリデーション方法
| 方法 | サンプル数 | 評価指標 | 目標値 |
|------|-----------|---------|--------|
| 手動レビュー | 100 | Precision | >= 0.85 |
| 手動レビュー | 100 | Recall | >= 0.75 |
| 構造化データ照合 | 全例 | 一致率 | >= 0.90 |

### 4.2 エラーパターン対応
| エラータイプ | 例 | 対応策 |
|-------------|-----|--------|
| False Positive | 否定文の見逃し | 否定パターン拡充 |
| False Negative | 表記揺れ | 同義語辞書拡充 |
| 誤分類 | severity誤判定 | 文脈ルール追加 |

### 4.3 継続的改善
- 定期的な精度検証（月次）
- 新規パターンの追加プロセス
- エラーケースのフィードバックループ

## 5. 出力データ構造

### 5.1 抽出結果スキーマ
```json
{
  "patient_id": "string",
  "event_id": "string",
  "event_type": "string",
  "event_name": "string",
  "source_text": "string",
  "source_document": "string",
  "extraction_date": "date",
  "event_date": "date (if extracted)",
  "severity": "string (if applicable)",
  "outcome": "string (if applicable)",
  "confidence_score": "float",
  "validation_status": "pending/validated/rejected"
}
```

## 6. JMDC/MDV差別化ポイント

| 情報 | クレームDB | 本抽出仕様 |
|------|-----------|-----------|
| AE詳細 | ICDコードのみ | 重症度・経過・転帰含む |
| 効果判定 | 取得不可 | IMWG基準奏効抽出可 |
| PS/症状 | 取得不可 | 経過記録から抽出可 |
| 中止理由 | 推定のみ | 医師記載から正確に取得 |

## 7. 注意事項・制限

1. **プライバシー保護**: 抽出結果に個人特定情報を含めない
2. **誤抽出リスク**: 重要な意思決定には手動検証を推奨
3. **施設差**: 記載スタイルの施設差による精度変動に注意
4. **時間コスト**: 大規模抽出には計算リソース・時間を要する
5. **更新管理**: 抽出ルールのバージョン管理を徹底

## 8. 参考資料
- CTCAE v5.0 (有害事象grading)
- IMWG Response Criteria (奏効判定)
- MedDRA (医学用語辞書)
```

## 機微情報保護ルール

1. **外部検索時**: 患者ID・施設名・具体的な記載内容を検索クエリに含めない
2. **出力時**: source_textは必要最小限とし、匿名化を確認
3. **保存時**: 抽出結果は元データと同等のセキュリティレベルで管理
