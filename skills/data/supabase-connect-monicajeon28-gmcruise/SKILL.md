---
name: supabase-connect
description: Direct Supabase PostgreSQL database connection and SQL execution. Use when creating tables, running SQL queries, managing schemas, or setting up database migrations. Automatically reads connection info from project .env files.
---

# Supabase Database Connection

Supabase PostgreSQL 데이터베이스에 직접 연결하여 테이블 생성, SQL 실행 등의 작업을 수행합니다.

## When to Use
- Supabase 테이블 생성/수정/삭제
- SQL 쿼리 직접 실행
- 데이터베이스 스키마 확인
- 데이터 마이그레이션

## Instructions

### Step 1: .env에서 연결 정보 확인
```bash
# 프로젝트 .env 또는 .env.local 파일에서 확인
SUPABASE_DB_HOST=aws-*.pooler.supabase.com
SUPABASE_DB_PORT=5432
SUPABASE_DB_USER=postgres.projectref
SUPABASE_DB_PASSWORD=your_password
SUPABASE_DB_NAME=postgres
```

### Step 2: Node.js로 연결 및 실행
```javascript
const dns = require('dns');
const { Client } = require('pg');

// WSL IPv6 문제 해결 - 필수
dns.setDefaultResultOrder('ipv4first');

const client = new Client({
  host: process.env.SUPABASE_DB_HOST,
  port: parseInt(process.env.SUPABASE_DB_PORT) || 5432,
  database: process.env.SUPABASE_DB_NAME || 'postgres',
  user: process.env.SUPABASE_DB_USER,
  password: process.env.SUPABASE_DB_PASSWORD,
  ssl: { rejectUnauthorized: false }
});

await client.connect();
const result = await client.query('YOUR SQL HERE');
console.log(result.rows);
await client.end();
```

## Common Issues

| 오류 | 해결책 |
|------|--------|
| `ENETUNREACH IPv6` | `dns.setDefaultResultOrder('ipv4first')` |
| `self-signed certificate` | `ssl: { rejectUnauthorized: false }` |
| `Tenant not found` | Pooler URL 사용 (aws-*.pooler.supabase.com) |
| `password authentication failed` | .env 비밀번호 확인 |

## Required Tools
- Bash (node 실행)
- Read (.env 파일 읽기)
