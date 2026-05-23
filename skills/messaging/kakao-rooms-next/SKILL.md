---
name: kakao-rooms-next
description: 카카오톡 다음 채팅방 목록. "카톡 다음 방", "더 보기", "kakao rooms next", "KakaoTalk more rooms" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: [step]
---

# 카카오톡 다음 채팅방 목록

다음 10개 채팅방을 표시합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py rooms-next $ARGUMENTS
```

## 옵션

- `/kakao-rooms-next` - 다음 10개 방 (기본)
- `/kakao-rooms-next 5` - 다음 5개 방

## 출력 형식

```
=== Chat Rooms (11-20) ===

11. 친구11
12. 그룹채팅2 (3 unread)
13. 다른친구
...
```

## 다음 단계

- `/kakao-rooms-prev` - 이전 방 목록으로
- `/kakao-open 15` - 15번 방 열기
- `/kakao-list` - 처음 10개로 리셋
