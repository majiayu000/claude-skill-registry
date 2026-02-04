---
name: gcp-usage
description: "GCP API 사용량 조회"
---

# GCP API 사용량 조회

프로젝트의 API 사용량을 조회합니다.

## 사용법

```
/gcp-usage                      # 기본 Billing Export 프로젝트 사용
/gcp-usage my-project-id        # 특정 프로젝트의 Billing Export 사용
/gcp-usage --realtime my-proj   # Cloud Logging 실시간 조회
```

## 설정

Billing Export 프로젝트와 데이터셋을 확인:
- 기본값: `patent-481206` (context.md 참조)
- 데이터셋: `billing_export.gcp_billing_export_v1_*`

## 실행할 쿼리

### SKU별 사용량 (Billing Export 기반)

```bash
BILLING_PROJECT=${1:-patent-481206}

bq query --project_id=$BILLING_PROJECT --use_legacy_sql=false "
SELECT
  service.description AS service,
  sku.description AS sku,
  ROUND(SUM(usage.amount), 2) AS usage_amount,
  usage.unit AS unit,
  ROUND(SUM(cost), 4) AS cost
FROM \`$BILLING_PROJECT.billing_export.gcp_billing_export_v1_*\`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND usage.amount > 0
GROUP BY service.description, sku.description, usage.unit
ORDER BY cost DESC
LIMIT 30
"
```

### 프로젝트별 API 사용량

```bash
bq query --project_id=$BILLING_PROJECT --use_legacy_sql=false "
SELECT
  project.id AS project_id,
  service.description AS service,
  ROUND(SUM(usage.amount), 2) AS usage_amount,
  usage.unit AS unit
FROM \`$BILLING_PROJECT.billing_export.gcp_billing_export_v1_*\`
WHERE DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND usage.amount > 0
GROUP BY project.id, service.description, usage.unit
ORDER BY usage_amount DESC
LIMIT 30
"
```

### Cloud Logging에서 API 호출 확인 (실시간)

```bash
# 특정 프로젝트의 최근 API 호출 로그
TARGET_PROJECT=${1:-$(gcloud config get-value project)}

gcloud logging read 'resource.type="audited_resource"' \
  --project=$TARGET_PROJECT \
  --limit=50 \
  --format='table(timestamp,protoPayload.methodName,protoPayload.status.code)'
```

## 출력 형식

```
## API 사용량 현황

### SKU별 사용량 (7일)
| 서비스 | SKU | 사용량 | 단위 | 비용 |
|--------|-----|--------|------|------|

### 프로젝트별 사용량
| 프로젝트 | 서비스 | 사용량 | 단위 |
|----------|--------|--------|------|

---
주요 사용: [가장 많이 사용된 서비스/API 요약]
```

## 관련 스킬

| 스킬 | 용도 |
|------|------|
| `/gcp-billing` | 비용 분석 |
| `/gcp-billing-accounts` | 결제 계정 목록 |
| `/gcp-project-status` | 프로젝트 리소스 상태 |
