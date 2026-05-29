---
name: migrate-tool
description: 레거시 플러그인 패턴을 최신 패턴으로 마이그레이션하는 가이드 제공.
disable-model-invocation: true
---

# /migrate-tool - 레거시 패턴 마이그레이션 가이드

기존 플러그인을 최신 패턴으로 마이그레이션하는 가이드를 제공합니다.

## 사용법

```
/migrate-tool <service>/<module> [--pattern <pattern>]
```

예시:
```
/migrate-tool ec2/unused                    # 모든 패턴 분석
/migrate-tool ec2/unused --pattern output   # 출력 경로 패턴만
/migrate-tool vpc/security --pattern error  # 에러 핸들링만
/migrate-tool s3/inventory --pattern excel  # Excel 출력만
/migrate-tool iam/audit --pattern parallel  # 병렬 처리만
```

## 지원 패턴

| 패턴 ID | 설명 | 우선순위 |
|---------|------|----------|
| `output` | OutputPath 빌더 패턴 | 중간 |
| `error` | 에러 핸들링 패턴 | 높음 |
| `excel` | Excel 출력 패턴 | 중간 |
| `parallel` | 병렬 처리 패턴 | 높음 |
| `client` | get_client() 래퍼 사용 | 높음 |
| `html` | HTML 리포트 패턴 | 중간 |
| `generate_reports` | 통합 출력 패턴 | 중간 |
| `cloudwatch` | CloudWatch 배치 메트릭 | 높음 |
| `inventory` | InventoryCollector 캐싱 | 높음 |
| `all` | 모든 패턴 분석 (기본값) | - |

## 실행 순서

### 1. 대상 파일 확인

`$ARGUMENTS`에서 서비스와 모듈 추출:
- 대상: `plugins/{service}/{module}.py`
- 파일이 없으면 오류 후 종료

### 2. 레거시 패턴 감지

대상 파일에서 레거시 패턴 검색:

#### 2.1 Output Path 레거시 패턴

감지 패턴:
```python
# 직접 경로 구성
output_dir = f"output/{account_id}/..."
os.makedirs(output_dir, exist_ok=True)

# 또는
output_path = os.path.join("output", account_id, ...)
Path(output_path).mkdir(parents=True, exist_ok=True)
```

#### 2.2 Error Handling 레거시 패턴

감지 패턴:
```python
# 단순 try-except
try:
    result = client.describe_xxx()
except Exception as e:
    print(f"Error: {e}")
    return []

# 또는 빈 except
except:
    pass
```

#### 2.3 Excel 레거시 패턴

감지 패턴:
```python
# 직접 openpyxl 사용
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.cell(row=1, column=1, value="Header")

# 직접 스타일 적용
from openpyxl.styles import Font, PatternFill
header_fill = PatternFill(...)
```

#### 2.4 Parallel 레거시 패턴

감지 패턴:
```python
# 순차 루프
for account in accounts:
    for region in regions:
        result = analyze(account, region)

# 또는 직접 ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    ...
```

### 3. 마이그레이션 가이드 생성

---

## 패턴별 마이그레이션 가이드

### 1. Output Path (`output`)

#### Before (레거시)
```python
import os
from datetime import datetime

def generate_report(results, account_id):
    today = datetime.now().strftime("%Y%m%d")
    output_dir = f"output/{account_id}/ec2/unused/{today}"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"report_{today}.xlsx")
    # ... 파일 저장
```

#### After (현재 패턴)
```python
from core.tools.output import OutputPath, open_in_explorer

def generate_report(results, ctx):
    # ctx에서 identifier 추출
    if hasattr(ctx, "is_sso_session") and ctx.is_sso_session() and ctx.accounts:
        identifier = ctx.accounts[0].id
    elif ctx.profile_name:
        identifier = ctx.profile_name
    else:
        identifier = "default"

    # OutputPath 빌더 사용
    output_path = OutputPath(identifier).sub("ec2", "unused").with_date().build()

    filepath = os.path.join(output_path, "report.xlsx")
    # ... 파일 저장

    open_in_explorer(output_path)
```

