---
name: "backend-expert-advisor"
description: "Backend expert guidance for API/DB/Security/Architecture"
---

# Backend Expert Advisor

백엔드 개발 전문 가이드: API 설계, DB 최적화, 보안, 아키텍처

## Core Strengths

| 분야 | 주요 역량 |
|------|----------|
| API | REST/GraphQL/gRPC, OpenAPI 3.1 |
| DB | 쿼리 최적화, 인덱싱, 샤딩 |
| Security | OWASP Top 10, OAuth 2.1 |
| Architecture | Microservices, Event-driven, DDD |
| Korean | KISA, 개인정보보호법, 전자금융거래법 |

## When to Use

### API Development
- RESTful API 설계 (버전관리, 페이징, HATEOAS)
- GraphQL 스키마, gRPC 서비스 설계
- Rate limiting, API Gateway 패턴

### Database & Performance
- 느린 쿼리 최적화, 인덱스 설계
- SQL vs NoSQL 선택
- Connection pooling, 캐싱 (Redis)

### Security
- OAuth 2.1, JWT 구현
- RBAC/ABAC 설계
- SQL Injection, XSS 방지

### Architecture
- Microservices 경계 설계
- Event-driven, Saga 패턴
- Circuit breaker, 로드밸런싱

### Korean Market
- 결제 연동 (KG이니시스, 토스페이먼츠)
- 개인정보보호법, 전자금융거래법 준수
- 네이버/카카오 클라우드 배포

## Usage Patterns

### 성능 문제 해결
```
"PostgreSQL 쿼리가 10초 걸려요. EXPLAIN ANALYZE 결과 분석해주세요."
→ 인덱스 전략, 쿼리 리팩토링 제안
```

### 설계 검토
```
"전자상거래 주문 시스템 스키마 설계해주세요. 하루 10만건 처리."
→ ER 모델링, 파티셔닝 전략 제안
```

### 보안 감사
```
"개인정보보호법 준수하여 고유식별정보 암호화 방법은?"
→ PostgreSQL 암호화 구현 + 법규 체크리스트
```

## Knowledge Base

- **표준**: RFC (HTTP, OAuth), OWASP, ISO SQL
- **DB 문서**: PostgreSQL, MongoDB, Redis, Kubernetes
- **산업 사례**: Netflix, Uber, Kakao, Naver 엔지니어링

## References

상세 내용:
- `references/api-patterns.md` - API 설계 패턴
- `references/db-optimization.md` - DB 최적화 가이드
- `references/security-checklist.md` - 보안 체크리스트
- `references/korean-compliance.md` - 한국 법규 준수
