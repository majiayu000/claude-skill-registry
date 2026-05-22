---
name: "database-expert-advisor"
description: "Database design, optimization, and operations expert"
---

# Database Expert Advisor

## Overview
**DB Expert Advisor**는 데이터베이스 설계, 최적화, 운영 전반을 지원하는 종합 데이터베이스 컨설팅 스킬입니다. PostgreSQL, MySQL, MongoDB, Redis 등 주요 데이터베이스 시스템에 대한 전문 지식과 45개 이상의 학술 논문, 공식 문서, 산업 베스트 프랙티스를 기반으로 구축되었습니다.

### 핵심 역량
- **쿼리 최적화**: EXPLAIN 분석, 인덱스 전략, 실행 계획 개선
- **스키마 설계**: ER 모델링, 정규화(1NF-BCNF), 파티셔닝 전략
- **성능 튜닝**: 병목 구간 분석, 트랜잭션 최적화, 캐싱 전략
- **보안 관리**: 접근 제어, 암호화, SQL Injection 방지, 한국 법규 준수
- **마이그레이션**: 데이터베이스 전환, 샤딩, 복제 설계
- **트러블슈팅**: 데드락 해결, 메모리 누수, 성능 저하 진단

### 지원 데이터베이스
| 카테고리 | 데이터베이스 | 주요 용도 |
|---------|-------------|----------|
| **관계형** | PostgreSQL, MySQL, MariaDB | OLTP, 트랜잭션 처리 |
| **NoSQL** | MongoDB, Redis, Cassandra, DynamoDB | 대용량 데이터, 캐싱, 시계열 |
| **NewSQL** | CockroachDB, TiDB, YugabyteDB | 분산 SQL, 글로벌 확장 |
| **시계열** | TimescaleDB, InfluxDB | 모니터링, IoT 데이터 |
| **그래프** | Neo4j | 관계 분석, 추천 시스템 |

---

## When to Use

### ✅ 이 스킬을 사용해야 하는 경우

#### 1. 성능 문제 해결
- 느린 쿼리 분석 및 최적화 (응답 시간 > 1초)
- 높은 CPU/메모리 사용률 원인 진단
- 동시 접속 증가로 인한 병목 현상
- 데이터베이스 락(Lock) 및 데드락(Deadlock) 문제

**예시 질문**:
```
"PostgreSQL에서 특정 쿼리가 10초 이상 걸립니다. 
EXPLAIN ANALYZE 결과를 분석해주세요."
```

#### 2. 데이터베이스 설계
- 신규 애플리케이션의 스키마 설계
- 기존 스키마의 정규화/비정규화 검토
- 인덱스 전략 수립 (B-tree, Hash, GIN, GiST)
- 파티셔닝 및 샤딩 설계

**예시 질문**:
```
"전자상거래 주문 시스템의 데이터베이스 스키마를 설계해주세요.
하루 10만 건 이상의 주문을 처리해야 합니다."
```

#### 3. 마이그레이션 및 전환
- MySQL → PostgreSQL 전환 계획
- 모놀리식 → 마이크로서비스 DB 분리
- 온프레미스 → 클라우드 이전
- 샤딩 또는 복제 구성

**예시 질문**:
```
"MySQL 5.7에서 PostgreSQL 16으로 마이그레이션하려고 합니다.
주의사항과 단계별 계획을 알려주세요."
```

#### 4. 보안 및 규정 준수
- 한국 개인정보보호법 준수 방안
- 전자금융거래법 요구사항 충족
- SQL Injection 방지
- 암호화 및 접근 제어 설정

**예시 질문**:
```
"개인정보보호법에 따라 고유식별정보를 암호화해야 합니다.
PostgreSQL에서 어떻게 구현하나요?"
```

#### 5. 대용량 데이터 처리
- 수억 건 이상의 데이터 관리
- 실시간 분석 쿼리 최적화
- 배치 처리 성능 개선
- 시계열 데이터 아키텍처

**예시 질문**:
```
"1억 건 이상의 로그 데이터를 저장하고 실시간 분석해야 합니다.
TimescaleDB vs InfluxDB 중 어떤 것이 적합한가요?"
```

### ❌ 이 스킬이 적합하지 않은 경우
- 단순 SQL 문법 질문 (공식 문서 참조)
- 프로그래밍 언어별 ORM 사용법 (별도 스킬 사용)
- 클라우드 서비스별 UI 조작 (공식 가이드 참조)
- 특정 DB 벤더의 최신 업데이트 정보 (웹 검색 권장)

---

## Core Capabilities

### 1. 쿼리 최적화 엔진

#### EXPLAIN 분석 및 해석
```sql
-- PostgreSQL 예시
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT o.order_id, c.name, SUM(oi.quantity * oi.price) AS total
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.created_at >= '2025-01-01'
GROUP BY o.order_id, c.name
HAVING SUM(oi.quantity * oi.price) > 1000000;
```

**분석 항목**:
- **Seq Scan vs Index Scan**: 전체 테이블 스캔인지 인덱스 사용인지
- **Cost**: 추정 비용 (startup cost, total cost)
- **Rows**: 예상 행 수 vs 실제 행 수
- **Buffers**: 공유 버퍼 사용량 (hit, read, written)
- **Planning Time vs Execution Time**: 계획 시간 vs 실행 시간

**최적화 전략**:
1. 인덱스 추가 (복합 인덱스, 부분 인덱스)
2. JOIN 순서 변경
3. 서브쿼리 → CTE 또는 JOIN으로 변경
4. 통계 정보 업데이트 (`ANALYZE`)

#### 인덱스 전략

| 인덱스 유형 | 사용 사례 | 데이터베이스 | 성능 특성 |
|------------|----------|-------------|----------|
| **B-tree** | 범위 검색, 정렬 | PostgreSQL, MySQL | 균형 잡힌 성능 |
| **Hash** | 동등 비교 (=) | PostgreSQL, Redis | 빠른 조회, 범위 불가 |
| **GIN** | 전문 검색, 배열, JSONB | PostgreSQL | 복잡한 검색, 느린 삽입 |
| **GiST** | 지리 정보, 범위 타입 | PostgreSQL | 범용 인덱스 프레임워크 |
| **BRIN** | 시계열, 순차 데이터 | PostgreSQL | 적은 공간, 대용량 |
| **Full-Text** | 자연어 검색 | MySQL, PostgreSQL | 텍스트 검색 최적화 |

**인덱스 설계 원칙**:
```
✅ DO:
- WHERE 절에 자주 사용되는 컬럼에 인덱스
- JOIN 키 컬럼에 인덱스
- ORDER BY, GROUP BY 컬럼에 인덱스
- 복합 인덱스는 선택도 높은 컬럼을 앞에 배치

❌ DON'T:
- 모든 컬럼에 무분별한 인덱스 (쓰기 성능 저하)
- 선택도 낮은 컬럼 인덱스 (Boolean 등)
- 자주 변경되는 컬럼에 과도한 인덱스
- 사용하지 않는 인덱스 유지 (공간 낭비)
```

---

### 2. 스키마 설계 및 정규화

#### 정규화 단계별 가이드

**제1정규형 (1NF)**: 원자성
```sql
-- ❌ 위반 사례
CREATE TABLE orders (
    order_id INT,
    product_names TEXT  -- "상품A,상품B,상품C" (반복 그룹)
);

-- ✅ 올바른 설계
CREATE TABLE orders (
    order_id INT PRIMARY KEY
);

CREATE TABLE order_items (
    order_id INT REFERENCES orders(order_id),
    product_name VARCHAR(100),
    PRIMARY KEY (order_id, product_name)
);
```

