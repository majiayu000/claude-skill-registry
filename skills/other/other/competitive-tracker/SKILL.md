---
name: competitive-tracker
description: |
  プロジェクト アプリの機能ポートフォリオを競合6アプリとMECEフレームワークで比較して
  ギャップ(欠けた機能)とポジション変化を追跡するスキル。
  競合データはcompetitor-registry.jsonに構造化されており、四半期ごとDeep Researchで更新する。

  v2.0: audit-runner.mjs 自動化スクリプト統合, JTBD Opportunity Score, 3-tier カバレッジ,
  フィードバックループ, Diff 追跡, 双方向比較(当社独自の差別化12個追跡)

  v3.0: 2-Phase LLM Pipeline 導入 (DR Markdown → Gemini 構造化抽出 → assessments 統合),
  registry v3 スキーマ (per-feature assessments + confidence_thresholds + extraction_log),
  dr-extractor.mjs (Gemini API ベース自動抽出), confidence ベース信頼度報告,
  --refresh-plan (更新必要優先順位リスト)

  "競合比較", "ベンチマーク", "業界標準チェック", "ポートフォリオチェック", "competitive", "ギャップ追跡" などの要求でトリガーされる。

  <example>
  user: "競合と比較して"
  assistant: "competitive-trackerを使用してポートフォリオギャップを分析します"
  </example>

  <example>
  user: "業界標準と当社アプリの差確認して"
  assistant: "competitive-trackerを実行して業界標準対カバレッジを分析します"
  </example>

  <example>
  user: "/competitive-tracker --import"
  assistant: "Deep Research 結果をcompetitor-registry.jsonにパースします"
  </example>
version: 3.0
updated: 2026-02-08
doc_contract:
  review_interval_days: 90
---

# Competitive Tracker v3.0

> **核心コンセプト**: "比較 → ギャップ発見 → 機会定量化 → 既存パイプライン接続"
>
> このスキルは**検出(Detection), 定量化(Quantification), 接続(Connection)**を担当する。
> 優先順位/定義/実装は既存ツールに委任する。

---

## SSOT (Single Source of Truth)

```
┌─────────────────────────────────────────────────────────────┐
│  SSOT 構造                                                    │
├─────────────────────────────────────────────────────────────┤
│  docs/analysis/competitor-registry.json  → 競合機能 DB     │
│  docs/analysis/mece-feature-analysis.md  → MECE 分析レポート   │
│  docs/features/*/CONTEXT.json            → 内部機能状態      │
│  docs/features/index.md                  → 機能リスト           │
│  .claude/state/audit-snapshots/          → 監査履歴スナップショット    │
└─────────────────────────────────────────────────────────────┘

⚠️ 原則:
   - 競合データはcompetitor-registry.jsonでのみ管理
   - ギャップ深刻度はregistryのgap_severity フィールドでのみ定義
   - MECE レポートはaudit-runnerの--save 出力物
   - Importance データはDeep Research 結果をregistryに統合
```

---

## 自動化エンジン: audit-runner.mjs v3.0

> **AI トークンコスト $0** — 決定論的(deterministic) Node.js スクリプト

```bash
# 基本実行 (全体レポート)
node .claude/scripts/audit-runner.mjs

# 主要CLI フラグ
node .claude/scripts/audit-runner.mjs --summary       # カバレッジ要約のみ
node .claude/scripts/audit-runner.mjs --gaps-only     # ギャップのみフィルタリング
node .claude/scripts/audit-runner.mjs --validate      # マッピング整合性検証
node .claude/scripts/audit-runner.mjs --json          # JSON 出力
node .claude/scripts/audit-runner.mjs --save          # mece-feature-analysis.md 保存
node .claude/scripts/audit-runner.mjs --diff          # 以前スナップショットと比較
node .claude/scripts/audit-runner.mjs --snapshot      # スナップショットのみ保存 (レポートなし)
node .claude/scripts/audit-runner.mjs --recommend     # MVP 推奨のみ出力
node .claude/scripts/audit-runner.mjs --no-recommend  # MVP 推奨除外
node .claude/scripts/audit-runner.mjs --refresh-plan  # 更新必要アプリ/機能優先順位リスト
```

