---
name: gcp-vm-resize
description: "GCP VM 머신 타입 변경 (스케일업/다운)"
---

# GCP VM Resize

VM의 머신 타입을 변경하여 스케일업/다운합니다.

## 사용법

```
/gcp-vm-resize                     # VM 목록 → 선택
/gcp-vm-resize my-vm               # 현재 스펙 확인 → 추천
/gcp-vm-resize my-vm e2-medium     # 직접 지정
```

## Workflow

### 1. 현재 VM 스펙 확인

```bash
gcloud compute instances describe VM_NAME --zone=ZONE \
  --format="table(name,machineType.basename(),scheduling.preemptible,disks[0].diskSizeGb)"
```

### 2. 사용 가능한 머신 타입 조회

```bash
# 해당 Zone의 머신 타입 목록
gcloud compute machine-types list --zones=ZONE \
  --format="table(name,guestCpus,memoryMb,description)" \
  --filter="name~'^e2-|^n2-|^n1-'"
```

### 3. VM 중지 (필수)

```bash
gcloud compute instances stop VM_NAME --zone=ZONE
```

### 4. 머신 타입 변경

```bash
gcloud compute instances set-machine-type VM_NAME \
  --zone=ZONE \
  --machine-type=NEW_MACHINE_TYPE
```

### 5. VM 재시작

```bash
gcloud compute instances start VM_NAME --zone=ZONE
```

## 머신 타입 추천

### E2 시리즈 (가성비, 범용)

| 타입 | vCPU | 메모리 | 용도 |
|------|------|--------|------|
| e2-micro | 0.25 | 1GB | 테스트, 경량 |
| e2-small | 0.5 | 2GB | 개발 |
| e2-medium | 1 | 4GB | 소규모 앱 |
| e2-standard-2 | 2 | 8GB | 일반 워크로드 |
| e2-standard-4 | 4 | 16GB | 중규모 앱 |
| e2-standard-8 | 8 | 32GB | 대규모 앱 |

### N2 시리즈 (고성능)

| 타입 | vCPU | 메모리 | 용도 |
|------|------|--------|------|
| n2-standard-2 | 2 | 8GB | 프로덕션 |
| n2-standard-4 | 4 | 16GB | 고부하 |
| n2-highmem-4 | 4 | 32GB | 메모리 집약 |
| n2-highcpu-4 | 4 | 4GB | CPU 집약 |

### 커스텀 머신

```bash
# vCPU 4개, 메모리 10GB
gcloud compute instances set-machine-type VM_NAME \
  --zone=ZONE \
  --custom-cpu=4 \
  --custom-memory=10GB
```

## 출력 형식

```
## VM 리사이즈 결과

| 항목 | 이전 | 이후 |
|------|------|------|
| 머신 타입 | e2-micro | e2-medium |
| vCPU | 0.25 | 1 |
| 메모리 | 1GB | 4GB |
| 예상 월 비용 | ~$6 | ~$25 |

---
VM이 재시작되었습니다.
```

## 비용 비교 (asia-northeast3, 월 기준)

| 타입 | 온디맨드 | Spot (80% 할인) |
|------|----------|-----------------|
| e2-micro | ~$6 | ~$1.2 |
| e2-small | ~$12 | ~$2.4 |
| e2-medium | ~$25 | ~$5 |
| e2-standard-2 | ~$50 | ~$10 |
| e2-standard-4 | ~$100 | ~$20 |

## 주의사항

- VM 중지 필수 (다운타임 발생)
- 디스크 크기는 별도 조정 (`gcloud compute disks resize`)
- GPU 추가 시 N1 시리즈만 가능
- Spot/Preemptible VM은 타입 변경 후에도 유지