**제2정규형 (2NF)**: 부분 종속 제거
```sql
-- ❌ 위반 사례 (order_id + product_id가 키인데 product_name은 product_id에만 종속)
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- ✅ 올바른 설계
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT REFERENCES products(product_id),
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);
```

**제3정규형 (3NF)**: 이행 종속 제거
```sql
-- ❌ 위반 사례 (customer_id → address → city, address와 city가 이행 종속)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    address VARCHAR(200),
    city VARCHAR(50)
);

-- ✅ 올바른 설계
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    address VARCHAR(200),
    city VARCHAR(50)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id)
);
```

**BCNF (Boyce-Codd 정규형)**: 모든 결정자가 후보키
```sql
-- ❌ 위반 사례 (instructor가 course를 결정하지만 instructor는 후보키가 아님)
CREATE TABLE courses (
    student_id INT,
    course_name VARCHAR(100),
    instructor VARCHAR(100),
    PRIMARY KEY (student_id, course_name)
);

-- ✅ 올바른 설계
CREATE TABLE instructors (
    course_name VARCHAR(100) PRIMARY KEY,
    instructor VARCHAR(100)
);

CREATE TABLE enrollments (
    student_id INT,
    course_name VARCHAR(100) REFERENCES instructors(course_name),
    PRIMARY KEY (student_id, course_name)
);
```

#### 비정규화 전략 (성능 최적화)

**언제 비정규화하는가**:
- 읽기 성능이 매우 중요한 경우
- JOIN 비용이 과도한 경우
- 집계 쿼리가 빈번한 경우
- 데이터 일관성보다 성능 우선인 경우

**비정규화 기법**:
```sql
-- 1. 계산된 컬럼 추가 (중복 허용)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    total_amount DECIMAL(10,2),  -- 실시간 계산 대신 저장
    item_count INT               -- order_items 테이블 집계값 저장
);

-- 2. 머티리얼라이즈드 뷰 (PostgreSQL)
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT 
    DATE(created_at) AS sale_date,
    SUM(total_amount) AS total_sales,
    COUNT(*) AS order_count
FROM orders
GROUP BY DATE(created_at);

-- 주기적 갱신
REFRESH MATERIALIZED VIEW daily_sales_summary;

-- 3. 파티셔닝 (시간 기반)
CREATE TABLE logs (
    log_id BIGSERIAL,
    created_at TIMESTAMP NOT NULL,
    message TEXT
) PARTITION BY RANGE (created_at);

CREATE TABLE logs_2025_01 PARTITION OF logs
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE logs_2025_02 PARTITION OF logs
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
```

---

### 3. 트랜잭션 및 동시성 제어

#### Isolation Level 비교

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read | 성능 | 사용 사례 |
|----------------|------------|---------------------|--------------|------|----------|
| **Read Uncommitted** | 발생 | 발생 | 발생 | 최고 | 로그 수집 (정확도 덜 중요) |
| **Read Committed** | 방지 | 발생 | 발생 | 높음 | 대부분의 애플리케이션 (기본값) |
| **Repeatable Read** | 방지 | 방지 | 발생 | 중간 | 리포트 생성, 일관된 읽기 필요 |
| **Serializable** | 방지 | 방지 | 방지 | 낮음 | 금융 거래, 재고 관리 |

#### 데드락 해결 전략

**데드락 예시**:
```sql
-- 트랜잭션 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- (대기...)
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- 트랜잭션 2 (동시 실행)
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE id = 2;
-- (대기...)
UPDATE accounts SET balance = balance + 50 WHERE id = 1;
COMMIT;

-- 결과: 데드락! 두 트랜잭션이 서로 상대방의 락을 기다림
```

**해결 방법**:
```sql
-- 1. 일관된 순서로 락 획득
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- 항상 ID 순서대로
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- 2. 타임아웃 설정
SET lock_timeout = '5s';

-- 3. 명시적 락 사용 (PostgreSQL)
BEGIN;
SELECT * FROM accounts WHERE id IN (1, 2) FOR UPDATE;  -- 먼저 모든 락 획득
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- 4. 낙관적 락 (애플리케이션 레벨)
UPDATE accounts 
SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = 10;  -- version이 변경되면 실패

-- 5. MySQL 데드락 감지 및 자동 롤백
-- MySQL은 자동으로 데드락을 감지하고 한 트랜잭션을 롤백
```

#### MVCC (Multi-Version Concurrency Control)

**PostgreSQL MVCC 동작**:
```sql
-- 트랜잭션 1: 데이터 읽기
BEGIN;
SELECT * FROM products WHERE id = 1;  -- version 1: price = 10000
-- (트랜잭션 유지)

-- 트랜잭션 2: 데이터 수정
BEGIN;
UPDATE products SET price = 12000 WHERE id = 1;  -- version 2 생성
COMMIT;

-- 트랜잭션 1: 다시 읽기
SELECT * FROM products WHERE id = 1;  -- 여전히 version 1: price = 10000
COMMIT;

-- MVCC 덕분에 읽기와 쓰기가 서로 블로킹하지 않음
```

**VACUUM 필요성**:
```sql
-- 오래된 버전 제거 (PostgreSQL)
VACUUM ANALYZE products;

-- 자동 VACUUM 설정 확인
SELECT * FROM pg_settings WHERE name LIKE 'autovacuum%';

-- 테이블별 VACUUM 통계
SELECT relname, last_vacuum, last_autovacuum, n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```

---

### 4. NoSQL 데이터베이스 가이드

#### MongoDB 스키마 설계

**Embedded vs Referenced**:
```javascript
// ✅ Embedded (1:Few, 빈번한 함께 조회)
{
  "_id": ObjectId("..."),
  "title": "MongoDB Best Practices",
  "author": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "comments": [
    { "user": "Alice", "text": "Great post!" },
    { "user": "Bob", "text": "Very helpful." }
  ]
}

// ✅ Referenced (1:Many, 독립적 조회)
// Posts 컬렉션
{
  "_id": ObjectId("..."),
  "title": "MongoDB Best Practices",
  "author_id": ObjectId("...")
}

// Users 컬렉션
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "email": "john@example.com"
}

// Comments 컬렉션
{
  "_id": ObjectId("..."),
  "post_id": ObjectId("..."),
  "user": "Alice",
  "text": "Great post!"
}
```

**인덱싱 전략**:
```javascript
// 1. 단일 필드 인덱스
db.users.createIndex({ email: 1 })

// 2. 복합 인덱스 (선택도 높은 필드 앞에)
db.orders.createIndex({ customer_id: 1, created_at: -1 })

// 3. 전문 검색 인덱스
db.articles.createIndex({ title: "text", content: "text" })

// 4. 지리 공간 인덱스
db.stores.createIndex({ location: "2dsphere" })

// 5. 부분 인덱스 (조건부)
db.orders.createIndex(
  { created_at: 1 },
  { partialFilterExpression: { status: "completed" } }
)
```

**Aggregation Pipeline**:
```javascript
db.orders.aggregate([
  // Stage 1: 필터링
  { $match: { created_at: { $gte: ISODate("2025-01-01") } } },
  
  // Stage 2: 조인
  { $lookup: {
      from: "customers",
      localField: "customer_id",
      foreignField: "_id",
      as: "customer"
  }},
  
  // Stage 3: 배열 언팩
  { $unwind: "$customer" },
  
  // Stage 4: 그룹화
  { $group: {
      _id: "$customer.city",
      total_sales: { $sum: "$total_amount" },
      order_count: { $sum: 1 }
  }},
  
  // Stage 5: 정렬
  { $sort: { total_sales: -1 } },
  
  // Stage 6: 제한
  { $limit: 10 }
])
```