### 3-tier カバレッジ指標

| 指標          | 公式                                    | 意味                     |
| ------------- | --------------------------------------- | ------------------------ |
| **Binary**    | 機能存在有無                            | "あるかないか"           |
| **Weighted**  | Σ(our_depth / competitor_max_depth) / N | "どれだけ深いか"         |
| **Effective** | Binary × CONTEXT.json progress 平均     | "実際どれだけ完成したか" |

### JTBD Opportunity Score (Strategyn ODI)

```
Opportunity = Importance + max(Importance - Satisfaction, 0)

範囲: 1.0 ~ 10.0
- 7.0+ → 🔴 核心投資領域
- 5.0~6.9 → 🟡 改善推奨
- < 5.0 → 🟢 現状維持可能
```

- **Importance**: Deep Research ベース学習者動機調査 (世宗学堂財団, Duolingo レポート, 学術研究)
- **Satisfaction**: registryのjtbd_satisfaction.matrix.hackathon_project 値

### フィードバックループ検出

audit-runnerは2つの不一致を自動検出する:

1. **Registry 更新必要**: CONTEXT.json progressが100%なのにregistryにdepth_gapで残っている場合
2. **未登録機能**: CONTEXT.jsonに進行中だがregistryにマッピングがない機能 (差別化登録候補)

---

## トリガー条件

### 基本モード (監査)

1. **定期チェック**: "競合比較して", "ベンチマーク回して"
2. **業界標準確認**: "業界標準と差何?", "当社アプリ欠けた機能ある?"
3. **ポートフォリオ分析**: "機能ポートフォリオチェック", "MECE 確認"
4. **ギャップ現状**: "ギャップ追跡", "competitive tracker"
5. **機会分析**: "JTBD 分析", "機会スコア", "opportunity"

### サブコマンド

| コマンド         | 説明                                                       |
| ---------------- | ---------------------------------------------------------- |
| (基本)           | audit-runner 実行 → 全体レポート                           |
| `--summary`      | カバレッジ要約 + JTBD 機会順位のみ                         |
| `--gaps-only`    | ギャップのみフィルタリングして報告                         |
| `--validate`     | registry ↔ CONTEXT.json マッピング整合性検証               |
| `--save`         | mece-feature-analysis.md ファイル保存                      |
| `--diff`         | 以前監査スナップショットと比較して変化点報告               |
| `--snapshot`     | スナップショットのみ保存 (レポート省略)                    |
| `--recommend`    | MVP 推奨のみ出力 (4要素複合スコアベース)                   |
| `--no-recommend` | MVP 推奨セクション除外                                     |
| `--refresh-plan` | 更新必要アプリ/機能優先順位リスト (stale + low confidence) |
| `--json`         | JSON 形式出力 (CI/CD 連携用)                               |
| `--import`       | Deep Research マークダウンをregistry.jsonにパース          |
| `--refresh`      | `/deep-research` 実行案内 → `--import` 案内                |
| `--action`       | ギャップに対するアクション提案 (MIS 候補登録含む)          |

---

## 核心原則

### 1. このスキルは"検出 + 定量化 + 接続"をする

```
❌ このスキルがしないこと:
   - 競合データ直接収集 (→ deep-research)
   - ギャップの優先順位算出 (→ priority-analyzer)
   - ギャップを機能として定義 (→ feature-architect)
   - 機能実装 (→ feature-pilot)

✅ このスキルがすること:
   - 内部機能 vs 競合機能比較 (3-tier カバレッジ)
   - ギャップ/重複/変化検出
   - JTBD Opportunity Scoreで機会定量化
   - MVP 推奨 (4要素複合スコアベース自動推奨, --recommend)
   - 双方向比較 (当社独自の差別化12個追跡)
   - フィードバックループ検出 (registry ↔ CONTEXT.json 不一致)
   - 発見されたギャップをmarket-intelligence-scanner 候補として接続提案
   - mece-feature-analysis.md 自動更新 (--save)
   - 監査スナップショット保存 + Diff 追跡
```

