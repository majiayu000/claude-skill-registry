---
name: db-schema-manager
description: |
  Manages all database table schemas for the AI Trading System. 
  Use when: creating tables, validating data before insert/update, 
  checking schema compatibility, generating migrations, or when user 
  mentions database schema, table structure, column definitions, 
  data validation, or schema mismatch.
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
---

# DB Schema Manager

**단일 진실의 소스(Single Source of Truth)**로 모든 DB 테이블 스키마를 관리합니다.

> ⚠️ **통합 참조 문서**: 모든 DB 작업 표준은 [`database_standards.md`](../../../../../../.gemini/antigravity/brain/c360bcf5-0a4d-48b1-b58b-0e2ef4000b25/database_standards.md)를 참조하세요.
> 
> db-schema-manager는 스키마 정의 및 검증을 담당하고, database_standards.md는 전체 DB 사용 규칙을 정의합니다.

## 🎯 핵심 기능

1. **스키마 정의**: 모든 테이블을 JSON으로 명확히 정의
2. **데이터 검증**: 삽입 전 스키마 준수 확인
3. **스키마 비교**: DB 실제 구조와 정의 비교
4. **마이그레이션**: SQL 마이그레이션 자동 생성

## 📚 관리 중인 테이블 (5개)

| 테이블 | 카테고리 | Repository | 용도 |
|--------|----------|-----------|------|
| stock_prices | 시계열 | StockRepository | 주가 OHLCV 데이터 |
| news_articles | 콘텐츠 | NewsRepository | 뉴스 기사 |
| trading_signals | 트레이딩 | SignalRepository | AI 매매 시그널 |
| data_collection_progress | 추적 | DataCollectionRepository | 백필 작업 추적 |
| dividend_aristocrats | 배당 | DividendRepository | 배당 귀족주 |

---

## 🤖 AI 개발 도구 통합

### 코드 작성 시 자동 검증

**VSCode / Antigravity / Claude**: DB 관련 코드를 작성하거나 검토할 때:

1. **새 테이블 추가 시**:
   ```bash
   # 1단계: 스키마 먼저 작성
   cat schemas/{table_name}.json
   
   # 2단계: 검증
   python scripts/validate_schema.py {table_name}
   
   # 3단계: SQL 생성
   python scripts/generate_migration.py {table_name}
   ```

2. **데이터 저장 전 검증**:
   ```bash
   python scripts/validate_data.py {table_name} '{...json_data...}'
   ```

3. **스키마 동기화 확인**:
   ```bash
   python scripts/compare_to_db.py {table_name}
   ```

### 필수 확인사항

✅ **코드 작성 전**:
- schemas/{table}.json 파일 존재 여부
- database_standards.md의 네이밍 규칙 준수
- **Repository 패턴 사용 여부** (`backend.database.repository` 확인)

❌ **절대 금지 (Zero Tolerance)**:
- **직접 SQL 작성 금지**: `SELECT`, `INSERT` 등 raw SQL 사용 적발 시 즉시 거부
- **Legacy Driver 사용 금지**: `psycopg2.connect()` / `asyncpg.connect()` 직접 호출 시 즉시 거부
- **스키마 우회 금지**: `models.py`에 정의되지 않은 컬럼 사용 금지
- **Repository 우회 금지**: `session` 객체를 직접 생성하여 사용하는 행위 금지 (`get_sync_session` 또는 Repository 활용)

---

## 🚀 Quick Start

### 스키마 확인
```bash
# 특정 테이블 스키마 보기
cat schemas/dividend_aristocrats.json

# 모든 테이블 나열
ls schemas/
```

### 데이터 검증 (삽입 전)
```bash
python scripts/validate_data.py dividend_aristocrats '{
  "ticker": "JNJ",
  "company_name": "Johnson & Johnson",
  "consecutive_years": 61,
  "sector": "Healthcare"
}'
```

**성공**: `✅ Validation passed`  
**실패**: 누락/잘못된 필드 나열

### DB와 스키마 비교
```bash
# 특정 테이블 비교
python scripts/compare_to_db.py dividend_aristocrats

# 모든 테이블 검사
python scripts/compare_to_db.py --all
```

---

## 📄 스키마 파일 형식

각 테이블은 `schemas/{table_name}.json` 파일로 정의됩니다:

```json
{
  "table_name": "dividend_aristocrats",
  "description": "배당 귀족주 (25+ 연속 배당 증가)",
  "primary_key": "ticker",
  "columns": [
    {
      "name": "ticker",
      "type": "VARCHAR(10)",
      "nullable": false,
      "description": "종목 코드",
      "example": "JNJ"
    },
    {
      "name": "company_name",
      "type": "VARCHAR(200)",
      "nullable": false,
      "description": "회사 이름"
    },
    {
      "name": "consecutive_years",
      "type": "INTEGER",
      "nullable": false,
      "description": "연속 배당 증가 연수"
    }
  ],
  "indexes": [
    {
      "name": "idx_aristocrat_ticker",
      "columns": ["ticker"],
      "unique": true
    }
  ],
  "metadata": {
    "phase": "Phase 21",
    "created": "2025-12-25",
    "update_frequency": "Annually (March 1)"
  }
}
```

---

## 📋 사용 패턴

