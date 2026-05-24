---
name: kakao-open
description: 카카오톡 채팅방 열기. "카톡 방 열어", "채팅방 들어가줘", "kakao open", "KakaoTalk open room" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: <번호|이름>
---

# 카카오톡 채팅방 열기

번호 또는 이름으로 채팅방을 엽니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py open $ARGUMENTS
```

## 옵션

- `/kakao-open 3` - 목록에서 3번 방 열기
- `/kakao-open "친구이름"` - 이름으로 방 열기

## 동작 방식

1. 카카오톡 채팅방 목록에서 해당 방 선택
2. Enter 키로 채팅창 열기
3. 세션 상태에 방 이름 저장

## 참고

- 방 번호는 `/kakao-list`에서 확인
- 이름 검색은 부분 일치 (대소문자 무관)
- 채팅창은 백그라운드에서 열림

## 다음 단계

- `/kakao-read` - 메시지 읽기
- `/kakao-send 메시지` - 메시지 보내기
- `/kakao-back` - 방 목록으로 돌아가기
