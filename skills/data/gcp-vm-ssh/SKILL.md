---
name: gcp-vm-ssh
description: "GCP VM SSH 접속 및 터널링 설정"
---

# GCP VM SSH

VM에 SSH 접속하거나 포트 포워딩/터널을 설정합니다.

## 사용법

```
/gcp-vm-ssh                        # VM 목록 → 선택
/gcp-vm-ssh my-vm                  # SSH 명령어 출력
/gcp-vm-ssh my-vm --tunnel 8080    # 로컬 8080 → VM 8080 터널
/gcp-vm-ssh my-vm --tunnel 3000:80 # 로컬 3000 → VM 80 터널
```

## Workflow

### 1. VM 정보 조회

```bash
PROJECT_ID=$(gcloud config get-value project)
gcloud compute instances list --project=$PROJECT_ID \
  --format="table(name,zone,status,networkInterfaces[0].networkIP,networkInterfaces[0].accessConfigs[0].natIP)"
```

### 2. SSH 명령어 생성

#### 기본 SSH 접속

```bash
# gcloud SSH (권장 - 키 자동 관리)
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT_ID

# 또는 직접 SSH (외부 IP 있는 경우)
ssh -i ~/.ssh/google_compute_engine USER@EXTERNAL_IP
```

#### IAP 터널 (외부 IP 없는 경우)

```bash
gcloud compute ssh VM_NAME --zone=ZONE --tunnel-through-iap
```

### 3. 포트 포워딩/터널

```bash
# 로컬 포트 → VM 포트 (예: 로컬 8080 → VM 8080)
gcloud compute ssh VM_NAME --zone=ZONE -- -L 8080:localhost:8080

# IAP 터널 + 포트 포워딩
gcloud compute ssh VM_NAME --zone=ZONE --tunnel-through-iap -- -L 8080:localhost:8080

# 백그라운드 터널 (포트만 열기)
gcloud compute start-iap-tunnel VM_NAME 22 --local-host-port=localhost:2222 --zone=ZONE &
```

### 4. SCP 파일 전송

```bash
# 로컬 → VM
gcloud compute scp LOCAL_FILE VM_NAME:~/REMOTE_PATH --zone=ZONE

# VM → 로컬
gcloud compute scp VM_NAME:~/REMOTE_FILE LOCAL_PATH --zone=ZONE

# 디렉토리
gcloud compute scp --recurse LOCAL_DIR VM_NAME:~/REMOTE_DIR --zone=ZONE
```

## 출력 형식

```
## SSH 접속 정보

| 항목 | 값 |
|------|-----|
| VM | my-instance |
| Zone | asia-northeast3-a |
| 내부 IP | 10.178.0.2 |
| 외부 IP | 34.64.xxx.xxx |
| 상태 | RUNNING |

### 접속 명령어

\`\`\`bash
# 기본 SSH
gcloud compute ssh my-instance --zone=asia-northeast3-a

# 포트 포워딩 (예: Jupyter)
gcloud compute ssh my-instance --zone=asia-northeast3-a -- -L 8888:localhost:8888
\`\`\`

### 파일 전송

\`\`\`bash
# 업로드
gcloud compute scp ./file.txt my-instance:~/ --zone=asia-northeast3-a

# 다운로드
gcloud compute scp my-instance:~/file.txt ./ --zone=asia-northeast3-a
\`\`\`
```

## 자주 쓰는 터널 패턴

| 용도 | 명령어 |
|------|--------|
| Jupyter Notebook | `-L 8888:localhost:8888` |
| Web Server | `-L 8080:localhost:80` |
| PostgreSQL | `-L 5432:localhost:5432` |
| MySQL | `-L 3306:localhost:3306` |
| Redis | `-L 6379:localhost:6379` |

## 트러블슈팅

| 문제 | 해결 |
|------|------|
| Permission denied | `gcloud compute config-ssh`로 키 재생성 |
| Connection timeout | 방화벽에서 22번 포트 확인 |
| IAP 터널 실패 | IAP API 활성화 + IAM 권한 확인 |