#### Redis 사용 패턴

**1. 캐싱**:
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

# Cache-Aside 패턴
def get_user(user_id):
    # 1. 캐시 확인
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    
    # 2. DB 조회
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    
    # 3. 캐시 저장 (TTL 1시간)
    r.setex(f"user:{user_id}", 3600, json.dumps(user))
    
    return user
```

**2. 세션 저장**:
```python
# 세션 생성
session_id = "sess_abc123"
session_data = {
    "user_id": 42,
    "username": "john",
    "login_time": "2025-01-15T10:30:00"
}
r.setex(f"session:{session_id}", 1800, json.dumps(session_data))  # 30분 TTL

# 세션 조회
session = r.get(f"session:{session_id}")

# 세션 갱신
r.expire(f"session:{session_id}", 1800)
```

**3. Rate Limiting**:
```python
def is_rate_limited(user_id, limit=100, window=60):
    """1분 동안 최대 100회 요청 허용"""
    key = f"rate:{user_id}"
    
    # 현재 카운트 조회
    count = r.incr(key)
    
    # 첫 요청이면 TTL 설정
    if count == 1:
        r.expire(key, window)
    
    return count > limit
```

**4. 리더보드 (Sorted Set)**:
```python
# 점수 추가/업데이트
r.zadd("leaderboard", {"player1": 1000, "player2": 1500})

# 상위 10명 조회
top_players = r.zrevrange("leaderboard", 0, 9, withscores=True)
# [('player2', 1500.0), ('player1', 1000.0)]

# 특정 플레이어 순위 조회
rank = r.zrevrank("leaderboard", "player1")  # 0-based index
```

---

### 5. 보안 및 규정 준수

#### SQL Injection 방지

```python
# ❌ 취약한 코드 (절대 금지!)
user_input = request.GET['username']
query = f"SELECT * FROM users WHERE username = '{user_input}'"
cursor.execute(query)

# 공격 시나리오: user_input = "admin' OR '1'='1"
# 결과: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# → 모든 사용자 정보 노출!

# ✅ 안전한 코드 (파라미터화된 쿼리)
user_input = request.GET['username']
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (user_input,))

# ✅ ORM 사용 (권장)
from sqlalchemy import select
stmt = select(User).where(User.username == user_input)
result = session.execute(stmt)
```

#### 한국 개인정보보호법 준수

**고유식별정보 암호화 (필수)**:
```sql
-- PostgreSQL pgcrypto 확장 사용
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 암호화하여 저장
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    resident_number BYTEA  -- 주민등록번호 암호화
);

-- 데이터 삽입
INSERT INTO users (name, resident_number)
VALUES ('홍길동', pgp_sym_encrypt('901231-1234567', 'encryption_key'));

-- 데이터 조회
SELECT 
    name,
    pgp_sym_decrypt(resident_number, 'encryption_key') AS resident_number
FROM users;

-- ✅ 권장: 환경 변수로 키 관리, 키 로테이션 주기적 실시
```

**접근 로그 보관 (3년)**:
```sql
-- 접근 로그 테이블
CREATE TABLE access_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id INT,
    table_name VARCHAR(100),
    action VARCHAR(50),  -- SELECT, INSERT, UPDATE, DELETE
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET
);

-- 파티셔닝으로 관리 (연도별)
CREATE TABLE access_logs (
    log_id BIGSERIAL,
    user_id INT,
    table_name VARCHAR(100),
    action VARCHAR(50),
    accessed_at TIMESTAMP NOT NULL,
    ip_address INET
) PARTITION BY RANGE (accessed_at);

-- 연도별 파티션 생성
CREATE TABLE access_logs_2025 PARTITION OF access_logs
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE access_logs_2026 PARTITION OF access_logs
FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

**비밀번호 암호화 (단방향)**:
```python
import bcrypt

# ✅ 안전한 비밀번호 저장
password = "user_password_123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# DB 저장
INSERT INTO users (username, password_hash)
VALUES ('john', hashed)

# 로그인 시 검증
stored_hash = db.query("SELECT password_hash FROM users WHERE username = 'john'")
is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash)
```

---

### 6. 성능 튜닝 및 모니터링

#### PostgreSQL 주요 설정

```conf
# postgresql.conf 주요 파라미터

# 메모리 설정 (서버 RAM의 25%)
shared_buffers = 4GB

# 작업 메모리 (쿼리당, 동시 연결 수 고려)
work_mem = 64MB

# 유지보수 작업 메모리 (VACUUM, CREATE INDEX)
maintenance_work_mem = 1GB

# WAL 설정 (Write-Ahead Logging)
wal_buffers = 16MB
min_wal_size = 1GB
max_wal_size = 4GB

# 체크포인트 (데이터 안정성 vs 성능)
checkpoint_completion_target = 0.9
checkpoint_timeout = 15min

# 연결 풀링
max_connections = 200

# 쿼리 플래너
effective_cache_size = 12GB  # OS 캐시 포함 총 메모리의 50-75%
random_page_cost = 1.1  # SSD일 경우 기본 4.0에서 낮춤

# 로깅 (느린 쿼리 추적)
log_min_duration_statement = 1000  # 1초 이상 쿼리 로깅
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
```

#### 모니터링 쿼리

```sql
-- 1. 느린 쿼리 상위 10개 (pg_stat_statements 확장 필요)
SELECT 
    query,
    calls,
    total_exec_time / 1000 AS total_sec,
    mean_exec_time / 1000 AS mean_sec,
    max_exec_time / 1000 AS max_sec
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- 2. 테이블별 캐시 히트율
SELECT 
    schemaname,
    relname,
    heap_blks_read,
    heap_blks_hit,
    ROUND(
        100.0 * heap_blks_hit / NULLIF(heap_blks_hit + heap_blks_read, 0),
        2
    ) AS cache_hit_ratio
FROM pg_statio_user_tables
ORDER BY heap_blks_read DESC
LIMIT 10;

-- 3. 인덱스 사용률
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- 사용되지 않는 인덱스
ORDER BY pg_relation_size(indexrelid) DESC;

-- 4. 블로킹 세션 (락 대기)
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- 5. 테이블별 VACUUM 필요성
SELECT 
    schemaname,
    relname,
    n_live_tup,
    n_dead_tup,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_ratio DESC;
```

---

## Usage Guide

### 빠른 시작

#### 1. 쿼리 최적화 요청
```
"PostgreSQL에서 다음 쿼리가 느립니다. 최적화해주세요:

SELECT c.name, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE c.created_at >= '2024-01-01'
GROUP BY c.name
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC;

테이블 크기:
- customers: 100만 행
- orders: 500만 행"
```

**예상 응답**:
- EXPLAIN ANALYZE 결과 분석
- 병목 구간 식별 (Seq Scan, 높은 Cost)
- 인덱스 추천 (`CREATE INDEX idx_customers_created ON customers(created_at)`)
- 최적화된 쿼리 제시

#### 2. 스키마 설계 요청
```
"블로그 플랫폼의 데이터베이스 스키마를 설계해주세요.

요구사항:
- 사용자 (회원가입, 로그인)
- 게시글 (제목, 내용, 작성일)
- 댓글 (계층형, 대댓글 지원)
- 태그 (게시글에 여러 태그 가능)
- 좋아요 (사용자가 게시글에 좋아요)

예상 트래픽:
- 일일 게시글: 1,000개
- 일일 댓글: 5,000개
- 동시 접속자: 1,000명"
```