#### 변경 포인트
- `os.makedirs()` 제거 → `OutputPath.build()`가 자동 생성
- 직접 경로 구성 제거 → 빌더 패턴 사용
- `open_in_explorer()` 추가로 사용자 경험 개선

---

### 2. Error Handling (`error`)

#### Before (레거시)
```python
from botocore.exceptions import ClientError

def collect_resources(session, account_id, region):
    client = session.client("ec2", region_name=region)

    try:
        response = client.describe_instances()
        return response.get("Reservations", [])
    except ClientError as e:
        print(f"Error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
```

#### After (현재 패턴)
```python
from botocore.exceptions import ClientError
from core.parallel import get_client
from core.parallel.errors import ErrorCollector, ErrorSeverity, try_or_default

def collect_resources(session, account_id, account_name, region, errors: ErrorCollector | None = None):
    client = get_client(session, "ec2", region_name=region)

    try:
        response = client.describe_instances()
        return response.get("Reservations", [])
    except ClientError as e:
        if errors:
            errors.collect(
                e, account_id, account_name, region,
                operation="describe_instances",
                severity=ErrorSeverity.WARNING
            )
        return []
```

#### 또는 try_or_default 사용
```python
def collect_resources(session, account_id, account_name, region, errors: ErrorCollector | None = None):
    client = get_client(session, "ec2", region_name=region)

    # 단일 API 호출에 적합
    reservations = try_or_default(
        lambda: client.describe_instances().get("Reservations", []),
        default=[],
        collector=errors,
        account_id=account_id,
        account_name=account_name,
        region=region,
        operation="describe_instances",
        severity=ErrorSeverity.WARNING,
    )
    return reservations
```

#### 변경 포인트
- `print()` 제거 → `ErrorCollector.collect()` 사용
- `Exception` → `ClientError` 명시적 처리
- 에러 컨텍스트 (account, region, operation) 추가
- `get_client()` 사용으로 재시도 로직 포함

---

### 3. Excel Output (`excel`)

#### Before (레거시)
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

