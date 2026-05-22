---
name: gcp-cloudrun
description: "GCP Cloud Run 서비스 배포/관리"
---

# GCP Cloud Run

Cloud Run 서비스를 배포하고 관리합니다.

## 사용법

```
/gcp-cloudrun                      # 서비스 목록 조회
/gcp-cloudrun deploy my-service    # 서비스 배포
/gcp-cloudrun logs my-service      # 로그 조회
/gcp-cloudrun traffic my-service   # 트래픽 분배
```

## Workflow

### 0. API 활성화 (최초 1회)

```bash
gcloud services enable run.googleapis.com --project=$PROJECT_ID
```

### 1. 서비스 목록 조회

```bash
PROJECT_ID=$(gcloud config get-value project)
REGION=asia-northeast3

gcloud run services list --project=$PROJECT_ID --region=$REGION \
  --format="table(metadata.name,status.url,status.traffic[0].percent,metadata.creationTimestamp.date())"
```

### 2. 소스에서 직접 배포

```bash
# 현재 디렉토리의 Dockerfile 사용
gcloud run deploy SERVICE_NAME \
  --source=. \
  --region=$REGION \
  --allow-unauthenticated

# 포트 지정
gcloud run deploy SERVICE_NAME \
  --source=. \
  --region=$REGION \
  --port=8080
```

### 3. 컨테이너 이미지 배포

```bash
# Artifact Registry 이미지
gcloud run deploy SERVICE_NAME \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/REPO/IMAGE:TAG \
  --region=$REGION \
  --allow-unauthenticated

# 환경변수 설정
gcloud run deploy SERVICE_NAME \
  --image=IMAGE_URL \
  --region=$REGION \
  --set-env-vars="KEY1=value1,KEY2=value2"

# 시크릿 마운트
gcloud run deploy SERVICE_NAME \
  --image=IMAGE_URL \
  --region=$REGION \
  --set-secrets="API_KEY=my-secret:latest"
```

### 4. 서비스 설정 업데이트

```bash
# 리소스 조정
gcloud run services update SERVICE_NAME \
  --region=$REGION \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --concurrency=80

# 타임아웃
gcloud run services update SERVICE_NAME \
  --region=$REGION \
  --timeout=300
```

### 5. 트래픽 관리

```bash
# 리비전 목록
gcloud run revisions list --service=SERVICE_NAME --region=$REGION

# 특정 리비전으로 100% 트래픽
gcloud run services update-traffic SERVICE_NAME \
  --region=$REGION \
  --to-revisions=REVISION_NAME=100

# 카나리 배포 (90/10)
gcloud run services update-traffic SERVICE_NAME \
  --region=$REGION \
  --to-revisions=OLD_REV=90,NEW_REV=10
```

### 6. 로그 조회

```bash
gcloud run services logs read SERVICE_NAME \
  --region=$REGION \
  --limit=100
```

### 7. 서비스 삭제

```bash
gcloud run services delete SERVICE_NAME --region=$REGION
```

## 출력 형식

```
## Cloud Run 서비스 목록

| 서비스 | URL | 트래픽 | 생성일 |
|--------|-----|--------|--------|
| api-service | https://api-xxx.run.app | 100% | 2024-01-15 |
| web-frontend | https://web-xxx.run.app | 100% | 2024-02-01 |

---

### api-service 상세

| 항목 | 값 |
|------|-----|
| 리전 | asia-northeast3 |
| CPU | 1 |
| 메모리 | 512Mi |
| 최소 인스턴스 | 0 |
| 최대 인스턴스 | 10 |
| 동시성 | 80 |
```

## 비용 최적화

| 설정 | 설명 | 권장 |
|------|------|------|
| `--min-instances=0` | 콜드 스타트 허용, 비용 절감 | 개발/테스트 |
| `--min-instances=1` | 항상 1개 유지, 빠른 응답 | 프로덕션 |
| `--cpu-throttling` | 요청 없을 때 CPU 제한 | 기본값 |
| `--cpu-boost` | 시작 시 CPU 부스트 | 콜드 스타트 개선 |

## 가격 (asia-northeast3)

| 리소스 | 무료 티어 | 초과 시 |
|--------|-----------|---------|
| CPU | 180,000 vCPU-초/월 | $0.0000024/100ms |
| 메모리 | 360,000 GB-초/월 | $0.00000025/100ms |
| 요청 | 200만 요청/월 | $0.40/100만 요청 |

## 주의사항

- 최대 요청 타임아웃: 60분
- 최대 메모리: 32GB
- `--allow-unauthenticated` 없으면 인증 필요
- 콜드 스타트 시간 고려 (--min-instances로 완화)
