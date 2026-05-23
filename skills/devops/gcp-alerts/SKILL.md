---
name: gcp-alerts
description: "GCP 알림 정책 설정 (비용/에러/성능)"
---

# GCP Alerting Policies

Cloud Monitoring 알림 정책을 설정하고 관리합니다.

## 사용법

```
/gcp-alerts                        # 알림 정책 목록
/gcp-alerts create budget          # 예산 알림 생성
/gcp-alerts create vm-cpu          # VM CPU 알림 생성
/gcp-alerts create error-rate      # 에러율 알림 생성
```

## Workflow

### 0. API 활성화 (최초 1회)

```bash
gcloud services enable monitoring.googleapis.com --project=$PROJECT_ID
```

### 1. 알림 정책 목록

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud alpha monitoring policies list --project=$PROJECT_ID \
  --format="table(displayName,enabled,conditions[0].displayName)"
```

### 2. 알림 채널 설정 (이메일)

```bash
# 이메일 채널 생성
cat > /tmp/email-channel.json << 'EOF'
{
  "type": "email",
  "displayName": "Admin Email",
  "labels": {
    "email_address": "admin@example.com"
  }
}
EOF

gcloud alpha monitoring channels create \
  --channel-content-from-file=/tmp/email-channel.json \
  --project=$PROJECT_ID
```

### 3. VM CPU 알림 정책 생성

```bash
cat > /tmp/cpu-alert.json << 'EOF'
{
  "displayName": "High CPU Usage",
  "conditions": [{
    "displayName": "CPU > 80%",
    "conditionThreshold": {
      "filter": "resource.type = \"gce_instance\" AND metric.type = \"compute.googleapis.com/instance/cpu/utilization\"",
      "comparison": "COMPARISON_GT",
      "thresholdValue": 0.8,
      "duration": "300s",
      "aggregations": [{
        "alignmentPeriod": "60s",
        "perSeriesAligner": "ALIGN_MEAN"
      }]
    }
  }],
  "combiner": "OR",
  "enabled": true,
  "notificationChannels": ["CHANNEL_ID"]
}
EOF

gcloud alpha monitoring policies create \
  --policy-from-file=/tmp/cpu-alert.json \
  --project=$PROJECT_ID
```

### 4. 예산 알림 설정

```bash
# 예산 API 활성화
gcloud services enable billingbudgets.googleapis.com

# 예산 생성 (월 $100, 80% 도달 시 알림)
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Monthly Budget" \
  --budget-amount=100USD \
  --threshold-rules=threshold-percent=0.8,spend-basis=current-spend \
  --threshold-rules=threshold-percent=1.0,spend-basis=current-spend \
  --all-updates-rule-pubsub-topic=projects/$PROJECT_ID/topics/budget-alerts
```

### 5. Cloud Run 에러율 알림

```bash
cat > /tmp/error-alert.json << 'EOF'
{
  "displayName": "Cloud Run Error Rate > 5%",
  "conditions": [{
    "displayName": "Error rate",
    "conditionThreshold": {
      "filter": "resource.type = \"cloud_run_revision\" AND metric.type = \"run.googleapis.com/request_count\" AND metric.labels.response_code_class = \"5xx\"",
      "comparison": "COMPARISON_GT",
      "thresholdValue": 0.05,
      "duration": "60s",
      "aggregations": [{
        "alignmentPeriod": "60s",
        "perSeriesAligner": "ALIGN_RATE"
      }]
    }
  }],
  "combiner": "OR",
  "enabled": true
}
EOF

gcloud alpha monitoring policies create \
  --policy-from-file=/tmp/error-alert.json \
  --project=$PROJECT_ID
```

### 6. 정책 활성화/비활성화

```bash
# 비활성화
gcloud alpha monitoring policies update POLICY_ID \
  --no-enabled \
  --project=$PROJECT_ID

# 활성화
gcloud alpha monitoring policies update POLICY_ID \
  --enabled \
  --project=$PROJECT_ID
```

### 7. 정책 삭제

```bash
gcloud alpha monitoring policies delete POLICY_ID --project=$PROJECT_ID
```

## 자주 쓰는 알림 템플릿

### VM 모니터링

| 알림 | 메트릭 | 임계값 |
|------|--------|--------|
| 높은 CPU | `compute.googleapis.com/instance/cpu/utilization` | > 80% |
| 높은 메모리 | `agent.googleapis.com/memory/percent_used` | > 90% |
| 디스크 부족 | `agent.googleapis.com/disk/percent_used` | > 85% |
| VM 다운 | Uptime Check 실패 | 2회 연속 |

### Cloud Run / Functions

| 알림 | 메트릭 | 임계값 |
|------|--------|--------|
| 에러율 | `5xx / total` | > 5% |
| 지연 시간 | `request_latencies` | p99 > 2s |
| 인스턴스 급증 | `instance_count` | > 50 |

### 비용

| 알림 | 설정 |
|------|------|
| 일일 예산 | threshold 80%, 100% |
| 이상 비용 | 전일 대비 200% 초과 |

## 출력 형식

```
## 알림 정책 목록

| 정책 이름 | 상태 | 조건 |
|-----------|------|------|
| High CPU Usage | 활성 | CPU > 80% for 5분 |
| Error Rate Alert | 활성 | 5xx > 5% for 1분 |
| Monthly Budget | 활성 | $100의 80%, 100% |

---

### 알림 채널

| 채널 | 유형 | 대상 |
|------|------|------|
| Admin Email | email | admin@example.com |
| Slack Webhook | webhook | #alerts |
```

## 알림 채널 유형

| 유형 | 설정 |
|------|------|
| Email | `email_address` |
| Slack | Webhook URL |
| PagerDuty | Integration Key |
| SMS | 전화번호 |
| Pub/Sub | Topic 이름 |

## 비용

- 알림 정책: 무료
- 알림 채널: 무료
- Uptime Check: 무료 (1백만 회/월)

## 주의사항

- 너무 민감한 임계값 설정 시 알림 폭주
- 적절한 duration 설정으로 일시적 스파이크 필터링
- 중요 알림은 여러 채널로 발송 권장
