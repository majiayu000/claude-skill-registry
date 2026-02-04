---
name: gcp-project-status
description: "GCP 프로젝트 상태 조회"
---

# GCP 프로젝트 상태 조회

현재 프로젝트의 리소스 및 상태를 종합적으로 조회합니다.

## 조회 항목

1. VM 인스턴스
2. 디스크
3. 활성화된 API
4. 방화벽 규칙
5. 서비스 계정
6. Storage 버킷
7. 외부 IP
8. API 키

## 실행할 명령어

```bash
# 현재 프로젝트 확인
PROJECT_ID=$(gcloud config get-value project)

# 병렬 조회
gcloud compute instances list --project=$PROJECT_ID
gcloud compute disks list --project=$PROJECT_ID
gcloud services list --enabled --project=$PROJECT_ID
gcloud compute firewall-rules list --project=$PROJECT_ID
gcloud iam service-accounts list --project=$PROJECT_ID
gcloud storage buckets list --project=$PROJECT_ID
gcloud compute addresses list --project=$PROJECT_ID
gcloud services api-keys list --project=$PROJECT_ID
```

## 출력 형식

조회 결과를 다음 형식으로 정리:

```
## [PROJECT_ID] 프로젝트 상태

### VM 인스턴스
| 이름 | 존 | 타입 | 내부 IP | 외부 IP | 상태 |
|------|-----|------|---------|---------|------|

### 디스크
| 이름 | 위치 | 크기 | 타입 | 상태 |
|------|------|------|------|------|

### 활성화된 API
| 주요 API | 용도 |
|----------|------|

### 방화벽 규칙
| 규칙 | 포트 | 용도 |
|------|------|------|

### 서비스 계정
| 이름 | 상태 |
|------|------|

### 기타
| 항목 | 상태 |
|------|------|
| Storage 버킷 | X개 / 없음 |
| 외부 고정 IP | X개 / 없음 |
| API 키 | X개 / 없음 |

---
**요약:** [리소스 현황 및 주요 포인트]
```

## 옵션

프로젝트 ID를 인자로 받으면 해당 프로젝트 조회:

```
/gcp-project-status patent-481206
```
