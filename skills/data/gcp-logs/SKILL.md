---
name: gcp-logs
description: "GCP Cloud Logging 로그 조회/필터링"
---

# GCP Cloud Logging

Cloud Logging에서 로그를 조회하고 필터링합니다.

## 사용법

```
/gcp-logs                          # 최근 로그 조회
/gcp-logs errors                   # 에러 로그만 조회
/gcp-logs my-vm                    # 특정 VM 로그
/gcp-logs --service cloudrun       # Cloud Run 로그
```

## Workflow

### 1. 기본 로그 조회

```bash
PROJECT_ID=$(gcloud config get-value project)

# 최근 로그 (기본 100개)
gcloud logging read --project=$PROJECT_ID --limit=100 \
  --format="table(timestamp,severity,resource.type,textPayload)"

# 최근 1시간
gcloud logging read --project=$PROJECT_ID \
  --freshness=1h \
  --limit=100
```

### 2. 에러 로그 필터링

```bash
# ERROR 이상
gcloud logging read 'severity>=ERROR' \
  --project=$PROJECT_ID \
  --limit=50 \
  --format="table(timestamp,severity,resource.type,textPayload)"

# 특정 시간 범위
gcloud logging read 'severity>=ERROR AND timestamp>="2024-01-15T00:00:00Z"' \
  --project=$PROJECT_ID \
  --limit=100
```

### 3. 리소스별 로그

```bash
# VM 인스턴스
gcloud logging read 'resource.type="gce_instance" AND resource.labels.instance_id="INSTANCE_ID"' \
  --project=$PROJECT_ID \
  --limit=100

# Cloud Run
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="SERVICE_NAME"' \
  --project=$PROJECT_ID \
  --limit=100

# Cloud Functions
gcloud logging read 'resource.type="cloud_function" AND resource.labels.function_name="FUNCTION_NAME"' \
  --project=$PROJECT_ID \
  --limit=100

# Kubernetes (GKE)
gcloud logging read 'resource.type="k8s_container" AND resource.labels.cluster_name="CLUSTER_NAME"' \
  --project=$PROJECT_ID \
  --limit=100
```

### 4. 텍스트 검색

```bash
# 특정 텍스트 포함
gcloud logging read 'textPayload:"error" OR jsonPayload.message:"error"' \
  --project=$PROJECT_ID \
  --limit=50

# 정규식 (RE2)
gcloud logging read 'textPayload=~"Exception.*failed"' \
  --project=$PROJECT_ID \
  --limit=50
```

### 5. JSON 로그 필터

```bash
# JSON 필드 필터
gcloud logging read 'jsonPayload.level="error"' \
  --project=$PROJECT_ID \
  --limit=50

# 중첩 필드
gcloud logging read 'jsonPayload.request.status>=500' \
  --project=$PROJECT_ID \
  --limit=50
```

### 6. 실시간 로그 스트리밍

```bash
# tail -f 스타일
gcloud logging tail --project=$PROJECT_ID

# 필터와 함께
gcloud logging tail 'severity>=WARNING' --project=$PROJECT_ID
```

## 자주 쓰는 필터

| 용도 | 필터 |
|------|------|
| 에러만 | `severity>=ERROR` |
| 경고 이상 | `severity>=WARNING` |
| 특정 시간 이후 | `timestamp>="2024-01-15T00:00:00Z"` |
| 최근 1시간 | `timestamp>="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ)"` |
| HTTP 500 에러 | `httpRequest.status>=500` |
| 특정 사용자 | `protoPayload.authenticationInfo.principalEmail="user@example.com"` |

## 출력 형식

```
## 로그 조회 결과

### 에러 로그 (최근 1시간)

| 시간 | 심각도 | 리소스 | 메시지 |
|------|--------|--------|--------|
| 14:32:15 | ERROR | cloud_run_revision | Connection refused |
| 14:28:03 | ERROR | gce_instance | Out of memory |
| 14:15:22 | WARNING | cloud_function | Timeout approaching |

---
총 3개 이벤트

### 필터 조건
\`\`\`
severity>=WARNING AND timestamp>="2024-01-15T13:00:00Z"
\`\`\`
```

## 로그 내보내기

```bash
# BigQuery로 내보내기 (싱크 생성)
gcloud logging sinks create my-sink \
  bigquery.googleapis.com/projects/$PROJECT_ID/datasets/logs \
  --log-filter='severity>=ERROR'

# Cloud Storage로 내보내기
gcloud logging sinks create my-sink \
  storage.googleapis.com/my-log-bucket \
  --log-filter='resource.type="gce_instance"'
```

## 로그 기반 메트릭 생성

```bash
# 에러 카운트 메트릭
gcloud logging metrics create error-count \
  --description="Count of error logs" \
  --log-filter='severity>=ERROR'
```

## 비용

| 항목 | 무료 티어 | 초과 시 |
|------|-----------|---------|
| 수집 | 50GB/월 | $0.50/GB |
| 보관 (30일) | 무료 | - |
| 보관 (30일+) | - | $0.01/GB/월 |

## 주의사항

- 기본 보관 기간: 30일
- 대용량 쿼리는 BigQuery 익스포트 권장
- 민감 정보 로깅 주의 (PII, 비밀번호 등)
