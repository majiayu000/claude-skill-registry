---
name: codex-review
description: "Codexにセカンドオピニオンを求める。AI同士の忖度なしガチレビュー。Use when user mentions 'Codex レビュー', 'セカンドオピニオン', 'Codex の意見', 'Codex でレビュー', or 'Codex セットアップ'. Do NOT load for: 'Codex に実装させて', 'Codex Worker', 'Codex に作らせて', '実装を依頼'."
description-en: "Ask Codex for second opinion. No-compromise AI peer review. Use when user mentions 'Codex レビュー', 'セカンドオピニオン', 'Codex の意見', 'Codex でレビュー', or 'Codex セットアップ'. Do NOT load for: 'Codex に実装させて', 'Codex Worker', 'Codex に作らせて', '実装を依頼'."
description-ja: "Codexにセカンドオピニオンを求める。AI同士の忖度なしガチレビュー。Use when user mentions 'Codex レビュー', 'セカンドオピニオン', 'Codex の意見', 'Codex でレビュー', or 'Codex セットアップ'. Do NOT load for: 'Codex に実装させて', 'Codex Worker', 'Codex に作らせて', '実装を依頼'."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
argument-hint: "[code|plan|scope]"
hooks:
  - event: PreToolCall
    type: command
    command: "${CLAUDE_PLUGIN_ROOT}/scripts/check-codex.sh"
    once: true
---

# Codex Review Integration Skill

OpenAI Codex CLI を使って Claude Code のコードレビュー時にセカンドオピニオンを提供するスキル。

## Do NOT Load For (誤発動防止)

以下のキーワードは `/work --codex` が担当します:

| トリガーワード | 正しいスキル | 理由 |
|---------------|-------------|------|
| "**Codex に実装させて**" | `/work --codex` | 実装 ≠ レビュー |
| "**Codex Worker**" | `/work --codex` | Worker = 実装役 |
| "**Codex に作らせて**" | `/work --codex` | 作成 = 実装 |
| "**実装を依頼**" | `/work --codex` | 実装目的 |

## 🎯 使用場面

### セットアップ
- **初回設定**: Codex CLI のインストール確認と `codex exec` 動作確認
- **認証設定**: Codex への OAuth / API キー認証

### レビュー
- **セカンドオピニオン**: Claude のレビュー結果に Codex の視点を追加
- **コード品質チェック**: 複数 AI モデルの得意分野を活用
- **設計レビュー**: アーキテクチャや実装パターンの多角的検証

## 機能詳細

| 機能 | 詳細 |
|------|------|
| **CLI セットアップ** | See [references/codex-mcp-setup.md](references/codex-mcp-setup.md) |
| **レビュー統合** | See [references/codex-review-integration.md](references/codex-review-integration.md) |
| **4並列レビュー** | See [references/codex-parallel-review.md](references/codex-parallel-review.md) |
| **モード切替** | See [references/codex-mode.md](references/codex-mode.md) |

## 実行手順

1. ユーザーのリクエストを分類
2. 上記の「機能詳細」から適切な参照ファイルを読む
3. その内容に従って設定またはレビューを実行

### ⚠️ 並列レビュー時の必須ルール

**Codex モード（`review.mode: codex`）でのレビュー実行時**:

1. **呼び出すエキスパートを判定**（全部ではなく必要なもののみ）:
   - 設定で `enabled: false` → 除外
   - CLI/バックエンド → Accessibility, SEO 除外
   - ドキュメントのみ変更 → Quality, Architect, Plan Reviewer, Scope Analyst を優先（Security, Performance は除外可）
2. 有効なエキスパートの `references/experts/*.md` から **プロンプトを個別に読み込む**
3. 有効なエキスパートのみ **Bash バックグラウンドプロセスで並列実行**
4. 絶対に1回の呼び出しで複数観点をまとめない

```
✅ 正しい（並列 CLI 実行）:
   # macOS: brew install coreutils
   TIMEOUT=$(command -v timeout || command -v gtimeout || echo "")
   $TIMEOUT 120 codex exec "$(cat /tmp/expert-security-prompt.md)" > /tmp/expert-security.txt 2>/dev/null &
   $TIMEOUT 120 codex exec "$(cat /tmp/expert-perf-prompt.md)" > /tmp/expert-perf.txt 2>/dev/null &
   $TIMEOUT 120 codex exec "$(cat /tmp/expert-quality-prompt.md)" > /tmp/expert-quality.txt 2>/dev/null &
   $TIMEOUT 120 codex exec "$(cat /tmp/expert-a11y-prompt.md)" > /tmp/expert-a11y.txt 2>/dev/null &
   wait

❌ 間違い:
   codex exec "セキュリティとパフォーマンスと品質をレビューして"
```

