---
globs:
  - "README.md"
  - "CLAUDE.md"
  - "docs/**/*.md"
  - "database_schema.md"
  - "docker-compose.yml"
  - "backend/package.json"
  - "frontend/package.json"
---

# Taiho App Context Skill

## Description
泰鵬支店アプリケーションのプロジェクト文脈を理解するためのスキルです。

## Automatic Activation
このスキルは以下のファイルを編集する際に自動で適用されます：
- `README.md`, `CLAUDE.md` - プロジェクトドキュメント
- `docs/**/*.md` - 各種ドキュメント
- `database_schema.md` - データベース設計
- `docker-compose.yml` - Docker設定
- `*/package.json` - パッケージ設定

## Project Overview

**泰鵬支店** - ラーメン屋のホームページアプリケーション

### Main Features
- メニュー表示・管理
- ユーザー登録・ログイン（AWS Cognito）
- オーダー管理（店内・テイクアウト）
- 注文履歴管理
- チャット機能（注文に紐づく）
- イベント・カレンダー管理
- クーポン機能
- Stripe決済

## Tech Stack

### Backend
- Runtime: Node.js 22
- Framework: Express.js + TypeScript
- Database: AWS DynamoDB
- Authentication: AWS Cognito
- Architecture: DDD（ドメイン駆動設計）

### Frontend
- Framework: React 18 + TypeScript
- Build Tool: Vite
- Styling: Tailwind CSS
- UI Components: Radix UI（shadcn/ui）

### Infrastructure
- Lambda: バックエンドAPI
- API Gateway: HTTP API v2
- DynamoDB: データベース
- Cognito: ユーザー認証
- S3 + CloudFront: フロントエンドホスティング
- CDK: インフラ管理

## Key Files

### Backend
| ファイル | 用途 |
|---------|------|
| `backend/src/index.ts` | Lambda用エントリーポイント |
| `backend/src/local.ts` | ローカル開発用エントリーポイント |
| `backend/src/server.ts` | Expressサーバー設定 |
| `backend/src/container/Container.ts` | DIコンテナ |
| `backend/src/config/swagger.ts` | API仕様書 |

### Frontend
| ファイル | 用途 |
|---------|------|
| `frontend/src/App.tsx` | ルートコンポーネント |
| `frontend/src/services/apiClient.ts` | API通信設定 |
| `frontend/src/services/*Api.ts` | 各種API |

### CDK
| ファイル | 用途 |
|---------|------|
| `cdk/bin/taiho-app.ts` | エントリーポイント |
| `cdk/lib/*-stack.ts` | 各種スタック |

## DynamoDB Tables

| テーブル | 用途 |
|---------|------|
| Users | ユーザー情報（Cognito連携） |
| Orders | 注文情報 |
| OrderLists | 注文明細 |
| Chats | チャット履歴 |
| Events | イベント情報 |
| Calendars | カレンダー情報 |
| Notices | お知らせ |
| Coupons | クーポンマスタ |
| UserCoupons | ユーザークーポン |
| Settings | 設定情報 |

## Order Status Flow

```
pending_payment → preparing → shipping → completed
                                      ↘ cancelled
```

| ステータス | 説明 | チャット |
|-----------|------|---------|
| pending_payment | 決済待ち | 可能 |
| preparing | 準備中 | 可能 |
| shipping | 配送中 | 可能 |
| completed | 完了 | 終了 |
| cancelled | キャンセル | 終了 |

## Development Commands

```bash
# 全サービス起動
docker compose up --build

# バックエンドのみ
docker compose up backend

# フロントエンドのみ
docker compose up frontend
```

### Access URLs (Local)
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- DynamoDB Admin: http://localhost:8001
- API Docs: http://localhost:8080/api-docs

### Access URLs (Production)
- Frontend: https://d3nb8mmcfxx6f2.cloudfront.net
- API: https://gia82b3ffb.execute-api.ap-northeast-1.amazonaws.com/prod/

## Documentation

| ドキュメント | 用途 |
|-------------|------|
| `README.md` | セットアップガイド |
| `CLAUDE.md` | Claude Code作業ガイド |
| `database_schema.md` | DB設計 |
| `docs/architecture.md` | システム構造 |
| `docs/api-reference.md` | API仕様 |
| `docs/CDK_DEPLOYMENT.md` | デプロイ手順 |
| `docs/STRIPE.md` | 決済機能 |
| `docs/DEVELOPMENT_STATUS.md` | 開発状況 |

## Important Notes

### Coding
- TypeScriptの厳密な型チェック
- DDDアーキテクチャに従う
- API追加時はSwagger定義も更新

### Git
- メインブランチ: `develop`
- コミットプレフィックス: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`

### Deploy
- デプロイはユーザーの明示的な指示があってから実行
- デプロイ前に`npm run build`と`npx cdk diff`を実行

### Documentation
- コードレビュー完了後、`docs/DEVELOPMENT_STATUS.md`を更新
