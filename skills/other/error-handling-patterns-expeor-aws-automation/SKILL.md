---
name: error-handling-patterns
description: 에러 핸들링 패턴. ErrorCollector, try_or_default, @safe_aws_call, 에러 분류 등.
---

# 에러 핸들링 패턴

프로젝트의 표준 에러 처리 패턴입니다.

## 권장 패턴: core/parallel/errors

```python
from core.parallel.errors import ErrorCollector, ErrorSeverity, try_or_default
```

## @safe_aws_call 데코레이터

Rate limiting + 재시도 + 구조화된 에러 처리를 제공하는 데코레이터:

```python
from core.parallel.decorators import safe_aws_call, RetryConfig
from core.parallel.types import TaskError

@safe_aws_call(service="ec2", operation="describe_volumes")
def get_volumes(session, region):
    ec2 = session.client("ec2", region_name=region)
    return ec2.describe_volumes()["Volumes"]

# 사용
result = get_volumes(session, "ap-northeast-2")
if isinstance(result, TaskError):
    print(f"Error: {result.category} - {result.message}")
else:
    print(f"Found {len(result)} volumes")
```

### RetryConfig 설정

```python
from core.parallel.decorators import RetryConfig, safe_aws_call

# 커스텀 재시도 설정
config = RetryConfig(
    max_retries=5,        # 최대 5회 재시도 (기본: 3)
    base_delay=2.0,       # 기본 대기 2초 (기본: 1.0)
    max_delay=60.0,       # 최대 대기 60초 (기본: 30.0)
    exponential_base=2.0, # 지수 백오프 밑수
    jitter=True,          # 랜덤 지터 추가 (기본: True)
)

@safe_aws_call(service="rds", operation="describe_instances", retry_config=config)
def get_rds_instances(session, region):
    rds = session.client("rds", region_name=region)
    return rds.describe_db_instances()["DBInstances"]
```

### 재시도 가능한 에러

자동으로 재시도되는 에러 코드:
- `Throttling`, `ThrottlingException`, `RequestLimitExceeded`
- `TooManyRequestsException`, `RateExceeded`
- `ServiceUnavailable`, `InternalError`
- `RequestTimeout`, `SlowDown`

재시도하지 않는 에러 (즉시 TaskError 반환):
- `AccessDenied`, `UnauthorizedAccess`
- `ResourceNotFound`, `NoSuchEntity`
- `ValidationException`

## categorize_error() 함수

에러를 자동으로 카테고리로 분류:

```python
from core.parallel.decorators import categorize_error
from core.parallel.types import ErrorCategory

try:
    result = client.describe_instances()
except Exception as e:
    category = categorize_error(e)
    if category == ErrorCategory.THROTTLING:
        print("API 호출 제한 초과")
    elif category == ErrorCategory.ACCESS_DENIED:
        print("권한 없음")
    elif category == ErrorCategory.EXPIRED_TOKEN:
        print("토큰 만료 - 재인증 필요")
```

## ErrorCollector 사용

### 기본 사용법

```python
from botocore.exceptions import ClientError
from core.parallel.errors import ErrorCollector, ErrorSeverity

def collect_resources(session, account_id: str, account_name: str, region: str):
    errors = ErrorCollector(service="ec2")
    client = get_client(session, "ec2", region_name=region)
    results = []

    try:
        response = client.describe_instances()
        results = response.get("Reservations", [])
    except ClientError as e:
        errors.collect(
            e,
            account_id=account_id,
            account_name=account_name,
            region=region,
            operation="describe_instances",
            severity=ErrorSeverity.WARNING,
        )

    return results, errors
```

### ErrorSeverity 레벨

| 레벨 | 용도 | 자동 다운그레이드 |
|------|------|------------------|
| `CRITICAL` | 핵심 기능 실패 | - |
| `WARNING` | 부분 실패, 계속 진행 | AccessDenied → INFO |
| `INFO` | 정보성 (권한 없음 등) | - |
| `DEBUG` | 개발/디버깅용 | - |

### ErrorSeverity 사용 예시

