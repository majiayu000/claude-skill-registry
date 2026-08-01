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

## Flow

```text
Step 1: LLM（あなた）がコードレビュー
    ↓
Step 2: Copilot CLIに精査＋独自レビューを依頼
    ↓
Step 3: Copilotの回答を受けて再検討
    ↓
Step 4: 必要に応じて再度Copilot呼び出し
    ↓
Step 5: 双方納得の結論をユーザーに回答
```

## Step 1: 自分でコードレビュー

対象コード（git diff、ファイル、PR など）をレビューし、以下の観点で問題点を洗い出す：

- バグ・ロジックエラー
- セキュリティ脆弱性
- パフォーマンス問題
- コード品質・保守性
- ベストプラクティス違反

レビュー結果を「Critical Issues / Warnings / Suggestions」形式でまとめる。

## Step 2: Copilot CLI で精査＋独自レビュー

以下のコマンドで Copilot CLI を呼び出す：

```bash
copilot -p "<プロンプト>" --add-dir . --allow-all-tools --model <model> -s
```

### プロンプトテンプレート

```text
I performed a code review and want you to both verify my findings AND conduct your own independent review.

## Review Target
<レビュー対象を以下のいずれかで指定>
- 特定のコミット: commit <hash>
- PR: PR #<number>
- 特定ファイル: <file paths>
- ディレクトリ全体の変更: all recent changes in the provided directory

## Code Changes
<対象コードまたはgit diffの概要>

## My Review Findings

### Critical Issues
<Critical Issues>

### Warnings
<Warnings>

### Suggestions
<Suggestions>

---

Please:

**Part 1: Verify my review**
1. Reading the actual source files to confirm my findings are accurate
2. Pointing out if any of my findings are incorrect or overstated

**Part 2: Your independent review**
3. Conduct your own code review within the specified Review Target scope, looking for:
   - Bugs or logic errors
   - Security vulnerabilities
   - Performance issues
   - Code quality and maintainability concerns
   - Best practice violations
4. List any issues I missed

Respond with:
- Confirmed: Issues you agree with
- Disputed: Issues you disagree with (explain why)
- Your Findings: Issues from your independent review (including ones I missed)
- Additional context: Relevant information from reading the source
```

### 利用可能なモデル

| Model                  | Notes                  |
| ---------------------- | ---------------------- |
| `gpt-5`                | デフォルト、バランス型 |
| `gpt-5.1`, `gpt-5.2`   | 新バージョン           |
| `gpt-5.1-codex-max`    | コード特化、高性能     |
| `gemini-3-pro-preview` | Google 製              |

## Step 3: Copilot の回答を受けて再検討

Copilot の精査結果を受けて：

1. **Confirmed** - 双方合意、最終レビューに含める
2. **Disputed** - Copilot の反論を検討し、必要なら修正
3. **Your Findings** - Copilot が独自レビューで発見した問題を確認し、妥当なら追加
4. **追加コンテキスト** - ソースを読んだ Copilot の情報を考慮

## Step 4: 必要に応じて再度 Copilot 呼び出し

Disputed な項目や追加確認が必要な場合：

```text
Regarding the disputed issue about <問題点>:

You mentioned <Copilotの反論>. However, I believe <あなたの見解>.

Please re-examine <ファイル名> and clarify:
1. <確認したい点1>
2. <確認したい点2>
```

## Step 5: 最終レビューをユーザーに回答

双方の視点を統合した最終レビューを提供：

```markdown
## Multi-Model Code Review Summary

**Reviewers:** [あなたのモデル名] + GitHub Copilot [モデル名]

### Critical Issues

- [双方合意の問題]
- [Copilot が追加で発見した問題]

### Warnings

- [警告事項]

### Suggestions

- [改善提案]

### Review Discussion

- **合意点:** 双方が同意した主要な問題
- **議論点:** 見解が分かれた点とその結論
- **補完:** 片方のみが発見した問題
```

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
copilot -p (Get-Content -Raw ".multi-model-review\review-prompt.txt") --add-dir . --allow-all-tools --model <model> -s
```

#### Windows (cmd.exe)

cmd.exe では直接のコマンド置換が難しいため、PowerShell 経由で実行するか、短いプロンプトを直接渡すことを推奨。

```cmd
:: PowerShell経由で実行（プロジェクト内の .multi-model-review/ ディレクトリを使用）
powershell -Command "copilot -p (Get-Content -Raw '.multi-model-review\review-prompt.txt') --add-dir . --allow-all-tools --model <model> -s"
```

## Copilot CLI 呼び出しのベストプラクティス（エージェント向け）

Copilot CLI は応答に時間がかかるため、エージェントから呼び出す際はバックグラウンド実行が必要。

### GitHub Copilot エージェント向け

> `run_in_terminal` / `get_terminal_output` を使用する場合

1. **プロンプトをファイルに保存** - `create_file` ツールでプロンプトを保存
   - **推奨**: プロジェクト内の `.multi-model-review/review-prompt.txt`
2. `run_in_terminal` で `isBackground: true` を指定してバックグラウンド実行

   **macOS / Linux (Bash/Zsh):**

   ```bash
   copilot -p "$(cat .multi-model-review/review-prompt.txt)" --add-dir . --allow-all-tools --model <model> -s
   ```

   **Windows (PowerShell):**

   ```powershell
   copilot -p (Get-Content -Raw ".multi-model-review\review-prompt.txt") --add-dir . --allow-all-tools --model <model> -s
   ```

3. `get_terminal_output` でターミナル ID を使って結果を確認
4. 3-5 秒間隔でポーリング（通常 10-15 回程度で結果取得）
5. 20 回以上応答がない場合はタイムアウトと判断

> **注意**: シェルで直接長いプロンプトを渡すと、エスケープ問題やツールによるコマンド簡略化で正しく実行されないことがある。ファイル経由が最も確実。

### Claude Code 向け

> `Bash` / `TaskOutput` を使用する場合

1. `Bash` ツールで `run_in_background: true` を指定してバックグラウンド実行
2. `TaskOutput` ツールで結果を取得（`block: true` で完了待ち可能）
3. タイムアウトは `timeout` パラメータで指定可能（最大 600000ms）
