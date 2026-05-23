---
name: kakao-read
description: 카카오톡 메시지 읽기. "카톡 메시지 보여줘", "채팅 내용", "kakao read", "KakaoTalk messages" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: [limit]
---

# 카카오톡 메시지 읽기

현재 열린 채팅방의 메시지를 읽습니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py read $ARGUMENTS
```

## 옵션

- `/kakao-read` - 최근 20개 메시지
- `/kakao-read 50` - 최근 50개 메시지

## 출력 형식

```
=== 친구이름 ===

[오후 3:32] 친구: 안녕!
[오후 3:33] Me: 응 안녕 (1명 안읽음)
[오후 3:35] 친구: 뭐해?

--- 2026년 1월 27일 월요일 ---

[오후 4:00] 친구: 좋은 아침
[오후 4:01] Me: [Image]
```

## 메시지 정보

- **발신자**: 내 메시지는 "Me", 상대방은 이름
- **시간**: 카카오톡 형식 그대로
- **안읽은 수**: "(N명 안읽음)" 표시
- **이미지**: `[Image]`로 표시
- **날짜 구분선**: `--- 날짜 ---`

## 네비게이션

- `/kakao-up` - 이전 메시지 보기
- `/kakao-down` - 최신 메시지 보기
- `/kakao-refresh` - 새로고침

## 다음 단계

- `/kakao-send 메시지` - 답장 보내기
- `/kakao-back` - 방 목록으로
