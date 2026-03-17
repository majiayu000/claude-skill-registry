---
name: roundcube-webmail
description: Reads and summarizes emails from Roundcube webmail with SAML/TOTP authentication using Playwright. Use when checking webmail, reading university email, automating Roundcube login, or setting up daily email digest via Slack/OpenClaw cron. macOS only.
---

# Roundcube Webmail Skill

> **macOS 専用**

SAML+TOTP 認証を自動突破して Roundcube の受信箱を読み、Slack に通知する。

## 認証情報の保存場所

| 変数 | 保存場所 |
|------|---------|
| `WEBMAIL_USERNAME` | `.env` |
| `WEBMAIL_URL` | `.env` |
| `WEBMAIL_PASSWORD` | macOS Keychain（必須） |
| `WEBMAIL_TOTP_SECRET` | macOS Keychain（必須） |

## セットアップ（初回のみ）

```bash
# 1. zbar インストール
brew install zbar

# 2. Google Authenticator から QR をエクスポート → スクリーンショット → AirDrop で Mac に送る
zbarimg --raw ~/Downloads/screenshot.PNG

# 3. TOTP シークレット抽出
python3 scripts/decode_totp_qr.py

# 4. Keychain に保存
bash scripts/setup-keychain.sh

# 5. .env に設定（機密情報は書かない）
WEBMAIL_USERNAME=your-username
WEBMAIL_URL=https://mailbox.naist.jp/roundcube/
```

## 使い方

```bash
# 受信箱を読む
node scripts/read-mail.js

# Slack に投稿する場合は .env に SLACK_WEBHOOK_URL を設定
```

## OpenClaw Cron 設定

```json
{
  "id": "naist-mail-reader",
  "schedule": "0 9 * * *",
  "kind": "agentTurn",
  "message": "exec コマンドで node scripts/read-mail.js を実行して、最新10件のメールを Slack C091G3PKHL2 に投稿してください。",
  "delivery": { "mode": "none" }
}
```

## 認証フロー

```
Navigate → NAIST IdP (SAML) → TOTP 入力 → Roundcube ログインフォーム → パスワード入力 → INBOX
```
