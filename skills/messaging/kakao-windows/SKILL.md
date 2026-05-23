---
name: kakao-windows
description: 카카오톡 열린 창 목록. "카톡 창 목록", "열린 창", "kakao windows", "KakaoTalk open windows" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

# 카카오톡 열린 창 목록

현재 열려 있는 모든 카카오톡 창을 표시합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py windows
```

## 출력 형식

```
=== Open KakaoTalk Windows ===

1. 💬 카카오톡 [main]
2. 🗨️ 친구이름 [chat]
3. 🗨️ 그룹채팅 [chat]
```

## 창 타입

- `main` - 메인 카카오톡 창 (방 목록)
- `chat` - 열린 채팅 창
- `popup` - 기타 팝업 창 (설정 등)
- `unknown` - 식별 불가 창

## 용도

- 방이 제대로 안 열릴 때 디버깅
- 현재 열린 창 확인
- 카카오톡 접근 가능 여부 확인

## 다음 단계

- `/kakao-setup` - 문제 시 전제조건 체크
- `/kakao-list` - 채팅방 목록 보기