**詳細**: [references/codex-parallel-review.md](references/codex-parallel-review.md)

---

## 📋 Codex CLI 実行方法

Codex CLI がインストールされていれば、以下のように呼び出します：

| 方法 | コマンド |
|------|---------|
| 単発レビュー | `$TIMEOUT 120 codex exec "$(cat prompt.md)" 2>/dev/null` |
| 並列レビュー | 各エキスパートを `&` で並列実行し `wait` で待機 |

---

## 🔧 クイックスタート

### 前提条件

1. **Codex CLI がインストール済み**
   ```bash
   which codex  # パスが表示されること
   ```

2. **タイムアウトコマンド**（macOS の場合）
   ```bash
   brew install coreutils  # gtimeout を提供
   ```

3. **Codex にログイン済み**
   ```bash
   codex login status  # 認証済みであること
   ```

### 動作確認

```bash
# Codex CLI の応答テスト
codex exec "echo hello"
```

---

## 🔄 レビューワークフロー

### Solo モード

```
/harness-review 実行
    │
    ├── Claude レビュー（従来通り）
    │
    └── Codex CLI 呼び出し（有効時）
            │
            └── 結果統合
```

### 2-Agent モード

```
PM（Cursor / Codex）
    │
    └── タスク依頼
            │
            ├── Claude Code 実装
            │
            └── /harness-review
                    │
                    ├── Claude レビュー
                    └── Codex セカンドオピニオン
```

---

## ⚙️ 設定

`.claude-code-harness.config.yaml` で Codex 統合を設定：

```yaml
review:
  codex:
    enabled: true           # Codex セカンドオピニオン有効化
    auto: false             # true: 自動実行 / false: 毎回確認
    prompt: "Review the code and output issues and improvement suggestions"
```

| 設定項目 | デフォルト | 説明 |
|---------|-----------|------|
| `enabled` | `false` | Codex 統合の有効/無効 |
| `auto` | `false` | 自動レビュー実行 |
| `prompt` | (上記) | Codex へのレビュープロンプト |
| `execution_mode` | `exec` | 実行モード（`exec`: CLI直接、推奨）|

> **Note**: 全ての Codex 呼び出しは `exec` (CLI) を使用。並列エキスパートは Bash バックグラウンドプロセス (`&` + `wait`) で並列実行

---

## 💡 活用例

### 例1: セットアップ

```
ユーザー: 「Codex でもレビューできるようにして」

Claude Code:
→ codex-mcp-setup.md を読み込み
→ Codex インストール確認
→ `codex exec` 動作確認
→ 設定ファイル更新
```

### 例2: レビュー時

```
ユーザー: 「セカンドオピニオンもらって」

Claude Code:
→ codex.enabled = true を確認
→ CLI 経由で Codex にレビュー依頼
→ 結果を統合して表示
```

---

## ⚠️ 注意事項

### パフォーマンス

- Codex CLI 呼び出しには数秒〜数十秒かかる場合があります
- 大規模ファイルの場合はチャンク分割が推奨

### コスト

- Codex API 利用には OpenAI のクレジットが必要です
- レビュー頻度に応じたコスト見積もりを推奨

### トラブルシューティング

**問題**: Codex CLI が応答しない
**解決策**:
1. `which codex` でインストール確認
2. `codex login status` で認証確認
3. `$TIMEOUT 10 codex exec "echo test"` でタイムアウトテスト

**問題**: レビュー結果が返らない
**解決策**:
1. ネットワーク接続を確認
2. API クレジット残高を確認
3. タイムアウト値を延長して再試行

---

## 📚 参考資料

- [Codex CLI Reference](https://developers.openai.com/codex/cli/reference/)
- [Codex CLI Installation](https://developers.openai.com/codex/cli/installation/)
- [Codex CLI Authentication](https://developers.openai.com/codex/cli/authentication/)
