---
name: harness-review
description: "コード・プラン・スコープを多角的にレビュー。品質の番人、参上。Use when user mentions reviews, code review, plan review, scope analysis, security, performance, quality checks, PRs, diffs, or change review. Do NOT load for: implementation work, new feature development, bug fixes, or setup."
description-en: "Multi-angle review of code, plans, and scope. Quality guardian at your service. Use when user mentions reviews, code review, plan review, scope analysis, security, performance, quality checks, PRs, diffs, or change review. Do NOT load for: implementation work, new feature development, bug fixes, or setup."
description-ja: "コード・プラン・スコープを多角的にレビュー。品質の番人、参上。Use when user mentions reviews, code review, plan review, scope analysis, security, performance, quality checks, PRs, diffs, or change review. Do NOT load for: implementation work, new feature development, bug fixes, or setup."
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task"]
context: fork
argument-hint: "[code|plan|scope]"
hooks:
  - event: PreToolCall
    type: command
    command: "${CLAUDE_PLUGIN_ROOT}/scripts/check-codex.sh"
    once: true
---

# Review Skills

コードレビュー、計画レビュー、スコープ分析を担当するスキル群です。
コンテキストからレビュータイプを自動判定します。

## レビュータイプ（Context-Aware）

レビュータイプはコンテキストから自動判定されます：

| Recent Activity | Review Type | 4 Experts |
|-----------------|-------------|-----------|
| `/plan-with-agent` 後 | **Plan Review** | Clarity, Feasibility, Dependencies, Acceptance |
| `/work` 後 | **Code Review** | Security, Performance, Quality, Accessibility |
| タスク追加後 | **Scope Review** | Scope-creep, Priority, Feasibility, Impact |

### 手動指定

```bash
/harness-review           # 自動判定
/harness-review code      # コードレビュー強制
/harness-review plan      # 計画レビュー強制
/harness-review scope     # スコープ分析強制
```

---

## 機能詳細（Code Review）

| 機能 | 詳細 |
|------|------|
| **変更レビュー** | See [references/changes-review.md](references/changes-review.md) |
| **品質チェック** | See [references/quality-review.md](references/quality-review.md) |
| **セキュリティ** | See [references/security-review.md](references/security-review.md) |
| **パフォーマンス** | See [references/performance-review.md](references/performance-review.md) |
| **アクセシビリティ** | See [references/accessibility-review.md](references/accessibility-review.md) |
| **SEO/OGP** | See [references/seo-review.md](references/seo-review.md) |
| **Codex 統合** | See [references/codex-integration.md](references/codex-integration.md) |
| **コミット判定** | See [references/commit-judgment-logic.md](references/commit-judgment-logic.md) |

## 機能詳細（Plan/Scope Review）

Plan Review と Scope Review は Codex エキスパートを使用します：

| レビュータイプ | エキスパート | 参照 |
|--------------|-------------|------|
| **Plan Review** | Clarity, Feasibility, Dependencies, Acceptance | `../codex-review/references/experts/clarity-expert.md` 等 |
| **Scope Review** | Scope-creep, Priority, Feasibility, Impact | `../codex-review/references/experts/scope-creep-expert.md` 等 |

詳細: [../codex-review/references/codex-parallel-review.md](../codex-review/references/codex-parallel-review.md)

## 実行手順

1. **品質判定ゲート**（Step 0）
2. **残コンテキスト確認（Codex モード時）**（Step 1）
3. ユーザーのリクエストを分類
4. **（Claude-mem 有効時）過去のレビュー指摘を検索**
5. 並列実行の判定（下記参照）
6. 上記の「機能詳細」から適切な参照ファイルを読む、または並列サブエージェント起動
7. 結果を統合してレビュー完了

### 入力の優先順位

- `files` が渡されている場合は **そのファイルのみ** を対象にレビューする
- `files` が渡されていない場合は `git_diff` から変更箇所を推定する
- `context_from: code_content` が渡されている場合は **その内容を優先** してレビューする

### Step 0: 品質判定ゲート（レビュー重点領域の特定）

レビュー開始前に変更内容を分析し、重点領域を特定:

```
変更ファイル分析
    ↓
┌─────────────────────────────────────────┐
│           品質判定ゲート                 │
├─────────────────────────────────────────┤
│  判定項目:                              │
│  ├── カバレッジ不足？（テストなし）     │
│  ├── セキュリティ注意？（auth/api/）    │
│  ├── a11y 注意？（UI コンポーネント）   │
│  └── パフォーマンス注意？（DB/ループ）  │
└─────────────────────────────────────────┘
          ↓
    重点レビュー領域を決定
```

