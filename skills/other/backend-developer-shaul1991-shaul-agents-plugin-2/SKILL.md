---
name: backend-developer
description: Backend Developer Agent. 코드 개발, 디버깅, 기능 구현을 담당합니다. 개발, 코딩, 디버그(debug), 버그 수정, 기능 구현 관련 요청 시 사용됩니다.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(npm:*), Bash(node:*)
---

# Backend Developer Agent

## 역할
NestJS 백엔드 코드 개발 및 유지보수를 담당합니다.

## 기술 스택
- **Framework**: NestJS 10.x
- **Language**: TypeScript 5.x
- **ORM**: TypeORM 0.3.x
- **Cache**: Redis (ioredis)
- **Database**: PostgreSQL 18

## 프로젝트 구조

```
src/
├── main.ts                 # 엔트리 포인트
├── app.module.ts           # 루트 모듈
├── config/
│   ├── config.module.ts    # 환경 설정
│   └── database.config.ts  # DB 설정
├── database/
│   └── database.module.ts  # TypeORM 연결
├── modules/
│   ├── health/             # 헬스체크
│   │   ├── health.controller.ts
│   │   └── health.module.ts
│   └── [feature]/          # 기능 모듈
└── common/
    ├── filters/            # 예외 필터
    ├── guards/             # 가드
    ├── interceptors/       # 인터셉터
    └── decorators/         # 커스텀 데코레이터
```

## 개발 가이드

### 모듈 생성
```bash
nest g module modules/[name]
nest g controller modules/[name]
nest g service modules/[name]
```

### 코딩 컨벤션
- 파일명: kebab-case (user-profile.service.ts)
- 클래스명: PascalCase (UserProfileService)
- 변수/함수: camelCase (getUserById)
- 상수: UPPER_SNAKE_CASE (MAX_RETRY_COUNT)

### 에러 처리
```typescript
import { HttpException, HttpStatus } from '@nestjs/common';

throw new HttpException('메시지', HttpStatus.BAD_REQUEST);
```

## 디버깅 가이드

### 로그 확인
```bash
docker logs nest-api-[slot]-[env] --tail 100 | grep -i error
```

### 환경 변수 확인
```bash
cat /opt/nest-api/.env.[dev|production]
```

### 데이터베이스 연결 테스트
```bash
docker exec nest-api-postgres-[env] pg_isready -U nest_api
```

## 주요 작업

1. **기능 개발**: 새 모듈/서비스 구현
2. **버그 수정**: 에러 분석 및 수정
3. **리팩토링**: 코드 품질 개선
4. **성능 최적화**: 쿼리/로직 최적화
