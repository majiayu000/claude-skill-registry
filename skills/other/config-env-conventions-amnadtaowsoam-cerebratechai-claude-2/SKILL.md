---
name: Config & Environment Conventions
description: Conventions for service configuration and environment variables: naming, precedence, validation at startup, secrets handling, environment detection, and documentation patterns
---

# Config & Environment Conventions

## Overview

มาตรฐานการจัดการ configuration และ environment variables ทุก service: naming, validation, defaults, และ secret handling ที่ทำให้ deploy ข้าม environments ได้อย่างมั่นใจ

## Why This Matters

- **Portability**: Same code, different configs per env
- **Safety**: Validate config at startup, fail fast
- **Security**: Clear separation of secrets
- **Debugging**: รู้ว่า config มาจากไหน

---

## Core Concepts

### 1. Environment Variable Naming

- รูปแบบ: `<APP>_<CATEGORY>_<NAME>` (ทั้งหมด **UPPER_SNAKE_CASE**)
- `URL`/`URI` ใช้ suffix เดียวกัน (`APP_REDIS_URL`), boolean ใช้ `true|false`
- แยก “config” กับ “secret” ชัดเจน (ดูข้อ 4)
- หลีกเลี่ยงชื่อกว้าง ๆ เช่น `TOKEN`, `KEY` (ต้องบอกบริบท เช่น `APP_STRIPE_SECRET_KEY`)

### 2. Config Hierarchy

กำหนดลำดับความสำคัญชัดเจน และ document ไว้ในทุก service:

1. Secret manager (Vault/AWS SM/GCP SM)
2. Environment variables (runtime)
3. Environment-specific file (`.env.production`) (เฉพาะ local/staging ที่อนุญาต)
4. Default `.env` (เฉพาะ local)
5. Code defaults (ปลอดภัย และไม่ใช่ production values)

### 3. Config Validation

- validate ตั้งแต่ startup (fail fast) ก่อนรับ traffic
- แยก `required` vs `optional` ชัดเจน
- validate type/format/range (เช่น port, URL, enum)
- log เฉพาะ keys ที่โหลดสำเร็จ (ไม่ log ค่า secret)

### 4. Secret vs Config

- **Secret**: credentials, tokens, private keys, passwords, encryption keys → ต้องมาจาก secret manager และ rotate ได้
- **Config**: hostnames, timeouts, feature toggles, limits → environment variables/ไฟล์ config ได้
- หลีกเลี่ยงการผสม: อย่าเอา secret ลง `.env.example` (ให้ใส่เป็นค่าว่าง + comment ว่า “from secret manager”)

### 5. Feature Flags Integration

- config ที่เปลี่ยน “ตอน runtime” (เช่น rollout %) → ใช้ feature flag system
- config ที่เป็น “deploy-time” (เช่น DB host, timeout) → ใช้ env vars
- หลีกเลี่ยง “config drift”: ทุก flag ต้องมี owner + cleanup date

### 6. Environment Detection

- มีตัวแปรเดียวสำหรับ env: `APP_ENV=development|staging|production|test`
- หลีกเลี่ยง inference จาก `NODE_ENV` เพียงอย่างเดียว (ใช้ร่วมได้ แต่ให้มี source-of-truth)
- gating behavior ที่อันตราย (debug endpoints, verbose logging) ต้องผูกกับ `APP_ENV`

### 7. Config Documentation

- ทุก service ต้องมี `.env.example` ที่ครบ keys และมีคำอธิบายสั้น ๆ
- ระบุ default/constraints เช่น `APP_HTTP_PORT=3000` (min/max ถ้ามี)
- ถ้ามี schema (Zod/JSON schema) ให้ link ในเอกสารของ service/README

### 8. Default Values

- defaults ต้อง “ปลอดภัย” (เช่น feature ปิด, rate limit conservative)
- ห้ามใส่ค่า production จริงเป็น default
- config สำคัญ (DB URL, secret keys) ควร required และบังคับให้ตั้งใน env/secret manager

## Quick Start

```typescript
import { z } from "zod";

const schema = z.object({
  APP_ENV: z.enum(["development", "staging", "production", "test"]).default("development"),
  APP_HTTP_PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  APP_DATABASE_URL: z.string().url(),
});

export type AppConfig = z.infer<typeof schema>;

export function loadConfig(env: Record<string, string | undefined> = process.env): AppConfig {
  const result = schema.safeParse(env);
  if (!result.success) {
    throw new Error(`Invalid config: ${result.error.message}`);
  }
  return result.data;
}
```

## Production Checklist

- [ ] All env vars documented in .env.example
- [ ] Config validated at startup
- [ ] Secrets not in .env files
- [ ] Defaults are safe (not production values)
- [ ] Required vs optional clearly marked
- [ ] Config changes don't require code changes

## Naming Convention

```bash
# Format: <APP>_<CATEGORY>_<NAME>

# Database
APP_DB_HOST=localhost
APP_DB_PORT=5432
APP_DB_NAME=myapp

# External Services
APP_REDIS_URL=redis://localhost:6379
APP_STRIPE_API_URL=https://api.stripe.com

# Feature Flags
APP_FEATURE_NEW_CHECKOUT=true

# Secrets (loaded from secret manager)
APP_SECRET_DB_PASSWORD=  # from Vault/AWS SM
APP_SECRET_API_KEY=      # from Vault/AWS SM
```

## Config Hierarchy

```
Priority (highest to lowest):
1. Secret Manager (Vault, AWS SM)
2. Environment Variables
3. Environment-specific file (.env.production)
4. Default .env file
5. Code defaults
```

## Anti-patterns

1. **Hardcoded values**: Config in code
2. **Secrets in .env**: Committed to git
3. **No validation**: Runtime failures
4. **Magic strings**: Config keys scattered in code
5. **Implicit env**: behavior เปลี่ยนตาม `NODE_ENV` แบบคาดเดายาก

## Integration Points

- Secret managers
- CI/CD pipelines
- Container orchestration
- Feature flag systems

## Further Reading

- [12-Factor App: Config](https://12factor.net/config)
- [Node.js Config Best Practices](https://github.com/goldbergyoni/nodebestpractices#1-project-structure-practices)
