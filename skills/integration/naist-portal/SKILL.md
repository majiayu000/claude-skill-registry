---
name: naist-portal
description: NAISTポータル（edu-portal.naist.jp/uprx/）にSAML+TOTP認証でアクセスし、成績・履修状況・お知らせをSlackに投稿する。Use when user says 「成績確認して」「履修状況教えて」「ポータルのお知らせは？」「単位確認して」or similar portal access requests in #ai-<name> channels.
metadata:
  source: roundcube-webmail-skill (same NAIST SSO pattern)
  requires:
    bins: [node, security]
    npm: [playwright, otplib]
---

# naist-portal

NAISTポータルにSAML+TOTP認証でアクセスし、成績・お知らせをSlackに返す。

## 認証情報の保存場所

| 変数 | 保存場所 |
|------|---------|
| `PORTAL_USERNAME` | `.env` |
| `PORTAL_PASSWORD` | macOS Keychain（`naist-portal` / `PORTAL_PASSWORD`） |
| `PORTAL_TOTP_SECRET` | macOS Keychain（`naist-portal` / `PORTAL_TOTP_SECRET`） |

## セットアップ（初回のみ — ダイスが実行）

```bash
# 1. スキルディレクトリで依存関係インストール
cd /Users/anicca/.openclaw/skills/naist-portal
npm install

# 2. TOTPシークレット取得（Google AuthenticatorのQRから）
brew install zbar
# Google Authenticator → アカウント長押し → 移動 → QRコードをスクリーンショット
# AirDrop で Mac Mini に送る
zbarimg --raw ~/Downloads/screenshot.PNG
# 出力例: otpauth://totp/...?secret=ABCDEF123456

# 3. Keychain に保存
bash scripts/setup-keychain.sh

# 4. .env に追記（機密情報なし）
echo "PORTAL_USERNAME=your-username" >> /Users/anicca/.openclaw/.env
```

## 使い方

```bash
# 成績・履修確認
node scripts/read-portal.js --mode grades

# お知らせ確認
node scripts/read-portal.js --mode notices

# 両方
node scripts/read-portal.js --mode all
```

## 実行手順（Aniccaが自動実行）

### 「成績確認して」と言われたら

```bash
cd /Users/anicca/.openclaw/skills/naist-portal && node scripts/read-portal.js --mode grades
```

### 「お知らせ確認して」と言われたら

```bash
cd /Users/anicca/.openclaw/skills/naist-portal && node scripts/read-portal.js --mode notices
```

## Slack 出力フォーマット

### 成績確認

```
📊 *NAIST ポータル — 成績・履修状況*

🎓 春学期 2025
━━━━━━━━━━━━━━━━━━━━━━
科目名           単位  評価
情報科学特論      2    A
機械学習          2    S
...
━━━━━━━━━━━━━━━━━━━━━━
取得単位: XX / XX
```

### お知らせ

```
📢 *NAIST ポータル — お知らせ*

1. [2025-02-20] 履修変更期間について（締切: 2025-03-01）
2. [2025-02-18] 奨学金申請書類の提出について
...

新着: X件
```

## 認証フロー

```
Navigate to edu-portal.naist.jp/uprx/
    ↓
NAIST IdP (SAML) リダイレクト
    ↓
username + TOTP コード入力
    ↓
ポータルトップページ
    ↓
成績 or お知らせページへ遷移
```

## 注意

- TOTPシークレット未設定の場合: セットアップ手順をSlackに返す
- セッションタイムアウト: 再ログインして1回リトライ
- ポータルHTML変更: エラー時はスクリーンショットを `/tmp/naist-portal-error.png` に保存
