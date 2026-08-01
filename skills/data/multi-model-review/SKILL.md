---
name: multi-model-review
description: マルチモデルコードレビュー。LLMがコードレビューを行った後、GitHub Copilot CLIに精査させて双方の視点を統合した最終レビューを提供。Use
  when user wants multi-model code review, second opinion, or wants to cross-check
  review findings with another AI. Trigger
---

---
name: multi-model-review
description: マルチモデルコードレビュー。LLMがコードレビューを行った後、GitHub Copilot CLIに精査させて双方の視点を統合した最終レビューを提供。Use when user wants multi-model code review, second opinion, or wants to cross-check review findings with another AI. Triggers: "/multi-model-review", "マルチモデルレビュー", "複数モデルでレビュー", "セカンドオピニオン"
---

# Multi-Model Code Review

LLM のコードレビュー結果を GitHub Copilot CLI に精査させ、双方の視点を統合した最終レビューを提供する。

## 出力ディレクトリ構成

レビュー結果は `.multi-model-review/` 配下にタイムスタンプ付きディレクトリを作成して保存する。
これにより、過去のレビュー結果と混在せず、履歴を追跡できる。

```text
.multi-model-review/
└── {YYYYMMDD-HHmmss}_{review-target}/
    ├── 01-my-review.md        # Step 1: 自分のレビュー結果
    ├── 02-copilot-prompt.txt  # Step 2: Copilot CLI に渡すプロンプト
    ├── 03-copilot-response.md # Step 2: Copilot CLI の回答
    └── 04-final-summary.md    # Step 5: 最終レビューサマリー
```

**ディレクトリ命名例:**

- `20260111-143052_feature-video-contents/`
- `20260111-150000_pr-123/`
- `20260111-160000_src-lib-auth/`

> **重要**: レビュー開始時に、まずタイムスタンプ付きディレクトリを作成すること。

## Flow

```text
Step 1: LLM（あなた）がコードレビュー → ファイル出力
    ↓
Step 2: Copilot CLIに精査＋独自レビューを依頼 → プロンプト＆回答をファイル出力
    ↓
Step 3: Copilotの回答を受けて再検討
    ↓
Step 4: 必要に応じて再度Copilot呼び出し
    ↓
Step 5: 双方納得の結論をユーザーに回答 → 最終サマリーをファイル出力
```

## Step 1: 自分でコードレビュー

対象コード（git diff、ファイル、PR など）をレビューし、以下の観点で問題点を洗い出す：

- バグ・ロジックエラー
- セキュリティ脆弱性
- パフォーマンス問題
- コード品質・保守性
- ベストプラクティス違反

**完了後**: `01-my-review.md` に以下の形式で保存：

```markdown
# Code Review: {レビュー対象}

**Reviewer:** {モデル名}
**Date:** {YYYY-MM-DD HH:mm}

## Review Target

{レビュー対象の説明}

## Critical Issues

1. **[Issue Title]** (file.ts#L10-L20)
   - Description
   - Impact
   - Suggested Fix

## Warnings

1. **[Warning Title]** (file.ts#L30)
   - Description
   - Recommendation

## Suggestions

1. **[Suggestion Title]**
   - Description
   - Benefit
```

## Step 2: Copilot CLI で精査＋独自レビュー

### 2.1 プロンプトファイルの作成

`02-copilot-prompt.txt` に以下のテンプレートでプロンプトを保存：

```text
I performed a code review and want you to both verify my findings AND conduct your own independent review.

## Review Target
{レビュー対象}

## Code Changes
{対象コードまたはgit diffの概要 - 詳細は --add-dir で渡されたファイルを参照}

## My Review Findings

### Critical Issues
{Critical Issues の要約}

### Warnings
{Warnings の要約}

### Suggestions
{Suggestions の要約}

---

Please:

**Part 1: Verify my review**
1. Read the actual source files to confirm my findings are accurate
2. Point out if any of my findings are incorrect or overstated

**Part 2: Your independent review**
3. Conduct your own code review within the specified Review Target scope
4. List any issues I missed

Respond with:
- **Confirmed:** Issues you agree with
- **Disputed:** Issues you disagree with (explain why)
- **Your Findings:** Issues from your independent review
- **Additional context:** Relevant information from reading the source
```

### 2.2 Copilot CLI の実行

以下のコマンドで Copilot CLI を呼び出し、結果をファイルに保存する：

> **重要**: Copilot CLI は統計情報を stderr に出力するため、`2>&1` でリダイレクトすると統計情報も含まれてしまう。stdout のみをキャプチャすること。

**macOS / Linux (Bash/Zsh):**

```bash
copilot -p "$(cat {review-dir}/02-copilot-prompt.txt)" --add-dir . --allow-all-tools --model gpt-5 -s > {review-dir}/03-copilot-response.md 2>/dev/null
```

**Windows (PowerShell):**

