---
name: ax-health-check
description: "프로젝트 점검 — 의존성/타입/린트/빌드/버전 체크 리포트"
---

# AX Health Check Skill (프로젝트 점검)

프로젝트의 전반적인 상태를 점검합니다. 의존성, 구조, 타입, 린트, 빌드, 버전 동기화를 체크합니다.

## 트리거

- `/ax:health-check` 명령
- "프로젝트 점검" 프롬프트

## 실행 흐름

```
1단계: 프로젝트 의존성 및 구조 확인
    ↓
2단계: 타입 체크 실행
    ↓
3단계: 린트 검사 실행
    ↓
4단계: 빌드 테스트
    ↓
5단계: 버전 동기화 확인
    ↓
6단계: 점검 결과 리포트
```

## 실행 단계

### 1단계: 프로젝트 의존성 및 구조 확인

**Python 환경**:
```bash
# Python 버전 확인
python --version

# 가상환경 상태 확인
pip list --outdated 2>/dev/null | head -20

# pyproject.toml 의존성 확인
cat pyproject.toml | grep -A 50 "dependencies"
```

**Node.js 환경**:
```bash
# Node.js 버전 확인
node --version

# pnpm 버전 확인
pnpm --version

# 의존성 상태 확인
pnpm outdated 2>/dev/null || echo "의존성 확인 완료"
```

**프로젝트 구조 확인**:
```bash
# 핵심 디렉토리 존재 여부
ls -la backend/ app/ .claude/ tests/ docs/
```

### 2단계: 타입 체크 실행

**Python (mypy)**:
```bash
mypy backend/ --ignore-missing-imports --no-error-summary 2>&1 || true
```

**TypeScript (tsc)**:
```bash
pnpm type-check 2>&1 || echo "TypeScript 타입 체크 완료"
```

### 3단계: 린트 검사 실행

**Python (ruff)**:
```bash
ruff check backend/ --output-format=concise 2>&1 || true
```

**TypeScript/JavaScript (ESLint)**:
```bash
pnpm lint 2>&1 || echo "ESLint 검사 완료"
```

### 4단계: 빌드 테스트

**Python 패키지 빌드**:
```bash
# 패키지 설치 가능 여부 확인 (dry-run)
pip install -e . --dry-run 2>&1 || echo "Python 빌드 확인 완료"
```

**TypeScript 빌드**:
```bash
pnpm build 2>&1 || echo "TypeScript 빌드 완료"
```

### 5단계: 버전 동기화 확인

버전 정보가 일치하는지 확인합니다:

| 파일 | 확인 항목 |
|------|----------|
| `package.json` | `version` 필드 |
| `pyproject.toml` | `version` 필드 |
| `CLAUDE.md` | 헤더의 버전 정보 |
| `docs/INDEX.md` | 버전 표기 (있는 경우) |

```bash
# 버전 추출 및 비교
echo "=== 버전 동기화 확인 ==="
echo "package.json: $(node -p "require('./package.json').version" 2>/dev/null || echo 'N/A')"
echo "pyproject.toml: $(grep -m1 'version = ' pyproject.toml | cut -d'"' -f2)"

# Git 태그 확인
echo "Latest Git tag: $(git describe --tags --abbrev=0 2>/dev/null || echo 'No tags')"
```

### 6단계: 점검 결과 리포트

모든 점검 결과를 요약하여 리포트합니다.

## 점검 항목 상세

### 의존성 점검

| 항목 | 기준 | 상태 |
|------|------|------|
| Python 버전 | >=3.11 | 확인 |
| Node.js 버전 | >=20.0.0 | 확인 |
| pnpm 버전 | >=9.0.0 | 확인 |
| 오래된 패키지 | 10개 미만 권장 | 확인 |

### 타입 체크 기준

| 언어 | 도구 | 기준 |
|------|------|------|
| Python | mypy | 에러 0개 |
| TypeScript | tsc | 에러 0개 |

### 린트 기준

| 언어 | 도구 | 기준 |
|------|------|------|
| Python | ruff | 에러 0개, 경고 최소화 |
| TypeScript | ESLint | 에러 0개 |

### 빌드 기준

| 대상 | 기준 |
|------|------|
| Python 패키지 | 설치 가능 |
| TypeScript | 빌드 성공 |

### 버전 동기화 기준

| 항목 | 기준 |
|------|------|
| package.json ↔ pyproject.toml | 동일 |
| 문서 버전 | 일치 |
| Git 태그 | package.json과 일치 |

## 출력 예시

