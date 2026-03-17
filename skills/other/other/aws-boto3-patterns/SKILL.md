---
name: aws-boto3-patterns
description: AWS boto3 사용 패턴. Paginator, 세션 관리, CloudWatch 배치 메트릭 등.
---

# AWS boto3 패턴

이 프로젝트의 boto3 사용 패턴입니다.

## Paginator 사용

대량 리소스 조회 시 필수:

```python
def list_all_instances(client) -> list:
    """모든 EC2 인스턴스 조회"""
    instances = []
    paginator = client.get_paginator('describe_instances')

    for page in paginator.paginate():
        for reservation in page['Reservations']:
            instances.extend(reservation['Instances'])

    return instances
```

## 세션 관리

`parallel_collect` 콜백에서 세션 사용:

```python
from core.parallel import get_client, parallel_collect

def _collect_and_analyze(session, account_id: str, account_name: str, region: str):
    """병렬 실행 콜백 (단일 계정/리전)"""
    client = get_client(session, "ec2", region_name=region)
    # ...

def run(ctx) -> None:
    result = parallel_collect(ctx, _collect_and_analyze, service="ec2")
    data = result.get_data()
```

## 에러 핸들링

```python
from botocore.exceptions import ClientError, BotoCoreError

try:
    response = client.describe_instances()
except ClientError as e:
    error_code = e.response['Error']['Code']

    if error_code == 'AccessDenied':
        console.print(f"[yellow]권한 부족: {region}[/yellow]")
        return []
    elif error_code == 'InvalidParameterValue':
        console.print(f"[red]잘못된 파라미터[/red]")
        raise
    else:
        raise
except BotoCoreError as e:
    console.print(f"[red]AWS 연결 오류: {e}[/red]")
    raise
```

## 병렬 리전 처리

core/parallel 모듈 사용:

```python
from core.parallel import get_client, parallel_collect

def _collect_and_analyze(session, account_id: str, account_name: str, region: str):
    """병렬 실행 콜백 - 멀티 계정/리전 자동 처리"""
    client = get_client(session, "ec2", region_name=region)
    # ... 리소스 수집 및 분석
    return result  # 또는 None

def run(ctx) -> None:
    result = parallel_collect(
        ctx,
        _collect_and_analyze,
        max_workers=20,
        service="ec2",  # 서비스명 (진행 표시용)
    )
    results = [r for r in result.get_data() if r is not None]

    if result.error_count > 0:
        console.print(f"[yellow]오류: {result.error_count}건[/yellow]")
```

## Waiter 사용

상태 대기:

```python
waiter = client.get_waiter('instance_running')
waiter.wait(
    InstanceIds=['i-1234567890abcdef0'],
    WaiterConfig={'Delay': 5, 'MaxAttempts': 20}
)
```

## 태그 필터링

```python
response = client.describe_instances(
    Filters=[
        {'Name': 'tag:Environment', 'Values': ['production']},
        {'Name': 'instance-state-name', 'Values': ['running']},
    ]
)
```

## 태그 정책 검증

리소스 태그 정책 준수 확인:

```python
from core.tools import (
    TagPolicyValidator,
    TagPolicy,
    TagRule,
    create_cost_allocation_policy,
    create_basic_policy,
)

# 기본 정책 사용
policy = create_basic_policy(
    required_tags=["Name", "Environment", "Owner"],
    environment_values=["prod", "stg", "dev"],
)

# 커스텀 정책
policy = TagPolicy(
    name="My Policy",
    rules=[
        TagRule(key="Environment", required=True, allowed_values=["prod", "dev"]),
        TagRule(key="CostCenter", required=True, pattern=r"^CC-\d{4}$"),
        TagRule(key="Owner", required=True, pattern=r"^[a-z]+@company\.com$"),
    ],
)

# 검증
validator = TagPolicyValidator(policy)
result = validator.validate({"Environment": "prod", "Owner": "john@company.com"})

if not result.is_valid:
    console.print(result.get_summary())
    for key in result.missing_required:
        console.print(f"  누락: {key}")

# 여러 리소스 일괄 검증
resources = [{"Id": "res-1", "Tags": {"Environment": "prod"}}]
results = validator.validate_resources(resources)
compliant, non_compliant, ids = validator.get_compliance_summary(results)
```

