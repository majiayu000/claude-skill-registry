---
name: tdd-workflow
description: TDD 워크플로우 가이드. Red-Green-Refactor 철학, pytest, moto 모킹, 테스트 패턴.
---

# TDD 워크플로우

테스트 주도 개발 가이드입니다.

## 철학: The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

테스트 전에 코드를 작성했다면? **삭제하고 다시 시작.**

- "참고용으로 보관" 금지
- "적용하면서 테스트 작성" 금지
- 테스트로부터 새로 구현

## Red-Green-Refactor

### RED - 실패하는 테스트 작성

하나의 행위만 테스트하는 최소한의 테스트 작성.

```python
def test_find_unused_volumes_returns_unattached_volumes():
    """미연결 볼륨만 반환하는지 테스트"""
    # Arrange
    volumes = [
        {"VolumeId": "vol-1", "Attachments": []},          # 미연결
        {"VolumeId": "vol-2", "Attachments": [{"InstanceId": "i-1"}]},  # 연결됨
    ]

    # Act
    result = find_unused_volumes(volumes)

    # Assert
    assert len(result) == 1
    assert result[0]["VolumeId"] == "vol-1"
```

**요구사항:**
- 하나의 행위만 테스트
- 명확한 이름 (무엇을_어떤상황에서_어떤결과)
- 실제 코드 테스트 (가능하면 mock 최소화)

### Verify RED - 반드시 실패 확인

```bash
pytest tests/plugins/ec2/test_ebs_audit.py::test_find_unused_volumes -v
```

확인:
- 테스트가 **실패**하는가? (에러가 아닌 실패)
- 실패 이유가 **기능 미구현** 때문인가? (오타 아님)

### GREEN - 최소한의 코드

테스트를 통과시키는 **가장 단순한** 코드 작성.

```python
def find_unused_volumes(volumes: list[dict]) -> list[dict]:
    return [v for v in volumes if not v.get("Attachments")]
```

**금지 사항:**
- 미래를 위한 확장성 추가
- 요청받지 않은 기능 추가
- "개선"을 위한 리팩토링

### Verify GREEN - 통과 확인

```bash
pytest tests/plugins/ec2/test_ebs_audit.py -v
```

확인:
- 테스트 통과
- 다른 테스트도 통과
- 경고/에러 없음

### REFACTOR - 코드 개선

GREEN 이후에만:
- 중복 제거
- 이름 개선
- 헬퍼 추출

**테스트는 항상 통과 상태 유지.**

---

## 프로젝트 테스트 구조

```
tests/
├── conftest.py           # 공유 fixtures
├── cli/                  # CLI 테스트
├── core/                 # Core 모듈 테스트
│   ├── parallel/         # 병렬 처리 테스트
│   └── tools/            # 도구 테스트
└── plugins/              # 플러그인 테스트
    └── cloudwatch/       # CloudWatch 배치 메트릭 테스트
```

## AWS 모킹 (moto)

### 기본 패턴

```python
import boto3
from moto import mock_aws

@mock_aws
def test_describe_instances():
    # moto가 AWS를 모킹
    client = boto3.client('ec2', region_name='ap-northeast-2')

    # 테스트 데이터 생성
    client.run_instances(
        ImageId='ami-12345678',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
    )

    # 테스트 실행
    response = client.describe_instances()
    assert len(response['Reservations']) == 1
```

### Fixture 사용

```python
# tests/conftest.py
import pytest
import boto3
from moto import mock_aws

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials"""
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

@pytest.fixture
def mock_ec2(aws_credentials):
    """Mocked EC2 client"""
    with mock_aws():
        yield boto3.client('ec2', region_name='ap-northeast-2')

@pytest.fixture
def mock_ctx():
    """Mocked CLI context"""
    from unittest.mock import MagicMock
    ctx = MagicMock()
    ctx.provider.get_session.return_value = boto3.Session()
    ctx.regions = ['ap-northeast-2']
    return ctx
```

## 테스트 명명 규칙

```python
def test_함수명_상황_예상결과():
    ...

# 예시
def test_find_unused_volumes_when_no_attachments_returns_volume():
    ...

def test_analyze_region_with_access_denied_returns_empty_list():
    ...
```

