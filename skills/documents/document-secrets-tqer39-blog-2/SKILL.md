---
name: document-secrets
description: シークレット追加時のドキュメント更新。「シークレットを追加」「環境変数を追加」「API キーを設定」などのリクエスト時に使用。
---

# Document Secrets

GitHub Secrets が追加された際に、関連ドキュメントを更新するスキル。

## 役割

新しいシークレットが追加されたら、以下のドキュメントを更新する:

- `/CLAUDE.md` (英語)
- `/docs/CLAUDE.ja.md` (日本語)

## 対象セクション

両ファイルの「GitHub Secrets Required」セクション内のテーブルを更新する。

## 既存カテゴリ

| カテゴリ | 用途 |
| -------- | ---- |
| Infrastructure Secrets | Vercel, CloudFlare 等のインフラ |
| Authentication Secrets | OAuth, Auth ライブラリ関連 |
| Third-party Service Secrets | Discord, OpenAI 等 |
| GitHub App Secrets | GitHub App ID, Private Key |

## テーブル形式

```markdown
| Secret | Description |
| ------ | ----------- |
| SECRET_NAME | What the secret is used for |
```

## 手順

1. **シークレット情報の確認**
   - シークレット名（例: `OPENAI_API_KEY`）
   - 用途・説明（英語と日本語）
   - 適切なカテゴリ

2. **CLAUDE.md の更新**
   - 該当カテゴリのテーブルにシークレットを追加
   - 説明は英語で記載
   - アルファベット順でソート

3. **docs/CLAUDE.ja.md の更新**
   - 該当カテゴリのテーブルにシークレットを追加
   - 説明は日本語で記載
   - アルファベット順でソート

4. **新規カテゴリが必要な場合**
   - 両ファイルに同じ構造でカテゴリを追加
   - 既存カテゴリの後に配置

## 例

### 追加前

```markdown
### Third-party Service Secrets

| Secret | Description |
| ------ | ----------- |
| OPENAI_API_KEY | OpenAI API key for PR desc |
| DISCORD_WEBHOOK_DEV | Discord webhook (dev) |
| DISCORD_WEBHOOK_PROD | Discord webhook (prod) |
```

### 追加後（GEMINI_API_KEY を追加）

```markdown
### Third-party Service Secrets

| Secret | Description |
| ------ | ----------- |
| GEMINI_API_KEY | Google Gemini API key for image generation |
| OPENAI_API_KEY | OpenAI API key for PR desc |
| DISCORD_WEBHOOK_DEV | Discord webhook (dev) |
| DISCORD_WEBHOOK_PROD | Discord webhook (prod) |
```

## 注意事項

- シークレットの実際の値は記載しない
- 説明は簡潔に（1行以内）
- 環境別サフィックス（`_DEV`, `_PROD`）がある場合はそのまま記載
- wrangler.toml や GitHub Actions で使用されるシークレットも対象
