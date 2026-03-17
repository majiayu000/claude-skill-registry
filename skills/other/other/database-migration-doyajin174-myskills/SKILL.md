---
name: database-migration
description: Manage database schema changes with version control. Use when modifying DB schema, adding tables/columns, or setting up new projects. Covers Prisma, Drizzle, and migration best practices.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Database Migration

데이터베이스 스키마 변경을 버전 관리하는 스킬입니다.

## Core Principle

> **"DB 스키마도 코드처럼 버전 관리한다."**
> **"수동으로 ALTER TABLE 치는 순간, 협업이 망가진다."**

## Rules

| 규칙 | 상태 | 설명 |
|------|------|------|
| 마이그레이션 파일 생성 | 🔴 필수 | 수동 SQL 실행 금지 |
| 롤백 가능 | 🔴 필수 | down migration 필수 |
| 순차 실행 | 🔴 필수 | 마이그레이션 순서 보장 |
| 프로덕션 백업 | 🔴 필수 | 마이그레이션 전 백업 |

## Prisma (권장)

### 초기 설정

```bash
# Prisma 설치
npm install prisma @prisma/client

# 초기화
npx prisma init

# .env에 DATABASE_URL 설정
# DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

### 스키마 정의

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### 마이그레이션 워크플로우

```bash
# 1. 스키마 변경 후 마이그레이션 생성
npx prisma migrate dev --name add_user_table

# 2. 마이그레이션 파일 확인
ls prisma/migrations/

# 3. 프로덕션 배포
npx prisma migrate deploy

# 4. 클라이언트 재생성
npx prisma generate
```

### 마이그레이션 파일 구조

```
prisma/
├── schema.prisma
└── migrations/
    ├── 20240101000000_init/
    │   └── migration.sql
    ├── 20240102000000_add_user_table/
    │   └── migration.sql
    └── migration_lock.toml
```

### 마이그레이션 명령어

```bash
# 개발: 마이그레이션 생성 + 적용
npx prisma migrate dev --name <migration_name>

# 프로덕션: 마이그레이션만 적용
npx prisma migrate deploy

# 상태 확인
npx prisma migrate status

# 리셋 (⚠️ 개발용만)
npx prisma migrate reset
```

## Drizzle ORM

### 초기 설정

```bash
# Drizzle 설치
npm install drizzle-orm postgres
npm install -D drizzle-kit
```

### 스키마 정의

```typescript
// src/db/schema.ts
import { pgTable, serial, text, timestamp, boolean, integer } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  authorId: integer('author_id').references(() => users.id),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});
```

### drizzle.config.ts

```typescript
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

### 마이그레이션 명령어

```bash
# 마이그레이션 생성
npx drizzle-kit generate:pg

# 마이그레이션 적용
npx drizzle-kit push:pg

# 스키마 시각화
npx drizzle-kit studio
```

## 마이그레이션 Best Practices

### 1. 작은 단위로 마이그레이션

```sql
-- ❌ BAD: 한 번에 많은 변경
-- migration: big_refactor
ALTER TABLE users ADD COLUMN age INT;
ALTER TABLE users ADD COLUMN address TEXT;
ALTER TABLE users DROP COLUMN old_field;
CREATE TABLE new_table (...);
DROP TABLE old_table;

-- ✅ GOOD: 작은 단위로 분리
-- migration: add_user_age
ALTER TABLE users ADD COLUMN age INT;

-- migration: add_user_address
ALTER TABLE users ADD COLUMN address TEXT;
```

### 2. 안전한 컬럼 추가

```sql
-- ❌ BAD: NOT NULL without default (기존 데이터 문제)
ALTER TABLE users ADD COLUMN status TEXT NOT NULL;

-- ✅ GOOD: default 값 포함
ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'active';

-- 또는 nullable로 추가 후 나중에 마이그레이션
ALTER TABLE users ADD COLUMN status TEXT;
UPDATE users SET status = 'active' WHERE status IS NULL;
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
```

### 3. 안전한 컬럼 삭제

```sql
-- ❌ BAD: 바로 삭제
ALTER TABLE users DROP COLUMN old_field;

-- ✅ GOOD: 단계적 삭제
-- Step 1: 코드에서 컬럼 사용 제거
-- Step 2: 배포 후 안정화 확인
-- Step 3: 마이그레이션으로 컬럼 삭제
```

### 4. 인덱스 추가

```sql
-- ❌ BAD: 큰 테이블에 동기 인덱스 생성 (락 발생)
CREATE INDEX idx_users_email ON users(email);

-- ✅ GOOD: CONCURRENTLY 사용 (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

## 롤백 전략

### Prisma 롤백

```bash
# 마지막 마이그레이션 롤백
npx prisma migrate resolve --rolled-back <migration_name>

# 또는 특정 시점으로 복구
npx prisma migrate reset  # ⚠️ 개발용만!
```

### 수동 롤백 스크립트

```sql
-- migrations/20240102_add_status/down.sql
ALTER TABLE users DROP COLUMN status;
```

## CI/CD 통합

### GitHub Actions

```yaml
# .github/workflows/migrate.yml
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'prisma/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### 마이그레이션 검증

```yaml
# PR에서 마이그레이션 유효성 검사
jobs:
  validate-migration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Run migrations on test DB
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test
```

## 프로덕션 체크리스트

### 마이그레이션 전

- [ ] 데이터베이스 백업 완료
- [ ] 마이그레이션 SQL 리뷰 완료
- [ ] 테스트 환경에서 검증 완료
- [ ] 롤백 계획 준비
- [ ] 유지보수 알림 (필요시)

### 마이그레이션 중

- [ ] 모니터링 대시보드 확인
- [ ] 에러 로그 모니터링
- [ ] 락 타임아웃 확인

### 마이그레이션 후

- [ ] 애플리케이션 정상 동작 확인
- [ ] 데이터 무결성 확인
- [ ] 성능 저하 여부 확인

## Workflow

### 개발 시

```
1. 스키마 파일 수정 (schema.prisma)
2. npx prisma migrate dev --name <description>
3. 생성된 SQL 확인
4. Git 커밋 (스키마 + 마이그레이션 파일)
```

### 배포 시

```
1. PR 머지
2. CI에서 npx prisma migrate deploy 실행
3. 프로덕션 확인
4. (문제 시) 롤백 실행
```

## Checklist

- [ ] 마이그레이션 도구 설정 (Prisma/Drizzle)
- [ ] 마이그레이션 파일 Git 추적
- [ ] CI/CD에 마이그레이션 단계 추가
- [ ] 롤백 스크립트 준비
- [ ] 프로덕션 백업 자동화

## References

- [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate)
- [Drizzle Kit](https://orm.drizzle.team/kit-docs/overview)
- [Zero-downtime migrations](https://planetscale.com/blog/safely-making-database-schema-changes)