#### カバレッジ判定

| 状況 | 指摘内容 |
|------|---------|
| 新規ファイルにテストなし | 「テストが不足しています」 |
| 変更ファイルのテストが古い | 「テストの更新を検討してください」 |
| カバレッジ < 60% | 「カバレッジ向上を推奨」 |

#### セキュリティ重点レビュー

| パス | 追加チェック項目 |
|------|-----------------|
| auth/, api/ | OWASP Top 10 チェックリスト |
| 入力処理 | サニタイズ、バリデーション |
| DB クエリ | パラメータ化確認 |

#### a11y 重点レビュー

| パス | チェック項目 |
|------|------------|
| src/components/ | alt, aria, キーボード操作 |
| src/pages/ | 見出し構造, フォーカス管理 |

#### パフォーマンス重点レビュー

| パターン | 警告内容 |
|---------|---------|
| ループ内 DB クエリ | N+1 クエリの可能性 |
| 大規模データ処理 | ページネーション検討 |
| useEffect 乱用 | レンダリング最適化 |

#### SEO/OGP 重点レビュー

| パス | チェック項目 |
|------|------------|
| src/pages/, app/ | title, description, canonical |
| public/ | robots.txt, sitemap.xml, OGP 画像 |
| layout.tsx, _document.tsx | viewport, OGP タグ, Twitter Card |

#### クロスプラットフォーム重点レビュー

| パス | チェック項目 |
|------|------------|
| src/components/, app/ | レスポンシブ（固定幅チェック） |
| *.css, *.scss, tailwind | 100vw 使用、overflow 設定 |
| public/ | favicon, apple-touch-icon |

#### 重点レビュー統合出力

```markdown
📊 品質判定結果 → 重点レビュー領域

| 判定 | 該当 | 対象ファイル |
|------|------|-------------|
| セキュリティ | ⚠️ | src/api/auth.ts |
| カバレッジ | ⚠️ | src/utils/helpers.ts (テストなし) |
| a11y | ✅ | - |
| パフォーマンス | ✅ | - |
| SEO/OGP | ⚠️ | app/layout.tsx (OGP 未設定) |
| クロスプラットフォーム | ✅ | - |

→ セキュリティ・カバレッジ・SEO を重点的にレビュー
```

#### LSP ベースの影響分析（推奨）

変更レビュー時に LSP ツールで影響範囲を確認:

| 変更タイプ | LSP 操作 | 確認内容 |
|-----------|---------|---------|
| 関数シグネチャ変更 | findReferences | 全呼び出し元が対応済みか |
| 型定義変更 | findReferences | 使用箇所での型互換性 |
| API 変更 | incomingCalls | 影響を受けるエンドポイント |

**レビューフロー**:
1. 変更ファイルを特定
2. `LSP.findReferences` で影響範囲を列挙
3. 影響を受けるファイルも含めてレビュー

**使用例**:
```
# 1. 変更された関数の参照箇所を確認
LSP operation=findReferences filePath="src/api/user.ts" line=42 character=15

# 2. 関数の呼び出し階層を確認
LSP operation=incomingCalls filePath="src/api/user.ts" line=42 character=15

# 3. 型定義の使用箇所を確認
LSP operation=findReferences filePath="src/types/api.ts" line=10 character=12
```

**出力例**:
```markdown
🔍 LSP 影響分析結果

変更: updateUserProfile() のシグネチャ変更

影響を受ける箇所:
├── src/pages/profile.tsx:89 ⚠️ 引数更新必要
├── src/pages/settings.tsx:145 ⚠️ 引数更新必要
├── tests/user.test.ts:67 ✅ 更新済み
└── src/api/admin.ts:23 ⚠️ 引数更新必要

→ 3箇所で引数の更新が必要
```

> **注**: LSP サーバーが設定されている言語でのみ動作します。

### Step 1: 残コンテキスト確認（Codex モード時）

Codex モード（`review.mode: codex`）の場合は、**残コンテキストが 30%以下なら /compact を先に実行**してください。

> **注意**: /compact 後も余裕が少ない場合は縮退せず続行します。

### Git log 拡張フラグの活用（CC 2.1.49+）

レビュー時のコミット分析で構造化されたログを活用します。

#### 変更履歴の構造化分析

```bash
# 構造化フォーマットでコミット履歴取得
git log --format="%h|%s|%an|%ad" --date=short -10

# マージコミットを除外してレビュー
git log --cherry-pick --no-merges main..HEAD

# 変更ファイル一覧付き
git log --raw -5
```

#### 主な活用場面

