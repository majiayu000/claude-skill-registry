---
globs:
  - "cdk/**/*.ts"
  - "cdk/.env"
  - "cdk/.env.example"
---

# CDK Review Skill

## Description
AWS CDKスタックのコードレビューとベストプラクティスを確認するためのスキルです。

## Automatic Activation
このスキルは以下のファイルを編集する際に自動で適用されます：
- `cdk/**/*.ts` - CDKスタック、エントリーポイント
- `cdk/.env` - 環境変数設定
- `cdk/.env.example` - 環境変数サンプル

## Stack Structure

```
cdk/
├── bin/
│   └── taiho-app.ts              # エントリーポイント
└── lib/
    ├── database-stack.ts         # DynamoDB
    ├── cognito-stack.ts          # Cognito User Pool
    ├── lambda-stack.ts           # Lambda関数
    ├── api-gateway-stack.ts      # HTTP API v2
    ├── frontend-stack.ts         # S3 + CloudFront
    ├── route53-stack.ts          # Route53（オプション）
    └── certificate-stack.ts      # ACM証明書（オプション）
```

## Review Checklist

### 1. Security
- [ ] IAMポリシーが最小権限になっているか
- [ ] CORS設定が適切か（本番は環境変数から取得）
- [ ] S3バケットのパブリックアクセスがブロックされているか
- [ ] シークレットがハードコードされていないか

### 2. Cost Optimization
- [ ] ログ保持期間が30日に設定されているか
- [ ] 不要なリソースがないか
- [ ] CloudFront Price Classが適切か（PRICE_CLASS_200推奨）
- [ ] DynamoDBがオンデマンドモードか

### 3. Best Practices
- [ ] 環境変数が`.env`から読み込まれているか
- [ ] 削除保護（RemovalPolicy.RETAIN）が重要リソースに設定されているか
- [ ] CfnOutputで必要な値が出力されているか
- [ ] スタック間の依存関係が正しいか

### 4. Consistency
- [ ] 命名規則が統一されているか（`TaihoApp`プレフィックス）
- [ ] ログ保持期間が統一されているか（30日）
- [ ] コメントが適切に記載されているか

## Current Configuration

### API Gateway (HTTP API v2)
```typescript
// REST API v1より約70%安価
corsPreflight: {
  allowOrigins: corsOrigins,  // 環境変数から取得
  allowMethods: [CorsHttpMethod.ANY],
  allowHeaders: ['Content-Type', 'Authorization'],
}

// ルート
/api/{proxy+}  // メインAPI
/health        // ヘルスチェック
```

### Lambda
- Runtime: Node.js 22.x
- Memory: 512MB
- Timeout: 29秒（API Gatewayの最大に合わせる）
- Log Retention: 30日

### CloudFront
- Price Class: PRICE_CLASS_200
- Error Response TTL: 60秒
- Compress: true
- Log Bucket Lifecycle: 30日

### DynamoDB
- Billing Mode: PAY_PER_REQUEST
- Point-in-time Recovery: enabled
- Removal Policy: RETAIN

## Environment Variables

`cdk/.env`に設定:

```bash
CDK_DEFAULT_ACCOUNT=123456789012
CDK_DEFAULT_REGION=ap-northeast-1
CORS_ORIGIN=https://xxx.cloudfront.net
ADMIN_EMAILS=admin@example.com
FRONTEND_URL=https://xxx.cloudfront.net
STRIPE_SECRET_KEY=sk_xxx
```

## Deploy Commands

```bash
cd cdk

# 差分確認（デプロイ前に必ず実行）
npx cdk diff

# 全スタックデプロイ
npx cdk deploy --all

# 個別デプロイ（推奨順序）
npx cdk deploy TaihoAppDatabaseStack
npx cdk deploy TaihoAppCognitoStack
npx cdk deploy TaihoAppLambdaStack
npx cdk deploy TaihoAppApiGatewayStack
npx cdk deploy TaihoAppFrontendStack
```
