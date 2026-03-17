---
name: parallel-execution-patterns
description: 병렬 실행 패턴. parallel_collect, Rate Limiter.
---

# 병렬 실행 패턴

멀티 계정/리전 병렬 처리 패턴입니다.

## 권장 패턴: parallel_collect

```python
from core.parallel import parallel_collect, get_client
```

## 기본 사용법

### 1. 콜백 함수 정의

```python
def _collect_and_analyze(session, account_id: str, account_name: str, region: str):
    """병렬 실행 콜백 (단일 계정/리전)

    Args:
        session: boto3 Session (자동 제공)
        account_id: AWS 계정 ID
        account_name: 계정 이름
        region: 리전 코드

    Returns:
        분석 결과 또는 None (결과 없음)
    """
    client = get_client(session, "ec2", region_name=region)

    # 수집
    volumes = client.describe_volumes()["Volumes"]
    if not volumes:
        return None

    # 분석
    return analyze_volumes(volumes, account_id, account_name, region)
```

### 2. parallel_collect 호출

```python
def run(ctx) -> None:
    result = parallel_collect(
        ctx,
        _collect_and_analyze,
        max_workers=20,      # 동시 실행 수 (기본: 20)
        service="ec2",       # 서비스명 (Rate limiter용)
    )

    # 결과 처리
    data = result.get_data()           # list[T | None]
    flat_data = result.get_flat_data()  # 평탄화 (결과가 list일 때)

    # 에러 처리
    if result.error_count > 0:
        console.print(f"[yellow]오류: {result.error_count}건[/yellow]")
        console.print(result.get_error_summary())
```

## ParallelExecutionResult

`parallel_collect` 반환값:

| 속성/메서드 | 설명 |
|------------|------|
| `get_data()` | 모든 결과 리스트 (None 포함) |
| `get_flat_data()` | 평탄화된 결과 (결과가 list일 때) |
| `success_count` | 성공 개수 |
| `error_count` | 에러 개수 |
| `total_count` | 전체 작업 개수 |
| `get_error_summary()` | 에러 요약 문자열 |
| `errors` | 에러 목록 |

```python
result = parallel_collect(ctx, callback, service="ec2")

# None 제외
results = [r for r in result.get_data() if r is not None]

# 통계
print(f"성공: {result.success_count}, 실패: {result.error_count}")
```

## get_client 사용

세션에서 클라이언트 생성 (재시도 로직 포함):

```python
from core.parallel import get_client

def _collect(session, account_id: str, account_name: str, region: str):
    # 권장: get_client 사용
    ec2 = get_client(session, "ec2", region_name=region)
    s3 = get_client(session, "s3", region_name=region)

    # 직접 client 생성 (재시도 없음) - 사용 지양
    # ec2 = session.client("ec2", region_name=region)
```

## Progress Tracking

진행 상황 표시:

```python
from core.parallel import parallel_collect, quiet_mode
from core.cli.ui import parallel_progress

def run(ctx):
    with parallel_progress("리소스 수집") as tracker:
        with quiet_mode():  # 진행 바 표시 중 로그 억제
            result = parallel_collect(
                ctx,
                _collect_and_analyze,
                progress_tracker=tracker,
                service="ec2",
            )

    success, failed, total = tracker.stats
    console.print(f"완료: {success}개 성공, {failed}개 실패 (총 {total}개)")
```

### progress_tracker 상세 사용

```python
from core.cli.ui import parallel_progress, console

def run(ctx):
    # 진행 바 컨텍스트 매니저
    with parallel_progress("VPC 분석") as tracker:
        # tracker.update(current, total) - 수동 업데이트
        # tracker.increment() - 1 증가
        # tracker.set_description("새 설명") - 설명 변경

        with quiet_mode():
            result = parallel_collect(
                ctx,
                _collect_vpcs,
                progress_tracker=tracker,  # 자동 업데이트
                service="ec2",
            )

    # tracker.stats: (success, failed, total) 튜플
    success, failed, total = tracker.stats

    if failed > 0:
        console.print(f"[yellow]! 일부 실패: {failed}/{total}[/yellow]")
    else:
        console.print(f"[green]✓ 전체 성공: {success}/{total}[/green]")
```

### quiet_mode() 컨텍스트 매니저

```python
from core.parallel import quiet_mode, is_quiet, set_quiet

# 컨텍스트 매니저 (권장)
with quiet_mode():
    # 이 블록 내에서 로그 출력 억제
    result = parallel_collect(ctx, callback, service="ec2")

# 수동 제어
set_quiet(True)   # 조용한 모드 활성화
set_quiet(False)  # 조용한 모드 비활성화

# 현재 상태 확인
if is_quiet():
    # 로그 출력 안함
    pass
else:
    console.print("상세 로그...")
```