| 用途 | フラグ | 効果 |
|------|--------|------|
| **コミット一覧取得** | `--format="%h|%s"` | 構造化された簡潔なログ |
| **レビュー対象の明確化** | `--cherry-pick --no-merges` | マージコミット除外 |
| **変更影響分析** | `--raw` | ファイル変更の詳細表示 |
| **時系列での原因追跡** | `--topo-order` | トポロジカルソート |

#### 出力例

```markdown
📊 コミット履歴分析（構造化）

| Hash | Subject | Author | Date |
|------|---------|--------|------|
| a1b2c3d | feat: add auth | Alice | 2026-02-04 |
| e4f5g6h | fix: cors error | Bob | 2026-02-03 |

変更ファイル（--raw）:
├── src/auth.ts (Modified)
├── src/api/middleware.ts (Added)
└── tests/auth.test.ts (Modified)

→ 認証周りの変更を重点的にレビュー
```

### Step 2: 過去のレビュー指摘検索（Memory-Enhanced）

Claude-mem が有効な場合、レビュー開始前に過去の類似指摘を検索:

```
# mem-search で過去のレビュー指摘を検索
mem-search: type:review "{変更ファイルのパターン}"
mem-search: concepts:security "{セキュリティ関連のキーワード}"
mem-search: concepts:gotcha "{変更箇所に関連するキーワード}"
```

**表示例**:

```markdown
📚 過去のレビュー指摘（関連あり）

| 日付 | 指摘内容 | ファイル |
|------|---------|---------|
| 2024-01-15 | XSS脆弱性: innerHTML 使用禁止 | src/components/*.tsx |
| 2024-01-20 | N+1クエリ: prefetch 必須 | src/api/*.ts |

💡 今回のレビューで上記パターンを重点チェック
```

> **注**: Claude-mem が未設定の場合、このステップはスキップされます。

## レビューモードの選択

レビュースキルは 2 つのモードで動作します:

```
設定確認: .claude-code-harness.config.yaml
    ↓
├── review.mode: default → Claude 単体レビュー
└── review.mode: codex   → Codex 並列レビュー（レビュータイプごとに4エキスパート）
```

### Default モード（Claude 単体）

Claude が直接レビューを実行。小〜中規模の変更に最適。

### Codex モード（並列エキスパート）

Codex CLI (`codex exec`) 経由で**レビュータイプに応じた4つのエキスパート**を **個別に並列呼び出し**:

| Review Type | エキスパート |
|-------------|-------------|
| **Code Review** | Security, Performance, Quality, Accessibility |
| **Plan Review** | Clarity, Feasibility, Dependencies, Acceptance |
| **Scope Review** | Scope-creep, Priority, Feasibility, Impact |

#### ⚠️ Codex モード実行時の必須ルール

**絶対に1回の `codex exec` 呼び出しで複数エキスパートをまとめないこと。**

```
✅ 正しい: 4回の `codex exec` 呼び出しを1つのレスポンス内で並列実行
❌ 間違い: 1回の呼び出しで「全観点をレビューして」と依頼（まとめ依頼）
```

**実行手順**:
1. **呼び出すエキスパートを判定**（全部ではなく必要なもののみ）:
   - 設定で `enabled: false` → 除外
   - CLI/バックエンド → Accessibility, SEO 除外
   - ドキュメントのみ変更 → Quality, Architect, Plan Reviewer, Scope Analyst を優先（Security, Performance は除外可）
2. 有効なエキスパートの `experts/*.md` からプロンプトを **個別に読み込む**
3. 有効なエキスパートのみ `codex exec` を **Bash バックグラウンドプロセスで並列実行**
4. 各結果を統合して判定

**詳細**: [codex-review/references/codex-parallel-review.md](../codex-review/references/codex-parallel-review.md)

**Codex モード有効化**:
```bash
/codex-mode on
```

**詳細**: [references/codex-integration.md](references/codex-integration.md)

---

## 並列サブエージェント起動（Default モード）

### 変更ファイル数・レビュー観点の算出（必須）

**files_count は merge-base 基準で算出すること**（staged/unstaged も含める）:

```bash
base=$(git merge-base HEAD origin/main 2>/dev/null \
  || git merge-base HEAD main 2>/dev/null \
  || git merge-base HEAD master 2>/dev/null \
  || git rev-parse HEAD~1 2>/dev/null \
  || git hash-object -t tree /dev/null)
committed=$(git diff --name-only --diff-filter=ACMRTUXB $base...HEAD)
staged=$(git diff --name-only --cached)
unstaged=$(git diff --name-only)
files=$(echo -e "$committed\n$staged\n$unstaged" | sort -u | grep -v '^$')
files_count=$(echo "$files" | wc -l)
```

