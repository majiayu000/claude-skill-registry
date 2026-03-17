---
name: sisyphus-implementation-guide
description: Sisyphus専用の実装フロー、Subtask処理、Phase別責任分担、チェックリスト、完了報告フォーマットを定義
---

# Sisyphusへの指示（必読）

> **参照元**: implement-issues.md から分離されたSisyphus専用実行指示
> **このセクションはSisyphus専用の実行指示です。上記ルールの要約版。**

---

## 🔄 実装フロー

```
1. Issue受領
     ↓
2. 【単一Issue指定時】Subtask自動検出 ★重要★
     ├─ Subtaskあり → Step 3へ（Subtask単位で実装）
     └─ Subtaskなし → 粒度チェックへ（Step 4へ）
     ↓
3. 粒度チェック（200行以下か?）
     ├─ No（大きい）→ `/decompose-issue` を実行してから再度呼び出し
     └─ Yes（適切）→ 実装開始
     ↓
4. 各Subtaskを順次実装（container-worker）
     ※ 各Subtaskが独立した実装フローを実行:
        ブランチ → 環境 → TDD → レビュー(9点以上までループ) → PR
     ↓
5. CI監視 → マージ（各PR単位）
     ↓
6. 次のSubtaskへ（Step 4に戻る）
     ↓
7. 全Subtask完了 → 親Issue自動クローズ
```

---

## 実装フローの単位

| 状況 | 実装単位 | 作成されるもの |
|------|---------|---------------|
| Subtaskなし | Issue単位 | 1ブランチ、1環境、1レビューループ、1PR |
| Subtaskあり | **Subtask単位** | **N個のブランチ、N個の環境、N個のレビューループ、N個のPR** |

---

## 各Subtaskで実行される完全フロー

```
Subtask #N:
  ブランチ作成 → container-use環境
       ↓
  TDD実装 (Red → Green → Refactor)
       ↓
  品質レビュー ←──────┐
       ↓             │
  9点以上? ──No────→ 修正（最大3回）
       ↓ Yes
  ユーザー承認
       ↓
  PR作成 → CI監視 → マージ → 環境削除
       ↓
  ✅ このSubtask完了 → 次のSubtaskへ
```

---

## ⚡ Subtask自動検出（単一Issue指定時は必須）

> **⚠️ 重要**: Subtaskがある場合、**各Subtaskごとに独立したfeatureブランチ・container-use環境・PR**を作成する。

詳細は [Subtask検出 & 依存関係解決](./subtask-detection.md) を参照。

---

## 粒度判定（実装開始前に必須）

| 推定コード量 | 対応 |
|-------------|------|
| **200行以下** | → そのまま実装 |
| **200行超** | → **`/decompose-issue` で分割してから再実行** |

詳細は [Issue粒度判定](./issue-size-estimation.md) を参照。

---

## 実装フロー（分岐条件）

| 状況 | 処理方法 | 作成されるもの |
|------|---------|---------------|
| **Subtaskあり** | 各Subtask単位で**順次**実装 | Subtask数 × (ブランチ + 環境 + PR) |
| **Subtaskなし + 200行以下** | Issue単位で直接実装 | 1ブランチ + 1環境 + 1PR |
| **Subtaskなし + 200行超** | `/decompose-issue` で分割 | - |
| **複数親Issue指定** | 各親Issue単位で**並列**実装 | 親Issue数 × (Subtask数 × ブランチ + 環境 + PR) |

---

## Phase別の責任分担（SSOT）

> **Note**: 以下のフローは**Issue単位でもSubtask単位でも同一**。
> **この表がPhase責任の唯一の定義（Single Source of Truth）です。**

### 責任分担マトリクス

| Phase | 実行者 | 内容 | 入力 | 出力 | ラベル操作 |
|-------|--------|------|------|------|-----------|
| **0** | Sisyphus | Subtask検出 & ブランチ作成 | Issue ID | branch_name, subtask_list | `+env:active +phase:0-branch` |
| **1** | container-worker | 環境構築 | branch_name | env_id | `phase:1-env` |
| **2** | container-worker | 設計書参照（マトリクス使用） | task_type | context | `phase:2-design` |
| **3** | container-worker | **設計書実現性チェック** | context | **OK/NG** | `phase:3-check`（NGなら`+env:blocked`） |
| **4** | container-worker | TDD: テスト作成（Red） | context, test_spec | test_files | `phase:4-red` |
| **5** | container-worker | TDD: 実装（Green） | test_files | impl_files | `phase:5-green` |
| **6** | container-worker | TDD: リファクタ | impl_files | impl_files (refined) | `phase:6-refactor` |
| **6.5** | container-worker | **実装完了自己チェック** | impl_files | **OK/NG** | - |
| **6.6** | container-worker | **設計書整合性チェック** | impl_files, design_doc | **OK/NG** | -（NGならPhase 5に戻る） |
| **7** | container-worker | 品質レビュー（+ ストレステスト任意） | impl_files | review_result | `phase:7-review`（任意: `8-stress`） |
| **9** | container-worker | ユーザー承認依頼 | review_score | approval | `phase:9-approval` |
| **10** | container-worker | コミット & プッシュ & PR作成 | approval | pr_number | `phase:10-pr +env:pr-created` |
| **11** | Sisyphus | CI監視 | pr_number | ci_status | `phase:11-ci` |
| **12** | Sisyphus | マージ & 環境削除 & 親Issueクローズ | ci_status, env_id | merged, closed | `phase:12-merge +env:merged` |