```
🔍 프로젝트 점검 시작...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 1. 프로젝트 의존성 및 구조 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Python 환경]
  Python: 3.11.5 ✅
  pip packages: 45개 설치됨
  오래된 패키지: 3개

[Node.js 환경]
  Node.js: v20.11.0 ✅
  pnpm: 9.15.4 ✅
  오래된 패키지: 2개

[프로젝트 구조]
  backend/          ✅ 존재
  app/              ✅ 존재
  .claude/          ✅ 존재
  tests/            ✅ 존재
  docs/             ✅ 존재

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔤 2. 타입 체크
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[mypy - Python]
  ✅ Success: no issues found in 42 source files

[tsc - TypeScript]
  ✅ 타입 에러 없음

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 3. 린트 검사
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ruff - Python]
  ✅ All checks passed!
  0 errors, 0 warnings

[ESLint - TypeScript]
  ✅ All checks passed!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔨 4. 빌드 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Python 패키지]
  ✅ 설치 가능 확인됨

[TypeScript 빌드]
  ✅ 빌드 성공

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 5. 버전 동기화 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

package.json:     0.5.0
pyproject.toml:   0.5.0
Git 태그:         v0.5.0

✅ 모든 버전 동기화됨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 점검 결과 요약
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 항목 | 상태 | 비고 |
|------|------|------|
| 의존성/구조 | ✅ | 정상 |
| 타입 체크 | ✅ | 에러 0개 |
| 린트 검사 | ✅ | 에러 0개 |
| 빌드 테스트 | ✅ | 성공 |
| 버전 동기화 | ✅ | 일치 |

🎉 프로젝트 상태: 양호 (5/5 통과)
```

## 문제 발견 시 출력 예시

```
🔍 프로젝트 점검 시작...

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔤 2. 타입 체크
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[mypy - Python]
  ❌ 에러 발견 (3개)

  backend/api/routes/inbox.py:45: error: Argument 1 to "create_signal"
  has incompatible type "str"; expected "SignalCreate"

  backend/agent_runtime/base.py:78: error: Missing return statement

  backend/integrations/confluence.py:112: error: "None" has no attribute "json"

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 5. 버전 동기화 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

package.json:     0.5.0
pyproject.toml:   0.5.0
Git 태그:         v0.4.1

⚠️ 버전 불일치 발견!
   Git 태그가 package.json과 일치하지 않습니다.

💡 해결: git tag -a v0.5.0 -m "v0.5.0 릴리스" && git push origin v0.5.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 점검 결과 요약
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 항목 | 상태 | 비고 |
|------|------|------|
| 의존성/구조 | ✅ | 정상 |
| 타입 체크 | ❌ | 에러 3개 |
| 린트 검사 | ✅ | 에러 0개 |
| 빌드 테스트 | ✅ | 성공 |
| 버전 동기화 | ⚠️ | Git 태그 불일치 |

⚠️ 프로젝트 상태: 점검 필요 (3/5 통과)

📋 권장 조치:
1. mypy 타입 에러 3개 수정
2. Git 태그 v0.5.0 생성 및 푸시
```

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--quick` | 빠른 점검 (타입/린트만) | false |
| `--full` | 전체 점검 (테스트 포함) | false |
| `--fix` | 자동 수정 가능한 항목 수정 | false |
| `--json` | JSON 형식으로 결과 출력 | false |

## 사용법

```
/ax:health-check              # 기본 점검 (5개 항목)
/ax:health-check --quick      # 빠른 점검 (타입/린트만)
/ax:health-check --full       # 전체 점검 (테스트 포함)
/ax:health-check --fix        # 자동 수정 적용 (ruff --fix)
```

## 자동 수정 지원

`--fix` 옵션 사용 시 자동으로 수정 가능한 항목:

| 항목 | 도구 | 명령 |
|------|------|------|
| Python 린트 | ruff | `ruff check --fix backend/` |
| Python 포맷 | ruff | `ruff format backend/` |
| TypeScript 린트 | ESLint | `pnpm lint --fix` |

## 에러 처리

| 에러 | 메시지 | 해결 방법 |
|------|--------|----------|
| Python 미설치 | "Python을 찾을 수 없습니다" | Python 3.11+ 설치 |
| Node.js 미설치 | "Node.js를 찾을 수 없습니다" | Node.js 20+ 설치 |
| 의존성 미설치 | "패키지가 설치되지 않았습니다" | `pip install -e .[dev]` 또는 `pnpm install` |
| 빌드 실패 | "빌드 중 오류 발생" | 에러 메시지 확인 후 수정 |

## 관련 스킬

- `/ax:wrap-up` - 작업 정리 및 커밋
- `/ax:confluence` - Confluence 동기화

## 관련 문서

- [CLAUDE.md](../../../CLAUDE.md) - 프로젝트 개발 문서
- [pyproject.toml](../../../pyproject.toml) - Python 프로젝트 설정
- [package.json](../../../package.json) - Node.js 프로젝트 설정
