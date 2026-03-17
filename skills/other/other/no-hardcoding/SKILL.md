---
name: no-hardcoding
description: Forbid hardcoded values in code. Use this when reviewing code, writing new features, or when magic numbers/strings are detected. Enforces constants, env variables, and config files.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# No Hardcoding Policy

코드에 하드코딩된 값을 금지하고 상수/환경변수/설정 파일을 사용하도록 강제하는 스킬입니다.

## Core Principle

> **"코드에 직접 값을 쓰는 순간, 변경이 배포가 된다."**

## Rules

| 유형 | 상태 | 대안 |
|------|------|------|
| Magic Number | 🔴 금지 | 상수/enum |
| Magic String | 🔴 금지 | 상수/enum |
| URL/경로 | 🔴 금지 | 환경변수/config |
| 크리덴셜 | 🔴 **절대 금지** | `.env` + secrets |
| 타임아웃/딜레이 | 🔴 금지 | 상수/config |
| 포트 번호 | 🔴 금지 | 환경변수 |
| API 키 | 🔴 **절대 금지** | 환경변수 + secrets |

## Detection Patterns

### Magic Numbers

```typescript
// ❌ BAD: 의미 불명확
if (users.length > 100) { ... }
setTimeout(callback, 3000);
const tax = price * 0.1;

// ✅ GOOD: 의미 명확
const MAX_USERS = 100;
const DEBOUNCE_MS = 3000;
const TAX_RATE = 0.1;

if (users.length > MAX_USERS) { ... }
setTimeout(callback, DEBOUNCE_MS);
const tax = price * TAX_RATE;
```

### Magic Strings

```typescript
// ❌ BAD: 문자열 반복, 오타 위험
if (status === 'pending') { ... }
if (status === 'pending') { ... }  // 다른 곳에서 또 사용

// ✅ GOOD: 상수 또는 enum
enum Status {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
}

if (status === Status.PENDING) { ... }
```

### URLs/Endpoints

```typescript
// ❌ BAD: URL 하드코딩
const response = await fetch('https://api.example.com/users');

// ✅ GOOD: 환경변수
const API_URL = process.env.NEXT_PUBLIC_API_URL;
const response = await fetch(`${API_URL}/users`);
```

### Credentials (절대 금지)

```typescript
// ❌ CRITICAL: 절대 금지 - 보안 위협
const apiKey = 'sk-1234567890abcdef';
const password = 'admin123';
const dbConnection = 'mongodb://user:pass@host:27017';

// ✅ GOOD: 환경변수 사용
const apiKey = process.env.API_KEY;
const password = process.env.DB_PASSWORD;
const dbConnection = process.env.DATABASE_URL;
```

### Timeouts/Delays

```typescript
// ❌ BAD: 하드코딩 타임아웃
await page.waitForTimeout(5000);
time.sleep(3);

// ✅ GOOD: 조건 기반 또는 상수
const ANIMATION_DURATION = 300;
await page.waitForSelector('#content');  // 조건 기반
await delay(ANIMATION_DURATION);          // 상수 사용
```

## File Organization

```
src/
├── constants/
│   ├── index.ts         # Re-exports
│   ├── api.ts           # API 관련 상수
│   ├── ui.ts            # UI 관련 상수
│   └── business.ts      # 비즈니스 로직 상수
├── config/
│   ├── index.ts
│   └── env.ts           # 환경변수 검증 및 타입
└── types/
    └── enums.ts         # Enum 정의
```

### constants 예시

```typescript
// constants/api.ts
export const API = {
  TIMEOUT_MS: 30000,
  RETRY_COUNT: 3,
  ENDPOINTS: {
    USERS: '/api/users',
    POSTS: '/api/posts',
  },
} as const;

// constants/ui.ts
export const UI = {
  DEBOUNCE_MS: 300,
  ANIMATION_DURATION_MS: 200,
  MAX_ITEMS_PER_PAGE: 20,
  BREAKPOINTS: {
    MOBILE: 768,
    TABLET: 1024,
    DESKTOP: 1280,
  },
} as const;
```

### 환경변수 검증

```typescript
// config/env.ts
const requiredEnvVars = [
  'DATABASE_URL',
  'API_KEY',
  'NEXT_PUBLIC_API_URL',
] as const;

export function validateEnv() {
  for (const envVar of requiredEnvVars) {
    if (!process.env[envVar]) {
      throw new Error(`Missing required env var: ${envVar}`);
    }
  }
}

export const env = {
  DATABASE_URL: process.env.DATABASE_URL!,
  API_KEY: process.env.API_KEY!,
  API_URL: process.env.NEXT_PUBLIC_API_URL!,
} as const;
```

## Detection Commands

```bash
# Magic Numbers 검색 (일반적인 패턴)
grep -rn "[^a-zA-Z][0-9]\{3,\}[^a-zA-Z0-9]" --include="*.ts" --include="*.tsx" src/

# 하드코딩된 URL 검색
grep -rn "https\?://" --include="*.ts" --include="*.tsx" src/ | grep -v "node_modules"

# 잠재적 크리덴셜 검색
grep -rn "password\|apiKey\|secret\|token" --include="*.ts" --include="*.tsx" src/ | grep -v "\.d\.ts"
```

## Workflow

### 1. 코드 리뷰 시

```
하드코딩 감지:
1. Magic Number/String 검색
2. URL/경로 하드코딩 확인
3. 크리덴셜 하드코딩 확인 (최우선)

위반 발견 시:
→ 상수 추출 권장
→ 환경변수 사용 안내
→ .env.example 업데이트 확인
```

### 2. 새 기능 작성 시

```
값 사용 전 체크:
- 이 값이 변경될 수 있는가? → 환경변수/config
- 이 값이 여러 곳에서 사용되는가? → 상수
- 이 값이 민감한가? → 환경변수 + secrets
- 이 값이 의미를 가지는가? → 상수 (이름으로 의미 부여)
```

## Exceptions

### 허용되는 경우

```typescript
// 0, 1, -1 (일반적으로 명확한 의미)
const index = array.indexOf(item);
if (index === -1) { ... }

// 배열 첫/마지막 요소
const first = array[0];
const last = array[array.length - 1];

// 명확한 수학적 연산
const half = total / 2;
const percentage = (part / whole) * 100;
```

## Checklist

- [ ] Magic Number 없음
- [ ] Magic String 없음 (반복 문자열)
- [ ] URL 하드코딩 없음
- [ ] 크리덴셜 하드코딩 없음
- [ ] 상수 파일에 정리됨
- [ ] .env.example 업데이트됨
- [ ] 환경변수 검증 로직 있음
