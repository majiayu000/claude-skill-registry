---
name: priority-analyzer
description: プロジェクト プロジェクトの開発機能優先順位を RICE(Reach × Impact × Confidence / Effort) モデルで分析するスキル。BRIEF.md/SPEC.md/CONTEXT.json/competitor-registry.json 等の多重ソースを読み取り、Evidence 基盤の優先順位スコアを算出・更新する。
version: 3.0
updated: 2026-02-09
doc_contract:
  review_interval_days: 90
---

# Priority Analyzer v3.0

## Overview

プロジェクト プロジェクトの **機能優先順位を RICE(Reach × Impact × Confidence / Effort) フレームワークで算出** するスキル。

### v3.0 主要変更 (WSJF → RICE 転換)

| 項目              | v2.x (WSJF)                                             | v3.0 (RICE)                                                                            |
| ----------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **モデル**        | AI-Adjusted WSJF Lite                                   | **RICE (Intercom 方法論)**                                                             |
| **核心公式**      | `(CoD × Confidence) / (JobSize × (1 + 0.2 × TechRisk))` | **`(Reach × Impact × Confidence) / Effort`**                                           |
| **データソース**  | CONTEXT.json 5個の整数のみ                              | **BRIEF.md + SPEC.md + CONTEXT.json + competitor-registry.json + gap-candidates.json** |
| **Confidence**    | EQS 5個のブーリアン                                     | **4要素加重エビデンスチェーン (0.0-1.0 連続値)**                                       |
| **完了機能処理**  | なし (100%完了でも高スコア)                             | **progress ≥ 100% → Reach=1, Impact=0.25**                                             |
| **Research 検証** | `sources: []`なのに `value: true` 可能 (バグ)           | **sources 配列長で自動判定、空配列 = 0点**                                             |

**転換動機**: Data Poverty Problem — 既存WSJFはBRIEF.md/SPEC.mdを一度も読まず、FR 7個の機能でも `job_size=2`、空の research_ids に `confidence=1.0` のようなバグが発生。

---

## SSOT (Single Source of Truth)

```
┌─────────────────────────────────────────────────────────────┐
│  SSOT 構造                                                   │
├─────────────────────────────────────────────────────────────┤
│  docs/features/{id}/CONTEXT.json   → priority セクション (SSOT)   │
│                                       RICE 入力値, 証拠, スコア│
│  docs/features/{id}/BRIEF.md       → Reach/Impact/Effort    │
│  docs/features/{id}/SPEC.md        → Confidence/Effort      │
│  docs/analysis/competitor-registry.json → Competitive Adj.   │
│  docs/analysis/gap-candidates.json → Impact (gap severity)   │
│  docs/research/*.md                → Confidence (参照)       │
└─────────────────────────────────────────────────────────────┘

⚠️ 原則:
   - priority データは CONTEXT.json でのみ管理
   - スコア算出時に実際に読んだファイルを data_sources_read に記録
   - 分析結果はユーザー確認後に更新
```

> スキーマ: [references/rice-section-schema.json](references/rice-section-schema.json)

> 計算エンジン: `.quality/scripts/rice_calculator.py`

---

## トリガー条件

以下のリクエストでこのスキルを使用:

- 「優先順位分析して」「機能の優先順位教えて」
- 「次に何を開発すべき？」
- 「開発ロードマップ確認して」
- 「MVPに何が必要？」
- 「どの機能が急ぎ？」

---

## 核心原則 (v3.0)

### 1. ROI 構造維持

> 価値(分子)とコスト(分母)を **絶対に合算しない**

```
Score = (Reach × Impact × Confidence) / Effort
```

### 2. Evidence 基盤 Confidence

> 根拠のない高い価値 = 低いスコア

- `research_ids: []` (空配列) → `research_evidence.score = 0.0` **強制**
- 4要素加重合算 (0.0-1.0 連続値)、二値判定なし

### 3. 完了機能自動減価

> 100% 完了した機能は自動的に最下位

- `progress >= 100%` → `Reach = 1`, `Impact = 0.25`
- 追加開発不要な機能が Top に上がる問題を解決

### 4. 多重ソース透明性

> 全てのスコアに `evidence` ディクショナリ + `data_sources_read` 配列を記録

