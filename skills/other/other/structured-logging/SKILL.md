---
name: structured-logging
description: Implement JSON-based structured logging for observability. Use when setting up logging, debugging production issues, or preparing for log aggregation (ELK, Datadog). Covers log levels, context, and best practices.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
license: MIT
metadata:
  author: antigravity-team
  version: "1.0"
---

# Structured Logging

JSON 포맷의 구조화된 로깅을 구현하는 스킬입니다.

## Core Principle

> **"print문 대신 구조화된 로그를 남겨라."**
> **"로그는 검색 가능하고, 집계 가능해야 한다."**

## 왜 Structured Logging인가?

### ❌ 일반 텍스트 로그

```
[2024-01-15 10:30:45] ERROR User login failed for user123
[2024-01-15 10:30:46] INFO Processing request
```

- 파싱 어려움
- 필터링/검색 제한
- 컨텍스트 손실

### ✅ 구조화된 로그 (JSON)

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "error",
  "message": "User login failed",
  "userId": "user123",
  "errorCode": "AUTH_INVALID_PASSWORD",
  "requestId": "req-abc-123",
  "duration": 45
}
```

- 쉬운 파싱/검색
- 필드별 필터링
- 풍부한 컨텍스트

## Log Levels

| Level | 용도 | 예시 |
|-------|------|------|
| `fatal` | 시스템 종료 필요 | DB 연결 완전 실패 |
| `error` | 에러 발생, 복구 가능 | API 호출 실패 |
| `warn` | 잠재적 문제 | 지연된 응답 |
| `info` | 주요 이벤트 | 사용자 로그인 성공 |
| `debug` | 디버깅 정보 | 함수 파라미터 |
| `trace` | 상세 추적 | 실행 흐름 |

### 프로덕션 로그 레벨

```
프로덕션: info 이상만
개발: debug 이상
디버깅 시: trace까지
```

## 필수 로그 필드

```typescript
interface LogEntry {
  // 필수
  timestamp: string;    // ISO 8601
  level: string;        // error, warn, info, debug
  message: string;      // 사람이 읽을 수 있는 메시지

  // 권장
  requestId?: string;   // 요청 추적
  userId?: string;      // 사용자 식별
  service?: string;     // 서비스명
  environment?: string; // prod, staging, dev

  // 상황별
  error?: {
    name: string;
    message: string;
    stack?: string;
  };
  duration?: number;    // ms
  metadata?: Record<string, unknown>;
}
```

## Node.js 구현

### Pino (권장 - 고성능)

```bash
npm install pino pino-pretty
```

```typescript
// lib/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',

  // 기본 필드
  base: {
    service: 'my-app',
    environment: process.env.NODE_ENV,
  },

  // 타임스탬프 포맷
  timestamp: pino.stdTimeFunctions.isoTime,

  // 개발 환경: pretty print
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
});

// 사용
logger.info({ userId: '123' }, 'User logged in');
logger.error({ error, requestId }, 'Request failed');
```

### Winston

```bash
npm install winston
```

```typescript
// lib/logger.ts
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'my-app',
    environment: process.env.NODE_ENV,
  },
  transports: [
    new winston.transports.Console({
      format: process.env.NODE_ENV === 'development'
        ? winston.format.combine(
            winston.format.colorize(),
            winston.format.simple()
          )
        : winston.format.json(),
    }),
  ],
});
```

## Request Context

### Request ID 전파

```typescript
// middleware/requestId.ts
import { randomUUID } from 'crypto';
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const requestId = request.headers.get('x-request-id') || randomUUID();

  const response = NextResponse.next();
  response.headers.set('x-request-id', requestId);

  return response;
}
```

### AsyncLocalStorage (권장)

```typescript
// lib/context.ts
import { AsyncLocalStorage } from 'async_hooks';

interface RequestContext {
  requestId: string;
  userId?: string;
  startTime: number;
}

export const asyncLocalStorage = new AsyncLocalStorage<RequestContext>();

// 미들웨어에서 설정
export function withContext<T>(context: RequestContext, fn: () => T): T {
  return asyncLocalStorage.run(context, fn);
}

// 로거에서 사용
export function getContext(): RequestContext | undefined {
  return asyncLocalStorage.getStore();
}
```

### Context-aware Logger

```typescript
// lib/logger.ts
import pino from 'pino';
import { getContext } from './context';

const baseLogger = pino({ /* config */ });

