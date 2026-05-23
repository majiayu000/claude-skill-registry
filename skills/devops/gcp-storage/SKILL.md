---
name: gcp-storage
description: "GCP Cloud Storage 버킷 관리"
---

# GCP Cloud Storage

Cloud Storage 버킷을 생성, 조회, 관리합니다.

## 사용법

```
/gcp-storage                       # 버킷 목록 조회
/gcp-storage create my-bucket      # 버킷 생성
/gcp-storage ls my-bucket          # 버킷 내용 조회
/gcp-storage upload file.txt gs://my-bucket/  # 업로드
```

## Workflow

### 1. 버킷 목록 조회

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud storage buckets list --project=$PROJECT_ID \
  --format="table(name,location,storageClass,timeCreated.date())"
```

### 2. 버킷 생성

```bash
# 기본 생성 (멀티 리전)
gcloud storage buckets create gs://BUCKET_NAME --project=$PROJECT_ID

# 리전 지정 (비용 절감)
gcloud storage buckets create gs://BUCKET_NAME \
  --project=$PROJECT_ID \
  --location=asia-northeast3 \
  --default-storage-class=STANDARD

# 저비용 아카이브
gcloud storage buckets create gs://BUCKET_NAME \
  --project=$PROJECT_ID \
  --location=asia-northeast3 \
  --default-storage-class=NEARLINE
```

### 3. 버킷 내용 조회

```bash
# 목록
gcloud storage ls gs://BUCKET_NAME/

# 상세 (크기 포함)
gcloud storage ls -l gs://BUCKET_NAME/

# 재귀적
gcloud storage ls -r gs://BUCKET_NAME/
```

### 4. 파일 업로드/다운로드

```bash
# 단일 파일 업로드
gcloud storage cp LOCAL_FILE gs://BUCKET_NAME/

# 디렉토리 업로드
gcloud storage cp -r LOCAL_DIR gs://BUCKET_NAME/

# 다운로드
gcloud storage cp gs://BUCKET_NAME/FILE LOCAL_PATH

# 동기화 (rsync)
gcloud storage rsync LOCAL_DIR gs://BUCKET_NAME/DIR
```

### 5. 버킷 삭제

```bash
# 빈 버킷 삭제
gcloud storage buckets delete gs://BUCKET_NAME

# 내용 포함 삭제 (주의!)
gcloud storage rm -r gs://BUCKET_NAME
```

## 스토리지 클래스

| 클래스 | 용도 | 최소 보관 | 비용 (GB/월) |
|--------|------|-----------|--------------|
| STANDARD | 자주 접근 | 없음 | $0.023 |
| NEARLINE | 월 1회 미만 | 30일 | $0.013 |
| COLDLINE | 분기 1회 미만 | 90일 | $0.006 |
| ARCHIVE | 연 1회 미만 | 365일 | $0.0025 |

## 출력 형식

```
## Cloud Storage 버킷 목록

| 버킷 이름 | 위치 | 클래스 | 생성일 |
|-----------|------|--------|--------|
| my-project-data | asia-northeast3 | STANDARD | 2024-01-15 |
| my-project-backup | asia | NEARLINE | 2024-02-01 |

---
총 2개 버킷
```

## 유용한 명령어

```bash
# 버킷 용량 확인
gcloud storage du -s gs://BUCKET_NAME/

# 공개 설정 (정적 웹사이트)
gcloud storage buckets add-iam-policy-binding gs://BUCKET_NAME \
  --member=allUsers \
  --role=roles/storage.objectViewer

# 수명 주기 설정 (30일 후 삭제)
cat > lifecycle.json << 'EOF'
{
  "rule": [{
    "action": {"type": "Delete"},
    "condition": {"age": 30}
  }]
}
EOF
gcloud storage buckets update gs://BUCKET_NAME --lifecycle-file=lifecycle.json
```

## 주의사항

- 버킷 이름은 전역 고유 (다른 프로젝트와 중복 불가)
- 삭제된 버킷은 복구 불가
- 대용량 전송 시 `gsutil -m` 또는 Transfer Service 권장