### 다단계 진행 표시

```python
def run(ctx):
    console.print("[bold]Step 1: 리소스 수집[/bold]")

    with parallel_progress("VPC 수집") as tracker1:
        with quiet_mode():
            vpcs_result = parallel_collect(ctx, _collect_vpcs, progress_tracker=tracker1, service="ec2")

    s1, f1, t1 = tracker1.stats
    console.print(f"  VPCs: {s1} 성공, {f1} 실패")

    console.print("[bold]Step 2: 보안 그룹 수집[/bold]")

    with parallel_progress("SG 수집") as tracker2:
        with quiet_mode():
            sgs_result = parallel_collect(ctx, _collect_sgs, progress_tracker=tracker2, service="ec2")

    s2, f2, t2 = tracker2.stats
    console.print(f"  SGs: {s2} 성공, {f2} 실패")

    # 전체 요약
    total_success = s1 + s2
    total_failed = f1 + f2
    console.print(f"\n[bold]전체: {total_success} 성공, {total_failed} 실패[/bold]")
```

## 상세 제어: ParallelSessionExecutor

더 세밀한 제어가 필요할 때:

```python
from core.parallel import ParallelSessionExecutor, ParallelConfig

config = ParallelConfig(
    max_workers=30,          # 동시 실행 수
    timeout=300,             # 작업당 타임아웃 (초)
    retry_count=3,           # 재시도 횟수
    retry_delay=1.0,         # 재시도 간격 (초)
)

executor = ParallelSessionExecutor(ctx, config)
result = executor.execute(_collect_func, service="ec2")
```

## Rate Limiter

API 쓰로틀링 방지:

```python
from core.parallel import get_rate_limiter, create_rate_limiter, RateLimiterConfig

# 기본 Rate limiter 사용 (service 파라미터로 자동 적용)
result = parallel_collect(ctx, callback, service="ec2")

# 커스텀 Rate limiter
config = RateLimiterConfig(
    tokens_per_second=10,
    max_tokens=100,
)
limiter = create_rate_limiter("custom", config)
```

## 콜백 함수 패턴

### 결과 반환 패턴

```python
# 단일 객체 반환
def _collect(session, account_id, account_name, region) -> AnalysisResult | None:
    data = collect_data(...)
    if not data:
        return None
    return AnalysisResult(data=data)

# 리스트 반환 (get_flat_data로 평탄화)
def _collect(session, account_id, account_name, region) -> list[Volume]:
    volumes = client.describe_volumes()["Volumes"]
    return [Volume.from_aws(v) for v in volumes]
```

### 에러 처리 패턴

```python
from botocore.exceptions import ClientError

def _collect(session, account_id, account_name, region):
    client = get_client(session, "ec2", region_name=region)

    try:
        volumes = client.describe_volumes()["Volumes"]
    except ClientError as e:
        # 권한 없음: None 반환 (정상적인 상황)
        if e.response["Error"]["Code"] == "AccessDenied":
            return None
        # 그 외: 예외 발생 (error_count에 집계)
        raise

    return volumes
```

## 전체 예시

```python
from core.parallel import parallel_collect, get_client
from core.shared.io.output import OutputPath, open_in_explorer
from rich.console import Console

console = Console()

def _collect_and_analyze(session, account_id: str, account_name: str, region: str):
    """EBS 볼륨 수집 및 분석"""
    client = get_client(session, "ec2", region_name=region)

    # 수집
    volumes = []
    paginator = client.get_paginator("describe_volumes")
    for page in paginator.paginate():
        volumes.extend(page.get("Volumes", []))

    if not volumes:
        return None

    # 분석
    unused = [v for v in volumes if v["State"] == "available"]

    return {
        "account_id": account_id,
        "account_name": account_name,
        "region": region,
        "total": len(volumes),
        "unused": len(unused),
        "volumes": unused,
    }

def run(ctx) -> None:
    console.print("[bold]EBS 분석 시작...[/bold]")

    result = parallel_collect(ctx, _collect_and_analyze, service="ec2")

    # 결과 집계
    results = [r for r in result.get_data() if r is not None]

    if result.error_count > 0:
        console.print(f"[yellow]일부 오류: {result.error_count}건[/yellow]")

    if not results:
        console.print("[yellow]분석 결과 없음[/yellow]")
        return

    total_unused = sum(r["unused"] for r in results)
    console.print(f"미사용 볼륨: [red]{total_unused}개[/red]")

    # 보고서 생성
    output_path = OutputPath(ctx.identifier).sub("ec2", "ebs").with_date().build()
    filepath = generate_report(results, output_path)

    console.print(f"[green]완료![/green] {filepath}")
    open_in_explorer(output_path)
```

