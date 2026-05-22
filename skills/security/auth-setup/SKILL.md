---
name: auth-setup
description: Google OAuth クライアント設定の手順を案内する。「OAuth 設定」「Google 認証の準備」「クライアント ID 作成」「認証手順を教えて」「Google ログイン準備」「OAuth セットアップ」「認証設定したい」などで起動。
allowed-tools: [Read]
---

# Auth Setup

Google OAuth クライアント（デスクトップアプリ）の作成手順を案内します。

## 前提条件

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 手順

### 1. Google Cloud Console にアクセス

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 上部の「プロジェクトを選択」→「新しいプロジェクト」
3. プロジェクト名を入力（例: `claude-code-plugins`）して「作成」

### 2. API を有効化

**メニュー → API とサービス → ライブラリ** で以下を検索して有効化:

- Google Drive API
- Google Docs API
- Google Sheets API
- Google Slides API
- Google Forms API
- Apps Script API
- Google Calendar API
- Gmail API

### 3. OAuth 同意画面を設定

**メニュー → Google Auth Platform → ブランディング**

（「Google Auth Platform が設定されていません」と表示されたら「開始」をクリック）

1. **アプリ情報**
   - アプリ名: 任意（例: `Claude Code Plugins`）
   - ユーザーサポートメール: 自分のメールアドレス
   - 「次へ」

2. **対象**
   - 「外部」を選択
   - 「次へ」

3. **連絡先情報**
   - メールアドレス: 自分のメールアドレス
   - 「次へ」

4. **終了**
   - 「Google API サービス: ユーザーデータに関するポリシー」に同意
   - 「続行」

5. **テストユーザーを追加**（重要）
   - 左メニューの「対象」をクリック
   - 「+ Add users」をクリック
   - 使いたい Google アカウントのメールアドレスを追加（複数可）

### 4. OAuth クライアント ID を作成

**左メニュー → クライアント**

1. 「+ クライアントを作成」をクリック
2. アプリケーションの種類: **デスクトップアプリ**
3. 名前: 任意（例: `Claude Code`）
4. 「作成」
5. **作成直後に JSON をダウンロード**（後からダウンロードできない場合あり）

### 5. クライアント設定を配置

```bash
mkdir -p ~/.config/shiiman-google/clients
mv ~/Downloads/client_secret_*.json ~/.config/shiiman-google/clients/default.json
```

### 6. 認証を実行

「Google ログインして」または「認証して」と言って認証を実行してください。

## よくある質問

### Q: OAuth クライアントは自動作成できる？

いいえ。セキュリティ上の理由で Google Cloud Console での手動作成が必須です。

### Q: OAuth 以外の認証方法は？

個人の Google アカウントデータ（Gmail, Calendar 等）にアクセスするには OAuth が唯一の方法です。API キーやサービスアカウントでは個人データにアクセスできません。

### Q: ドメインごとに OAuth クライアントが必要？

いいえ。1 つの OAuth クライアントで複数の Google アカウント（異なるドメイン含む）に対応できます。`--profile` オプションでアカウントを切り替えられます。

## 注意事項

- クライアント設定ファイル（`default.json`）には秘密情報が含まれています
- Git にコミットしないでください
- 複数アカウントを使う場合は、プロファイル名を指定して認証できます