**예상 응답**:
- ER 다이어그램
- 각 테이블 DDL (CREATE TABLE 문)
- 인덱스 전략
- 외래키 설정
- 정규화 수준 (3NF 권장)

#### 3. 마이그레이션 계획 요청
```
"MySQL 8.0에서 PostgreSQL 16으로 마이그레이션하려고 합니다.

현재 상황:
- DB 크기: 50GB
- 테이블 수: 80개
- 일일 쓰기: 100만 건
- 다운타임 허용: 최대 4시간

알려주세요:
1. 단계별 마이그레이션 계획
2. 주의사항 (MySQL vs PostgreSQL 차이)
3. 데이터 무결성 검증 방법"
```

#### 4. 보안 검토 요청
```
"금융 서비스를 개발 중입니다. 보안 체크리스트를 만들어주세요.

환경:
- PostgreSQL 16
- AWS RDS
- Django ORM

준수해야 할 규정:
- 전자금융거래법
- 개인정보보호법"
```

---

## Examples

### Example 1: 느린 쿼리 최적화

**시나리오**: 전자상거래 주문 현황 조회 쿼리가 15초 소요

**입력**:
```sql
-- 현재 쿼리 (PostgreSQL)
EXPLAIN ANALYZE
SELECT 
    p.product_name,
    c.category_name,
    COUNT(oi.order_id) AS total_orders,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.created_at BETWEEN '2024-01-01' AND '2024-12-31'
  AND o.status = 'completed'
GROUP BY p.product_name, c.category_name
ORDER BY total_revenue DESC
LIMIT 100;

-- 테이블 크기
-- products: 10,000 행
-- categories: 50 행
-- order_items: 5,000,000 행
-- orders: 2,000,000 행
```

**EXPLAIN ANALYZE 결과**:
```
Limit  (cost=850000.12..850000.37 rows=100 width=68) (actual time=15234.521..15234.612 rows=100 loops=1)
  ->  Sort  (cost=850000.12..850500.23 rows=200000 width=68) (actual time=15234.519..15234.565 rows=100 loops=1)
        Sort Key: (sum((oi.quantity * oi.price))) DESC
        Sort Method: top-N heapsort  Memory: 35kB
        ->  HashAggregate  (cost=800000.00..820000.00 rows=200000 width=68) (actual time=14500.234..15100.876 rows=9850 loops=1)
              ->  Hash Join  (cost=50000.00..750000.00 rows=1000000 width=40) (actual time=234.123..12345.678 rows=987654 loops=1)
                    Hash Cond: (oi.product_id = p.product_id)
                    ->  Hash Join  (cost=30000.00..650000.00 rows=1000000 width=24) (actual time=123.456..10234.567 rows=987654 loops=1)
                          Hash Cond: (oi.order_id = o.order_id)
                          ->  Seq Scan on order_items oi  (cost=0.00..150000.00 rows=5000000 width=24) (actual time=0.023..3456.789 rows=5000000 loops=1)
                          ->  Hash  (cost=25000.00..25000.00 rows=400000 width=8) (actual time=123.234..123.234 rows=456789 loops=1)
                                Buckets: 65536  Batches: 8  Memory Usage: 4567kB
                                ->  Seq Scan on orders o  (cost=0.00..25000.00 rows=400000 width=8) (actual time=0.012..89.123 rows=456789 loops=1)
                                      Filter: ((created_at >= '2024-01-01'::date) AND (created_at <= '2024-12-31'::date) AND (status = 'completed'::text))
                                      Rows Removed by Filter: 1543211
                    ->  Hash  (cost=15000.00..15000.00 rows=10000 width=24) (actual time=45.678..45.678 rows=10000 loops=1)
                          Buckets: 16384  Batches: 1  Memory Usage: 789kB
                          ->  Hash Join  (cost=1.25..15000.00 rows=10000 width=24) (actual time=0.034..34.567 rows=10000 loops=1)
                                Hash Cond: (p.category_id = c.category_id)
                                ->  Seq Scan on products p  (cost=0.00..250.00 rows=10000 width=20) (actual time=0.012..12.345 rows=10000 loops=1)
                                ->  Hash  (cost=1.00..1.00 rows=50 width=12) (actual time=0.018..0.018 rows=50 loops=1)
                                      Buckets: 1024  Batches: 1  Memory Usage: 10kB
                                      ->  Seq Scan on categories c  (cost=0.00..1.00 rows=50 width=12) (actual time=0.003..0.008 rows=50 loops=1)
Planning Time: 2.345 ms
Execution Time: 15234.789 ms
```

**분석**:
1. **병목 #1**: `Seq Scan on orders` - 200만 행 전체 스캔 (Filter로 154만 행 제거)
2. **병목 #2**: `Seq Scan on order_items` - 500만 행 전체 스캔
3. **병목 #3**: `HashAggregate` - 98만 행 집계

**최적화 전략**:

**1단계: 인덱스 생성**
```sql
-- orders 테이블에 복합 인덱스
CREATE INDEX idx_orders_completed ON orders(created_at, status) 
WHERE status = 'completed';

-- order_items 테이블에 복합 인덱스
CREATE INDEX idx_order_items_lookup ON order_items(order_id, product_id);

-- products 테이블에 인덱스 (이미 있을 가능성)
CREATE INDEX idx_products_category ON products(category_id);
```

**2단계: 쿼리 재작성**
```sql
-- 최적화된 쿼리
EXPLAIN ANALYZE
SELECT 
    p.product_name,
    c.category_name,
    COUNT(*) AS total_orders,
    SUM(oi.quantity * oi.price) AS total_revenue
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN categories c ON p.category_id = c.category_id
WHERE o.created_at BETWEEN '2024-01-01' AND '2024-12-31'
  AND o.status = 'completed'
GROUP BY p.product_id, p.product_name, c.category_name
ORDER BY total_revenue DESC
LIMIT 100;
```

