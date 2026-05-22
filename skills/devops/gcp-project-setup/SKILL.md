---
name: gcp-project-setup
description: "GCP 프로젝트 생성부터 결제 계정 연결, API 활성화까지 원스텝 자동화. 트리거: GCP 프로젝트 만들어줘, 새 프로젝트 생성, 프로젝트 셋업해줘, GCP 프로젝트 설정"
---

# GCP Project Setup

GCP 프로젝트 생성 → 결제 계정 연결 → API 활성화를 순차적으로 수행.

## Workflow

### 1. 정보 수집

```
필수:
- 프로젝트 ID (전역 고유, 영문 소문자/숫자/하이픈, 6-30자)
- 프로젝트 이름 (표시용)

선택:
- 용도 (결제 계정 선택 참고)
- 활성화할 API 목록
```

### 2. 조직 확인

```bash
gcloud organizations list
```

조직이 있으면 `--organization=ORG_ID` 옵션 사용.

### 3. 프로젝트 생성

```bash
# 조직 있는 경우
gcloud projects create PROJECT_ID --name="PROJECT_NAME" --organization=ORG_ID

# 조직 없는 경우
gcloud projects create PROJECT_ID --name="PROJECT_NAME"
```

### 4. 결제 계정 연결

```bash
# 사용 가능한 결제 계정 조회
gcloud billing accounts list

# 연결
gcloud billing projects link PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

### 5. API 활성화 (선택)

용도별 권장 API:

| 용도 | API |
|------|-----|
| VM | `compute.googleapis.com` |
| 스토리지 | `storage.googleapis.com` |
| Cloud Run | `run.googleapis.com` |
| Cloud Functions | `cloudfunctions.googleapis.com` |

```bash
gcloud services enable API_NAME --project=PROJECT_ID
```

### 6. 기본 프로젝트 설정

```bash
gcloud config set project PROJECT_ID
```

## 출력 형식

```
| 항목 | 값 |
|------|-----|
| 프로젝트 ID | xxx |
| 프로젝트 이름 | xxx |
| 조직 | xxx |
| 결제 계정 | xxx |
| 활성화된 API | xxx |
| 기본 프로젝트 | ✅ 설정됨 |
```

## 에러 처리

| 에러 | 해결 |
|------|------|
| `project ID is already in use` | 다른 프로젝트 ID 제안 |
| `does not have permission` | 현재 계정 권한 확인, 조직 관리자 권한으로 해결 |
| `Reauthentication failed` | `gcloud auth login` 실행 안내 |