## 멀티 계정 필수 요구사항 (중요!)

**모든 플러그인은 반드시 `parallel_collect` 패턴을 사용해야 합니다.**

SSO Session에서 여러 계정을 선택할 수 있으므로, 단일 세션만 처리하면 오류가 발생합니다:
```
오류: SSO Session에서 여러 계정이 선택된 경우 account_id를 명시해야 합니다
```

### 잘못된 패턴 (사용 금지)

```python
# ❌ 단일 세션만 처리 - 멀티 계정 미지원
from core.auth.session import get_context_session

def run(ctx):
    session = get_context_session(ctx, "us-east-1")  # 오류 발생!
    result = analyze(session)
```

### 올바른 패턴 (필수)

```python
# ✅ parallel_collect 사용 - 멀티 계정 지원
from core.parallel import parallel_collect

def _collect(session, account_id: str, account_name: str, region: str):
    return analyze(session, account_id, account_name, region)

def run(ctx):
    result = parallel_collect(ctx, _collect, service="my-service")
```

## 글로벌 서비스 패턴

IAM, Health, SSO 등 글로벌 서비스도 `parallel_collect` 패턴을 사용해야 합니다.
리전 파라미터는 받지만, 글로벌 서비스는 항상 `us-east-1` 등 고정 리전을 사용합니다.

### Health API 예시 (us-east-1 전용)

```python
from core.parallel import parallel_collect

def _collect_health(session, account_id: str, account_name: str, region: str):
    """병렬 실행 콜백

    region 파라미터는 받지만, Health API는 항상 us-east-1 사용
    """
    # Health API는 session 생성 시 이미 적절한 리전 설정됨
    collector = HealthCollector(session, account_id, account_name)
    return collector.collect_all()

def run(ctx):
    # CLI에서 리전이 "Global (us-east-1)"로 설정됨
    result = parallel_collect(ctx, _collect_health, service="health")

    # 여러 계정 결과 병합
    results = [r for r in result.get_data() if r is not None]
    merged = CollectionResult.merge(results)
```

### IAM 예시 (글로벌 서비스)

```python
def _collect_iam(session, account_id: str, account_name: str, region: str):
    """IAM은 글로벌이지만 region 파라미터는 무시"""
    collector = IAMCollector()
    return collector.collect(session, account_id, account_name)

def run(ctx):
    # IAM은 어느 리전에서든 호출 가능
    result = parallel_collect(ctx, _collect_iam, service="iam")
```

## 대체 패턴 (특수 상황용)

### InventoryCollector (VPC/리소스 인벤토리)

대규모 리소스 수집 시 스트리밍 방식 사용:

```python
from plugins.resource_explorer.common import InventoryCollector

def run(ctx):
    collector = InventoryCollector(ctx)  # 내부적으로 parallel_collect 사용
    vpcs = collector.collect_vpcs()
    subnets = collector.collect_subnets()
```

### SessionIterator (글로벌 서비스, 한 번만 실행)

SSO처럼 조직 전체에서 한 번만 실행해야 하는 경우:

```python
from core.auth import SessionIterator

def run(ctx):
    with SessionIterator(ctx) as sessions:
        for session, identifier, region in sessions:
            # 첫 번째 성공 시 종료
            result = collect_org_data(session)
            if result:
                break
```

## 레거시 패턴 (사용 금지)

```python
# ❌ 순차 루프 - 멀티 계정 미지원
for account in accounts:
    for region in regions:
        session = ctx.provider.get_session(account.id, region=region)
        result = analyze(session, account, region)

# ❌ 직접 ThreadPoolExecutor - 세션 관리 복잡
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(func, args) for args in items]

# ❌ get_context_session 직접 사용 - 멀티 계정 미지원
from core.auth.session import get_context_session
session = get_context_session(ctx, "us-east-1")  # 오류 발생!
```

## 참조

- `core/parallel/__init__.py` - parallel_collect, get_client
- `core/parallel/executor.py` - ParallelSessionExecutor, ParallelConfig
- `core/parallel/rate_limiter.py` - Rate limiter
- `core/parallel/types.py` - ParallelExecutionResult