**최적화 후 EXPLAIN ANALYZE** (예상):
```
Limit  (cost=12000.12..12000.37 rows=100 width=68) (actual time=450.123..450.234 rows=100 loops=1)
  ->  Sort  (cost=12000.12..12500.23 rows=200000 width=68) (actual time=450.121..450.178 rows=100 loops=1)
        Sort Key: (sum((oi.quantity * oi.price))) DESC
        Sort Method: top-N heapsort  Memory: 35kB
        ->  HashAggregate  (cost=10000.00..11000.00 rows=200000 width=68) (actual time=380.234..420.567 rows=9850 loops=1)
              ->  Hash Join  (cost=3000.00..8000.00 rows=1000000 width=40) (actual time=45.123..320.456 rows=987654 loops=1)
                    Hash Cond: (p.category_id = c.category_id)
                    ->  Hash Join  (cost=2998.75..7000.00 rows=1000000 width=32) (actual time=45.089..280.345 rows=987654 loops=1)
                          Hash Cond: (oi.product_id = p.product_id)
                          ->  Nested Loop  (cost=2748.75..5500.00 rows=1000000 width=24) (actual time=25.123..200.234 rows=987654 loops=1)
                                ->  Bitmap Heap Scan on orders o  (cost=2748.32..4500.00 rows=400000 width=8) (actual time=25.056..80.123 rows=456789 loops=1)
                                      Recheck Cond: ((created_at >= '2024-01-01'::date) AND (created_at <= '2024-12-31'::date) AND (status = 'completed'::text))
                                      Heap Blocks: exact=12345
                                      ->  Bitmap Index Scan on idx_orders_completed  (cost=0.00..2648.32 rows=400000 width=0) (actual time=20.123..20.123 rows=456789 loops=1)
                                            Index Cond: ((created_at >= '2024-01-01'::date) AND (created_at <= '2024-12-31'::date) AND (status = 'completed'::text))
                                ->  Index Scan using idx_order_items_lookup on order_items oi  (cost=0.43..1.50 rows=2 width=24) (actual time=0.001..0.001 rows=2 loops=456789)
                                      Index Cond: (order_id = o.order_id)
                          ->  Hash  (cost=250.00..250.00 rows=10000 width=20) (actual time=19.890..19.890 rows=10000 loops=1)
                                Buckets: 16384  Batches: 1  Memory Usage: 789kB
                                ->  Seq Scan on products p  (cost=0.00..250.00 rows=10000 width=20) (actual time=0.012..12.345 rows=10000 loops=1)
                    ->  Hash  (cost=1.00..1.00 rows=50 width=12) (actual time=0.018..0.018 rows=50 loops=1)
                          Buckets: 1024  Batches: 1  Memory Usage: 10kB
                          ->  Seq Scan on categories c  (cost=0.00..1.00 rows=50 width=12) (actual time=0.003..0.008 rows=50 loops=1)
Planning Time: 2.123 ms
Execution Time: 450.456 ms  -- 15초 → 0.45초로 개선! (33배 향상)
```

**결과**:
- **실행 시간**: 15,234ms → 450ms (97% 감소, 33배 향상)
- **읽은 행 수**: 750만 행 → 146만 행 (81% 감소)
- **인덱스 스캔**: Seq Scan → Index Scan 전환
- **메모리 사용**: 일부 증가 (Hash Join), 하지만 디스크 I/O 대폭 감소

---

### Example 2: 전자상거래 데이터베이스 설계

**시나리오**: 중소형 전자상거래 플랫폼 (일일 주문 1만 건, 상품 10만 개)

**요구사항**:
- 회원 관리 (일반/기업 회원, SNS 로그인)
- 상품 관리 (카테고리, 옵션, 재고)
- 주문 처리 (장바구니, 결제, 배송)
- 리뷰 및 평점
- 쿠폰 및 프로모션

**설계 결과**:

```sql
-- 1. 회원 관리
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    user_type VARCHAR(20) DEFAULT 'individual' CHECK (user_type IN ('individual', 'business')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_addresses (
    address_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    address_type VARCHAR(20) CHECK (address_type IN ('shipping', 'billing')),
    recipient_name VARCHAR(100),
    phone VARCHAR(20),
    postal_code VARCHAR(10),
    address_line1 VARCHAR(200),
    address_line2 VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_addresses_user ON user_addresses(user_id);

-- 2. 상품 관리
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    parent_category_id INT REFERENCES categories(category_id),
    category_name VARCHAR(100) NOT NULL,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(category_id),
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = TRUE;

CREATE TABLE product_options (
    option_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    option_name VARCHAR(50) NOT NULL,  -- 색상, 사이즈 등
    option_value VARCHAR(50) NOT NULL,  -- 빨강, L 등
    price_adjustment DECIMAL(10,2) DEFAULT 0,
    stock_quantity INT DEFAULT 0,
    UNIQUE (product_id, option_name, option_value)
);

CREATE INDEX idx_product_options_product ON product_options(product_id);

-- 3. 주문 처리
CREATE TABLE carts (
    cart_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INT REFERENCES carts(cart_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    option_id INT REFERENCES product_options(option_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    order_status VARCHAR(20) DEFAULT 'pending' 
        CHECK (order_status IN ('pending', 'paid', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_fee DECIMAL(10,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    final_amount DECIMAL(10,2) NOT NULL,
    shipping_address_id INT REFERENCES user_addresses(address_id),
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending'
        CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_created ON orders(created_at);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES products(product_id),
    option_id INT REFERENCES product_options(option_id),
    product_name VARCHAR(200),  -- 스냅샷 (상품 정보 변경 시 주문 기록 보존)
    option_name VARCHAR(50),
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    subtotal DECIMAL(10,2) NOT NULL
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- 4. 리뷰 및 평점
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    order_item_id INT REFERENCES order_items(order_item_id),
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title VARCHAR(200),
    content TEXT,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (order_item_id)  -- 주문 항목당 1개 리뷰만
);

CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);

-- 5. 쿠폰 및 프로모션
CREATE TABLE coupons (
    coupon_id SERIAL PRIMARY KEY,
    coupon_code VARCHAR(50) UNIQUE NOT NULL,
    discount_type VARCHAR(20) CHECK (discount_type IN ('percentage', 'fixed_amount')),
    discount_value DECIMAL(10,2) NOT NULL,
    min_purchase_amount DECIMAL(10,2) DEFAULT 0,
    max_discount_amount DECIMAL(10,2),
    usage_limit INT,
    usage_count INT DEFAULT 0,
    valid_from TIMESTAMP,
    valid_until TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE user_coupons (
    user_coupon_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    coupon_id INT REFERENCES coupons(coupon_id),
    used_at TIMESTAMP,
    order_id INT REFERENCES orders(order_id),
    UNIQUE (user_id, coupon_id)
);

-- 6. 통계 및 집계 (머티리얼라이즈드 뷰)
CREATE MATERIALIZED VIEW product_stats AS
SELECT 
    p.product_id,
    p.product_name,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue,
    AVG(r.rating) AS avg_rating,
    COUNT(r.review_id) AS review_count
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.product_name;

CREATE UNIQUE INDEX idx_product_stats_id ON product_stats(product_id);

-- 주기적 갱신 (예: 매일 자정)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY product_stats;
```

**인덱싱 전략 요약**:
- **외래키 인덱스**: 모든 외래키 컬럼 (JOIN 최적화)
- **검색 조건 인덱스**: `order_status`, `is_active` (WHERE 절 빈번)
- **시간 기반 인덱스**: `created_at` (날짜 범위 쿼리)
- **부분 인덱스**: `is_active = TRUE` (활성 상품만)
- **고유 인덱스**: `email`, `order_number` (중복 방지)

**성능 예상**:
- 주문 조회: < 50ms (인덱스 사용)
- 상품 검색: < 100ms (카테고리 + 전문 검색)
- 리뷰 조회: < 30ms (product_id 인덱스)
- 통계 조회: < 10ms (머티리얼라이즈드 뷰)

---

### Example 3: MongoDB 샤딩 설계 (대용량 로그 시스템)

**시나리오**: IoT 센서 로그 저장 (1일 1억 건, 보관 기간 1년)

**요구사항**:
- 초당 1,000건 이상 삽입
- 센서별/날짜별 조회 빈번
- 데이터 크기: 연간 약 5TB
- 고가용성 (24/7 운영)

**설계 결과**:

```javascript
// 1. 샤드 키 선택
// sensor_id + timestamp 복합 키 (시간 기반 + 해시 분산)

// 컬렉션 정의
db.createCollection("sensor_logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sensor_id", "timestamp", "value"],
      properties: {
        sensor_id: { bsonType: "string" },
        timestamp: { bsonType: "date" },
        sensor_type: { bsonType: "string", enum: ["temperature", "humidity", "pressure"] },
        value: { bsonType: "double" },
        location: {
          bsonType: "object",
          properties: {
            type: { enum: ["Point"] },
            coordinates: { bsonType: "array" }
          }
        },
        metadata: { bsonType: "object" }
      }
    }
  }
})

// 2. 샤딩 활성화
sh.enableSharding("iot_database")

// 3. 샤드 키 설정 (해시 샤딩 - 균등 분산)
sh.shardCollection(
  "iot_database.sensor_logs",
  { sensor_id: "hashed", timestamp: 1 }
)

// 4. 인덱스 생성
db.sensor_logs.createIndex({ sensor_id: 1, timestamp: -1 })  // 센서별 시간 순 조회
db.sensor_logs.createIndex({ sensor_type: 1, timestamp: -1 })  // 타입별 조회
db.sensor_logs.createIndex({ "location": "2dsphere" })  // 지리 쿼리
db.sensor_logs.createIndex({ timestamp: 1 }, { expireAfterSeconds: 31536000 })  // TTL 1년

// 5. 쓰기 관심사 (Write Concern) 설정
db.sensor_logs.insert(
  { /* 문서 */ },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)

// 6. 읽기 선호도 (Read Preference) 설정
db.sensor_logs.find({ sensor_id: "sensor_001" })
  .readPref("secondaryPreferred")  // 복제본 읽기 우선, 없으면 Primary
```

**샤딩 아키�ekstur**:
```
Client
  ↓
mongos (쿼리 라우터)
  ↓
Config Servers (샤드 메타데이터)
  ↓
Shard 1 (센서 1-1000)   Shard 2 (센서 1001-2000)   Shard 3 (센서 2001-3000)
   ↓                        ↓                          ↓
Primary + 2 Secondaries  Primary + 2 Secondaries    Primary + 2 Secondaries
```

**쿼리 예시**:

```javascript
// 1. 특정 센서의 최근 1시간 데이터 (샤드 키 포함, 단일 샤드 조회)
db.sensor_logs.find({
  sensor_id: "sensor_001",
  timestamp: { $gte: ISODate("2025-01-15T09:00:00Z") }
}).sort({ timestamp: -1 })

// 2. 전체 센서 평균값 (모든 샤드 조회, 병렬 처리)
db.sensor_logs.aggregate([
  { $match: { timestamp: { $gte: ISODate("2025-01-15T00:00:00Z") } } },
  { $group: {
      _id: "$sensor_type",
      avg_value: { $avg: "$value" },
      count: { $sum: 1 }
  }}
])

// 3. 지리 기반 쿼리 (특정 지역 내 센서)
db.sensor_logs.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [127.0276, 37.4979] },  // 서울
      $maxDistance: 5000  // 5km 반경
    }
  },
  timestamp: { $gte: ISODate("2025-01-15T00:00:00Z") }
})

// 4. 배치 삽입 (성능 최적화)
db.sensor_logs.insertMany([
  { sensor_id: "sensor_001", timestamp: ISODate(), value: 25.3, sensor_type: "temperature" },
  { sensor_id: "sensor_002", timestamp: ISODate(), value: 60.1, sensor_type: "humidity" },
  // ... 1000개 배치
], { ordered: false })  // 순서 무관, 병렬 처리
```

**성능 모니터링**:
```javascript
// 샤드 분산 확인
db.sensor_logs.getShardDistribution()

// 청크 분포 확인
sh.status()

// 현재 실행 중인 쿼리
db.currentOp()

// 느린 쿼리 로그
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(5)
```

**결과**:
- **삽입 속도**: 평균 2,000 docs/sec (배치 삽입 시 10,000+)
- **조회 속도**: < 50ms (샤드 키 포함), < 500ms (전체 샤드)
- **저장 공간**: 샤드당 약 1.7TB (3개 샤드 = 5TB)
- **고가용성**: 각 샤드 3-복제본 (Primary + 2 Secondary)

---

## Best Practices

### 데이터베이스 선택 가이드

| 사용 사례 | 권장 DB | 이유 |
|----------|---------|------|
| **OLTP** (은행, 전자상거래) | PostgreSQL, MySQL | ACID 보장, 트랜잭션 안정성 |
| **대용량 읽기** (SNS 피드) | Redis (캐시) + MySQL | 읽기 부하 분산 |
| **문서 저장** (CMS, 블로그) | MongoDB | 유연한 스키마, JSON 친화적 |
| **실시간 분석** (대시보드) | TimescaleDB, InfluxDB | 시계열 최적화 |
| **세션 저장** (로그인) | Redis | 빠른 메모리 액세스 |
| **지리 정보** (배달 앱) | PostgreSQL (PostGIS) | GIS 기능 |
| **그래프 관계** (SNS 친구) | Neo4j | 관계 탐색 최적화 |
| **검색 엔진** (상품 검색) | Elasticsearch | 전문 검색, 자동완성 |
| **분산 SQL** (글로벌 서비스) | CockroachDB, TiDB | 지역 간 복제, 확장성 |

### ✅ DO

#### 1. 인덱스 전략
```sql
-- ✅ 복합 인덱스는 선택도 높은 컬럼을 앞에
CREATE INDEX idx_orders_lookup ON orders(user_id, created_at);

-- ✅ 부분 인덱스로 공간 절약
CREATE INDEX idx_active_products ON products(product_id) WHERE is_active = TRUE;

-- ✅ 커버링 인덱스 (Index Only Scan)
CREATE INDEX idx_orders_covering ON orders(user_id, created_at) INCLUDE (total_amount);
```

#### 2. 쿼리 최적화
```sql
-- ✅ EXISTS 사용 (서브쿼리 최적화)
SELECT * FROM products p
WHERE EXISTS (
    SELECT 1 FROM order_items oi 
    WHERE oi.product_id = p.product_id
);

-- ✅ LIMIT으로 불필요한 데이터 조회 방지
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;

-- ✅ 집계 쿼리는 인덱스 활용
SELECT user_id, COUNT(*) FROM orders
WHERE created_at >= '2025-01-01'
GROUP BY user_id;
```

#### 3. 트랜잭션 관리
```python
# ✅ 짧은 트랜잭션 유지
with conn.cursor() as cur:
    cur.execute("BEGIN")
    cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    cur.execute("COMMIT")

# ✅ 타임아웃 설정
cur.execute("SET statement_timeout = '5s'")
```

#### 4. 연결 풀링
```python
# ✅ 연결 풀 사용 (psycopg2)
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=5,
    maxconn=20,
    host='localhost',
    database='mydb'
)

conn = connection_pool.getconn()
# ... 쿼리 실행
connection_pool.putconn(conn)
```

#### 5. 보안
```python
# ✅ 파라미터화된 쿼리
cur.execute("SELECT * FROM users WHERE email = %s", (user_email,))

# ✅ 최소 권한 원칙
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE ON TABLE orders TO app_user;
-- DELETE 권한은 부여하지 않음
```

---

### ❌ DON'T

#### 1. 안티패턴
```sql
-- ❌ SELECT * (불필요한 컬럼 조회)
SELECT * FROM orders;  -- 100개 컬럼 중 3개만 필요한데...

-- ✅ 필요한 컬럼만 명시
SELECT order_id, total_amount, created_at FROM orders;

-- ❌ OR 대신 IN 사용 권장
SELECT * FROM products WHERE category_id = 1 OR category_id = 2 OR category_id = 3;

-- ✅ IN 사용 (인덱스 활용 가능)
SELECT * FROM products WHERE category_id IN (1, 2, 3);

-- ❌ LIKE 앞에 와일드카드 (인덱스 사용 불가)
SELECT * FROM products WHERE product_name LIKE '%카메라%';

-- ✅ 전문 검색 인덱스 사용
SELECT * FROM products WHERE to_tsvector('korean', product_name) @@ to_tsquery('korean', '카메라');
```