どのファイルからどのデータを読んだか完全追跡可能。ブラックボックスなし。

---

## スコアリングモデル: RICE

### 公式

```
RICE Score = (Reach × Impact × Confidence) / Effort
Adjusted Score = RICE Score × Competitive Adjustment × Manual Override
```

### 1. Reach (到達範囲, 1-10)

「この機能がどれだけ多くのユーザーに影響を与えるか？」

| データソース            | 抽出項目                                         | 加重 |
| ----------------------- | ------------------------------------------------ | :--: |
| `BRIEF.md §1`           | target_users 範囲 (core_goal キーワード)         | 0.40 |
| `BRIEF.md §7`           | ビジネスメトリクス (LTV/リテンション キーワード) | 0.35 |
| `CONTEXT.json progress` | 進捗率逆比例 (100% → Reach=1)                    | 0.25 |

**スケール**: 1(niche) ~ 10(全ユーザー)
**完了減価**: `progress >= 100%` → `Reach = 1` (強制)

### 2. Impact (影響度, Intercom 5段階)

「この機能が各ユーザーにどれだけ大きな変化を与えるか？」

|  値  | レベル  | 基準                   |
| :--: | ------- | ---------------------- |
| 0.25 | Minimal | ほとんど目立たない変化 |
| 0.5  | Low     | 若干の利便性改善       |
|  1   | Medium  | 測定可能な改善         |
|  2   | High    | コアワークフロー変化   |
|  3   | Massive | ゲームチェンジャー     |

| データソース          | 抽出項目                                                    |
| --------------------- | ----------------------------------------------------------- |
| `BRIEF.md §1`         | core_goal キーワード (核心/収益 → High, 重要/改善 → Medium) |
| `BRIEF.md §7`         | LTV/リテンション キーワード → floor 保証                    |
| `gap-candidates.json` | gap_severity (HIGH→2, MEDIUM→1 floor)                       |

**完了減価**: `progress >= 100%` → `Impact = 0.25` (強制)

### 3. Confidence (信頼度, 0.0-1.0)

「このスコアをどれだけ信頼できるか？」

4要素加重エビデンスチェーン (EQS 二値判定を代替、v3.0で competitor_data を分離):

| 証拠要素                  | 加重 | データソース                | 判定基準                                      |
| ------------------------- | :--: | --------------------------- | --------------------------------------------- |
| **brief_completeness**    | 0.30 | `BRIEF.md`                  | §1-§7 実質的内容セクション数 / 全セクション数 |
| **spec_quality**          | 0.25 | `SPEC.md`                   | FR 定義数基準 (なければ 0.0)                  |
| **research_evidence**     | 0.25 | `CONTEXT.json research_ids` | **空配列なら 0.0 強制**、個数比例             |
| **implementation_status** | 0.20 | `CONTEXT.json progress`     | 実装開始/完了有無                             |

> **v3.0 変更**: `competitor_data` は Confidence から削除され、別途 `competitive_adjustment` post-multiplier に分離。

```
Confidence = Σ(weight_i × factor_i)   // 各 factor は 0.0-1.0 連続値
Final_Confidence = clamp(Confidence, 0.05, 1.0)
```

**核心改善**: `sources: []` なのに `value: true` の EQS バグが不可能 — sources 配列長で自動判定。

### 4. Effort (工数, person-weeks)

「この機能を実装するのにどれだけかかるか？」

| データソース            | 抽出項目        | 算出方法                    |
| ----------------------- | --------------- | --------------------------- |
| `SPEC.md §0`            | Target Files 数 | ファイル数 × 複雑度         |
| `SPEC.md §2`            | FR 個数         | FR あたり 0.5-2 person-days |
| `BRIEF.md §6`           | Constraints 数  | 制約が多いほど +加重        |
| `CONTEXT.json progress` | 完了 FR         | 残り作業のみ計算            |

**スケール**: 0.5 ~ 20 person-weeks (実数値)
**下限 0.5**: 分母 0 防止

### 5. Competitive Adjustment (競合調整, 0.8-1.3)

純粋 RICE スコアに乗じる post-multiplier。競合データがなければ 1.0 (中立)。

