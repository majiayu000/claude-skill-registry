# GCP VM Initial Setup

GCP VM 초기 설정 자동화. 시스템 업데이트, 타임존, 방화벽, fail2ban, 스왑 설정.

## Triggers

- "VM 초기 설정", "VM 셋업", "서버 초기화"
- "VM 보안 설정", "VM 기본 설정"
- "initialize VM", "setup VM"

## Workflow

### 1. 정보 수집

필수:
- VM 이름 (필수)
- 프로젝트 ID (기본: 현재 설정된 프로젝트)
- 존 (기본: asia-northeast3-a)

선택:
- 타임존 (기본: Asia/Seoul)
- 스왑 크기 (기본: 2GB)

```bash
# 현재 프로젝트 확인
gcloud config get-value project

# VM 목록에서 선택
gcloud compute instances list --format="table(name,zone,status)"
```

### 2. SSH 접속 확인

```bash
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT \
  --command="echo 'SSH 접속 성공' && uname -a"
```

### 3. 시스템 업데이트

```bash
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT \
  --command="sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt upgrade -y"
```

### 4. 타임존 설정

```bash
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT \
  --command="sudo timedatectl set-timezone Asia/Seoul && timedatectl"
```

### 5. UFW 방화벽 설정

```bash
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT \
  --command="sudo ufw allow OpenSSH && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp && sudo ufw --force enable && sudo ufw status verbose"
```

### 6. fail2ban 설치

```bash
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT \
  --command="sudo DEBIAN_FRONTEND=noninteractive apt install -y fail2ban && sudo systemctl enable fail2ban && sudo systemctl start fail2ban && sudo systemctl status fail2ban --no-pager"
```

### 7. 스왑 설정

```bash
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT \
  --command="sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile && echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab && free -h"
```

### 8. 기본 도구 확인

```bash
gcloud compute ssh VM_NAME --zone=ZONE --project=PROJECT \
  --command="echo '=== 설치된 도구 ===' && git --version && curl --version | head -1 && wget --version | head -1 && vim --version | head -1 && htop --version && tmux -V"
```

## 출력 형식

```
✅ VM 초기 설정 완료: [VM_NAME]

| 항목 | 상태 | 세부 |
|------|------|------|
| 시스템 업데이트 | ✅ | apt update/upgrade 완료 |
| 타임존 | ✅ | Asia/Seoul (KST) |
| UFW 방화벽 | ✅ | SSH(22), HTTP(80), HTTPS(443) 허용 |
| fail2ban | ✅ | SSH 무차별 공격 방지 활성화 |
| 스왑 | ✅ | 2GB 설정됨 |
| 기본 도구 | ✅ | git, curl, wget, vim, htop, tmux |

SSH 접속:
gcloud compute ssh [VM_NAME] --zone=[ZONE] --project=[PROJECT]
```

## 에러 처리

| 에러 | 해결 |
|------|------|
| SSH 연결 실패 | VM이 RUNNING 상태인지 확인, 방화벽 규칙 확인 |
| 권한 부족 | sudo 권한 확인, 계정 인증 상태 확인 |
| 스왑 파일 존재 | `swapon --show`로 확인 후 기존 스왑 사용 |
| fail2ban 설치 실패 | `sudo apt update` 재실행 후 재시도 |
| 타임존 설정 실패 | `timedatectl list-timezones | grep Seoul` 확인 |

## 고급 옵션

### 커스텀 타임존

```bash
# 타임존 목록 확인
timedatectl list-timezones | grep America

# 다른 타임존 설정
sudo timedatectl set-timezone America/New_York
```

### 스왑 크기 조정

```bash
# 4GB 스왑 (RAM 4GB 이상 VM용)
sudo fallocate -l 4G /swapfile
```

### 추가 포트 허용

```bash
# 커스텀 포트 허용 (예: 3000번)
sudo ufw allow 3000/tcp
```

## 참고

- GCP Ubuntu 22.04 이미지는 git, curl, wget, vim, htop, tmux가 기본 설치됨
- GCP 방화벽(네트워크)과 UFW(호스트) 이중 방어 권장
- fail2ban은 기본 SSH jail만 활성화 (추가 설정 가능)
- 스왑 크기: RAM 2GB 이하는 100%, 2-8GB는 50-100% 권장
