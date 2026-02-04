---
name: gcp-snapshot
description: "GCP 디스크 스냅샷 생성/복원/정리"
---

# GCP Disk Snapshot

디스크 스냅샷을 생성, 복원, 관리합니다.

## 사용법

```
/gcp-snapshot                      # 스냅샷 목록 조회
/gcp-snapshot create my-disk       # 디스크 스냅샷 생성
/gcp-snapshot restore snap-001     # 스냅샷에서 디스크 복원
/gcp-snapshot cleanup              # 오래된 스냅샷 정리
```

## Workflow

### 1. 스냅샷 목록 조회

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud compute snapshots list --project=$PROJECT_ID \
  --format="table(name,sourceDisk.basename(),diskSizeGb,status,creationTimestamp.date())"
```

### 2. 디스크 목록 조회

```bash
gcloud compute disks list --project=$PROJECT_ID \
  --format="table(name,zone.basename(),sizeGb,type.basename(),status,users.basename())"
```

### 3. 스냅샷 생성

```bash
# 기본 스냅샷
gcloud compute disks snapshot DISK_NAME \
  --zone=ZONE \
  --snapshot-names=SNAPSHOT_NAME

# 설명 추가
gcloud compute disks snapshot DISK_NAME \
  --zone=ZONE \
  --snapshot-names=SNAPSHOT_NAME \
  --description="Before upgrade - $(date +%Y-%m-%d)"

# 여러 디스크 동시에
gcloud compute disks snapshot DISK1 DISK2 \
  --zone=ZONE \
  --snapshot-names=SNAP1,SNAP2
```

### 4. 스냅샷에서 디스크 복원

```bash
# 새 디스크 생성
gcloud compute disks create NEW_DISK_NAME \
  --zone=ZONE \
  --source-snapshot=SNAPSHOT_NAME \
  --type=pd-balanced

# VM에 연결
gcloud compute instances attach-disk VM_NAME \
  --zone=ZONE \
  --disk=NEW_DISK_NAME
```

### 5. 스냅샷 삭제

```bash
# 단일 삭제
gcloud compute snapshots delete SNAPSHOT_NAME

# 7일 이상 된 스냅샷 목록
gcloud compute snapshots list \
  --filter="creationTimestamp<-P7D" \
  --format="value(name)"
```

## 스냅샷 스케줄 설정

```bash
# 일일 스냅샷 스케줄 생성
gcloud compute resource-policies create snapshot-schedule daily-backup \
  --region=asia-northeast3 \
  --max-retention-days=7 \
  --daily-schedule \
  --start-time=02:00

# 디스크에 스케줄 적용
gcloud compute disks add-resource-policies DISK_NAME \
  --zone=ZONE \
  --resource-policies=daily-backup
```

## 출력 형식

```
## 스냅샷 목록

| 스냅샷 이름 | 소스 디스크 | 크기 | 상태 | 생성일 |
|-------------|-------------|------|------|--------|
| snap-2024-01-15 | my-disk | 50GB | READY | 2024-01-15 |
| snap-2024-01-14 | my-disk | 50GB | READY | 2024-01-14 |

---
총 2개 스냅샷, 100GB 사용 중
예상 월 비용: ~$5 (스냅샷 $0.05/GB/월)
```

## 스냅샷 비용

| 항목 | 비용 |
|------|------|
| 스냅샷 저장 | $0.05/GB/월 |
| 첫 스냅샷 | 디스크 전체 크기 |
| 이후 스냅샷 | 변경분만 (증분) |

## 모범 사례

1. **명명 규칙**: `{disk}-{date}` (예: `web-server-2024-01-15`)
2. **정기 백업**: 스케줄 정책 사용
3. **보관 기간**: 개발 7일, 프로덕션 30일
4. **복원 테스트**: 정기적으로 복원 테스트

## 주의사항

- 스냅샷 생성 중 I/O 성능 저하 가능
- 프로덕션은 비피크 시간에 생성 권장
- 스냅샷은 리전 독립적 (다른 리전에서 복원 가능)
