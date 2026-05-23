---
name: kakao-back
description: 카카오톡 방 목록으로 돌아가기. "카톡 뒤로", "방 목록", "kakao back", "KakaoTalk back to list" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

# 카카오톡 방 목록으로 돌아가기

채팅에서 방 목록으로 돌아갑니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py back
```

## 동작 방식

- `in_chat` 상태를 false로 변경
- 메시지 offset을 0으로 리셋
- 현재 페이지의 방 목록 표시

## 출력 형식

```
✓ Back to room list
=== Chat Rooms (1-10) ===

1. 친구이름 (2 unread)
2. 그룹채팅
...
```

## 다음 단계

- `/kakao-open 3` - 다른 방 열기
- `/kakao-rooms-next` - 더 많은 방 보기
- `/kakao-search 검색어` - 방 검색
