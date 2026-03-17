---
name: analyze-what-to-build
description: |
  競合分析パイプラインのオーケストレーター。competitive-tracker → market-intelligence-scanner → priority-analyzer を
  順次呼び出して「次に何を作るべきか?」に対するデータ駆動の回答を提供する。
  "何作る", "次の機能", "パイプライン分析", "ポートフォリオ分析", "what to build" などの要求でトリガーされる。
version: 1.2
updated: 2026-02-09
doc_contract:
  review_interval_days: 90
---

# Analyze What to Build v1.0

競合分析パイプラインの**オーケストレーター**。3つのスキルを順次呼び出して「次に何を作るべきか?」に対する**データ駆動**の回答を提供する。

**核心価値**: 検出(Stage 1) → 候補生成(Stage 2) → 優先順位(Stage 3) → 意思決定(Stage 4)

---

## パイプラインアーキテクチャ

```
[Stage 1: competitive-tracker]        ($0, ~2秒)
  audit-runner.mjs
  └→ docs/analysis/gap-candidates.json  (Bridge Artifact)
         │
         │ gap-candidates-v1 contract
         ▼
[Stage 2: market-intelligence-scanner] (~sonnet 1回)
  Phase 0.5: gap-candidates.json ロード + 重複検査
  Phase 1-6: docs/research/*.md スキャン + 候補生成
  └→ scan-status.json (v4)
         │
         │ scan-status-v4 contract
         ▼
[Stage 3: priority-analyzer]           (~sonnet 1回)
  Phase 0: scan-status.json 候補ロード + Provisional RICE
  Phase 1-4: Multi-Source RICE 計算 (BRIEF+SPEC+CONTEXT+Registry)
  └→ 統合ランキング出力
         │
         ▼
[Stage 4: 意思決定支援]               (インタラクティブ)
  ユーザーに行動選択提示
```

---

## トリガー条件

次の要求でこのスキル使用:

- "何作る", "次の機能何?"
- "パイプライン分析して"
- "ポートフォリオ分析"
- "what to build", "analyze what to build"

---

## ワークフロー

### Stage 1: 競合ギャップ分析 (自動, $0)

> `node .claude/scripts/audit-runner.mjs --json --save --snapshot`

- competitor-registry.json → ギャップ分析実行
- gap-candidates.json 自動生成
- 所要: ~2秒, 費用: $0

**`--skip-audit` フラグ時**: gap-candidates.jsonが存在しfreshness_ttl_days以内ならStage 1 skip.

**出力要約**:

```
## Stage 1 結果: 競合ギャップ分析

- 総ギャップ: {N}個 (HIGH: {n}, MEDIUM: {n}, LOW: {n})
- 新規actionable ギャップ: {n}個
- 既に追跡中: {n}個
- 戦略的skip: {n}個
```

---

### Stage 2: 候補生成 (AI, ~sonnet 1回)

> `/market-intelligence-scanner` 呼び出し (Phase 0.5 + Phase 1-6)

- gap-candidates.jsonから未追跡ギャップ候補生成
- docs/research/\*.mdから研究ベース候補生成
- Evidence Gate 適用 (証拠なし候補遮断)

**`--dry-run` フラグ時**: 候補生成なしで分析結果のみ出力.

**出力要約**:

```
## Stage 2 結果: 候補生成

- ギャップベース新規候補: {n}個
- 研究ベース新規候補: {n}個
- 重複検出 (hybridで統合): {n}個
- 現在pending_review 合計: {n}個
```

---

### Stage 3: 統合優先順位ランキング (AI, ~sonnet 1回)

> `/priority-analyzer --all --candidates` 呼び出し

- 既存機能: RICE 確定スコア (BRIEF+SPEC+CONTEXT+Registry 多重ソース)
- 待機候補: Provisional RICE スコア
- 統合ランキング生成

**出力要約**:

```
## Stage 3 結果: 統合優先順位ランキング

### A. 既存機能 Top 5
| Rank | ID  | Name | RICE  | R | I | C | E(pw) |
|------|-----|------|-------|---|---|---|-------|

### B. 待機候補 Top 5
| Rank | Candidate | ICE  | Prov.RICE | Source | Gap Ref |
|------|-----------|------|-----------|--------|---------|

### C. 推奨: 次の変換対象
| Priority | Candidate | 根拠 |
|----------|-----------|------|
```

---

### Stage 4: 意思決定支援 (インタラクティブ)

統合ランキング表示後ユーザーに行動選択:

| 選択     | コマンド                                     | 説明               |
| -------- | -------------------------------------------- | ------------------ |
| 候補承認 | `/market-intelligence-scanner --accept <id>` | 機能に変換         |
| 候補却下 | `/market-intelligence-scanner --reject <id>` | 理由記録後却下     |
| 候補保留 | `/market-intelligence-scanner --defer <id>`  | 日付指定保留       |
| 詳細分析 | 候補文書を開く                               | 特定候補深掘り分析 |
| 終了     | (なし)                                       | パイプライン完了   |

#### Post-Accept Quality Gate (必須)

> `--accept` 実行後 **feature-architect** 呼び出し前に下記項目を必ず検証する。

|  #  | 検証項目                     | 処置                                                                                                                       | 違反時                               |
| :-: | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
|  1  | **feature_type 分類**        | CONTEXT.jsonに `feature_type` 設定 (`ui_feature` / `backend_feature` / `system_feature` / `strategy_feature`)              | SPEC 生成時Screen必須判定不可        |
|  2  | **Screen Enforcement Chain** | `ui_feature` → feature-spec-generatorがscreens/ 必須生成 → Readiness Gate Phase 2.1が検証 → validate_spec.pyがBLOCKING遮断 | Screen文書欠落でReadiness Gate No-Go |
|  3  | **feature-pilot 経由推奨**   | 候補変換後実装時必ず `/feature-pilot`をオーケストレーターとして使用 (直接feature-implementer呼び出し禁止)                  | Readiness Gate迂回で品質ゲート無効化 |

**feature_type 自動分類基準**:

| 判別条件                          |    feature_type    | 例                                    |
| --------------------------------- | :----------------: | ------------------------------------- |
| ユーザー対面画面/UI存在           |    `ui_feature`    | 書き取り、単語帳、AI チューター       |
| サーバーロジック/バックエンドのみ | `backend_feature`  | AI コスト監視、コンテンツパイプライン |
| インフラ/システム運用             |  `system_feature`  | オフラインモード、プッシュ通知        |
| 非技術戦略                        | `strategy_feature` | ユーザー獲得、リテンション戦略        |

---

## コマンド

```bash
# 全体パイプライン実行
/analyze-what-to-build

# Stage 2から開始 (既存gap-candidates.json使用)
/analyze-what-to-build --stage 2

# Stage 1のみ実行 (ギャップ分析のみ)
/analyze-what-to-build --stage 1

# Stage 1 省略 (gap-candidates.jsonが最新の時)
/analyze-what-to-build --skip-audit

# 候補生成なしで分析結果のみ出力
/analyze-what-to-build --dry-run
```

### フラグ説明

| Flag           | 説明                                         |
| -------------- | -------------------------------------------- |
| `--stage <N>`  | 特定Stageから開始 (以前Stage結果存在前提)    |
| `--skip-audit` | Stage 1 省略 (gap-candidates.jsonが最新の時) |
| `--dry-run`    | 候補生成なしで分析結果のみ出力               |

---

## 核心原則

### 1. コスト効率性

- Stage 1は $0 (Node.js スクリプト)
- Stage 2-3は sonnet 各1回 (~$0.10-0.30)
- 総パイプラインコスト: ~$0.20-0.60

### 2. 増分実行

- `--stage` フラグで部分実行可能
- 各Stageは独立産出物を残す (Bridge Artifact パターン)
- 以前Stage結果が最新なら再実行不要

### 3. データ契約 (Pipeline Contract)

- Stage間データフローは明示的スキーマで保証
- gap-candidates-v1, scan-status-v4 契約遵守
- freshness SLOでstale データ自動検出

### 4. インタラクティブ意思決定