```python
from core.parallel.errors import ErrorCollector, ErrorSeverity

errors = ErrorCollector(service="ec2")

# CRITICAL: 필수 API 실패 (전체 도구 실행 불가)
try:
    instances = client.describe_instances()
except ClientError as e:
    errors.collect(
        e, account_id, account_name, region,
        operation="describe_instances",
        severity=ErrorSeverity.CRITICAL,  # 핵심 기능 실패
    )
    return None  # 분석 불가

# WARNING: 부분 실패 (계속 진행 가능)
try:
    tags = client.describe_tags(...)
except ClientError as e:
    errors.collect(
        e, account_id, account_name, region,
        operation="describe_tags",
        severity=ErrorSeverity.WARNING,  # 태그 없어도 계속 가능
    )
    tags = []

# INFO: 예상된 상황 (권한 없음 등)
# AccessDenied는 자동으로 INFO로 다운그레이드됨
try:
    secrets = client.list_secrets()
except ClientError as e:
    errors.collect(
        e, account_id, account_name, region,
        operation="list_secrets",
        severity=ErrorSeverity.WARNING,  # AccessDenied면 INFO로 변환
    )

# DEBUG: 옵션 데이터 (없어도 무관)
snapshot_count = try_or_default(
    lambda: len(client.describe_snapshots(...)["Snapshots"]),
    default=0,
    collector=errors,
    operation="describe_snapshots",
    severity=ErrorSeverity.DEBUG,  # 실패해도 로그만
)
```

### 에러 조회

```python
# 에러 존재 여부
if errors.has_errors:
    print(errors.get_summary())  # "에러 3건 (warning: 2건, info: 1건)"

# 심각도별 조회
critical = errors.critical_errors
warnings = errors.warning_errors

# 계정별 그룹핑
by_account = errors.get_by_account()
for account, account_errors in by_account.items():
    print(f"{account}: {len(account_errors)}건")
```

### get_by_account() 그룹핑 예시

```python
def print_error_report(errors: ErrorCollector):
    """계정별 에러 리포트 출력"""
    by_account = errors.get_by_account()

    if not by_account:
        console.print("[green]✓ 에러 없음[/green]")
        return

    console.print("\n[bold]계정별 에러 요약[/bold]")
    for account_id, account_errors in by_account.items():
        console.print(f"\n[cyan]{account_id}[/cyan]")

        # 에러 유형별 그룹화
        by_category = {}
        for err in account_errors:
            cat = err.category.name
            by_category.setdefault(cat, []).append(err)

        for category, errs in by_category.items():
            console.print(f"  {category}: {len(errs)}건")
            for err in errs[:3]:  # 최대 3개만 표시
                console.print(f"    - {err.operation}: {err.message[:50]}...")

    # 전체 요약
    console.print(f"\n[bold]총 {errors.error_count}건 에러[/bold]")
    console.print(f"  CRITICAL: {len(errors.critical_errors)}건")
    console.print(f"  WARNING: {len(errors.warning_errors)}건")
    console.print(f"  INFO: {len(errors.info_errors)}건")
```

## try_or_default 함수

단일 API 호출에 간편하게 사용:

```python
from core.parallel.errors import try_or_default, ErrorSeverity

def get_instance_tags(client, instance_id: str, errors: ErrorCollector) -> dict:
    """태그 조회 - 실패해도 기본값 반환"""
    return try_or_default(
        lambda: client.describe_tags(
            Filters=[{"Name": "resource-id", "Values": [instance_id]}]
        ).get("Tags", []),
        default={},
        collector=errors,
        account_id=account_id,
        account_name=account_name,
        region=region,
        operation="describe_tags",
        severity=ErrorSeverity.DEBUG,  # 태그는 옵션이라 DEBUG
    )
```

### 옵션 데이터 조회 패턴

```python
def collect_volume_info(client, volume_id: str, errors: ErrorCollector):
    # 필수 데이터
    volume = client.describe_volumes(VolumeIds=[volume_id])["Volumes"][0]

    # 옵션 데이터 (실패해도 계속)
    tags = try_or_default(
        lambda: client.describe_tags(...)["Tags"],
        default=[],
        collector=errors,
        operation="describe_tags",
        severity=ErrorSeverity.DEBUG,
    )

    snapshots = try_or_default(
        lambda: client.describe_snapshots(...)["Snapshots"],
        default=[],
        collector=errors,
        operation="describe_snapshots",
        severity=ErrorSeverity.DEBUG,
    )

    return VolumeInfo(volume=volume, tags=tags, snapshots=snapshots)
```

## 에러 카테고리 자동 분류

`ErrorCollector`는 에러 코드를 자동 분류:

