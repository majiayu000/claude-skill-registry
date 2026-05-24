---
name: kakao-up
description: 카카오톡 이전 메시지 보기. "카톡 위로", "이전 메시지", "kakao up", "KakaoTalk scroll up" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: [step]
---

# 카카오톡 이전 메시지 보기

위로 스크롤하여 이전 메시지를 봅니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py up $ARGUMENTS
```

## 옵션

- `/kakao-up` - 10개 이전 메시지 (기본)
- `/kakao-up 20` - 20개 이전 메시지

## 출력 형식

```
=== 친구이름 (offset: 10) ===

[오후 3:20] 친구: 이전 메시지
[오후 3:22] Me: 또 다른 이전 메시지
...
```

## 동작 방식

- 호출할 때마다 offset 증가
- 메시지 히스토리에서 더 이전 것을 읽음
- offset은 세션 상태에 저장

## 다음 단계

- `/kakao-down` - 최신 메시지로 돌아가기
- `/kakao-refresh` - 가장 최신 메시지로
