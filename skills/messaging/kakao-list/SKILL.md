---
name: kakao-list
description: 카카오톡 채팅방 목록 조회. "카톡 방 목록", "채팅방 보여줘", "kakao list", "KakaoTalk rooms" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: [limit]
---

# 카카오톡 채팅방 목록

KakaoTalk 채팅방 목록을 조회합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py list $ARGUMENTS
```

## 옵션

- `/kakao-list` - 처음 10개 방
- `/kakao-list 20` - 처음 20개 방

## 출력 형식

```
=== Chat Rooms (1-10) ===

1. 친구이름 (2 unread) - 마지막 메시지...
2. 그룹채팅 - 내일 봐요
3. 다른친구
```

## 네비게이션

- `/kakao-rooms-next` - 다음 10개 방
- `/kakao-rooms-prev` - 이전 10개 방
- `/kakao-search 검색어` - 방 검색

## 다음 단계

- `/kakao-open 3` - 3번 방 열기
- `/kakao-open "친구이름"` - 이름으로 방 열기
