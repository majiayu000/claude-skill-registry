---
name: gcp-vm-control
description: "GCP VM 시작/중지/재시작 제어"
---

# GCP VM Control

VM 인스턴스의 시작, 중지, 재시작을 수행합니다.

## 사용법

```
/gcp-vm-control                    # 현재 프로젝트 VM 목록 → 선택
/gcp-vm-control my-vm              # 특정 VM 제어
/gcp-vm-control my-vm start        # 직접 시작
/gcp-vm-control my-vm stop         # 직접 중지
```

## Workflow

### 1. VM 목록 조회

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud compute instances list --project=$PROJECT_ID \
  --format="table(name,zone,machineType.basename(),status,networkInterfaces[0].accessConfigs[0].natIP)"
```

### 2. 사용자에게 액션 선택 요청

- **start** - VM 시작
- **stop** - VM 중지 (비용 절감)
- **reset** - VM 재시작 (강제 재부팅)
- **suspend** - VM 일시 중지 (메모리 유지)
- **resume** - 일시 중지된 VM 재개

### 3. 명령 실행

```bash
# 시작
gcloud compute instances start VM_NAME --zone=ZONE

# 중지
gcloud compute instances stop VM_NAME --zone=ZONE

# 재시작 (강제)
gcloud compute instances reset VM_NAME --zone=ZONE

# 일시 중지
gcloud compute instances suspend VM_NAME --zone=ZONE

# 재개
gcloud compute instances resume VM_NAME --zone=ZONE
```

### 4. 상태 확인

```bash
gcloud compute instances describe VM_NAME --zone=ZONE --format="value(status)"
```

## 출력 형식

```
## VM 제어 결과

| 항목 | 값 |
|------|-----|
| VM | my-instance |
| Zone | asia-northeast3-a |
| 이전 상태 | RUNNING |
| 액션 | stop |
| 현재 상태 | TERMINATED |

---
비용 참고: 중지된 VM은 컴퓨팅 비용이 발생하지 않습니다 (디스크 비용은 유지)
```

## 비용 절감 팁

- **야간/주말 중지**: 개발 VM은 사용하지 않을 때 중지
- **일시 중지 vs 중지**:
  - `suspend`: 빠른 재개, 메모리 비용 발생
  - `stop`: 느린 시작, 비용 없음

## 주의사항

- `reset`은 강제 재부팅 (데이터 손실 가능)
- 프로덕션 VM 중지 시 경고 표시
- Preemptible/Spot VM은 중지 후 재시작 불가할 수 있음
