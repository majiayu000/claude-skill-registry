---
name: kakao-send
description: 카카오톡 메시지 전송. "카톡 보내줘", "메시지 전송", "kakao send", "KakaoTalk send message" 시 사용.
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash
argument-hint: <메시지>
---

# 카카오톡 메시지 전송

현재 열린 채팅방에 메시지를 보냅니다.

## 중요: 사용자만 호출 가능

이 스킬은 `disable-model-invocation: true`로 설정되어 있어 Claude가 자동으로 메시지를 보낼 수 없습니다. 반드시 사용자가 `/kakao-send`를 직접 입력해야 합니다.

## 경고

자동화된 메시지 전송은 카카오톡 이용약관 위반 가능성이 있으며 계정 정지 위험이 있습니다. 개인 용도로만 책임감 있게 사용하세요.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py send "$ARGUMENTS"
```

## 예시

- `/kakao-send 안녕하세요`
- `/kakao-send "내일 3시에 만나요"`
- `/kakao-send Hello!`

## 안전 기능

- **Rate limiting**: 메시지 간 500ms+ 딜레이
- **랜덤 지터**: 추가 100-300ms 랜덤 딜레이
- **세션 추적**: 50개 메시지 초과 시 경고
- **사용자 전용**: Claude 자동 호출 불가

## 다음 단계

- `/kakao-read` - 답장 확인
- `/kakao-status` - 세션 통계 확인