### 1. 새 테이블 설계 확인
```bash
# 스키마 파일이 올바른지 검증
python scripts/validate_schema.py new_table

# 통과하면 마이그레이션 SQL 생성
python scripts/generate_migration.py new_table
```

### 2. 데이터 삽입 전 검증
**Why**: DB에 잘못된 데이터가 들어가는 것을 사전에 방지

```python
# Python 코드에서 사용 예시
import subprocess
import json

data = {
    "ticker": "JNJ",
    "company_name": "Johnson & Johnson",
    "consecutive_years": 61
}

# 검증 스크립트 실행
result = subprocess.run(
    ["python", "scripts/validate_data.py", "dividend_aristocrats", json.dumps(data)],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ Valid - proceed to insert")
    # db.insert(data)
else:
    print(f"❌ Invalid:\n{result.stdout}")
```

### 3. 스키마 불일치 발견
**Why**: 코드의 모델이 실제 DB와 다를 수 있음

```bash
# 모든 테이블 검사
python scripts/compare_to_db.py --all
```

**출력 예시**:
```
✅ dividend_aristocrats: Schema matches!
❌ news_articles: Schema mismatch!
  ❌ Missing columns in DB: {'sentiment_score'}
  ⚠️  Extra columns in DB: {'old_field'}
  ❌ Type mismatch for published_at: defined=TIMESTAMP, actual=DATE
```

---

## 🔍 스키마 탐색

### 모든 테이블 찾기
```bash
ls schemas/*.json | sed 's/schemas\///' | sed 's/.json//'
```

### 특정 컬럼을 가진 테이블 찾기
```bash
grep -l '"name": "ticker"' schemas/*.json
```

### 테이블 메타데이터 확인
```bash
# Phase 21에 속한 테이블 찾기
grep -l '"phase": "Phase 21"' schemas/*.json
```

---

## 🛠️ 스크립트 상세

### `scripts/validate_data.py`
**목적**: 데이터가 스키마를 만족하는지 검증

**사용**:
```bash
python scripts/validate_data.py <table_name> '<json_data>'
```

**예시**:
```bash
python scripts/validate_data.py dividend_aristocrats '{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "consecutive_years": 11
}'
```

**Pydantic 사용**: JSON 스키마 → Pydantic 모델 변환하여 타입 검증

### `scripts/compare_to_db.py`
**목적**: 정의된 스키마와 실제 DB 비교

**사용**:
```bash
python scripts/compare_to_db.py <table_name>
python scripts/compare_to_db.py --all
```

**확인 사항**:
- 누락된 컬럼
- 추가 컬럼 (정의에 없음)
- 타입 불일치
- Nullable 속성 차이

### `scripts/generate_migration.py`
**목적**: 스키마 정의에서 SQL 마이그레이션 생성

**사용**:
```bash
python scripts/generate_migration.py <table_name>
```

**출력**: `CREATE TABLE`, `CREATE INDEX` SQL

### `scripts/validate_schema.py`
**목적**: JSON 스키마 파일 자체가 올바른지 검증

**사용**:
```bash
python scripts/validate_schema.py <table_name>
```

**확인 사항**:
- 필수 필드 존재 (table_name, columns)
- 타입 유효성 (VARCHAR, INTEGER 등)
- Primary key 정의
- JSON 구문 오류

---

## 📚 추가 문서

- **전체 스키마 참조**: [docs/SCHEMA_REFERENCE.md](docs/SCHEMA_REFERENCE.md)
- **마이그레이션 가이드**: [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)

---

## 🎓 예제 시나리오

### Scenario 1: 새 테이블 추가
```
User: "DividendHistory 테이블을 추가하고 싶어"

Claude:
1. templates/new_table_template.json 복사
2. 사용자와 함께 스키마 정의
3. validate_schema.py로 검증
4. generate_migration.py로 SQL 생성
5. SQL 실행하여 테이블 생성
```

### Scenario 2: 데이터 검증 실패
```
User: "이 데이터를 dividend_aristocrats에 넣어줘"
Data: {"ticker": "AAPL", "consecutive_years": "invalid"}

Claude:
1. Read schemas/dividend_aristocrats.json
2. Run validate_data.py
3. 결과: ❌ Validation failed: consecutive_years must be integer
4. 사용자에게 수정 요청
```

### Scenario 3: 스키마 불일치 해결
```
User: "왜 DividendAristocrat 모델이 DB와 안 맞아?"

Claude:
1. Run compare_to_db.py dividend_aristocrats
2. 불일치 발견: Missing columns: payout_ratio, market_cap
3. 설명: "models.py가 구버전입니다. DB는 18개 컬럼, 모델은 11개"
4. 제안: "models.py를 schemas/dividend_aristocrats.json 기준으로 업데이트하시겠어요?"
```

---

## ⚡ 빠른 참조

| 명령어 | 용도 |
|--------|------|
| `cat schemas/<table>.json` | 스키마 확인 |
| `python scripts/validate_data.py <table> '<data>'` | 데이터 검증 |
| `python scripts/compare_to_db.py <table>` | DB 비교 |
| `python scripts/generate_migration.py <table>` | SQL 생성 |
| `ls schemas/*.json` | 모든 테이블 나열 |

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-25  
**Maintainer**: AI Trading System Team
