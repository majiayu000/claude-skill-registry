---
name: gcp-iam
description: "GCP IAM 서비스 계정 및 권한 관리"
---

# GCP IAM Management

서비스 계정 생성, 역할 부여, 키 관리를 수행합니다.

## 사용법

```
/gcp-iam                           # 서비스 계정 목록
/gcp-iam create my-service         # 서비스 계정 생성
/gcp-iam grant viewer              # 역할 부여
/gcp-iam key my-service            # JSON 키 생성
```

## Workflow

### 1. 서비스 계정 목록

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud iam service-accounts list --project=$PROJECT_ID \
  --format="table(email,displayName,disabled)"
```

### 2. 서비스 계정 생성

```bash
gcloud iam service-accounts create SA_NAME \
  --display-name="SA_DISPLAY_NAME" \
  --description="Description" \
  --project=$PROJECT_ID
```

### 3. 역할 부여

```bash
# 프로젝트 수준 역할
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:SA_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# 여러 역할 부여
for role in roles/storage.objectViewer roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:SA_EMAIL" \
    --role="$role"
done
```

### 4. 역할 제거

```bash
gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/ROLE_NAME"
```

### 5. JSON 키 생성

```bash
gcloud iam service-accounts keys create ./sa-key.json \
  --iam-account=SA_EMAIL
```

### 6. 서비스 계정 삭제

```bash
gcloud iam service-accounts delete SA_EMAIL
```

## 자주 쓰는 역할

### 조회 전용

| 역할 | 설명 |
|------|------|
| `roles/viewer` | 프로젝트 전체 읽기 |
| `roles/storage.objectViewer` | Storage 객체 읽기 |
| `roles/bigquery.dataViewer` | BigQuery 데이터 읽기 |
| `roles/logging.viewer` | 로그 읽기 |

### 쓰기 포함

| 역할 | 설명 |
|------|------|
| `roles/editor` | 프로젝트 전체 편집 |
| `roles/storage.objectAdmin` | Storage 객체 관리 |
| `roles/cloudsql.client` | Cloud SQL 접속 |
| `roles/secretmanager.secretAccessor` | Secret 읽기 |

### Cloud Run / Functions

| 역할 | 설명 |
|------|------|
| `roles/run.invoker` | Cloud Run 호출 |
| `roles/cloudfunctions.invoker` | Functions 호출 |
| `roles/run.admin` | Cloud Run 관리 |

## 출력 형식

```
## 서비스 계정 목록

| 이메일 | 이름 | 상태 |
|--------|------|------|
| my-sa@project.iam.gserviceaccount.com | My Service Account | 활성 |
| compute@...gserviceaccount.com | Compute Engine SA | 활성 |

---

### my-sa@project.iam.gserviceaccount.com 역할

| 역할 | 범위 |
|------|------|
| roles/storage.objectViewer | 프로젝트 |
| roles/logging.logWriter | 프로젝트 |
```

## 현재 계정의 역할 확인

```bash
# 프로젝트 IAM 정책 조회
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --format="table(bindings.role)" \
  --filter="bindings.members:SA_EMAIL"
```

## 모범 사례

1. **최소 권한**: 필요한 역할만 부여
2. **서비스 계정 분리**: 용도별로 별도 생성
3. **키 관리**:
   - 가능하면 키 대신 Workload Identity 사용
   - 키는 90일마다 순환
4. **비활성화**: 미사용 계정은 비활성화 후 삭제

## 주의사항

- `roles/owner`는 부여하지 않음 (보안 위험)
- JSON 키는 안전하게 보관 (Git 커밋 금지!)
- 키 유출 시 즉시 삭제 후 재생성