### 2. 批判的思考5段階適用

| 段階 | 質問                                                          |
| ---- | ------------------------------------------------------------- |
| 分解 | ギャップのカテゴリ別分布は? (Lifecycle × Domain)              |
| 解決 | 各ギャップの深刻度とJTBD Opportunity Scoreは?                 |
| 検証 | 本当にギャップか、戦略的選択か? (AI 100% 戦略と衝突しないか?) |
| 統合 | 全体ポートフォリオカバレッジ率(3-tier)とポジションは?         |
| 反省 | 競合データが最新か? Importance データ根拠は十分か?            |

### 3. "全てのギャップを埋める必要はない"

ギャップ発見時3つに分類:

| 分類                   | 意味                                      | アクション                         |
| ---------------------- | ----------------------------------------- | ---------------------------------- |
| **埋めるべきギャップ** | 業界標準(4+アプリ)なのに当社だけない      | → MIS 候補登録                     |
| **戦略的選択**         | 当社戦略と合わない (例: コミュニティ添削) | → registryに `strategic_skip` 表示 |
| **観察対象**           | まだ標準ではないがトレンド                | → モニタリング維持                 |

---

## ワークフロー

### Phase 1: audit-runner 自動実行

```bash
# 基本: 全体レポート + スナップショット自動保存
node .claude/scripts/audit-runner.mjs

# レポート出力内容:
# 1. カバレッジ要約 (Binary/Weighted/Effective)
# 2. 🔴 緊急ギャップ (業界標準未カバー)
# 3. 🟡 Depth Gap (あるが競合より浅い)
# 4. 🎯 JTBD Opportunity Score 表
# 5. 🛡️ 当社独自の差別化12個
# 6. 📂 カテゴリ別ギャップ分布
# 7. 🔄 フィードバックループ通知
# 8. 🎯 MVP 推奨 (4要素複合スコア TOP 10 + 2×2 マトリックス)
# 9. 💡 推奨アクション
```

### Phase 2: ユーザー決定

```
HIGH ギャップ:
  → "comp-025 (Speaking SRS)をmarket-intelligence-scanner 候補として登録しますか?"
  → 承認時: /market-intelligence-scanner --accept comp-025
  → その後: /feature-architect → /feature-pilot パイプラインで自動接続

戦略的skip:
  → "comp-029 (コミュニティ添削)はAI 100% 戦略と衝突します. Skip 処理しますか?"
  → 承認時: registryにstrategic_skip マーキング

JTBD 機会:
  → "culture (機会スコア7.0)が最優先投資領域です"
  → K-コンテンツ統合機能強化のためのfeature-architect 呼び出し提案
```

---

## --add-competitor ワークフロー (competitor-importer.mjs)

> **AI トークンコスト $0** — 決定論的Node.js スクリプト (検証/統合/バックアップ)

新しい競合アプリをregistryに追加する7-Step パイプライン:

```bash
# Step 1: 空テンプレート生成 ($0)
node .claude/scripts/competitor-importer.mjs --generate-template rosetta
# → .claude/state/import-templates/rosetta-profile.json (64機能 + 8 JTBD 空値)

# Step 2: Deep Research ($1-2)
/deep-research --provider gemini "Rosetta Stone Korean 機能分析"

# Step 3: AIがテンプレート記入
# Deep Research 結果をベースにhas_feature/depth/evidence 作成

# Step 4: 検証 ($0)
node .claude/scripts/competitor-importer.mjs --validate .claude/state/import-templates/rosetta-profile.json

# Step 5: プレビュー ($0)
node .claude/scripts/competitor-importer.mjs --dry-run .claude/state/import-templates/rosetta-profile.json

# Step 6: 適用 ($0, 自動バックアップ)
node .claude/scripts/competitor-importer.mjs --apply .claude/state/import-templates/rosetta-profile.json

# Step 7: 影響度確認 ($0)
node .claude/scripts/audit-runner.mjs --diff
```

### テンプレートスキーマ

