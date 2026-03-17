---
name: novelty-gap-mapper
description: |
  evidence-scoutの結果を受け、研究ギャップを体系的にマッピングし、
  新規性の高い研究機会を特定・スコアリングする。EHR-RWDの優位性を活かした差別化ポイントを明確化。
allowed-tools:
  - Read
  - Grep
  - Glob
context: fork
---

# Novelty Gap Mapper Skill

## 目的
既存エビデンスと比較し、研究ギャップを体系的に分類・評価。新規性スコアを算出し、最も価値の高い研究機会を特定する。

## 入力パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| EVIDENCE_REPORT | Yes | evidence-scoutの出力またはパス | ./evidence_report.md |
| DRUG | Yes | 対象薬剤 | daratumumab |
| INDICATION | Yes | 対象疾患 | multiple myeloma |
| OUR_DB_STRENGTHS | Yes | 当社DB強み | EHR連携、経過記録、検査値 |
| COMPETITOR_DB | No | 比較対象DB | JMDC, MDV, NDB |

## 実行手順

### Step 1: ギャップ分類フレームワーク適用

以下の6軸でギャップを分類:

| 軸 | 説明 | ギャップ例 |
|----|------|-----------|
| **Population** | 未研究の患者集団 | 高齢frail患者、腎機能障害患者 |
| **Intervention** | 未検証の治療パターン | 用量調整、皮下注 vs 静注 |
| **Comparator** | 未比較の対照群 | Active comparator未使用 |
| **Outcome** | 未評価のアウトカム | PRO、医療経済、長期安全性 |
| **Time** | 未評価の時間軸 | 長期追跡、治療シーケンス |
| **Setting** | 未検証の医療環境 | 日本の実臨床、地域差 |

### Step 2: 新規性スコアリング

各ギャップに対して以下のスコアを付与（1-5点）:

| 評価軸 | 基準 |
|--------|------|
| **Publication Gap** | 同テーマの既存論文数（少ないほど高得点）|
| **Methodological Advance** | 方法論的改善可能性 |
| **Data Uniqueness** | 当社DBでしか不可能な程度 |
| **Timing Advantage** | 市場・規制環境での適時性 |
| **Differentiation** | クレームDB研究との差別化度 |

**総合新規性スコア** = 各軸の加重平均（重み: Publication 0.3, Method 0.2, Uniqueness 0.25, Timing 0.1, Differentiation 0.15）

### Step 3: EHR優位性マッピング

```
各ギャップに対して:
- クレームDBで実施可能か？ → Yes/No
- EHR-RWDで追加的に可能なこと → 具体的に記載
- 差別化インパクト → High/Medium/Low
```

### Step 4: ギャップ×実現可能性マトリックス作成

```
           高新規性
              │
    ★優先     │    要検討
    （即着手） │  （リソース次第）
─────────────┼─────────────
    検討不要   │    低優先
              │
           低新規性

    ← 低実現可能性    高実現可能性 →
```

## 出力フォーマット

```markdown
# Novelty Gap Analysis: {DRUG} in {INDICATION}

## 1. ギャップサマリー

| # | ギャップ | 分類軸 | 新規性スコア | EHR優位性 | 優先度 |
|---|----------|--------|-------------|-----------|--------|
| 1 | ... | Population | 4.2/5.0 | High | ★★★ |
| 2 | ... | Outcome | 3.8/5.0 | High | ★★★ |
| 3 | ... | Comparator | 3.5/5.0 | Medium | ★★☆ |

## 2. 詳細ギャップ分析

### Gap 1: [ギャップ名]
- **分類**: Population / Intervention / Comparator / Outcome / Time / Setting
- **既存研究**: [X件、主要文献PMID]
- **未充足ニーズ**: [具体的記述]
- **新規性スコア内訳**:
  - Publication Gap: X/5
  - Methodological Advance: X/5
  - Data Uniqueness: X/5
  - Timing Advantage: X/5
  - Differentiation: X/5
  - **総合**: X.X/5.0

#### EHR優位性評価
| 観点 | クレームDB | 当社EHR-RWD |
|------|-----------|-------------|
| 実施可否 | △/× | ○ |
| データ品質 | ... | ... |
| 差別化インパクト | - | High/Medium/Low |

## 3. JMDC/MDV等との差別化マトリックス

| ギャップ | JMDC/MDVで対応可能 | EHR-RWD差別化ポイント |
|----------|-------------------|----------------------|
| Gap 1 | No | 経過記録から詳細臨床情報取得可 |
| Gap 2 | Partial | 検査値時系列で精密評価可 |
| Gap 3 | Yes（既出） | 低差別化→優先度下げ |

## 4. 研究機会Top 3（推奨）

### 推奨1: [研究タイトル]
- **新規性スコア**: X.X/5.0
- **差別化度**: High
- **EHR活用ポイント**: [具体的]
- **想定インパクト**: [学術/臨床/ビジネス]

### 推奨2: [研究タイトル]
...

### 推奨3: [研究タイトル]
...

## 5. 根拠・限界
- 根拠文献: [PMID/DOI一覧]
- 評価の限界: [主観性、検索網羅性の限界等]
```

## 注意事項

1. **スコアリングの透明性**: 各スコアの根拠を明示、主観的判断は「著者評価」と明記
2. **クレームDB研究の公平な評価**: 既存研究の質が高い場合は新規性スコアを適切に下げる
3. **実現可能性の現実的評価**: データ量、期間、倫理審査等の制約を考慮
4. **定期的更新**: エビデンス環境は変化するため、6-12ヶ月ごとの再評価を推奨

## 依存関係
- 入力として `evidence-scout` の出力を想定
- 後続処理として `finer-gate`, `clinical-value`, `business-value` に引き継ぐ