def generate_excel(results, output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # 헤더 스타일
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")

    # 헤더 작성
    headers = ["Account", "Region", "Resource ID", "Status"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font

    # 데이터 작성
    for row_idx, item in enumerate(results, 2):
        ws.cell(row=row_idx, column=1, value=item.account_id)
        ws.cell(row=row_idx, column=2, value=item.region)
        ws.cell(row=row_idx, column=3, value=item.resource_id)
        ws.cell(row=row_idx, column=4, value=item.status)

    # 컬럼 너비 조정
    for col in ws.columns:
        max_len = max(len(str(c.value) if c.value else "") for c in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 2

    wb.save(output_path)
```

#### After (현재 패턴)
```python
from core.tools.io.excel import Workbook, ColumnDef, Styles

def generate_excel(results, output_path):
    wb = Workbook()

    # 컬럼 정의
    columns = [
        ColumnDef(header="Account", header_en="Account", width=15, style="data"),
        ColumnDef(header="Region", header_en="Region", width=15, style="center"),
        ColumnDef(header="Resource ID", header_en="Resource ID", width=25, style="data"),
        ColumnDef(header="Status", header_en="Status", width=12, style="center"),
    ]

    # 시트 생성
    sheet = wb.new_sheet("Results", columns=columns)

    # 데이터 추가
    for item in results:
        style = Styles.danger() if item.status == "unused" else None
        sheet.add_row(
            [item.account_id, item.region, item.resource_id, item.status],
            style=style
        )

    # 저장 (자동 필터, 틀 고정 자동 적용)
    wb.save(output_path)
```

#### Summary 시트 추가
```python
# Summary 시트 생성 (맨 앞에 위치)
summary = wb.new_summary_sheet()
summary.add_title("리소스 분석 보고서")
summary.add_section("분석 정보")
summary.add_item("총 리소스", len(results))
summary.add_item("미사용", unused_count, highlight="danger" if unused_count > 0 else None)
summary.add_section("상위 항목")
summary.add_list_section("Top 5 계정", top_accounts)
```

#### 변경 포인트
- 직접 `openpyxl.Workbook` → `core.tools.io.excel.Workbook`
- 수동 스타일 → `ColumnDef.style`, `Styles.danger()`
- 수동 컬럼 너비 → `ColumnDef.width`
- 수동 필터/고정 → 자동 적용
- Summary 시트 → `SummarySheet` 빌더

---

### 4. Parallel Processing (`parallel`)

#### Before (레거시)
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def analyze_all(ctx):
    results = []
    errors = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {}
        for account in ctx.accounts:
            for region in ctx.regions:
                session = ctx.provider.get_session(account.id, region=region)
                future = executor.submit(
                    collect_resources, session, account.id, account.name, region
                )
                futures[future] = (account.id, region)

        for future in as_completed(futures):
            account_id, region = futures[future]
            try:
                result = future.result()
                results.extend(result)
            except Exception as e:
                errors.append(f"{account_id}/{region}: {e}")

    return results, errors
```

#### After (현재 패턴)
```python
from core.parallel import parallel_collect, get_client

def _collect_and_analyze(session, account_id: str, account_name: str, region: str):
    """단일 계정/리전 수집 및 분석 (병렬 실행용)"""
    client = get_client(session, "ec2", region_name=region)

    # 수집
    resources = []
    paginator = client.get_paginator("describe_instances")
    for page in paginator.paginate():
        resources.extend(page.get("Reservations", []))

    # 분석
    return analyze_resources(resources, account_id, account_name, region)


def run(ctx):
    """플러그인 실행"""
    # parallel_collect가 모든 계정/리전 조합을 병렬 실행
    result = parallel_collect(
        ctx,
        _collect_and_analyze,
        max_workers=20,
        service="ec2"  # Rate limiter용
    )

    # 결과 처리
    all_data = result.get_data()  # list of results
    flat_data = result.get_flat_data()  # flattened if results are lists

    if result.error_count > 0:
        console.print(f"[yellow]일부 오류: {result.error_count}건[/yellow]")
        console.print(result.get_error_summary())

    # 보고서 생성
    generate_report(all_data, ctx)
```

#### 변경 포인트
- 직접 `ThreadPoolExecutor` → `parallel_collect()`
- 수동 세션 관리 → 자동 세션/계정/리전 조합
- 수동 에러 수집 → `ParallelExecutionResult.error_count`
- Rate limiting 자동 적용 (`service` 파라미터)

---

### 5. Client Creation (`client`)

#### Before (레거시)
```python
def collect_resources(session, account_id, account_name, region):
    client = session.client("ec2", region_name=region)
    response = client.describe_instances()
    return response.get("Reservations", [])
```

#### After (현재 패턴)
```python
from core.parallel import get_client

def collect_resources(session, account_id, account_name, region):
    client = get_client(session, "ec2", region_name=region)
    response = client.describe_instances()
    return response.get("Reservations", [])
```

#### 변경 포인트
- `session.client()` → `get_client(session, ...)`
- 자동 Rate limiting 적용
- 재시도 로직 내장
- 서비스별 최적화된 호출 간격

---

### 6. HTML Report (`html`)

#### Before (레거시)
```python
# HTML 미지원 또는 직접 생성
def generate_report(results, output_path):
    wb = Workbook()
    # ... Excel만 생성

# 또는 직접 HTML 생성
html_content = f"<html><body>{data}</body></html>"
with open("report.html", "w") as f:
    f.write(html_content)
```

#### After (현재 패턴)
```python
from core.tools.io.html import create_aws_report

def generate_report(results, output_path, ctx):
    report = create_aws_report(
        title="EC2 미사용 리소스",
        service="EC2",
        tool_name="unused",
        ctx=ctx,
        resources=results,
        charts=[
            {"type": "pie", "title": "리전별 분포", "data_key": "region"},
            {"type": "bar", "title": "계정별 현황", "data_key": "account_name"},
        ]
    )
    report.save(output_path)
```

#### 변경 포인트
- 직접 HTML 생성 → `create_aws_report()` 사용
- ECharts 시각화 자동 포함
- 통일된 스타일 적용
- 필터링/정렬 자동 지원

---

### 7. generate_reports 통합 출력 (`generate_reports`)

#### Before (레거시)
```python
# Excel과 HTML을 별도로 생성
def run(ctx):
    results = collect_data(ctx)

    # Excel 생성
    wb = Workbook()
    # ... Excel 로직
    wb.save("output.xlsx")

    # HTML 생성 (별도)
    report = create_aws_report(...)
    report.save("output.html")
```

#### After (현재 패턴)
```python
from core.tools.io import generate_reports
from core.tools.io.excel import ColumnDef

def run(ctx):
    results = collect_data(ctx)

    # Excel + HTML 동시 생성 (ctx.output_config에 따라)
    generate_reports(
        ctx,
        data=results,
        columns=[
            ColumnDef(header="계정 ID", width=15),
            ColumnDef(header="리전", width=15),
            ColumnDef(header="리소스", width=30),
        ],
        charts=[
            {"type": "pie", "title": "리전별 분포", "data_key": "region"},
        ]
    )
```

#### 변경 포인트
- 분리된 Excel/HTML 로직 → `generate_reports()` 단일 호출
- 출력 형식 자동 결정 (`ctx.output_config`)
- 컬럼 정의 재사용
- 차트 설정 통합

---

### 8. CloudWatch Batch Metrics (`cloudwatch`)

#### Before (레거시)
```python
# 메트릭당 개별 API 호출 (N개 메트릭 = N회 API 호출)
def get_function_metrics(cw, function_name, start, end):
    invocations = cw.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName="Invocations",
        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
        StartTime=start,
        EndTime=end,
        Period=86400,
        Statistics=["Sum"]
    )
    errors = cw.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName="Errors",
        ...
    )
    return invocations, errors

# 100개 함수 × 3개 메트릭 = 300회 API 호출!
for func in functions:
    metrics = get_function_metrics(cw, func["FunctionName"], start, end)
```

#### After (현재 패턴)
```python
from shared.aws.metrics import (
    batch_get_metrics,
    build_lambda_metric_queries,
)

def get_all_metrics(cw, functions, start, end):
    # 쿼리 빌드
    queries = build_lambda_metric_queries(
        function_names=[f["FunctionName"] for f in functions],
        metrics=["Invocations", "Errors", "Duration"]
    )

    # 배치 조회 (500개 메트릭 = 1회 API 호출)
    results = batch_get_metrics(
        cloudwatch_client=cw,
        queries=queries,
        start_time=start,
        end_time=end,
        period=86400
    )
    # results: {"func1_invocations_sum": 1000, "func1_errors_sum": 5, ...}
    return results

# 100개 함수 × 3개 메트릭 = 1회 API 호출! (85% 감소)
metrics = get_all_metrics(cw, functions, start, end)
```

#### 변경 포인트
- `get_metric_statistics()` 개별 호출 → `batch_get_metrics()` 배치 호출
- API 호출 횟수 85% 이상 감소
- 500개 메트릭까지 단일 호출로 처리
- 빌더 함수로 쿼리 생성 간소화

---

### 9. InventoryCollector 캐싱 (`inventory`)

#### Before (레거시)
```python
# 여러 도구에서 동일 리소스 반복 조회
def tool1_collect(session, region):
    ec2 = session.client("ec2", region_name=region)
    instances = ec2.describe_instances()  # 첫 번째 조회
    volumes = ec2.describe_volumes()
    return analyze_tool1(instances, volumes)

def tool2_collect(session, region):
    ec2 = session.client("ec2", region_name=region)
    instances = ec2.describe_instances()  # 중복 조회!
    snapshots = ec2.describe_snapshots(OwnerIds=["self"])
    return analyze_tool2(instances, snapshots)
```

#### After (현재 패턴)
```python
from shared.aws.inventory import InventoryCollector

def tool1_collect(ctx, session, region):
    collector = InventoryCollector(ctx)
    instances = collector.collect_ec2()       # 첫 번째 수집 (캐싱)
    volumes = collector.collect_ebs_volumes()  # 별도 수집
    return analyze_tool1(instances, volumes)

def tool2_collect(ctx, session, region):
    collector = InventoryCollector(ctx)
    instances = collector.collect_ec2()       # 캐시에서 반환 (API 호출 없음)
    snapshots = collector.collect_snapshots()
    return analyze_tool2(instances, snapshots)
```

#### 변경 포인트
- 직접 API 호출 → `InventoryCollector` 사용
- 동일 리소스 중복 조회 방지 (TTL 기반 캐싱)
- 리소스 타입별 최적화된 수집
- 여러 도구 간 데이터 공유

---

## 마이그레이션 우선순위

| 우선순위 | 패턴 | 이유 |
|---------|------|------|
| 1 | `error` | 에러 가시성 개선 |
| 2 | `parallel` | 성능 개선 |
| 3 | `cloudwatch` | API 호출 85% 감소 |
| 4 | `inventory` | 중복 수집 방지 |
| 5 | `client` | Rate limiting 자동 적용 |
| 6 | `generate_reports` | 통합 출력 간소화 |
| 7 | `output` | 경로 일관성 |
| 8 | `excel` | 코드 간소화 |
| 9 | `html` | 시각화 지원 |

---

## 출력 예시

```
/migrate-tool ec2/unused 실행 중...

[분석] plugins/ec2/unused.py

[감지된 레거시 패턴]

1. Output Path (Line 45-47)
   ────────────────────────
   현재:
     output_dir = f"output/{account_id}/ec2/unused/{today}"
     os.makedirs(output_dir, exist_ok=True)

   권장:
     from core.tools.output import OutputPath
     output_path = OutputPath(identifier).sub("ec2", "unused").with_date().build()

2. Error Handling (Line 78-82)
   ────────────────────────────
   현재:
     except Exception as e:
         print(f"Error: {e}")
         return []

   권장:
     from core.parallel.errors import ErrorCollector
     errors.collect(e, account_id, account_name, region, "describe_volumes")

3. Excel Output (Line 120-145)
   ────────────────────────────
   현재:
     from openpyxl import Workbook
     wb = Workbook()
     ws.cell(row=1, column=1, value="Header")

   권장:
     from core.tools.io.excel import Workbook, ColumnDef
     wb = Workbook()
     sheet = wb.new_sheet("Results", columns=[...])

[요약]
  - 총 3개 레거시 패턴 감지
  - 예상 변경: 약 50줄

마이그레이션을 진행하시겠습니까?
  자동 적용: 파일 직접 수정
  수동 적용: 가이드만 출력 (기본값)
```

## 참조 파일

- `core/tools/output/__init__.py` - OutputPath 패턴
- `core/parallel/errors.py` - 에러 핸들링 패턴
- `core/tools/io/excel/workbook.py` - Excel 출력 패턴
- `core/parallel/__init__.py` - 병렬 처리 패턴

## 주의사항

1. **백업 권장**: 자동 마이그레이션 전 git commit 또는 백업
2. **테스트 필수**: 마이그레이션 후 기능 테스트 실행
3. **점진적 적용**: 한 번에 모든 패턴 변경보다 단계적 적용 권장
4. **린트 확인**: 변경 후 `ruff check` 실행