**review_aspects はパスベースで検出**:

```javascript
function countReviewAspects(files) {
  let aspects = 0;
  if (files.some(f => /\/(auth|api|middleware|security)\//.test(f))) aspects++;
  if (files.some(f => /\/(db|sql|repository|cache)\//.test(f))) aspects++;
  if (files.some(f => /\/(components|pages|app)\/.*\.tsx$/.test(f))) aspects++;
  if (files.some(f => /\/(pages|app)\/.*\.(metadata|head|seo)/.test(f))) aspects++;
  return Math.max(aspects, 1);
}
```

以下の条件を**両方**満たす場合、Task tool で code-reviewer を並列起動:

- レビュー観点 >= 2（例: セキュリティ + パフォーマンス）
- 変更ファイル >= 5

**起動パターン（1つのレスポンス内で複数の Task tool を同時呼び出し）:**

```
Task tool 並列呼び出し:
  #1: subagent_type="code-reviewer"
      prompt="セキュリティ観点でレビュー: {files}"
  #2: subagent_type="code-reviewer"
      prompt="パフォーマンス観点でレビュー: {files}"
  #3: subagent_type="code-reviewer"
      prompt="コード品質観点でレビュー: {files}"
```

**小規模な場合（条件を満たさない）:**
- 子スキル（doc.md）を順次読み込んで直列実行

---

## 🔧 MCP Code Intelligence ツールの活用

レビューでは MCP ツール（AST-Grep, LSP）を活用して精度を向上します。

> **重要**: `/dev-tools-setup` で MCP サーバーが設定されている場合、標準ツール（Grep, Read）ではなく **MCP ツールを優先使用**してください。MCP ツールは構造的な検索が可能で、より正確な結果を得られます。

### AST-Grep MCP ツール（harness_ast_search）

**構造的なコードパターン検索**に使用します。正規表現ベースの Grep より精度が高く、コードスメル検出に最適です。

| 検出パターン | AST-Grep パターン | 用途 |
|-------------|------------------|------|
| Debug logs | `console.log($$$)` | リリース前の残留ログ検出 |
| Empty catch | `catch ($ERR) { }` | エラー握りつぶし検出 |
| Unused async | `async function $NAME($$$) { $BODY }` | await なし async 検出 |
| Magic numbers | 数値リテラル検索 | ハードコード定数検出 |

**使用例**:
```
harness_ast_search pattern="console.log($$$)" language="typescript" path="src/"
harness_ast_search pattern="catch ($ERR) { }" language="typescript" path="src/"
```

**出力例**:
```markdown
🔍 AST-Grep Code Smell Scan

Patterns checked:
- console.log($$$) → Debug logs
- catch ($ERR) { } → Empty catch blocks

Results:
├── 3x console.log found (src/api/*.ts)
├── 1x empty catch block (src/utils/error.ts:45)
└── 0x unused async
```

> **注**: `harness_ast_search` が利用できない場合は、`sg` コマンド（Bash）または Grep にフォールバックします。

---

## 🔧 LSP 機能の活用

レビューでは LSP（Language Server Protocol）を活用して精度を向上します。

> **MCP 版優先**: `harness_lsp_*` MCP ツールが利用可能な場合は、標準 LSP ツールより優先して使用してください。

### LSP をレビューに統合

| レビュー観点 | LSP 活用方法 |
|-------------|-------------|
| **品質** | Diagnostics で型エラー・未使用変数を自動検出 |
| **セキュリティ** | Find-references で機密データの流れを追跡 |
| **パフォーマンス** | Go-to-definition で重い処理の実装を確認 |

### LSP Diagnostics の出力例

```
📊 LSP 診断結果

| ファイル | エラー | 警告 |
|---------|--------|------|
| src/components/Form.tsx | 0 | 2 |
| src/utils/api.ts | 1 | 0 |

⚠️ 1件のエラーを検出
→ レビューで指摘事項に追加
```

### Find-references による影響分析

```
🔍 変更影響分析

変更: validateInput()

参照箇所:
├── src/pages/signup.tsx:34
├── src/pages/settings.tsx:56
└── tests/validate.test.ts:12

→ テストでカバー済み ✅
```

詳細: [docs/LSP_INTEGRATION.md](../../docs/LSP_INTEGRATION.md)

---

## 🔧 PDF ページ範囲読み取り（Claude Code 2.1.49+）

ドキュメントレビュー時に大型 PDF を効率的に扱うための機能です。

### ページ範囲指定で読み取り