```json
{
  "$schema": "competitor-app-profile-v1",
  "generated_date": "2026-02-07",
  "registry_feature_count": 64,
  "app": {
    "id": "rosetta",
    "name": "Rosetta Stone",
    "note": "Immersion-based learning",
    "mau": "12M+"
  },
  "features": [
    {
      "registry_id": "comp-001",
      "registry_name": "配置試験 / レベルテスト",
      "category": "Onboarding",
      "has_feature": true,
      "depth": 3,
      "evidence": "Rosetta Stone: Placement assessment..."
    }
  ],
  "jtbd_satisfaction": {
    "listening": 3,
    "speaking": 2,
    "reading": 3,
    "writing": 2,
    "exam_prep": 2,
    "culture": 1,
    "habit": 3,
    "retention": 3
  },
  "new_features": []
}
```

### 検証ルール (15個)

| コード | ルール                                                               |   レベル   |
| ------ | -------------------------------------------------------------------- | :--------: |
| V01    | $schema = competitor-app-profile-v1                                  |   ERROR    |
| V02    | app.id フォーマット (小文字英数字/ハイフン/アンダースコア, 2-31文字) |   ERROR    |
| V03    | app.id 固有性 (registry 内重複不可)                                  |   ERROR    |
| V04    | app.name 必須                                                        |   ERROR    |
| V05    | features 数 = registry features 数                                   |   ERROR    |
| V06    | registry_feature_count staleness チェック                            |    WARN    |
| V07    | registry_idがregistryに存在                                          |   ERROR    |
| V08    | registry_id 重複不可                                                 |   ERROR    |
| V09    | has_featureはboolean                                                 |   ERROR    |
| V10    | has_feature=true → depth 1-5 整数必須                                |   ERROR    |
| V11    | has_feature=false → depthはnull                                      |    WARN    |
| V12    | has_feature=true → evidence 作成推奨                                 |    WARN    |
| V13    | JTBD 8個職務 + スコア範囲 1-5                                        | ERROR/WARN |
| V14    | new_features.name 必須                                               |   ERROR    |
| V15    | 最低1個以上has_feature=true                                          |    WARN    |

### --remove-competitor <app_id>

競合アプリをregistryから完全削除:

```bash
# アプリリスト確認
node .claude/scripts/competitor-importer.mjs --list-apps

# 削除 (自動バックアップ)
node .claude/scripts/competitor-importer.mjs --remove-app <app_id>
```

削除時処理:

- `apps[]`から除去
- 全ての`features[].apps`から除去
- `features[].app_depth`から除去
- `app_count`, `is_industry_standard` 再計算
- `jtbd_satisfaction.matrix`から除去
- `summary` 再計算
- 自動バックアップ → `.claude/state/import-backups/`

### ユーティリティコマンド

```bash
# 現在登録済みアプリリスト
node .claude/scripts/competitor-importer.mjs --list-apps

# 手動バックアップ
node .claude/scripts/competitor-importer.mjs --backup
```

---

## 2-Phase LLM Pipeline (dr-extractor.mjs)

> **Phase 1**: DR Markdown → Gemini 構造化抽出 → profile-v2 JSON (コスト: ~$0.02-0.05/アプリ)
> **Phase 2**: profile → competitor-importer.mjs → registry 統合 (コスト: $0)

```bash
# Phase 1: DR 分析 → Gemini 構造化抽出
node .claude/scripts/dr-extractor.mjs --extract docs/research/rosetta-stone-analysis.md --app rosetta
# → .claude/state/import-templates/rosetta-profile.json

# 検討: 低信頼度項目ハイライト
node .claude/scripts/dr-extractor.mjs --review .claude/state/import-templates/rosetta-profile.json

# Phase 2: profile → registry 統合
node .claude/scripts/competitor-importer.mjs --validate .claude/state/import-templates/rosetta-profile.json
node .claude/scripts/competitor-importer.mjs --apply .claude/state/import-templates/rosetta-profile.json

# 影響度確認
node .claude/scripts/audit-runner.mjs --diff

# 更新必要リスト確認
node .claude/scripts/audit-runner.mjs --refresh-plan
```