> **Note**: Phase 0〜10 は container-worker、Phase 11-12 は Sisyphus が担当。
> Phase 6.6（設計書整合性チェック）は**統合漏れ防止のため必須**。Phase 8 (ストレステスト) は任意のためスキップ可。

### ラベル操作ルール（必須）

> **API詳細**: {{skill:github-issue-state-management}} セクション「必須更新ポイント」を参照

| タイミング | 実行者 | 操作 | API |
|-----------|--------|------|-----|
| Phase開始時 | container-worker | Phaseラベル更新 | `issue-state.sh phase <num> <phase>` |
| Blocked発生時 | container-worker | ステータス変更 | `issue-state.sh block <num> <reason> "<説明>"` |
| PR作成時 | container-worker | ステータス + PR番号記録 | `issue-state.sh pr-created <num> <pr_number>` |
| マージ完了時 | Sisyphus | ステータス変更 | `issue-state.sh merged <num>` |

**⛔ 違反禁止**: Phase遷移時にラベルを更新しないこと。

### Token消費の最適化ポイント

> **Note**: 削減率は推定値です。実際の効果はプロジェクト構成に依存します。

| Phase | 最適化手法 | 推定効果 |
|-------|-----------|------|
| Phase 2 | 設計書参照マトリクス（必須セクションのみ） | 大幅削減（全文読込回避） |
| Phase 3 | **設計書実現性チェック**（Gate） | **手戻り防止**（無限Token消費回避） |
| Phase 6.5 | **実装完了自己チェック**（到達可能性/定義-使用相関） | **統合漏れ/スタブ残存防止** |
| Phase 7 | TODO駆動再実装（TODOファイルのみ参照） | 大幅削減（設計書再読込回避） |
| Phase 8 | ストレステスト（読み取り専用エージェント並列） | 並列実行で時間短縮 |
| Phase 7, 10 | Sisyphusからworkerへの委譲 | メインエージェントのコンテキスト維持 |

### 責任境界（厳格）

| 操作 | Sisyphus | container-worker | Phase |
|------|----------|------------------|-------|
| Subtask検出 | ✅ | ❌ | 0 |
| ブランチ作成 | ✅ | ❌ | 0 |
| 環境作成/操作 | ❌ | ✅ | 1 |
| 設計書参照 | ❌ | ✅ | 2-3 |
| TDD実装 | ❌ | ✅ | 4-6 |
| 品質レビュー | ❌ | ✅ | 7-8 |
| ユーザー承認依頼 | ❌ | ✅ | 9 |
| PR作成 | ❌ | ✅ | 10 |
| CI監視 | ✅ | ❌ | 11 |
| マージ | ✅ | ❌ | 12 |
| 環境削除 | ✅ | ❌ | 12 |
| 親Issueクローズ | ✅ | ❌ | 12 |

**⛔ 違反禁止**: container-workerがSisyphusの責任を実行すること、またはその逆。

---

## Subtask順次実装時の全体像

```
Sisyphus (親エージェント)
│
├── Subtask #9 を処理
│   ├── Phase 0: ブランチ作成 (feature/issue-9-data-types) [Sisyphus]
│   ├── Phase 1-10: container-worker → 実装 → PR #25
│   └── Phase 11-12: CI監視 → マージ → 環境削除 [Sisyphus]
│
├── Subtask #10 を処理（#9と並列可能なら同時実行）
│   ├── Phase 0: ブランチ作成 (feature/issue-10-timer-engine) [Sisyphus]
│   ├── Phase 1-10: container-worker → 実装 → PR #26
│   └── Phase 11-12: CI監視 → マージ → 環境削除 [Sisyphus]
│
└── Phase 12（最終）: 全Subtask完了 → 親Issue自動クローズ [Sisyphus]
```

---

## ⛔ 必須チェックリスト

### 実装前チェック
```
□ 【単一Issue指定時】Subtask検出を実行したか? ★最優先★
□ Issue粒度チェック（200行以下か?）
□ 大きい場合は `/decompose-issue` を案内したか?
```

### 実装中チェック
```
□ 【Subtaskあり】各Subtaskに独立したfeatureブランチを作成したか? ★重要★
□ 【Subtaskあり】各Subtaskに独立したcontainer-use環境を作成したか? ★重要★
□ 【Subtaskあり】各Subtaskで独立したレビューループを実行したか? ★重要★
□ 【Subtaskあり】各Subtaskに独立したPRを作成したか? ★重要★
□ 【レビュー】各Subtaskが9点以上を獲得するまでループしたか?
□ background_task を使用しているか?（⛔ task 禁止）
□ Subtaskは順次処理しているか?（1つ完了してから次へ）
```

### 設計書整合性チェック（Phase 6.6）★重要：統合漏れ防止★