## 테스트 실행

```bash
# 전체 테스트
pytest tests/ -v

# 특정 파일
pytest tests/plugins/ec2/test_ebs_audit.py -v

# 특정 함수
pytest tests/plugins/ec2/test_ebs_audit.py::test_unused_volumes -v

# 커버리지
pytest tests/ --cov=core --cov=cli --cov=plugins --cov-report=html

# 실패 시 즉시 중단
pytest tests/ -x

# 마지막 실패 테스트만
pytest tests/ --lf
```

## 테스트 카테고리

### 단위 테스트
개별 함수/메서드 테스트:
```python
def test_validate_account_id():
    assert validate_account_id('123456789012') is True
    assert validate_account_id('invalid') is False
```

### 통합 테스트
모듈 간 상호작용 테스트:
```python
@mock_aws
def test_ebs_audit_full_workflow():
    # 데이터 생성 → 분석 → 결과 검증
```

### E2E 테스트
전체 CLI 플로우 테스트:
```python
from click.testing import CliRunner
from core.cli.app import cli

def test_list_tools_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['list-tools'])
    assert result.exit_code == 0
    assert 'ec2' in result.output
```

## 고급 패턴

### Parameterized 테스트

```python
import pytest

@pytest.mark.parametrize("volume,expected", [
    ({"VolumeId": "vol-1", "Attachments": []}, True),       # 미연결
    ({"VolumeId": "vol-2", "Attachments": [{}]}, False),    # 연결됨
    ({"VolumeId": "vol-3", "Attachments": None}, True),     # None 처리
])
def test_is_volume_unused(volume, expected):
    assert is_volume_unused(volume) == expected
```

### 예외 테스트

```python
import pytest
from botocore.exceptions import ClientError

def test_collect_with_access_denied_returns_empty():
    """AccessDenied 에러 시 빈 결과 반환"""
    with pytest.raises(ClientError) as exc_info:
        raise_access_denied()

    assert exc_info.value.response['Error']['Code'] == 'AccessDenied'
```

### Async 테스트

```python
import pytest

@pytest.mark.asyncio
async def test_async_collect():
    result = await async_collect_resources()
    assert len(result) > 0
```

---

## TDD 체크리스트

### 작업 시작 전
- [ ] 구현하려는 기능 명확히 이해
- [ ] 실패하는 테스트 먼저 작성

### RED 단계
- [ ] 하나의 행위만 테스트
- [ ] 테스트 이름이 행위를 설명
- [ ] 테스트 실행 → 실패 확인
- [ ] 실패 이유가 기능 미구현 (오타 아님)

### GREEN 단계
- [ ] 최소한의 코드만 작성
- [ ] YAGNI 원칙 (필요 없는 것은 만들지 않음)
- [ ] 테스트 통과 확인
- [ ] 다른 테스트도 통과

### REFACTOR 단계
- [ ] GREEN 상태에서만 리팩토링
- [ ] 리팩토링 후에도 테스트 통과
- [ ] 중복 제거, 이름 개선

### 완료 전
- [ ] 모든 새 함수에 테스트 있음
- [ ] 엣지 케이스 테스트 (빈 목록, None 등)
- [ ] 에러 케이스 테스트 (AccessDenied 등)
- [ ] 린트 통과 (ruff check)

---

## 흔한 합리화 (금지)

| 합리화 | 현실 |
|--------|------|
| "너무 단순해서 테스트 불필요" | 단순한 코드도 깨진다. 테스트 30초면 됨. |
| "나중에 테스트 작성" | 통과하는 테스트는 아무것도 증명 못함. |
| "수동 테스트했음" | 기록 없음, 재실행 불가, 누락 가능. |
| "시간 낭비" | TDD가 디버깅보다 빠름. |
| "이미 X시간 투자" | 매몰 비용. 신뢰할 수 없는 코드 유지가 더 낭비. |

---

## 참조

- `obra-superpowers/skills/test-driven-development/` - TDD 철학 상세
- `wshobson-agents/plugins/python-development/skills/python-testing-patterns/` - pytest 고급 패턴
- `core/parallel/errors.py` - ErrorCollector 테스트 예시
- `tests/conftest.py` - 공유 fixtures
