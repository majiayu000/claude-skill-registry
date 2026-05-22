---
name: gcp-functions
description: "GCP Cloud Functions 배포/관리"
---

# GCP Cloud Functions

Cloud Functions를 배포하고 관리합니다.

## 사용법

```
/gcp-functions                     # 함수 목록 조회
/gcp-functions deploy my-func      # 함수 배포
/gcp-functions logs my-func        # 로그 조회
/gcp-functions delete my-func      # 함수 삭제
```

## Workflow

### 0. API 활성화 (최초 1회)

```bash
gcloud services enable cloudfunctions.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
```

### 1. 함수 목록 조회

```bash
PROJECT_ID=$(gcloud config get-value project)
REGION=asia-northeast3

# Gen 2 (권장)
gcloud functions list --project=$PROJECT_ID --gen2 \
  --format="table(name.basename(),state,runtime,updateTime.date())"

# Gen 1
gcloud functions list --project=$PROJECT_ID \
  --format="table(name,status,runtime,updateTime.date())"
```

### 2. HTTP 함수 배포 (Gen 2)

```bash
# 현재 디렉토리에서 배포
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=python311 \
  --region=$REGION \
  --source=. \
  --entry-point=main \
  --trigger-http \
  --allow-unauthenticated

# 환경변수 설정
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=nodejs20 \
  --region=$REGION \
  --source=. \
  --entry-point=handler \
  --trigger-http \
  --set-env-vars="API_KEY=xxx,DEBUG=true"
```

### 3. 이벤트 트리거 함수

```bash
# Pub/Sub 트리거
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=python311 \
  --region=$REGION \
  --source=. \
  --entry-point=process_message \
  --trigger-topic=TOPIC_NAME

# Cloud Storage 트리거
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=python311 \
  --region=$REGION \
  --source=. \
  --entry-point=process_file \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=BUCKET_NAME"
```

### 4. 함수 설정 업데이트

```bash
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --region=$REGION \
  --memory=256MB \
  --timeout=60s \
  --min-instances=0 \
  --max-instances=100
```

### 5. 로그 조회

```bash
gcloud functions logs read FUNCTION_NAME \
  --region=$REGION \
  --gen2 \
  --limit=50
```

### 6. 함수 호출 (테스트)

```bash
# HTTP 함수
curl $(gcloud functions describe FUNCTION_NAME --gen2 --region=$REGION --format='value(url)')

# 데이터와 함께
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}' \
  $(gcloud functions describe FUNCTION_NAME --gen2 --region=$REGION --format='value(url)')
```

### 7. 함수 삭제

```bash
gcloud functions delete FUNCTION_NAME --region=$REGION --gen2
```

## 런타임 지원

| 런타임 | 버전 |
|--------|------|
| Python | python311, python312 |
| Node.js | nodejs18, nodejs20 |
| Go | go121, go122 |
| Java | java17, java21 |
| Ruby | ruby32 |

## 출력 형식

```
## Cloud Functions 목록

| 함수 이름 | 상태 | 런타임 | 트리거 | 업데이트 |
|-----------|------|--------|--------|----------|
| process-order | ACTIVE | python311 | HTTP | 2024-01-15 |
| send-email | ACTIVE | nodejs20 | Pub/Sub | 2024-02-01 |

---

### process-order 상세

| 항목 | 값 |
|------|-----|
| URL | https://xxx.cloudfunctions.net/process-order |
| 리전 | asia-northeast3 |
| 메모리 | 256MB |
| 타임아웃 | 60s |
| 최대 인스턴스 | 100 |
```

## 샘플 코드

### Python (main.py)

```python
import functions_framework

@functions_framework.http
def main(request):
    name = request.args.get('name', 'World')
    return f'Hello, {name}!'
```

### Node.js (index.js)

```javascript
exports.handler = (req, res) => {
  const name = req.query.name || 'World';
  res.send(`Hello, ${name}!`);
};
```

## Gen 1 vs Gen 2

| 기능 | Gen 1 | Gen 2 |
|------|-------|-------|
| 기반 | Cloud Functions | Cloud Run |
| 최대 타임아웃 | 9분 | 60분 |
| 최대 메모리 | 8GB | 32GB |
| 동시성 | 1 | 1000 |
| 가격 | 조금 저렴 | 유연 |

## 비용 (Gen 2)

| 리소스 | 무료 티어 | 초과 시 |
|--------|-----------|---------|
| 호출 | 200만/월 | $0.40/100만 |
| 컴퓨팅 | 400,000 GB-초/월 | $0.0000025/100ms |
| 네트워크 | 5GB/월 | $0.12/GB |

## 주의사항

- Gen 2 권장 (새 프로젝트)
- 콜드 스타트 시간 고려
- 로컬 테스트: `functions-framework` 사용