| シグナル             | ソース                     | 寄与範囲      |
| -------------------- | -------------------------- | ------------- |
| assessment_count     | `competitor-registry.json` | +0.00 ~ +0.10 |
| is_industry_standard | `gap-candidates.json`      | +0.00 ~ +0.05 |
| opportunity_score    | `gap-candidates.json`      | -0.05 ~ +0.10 |
| gap_severity         | `gap-candidates.json`      | -0.02 ~ +0.10 |

### 最終スコア

```
RICE Score = (Reach × Impact × Confidence) / Effort          // 純粋 RICE
Adjusted Score = RICE Score × Competitive Adjustment × Manual Override
```

- `competitive_adjustment`: 0.8~1.3 (データなしなら 1.0)
- `manual_override`: 0.8~1.2 (デフォルト 1.0)

---

## データ構造

### CONTEXT.json priority セクション (RICE v2)

```json
{
  "priority": {
    "version": "3.0",
    "schema": "rice-v2",
    "last_updated": "2026-02-09T12:00:00+00:00",
    "phase": "mvp",

    "rice_inputs": {
      "reach": {
        "score": 7,
        "evidence": {
          "target_user_scope": { "value": "all learners", "source": "BRIEF.md §1" },
          "business_metrics": { "value": "MAU retention", "source": "BRIEF.md §7" },
          "progress_adjustment": { "value": 30, "source": "CONTEXT.json progress" }
        },
        "rationale": "user_scope=9, biz=7, progress_factor=5"
      },
      "impact": {
        "score": 2,
        "evidence": {
          "core_goal": { "value": "AI 基盤カスタム学習", "source": "BRIEF.md §1" },
          "ltv_contribution": { "value": "LTV 直接貢献", "source": "BRIEF.md §7" },
          "gap_severity": { "value": "HIGH", "source": "gap-candidates.json" }
        },
        "rationale": "Impact=High (2). Gap severity=HIGH"
      },
      "confidence": {
        "score": 0.47,
        "factors": {
          "brief_completeness": { "score": 0.8, "section_count": 6, "source": "BRIEF.md" },
          "spec_quality": { "score": 0.7, "fr_count": 5, "source": "SPEC.md" },
          "research_evidence": { "score": 0.4, "research_count": 2, "sources": ["R-20260110-001"] },
          "implementation_status": { "score": 0.3, "progress_pct": 30, "source": "CONTEXT.json" }
        }
      },
      "effort": {
        "score": 4.2,
        "unit": "person-weeks",
        "evidence": {
          "fr_count": { "value": 5, "source": "SPEC.md §2" },
          "target_files": { "value": 12, "source": "SPEC.md §0" },
          "constraint_count": { "value": 3, "source": "BRIEF.md §6" },
          "remaining_pct": { "value": 70, "source": "CONTEXT.json progress" }
        },
        "rationale": "FR 5個, 70% 残り, 中規模"
      }
    },

    "competitive_adjustment": {
      "adjustment": 1.13,
      "has_data": true,
      "evidence": {
        "assessment_count": {
          "value": 3,
          "contribution": 0.03,
          "source": "competitor-registry.json"
        },
        "is_industry_standard": {
          "value": true,
          "contribution": 0.05,
          "source": "gap-candidates.json"
        },
        "opportunity_score": { "value": 7.5, "contribution": 0.1, "source": "gap-candidates.json" },
        "gap_severity": { "value": "MEDIUM", "contribution": 0.05, "source": "gap-candidates.json" }
      },
      "rationale": "CompAdj=1.13"
    },

    "calculated": {
      "rice_score": 1.57,
      "adjusted_score": 1.77,
      "competitive_adjustment": 1.13,
      "manual_override_applied": 1.0,
      "formula": "Adjusted = (R×I×C)/E × CompAdj × Override",
      "component_breakdown": {
        "numerator": 6.58,
        "denominator": 4.2
      }
    },

    "data_sources_read": [
      "BRIEF.md (date: 2026-02-09)",
      "SPEC.md (date: 2026-02-09)",
      "CONTEXT.json (date: 2026-02-09)",
      "competitor-registry.json (date: 2026-02-09)",
      "gap-candidates.json (date: 2026-02-09)"
    ],

    "manual_override": {
      "value": 1.0,
      "reason": null
    },

    "ai_rationale": "R=7, I=2, C=0.47, E=4.2, CompAdj=1.13",

    "history": [
      {
        "timestamp": "2026-02-09T12:00:00+00:00",
        "actor": "ai",
        "change_summary": "rice_calculator.py v2 再計算",
        "rice_score": 1.57,
        "adjusted_score": 1.77,
        "inputs_snapshot": {
          "reach": 7,
          "impact": 2,
          "confidence": 0.47,
          "effort": 4.2,
          "competitive_adjustment": 1.13
        }
      }
    ]
  }
}
```

