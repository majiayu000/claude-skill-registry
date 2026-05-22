---
name: quality-review-flow
description: PR作成前の品質レビュー実行フロー、客観的品質基準、同一指摘検出、エスカレーション手順を定義
---

# 品質レビューフロー & 客観的品質基準

> **参照元**: implement-issues.md から分離された品質レビューロジック

---

## 1. 品質レビュー実行フロー ⚠️ 必須

> **⚠️ 重要**: PR作成前に必ず品質レビューを実行。スキップ厳禁。

### 1.1 レビューエージェント選択

| 実装内容 | エージェント |
|----------|-------------|
| バックエンド/CLI | `backend-reviewer` |
| フロントエンド | `frontend-reviewer` |
| DB関連 | `database-reviewer` |
| インフラ | `infra-reviewer` |
| セキュリティ | `security-reviewer` |

### 1.3 Token最適化（Diff-Driven Review）

> **⚠️ 重要**: レビュアーエージェントは、ファイル全体ではなく**変更差分**を中心にレビューすること。

1. **差分取得**: `git diff main...HEAD` で変更箇所のみを取得
2. **重点確認**: 差分とその周辺コンテキストのみを読み込む
3. **全文読み込み禁止**: ファイル全体の読み込みは、構造理解が必要な場合のみに限定する

```python
# レビューエージェントへの指示例
prompt = """
レビュー対象:
1. `git diff main...HEAD` の出力（変更点）
2. 変更されたファイルの関連箇所（全体ではない）

確認事項:
- 変更が要件を満たしているか
- 既存機能を破壊していないか
"""
```

### 1.4 スコア判定基準

> **参照**: 閾値の正式定義は {{skill:workflow-phase-convention}} §レビュースコア閾値を参照

| スコア | アクション |
|--------|----------|
| 9-10点 | ✅ PR作成へ |
| 7-8点 | 修正 → 再レビュー |
| 6点以下 | 設計見直し |

---

## 2. 客観的品質基準（必須条件）★SSOT★

> **このセクションが客観的品質基準の唯一の定義（Single Source of Truth）です。**
> 他ファイルからはこのセクションを参照してください。

レビュースコアに加え、以下の**客観的基準**を満たす必要があります。
これらはAIの主観に依存せず、ツールで検証可能です。

### 2.1 ツール検証可能な基準

| 基準 | 検証コマンド（Rust） | 検証コマンド（TypeScript） | 必須 |
|------|---------------------|--------------------------|------|
| **Lintエラー 0件** | `cargo clippy -- -D warnings` | `npm run lint` | ✅ |
| **型エラー 0件** | `cargo check` | `npm run type-check` | ✅ |
| **フォーマット準拠** | `cargo fmt --check` | `npm run format:check` | ✅ |
| **テスト全通過** | `cargo test` | `npm test` | ✅ |
| **カバレッジ 80%以上** | `cargo tarpaulin` | `npm run coverage` | 推奨 |

### 2.2 到達可能性チェック（Reachability Check）

実装したコードがエントリポイントから呼び出されることを確認する。

| プロジェクト種別 | エントリポイント | 確認コマンド例 |
|-----------------|-----------------|---------------|
| Rust CLI | `src/main.rs` | `grep -E 'handler_name\|mod handler' src/main.rs` |
| Next.js App Router | `app/**/page.tsx` | 実装コンポーネントの import 確認 |
| Next.js Pages Router | `pages/**/*.tsx` | 実装コンポーネントの import 確認 |
| Express/Fastify | `src/app.ts` or `src/index.ts` | route/controller 参照確認 |
| Spring Boot | `*Application.java` | Bean/Component 参照確認 |

**アクション**:
- 参照がない場合 → エントリポイントを修正して統合
- import されていない場合 → use/import 文を追加
- **このチェックを通過しないとPR作成不可**

### 2.3 定義-使用相関チェック（Definition-Usage Correlation Check）

定義された引数/Props/パラメータが実際に使用されているかを確認する。

| プロジェクト種別 | 定義元 | 使用先 | 確認コマンド例 |
|-----------------|--------|-------|---------------|
| Rust CLI | `args.rs` (struct fields) | `handlers.rs` | `grep 'args\.field_name' src/` |
| Python CLI | `argparse.add_argument()` | handler関数 | 引数変数の使用確認 |
| REST API | OpenAPI spec / DTO | Controller | パラメータ使用確認 |
| React/Vue | Props 定義 | Component 本体 | props 参照確認 |

**アクション**:
- 未使用の定義がある場合 → **スタブとして報告**（実装を追加 or 定義を削除）
- **スタブ残存時の減点**: **-2点**

### 2.4 判定ルール

| 条件 | 結果 |
|------|------|
| 全基準クリア | PR作成可 |
| ツール検証失敗（Lint/型/テスト） | 修正必須、PR作成不可 |
| 到達可能性NG | 統合必須、PR作成不可 |
| 定義-使用相関NG（スタブあり） | -2点減点、軽微なら警告付きで続行可 |

> **Note**: 客観的基準が未達の場合、レビュースコアに関係なく PR 作成不可。

---

## 3. 同一指摘の検出（無限ループ防止）

同じ指摘が繰り返される場合は即座にエスカレーションします。