```javascript
// ページ範囲指定で読み取り
Read({ file_path: "docs/architecture.pdf", pages: "1-15" })

// 変更履歴セクションのみ
Read({ file_path: "docs/changelog.pdf", pages: "5-12" })

// セキュリティ要件のみ
Read({ file_path: "docs/requirements.pdf", pages: "45-60" })
```

### ドキュメントレビュー時の推奨アプローチ

| レビュー対象 | 推奨読み取り方法 | 理由 |
|------------|----------------|------|
| **大型仕様書** | 目次 + 変更箇所のみ | 関連セクションに集中 |
| **API設計書** | エンドポイント一覧 + セキュリティ章 | 重要な観点を優先 |
| **アーキテクチャ文書** | システム構成図 + 非機能要件 | レビュー対象を絞り込み |
| **ユーザーマニュアル** | 目次 + アクセシビリティ項 | 使いやすさを確認 |
| **リリースノート** | 最新バージョンの変更点のみ | 関連する変更を特定 |

### レビュー観点別の活用例

#### セキュリティレビュー

```markdown
大型セキュリティ仕様書（200ページ）のレビュー:

1. **目次で構造を把握**（1-3ページ）
   Read({ file_path: "security-spec.pdf", pages: "1-3" })

2. **認証・認可の章を精読**（25-45ページ）
   Read({ file_path: "security-spec.pdf", pages: "25-45" })

3. **脆弱性対策の章を精読**（78-92ページ）
   Read({ file_path: "security-spec.pdf", pages: "78-92" })

この方法で、セキュリティレビューに必要な部分だけを効率的に確認できます。
```

#### パフォーマンスレビュー

```markdown
パフォーマンス要件書（150ページ）のレビュー:

1. **目次とサマリー**（1-5ページ）
   Read({ file_path: "performance-spec.pdf", pages: "1-5" })

2. **レスポンスタイム要件**（34-50ページ）
   Read({ file_path: "performance-spec.pdf", pages: "34-50" })

3. **負荷テスト結果**（120-135ページ）
   Read({ file_path: "performance-spec.pdf", pages: "120-135" })
```

### レビューワークフロー統合

#### Step 0: 品質判定ゲート（ドキュメント分析）

ドキュメントレビュー時に、まずページ範囲指定で概要を把握:

```
1. 目次を読んで構造を理解
   Read({ file_path: "spec.pdf", pages: "1-3" })

2. 変更箇所を特定
   目次から変更セクションのページ番号を取得

3. 関連セクションのみ精読
   Read({ file_path: "spec.pdf", pages: "{変更範囲}" })
```

#### 4視点レビューでの活用

| 観点 | 読むべきページ範囲 | 例 |
|------|------------------|-----|
| **セキュリティ** | 認証・認可、暗号化、脆弱性対策 | pages: "25-45,78-92" |
| **パフォーマンス** | 非機能要件、負荷テスト結果 | pages: "34-50,120-135" |
| **品質** | コーディング規約、テスト戦略 | pages: "60-75" |
| **アクセシビリティ** | UI/UX要件、WCAG準拠 | pages: "95-110" |

### ベストプラクティス

| 原則 | 説明 |
|------|------|
| **目次優先** | 常に目次で構造を把握してから詳細へ |
| **観点別ページ範囲** | レビュー観点ごとに必要なページを特定 |
| **変更差分に集中** | 既存ドキュメントは変更箇所のみレビュー |
| **重要度順** | Critical → Major → Minor の順に読む |

### トークン消費の比較

| レビュー方法 | ドキュメント規模 | トークン消費 | レビュー精度 |
|------------|---------------|------------|-------------|
| **全ページ読み込み** | 200ページ | ~100,000 | 高 |
| **ページ範囲指定** | 必要な30ページ | ~15,000 | 高 |

→ **85%のトークン削減とレビュー時間短縮が可能**

### 注意事項

- ページ範囲は1-indexed（1ページ目は `pages: "1"`）
- 複数範囲は未サポート（将来の拡張で対応予定）
- 現時点では連続したページ範囲のみ指定可能

---

## VibeCoder 向け

```markdown
📝 コードチェックを依頼するときの言い方

1. **「チェックして」**
   - 全体的に問題がないか見てもらう

2. **「セキュリティ大丈夫？」**
   - 悪意ある攻撃に耐えられるかチェック

3. **「遅くない？」**
   - 速度に問題がないかチェック

4. **「誰でも使える？」**
   - 障害のある方でも使えるかチェック

💡 ヒント: 「全部チェックして」と言えば、
4つの観点すべてを自動で確認します
```
