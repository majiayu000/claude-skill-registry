---
name: gcp-vm-create
description: "GCP VM 생성 마법사. 용도 기반 사양 추천, VM 생성, 방화벽 설정까지 자동화. 트리거: VM 만들어줘, GCP VM 생성, 서버 하나 띄워줘, 인스턴스 생성"
---

# GCP VM Create

용도 기반 사양 추천 → VM 생성 → 방화벽 설정 자동화.

## Workflow

### 1. 용도 파악

사용자에게 확인:
- 웹/API 서버
- 개발 환경
- 경량 작업 (봇, 스케줄러)
- 데이터베이스
- 기타

### 2. 사양 추천

용도별 추천은 [references/vm-presets.md](references/vm-presets.md) 참조.

### 3. 정보 수집

```
필수:
- VM 이름 (프로젝트 내 고유)
- 프로젝트 ID

선택 (기본값 있음):
- 리전/존: asia-northeast3-a (서울)
- OS: ubuntu-2204-lts
- 머신 타입: 용도별 추천값
- 디스크 크기: 용도별 추천값
```

### 4. API 활성화

```bash
gcloud services enable compute.googleapis.com --project=PROJECT_ID
```

### 5. VM 생성

```bash
gcloud compute instances create VM_NAME \
  --project=PROJECT_ID \
  --zone=ZONE \
  --machine-type=MACHINE_TYPE \
  --image-family=IMAGE_FAMILY \
  --image-project=IMAGE_PROJECT \
  --boot-disk-size=DISK_SIZE \
  --boot-disk-type=pd-ssd \
  --tags=http-server,https-server
```

### 6. 방화벽 규칙

```bash
# HTTP
gcloud compute firewall-rules create allow-http \
  --project=PROJECT_ID \
  --allow=tcp:80 \
  --target-tags=http-server

# HTTPS
gcloud compute firewall-rules create allow-https \
  --project=PROJECT_ID \
  --allow=tcp:443 \
  --target-tags=https-server
```

## 출력 형식

```
| 항목 | 값 |
|------|-----|
| VM 이름 | xxx |
| 존 | asia-northeast3-a |
| 머신 타입 | e2-small |
| 내부 IP | 10.x.x.x |
| 외부 IP | 34.x.x.x |
| 디스크 | 20GB SSD |
| OS | Ubuntu 22.04 LTS |
| 상태 | ✅ RUNNING |

방화벽: HTTP (80) ✅, HTTPS (443) ✅

SSH 접속:
gcloud compute ssh VM_NAME --zone=ZONE
```

## 에러 처리

| 에러 | 해결 |
|------|------|
| `Quota 'CPUS' exceeded` | 다른 리전 시도 또는 할당량 증가 요청 |
| `Compute Engine API has not been enabled` | 자동으로 API 활성화 |
| `resource already exists` | 다른 VM 이름 제안 |

## 고급 옵션

### Preemptible VM

```bash
--preemptible
```

최대 80% 저렴, 24시간 후 자동 종료.

### 고정 IP

```bash
gcloud compute addresses create IP_NAME --region=REGION
# VM 생성 시 --address=IP_NAME
```
