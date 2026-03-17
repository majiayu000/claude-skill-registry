---
name: output-patterns
description: 리포트 출력 패턴. Excel, HTML 보고서, 콘솔 출력 스타일 가이드.
---

# 리포트 출력 패턴

프로젝트의 표준 리포트 생성 패턴입니다. Excel과 HTML을 동시에 생성합니다.

## 권장 패턴: generate_dual_report() (Primary)

**새 플러그인 작성 시 권장하는 통합 출력 API**

```python
from core.shared.io.compat import generate_dual_report
from core.shared.io.output.helpers import create_output_path
from core.shared.io.output import print_report_complete, open_in_explorer
from core.shared.io.excel import Workbook, ColumnDef, Styles

def _build_excel(results: list, data: list) -> Workbook:
    """Excel Workbook 빌더 (저장하지 않고 반환)"""
    wb = Workbook()
    columns = [
        ColumnDef(header="Account", width=20),
        ColumnDef(header="Region", width=15),
        ColumnDef(header="Resource", width=30),
        ColumnDef(header="Status", width=12, style="center"),
        ColumnDef(header="Cost", width=12, style="currency"),
    ]
    sheet = wb.new_sheet("Results", columns)
    for row in data:
        style = Styles.danger() if row["status"] == "unused" else None
        sheet.add_row(
            [row["account"], row["region"], row["resource"], row["status"], row["cost"]],
            style=style,
        )
    return wb

def run(ctx) -> None:
    results = parallel_collect(ctx, _collect_and_analyze, service="ec2")
    flat_data = results.get_flat_data()

    if not flat_data:
        console.print("[yellow]분석 결과 없음[/yellow]")
        return

    # 출력 경로 (1줄)
    output_path = create_output_path(ctx, "ec2", "unused")

    # Excel + HTML 동시 생성
    report_paths = generate_dual_report(
        ctx,
        data=flat_data,
        output_dir=output_path,
        prefix="EC2_Unused",
        excel_builder=lambda: _build_excel(results, flat_data),
        html_config={
            "title": "EC2 미사용 인스턴스 분석",
            "service": "EC2",
            "tool_name": "unused",
            "total": total_count,
            "found": unused_count,
            "savings": total_savings,
        },
    )

    # 표준 완료 메시지
    print_report_complete(report_paths)
    open_in_explorer(output_path)
```

### 커스텀 HTML이 필요한 경우

복잡한 차트/섹션이 필요하면 `html_builder` 파라미터를 사용:

```python
def _build_html(output_dir: str) -> str:
    """커스텀 HTML 빌더 (output_dir -> filepath)"""
    from core.shared.io.html import HTMLReport
    report = HTMLReport(title="Custom Report")
    report.add_summary({"total": 100, "found": 10})
    report.add_pie_chart("Distribution", labels, values)
    report.add_table("Details", headers, rows)
    filepath = f"{output_dir}/custom_report.html"
    report.save(filepath, auto_open=False)
    return filepath

report_paths = generate_dual_report(
    ctx,
    data=flat_data,
    output_dir=output_path,
    prefix="EC2_Unused",
    excel_builder=lambda: _build_excel(results, flat_data),
    html_builder=_build_html,  # html_config 대신 사용
)
```

## 대안 패턴: generate_reports()

기존 플러그인의 Excel 생성 함수를 래핑하는 경우:

```python
from core.shared.io.compat import generate_reports

report_paths = generate_reports(
    ctx,
    data=flat_data,
    excel_generator=lambda d: _save_excel(results, d),
    html_config={
        "title": "EC2 미사용 인스턴스 분석",
        "service": "EC2",
        "tool_name": "unused",
    },
    output_dir=output_path,
)
```

## 출력 경로 헬퍼

```python
from core.shared.io.output.helpers import create_output_path, get_context_identifier

# 6줄 → 1줄
output_path = create_output_path(ctx, "ec2", "unused")
# 결과: output/{profile}/ec2/unused/2026-02-07/

# 식별자만 필요한 경우
identifier = get_context_identifier(ctx)
```

## Excel 출력 패턴

### 기본 사용법

```python
from core.shared.io.excel import Workbook, ColumnDef, Styles

# Workbook 생성
wb = Workbook()  # 한국어 (기본)
wb = Workbook(lang="en")  # 영어

# 컬럼 정의
columns = [
    ColumnDef(header="계정", header_en="Account", width=15, style="data"),
    ColumnDef(header="리전", header_en="Region", width=12, style="center"),
    ColumnDef(header="크기(GB)", header_en="Size(GB)", width=10, style="number"),
    ColumnDef(header="비용", header_en="Cost", width=12, style="currency"),
]

# 시트 생성 및 데이터 추가
sheet = wb.new_sheet("분석 결과", columns=columns)

for item in results:
    style = Styles.danger() if item.unused else None
    sheet.add_row([item.account, item.region, item.size, item.cost], style=style)

# 요약 행
sheet.add_summary_row(["합계", "", total_size, total_cost])

# 저장
wb.save_as(output_dir, prefix="EC2_Unused", region="ap-northeast-2")
```

