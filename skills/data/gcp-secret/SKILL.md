---
name: gcp-secret
description: "GCP Secret Manager 조회/추가/관리"
---

# GCP Secret Manager

Secret Manager를 사용하여 비밀(API 키, 비밀번호 등)을 안전하게 관리합니다.

## 사용법

```
/gcp-secret                        # 시크릿 목록 조회
/gcp-secret get my-api-key         # 시크릿 값 조회
/gcp-secret create my-secret       # 새 시크릿 생성
/gcp-secret update my-secret       # 시크릿 값 업데이트
```

## Workflow

### 0. API 활성화 (최초 1회)

```bash
gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID
```

### 1. 시크릿 목록 조회

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud secrets list --project=$PROJECT_ID \
  --format="table(name.basename(),createTime.date(),replication.automatic)"
```

### 2. 시크릿 생성

```bash
# 빈 시크릿 생성
gcloud secrets create SECRET_NAME --project=$PROJECT_ID

# 값과 함께 생성
echo -n "my-secret-value" | gcloud secrets create SECRET_NAME \
  --data-file=- \
  --project=$PROJECT_ID

# 파일에서 생성
gcloud secrets create SECRET_NAME \
  --data-file=./secret.txt \
  --project=$PROJECT_ID
```

### 3. 시크릿 값 조회

```bash
# 최신 버전
gcloud secrets versions access latest --secret=SECRET_NAME

# 특정 버전
gcloud secrets versions access 1 --secret=SECRET_NAME
```

### 4. 시크릿 버전 추가 (업데이트)

```bash
echo -n "new-secret-value" | gcloud secrets versions add SECRET_NAME --data-file=-
```

### 5. 버전 목록 조회

```bash
gcloud secrets versions list SECRET_NAME \
  --format="table(name.basename(),state,createTime.date())"
```

### 6. 시크릿 삭제

```bash
# 버전 비활성화
gcloud secrets versions disable 1 --secret=SECRET_NAME

# 시크릿 전체 삭제
gcloud secrets delete SECRET_NAME
```

## 출력 형식

```
## Secret Manager 목록

| 시크릿 이름 | 생성일 | 버전 수 |
|-------------|--------|---------|
| api-key-prod | 2024-01-15 | 3 |
| db-password | 2024-01-10 | 1 |
| oauth-secret | 2024-02-01 | 2 |

---
총 3개 시크릿

### api-key-prod 버전

| 버전 | 상태 | 생성일 |
|------|------|--------|
| 3 | ENABLED | 2024-02-15 |
| 2 | DISABLED | 2024-01-20 |
| 1 | DESTROYED | 2024-01-15 |
```

## 애플리케이션에서 사용

### Python

```python
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
response = client.access_secret_version(request={"name": name})
secret_value = response.payload.data.decode("UTF-8")
```

### Cloud Run 환경변수로 마운트

```bash
gcloud run deploy SERVICE_NAME \
  --set-secrets=API_KEY=api-key-prod:latest
```

### VM에서 접근

```bash
# gcloud로 직접 접근
gcloud secrets versions access latest --secret=SECRET_NAME

# 서비스 계정에 권한 부여 필요
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/secretmanager.secretAccessor"
```

## 비용

| 항목 | 비용 |
|------|------|
| 활성 시크릿 버전 | $0.06/월 |
| 액세스 | $0.03/10,000회 |
| 순환 작업 | 무료 |

## 모범 사례

1. **버전 관리**: 이전 버전은 비활성화 후 삭제
2. **자동 순환**: 정기적으로 시크릿 값 변경
3. **최소 권한**: `secretAccessor` 역할만 부여
4. **감사 로그**: Cloud Audit Logs로 접근 모니터링

## 주의사항

- 시크릿 값은 로그에 남기지 않음
- 삭제된 버전은 복구 불가
- 시크릿 이름은 변경 불가 (삭제 후 재생성)