```powershell
copilot -p (Get-Content -Raw "{review-dir}\02-copilot-prompt.txt") --add-dir . --allow-all-tools --model gpt-5 -s 2>$null > "{review-dir}\03-copilot-response.md"
```

### 2.3 レスポンスの確認

上記コマンドで `03-copilot-response.md` に保存された内容を確認。必要に応じて以下のフォーマットで整形：

```markdown
# Copilot CLI Review Response

**Model:** gpt-5
**Date:** {YYYY-MM-DD HH:mm}

## Part 1: Verification of Original Review

### ✅ Confirmed Issues

{確認された問題}

### ❌ Disputed Issues

{反論された問題}

## Part 2: Independent Review

### Additional Issues Found

{追加で発見された問題}

### Additional Context

{追加のコンテキスト}
```

## Step 3-4: 再検討と追加確認

Copilot の精査結果を受けて：

- **Confirmed** → 最終レビューに含める
- **Disputed** → 反論を検討、必要なら再度 Copilot に確認
- **Your Findings** → 妥当なら追加

### 再確認が必要な場合のプロンプト

```text
Regarding the disputed issue about <問題点>:

You mentioned <Copilotの反論>. However, I believe <あなたの見解>.

Please re-examine <ファイル名> and clarify:
1. <確認したい点1>
2. <確認したい点2>
```

## Step 5: 最終レビュー出力

`04-final-summary.md` に以下の形式で保存：

```markdown
# Multi-Model Code Review Summary

**Review Target:** {レビュー対象}
**Date:** {YYYY-MM-DD HH:mm}
**Reviewers:** {モデル名} + GitHub Copilot (gpt-5)

---

## Critical Issues（マージ前に必須修正）

1. **[Issue Title]** (file.ts#L10-L20)
   - Description
   - Impact
   - Agreed by: Both reviewers

## Warnings（修正推奨）

1. **[Warning Title]** (file.ts#L30)
   - Description
   - Agreed by: {Reviewer}

## Suggestions（改善提案）

1. **[Suggestion Title]**
   - Description
   - Benefit

---

## Review Discussion

### 合意点

{双方が同意した主要な問題}

### 議論点

{見解が分かれた点とその結論}

### 補完

{片方のみが発見した問題}

---

## Action Items

| Priority      | Issue | File | Action Required |
| ------------- | ----- | ---- | --------------- |
| 🔴 Critical   | ...   | ...  | ...             |
| 🟡 Warning    | ...   | ...  | ...             |
| 🟢 Suggestion | ...   | ...  | ...             |
```

## 利用可能なモデル

| Model                  | Notes                  |
| ---------------------- | ---------------------- |
| `gpt-5`                | デフォルト、バランス型 |
| `gpt-5.1-codex-max`    | コード特化、高性能     |
| `gemini-3-pro-preview` | Google 製              |
| `claude-sonnet-4`      | Anthropic 製           |
| `claude-sonnet-4.5`    | Anthropic 製（最新）   |
| `claude-haiku-4.5`     | Anthropic 製（軽量）   |

> **注意**: 利用可能なモデルは `copilot --help` で確認できます。`gpt-5.1-codex-max` などは利用できない場合があります。

## 注意事項

- `copilot` CLI がインストールされている必要がある
- `--add-dir .` でプロジェクトへのアクセスを許可
- 複数回のやり取りが必要な場合、それぞれ別の copilot コマンドとして実行
- 大規模なコード変更の場合、レビュー対象を分割して精査することを推奨

## 引数長制限とシェルエスケープへの対応

シェルの引数長制限（macOS: 約 262KB、Linux: 約 2MB）を超えると `Argument list too long` エラーが発生する。
また、長いプロンプトをシェルで直接渡すとエスケープ問題でコマンドが正しく実行されないことがある。

### 対策

1. **コード変更の詳細は省略** - `--add-dir .` により Copilot が直接ファイルを読めるため、diff 全文をプロンプトに含める必要はない
2. **レビュー結果を要約** - 各問題を 1-2 行で簡潔に記述し、詳細は Copilot に確認させる
3. **対象を分割** - 大規模な変更は複数回に分けてレビュー（例: ディレクトリ単位、機能単位）
4. **ファイル経由でプロンプトを渡す** - 長いプロンプトはファイルに保存してコマンド置換で渡す（推奨）

### ファイル経由でプロンプトを渡す方法（推奨）

長いプロンプトやマークダウン形式のプロンプトは、ファイルに保存してからコマンド置換で渡すことで、シェルのエスケープ問題を回避できる。

#### macOS / Linux (Bash/Zsh)

```bash
# 1. プロンプトをファイルに保存（エージェントの場合は create_file ツールを使用）
#    推奨: プロジェクト内 .multi-model-review/ ディレクトリに保存
# 2. コマンド置換でプロンプトを渡す
copilot -p "$(cat .multi-model-review/review-prompt.txt)" --add-dir . --allow-all-tools --model <model> -s
```