### 検出ルール

| 条件 | アクション |
|------|----------|
| 前回指摘と50%以上重複 | 即座にエスカレーション |
| 3回連続で9点未満 | Blocked状態へ移行 |

### レビューループフロー

```
レビュー実行 → スコア9点以上? → Yes → PR作成へ
                    ↓ No
              同一指摘50%以上? → Yes → エスカレーション
                    ↓ No
              リトライ回数 < 3? → Yes → 修正 → 再レビュー
                    ↓ No
              Blocked状態へ移行
```

---

## 4. 修正 & 再レビュー（TODO駆動インクリメンタル方式）

> **Token最適化**: レビュー指摘をTODOファイルに保存し、再実装時はTODOのみ参照。
> 設計書・既存コードの再読み込みを最小限に抑える。

### 4.1 TODOファイル生成（レビュー後）

レビュー指摘事項を構造化TODOファイルに保存：

**保存先**: `.review-todo/issue-{subtask_id}-attempt-{attempt}.md`

**TODOファイル形式**:
```markdown
# Review TODO: Issue #42
## Review Score: 7/10
## Attempt: 1/3

### 指摘事項（優先度順）
- [ ] **HIGH**: エラーハンドリング不足 (File: handlers.rs, Line: 45)
- [ ] **MEDIUM**: 命名規則違反 (File: args.rs, Line: 12)

### 修正ガイド
| 指摘 | 修正方針 | 参照セクション |
|------|---------|--------------|
| エラーハンドリング... | Result型でラップ | ## エラー処理 |
| 命名規則違反... | snake_caseに修正 | N/A |

### ⚠️ 再実装時の注意
- このTODOファイルのみ参照して修正
- 設計書の再読み込みは「参照セクション」が指定された場合のみ
```

### 4.2 TODO駆動の再実装フロー

```
📋 レビュー完了（スコア < 9）
     ↓
💾 TODOファイル生成 (.review-todo/issue-N-attempt-M.md)
     ↓
🔧 再実装（TODOファイルのみ参照）
     ├─ 指摘事項を上から順に修正
     ├─ 修正完了したらチェック☑
     └─ 「参照セクション」がある場合のみ設計書をピンポイント読み込み
     ↓
🧪 テスト再実行
     ↓
📝 再レビュー依頼（修正サマリ付き）
```

### 4.3 再レビュー呼び出し

再レビュー時は以下の情報のみを渡す（トークン最適化）：

| 渡す情報 | 内容 |
|---------|------|
| 前回スコア | `7/10` など |
| 修正TODOファイル | `.review-todo/issue-N-attempt-M.md` の内容 |
| 修正サマリ | 何を修正したかの簡潔な説明 |

> **禁止**: 設計書・コード全文の再読み込み

### 4.4 Token節約効果（推定）

> **Note**: 以下は設計書全文（2,000-5,000トークン）をTODOファイル（300-500トークン）に置き換えた場合の推定値です。
> 実際の削減率はプロジェクトの設計書サイズやレビュー指摘数に依存します。

| フェーズ | 従来方式 | TODO駆動方式 | 推定削減率 |
|---------|---------|-------------|--------|
| 1回目レビュー後 | 設計書全文 + コード全文読み込み | TODOファイルのみ | 約60-70% |
| 2回目レビュー後 | 設計書全文 + コード全文読み込み | TODOファイルのみ | 約60-70% |
| 3回目レビュー後 | 設計書全文 + コード全文読み込み | TODOファイルのみ | 約60-70% |

**推定累積効果**: 3回のレビューループで数千トークン節約

### 4.5 TODOファイルのセッション間永続化

> **重要**: TODOファイルはcontainer-use環境内に保存されるため、セッション間で永続化される。

#### GitHub Issue との連携

> **状態管理API**: {{skill:github-issue-state-management}} を参照

| タイミング | 操作 |
|-----------|------|
| TODOファイル生成時 | Issue にコメントを追加（`gh issue comment`） |
| Phaseを `review-fix` に更新 | `issue-state.sh phase <num> 7-review` |
| セッション再開時 | Issue コメントから直近の review-todo を検索 |

#### ディレクトリ構造

```
.review-todo/
├── issue-42-attempt-1.md    # 1回目レビュー後のTODO
├── issue-42-attempt-2.md    # 2回目レビュー後のTODO
├── issue-42-attempt-3.md    # 3回目レビュー後のTODO（Blocked判定）
└── .gitignore               # Git管理外（環境内のみ）
```

### 4.6 Blocked状態への移行

レビュー3回失敗時、Issue を `blocked` 状態に更新（{{skill:github-issue-state-management}} API）：

```bash
bash .opencode/skill/github-issue-state-management/scripts/issue-state.sh block <issue-num> review_loop_exceeded "レビュー3回失敗（最終スコア: X/10）"
```

その後、Draft PRを作成して中断。

---

## 5. レビュー失敗時のエスカレーション

3回連続でスコア9点未満の場合：

1. Issue に `env:blocked` ラベルを追加、Blocked コメントを投稿
2. Draft PRを作成（`--draft`フラグ）
3. PRの本文に「レビュー未通過」と明記
4. 未解決の指摘事項をPRコメントに記載
5. ユーザーに報告して判断を仰ぐ
