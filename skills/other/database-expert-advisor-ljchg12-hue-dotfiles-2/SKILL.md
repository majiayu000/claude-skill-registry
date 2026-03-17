---
name: "database-expert-advisor"
description: "Database design, optimization, and operations expert"
---

# Database Expert Advisor

데이터베이스 설계, 최적화, 운영 종합 컨설팅

## Core Capabilities

| 역량 | 상세 |
|------|------|
| 쿼리 최적화 | EXPLAIN 분석, 인덱스 전략, 실행 계획 |
| 스키마 설계 | ER 모델링, 정규화(1NF-BCNF), 파티셔닝 |
| 성능 튜닝 | 병목 분석, 트랜잭션 최적화, 캐싱 |
| 보안 | 접근 제어, 암호화, SQL Injection 방지 |
| 마이그레이션 | DB 전환, 샤딩, 복제 |
| 트러블슈팅 | 데드락 해결, 메모리 누수, 성능 저하 |

## Supported Databases

| 카테고리 | DB | 용도 |
|---------|-----|------|
| 관계형 | PostgreSQL, MySQL, MariaDB | OLTP |
| NoSQL | MongoDB, Redis, Cassandra | 대용량, 캐싱 |
| NewSQL | CockroachDB, TiDB | 분산 SQL |
| 시계열 | TimescaleDB, InfluxDB | 모니터링 |
| 그래프 | Neo4j | 관계 분석 |

## When to Use

### ✅ 적합한 경우
- 느린 쿼리 분석 (응답 > 1초)
- 신규 스키마 설계
- MySQL → PostgreSQL 마이그레이션
- 개인정보보호법 준수
- 수억 건 대용량 데이터

### ❌ 부적합한 경우
- 단순 SQL 문법 질문
- ORM 사용법
- 클라우드 UI 조작

## Usage Patterns

### 성능 최적화
```
"EXPLAIN ANALYZE 결과 분석해주세요"
→ 인덱스 추가/수정, 쿼리 리팩토링 제안
```

### 스키마 설계
```
"주문 시스템 DB 설계, 하루 10만건 처리"
→ ER 다이어그램 + 파티셔닝 전략
```

### 마이그레이션
```
"MySQL 5.7 → PostgreSQL 16 전환 계획"
→ 단계별 마이그레이션 가이드
```

### 보안
```
"개인정보 암호화 구현 방법"
→ PostgreSQL pgcrypto 사용법 + 법규 체크리스트
```

## References

- `references/query-optimization.md` - 쿼리 최적화 기법
- `references/schema-patterns.md` - 스키마 설계 패턴
- `references/migration-guide.md` - 마이그레이션 가이드
- `references/security-best-practices.md` - 보안 베스트 프랙티스