### 스타일 타입

| style | 설명 | 정렬 |
|-------|------|------|
| `data` | 일반 텍스트 (기본) | 왼쪽, 줄바꿈 |
| `center` | 중앙 정렬 | 중앙, 줄바꿈 |
| `number` | 정수 (1,234) | 오른쪽 |
| `currency` | 통화 ($1,234.56) | 오른쪽 |
| `percent` | 백분율 (12.34%) | 오른쪽 |

### Styles 프리셋

```python
Styles.danger()   # 빨간 배경 + 흰 글씨
Styles.warning()  # 노란 배경
Styles.success()  # 초록 배경
Styles.summary()  # 연노랑 배경 + 볼드 (합계용)
```

### Summary 시트

```python
summary = wb.new_summary_sheet()
summary.add_title("EBS 볼륨 분석 보고서")
summary.add_section("분석 정보")
summary.add_item("분석 일시", "2026-01-23 15:30:00")
summary.add_item("계정 수", "5개")
summary.add_section("분석 결과")
summary.add_item("미사용 볼륨", 23, highlight="danger")
summary.add_item("월간 예상 비용", "$1,234.56", highlight="warning")
```

## HTML 출력 패턴

### HTMLReport (커스텀 차트)

```python
from core.shared.io.html import HTMLReport

report = HTMLReport(title="EC2 미사용 리소스 분석")
report.add_summary({"total": 150, "found": 23, "savings": 1234.56})
report.add_pie_chart("계정별 분포", labels, values)
report.add_bar_chart("리전별 분포", labels, values)
report.add_table("리소스 상세", headers, rows)
report.save("output.html")
```

### AWSReport (자동 시각화)

```python
from core.shared.io.html import create_aws_report

report = create_aws_report(
    title="EC2 미사용",
    service="EC2",
    tool_name="unused",
    ctx=ctx,
    resources=results,  # list[dict]
    total=100,
    found=10,
    savings=500.0,
)
report.save("output.html")
```

### 자동 생성 기능

AWSReport 사용 시 자동 생성:
- 요약 카드 (전체, 발견, 비율, 절감액)
- 계정별 분포 차트 (Pie)
- 리전별 분포 차트 (Bar)
- 상태별 분포 차트 (있는 경우)
- 리소스 상세 테이블 (검색, 정렬, 페이지네이션)

## 콘솔 출력 스타일 가이드

### 표준 심볼 (이모지 사용 금지)

```python
from core.cli.ui import (
    SYMBOL_SUCCESS,   # ✓ - 완료
    SYMBOL_ERROR,     # ✗ - 에러
    SYMBOL_WARNING,   # ! - 경고
    SYMBOL_INFO,      # • - 정보
    SYMBOL_PROGRESS,  # • - 진행 중
)
```

### 표준 출력 함수

```python
from core.cli.ui import (
    print_success,      # [green]✓ 메시지[/green]
    print_error,        # [red]✗ 메시지[/red]
    print_warning,      # [yellow]! 메시지[/yellow]
    print_info,         # [blue]• 메시지[/blue]
    print_step_header,  # [bold cyan]Step N: 메시지[/bold cyan]
)
```

### 완료 메시지

```python
from core.shared.io.output import print_report_complete

# 단일 경로
print_report_complete("/output/path/report.xlsx")

# 멀티 경로 (generate_dual_report 반환값)
print_report_complete({"excel": "report.xlsx", "html": "report.html"})
```

### 금지 사항

- **이모지 사용 금지**: `📊`, `🔍`, `⏰`, `🚀` 등
- **이모지 체크마크 금지**: `✅`, `❌` → `✓`, `✗` 사용
- **이모지 경고 금지**: `⚠️` → `!` 사용

## 참조

- `shared/io/config.py` - OutputConfig, OutputFormat
- `shared/io/compat.py` - generate_reports, generate_dual_report
- `shared/io/excel/workbook.py` - Workbook, Sheet, ColumnDef
- `shared/io/html/report.py` - HTMLReport
- `shared/io/html/aws_report.py` - AWSReport, create_aws_report
- `shared/io/output/helpers.py` - create_output_path, get_context_identifier
- `shared/io/output/builder.py` - OutputPath, print_report_complete