### Confidence モデル (4要素加重)

```
confidence = 0.4 × evidence_quality + 0.2 × source_freshness
           + 0.2 × cross_reference + 0.2 × extraction_clarity

evidence_quality: 証拠テキスト長(200字基準) + 具体的数値/表現有無
source_freshness: DR 生成日基準180日減衰
cross_reference: 既存registry アプリ数ベースクロス検証度
extraction_clarity: Gemini certainty 値直接使用
```

### 信頼度ベース報告 (audit-runner v3.0)

```
📊 信頼度報告 (Confidence Report)
┌─────────────────────┬───────┐
│ 総Assessment       │ N個   │
│ 平均信頼度         │ 0.XX  │
│ 🟢 High (≥0.80)    │ N個   │
│ 🟡 Medium (0.50-79) │ N個   │
│ 🔴 Low (0.30-0.49)  │ N個   │
│ ❌ Rejected (<0.30)  │ N個   │
│ ⏰ Stale (90日+)    │ N個   │
│ ⚠️ 根拠不足        │ N個   │
└─────────────────────┴───────┘
```

---

## --import モード詳細 (レガシー)

> ⚠️ 構造化されたテンプレートベース`--add-competitor` ワークフローを推奨します。

Deep Research 結果(マークダウン)をregistry.jsonに変換:

### 入力

```
docs/analysis/deep-research-competitor-features.md
(またはユーザーが指定したDeep Research 結果ファイル)
```

### 処理

1. マークダウンパース: アプリ別セクション → 機能抽出
2. 既存registryと比較: 新規/変更/削除検出
3. MECE カテゴリ自動マッピング (Lifecycle × Domain)
4. Depth Score 算定 (1-5)
5. JTBD タグ付け
6. ユーザー確認後registry 更新

### 出力

```
## Import 結果

- 新規機能: N個追加
- 既存機能更新: N個
- 削除された機能: N個 (確認必要)
- registry 更新完了: YYYY-MM-DD
```

---

## 更新周期ガイド

| 活動                                                    |        周期        | コスト | トリガー                    |
| ------------------------------------------------------- | :----------------: | :----: | --------------------------- |
| **監査** (`audit-runner.mjs`)                           | 毎週 or 機能追加時 |   $0   | 手動 or CI                  |
| **Diff 追跡** (`--diff`)                                |        隔週        |   $0   | 手動                        |
| **Deep Research 更新** (`/deep-research` + `--import`)  |     四半期ごと     | ~$1-2  | 手動                        |
| **JTBD Importance 更新** (`/deep-research` JTBD クエリ) |      半期ごと      |  ~$1   | 手動                        |
| **Registry 鮮度通知**                                   |        自動        |   $0   | 90日経過時audit-runner 警告 |

---

## 既存ツール接続マップ

```
[半期ごと]
/deep-research --provider gemini "JTBD Importance 学習者動機調査"
    └→ registry.jtbd_satisfaction.importance 手動更新

[四半期ごと]
/deep-research --provider gemini "競合機能更新2026"
    └→ /competitive-tracker --import
        └→ competitor-registry.json 更新

[毎週/随時]
node .claude/scripts/audit-runner.mjs    ← $0 自動化
    ├→ ギャップレポート出力 (ターミナル)
    ├→ mece-feature-analysis.md 更新 (--save)
    ├→ 監査スナップショット保存 (--snapshot)
    └→ HIGH ギャップ発見時:
        └→ /market-intelligence-scanner (候補登録提案)
            └→ --accept 時:
                └→ /feature-architect (CONTEXT.json 生成)
                    └→ /feature-pilot (実装)

[優先順位調整必要時]
/priority-analyzer (全体ポートフォリオWSJF 再分析)
```

---

## 制限事項