#### 2. 트랜잭션 오용
```python
# ❌ 긴 트랜잭션 (락 유지 시간 증가)
cur.execute("BEGIN")
cur.execute("SELECT * FROM orders")  # 100만 행 조회
time.sleep(10)  # 외부 API 호출
cur.execute("UPDATE orders SET status = 'processed'")
cur.execute("COMMIT")

# ✅ 트랜잭션 분리
data = cur.execute("SELECT * FROM orders").fetchall()
processed_data = call_external_api(data)  # 트랜잭션 밖에서 실행

cur.execute("BEGIN")
cur.execute("UPDATE orders SET status = 'processed'")
cur.execute("COMMIT")
```

#### 3. N+1 문제
```python
# ❌ N+1 쿼리 (1 + N번 쿼리)
orders = cur.execute("SELECT * FROM orders").fetchall()
for order in orders:
    customer = cur.execute("SELECT * FROM customers WHERE id = %s", (order['customer_id'],)).fetchone()

# ✅ JOIN 사용 (1번 쿼리)
result = cur.execute("""
    SELECT o.*, c.name, c.email
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
""").fetchall()
```

#### 4. 인덱스 오용
```sql
-- ❌ 함수 사용 (인덱스 무효화)
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';

-- ✅ 함수 기반 인덱스 또는 데이터 정규화
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- 또는
SELECT * FROM users WHERE email = 'john@example.com';  -- 데이터를 소문자로 저장
```

#### 5. 보안 취약점
```python
# ❌ SQL Injection 취약
query = f"SELECT * FROM users WHERE username = '{user_input}'"
cur.execute(query)

# ✅ 파라미터화된 쿼리
query = "SELECT * FROM users WHERE username = %s"
cur.execute(query, (user_input,))
```

---

## Troubleshooting

### Issue 1: 쿼리 응답 시간 느림 (> 1초)

**증상**:
- 특정 쿼리가 일관되게 1초 이상 소요
- 사용자 페이지 로딩 지연

**진단 단계**:
```sql
-- 1. EXPLAIN ANALYZE 실행
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT * FROM orders WHERE user_id = 123;

-- 2. 실행 계획 확인
-- - Seq Scan인지 Index Scan인지
-- - Cost 값이 높은 부분
-- - Actual Time vs Estimated Rows 차이

-- 3. 인덱스 존재 확인
SELECT * FROM pg_indexes WHERE tablename = 'orders';

-- 4. 통계 정보 업데이트 여부
SELECT last_analyze FROM pg_stat_user_tables WHERE relname = 'orders';
```

**해결 방법**:
```sql
-- A. 인덱스 추가
CREATE INDEX idx_orders_user ON orders(user_id);

-- B. 통계 정보 업데이트
ANALYZE orders;

-- C. 쿼리 재작성 (필요 시)
-- 서브쿼리 → JOIN 변경
-- OR → IN 변경
```

**예방**:
- 정기적 ANALYZE 실행 (Autovacuum 활성화)
- 슬로우 쿼리 로그 모니터링
- 인덱스 사용률 주기적 검토

---

### Issue 2: 데드락 발생

**증상**:
```
ERROR: deadlock detected
DETAIL: Process 12345 waits for ShareLock on transaction 67890
Process 67890 waits for ShareLock on transaction 12345
```

**진단 단계**:
```sql
-- 1. 데드락 로그 확인
SELECT * FROM pg_stat_database WHERE datname = 'mydb';

-- 2. 현재 락 상황 조회
SELECT 
    locktype, relation::regclass, mode, granted, pid
FROM pg_locks
WHERE NOT granted
ORDER BY pid;

-- 3. 블로킹 세션 확인
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocking_locks.pid AS blocking_pid,
    blocked_activity.query AS blocked_query,
    blocking_activity.query AS blocking_query
FROM pg_locks blocked_locks
JOIN pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted AND blocking_locks.granted;
```

**해결 방법**:
```sql
-- A. 일관된 락 순서 (애플리케이션 레벨)
-- 항상 ID 순서대로 락 획득
BEGIN;
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- B. 타임아웃 설정
SET lock_timeout = '5s';
SET statement_timeout = '10s';

-- C. Isolation Level 낮춤 (신중히)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

**예방**:
- 트랜잭션 최소화 (짧게 유지)
- 일관된 락 순서 유지
- 필요한 경우에만 FOR UPDATE 사용

---

### Issue 3: 높은 CPU 사용률 (> 80%)

**증상**:
- 데이터베이스 서버 CPU 사용률 지속적으로 높음
- 전체 시스템 성능 저하

**진단 단계**:
```sql
-- 1. 현재 실행 중인 쿼리 확인
SELECT pid, state, query, query_start
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;

-- 2. 장시간 실행 쿼리
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '5 minutes';

-- 3. CPU 사용량 높은 쿼리 (pg_stat_statements 필요)
SELECT 
    query,
    calls,
    total_exec_time / 1000 AS total_sec,
    mean_exec_time / 1000 AS mean_sec
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

**해결 방법**:
```sql
-- A. 비효율적 쿼리 종료
SELECT pg_terminate_backend(12345);  -- PID

-- B. 쿼리 최적화
-- EXPLAIN ANALYZE로 분석 → 인덱스 추가

-- C. 연결 제한 (Connection Pooling)
ALTER SYSTEM SET max_connections = 100;
SELECT pg_reload_conf();
```

**예방**:
- 연결 풀 사용 (PgBouncer, pgPool)
- 슬로우 쿼리 정기 점검
- 리소스 모니터링 (Prometheus + Grafana)

---

### Issue 4: 디스크 공간 부족

**증상**:
```
ERROR: could not extend file "base/16384/12345": No space left on device
```

**진단 단계**:
```sql
-- 1. 데이터베이스별 크기
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;

-- 2. 테이블별 크기
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- 3. 인덱스 크기
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 10;

-- 4. Bloat 확인 (오래된 버전)
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    n_dead_tup,
    ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY n_dead_tup DESC;
```

**해결 방법**:
```sql
-- A. VACUUM 실행 (공간 회수)
VACUUM FULL orders;  -- 주의: 테이블 락 발생, 다운타임 필요

-- 또는
VACUUM ANALYZE orders;  -- 락 없음, 점진적 회수

-- B. 오래된 데이터 아카이브
CREATE TABLE orders_2024_archive AS 
SELECT * FROM orders WHERE created_at < '2024-01-01';

DELETE FROM orders WHERE created_at < '2024-01-01';

VACUUM FULL orders;

-- C. 파티셔닝 (자동 정리)
-- 오래된 파티션 DROP으로 즉시 공간 회수

-- D. 사용하지 않는 인덱스 삭제
DROP INDEX idx_unused_index;
```

**예방**:
- Autovacuum 활성화 및 튜닝
- 파티셔닝으로 데이터 관리
- 정기적 아카이브 정책
- 디스크 사용률 모니터링

---

### Issue 5: 연결 거부 (Too Many Connections)

**증상**:
```
FATAL: remaining connection slots are reserved for non-replication superuser connections
FATAL: sorry, too many clients already
```