> **詳細**: {{skill:quality-review-flow}} セクション2.5（設計書整合性チェック）を参照

```
□ 設計書「実装内容」の全項目が実装されているか?
□ 設計書「呼び出し元」の全統合ポイントで実際に呼び出されているか? ★最重要★
□ CLIコマンド（定義されている場合）が実際に動作するか?
□ E2Eフローが正常に動作するか?
□ 「呼び出し元」セクションがない場合、実装者が統合ポイントを特定し設計書に追記したか?
```

> **⛔ 禁止**: 設計書整合性チェックをスキップしてPhase 7（品質レビュー）に進むこと。
> **理由**: 単体テスト・コードレビューだけでは「機能が統合されているか」を検出できない。

### 機能完了チェック（PRマージ後の再確認）

> **重要**: Phase 6.5 で既にチェック済みだが、PRマージ後に再確認を推奨。
> **詳細**: {{skill:quality-review-flow}} セクション2（客観的品質基準）を参照

| チェック | 確認方法 | 必須 |
|---------|---------|------|
| **到達可能性** | エントリポイントからの参照確認（Phase 6.5で実施済み） | 再確認推奨 |
| **定義-使用相関** | 未使用の引数/Props/パラメータがないこと（Phase 6.5で実施済み） | 再確認推奨 |
| **Smoke Test** | `cargo run` / `npm run dev` で基本動作確認 | ✅ |
| Epic紐付け | Epic Issue の機能リスト（F-XXX）に完了マーク | 推奨 |

```
□ 【Smoke Test】アプリケーションが正常に起動・動作するか?
□ 全Subtask完了後、親Issueをクローズしたか?
```

---

## ツール使用ルール

| 操作 | 使用ツール | 備考 |
|------|-----------|------|
| container-worker起動 | `background_task` | ⛔ `task` 禁止（MCPツール継承されない） |
| 品質レビュー起動 | `task` | ✅ OK（レビューエージェントはMCP不要） |
| ファイル操作 | `container-use_environment_file_*` | ⛔ `edit`/`write` 禁止 |
| コマンド実行 | `container-use_environment_run_cmd` | ⛔ `bash` でのテスト/ビルド禁止 |
| CI監視・マージ | `bash` (gh コマンド) | ✅ OK（環境外のGitHub API操作） |
| 環境クリーンアップ | `delete_env.sh` (delete-environment skill) | ✅ OK（Sisyphusが実行） |
| 親Issueクローズ | `bash` (gh issue close) | 全Subtask完了後 |

---

## ⛔ よくある間違い

| ❌ 間違い | ✅ 正しい方法 |
|----------|-------------|
| **単一Issue指定時にSubtask検出をスキップ** | **必ず `detect_subtasks()` を実行** |
| 親IssueをそのままSubtaskなしで実装開始 | まずSubtask検出 → なければ粒度チェック |
| **Subtask全体で1つのブランチを共有** | **各Subtaskごとに独立したfeatureブランチを作成** |
| **Subtask全体で1つのPRを作成** | **各Subtaskごとに独立したPRを作成** |
| **Subtask全体で1つのcontainer-use環境を共有** | **各Subtaskごとに独立した環境を作成** |
| **レビューをスキップしてPR作成** | **各Subtaskで9点以上になるまでレビューループ** |
| **レビュー1回で諦めてPR作成** | **最大3回までリトライ、それでも失敗ならDraft PR** |
| 大きなIssueをそのまま実装 | `/decompose-issue` で分割してから実装 |
| `task(subagent_type="container-worker", ...)` | `background_task(agent="container-worker", ...)` |
| Subtaskを並列実行 | Subtaskは順次実行（1つ完了してから次へ） |
| 全Subtask完了後、親Issueを放置 | 必ず自動クローズ処理を実行 |
| **設計書整合性チェック(Phase 6.6)をスキップ** | **必ず「呼び出し元」からの統合を確認してからレビューへ** ★新規★ |
| **クラス/関数を作成したが呼び出し元を実装しない** | **設計書「呼び出し元」セクションの全ポイントで呼び出しコードを実装** ★新規★ |
| **CLIコマンドを定義したが実際に動作確認しない** | **`{command} --help` と基本動作を必ず確認** ★新規★ |

---

## 完了報告フォーマット

```markdown
## 📋 実装完了サマリー

### 親Issue
- **#{parent_id}**: {parent_title} → ✅ Closed

### Subtask結果

| Subtask | ブランチ | 環境ID | レビュー | PR | CI | マージ |
|---------|---------|--------|---------|-----|-----|-------|
| #{s1} | feature/issue-{s1}-xxx | env-aaa | 10/10 (1回目) | PR #{p1} | ✅ | ✅ |
| #{s2} | feature/issue-{s2}-xxx | env-bbb | 9/10 (2回目) | PR #{p2} | ✅ | ✅ |

### 統計
- 総Subtask数: N
- 成功: N
- 失敗: 0
- レビュー平均スコア: X.X/10

### 環境クリーンアップ
- ✅ env-aaa 削除済み
- ✅ env-bbb 削除済み
```