---

## ワークフロー

### Phase 0: Candidate Pipeline Awareness (候補パイプライン認識)

> `--candidates` または `--all` フラグ使用時にアクティベート。scan-status.json がなければ自動 skip。

**入力**: `.claude/skills/market-intelligence-scanner/assets/scan-status.json`

**実行条件**:

1. scan-status.json 存在確認
2. スキーマ検証: `schema_version >= 3`
3. `status == "pending_review" || status == "approved"` 候補フィルタ

**ICE → Provisional RICE マッピング公式**:

```
# Reach: 候補の target_users 範囲基盤
reach = user_scope_estimate                     // 1-10 スケール (キーワード推定)
if gap_severity == "HIGH" and is_industry_standard:
    reach = min(reach + 1, 10)

# Impact: ICE Impact → RICE Impact (Intercom 5段階)
impact_map = {
    ice >= 9: 3,      // Massive
    ice >= 7: 2,      // High
    ice >= 5: 1,      // Medium
    ice >= 3: 0.5,    // Low
    else:    0.25     // Minimal
}

# Confidence: 候補は基本的に低い信頼度
confidence_base = 0.3                           // 候補デフォルト値
if source_type includes "competitor_gap":
    confidence_base += 0.15                     // 競合データあり
if evidence.length >= 2:
    confidence_base += 0.10                     // 複数証拠
// 典型的な candidate Confidence: 0.30~0.55

# Effort: ICE Effort 逆変換
effort = clamp(round((11 - ice_effort) × 1.5), 1, 15)  // person-weeks

Provisional RICE = (Reach × Impact × Confidence) / Effort
```

**`needs_human_review: true` フラグ**: Provisional RICE は参考指標。`--accept` 後に正式 RICE 再算出必須。

### Phase 1: Multi-Source Data Read (多重ソース読み込み)

```python
# 1. CONTEXT.json ロード
context = Read("docs/features/{feature_id}/CONTEXT.json")

# 2. schema 確認
assert context["priority"].get("schema") == "rice-v2"

# 3. BRIEF.md パース (§1-§7 セクション別分析)
brief = Read("docs/features/{feature_id}/BRIEF.md")
sections = parse_brief_sections(brief)  # §1 Problem, §5 Scope, §6 Constraints, §7 Metrics

# 4. SPEC.md パース (FR/AC カウント, Target Files)
spec = Read("docs/features/{feature_id}/SPEC.md")  # なければ None
fr_count = count_fr_definitions(spec)
target_files = extract_target_files(spec)

# 5. competitor-registry.json (competitive adjustment用)
registry = Read("docs/analysis/competitor-registry.json")

# 6. gap-candidates.json (gap severity, competitive adjustment用)
gaps = Read("docs/analysis/gap-candidates.json")
```

### Phase 2: Evidence Chain Validation (証拠チェーン検証)

各 Confidence 要素を **自動検証** (ユーザー確認最小化):

| Confidence 要素           | 自動検証方法                                | 0点条件               |
| ------------------------- | ------------------------------------------- | --------------------- |
| **brief_completeness**    | BRIEF.md §1-§7 実質内容セクション数カウント | BRIEF.md なし         |
| **spec_quality**          | SPEC.md FR 定義数カウント                   | SPEC.md なし          |
| **research_evidence**     | `research_ids` 配列長                       | **空配列 = 0.0 強制** |
| **implementation_status** | `CONTEXT.json progress.percentage`          | 未着手                |

### Phase 3: RICE Component Calculation (RICE コンポーネント計算)

AIが多重ソースデータを総合して各コンポーネントを算出:

```markdown
## RICE コンポーネント算出

| コンポーネント |  スコア  | 主要根拠                                |
| -------------- | :------: | --------------------------------------- |
| Reach          |    7     | 全学習者対象、高いビジネスメトリクス    |
| Impact         | 2 (High) | コアワークフロー変化, gap severity HIGH |
| Confidence     |  0.575   | SPEC あり(0.7), Research 不足(0.4)      |
| Effort         |  4.2 pw  | FR 5個, 70% 残り                        |

この値は適切ですか？修正が必要であればお知らせください。
```

### Phase 4: RICE Score Calculation (スコア計算)

```
1. 純粋 RICE
   Numerator = Reach × Impact × Confidence = 7 × 2 × 0.575 = 8.05
   Denominator = Effort = 4.2
   RICE Score = 8.05 / 4.2 = 1.92

2. 調整スコア
   Competitive Adjustment = 1.05 (競合データ基盤)
   Manual Override = 1.0 (補正なし)
   Adjusted Score = 1.92 × 1.05 × 1.0 = 2.02
```

### Phase 5: Integrated Ranking (統合ランキング)

計算結果をユーザーに提示し CONTEXT.json 更新有無を確認:

```markdown
## 分析結果

| 項目               | 値                |
| ------------------ | ----------------- |
| **RICE Score**     | 1.92              |
| **Adjusted Score** | 2.02              |
| **Tier**           | Tier 1 (即時着手) |
| **Confidence**     | 0.575             |

CONTEXT.json にこの結果を保存しますか？

- `--apply`: 即時保存
- 修正後保存: 値をお知らせください
```

---

## 更新トリガー

| トリガー          | 説明                       |          自動化          |
| ----------------- | -------------------------- | :----------------------: |
| progress ±10%     | 進捗度が 10% 以上変化      |   feature-pilot Step 6   |
| BRIEF.md 変更     | Reach/Impact/Effort 再計算 |           手動           |
| SPEC.md 変更      | Confidence/Effort 再計算   |           手動           |
| research_ids 変更 | Confidence 再計算          |           手動           |
| 14日経過          | 最終更新から2週間          | feature-status-sync 警告 |

### Staleness 自動検知 (v5)

次の条件のいずれかを満たすと自動再計算トリガー:

- `progress.percentage` 変動 >= 10% (前回計算時点比)
- 最終計算から 14日経過 (`priority.last_updated`)
- `competitive_data` 更新検知 (linked_at 変更)

### Competitive Data 経路 (v5)

RICE 計算時 `competitive_data` (root フィールド) 直接参照:

- `competitive_data.comp_ids` → 競合項目マッピング
- `competitive_data.gap_severity` → Impact 補正
- `competitive_data.is_industry_standard` → Reach 補正
  既存 `priority.competitive_adjustment` 内部経路と併用。

### 自動化メカニズム

```
┌─────────────────────────────────────────────────────────────┐
│ 自動化トリガーフロー                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  feature-pilot (実装完了)                                    │
│       │                                                     │
│       ▼                                                     │
│  feature-status-sync (Step 5)                               │
│       │ ← 14日+ 経過時に警告メッセージ                          │
│       ▼                                                     │
│  priority-analyzer (Step 6, 選択的)                          │
│       │ ← progress ±10% または staleness 検知時              │
│       ▼                                                     │
│  pre-quality-gate (Step 7)                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

CLI ツール:
  python3 .quality/scripts/rice_calculator.py --all           # 全体再計算
  python3 .quality/scripts/rice_calculator.py --feature 008   # 単一再計算
  python3 .quality/scripts/rice_calculator.py --json-output   # JSON 出力
```

---

## 出力形式

### 単一 Feature 分析

