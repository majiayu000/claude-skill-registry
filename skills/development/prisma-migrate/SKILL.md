---
name: prisma-migrate
description: Prisma 마이그레이션 생성 및 적용
disable-model-invocation: true
---

# /prisma-migrate

Prisma 스키마 변경 후 마이그레이션을 안전하게 생성합니다.

## 실행 단계

1. `git diff apps/api/prisma/schema.prisma`로 스키마 변경사항 확인
2. 변경사항 분석 후 마이그레이션 이름 제안
3. 사용자 확인 후 `pnpm --filter @school/api prisma migrate dev --name <이름>` 실행
4. 생성된 SQL 파일 검토 (`apps/api/prisma/migrations/` 확인)
5. `pnpm --filter @school/api prisma generate`로 클라이언트 재생성

## 주의사항

- 프로덕션 DB에 직접 `migrate deploy` 하지 않음
- 데이터 손실 가능성 있는 변경(컬럼 삭제, 타입 변경 등)은 사용자에게 경고
- 마이그레이션 이름은 snake_case 사용 (예: `add_phone_column`)