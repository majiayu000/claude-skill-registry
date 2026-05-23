---
name: kakao-down
description: 카카오톡 최신 메시지 보기. "카톡 아래로", "최신 메시지", "kakao down", "KakaoTalk scroll down" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
argument-hint: [step]
---

# 카카오톡 최신 메시지 보기

아래로 스크롤하여 최신 메시지를 봅니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py down $ARGUMENTS
```

## 옵션

- `/kakao-down` - 10개 최신으로 (기본)
- `/kakao-down 20` - 20개 최신으로

## 동작 방식

- 호출할 때마다 offset 감소
- 최소 offset은 0 (가장 최신)
- 현재에 가까운 메시지를 읽음

## 다음 단계

- `/kakao-up` - 이전 메시지로
- `/kakao-refresh` - 가장 최신으로 리셋