export const logger = {
  info: (obj: object, msg?: string) => {
    const ctx = getContext();
    baseLogger.info({ ...obj, ...ctx }, msg);
  },
  error: (obj: object, msg?: string) => {
    const ctx = getContext();
    baseLogger.error({ ...obj, ...ctx }, msg);
  },
  // ... other levels
};
```

## 로깅 패턴

### API 요청 로깅

```typescript
// middleware/logging.ts
export async function loggingMiddleware(req: Request, handler: Function) {
  const startTime = Date.now();
  const requestId = randomUUID();

  logger.info({
    requestId,
    method: req.method,
    url: req.url,
    userAgent: req.headers.get('user-agent'),
  }, 'Request started');

  try {
    const response = await handler(req);

    logger.info({
      requestId,
      statusCode: response.status,
      duration: Date.now() - startTime,
    }, 'Request completed');

    return response;
  } catch (error) {
    logger.error({
      requestId,
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack,
      },
      duration: Date.now() - startTime,
    }, 'Request failed');

    throw error;
  }
}
```

### 비즈니스 이벤트 로깅

```typescript
// 사용자 활동
logger.info({
  event: 'user.login',
  userId,
  method: 'google_oauth',
  ip: request.ip,
}, 'User logged in');

// 결제
logger.info({
  event: 'payment.success',
  userId,
  amount: 9900,
  currency: 'KRW',
  paymentId,
}, 'Payment completed');

// 에러
logger.error({
  event: 'payment.failed',
  userId,
  amount: 9900,
  errorCode: 'CARD_DECLINED',
  paymentId,
}, 'Payment failed');
```

### 성능 로깅

```typescript
async function fetchData() {
  const startTime = Date.now();

  try {
    const result = await db.query(/* ... */);

    logger.info({
      operation: 'db.query',
      table: 'users',
      duration: Date.now() - startTime,
      rowCount: result.length,
    }, 'Database query completed');

    return result;
  } catch (error) {
    logger.error({
      operation: 'db.query',
      table: 'users',
      duration: Date.now() - startTime,
      error: error.message,
    }, 'Database query failed');

    throw error;
  }
}
```

## 금지 패턴

```typescript
// ❌ BAD: 민감 정보 로깅
logger.info({ password, creditCard, ssn }, 'User data');

// ❌ BAD: 과도한 로깅 (성능 저하)
for (const item of items) {
  logger.debug({ item }, 'Processing item');  // 수천 번 호출
}

// ❌ BAD: 구조화되지 않은 로그
logger.info(`User ${userId} logged in at ${timestamp}`);

// ✅ GOOD: 구조화된 로그
logger.info({ userId, timestamp }, 'User logged in');
```

## 민감 정보 제거

```typescript
// lib/logger.ts
const sensitiveFields = ['password', 'token', 'apiKey', 'creditCard'];

function redactSensitiveData(obj: object): object {
  const redacted = { ...obj };

  for (const key of Object.keys(redacted)) {
    if (sensitiveFields.some(f => key.toLowerCase().includes(f))) {
      redacted[key] = '[REDACTED]';
    }
  }

  return redacted;
}

// Pino redact 옵션
const logger = pino({
  redact: ['password', 'creditCard', '*.token', 'headers.authorization'],
});
```

## Log Aggregation 연동

### ELK Stack (Elasticsearch)

```typescript
// filebeat.yml에서 JSON 파싱
// 또는 직접 Elasticsearch로 전송
import { Client } from '@elastic/elasticsearch';

const esClient = new Client({ node: 'http://localhost:9200' });

const esTransport = new winston.transports.Stream({
  stream: {
    write: async (log: string) => {
      await esClient.index({
        index: 'app-logs',
        document: JSON.parse(log),
      });
    },
  },
});
```

### Datadog

```bash
npm install dd-trace
```

```typescript
// tracer.ts
import tracer from 'dd-trace';

tracer.init({
  service: 'my-app',
  env: process.env.NODE_ENV,
});

// 로그에 trace ID 포함
logger.info({
  dd: {
    trace_id: tracer.scope().active()?.context().toTraceId(),
    span_id: tracer.scope().active()?.context().toSpanId(),
  },
}, 'Event with trace');
```

## Checklist

### 설정

- [ ] 구조화된 로깅 라이브러리 설치 (Pino/Winston)
- [ ] 로그 레벨 환경변수 설정
- [ ] 기본 필드 (service, environment) 설정
- [ ] Request ID 미들웨어 적용
- [ ] 민감 정보 redaction 설정

### 로깅 표준

- [ ] JSON 포맷 사용
- [ ] 적절한 로그 레벨 사용
- [ ] 비즈니스 이벤트 로깅
- [ ] 에러에 스택 트레이스 포함
- [ ] 성능 측정 로깅

### 운영

- [ ] 로그 집계 시스템 연동
- [ ] 로그 기반 알림 설정
- [ ] 로그 보관 정책 수립

## References

- [Pino](https://getpino.io/)
- [Winston](https://github.com/winstonjs/winston)
- [12-Factor App Logs](https://12factor.net/logs)