```markdown
# Priority Analysis: {feature_id}

## RICE スコア要約

| 項目               | 値                |
| ------------------ | ----------------- |
| **RICE Score**     | 1.92              |
| **Adjusted Score** | 2.02              |
| **Tier**           | Tier 1 (即時着手) |
| **Confidence**     | 0.575             |

## RICE 分解

### Reach (到達範囲)

| Evidence            | 値                     | ソース                   |
| ------------------- | ---------------------- | ------------------------ |
| Target Users        | all learners (scope 8) | BRIEF.md §1              |
| Business Metrics    | MAU retention (biz 7)  | BRIEF.md §7              |
| Progress Adjustment | 30% (factor 5)         | CONTEXT.json             |
| **Reach Score**     | **7**                  | 8×0.40 + 7×0.35 + 5×0.25 |

### Impact (影響度)

| Evidence         | 値                            | ソース              |
| ---------------- | ----------------------------- | ------------------- |
| Core Goal        | AI 基盤カスタム学習 → High(2) | BRIEF.md §1         |
| LTV Contribution | 直接貢献 → floor 2            | BRIEF.md §7         |
| Gap Severity     | HIGH → floor 2                | gap-candidates.json |
| **Impact Score** | **2 (High)**                  | Intercom snap       |

### Confidence (信頼度)

| 要素           | スコア | 加重 |   寄与    | ソース                    |
| -------------- | :----: | :--: | :-------: | ------------------------- |
| BRIEF 完成度   |  0.80  | 0.30 |   0.240   | BRIEF.md (6/7 セクション) |
| SPEC 品質      |  0.70  | 0.25 |   0.175   | SPEC.md (5 FRs)           |
| Research 根拠  |  0.40  | 0.25 |   0.100   | 2 research_ids            |
| 実装実績       |  0.30  | 0.20 |   0.060   | 30% progress              |
| **Confidence** |   -    |  -   | **0.575** |                           |

### Effort (工数)

| Evidence         | 値         | ソース       |
| ---------------- | ---------- | ------------ |
| FR Count         | 5          | SPEC.md §2   |
| Target Files     | 12         | SPEC.md §0   |
| Constraints      | 3          | BRIEF.md §6  |
| Remaining        | 70%        | CONTEXT.json |
| **Effort Score** | **4.2 pw** |              |

### 計算
```

RICE Score = (7 × 2 × 0.575) / 4.2 = 1.92
Adjusted = 1.92 × 1.05 (comp_adj) × 1.0 (override) = 2.02

```

## AI 分析

> {ai_rationale}

## 読んだデータソース
- BRIEF.md (date: 2026-02-09)
- SPEC.md (date: 2026-02-09)
- CONTEXT.json (date: 2026-02-09)
- competitor-registry.json (date: 2026-02-09)
```

### 全体 Feature ランキング

```markdown
# Priority Ranking Report

> 分析日: 2026-02-09
> Phase: MVP
> 分析対象: 49 Features

## Tier 1: 即時着手 (Score >= 1.5)

| 順位 | Feature             | RICE |  R  |  I  |  C   | E(pw) |
| :--: | ------------------- | :--: | :-: | :-: | :--: | :---: |
|  1   | 024-ai-tutor-system | 2.34 |  8  |  2  | 0.62 |  4.2  |
|  2   | 003-ai-content      | 1.89 |  7  |  2  | 0.55 |  4.1  |

## Tier 2: 1-2週間以内 (1.0 <= Score < 1.5)

...

## Tier 3: MVP 後 (0.5 <= Score < 1.0)

...

## Tier 4: Phase 2 (Score < 0.5)

...
```

### 統合ランキング (--all --candidates)

`--candidates` フラグ使用時、既存機能と待機候補を統合表示:

```markdown
## 統合優先順位ランキング

### A. 既存機能 (CONTEXT.json, RICE 確定)

| Rank | ID  | Name | RICE | R   | I   | C   | E(pw) |
| ---- | --- | ---- | ---- | --- | --- | --- | ----- |

### B. 待機候補 (scan-status.json, Provisional RICE)

| Rank | Candidate ID | Name | Prov.RICE | R   | I   | C   | E(pw) | Source | Status |
| ---- | ------------ | ---- | --------- | --- | --- | --- | ----- | ------ | ------ |

### C. 推奨: 次の変換対象

| Priority | Candidate                  | 根拠                                  |
| -------- | -------------------------- | ------------------------------------- |
| 1        | contextual-paywall-trigger | RICE 2.1, HIGH gap, industry standard |
| 2        | speaking-srs               | RICE 1.8, HIGH gap, speaking gap HIGH |
```

---

## コマンド