#### Windows (PowerShell)

```powershell
# 1. プロンプトをファイルに保存（エージェントの場合は create_file ツールを使用）
#    推奨: プロジェクト内 .multi-model-review/ ディレクトリに保存
# 2. Get-Content でファイルを読み込んで渡す
copilot -p (Get-Content -Raw ".multi-model-review\review-prompt.txt") --add-dir . --allow-all-tools --model <model> -Encoding UTF8 -s
```

#### Windows (cmd.exe)

cmd.exe では直接のコマンド置換が難しいため、PowerShell 経由で実行するか、短いプロンプトを直接渡すことを推奨。

```cmd
:: PowerShell経由で実行（プロジェクト内の .multi-model-review/ ディレクトリを使用）
powershell -Command "copilot -p (Get-Content -Raw '.multi-model-review\review-prompt.txt') --add-dir . --allow-all-tools --model <model> -Encoding UTF8 -s"
```

## Copilot CLI 呼び出しのベストプラクティス（エージェント向け）

Copilot CLI は応答に時間がかかるため、エージェントから呼び出す際は適切な待機処理が必要。

> ⚠️ **重要**: `isBackground: true` とリダイレクト `>` を組み合わせると、**出力ファイルが空（0 バイト）になる問題**が発生する。これは PowerShell がリダイレクト演算子でファイルをコマンド開始前に作成してしまうため。

### GitHub Copilot エージェント向け

> `run_in_terminal` / `get_terminal_output` を使用する場合

#### 推奨方法: フォアグラウンド実行

`isBackground: false`（デフォルト）で実行し、コマンド完了を待つ。Copilot CLI は通常 30 秒〜2 分で完了する。

1. **レビューディレクトリを作成** - タイムスタンプ付きディレクトリを作成

   ```text
   .multi-model-review/{YYYYMMDD-HHmmss}_{review-target}/
   ```

2. **自分のレビュー結果を保存** - `01-my-review.md` に保存
3. **プロンプトをファイルに保存** - `02-copilot-prompt.txt` に保存
4. `run_in_terminal` で `isBackground: false` を指定してフォアグラウンド実行

   **macOS / Linux (Bash/Zsh):**

   ```bash
   copilot -p "$(cat .multi-model-review/{dir}/02-copilot-prompt.txt)" --add-dir . --allow-all-tools --model gpt-5 -s 2>/dev/null > .multi-model-review/{dir}/03-copilot-response.md
   ```

   **Windows (PowerShell):**

   ```powershell
   copilot -p (Get-Content -Raw ".multi-model-review\{dir}\02-copilot-prompt.txt") --add-dir . --allow-all-tools --model gpt-5 -Encoding UTF8 -s 2>$null > ".multi-model-review\{dir}\03-copilot-response.md"
   ```

5. コマンド完了後、出力ファイルを確認
6. **Copilot の回答を読み取る** - `read_file` で `03-copilot-response.md` の内容を取得
7. **最終サマリーを保存** - `04-final-summary.md` に保存

#### 代替方法: バックグラウンド実行（リダイレクトなし）

リダイレクトを使わず、`get_terminal_output` で直接出力を取得する方法：

1. `run_in_terminal` で `isBackground: true` を指定（**リダイレクトなし**）

   ```powershell
   copilot -p (Get-Content -Raw ".multi-model-review\{dir}\02-copilot-prompt.txt") --add-dir . --allow-all-tools --model gpt-5 -Encoding UTF8 -s 2>$null
   ```

2. `get_terminal_output` でターミナル ID を使って出力を取得
3. 10 秒間隔でポーリング（通常 3-12 回程度で完了）
4. 出力が得られたら、`create_file` で `03-copilot-response.md` に保存

> **注意**: シェルで直接長いプロンプトを渡すと、エスケープ問題やツールによるコマンド簡略化で正しく実行されないことがある。ファイル経由が最も確実。

### Claude Code 向け

> `Bash` / `TaskOutput` を使用する場合

1. **レビューディレクトリを作成** - タイムスタンプ付きディレクトリを作成
2. **自分のレビュー結果を保存** - `01-my-review.md` に保存
3. **プロンプトをファイルに保存** - `02-copilot-prompt.txt` に保存
4. `Bash` ツールで `run_in_background: true` を指定してバックグラウンド実行
5. `TaskOutput` ツールで結果を取得（`block: true` で完了待ち可能）
6. タイムアウトは `timeout` パラメータで指定可能（最大 600000ms）
7. **Copilot の回答を保存** - `03-copilot-response.md` に保存
8. **最終サマリーを保存** - `04-final-summary.md` に保存

## .gitignore への追加

レビュー結果をリポジトリにコミットしない場合は、`.gitignore` に追加：

```gitignore
# Multi-model review outputs
.multi-model-review/
```

レビュー履歴を残したい場合は、この行を追加しないでください。
