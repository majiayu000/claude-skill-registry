---
name: vercel-deploy
description: Vercelへのデプロイ操作を実行する。プレビュー/本番デプロイ、環境変数管理、デプロイ状態確認、ロールバック、ドメイン設定など。「Vercelにデプロイ」「プレビュー環境を作成」「本番反映」「デプロイログ確認」「環境変数を設定」などの依頼時に使用。
---

# Vercel Deploy Skill

Vercel CLIを使用したデプロイ操作を支援する。

## 前提条件

- Vercel CLIがインストール済み（`pnpm add -g vercel`）
- `vercel login` で認証済み
- プロジェクトがVercelにリンク済み（`.vercel/project.json` が存在）

## デプロイワークフロー

### 1. プレビューデプロイ（推奨フロー）

```bash
# ビルド検証
pnpm build

# プレビューデプロイ（PRごとの確認用）
vercel

# 出力されるURLを確認
```

### 2. 本番デプロイ

```bash
# 本番環境へデプロイ
vercel --prod

# または、プレビューを本番に昇格
vercel promote <deployment-url>
```

### 3. デプロイ前チェックリスト

1. `pnpm lint` - Lintエラーがないこと
2. `pnpm test` - テストが通ること
3. `pnpm build` - ビルドが成功すること
4. 環境変数が設定済みであること

## 環境変数管理

### 環境変数の確認

```bash
# 全環境変数をリスト
vercel env ls

# 特定環境の変数を確認
vercel env ls production
vercel env ls preview
vercel env ls development
```

### 環境変数の追加

```bash
# インタラクティブに追加
vercel env add <NAME>

# 値を直接指定（preview/production両方）
echo "value" | vercel env add <NAME> production
echo "value" | vercel env add <NAME> preview

# ファイルから追加
vercel env add <NAME> < secret.txt
```

### 環境変数の削除

```bash
vercel env rm <NAME> production
```

### このプロジェクトの必須環境変数

| 変数名 | 用途 | 環境 |
|--------|------|------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase URL | all |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase匿名キー | all |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase管理キー | production, preview |
| `GEMINI_API_KEY` | Gemini API | production, preview |
| `RESEND_API_KEY` | メール送信 | production, preview |
| `CRON_SECRET` | Cron認証 | production, preview |

## デプロイ状態の確認

```bash
# 最新デプロイ一覧
vercel ls

# デプロイ詳細
vercel inspect <deployment-url>

# ビルドログ確認
vercel logs <deployment-url>

# リアルタイムログ
vercel logs <deployment-url> --follow
```

## ロールバック

```bash
# 前のデプロイに戻す
vercel rollback

# 特定デプロイに戻す
vercel rollback <deployment-url>
```

## ドメイン管理

```bash
# ドメイン一覧
vercel domains ls

# ドメイン追加
vercel domains add <domain>

# ドメイン削除
vercel domains rm <domain>
```

## Cronジョブ（本プロジェクト固有）

`vercel.json` で定義済み:

| パス | スケジュール | 用途 |
|------|-------------|------|
| `/api/cron/collect` | 毎日 06:00 JST | 記事収集 |
| `/api/cron/digest` | 毎日 06:30 JST | ダイジェスト生成 |
| `/api/cron/notify` | 15分ごと | 通知送信 |

Cron実行ログ確認:
```bash
vercel logs <deployment-url> --filter /api/cron
```

## トラブルシューティング

### ビルドエラー

```bash
# ローカルでビルド確認
pnpm build

# Vercel環境でのビルドログ
vercel logs <deployment-url> --type=build
```

### 環境変数が反映されない

```bash
# 再デプロイで環境変数を反映
vercel --force

# 環境変数の確認
vercel env ls production
```

### Function timeout

`vercel.json` で調整:
```json
{
  "functions": {
    "src/app/api/**/*.ts": {
      "maxDuration": 60
    }
  }
}
```

## クイックコマンド一覧

| 目的 | コマンド |
|------|---------|
| プレビューデプロイ | `vercel` |
| 本番デプロイ | `vercel --prod` |
| デプロイ一覧 | `vercel ls` |
| ログ確認 | `vercel logs <url>` |
| 環境変数一覧 | `vercel env ls` |
| ロールバック | `vercel rollback` |
