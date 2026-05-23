---
name: kakao-setup
description: 카카오톡 연동 전제조건 체크. "카톡 설정", "권한 확인", "kakao setup", "KakaoTalk setup" 시 사용.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

# 카카오톡 초기 설정 가이드

KakaoTalk 연동을 위한 전제조건을 확인하고 설정합니다.

## 실행

```bash
cd /Users/taehoje/space/kakao-terminal && python kakao_cli.py setup
```

## 초기 설정 (최초 1회)

### 1. 손쉬운 사용 권한 설정

터미널(또는 Claude Code)에서 카카오톡을 제어하려면 macOS 접근성 권한이 필요합니다.

**설정 방법:**

1. **시스템 설정 열기**: `Cmd + Space` → "시스템 설정" 검색
2. **개인정보 보호 및 보안** 클릭
3. **손쉬운 사용** 클릭
4. 좌측 하단 자물쇠 클릭 → 비밀번호 입력
5. 다음 앱에 체크 표시:
   - **Terminal** (터미널 사용시)
   - **Claude** (Claude Code 사용시)
   - **iTerm** (iTerm2 사용시)

**권한 없으면:**
```
✗ Accessibility permission denied
```

### 2. 카카오톡 실행 및 로그인

1. Dock에서 **카카오톡** 아이콘 클릭
2. 로그인 (QR코드 또는 비밀번호)
3. 로그인 완료 후 메인 창 표시 확인

### 3. 채팅 목록 화면으로 이동

카카오톡 창에서:

1. 상단 탭 중 **채팅** 클릭 (친구/더보기 아님)
2. 채팅방 목록이 보이는 상태로 두기
3. 창을 최소화해도 됨 (숨겨둬도 동작)

**주의**: 개별 채팅방이 열린 상태가 아니라 **채팅 목록**이 보여야 합니다.

## 체크 항목

| 항목 | 설명 | 해결 방법 |
|------|------|-----------|
| 카카오톡 실행 | 앱이 실행되어 있어야 함 | Dock에서 실행 |
| 접근성 권한 | 터미널에 권한 부여 | 위 "손쉬운 사용" 참고 |
| 창 열림 | 최소 하나의 창이 열려 있어야 함 | Dock 아이콘 클릭 |
| 채팅 탭 | 채팅 탭이 활성화되어 있어야 함 | 채팅 탭 클릭 |

## 출력 예시

**정상:**
```
=== KakaoTalk Prerequisites Check ===

✓ KakaoTalk is running
✓ Accessibility permission granted
✓ KakaoTalk window found
✓ Chat list is visible

All checks passed! Ready to use.
```

**문제 발생시:**
```
=== KakaoTalk Prerequisites Check ===

✓ KakaoTalk is running
✗ Accessibility permission denied
  → System Settings > Privacy & Security > Accessibility
  → Add and enable Terminal or your IDE
```

## 다음 단계

설정 완료 후:
- `/kakao-list` - 채팅방 목록 보기
- `/kakao-status` - 연결 상태 확인
