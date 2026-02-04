---
name: gcp-auth
description: Google Cloud Platform (GCP) の Application Default Credentials 認証を実行。BigQuery や Cloud Storage 等の GCP サービス利用前に「GCP認証して」と言うだけで認証手順をガイド。
---

# GCP Authentication

Google Cloud の Application Default Credentials (ADC) 認証を実行するスキルです。

## Workflow

1. ユーザーが「GCP認証して」「BigQuery使いたい」等と言う
2. 認証コマンドをターミナルで実行するよう案内
3. ブラウザでGoogleアカウント認証
4. 認証完了を確認

## Usage

### 認証コマンド（ターミナルで直接実行）

```bash
gcloud auth application-default login
```

**注意**: このコマンドはブラウザでの認証が必要なため、ターミナルで直接実行してください。

## 認証フロー

1. **コマンド実行** → ブラウザが自動的に開く
2. **Googleアカウント選択** → 使用するアカウントを選択
3. **権限許可** → 「Google Auth Library にアクセスを許可」で「許可」をクリック
4. **完了確認** → ターミナルに「Credentials saved to file」と表示

## トラブルシューティング

| エラー | 対処法 |
|--------|--------|
| Reauthentication is needed | 認証期限切れ。再度 `gcloud auth application-default login` を実行 |
| GOOGLE_APPLICATION_CREDENTIALS 警告 | `.env` から該当行を削除するか、ADC を使用 |
| Project not set | `gcloud config set project PROJECT_ID` でプロジェクト設定 |

## 認証状態の確認

```bash
# トークンが表示されれば認証済み
gcloud auth application-default print-access-token

# 現在のプロジェクト確認
gcloud config get-value project
```

## Requirements

- Google Cloud SDK (`gcloud`) がインストール済み
- ブラウザでGoogleアカウントにログイン可能


