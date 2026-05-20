---
name: spool
description: "Threads CLI - Read, post, reply, and search on Meta's Threads using OpenClaw browser tool. Use when the user wants to interact with Threads: posting, reading timeline, viewing profiles, replying to threads, or searching."
homepage: https://github.com/zizi-cat/spool
metadata: {"clawdhub":{"emoji":"🧵"}}
---

# spool

OpenClaw browser 도구로 Threads (threads.net) 조작하기.

## Prerequisites

### 환경 요구사항
- OpenClaw with browser tool enabled
- `openclaw` browser profile
- Threads 계정 로그인 완료

### Headless 서버인 경우 (GUI 없음)

Xvfb 가상 디스플레이 필요:

```bash
# 1. Xvfb 설치 및 서비스 등록
sudo apt install -y xvfb
sudo tee /etc/systemd/system/xvfb.service << 'EOF'
[Unit]
Description=X Virtual Frame Buffer
After=network.target
[Service]
Type=simple
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24
Restart=always
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable --now xvfb

# 2. OpenClaw Gateway에 DISPLAY 환경변수 추가
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
echo -e '[Service]\nEnvironment=DISPLAY=:99' > ~/.config/systemd/user/openclaw-gateway.service.d/display.conf
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

### 로그인 (처음 한 번만)

```
browser action=start profile=openclaw
browser action=open profile=openclaw targetUrl="https://www.threads.net/login"
# 사용자에게 수동 로그인 요청
```

---

## 사용법

### 1. 타임라인 읽기

```
browser action=open profile=openclaw targetUrl="https://www.threads.net"
browser action=snapshot profile=openclaw compact=true
```

결과에서 각 게시물의 작성자, 내용, 좋아요/댓글 수 확인 가능.

### 2. 포스팅 (전체 플로우)

**Step 1: 홈으로 이동**
```
browser action=open profile=openclaw targetUrl="https://www.threads.net"
browser action=snapshot profile=openclaw compact=true
```

**Step 2: "What's new?" 버튼 찾아서 클릭**
snapshot에서 `"What's new?"` 또는 `"Empty text field"` 포함된 button의 ref 찾기
```
browser action=act profile=openclaw request={"kind":"click","ref":"e14"}
```
(ref는 snapshot마다 다름! 반드시 snapshot에서 확인)

**Step 3: 다이얼로그에서 텍스트 입력**
```
browser action=snapshot profile=openclaw compact=true
```
`textbox` ref 찾아서:
```
browser action=act profile=openclaw request={"kind":"type","ref":"e14","text":"포스팅 내용"}
```

**Step 4: Post 버튼 클릭**
```
browser action=act profile=openclaw request={"kind":"click","ref":"e22"}
```
(Post 버튼 ref도 snapshot에서 확인)

**Step 5: 확인**
```
browser action=snapshot profile=openclaw compact=true
```
→ "Posted" 텍스트와 "View" 링크가 보이면 성공!

### 3. 프로필 보기

```
browser action=open profile=openclaw targetUrl="https://www.threads.net/@username"
browser action=snapshot profile=openclaw compact=true
```

### 4. 검색

```
browser action=open profile=openclaw targetUrl="https://www.threads.net/search?q=검색어"
browser action=snapshot profile=openclaw compact=true
```

### 5. 답글 달기

```
# 게시물 열기
browser action=open profile=openclaw targetUrl="https://www.threads.net/@user/post/POSTID"
browser action=snapshot profile=openclaw compact=true

# Reply 버튼 클릭 (ref 확인 후)
browser action=act profile=openclaw request={"kind":"click","ref":"<reply-ref>"}

# 텍스트 입력 및 게시 (포스팅과 동일)
```

---

## 핵심 포인트

1. **snapshot 먼저!** - 모든 작업 전에 snapshot으로 현재 페이지 상태와 ref 확인
2. **ref는 매번 달라짐** - snapshot 결과에서 항상 새로 찾기
3. **compact=true** - 토큰 절약을 위해 항상 사용
4. **targetId 유지** - 같은 탭에서 작업하려면 targetId 파라미터 사용
5. **포스팅 전 확인** - 사용자에게 내용 확인받고 포스팅

---

## 트러블슈팅

| 문제 | 해결 |
|------|------|
| browser 도구 안 됨 | Xvfb 실행 확인, DISPLAY=:99 설정 확인, Gateway 재시작 |
| 로그인 안 됨 | `/login` 페이지로 이동 후 수동 로그인 요청 |
| ref 못 찾음 | snapshot 다시 찍고 비슷한 텍스트/버튼 찾기 |
| 포스팅 안 됨 | Post 버튼이 disabled인지 확인 (텍스트 입력 필요) |
