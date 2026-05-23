---
name: gcp-cleanup
description: "GCP 리소스 정리 (Read-Only 스캔)"
---

# GCP 리소스 정리 (Read-Only 스캔)

사용하지 않는 GCP 리소스를 **탐지만** 수행. 삭제는 사용자가 직접 실행.

## 안전 원칙

1. **읽기 전용** - 이 스킬은 조회만 수행, 삭제 명령 실행 안 함
2. **명령어 제공** - 삭제가 필요하면 명령어를 출력하고 사용자가 직접 실행
3. **보호 규칙** - prod/production 포함 프로젝트는 경고 표시
4. **복구 안내** - 프로젝트 삭제는 30일 내 복구 가능함을 안내

## 수행 작업

### 1. 프로젝트 목록 조회

```bash
gcloud projects list --format="table(projectId,name,lifecycleState)"
```

### 2. 각 프로젝트별 리소스 스캔

```bash
for PROJECT in $(gcloud projects list --format="value(projectId)" --filter="lifecycleState:ACTIVE"); do
  echo "=== $PROJECT ==="

  # TERMINATED VM (중지된 상태로 방치)
  echo "TERMINATED VMs:"
  gcloud compute instances list --project=$PROJECT \
    --filter="status:TERMINATED" \
    --format="table(name,zone,status)" 2>/dev/null || echo "  (접근 권한 없음)"

  # 연결되지 않은 디스크 (orphaned)
  echo "Orphaned Disks:"
  gcloud compute disks list --project=$PROJECT \
    --filter="-users:*" \
    --format="table(name,zone,sizeGb,type)" 2>/dev/null || echo "  (접근 권한 없음)"

  # 예약된 외부 IP (사용 안 함)
  echo "Unused Static IPs:"
  gcloud compute addresses list --project=$PROJECT \
    --filter="status:RESERVED" \
    --format="table(name,region,status)" 2>/dev/null || echo "  (접근 권한 없음)"

  # 리소스 카운트 (빈 프로젝트 판단)
  VM_COUNT=$(gcloud compute instances list --project=$PROJECT --format="value(name)" 2>/dev/null | wc -l)
  DISK_COUNT=$(gcloud compute disks list --project=$PROJECT --format="value(name)" 2>/dev/null | wc -l)

  if [ "$VM_COUNT" -eq 0 ] && [ "$DISK_COUNT" -eq 0 ]; then
    echo "  빈 프로젝트 (리소스 0개)"
  fi
  echo ""
done
```

## 출력 형식

```markdown
## GCP 리소스 스캔 결과

### 정리 검토 대상

| 프로젝트 | 리소스 타입 | 이름 | 위치 | 비고 |
|----------|-------------|------|------|------|
| test-old | 빈 프로젝트 | - | - | 리소스 0개 |
| main-project | Orphaned 디스크 | disk-backup | asia-northeast3-a | 50GB, 미연결 |
| dev-project | TERMINATED VM | vm-test | us-central1-a | 중지 상태 |

---

## 직접 실행 필요

아래 명령어는 **복사하여 직접 실행**하세요. 이 스킬은 삭제를 수행하지 않습니다.

### 빈 프로젝트 삭제
\`\`\`bash
# test-old 프로젝트 삭제 (30일 내 복구 가능: gcloud projects undelete test-old)
gcloud projects delete test-old
\`\`\`

### Orphaned 디스크 삭제
\`\`\`bash
# 삭제 전 확인: 정말 사용하지 않는 디스크인가?
gcloud compute disks describe disk-backup --zone=asia-northeast3-a --project=main-project

# 삭제 실행
gcloud compute disks delete disk-backup --zone=asia-northeast3-a --project=main-project
\`\`\`

### TERMINATED VM 삭제
\`\`\`bash
# VM 삭제 (연결된 디스크도 함께 삭제됨)
gcloud compute instances delete vm-test --zone=us-central1-a --project=dev-project
\`\`\`

---

## 주의사항

- **prod/production** 포함 프로젝트는 신중히 검토
- 프로젝트 삭제는 30일 내 `gcloud projects undelete PROJECT_ID`로 복구 가능
- 디스크/VM 삭제는 **복구 불가** - 스냅샷 백업 권장
```

## 보호 규칙

다음 패턴의 프로젝트는 자동으로 경고 표시:
- 이름에 `prod`, `production`, `live`, `main` 포함
- 최근 7일 내 생성된 리소스
- 결제 계정이 연결된 활성 프로젝트

## 사용 시나리오

```
사용자: /gcp-cleanup

Claude: [스캔 결과 출력]
        삭제가 필요하면 위의 명령어를 복사하여 직접 실행하세요.

사용자: (명령어 복사 후 터미널에서 직접 실행)
```

## 참고

- 이 스킬은 **조회 전용**입니다
- 삭제 명령은 사용자가 검토 후 직접 실행해야 합니다
- 비용 추정은 대략적인 참고값입니다 (실제 비용은 GCP 콘솔에서 확인)
