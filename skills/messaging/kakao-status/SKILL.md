---
name: kakao-status
description: 카카오톡 연결 상태 확인. "카톡 상태", "연결 확인", "kakao status", "KakaoTalk connection" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

# 카카오톡 상태 확인

현재 연결 상태와 세션 정보를 확인합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py status
```

## 출력 형식

```
=== KakaoTalk Status ===

Current room: 친구이름
Messages sent this session: 5
Connection: ✓ Connected
```

## 상태 정보

- **Current room**: 현재 열린 채팅방 (없으면 None)
- **Messages sent**: 이번 세션에서 보낸 메시지 수
- **Connection**: 카카오톡 접근 가능 여부

## 연결 상태

- `✓ Connected` - 정상 작동
- `✗ KakaoTalk is not running` - 앱 실행 필요
- `✗ Permission denied` - 접근성 권한 필요
- `⚠️ Cannot read room list` - 채팅 탭으로 전환 필요

## 다음 단계

- `/kakao-setup` - 전체 전제조건 체크
- `/kakao-list` - 채팅방 목록 보기