| 制限                                 | 原因                            | 緩和方法                                                |
| ------------------------------------ | ------------------------------- | ------------------------------------------------------- |
| 競合非公開機能検出不可               | Deep Researchは公開情報のみ収集 | app-review-analyzerでユーザーレビューから新機能言及検出 |
| "業界標準"基準が恣意的               | 4+ アプリ保有 = 標準            | registryでthreshold 調整可能                            |
| 四半期更新間死角                     | Deep Research 周期的コスト      | 主要競合更新ニュースモニタリング推奨                    |
| 全てのギャップが価値あるわけではない | 戦略不一致ギャップ存在          | strategic_skip 分類でノイズ除去                         |
| Importance データ主観性              | 学習者調査ベースだが定量的限界  | 半期ごとDeep Research 更新 + 多重ソースクロス検証       |

---

## スキーマ: competitor-registry.json (v3)

```json
{
  "$schema": "competitor-registry-v3",
  "last_updated": "ISO 8601 date",
  "data_source": "出典説明",
  "next_refresh_due": "ISO 8601 date",
  "confidence_thresholds": {
    "high": 0.80,
    "medium": 0.50,
    "low": 0.30,
    "reject_below": 0.30,
    "auto_approve_above": 0.80,
    "stale_days": 90
  },
  "apps": [
    { "id": "string", "name": "string", "note": "string", "mau": "string" }
  ],
  "features": [
    {
      "id": "comp-NNN",
      "name": "機能名",
      "category": "Speaking|Writing|Reading|...",
      "sub_category": "詳細分類",
      "lifecycle": "L1-L8|cross",
      "domain": "D1-D8|P1-P8|cross",
      "apps": ["app_id"],
      "app_count": "number",
      "is_industry_standard": "boolean (app_count >= 4)",
      "app_depth": { "app_id": "1-5 depth score" },
      "assessments": {
        "app_id": {
          "has_feature": "boolean",
          "depth": "1-5|null",
          "confidence": "0.0-1.0",
          "evidence_excerpt": "string (最大200字)",
          "source_id": "R-YYYY-MM-DD-competitor-{app_id}",
          "last_verified": "ISO 8601 date"
        }
      },
      "hackathon_project_coverage": "feature_id|null|feature_id-partial",
      "hackathon_project_depth": "1-5|null",
      "gap_severity": "HIGH|MEDIUM|LOW|null",
      "gap_type": "missing|depth_gap|partial|null",
      "jtbd": ["job_id"],
      "strategic_skip": "boolean (optional)",
      "strategic_skip_reason": "string (optional)",
      "evidence": "根拠説明",
      "detected_date": "ISO 8601 date"
    }
  ],
  "extraction_log": [
    {
      "source_id": "R-YYYY-MM-DD-competitor-{app_id}",
      "app_id": "string",
      "extracted_at": "ISO 8601 timestamp",
      "model": "gemini-2.5-flash-preview-05-20",
      "feature_count": "number",
      "avg_confidence": "0.0-1.0",
      "low_confidence_count": "number"
    }
  ],
  "our_differentiators": [...],
  "jtbd_satisfaction": {
    "jobs": [{ "id": "string", "name": "string" }],
    "matrix": { "job_id": { "app_id": "1-5 score" } },
    "importance": {
      "_source": "Deep Research 出典",
      "_methodology": "方法論説明",
      "job_id": "1.0-5.0 importance score"
    }
  },
  "summary": {
    "total_features_tracked": "number",
    "industry_standards": "number",
    "our_gaps": { "HIGH": [], "MEDIUM": [], "LOW": [] },
    "fully_covered": "number",
    "partially_covered": "number",
    "depth_gaps": "number",
    "not_covered": "number",
    "coverage_rate_binary": "string (%)",
    "coverage_rate_weighted": "string (%)",
    "our_unique_differentiators": "number"
  }
}
```

### v3 新規フィールド説明

| フィールド              | 位置                   | 説明                                                 |
| ----------------------- | ---------------------- | ---------------------------------------------------- |
| `confidence_thresholds` | ルート                 | 信頼度閾値 (スキル別カスタマイズ可能)                |
| `assessments`           | features[].assessments | アプリ別個別評価 (confidence, evidence, source 含む) |
| `extraction_log`        | ルート                 | Gemini 抽出履歴追跡 (監査/デバッグ用)                |