- Stage 4でユーザー選択待機
- 候補承認/却下/保留アクション提供
- Provisional RICEは参考指標 (正式RICEは変換後算出)

---

## データフロー契約

| Artifact              | 生成者            | 消費者                    | スキーマ          | Freshness SLO |
| --------------------- | ----------------- | ------------------------- | ----------------- | :-----------: |
| `gap-candidates.json` | audit-runner.mjs  | MIS Phase 0.5             | gap-candidates-v1 |     90日      |
| `scan-status.json`    | MIS               | priority-analyzer Phase 0 | scan-status-v4    |     30日      |
| `CONTEXT.json`        | priority-analyzer | (既存機能)                | rice-v1           |     14日      |

---

## 関連スキル

| スキル                         | 役割                                                                  | Stage |
| ------------------------------ | --------------------------------------------------------------------- | :---: |
| `/competitive-tracker`         | 競合ギャップ分析 + gap-candidates.json 生成                           |   1   |
| `/market-intelligence-scanner` | 候補生成 + scan-status.json 管理                                      |   2   |
| `/priority-analyzer`           | RICE 算出 + 統合ランキング                                            |   3   |
| `/feature-architect`           | 承認された候補 → SPEC + Screen 生成 (後続)                            |  4→   |
| `/feature-pilot`               | **実装オーケストレーター** — Readiness Gate + Screen Enforcement 含む |  4→   |

---

## Stage 失敗処理 (Failure Handling)

各Stage失敗時パイプラインを安全に中断しユーザーに明確な状態を伝達する。

| Stage | 失敗タイプ                     | 対応                       | ユーザーメッセージ                                                                                                |
| :---: | ------------------------------ | -------------------------- | ----------------------------------------------------------------------------------------------------------------- |
|   1   | audit-runner.mjs 実行エラー    | パイプライン中断           | "Stage 1 失敗: audit-runner エラー. `node .claude/scripts/audit-runner.mjs --validate`で registry 整合性確認必要" |
|   1   | competitor-registry.json なし  | パイプライン中断           | "Stage 1 失敗: competitor-registry.jsonがありません. `/competitive-tracker --import`で生成してください"           |
|   2   | MIS 呼び出し失敗               | Stage 2 skip, Stage 3 進行 | "⚠️ Stage 2 skip: MIS 呼び出し失敗. 既存scan-status.jsonでStage 3 進行"                                           |
|   2   | scan-status.json 未生成        | Stage 3でPhase 0 skip      | "⚠️ scan-status.json なし: Stage 3で既存機能のみランキングします"                                                 |
|   3   | priority-analyzer 呼び出し失敗 | パイプライン中断           | "Stage 3 失敗: priority-analyzer エラー. Stage 1-2 産出物は保存済み. `--stage 3`で再試行可能"                     |

**核心原則**:

- Stage 1 失敗 → 全体中断 (基盤データなし)
- Stage 2 失敗 → 可能ならStage 3 進行 (graceful degradation)
- Stage 3 失敗 → 中断しつつ以前産出物保存 (`--stage 3`で再試行)
- 全失敗時どのStageまで成功したか明示

---

## 制限事項

| 制限                                       | 原因                          | 緩和                   |
| ------------------------------------------ | ----------------------------- | ---------------------- |
| gap-candidates.json なければStage 2 制限的 | audit-runner 未実行           | Stage 1 自動実行       |
| Provisional RICEは近似値                   | ICE→RICE マッピングの情報損失 | 変換後正式RICE再算出   |
| リサーチ文書最新性                         | 四半期更新周期                | Deep Research 更新推奨 |
| 同時実行不可                               | Stage間依存性                 | 順次実行必須           |

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                                                                            |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------- |
| 2026-02-09 | v1.2       | Stage 4 Post-Accept Quality Gate 追加: feature_type 自動分類, Screen Enforcement Chain 参照, feature-pilot 経由推奨 |
| 2026-02-09 | v1.1       | WSJF→RICE 切替反映: Stage 3 出力形式, データ契約更新                                                                |
| 2026-02-07 | v1.0       | 初期生成 - Pipeline Contract System オーケストレーター                                                              |
