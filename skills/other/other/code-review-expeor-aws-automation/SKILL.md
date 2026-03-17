---
name: code-review
description: 코드 리뷰 체크리스트. PR 전 자체 검토용. 필수/권장/금지 항목 정리.
---

# Code Review Checklist

PR 제출 전 자체 코드 리뷰를 위한 체크리스트입니다.

---

## 필수 (Must Have)

머지 전 반드시 충족해야 하는 항목입니다.

### 멀티 계정 지원

- [ ] `parallel_collect` 패턴 사용
- [ ] `get_context_session()` 직접 호출 없음

```python
# 금지
session = ctx.provider.get_context_session()
client = session.client("ec2")

# 권장
from core.parallel import parallel_collect, get_client

def _collect(session, account_id, account_name, region):
    client = get_client(session, "ec2", region_name=region)
    ...

result = parallel_collect(ctx, _collect, service="ec2")
```

### 에러 핸들링

- [ ] `ClientError` 예외 처리
- [ ] `AccessDenied` 시 적절한 처리 (빈 결과 또는 로깅)
- [ ] `Throttling` 처리 (`get_client` 사용 시 자동)

```python
from botocore.exceptions import ClientError

try:
    response = client.describe_xxx()
except ClientError as e:
    if e.response["Error"]["Code"] == "AccessDenied":
        return []
    raise
```

### 타입 힌트

- [ ] 함수 파라미터 타입 힌트 완비
- [ ] 반환 타입 힌트 완비
- [ ] Python 3.10+ 스타일 (`list[str]` not `List[str]`)

```python
def analyze(resources: list[dict], region: str) -> list[dict]:
    ...
```

### 테스트

- [ ] 주요 함수에 테스트 존재
- [ ] 테스트 커버리지 80% 이상 권장
- [ ] 엣지 케이스 테스트 (빈 목록, None)
- [ ] 에러 케이스 테스트 (AccessDenied)

### 린트/타입 체크

- [ ] `ruff check` 통과
- [ ] `ruff format` 적용
- [ ] `mypy` 통과 (경고만 허용)

```bash
ruff check plugins/{service}/ --fix
ruff format plugins/{service}/
mypy plugins/{service}/
```

---

## 권장 (Should Have)

코드 품질 향상을 위해 권장하는 항목입니다.

### 함수 크기

- [ ] 함수당 50줄 이하
- [ ] 이상적으로 20줄 이하
- [ ] 한 가지 일만 수행

### 코드 복잡도

- [ ] if 중첩 3단계 이하
- [ ] 조기 반환 (early return) 활용
- [ ] guard clause 패턴 사용

```python
# 금지: 깊은 중첩
if condition1:
    if condition2:
        if condition3:
            do_something()

# 권장: 조기 반환
if not condition1:
    return
if not condition2:
    return
if not condition3:
    return
do_something()
```

### 명명 규칙

- [ ] 명확한 변수명 (약어 지양)
- [ ] 함수명: 동사로 시작 (`get_`, `find_`, `analyze_`)
- [ ] 상수: 대문자 스네이크 케이스 (`MAX_RETRIES`)

### Paginator 사용

- [ ] 대량 리소스 조회 시 Paginator 사용
- [ ] 단일 API 호출 시 결과 제한 인지

```python
# 권장
paginator = client.get_paginator("describe_instances")
for page in paginator.paginate():
    instances.extend(page.get("Reservations", []))
```

### 문서화

- [ ] 모듈 docstring
- [ ] 공개 함수 docstring
- [ ] 복잡한 로직 주석

---

## 금지 (Must Not)

절대 하면 안 되는 항목입니다. 발견 시 PR 차단.

### 자격 증명 하드코딩

- [ ] Access Key 하드코딩 없음
- [ ] Secret Key 하드코딩 없음
- [ ] 세션 토큰 하드코딩 없음

```python
# 절대 금지
client = boto3.client(
    "ec2",
    aws_access_key_id="AKIA...",      # 금지!
    aws_secret_access_key="...",       # 금지!
)
```

### 민감 정보 로깅

- [ ] 자격 증명 로깅 없음
- [ ] 전체 응답 로깅 없음 (토큰 포함 가능)
- [ ] 개인 정보 로깅 없음

```python
# 금지
logger.info(f"Credentials: {access_key}")
logger.debug(f"Response: {response}")

# 권장
logger.info(f"Account: {account_id}")
logger.debug(f"Found {len(instances)} instances")
```

### 리전/계정 하드코딩

- [ ] 리전 하드코딩 없음 (테스트 제외)
- [ ] 계정 ID 하드코딩 없음 (테스트 제외)

```python
# 금지
region = "ap-northeast-2"  # 하드코딩

# 권장
region = ctx.regions[0]  # 컨텍스트에서 가져오기
```

### get_context_session 직접 호출

- [ ] `ctx.provider.get_context_session()` 직접 호출 없음

```python
# 금지: SSO Session 멀티 계정 선택 시 오류 발생
session = ctx.provider.get_context_session()

# 권장: parallel_collect 사용
result = parallel_collect(ctx, callback, service="ec2")
```

---

## 프로젝트 패턴 체크리스트

### 플러그인 구조

- [ ] `__init__.py`에 `CATEGORY`, `TOOLS` 정의
- [ ] 도구 모듈에 `run(ctx)` 함수 존재
- [ ] `parallel_collect` 콜백 시그니처 준수

### 출력 패턴

- [ ] `generate_reports` 사용
- [ ] 컬럼 정의 명확
- [ ] 에러 요약 출력 (`result.get_error_summary()`)

### 에러 수집

- [ ] `ErrorCollector` 또는 `result.error_count` 활용
- [ ] 에러 시 계속 진행 (fail-safe)

---

## 자동화 검사 명령

```bash
# 전체 검사
ruff check cli core plugins
ruff format --check cli core plugins
mypy cli core plugins
bandit -r cli core plugins -c pyproject.toml

# 특정 모듈 검사
ruff check plugins/{service}/ --fix
ruff format plugins/{service}/
mypy plugins/{service}/
pytest tests/plugins/{service}/ -v --cov=plugins/{service}/
```

---

## 리뷰 심각도 분류

| 심각도 | 설명 | 조치 |
|--------|------|------|
| **Critical** | 머지 차단 | 즉시 수정 필수 |
| **Warning** | 수정 권장 | PR 코멘트로 피드백 |
| **Info** | 제안 사항 | 선택적 개선 |

### Critical 예시

- 하드코딩된 자격 증명
- `get_context_session()` 직접 호출
- 테스트 없음
- 린트 에러

### Warning 예시

- 타입 힌트 누락
- 함수 50줄 초과
- Paginator 미사용

### Info 예시

- 변수명 개선 제안
- 코드 스타일 제안
- 리팩토링 제안

---

## 참조

- `.claude/agents/review-pr.md` - PR 리뷰 에이전트
- `.claude/skills/security-review/` - 보안 리뷰 상세
- `.claude/skills/python-best-practices/` - Python 코딩 표준
- `.claude/skills/tdd-workflow/` - TDD 가이드
- `CLAUDE.md` - 프로젝트 가이드
