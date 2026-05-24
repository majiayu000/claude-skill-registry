---
name: kakao-refresh
description: 카카오톡 메시지 새로고침. "카톡 새로고침", "리프레시", "kakao refresh", "KakaoTalk reload" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

# 카카오톡 메시지 새로고침

현재 채팅방의 최신 메시지를 새로고침합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py refresh
```

## 동작 방식

- 메시지 offset을 0으로 리셋
- 최신 20개 메시지를 다시 불러옴
- 스크롤 후 최신으로 돌아올 때 유용

## 다음 단계

- `/kakao-up` - 이전 메시지 보기
- `/kakao-send 메시지` - 답장 보내기
- `/kakao-back` - 방 목록으로
