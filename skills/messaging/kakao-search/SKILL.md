---
name: kakao-search
description: 카카오톡 채팅방 검색. "카톡 방 검색", "채팅방 찾기", "kakao search", "KakaoTalk find room" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: <검색어>
---

# 카카오톡 채팅방 검색

이름으로 채팅방을 검색합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py search $ARGUMENTS
```

## 예시

- `/kakao-search 친구` - "친구" 포함 방 검색
- `/kakao-search "그룹"` - "그룹" 포함 방 검색

## 출력 형식

```
=== Search Results: '친구' (3 found) ===

1. 친구1
2. 대학 친구들 (5 unread)
3. 친구2
```

## 참고

- 대소문자 구분 없음
- 최대 50개 방에서 검색
- 안읽은 메시지 수도 표시

## 다음 단계

- `/kakao-open "친구1"` - 검색 결과에서 방 열기
- `/kakao-list` - 전체 방 목록 보기
