---
name: environment-manager
description: Manage environment configurations, secrets, and .env files across environments. Use when configuring application environments or managing secrets.
---

# Environment Manager Skill

環境変数管理を支援するスキルです。

## 主な機能

- **.env ファイル生成**: テンプレート作成
- **環境変数検証**: 必須項目チェック
- **セキュリティ**: 機密情報の扱い
- **ドキュメント**: 変数の説明

## .env テンプレート

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
DATABASE_POOL_SIZE=10

# Redis
REDIS_URL=redis://localhost:6379
REDIS_TTL=3600

# API Keys (Never commit actual keys!)
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG...

# App Config
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# JWT
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=7d
```

## .env.example

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/dbname

# API Keys (Get from https://dashboard.stripe.com)
STRIPE_SECRET_KEY=

# Application
NODE_ENV=development
PORT=3000
```

## 環境変数検証

```javascript
// config/env.js
const requiredEnvVars = [
  'DATABASE_URL',
  'REDIS_URL',
  'JWT_SECRET'
];

function validateEnv() {
  const missing = requiredEnvVars.filter(key => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
  }
}

validateEnv();
```

## バージョン情報
- Version: 1.0.0
