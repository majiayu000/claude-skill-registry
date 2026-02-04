---
name: gcp-billing
description: "GCP Billing 조회"
---

# GCP Billing 조회

결제 계정의 프로젝트별/서비스별 비용을 조회합니다.

## 사용법

```
/gcp-billing                    # 기본 Billing Export 프로젝트 사용
/gcp-billing my-project-id      # 특정 프로젝트의 Billing Export 사용
```

## 설정

Billing Export 프로젝트와 데이터셋을 확인:
- 기본값: `patent-481206` (context.md 참조)
- 데이터셋: `billing_export.gcp_billing_export_v1_*`

## 실행할 쿼리

### 프로젝트별 비용 (최근 30일)

```bash
BILLING_PROJECT=${1:-patent-481206}

bq query --project_id=$BILLING_PROJECT --use_legacy_sql=false "
SELECT
  project.id AS project_id,
  project.name AS project_name,
  ROUND(SUM(cost), 2) AS total_cost,
  currency
FROM \`$BILLING_PROJECT.billing_export.gcp_billing_export_v1_*\`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY project.id, project.name, currency
ORDER BY total_cost DESC
"
```

### 서비스별 비용 (최근 30일)

```bash
bq query --project_id=$BILLING_PROJECT --use_legacy_sql=false "
SELECT
  service.description AS service,
  ROUND(SUM(cost), 2) AS total_cost,
  currency
FROM \`$BILLING_PROJECT.billing_export.gcp_billing_export_v1_*\`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY service.description, currency
ORDER BY total_cost DESC
LIMIT 20
"
```

### 일별 비용 추이 (최근 7일)

```bash
bq query --project_id=$BILLING_PROJECT --use_legacy_sql=false "
SELECT
  DATE(usage_start_time) AS date,
  ROUND(SUM(cost), 2) AS daily_cost
FROM \`$BILLING_PROJECT.billing_export.gcp_billing_export_v1_*\`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY date
ORDER BY date DESC
"
```

## 출력 형식

```
## 비용 현황

### 프로젝트별 비용 (30일)
| 프로젝트 | 비용 |
|----------|------|

### 서비스별 비용 (30일)
| 서비스 | 비용 |
|--------|------|

### 일별 추이 (7일)
| 날짜 | 비용 |
|------|------|

---
총 비용: $XX.XX
```

## 관련 스킬

| 스킬 | 용도 |
|------|------|
| `/gcp-billing-accounts` | 결제 계정 목록 |
| `/gcp-billing-projects` | 계정별 프로젝트 |
| `/gcp-usage` | API 사용량 조회 |
