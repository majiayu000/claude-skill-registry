---
name: kakao-rooms-prev
description: 카카오톡 이전 채팅방 목록. "카톡 이전 방", "앞으로", "kakao rooms prev", "KakaoTalk previous rooms" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: [step]
---

# 카카오톡 이전 채팅방 목록

이전 10개 채팅방을 표시합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py rooms-prev $ARGUMENTS
```

## 옵션

- `/kakao-rooms-prev` - 이전 10개 방 (기본)
- `/kakao-rooms-prev 5` - 이전 5개 방

## 동작 방식

- 방 목록 offset 감소
- 최소 offset은 0 (첫 페이지)

## 다음 단계

- `/kakao-rooms-next` - 다음 페이지로
- `/kakao-open 3` - 3번 방 열기
- `/kakao-search 검색어` - 방 검색