**사전 정의 정책:**
- `create_basic_policy()` - 기본 태그 (Name, Environment, Owner)
- `create_cost_allocation_policy()` - 비용 할당 태그
- `create_security_policy()` - 보안 태그 (DataClassification 등)
- `create_map_migration_policy()` - MAP 2.0 마이그레이션 태그

## 리전 가용성 확인

계정에서 접근 가능한 리전 확인 (옵트인 리전 지원):

```python
from core.region import (
    get_available_regions,
    filter_available_regions,
    validate_regions,
    RegionAvailabilityChecker,
)

# 간편 사용
available = get_available_regions(session)

# 요청 리전 검증
requested = ["ap-northeast-2", "me-south-1"]
available, unavailable = validate_regions(session, requested)

for region, reason in unavailable:
    console.print(f"[yellow]{region}: {reason}[/yellow]")

# 상세 제어
checker = RegionAvailabilityChecker(session=session)
opt_in_regions = checker.get_opt_in_regions()  # 옵트인 필요 리전
enabled_opt_ins = checker.get_enabled_opt_in_regions()  # 활성화된 옵트인 리전
```

**특징:**
- 옵트인 리전(me-south-1, af-south-1 등) 자동 처리
- TTL 기반 캐싱 (1시간)
- `expand_region_pattern()`과 연동 가능

## CloudWatch 메트릭 배치 수집

미사용 리소스 탐지 시 CloudWatch 메트릭을 효율적으로 조회:

```python
from core.shared.aws.metrics import (
    batch_get_metrics,
    build_ec2_metric_queries,
    build_lambda_metric_queries,
)

# EC2 인스턴스 메트릭 조회 (14일)
queries = build_ec2_metric_queries(
    instance_ids=["i-123", "i-456"],
    days=14,
)
metrics = batch_get_metrics(session, queries, region)

# Lambda 함수 메트릭 조회
queries = build_lambda_metric_queries(
    function_names=["my-func-1", "my-func-2"],
    days=14,
)
metrics = batch_get_metrics(session, queries, region)
```

**지원 함수:**
- `build_ec2_metric_queries()` - EC2 CPUUtilization
- `build_lambda_metric_queries()` - Lambda Invocations
- `build_rds_metric_queries()` - RDS DatabaseConnections
- `build_elasticache_metric_queries()` - ElastiCache CurrConnections
- `build_nat_metric_queries()` - NAT Gateway BytesOutToDestination

**특징:**
- GetMetricData API로 500개 메트릭/호출 (85% API 감소)
- 자동 배치 처리
- Rate limiting 적용

## 리소스 인벤토리 수집

서비스별 인벤토리 도구에서 공통 컬렉터 사용:

```python
from core.shared.aws.inventory import InventoryCollector

def run(ctx) -> None:
    collector = InventoryCollector(ctx)

    # EC2 인스턴스 수집
    instances = collector.collect_ec2()

    # Security Group 수집
    security_groups = collector.collect_security_groups()

    # VPC 리소스 수집
    enis = collector.collect_enis()
    nat_gateways = collector.collect_nat_gateways()
    vpc_endpoints = collector.collect_vpc_endpoints()

    # ELB 리소스 수집
    load_balancers = collector.collect_load_balancers()
    target_groups = collector.collect_target_groups()
```

**캐싱:**
- TTL 기반 글로벌 캐시 (기본 5분)
- 동일 세션 내 중복 API 호출 방지

## 자격 증명 Best Practices

- 하드코딩 금지
- 환경 변수 또는 AWS 프로필 사용
- IAM Role 사용 권장 (EC2, Lambda)
- 세션 토큰 만료 처리

```python
# SSO 세션 갱신은 parallel_collect 내부에서 자동 처리됨
# 토큰 만료 시 자동으로 재인증 시도

# ctx.provider 직접 사용 (특수한 경우):
if ctx.provider:
    try:
        session = ctx.provider.get_session(region=region)
    except Exception:
        console.print("[yellow]SSO 토큰 만료. 재인증 필요.[/yellow]")
        raise
```
