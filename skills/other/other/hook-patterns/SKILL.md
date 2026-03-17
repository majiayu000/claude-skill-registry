---
name: hook-patterns
version: 1.0.0
description: Claude Code 훅 사용 패턴과 작성 표준
user-invocable: false
---

# Hook Patterns

Claude Code 훅 사용 패턴과 작성 표준입니다.

---

## Hook vs Skill

| 기준 | Hook | Skill |
|-----|------|-------|
| 트리거 | 도구 실행 전후 **자동** | 사용자 **수동** 호출 |
| 목적 | 검증, 알림, 로깅 | 워크플로우 실행 |
| 제어 | 차단 또는 통과 | 복잡한 분기 처리 |
| 예시 | 커밋 메시지 검증 | `/commit` 워크플로우 |

**원칙**: 훅은 **게이트키퍼**, 스킬은 **오케스트레이터**

---

## 훅 유형

### PreToolUse

도구 실행 **전**에 트리거됩니다.

**사용 사례**:
- 위험한 명령 차단
- 인자 검증
- 권한 확인

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

### PostToolUse

도구 실행 **후**에 트리거됩니다.

**사용 사례**:
- 결과 로깅
- 알림 전송
- 후속 작업 트리거

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/log-file-write.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 훅 작성 표준

### 파일 구조

```
~/.claude/hooks/
├── validate-bash.sh      # PreToolUse: Bash 검증
├── log-file-write.sh     # PostToolUse: 파일 쓰기 로깅
└── notify-error.sh       # PostToolUse: 에러 알림
```

### 스크립트 템플릿

```bash
#!/bin/bash
# Hook: {hook-name}
# Type: PreToolUse | PostToolUse
# Matcher: {matcher}
# Purpose: {한 줄 설명}

set -euo pipefail

# stdin에서 입력 읽기
input=$(cat)

# JSON 파싱 (jq 사용)
# command=$(echo "$input" | jq -r '.tool_input.command // ""')

# 검증 로직
# ...

# 필수: stdin 데이터를 stdout으로 패스스루
echo "$input"
```

### 차단 응답 형식

```bash
# 차단 시
echo '{"decision": "block", "reason": "위험한 명령입니다"}'
exit 2
```

---

## 인라인 vs 파일 분리

### 인라인 (settings.json)

**장점**: 간단한 로직에 적합
**단점**: 복잡한 로직 관리 어려움

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"decision\": \"allow\"}'"
          }
        ]
      }
    ]
  }
}
```

### 파일 분리 (권장)

**장점**: 버전 관리, 테스트, 재사용 용이

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 실제 예시

### 위험 명령 차단

```bash
#!/bin/bash
# Hook: validate-bash
# Type: PreToolUse
# Matcher: Bash
# Purpose: 위험한 bash 명령 차단

set -euo pipefail

input=$(cat)

# command 추출
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# rm -rf / 차단
if echo "$command" | grep -qE 'rm\s+-rf\s+/'; then
  echo '{"decision": "block", "reason": "루트 삭제 명령은 허용되지 않습니다"}'
  exit 2
fi

# 통과
echo "$input"
```

### 파일 쓰기 로깅

```bash
#!/bin/bash
# Hook: log-file-write
# Type: PostToolUse
# Matcher: Write
# Purpose: 파일 쓰기 작업 로깅

set -euo pipefail

input=$(cat)

# file_path 추출
file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""')
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# 로그 디렉토리 생성
log_dir="$HOME/.claude/logs"
mkdir -p "$log_dir"

# 로그 기록
echo "[$timestamp] File written: $file_path" >> "$log_dir/file-writes.log"

# 패스스루
echo "$input"
```

---

## 체크리스트

훅 작성 시 확인:

- [ ] 목적이 검증/알림/로깅인가? (워크플로우면 스킬로)
- [ ] 적절한 훅 유형 선택 (Pre/Post)
- [ ] 표준 헤더에 메타데이터 포함 (Hook, Type, Matcher, Purpose)
- [ ] stdin 데이터를 stdout으로 패스스루
- [ ] 차단 시 명확한 이유 제공 + exit 2
