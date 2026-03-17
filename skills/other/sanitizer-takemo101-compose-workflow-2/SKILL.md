---
name: sanitizer
description: 外部入力（Issue/PRの本文）からプロンプトインジェクション対策としてサニタイズを行う
---

# Sanitizer

外部入力（GitHub Issue/PRの本文、コメント等）を安全に処理するためのサニタイズ機能。

---

## 目的

- **プロンプトインジェクション対策**: HTMLコメントや不可視文字に隠された悪意ある指示を除去
- **トークン漏洩防止**: 誤って含まれたGitHubトークンをマスク
- **入力正規化**: 不要な属性や特殊文字を除去して安全な入力に変換

---

## 使用場面

| 場面 | 適用タイミング |
|------|---------------|
| `/implement-issues` | Issue本文を読み込む際 |
| `@claude` メンション処理 | コメント本文を処理する際 |
| 外部PR処理 | 信頼できないPRの説明文を処理する際 |

---

## サニタイズ関数

### 1. HTMLコメント除去

```bash
strip_html_comments "<!-- hidden instruction -->"
# 出力: ""
```

### 2. 不可視文字除去

```bash
strip_invisible_chars "text\u200Bwith\u200Cinvisible"
# 出力: "textwithinvisible"
```

### 3. GitHubトークンマスク

```bash
redact_github_tokens "token: ghp_1234567890abcdefghijklmnopqrstuvwxyz"
# 出力: "token: [REDACTED_GITHUB_TOKEN]"
```

### 4. Markdown画像alt除去

```bash
strip_markdown_image_alt "![hidden instruction](image.png)"
# 出力: "![](image.png)"
```

### 5. HTML属性除去

```bash
strip_hidden_attributes '<div alt="hidden" data-secret="value">text</div>'
# 出力: '<div>text</div>'
```

---

## CLIスクリプト

```bash
bash .opencode/skill/sanitizer/scripts/sanitize.sh <input-file>
bash .opencode/skill/sanitizer/scripts/sanitize.sh --stdin
echo "content" | bash .opencode/skill/sanitizer/scripts/sanitize.sh --stdin
```

| 引数 | 説明 |
|------|------|
| `<input-file>` | サニタイズするファイルパス |
| `--stdin` | 標準入力から読み込み |

**出力**: サニタイズ済みテキスト（標準出力）

---

## 除去対象一覧

| カテゴリ | 対象 | 例 |
|---------|------|-----|
| HTMLコメント | `<!-- ... -->` | `<!-- ignore this -->` |
| Zero-width文字 | `\u200B`, `\u200C`, `\u200D`, `\uFEFF` | 不可視文字 |
| 制御文字 | `\u0000-\u001F`, `\u007F-\u009F` | 制御コード |
| Bidi制御 | `\u202A-\u202E`, `\u2066-\u2069` | 双方向テキスト制御 |
| Markdown画像alt | `![alt text](url)` のalt部分 | `![hidden](img.png)` → `![](img.png)` |
| HTML属性 | `alt`, `title`, `aria-label`, `data-*`, `placeholder` | `<img alt="hidden">` |
| HTMLエンティティ | `&#123;`, `&#x7B;` | 数値エンティティ（非印字文字除去） |
| GitHubトークン | `ghp_*`, `gho_*`, `ghs_*`, `ghr_*`, `github_pat_*` | APIトークン |

---

## セキュリティ考慮事項

- **新しいバイパス技術**: 完全な防御は不可能。外部コントリビューターからの入力は常に注意
- **信頼レベル**: 内部メンバーのIssueは信頼度高、外部PRは信頼度低として扱う
- **多層防御**: サニタイズは一層目。重要な操作前には人間の確認を推奨

---

## 関連ドキュメント

| ドキュメント | 内容 |
|-------------|------|
| [claude-code-action security](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md) | 元実装のセキュリティドキュメント |