**진단 단계**:
```sql
-- 1. 현재 연결 수
SELECT count(*) FROM pg_stat_activity;

-- 2. 최대 연결 수 확인
SHOW max_connections;

-- 3. 데이터베이스별 연결 수
SELECT datname, count(*) 
FROM pg_stat_activity 
GROUP BY datname 
ORDER BY count(*) DESC;

-- 4. 유휴 연결 확인
SELECT pid, state, state_change, query_start
FROM pg_stat_activity
WHERE state = 'idle'
ORDER BY state_change;
```

**해결 방법**:
```sql
-- A. 유휴 연결 종료
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle' AND now() - state_change > interval '10 minutes';

-- B. max_connections 증가 (임시 조치)
ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();
-- 주의: 재시작 필요

-- C. 연결 풀링 도입 (근본 해결)
-- PgBouncer 설정
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = md5
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

**예방**:
- 애플리케이션에서 연결 풀 사용
- PgBouncer 또는 pgPool 도입
- 연결 타임아웃 설정
- 모니터링 알림 설정

---

## Security Guidelines

### 한국 법규 준수 체크리스트

#### 개인정보보호법
- [ ] **암호화**: 고유식별정보(주민번호, 여권번호 등) 암호화 저장
- [ ] **접근 제어**: 개인정보 처리 시스템 접근 권한 최소화
- [ ] **로그 보관**: 접근 기록 3년 이상 보관
- [ ] **비밀번호**: 단방향 암호화 (bcrypt, scrypt)
- [ ] **전송 암호화**: TLS/SSL 사용
- [ ] **백업 암호화**: 백업 데이터도 암호화

```sql
-- 암호화 컬럼 예시
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    resident_number BYTEA,  -- 암호화 저장
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 암호화 저장
INSERT INTO users (name, resident_number)
VALUES ('홍길동', pgp_sym_encrypt('901231-1234567', current_setting('app.encryption_key')));

-- 복호화 조회 (권한 있는 사용자만)
SELECT name, pgp_sym_decrypt(resident_number, current_setting('app.encryption_key'))
FROM users
WHERE user_id = 123;
```

#### 전자금융거래법
- [ ] **트랜잭션 무결성**: ACID 보장
- [ ] **백업 주기**: 일일 백업 + 실시간 복제
- [ ] **복구 시간**: RTO < 4시간, RPO < 1시간
- [ ] **감사 로그**: 모든 금융 거래 기록 보관

```sql
-- 금융 거래 로그 테이블
CREATE TABLE transaction_logs (
    log_id BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    user_id INT,
    transaction_type VARCHAR(50),
    amount DECIMAL(15,2),
    status VARCHAR(20),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_amount CHECK (amount >= 0)
);

-- 파티셔닝으로 관리
CREATE TABLE transaction_logs (
    log_id BIGSERIAL,
    transaction_id VARCHAR(50) NOT NULL,
    -- ... 기타 컬럼
    created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

-- 월별 파티션
CREATE TABLE transaction_logs_2025_01 PARTITION OF transaction_logs
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

---

## Performance Benchmarks

### PostgreSQL 벤치마크 (TPC-C 기준)

| 하드웨어 | Connections | TPS | 평균 응답 시간 |
|----------|-------------|-----|---------------|
| 4 vCPU, 16GB RAM, SSD | 50 | 1,200 | 15ms |
| 8 vCPU, 32GB RAM, SSD | 100 | 3,500 | 12ms |
| 16 vCPU, 64GB RAM, NVMe | 200 | 8,000 | 8ms |

### MongoDB 벤치마크 (YCSB 기준)

| 워크로드 | 읽기 | 쓰기 | 처리량 (ops/sec) |
|---------|------|------|-----------------|
| Read-Heavy | 95% | 5% | 15,000 |
| Balanced | 50% | 50% | 8,000 |
| Write-Heavy | 5% | 95% | 5,500 |

### Redis 벤치마크

| 명령어 | QPS | 평균 레이턴시 |
|--------|-----|-------------|
| GET | 100,000 | 0.2ms |
| SET | 80,000 | 0.3ms |
| INCR | 100,000 | 0.2ms |
| LPUSH | 70,000 | 0.4ms |

---

## Migration Guides

### MySQL → PostgreSQL

**호환성 이슈**:
```sql
-- 1. AUTO_INCREMENT → SERIAL
-- MySQL
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY
);

-- PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY
);

-- 2. 날짜 함수
-- MySQL: NOW()
-- PostgreSQL: CURRENT_TIMESTAMP

-- 3. 문자열 연결
-- MySQL: CONCAT(a, b)
-- PostgreSQL: a || b

-- 4. LIMIT OFFSET
-- MySQL: LIMIT 10 OFFSET 20
-- PostgreSQL: LIMIT 10 OFFSET 20 (동일, 하지만 FETCH FIRST 권장)

-- 5. 대소문자 구분
-- MySQL: 기본적으로 대소문자 무시 (collation 의존)
-- PostgreSQL: 대소문자 구분 (ILIKE 사용)
```

**마이그레이션 도구**:
```bash
# pgLoader 사용
apt-get install pgloader

# MySQL → PostgreSQL 마이그레이션
pgloader mysql://user:pass@localhost/mydb postgresql://user:pass@localhost/mydb

# 스키마만 마이그레이션
pgloader --schema-only mysql://... postgresql://...

# 데이터 검증
SELECT COUNT(*) FROM users;  -- MySQL
SELECT COUNT(*) FROM users;  -- PostgreSQL
```

**마이그레이션 체크리스트**:
- [ ] 스키마 변환 (DDL 문법 차이)
- [ ] 데이터 타입 매핑 (DATETIME → TIMESTAMP)
- [ ] 인덱스 재생성
- [ ] 트리거 및 프로시저 재작성
- [ ] 애플리케이션 코드 수정 (SQL 문법)
- [ ] 성능 테스트 (EXPLAIN 분석)
- [ ] 롤백 계획 수립

---

## Version History

### v1.0.0 (2025-01-15)
- 초기 릴리스
- PostgreSQL, MySQL, MongoDB, Redis 지원
- 쿼리 최적화, 스키마 설계, 보안 가이드 포함
- 한국 법규 준수 섹션 추가

### 향후 계획
- v1.1.0: Elasticsearch, ClickHouse 추가
- v1.2.0: 클라우드 DB (AWS RDS, Aurora) 최적화 가이드
- v1.3.0: 대화형 쿼리 분석 (자동 EXPLAIN)
- v2.0.0: 실시간 성능 모니터링 통합

---

## Additional Resources

### 공식 문서
- PostgreSQL 16: https://www.postgresql.org/docs/16/
- MySQL 8.0: https://dev.mysql.com/doc/refman/8.0/
- MongoDB 7.0: https://docs.mongodb.com/manual/
- Redis: https://redis.io/docs/

### 학습 자료
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Database Internals" by Alex Petrov
- CMU 15-445 (Database Systems): https://15445.courses.cs.cmu.edu/

### 한국 커뮤니티
- PostgreSQL 한국 사용자 모임: https://postgresql.kr
- MySQL 한국 사용자 모임: https://www.facebook.com/groups/mysqlkorea

### 벤치마크
- TPC-C (OLTP): http://www.tpc.org/tpcc/
- YCSB (NoSQL): https://github.com/brianfrankcooper/YCSB

---

## License
이 스킬은 MIT 라이선스 하에 배포됩니다.

## Support
문의: db-expert-skill@example.com

---

**마지막 업데이트**: 2025-01-15  
**작성자**: Claude Skills Generator  
**버전**: 1.0.0