| 카테고리 | 에러 코드 예시 |
|----------|---------------|
| `ACCESS_DENIED` | AccessDenied, Unauthorized, Forbidden |
| `NOT_FOUND` | NotFound, NoSuch, DoesNotExist |
| `THROTTLING` | Throttling, RateLimit, TooManyRequests |
| `TIMEOUT` | Timeout, TimedOut |
| `EXPIRED_TOKEN` | ExpiredToken, ExpiredTokenException |
| `NETWORK` | ConnectionError, TimeoutError, OSError |
| `UNKNOWN` | 기타 |

## 병렬 처리와 에러 핸들링

```python
from core.parallel import parallel_collect
from core.parallel.errors import ErrorCollector

def _collect_and_analyze(session, account_id: str, account_name: str, region: str):
    """병렬 콜백 - 에러는 내부에서 처리"""
    errors = ErrorCollector(service="ec2")
    client = get_client(session, "ec2", region_name=region)

    try:
        # 수집
        volumes = client.describe_volumes()["Volumes"]
    except ClientError as e:
        errors.collect(e, account_id, account_name, region, "describe_volumes")
        return None  # 또는 빈 결과 반환

    # 분석 및 반환
    return AnalysisResult(data=volumes, errors=errors)

def run(ctx):
    result = parallel_collect(ctx, _collect_and_analyze, service="ec2")

    # parallel_collect의 에러 카운트
    if result.error_count > 0:
        console.print(f"[yellow]오류 {result.error_count}건[/yellow]")
        console.print(result.get_error_summary())
```

## 레거시 패턴 (사용 지양)

```python
# 단순 try-except
try:
    result = client.describe_instances()
except Exception as e:
    print(f"Error: {e}")
    return []

# 빈 except
except:
    pass

# print로 에러 출력
except ClientError as e:
    print(f"Error in {region}: {e}")
```

## 권장 패턴

```python
# ErrorCollector 사용
from core.parallel.errors import ErrorCollector, ErrorSeverity

errors = ErrorCollector(service="ec2")

try:
    result = client.describe_instances()
except ClientError as e:
    errors.collect(
        e,
        account_id=account_id,
        account_name=account_name,
        region=region,
        operation="describe_instances",
        severity=ErrorSeverity.WARNING,
    )
    return []

# try_or_default로 간소화
tags = try_or_default(
    lambda: client.describe_tags(...)["Tags"],
    default=[],
    collector=errors,
    operation="describe_tags",
)
```

## 전체 예시

```python
from botocore.exceptions import ClientError
from core.parallel import get_client, parallel_collect
from core.parallel.errors import ErrorCollector, ErrorSeverity, try_or_default

def _collect_volumes(session, account_id: str, account_name: str, region: str):
    """볼륨 수집 (병렬 콜백)"""
    errors = ErrorCollector(service="ec2")
    client = get_client(session, "ec2", region_name=region)

    volumes = []
    try:
        paginator = client.get_paginator("describe_volumes")
        for page in paginator.paginate():
            for vol in page.get("Volumes", []):
                # 옵션 데이터: 스냅샷 개수
                snapshot_count = try_or_default(
                    lambda vid=vol["VolumeId"]: len(
                        client.describe_snapshots(
                            Filters=[{"Name": "volume-id", "Values": [vid]}]
                        ).get("Snapshots", [])
                    ),
                    default=0,
                    collector=errors,
                    account_id=account_id,
                    account_name=account_name,
                    region=region,
                    operation="describe_snapshots",
                    severity=ErrorSeverity.DEBUG,
                )
                volumes.append({**vol, "SnapshotCount": snapshot_count})

    except ClientError as e:
        errors.collect(
            e, account_id, account_name, region,
            operation="describe_volumes",
            severity=ErrorSeverity.WARNING,
        )

    return {"volumes": volumes, "errors": errors}

def run(ctx):
    result = parallel_collect(ctx, _collect_volumes, service="ec2")

    # 결과 집계
    all_volumes = []
    for r in result.get_data():
        if r:
            all_volumes.extend(r["volumes"])

    if result.error_count > 0:
        console.print(f"[yellow]일부 오류: {result.error_count}건[/yellow]")
```

## 참조

- `core/parallel/errors.py` - ErrorCollector, try_or_default
- `core/parallel/decorators.py` - safe_aws_call, RetryConfig, categorize_error
- `core/parallel/types.py` - ErrorCategory, TaskError