```bash
# 特定 Feature 分析
"/priority-analyzer 008-monetization"
"/priority-analyzer --feature 008,015,024"

# 分析後 CONTEXT.json に保存
"/priority-analyzer 008 --apply"

# 全 Feature 分析 (保存なしで比較のみ)
"/priority-analyzer --all"

# 全 Feature + 待機候補統合ランキング
"/priority-analyzer --all --candidates"

# Phase 変更後全体再計算
"/priority-analyzer --set-phase growth --apply"

# CLI 直接実行
# python3 .quality/scripts/rice_calculator.py --all --verbose
# python3 .quality/scripts/rice_calculator.py --feature 008 --apply
```

---

## 検証ルール

### スキーマ検証

| フィールド                     | 型     | 範囲/パターン                    |
| ------------------------------ | ------ | -------------------------------- |
| `schema`                       | 文字列 | `"rice-v2"`                      |
| `rice_inputs.reach.score`      | 数値   | 1-10                             |
| `rice_inputs.impact.score`     | 数値   | 0.25, 0.5, 1, 2, 3               |
| `rice_inputs.confidence.score` | 数値   | 0.0-1.0                          |
| `rice_inputs.effort.score`     | 数値   | 0.5-20                           |
| `rice_inputs.effort.unit`      | 文字列 | `"person-weeks"`                 |
| `manual_override.value`        | 数値   | 0.8-1.2                          |
| `phase`                        | enum   | exploration/mvp/growth/stability |
| `calculated.rice_score`        | 数値   | >= 0                             |

### エラー処理

| 状況                          | 深刻度  | 処理                                           |
| ----------------------------- | :-----: | ---------------------------------------------- |
| BRIEF.md なし                 | warning | fallback to CONTEXT.json メタデータ            |
| SPEC.md なし                  |  info   | spec_quality = 0.0, effort は BRIEF のみで推定 |
| research ファイルなし         | warning | research_evidence = 0.0, ai_rationale に記録   |
| competitor-registry.json なし |  info   | competitive_adjustment = 1.0 (中立), 続行      |
| calculated 不一致             |  info   | 再計算値を提案                                 |

---

## 関連スキル

| スキル                   | 役割                    | 呼び出し条件                        |
| ------------------------ | ----------------------- | ----------------------------------- |
| `/feature-status-sync`   | CONTEXT.json-コード同期 | 分析前 progress 最新化              |
| `/research-gap-analyzer` | Research 不足発見       | Confidence が低い時                 |
| `deep-research`          | 追加市場調査            | Research 補強必要時                 |
| `/competitive-tracker`   | 競合データ更新          | competitive_adjustment データ不足時 |

---

## 限界点・注意事項 (v3.0)

### 既知の限界

1. **BRIEF.md パースのヒューリスティック**: セクションヘッダーパターン(`## N.`)に依存。非標準形式で精度低下。
2. **Phase 手動設定が必要**: 自動遷移ロジックなし。PM判断が必要。
3. **Impact は離散値**: 0.25/0.5/1/2/3 の5段階のみ許容。
4. **単一プロジェクト最適化**: プロジェクト 特化設計。汎用性に制限。

### スコア解釈の注意

- **Score は相対的優先順位**: 絶対的価値ではない
- **Confidence が低ければ Score も低い**: 良い機能でも根拠がなければ後順位
- **完了機能は自動最下位**: 100% 完了 → Reach=1, Impact=0.25

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                                                                                                                                                                   |
| ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-09 | v3.0       | **WSJF→RICE 転換**: 多重ソース Evidence 基盤、BRIEF/SPEC パース、Intercom 5段階 Impact、4要素加重 Confidence + Competitive Adjustment 分離、完了機能減価、`rice_calculator.py` + `migrate_wsjf_to_rice.py` |
| 2026-02-07 | v2.2       | **Pipeline Contract**: Phase 0 Candidate Pipeline Awareness, ICE→Provisional WSJF, --candidates フラグ                                                                                                     |
| 2026-01-26 | v2.1       | **自動化統合**: feature-pilot Step 6 連動、staleness 警告                                                                                                                                                  |
| 2026-01-25 | v2.0       | **ゼロベース再設計**: AI-Adjusted WSJF Lite, EQS Confidence                                                                                                                                                |
| 2026-01-25 | v1.3       | SSOT 統一: CONTEXT.json 基盤転換                                                                                                                                                                           |
| 2026-01-18 | v1.0       | 初期バージョン - 3軸分析フレームワーク (廃止)                                                                                                                                                              |
